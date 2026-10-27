"""Bakes the Cycles lighting of the approved scene onto the building shell and exports a GLB for the web tour.
Runs on the approved .blend but never saves it (the bake lives only in the exported GLB).
blender -b Final_Office_Interior.blend --python bake_shell_lighting.py -- OUT.glb [--samples 64] [--edge 0.4] [--scale 16] [--limit N]

Shell = floor finishes, walls and partitions, wall finishes, ceilings / rafts / baffles, steel deck, beams, columns.
Each shell object is made single-user, its modifiers applied (door openings), triangulated and split until no edge is longer
than --edge metres; the objects are joined into WEB_SHELL_INTERIOR and WEB_SHELL_OVERHEAD (ceilings, beams, deck) and Cycles
bakes DIFFUSE light (direct + indirect, no surface colour) to a per-vertex colour attribute.
The value stored is light / --scale (so it fits 0..1); the viewer multiplies the base colour by colour x scale x exposure.
Furniture, glazing and light fittings are not baked (they stay lit in real time); they still cast their shadows on the shell.
"""
import math
import sys
import time

import bmesh
import bpy
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:]
OUT = argv[0]


def opt(k, d):
    return type(d)(argv[argv.index(k) + 1]) if k in argv else d


SAMPLES, EDGE, K, LIMIT, AREA = opt("--samples", 64), opt("--edge", 0.4), opt("--scale", 16.0), opt("--limit", 0), opt("--area", 0.3)
SHELL = {"Walls", "Wall Finishes", "Ceilings", "Beams", "Structure", "Existing Walls", "Existing Partitions", "New Partitions", "Columns"}
NOT_BAKED = ("glass", "led_", "lightbox", "screen_", "mirror", "modern_ceiling_lamp", "modern_ceiling_globe")


def in_shell(o):
    if o.type != "MESH" or o.hide_render:
        return False
    if " - floor finish" in o.name or o.name.startswith("Steel deck"):
        return True
    return any(c.name in SHELL for c in o.users_collection)


def bakeable(o):
    mats = [s.material for s in o.material_slots if s.material]
    return bool(mats) and not all(any(m.name.startswith(p) or p in m.name for p in NOT_BAKED) for m in mats)


t0 = time.time()
targets = [o for o in bpy.data.objects if in_shell(o) and bakeable(o)]
if LIMIT:
    targets = targets[:LIMIT]
for o in targets:
    o.hide_set(False)
    o.hide_viewport = False
    if o.data.users > 1:
        o.data = o.data.copy()

# apply modifiers (boolean door openings) on the copies
bpy.ops.object.select_all(action="DESELECT")
for o in targets:
    o.select_set(True)
bpy.context.view_layer.objects.active = targets[0]
bpy.ops.object.convert(target="MESH")

# split long edges so the light varies across large floors and walls
tris = 0
for o in targets:
    bm = bmesh.new()
    bm.from_mesh(o.data)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    s = max(o.matrix_world.to_scale())
    for _ in range(9):                                 # only edges of large faces: slats, trims and thin parts keep their mesh
        long_edges = [e for e in bm.edges if e.calc_length() * s > EDGE and any(f.calc_area() * s * s > AREA for f in e.link_faces)]
        if not long_edges:
            break
        bmesh.ops.subdivide_edges(bm, edges=long_edges, cuts=1, use_grid_fill=True)
        bmesh.ops.triangulate(bm, faces=[f for f in bm.faces if len(f.verts) > 3])
    bm.to_mesh(o.data)
    tris += len(bm.faces)
    bm.free()

# join into two objects (Cycles bakes object by object with a full scene sync each: 600 objects would take hours)
OVERHEAD_COLLS = {"Beams", "Ceilings", "Light Fixtures", "MEP_Fire_Safety"}
groups = {"WEB_SHELL_OVERHEAD": [], "WEB_SHELL_INTERIOR": []}
for o in targets:
    over = o.name.startswith("Steel deck") or any(c.name in OVERHEAD_COLLS for c in o.users_collection)
    groups["WEB_SHELL_OVERHEAD" if over else "WEB_SHELL_INTERIOR"].append(o)
targets = []
for name, objs in groups.items():
    if not objs:
        continue
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    bpy.ops.object.join()
    j = bpy.context.view_layer.objects.active
    j.name = j.data.name = name
    ca = j.data.color_attributes.new("BakedLight", "FLOAT_COLOR", "POINT")     # one sample per vertex: ~6x faster than per corner
    j.data.color_attributes.active_color = ca
    j.data.color_attributes.render_color_index = list(j.data.color_attributes).index(ca)
    targets.append(j)
print(f"BAKE_PREP {sum(len(v) for v in groups.values())} objects joined into {len(targets)}, {tris} triangles, "
      f"{sum(len(t.data.vertices) for t in targets)} vertices, {time.time() - t0:.0f} s", flush=True)

sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = SAMPLES
sc.render.bake.target = "VERTEX_COLORS"
sc.render.bake.use_pass_direct = True
sc.render.bake.use_pass_indirect = True
sc.render.bake.use_pass_color = False
bpy.ops.object.select_all(action="DESELECT")
for o in targets:
    o.select_set(True)
bpy.context.view_layer.objects.active = targets[0]
t1 = time.time()
bpy.ops.object.bake(type="DIFFUSE", pass_filter={"DIRECT", "INDIRECT"}, target="VERTEX_COLORS")
print(f"BAKE_DONE {time.time() - t1:.0f} s at {SAMPLES} samples", flush=True)

peak = 0.0
for o in targets:
    ca = o.data.color_attributes["BakedLight"]
    a = np.empty(len(ca.data) * 4, np.float32)
    ca.data.foreach_get("color", a)
    a = a.reshape(-1, 4)
    peak = max(peak, float(np.percentile(a[:, :3], 99.5)) if len(a) else 0.0)
    a[:, :3] = np.clip(a[:, :3] / K, 0.0, 1.0)
    a[:, 3] = 1.0
    ca.data.foreach_set("color", a.ravel())
    o["baked_light_scale"] = K
print(f"BAKE_PEAK 99.5th percentile light {peak:.2f} (stored / {K})", flush=True)

bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", use_renderable=True, export_apply=True, export_extras=True,
                          export_cameras=True, export_lights=False, export_yup=True, export_image_format="JPEG",
                          export_jpeg_quality=85, export_vertex_color="ACTIVE", export_all_vertex_colors=False,
                          export_active_vertex_color_when_no_material=False)
print(f"BAKE_EXPORTED {OUT} total {time.time() - t0:.0f} s", flush=True)
