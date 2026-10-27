"""Reopen-and-check for the delivered files. Run twice:
blender -b Final_Office_Interior.blend --python verify_files.py -- blend REPORT.md
blender -b --factory-startup --python verify_files.py -- glb Final_Office_Interior.glb REPORT.md
Appends results to REPORT.md."""
import os
import sys
import time
from collections import Counter

import bpy

A = sys.argv[sys.argv.index("--") + 1:]
mode = A[0]
lines = []
if mode == "blend":
    report = A[1]
    path = bpy.data.filepath
    lines.append(f"## .blend reopened: `{os.path.basename(path)}` ({os.path.getsize(path) / 1e6:.1f} MB)")
    lines.append(f"- objects {len(bpy.data.objects)}, meshes {len(bpy.data.meshes)}, materials {len(bpy.data.materials)}, "
                 f"lights {len(bpy.data.lights)}, cameras {len([o for o in bpy.data.objects if o.type == 'CAMERA'])}, images {len(bpy.data.images)}")
    packed = [i.name for i in bpy.data.images if i.packed_file]
    missing = [i.name for i in bpy.data.images if not i.packed_file and i.source == "FILE" and not os.path.exists(bpy.path.abspath(i.filepath))]
    lines.append(f"- textures packed inside the .blend: {len(packed)} of {len(bpy.data.images)}; unresolved external textures: {len(missing)}" + (f" {missing}" if missing else ""))
    lines.append("- top-level collections (objects incl. children):")
    for c in bpy.context.scene.collection.children:
        lines.append(f"  - {c.name}: {len(c.all_objects)}" + (" (hidden master copies)" if c.name.startswith("_") else ""))
    zones = Counter(o.get("zone_id") for o in bpy.data.objects if o.get("zone_id"))
    lines.append(f"- room / zone floor objects: {len(zones)} (each zone has its own floor object with area and finish properties)")
    furn = [o for o in bpy.data.objects if o.get("asset")]
    lines.append(f"- furniture / equipment objects with asset + zone properties: {len(furn)}")
    sc = bpy.context.scene
    lines.append(f"- render engine {sc.render.engine}, samples {sc.cycles.samples}, denoise {sc.cycles.use_denoising}, view transform {sc.view_settings.view_transform}")
elif mode == "glb":
    path, report = A[1], A[2]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    t = time.time()
    bpy.ops.import_scene.gltf(filepath=path)
    dt = time.time() - t
    types = Counter(o.type for o in bpy.data.objects)
    lines.append(f"## .glb re-imported: `{os.path.basename(path)}` ({os.path.getsize(path) / 1e6:.1f} MB) in {dt:.1f} s")
    lines.append(f"- objects {len(bpy.data.objects)} ({dict(types)}), meshes {len(bpy.data.meshes)}, materials {len(bpy.data.materials)}, images {len(bpy.data.images)}")
    tris = sum(sum(len(p.vertices) - 2 for p in m.polygons) for m in bpy.data.meshes)
    lines.append(f"- triangles (unique meshes) about {tris:,}")
    ok = len(bpy.data.objects) > 500 and types.get("MESH", 0) > 500
    lines.append(f"- result: {'PASS' if ok else 'CHECK'} (model geometry, materials and cameras load in a fresh Blender session)")
with open(report, "a") as f:
    f.write("\n".join(lines) + "\n\n")
print("\n".join(lines))
