"""Annotated plan of the /bengal-earth-lab/ proposal: the viewer's own top view (CAM_TOP_Plan, captured with
bel_check.py --cams CAM_TOP_Plan --size 1240x1612) with room outlines and labels from office_web_metadata.json.
python3 -I plan_annotate.py TOP_VIEW.png OUT.jpg [SOURCE_COMMIT]"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

src, out = sys.argv[1], sys.argv[2]
source = sys.argv[3] if len(sys.argv) > 3 else 'local build'
meta = json.loads((Path(__file__).resolve().parents[2] / 'revised-model' / 'office_web_metadata.json').read_text())
cam = next(c for c in meta['cameras'] if c['name'] == 'CAM_TOP_Plan')
im = Image.open(src).convert('RGB'); W, H = im.size
k = H / cam['ortho_scale']                       # portrait frame: the ortho scale is the height
cx, cz = cam['position'][0], cam['position'][2]  # up = -z (model orientation; true north is not confirmed)
P = lambda x, z: ((x - cx) * k + W / 2, (z - cz) * k + H / 2)
polys = {r['zone']: r['polygon_xz'] for r in meta['rooms']}
GREEN, ORANGE, TEAL = (120, 200, 140), (240, 160, 70), (110, 190, 210)
groups = [(GREEN, ['Z01', 'Z02', 'Z03', 'Z30', 'Z08', 'Z18', 'Z12', 'Z21', 'Z20', 'Z09', 'Z04']), (TEAL, ['Z14']), (TEAL, ['Z15', 'Z16', 'Z17', 'Z22']), (ORANGE, ['Z07', 'Z06'])]
canvas = Image.new('RGB', (W + 520, H + 120), (22, 32, 27)); canvas.paste(im, (0, 120))
d = ImageDraw.Draw(canvas)
F = lambda s, b=False: ImageFont.truetype(f"/usr/share/fonts/truetype/crosextra/Carlito-{'Bold' if b else 'Regular'}.ttf", s)
for col, zones in groups:
    for z in zones:
        pts = [P(x, zz) for x, zz in polys[z]]; pts = [(x, y + 120) for x, y in pts]
        d.line(pts + [pts[0]], fill=col, width=4)
labels = [   # (text, x, z of the anchor, colour)
    ('1 Arrival gallery', 3.8, 3.2, GREEN), ('2 Reception, tea, rural instruments', 11.0, 3.0, GREEN), ('3 Earth & Sun passage', 10.0, -3.0, GREEN),
    ('4 Earth to product, Future of Bengal', 15.5, -8.2, GREEN), ('5 Negotiation suite', 17.0, -3.0, GREEN), ('6 Collaborative studio, sunning shelf', 31.0, -22.0, GREEN),
    ('7 Making line (design-wing entrance)', 24.3, -22.1, TEAL), ('8 Living materials library', 24.3, -9.0, TEAL), ('9 Materials lab', 24.3, -13.2, TEAL), ('10 Prototype workshop', 24.3, -18.2, TEAL),
    ('11 Academy annex (pilot academy)', 24.6, -35.6, GREEN), ('12 Staff and artisan dining', 25.15, -27.8, GREEN), ('13 Records room', 4.45, -20.0, GREEN),
    ('14 Lab B, digital product design', 24.3, -3.4, TEAL), ('15 Buyer project room, order desk', 0.3, -1.4, GREEN),
    ('A Green Uthan, artisan corner, room-sets', 15.6, -16.1, ORANGE), ('B Design academy (20 seats)', 5.0, -12.5, ORANGE),
]
x0 = W + 30; y = 150
def badge(px, py, tag, col):
    r = 17; d.ellipse([px - r, py - r, px + r, py + r], fill=col, outline=(20, 20, 20), width=3)
    d.text((px, py + 1), tag, font=F(22, True), fill=(20, 24, 22), anchor='mm')
for text, ax, az, col in labels:
    tag, name = text.split(' ', 1)
    px, py = P(ax, az); badge(px, py + 120, tag, col)
    badge(x0 + 17, y + 14, tag, col); d.text((x0 + 46, y), name, font=F(24, True), fill=col); y += 46
y += 20
for col, t in [(GREEN, 'Every option, including the pilot'), (TEAL, 'Design wing, every option'), (ORANGE, 'Option A only: if the merchandising and')]:
    d.rectangle([x0, y + 4, x0 + 26, y + 24], outline=col, width=4); d.text((x0 + 38, y), t, font=F(22), fill=(225, 230, 226)); y += 34
d.text((x0 + 38, y - 4), 'accounts teams move (owner decision)', font=F(22), fill=(225, 230, 226)); y += 44
for t in ['Oriented as the model; true north is not yet', 'confirmed. The viewer\'s own top view of the', 'proposal route; concept proposal, no people.', 'Walls, doors, windows and the approved floor', 'are unchanged. Not a measured survey.']:
    d.text((x0, y), t, font=F(20), fill=(190, 200, 194)); y += 28
d.text((24, 26), 'Bengal Earth Lab · /bengal-earth-lab/ proposal on the approved Stage II floor', font=F(36, True), fill=(241, 234, 220))
d.text((24, 74), f'Plan view from the 3D viewer, 30 Oct 2026 (source: {source})', font=F(24), fill=(200, 210, 204))
canvas.save(out, quality=88); print(out, canvas.size)
