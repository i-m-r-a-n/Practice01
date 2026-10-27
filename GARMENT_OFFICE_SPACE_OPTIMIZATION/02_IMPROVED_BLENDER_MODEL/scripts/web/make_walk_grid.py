"""Walk-mode floor map from the collision triangles written by export_web_metadata.py (system Python: numpy + Pillow).
python3 make_walk_grid.py collision_tris.npy blender_cameras.json blender_rooms.json door_openings.json OUT_DIR
A 0.10 m grid over the floor (glTF x / z). A cell is blocked when any render-visible object (walls, glazing, frames,
furniture, fixtures, stair; overhead objects and door leaves excluded) passes through it between 0.10 m and 1.90 m.
Door openings (the hidden boolean cutters of the "Doors" collection) are kept free: the aluminium frame rail on top of the
48 in walls runs across six doorways at 1.22 m in the model, which would otherwise close them.
The map is then grown by ~0.15 m (walker radius) so the eye point can be tested with one lookup.
Writes walk_grid.json (bit-packed, base64) and walk_grid.png (QC image: blocked dark, free light, cameras red).
"""
import base64
import json
import os
import sys
from collections import deque

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

tris_path, cams_path, rooms_path, doors_path, out = sys.argv[1:6]
os.makedirs(out, exist_ok=True)
RES, ZLO, ZHI, PAD = 0.10, 0.10, 1.90, 1.0
tris = np.load(tris_path).astype(np.float64)          # Blender world (x east, y north, z up)
cams = json.load(open(cams_path))
rooms = json.load(open(rooms_path))

# glTF floor coords: X = x, Z = -y
X = tris[:, :, 0]
Z = -tris[:, :, 1]
H = tris[:, :, 2]
x0, z0 = X.min() - PAD, Z.min() - PAD
nx, nz = int(np.ceil((X.max() + PAD - x0) / RES)), int(np.ceil((Z.max() + PAD - z0) / RES))
img = Image.new("L", (nx, nz), 0)
dr = ImageDraw.Draw(img)


def clip(poly, keep_above, h):
    """Sutherland-Hodgman against the plane height = h (poly: list of (x, z, height))."""
    res = []
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        ina = a[2] >= h if keep_above else a[2] <= h
        inb = b[2] >= h if keep_above else b[2] <= h
        if ina:
            res.append(a)
        if ina != inb:
            t = (h - a[2]) / (b[2] - a[2])
            res.append(tuple(a[k] + t * (b[k] - a[k]) for k in range(3)))
    return res


def px(p):
    return ((p[0] - x0) / RES, (p[1] - z0) / RES)


inside = (H.min(1) >= ZLO) & (H.max(1) <= ZHI)
for t in np.where(inside)[0]:
    pts = [px((X[t, k], Z[t, k])) for k in range(3)]
    dr.polygon(pts, fill=255, outline=255)
    dr.line(pts + [pts[0]], fill=255, width=1)
for t in np.where(~inside)[0]:
    poly = [(X[t, k], Z[t, k], H[t, k]) for k in range(3)]
    poly = clip(poly, True, ZLO)
    if len(poly) >= 2:
        poly = clip(poly, False, ZHI)
    if len(poly) < 2:
        continue
    pts = [px(p) for p in poly]
    if len(pts) >= 3:
        dr.polygon(pts, fill=255, outline=255)
    dr.line(pts + [pts[0]], fill=255, width=1)

for o in json.load(open(doors_path)):                          # keep every door opening passable
    if o["coll"] != "Doors" or "head cut" in o["name"]:
        continue
    (ax0, ax1), (az0, az1) = o["x"], o["z_south"]
    if ax1 - ax0 > az1 - az0:
        ax0, ax1 = ax0 + 0.04, ax1 - 0.04
    else:
        az0, az1 = az0 + 0.04, az1 - 0.04
    dr.rectangle([px((ax0, az0)), px((ax1, az1))], fill=0)
raw = np.array(img) > 0
grown = np.array(img.filter(ImageFilter.MaxFilter(3))) > 0       # +/- 1 cell: walker radius ~0.15 m


