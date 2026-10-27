"""Space-optimisation layouts for Z06 Commercial & Accounts and Z07 Merchandising (pure Python).

Three alternatives per department (A operational efficiency, B balanced premium, C flexible growth) in the
same placement format as office_layout.PLACEMENTS: (key, x, y, facing, zone, z, label). Plan inches, x east,
y south, facing 0 = front looks south, 90 east, 180 north, 270 west. Option B is the selected design; the
Blender build (office_layout.py, this folder) replaces the original Z06 / Z07 fit-out with OPTIONS["B"].

Status of everything here: PROPOSED REVISED CONCEPT. Partitions are new non-structural glazed screens;
the shell, columns, beams, doors in existing walls and all six AC positions stay where they are.
"""
S, E, N, Wd = 0, 90, 180, 270

# New asset keys (builder in lib_assets / lib_props, kwargs, plan footprint w x d in inches, schedule description)
NEW_ASSETS = {
    "bench4": ("bench_desk", {"n": 4}, (220, 55), "Bench workstation 2 x 4 desks (1400 x 700 mm), 400 mm felt screen, monitors, pedestals"),
    "bench3_47": ("bench_desk", {"n": 3, "w": 47}, (141, 55), "Finance bench 2 x 3 desks (1200 x 700 mm), felt screen, monitors, lockable pedestals"),
    "bench2_47": ("bench_desk", {"n": 2, "w": 47}, (94, 55), "Bench 2 x 2 desks (1200 x 700 mm)"),
    "bench2_mob": ("bench_desk", {"n": 2}, (110, 55), "Mobile bench 2 x 2 desks (1400 x 700 mm) on locking castors"),
    "insp_table": ("inspection_table", {"w": 96, "d": 48}, (96, 48), "Sample inspection island 2440 x 1220 mm, 915 mm high, white top, daylight task light, garment props"),
    "rail_60": ("rolling_rail", {"w": 60, "seed": 51}, (60, 22), "Rolling sample rail 1520 mm, labelled by buyer / season"),
    "rail_60b": ("rolling_rail", {"w": 60, "seed": 52}, (60, 22), "Rolling sample rail 1520 mm"),
    "sample_cab_72": ("cabinet", {"w": 72, "d": 24, "h": 84, "body": "plastic_white", "front": "oak", "doors": 3}, (72, 24), "Lockable sample storage, full height 2130 mm, oak fronts"),
    "approval_counter": ("cabinet", {"w": 72, "d": 20, "h": 36, "body": "plastic_white", "front": "oak", "doors": 3, "top": "terrazzo_counter"}, (72, 20), "Approval counter 1830 mm, terrazzo top, below the trim / colour approval board"),
    "approval_board": ("pinboard_wall", {"w": 72, "h": 40, "seed": 33}, (72, 2), "Trim / colour approval board, linen"),
    "mirror_full": ("mirror_panel", {"w": 22, "h": 68}, (22, 2), "Full-length fitting mirror on the column"),
    "screen_stand_65": ("screen_stand", {"w": 57, "h": 32}, (40, 26), "65 in display on mobile stand"),
    "flip_table": ("table", {"w": 60, "d": 30, "top": "oak", "kind": "legs"}, (60, 30), "Flip-top table 1520 x 760 mm on castors (desk / review / training)"),
    "doc_counter_66": ("cabinet", {"w": 66, "d": 24, "h": 36, "body": "plastic_white", "front": "oak", "doors": 3, "top": "terrazzo_counter"}, (66, 24), "Document processing counter 1680 mm: in / out trays, scanner, cupboards"),
    "filing_120l": ("cabinet", {"w": 120, "d": 20, "h": 42, "body": "plastic_white", "front": "oak", "doors": 5, "top": "oak"}, (120, 20), "Lockable lateral filing 3050 mm, oak top (records)"),
    "filing_96l": ("cabinet", {"w": 96, "d": 20, "h": 42, "body": "plastic_white", "front": "oak", "doors": 4, "top": "oak"}, (96, 20), "Lockable lateral filing 2440 mm, oak top"),
    "dispatch_counter": ("cabinet", {"w": 60, "d": 24, "h": 36, "body": "plastic_white", "front": "oak", "doors": 3, "top": "terrazzo_counter"}, (60, 24), "Sample dispatch counter 1520 mm: courier boxes, scale, labels"),
    "archive_cab_66": ("cabinet", {"w": 66, "d": 18, "h": 84, "body": "plastic_white", "front": "oak", "doors": 3}, (66, 18), "Lockable archive cabinet, full height 2130 mm (closed financial years)"),
    "tall_cab_36": ("cabinet", {"w": 36, "d": 18, "h": 78, "body": "plastic_white", "front": "oak", "doors": 2}, (36, 18), "Stationery cabinet, full height"),
    "swatch_shelf": ("shelving", {"w": 105, "d": 14, "h": 28, "shelves": 2, "seed": 61, "mix": ("g_navy", "g_white", "g_heather", "g_sand", "g_sage", "paper")}, (105, 14), "Low swatch / tech-pack shelving"),
    "meet_round_36": ("round_table", {"dia": 36, "h": 29.5, "top": "oak"}, (36, 36), "Round table 915 mm"),
}

