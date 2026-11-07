"""Blender (5.x) Cycles render of a GLB exported from the proposal page.
blender -b -P render_cycles.py -- GLB CAMERA_NAME OUT.png WIDTH HEIGHT SAMPLES [ORTHO] [MODE] [EMIT]
MODE: 'overview' (sun and sky), 'interior' (lit by the light fittings and a warm daylight fill through the existing glazing) or 'night'
(the fittings only, a dark sky outside the glass). Fittings of the proposal layer that carry their own light (node extras 'light':
SPOT or AREA, watts, kelvin, target in viewer coordinates) become real Blender lights in 'interior' and 'night'; LIGHT_GAIN scales them."""
import bpy, sys, math, mathutils
argv = sys.argv[sys.argv.index('--') + 1:]
glb, cam_name, out, W, H, S = argv[0], argv[1], argv[2], int(argv[3]), int(argv[4]), int(argv[5])
ORTHO = float(argv[6]) if len(argv) > 6 else 0   # ortho_scale of the reference camera (office_web_metadata.json), 0 = perspective
MODE = argv[7] if len(argv) > 7 else 'overview'   # 'interior' / 'night': lit by the light fittings, no sun
INTERIOR = MODE in ('interior', 'night')
EMIT = float(argv[8]) if len(argv) > 8 else 4.0   # interior views: the light fittings' emission is multiplied by this

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
sc = bpy.context.scene
cam = next((o for o in sc.objects if o.type == 'CAMERA' and cam_name in o.name), None) or next(o for o in sc.objects if o.type == 'CAMERA')
sc.camera = cam
import json, os
camjson = os.path.join(os.path.dirname(glb), 'camera_' + cam_name.replace('VIEW_', '') + '.json')
fov = json.load(open(camjson))['fov'] if os.path.exists(camjson) else 35
cam.data.type = 'PERSP'; cam.data.lens_unit = 'FOV'; cam.data.sensor_fit = 'VERTICAL'   # three.js fov is the vertical angle
cam.data.angle_y = math.radians(fov)
ref = json.load(open(camjson)).get('ref', {}) if os.path.exists(camjson) else {}
if ref.get('type') == 'PERSP' and ref.get('lens'):          # the approved Blender camera: lens, sensor and lens shift
    cam.data.sensor_fit = 'AUTO'; cam.data.lens_unit = 'MILLIMETERS'; cam.data.sensor_width = ref.get('sensor_width') or 36; cam.data.lens = ref['lens']
    cam.data.shift_x = ref.get('shift_x') or 0; cam.data.shift_y = ref.get('shift_y') or 0
if ORTHO:
    cam.data.type = 'ORTHO'; cam.data.sensor_fit = 'AUTO'; cam.data.ortho_scale = ORTHO   # three.js: width = ortho_scale when landscape
print('FOV', fov, 'lens', round(cam.data.lens, 2), flush=True)
cam.data.clip_start, cam.data.clip_end = 0.5, 1000

