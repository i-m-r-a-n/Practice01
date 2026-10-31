"""Contact sheet of the stop images (AI concept images and renders from the 3D), in tour order, labelled by kind."""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
R = Path('/home/user/bel/GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC')
F = lambda s, b=False: ImageFont.truetype(f"/usr/share/fonts/truetype/crosextra/Carlito-{'Bold' if b else 'Regular'}.ttf", s)
cfg = json.loads((R / 'viewer/bel-config.json').read_text()); stills = cfg['conceptStills']; tour = cfg['tour']
items = [(t['stop'], t['title'], t['camera']) for t in tour if t['camera'] in stills]
PW, PH, LB, M, COLS = 640, 360, 44, 16, 3
rows = (len(items) + COLS - 1) // COLS
sheet = Image.new('RGB', (M + COLS * (PW + M), 70 + rows * (LB + PH + M) + M), (20, 26, 22)); d = ImageDraw.Draw(sheet)
d.text((M, 18), f'STAGE II · Zara Fashion · images at the tour stops ({len(items)} of {len(tour)})  ·  gold = AI concept image (fictional people)  ·  green = rendered from the 3D', font=F(26, True), fill=(235, 230, 215))
for k, (stop, title, cam) in enumerate(items):
    v = stills[cam]; kind = v['kind'] if isinstance(v, dict) else 'ai'; src = v['src'] if isinstance(v, dict) else v
    x, y = M + (k % COLS) * (PW + M), 70 + (k // COLS) * (LB + PH + M)
    im = Image.open(R / src).convert('RGB'); im = im.resize((PW, round(PW * im.height / im.width)))
    if im.height > PH: top = (im.height - PH) // 2; im = im.crop((0, top, PW, top + PH))
    sheet.paste(im, (x, y + LB))
    d.text((x, y + 8), f'{stop:02d} · {title[:40]}', font=F(24, True), fill=(225, 190, 120) if kind == 'ai' else (130, 210, 160))
out = Path(sys.argv[1]); sheet.save(out, quality=84, optimize=True); print(out, sheet.size)
