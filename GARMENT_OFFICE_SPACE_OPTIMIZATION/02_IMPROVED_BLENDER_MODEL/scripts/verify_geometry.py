"""Checkpoint A - measure the built Blender model and compare with the survey values (from the client's
hand-measured sketches, reconciled in survey.SCHEDULE).

blender -b Final_Office_Interior.blend --python verify_geometry.py -- REPORT_DIR
Writes geometry_verification.csv and geometry_verification.md. Every number is measured from the evaluated
objects in the .blend (modifiers applied), converted from metres to inches.
"""
import csv
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import survey as S  # noqa: E402

OUT = os.path.abspath(sys.argv[sys.argv.index("--") + 1]) if "--" in sys.argv else os.getcwd()
os.makedirs(OUT, exist_ok=True)
IN = 0.0254
dg = bpy.context.evaluated_depsgraph_get()


def bounds(ob):
    """World bounding box of the evaluated object in plan inches: (x0, x1, y0, y1, z0, z1), plan y = -Blender y."""
    ev = ob.evaluated_get(dg)
    pts = [ev.matrix_world @ Vector(c) for c in ev.bound_box]
    xs, ys, zs = [p.x / IN for p in pts], [-p.y / IN for p in pts], [p.z / IN for p in pts]
    return min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)


def find(prefix):
    for ob in bpy.data.objects:
        if ob.name.startswith(prefix + " "):
            return ob
    raise KeyError(prefix)


rows = []


def check(item, group, expected, measured, source, tol=0.05, note=""):
    diff = measured - expected
    ok = abs(diff) <= tol
    rows.append([item, group, round(expected, 2), round(measured, 2), round(diff, 2), "PASS" if ok else "CHECK", source, note])


W = {wid: bounds(find(wid)) for wid in [w["id"] for w in S.WALLS]}
sched = {r[0]: r for r in S.SCHEDULE}


def val(k):
    return sched[k][4]


def src(k):
    r = sched[k]
    return f'{r[6]}: "{r[3]}" ({r[7]})'


# ---------------------------------------------------------------- overall
check("Front width, outside faces (EW02 outer - EW03 outer)", "Overall", val("OV01"), W["EW03"][1] - W["EW02"][0], src("OV01"))
check("Depth west side (front facade outer - middle block north outer)", "Overall", val("OV02"), W["EW01"][3] - W["EW05"][2], src("OV02"))
check("Depth east side (front facade outer - room 8 north outer)", "Overall", val("OV03"), W["EW01"][3] - W["EW09"][2], src("OV03"))
# ---------------------------------------------------------------- rooms (clear, between wall faces)
check("Room 1 width", "Rooms", val("R1W"), W["IW04"][0] - W["EW02"][1], src("R1W"))
check("Room 1 depth", "Rooms", val("R1D"), W["EW01"][2] - W["IW01"][3], src("R1D"))
check("Room 2 width", "Rooms", val("R2W"), W["IW07"][0] - W["EW07"][1], src("R2W"))
check("Room 2 depth", "Rooms", val("R2D"), W["IW01"][2] - W["IW06"][3], src("R2D"))
check("Room 3 width", "Rooms", val("R3W"), W["IW05"][0] - W["IW04"][1], src("R3W"))
check("Room 3 depth", "Rooms", val("R3D"), W["EW01"][2] - W["IW02"][3], src("R3D"))
check("Room 4 width", "Rooms", val("R4W"), W["EW03"][0] - W["IW05"][1], src("R4W"))
check("Room 4 depth", "Rooms", val("R4D"), W["EW01"][2] - W["IW03"][3], src("R4D"))
check("Room 5 width", "Rooms", val("R5W"), W["IW09"][0] - W["PW05"][1], src("R5W"))
check("Room 5 depth", "Rooms", val("R5D"), W["PW01"][2] - W["PW07"][3], src("R5D"))
check("Room 6 width", "Rooms", val("R6W"), W["IW09"][0] - W["PW05"][1], src("R6W"))
check("Room 6 depth", "Rooms", val("R6D"), W["PW07"][2] - W["PW06"][3], src("R6D"))
check("Room 7 lower width (room 2 wall - low wall)", "Rooms", val("R7WL"), W["PW05"][0] - W["IW07"][1], src("R7WL"))
check("Room 7 upper width", "Rooms", val("R7WU"), W["PW05"][0] - W["IW08"][1], src("R7WU"))
check("Room 7 jog at washroom row", "Rooms", val("R7J"), W["IW07"][1] - W["IW08"][1], src("R7J"))
check("Room 7 lower west wall length", "Rooms", val("R7WW"), W["IW07"][3] - W["IW07"][2], src("R7WW"))
check("Middle block depth (north wall inner - row wall)", "Rooms", val("R7D"), W["IW01"][2] - W["EW05"][3], src("R7D"))
check("Hallway width", "Rooms", val("HALW"), W["PW06"][2] - W["EW05"][3], src("HALW"))
check("Hallway length", "Rooms", val("HALL"), W["IW09"][0] - W["PW05"][0], src("HALL"))
check("Washroom row length", "Rooms", val("STL"), W["IW08"][3] - W["IW08"][2], src("STL"))
check("Room 8 width (ASSUMED)", "Rooms", val("R8W"), W["EW10"][0] - W["IW09"][1], src("R8W"), note="not measured on site")
check("Room 8 length", "Rooms", val("R8L"), W["IW03"][2] - W["EW09"][3], src("R8L"))
check("Room 8 west wall, north corner to hallway door", "Rooms", val("R8WN"), (S.MID_N + (48 - S.HALL_DOOR) / 2) - W["EW09"][3], src("R8WN"),
      tol=4, note="door position uses the standard 42 in door centred in the 48 in hallway (door width not written)")
