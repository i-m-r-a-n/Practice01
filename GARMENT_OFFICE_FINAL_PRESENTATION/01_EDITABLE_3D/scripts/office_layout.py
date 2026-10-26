"""Office fit-out data for the ground floor (pure Python; used by the Blender builder and the 2D drawings).

Concept: PREMIUM INTERNATIONAL FASHION CORPORATE HEADQUARTERS & DESIGN DEVELOPMENT CENTER.
Zoning: visitor zone at the front (lobby -> reception -> passage -> experience centre -> boardroom, executive
suite beside the reception), administration in room 7, merchandising open office in room 6 (north), design
development + staff support in room 8. Department list from the client's company profile (Reception,
Merchandising, Commercial, HR & administration, Conference/showroom, Directors room, Sample section, CAD room)
plus the written office programme and the Global Design Studio master plan (studio zones, about 1,400 sft).
Head count basis: about 30 management/staff (company profile) + about 6 studio staff (master plan) -> about
54 work seats including growth and guests (assumption, see documentation).

Plan coordinates in inches (x east, y south, origin = inner NW corner of room 1); facing in degrees:
0 = the item's front looks south, 90 east, 180 north, 270 west (see lib_mesh.place).
Status of every partition: PROPOSED (new fit-out work). Existing walls come from survey.py.
"""
from survey import (FRONT, MID_S, MID_N, HALL_S, R6_N, R6_S, R5_N, R5_S, R7_E, R7_LOW_W, STRIP_E, R2_W, R2_E,
                    R2_N, JOG, R8_W, R8_E, R8_N, SE_N, ENG_S, ENG_N, DECK_H, HALF_H, LINTEL, W)

S, E, N, Wd = 0, 90, 180, 270

# ------------------------------------------------------------------------------------------ partitions
# infill above the existing 48" walls: (wall id, a, b, treatment)
HALF_TREAT = [("PW01", 362, 420, "glass"), ("PW01", 420, 485, "solid"), ("PW01", 485, 565, "glass"),
              ("PW05", -228, -10, "glass"), ("PW05", -423, -228, "solid"), ("PW05", -843, -423, "glass"),
              ("PW06", R7_E, 866, "glass"),
              ("PW07", 367, 420, "glass"), ("PW07", 420, 485, "solid"), ("PW07", 485, 866, "glass")]

# new openings in existing walls: (wall id, op)
NEW_OPENINGS = [("IW04", ("W11", "win", 60, 112, "Lobby - reception glass", 60)),
                ("IW04", ("W12", "win", 136, 188, "Lobby - reception glass", 60)),
                ("IW01", ("D17", "door", 114, 156, "Staff entrance: lobby - staff corridor 42\"")),
                ("PW01", ("D18", "door", 372, 414, "Reception - visitor passage 42\"")),
                ("PW01", ("D19", "door", 500, 542, "Reception - boardroom 42\"")),
                ("IW03", ("D20", "door", 620, 662, "Executive suite - boardroom 42\"")),
                ("PW07", ("D21", "door", 805, 847, "Experience centre - boardroom 42\""))]
REMOVED_OPENINGS = {"IW08": ["D07"]}          # 64" store opening re-used as the female prayer door D22 (36")
EXTRA_OPENINGS = [("IW08", ("D22", "door", -806, -770, "Female prayer room door 36\""))]


def NP(wid, name, axis, c0, c1, a, b, ops=(), glass=False):
    return W(wid, name, axis, c0, c1, a, b, "glass" if glass else "new", ops, status="PROPOSED")


NEW_WALLS = [
    NP("NP01", "HR & admin - commercial, glass", "h", -231, -228, 163, 362, glass=True),
    NP("NP32", "Staff corridor - HR & admin, glass", "v", 160, 163, -231, -10, [("D48", "door", -150, -114, "HR & admin")], True),
    NP("NP02", "Audit room west", "v", 96, 100, -891, -744),
    NP("NP03", "Audit room east", "v", 250, 254, -891, -744),
    NP("NP04", "Audit room front, glass", "h", -744, -740, 96, 254, [("D31", "door", 152, 188, "Audit room (sliding)")], True),
    NP("NP05", "Visitor passage - guest WCs", "v", 420, 425, -214, -10, [("D32", "door", -190, -160, "Guest WC"), ("D33", "door", -60, -30, "Guest WC")]),
    NP("NP06", "Guest WC divider", "h", -114, -110, 425, 480),
    NP("NP07", "Guest WCs - boardroom", "v", 480, 485, -214, -10),
    NP("NP08", "Female prayer - female washroom", "h", -720, -715, R2_W, STRIP_E),
    NP("NP09", "Store opening infill", "v", STRIP_E, 46, -834, -806),
    NP("NP33", "Experience centre - merchandising (display wall)", "h", -428, -423, 367, 866, [("D49", "door", 818, 860, "Merchandising - experience centre")]),
    NP("NP10", "Sample room north", "h", -843, -838, R8_W, 1045),
    NP("NP11", "Sample room front, glass", "v", 1040, 1045, -838, -600, [("D34", "door", -702, -660, "Sample room")], True),
    NP("NP12", "Sample room - 3D lab", "h", -600, -595, R8_W, 1045),
    NP("NP13", "3D lab front, glass", "v", 1040, 1045, -595, -445, [("D35", "door", -540, -504, "3D printing lab")], True),
    NP("NP14", "3D lab - fabric library", "h", -445, -440, R8_W, 1045),
    NP("NP15", "Fabric library front, glass", "v", 1040, 1045, -440, -262, [("D36", "door", -380, -338, "Fabric & trim library")], True),
    NP("NP16", "Fabric library - CAD", "h", -262, -257, R8_W, 1045),
    NP("NP17", "CAD room front, glass", "v", 1040, 1045, -257, -219, [("D37", "door", -255, -219, "CAD / technical design")], True),
    NP("NP18", "Design studio front, glass", "v", 1100, 1105, -843, -530, [("D38", "door", -700, -640, "Global Design Studio")], True),
    NP("NP19", "Store west", "v", 1100, 1105, -530, -432),
    NP("NP20", "Design studio - store", "h", -530, -525, 1105, R8_E, [("D39", "door", 1210, 1246, "Sample & material store")]),
    NP("NP21", "Store south", "h", -437, -432, 1105, 1156),
    NP("NP22", "Staff cafe - corridor, glass", "h", -905, -900, R8_W, 1078, [("D40", "door", 940, 1000, "Staff cafe 60\"")], True),
    NP("NP23", "Lounge and cafe - north corridor, glass", "v", 1073, 1078, -1440, -905, [("D41", "door", -1300, -1258, "Lounge / training"), ("D42", "door", -1140, -1098, "Staff cafe")], True),
    NP("NP24", "Lounge - cafe, glass", "h", -1250, -1245, R8_W, 1073, glass=True),
    NP("NP25", "Prayer and wudu - north corridor", "v", 1150, 1155, -1440, -1210, [("D43", "door", -1400, -1358, "Prayer (male)"), ("D44", "door", -1265, -1229, "Wudu (male)")]),
    NP("NP26", "Design studio - north corridor (mood-board wall)", "v", 1150, 1155, -1210, -900),
    NP("NP27", "Prayer - wudu", "h", -1283, -1278, 1155, R8_E, [("D45", "door", 1240, 1270, "Prayer - wudu")]),
    NP("NP28", "Wudu - design studio", "h", -1215, -1210, 1155, R8_E),
    NP("NP29", "Executive offices front, glass", "h", 54, 57, 700, 1088, [("D46", "door", 740, 776, "Director"), ("D47", "door", 880, 922, "Managing Director")], True),
    NP("NP30", "Executive reception - director, glass", "v", 700, 703, 57, FRONT, glass=True),
    NP("NP31", "Director - MD, glass", "v", 858, 861, 57, FRONT, glass=True),
]

