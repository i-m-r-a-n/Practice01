"""Assembles office_web_metadata.json for the web tour from the Blender export (export_web_metadata.py), the walk grid
(make_walk_grid.py) and the approved documents (room schedule, design concept). Descriptions only restate those documents.
python3 make_web_metadata.py EXPORT_DIR RENDER_DIR OUT_DIR
"""
import json
import math
import os
import re
import sys

from PIL import Image

EXP, RENDERS, OUT = sys.argv[1:4]
os.makedirs(OUT, exist_ok=True)
cams = json.load(open(os.path.join(EXP, "blender_cameras.json")))
rooms = json.load(open(os.path.join(EXP, "blender_rooms.json")))
names = json.load(open(os.path.join(EXP, "blender_names.json")))

# --------------------------------------------------------------- room names, function groups and descriptions
# Sources: 04_DOCUMENTATION/room_schedule.md (areas, finishes, furniture) and design_concept_and_notes.md section 4.
ROOM = {
    "Z01": ("Entrance lobby", "Arrival & visitors", "Security / visitor check-in desk in walnut facing the main gate; oak-slat brand wall with the three client logos and the tagline, lit by track spots. The existing stair is kept."),
    "Z02": ("Reception & visitor waiting", "Arrival & visitors", "Fluted-oak reception counter with a terrazzo ledge and an accessible lower section; backlit logo plate on a fluted oak wall; waiting lounge (sofa, green armchairs, walnut table, wool rug) under a suspended oak slat raft with a brass halo pendant."),
    "Z03": ("Visitor passage", "Arrival & visitors", "Links the reception with the experience centre and the guest WCs, so visitors never cross the office areas."),
    "Z28": ("Guest WCs", "Arrival & visitors", "Two guest WCs with vanities off the visitor passage."),
    "Z30": ("Experience centre", "Experience & meeting", "Brand-story wall with the logos and tagline, four garment display bays with deep-green backs, brass rails and LED shelves, a mannequin plinth, a 'yarn to garment' touch table, a long terrazzo display counter and a digital totem. Track lights on the existing beams; glass to the boardroom and the fabric library."),
    "Z08": ("Boardroom", "Experience & meeting", "15 seats: 6.1 m walnut table with a power/data trough, black leather chairs, 86 in screen on an oak slat media wall, walnut acoustic slats, green felt rafts between the existing beams and linear pendants over the table."),
    "Z09": ("Audit room", "Experience & meeting", "Meeting table (1500 x 900 mm) for 5 with tall document cabinets."),
    "Z10": ("Executive reception", "Executive suite", "PA desk and executive waiting on the executive link, oak herringbone floor."),
    "Z11": ("Director", "Executive suite", "Director desk (1680 x 810 mm), credenza and two visitor chairs; glass front on the oak-lined executive corridor."),
    "Z12": ("Managing Director", "Executive suite", "2.1 m walnut desk with leather pad, cognac executive chair, walnut feature wall with the logo, lounge corner (sofa, armchair, coffee table, rug), oak slat raft with a halo pendant, oak herringbone floor."),
    "Z13": ("Executive corridor", "Executive suite", "Glass-fronted, oak-lined corridor linking the executive reception with the Director and Managing Director; direct door from the executive suite to the boardroom."),
    "Z05": ("HR & admin", "Workplace", "Four desks and a round meeting table; the room also opens to the reception for candidates and vendors."),
    "Z06": ("Commercial & accounts", "Workplace", "Proposed revised concept: a finance suite behind privacy glass with 12 finance desks, the manager's desk facing the team, a document processing counter with scanner and printer, lockable records filing, a small finance discussion room and archive cabinets by the audit room. A clear corridor keeps the route to the washrooms and the prayer room outside the suite."),
    "Z07": ("Merchandising", "Workplace", "Proposed revised concept: 16 merchandiser desks, a sample hub with an inspection island, rolling sample rails, dress forms and a fitting mirror, a buyer review table with a 65 in screen, lockable sample storage, a trim and colour approval wall and a sample dispatch counter. The four ceiling AC positions are unchanged."),
    "Z04": ("Guest workspace", "Workplace", "Six work seats at a 2130 x 1000 mm table with a 55 in display for visiting staff."),
    "Z31": ("Staff corridor", "Workplace", "Staff route from the lobby staff door to HR & admin and commercial & accounts."),
    "Z14": ("CAD / technical design", "Design development", "Three CAD workstations, a large-format plotter, a layout / digitiser table and a brand-green felt pinboard for tech packs."),
    "Z15": ("Fabric & trim library", "Design development", "Fabric, colour, print and trim library: shelving, low swatch shelving, a swatch / garment rail and a D65 colour booth."),
    "Z16": ("3D printing lab", "Design development", "Four enclosed 3D printers, a printer bench, a post-processing bench with sink and a desk."),
    "Z17": ("Sample development", "Design development", "Pattern & cutting table (2440 x 1220 mm), two sample machine stations, dress forms and a steam station - an office-grade sample studio, not production."),
    "Z18": ("Global Design Studio", "Design development", "Creative workstations by the east windows, a 7.4 m mood-board wall, trend table, collection display and buyer-presentation table with an 86 in screen. 'Global Design Studio' is the name proposed in the master plan."),
    "Z19": ("Sample & material store", "Design development", "Store shelving for sample boxes and materials."),
    "Z22": ("Design-wing corridor", "Design development", "Corridor through the design-development wing."),
    "Z20": ("Staff cafe & pantry", "Staff facilities", "16 seats at two 2440 mm cafe tables and a 3660 mm pantry with sink and refrigerator."),
    "Z21": ("Staff lounge / training", "Staff facilities", "Multipurpose room: sofa group, 6-seat workshop table and screen."),
    "Z32": ("North corridor", "Staff facilities", "Circulation to the staff cafe, lounge / training and prayer rooms."),
    "Z33": ("Hallway", "Staff facilities", "Staff hallway between the workplace and the design wing."),
    "Z23": ("Prayer room (male)", "Prayer & wudu", "Prayer room with green prayer carpet, shoe rack and book shelf under 3000 K downlights."),
    "Z24": ("Wudu (male)", "Prayer & wudu", "Ablution room with a wudu bench next to the male prayer room."),
    "Z25": ("Prayer room (female)", "Prayer & wudu", "Separate prayer room with green prayer carpet, shoe rack and book shelf."),
    "Z34": ("Wudu (female)", "Prayer & wudu", "Ablution space with a wudu bench next to the female prayer room."),
    "Z26": ("Washroom (female)", "Washrooms", "Two WC cubicles and a 1520 mm vanity."),
    "Z27": ("Washroom (male)", "Washrooms", "Two WC cubicles, two urinals and a 1520 mm vanity."),
    "Z29": ("Guest workspace WC", "Washrooms", "WC with vanity for the guest workspace."),
}
GROUP_ORDER = ["Arrival & visitors", "Experience & meeting", "Executive suite", "Workplace", "Design development",
               "Staff facilities", "Prayer & wudu", "Washrooms"]
