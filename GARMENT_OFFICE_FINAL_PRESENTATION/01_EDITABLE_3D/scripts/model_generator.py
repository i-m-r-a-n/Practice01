"""
Stage II Knitting Apparel Ltd. / Zara Fashion - ground floor, Blender model generator.

Phase 1  building shell from the A-100 survey plan: slab, walls, 48" partitions, openings, stairs,
         columns, beams, deck, dimensions, cameras, lighting.
Phase 2  office-only furnished layout on the same shell (zoning from A-103, revised for office use).

Run headless with Blender 5.2:
    blender -b --factory-startup --python model_generator.py -- OUT_DIR --phase 1
    blender -b --factory-startup --python model_generator.py -- OUT_DIR --phase 2
Add --no-render to skip the preview images.

Plan units are inches, exactly as on the drawings. Plan x = east -> Blender +X; plan y = south (toward
the main gate) -> Blender -Y; height -> +Z. Origin = A-100 (0, 0): inner north-west corner of room 1.
1 inch = 25.4 mm. Every value has a status in SCHEDULE (written to dimension_schedule.csv):
MEASURED (written on a sketch), DERIVED (sum of measured values), RESOLVED (one value chosen where
sketches disagree), ASSUMED / STANDARD / PHOTO-EST (common-sense values where nothing was measured).
"""
import csv
import math
import os
import sys

import bmesh
import bpy

ARGV = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = os.path.abspath(ARGV[0]) if ARGV and not ARGV[0].startswith("--") else os.getcwd()
PHASE = ARGV[ARGV.index("--phase") + 1] if "--phase" in ARGV else "1"
RENDER = "--no-render" not in ARGV
IN = 0.0254                                   # metres per inch

# =====================================================================================================
# PARAMETERS - plan (inches), A-100
# =====================================================================================================
FRONT = 247            # front-row inner depth (rooms 1, 3, 4): RESOLVED from 236 / 249 / 244 / 242.5
MID_S, MID_N = -10, -891   # middle block inner faces: depth 881 DERIVED (both sides of the block agree)
HALL_S = -843          # hallway 48" MEASURED
R6_N, R6_S = -838, -219    # room 6 depth 619 MEASURED
R5_N, R5_S = -214, -10     # room 5 depth 204 MEASURED
R7_E = 362             # room 7 east face = room 3 west face (305) + 57" opening
R7_LOW_W = 110         # 362 - (195 + 57)
STRIP_E = 41           # washroom row east face (wall 41..46); jog 64" MEASURED
R2_W, R2_E, R2_N = -55, 105, -221   # room 2 160 x 211 MEASURED
JOG = -231
R8_W, R8_E = 876, 1326     # room 8 width 450 ASSUMED (not measured)
R8_N = MID_N - 657         # 657" MEASURED from the north-west corner to the hallway door
STAIR_T = 103              # north-east stair depth ASSUMED (one equation, three unknowns)
G1, G2 = 86, 59            # wall between room 8 windows 3-4 and 4-5 ASSUMED
SE_N = MID_S - 204         # south-east stair 204" MEASURED
ENG_S, ENG_N = SE_N - 5, SE_N - 5 - 213   # engine room (sub-station) 213" MEASURED
D60_FROM_N = 7.5           # room 3 / 4 door: 7.5" from the corner on the room 4 sketch (A-100 drew 9)
HALL_DOOR = 42             # hallway -> room 8 door: width not written; photo shows jambs; 3'-6" standard
T_IN, T_OUT = 5, 10        # wall thickness ASSUMED (not measured)

# =====================================================================================================
# PARAMETERS - heights (inches); none measured except the 48" walls and window heights
# =====================================================================================================
DECK_H = 114           # floor to underside of steel deck: PHOTO-EST (9'-6")
HALF_H = 48            # "Wall Height 48" written on the sketches: MEASURED
LINTEL = 84            # door and window heads: STANDARD 7'-0" lintel level
GATE_H = 96            # main gate head: PHOTO-EST
SLAB_T, DECK_T = 6, 4  # graphic thicknesses: ASSUMED
BEAM_SEC = (5, 12)     # secondary beam width, depth: PHOTO-EST
BEAM_MAIN = (8, 16)    # main beam width, depth: PHOTO-EST
COL_W = 10             # steel column size: PHOTO-EST
TREAD = 11             # stair tread: STANDARD
FLOOR_TO_FLOOR = DECK_H + DECK_T

# =====================================================================================================
# GEOMETRY - as-built walls (A-100). ops: (id, kind, a, b, label[, window height])
# kind: "ext" outside wall, "int" full-height inside wall, "half" 48" wall, "part" light partition
# =====================================================================================================


def W(wid, name, axis, c0, c1, a, b, kind, ops=(), status="MEASURED", note=""):
    return dict(id=wid, name=name, axis=axis, c0=c0, c1=c1, a=a, b=b, kind=kind,
                ops=[list(o) for o in ops], status=status, note=note, treat=None)


w1 = R8_N + STAIR_T + 5 + 10           # room 8 east windows, from the measured chain on the sketch
w2 = w1 + 60 + 16
w3 = w2 + 71 + 107
w4 = w3 + 114 + G1
w5 = w4 + 114 + G2
HALL_DOOR_A = MID_N + (48 - HALL_DOOR) / 2

WALLS = [
    W("EW01", "Front facade with main gate", "h", FRONT, FRONT + T_OUT, -10, 1098, "ext",
      [("D01", "gate", 160, 300, 'Main gate 140"')]),
    W("EW02", "Room 1 west wall", "v", -10, 0, 0, FRONT + T_OUT, "ext"),
    W("EW03", "Room 4 east wall", "v", 1088, 1098, 0, FRONT + T_OUT, "ext"),
    W("IW01", "Row wall, rooms 1 and 2", "h", MID_S, 0, -65, 305, "int",
      [("D02", "door", 62, 104, 'D42 room 1 - room 2')]),
    W("IW02", "Row wall over the room 3 - room 7 opening", "h", MID_S, 0, 305, 362, "int",
      [("D03", "door", 305, 362, '57" opening room 3 - room 7')]),
    W("PW01", "Row wall, room 3 - room 5 (48 in)", "h", MID_S, 0, 362, 565, "half"),
    W("IW03", "Row wall, room 4 - rooms 5 and 8", "h", MID_S, 0, 565, 1098, "int"),
    W("EW04", "South wall of the east stair", "h", MID_S, 0, 1098, 1336, "ext"),
    W("IW04", "Room 1 - room 3", "v", 300, 305, 0, FRONT, "int",
      [("D04", "door", 15, 62, 'D47 room 1 - room 3')]),
    W("IW05", "Room 3 - room 4", "v", 565, 570, 0, FRONT, "int",
      [("D05", "door", D60_FROM_N, D60_FROM_N + 60, 'D60 room 3 - room 4')]),
    W("EW05", "Middle block north wall", "h", MID_N - T_OUT, MID_N, -65, 876, "ext"),
    W("EW06", "Washroom row west wall", "v", -65, -55, MID_N - T_OUT, JOG, "ext", status="ASSUMED",
      note="position assumed in line with room 2 west wall"),
    W("EW07", "Room 2 west wall", "v", -65, -55, JOG, 0, "ext"),
    W("IW06", "Room 2 north wall (64 in jog)", "h", JOG, R2_N, -55, R7_LOW_W, "int"),
    W("IW07", "Room 2 - room 7", "v", R2_E, R7_LOW_W, JOG, MID_S, "int",
      [("W01", "win", -174, -60, 'W114 room 2 - room 7', 48)]),
    W("PW02", "Room 2 washroom, east", "v", 47, 50, R2_N, -155, "part",
      [("D06", "door", -181.5, -155, 'D26.5 washroom')]),
    W("PW03", "Room 2 washroom, south", "h", -155, -152, R2_W, 50, "part"),
    W("IW08", "Washroom row - room 7", "v", STRIP_E, 46, MID_N, JOG, "int",
      [("D07", "door", -834, -770, '64" store opening'), ("D08", "door", -636, -606, 'D30 washroom 2'),
       ("D09", "door", -432, -402, 'D30 washroom 1')]),
    W("PW04", "Washroom 1 - washroom 2", "h", -519, -514, R2_W, STRIP_E, "part", status="ASSUMED",
      note="midway between the two doors"),
    W("PW05", "Room 7 - rooms 5 and 6 (48 in)", "v", R7_E, 367, HALL_S, MID_S, "half",
      [("D10", "door", -58, -10, '48" opening room 7 - room 5')]),
    W("PW06", "Hallway - room 6 (48 in)", "h", HALL_S, R6_N, R7_E, 866, "half",
      [("D11", "door", 783, 835, '52" opening hallway - room 6')]),
    W("PW07", "Room 5 - room 6 (48 in)", "h", R6_S, R5_N, 367, 866, "half",
      [("D12", "door", 367, 416, '49" opening room 5 - room 6')]),
    W("IW09", "Rooms 5, 6, hallway - room 8", "v", 866, 876, MID_N, MID_S, "int",
      [("D13", "door", HALL_DOOR_A, HALL_DOOR_A + HALL_DOOR, 'Hallway - room 8 (42" standard)'),
       ("W02", "win", -795, -682, 'W113 room 6 - room 8', 54), ("W03", "win", -585, -472, 'W113 room 6 - room 8', 54),
       ("W04", "win", -375, -262, 'W113 room 6 - room 8', 54), ("W05", "win", -172, -58, 'W114 room 5 - room 8', 37)]),
    W("EW08", "Room 8 west wall, north part", "v", 866, 876, R8_N - T_OUT, MID_N - T_OUT, "ext"),
    W("EW09", "Room 8 north wall", "h", R8_N - T_OUT, R8_N, 866, R8_E + T_OUT, "ext", status="ASSUMED",
      note="length depends on the assumed room 8 width"),
    W("EW10", "Room 8 east wall", "v", R8_E, R8_E + T_OUT, R8_N - T_OUT, 0, "ext",
      [("W06", "win", w1, w1 + 60, 'W60 room 8', 46), ("W07", "win", w2, w2 + 71, 'W71 room 8', 54),
       ("W08", "win", w3, w3 + 114, 'W114 room 8', 54), ("W09", "win", w4, w4 + 114, 'W114 room 8', 54),
       ("W10", "win", w5, w5 + 114, 'W114 room 8', 54)], status="ASSUMED",
      note="position from the assumed room 8 width; windows 3-4 placed with assumed piers"),
    W("IW10", "North-east stair, south wall", "h", R8_N + STAIR_T, R8_N + STAIR_T + 5, R8_E - 278, R8_E, "int",
      [("D14", "door", R8_E - 243, R8_E - 194, 'D49 north-east stair')], status="ASSUMED",
      note="depth of the stair room assumed"),
    W("IW11", "North-east stair, west wall", "v", R8_E - 278, R8_E - 273, R8_N, R8_N + STAIR_T, "int"),
    W("IW12", "Engine room (sub-station), north wall", "h", ENG_N - 5, ENG_N, R8_E - 170, R8_E, "int"),
    W("IW13", "Engine room (sub-station), west wall", "v", R8_E - 170, R8_E - 165, ENG_N - 5, ENG_S, "int",
      [("D15", "door", ENG_S - 49, ENG_S, 'D49 engine room')]),
    W("IW14", "South-east stair, north wall", "h", ENG_S, SE_N, R8_E - 282, R8_E, "int",
      [("D16", "door", R8_E - 251, R8_E - 199, 'D52 south-east stair')]),
    W("IW15", "South-east stair, west wall", "v", R8_E - 282, R8_E - 277, ENG_S, MID_S, "int"),
]

