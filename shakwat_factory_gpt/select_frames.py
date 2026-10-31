#!/usr/bin/env python3
"""Drop near-blank frames (plain wall close-ups) from a capture folder; keeps at least 5 per room.
Usage: python3 select_frames.py SHOTS_DIR  -> writes SHOTS_DIR/selected/ with the kept JPEGs."""
import json, os, re, shutil, sys
from PIL import Image, ImageStat

def detail(p):
    return ImageStat.Stat(Image.open(p).convert('L').resize((64, 36))).stddev[0]

src = sys.argv[1]
dst = os.path.join(src, 'selected'); os.makedirs(dst, exist_ok=True)
by_room = {}
for f in sorted(os.listdir(src)):
    m = re.match(r'^(\d\d)_(Z\d\d)_.+\.jpg$', f)
    if m: by_room.setdefault(m.group(2), []).append(f)
kept = 0
for z, files in by_room.items():
    scored = [(f, detail(os.path.join(src, f))) for f in files]
    keep = [f for f, s in scored if s >= 15 or '_00_room_view' in f]
    if len(keep) < 5:
        keep += [f for f, s in sorted(scored, key=lambda x: -x[1]) if f not in keep][:5 - len(keep)]
    for f in keep: shutil.copy(os.path.join(src, f), os.path.join(dst, f)); kept += 1
print('kept', kept, 'frames in', dst)
