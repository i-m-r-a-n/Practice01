"""Shot list for the walkthrough videos (pure data, no bpy).
Interior shots: plan inches (x east, y south, z height), as in GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/scripts/cameras.py;
each move starts and ends near a camera position that was already rendered and checked for the stills.
Overview shots: metres in Blender coordinates around the building centre.
fields: name, video ("A" = client pitch + full tour, "B" = full tour only), scene label, kind, duration (s), params
"""
FPS_RENDER = 12          # rendered frames per second (motion-interpolated to 24 fps in the edit)
CENTRE = (16.14, 16.52)  # Blender metres, centre of the building outline

SHOTS = [
    # ---------------- client pitch (A), in story order
    dict(name="A01_overview_orbit", video="A", scene="Overview", label="The complete ground floor", kind="orbit", dur=8.0,
         target=(16.14, 16.52, 0.0), dist=(96.0, 90.0), elev=(41.0, 39.0), azim=(-74.0, -38.0), lens=50),
    dict(name="A02_entrance_lobby", video="A", scene="Main entrance", label="Entrance lobby", kind="dolly", dur=6.0,
         pos=((250, 230, 62), (238, 176, 62)), tgt=((222, 0, 60), (210, 0, 60)), lens=20),
    dict(name="A03_reception", video="A", scene="Reception", label="Reception", kind="dolly", dur=6.0,
         pos=((322, 32, 60), (352, 18, 60)), tgt=((520, 175, 50), (545, 150, 52)), lens=18),
    dict(name="A04_reception_logo", video="A", scene="Reception", label="Reception", kind="dolly", dur=5.0,
         pos=((442, 238, 58), (458, 216, 57)), tgt=((573, 70, 56), (573, 74, 56)), lens=19),
    dict(name="A05_experience_centre", video="A", scene="Experience centre", label="Experience centre", kind="dolly", dur=7.0,
         pos=((384, -228, 62), (440, -246, 62)), tgt=((700, -405, 50), (730, -395, 50)), lens=18),
    dict(name="A06_experience_story_wall", video="A", scene="Experience centre", label="Experience centre", kind="dolly", dur=6.0,
         pos=((856, -234, 62), (800, -246, 62)), tgt=((430, -385, 56), (420, -375, 54)), lens=18),
    dict(name="A07_boardroom", video="A", scene="Boardroom", label="Boardroom", kind="dolly", dur=6.0,
         pos=((858, -198, 62), (790, -200, 62)), tgt=((490, -100, 56), (495, -110, 54)), lens=18),
    dict(name="A08_md_office", video="A", scene="Executive suite", label="Managing Director's office", kind="dolly", dur=6.0,
         pos=((868, 72, 60), (898, 98, 58)), tgt=((1040, 225, 54), (1046, 218, 52)), lens=18),
    dict(name="A09_merchandising", video="A", scene="Corporate workspaces", label="Merchandising", kind="dolly", dur=5.0,
         pos=((380, -444, 64), (436, -468, 64)), tgt=((720, -770, 40), (756, -770, 42)), lens=18),
    dict(name="A10_design_studio", video="A", scene="Design & development", label="Global Design Studio", kind="dolly", dur=6.0,
         pos=((1112, -542, 62), (1130, -590, 62)), tgt=((1290, -900, 50), (1298, -890, 50)), lens=18),
    dict(name="A11_staff_cafe", video="A", scene="Staff facilities", label="Staff cafe", kind="dolly", dur=5.0,
         pos=((1066, -914, 62), (1044, -955, 62)), tgt=((890, -1210, 40), (884, -1196, 42)), lens=18),
    dict(name="A12_overview_final", video="A", scene="Final reveal", label="", kind="crane", dur=8.0,
         target=((13.8, 2.2, 0.0), (16.14, 16.52, 0.0)), dist=(30.0, 94.0), elev=(50.0, 40.0), azim=(-58.0, -48.0), lens=50),
    # ---------------- full tour only (B), placed by scene in the edit
    dict(name="B01_experience_detail", video="B", scene="Experience centre", label="Experience centre - display", kind="dolly", dur=3.0,
         pos=((582, -262, 50), (566, -262, 50)), tgt=((500, -380, 48), (492, -380, 48)), lens=26),
    dict(name="B02_boardroom_east", video="B", scene="Boardroom", label="Boardroom", kind="dolly", dur=3.0,
         pos=((494, -45, 62), (514, -52, 62)), tgt=((810, -160, 46), (814, -160, 46)), lens=18),
    dict(name="B03_executive_reception", video="B", scene="Executive suite", label="Executive reception", kind="dolly", dur=3.0,
         pos=((696, 10, 60), (690, 26, 60)), tgt=((578, 205, 46), (582, 205, 46)), lens=18),
    dict(name="B04_director", video="B", scene="Executive suite", label="Director's office", kind="dolly", dur=3.0,
         pos=((716, 74, 58), (727, 88, 58)), tgt=((830, 225, 46), (834, 222, 46)), lens=18),
    dict(name="B05_executive_corridor", video="B", scene="Executive suite", label="Executive corridor", kind="dolly", dur=3.5,
         pos=((706, 28, 60), (752, 28, 60)), tgt=((1088, 28, 52), (1088, 28, 52)), lens=20),
    dict(name="B06_commercial", video="B", scene="Corporate workspaces", label="Commercial & accounts", kind="dolly", dur=3.0,
         pos=((352, -405, 62), (336, -424, 62)), tgt=((60, -680, 40), (60, -690, 40)), lens=18),
    dict(name="B07_hr_admin", video="B", scene="Corporate workspaces", label="HR & administration", kind="dolly", dur=3.0,
         pos=((356, -18, 60), (344, -34, 60)), tgt=((175, -215, 40), (175, -215, 40)), lens=18),
    dict(name="B08_merchandising_team", video="B", scene="Corporate workspaces", label="Merchandising", kind="dolly", dur=3.0,
         pos=((856, -830, 64), (836, -814, 64)), tgt=((440, -500, 44), (440, -500, 44)), lens=18),
    dict(name="B09_cad", video="B", scene="Design & development", label="CAD / technical design", kind="dolly", dur=3.0,
         pos=((1033, -247, 60), (1022, -230, 60)), tgt=((885, -50, 44), (885, -50, 44)), lens=18),
    dict(name="B10_sample_room", video="B", scene="Design & development", label="Sample development", kind="dolly", dur=3.0,
         pos=((1031, -645, 60), (1020, -660, 60)), tgt=((885, -800, 40), (885, -800, 40)), lens=18),
    dict(name="B11_fabric_library", video="B", scene="Design & development", label="Fabric & trim library", kind="dolly", dur=3.0,
         pos=((1022, -414, 60), (1010, -402, 60)), tgt=((895, -290, 42), (895, -290, 42)), lens=18),
    dict(name="B12_3d_lab", video="B", scene="Design & development", label="3D printing lab", kind="dolly", dur=3.0,
         pos=((1031, -494, 60), (1020, -504, 60)), tgt=((885, -592, 40), (885, -592, 40)), lens=18),
    dict(name="B13_design_corridor", video="B", scene="Design & development", label="Design wing corridor", kind="dolly", dur=3.5,
         pos=((1070, -565, 62), (1070, -608, 62)), tgt=((1070, -880, 50), (1070, -880, 50)), lens=20),
    dict(name="B14_studio_workstations", video="B", scene="Design & development", label="Global Design Studio", kind="dolly", dur=3.5,
         pos=((1318, -1198, 62), (1306, -1172, 62)), tgt=((1165, -905, 48), (1165, -905, 48)), lens=18),
    dict(name="B15_lounge", video="B", scene="Staff facilities", label="Staff lounge / training", kind="dolly", dur=3.0,
         pos=((1066, -1260, 62), (1052, -1284, 62)), tgt=((890, -1520, 40), (890, -1520, 40)), lens=18),
    dict(name="B16_prayer_male", video="B", scene="Staff facilities", label="Prayer room", kind="dolly", dur=3.0,
         pos=((1164, -1294, 60), (1176, -1306, 60)), tgt=((1320, -1432, 28), (1320, -1432, 28)), lens=18),
]

# edit order of the full tour (B): pitch shots plus the extra rooms, grouped by scene
TOUR_ORDER = ["A01_overview_orbit", "A02_entrance_lobby", "A03_reception", "A04_reception_logo",
              "A05_experience_centre", "A06_experience_story_wall", "B01_experience_detail",
              "A07_boardroom", "B02_boardroom_east",
              "B03_executive_reception", "B05_executive_corridor", "B04_director", "A08_md_office",
              "B07_hr_admin", "B06_commercial", "A09_merchandising", "B08_merchandising_team",
              "B09_cad", "B11_fabric_library", "B12_3d_lab", "B10_sample_room", "B13_design_corridor",
              "A10_design_studio", "B14_studio_workstations",
              "A11_staff_cafe", "B15_lounge", "B16_prayer_male",
              "A12_overview_final"]
PITCH_ORDER = [s["name"] for s in SHOTS if s["video"] == "A"]


def frames(shot):
    return int(round(shot["dur"] * FPS_RENDER)) + 1
