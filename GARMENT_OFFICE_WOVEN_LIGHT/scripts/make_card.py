"""Draws the placeholder "Water record" card shown at the Water & Wellbeing point.

Every value the client has not supplied stays a visible placeholder; nothing is invented.
Usage: python3 make_card.py OUT.png
"""
import sys
from PIL import Image, ImageDraw, ImageFont

C = '/usr/share/fonts/truetype/crosextra/'
W, H = 600, 840
img = Image.new('RGB', (W, H), (244, 240, 232))
d = ImageDraw.Draw(img)
bold = ImageFont.truetype(C + 'Carlito-Bold.ttf', 46)
sub = ImageFont.truetype(C + 'Carlito-Regular.ttf', 22)
lab = ImageFont.truetype(C + 'Carlito-Bold.ttf', 22)
txt = ImageFont.truetype(C + 'Carlito-Regular.ttf', 21)
ink, quiet, green = (40, 44, 40), (110, 112, 104), (38, 103, 61)

d.text((48, 54), 'Our water', font=bold, fill=ink)
d.rectangle((48, 116, 118, 120), fill=green)
d.multiline_text((48, 140), 'We know our water source, test it\nappropriately and maintain the system.', font=sub, fill=ink, spacing=6)
rows = [
    ('Source', 'Deep tube well (client-stated)\nDepth: [PLACEHOLDER]'),
    ('Treatment', '[PLACEHOLDER: confirmed after testing]'),
    ('S1 Source', 'Date / lab / standard: [PLACEHOLDER]'),
    ('S2 After treatment', 'Date / lab / standard: [PLACEHOLDER]'),
    ('S3 This outlet', 'Date / lab / standard: [PLACEHOLDER]'),
    ('Maintenance', 'Tank cleaned: [PLACEHOLDER]\nNext sampling: [PLACEHOLDER]'),
]
y = 236
for k, v in rows:
    d.line((48, y - 14, W - 48, y - 14), fill=(210, 204, 192), width=2)
    d.text((48, y), k, font=lab, fill=ink)
    d.multiline_text((48, y + 30), v, font=txt, fill=quiet, spacing=5)
    y += 30 + 30 * (v.count('\n') + 1) + 22
d.rectangle((W - 48 - 120, H - 48 - 120, W - 48, H - 48), outline=quiet, width=2)
d.multiline_text((W - 48 - 108, H - 48 - 84), 'QR when\nreports\nare online', font=txt, fill=quiet, spacing=4)
d.multiline_text((48, H - 140), 'Groundwater use is a separate\nquestion. Permit: [PLACEHOLDER]', font=txt, fill=quiet, spacing=5)
img.save(sys.argv[1])