OUTLINE = [(-10, FRONT + 10), (1098, FRONT + 10), (1098, 0), (R8_E + 10, 0), (R8_E + 10, R8_N - 10),
           (866, R8_N - 10), (866, MID_N - 10), (-65, MID_N - 10), (-65, 0), (-10, 0)]

ROOMS = {   # as-built rooms (A-100): polygon, label
    "R1": ([(0, 0), (300, 0), (300, FRONT), (0, FRONT)], "ROOM 1  LOBBY"),
    "R2": ([(R2_W, R2_N), (R2_E, R2_N), (R2_E, MID_S), (R2_W, MID_S)], "ROOM 2"),
    "R3": ([(305, 0), (565, 0), (565, FRONT), (305, FRONT)], "ROOM 3"),
    "R4": ([(570, 0), (1088, 0), (1088, FRONT), (570, FRONT)], "ROOM 4"),
    "R5": ([(367, R5_N), (866, R5_N), (866, R5_S), (367, R5_S)], "ROOM 5"),
    "R6": ([(367, R6_N), (866, R6_N), (866, R6_S), (367, R6_S)], "ROOM 6"),
    "R7": ([(46, MID_N), (R7_E, MID_N), (R7_E, MID_S), (R7_LOW_W, MID_S), (R7_LOW_W, JOG), (46, JOG)], "ROOM 7"),
    "HALL": ([(R7_E, MID_N), (866, MID_N), (866, HALL_S), (R7_E, HALL_S)], "HALLWAY"),
    "STRIP": ([(R2_W, MID_N), (STRIP_E, MID_N), (STRIP_E, JOG), (R2_W, JOG)], "STORE + WC 1, 2"),
    "R8": ([(R8_W, R8_N), (R8_E - 278, R8_N), (R8_E - 278, R8_N + STAIR_T + 5), (R8_E, R8_N + STAIR_T + 5),
            (R8_E, ENG_N - 5), (R8_E - 170, ENG_N - 5), (R8_E - 170, ENG_S), (R8_E - 282, ENG_S),
            (R8_E - 282, MID_S), (R8_W, MID_S)], "ROOM 8"),
    "ENG": ([(R8_E - 165, ENG_N), (R8_E, ENG_N), (R8_E, ENG_S), (R8_E - 165, ENG_S)], "ENGINE ROOM (SUB-STATION)"),
}

# columns: positions not measured. Estimated from the site photos: room 7 columns under the sketched beam
# (x 300), room 6 and room 8 columns on the middle line of each room, rows following the 210" rhythm of the
# room 6 window piers (y -633, -423) measured on the room 6 sketch.
COLUMNS = [(300, -217), (300, -423), (300, -633), (300, -843),
           (616, -217), (616, -423), (616, -633), (616, -843),
           (1101, -423), (1101, -633), (1101, -843)]

# =====================================================================================================
# MEASUREMENT SCHEDULE: (id, group, element, written on sketch, value, unit, status, source, note)
# =====================================================================================================
SCHEDULE = [
    ("OV01", "Overall", "Front width, outside faces", "92'-4\" (A-100)", 1108, "in", "DERIVED", "A-100", "rooms 300 + 260 + 518 + walls"),
    ("OV02", "Overall", "Depth, west side (front facade to middle block north wall)", "96'-6\" (A-100)", 1158, "in", "DERIVED", "A-100", ""),
    ("OV03", "Overall", "Depth, east side (front facade to room 8 north wall)", "151'-3\" (A-100)", 1815, "in", "DERIVED", "A-100", ""),
    ("OV04", "Overall", "Gross floor area incl. walls", "12,888 sft (A-100)", 12888, "sft", "DERIVED", "A-100", "changes if room 8 width changes"),
    ("R1W", "Room 1", "Width", "300", 300, "in", "MEASURED", "Room 1 sketch", "lobby, main stair, main gate"),
    ("R1D", "Room 1", "Depth", "236 (room 1 sketch) / 249 (room 3 sketch)", 247, "in", "RESOLVED", "A-100", "front-row line shared with rooms 3 and 4"),
    ("R2W", "Room 2", "Width", "160", 160, "in", "MEASURED", "Room 2 sketch", ""),
    ("R2D", "Room 2", "Depth", "211", 211, "in", "MEASURED", "Room 2 sketch", "221 on the room 7 side incl. 10\" wall"),
    ("R2WC", "Room 2", "Washroom inside room 2", "102 x 66", 102, "in", "MEASURED", "Room 2 sketch", "66\" deep"),
    ("R3W", "Room 3", "Width", "255 / 265", 260, "in", "RESOLVED", "Room 3 sketch", "mean of the two sides"),
    ("R3D", "Room 3", "Depth", "247 - 249", 247, "in", "RESOLVED", "Room 3 sketch", ""),
    ("R4W", "Room 4", "Width", "518 / 518", 518, "in", "MEASURED", "Room 4 sketch", ""),
    ("R4D", "Room 4", "Depth", "244 / 242.5 (7.5 + 60 + 175)", 247, "in", "RESOLVED", "Room 4 sketch", "drawn on the front-row line, 3 - 4.5\" over the measured depth"),
    ("R5W", "Room 5", "Width", "499 (49 + 450) / 504", 499, "in", "RESOLVED", "Room 5 sketch", "aligned with room 6"),
    ("R5D", "Room 5", "Depth", "42 + 114 + 48 = 204", 204, "in", "MEASURED", "Room 5 sketch", ""),
    ("R6W", "Room 6", "Width", "49 + 450 = 499", 499, "in", "MEASURED", "Room 6 sketch", ""),
    ("R6D", "Room 6", "Depth", "43 + 113 + 97 + 113 + 97 + 113 + 43 = 619", 619, "in", "MEASURED", "Room 6 sketch", ""),
    ("R7WL", "Room 7", "Width, lower part", "195 + 57 = 252", 252, "in", "DERIVED", "Room 7 sketch", ""),
    ("R7WU", "Room 7", "Width, upper part", "234 (written)", 316, "in", "RESOLVED", "Room 7 sketch", "252 + 64\" jog; 234 does not fit the hallway (504) and rooms 5 / 6 (499)"),
    ("R7J", "Room 7", "Jog at the washroom row", "64", 64, "in", "MEASURED", "Room 7 sketch", ""),
    ("R7WW", "Room 7", "Lower west wall", "55 + 114 + 52 = 221", 221, "in", "MEASURED", "Room 7 sketch", ""),
    ("R7D", "Room 7", "Depth", "649 + 10 + 221 = 880 / 48 + 619 + 204 + walls = 881", 881, "in", "DERIVED", "Room 5, 6, 7 sketches", ""),
    ("HALW", "Hallway", "Width", "48", 48, "in", "MEASURED", "Room 7 sketch", ""),
    ("HALL", "Hallway", "Length", "504", 504, "in", "MEASURED", "A-100", "= room 6 width + 5\" wall"),
    ("STW", "Washroom row", "Width", "not measured", 96, "in", "ASSUMED", "A-100", "outer wall in line with room 2"),
    ("STL", "Washroom row", "Length", "160 + 30 + 174 + 30 + 134 + 64 + 57 = 649", 660, "in", "RESOLVED", "Room 7 sketch", "11\" added to the first piece"),
    ("R8W", "Room 8", "Width", "not measured", 450, "in", "ASSUMED", "A-100", "north-east stair 273 + 5 + 172"),
    ("R8WN", "Room 8", "West wall, north corner to hallway door", "657", 657, "in", "MEASURED", "Room 8 sketch", ""),
    ("R8L", "Room 8", "Length", "657 + 881", 1538, "in", "DERIVED", "Room 8 sketch", ""),
    ("NESW", "North-east stair", "Width", "30 + 49 + 194 = 273", 273, "in", "MEASURED", "Room 8 sketch", ""),
    ("NESD", "North-east stair", "Depth", "not measured", STAIR_T, "in", "ASSUMED", "A-100", "east wall 1538 minus measured pieces = depth + 2 piers"),
    ("R8G1", "Room 8", "Wall between windows 3 and 4", "not written", G1, "in", "ASSUMED", "A-100", ""),
    ("R8G2", "Room 8", "Wall between windows 4 and 5", "not written", G2, "in", "ASSUMED", "A-100", ""),
    ("R8P1", "Room 8", "Stair wall to window 1", "10", 10, "in", "MEASURED", "Room 8 sketch", ""),
    ("R8P2", "Room 8", "Window 1 to window 2", "16", 16, "in", "MEASURED", "Room 8 sketch", ""),
    ("R8P3", "Room 8", "Window 2 to window 3", "49 + 10 + 48 = 107", 107, "in", "MEASURED", "Room 8 sketch", ""),
    ("R8P4", "Room 8", "Window 5 to engine room", "252", 252, "in", "MEASURED", "Room 8 sketch", ""),
    ("ENGW", "Engine room", "Width", "165", 165, "in", "MEASURED", "Room 8 sketch", "door sign reads SUB-STATION"),
    ("ENGD", "Engine room", "Depth", "96 + 68 + 49 = 213", 213, "in", "MEASURED", "Room 8 sketch", ""),
    ("SESW", "South-east stair", "Width", "277", 277, "in", "MEASURED", "Room 8 sketch", "north wall 26 + 52 + 34 + engine wall"),
    ("SESD", "South-east stair", "Depth", "204", 204, "in", "MEASURED", "Room 8 sketch", "A-100 v3 drew 209; corrected"),
    ("WT1", "Walls", "Inside wall thickness", "not measured", T_IN, "in", "ASSUMED", "A-100", ""),
    ("WT2", "Walls", "Outside wall and row wall thickness", "not measured", T_OUT, "in", "ASSUMED", "A-100", ""),
    ("WH1", "Walls", "Low wall height (rooms 3, 5, 6, 7, hallway)", "Wall Height 48", HALF_H, "in", "MEASURED", "Room 5, 6, 7 sketches", "confirmed in photos"),
    ("H01", "Heights", "Floor to underside of steel deck", "not measured", DECK_H, "in", "PHOTO-EST", "Site photos", "9'-6\""),
    ("H02", "Heights", "Door and window head (lintel level)", "not measured", LINTEL, "in", "STANDARD", "", "7'-0\""),
    ("H03", "Heights", "Main gate head", "not measured", GATE_H, "in", "PHOTO-EST", "Site photos", ""),
    ("H04", "Heights", "Secondary beam depth below deck", "not measured", BEAM_SEC[1], "in", "PHOTO-EST", "Site photos", ""),
    ("H05", "Heights", "Main beam depth below deck", "not measured", BEAM_MAIN[1], "in", "PHOTO-EST", "Site photos", ""),
    ("H06", "Heights", "Floor to floor (stair rise)", "not measured", FLOOR_TO_FLOOR, "in", "ASSUMED", "", "deck height + deck"),
    ("H07", "Heights", "Gate steps (2), heights", "not measured", 14, "in", "PHOTO-EST", "Site photos", "7\" + 7\", treads 12\" and 24\""),
    ("ST1", "Stairs", "Room 1 stair footprint", "about 160 wide", 160, "in", "MEASURED", "Room 1 sketch", "configuration: up from the back along the outer wall, landing at the front (owner + photos)"),
    ("ST2", "Stairs", "Stair tread", "not measured", TREAD, "in", "STANDARD", "", "risers = floor to floor / count"),
    ("ST3", "Stairs", "North-east and south-east stair layouts", "not surveyed", 0, "", "ASSUMED", "", "drawn as U-stairs inside the measured stair rooms"),
    ("STR1", "Structure", "Room 7 beam line", "drawn on the room 7 sketch, not dimensioned", 300, "in", "PHOTO-EST", "Room 7 sketch + photos", "x position approximate"),
    ("STR2", "Structure", "Steel columns", "seen in photos of rooms 5, 6, 7, 8", COL_W, "in", "PHOTO-EST", "Site photos", "11 columns at estimated positions; measure on site"),
    ("STR3", "Structure", "Main beams rooms 6 and 8, secondary beams", "seen in photos", 72, "in", "PHOTO-EST", "Site photos", "secondaries at most 72\" apart"),
]
OPENING_STATUS = {"D05": ("7.5 (room 4 sketch) / 9 (A-100)", "MEASURED", "room 4 sketch value used"),
                  "D13": ("not written", "STANDARD", "photo shows jambs; A-100 drew the full 48\" hallway end"),
                  "W01": ("114, height 48 per A-100", "MEASURED", "height from A-100 (room 2 sketch)")}