PRIMARY = {"Z02": "CAM_01_Reception_A", "Z30": "CAM_04_Experience_Centre_A", "Z08": "CAM_09_Boardroom_A", "Z12": "CAM_07_MD_Office_A",
           "Z07": "CAM_34_Merchandising_Sample_Hub", "Z06": "CAM_36_Accounts_Suite", "Z18": "CAM_13_Design_Studio_A"}

# --------------------------------------------------------------- cameras + render files
by_name = {c["name"]: c for c in cams}
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
for c in cams:                                          # RENDERS: comma-separated folders, first match wins (redesign renders first)
    jpg = next((p for p in (os.path.join(d, c["name"] + ".jpg") for d in RENDERS.split(",")) if os.path.exists(p)), None)
    if not jpg:
        c["render"] = None
        print("NO RENDER", c["name"])
        c["zone"] = next((r["zone"] for r in rooms if c["name"] in r["cameras"]), None)
        continue
    w, h = Image.open(jpg).size
    c["render"] = dict(file=os.path.relpath(os.path.abspath(jpg), REPO),
                       worker_path="/renders/" + c["name"] + ".jpg", width=w, height=h)
    if c["type"] == "PERSP":
        hf = 2 * math.atan(c["sensor_width"] / 2 / c["lens"])           # sensor fit AUTO: sensor width = larger image side
        c["hfov_deg_render"] = round(math.degrees(hf if w >= h else 2 * math.atan(math.tan(hf / 2) * w / h)), 4)
        c["vfov_deg_render"] = round(math.degrees(2 * math.atan(math.tan(hf / 2) * h / w) if w >= h else hf), 4)
    c["zone"] = next((r["zone"] for r in rooms if c["name"] in r["cameras"]), None)

out_rooms = []
for r in rooms:
    name, group, desc = ROOM[r["zone"]]
    prim = PRIMARY.get(r["zone"]) or (r["cameras"][0] if r["cameras"] else None)
    out_rooms.append(dict(zone=r["zone"], name=name, group=group, schedule_label=r["label"], area_sft=r["area_sft"], area_m2=r["area_m2"],
                          description=desc, floor_finish=r["floor_finish"], ceiling=r["ceiling"], cameras=r["cameras"], primary_camera=prim,
                          polygon_xz=r["polygon_xz"], centroid_xz=r["centroid_xz"]))
out_rooms.sort(key=lambda r: (GROUP_ORDER.index(r["group"]), r["zone"]))