# door leaves: opening id -> (type, finish). type: glass | glass2 (double) | solid | solid2 | fire | slide | none
DOOR_TYPES = {"D01": ("glass2", "alu_black"), "D02": ("solid", "oak"), "D03": ("glass2", "alu_black"), "D04": ("glass", "alu_black"),
              "D05": ("solid2", "walnut"), "D06": ("solid", "oak"), "D08": ("solid", "oak"), "D09": ("solid", "oak"),
              "D10": ("glass", "alu_black"), "D11": ("none", ""), "D12": ("none", ""), "D13": ("glass", "alu_black"),
              "D14": ("fire", "steel_painted"), "D15": ("fire", "steel_painted"), "D16": ("fire", "steel_painted"),
              "D17": ("solid", "oak"), "D18": ("glass", "alu_black"), "D19": ("glass", "alu_black"), "D20": ("solid", "walnut"),
              "D21": ("glass", "alu_black"), "D22": ("solid", "oak"), "D31": ("slide", "alu_black"), "D32": ("solid", "oak"),
              "D33": ("solid", "oak"), "D34": ("glass", "alu_black"), "D35": ("glass", "alu_black"), "D36": ("glass", "alu_black"),
              "D37": ("glass", "alu_black"), "D38": ("glass2", "alu_black"), "D39": ("solid", "oak"), "D40": ("glass2", "alu_black"),
              "D41": ("glass", "alu_black"), "D42": ("glass", "alu_black"), "D43": ("solid", "oak"), "D44": ("solid", "oak"),
              "D45": ("none", ""), "D46": ("glass", "alu_black"), "D47": ("glass", "alu_black"), "D48": ("glass", "alu_black"),
              "D49": ("solid", "oak")}

# ------------------------------------------------------------------------------------------ zones
# (collection, id, label, polygon, floor finish, ceiling note)
ZONES = [
    ("Reception", "Z01", "ENTRANCE LOBBY\nsecurity + visitor check-in", [(0, 0), (300, 0), (300, FRONT), (0, FRONT)], "fl_terrazzo", "exposed deck, linear pendants, brand-wall spots"),
    ("Reception", "Z02", "RECEPTION + VISITOR WAITING", [(305, 0), (565, 0), (565, FRONT), (305, FRONT)], "fl_terrazzo", "oak slat raft, brass halo, linear pendant on the beam"),
    ("Reception", "Z03", "VISITOR PASSAGE", [(367, -214), (420, -214), (420, -10), (367, -10)], "fl_terrazzo", "downlights"),
    ("Experience_Center", "Z30", "EXPERIENCE CENTRE\nbrand story + collection gallery", [(367, -423), (866, -423), (866, -219), (367, -219)], "fl_terrazzo", "track lights fixed to the beams"),
    ("Meeting_Rooms", "Z08", "BOARDROOM\n15 seats", [(485, -214), (866, -214), (866, -10), (485, -10)], "fl_herringbone", "green felt rafts between beams"),
    ("Meeting_Rooms", "Z09", "AUDIT ROOM", [(100, -891), (250, -891), (250, -744), (100, -744)], "fl_carpet", "linear pendant"),
    ("Executive_Area", "Z10", "EXECUTIVE RECEPTION\nPA + waiting", [(570, 0), (700, 0), (700, FRONT), (570, FRONT)], "fl_herringbone", "linear pendant"),
    ("Executive_Area", "Z11", "DIRECTOR", [(703, 57), (858, 57), (858, FRONT), (703, FRONT)], "fl_herringbone", "linear pendant"),
    ("Executive_Area", "Z12", "MANAGING DIRECTOR", [(861, 57), (1088, 57), (1088, FRONT), (861, FRONT)], "fl_herringbone", "oak slat raft + halo"),
    ("Executive_Area", "Z13", "EXECUTIVE CORRIDOR", [(700, 0), (1088, 0), (1088, 54), (700, 54)], "fl_herringbone", "downlights"),
    ("Workstations", "Z04", "GUEST WORKSPACE\n6 seats", [(R2_W, -152), (50, -152), (50, R2_N), (R2_E, R2_N), (R2_E, MID_S), (R2_W, MID_S)], "fl_carpet", "linear pendant"),
    ("Workstations", "Z05", "HR & ADMIN", [(163, -228), (362, -228), (362, -10), (163, -10)], "fl_carpet", "linear pendant"),
    ("Workstations", "Z31", "STAFF CORRIDOR", [(110, -228), (160, -228), (160, -10), (110, -10)], "fl_terrazzo", "downlights"),
    ("Workstations", "Z06", "COMMERCIAL & ACCOUNTS\n12 workstations + manager", [(46, -231), (362, -231), (362, MID_N), (254, MID_N), (254, -740), (96, -740), (96, MID_N), (46, MID_N)], "fl_carpet", "linear pendants"),
    ("Workstations", "Z07", "MERCHANDISING\nopen office, 16 workstations", [(367, R6_N), (866, R6_N), (866, -428), (367, -428)], "fl_carpet", "felt baffles between beams"),
    ("Design_Development", "Z14", "CAD / TECHNICAL\nDESIGN", [(R8_W, -257), (1040, -257), (1040, MID_S), (R8_W, MID_S)], "fl_carpet", "linear pendants 4000K"),
    ("Design_Development", "Z15", "FABRIC & TRIM LIBRARY\nfabric, colour, print, trims", [(R8_W, -440), (1040, -440), (1040, -262), (R8_W, -262)], "fl_concrete", "linear pendants"),
    ("Design_Development", "Z16", "3D PRINTING LAB", [(R8_W, -595), (1040, -595), (1040, -445), (R8_W, -445)], "fl_concrete", "linear pendants"),
    ("Design_Development", "Z17", "SAMPLE DEVELOPMENT\npattern + cutting support", [(R8_W, R6_N), (1040, R6_N), (1040, -600), (R8_W, -600)], "fl_concrete", "linear pendants"),
    ("Design_Development", "Z18", "GLOBAL DESIGN STUDIO\n(name as proposed in the master plan)", [(1155, -1210), (R8_E, -1210), (R8_E, -530), (1105, -530), (1105, -900), (1155, -900)], "fl_oak_planks", "linear pendants + mood-board track"),
    ("Design_Development", "Z19", "SAMPLE & MATERIAL STORE", [(1105, -525), (R8_E, -525), (R8_E, -437), (1105, -437)], "fl_concrete", "batten lights"),
    ("Support_Rooms", "Z20", "STAFF CAFE + PANTRY", [(R8_W, -1245), (1073, -1245), (1073, -905), (R8_W, -905)], "fl_oak_planks", "pendants"),
    ("Support_Rooms", "Z21", "STAFF LOUNGE / TRAINING\n(multipurpose)", [(R8_W, R8_N), (1048, R8_N), (1048, -1440), (1073, -1440), (1073, -1250), (R8_W, -1250)], "fl_oak_planks", "halo + downlights"),
    ("Support_Rooms", "Z22", "CORRIDOR", [(R8_W, -900), (1100, -900), (1100, -437), (1156, -437), (1156, ENG_S), (1045, ENG_S), (1045, -843), (R8_W, -843)], "fl_terrazzo", "downlights"),
    ("Support_Rooms", "Z32", "NORTH CORRIDOR", [(1078, -1440), (1150, -1440), (1150, -900), (1078, -900)], "fl_terrazzo", "downlights"),
    ("Support_Rooms", "Z33", "HALLWAY", [(R7_E, MID_N), (866, MID_N), (866, HALL_S), (R7_E, HALL_S)], "fl_terrazzo", "downlights"),
    ("Prayer_Rooms", "Z23", "PRAYER (MALE)", [(1155, -1440), (R8_E, -1440), (R8_E, -1283), (1155, -1283)], "fl_carpet_green", "downlights 3000K"),
    ("Prayer_Rooms", "Z24", "WUDU (MALE)", [(1155, -1278), (R8_E, -1278), (R8_E, -1215), (1155, -1215)], "fl_porcelain", "downlights"),
    ("Prayer_Rooms", "Z25", "PRAYER (FEMALE)", [(R2_W, MID_N), (STRIP_E, MID_N), (STRIP_E, -760), (R2_W, -760)], "fl_carpet_green", "downlights 3000K"),
    ("Prayer_Rooms", "Z34", "WUDU (FEMALE)", [(R2_W, -760), (STRIP_E, -760), (STRIP_E, -720), (R2_W, -720)], "fl_porcelain", "downlight"),
    ("Washrooms", "Z26", "WASHROOM (FEMALE)", [(R2_W, -715), (STRIP_E, -715), (STRIP_E, -519), (R2_W, -519)], "fl_porcelain", "downlights"),
    ("Washrooms", "Z27", "WASHROOM (MALE)", [(R2_W, -514), (STRIP_E, -514), (STRIP_E, JOG), (R2_W, JOG)], "fl_porcelain", "downlights"),
    ("Washrooms", "Z28", "GUEST WC (2)", [(425, -214), (480, -214), (480, -10), (425, -10)], "fl_porcelain", "downlights"),
    ("Washrooms", "Z29", "GUEST WORKSPACE WC", [(R2_W, R2_N), (47, R2_N), (47, -155), (R2_W, -155)], "fl_porcelain", "downlight"),
]
LABEL_AT = {"Z01": (232, 60), "Z02": (400, 70), "Z03": (394, -120), "Z30": (616, -300), "Z08": (676, -190), "Z09": (175, -870),
            "Z10": (635, 40), "Z11": (780, 100), "Z12": (975, 100), "Z13": (900, 27), "Z04": (25, -130), "Z05": (262, -212),
            "Z31": (135, -120), "Z06": (175, -560), "Z07": (616, -650), "Z14": (965, -95), "Z15": (958, -300), "Z16": (958, -520),
            "Z17": (958, -690), "Z18": (1240, -760), "Z19": (1215, -480), "Z20": (975, -1100), "Z21": (975, -1380), "Z22": (988, -872),
            "Z32": (1114, -1100), "Z33": (614, -867), "Z23": (1240, -1330), "Z24": (1240, -1246), "Z25": (-7, -820), "Z34": (-7, -740), "Z26": (-7, -600),
            "Z27": (-7, -330), "Z28": (452, -112), "Z29": (0, -170)}
