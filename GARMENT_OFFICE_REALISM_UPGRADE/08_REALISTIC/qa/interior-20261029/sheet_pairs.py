"""Before / after rows of actual local viewer frames (same camera per row, UI hidden).
python3 sheet_pairs.py OUT.jpg "Title" "before label" "after label" "row caption" BEFORE.png AFTER.png ["row caption" BEFORE AFTER ...]"""
import sys
from PIL import Image, ImageDraw, ImageFont
out, title, lb, la, *rest = sys.argv[1:]
rows = [rest[i:i + 3] for i in range(0, len(rest), 3)]
F = ImageFont.truetype('/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf', 26); f2 = ImageFont.truetype('/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf', 21)
def frame(f, w, h):                      # crop the letterbox bars of a reference-camera frame, then fit
    i = Image.open(f).convert('RGB'); g = i.convert('L'); ys = [y for y in range(i.height) if g.crop((0, y, i.width, y + 1)).getextrema()[1] > 30]
    return i.crop((0, ys[0], i.width, ys[-1] + 1)).resize((w, h))
W, H = 760, 428
s = Image.new('RGB', (20 + 2 * (W + 20), 110 + len(rows) * (H + 50) + 50), '#16201b'); d = ImageDraw.Draw(s)
d.text((20, 18), title, font=F, fill='#f1eadc'); d.text((20, 66), lb, font=F, fill='#c29a55'); d.text((40 + W, 66), la, font=F, fill='#a9d8b8')
for k, (cap, b, a) in enumerate(rows):
    y = 110 + k * (H + 50); d.text((20, y), cap, font=f2, fill='#d0d8d3')
    s.paste(frame(b, W, H), (20, y + 30)); s.paste(frame(a, W, H), (40 + W, y + 30))
d.text((20, s.height - 36), 'Actual local viewer frames (Chromium, software WebGL), UI hidden. Concept proposal; people are illustrative. Not a live-site or MacBook capture.', font=f2, fill='#d0d8d3')
s.save(out, quality=86); print(out, s.size)