TOUR = [
    ("overview", None, "CAM_ISO_SE", "The complete ground floor", "Ground floor of the proposed corporate headquarters & design development centre: visitor zone at the front, executive suite, workplace, design wing and staff facilities."),
    ("Z01", None, "CAM_03_Entrance_Lobby", None, None), ("Z02", None, "CAM_01_Reception_A", None, None),
    ("Z30", None, "CAM_04_Experience_Centre_A", None, None), ("Z08", None, "CAM_09_Boardroom_A", None, None),
    ("Z10", "Z12", "CAM_17_Executive_Reception", "Executive reception & Managing Director", None),
    ("Z06", None, "CAM_36_Accounts_Suite", None, None), ("Z05", None, "CAM_19_HR_Admin", None, None),
    ("Z07", None, "CAM_34_Merchandising_Sample_Hub", None, None), ("Z14", None, "CAM_15_CAD_Room", None, None),
    ("Z18", None, "CAM_13_Design_Studio_A", None, None), ("Z17", None, "CAM_23_Sample_Room", None, None),
    ("Z20", None, "CAM_20_Staff_Cafe", None, None), ("Z21", None, "CAM_21_Lounge_Training", None, None),
    ("Z23", "Z24", "CAM_22_Prayer_Male", "Prayer & wudu", None),
    ("final", None, "CAM_ISO_SW", "The complete ground floor", "Proposed interior visualization. Final dimensions and technical details subject to site verification."),
]
rz = {r["zone"]: r for r in out_rooms}
tour = []
for i, (z, z2, cam, title, desc) in enumerate(TOUR):
    st = dict(stop=i + 1, zone=z if z.startswith("Z") else None, camera=cam,
              title=title or rz[z]["name"], description=desc or rz[z]["description"])
    if z2:
        st["also_zone"] = z2
        st["also_camera"] = "CAM_07_MD_Office_A" if z2 == "Z12" else "CAM_33_Wudu_Male"
    tour.append(st)


QUICK = [("overview", "CAM_ISO_SE"), ("Z02", "CAM_01_Reception_A"), ("Z30", "CAM_04_Experience_Centre_A"), ("Z08", "CAM_09_Boardroom_A"),
         ("Z12", "CAM_07_MD_Office_A"), ("Z07", "CAM_34_Merchandising_Sample_Hub"), ("Z06", "CAM_36_Accounts_Suite"),
         ("Z18", "CAM_13_Design_Studio_A"), ("final", "CAM_ISO_SW")]
quick = []
for i, (z, cam) in enumerate(QUICK):
    src = next((t for t in tour if t["camera"] == cam), None)
    st = dict(stop=i + 1, zone=z if z.startswith("Z") else None, camera=cam,
              title=src["title"] if src else rz[z]["name"], description=src["description"] if src else rz[z]["description"])
    quick.append(st)


def sanitize(n):   # three.js PropertyBinding.sanitizeNodeName (GLTFLoader node names)
    return re.sub(r"[\[\]\.:/]", "", re.sub(r"\s", "_", n))


meta = dict(
    version="2026-10-27",
    note="Generated from the space-optimisation model (GARMENT_OFFICE_SPACE_OPTIMIZATION/02_IMPROVED_BLENDER_MODEL/Optimized_Office_Interior.blend: "
         "approved design with Z06 / Z07 replaced by the proposed option B) by scripts/web/export_web_metadata.py + make_web_metadata.py. "
         "Proposed interior visualization; final dimensions and technical details subject to site verification.",
    axes="glTF / three.js world: metres, x east, y up, z south (Blender (x, y, z) -> (x, z, -y)). Floor at y = 0, underside of the steel deck at 2.90 m.",
    eye_height_m=1.6,
    web_glb=dict(path="GARMENT_OFFICE_SPACE_OPTIMIZATION/04_SIMPLE_VIEWER/assets/Optimized_Office_Interior_web_baked.glb",
                 groups=dict(WEB_INTERIOR="walls, floors, glazing, doors, furniture, plants, branding",
                             WEB_OVERHEAD="steel deck, beams, ceiling rafts / baffles, light fittings, AC and fire devices (hide for the dollhouse view)",
                             WEB_CAMERAS="the render cameras (same names as the renders)")),
    cameras=cams,
    camera_notes=("position / direction / up / quaternion are the exact Blender camera matrices converted to glTF axes (checked against "
                  "the camera nodes in the GLB: <= 0.005 mm, <= 0.12 deg). Perspective cameras are level; the renders frame the view with a "
                  "vertical lens shift (shift_y, fraction of the larger image side). In three.js: camera.fov = vfov for the window aspect "
                  "(keep the horizontal fov of the render on landscape windows), then camera.setViewOffset(W, H, 0, -shift_y * max(W, H), W, H)."),
    rooms=out_rooms,
    room_groups=GROUP_ORDER,
    tour=tour,
    quick_tour=quick,
    names=dict(overhead=names["overhead"], overhead_threejs=[sanitize(n) for n in names["overhead"]],
               walls_glazing_doors_structure=names["walls_glazing_doors_structure"], door_leaves=names["door_leaves"]),
    walk_grid="walk_grid.json",
)
json.dump(meta, open(os.path.join(OUT, "office_web_metadata.json"), "w"), indent=1)
print("METADATA", len(cams), "cameras,", len(out_rooms), "rooms,", len(tour), "tour stops")
