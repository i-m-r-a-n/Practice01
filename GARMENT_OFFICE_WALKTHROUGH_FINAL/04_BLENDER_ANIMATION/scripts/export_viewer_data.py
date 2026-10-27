"""Writes 03_INTERACTIVE_3D/data/office_tour.json for the browser viewer (run on the approved .blend, read-only):
blender -b Final_Office_Interior.blend --python export_viewer_data.py -- OUT.json
- overhead: objects hidden by the "ceilings off" switch (deck, beams, ceiling elements, light fittings, AC / fire devices)
- solid:    objects the eye-level walk mode collides with (walls, partitions, doors, glazing, columns, stairs)
- rooms:    the 34 zones of the design (name, area, centre) from office_layout.py
- views:    the 33 interior still cameras (cameras.py) as eye-level viewpoints
- tour:     the walkthrough shots (shots.py) as animated camera moves, in the order of the full tour
All positions in glTF metres (x east, y up, z south), the frame of Final_Office_Interior.glb.
"""
import json
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "..", "..", "GARMENT_OFFICE_FINAL_PRESENTATION", "01_EDITABLE_3D", "scripts"))
sys.path.insert(0, HERE)
sys.path.insert(0, SRC)
import cameras as C  # noqa: E402
import office_layout as O  # noqa: E402
import shots as SH  # noqa: E402
import survey as S  # noqa: E402

OUT = os.path.abspath(sys.argv[sys.argv.index("--") + 1])
IN = 0.0254


def g(x, y, z):          # plan inches -> glTF metres
    return [round(x * IN, 3), round(z * IN, 3), round(y * IN, 3)]


def coll_objects(names):
    out = set()
    for c in bpy.data.collections:
        if c.name in names:
            out.update(o.name for o in c.all_objects if o.type in ("MESH", "EMPTY", "CURVE", "FONT"))
    return out


overhead = coll_objects({"Beams", "Ceilings", "Light Fixtures", "MEP_Fire_Safety"})
overhead |= {o.name for o in bpy.data.objects if o.name.startswith("Steel deck")}
solid = coll_objects({"Walls", "Doors_Windows", "Stairs", "Structure"}) - overhead
solid = {n for n in solid if " door (" not in n and not n.startswith("Steel deck")}   # door leaves stay passable in walk mode
def inside(x, y, poly):
    res = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0:
            res = not res
    return res


rooms = []
for coll, zid, label, pts, fin, ceil in O.ZONES:
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    # area-weighted centroid of the polygon
    a = cx = cy = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        cr = x0 * y1 - x1 * y0
        a += cr
        cx += (x0 + x1) * cr
        cy += (y0 + y1) * cr
    a *= 0.5
    c = (cx / (6 * a), cy / (6 * a)) if abs(a) > 1e-6 else (sum(xs) / len(xs), sum(ys) / len(ys))
    name = (label.split("\n")[0].title().replace("Hr ", "HR ").replace("Md ", "MD ").replace("Cad", "CAD").replace("3d", "3D")
            .replace("Pa ", "PA ").replace(" Wc", " WC"))
    view = next((cm["name"] for cm in C.CAMERAS if "pos" in cm and inside(cm["pos"][0], cm["pos"][1], pts)), None)
    rooms.append(dict(id=zid, name=name, group=coll.replace("_", " "), area_sft=round(S.poly_area_sft(pts)),
                      centre=g(c[0], c[1], 96), view=view))
views = []
for cam in C.CAMERAS:
    if "pos" not in cam:
        continue
    views.append(dict(id=cam["name"], room=cam["room"], pos=g(*cam["pos"]), target=g(*cam["target"]), lens=cam.get("lens", 20)))
tour = []
by_name = {s["name"]: s for s in SH.SHOTS}
for name in SH.TOUR_ORDER:
    s = by_name[name]
    if s["kind"] == "dolly":
        tour.append(dict(id=name, scene=s["scene"], label=s["label"], kind="dolly", dur=s["dur"],
                         pos=[g(*s["pos"][0]), g(*s["pos"][1])], target=[g(*s["tgt"][0]), g(*s["tgt"][1])], lens=s["lens"]))
    else:
        tour.append(dict(id=name, scene=s["scene"], label=s["label"] or "The complete ground floor", kind="overview", dur=s["dur"]))
bounds_pts = [(x, y) for x, y in S.OUTLINE]
data = dict(
    note="Generated from the approved model data (office_layout.py, cameras.py) and the walkthrough shot list (shots.py).",
    units="metres, glTF axes (x east, y up, z south)",
    centre=g(sum(p[0] for p in bounds_pts) / len(bounds_pts), sum(p[1] for p in bounds_pts) / len(bounds_pts), 0),
    bounds=[g(min(p[0] for p in bounds_pts), min(p[1] for p in bounds_pts), 0), g(max(p[0] for p in bounds_pts), max(p[1] for p in bounds_pts), S.DECK_H)],
    eye_height=1.6, overhead=sorted(overhead), solid=sorted(solid), rooms=rooms, views=views, tour=tour)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump(data, f, indent=1)
print("VIEWER_DATA", len(overhead), "overhead,", len(solid), "solid,", len(rooms), "rooms,", len(views), "views,", len(tour), "tour steps")