GROUPS = {   # schedule / metric category of every key used in Z06 / Z07
    "workstation": {"bench4", "bench3", "bench2", "bench3_47", "bench2_47", "bench2_mob", "desk_single"},
    "seat": {"task_chair", "task_chair_green", "exec_chair_black", "visitor_chair", "visitor_chair_green", "stool"},
    "storage": {"dispatch_counter", "archive_cab_66", "sample_cab_72", "filing_120l", "filing_96l", "filing_120", "tall_cab_36", "swatch_shelf", "lockers8",
                "under_window_110", "approval_counter", "doc_counter_66", "review_counter", "credenza_72"},
    "activity": {"insp_table", "rail_60", "rail_60b", "table_team", "table_guest", "meet_round", "meet_round_36", "flip_table",
                 "dress_form", "screen_stand_65"},
    "equipment": {"mfp"},
    "wall": {"pinboard_merch", "approval_board", "screen_65", "screen_55", "mirror_full", "fire_ext"},
    "plant": {"planter_l", "planter_m"},
}
STORAGE_HEIGHT = {"dispatch_counter": 36, "archive_cab_66": 84, "sample_cab_72": 84, "filing_120l": 42, "filing_96l": 42, "filing_120": 42, "tall_cab_36": 78, "swatch_shelf": 28,
                  "lockers8": 44, "under_window_110": 28, "approval_counter": 36, "doc_counter_66": 36, "review_counter": 36, "credenza_72": 30}


def group_of(key):
    for g, keys in GROUPS.items():
        if key in keys:
            return g
    return "other"


class Layout:
    def __init__(self, name):
        self.name = name
        self.items = []          # (key, x, y, facing, zone, z, label)
        self.walls = []          # partitions: dict like survey.W (id, name, axis, c0, c1, a, b, ops, glass)
        self.functions = []      # (label, x0, y0, x1, y1) designer zones for the plan legend
        self.notes = []

    def P(self, key, x, y, facing=S, zone="", z=0.0, label=None):
        self.items.append((key, x, y, facing, zone, z, label))

    def bench(self, key, cx, cy, n, w, zone, chair="task_chair", d=27.5):
        self.P(key, cx, cy, S, zone)
        L = n * w
        for k in range(n):
            x = cx - L / 2 + w * (k + 0.5)
            self.P(chair, x, cy + d + 16, N, zone)
            self.P(chair, x, cy - d - 16, S, zone)

    def wall(self, wid, name, axis, c0, c1, a, b, ops=(), glass=True, privacy=False):
        self.walls.append(dict(id=wid, name=name, axis=axis, c0=c0, c1=c1, a=a, b=b, ops=[list(o) for o in ops],
                               glass=glass, privacy=privacy))

    def zone(self, label, x0, y0, x1, y1):
        self.functions.append((label, x0, y0, x1, y1))