VERTICAL_LABELS = {"Z25", "Z26", "Z27", "Z03", "Z28", "Z31", "Z32"}
SMALL_LABELS = {"Z34", "Z24", "Z29", "Z13", "Z22", "Z33", "Z28", "Z03"}

# ------------------------------------------------------------------------------------------ assets
# key -> (builder in lib_assets, kwargs, plan footprint w x d in inches, schedule description)
ASSETS = {
    "task_chair": ("task_chair", {}, (26, 26), "Ergonomic task chair, mesh back, 5-star base"),
    "task_chair_green": ("task_chair", {"seat": "fab_green"}, (26, 26), "Ergonomic task chair, green upholstery"),
    "exec_chair_black": ("exec_chair", {"cover": "leather_black"}, (28, 28), "High-back executive chair, black leather"),
    "exec_chair_cognac": ("exec_chair", {"cover": "leather_cognac"}, (28, 28), "High-back executive chair, cognac leather"),
    "board_chair": ("exec_chair", {"cover": "leather_black", "high": False}, (26, 26), "Boardroom chair, black leather, polished base"),
    "visitor_chair": ("cantilever_chair", {"seat": "fab_charcoal"}, (21, 22), "Cantilever visitor chair, chrome frame"),
    "visitor_chair_green": ("cantilever_chair", {"seat": "fab_green"}, (21, 22), "Cantilever chair, green upholstery"),
    "dining_chair": ("side_chair", {"seat": "fab_green", "frame": "oak"}, (20, 21), "Oak dining chair, green upholstered seat"),
    "stool": ("stool", {}, (16, 16), "Oak-top stool, black base"),
    "sofa_84_sand": ("sofa", {"length": 84, "cover": "fab_sand"}, (84, 34), "3-seat sofa, sand woven fabric"),
    "sofa_72_sand": ("sofa", {"length": 72, "cover": "fab_sand"}, (72, 34), "2-seat sofa, sand woven fabric"),
    "sofa_96_green": ("sofa", {"length": 96, "cover": "fab_green"}, (96, 34), "3-seat sofa, brand-green woven fabric"),
    "lounge_green": ("lounge_chair", {"cover": "fab_green"}, (28, 28), "Lounge armchair, green fabric, oak legs"),
    "lounge_grey": ("lounge_chair", {"cover": "fab_grey"}, (28, 28), "Lounge armchair, grey fabric, oak legs"),
    "bench3": ("bench_desk", {"n": 3}, (165, 55), "Bench workstation 2 x 3 desks (1400 x 700 mm), 400 mm felt screen, monitors, pedestals"),
    "bench2": ("bench_desk", {"n": 2}, (110, 55), "Bench workstation 2 x 2 desks (1400 x 700 mm)"),
    "bench_design": ("bench_desk", {"n": 2, "w": 63, "d": 31.5, "screen": "felt_grey", "top": "oak"}, (126, 63), "Designer bench 2 x 2 desks (1600 x 800 mm), oak"),
    "cad_desk": ("single_desk", {"mons": 2}, (63, 31.5), "CAD workstation 1600 x 800 mm, dual monitors"),
    "desk_single": ("single_desk", {"mons": 1}, (63, 31.5), "Desk 1600 x 800 mm, oak top, monitor, pedestal"),
    "security_desk": ("single_desk", {"w": 48, "d": 24, "mons": 1, "top": "walnut", "base": "metal_black", "ped": False}, (48, 24), "Security / visitor desk, walnut"),
    "exec_desk_md": ("exec_desk", {"w": 84, "d": 38}, (84, 38), "MD desk 2130 x 965 mm, smoked walnut, leather pad"),
    "exec_desk_dir": ("exec_desk", {"w": 66, "d": 32}, (66, 32), "Director desk 1680 x 810 mm, smoked walnut"),
    "board_table": ("boardroom_table", {"L": 240, "D": 54}, (240, 54), "Boardroom table 6100 x 1370 mm, walnut, power/data trough"),
    "reception_desk": ("reception_desk", {"L": 108, "D": 30}, (110, 37), "Reception counter 2750 mm, fluted oak, terrazzo top, accessible low section"),
    "table_team": ("table", {"w": 150, "d": 48, "top": "oak", "kind": "sled"}, (150, 48), "Team table 3800 x 1200 mm, oak, sled base"),
    "table_audit": ("table", {"w": 60, "d": 36, "top": "oak", "kind": "legs"}, (60, 36), "Meeting table 1500 x 900 mm"),
    "table_guest": ("table", {"w": 84, "d": 40, "top": "oak", "kind": "sled"}, (84, 40), "Work table 2130 x 1000 mm"),
    "table_present": ("table", {"w": 120, "d": 48, "top": "walnut", "kind": "pedestal"}, (120, 48), "Presentation table 3050 x 1200 mm, walnut"),
    "table_trend": ("table", {"w": 96, "d": 42, "h": 36, "top": "oak", "kind": "sled"}, (96, 42), "Trend research table 2440 x 1070 mm, counter height"),
    "table_pattern": ("table", {"w": 96, "d": 48, "h": 36, "top": "plastic_white", "kind": "legs", "edge": "oak"}, (96, 48), "Pattern & cutting table 2440 x 1220 mm, 915 mm high"),
    "table_dining": ("table", {"w": 96, "d": 36, "top": "oak", "kind": "panel"}, (96, 36), "Cafe table 2440 x 915 mm, oak"),
    "table_training": ("table", {"w": 96, "d": 36, "top": "oak", "kind": "sled"}, (96, 36), "Training / workshop table"),
    "table_review": ("table", {"w": 60, "d": 36, "h": 36, "top": "plastic_white", "kind": "legs"}, (60, 36), "Review counter table"),
    "table_layout": ("table", {"w": 72, "d": 48, "h": 36, "top": "plastic_white", "kind": "legs", "edge": "oak"}, (72, 48), "Layout / digitiser table, counter height"),
    "coffee_round": ("round_table", {"dia": 32, "h": 16, "top": "walnut"}, (32, 32), "Coffee table 810 mm, walnut"),
    "side_round": ("round_table", {"dia": 20, "h": 20, "top": "terrazzo_counter"}, (20, 20), "Side table, terrazzo top"),
    "meet_round": ("round_table", {"dia": 42, "h": 29.5, "top": "oak"}, (42, 42), "Round meeting table 1070 mm"),
    "console": ("cabinet", {"w": 72, "d": 16, "h": 30, "body": "oak", "front": "oak", "doors": 2, "top": "walnut"}, (72, 16), "Console 1830 mm, oak + walnut top"),
    "credenza_walnut": ("cabinet", {"w": 96, "d": 20, "h": 30, "body": "walnut", "front": "walnut", "doors": 4, "pulls": "brass"}, (96, 20), "Credenza 2440 mm, smoked walnut"),
    "credenza_oak": ("cabinet", {"w": 96, "d": 18, "h": 30, "body": "plastic_white", "front": "oak", "doors": 4}, (96, 18), "Credenza 2440 mm, oak fronts"),
    "credenza_72": ("cabinet", {"w": 72, "d": 18, "h": 30, "body": "plastic_white", "front": "oak", "doors": 3}, (72, 18), "Low storage 1830 mm"),
    "filing_96": ("cabinet", {"w": 96, "d": 18, "h": 42, "body": "plastic_white", "front": "plastic_white", "doors": 4, "top": "oak"}, (96, 18), "Lateral filing 2440 mm, oak top"),
    "filing_120": ("cabinet", {"w": 120, "d": 20, "h": 42, "body": "plastic_white", "front": "oak", "doors": 5, "top": "oak"}, (120, 20), "Filing / storage 3050 mm"),
    "tall_cab_90": ("cabinet", {"w": 90, "d": 16, "h": 78, "body": "plastic_white", "front": "plastic_white", "doors": 4}, (90, 16), "Tall document cabinets 2290 mm"),
    "under_window_110": ("cabinet", {"w": 110, "d": 18, "h": 28, "body": "plastic_white", "front": "oak", "doors": 4, "top": "oak"}, (110, 18), "Low storage under window"),
    "review_counter": ("cabinet", {"w": 270, "d": 18, "h": 36, "body": "plastic_white", "front": "oak", "doors": 10, "top": "terrazzo_counter"}, (270, 18), "Sample review counter 6860 mm, terrazzo top"),
    "ec_counter": ("cabinet", {"w": 360, "d": 20, "h": 34, "body": "oak", "front": "oak", "doors": 12, "top": "terrazzo_counter", "pulls": None}, (360, 20), "Experience centre low display counter, oak"),
    "printer_bench": ("cabinet", {"w": 130, "d": 24, "h": 30, "body": "plastic_white", "front": "plastic_white", "doors": 5, "top": "plastic_white"}, (130, 24), "3D printer bench"),
    "post_bench": ("cabinet", {"w": 110, "d": 24, "h": 30, "body": "plastic_white", "front": "plastic_white", "doors": 4, "top": "terrazzo_counter"}, (110, 24), "Post-processing bench with sink"),
    "plan_chest": ("cabinet", {"w": 60, "d": 24, "h": 36, "body": "plastic_white", "front": "plastic_white", "doors": 2, "top": "oak"}, (60, 24), "Plan chest"),
    "dry_cabinet": ("cabinet", {"w": 24, "d": 20, "h": 72, "body": "plastic_dark", "front": "plastic_dark", "doors": 1}, (24, 20), "Filament dry cabinet"),
    "shoe_rack_36": ("cabinet", {"w": 36, "d": 16, "h": 24, "body": "oak", "front": "oak", "doors": 0}, (36, 16), "Shoe rack, oak"),
    "visitor_leather": ("cantilever_chair", {"seat": "leather_black"}, (21, 22), "Cantilever visitor chair, black leather"),
    "shelf_store72": ("shelving", {"w": 72, "d": 18, "h": 84, "seed": 15, "books": True, "mix": ("paper", "g_white", "g_heather", "g_sand")}, (72, 18), "Store shelving"),
    "quran_shelf": ("shelving", {"w": 60, "d": 12, "h": 54, "shelves": 3, "seed": 41, "mix": ("g_green", "g_white", "g_sand", "g_navy")}, (60, 12), "Book shelf, oak (prayer room)"),
    "quran_shelf_f": ("shelving", {"w": 40, "d": 10, "h": 48, "shelves": 3, "seed": 42, "mix": ("g_green", "g_white", "g_sand", "g_navy")}, (40, 10), "Book shelf, oak (prayer room)"),
    "shoe_rack": ("cabinet", {"w": 50, "d": 16, "h": 30, "body": "oak", "front": "oak", "doors": 0}, (50, 16), "Shoe rack, oak"),
    "shelf_lib_150": ("shelving", {"w": 150, "d": 14, "h": 84, "seed": 11, "mix": ("g_navy", "g_white", "g_heather", "g_sand", "g_olive", "g_rust", "g_sage", "g_denim")}, (150, 14), "Fabric & trim library shelving, oak"),
    "shelf_lib_low": ("shelving", {"w": 105, "d": 14, "h": 28, "shelves": 2, "seed": 12, "mix": ("g_navy", "g_white", "g_heather", "g_sand", "g_sage")}, (105, 14), "Low swatch shelving under window"),
    "shelf_store": ("shelving", {"w": 92, "d": 18, "h": 84, "seed": 13, "books": True, "mix": ("paper", "g_white", "g_heather", "g_sand")}, (92, 18), "Store shelving (sample boxes)"),
    "shelf_book_72": ("shelving", {"w": 72, "d": 14, "h": 78, "seed": 14}, (72, 14), "Bookshelf, oak"),
    "lockers8": ("lockers", {"n": 6, "w": 15, "d": 18, "h": 44}, (90, 18), "Staff lockers (6), oak + white"),
    "bay_104": ("garment_rail_bay", {"width": 104, "seed": 21}, (104, 24), "Garment display bay 2640 mm: oak frame, green back, brass rail, LED"),
    "bay_104b": ("garment_rail_bay", {"width": 104, "seed": 22}, (104, 24), "Garment display bay 2640 mm"),
    "bay_86": ("garment_rail_bay", {"width": 86, "seed": 23}, (86, 24), "Garment display bay 2180 mm"),
    "bay_86b": ("garment_rail_bay", {"width": 86, "seed": 24}, (86, 24), "Garment display bay 2180 mm"),
    "bay_120_white": ("garment_rail_bay", {"width": 120, "seed": 25, "back": "paint_white"}, (120, 24), "Collection rail bay, white back"),
    "bay_110_white": ("garment_rail_bay", {"width": 110, "seed": 26, "back": "paint_white"}, (110, 24), "Swatch / garment rail bay"),
    "bay_72_white": ("garment_rail_bay", {"width": 72, "seed": 27, "back": "paint_white"}, (72, 24), "Sample rail"),
    "plinth": ("plinth_display", {"w": 130, "d": 44, "h": 8}, (130, 44), "Mannequin plinth, oak + terrazzo, LED base"),
    "material_table": ("material_table", {"w": 144, "d": 40, "h": 34}, (144, 40), "Yarn-to-garment touch table, oak"),
    "mannequin_navy": ("mannequin_garment", {"cover_mat": "g_navy"}, (18, 18), "Display form with garment"),
    "mannequin_sand": ("mannequin_garment", {"cover_mat": "g_sand"}, (18, 18), "Display form with garment"),
    "mannequin_olive": ("mannequin_garment", {"cover_mat": "g_olive"}, (18, 18), "Display form with garment"),
    "mannequin_white": ("mannequin_garment", {"cover_mat": "g_white"}, (18, 18), "Display form with garment"),
    "dress_form": ("dress_form", {}, (16, 16), "Dress form, brass stand"),
    "light_booth": ("light_booth", {}, (32, 22), "Colour assessment booth (D65)"),
    "sewing": ("sewing_station", {}, (48, 20), "Sample machine station"),
    "printer3d": ("printer_3d", {}, (20, 20), "Enclosed 3D printer"),
    "plotter": ("plotter", {}, (62, 26), "Large-format plotter"),
    "steam": ("steam_station", {}, (50, 18), "Steam pressing station"),
    "mfp": ("cabinet", {"w": 24, "d": 24, "h": 44, "body": "plastic_white", "front": "plastic_white", "doors": 1, "top": "plastic_dark", "pulls": None}, (24, 24), "Multifunction printer"),
    "wc": ("wc_pan", {}, (18, 29), "Wall-hung WC, concealed cistern"),
    "urinal": ("urinal", {}, (14, 13), "Urinal"),
    "vanity2": ("vanity", {"L": 60, "D": 21, "basins": 2}, (60, 21), "Vanity 1520 mm, 2 vessel basins, mirror, LED"),
    "vanity1": ("vanity", {"L": 30, "D": 18, "basins": 1}, (30, 18), "Vanity 760 mm, 1 basin, mirror"),
    "cubicle": ("cubicle", {}, (36, 60), "WC cubicle, compact laminate"),
    "wudu4": ("wudu_station", {"L": 80, "n": 3}, (80, 30), "Wudu bench, 3 places"),
    "wudu5": ("wudu_station", {"L": 120, "n": 5}, (120, 30), "Wudu bench, 5 places"),
    "pantry": ("pantry_run", {"L": 144, "D": 25}, (144, 25), "Pantry 3660 mm: sink, upper cabinets, coffee, microwave"),
    "fridge": ("fridge", {}, (30, 28), "Refrigerator"),
    "water": ("water_dispenser", {}, (13, 13), "Water dispenser"),
    "screen_86": ("wall_screen", {"w": 75, "h": 42}, (75, 3), "86 in display"),
    "screen_75": ("wall_screen", {"w": 66, "h": 37}, (66, 3), "75 in display"),
    "screen_65": ("wall_screen", {"w": 57, "h": 32, "mat": "screen_ui"}, (57, 3), "65 in display"),
    "screen_55": ("wall_screen", {"w": 48, "h": 27, "mat": "screen_ui"}, (48, 3), "55 in display"),
    "totem": ("wall_screen", {"w": 28, "h": 50, "depth": 3}, (28, 6), "Digital totem 55 in portrait"),
    "whiteboard": ("whiteboard", {"w": 72, "h": 40}, (72, 1), "Whiteboard"),
    "pinboard_merch": ("pinboard_wall", {"w": 270, "h": 40, "seed": 31}, (270, 2), "Linen pinboard (trims / sample boards)"),
    "moodboard": ("pinboard_wall", {"w": 290, "h": 72, "seed": 32}, (290, 2), "Mood-board wall, linen pinboard"),
    "pinboard_cad": ("pinboard_wall", {"w": 120, "h": 52, "seed": 7, "board": "felt_green", "palette": ["paper", "paper", "g_white"],
                                       "card_w": (11, 15), "card_h": (8, 11), "gap_x": (5, 10), "gap_z": (4, 8)},
                     (120, 2), "Felt pinboard for tech packs (acoustic), brand green"),
    "rug_reception": ("rug", {"w": 108, "d": 78, "mat": "rug_wool"}, (108, 78), "Rug, wool, grey"),
    "rug_md": ("rug", {"w": 96, "d": 72, "mat": "rug_wool"}, (96, 72), "Rug, wool, sand"),
    "rug_lounge": ("rug", {"w": 120, "d": 90, "mat": "rug_wool"}, (120, 90), "Rug, wool"),
    "planter_l": ("planter", {"r": 10, "h": 20}, (20, 20), "Planter (large)"),
    "planter_m": ("planter", {"r": 8, "h": 16}, (16, 16), "Planter (medium)"),
    "fire_ext": ("fire_extinguisher", {}, (8, 8), "Fire extinguisher (wall bracket)"),
}