# =====================================================================================================
# Blender helpers
# =====================================================================================================
MAT = {}


def material(name, rgb, rough=0.7, metal=0.0, alpha=1.0, emit=0.0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (rgb[0], rgb[1], rgb[2], alpha)
    if m.node_tree is None:
        try:
            m.use_nodes = True
        except Exception:
            pass
    if m.node_tree is not None:
        b = m.node_tree.nodes.get("Principled BSDF")
        if b:
            b.inputs["Base Color"].default_value = (rgb[0], rgb[1], rgb[2], 1)
            b.inputs["Roughness"].default_value = rough
            b.inputs["Metallic"].default_value = metal
            b.inputs["Alpha"].default_value = alpha
            if emit:
                b.inputs["Emission Color"].default_value = (rgb[0], rgb[1], rgb[2], 1)
                b.inputs["Emission Strength"].default_value = emit
    if alpha < 1 and hasattr(m, "surface_render_method"):
        m.surface_render_method = "BLENDED"
    MAT[name] = m
    return m


def make_materials():
    for name, rgb, kw in [
        ("slab", (0.78, 0.76, 0.72), {}), ("deck", (0.86, 0.85, 0.82), {}),
        ("wall_ext", (0.66, 0.66, 0.64), {}), ("wall_int", (0.84, 0.84, 0.82), {}),
        ("wall_half", (0.78, 0.75, 0.68), {}), ("wall_assumed", (0.86, 0.72, 0.55), {}),
        ("wall_new", (0.95, 0.94, 0.91), {}), ("glass", (0.60, 0.80, 0.88), {"alpha": 0.28, "rough": 0.05}),
        ("frame", (0.10, 0.10, 0.10), {"metal": 0.6}), ("column", (0.55, 0.60, 0.67), {"metal": 0.4}),
        ("beam", (0.70, 0.72, 0.75), {"metal": 0.3}), ("stair", (0.74, 0.71, 0.66), {}),
        ("cutter", (1.0, 0.1, 0.1), {}), ("dim", (0.06, 0.06, 0.06), {}), ("label", (0.05, 0.28, 0.17), {}),
        ("note", (0.70, 0.20, 0.05), {}),
        # office finishes
        ("fl_stone", (0.90, 0.89, 0.86), {"rough": 0.3}), ("fl_oak", (0.72, 0.56, 0.38), {"rough": 0.5}),
        ("fl_carpet", (0.56, 0.58, 0.61), {"rough": 1.0}), ("fl_vinyl", (0.80, 0.81, 0.82), {}),
        ("fl_tile", (0.84, 0.88, 0.89), {"rough": 0.3}), ("fl_prayer", (0.28, 0.46, 0.36), {"rough": 1.0}),
        ("fl_warm", (0.76, 0.63, 0.47), {}), ("fl_concrete", (0.79, 0.77, 0.74), {}),
        # furniture
        ("white", (0.95, 0.95, 0.93), {"rough": 0.4}), ("oak", (0.78, 0.61, 0.43), {"rough": 0.5}),
        ("walnut", (0.40, 0.27, 0.17), {"rough": 0.45}), ("black", (0.07, 0.07, 0.08), {"metal": 0.5, "rough": 0.4}),
        ("charcoal", (0.22, 0.24, 0.24), {"rough": 0.8}), ("navy", (0.13, 0.20, 0.31), {"rough": 0.9}),
        ("green", (0.16, 0.38, 0.28), {"rough": 0.9}), ("leather", (0.33, 0.21, 0.13), {"rough": 0.5}),
        ("sofa", (0.58, 0.55, 0.51), {"rough": 1.0}), ("camel", (0.69, 0.53, 0.36), {"rough": 0.9}),
        ("plant", (0.22, 0.47, 0.28), {"rough": 0.9}), ("pot", (0.86, 0.85, 0.81), {}),
        ("screen", (0.05, 0.06, 0.07), {"rough": 0.2}), ("brand", (0.05, 0.34, 0.20), {}),
        ("brass", (0.74, 0.60, 0.34), {"metal": 0.9, "rough": 0.3}), ("porcelain", (0.97, 0.97, 0.97), {"rough": 0.15}),
        ("metal", (0.72, 0.73, 0.74), {"metal": 0.9, "rough": 0.3}), ("felt", (0.55, 0.69, 0.60), {"rough": 1.0}),
        ("feltw", (0.90, 0.89, 0.86), {"rough": 1.0}), ("garment", (0.44, 0.52, 0.66), {"rough": 1.0}),
        ("garment2", (0.86, 0.80, 0.70), {"rough": 1.0}), ("machine", (0.86, 0.87, 0.85), {}),
        ("orange", (0.95, 0.52, 0.18), {}), ("cork", (0.77, 0.60, 0.43), {"rough": 1.0}),
        ("light", (1.0, 0.98, 0.92), {"emit": 4.0}),
    ]:
        material(name, rgb, **kw)


def collection(name, parent=None):
    c = bpy.data.collections.new(name)
    (parent or bpy.context.scene.collection).children.link(c)
    return c


class Item:
    """One editable object built from axis-aligned boxes given in plan inches (y south)."""

    def __init__(self, name, coll, **props):
        self.name, self.coll, self.boxes, self.props = name, coll, [], props

    def box(self, x0, x1, y0, y1, z0, z1, mat):
        x0, x1, y0, y1 = min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1)
        if x1 - x0 > 0.01 and y1 - y0 > 0.01 and z1 - z0 > 0.01:
            self.boxes.append((x0, x1, y0, y1, z0, z1, mat))
        return self

    def done(self):
        if not self.boxes:
            return None
        cx = (min(b[0] for b in self.boxes) + max(b[1] for b in self.boxes)) / 2
        cy = (min(b[2] for b in self.boxes) + max(b[3] for b in self.boxes)) / 2
        z_base = min(b[4] for b in self.boxes)
        verts, faces, mats, order = [], [], [], {}
        for x0, x1, y0, y1, z0, z1, m in self.boxes:
            X0, X1 = (x0 - cx) * IN, (x1 - cx) * IN
            Y0, Y1 = -(y1 - cy) * IN, -(y0 - cy) * IN
            Z0, Z1 = (z0 - z_base) * IN, (z1 - z_base) * IN
            k = len(verts)
            verts += [(X0, Y0, Z0), (X1, Y0, Z0), (X1, Y1, Z0), (X0, Y1, Z0),
                      (X0, Y0, Z1), (X1, Y0, Z1), (X1, Y1, Z1), (X0, Y1, Z1)]
            mi = order.setdefault(m, len(order))
            for f in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
                faces.append(tuple(k + i for i in f))
                mats.append(mi)
        me = bpy.data.meshes.new(self.name)
        me.from_pydata(verts, [], faces)
        for m in sorted(order, key=order.get):
            me.materials.append(MAT[m])
        for poly, mi in zip(me.polygons, mats):
            poly.material_index = mi
        me.update()
        ob = bpy.data.objects.new(self.name, me)
        ob.location = (cx * IN, -cy * IN, z_base * IN)
        self.coll.objects.link(ob)
        for k, v in self.props.items():
            ob[k] = v
        return ob


def solid(name, coll, x0, x1, y0, y1, z0, z1, mat, **props):
    return Item(name, coll, **props).box(x0, x1, y0, y1, z0, z1, mat).done()


