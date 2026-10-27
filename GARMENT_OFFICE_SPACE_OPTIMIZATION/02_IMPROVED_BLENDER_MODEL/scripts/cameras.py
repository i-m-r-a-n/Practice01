"""Camera set (plan inches: x east, y south, z height). Perspective cameras stay level (vertical lines vertical,
two-point perspective) and use lens shift for the vertical framing. priority 1 = presentation key views."""
import math

IN = 0.0254
CAMERAS = [
    # ---------------- priority 1: key presentation spaces
    dict(name="CAM_01_Reception_A", room="Reception", priority=1, pos=(318, 26, 60), target=(520, 170, 50), lens=18),
    dict(name="CAM_02_Reception_B", room="Reception", priority=1, pos=(442, 238, 58), target=(573, 70, 56), lens=19),
    dict(name="CAM_03_Entrance_Lobby", room="Entrance lobby", priority=1, pos=(246, 226, 64), target=(222, 0, 60), lens=19),
    dict(name="CAM_04_Experience_Centre_A", room="Experience centre", priority=1, pos=(392, -226, 62), target=(700, -405, 50), lens=18),
    dict(name="CAM_05_Experience_Centre_B", room="Experience centre", priority=1, pos=(852, -232, 62), target=(430, -385, 56), lens=18),
    dict(name="CAM_06_Experience_Centre_Detail", room="Experience centre", priority=1, pos=(575, -262, 50), target=(500, -380, 48), lens=26),
    dict(name="CAM_07_MD_Office_A", room="MD office", priority=1, pos=(870, 64, 60), target=(1040, 225, 54), lens=18),
    dict(name="CAM_08_MD_Office_B", room="MD office", priority=1, pos=(1082, 212, 58), target=(875, 110, 46), lens=18),
    dict(name="CAM_09_Boardroom_A", room="Boardroom", priority=1, pos=(860, -200, 62), target=(490, -100, 56), lens=18),
    dict(name="CAM_10_Boardroom_B", room="Boardroom", priority=1, pos=(494, -45, 62), target=(810, -160, 46), lens=18),
    dict(name="CAM_11_Merchandising_A", room="Merchandising (open office)", priority=1, pos=(378, -440, 64), target=(720, -770, 40), lens=18),
    dict(name="CAM_12_Merchandising_B", room="Merchandising (open office)", priority=1, pos=(856, -832, 64), target=(440, -500, 44), lens=18),
    dict(name="CAM_13_Design_Studio_A", room="Global Design Studio", priority=1, pos=(1112, -538, 62), target=(1290, -900, 50), lens=18),
    dict(name="CAM_14_Design_Studio_B", room="Global Design Studio", priority=1, pos=(1318, -1200, 62), target=(1165, -905, 48), lens=18),
    dict(name="CAM_15_CAD_Room", room="CAD / technical design", priority=1, pos=(1033, -245, 60), target=(885, -50, 44), lens=18),
    dict(name="CAM_16_Commercial_Accounts", room="Commercial & accounts", priority=1, pos=(352, -405, 62), target=(60, -680, 40), lens=18),
    # ---------------- priority 2: all other rooms
    dict(name="CAM_17_Executive_Reception", room="Executive reception (PA)", priority=2, pos=(696, 8, 60), target=(578, 205, 46), lens=18),
    dict(name="CAM_18_Director", room="Director", priority=2, pos=(708, 64, 58), target=(830, 225, 46), lens=18),
    dict(name="CAM_19_HR_Admin", room="HR & admin", priority=2, pos=(356, -16, 60), target=(175, -215, 40), lens=18),
    dict(name="CAM_20_Staff_Cafe", room="Staff cafe + pantry", priority=2, pos=(1066, -912, 62), target=(890, -1210, 40), lens=18),
    dict(name="CAM_21_Lounge_Training", room="Staff lounge / training", priority=2, pos=(1066, -1258, 62), target=(890, -1520, 40), lens=18),
    dict(name="CAM_22_Prayer_Male", room="Prayer (male)", priority=2, pos=(1162, -1292, 60), target=(1320, -1432, 28), lens=18),
    dict(name="CAM_23_Sample_Room", room="Sample development", priority=2, pos=(1031, -645, 60), target=(885, -800, 40), lens=18),
    dict(name="CAM_24_3D_Printing_Lab", room="3D printing lab", priority=2, pos=(1031, -492, 60), target=(885, -592, 40), lens=18),
    dict(name="CAM_25_Fabric_Library", room="Fabric, colour & trim library", priority=2, pos=(1030, -428, 60), target=(895, -290, 42), lens=18),
    dict(name="CAM_26_Guest_Workspace", room="Guest workspace", priority=2, pos=(98, -16, 60), target=(-45, -145, 40), lens=18),
    dict(name="CAM_27_Audit_Room", room="Audit room", priority=2, pos=(244, -750, 58), target=(108, -885, 40), lens=18),
    dict(name="CAM_28_Washroom_Male", room="Washroom (male)", priority=2, pos=(36, -238, 60), target=(-50, -440, 40), lens=18),
    dict(name="CAM_29_Washroom_Female", room="Washroom (female)", priority=2, pos=(36, -525, 60), target=(-50, -700, 40), lens=18),
    dict(name="CAM_30_Prayer_Female", room="Prayer (female)", priority=2, pos=(34, -768, 58), target=(-45, -880, 24), lens=16),
    dict(name="CAM_31_Executive_Corridor", room="Executive corridor", priority=2, pos=(706, 28, 60), target=(1088, 28, 52), lens=20),
    dict(name="CAM_32_Design_Corridor", room="Corridor (design wing)", priority=2, pos=(1070, -560, 62), target=(1070, -880, 50), lens=20),
    dict(name="CAM_33_Wudu_Male", room="Wudu (male)", priority=2, pos=(1160, -1220, 60), target=(1320, -1250, 30), lens=18),
]


