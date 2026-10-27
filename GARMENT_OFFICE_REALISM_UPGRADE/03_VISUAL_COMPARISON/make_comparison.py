"""Comparison sheets for the six flagship rooms: Cycles render | current live tour | improved build (same camera).
python3 make_comparison.py   (run in 03_VISUAL_COMPARISON after capture_rooms.js for both labels)
Writes comparison_<camera>.jpg (full width) and comparison_contact_sheet.jpg, and metrics.json (mean RGB difference to the
render at 64 px width: lower = closer)."""
import json
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "..", "..", "GARMENT_OFFICE_FINAL_PRESENTATION", "02_RENDERED_IMAGES", "final")
ROOMS = [("Reception", "CAM_01_Reception_A"), ("Experience centre", "CAM_04_Experience_Centre_A"), ("Boardroom", "CAM_09_Boardroom_A"),
         ("Managing Director's office", "CAM_07_MD_Office_A"), ("Merchandising", "CAM_11_Merchandising_A"), ("Global Design Studio", "CAM_13_Design_Studio_A")]
F = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf", 22)
FS = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Regular.otf", 17)
COLS = ["Cycles render (offline, reference)", "Live tour now (real-time)", "Improved (real-time, baked light)"]


def score(a, b):
    sz = (64, 36)
    return float(np.abs(np.asarray(a.resize(sz, Image.BOX), np.float32) - np.asarray(b.resize(sz, Image.BOX), np.float32)).mean())


metrics, rows = {}, []
for title, cam in ROOMS:
    ims = [Image.open(os.path.join(R, cam + ".jpg")).convert("RGB")]
    for label in ("current_live", "improved"):
        p = os.path.join(HERE, "shots", f"{label}_{cam}.png")
        ims.append(Image.open(p).convert("RGB") if os.path.exists(p) else Image.new("RGB", (1280, 720), (90, 90, 90)))
    ims = [im.resize((960, 540), Image.LANCZOS) for im in ims]
    metrics[cam] = dict(room=title, live_vs_render=round(score(ims[0], ims[1]), 2), improved_vs_render=round(score(ims[0], ims[2]), 2))
    sheet = Image.new("RGB", (3 * 960 + 4 * 16, 540 + 96), (246, 243, 238))
    d = ImageDraw.Draw(sheet)
    d.text((16, 14), f"{title}  ({cam})", font=F, fill=(30, 30, 28))
    for i, im in enumerate(ims):
        x = 16 + i * (960 + 16)
        sheet.paste(im, (x, 80))
        d.text((x, 52), COLS[i], font=FS, fill=(38, 103, 61) if i == 2 else (70, 70, 68))
    sheet.save(os.path.join(HERE, f"comparison_{cam}.jpg"), quality=88)
    rows.append(sheet)
W = 1800
small = [r.resize((W, round(r.height * W / r.width)), Image.LANCZOS) for r in rows]
cs = Image.new("RGB", (W, sum(s.height for s in small)), (246, 243, 238))
y = 0
for s in small:
    cs.paste(s, (0, y))
    y += s.height
cs.save(os.path.join(HERE, "comparison_contact_sheet.jpg"), quality=86)
json.dump(dict(note="mean absolute RGB difference (0-255) to the Cycles render, all images reduced to 64 x 36; lower = closer",
               rooms=metrics), open(os.path.join(HERE, "metrics.json"), "w"), indent=1)
print(json.dumps(metrics, indent=1))
