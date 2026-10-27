"""Contact sheets for the camera QC: final Cycles render (left) | web GLB in three.js from the same camera (right).
python3 make_qc_sheets.py   (run in 05_PRODUCTION/camera_qc after run_camera_qc.js)"""
import json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
R = '../../../GARMENT_OFFICE_FINAL_PRESENTATION/02_RENDERED_IMAGES/final'
meta = json.load(open('../../07_WEB_TOUR_ASSETS/office_web_metadata.json'))
F = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-SemiBold.otf', 20)
FS = ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Regular.otf', 16)
TW = 560
rows = []
for c in meta['cameras']:
    a = Image.open(os.path.join(R, c['name'] + '.jpg')).convert('RGB')
    b = Image.open(f"shots/web_{c['name']}.jpg").convert('RGB')
    h = round(TW * a.height / a.width)
    rows.append((c, a.resize((TW, h), Image.LANCZOS), b.resize((TW, h), Image.LANCZOS)))
per = 8
pages = []
for p in range(0, len(rows), per):
    chunk = rows[p:p + per]
    H = sum(r[1].height + 40 for r in chunk) + 70
    sheet = Image.new('RGB', (TW * 2 + 60, H), (246, 243, 238))
    d = ImageDraw.Draw(sheet)
    d.text((20, 18), 'Camera QC  -  left: final Cycles render  |  right: web GLB in three.js r169 (same camera matrix, fov, lens shift)', font=F, fill=(30, 30, 28))
    y = 60
    for c, a, b in chunk:
        d.text((20, y), f"{c['name']}  ({c['room']})", font=FS, fill=(38, 103, 61))
        sheet.paste(a, (20, y + 22)); sheet.paste(b, (40 + TW, y + 22))
        y += a.height + 40
    fn = f'camera_qc_sheet_{p // per + 1}.jpg'
    sheet.save(fn, quality=88)
    pages.append(fn)
# web GLB vs original GLB, same real-time renderer
diffs = {}
for n in ['CAM_01_Reception_A', 'CAM_04_Experience_Centre_A', 'CAM_09_Boardroom_A', 'CAM_13_Design_Studio_A', 'CAM_07_MD_Office_A', 'CAM_ISO_SE']:
    w = np.asarray(Image.open(f'shots/web_{n}.jpg').convert('RGB'), np.float32)
    o = np.asarray(Image.open(f'shots/original_{n}.jpg').convert('RGB'), np.float32)
    dd = np.abs(w - o)
    diffs[n] = dict(mean_abs_diff_0_255=round(float(dd.mean()), 3), pixels_diff_gt_16=round(float((dd.max(2) > 16).mean() * 100), 3))
json.dump(dict(sheets=pages, web_vs_original=diffs), open('camera_qc_summary.json', 'w'), indent=1)
print(pages, json.dumps(diffs))