def prism(name, coll, pts, z0, z1, mat, **props):
    bm = bmesh.new()
    vs = [bm.verts.new((x * IN, -y * IN, z0 * IN)) for x, y in pts]
    face = bm.faces.new(vs)
    ext = bmesh.ops.extrude_face_region(bm, geom=[face])
    top = [e for e in ext["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, (z1 - z0) * IN), verts=top)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(MAT[mat])
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    for k, v in props.items():
        ob[k] = v
    return ob


def text(name, coll, body, x, y, z, size, mat="dim", rot=0.0, align="CENTER"):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body = body
    cu.size = size * IN
    cu.align_x, cu.align_y = align, "CENTER"
    cu.materials.append(MAT[mat])
    ob = bpy.data.objects.new(name, cu)
    ob.location = (x * IN, -y * IN, z * IN)
    ob.rotation_euler = (0, 0, rot)
    coll.objects.link(ob)
    return ob


def cutter(name, coll, wall, a, b, z0, z1, **props):
    c0, c1 = wall["c0"] - 2, wall["c1"] + 2
    ob = solid(name, coll, a, b, c0, c1, z0, z1, "cutter", **props) if wall["axis"] == "h" else \
        solid(name, coll, c0, c1, a, b, z0, z1, "cutter", **props)
    ob.display_type = "WIRE"
    ob.hide_render = True
    return ob


def boolean(target, cut):
    m = target.modifiers.new("cut " + cut.name, "BOOLEAN")
    m.operation, m.object, m.solver = "DIFFERENCE", cut, "EXACT"


def fmt_ftin(v):
    v = round(v)
    return f"{v // 12}'-{v % 12}\""


# =====================================================================================================
# Phase 1 - shell
# =====================================================================================================
C = {}


def setup_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = "METRIC"
    sc.unit_settings.scale_length = 1.0
    sc.unit_settings.length_unit = "MILLIMETERS"
    if sc.world is None:
        sc.world = bpy.data.worlds.new("World")
    sc.world.color = (0.95, 0.95, 0.94)
    make_materials()
    for name in ("Structure", "Walls", "Doors_Windows", "Stairs", "Dimensions", "Cameras", "Lighting"):
        C[name] = collection(name)
    C["Columns"] = collection("Columns", C["Structure"])
    C["Beams"] = collection("Beams", C["Structure"])
    C["Existing Walls"] = collection("Existing Walls", C["Walls"])
    C["Existing Partitions"] = collection("Existing Partitions", C["Walls"])
    C["Doors"] = collection("Doors", C["Doors_Windows"])
    C["Windows"] = collection("Windows", C["Doors_Windows"])


def wall_height(w):
    return HALF_H if w["kind"] == "half" else DECK_H


def build_wall(w, coll=None, mat=None):
    h = wall_height(w)
    if mat is None:
        mat = {"ext": "wall_ext", "int": "wall_int", "half": "wall_half", "part": "wall_int",
               "new": "wall_new", "glass": "glass"}[w["kind"]]
        if w["status"] == "ASSUMED" and w["kind"] in ("ext", "int", "part"):
            mat = "wall_assumed"
    if coll is None:
        coll = C["Existing Partitions"] if w["kind"] in ("half", "part") else C["Existing Walls"]
    box = (w["a"], w["b"], w["c0"], w["c1"]) if w["axis"] == "h" else (w["c0"], w["c1"], w["a"], w["b"])
    name = f'{w["id"]} {w["name"]}'
    ob = solid(name, coll, box[0], box[1], box[2], box[3], 0, h, mat, wall_id=w["id"], kind=w["kind"],
               status=w["status"], plan_box_in=str([round(v, 2) for v in box]), height_in=h, note=w["note"])
    for op in w["ops"]:
        oid, kind, a, b, label = op[:5]
        if kind == "win":
            hgt = op[5]
            sill = LINTEL - hgt
            cut = cutter(f"{oid} {label}", C["Windows"], w, a, b, sill, LINTEL, opening_id=oid, kind="window",
                         width_in=round(b - a, 2), height_in=hgt, sill_in=sill, head_in=LINTEL)
            gl = solid(f"{oid} glass", C["Windows"], *(
                (a, b, (w["c0"] + w["c1"]) / 2 - 0.5, (w["c0"] + w["c1"]) / 2 + 0.5) if w["axis"] == "h" else
                ((w["c0"] + w["c1"]) / 2 - 0.5, (w["c0"] + w["c1"]) / 2 + 0.5, a, b)), sill, LINTEL, "glass",
                opening_id=oid)
        else:
            top = HALF_H + 2 if w["kind"] == "half" else (GATE_H if kind == "gate" else LINTEL)
            cut = cutter(f"{oid} {label}", C["Doors"], w, a, b, -1, top, opening_id=oid, kind=kind,
                         width_in=round(b - a, 2), head_in=top if w["kind"] != "half" else "full height of low wall")
        boolean(ob, cut)
    return ob


def build_shell():
    S = C["Structure"]
    prism("Floor slab", S, OUTLINE, -SLAB_T, 0, "slab", status="graphic thickness", note="top of slab = finished floor 0")
    deck = prism("Steel deck (floor above)", S, OUTLINE, DECK_H, DECK_H + DECK_T, "deck",
                 status="PHOTO-EST", note="underside at 9'-6\" from photos")
    for name, box in (("room 1 stair", (0, 160, 102, FRONT)), ("north-east stair", (R8_E - 273, R8_E, R8_N, R8_N + STAIR_T)),
                      ("south-east stair", (R8_E - 277, R8_E, SE_N, MID_S))):
        hole = solid(f"Deck opening over {name}", S, box[0], box[1], box[2], box[3], DECK_H - 2, DECK_H + DECK_T + 2, "cutter")
        hole.display_type, hole.hide_render = "WIRE", True
        boolean(deck, hole)
    for w in WALLS:
        build_wall(w)
    # columns and beams (estimated from photos)
    for i, (x, y) in enumerate(COLUMNS, 1):
        solid(f"COL{i:02d} steel column (estimated)", C["Columns"], x - COL_W / 2, x + COL_W / 2, y - COL_W / 2,
              y + COL_W / 2, 0, DECK_H - BEAM_MAIN[1], "column", status="PHOTO-EST", plan_xy_in=str((x, y)))
    beams = []

    def main(name, x, y0, y1):
        beams.append((name, x - BEAM_MAIN[0] / 2, x + BEAM_MAIN[0] / 2, y0, y1, BEAM_MAIN[1]))

    def across(x0, x1, y0, y1, along, tag):
        span = (x1 - x0) if along == "y" else (y1 - y0)
        n = int(span // 72)
        for k in range(1, n + 1):
            c = (x0 if along == "y" else y0) + span * k / (n + 1)
            if along == "y":
                beams.append((f"{tag} secondary", c - BEAM_SEC[0] / 2, c + BEAM_SEC[0] / 2, y0, y1, BEAM_SEC[1]))
            else:
                beams.append((f"{tag} secondary", x0, x1, c - BEAM_SEC[0] / 2, c + BEAM_SEC[0] / 2, BEAM_SEC[1]))

    main("Room 7 main beam (sketch line)", 300, MID_N, MID_S)
    main("Room 6 - 5 main beam", 616, R6_N, MID_S)
    main("Room 8 main beam", 1101, R8_N, MID_S)
    across(0, 300, 0, FRONT, "y", "Room 1")
    across(305, 565, 0, FRONT, "y", "Room 3")
    across(570, 1088, 0, FRONT, "y", "Room 4")
    across(R2_W, R2_E, R2_N, MID_S, "x", "Room 2")
    across(R2_W, R7_E, MID_N, JOG, "x", "Room 7")
    across(R7_LOW_W, R7_E, JOG, MID_S, "x", "Room 7")
    across(R7_E, 866, MID_N, HALL_S, "y", "Hallway")
    across(367, 866, R5_N, R5_S, "y", "Room 5")
    across(367, 612, R6_N, R6_S, "x", "Room 6")
    across(620, 866, R6_N, R6_S, "x", "Room 6")
    across(R8_W, 1097, R8_N, MID_S, "x", "Room 8")
    across(1105, R8_E, R8_N, MID_S, "x", "Room 8")
    for i, (name, x0, x1, y0, y1, d) in enumerate(beams, 1):
        solid(f"BM{i:03d} {name}", C["Beams"], x0, x1, y0, y1, DECK_H - d, DECK_H, "beam",
              status="PHOTO-EST" if "sketch" not in name else "SKETCH (approximate)")
    build_stairs()
    build_dimensions()


def flight(it, x0, x1, y0, y1, axis, direction, z0, risers, rise):
    """Solid stair flight: risers count, each tread TREAD deep, climbing along +/- axis from (x0 or y0)."""
    for i in range(risers):
        top = z0 + rise * (i + 1)
        if axis == "y":
            a = y0 + i * TREAD if direction > 0 else y1 - (i + 1) * TREAD
            it.box(x0, x1, a, a + TREAD, max(0, top - 8), top, "stair")
        else:
            a = x0 + i * TREAD if direction > 0 else x1 - (i + 1) * TREAD
            it.box(a, a + TREAD, y0, y1, max(0, top - 8), top, "stair")


def build_stairs():
    st = C["Stairs"]
    n = round(FLOOR_TO_FLOOR / 7)
    rise = FLOOR_TO_FLOOR / n
    up1 = n // 2 + 1          # risers to the landing
    up2 = n - up1
    # room 1: first flight up from the back along the outer (west) wall, landing at the front, return flight
    it = Item("ST1 room 1 stair, flight 1 (from the back along the outer wall)", st, status="configuration confirmed; risers ASSUMED")
    flight(it, 2, 78, 102, 102 + up1 * TREAD, "y", 1, 0, up1, rise)
    it.done()
    land_z = up1 * rise
    Item("ST1 room 1 stair, landing at the front wall", st).box(2, 158, 102 + up1 * TREAD, FRONT, land_z - 8, land_z, "stair").done()
    it = Item("ST1 room 1 stair, flight 2 (return to the floor above)", st)
    flight(it, 82, 158, 102 + up1 * TREAD - up2 * TREAD, 102 + up1 * TREAD, "y", -1, land_z, up2, rise)
    it.done()
    # north-east and south-east stairs: layout not surveyed, drawn as U-stairs in the measured rooms
    for tag, x0, x1, y0, y1, wide in (("ST2 north-east stair", R8_E - 273, R8_E, R8_N, R8_N + STAIR_T, 48),
                                      ("ST3 south-east stair", R8_E - 277, R8_E, SE_N, MID_S, 54)):
        run1 = up1 * TREAD
        xs = x1 - 50 - run1                      # flights end at a 50" landing on the east wall
        a = Item(f"{tag}, flight 1 (layout ASSUMED)", st, status="ASSUMED")
        flight(a, xs, xs + run1, y1 - wide, y1, "x", 1, 0, up1, rise)
        a.done()
        Item(f"{tag}, landing (layout ASSUMED)", st).box(x1 - 50, x1, y1 - 2 * wide - 4, y1, land_z - 8, land_z, "stair").done()
        b = Item(f"{tag}, flight 2 (layout ASSUMED)", st)
        flight(b, x1 - 50 - up2 * TREAD, x1 - 50, y1 - 2 * wide - 4, y1 - wide - 4, "x", -1, land_z, up2, rise)
        b.done()
    gs = Item("ST4 gate steps inside room 1 (2 steps, PHOTO-EST)", st, status="PHOTO-EST")
    gs.box(160, 300, FRONT - 36, FRONT - 24, 0, 7, "stair").box(160, 300, FRONT - 24, FRONT, 0, 14, "stair").done()


def dim(tag, p, q, off_axis, off, label, z=150):
    """Dimension line between plan points p and q (same x or same y), offset by off along off_axis."""
    D = C["Dimensions"]
    it = Item(f"DIM {tag}", D)
    t = 2.5
    if p[1] == q[1]:   # horizontal dimension
        y = p[1] + off
        it.box(p[0], q[0], y - t / 2, y + t / 2, z, z + 1, "dim")
        for x in (p[0], q[0]):
            it.box(x - t / 2, x + t / 2, y - 14, y + 14, z, z + 1, "dim")
        it.done()
        text(f"DIM {tag} text", D, label, (p[0] + q[0]) / 2, y - 22, z, 20)
    else:              # vertical dimension
        x = p[0] + off
        it.box(x - t / 2, x + t / 2, p[1], q[1], z, z + 1, "dim")
        for y in (p[1], q[1]):
            it.box(x - 14, x + 14, y - t / 2, y + t / 2, z, z + 1, "dim")
        it.done()
        text(f"DIM {tag} text", D, label, x - 24, (p[1] + q[1]) / 2, z, 20, rot=math.pi / 2)


def lab(v, assumed=False):
    s = f'{fmt_ftin(v)} ({v:g}" = {v * 25.4:,.0f} mm)'
    return s + "  ASSUMED" if assumed else s


def build_dimensions():
    dim("room 1 width", (0, FRONT), (300, FRONT), "y", 70, lab(300))
    dim("room 3 width", (305, FRONT), (565, FRONT), "y", 70, lab(260))
    dim("room 4 width", (570, FRONT), (1088, FRONT), "y", 70, lab(518))
    dim("front overall", (-10, FRONT + 10), (1098, FRONT + 10), "y", 140, lab(1108))
    dim("front row depth", (-10, 0), (-10, FRONT), "x", -110, lab(247))
    dim("middle block depth", (-65, MID_N), (-65, MID_S), "x", -60, lab(881))
    dim("west overall", (-65, MID_N - 10), (-65, FRONT + 10), "x", -150, lab(1158))
    dim("room 8 length", (R8_E + 10, R8_N), (R8_E + 10, MID_S), "x", 70, lab(1538))
    dim("east overall", (R8_E + 10, R8_N - 10), (R8_E + 10, FRONT + 10), "x", 150, lab(1815))
    dim("room 8 width", (R8_W, R8_N - 10), (R8_E, R8_N - 10), "y", -70, lab(450, True))
    dim("rooms 5 6 width", (367, MID_N - 10), (866, MID_N - 10), "y", -70, lab(499))
    dim("room 7 upper width", (46, MID_N - 10), (R7_E, MID_N - 10), "y", -150, lab(316))


def room_labels(coll, mat="dim"):
    for key, (pts, name) in ROOMS.items():
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        area = abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1]
                       for i in range(len(pts)))) / 2 / 144
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        if key == "R7":
            cx, cy = 200, -560
        if key == "R8":
            cx, cy = 980, -900
        if key == "STRIP":
            text(f"LABEL {name}", coll, name, -7, -560, 152, 14, mat, rot=math.pi / 2)
            continue
        if key == "ENG":
            cy -= 20
        size = 26 if area > 600 else 18
        text(f"LABEL {name}", coll, f"{name}\n{area:,.0f} sft", cx, cy, 152, size, mat)


