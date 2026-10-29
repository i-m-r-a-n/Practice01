"""A captioned slideshow and a contact sheet of the /bengal-earth-lab/ guided tour, made from the viewer's own tour frames
(after-tour18/, captured with bel_check.py) and the tour titles in viewer/bel-config.json. For people who cannot open the
3D route yet (it is not deployed). Nothing is rendered or retouched here: frames are cropped, scaled and captioned.
python3 -I tour_slideshow.py OUT_DIR"""
import json, subprocess, sys, tempfile, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
cfg = json.loads((HERE.parents[1] / 'viewer' / 'bel-config.json').read_text())
tour = cfg['tour']
F = lambda s, b=False: ImageFont.truetype(f"/usr/share/fonts/truetype/crosextra/Carlito-{'Bold' if b else 'Regular'}.ttf", s)


def frame(cam, w, h):   # crop the letterbox bars of a reference-camera frame, centre-crop to w:h, scale
    i = Image.open(HERE / 'after-tour18' / f'1440_{cam}.jpg').convert('RGB'); g = i.convert('L')
    ys = [y for y in range(i.height) if g.crop((0, y, i.width, y + 1)).getextrema()[1] > 30]
    i = i.crop((0, ys[0], i.width, ys[-1] + 1))
    if i.width / i.height > w / h: cw = round(i.height * w / h); i = i.crop(((i.width - cw) // 2, 0, (i.width - cw) // 2 + cw, i.height))
    else: ch = round(i.width * h / w); i = i.crop((0, (i.height - ch) // 2, i.width, (i.height - ch) // 2 + ch))
    return i.resize((w, h), Image.LANCZOS)


W, H, BAND = 1280, 720, 150
slides = []
with tempfile.TemporaryDirectory() as tmp:
    for k, st in enumerate(tour, 1):
        im = Image.new('RGB', (W, H), (22, 32, 27)); im.paste(frame(st['camera'], W, H - BAND), (0, 0)); d = ImageDraw.Draw(im)
        option_a = st['title'].startswith('Option A')
        d.text((28, H - BAND + 16), f"{k}/{len(tour)}  {st['title']}", font=F(34, True), fill=(240, 160, 70) if option_a else (241, 234, 220))
        for j, line in enumerate(textwrap.wrap(st['description'], 118)[:2]):
            d.text((28, H - BAND + 62 + j * 28), line, font=F(23), fill=(214, 222, 217))
        d.text((W - 28, H - 14), 'Bengal Earth Lab · concept proposal · local 3D viewer frames · not deployed · no people shown', font=F(17), fill=(160, 172, 166), anchor='rb')
        p = Path(tmp) / f'{k:02d}.png'; im.save(p); slides.append(p)
    # contact sheet: 3 x 6 thumbnails with their numbers and titles
    tw, th = 420, 236; sheet = Image.new('RGB', (3 * tw + 4 * 16, 6 * (th + 46) + 110), (22, 32, 27)); sd = ImageDraw.Draw(sheet)
    sd.text((16, 22), 'Bengal Earth Lab · the guided tour of /bengal-earth-lab/ (18 stops)', font=F(34, True), fill=(241, 234, 220))
    sd.text((16, 66), 'Local 3D viewer frames, concept proposal, not deployed. Orange titles: option A only (the teams would move first).', font=F(20), fill=(200, 210, 204))
    for k, st in enumerate(tour):
        x, y = 16 + (k % 3) * (tw + 16), 110 + (k // 3) * (th + 46)
        sheet.paste(frame(st['camera'], tw, th), (x, y))
        sd.text((x, y + th + 6), f"{k + 1}. {st['title']}"[:52], font=F(21, True), fill=(240, 160, 70) if st['title'].startswith('Option A') else (230, 236, 232))
    sheet.save(out / 'BEL_tour_contact_sheet.jpg', quality=88)
    # slideshow: 4.5 s per stop, 0.6 s cross-fades, H.264
    L, D = 4.5, .6
    args = ['ffmpeg', '-y', '-loglevel', 'error']
    for p in slides: args += ['-loop', '1', '-t', str(L), '-i', str(p)]
    chain, last = [], '[0]'
    for i in range(1, len(slides)):
        chain.append(f"{last}[{i}]xfade=transition=fade:duration={D}:offset={i * (L - D):.2f}[v{i}]"); last = f'[v{i}]'
    args += ['-filter_complex', ';'.join(chain), '-map', last, '-r', '30', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '24', '-movflags', '+faststart', str(out / 'BEL_tour_slideshow.mp4')]
    subprocess.run(args, check=True)
print(out / 'BEL_tour_slideshow.mp4', (out / 'BEL_tour_slideshow.mp4').stat().st_size, out / 'BEL_tour_contact_sheet.jpg')
