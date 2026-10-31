"""A short film of the guided tour in images: every stop's image (the owner's AI concept images and the Cycles renders of the 3D),
in tour order, each with its stop number, title and kind label burned in, between an opening and a closing card.
Nothing is retouched: each image is fitted to 16:9, slowly zoomed, and captioned. The kind label stays on screen for the whole shot.
python3 -I stop_images_film.py OUT.mp4 [--seconds 4.2] [--size 1920x1080]"""
import argparse, json, subprocess, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

p = argparse.ArgumentParser()
p.add_argument('out'); p.add_argument('--seconds', type=float, default=4.2); p.add_argument('--size', default='1920x1080'); p.add_argument('--fps', type=int, default=30)
a = p.parse_args()
W, H = map(int, a.size.split('x')); FPS = a.fps; S = W / 1920
ROOT = Path(__file__).resolve().parents[2]
cfg = json.loads((ROOT / 'viewer' / 'bel-config.json').read_text())
tour, stills = cfg['tour'], cfg['conceptStills']
F = lambda s, b=False: ImageFont.truetype(f"/usr/share/fonts/truetype/crosextra/Carlito-{'Bold' if b else 'Regular'}.ttf", round(s * S))
INK, MINT, GOLD, GREEN_BG = (246, 243, 238), (169, 216, 184), (226, 196, 140), (20, 33, 26)
KIND = {'ai': ('AI CONCEPT IMAGE  ·  made from the 3D views  ·  people are fictional  ·  not a photograph', GOLD),
        'render': ('RENDERED FROM THE 3D MODEL  ·  Blender Cycles, simulated light  ·  no people  ·  not a photograph', MINT)}
LINK = 'stage2-office-virtual-tour.imranahmedjh611.workers.dev/stage2-concept/'


def cover(im, w, h):   # fit to w:h by centre-cropping, no stretching
    r = max(w / im.width, h / im.height); im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def shade(img, box, alpha):   # a dark band behind the captions
    o = Image.new('RGBA', img.size, (0, 0, 0, 0)); ImageDraw.Draw(o).rectangle(box, fill=(8, 12, 10, alpha))
    return Image.alpha_composite(img.convert('RGBA'), o).convert('RGB')


def card(lines):   # an opening or closing card: brand green, centred lines (text, size, bold, colour)
    im = Image.new('RGB', (W, H), GREEN_BG); d = ImageDraw.Draw(im)
    total = sum(round(s * S * 1.45) for _, s, _, _ in lines); y = (H - total) // 2
    for text, size, bold, col in lines:
        f = F(size, bold); w = d.textlength(text, font=f); d.text(((W - w) / 2, y), text, font=f, fill=col); y += round(size * S * 1.45)
    return im


shots = []   # (base image at 1.06x of the frame for the zoom, caption overlay function)
for i, st in enumerate(tour):
    v = stills.get(st['camera'])
    if not v: continue
    src, kind = (v, 'ai') if isinstance(v, str) else (v['src'], v.get('kind', 'ai'))
    base = cover(Image.open(ROOT / src).convert('RGB'), round(W * 1.06), round(H * 1.06))
    shots.append((base, i + 1, st['title'], kind))
print(len(shots), 'of', len(tour), 'stops have an image', flush=True)


def caption(frame, stop, title, kind):
    frame = shade(frame, (0, H - round(150 * S), W, H), 150); frame = shade(frame, (0, 0, W, round(56 * S)), 120)
    d = ImageDraw.Draw(frame)
    d.text((round(60 * S), H - round(128 * S)), f'STOP {stop} OF {len(tour)}', font=F(26, True), fill=MINT)
    d.text((round(60 * S), H - round(94 * S)), title, font=F(52, True), fill=INK)
    label, col = KIND[kind]; f = F(22, True); w = d.textlength(label, font=f)
    d.text(((W - w) / 2, round(16 * S)), label, font=f, fill=col)
    brand = 'STAGE II · Zara Fashion  ·  concept proposal'; f2 = F(22); w2 = d.textlength(brand, font=f2)
    d.text((W - w2 - round(60 * S), H - round(46 * S)), brand, font=f2, fill=(200, 210, 204))
    return frame


opening = card([('STAGE II  ·  Zara Fashion', 40, True, MINT), ('The ground floor, reimagined', 76, True, INK), ('A concept proposal: the guided tour in images', 40, False, INK),
                (f'{len(shots)} stops  ·  gold label: AI concept image (fictional people)  ·  green label: rendered from the 3D model', 28, False, GOLD)])
note = textwrap.wrap('Concept proposal on the approved Stage II floor. The AI concept images show fictional people and can differ from the 3D; the renders are made '
                     'from the 3D model with simulated light. None of the images is a photograph. Fibre origins, recycled shares, tests, makers, artists, growers, '
                     'stone sources and energy data are still to be identified.', 92)
closing = card([('Walk through it in 3D, on a computer or a phone', 52, True, INK), (LINK, 36, True, MINT), ('', 20, False, INK)] + [(t, 28, False, (214, 223, 217)) for t in note])

cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '22', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-threads', '4', a.out]
ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
put = lambda im: ff.stdin.write(im.tobytes())
fade = round(0.6 * FPS)


def frames_of(k):   # the frames of shot k: a slow zoom from 1.06x to 1.0x of the frame, centred, with captions
    base, stop, title, kind = shots[k]; n = round(a.seconds * FPS)
    for j in range(n):
        z = 1.06 - 0.06 * j / max(1, n - 1); w, h = round(W * z), round(H * z)
        x, y = (base.width - w) // 2, (base.height - h) // 2
        yield caption(base.crop((x, y, x + w, y + h)).resize((W, H), Image.BILINEAR), stop, title, kind)


def hold(im, sec):
    for _ in range(round(sec * FPS)): put(im)


hold(opening, 3.5)
prev = opening
for k in range(len(shots)):
    it = frames_of(k)
    first = next(it)
    for j in range(fade): put(Image.blend(prev, first, (j + 1) / (fade + 1)))   # cross-fade from the last frame of the previous shot
    put(first)
    for fr in it: prev = fr; put(fr)
for j in range(fade): put(Image.blend(prev, closing, (j + 1) / (fade + 1)))
hold(closing, 6)
ff.stdin.close(); ff.wait()
dur = 3.5 + len(shots) * (a.seconds + 0.6) + 0.6 + 6
print(json.dumps({'out': a.out, 'shots': len(shots), 'seconds': round(dur, 1), 'bytes': Path(a.out).stat().st_size, 'ffmpeg': ff.returncode}))
