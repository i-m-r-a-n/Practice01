"""Blender (5.x) Cycles render of a GLB exported from the proposal page.
blender -b -P render_cycles.py -- GLB CAMERA_NAME OUT.png WIDTH HEIGHT SAMPLES"""
import bpy, sys, math, mathutils
argv = sys.argv[sys.argv.index('--') + 1:]
glb, cam_name, out, W, H, S = argv[0], argv[1], argv[2], int(argv[3]), int(argv[4]), int(argv[5])
ORTHO = float(argv[6]) if len(argv) > 6 else 0   # ortho_scale of the reference camera (office_web_metadata.json), 0 = perspective

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
if ORTHO:
    cam.data.type = 'ORTHO'; cam.data.sensor_fit = 'AUTO'; cam.data.ortho_scale = ORTHO   # three.js: width = ortho_scale when landscape
print('FOV', fov, 'lens', round(cam.data.lens, 2), flush=True)
cam.data.clip_start, cam.data.clip_end = 0.5, 1000

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
sun = bpy.data.lights.new('SUN', 'SUN'); sun.energy = 3.2; sun.angle = math.radians(6); sun.color = (1.0, 0.95, 0.88)
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
except Exception: pass
sc.render.image_settings.file_format = 'PNG'
sc.render.filepath = out
n_mesh = sum(1 for o in sc.objects if o.type == 'MESH'); n_mat = len(bpy.data.materials)
print('RENDER', cam.name, 'meshes', n_mesh, 'materials', n_mat, 'zmin', round(zmin, 3), flush=True)
bpy.ops.render.render(write_still=True)
print('DONE', out, flush=True)
