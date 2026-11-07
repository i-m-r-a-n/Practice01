"""Top-down plan of part of the floor from an exported GLB: objects above a cut height are removed, an orthographic camera looks
straight down, Workbench draws it with material colours and a cavity outline. Viewer coordinates (x east, z south) are given.
blender -b -P plan_render.py -- GLB OUT.png CX CZ SPAN_M CUT_Y [PX]"""
import bpy, sys, math
argv = sys.argv[sys.argv.index('--') + 1:]
glb, out, cx, cz, span, cut = argv[0], argv[1], float(argv[2]), float(argv[3]), float(argv[4]), float(argv[5])
px = int(argv[6]) if len(argv) > 6 else 1600
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
sc = bpy.context.scene
removed = 0
for o in list(sc.objects):
    if o.type != 'MESH': continue
    zs = [(o.matrix_world @ v.co).z for v in o.data.vertices] if len(o.data.vertices) < 200000 else [o.matrix_world.translation.z]
    if zs and min(zs) > cut: bpy.data.objects.remove(o, do_unlink=True); removed += 1
cam = bpy.data.cameras.new('PLAN'); cam.type = 'ORTHO'; cam.ortho_scale = span
co = bpy.data.objects.new('PLAN', cam); sc.collection.objects.link(co); sc.camera = co
co.location = (cx, -cz, 30.0); co.rotation_euler = (0, 0, 0)   # viewer (x, y, z) -> Blender (x, -z, y); looking down, north (-z viewer = +y Blender) up
sc.render.engine = 'BLENDER_WORKBENCH'
sh = sc.display.shading; sh.light = 'STUDIO'; sh.color_type = 'MATERIAL'; sh.show_cavity = True; sh.cavity_type = 'BOTH'; sh.show_object_outline = True
sc.render.resolution_x = px; sc.render.resolution_y = px; sc.render.filepath = out
bpy.ops.render.render(write_still=True)
print('PLAN', out, 'removed above cut:', removed)