PLACEMENTS = []          # (key, x, y, facing, zone, z, label)


def P(key, x, y, facing=S, zone="", z=0.0, label=None):
    PLACEMENTS.append((key, x, y, facing, zone, z, label))


def bench_with_chairs(key, cx, cy, n, w, d, zone, chair="task_chair"):
    """Bench centred at (cx, cy), long axis east-west; chairs on both sides."""
    P(key, cx, cy, S, zone)
    L = n * w
    for k in range(n):
        x = cx - L / 2 + w * (k + 0.5)
        P(chair, x, cy + d + 16, N, zone)            # south row looks north
        P(chair, x, cy - d - 16, S, zone)            # north row looks south


# ---------------------------------------------------------------- Z01 entrance lobby
P("security_desk", 229, 120, N, "Z01")
P("task_chair", 229, 94, S, "Z01")
P("planter_l", 280, 195, S, "Z01", label="PLANT:pachira")
P("planter_m", 176, 196, S, "Z01", label="PLANT:calathea")
P("fire_ext", 295, 205, Wd, "Z01", z=4)
# ---------------------------------------------------------------- Z02 reception + waiting
P("reception_desk", 500, 150, Wd, "Z02")
P("exec_chair_black", 536, 122, Wd, "Z02")
P("exec_chair_black", 536, 178, Wd, "Z02")
P("sofa_84_sand", 380, 228, N, "Z02")
P("coffee_round", 380, 185, S, "Z02")
P("lounge_green", 332, 172, E, "Z02")
P("lounge_green", 428, 172, Wd, "Z02")
P("rug_reception", 380, 195, S, "Z02", z=0.45)
P("console", 457, 9, S, "Z02")
P("planter_l", 320, 230, S, "Z02", label="PLANT:pachira")
P("planter_m", 548, 232, S, "Z02", label="PLANT:calathea")
# ---------------------------------------------------------------- Z30 experience centre
for key, x in (("bay_104", 436), ("bay_104b", 544), ("bay_86", 677), ("bay_86b", 767)):
    P(key, x, -411, S, "Z30")
