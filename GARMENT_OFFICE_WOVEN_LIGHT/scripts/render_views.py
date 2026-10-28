"""Render named cameras of a .blend: blender -b X.blend --python render_views.py -- OUTDIR SAMPLES SCALE CAM [CAM ...]
Skips a camera whose PNG already exists (resumable)."""
import bpy, sys, os, time
a = sys.argv[sys.argv.index('--') + 1:]
out, samples, scale, cams = a[0], int(a[1]), int(a[2]), a[3:]
os.makedirs(out, exist_ok=True)
sc = bpy.context.scene
sc.cycles.samples = samples
sc.render.resolution_percentage = scale
sc.render.image_settings.file_format = 'PNG'
for c in cams:
    f = os.path.join(out, c + '.png')
    if os.path.exists(f): print('SKIP', c); continue
    sc.camera = bpy.data.objects[c]
    t = time.time(); sc.render.filepath = f + '.tmp.png'
    bpy.ops.render.render(write_still=True)
    os.replace(f + '.tmp.png', f)
    print('DONE', c, round(time.time() - t), 's', flush=True)
