"""Quick Workbench previews (textures, studio light) of an exported GLB from several viewpoints, to study a space.
Views are given in viewer coordinates (x east, y up, z south): name:px,py,pz:tx,ty,tz:lens_mm
blender -b -P preview_views.py -- GLB OUTDIR W H VIEW [VIEW ...]"""
import bpy, sys, os, mathutils
argv = sys.argv[sys.argv.index('--') + 1:]
glb, outdir, W, H = argv[0], argv[1], int(argv[2]), int(argv[3])
views = argv[4:]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
sc = bpy.context.scene
sc.render.engine = 'BLENDER_WORKBENCH'
sh = sc.display.shading; sh.light = 'STUDIO'; sh.color_type = 'TEXTURE'; sh.show_cavity = True; sh.cavity_type = 'WORLD'; sh.show_shadows = True
sc.render.resolution_x, sc.render.resolution_y = W, H
cam = bpy.data.cameras.new('PREV'); cam.sensor_width = 36; cam.sensor_fit = 'AUTO'
co = bpy.data.objects.new('PREV', cam); sc.collection.objects.link(co); sc.camera = co
b = lambda x, y, z: mathutils.Vector((x, -z, y))   # viewer -> Blender
for v in views:
    name, p, t, lens = v.split(':')
    p = [float(s) for s in p.split(',')]; t = [float(s) for s in t.split(',')]
    cam.lens = float(lens); co.location = b(*p)
    d = b(*t) - b(*p); co.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    sc.render.filepath = os.path.join(outdir, f'prev_{name}.png'); bpy.ops.render.render(write_still=True)
    print('VIEW', name, 'done')