P("plinth", 500, -335, S, "Z30")
for key, x in (("mannequin_navy", 458), ("mannequin_sand", 486), ("mannequin_olive", 514), ("mannequin_white", 542)):
    P(key, x, -337, S, "Z30", z=8)
P("material_table", 722, -335, S, "Z30")
P("ec_counter", 610, -229, N, "Z30")
P("totem", 384, -300, E, "Z30")
P("planter_l", 850, -300, S, "Z30", label="PLANT:pachira")
P("fire_ext", 860, -405, Wd, "Z30", z=4)
# ---------------------------------------------------------------- Z08 boardroom
P("board_table", 675, -112, S, "Z08")
for x in (579, 611, 643, 675, 707, 739, 771):
    P("board_chair", x, -153, S, "Z08")
    P("board_chair", x, -71, N, "Z08")
P("exec_chair_black", 812, -112, Wd, "Z08")
P("screen_86", 489.1, -112, E, "Z08", z=40)
P("credenza_walnut", 498, -112, E, "Z08")
P("credenza_walnut", 856, -112, Wd, "Z08")
P("planter_m", 500, -195, S, "Z08", label="PLANT:calathea")
# ---------------------------------------------------------------- executive suite
P("desk_single", 628, 112, E, "Z10")
P("exec_chair_black", 660, 112, Wd, "Z10")
P("cc0:modern_arm_chair_01", 600, 212, N, "Z10")
P("cc0:modern_arm_chair_01", 650, 212, N, "Z10")
P("side_round", 625, 226, S, "Z10")
P("planter_m", 683, 235, S, "Z10", label="PLANT:calathea")
P("exec_desk_dir", 780, 164, S, "Z11")
P("exec_chair_black", 780, 199, N, "Z11")
P("visitor_chair", 765, 130, S, "Z11")
P("visitor_chair", 797, 130, S, "Z11")
P("credenza_oak", 780, 238, N, "Z11")
P("planter_m", 845, 232, S, "Z11", label="PLANT:calathea")
P("exec_desk_md", 1030, 158, S, "Z12")
P("exec_chair_cognac", 1030, 195, N, "Z12")
P("visitor_leather", 1010, 118, S, "Z12")
P("visitor_leather", 1050, 118, S, "Z12")
P("credenza_walnut", 1030, 237, N, "Z12")
P("sofa_72_sand", 880, 160, E, "Z12")
P("coffee_round", 916, 160, S, "Z12")
P("lounge_grey", 952, 160, Wd, "Z12")
P("rug_md", 918, 160, S, "Z12", z=0.45)
P("planter_l", 1072, 75, S, "Z12", label="PLANT:pachira")
# ---------------------------------------------------------------- Z07 merchandising open office
bench_with_chairs("bench3", 487.5, -742.5, 3, 55, 27.5, "Z07")
bench_with_chairs("bench3", 487.5, -582.5, 3, 55, 27.5, "Z07")
bench_with_chairs("bench2", 715, -742.5, 2, 55, 27.5, "Z07")
P("table_team", 725, -585, S, "Z07")
for x in (680, 710, 740, 770):
    P("task_chair_green", x, -623, S, "Z07")
    P("task_chair_green", x, -547, N, "Z07")
