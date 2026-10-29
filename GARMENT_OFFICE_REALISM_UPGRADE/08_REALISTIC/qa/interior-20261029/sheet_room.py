"""Before / after sheet of actual local viewer frames for one room, same camera (UI hidden), plus optional detail frames.
python3 sheet_room.py OUT.jpg "Title" BEFORE.png AFTER.png "before label" "after label" [DETAIL.png "caption" ...]"""
import sys
from PIL import Image, ImageDraw, ImageFont
out, title, before, after, lb, la, *rest = sys.argv[1:]
F = ImageFont.truetype('/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf', 28); f2 = ImageFont.truetype('/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf', 21)
def frame(f, w, h):                      # crop the letterbox bars of a reference-camera frame, then fit
    i = Image.open(f).convert('RGB'); g = i.convert('L'); rows = [y for y in range(i.height) if g.crop((0, y, i.width, y + 1)).getextrema()[1] > 30]
    return i.crop((0, rows[0], i.width, rows[-1] + 1)).resize((w, h))
W, H = 960, 540; details = list(zip(rest[0::2], rest[1::2]))
dh0 = int(((2 * W + 20 - (len(details) - 1) * 20) // max(1, len(details))) * 9 / 16) if details else 0
rowsH = 112 + H + (30 + 30 + dh0 if details else 0) + 60
s = Image.new('RGB', (40 + 2 * W + 20, rowsH), '#16201b'); d = ImageDraw.Draw(s)
d.text((20, 20), title, font=F, fill='#f1eadc')
for k, (f, lab, col) in enumerate([(before, lb, '#c29a55'), (after, la, '#a9d8b8')]):
    x = 20 + k * (W + 20); d.text((x, 74), lab, font=F, fill=col); s.paste(frame(f, W, H), (x, 112))
if details:
    n = len(details); dw = (2 * W + 20 - (n - 1) * 20) // n; dh = int(dw * 9 / 16); y = 112 + H + 30
    for k, (f, cap) in enumerate(details):
        x = 20 + k * (dw + 20); d.text((x, y), cap, font=f2, fill='#a9d8b8'); s.paste(Image.open(f).convert('RGB').resize((dw, dh)), (x, y + 30))
    s = s.crop((0, 0, s.width, y + 30 + dh + 50)); d = ImageDraw.Draw(s)
d.text((20, s.height - 36), 'Actual local viewer frames (Chromium, software WebGL), UI hidden. Concept proposal; people are illustrative. Not a live-site or MacBook capture.', font=f2, fill='#d0d8d3')
s.save(out, quality=88); print(out, s.size)