# =====================================================================================================
# ORIGINAL (as in GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/scripts/office_layout.py)
# =====================================================================================================
def original():
    L = Layout("Original")
    for cy in (-742.5, -582.5):
        L.bench("bench3", 487.5, cy, 3, 55, "Z07")
    L.bench("bench2", 715, -742.5, 2, 55, "Z07")
    L.P("table_team", 725, -585, S, "Z07")
    for x in (680, 710, 740, 770):
        L.P("task_chair_green", x, -623, S, "Z07")
        L.P("task_chair_green", x, -547, N, "Z07")
    L.P("review_counter", 555, -437, N, "Z07")
    L.P("pinboard_merch", 555, -428.8, N, "Z07", z=46)
    L.P("mfp", 402, -440, N, "Z07")
    L.P("lockers8", 857, -634, Wd, "Z07")
    L.P("under_window_110", 857, -738, Wd, "Z07")
    L.P("under_window_110", 857, -528, Wd, "Z07")
    L.P("planter_l", 385, -820, S, "Z07", label="PLANT:pachira")
    L.P("planter_m", 395, -470, S, "Z07", label="PLANT:calathea")
    L.P("fire_ext", 372, -500, E, "Z07", z=4)
    for cy in (-640.5, -485):
        L.bench("bench3", 170.5, cy, 3, 55, "Z06")
    L.P("desk_single", 175, -330, S, "Z06")
    L.P("exec_chair_black", 175, -298, N, "Z06")
    L.P("visitor_chair", 160, -370, S, "Z06")
    L.P("visitor_chair", 190, -370, S, "Z06")
    L.P("filing_120", 260, -241, N, "Z06")
    L.P("mfp", 272, -726, S, "Z06")
    L.P("planter_m", 60, -245, S, "Z06", label="PLANT:calathea")
    L.P("fire_ext", 51, -300, E, "Z06", z=4)
    return L


def _merch_common(L):
    """Kept in every option: lockers between the two east windows, low storage under both windows, fire extinguisher."""
    L.P("lockers8", 857, -634, Wd, "Z07")
    L.P("under_window_110", 857, -738, Wd, "Z07")
    L.P("under_window_110", 857, -528, Wd, "Z07")
    L.P("fire_ext", 372, -500, E, "Z07", z=4)


def _accounts_common(L):
    L.P("fire_ext", 51, -300, E, "Z06", z=4)      # the original lobby planter (60, -245) narrowed the washroom route to 37 in: removed


# =====================================================================================================
# OPTION A - maximum operational efficiency (open plan, no new partitions, more seats and storage)
# =====================================================================================================
def option_a():
    L = Layout("A - Operational efficiency")
    # Z07: 16 merchandiser desks west of the column line + 4 touchdown desks + team table + long review counter
    L.bench("bench4", 489, -719.5, 4, 55, "Z07")
    L.bench("bench4", 489, -604.5, 4, 55, "Z07")
    L.bench("bench2", 700, -755, 2, 55, "Z07")
    L.P("table_guest", 700, -615, S, "Z07")
    for x in (672, 700, 728):
        L.P("task_chair_green", x, -651, S, "Z07")
        L.P("task_chair_green", x, -579, N, "Z07")
    L.P("review_counter", 520, -437, N, "Z07")
    L.P("pinboard_merch", 520, -428.8, N, "Z07", z=46)
    L.P("sample_cab_72", 700, -440, N, "Z07")
    L.P("mfp", 760, -440, N, "Z07")
    L.P("swatch_shelf", 433, -831, S, "Z07")
    L.P("swatch_shelf", 545, -831, S, "Z07")
    _merch_common(L)
    L.zone("16 desks", 379, -763, 599, -561)
    L.zone("4 touchdown", 645, -800, 755, -710)
    L.zone("team table", 655, -665, 745, -565)
    L.zone("review counter", 385, -452, 655, -428)
    # Z06: 16 finance desks (12 + 4 growth), manager, filing on the east half wall, processing counter
    L.bench("bench4_47", 206, -582.5, 4, 47, "Z06")
    L.bench("bench4_47", 206, -467.5, 4, 47, "Z06")
    L.P("desk_single", 205, -350, S, "Z06")
    L.P("exec_chair_black", 205, -318, N, "Z06")
    L.P("filing_120l", 352, -620, Wd, "Z06")
    L.P("filing_120l", 352, -490, Wd, "Z06")
    L.P("filing_96l", 352, -370, Wd, "Z06")
    L.P("doc_counter_66", 217, -243, N, "Z06")
    L.P("mfp", 172, -243, N, "Z06")
    L.P("filing_96l", 314, -241, N, "Z06")
    _accounts_common(L)
    L.zone("16 desks", 112, -626, 300, -424)
    L.zone("manager", 170, -366, 240, -305)
    L.zone("records", 342, -680, 362, -322)
    return L


NEW_ASSETS["bench4_47"] = ("bench_desk", {"n": 4, "w": 47}, (188, 55), "Bench 2 x 4 desks (1200 x 700 mm)")
GROUPS["workstation"].add("bench4_47")