P("review_counter", 555, -437, N, "Z07")
P("pinboard_merch", 555, -428.8, N, "Z07", z=46)
P("mfp", 402, -440, N, "Z07")
P("lockers8", 857, -634, Wd, "Z07")
P("under_window_110", 857, -738, Wd, "Z07")
P("under_window_110", 857, -528, Wd, "Z07")
P("planter_l", 385, -820, S, "Z07", label="PLANT:pachira")
P("planter_m", 395, -470, S, "Z07", label="PLANT:calathea")
P("fire_ext", 372, -500, E, "Z07", z=4)
# ---------------------------------------------------------------- Z06 commercial & accounts, Z09 audit
bench_with_chairs("bench3", 170.5, -640.5, 3, 55, 27.5, "Z06")
bench_with_chairs("bench3", 170.5, -485, 3, 55, 27.5, "Z06")
P("desk_single", 175, -330, S, "Z06")
P("exec_chair_black", 175, -298, N, "Z06")
P("visitor_chair", 160, -370, S, "Z06")
P("visitor_chair", 190, -370, S, "Z06")
P("filing_120", 260, -241, N, "Z06")
P("mfp", 272, -726, S, "Z06")
P("planter_m", 60, -245, S, "Z06", label="PLANT:calathea")
P("fire_ext", 51, -300, E, "Z06", z=4)
P("table_audit", 175, -815, S, "Z09")
for x in (160, 190):
    P("visitor_chair", x, -847, S, "Z09")
    P("visitor_chair", x, -783, N, "Z09")
P("visitor_chair", 131, -815, E, "Z09")
P("tall_cab_90", 242, -830, Wd, "Z09")
# ---------------------------------------------------------------- Z05 HR & admin, Z04 guest workspace
bench_with_chairs("bench2", 250, -160, 2, 55, 27.5, "Z05")
P("meet_round", 300, -75, S, "Z05")
for x, y, f in ((300, -102, S), (273, -65, E), (327, -65, Wd)):
    P("visitor_chair", x, y, f, "Z05")
P("filing_96", 220, -19, N, "Z05")
P("planter_m", 175, -40, S, "Z05", label="PLANT:calathea")
P("table_guest", 10, -88, S, "Z04")
for x in (-17, 10, 37):
    P("visitor_chair_green", x, -122, S, "Z04")
    P("visitor_chair_green", x, -54, N, "Z04")
P("screen_55", 14, -150.9, S, "Z04", z=38)
P("planter_m", 92, -35, S, "Z04", label="PLANT:calathea")
# ---------------------------------------------------------------- strip: prayer (F), washrooms
P("wudu4", -12, -738, N, "Z34")
P("shoe_rack_36", 20, -760, N, "Z25")
for y in (-694, -658):
    P("cubicle", -25, y, E, "Z26")
    P("wc", -42, y, E, "Z26")
P("vanity2", -44.5, -570, E, "Z26")
for y in (-493, -457):
    P("cubicle", -25, y, E, "Z27")
    P("wc", -42, y, E, "Z27")
P("urinal", -42, -380, E, "Z27")
P("urinal", -42, -352, E, "Z27")
P("vanity2", -44.5, -270, E, "Z27")
P("wc", 467, -192, Wd, "Z28")
P("vanity1", 471, -132, Wd, "Z28")
P("wc", 467, -95, Wd, "Z28")
P("vanity1", 471, -28, Wd, "Z28")
P("wc", -42, -200, E, "Z29")
P("vanity1", 20, -212, S, "Z29")
# ---------------------------------------------------------------- room 8 design development
for y in (-225, -155, -85):
    P("cad_desk", 891.75, y, E, "Z14")
    P("task_chair", 923.5, y, Wd, "Z14")
P("plotter", 985, -24, N, "Z14")
P("table_layout", 1000, -140, S, "Z14")
P("plan_chest", 1028, -60, Wd, "Z14")
P("screen_65", 990, -255.9, S, "Z14", z=42)
P("pinboard_cad", 975, -10.8, N, "Z14", z=40)
P("shelf_lib_150", 958, -433, S, "Z15")
P("shelf_lib_low", 883, -318, E, "Z15")
P("bay_110_white", 950, -274, N, "Z15")
P("table_review", 960, -352, S, "Z15")
P("light_booth", 960, -356, S, "Z15", z=36)
P("stool", 940, -324, S, "Z15")
P("stool", 980, -324, S, "Z15")
P("printer_bench", 950, -583, S, "Z16")
for x in (905, 935, 965, 995):
    P("printer3d", x, -583, S, "Z16", z=31)
P("post_bench", 888, -530, E, "Z16")
P("desk_single", 975, -470, N, "Z16")
P("task_chair", 975, -502, S, "Z16")
P("dry_cabinet", 1025, -460, Wd, "Z16")
P("sewing", 900, -770, E, "Z17")
P("task_chair", 926, -770, Wd, "Z17")
P("sewing", 900, -715, E, "Z17")
P("task_chair", 926, -715, Wd, "Z17")
P("table_pattern", 1005, -760, E, "Z17")
for x in (905, 935, 965):
    P("dress_form", x, -655, S, "Z17")
P("steam", 930, -609, N, "Z17")
P("bay_72_white", 1003, -612, N, "Z17")
# Global Design Studio (master plan zones: creative workstations, trend/mood-board wall, collection
# display + buyer meeting, technical design = CAD room, fabric library = Z15, storage = Z19)
for cy in (-1120, -960):
    P("bench_design", 1253, cy, S, "Z18")
    for x in (1221.5, 1284.5):
        P("task_chair_green", x, cy + 31.5 + 16, N, "Z18")
        P("task_chair_green", x, cy - 31.5 - 16, S, "Z18")
P("moodboard", 1157.8, -1055, E, "Z18", z=18)
P("table_trend", 1240, -800, S, "Z18")
for x in (1210, 1240, 1270):
    P("stool", x, -837, S, "Z18")
    P("stool", x, -763, N, "Z18")
