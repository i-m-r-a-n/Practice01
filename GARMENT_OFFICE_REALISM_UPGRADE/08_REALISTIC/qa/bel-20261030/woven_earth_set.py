"""The Woven Earth set (the owner's entrance brief, 7 Nov 2026) in concept-images/woven-earth/, from the Cycles renders of this 3D model:
- 01_arrival_before_after.jpg: the arrival camera CAM_03 before the brief (the proposal of 1 Nov 2026, concept-images/model/) and after it,
  same camera and the same Cycles light, side by side and labelled. Nothing is retouched: both images are only scaled.
- thumbs/: 640 px copies of the set's own images for the light images page.
Run after the renders are in concept-images/ and before woven_earth_board.py:  python3 -I woven_earth_set.py"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

R = Path(__file__).resolve().parents[2]
C = R / 'concept-images'; W = C / 'woven-earth'; T = W / 'thumbs'; T.mkdir(parents=True, exist_ok=True)
F = lambda s, b=False: ImageFont.truetype(f"/usr/share/fonts/truetype/crosextra/Carlito-{'Bold' if b else 'Regular'}.ttf", s)

before, after = Image.open(C / 'model' / 'render_CAM_03_Entrance_Lobby.jpg').convert('RGB'), Image.open(C / 'render_CAM_03_Entrance_Lobby.jpg').convert('RGB')
PW = 1200; PH = round(PW * 9 / 16); M = 24; TOP = 96; LB = 92
sheet = Image.new('RGB', (2 * PW + 3 * M, TOP + PH + LB + M), (20, 26, 22)); d = ImageDraw.Draw(sheet)
d.text((M, 22), 'STAGE II · Zara Fashion · the arrival camera, before and after the Woven Earth brief', font=F(40, True), fill=(240, 235, 222))
for k, (im, head, sub, col) in enumerate([
        (before, 'Before · the proposal of 1 Nov 2026', 'Bonsai on granite, three stones, six plaques, terracotta on the desk', (226, 196, 140)),
        (after, 'After · Woven Earth, 7 Nov 2026', 'An open arrival under the Woven Threshold; check-in at a terracotta counter under the stair', (169, 216, 184))]):
    x = M + k * (PW + M); sheet.paste(im.resize((PW, PH), Image.LANCZOS), (x, TOP))
    d.text((x, TOP + PH + 8), head, font=F(30, True), fill=col); d.text((x, TOP + PH + 46), sub, font=F(24), fill=(214, 222, 216))
d.text((M, TOP - 34), 'Both rendered from the 3D model with the same camera and the same Cycles light (simulated, no people); not photographs.', font=F(24), fill=(190, 200, 194))
out = W / '01_arrival_before_after.jpg'; sheet.save(out, quality=88, optimize=True, progressive=True); print(out, sheet.size)

made = 0
for f in sorted(W.glob('*.jpg')):
    t = T / f.name
    if t.exists() and t.stat().st_mtime >= f.stat().st_mtime: continue
    im = Image.open(f).convert('RGB'); im.resize((640, round(640 * im.height / im.width)), Image.LANCZOS).save(t, quality=80, optimize=True, progressive=True); made += 1
for t in sorted(T.glob('*.jpg')):
    if not (W / t.name).exists(): t.unlink()
print(T, made, 'thumbs made')