# =====================================================================================================
# Phase 2 - office-only layout (zoning from A-103, revised: visitor zone at the front, offices in the
# middle, design-development and staff support at the back)
# =====================================================================================================
# glass / solid treatment above the existing 48" walls: (wall id, a, b, treatment)
HALF_TREAT = [("PW01", 362, 420, "glass"), ("PW01", 420, 485, "solid"), ("PW01", 485, 565, "glass"),
              ("PW05", -228, -10, "glass"), ("PW07", 367, 420, "glass"), ("PW07", 420, 485, "solid"),
              ("PW07", 485, 866, "glass")]
# new openings in existing walls: (wall id, op)
NEW_OPENINGS = [("IW04", ("W11", "win", 60, 112, "Entrance - reception glass", 60)),
                ("IW04", ("W12", "win", 136, 188, "Entrance - reception glass", 60)),
                ("IW01", ("D17", "door", 114, 156, "Staff door entrance - HR 42\"")),
                ("PW01", ("D18", "door", 372, 414, "Reception - passage 42\"")),
                ("PW01", ("D19", "door", 500, 542, "Reception - boardroom 42\"")),
                ("IW03", ("D20", "door", 620, 662, "Executive center - boardroom 42\"")),
                ("PW07", ("D21", "door", 805, 847, "Open office - boardroom 42\""))]


def NP(wid, name, axis, c0, c1, a, b, ops=(), glass=False):
    w = W(wid, name, axis, c0, c1, a, b, "glass" if glass else "new", ops, status="PROPOSED")
    return w


NEW_WALLS = [
    NP("NP01", "HR - commercial, glass", "h", -231, -228, 110, 362, [("D30", "door", 240, 276, "HR glass door")], True),
    NP("NP02", "Audit room west", "v", 96, 100, -891, -744),
    NP("NP03", "Audit room east", "v", 250, 254, -891, -744),
    NP("NP04", "Audit room front, glass", "h", -744, -740, 96, 254, [("D31", "door", 152, 188, "Audit door")], True),
    NP("NP05", "Passage - guest washrooms", "v", 420, 425, -214, -10, [("D32", "door", -190, -160, "Guest WC"), ("D33", "door", -60, -30, "Guest WC")]),
    NP("NP06", "Guest washrooms divider", "h", -114, -110, 425, 480),
    NP("NP07", "Guest washrooms - boardroom", "v", 480, 485, -214, -10),
    NP("NP08", "Female prayer - washroom 2", "h", -720, -715, -55, 41),
    NP("NP09", "Store opening infill", "v", 41, 46, -834, -806),
    NP("NP10", "Sample room north", "h", -843, -838, 876, 1045),
    NP("NP11", "Sample room front, glass", "v", 1040, 1045, -838, -595, [("D34", "door", -702, -660, "Sample room")], True),
    NP("NP12", "Sample room - 3D lab", "h", -600, -595, 876, 1045),
    NP("NP13", "3D lab front, glass", "v", 1040, 1045, -595, -445, [("D35", "door", -540, -504, "3D lab")], True),
    NP("NP14", "3D lab - pattern room", "h", -445, -440, 876, 1045),
    NP("NP15", "Pattern room front, glass", "v", 1040, 1045, -440, -262, [("D36", "door", -380, -338, "Pattern room")], True),
    NP("NP16", "Pattern room - CAD", "h", -262, -257, 876, 1045),
    NP("NP17", "CAD room front, glass", "v", 1040, 1045, -257, -10, [("D37", "door", -255, -219, "CAD room")], True),
    NP("NP18", "Design studio front, glass", "v", 1100, 1105, -843, -530, [("D38", "door", -700, -640, "Design studio")], True),
    NP("NP19", "Material library west", "v", 1100, 1105, -530, -432),
    NP("NP20", "Design studio - material library", "h", -530, -525, 1105, 1326, [("D39", "door", 1210, 1246, "Library")]),
    NP("NP21", "Material library south", "h", -437, -432, 1105, 1156),
    NP("NP22", "Dining - corridor", "h", -905, -900, 876, 1078, [("D40", "door", 940, 1000, "Dining 60\"")], True),
    NP("NP23", "Lounge and dining - corridor, glass", "v", 1073, 1078, -1440, -905, [("D41", "door", -1300, -1258, "Lounge"), ("D42", "door", -1140, -1098, "Dining")], True),
    NP("NP24", "Lounge - dining, glass", "h", -1250, -1245, 876, 1073, glass=True),
    NP("NP25", "Prayer and wudu - corridor", "v", 1150, 1155, -1440, -1210, [("D43", "door", -1400, -1358, "Prayer (male)"), ("D44", "door", -1265, -1229, "Wudu")]),
    NP("NP26", "Design studio - corridor, glass", "v", 1150, 1155, -1210, -900, glass=True),
    NP("NP27", "Prayer - wudu", "h", -1283, -1278, 1155, 1326, [("D45", "door", 1240, 1270, "Prayer - wudu")]),
    NP("NP28", "Wudu - design studio", "h", -1215, -1210, 1155, 1326),
    NP("NP29", "Executive offices front, glass", "h", 54, 57, 700, 1088, [("D46", "door", 740, 776, "Director"), ("D47", "door", 880, 922, "MD")], True),
    NP("NP30", "PA - director, glass", "v", 700, 703, 57, FRONT, glass=True),
    NP("NP31", "Director - MD, glass", "v", 858, 861, 57, FRONT, glass=True),
]

ZONES = [   # (collection, id, label, polygon, floor finish)
    ("Reception", "Z01", "MAIN GATE + ENTRANCE\nsecurity, visitor check-in", [(160, 0), (300, 0), (300, 211), (160, 211)], "fl_stone"),
    ("Reception", "Z02", "RECEPTION + VISITOR WAITING", [(305, 0), (565, 0), (565, FRONT), (305, FRONT)], "fl_stone"),
    ("Reception", "Z03", "PASSAGE", [(367, -214), (420, -214), (420, -10), (367, -10)], "fl_stone"),
    ("Workstations", "Z04", "GUEST WORKSPACE\n4 desks + WC", [(R2_W, -152), (R2_E, -152), (R2_E, MID_S), (R2_W, MID_S)], "fl_oak"),
    ("Workstations", "Z05", "HR + ADMIN", [(110, -228), (362, -228), (362, -10), (110, -10)], "fl_carpet"),
    ("Workstations", "Z06", "COMMERCIAL + ACCOUNTS\n18 workstations", [(100, -740), (254, -740), (254, -891), (362, -891), (362, -231), (46, -231), (46, -891), (96, -891), (96, -740)], "fl_carpet"),
    ("Workstations", "Z07", "OPEN OFFICE WORKSTATIONS\n36 desks", [(367, R6_N), (866, R6_N), (866, R6_S), (367, R6_S)], "fl_carpet"),
    ("Meeting_Rooms", "Z08", "BOARDROOM\n16 seats", [(485, -214), (866, -214), (866, -10), (485, -10)], "fl_oak"),
    ("Meeting_Rooms", "Z09", "AUDIT ROOM", [(100, -891), (250, -891), (250, -744), (100, -744)], "fl_carpet"),
    ("Executive_Area", "Z10", "EXECUTIVE CENTER\nPA + waiting", [(570, 0), (700, 0), (700, FRONT), (570, FRONT)], "fl_oak"),
    ("Executive_Area", "Z11", "DIRECTOR", [(703, 57), (858, 57), (858, FRONT), (703, FRONT)], "fl_oak"),
    ("Executive_Area", "Z12", "MANAGING DIRECTOR", [(861, 57), (1088, 57), (1088, FRONT), (861, FRONT)], "fl_oak"),
    ("Executive_Area", "Z13", "EXECUTIVE CORRIDOR", [(700, 0), (1088, 0), (1088, 54), (700, 54)], "fl_oak"),
    ("Design_Development", "Z14", "CAD ROOM", [(876, -257), (1040, -257), (1040, -10), (876, -10)], "fl_vinyl"),
    ("Design_Development", "Z15", "PATTERN SUPPORT", [(876, -440), (1040, -440), (1040, -262), (876, -262)], "fl_vinyl"),
    ("Design_Development", "Z16", "3D PRINTING LAB", [(876, -595), (1040, -595), (1040, -445), (876, -445)], "fl_vinyl"),
    ("Design_Development", "Z17", "SAMPLE ROOM", [(876, -838), (1040, -838), (1040, -600), (876, -600)], "fl_vinyl"),
    ("Design_Development", "Z18", "DESIGN STUDIO\ndaylight from 3 windows", [(1155, -1210), (1326, -1210), (1326, -530), (1105, -530), (1105, -900), (1155, -900)], "fl_vinyl"),
    ("Design_Development", "Z19", "MATERIAL LIBRARY + SAMPLE STORE", [(1105, -525), (1326, -525), (1326, -437), (1105, -437)], "fl_vinyl"),
    ("Support_Rooms", "Z20", "DINING + PANTRY", [(876, -1245), (1073, -1245), (1073, -905), (876, -905)], "fl_warm"),
    ("Support_Rooms", "Z21", "LOUNGE", [(876, -1548), (1048, -1548), (1048, -1440), (1073, -1440), (1073, -1250), (876, -1250)], "fl_warm"),
    ("Support_Rooms", "Z22", "CORRIDOR", [(876, -900), (1100, -900), (1100, -843), (876, -843)], "fl_concrete"),
    ("Prayer_Rooms", "Z23", "PRAYER (MALE)", [(1155, -1440), (1326, -1440), (1326, -1283), (1155, -1283)], "fl_prayer"),
    ("Prayer_Rooms", "Z24", "WUDU", [(1155, -1278), (1326, -1278), (1326, -1215), (1155, -1215)], "fl_tile"),
    ("Prayer_Rooms", "Z25", "PRAYER (FEMALE)", [(-55, -891), (41, -891), (41, -720), (-55, -720)], "fl_prayer"),
    ("Washrooms", "Z26", "WASHROOM (FEMALE)", [(-55, -715), (41, -715), (41, -519), (-55, -519)], "fl_tile"),
    ("Washrooms", "Z27", "WASHROOM (MALE)", [(-55, -514), (41, -514), (41, -231), (-55, -231)], "fl_tile"),
    ("Washrooms", "Z28", "GUEST WC", [(425, -214), (480, -214), (480, -10), (425, -10)], "fl_tile"),
    ("Washrooms", "Z29", "GUEST WORKSPACE WC", [(R2_W, R2_N), (47, R2_N), (47, -155), (R2_W, -155)], "fl_tile"),
]
LABEL_AT = {"Z01": (232, 60), "Z02": (400, 70), "Z03": (394, -120), "Z04": (25, -110), "Z05": (180, -205), "Z06": (175, -575),
            "Z07": (616, -540), "Z08": (676, -190), "Z09": (175, -820), "Z10": (635, 70), "Z11": (780, 120),
            "Z12": (975, 120), "Z13": (900, 27), "Z14": (958, -50), "Z15": (958, -300), "Z16": (958, -520),
            "Z17": (958, -690), "Z18": (1250, -1030), "Z19": (1215, -485), "Z20": (975, -985), "Z21": (975, -1285),
            "Z22": (988, -872), "Z23": (1240, -1360), "Z24": (1240, -1246), "Z25": (-7, -800), "Z26": (-7, -580),
            "Z27": (-7, -330), "Z28": (452, -112), "Z29": (-4, -188)}