P("table_present", 1215, -660, E, "Z18")
for y in (-705, -675, -645, -615):
    P("visitor_chair", 1177, y, E, "Z18")
    P("visitor_chair", 1253, y, Wd, "Z18")
P("screen_86", 1215, -531.1, N, "Z18", z=40)
P("bay_120_white", 1314, -620, Wd, "Z18")
P("planter_l", 1300, -880, S, "Z18", label="PLANT:pachira")
P("shelf_store", 1157, -516, S, "Z19")
P("shelf_store72", 1287, -516, S, "Z19")
P("shelf_store", 1157, -446, N, "Z19")
P("shelf_store", 1260, -446, N, "Z19")
# ---------------------------------------------------------------- support
P("pantry", 888.5, -1150, E, "Z20")
P("fridge", 890, -1058, E, "Z20")
P("water", 884, -1030, E, "Z20")
for cy in (-1170, -1020):
    P("table_dining", 990, cy, S, "Z20")
    for x in (954, 978, 1002, 1026):
        P("dining_chair", x, cy - 32, S, "Z20")
        P("dining_chair", x, cy + 32, N, "Z20")
P("planter_l", 1058, -1232, S, "Z20", label="PLANT:pachira")
P("sofa_96_green", 960, -1531, S, "Z21")
P("coffee_round", 960, -1478, S, "Z21")
P("lounge_grey", 920, -1428, N, "Z21")
P("lounge_grey", 1000, -1428, N, "Z21")
P("rug_lounge", 960, -1485, S, "Z21", z=0.45)
P("screen_75", 877.1, -1400, E, "Z21", z=36)
P("table_training", 975, -1330, S, "Z21")
for x in (945, 975, 1005):
    P("visitor_chair_green", x, -1362, S, "Z21")
    P("visitor_chair_green", x, -1298, N, "Z21")
P("planter_l", 1035, -1530, S, "Z21", label="PLANT:pachira")
P("shoe_rack", 1166, -1325, E, "Z23")
P("quran_shelf", 1240, -1435, S, "Z23", z=0)
P("quran_shelf_f", -7, -886, S, "Z25", z=0)
P("wudu5", 1240, -1233, N, "Z24")
for x, y, f in ((371, -600, E), (1095, -870, Wd), (881, -1260, E), (1145, -1200, Wd), (50, -880, E), (1050, -230, S)):
    P("fire_ext", x, y, f, "", z=4)

# ------------------------------------------------------------------------------------------ wall finishes & branding
# (kind, x0, x1, y0, y1, z0, z1, material/params, label)
FINISHES = [
    ("slatwall", 168, 296, 0, 3, 0, 108, "oak_slat", "Lobby brand wall: vertical oak slats", S),
    ("panel", 182, 282, 3, 4.2, 38, 82, "plastic_white", "Lobby brand panel (white solid surface)", S),
    ("slatwall", 562, 565, 80, 240, 0, 110, "oak_slat", "Reception feature wall: fluted oak", Wd),
    ("slatwall", 367, 370, -410, -232, 0, 108, "oak_slat", "Experience centre story wall frame", E),
    ("panel", 370, 371.2, -400, -242, 30, 96, "plastic_white", "Experience centre story panel", E),
    ("slatwall", 485, 488, -205, -19, 0, 108, "oak_slat", "Boardroom media wall", E),
    ("slatwall", 672, 863, -13, -10, 0, 108, "walnut", "Boardroom acoustic walnut slats", N),
    ("panel", 930, 1072, 244, 247, 0, 102, "walnut", "MD feature wall, walnut", N),
    ("panel", 995, 1065, 243.6, 244, 52, 72, "plastic_white", "MD logo plate", N),
    ("slatwall", 703, 1086, 0, 3, 0, 102, "oak_slat", "Executive corridor oak wall", S),
    ("panel", 561, 562, 118, 202, 56, 82, "plastic_white", "Reception logo plate (backlit)", Wd),
    ("panel", 1155, 1157, -1205, -905, 0, 108, "pinboard_linen", "Mood-board wall backing", E),
]
# client logos (actual artwork from the business card / company profile): (material, centre x, y, z bottom, width in, facing)
LOGOS = [
    ("logo_zf", 232, 4.3, 62, 56, S), ("logo_s2_ltd", 208, 4.3, 46, 36, S), ("logo_s2_unit1", 256, 4.3, 46, 36, S),
    ("tagline", 232, 4.3, 40, 64, S),
    ("logo_zf", 560.8, 160, 61.5, 70, Wd),
    ("logo_zf", 371.4, -321, 66, 60, E), ("logo_s2_ltd", 371.4, -295, 50, 40, E), ("logo_s2_unit1", 371.4, -347, 50, 40, E),
    ("tagline", 371.4, -321, 42, 70, E),
    ("logo_zf", 1030, 243.4, 56, 52, N),
]

# ------------------------------------------------------------------------------------------ ceilings
# (kind, cx, cy, z_bottom, params, zone)
CEILING = []


def C_(kind, cx, cy, z, zone, **kw):
    CEILING.append((kind, cx, cy, z, kw, zone))


C_("slat_raft", 395, 190, 98.5, "Z02", w=150, d=96)
C_("slat_raft", 1030, 160, 98.5, "Z12", w=110, d=72)
for x0, x1 in ((510, 581), (581, 652), (652, 724), (724, 795)):            # boardroom rafts between beams
    C_("raft", (x0 + x1) / 2, -112, 104.0, "Z08", w=x1 - x0 - 12, d=120, mat="felt_green")
# merchandising: felt baffles between the room 6 beams (north-south fins)
for y0, y1 in ((-838, -769.2), (-769.2, -700.4), (-700.4, -631.7), (-631.7, -562.9), (-562.9, -494.1), (-494.1, -428)):
    for xs, xe in ((380, 606), (626, 856)):
        x = xs + 6
        k = 0
        while x < xe - 4:
            C_("baffle", x, (y0 + y1) / 2, 101.5, "Z07", L=(y1 - y0) - 10, mat="felt_green" if k % 6 == 3 else "felt_grey")
            x += 16
            k += 1

# ------------------------------------------------------------------------------------------ lighting
# fixtures: (kind, x, y, z_bottom, params, zone); kinds: lin (linear pendant, along x unless rot=90), halo,
# down (downlight), spot (track spot with aim), track (rail), pendant_cc0, cove (LED strip)
LIGHTS = []


def L_(kind, x, y, z, zone, **kw):
    LIGHTS.append((kind, x, y, z, kw, zone))


# lobby
L_("lin", 210, 60, 84, "Z01", L=96, rot=90, temp=3500)
L_("lin", 210, 170, 84, "Z01", L=72, rot=90, temp=3500)
for x in (190, 232, 274):
    L_("spot", x, 40, 110, "Z01", aim=(x, 0, 60), temp=3000, w=60)
# reception
L_("halo", 380, 185, 80, "Z02", r=20, temp=3000)
L_("lin", 500, 150, 82, "Z02", L=96, rot=90, temp=3500)
for y in (95, 135, 175, 215):
    L_("spot", 545, y, 110, "Z02", aim=(565, y, 50), temp=3000, w=40)
for x in (330, 450):
    L_("down", x, 40, 110, "Z02", temp=3500)
L_("down", 394, -60, 110, "Z03", temp=3500)
L_("down", 394, -160, 110, "Z03", temp=3500)
# experience centre: tracks on the beams at y -287.8 and -356.6, spots aimed at bays / plinth / table
for yb in (-287.8, -356.6):
    L_("track", 490, yb, 102, "Z30", L=230)
    L_("track", 743, yb, 102, "Z30", L=230)