def cell(x, z):
    return int((z - z0) / RES), int((x - x0) / RES)            # row, col


# reachability on foot from the middle of the entrance lobby (Z01)
lobby = next(rm for rm in rooms if rm["zone"] == "Z01")["centroid_xz"]
seen = np.zeros_like(grown)
r0, c0 = cell(lobby[0], lobby[1])
fr, fc = np.nonzero(~grown)                                  # nearest free cell to the lobby centre
k = int(np.argmin((fr - r0) ** 2 + (fc - c0) ** 2))
r0, c0 = int(fr[k]), int(fc[k])
q = deque([(r0, c0)])
seen[r0, c0] = True
while q:
    r, c = q.popleft()
    for dr_, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        rr, cc = r + dr_, c + dc
        if 0 <= rr < nz and 0 <= cc < nx and not seen[rr, cc] and not grown[rr, cc]:
            seen[rr, cc] = True
            q.append((rr, cc))

report = []
for c in cams:
    if c["type"] != "PERSP":
        continue
    r, cc = cell(c["position"][0], c["position"][2])
    # a camera may stand close to a wall: accept the nearest free reachable cell within 0.5 m
    win = seen[max(0, r - 5):r + 6, max(0, cc - 5):cc + 6]
    report.append(dict(camera=c["name"], free=bool(not grown[r, cc]), reachable_within_0_5m=bool(win.any())))
room_rep = []
for rm in rooms:
    xs = [p[0] for p in rm["polygon_xz"]]
    zs = [p[1] for p in rm["polygon_xz"]]
    rr0, cc0 = cell(min(xs), min(zs))
    rr1, cc1 = cell(max(xs), max(zs))
    mask = Image.new("L", (nx, nz), 0)
    ImageDraw.Draw(mask).polygon([px(p) for p in rm["polygon_xz"]], fill=255)
    m = np.array(mask) > 0
    room_rep.append(dict(zone=rm["zone"], label=rm["label"], free_cells=int((m & ~grown).sum()),
                         reachable_cells=int((m & seen).sum()), reachable=bool((m & seen).any())))

bits = np.packbits(grown.astype(np.uint8), axis=None, bitorder="little")
grid = dict(note="Walk-mode floor map: 1 = blocked for the eye point (obstacle grown by the walker radius). Row-major, "
                 "row = z (south), column = x (east), bit i of the stream = cell i (little-endian bit order).",
            res=RES, origin_xz=[round(x0, 4), round(z0, 4)], cols=nx, rows=nz, slab_m=[ZLO, ZHI], walker_radius_m=0.15,
            blocked_bits_base64=base64.b64encode(bits.tobytes()).decode(),
            stats=dict(cells=int(nx * nz), blocked_raw=int(raw.sum()), blocked_grown=int(grown.sum()), reachable=int(seen.sum())),
            cameras=report, rooms=room_rep)
json.dump(grid, open(os.path.join(out, "walk_grid.json"), "w"))

vis = np.full((nz, nx, 3), 236, np.uint8)
vis[grown] = (150, 160, 152)
vis[raw] = (24, 40, 30)
vis[seen] = (205, 230, 212)
im = Image.fromarray(vis).resize((nx * 3, nz * 3), Image.NEAREST)
d = ImageDraw.Draw(im)
for rm in rooms:
    d.polygon([((p[0] - x0) / RES * 3, (p[1] - z0) / RES * 3) for p in rm["polygon_xz"]], outline=(184, 146, 74))
for c in cams:
    if c["type"] == "PERSP":
        x, z = (c["position"][0] - x0) / RES * 3, (c["position"][2] - z0) / RES * 3
        d.ellipse((x - 4, z - 4, x + 4, z + 4), fill=(200, 40, 40))
im.save(os.path.join(out, "walk_grid.png"))
bad = [r for r in report if not r["reachable_within_0_5m"]]
badr = [r["zone"] + " " + r["label"] for r in room_rep if not r["reachable"]]
print("WALK_GRID", nx, "x", nz, "blocked", grid["stats"], "cameras not reachable:", [b["camera"] for b in bad], "rooms not reachable:", badr)