def _ortho(name, target_m, rx_deg, rz_deg, dist, scale, room, priority=1, exposure="-0.3"):
    rx, rz = math.radians(rx_deg), math.radians(rz_deg)
    d = (-math.sin(rx) * math.sin(rz), math.sin(rx) * math.cos(rz), -math.cos(rx))
    loc = tuple(t - v * dist for t, v in zip(target_m, d))
    return dict(name=name, room=room, priority=priority, ortho=scale, loc_m=loc, rot_deg=(rx_deg, 0, rz_deg), exposure=exposure)


# plan extents: x -65..1336, y -1558..257 (inches) -> centre in metres
_cx = (-65 + 1336) / 2 * IN
_cy = -((-1558 + 257) / 2) * IN
CAMERAS += [
    dict(name="CAM_TOP_Plan", room="Whole floor", priority=1, ortho=49.0, loc_m=(_cx, _cy, 60.0), rot_deg=(0, 0, 0), exposure="-0.3"),  # render portrait 1240 x 1600
    _ortho("CAM_ISO_SE", (_cx + 1.84, _cy - 1.46, -0.82), 47, 38, 120, 58.6, "Whole floor"),          # centred on the projected outline
    _ortho("CAM_ISO_SW", (_cx + 2.53, _cy - 1.84, 1.75), 47, -38, 120, 59.0, "Whole floor"),          # render 4:3 (1600 x 1200)
    _ortho("CAM_ISO_Front_Zone", (13.8, 2.2, 0.0), 50, 32, 100, 24.0, "Visitor zone (lobby, reception, experience centre, boardroom, executive suite)"),
    _ortho("CAM_ISO_Design_Wing", (28.0, 19.8, 0.0), 50, 140, 100, 26.0, "Design development wing + staff support"),
]

# ---------------- space optimisation (Z06 / Z07 option B): extra views of the redesigned departments
CAMERAS += [
    dict(name="CAM_34_Merchandising_Sample_Hub", room="Merchandising (sample hub)", priority=1, pos=(838, -452, 62), target=(640, -770, 44), lens=18),
    dict(name="CAM_35_Merchandising_Desks", room="Merchandising (team desks)", priority=1, pos=(770, -690, 62), target=(380, -640, 40), lens=19),
    dict(name="CAM_36_Accounts_Suite", room="Commercial & accounts (finance suite)", priority=1, pos=(122, -300, 62), target=(300, -650, 42), lens=18),
    dict(name="CAM_37_Accounts_Records_Discussion", room="Commercial & accounts (records + discussion room)", priority=1, pos=(336, -680, 60), target=(240, -262, 40), lens=18),
    dict(name="CAM_38_Accounts_Public_Corridor", room="Commercial & accounts (public corridor)", priority=2, pos=(80, -262, 60), target=(80, -860, 44), lens=18),
    dict(name="CAM_TOP_Z06_Z07", room="Merchandising + Commercial & accounts (plan)", priority=1, ortho=21.6, loc_m=(456 * IN, 562 * IN, 60.0), rot_deg=(0, 0, 0), exposure="-0.3"),
    _ortho("CAM_ISO_Z06_Z07", (456 * IN, 562 * IN, 0.0), 48, 28, 100, 19.5, "Merchandising + Commercial & accounts"),
]