check("North-east stair width", "Rooms", val("NESW"), W["EW10"][0] - W["IW11"][1], src("NESW"))
check("Engine room (sub-station) width", "Rooms", val("ENGW"), W["EW10"][0] - W["IW13"][1], src("ENGW"))
check("Engine room depth", "Rooms", val("ENGD"), W["IW14"][2] - W["IW12"][3], src("ENGD"))
check("South-east stair width", "Rooms", val("SESW"), W["EW10"][0] - W["IW15"][1], src("SESW"))
check("South-east stair depth", "Rooms", val("SESD"), W["IW03"][2] - W["IW14"][3], src("SESD"))
# ---------------------------------------------------------------- heights
for wid in ("PW01", "PW05", "PW06", "PW07"):
    check(f"{wid} low wall height", "Heights", val("WH1"), W[wid][5] - W[wid][4], src("WH1"))
check("Floor to underside of deck (PHOTO-EST)", "Heights", val("H01"), bounds(find("Steel deck"))[4], src("H01"), note="estimate - verify on site")
# ---------------------------------------------------------------- openings (cutter widths / heights)
expect = {"D01": 140, "D02": 42, "D04": 47, "D05": 60, "D06": 26.5, "D08": 30, "D09": 30, "D10": 48, "D11": 52, "D12": 49,
          "D13": 42, "D14": 49, "D15": 49, "D16": 52, "W01": 114, "W02": 113, "W03": 113, "W04": 113, "W05": 114, "W06": 60,
          "W07": 71, "W08": 114, "W09": 114, "W10": 114}
heights = {"W01": 48, "W02": 54, "W03": 54, "W04": 54, "W05": 37, "W06": 46, "W07": 54, "W08": 54, "W09": 54, "W10": 54}
for ob in bpy.data.objects:
    oid = ob.get("opening_id")
    if not oid or oid not in expect or ob.display_type != "WIRE":
        continue
    b = bounds(ob)
    w = max(b[1] - b[0], b[3] - b[2]) if (b[1] - b[0]) > 30 or (b[3] - b[2]) > 30 else min(b[1] - b[0], b[3] - b[2])
    span = (b[1] - b[0]) if (b[1] - b[0]) > (b[3] - b[2]) else (b[3] - b[2])
    check(f"{oid} opening width", "Openings", expect[oid], span, "Survey sketches (see dimension_schedule.csv)",
          note="D13 width STANDARD (not written)" if oid == "D13" else "")
    if oid in heights:
        check(f"{oid} window height", "Openings", heights[oid], b[5] - b[4], "Survey sketches (window heights)")
# ---------------------------------------------------------------- structure + stairs
cols = [o for o in bpy.data.objects if o.name.startswith("COL")]
check("Steel columns modelled (PHOTO-EST positions)", "Structure", 11, len(cols), "Site photos", tol=0)
beams = [o for o in bpy.data.objects if o.name.startswith("BM")]
check("Beams modelled (PHOTO-EST layout)", "Structure", len(S.beam_list()), len(beams), "Site photos", tol=0)
fl = [o for o in bpy.data.objects if o.name.startswith("ST1 room 1 stair, flight")]
landing = find("ST1 room 1 stair, landing")
n = round(S.FLOOR_TO_FLOOR / 7)
check("Room 1 stair: landing top = risers x rise", "Stairs", (n // 2 + 1) * S.FLOOR_TO_FLOOR / n, bounds(landing)[5], "risers ASSUMED (floor-to-floor estimated)")
check("Room 1 stair footprint width", "Stairs", val("ST1"), bounds(landing)[1] - 0, src("ST1"), tol=2.5, note="stair spans x 2..158 inside the 160 in zone")
# ---------------------------------------------------------------- evaluated mesh sanity (booleans)
bad = []
for ob in bpy.data.objects:
    if ob.type == "MESH" and any(m.type == "BOOLEAN" for m in ob.modifiers):
        ev = ob.evaluated_get(dg)
        me = ev.to_mesh()
        if len(me.polygons) < 6:
            bad.append(ob.name)
        ev.to_mesh_clear()
rows.append(["Walls with boolean openings evaluate to valid meshes", "Mesh check", "", "", "", "PASS" if not bad else "CHECK",
             "Blender evaluated meshes", "; ".join(bad) or f"{sum(1 for o in bpy.data.objects if o.type == 'MESH' and any(m.type == 'BOOLEAN' for m in o.modifiers))} objects checked"])

with open(os.path.join(OUT, "geometry_verification.csv"), "w", newline="") as f:
    wr = csv.writer(f)
    wr.writerow(["item", "group", "expected_in", "measured_in_model", "difference_in", "result", "source", "note"])
    wr.writerows(rows)
npass = sum(1 for r in rows if r[5] == "PASS")
with open(os.path.join(OUT, "geometry_verification.md"), "w") as f:
    f.write("# Geometry verification (checkpoint A)\n\n")
    f.write(f"Model: `{os.path.basename(bpy.data.filepath)}`. Each value below was measured from the evaluated Blender "
            "objects (booleans applied) and compared with the survey value reconciled from the client's hand-measured "
            "sketches. Tolerance 0.05 in unless noted.\n\n")
    f.write(f"**Result: {npass} of {len(rows)} checks pass.**\n\n")
    f.write("| Item | Group | Expected (in) | Measured (in) | Diff | Result | Source / note |\n|---|---|---|---|---|---|---|\n")
    for r in rows:
        f.write(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]}{' - ' + r[7] if r[7] else ''} |\n")
print("VERIFY", npass, "of", len(rows), "pass")
for r in rows:
    if r[5] != "PASS":
        print("CHECK:", r)