VERTICAL_LABELS = {"Z25", "Z26", "Z27", "Z03", "Z28"}


def furniture():
    F = C["Furniture"]
    sub = {k: collection(f"Furniture_{k}", F) for k in
           ("Reception", "Workstations", "Meeting", "Executive", "Design", "Support", "Prayer", "Washrooms")}
    count = {"n": 0}

    def it(zone, name):
        count["n"] += 1
        return Item(f"F{count['n']:03d} {name}", sub[zone], zone=zone)

    def chair(zone, x, y, facing, mat="charcoal", back=36, name="Task chair"):
        c = it(zone, name)
        c.box(x - 10, x + 10, y - 10, y + 10, 16, 19, mat)
        c.box(x - 2, x + 2, y - 2, y + 2, 2, 16, "black").box(x - 11, x + 11, y - 11, y + 11, 0, 2, "black")
        if facing == "s":
            c.box(x - 10, x + 10, y - 10, y - 7, 19, back, mat)
        elif facing == "n":
            c.box(x - 10, x + 10, y + 7, y + 10, 19, back, mat)
        elif facing == "e":
            c.box(x - 10, x - 7, y - 10, y + 10, 19, back, mat)
        else:
            c.box(x + 7, x + 10, y - 10, y + 10, 19, back, mat)
        return c.done()

    def table(zone, name, x0, x1, y0, y1, top="oak", h=29, base="black"):
        t = it(zone, name).box(x0, x1, y0, y1, h - 1.5, h, top)
        inset = 6
        t.box(x0 + inset, x0 + inset + 2, y0 + inset, y1 - inset, 0, h - 1.5, base)
        t.box(x1 - inset - 2, x1 - inset, y0 + inset, y1 - inset, 0, h - 1.5, base)
        return t.done()

    def bench(zone, x0, y0, n, divider="green", name="Workstation bench"):
        b = it(zone, f"{name} ({2 * n} desks)")
        b.box(x0, x0 + 54 * n, y0, y0 + 60, 27.5, 29, "white").box(x0, x0 + 54 * n, y0 + 29, y0 + 31, 29, 47, divider)
        for k in range(n + 1):
            b.box(x0 + 54 * k - 1, x0 + 54 * k + 1, y0 + 2, y0 + 58, 0, 27.5, "black")
        for k in range(n):
            cx = x0 + 27 + 54 * k
            b.box(cx - 11, cx + 11, y0 + 23, y0 + 25, 31, 45, "screen").box(cx - 11, cx + 11, y0 + 35, y0 + 37, 31, 45, "screen")
        b.done()
        for k in range(n):
            cx = x0 + 27 + 54 * k
            chair(zone, cx, y0 - 14, "s")
            chair(zone, cx, y0 + 74, "n")

    def plant(zone, x, y, h=54):
        it(zone, "Plant").box(x - 9, x + 9, y - 9, y + 9, 0, 18, "pot").box(x - 8, x + 8, y - 8, y + 8, 18, h, "plant").done()

    def sofa(zone, x0, x1, y0, y1, back, mat="sofa", name="Sofa"):
        s = it(zone, name).box(x0, x1, y0, y1, 0, 17, mat)
        if back == "n":
            s.box(x0, x1, y0, y0 + 8, 17, 32, mat)
        elif back == "s":
            s.box(x0, x1, y1 - 8, y1, 17, 32, mat)
        elif back == "w":
            s.box(x0, x0 + 8, y0, y1, 17, 32, mat)
        else:
            s.box(x1 - 8, x1, y0, y1, 17, 32, mat)
        return s.done()

    def cabinet(zone, name, x0, x1, y0, y1, h, mat="white"):
        return it(zone, name).box(x0, x1, y0, y1, 0, h, mat).done()

    # ---- entrance and reception (visitor zone)
    it("Reception", "Security and visitor desk").box(170, 230, 150, 174, 0, 40, "walnut").box(168, 232, 148, 176, 40, 42, "white").done()
    chair("Reception", 200, 136, "s", "charcoal", 40, "Security chair")
    it("Reception", "Brand wall, entrance").box(165, 295, 0, 2.5, 20, 100, "brand").box(200, 260, 2.5, 3.5, 50, 70, "brass").done()
    plant("Reception", 288, 196)
    it("Reception", "Reception desk").box(505, 535, 100, 215, 0, 40, "walnut").box(500, 537, 98, 217, 40, 42, "white") \
        .box(535, 552, 100, 215, 26, 28, "white").done()
    chair("Reception", 552, 158, "w", "leather", 40, "Receptionist chair")
    it("Reception", "Wood slat feature wall behind reception").box(561, 565, 70, 240, 0, 100, "oak").done()
    sofa("Reception", 330, 440, 214, 245, "s", "camel", "Waiting sofa")
    sofa("Reception", 318, 350, 150, 186, "w", "sofa", "Waiting armchair")
    sofa("Reception", 420, 452, 150, 186, "e", "sofa", "Waiting armchair")
    table("Reception", "Coffee table", 362, 408, 150, 188, "walnut", 16)
    plant("Reception", 322, 95)
    plant("Reception", 470, 232)
    it("Reception", "Sample display shelf").box(310, 322, 20, 56, 0, 72, "oak").done()
    it("Reception", "Welcome screen, passage").box(416, 420, -145, -95, 46, 84, "screen").done()

    # ---- guest workspace (room 2) and its WC
    bench("Workstations", -40, -130, 2, "oak", "Guest workspace bench")
    cabinet("Workstations", "Guest workspace storage", -53, -41, -148, -98, 36)
    plant("Workstations", 90, -140)
    it("Washrooms", "WC, guest workspace").box(-50, -30, -216, -190, 0, 16, "porcelain").box(-50, -30, -218, -212, 16, 30, "porcelain").done()
    it("Washrooms", "Basin, guest workspace").box(5, 40, -219, -200, 30, 33, "porcelain").box(5, 40, -219, -217, 0, 30, "white").done()

    # ---- HR and admin
    bench("Workstations", 118, -170, 2, "green", "HR bench")
    table("Workstations", "HR interview table", 236, 292, -150, -114, "white")
    chair("Workstations", 250, -100, "n")
    chair("Workstations", 278, -100, "n")
    chair("Workstations", 264, -164, "s")
    cabinet("Workstations", "HR filing cabinets", 180, 296, -28, -10, 42)

    # ---- commercial and accounts, audit room
    for y0 in (-680, -520, -360):
        bench("Workstations", 94, y0, 3, "green", "Commercial and accounts bench")
    cabinet("Workstations", "Printer and tea counter", 338, 362, -720, -660, 36)
    it("Workstations", "Printer").box(340, 360, -715, -690, 36, 52, "metal").done()
    table("Meeting", "Audit table", 130, 220, -840, -804, "oak")
    for cx in (145, 175, 205):
        chair("Meeting", cx, -854, "s")
        chair("Meeting", cx, -790, "n")
    cabinet("Meeting", "Audit document cabinets", 110, 240, -889, -871, 78)

    # ---- open office workstations (room 6), aisle on the column line x 616
    for x0 in (400, 670):
        for y0 in (-770, -610, -450):
            bench("Workstations", x0, y0, 3, "green", "Open office bench")
    table("Workstations", "Team table", 470, 590, -330, -290, "oak")
    for cx in (485, 515, 545, 575):
        chair("Workstations", cx, -344, "s", "navy")
        chair("Workstations", cx, -276, "n", "navy")
    sofa("Workstations", 690, 790, 300 - 600, 330 - 600, "s", "camel", "Breakout sofa")
    table("Workstations", "Breakout coffee table", 715, 765, -330, -310, "walnut", 16)
    for y0 in (-800, -650, -500):
        cabinet("Workstations", "Low storage on the 48 in wall", 371, 387, y0, y0 + 120, 36)
    plant("Workstations", 850, -330)
    plant("Workstations", 400, -250)

    # ---- boardroom (premium)
    table("Meeting", "Boardroom table, walnut", 555, 795, -139, -85, "walnut", 30)
    for cx in (570, 605, 640, 675, 710, 745, 780):
        chair("Meeting", cx, -153, "s", "leather", 40, "Boardroom chair")
        chair("Meeting", cx, -71, "n", "leather", 40, "Boardroom chair")
    chair("Meeting", 537, -112, "e", "leather", 40, "Boardroom chair")
    chair("Meeting", 813, -112, "w", "leather", 40, "Boardroom chair")
    it("Meeting", "Video conference screen").box(485, 489, -160, -64, 40, 86, "screen").done()
    it("Meeting", "Sample display rail").box(560, 790, -206, -200, 64, 66, "black").box(560, 790, -210, -196, 30, 62, "garment") \
        .box(560, 562, -206, -200, 0, 66, "black").box(788, 790, -206, -200, 0, 66, "black").done()

    # ---- guest washrooms
    for wc, van in ((-204, -144), (-36, -105)):
        it("Washrooms", "Guest WC").box(455, 478, wc, wc + 22, 0, 16, "porcelain").box(474, 478, wc, wc + 22, 16, 30, "porcelain").done()
        it("Washrooms", "Guest vanity").box(427, 478, van, van + 22, 30, 34, "white").box(427, 478, van, van + 22, 0, 30, "walnut").done()

    # ---- executive center (room 4)
    it("Executive", "PA desk").box(620, 650, 90, 162, 0, 29, "walnut").box(618, 652, 88, 164, 29, 30.5, "white").done()
    chair("Executive", 666, 126, "w", "leather", 40, "PA chair")
    sofa("Executive", 585, 615, 190, 238, "w", "camel", "Executive waiting chair")
    sofa("Executive", 655, 690, 205, 238, "s", "camel", "Executive waiting chair")
    table("Executive", "Executive waiting side table", 622, 648, 205, 230, "walnut", 18)
    it("Executive", "Director desk").box(745, 811, 170, 200, 0, 29, "walnut").box(743, 813, 168, 202, 29, 30.5, "walnut").done()
    chair("Executive", 778, 214, "n", "leather", 44, "Director chair")
    chair("Executive", 760, 150, "s", "charcoal", 36, "Visitor chair")
    chair("Executive", 796, 150, "s", "charcoal", 36, "Visitor chair")
    cabinet("Executive", "Director bookshelf", 707, 719, 80, 160, 72, "oak")
    plant("Executive", 840, 230)
    it("Executive", "MD desk").box(980, 1058, 160, 196, 0, 29, "walnut").box(978, 1060, 158, 198, 29, 30.5, "walnut").done()
    chair("Executive", 1019, 212, "n", "leather", 46, "MD chair")
    chair("Executive", 1000, 140, "s", "leather", 38, "Visitor chair")
    chair("Executive", 1038, 140, "s", "leather", 38, "Visitor chair")
    cabinet("Executive", "MD credenza", 1068, 1086, 90, 200, 30, "walnut")
    sofa("Executive", 868, 900, 140, 230, "w", "camel", "MD sofa")
    table("Executive", "MD coffee table", 910, 945, 165, 205, "walnut", 16)
    sofa("Executive", 915, 945, 215, 240, "s", "sofa", "MD armchair")
    plant("Executive", 880, 80)

    # ---- design development: CAD, pattern support, 3D printing, sample room, design studio, library
    for y0 in (-240, -170, -100):
        it("Design", "CAD workstation").box(878, 908, y0, y0 + 60, 27.5, 29, "white").box(878, 908, y0, y0 + 2, 0, 27.5, "black") \
            .box(878, 908, y0 + 58, y0 + 60, 0, 27.5, "black").box(886, 889, y0 + 8, y0 + 28, 31, 50, "screen") \
            .box(886, 889, y0 + 32, y0 + 52, 31, 50, "screen").done()
        chair("Design", 925, y0 + 30, "w")
    it("Design", "Plotter").box(930, 1000, -250, -232, 0, 42, "metal").done()
    table("Design", "CAD layout table", 950, 1020, -150, -90, "white", 36)
    table("Design", "Pattern table", 900, 1004, -400, -340, "white", 36)
    it("Design", "Pattern hanging rail").box(880, 1000, -436, -430, 70, 72, "black").box(880, 1000, -438, -428, 30, 70, "garment2").done()
    it("Design", "3D printer bench").box(878, 902, -585, -455, 0, 29, "white").box(880, 900, -580, -560, 29, 52, "charcoal") \
        .box(880, 900, -540, -520, 29, 52, "charcoal").box(880, 900, -500, -480, 29, 52, "charcoal").done()
    table("Design", "3D lab workstation", 930, 990, -500, -470, "white")
    chair("Design", 960, -456, "n")
    cabinet("Design", "Filament dry cabinet", 1000, 1035, -470, -452, 72)
    cabinet("Design", "Post-processing bench", 920, 1030, -593, -575, 34)
    for i, y0 in enumerate((-790, -740)):
        it("Design", "Sample machine desk").box(880, 920, y0, y0 + 22, 28, 30, "white").box(884, 910, y0 + 6, y0 + 16, 30, 44, "machine") \
            .box(882, 884, y0, y0 + 22, 0, 28, "black").box(916, 918, y0, y0 + 22, 0, 28, "black").done()
        chair("Design", 935, y0 + 11, "w", "navy")
    table("Design", "Sample review table", 950, 1030, -800, -740, "white", 36)
    for i, x in enumerate((900, 928)):
        it("Design", "Dress form").box(x - 7, x + 7, -662, -648, 0, 4, "black").box(x - 1, x + 1, -656, -654, 4, 40, "black") \
            .box(x - 7, x + 7, -662, -648, 40, 64, "garment2").done()
    it("Design", "Sample rail").box(965, 1030, -616, -610, 64, 66, "black").box(965, 1030, -620, -606, 26, 62, "garment").done()
    it("Design", "Steam press table").box(960, 1020, -680, -664, 0, 34, "white").done()
    for y0 in (-1150, -810):
        bench("Design", 1200, y0, 2, "oak", "Designer bench")
    table("Design", "Design worktable", 1190, 1310, -1000, -940, "oak", 36)
    it("Design", "Mood board wall").box(1160, 1320, -1210, -1207, 30, 96, "cork").done()
    table("Design", "Design review table", 1180, 1300, -660, -620, "oak")
    for cx in (1200, 1240, 1280):
        chair("Design", cx, -674, "s", "navy")
        chair("Design", cx, -606, "n", "navy")
    it("Design", "Garment rail").box(1110, 1126, -630, -545, 26, 62, "garment").box(1117, 1119, -630, -545, 62, 64, "black").done()
    cabinet("Design", "Fabric library shelves", 1110, 1130, -880, -760, 84, "oak")
    for x0 in (1110, 1170, 1230):
        cabinet("Design", "Material library shelves", x0, x0 + 50, -455, -437, 84, "oak")
    cabinet("Design", "Sample store shelves", 1290, 1324, -520, -460, 84)

    # ---- support: dining and pantry, lounge
    it("Support", "Pantry counter").box(878, 902, -1240, -1120, 0, 36, "white").box(878, 902, -1240, -1120, 36, 37.5, "walnut").done()
    cabinet("Support", "Refrigerator", 878, 902, -1110, -1080, 72, "metal")
    for cx, cy in ((948, -1180), (1030, -1180), (948, -1060), (1030, -1060), (1030, -960)):
        table("Support", "Dining table", cx - 18, cx + 18, cy - 18, cy + 18, "oak", 29)
        chair("Support", cx - 28, cy, "e", "green", 32, "Dining chair")
        chair("Support", cx + 28, cy, "w", "green", 32, "Dining chair")
    sofa("Support", 890, 1000, -1530, -1500, "n", "camel", "Lounge sofa")
    sofa("Support", 890, 920, -1500, -1420, "w", "camel", "Lounge sofa")
    table("Support", "Lounge coffee table", 935, 985, -1480, -1440, "walnut", 16)
    sofa("Support", 1000, 1032, -1420, -1388, "e", "sofa", "Lounge armchair")
    sofa("Support", 960, 992, -1360, -1328, "s", "sofa", "Lounge armchair")
    it("Support", "Lounge TV wall").box(876, 880, -1400, -1320, 36, 76, "screen").done()
    plant("Support", 1040, -1530)
    plant("Support", 900, -1270)

    # ---- prayer rooms and wudu
    it("Prayer", "Prayer carpet (male)").box(1180, 1316, -1435, -1290, 0, 0.6, "fl_prayer").done()
    cabinet("Prayer", "Shoe rack (male)", 1157, 1175, -1350, -1300, 30)
    it("Prayer", "Wudu stools").box(1195, 1316, -1246, -1237, 0, 14, "white").done()
    it("Prayer", "Wudu tap ledge").box(1160, 1316, -1218, -1215, 30, 34, "porcelain").done()
    it("Prayer", "Prayer carpet (female)").box(-50, 36, -886, -775, 0, 0.6, "fl_prayer").done()
    it("Prayer", "Low screen, female prayer").box(-55, 5, -771, -768, 0, 42, "white").done()
    it("Prayer", "Wudu stools (female)").box(-50, 36, -742, -733, 0, 14, "white").done()
    it("Prayer", "Wudu tap ledge (female)").box(-50, 36, -723, -720, 30, 34, "porcelain").done()
    cabinet("Prayer", "Shoe rack (female)", 23, 39, -886, -842, 30)

    # ---- staff washrooms
    for y in (-700, -650):          # female: two stalls
        it("Washrooms", "WC").box(-53, -27, y, y + 20, 0, 16, "porcelain").box(-55, -51, y, y + 20, 16, 30, "porcelain").done()
    it("Washrooms", "Stall partitions").box(-55, 0, -670, -669, 0, 72, "feltw").box(-55, 0, -620, -619, 0, 72, "feltw").done()
    it("Washrooms", "Basin counter (female)").box(-50, -14, -570, -526, 30, 33, "white").box(-50, -48, -570, -526, 0, 30, "walnut").done()
    for y in (-500, -450):          # male: two stalls, two urinals, basins
        it("Washrooms", "WC").box(-53, -27, y, y + 20, 0, 16, "porcelain").box(-55, -51, y, y + 20, 16, 30, "porcelain").done()
    it("Washrooms", "Stall partitions").box(-55, 0, -470, -469, 0, 72, "feltw").box(-55, 0, -420, -419, 0, 72, "feltw").done()
    for y in (-380, -350):
        it("Washrooms", "Urinal").box(-55, -43, y, y + 14, 24, 48, "porcelain").done()
    it("Washrooms", "Basin counter (male)").box(-50, -14, -300, -256, 30, 33, "white").box(-50, -48, -300, -256, 0, 30, "walnut").done()
    return count["n"]


