"""Before / after sheet of actual local viewer frames: before = GPT local baseline (live source bcb92b0 + drag fix), after = this sprint build."""
import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
Q = '/home/user/rs/GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/qa/'
pairs = [('Reception', Q + 'sprint-20261028/local-baseline/1440_CAM_01_Reception_A_room.png', Q + 'sprint-claude-20261028/r2/cams/1440_CAM_01_Reception_A.png'),
         ('Experience Centre', Q + 'sprint-20261028/local-baseline/1440_CAM_04_Experience_Centre_A_room.png', Q + 'sprint-claude-20261028/r2/cams/1440_CAM_04_Experience_Centre_A.png')]
def crop(f):
    i = Image.open(f).convert('RGB'); a = np.asarray(i).sum(axis=2); rows = np.where(a.max(axis=1) > 30)[0]
    return i.crop((0, rows[0], i.width, rows[-1] + 1)).resize((800, 450))
F = ImageFont.truetype('/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf', 26); f2 = ImageFont.truetype('/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf', 20)
s = Image.new('RGB', (1640, 70 + len(pairs) * 500 + 40), '#16201b'); d = ImageDraw.Draw(s)
d.text((20, 20), 'STAGE II /realistic/ sprint: actual local viewer frames (Chromium, software WebGL) — before (live source) | after (this build)', font=F, fill='#f1eadc')
for k, (name, b, a) in enumerate(pairs):
    y = 70 + k * 500
    s.paste(crop(b), (20, y + 36)); s.paste(crop(a), (820 + 0, y + 36))
    d.text((20, y + 4), f'{name}: before', font=F, fill='#c29a55'); d.text((820, y + 4), f'{name}: after', font=F, fill='#a9d8b8')
d.text((20, s.height - 34), 'Concept proposal. People shown are illustrative. Not a live-site or MacBook capture.', font=f2, fill='#d0d8d3')
s.save(sys.argv[1], quality=88)
print(sys.argv[1])
