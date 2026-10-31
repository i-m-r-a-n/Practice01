"""640 px copies of the stop images for the tour in images (the grid behind the "Images" button of the proposal route).
A phone loads about 40 KB per card instead of the full image; the full image still shows at the stop.
Run it before make_bel_config.py whenever concept-images/ changes:  python3 -I make_concept_thumbs.py"""
from pathlib import Path
from PIL import Image

SRC = Path(__file__).resolve().parent.parent / 'concept-images'
OUT = SRC / 'thumbs'
OUT.mkdir(exist_ok=True)
made = 0
for f in sorted(SRC.glob('*.jpg')):
    t = OUT / f.name
    if t.exists() and t.stat().st_mtime >= f.stat().st_mtime:
        continue
    im = Image.open(f).convert('RGB')
    w = 640
    im = im.resize((w, round(w * im.height / im.width)), Image.LANCZOS)
    im.save(t, quality=80, optimize=True, progressive=True)
    made += 1
for t in sorted(OUT.glob('*.jpg')):           # a thumbnail whose image was removed goes too
    if not (SRC / t.name).exists():
        t.unlink()
print(OUT, made, 'made,', len(list(OUT.glob('*.jpg'))), 'in all')