# interior views: only the real light fittings emit; the web view's painted light pools are hidden (Cycles makes real ones)
if INTERIOR:
    import re
    FIX = re.compile(r'^led_|_led$|bulb|lantern_glow|growlight|niche_glow|paper_glow|basket_lamp', re.I)
    SCREEN = re.compile(r'screen|slide|project_board', re.I)
    FAKE = re.compile(r'pool|scallop|daylight_spill|daylight_sky', re.I)
    lit, screens, fake = 0, 0, set()
    for m in bpy.data.materials:
        if not m.use_nodes: continue
        if FAKE.search(m.name): fake.add(m.name); continue
        for n in m.node_tree.nodes:
            if n.type != 'BSDF_PRINCIPLED': continue
            s = n.inputs['Emission Strength'].default_value
            if FIX.search(m.name): n.inputs['Emission Strength'].default_value = max(s, 1.0) * EMIT; lit += 1
            elif SCREEN.search(m.name): screens += 1                       # screens keep their own glow
            else: n.inputs['Emission Strength'].default_value = 0.0        # self-lit helpers of the web view
    hidden = 0
    for o in bpy.data.objects:
        if o.type == 'MESH' and any(s.material and s.material.name in fake for s in o.material_slots): o.hide_render = True; hidden += 1
    print('FIXTURES', lit, 'SCREENS', screens, 'FAKE_POOLS_HIDDEN', hidden, flush=True)
    # the proposal layer's spots and wall-washers: a real light at the lens, aimed at the fitting's target (viewer x, y, z -> Blender x, -z, y)
    KELVIN = {2700: (1.0, .74, .50), 3000: (1.0, .79, .58), 3500: (1.0, .85, .69), 4000: (1.0, .89, .78)}
    V = lambda q: mathutils.Vector((q[0], -q[2], q[1]))
    gain, made = float(os.environ.get('LIGHT_GAIN', '1')), 0
    for o in list(sc.objects):
        L = o.get('light')
        if L is None: continue
        L = L.to_dict() if hasattr(L, 'to_dict') else dict(L)
        kind = str(L.get('type', 'SPOT')).upper(); loc = o.matrix_world.translation.copy(); d = (V(L['target']) - loc).normalized()
        ld = bpy.data.lights.new('FIT_' + o.name, 'SPOT' if kind == 'SPOT' else 'AREA')
        ld.energy = float(L.get('watts', 10)) * gain; ld.color = KELVIN[min(KELVIN, key=lambda t: abs(t - int(L.get('kelvin', 3000))))]
        Z = -d
        if kind == 'SPOT':
            ld.spot_size = math.radians(float(L.get('deg', 25))); ld.spot_blend = float(L.get('blend', .4)); ld.shadow_soft_size = .015
            X = Z.orthogonal().normalized()
        else:
            w, hh = L.get('size', [1.0, .05]); ld.shape = 'RECTANGLE'; ld.size = float(w); ld.size_y = float(hh)
            lg = V(L.get('long', [0, 0, 1])); X = (lg - d * lg.dot(d)).normalized()
        Y = Z.cross(X); lo = bpy.data.objects.new('FIT_' + o.name, ld); sc.collection.objects.link(lo)
        lo.matrix_world = mathutils.Matrix.Translation(loc + d * .012) @ mathutils.Matrix((X, Y, Z)).transposed().to_4x4(); made += 1
    print('FITTING_LIGHTS', made, 'gain', gain, flush=True)
# a ground under the slab, to take the model's shadow
zs = [ (o.matrix_world @ mathutils.Vector(c)).z for o in sc.objects if o.type == 'MESH' for c in o.bound_box ]
zmin = min(zs) if zs else 0
bpy.ops.mesh.primitive_plane_add(size=600, location=(0, 0, zmin - 0.002))
g = bpy.context.active_object; g.name = 'GROUND'
gm = bpy.data.materials.new('ground'); gm.use_nodes = True
bsdf = gm.node_tree.nodes['Principled BSDF']; bsdf.inputs['Base Color'].default_value = (0.62, 0.60, 0.57, 1); bsdf.inputs['Roughness'].default_value = 0.85
g.data.materials.append(gm)

# light: a soft warm sun from the camera's left plus a pale sky fill
world = bpy.data.worlds.new('W'); sc.world = world; world.use_nodes = True
bg = world.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (0.80, 0.80, 0.78, 1); bg.inputs['Strength'].default_value = 0.9
if MODE == 'interior': bg.inputs['Strength'].default_value = 0.55; bg.inputs['Color'].default_value = (0.95, 0.88, 0.78, 1)   # a warm, soft fill like light bouncing off white walls
if MODE == 'night': bg.inputs['Strength'].default_value = 0.05; bg.inputs['Color'].default_value = (0.32, 0.38, 0.55, 1)      # a dark sky beyond the glass: the fittings light the room
sun = bpy.data.lights.new('SUN', 'SUN'); sun.energy = 0.0 if INTERIOR else 3.2; sun.angle = math.radians(6); sun.color = (1.0, 0.95, 0.88)
so = bpy.data.objects.new('SUN', sun); sc.collection.objects.link(so)
so.rotation_euler = (math.radians(38), math.radians(-14), math.radians(-35))

sc.render.engine = 'CYCLES'
cy = sc.cycles; cy.device = 'CPU'; cy.samples = S; cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.02
cy.use_denoising = True
try: cy.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
cy.max_bounces = 6; cy.diffuse_bounces = 3; cy.glossy_bounces = 3; cy.transmission_bounces = 6; cy.transparent_max_bounces = 12
sc.render.threads_mode = 'FIXED'; sc.render.threads = 4
sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = W, H, 100
sc.render.film_transparent = False
try:
    sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
    if MODE == 'interior': sc.view_settings.exposure = 0.45
    if MODE == 'night': sc.view_settings.exposure = float(os.environ.get('NIGHT_EXPOSURE', '0.9'))
except Exception: pass
sc.render.image_settings.file_format = 'PNG'
sc.render.filepath = out
n_mesh = sum(1 for o in sc.objects if o.type == 'MESH'); n_mat = len(bpy.data.materials)
print('RENDER', cam.name, 'meshes', n_mesh, 'materials', n_mat, 'zmin', round(zmin, 3), flush=True)
bpy.ops.render.render(write_still=True)
print('DONE', out, flush=True)
