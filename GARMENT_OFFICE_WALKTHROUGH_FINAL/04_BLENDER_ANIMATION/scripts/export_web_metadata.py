"""Exports the data a web viewer needs from the approved model (read-only; the .blend is not saved):
blender -b Final_Office_Interior.blend --python export_web_metadata.py -- OUT_DIR
- OUT_DIR/blender_cameras.json   the 38 render cameras: exact world matrices from the .blend (position, view direction, up,
                                 quaternion) in glTF axes, lens / sensor / shift / ortho scale
- OUT_DIR/blender_rooms.json     the 34 zones: id, name, group, area, floor polygon (glTF x/z), cameras inside the zone
- OUT_DIR/blender_names.json     object names: overhead (ceilings off), walls / glazing / doors, door leaves
- OUT_DIR/collision_tris.npy     world triangles of every render-visible object between 0.10 m and 1.90 m above the floor
                                 (overhead objects and door leaves excluded) for the walk-mode floor map
Axes: Blender (x east, y north, z up) -> glTF (x, z, -y) = (x east, y up, z south).
"""
import json
import os
import sys

import bpy
import numpy as np
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "..", "..", "GARMENT_OFFICE_FINAL_PRESENTATION", "01_EDITABLE_3D", "scripts"))
sys.path.insert(0, SRC)
import cameras as CAMS  # noqa: E402
import office_layout as O  # noqa: E402
import survey as S  # noqa: E402

OUT = os.path.abspath(sys.argv[sys.argv.index("--") + 1])
os.makedirs(OUT, exist_ok=True)
IN = 0.0254
M = Matrix(((1, 0, 0), (0, 0, 1), (0, -1, 0)))          # Blender world -> glTF world


def gv(v):
    w = M @ Vector(v)
    return [round(w.x, 5), round(w.y, 5), round(w.z, 5)]


def coll_objects(names):
    out = set()
    for c in bpy.data.collections:
        if c.name in names:
            out.update(o.name for o in c.all_objects)
    return out


scene = bpy.context.scene
# ------------------------------------------------------------------ cameras (exact matrices)
cams = []
spec = {c["name"]: c for c in CAMS.CAMERAS}
for ob in sorted((o for o in bpy.data.objects if o.type == "CAMERA" and o.name.startswith("CAM_")), key=lambda o: o.name):
    mw = ob.matrix_world
    r3 = mw.to_3x3().normalized()
    d = r3 @ Vector((0, 0, -1))
    u = r3 @ Vector((0, 1, 0))
    dg, ug = M @ d, M @ u
    back, right = -dg, ug.cross(-dg)
    rot = Matrix((right, ug, back)).transposed()       # columns: local x, y, z in glTF world
    q = rot.to_quaternion()
    cd = ob.data
    c = dict(name=ob.name, room=spec.get(ob.name, {}).get("room", ""), priority=int(spec.get(ob.name, {}).get("priority", 2)),
             type=cd.type, position=gv(mw.translation), direction=[round(x, 6) for x in dg], up=[round(x, 6) for x in ug],
             quaternion_xyzw=[round(q.x, 6), round(q.y, 6), round(q.z, 6), round(q.w, 6)],
             clip=[cd.clip_start, cd.clip_end], shift_x=round(cd.shift_x, 6), shift_y=round(cd.shift_y, 6), sensor_fit=cd.sensor_fit)
    if cd.type == "ORTHO":
        c["ortho_scale"] = round(cd.ortho_scale, 4)
    else:
        c.update(lens=cd.lens, sensor_width=cd.sensor_width)
    cams.append(c)
json.dump(cams, open(os.path.join(OUT, "blender_cameras.json"), "w"), indent=1)

# ------------------------------------------------------------------ rooms
def inside(x, y, poly):
    res = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0:
            res = not res
    return res


rooms = []
for coll, zid, label, pts, fin, ceil in O.ZONES:
    a = cx = cy = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        cr = x0 * y1 - x1 * y0
        a += cr
        cx += (x0 + x1) * cr
        cy += (y0 + y1) * cr
    a *= 0.5
    c = (cx / (6 * a), cy / (6 * a))
    rooms.append(dict(zone=zid, label=label.replace("\n", " "), group=coll, area_sft=round(S.poly_area_sft(pts)),
                      area_m2=round(S.poly_area_sft(pts) * 0.09290304, 1),
                      polygon_xz=[[round(x * IN, 4), round(y * IN, 4)] for x, y in pts],
                      centroid_xz=[round(c[0] * IN, 4), round(c[1] * IN, 4)],
                      cameras=[cm["name"] for cm in CAMS.CAMERAS if "pos" in cm and inside(cm["pos"][0], cm["pos"][1], pts)],
                      floor_finish=str(fin), ceiling=str(ceil)))
json.dump(rooms, open(os.path.join(OUT, "blender_rooms.json"), "w"), indent=1)

# ------------------------------------------------------------------ object name sets
overhead = coll_objects({"Beams", "Ceilings", "Light Fixtures", "MEP_Fire_Safety"}) | {o.name for o in bpy.data.objects if o.name.startswith("Steel deck")}
shell = coll_objects({"Walls", "Doors_Windows", "Stairs", "Structure"}) - overhead
door_leaves = sorted(n for n in shell if " door (" in n)
names = dict(overhead=sorted(n for n in overhead if bpy.data.objects[n].type == "MESH"),
             walls_glazing_doors_structure=sorted(n for n in shell if bpy.data.objects[n].type == "MESH" and n not in door_leaves),
             door_leaves=door_leaves,
             collections={c.name: len([o for o in c.all_objects if o.type == "MESH"]) for c in bpy.data.collections})
json.dump(names, open(os.path.join(OUT, "blender_names.json"), "w"), indent=1)

# ------------------------------------------------------------------ collision triangles (0.10 .. 1.90 m)
dg = bpy.context.evaluated_depsgraph_get()
skip = overhead | set(door_leaves)
chunks = []
for ob in bpy.data.objects:
    if ob.type != "MESH" or ob.hide_render or ob.name in skip or not ob.visible_get():
        continue
    ev = ob.evaluated_get(dg)
    me = ev.to_mesh()
    me.calc_loop_triangles()
    nv, nt = len(me.vertices), len(me.loop_triangles)
    if nt:
        co = np.empty(nv * 3, np.float32)
        me.vertices.foreach_get("co", co)
        tri = np.empty(nt * 3, np.int32)
        me.loop_triangles.foreach_get("vertices", tri)
        mw = np.array(ob.matrix_world, np.float32)
        co = co.reshape(-1, 3) @ mw[:3, :3].T + mw[:3, 3]
        t = co[tri.reshape(-1, 3)]
        z = t[:, :, 2]
        keep = (z.min(1) < 1.90) & (z.max(1) > 0.10)
        if keep.any():
            chunks.append(t[keep])
    ev.to_mesh_clear()
tris = np.concatenate(chunks) if chunks else np.zeros((0, 3, 3), np.float32)
np.save(os.path.join(OUT, "collision_tris.npy"), tris)
print("WEB_METADATA cameras", len(cams), "rooms", len(rooms), "overhead", len(names["overhead"]), "collision tris", len(tris))