# =====================================================================================================
# OPTION B - balanced premium (SELECTED)
# =====================================================================================================
def option_b():
    L = Layout("B - Balanced premium (selected)")
    # ---------------- Z07 Merchandising: desk neighbourhood west of the column line, sample hub east, spine D11 -> D49
    L.bench("bench4", 489, -724.5, 4, 55, "Z07")              # column (616, -633) sits beside the end of bench 2,
    L.bench("bench4", 489, -609.5, 4, 55, "Z07")              # not in the mouth of the aisle between the benches
    L.P("swatch_shelf", 433, -831, S, "Z07")                     # tech-pack / swatch library along the hallway half wall
    L.P("swatch_shelf", 545, -831, S, "Z07")
    L.P("approval_counter", 416, -438, N, "Z07")                  # low approval counter at the west end keeps the saved
    L.P("approval_board", 416, -428.8, N, "Z07", z=46)             # camera CAM_11 (378, -440, 64 in) clear
    L.P("sample_cab_72", 490, -440, N, "Z07")                     # lockable sample storage on the full-height display wall
    L.P("sample_cab_72", 564, -440, N, "Z07")
    L.P("mfp", 616, -440, N, "Z07")
    L.P("dispatch_counter", 379, -535, E, "Z07")                   # courier dispatch of approval samples, by the west half wall
    # sample hub
    L.P("rail_60", 660, -805, S, "Z07")
    L.P("rail_60b", 735, -805, S, "Z07")
    L.P("dress_form", 682, -745, S, "Z07")
    L.P("dress_form", 718, -745, S, "Z07")
    L.P("mirror_full", 622, -633, E, "Z07", z=6)
    L.P("insp_table", 700, -650, E, "Z07")
    L.P("table_guest", 700, -520, E, "Z07")                       # buyer review / video-call table
    for y in (-545, -520, -495):
        L.P("task_chair_green", 664, y, E, "Z07")
        L.P("task_chair_green", 736, y, Wd, "Z07")
    L.P("screen_65", 700, -428.9, N, "Z07", z=40)
    L.P("screen_55", 865, -634, Wd, "Z07", z=52)                  # T&A / production milestone dashboard over the lockers
    _merch_common(L)
    L.P("planter_m", 606, -828, S, "Z07", label="PLANT:calathea")
    L.P("planter_m", 385, -475, S, "Z07", label="PLANT:calathea")
    L.zone("16 merchandiser desks", 379, -768, 599, -566)
    L.zone("tech-pack + swatch shelves", 380, -838, 598, -824)
    L.zone("sample storage + approval wall", 380, -452, 628, -428)
    L.zone("sample rails", 630, -816, 765, -794)
    L.zone("dispatch", 367, -565, 391, -505)
    L.zone("inspection island", 676, -698, 724, -602)
    L.zone("buyer review + screen", 651, -562, 749, -428)
    L.zone("circulation spine D11 - D49", 780, -838, 848, -428)
    # ---------------- Z06 Commercial & Accounts: public L-corridor kept clear, finance suite behind privacy glass
    L.wall("NP34", "Accounts suite - public corridor (privacy glass)", "v", 106, 109, -687, -290, privacy=True)
    L.wall("NP35", "Accounts suite - staff arrival (privacy glass)", "h", -293, -290, 106, 163,
           [("D50", "door", 112, 154, "Accounts suite entrance 42\"")], privacy=True)
    L.wall("NP36", "Staff corridor - accounts suite, glass", "v", 160, 163, -290, -231, privacy=True)
    L.wall("NP37", "Accounts suite - north corridor (privacy glass)", "h", -690, -687, 106, 362,
           [("D51", "door", 300, 342, "Accounts suite - north corridor 42\"")], privacy=True)
    L.wall("NP38", "Finance discussion room west, glass", "v", 257, 260, -338, -231, privacy=True)
    L.wall("NP39", "Finance discussion room north, glass", "h", -338, -335, 257, 362,
           [("D52", "door", 262, 302, "Finance discussion room (sliding) 40\"")], privacy=True)
    L.bench("bench3_47", 219.5, -615, 3, 47, "Z06")
    L.bench("bench3_47", 219.5, -500, 3, 47, "Z06")
    L.P("desk_single", 205, -390, S, "Z06")                       # manager: faces the team, next to the entrance
    L.P("exec_chair_black", 205, -358, N, "Z06")
    L.P("filing_120l", 352, -626, Wd, "Z06")
    L.P("filing_120l", 352, -505, Wd, "Z06")
    L.P("filing_96l", 352, -396, Wd, "Z06")
    L.P("doc_counter_66", 222, -243, N, "Z06")
    L.P("mfp", 175, -243, N, "Z06")
    L.P("meet_round_36", 311, -284, S, "Z06")
    for x, y, f in ((311, -312, S), (311, -256, N), (283, -284, E), (339, -284, Wd)):
        L.P("visitor_chair", x, y, f, "Z06")
    L.P("tall_cab_36", 351, -250, Wd, "Z06")
    L.P("archive_cab_66", 263, -792, E, "Z06")                    # unused bay at the hallway end, against the audit room wall
    _accounts_common(L)
    L.zone("archive", 254, -825, 272, -759)
    L.zone("12 finance desks", 149, -658, 290, -457)
    L.zone("manager", 173, -406, 237, -345)
    L.zone("secure records", 342, -688, 362, -352)
    L.zone("document processing", 163, -255, 255, -231)
    L.zone("finance discussion", 260, -335, 362, -231)
    L.zone("public corridor", 46, -740, 106, -231)
    L.zone("public corridor", 106, -740, 362, -690)
    return L


