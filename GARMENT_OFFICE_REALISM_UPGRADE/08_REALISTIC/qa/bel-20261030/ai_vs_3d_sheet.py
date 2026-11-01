"""One sheet with each AI concept image beside the render of the same camera in the 3D model (concept-images/model/), in tour order
(the three room images last). It shows where an AI image differs from the 3D. Nothing is retouched: images are scaled and cropped to 16:9.
python3 -I ai_vs_3d_sheet.py OUT.jpg"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

R = Path(__file__).resolve().parents[2]
F = lambda s, b=False: ImageFont.truetype(f"/usr/share/fonts/truetype/crosextra/Carlito-{'Bold' if b else 'Regular'}.ttf", s)
cfg = json.loads((R / 'viewer/bel-config.json').read_text()); stills = cfg['conceptStills']
names = {t['camera']: f"{i + 1:02d} · {t['title']}" for i, t in enumerate(cfg['tour'])}
names.update({'CAM_07_MD_Office_A': 'Room · MD office', 'CAM_25_Fabric_Library': 'Room · fibre library', 'CAM_23_Sample_Room': 'Room · sample room'})
order = [t['camera'] for t in cfg['tour']] + ['CAM_07_MD_Office_A', 'CAM_25_Fabric_Library', 'CAM_23_Sample_Room']
pairs = [(c, stills[c]) for c in order if isinstance(stills.get(c), dict) and stills[c].get('model')]
PW, PH, M, LB = 560, 315, 14, 40


def fit(path):
    im = Image.open(R / path).convert('RGB'); r = max(PW / im.width, PH / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS); x, y = (im.width - PW) // 2, (im.height - PH) // 2
    return im.crop((x, y, x + PW, y + PH))


W = M + 2 * (2 * PW + M) + 3 * M
rows = (len(pairs) + 1) // 2
sheet = Image.new('RGB', (W, 70 + rows * (LB + PH + 24 + M) + M), (20, 26, 22)); d = ImageDraw.Draw(sheet)
d.text((M, 18), f'STAGE II · Zara Fashion · AI concept image (left, gold) beside the same camera in the 3D model (right, green) · {len(pairs)} views', font=F(26, True), fill=(235, 230, 215))
for k, (cam, v) in enumerate(pairs):
    x = M + (k % 2) * (2 * PW + 3 * M); y = 70 + (k // 2) * (LB + PH + 24 + M)
    d.text((x, y + 6), names.get(cam, cam), font=F(24, True), fill=(235, 230, 215))
    sheet.paste(fit(v['src']), (x, y + LB)); sheet.paste(fit(v['model']), (x + PW + M, y + LB))
    d.text((x, y + LB + PH + 3), 'AI concept image · fictional people', font=F(18), fill=(226, 196, 140))
    d.text((x + PW + M, y + LB + PH + 3), 'Rendered from the 3D model · no people', font=F(18), fill=(169, 216, 184))
out = Path(sys.argv[1]); sheet.save(out, quality=84, optimize=True); print(out, sheet.size, len(pairs), 'pairs')