def lighting_fixtures():
    L = C["Fixtures"]
    n = 0

    def lin(name, x0, x1, y0, y1, h=96):
        nonlocal n
        n += 1
        Item(f"L{n:03d} {name}", L).box(x0, x1, y0, y1, h, h + 2, "light").box((x0 + x1) / 2 - 0.3, (x0 + x1) / 2 + 0.3,
                                                                                 (y0 + y1) / 2 - 0.3, (y0 + y1) / 2 + 0.3, h + 2, DECK_H, "black").done()

    for x0 in (400, 670):                                  # open office: one linear pendant per bench
        for y0 in (-770, -610, -450):
            lin("Linear pendant, open office", x0 + 10, x0 + 152, y0 + 28, y0 + 32)
    for y0 in (-680, -520, -360):
        lin("Linear pendant, commercial", 104, 246, y0 + 28, y0 + 32)
    lin("Linear pendant, boardroom", 565, 785, -114, -110, 90)
    for x in (340, 385, 430):
        lin("Pendant, reception", x - 6, x + 6, 164, 176, 84)
    for y0 in (-1150, -810):
        lin("Linear pendant, design studio", 1205, 1303, y0 + 28, y0 + 32)
    lin("Linear pendant, design worktable", 1200, 1300, -972, -968)
    lin("Linear pendant, MD", 990, 1050, 176, 180, 88)
    lin("Linear pendant, director", 750, 806, 183, 187, 88)
    return n