# =====================================================================================================
# OPTION C - flexible growth (mobile benches, multipurpose project zone, +8 seats only where clearances allow)
# =====================================================================================================
def option_c():
    L = Layout("C - Flexible growth")
    for cx in (431.5, 546.5):
        for cy in (-724.5, -609.5):
            L.bench("bench2_mob", cx, cy, 2, 55, "Z07")
    L.P("swatch_shelf", 433, -831, S, "Z07")
    L.P("swatch_shelf", 545, -831, S, "Z07")
    L.P("sample_cab_72", 416, -440, N, "Z07")
    L.P("sample_cab_72", 490, -440, N, "Z07")
    L.P("approval_counter", 564, -438, N, "Z07")
    L.P("approval_board", 564, -428.8, N, "Z07", z=46)
    L.P("mfp", 616, -440, N, "Z07")
    L.P("rail_60", 660, -805, S, "Z07")
    L.P("rail_60b", 735, -805, S, "Z07")
    for cx in (665, 735):                                          # project zone: 4 flip-top tables (8 seats / 8 growth desks)
        for cy in (-690, -585):
            L.P("flip_table", cx, cy, S, "Z07")
            L.P("task_chair_green", cx, cy + 31, N, "Z07")
            L.P("task_chair_green", cx, cy - 31, S, "Z07")
    L.P("screen_stand_65", 700, -480, N, "Z07")
    _merch_common(L)
    L.zone("16 desks (mobile)", 376, -768, 602, -566)
    L.zone("project zone: 8 seats / growth", 635, -734, 765, -541)
    L.zone("sample rails", 630, -816, 765, -794)
    # Z06: mobile benches, one glazed screen to the corridor only, flexible table that becomes 4 growth desks
    L.wall("NP34", "Accounts - public corridor (privacy glass)", "v", 106, 109, -687, -290, privacy=True)
    L.bench("bench2_47", 172, -615, 2, 47, "Z06")
    L.bench("bench2_47", 172, -500, 2, 47, "Z06")
    L.bench("bench2_47", 270, -500, 2, 47, "Z06")
    L.P("desk_single", 205, -390, S, "Z06")
    L.P("exec_chair_black", 205, -358, N, "Z06")
    L.P("flip_table", 255, -615, E, "Z06")
    for y in (-650, -580):
        L.P("visitor_chair", 281, y, Wd, "Z06")
    L.P("filing_120l", 352, -626, Wd, "Z06")
    L.P("filing_96l", 352, -396, Wd, "Z06")
    L.P("doc_counter_66", 217, -243, N, "Z06")
    L.P("mfp", 172, -243, N, "Z06")
    L.P("filing_96l", 314, -241, N, "Z06")
    _accounts_common(L)
    L.zone("12 desks (mobile)", 125, -658, 317, -457)
    L.zone("flex table / 4 growth", 245, -650, 290, -580)
    return L


OPTIONS = {"original": original, "A": option_a, "B": option_b, "C": option_c}
