"""Two more sheets of actual local viewer frames: phone toolbar before / after, and the new identity details (after only)."""
import sys
from PIL import Image, ImageDraw, ImageFont
Q = '/home/user/rs/GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/qa/sprint-claude-20261028/'
out = sys.argv[1]
F = ImageFont.truetype('/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf', 24)
f2 = ImageFont.truetype('/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf', 19)
BG, INK, OLD, NEW, NOTE = '#16201b', '#f1eadc', '#c29a55', '#a9d8b8', '#d0d8d3'

# 1. phone header: before (baseline = live source + GPT drag fix) | after (this build), 390 and 360 px wide
phones = [('390 px: before', Q + 'baseline/390_interactive_reception.png', OLD), ('390 px: after', Q + 'r2/390_interactive_reception.png', NEW),
          ('360 px: before', Q + 'baseline/360_interactive_reception.png', OLD), ('360 px: after', Q + 'r2/360_interactive_reception.png', NEW)]
ims = [Image.open(f).convert('RGB') for _, f, _ in phones]
H = max(i.height for i in ims)
s = Image.new('RGB', (20 + sum(i.width + 20 for i in ims), 70 + 40 + H + 50), BG); d = ImageDraw.Draw(s)
d.text((20, 18), 'Phone toolbar: actual local viewer frames (Chromium, software WebGL)', font=F, fill=INK)
x = 20
for (label, _, col), im in zip(phones, ims):
    d.text((x, 74), label, font=F, fill=col); s.paste(im, (x, 110)); x += im.width + 20
d.text((20, s.height - 34), 'Before: Help and Full screen are cut off at the right edge and People is hard to read. After: two rows, everything visible.', font=f2, fill=NOTE)
s.save(out + '_phone.jpg', quality=88)

# 2. new client-identity details, visitor eye height (after only: these objects did not exist before)
det = [('Water & Wellbeing point (results: pending)', Q + 'r2/visitor/visitor_water_point.png'),
       ('Boardroom: fabric review trays', Q + 'r2/visitor/visitor_board_review.png'),
       ('Jamdani-inspired panel (design reference)', Q + 'r2/visitor/visitor_jamdani_panel.png'),
       ('MD office: development samples', Q + 'r2/visitor/visitor_md_development.png')]
W, Hh = 780, 439
s = Image.new('RGB', (20 + 2 * (W + 20), 70 + 2 * (Hh + 50) + 40), BG); d = ImageDraw.Draw(s)
d.text((20, 18), 'New in this build: actual local viewer frames at visitor eye height (Chromium, software WebGL)', font=F, fill=INK)
for k, (label, f) in enumerate(det):
    x, y = 20 + (k % 2) * (W + 20), 70 + (k // 2) * (Hh + 50)
    d.text((x, y + 4), label, font=F, fill=NEW)
    s.paste(Image.open(f).convert('RGB').resize((W, Hh)), (x, y + 38))
d.text((20, s.height - 34), 'Concept proposal. Every water, supplier and solar value reads "pending" until real data exists. Not a live-site or MacBook capture.', font=f2, fill=NOTE)
s.save(out + '_details.jpg', quality=88)
print(out + '_phone.jpg', out + '_details.jpg')
