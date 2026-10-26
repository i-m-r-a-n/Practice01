"""Survey data of the ground floor (pure Python, no Blender): plan in inches, x east, y south (toward the main
gate), origin = inner north-west corner of room 1. Source: the client's hand-measured site sketches
(overview + rooms 4, 5, 6, 7, 8) and site photos, reconciled in this project (see SCHEDULE status values:
MEASURED / DERIVED / RESOLVED / ASSUMED / STANDARD / PHOTO-EST). Used by the Blender builder and the 2D drawings.
"""
IN = 0.0254                                   # metres per inch                                   # metres per inch

# =====================================================================================================
# PARAMETERS - plan (inches), survey reconstruction
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
D60_FROM_N = 7.5           # room 3 / 4 door: 7.5" from the corner on the room 4 sketch (earlier draft drew 9)
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
# GEOMETRY - as-built walls (derived: sum of sketch dimensions). ops: (id, kind, a, b, label[, window height])
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

ROOMS = {   # as-built rooms (derived: sum of sketch dimensions): polygon, label
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
    ("OV01", "Overall", "Front width, outside faces", "92'-4\" (derived)", 1108, "in", "DERIVED", "Derived from sketches", "rooms 300 + 260 + 518 + assumed walls"),
    ("OV02", "Overall", "Depth, west side (front facade to middle block north wall)", "96'-6\" (derived)", 1158, "in", "DERIVED", "Survey reconstruction", ""),
    ("OV03", "Overall", "Depth, east side (front facade to room 8 north wall)", "151'-3\" (derived)", 1815, "in", "DERIVED", "Survey reconstruction", ""),
    ("OV04", "Overall", "Gross floor area incl. walls", "12,888 sft (derived: sum of sketch dimensions)", 12888, "sft", "DERIVED", "Survey reconstruction", "changes if room 8 width changes"),
    ("R1W", "Room 1", "Width", "300", 300, "in", "MEASURED", "Room 1 sketch", "lobby, main stair, main gate"),
    ("R1D", "Room 1", "Depth", "236 (room 1 sketch) / 249 (room 3 sketch)", 247, "in", "RESOLVED", "Survey reconstruction", "front-row line shared with rooms 3 and 4"),
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
    ("HALL", "Hallway", "Length", "504", 504, "in", "MEASURED", "Survey reconstruction", "= room 6 width + 5\" wall"),
    ("STW", "Washroom row", "Width", "not measured", 96, "in", "ASSUMED", "Survey reconstruction", "outer wall in line with room 2"),
    ("STL", "Washroom row", "Length", "160 + 30 + 174 + 30 + 134 + 64 + 57 = 649", 660, "in", "RESOLVED", "Room 7 sketch", "11\" added to the first piece"),
    ("R8W", "Room 8", "Width", "not measured", 450, "in", "ASSUMED", "Survey reconstruction", "north-east stair 273 + 5 + 172"),
    ("R8WN", "Room 8", "West wall, north corner to hallway door", "657", 657, "in", "MEASURED", "Room 8 sketch", ""),
    ("R8L", "Room 8", "Length", "657 + 881", 1538, "in", "DERIVED", "Room 8 sketch", ""),
    ("NESW", "North-east stair", "Width", "30 + 49 + 194 = 273", 273, "in", "MEASURED", "Room 8 sketch", ""),
    ("NESD", "North-east stair", "Depth", "not measured", STAIR_T, "in", "ASSUMED", "Survey reconstruction", "east wall 1538 minus measured pieces = depth + 2 piers"),
    ("R8G1", "Room 8", "Wall between windows 3 and 4", "not written", G1, "in", "ASSUMED", "Survey reconstruction", ""),
    ("R8G2", "Room 8", "Wall between windows 4 and 5", "not written", G2, "in", "ASSUMED", "Survey reconstruction", ""),
    ("R8P1", "Room 8", "Stair wall to window 1", "10", 10, "in", "MEASURED", "Room 8 sketch", ""),
    ("R8P2", "Room 8", "Window 1 to window 2", "16", 16, "in", "MEASURED", "Room 8 sketch", ""),
    ("R8P3", "Room 8", "Window 2 to window 3", "49 + 10 + 48 = 107", 107, "in", "MEASURED", "Room 8 sketch", ""),
    ("R8P4", "Room 8", "Window 5 to engine room", "252", 252, "in", "MEASURED", "Room 8 sketch", ""),
    ("ENGW", "Engine room", "Width", "165", 165, "in", "MEASURED", "Room 8 sketch", "door sign reads SUB-STATION"),
    ("ENGD", "Engine room", "Depth", "96 + 68 + 49 = 213", 213, "in", "MEASURED", "Room 8 sketch", ""),
    ("SESW", "South-east stair", "Width", "277", 277, "in", "MEASURED", "Room 8 sketch", "north wall 26 + 52 + 34 + engine wall"),
    ("SESD", "South-east stair", "Depth", "204", 204, "in", "MEASURED", "Room 8 sketch", "an earlier draft drew 209; corrected to the sketch"),
    ("WT1", "Walls", "Inside wall thickness", "not measured", T_IN, "in", "ASSUMED", "Survey reconstruction", ""),
    ("WT2", "Walls", "Outside wall and row wall thickness", "not measured", T_OUT, "in", "ASSUMED", "Survey reconstruction", ""),
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
OPENING_STATUS = {"D05": ("7.5 (room 4 sketch) / 9 (earlier draft)", "MEASURED", "room 4 sketch value used"),
                  "D13": ("not written", "STANDARD", "photo shows jambs; earlier draft drew the full 48\" hallway end"),
                  "W01": ("114, height 48 (room 2 sketch)", "MEASURED", "height from the room 2 sketch")}



def beam_list():
    """Main + secondary beams (estimated from photos, PHOTO-EST): (name, x0, x1, y0, y1, depth)."""
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
    return beams


def poly_area_sft(pts):
    n = len(pts)
    return abs(sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))) / 2 / 144