def build_office():
    for key in ("Reception", "Workstations", "Meeting_Rooms", "Executive_Area", "Design_Development",
                "Support_Rooms", "Prayer_Rooms", "Washrooms", "Furniture"):
        C[key] = collection(key)
    C["New Partitions"] = collection("New Partitions", C["Walls"])
    C["Fixtures"] = collection("Fixtures", C["Lighting"])
    # new openings in existing walls
    by_id = {w["id"]: w for w in WALLS}
    for wid, op in NEW_OPENINGS:
        by_id[wid]["ops"].append(list(op))
    by_id["IW08"]["ops"] = [o for o in by_id["IW08"]["ops"] if o[0] != "D07"] + [["D22", "door", -806, -770, "Female prayer door 36\""]]


def build_office_after_shell():
    by_id = {w["id"]: w for w in WALLS}
    # infill above the 48" walls: glass or solid, cut by the doors in the low wall
    for k, (wid, a, b, treat) in enumerate(HALF_TREAT, 1):
        w = by_id[wid]
        box = (a, b, w["c0"], w["c1"]) if w["axis"] == "h" else (w["c0"], w["c1"], a, b)
        if treat == "glass":
            mid = (w["c0"] + w["c1"]) / 2
            gbox = (a, b, mid - 0.5, mid + 0.5) if w["axis"] == "h" else (mid - 0.5, mid + 0.5, a, b)
            ob = solid(f"NI{k:02d} glass above {wid}", C["New Partitions"], *gbox, HALF_H, DECK_H, "glass", status="PROPOSED")
            Item(f"NI{k:02d} frame above {wid}", C["New Partitions"]).box(*box, DECK_H - 2, DECK_H, "frame").done()
        else:
            ob = solid(f"NI{k:02d} solid infill above {wid}", C["New Partitions"], *box, HALF_H, DECK_H, "wall_new", status="PROPOSED")
        for op in w["ops"]:
            if op[2] == "door" and a <= op[2 + 0] if False else (op[1] == "door" and a < op[3] and op[2] < b):
                cut = cutter(f"{op[0]} head cut {wid}", C["Doors"], w, op[2], op[3], HALF_H - 1, LINTEL)
                boolean(ob, cut)
    for w in NEW_WALLS:
        coll = C["New Partitions"]
        if w["kind"] == "glass":
            mid = (w["c0"] + w["c1"]) / 2
            ww = dict(w, c0=mid - 0.5, c1=mid + 0.5)
            ob = build_wall(dict(ww, kind="glass"), coll, "glass")
            fb = (w["a"], w["b"], w["c0"], w["c1"]) if w["axis"] == "h" else (w["c0"], w["c1"], w["a"], w["b"])
            Item(f'{w["id"]} frame', coll).box(*fb, DECK_H - 2, DECK_H, "frame").box(*fb, 0, 3, "frame").done()
        else:
            build_wall(w, coll, "wall_new")
    for coll_name, zid, label, pts, fin in ZONES:
        z = prism(f"{zid} {label.splitlines()[0]} (floor)", C[coll_name], pts, 0, 0.4, fin, zone_id=zid, function=label.replace("\n", " "))
        x, y = LABEL_AT[zid]
        area = abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))) / 2 / 144
        body = f"{label}\n{area:,.0f} sft" if zid not in ("Z13", "Z22", "Z03") else label
        size = 15 if zid in VERTICAL_LABELS or area < 260 else 20
        text(f"{zid} label", C[coll_name], body, x, y, 150, size, "label", rot=math.pi / 2 if zid in VERTICAL_LABELS else 0)
    return furniture(), lighting_fixtures()


# =====================================================================================================
# cameras, lights, render, export
# =====================================================================================================
def cameras_and_lights():
    def cam(name, loc, rot, ortho=None, lens=None):
        cd = bpy.data.cameras.new(name)
        if ortho:
            cd.type, cd.ortho_scale = "ORTHO", ortho
        else:
            cd.lens = lens
        cd.clip_start, cd.clip_end = 0.05, 1000
        ob = bpy.data.objects.new(name, cd)
        ob.location, ob.rotation_euler = loc, rot
        C["Cameras"].objects.link(ob)
        return ob

    cx, cy = 640 * IN, -(-650) * IN
    cams = {
        "top": cam("CAM Top (orthographic plan)", (cx, -(-650) * IN * -1 if False else 650 * IN * 0 + 16.3, 60), (0, 0, 0), ortho=57.5),
        "iso": cam("CAM Isometric (open top)", (cx + 45, -(-650 * IN) * 0 + 16.5 - 45, 45),
                   (math.radians(54.7356), 0, math.radians(45)), ortho=50),
    }
    cams["top"].location = (16.25, 14.45, 60)
    cams["iso"].location = (16.25 + 40, 14.45 - 40, 40 * 1.1547 * 0.866)
    lc = C["Lighting"]
    sd = bpy.data.lights.new("Sun", "SUN")
    sd.energy, sd.angle = 3.0, math.radians(8)
    sun = bpy.data.objects.new("LGT Sun", sd)
    sun.rotation_euler = (math.radians(50), 0, math.radians(30))
    lc.objects.link(sun)
    for name, x, y in (("Room 7", 200, -500), ("Room 6", 616, -530), ("Room 8", 1100, -900), ("Front", 540, 120)):
        ld = bpy.data.lights.new(f"Area {name}", "AREA")
        ld.energy, ld.size = 800, 4.0
        ob = bpy.data.objects.new(f"LGT Area {name}", ld)
        ob.location = (x * IN, -y * IN, (DECK_H - 14) * IN)
        lc.objects.link(ob)
    return cams


def iso_fit(cam_ob, ortho):
    cam_ob.data.ortho_scale = ortho


def workbench(shadows=True):
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light, sh.color_type = "STUDIO", "MATERIAL"
    sh.show_cavity, sh.cavity_type = True, "BOTH"
    sh.show_object_outline = True
    sh.object_outline_color = (0.25, 0.25, 0.25)
    sh.show_shadows = shadows
    sh.show_specular_highlight = True
    sc.display.render_aa = "8"
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = "PNG"


def render(path, cam, res, hide=(), shadows=True):
    sc = bpy.context.scene
    workbench(shadows)
    states = {}
    for name in hide:
        if name in C:
            states[name] = C[name].hide_render
            C[name].hide_render = True
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    for name, v in states.items():
        C[name].hide_render = v
    print("RENDERED", path)


def hide_deck(hidden):
    for ob in C["Structure"].objects:
        if ob.name.startswith("Steel deck"):
            ob.hide_render = hidden


def write_schedule(path):
    with open(path, "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["id", "group", "element", "written_on_sketch", "value", "unit", "value_mm", "value_m", "status", "source", "note"])
        for row in SCHEDULE:
            rid, grp, el, written, val, unit, status, src, note = row
            mm = round(val * 25.4, 1) if unit == "in" else ""
            m = round(val * IN, 4) if unit == "in" else ""
            wr.writerow([rid, grp, el, written, val, unit, mm, m, status, src, note])
        for w in WALLS:
            for op in w["ops"]:
                oid, kind, a, b, label = op[:5]
                written, status, note = OPENING_STATUS.get(oid, (f"{b - a:g}", "MEASURED", ""))
                wr.writerow([oid, "Openings", f"{label} ({kind})", written, round(b - a, 2), "in", round((b - a) * 25.4, 1),
                             round((b - a) * IN, 4), status, "A-100", (f"height {op[5]}\", sill {LINTEL - op[5]}\"" if kind == "win" else note)])
        for i, (x, y) in enumerate(COLUMNS, 1):
            wr.writerow([f"COL{i:02d}", "Columns", f"Steel column at plan ({x}, {y})", "not measured", COL_W, "in", COL_W * 25.4,
                         round(COL_W * IN, 4), "PHOTO-EST", "Site photos", "position estimated"])


def main():
    os.makedirs(OUT, exist_ok=True)
    setup_scene()
    if PHASE == "2":
        build_office()
    build_shell()
    cams = cameras_and_lights()
    sc = bpy.context.scene
    info = {}
    if PHASE == "2":
        info["furniture"], info["fixtures"] = build_office_after_shell()
        C["Dimensions"].hide_render = True
        C["Dimensions"].hide_viewport = True
    else:
        room_labels(C["Dimensions"])
    # persp camera
    if PHASE == "2":
        persp_loc, persp_rot, lens = (330 * IN, -(30) * IN, 63 * IN), (math.radians(92), 0, math.radians(-128)), 16
    else:
        persp_loc, persp_rot, lens = (230 * IN, 40 * IN, 63 * IN), (math.radians(94), 0, math.radians(-12)), 16
    cd = bpy.data.cameras.new("CAM Perspective (eye level)")
    cd.lens, cd.clip_start = lens, 0.05
    persp = bpy.data.objects.new("CAM Perspective (eye level)", cd)
    persp.location, persp.rotation_euler = persp_loc, persp_rot
    C["Cameras"].objects.link(persp)
    stem = "garment_factory_ground_floor_phase1" if PHASE == "1" else "garment_office_ground_floor_phase2"
    blend = os.path.join(OUT, stem + ".blend")
    glb = os.path.join(OUT, stem + ".glb")
    if RENDER:
        if PHASE == "1":
            hide_deck(True)
            render(os.path.join(OUT, "top_view.png"), cams["top"], (2000, 2512), hide=("Beams",), shadows=False)
            render(os.path.join(OUT, "isometric_view.png"), cams["iso"], (2400, 1600), hide=("Dimensions",))
            hide_deck(False)
            render(os.path.join(OUT, "perspective_view.png"), persp, (2000, 1250), hide=("Dimensions",))
        else:
            hide_deck(True)
            render(os.path.join(OUT, "office_top_view.png"), cams["top"], (2000, 2512), hide=("Beams", "Lighting"), shadows=False)
            render(os.path.join(OUT, "office_isometric_view.png"), cams["iso"], (2400, 1600), hide=("Beams", "Lighting"))
            hide_deck(False)
            render(os.path.join(OUT, "office_perspective_reception.png"), persp, (2000, 1250))
    hide_deck(False)
    sc.camera = cams["iso"]
    if PHASE == "1":
        write_schedule(os.path.join(OUT, "dimension_schedule.csv"))
    bpy.ops.wm.save_as_mainfile(filepath=blend, compress=True)
    bpy.ops.export_scene.gltf(filepath=glb, export_format="GLB", use_renderable=True, export_apply=True,
                              export_extras=True, export_cameras=True, export_lights=True, export_yup=True)
    print("SAVED", blend, glb, info)


main()