for x, tx, ty, tz in ((420, 436, -405, 60), (460, 470, -405, 60), (530, 544, -405, 60), (570, 560, -405, 60),
                      (650, 677, -405, 60), (700, 690, -405, 60), (750, 767, -405, 60), (790, 780, -405, 60)):
    L_("spot", x, -356.6, 100, "Z30", aim=(tx, ty, tz), temp=3000, w=45)
for x, tx, ty, tz in ((455, 470, -337, 45), (500, 500, -337, 45), (545, 530, -337, 45), (690, 700, -335, 36),
                      (740, 745, -335, 36), (400, 371, -320, 70), (440, 371, -300, 60), (600, 610, -229, 40), (760, 700, -229, 40)):
    L_("spot", x, -287.8, 100, "Z30", aim=(tx, ty, tz), temp=3000, w=45)
L_("lin", 722, -335, 76, "Z30", L=120, temp=3500)
# boardroom
L_("lin", 627, -112, 80, "Z08", L=96, temp=3500)
L_("lin", 723, -112, 80, "Z08", L=96, temp=3500)
for x in (545, 805):
    for y in (-185, -40):
        L_("down", x, y, 110, "Z08", temp=3500)
for y in (-185, -150, -112, -74, -40):
    L_("spot", 500, y, 110, "Z08", aim=(485, y, 50), temp=3000, w=35)
# executive suite
L_("lin", 628, 112, 82, "Z10", L=60, rot=90, temp=3500)
L_("down", 600, 200, 110, "Z10", temp=3000)
L_("lin", 780, 164, 82, "Z11", L=60, temp=3500)
L_("down", 780, 230, 110, "Z11", temp=3000)
L_("lin", 1030, 158, 84, "Z12", L=72, temp=3500)
L_("halo", 916, 160, 82, "Z12", r=16, temp=3000)
for x in (950, 1000, 1050):
    L_("spot", x, 225, 110, "Z12", aim=(x, 247, 60), temp=3000, w=40)
for x in (740, 820, 900, 980, 1060):
    L_("down", x, 27, 110, "Z13", temp=3000)
# merchandising, commercial, HR, guest, audit
for cx in (487.5,):
    for cy in (-742.5, -582.5):
        L_("lin", cx, cy, 80, "Z07", L=150, temp=4000)
L_("lin", 715, -742.5, 80, "Z07", L=100, temp=4000)
L_("lin", 725, -585, 80, "Z07", L=130, temp=4000)
L_("lin", 555, -460, 84, "Z07", L=200, temp=4000)
for cy in (-640.5, -485):
    L_("lin", 170.5, cy, 80, "Z06", L=150, temp=4000)
L_("lin", 175, -330, 82, "Z06", L=60, temp=4000)
for x, y in ((330, -300), (330, -420), (330, -540), (330, -660), (330, -780), (68, -300), (68, -420), (68, -560), (68, -700), (68, -840), (175, -260)):
    L_("down", x, y, 110, "Z06", temp=4000)
for x, y in ((390, -470), (390, -800), (840, -800), (840, -470), (616, -800), (616, -470)):
    L_("down", x, y, 110, "Z07", temp=4000)
L_("lin", 175, -815, 80, "Z09", L=60, temp=4000)
L_("lin", 250, -160, 80, "Z05", L=100, temp=4000)
L_("down", 300, -75, 110, "Z05", temp=3500)
L_("lin", 10, -88, 80, "Z04", L=72, temp=4000)
for y in (-40, -120, -200):
    L_("down", 135, y, 110, "Z31", temp=3500)
# design development
for y in (-225, -155, -85):
    L_("lin", 915, y, 82, "Z14", L=60, rot=90, temp=4000)
L_("lin", 985, -140, 82, "Z14", L=60, temp=4000)
L_("lin", 958, -350, 82, "Z15", L=96, temp=4000)
L_("lin", 958, -520, 82, "Z16", L=96, temp=4000)
L_("lin", 958, -700, 82, "Z17", L=120, rot=90, temp=4000)
for cy in (-1120, -960):
    L_("lin", 1253, cy, 82, "Z18", L=110, temp=4000)
L_("lin", 1240, -800, 84, "Z18", L=80, temp=4000)
L_("lin", 1215, -660, 82, "Z18", L=96, rot=90, temp=3500)
L_("track", 1175, -1055, 104, "Z18", L=280, rot=90)
for y in (-1180, -1120, -1060, -1000, -940):
    L_("spot", 1175, y, 102, "Z18", aim=(1157, y, 54), temp=3500, w=50)
L_("lin", 1215, -481, 90, "Z19", L=96, temp=4000)
# support
for cy in (-1170, -1020):
    for x in (960, 990, 1020):
        L_("pendant_cc0", x, cy, 0, "Z20")
L_("lin", 905, -1150, 86, "Z20", L=96, rot=90, temp=3500)
L_("halo", 960, -1478, 82, "Z21", r=18, temp=3000)
L_("lin", 975, -1330, 82, "Z21", L=96, temp=3500)
for x, y in ((1200, -1400), (1280, -1400), (1200, -1320), (1280, -1320)):
    L_("down", x, y, 110, "Z23", temp=3000)
for x in (1200, 1280):
    L_("down", x, -1246, 110, "Z24", temp=3500)
for x, y in ((-7, -860), (-7, -790), (-7, -740)):
    L_("down", x, y, 110, "Z25", temp=3000)
for y in (-690, -630, -570):
    L_("down", -7, y, 110, "Z26", temp=3500)
for y in (-480, -400, -330, -270):
    L_("down", -7, y, 110, "Z27", temp=3500)
for y in (-170, -60):
    L_("down", 452, y, 110, "Z28", temp=3500)
L_("down", -4, -188, 110, "Z29", temp=3500)
for x in (420, 520, 620, 720, 820):
    L_("down", x, -867, 110, "Z33", temp=3500)
for x, y in ((920, -872), (1000, -872), (1072, -800), (1072, -700), (1072, -600), (1072, -500), (1100, -330)):
    L_("down", x, y, 110, "Z22", temp=3500)
for x, y in ((1114, -1000), (1114, -1150), (1114, -1300)):
    L_("down", x, y, 110, "Z32", temp=3500)

# under-ceiling AC units (VRF indoor units, between beams; capacity by MEP engineer): (x, y, rot, zone)
AC_UNITS = [(490, -666, 0, "Z07"), (740, -666, 0, "Z07"), (490, -528, 0, "Z07"), (740, -528, 0, "Z07"),
            (170, -560, 0, "Z06"), (170, -400, 0, "Z06"), (250, -100, 0, "Z05"), (616, -322, 0, "Z30"),
            (616, -190, 90, "Z08"), (430, 120, 90, "Z02"), (1025, 120, 90, "Z12"), (780, 120, 90, "Z11"),
            (958, -140, 0, "Z14"), (1240, -1040, 0, "Z18"), (1240, -720, 0, "Z18"), (975, -1100, 0, "Z20"),
            (975, -1400, 0, "Z21"), (1240, -1360, 0, "Z23"), (230, 60, 90, "Z01")]
SMOKE_DETECTORS = [(232, 120), (435, 120), (616, -300), (675, -112), (490, -630), (740, -630), (170, -560), (250, -120),
                   (958, -140), (958, -350), (958, -520), (958, -720), (1240, -1050), (1215, -680), (975, -1080), (975, -1400),
                   (1240, -1360), (635, 120), (780, 150), (975, 150), (614, -867), (988, -872), (1072, -650)]
EXIT_SIGNS = [(230, 244, S), (1101, -219, S), (1107, -1440, N), (614, -846, S)]

# wet rooms with porcelain wall tiles up to 96 in (zone ids)
TILED_ZONES = ["Z24", "Z26", "Z27", "Z28", "Z29", "Z34"]
WALL_CLOCKS = [(1240, -1438.5, 82, S), (975, -1243.5, 84, N), (-7, -888.5, 80, S)]
