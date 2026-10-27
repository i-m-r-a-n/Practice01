"""Renders walkthrough shots from Office_Walkthrough_Animation.blend (cameras WT_<shot>, keyed visibility and exposure).

blender -b Office_Walkthrough_Animation.blend --python render_shots.py -- --out DIR [--shots A|B|ALL|name,name]
        [--res 1280x720] [--samples 4] [--story]
- default: every 2nd frame of each shot (12 fps from the 24 fps timeline) into DIR/<shot>/f_####.png; existing frames
  are skipped, so an interrupted render resumes where it stopped; per-frame times go to DIR/render_times.csv
- --story: only the first, middle and last frame of each shot (storyboard check)
"""
import csv
import os
import sys
import time

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import shots as S  # noqa: E402
from cycles_anim_setup import setup_cycles_anim  # noqa: E402

A = sys.argv[sys.argv.index("--") + 1:]


def arg(k, d=None):
    return A[A.index(k) + 1] if k in A else d


OUT = os.path.abspath(arg("--out"))
SEL = arg("--shots", "ALL")
W, H = (int(v) for v in arg("--res", "1280x720").split("x"))
SAMPLES = int(arg("--samples", "4"))
STORY = "--story" in A
sc = bpy.context.scene
setup_cycles_anim(sc, samples=SAMPLES, res=(W, H))
sc.render.image_settings.file_format = "PNG"
sc.render.image_settings.color_depth = "8"
sc.render.use_overwrite = False
sc.render.use_placeholder = True
order = [s for s in S.SHOTS if s["video"] == "A"] + [s for s in S.SHOTS if s["video"] == "B"]
if SEL in ("A", "B"):
    order = [s for s in order if s["video"] == SEL]
elif SEL != "ALL":
    want = SEL.split(",")
    order = [s for s in order if s["name"] in want]
os.makedirs(OUT, exist_ok=True)
log_path = os.path.join(OUT, "render_times.csv")
new_log = not os.path.exists(log_path)
logf = open(log_path, "a", newline="")
log = csv.writer(logf)
if new_log:
    log.writerow(["shot", "frame", "seconds", "res", "samples"])
state = {"t": 0.0, "shot": ""}
bpy.app.handlers.render_pre.append(lambda s, d=None: state.__setitem__("t", time.time()))


def post(s, d=None):
    log.writerow([state["shot"], s.frame_current, round(time.time() - state["t"], 1), f"{W}x{H}", SAMPLES])
    logf.flush()


bpy.app.handlers.render_post.append(post)
for shot in order:
    cam = bpy.data.objects["WT_" + shot["name"]]
    f0, f1 = cam["frame_start"], cam["frame_end"]
    sc.camera = cam
    state["shot"] = shot["name"]
    d = os.path.join(OUT, shot["name"])
    os.makedirs(d, exist_ok=True)
    if STORY:
        for f in (f0, (f0 + f1) // 2, f1):
            path = os.path.join(d, f"f_{f:04d}.png")
            if os.path.exists(path):
                continue
            sc.frame_set(f)
            sc.render.filepath = path
            bpy.ops.render.render(write_still=True)
    else:
        sc.frame_start, sc.frame_end, sc.frame_step = f0, f1, 24 // S.FPS_RENDER
        sc.render.filepath = os.path.join(d, "f_")
        bpy.ops.render.render(animation=True)
    print("SHOT_DONE", shot["name"], time.strftime("%H:%M:%S"), flush=True)
logf.close()
print("ALL_DONE", flush=True)
