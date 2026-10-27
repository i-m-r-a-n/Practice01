"""Space audit of Z06 Commercial & Accounts and Z07 Merchandising for the original layout and options A / B / C.

python3 analyze_space.py OUT_DIR   ->  metrics.json, metrics.md, plan_<option>.svg (scaled 1 in = 1 SVG unit)

Method (all from the project's own source data, no new site measurements):
  * room polygons, columns, doors, AC units: survey.py + office_layout.py (02_IMPROVED_BLENDER_MODEL/scripts)
  * furniture footprints: the asset table (real sizes) and the placements of each option (z06_z07_options.py)
  * 1 in raster: floor = zone polygon minus columns and new partitions; obstacles = every floor-standing item
    (wall-mounted screens / boards above 30 in are ignored), chairs at their working position
  * clear width at a point = 2 x chessboard distance to the nearest obstacle - 1 (in); a route's clear width is the
    widest-path bottleneck between its two end points (Dijkstra on the clearance map)
  * seat access: chairs removed (tucked in), every seat position must connect to the room entrance
Planning check only: 36 in (915 mm) for secondary routes and seat access, 48 in (1220 mm) for the main routes.
These are design targets, not a statement of code compliance; egress, accessibility and fire review by the
project architect / engineer is still required.
"""
import heapq
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "02_IMPROVED_BLENDER_MODEL", "scripts")
sys.path.insert(0, SCRIPTS)
os.environ["OFFICE_LAYOUT_ORIGINAL"] = "1"            # office_layout.py: keep the original Z06 / Z07 data for reference
import office_layout as O  # noqa: E402
import survey as SV  # noqa: E402
import z06_z07_options as ZO  # noqa: E402

OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else HERE
os.makedirs(OUT, exist_ok=True)
SFT = 144.0
X0, X1, Y0, Y1 = 30, 880, -905, -220                  # raster window (plan inches)
W_, H_ = X1 - X0, Y1 - Y0

ZPOLY = {z[1]: z[3] for z in O.ZONES}
ZLABEL = {z[1]: z[2].split("\n")[0] for z in O.ZONES}
ASSETS = dict(O.ASSETS)
ASSETS.update(ZO.NEW_ASSETS)
FP_EXTRA = {"dress_form": (16, 16)}

# entrances / doors used by the route checks (point just inside the zone) and keep-clear boxes in front of doors
POINTS = {
    "Z07": {"D11 hallway opening": (809, -826), "D49 to experience centre": (839, -440)},
    "Z06": {"Staff corridor (south)": (135, -240), "D09 male washroom": (54, -417), "D08 female washroom": (54, -621),
            "D22 female prayer": (54, -788), "D31 audit room": (170, -735), "Hallway (north-east)": (352, -868)},
}
ROUTES = {
    "Z07": [("D11 hallway opening", "D49 to experience centre", 48)],
    "Z06": [("Staff corridor (south)", "D09 male washroom", 48), ("Staff corridor (south)", "D08 female washroom", 48),
            ("Staff corridor (south)", "D22 female prayer", 48), ("Staff corridor (south)", "D31 audit room", 36),
            ("Hallway (north-east)", "D08 female washroom", 48), ("Hallway (north-east)", "Staff corridor (south)", 48)],
}
ENTRY = {"Z07": "D11 hallway opening", "Z06": "Staff corridor (south)"}
KEEP_CLEAR = {   # (label, x0, y0, x1, y1): door swings into the zone and approach space at doors in the zone walls
    "Z07": [("D49 door swing", 818, -470, 860, -428), ("D11 approach", 783, -838, 835, -802)],
    "Z06": [("D09 approach", 46, -432, 82, -402), ("D08 approach", 46, -636, 82, -606), ("D22 approach", 46, -806, 82, -770),
            ("D31 approach", 152, -740, 188, -704), ("Staff corridor arrival", 110, -260, 160, -231)],
}


def footprint(key, x, y, facing):
    if key in FP_EXTRA:
        w, d = FP_EXTRA[key]
    else:
        w, d = ASSETS[key][2]
    if int(round(facing)) % 180 == 90:
        w, d = d, w
    return x - w / 2, y - d / 2, x + w / 2, y + d / 2


def is_floor_item(key, z):
    return ZO.group_of(key) != "wall"         # wall-mounted screens, boards, mirror, extinguisher do not take floor


def poly_mask(pts):
    xs = np.arange(X0, X1) + 0.5
    ys = np.arange(Y0, Y1) + 0.5
    X, Y = np.meshgrid(xs, ys)
    inside = np.zeros(X.shape, bool)
    n = len(pts)
    for i in range(n):
        (xa, ya), (xb, yb) = pts[i], pts[(i + 1) % n]
        cond = ((ya > Y) != (yb > Y))
        with np.errstate(divide="ignore", invalid="ignore"):
            xint = (xb - xa) * (Y - ya) / (yb - ya) + xa
        inside ^= cond & (X < xint)
    return inside


def rect_slice(x0, y0, x1, y1):
    i0, i1 = int(math.floor(y0 - Y0)), int(math.ceil(y1 - Y0))
    j0, j1 = int(math.floor(x0 - X0)), int(math.ceil(x1 - X0))
    return slice(max(i0, 0), max(min(i1, H_), 0)), slice(max(j0, 0), max(min(j1, W_), 0))


def chessboard(free):
    """Chessboard distance (in) from each free cell to the nearest blocked cell (iterative dilation)."""
    d = np.zeros(free.shape, np.int32)
    cur = ~free
    k = 0
    while True:
        k += 1
        nxt = cur.copy()
        nxt[1:, :] |= cur[:-1, :]
        nxt[:-1, :] |= cur[1:, :]
        nxt[:, 1:] |= cur[:, :-1]
        nxt[:, :-1] |= cur[:, 1:]
        nxt[1:, 1:] |= cur[:-1, :-1]
        nxt[1:, :-1] |= cur[:-1, 1:]
        nxt[:-1, 1:] |= cur[1:, :-1]
        nxt[:-1, :-1] |= cur[1:, 1:]
        new = nxt & ~cur
        if not new.any() or k > 80:
            d[~nxt] = k
            break
        d[new] = k
        cur = nxt
    return d


def widest(clear, src):
    """Bottleneck (max-min clearance) from src to every cell; 4-neighbour Dijkstra."""
    H, W = clear.shape
    best = np.full(clear.shape, -1, np.int32)
    i, j = src
    best[i, j] = clear[i, j]
    hp = [(-int(clear[i, j]), i, j)]
    flat_clear = clear
    while hp:
        nb, i, j = heapq.heappop(hp)
        b = -nb
        if b < best[i, j]:
            continue
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a, c = i + di, j + dj
            if 0 <= a < H and 0 <= c < W:
                v = flat_clear[a, c]
                if v <= 0:
                    continue
                nbv = b if b < v else v
                if nbv > best[a, c]:
                    best[a, c] = nbv
                    heapq.heappush(hp, (-int(nbv), a, c))
    return best


def relieve(clear, pts, r):
    """Copy of the clearance map with the cells around the end points set to 'wide' (doors / desks there are the
    destination, not a pinch point of the route)."""
    c = clear.copy()
    for pt in pts:
        i, j = cell(pt)
        c[max(i - r, 0):i + r + 1, max(j - r, 0):j + r + 1] = np.maximum(c[max(i - r, 0):i + r + 1, max(j - r, 0):j + r + 1], 99)
    return c


def cell(pt):
    return int(pt[1] - Y0), int(pt[0] - X0)


def width_of(d):
    return max(0, 2 * int(d) - 1)


def analyse(layout):
    res = {"name": layout.name, "zones": {}}
    cols = [(x - SV.COL_W / 2, y - SV.COL_W / 2, x + SV.COL_W / 2, y + SV.COL_W / 2) for x, y in SV.COLUMNS]
    for zid in ("Z07", "Z06"):
        zmask = poly_mask(ZPOLY[zid])
        gross = zmask.sum() / SFT
        colm = np.zeros_like(zmask)
        for r in cols:
            colm[rect_slice(*r)] = True
        colm &= zmask
        wallm = np.zeros_like(zmask)
        for w in layout.walls:
            if w["axis"] == "h":
                wallm[rect_slice(min(w["a"], w["b"]), w["c0"], max(w["a"], w["b"]), w["c1"])] = True
            else:
                wallm[rect_slice(w["c0"], min(w["a"], w["b"]), w["c1"], max(w["a"], w["b"]))] = True
            for op in w["ops"]:              # door openings are walkable
                if w["axis"] == "h":
                    wallm[rect_slice(op[2], w["c0"], op[3], w["c1"])] = False
                else:
                    wallm[rect_slice(w["c0"], op[2], w["c1"], op[3])] = False
        wallm &= zmask
        floor = zmask & ~colm & ~wallm
        items = [it for it in layout.items if it[4] == zid]
        by_group = {}
        occ = np.zeros_like(zmask)
        occ_nochair = np.zeros_like(zmask)
        rects = []
        for key, x, y, f, z, zz, lab in items:
            if not is_floor_item(key, zz):
                continue
            r = footprint(key, x, y, f)
            rects.append((key, r))
            m = np.zeros_like(zmask)
            m[rect_slice(*r)] = True
            m &= floor
            g = ZO.group_of(key)
            by_group[g] = by_group.get(g, 0) + m.sum() / SFT
            occ |= m
            if g != "seat":
                occ_nochair |= m
        free = floor & ~occ
        # overlaps between items (chairs may tuck under desks: ignore seat-workstation pairs) and items out of the zone
        clashes = []
        for a in range(len(rects)):
            ka, ra = rects[a]
            out = np.zeros_like(zmask)
            out[rect_slice(*ra)] = True
            if (out & ~floor).sum() > 4:
                clashes.append(f"{ka} at ({(ra[0] + ra[2]) / 2:.0f}, {(ra[1] + ra[3]) / 2:.0f}) outside the floor / on a column or partition: {(out & ~floor).sum()} sq in")
            for b in range(a + 1, len(rects)):
                kb, rb = rects[b]
                ga, gb = ZO.group_of(ka), ZO.group_of(kb)
                if {ga, gb} & {"seat"} and {ga, gb} & {"workstation", "activity"}:
                    continue
                ox = min(ra[2], rb[2]) - max(ra[0], rb[0])
                oy = min(ra[3], rb[3]) - max(ra[1], rb[1])
                if ox > 1 and oy > 1:
                    clashes.append(f"{ka} overlaps {kb} ({ox:.0f} x {oy:.0f} in)")
        keep = []
        for lab, *r in KEEP_CLEAR[zid]:
            m = np.zeros_like(zmask)
            m[rect_slice(*r)] = True
            hit = (m & occ).sum()
            keep.append({"zone": lab, "blocked_sq_in": int(hit), "ok": bool(hit == 0)})
        # clearances
        clear = chessboard(free)
        pts = POINTS[zid]
        routes = []
        crel = relieve(clear, list(pts.values()), 24)
        crel[~free] = 0
        cache = {}
        for a, b, need in ROUTES[zid]:
            if a not in cache:
                cache[a] = widest(crel, cell(pts[a]))
            bt = cache[a][cell(pts[b])]
            w = width_of(bt) if bt > 0 else 0
            routes.append({"from": a, "to": b, "clear_width_in": w, "target_in": need, "ok": bool(w >= need)})
        # seat access with chairs tucked in
        free2 = floor & ~occ_nochair
        clear2 = chessboard(free2)
        seats = [(k, x, y) for k, x, y, f, z, zz, lab in items if ZO.group_of(k) == "seat"]
        clear2 = relieve(clear2, [pts[ENTRY[zid]]], 24)
        clear2 = relieve(clear2, [(x, y) for k, x, y in seats], 12)
        clear2[~free2] = 0
        acc = widest(clear2, cell(pts[ENTRY[zid]]))
        seat_w = [width_of(acc[cell((x, y))]) for k, x, y in seats]
        work = 0
        for k, x, y, f, z, zz, lab in items:
            if k in ASSETS and ASSETS[k][0] == "bench_desk":
                work += 2 * ASSETS[k][1].get("n", 3)
            elif k == "desk_single":
                work += 1
        storage_lin = sum(ASSETS[k][2][0] for k, *_ in items if k in ZO.STORAGE_HEIGHT)
        storage_vol = sum(ASSETS[k][2][0] * ASSETS[k][2][1] * ZO.STORAGE_HEIGHT[k] for k, *_ in items if k in ZO.STORAGE_HEIGHT) / 1728
        res["zones"][zid] = {
            "label": ZLABEL[zid], "gross_sft": round(gross, 1), "columns_sft": round(colm.sum() / SFT, 1),
            "new_partitions_sft": round(wallm.sum() / SFT, 1), "net_floor_sft": round(floor.sum() / SFT, 1),
            "footprint_sft": {g: round(v, 1) for g, v in sorted(by_group.items())},
            "free_floor_sft": round(free.sum() / SFT, 1),
            "idle_floor_sft": round((clear > 30).sum() / SFT, 1),      # floor more than 30 in from any wall, column or item
            "workstations": work, "seats_total": len(seats), "other_seats": len(seats) - work,
            "net_sft_per_workstation": round(floor.sum() / SFT / max(work, 1), 1),
            "storage_linear_in": storage_lin, "storage_volume_cuft": round(storage_vol, 1),
            "routes": routes, "keep_clear": keep,
            "seat_access_min_in": min(seat_w) if seat_w else None,
            "seats_below_36in": sum(1 for v in seat_w if v < 36),
            "seats_unreachable": sum(1 for v in seat_w if v <= 0),
            "seats_below_36in_at": [f"{k} ({x:.0f}, {y:.0f}): {v} in" for (k, x, y), v in zip(seats, seat_w) if v < 36],
            "clashes": clashes,
            "functions": [f[0] for f in layout.functions if _in_zone(f, ZPOLY[zid])],
        }
        res["zones"][zid]["_free"] = free
        res["zones"][zid]["_clear"] = clear
    return res


def _in_zone(f, poly):
    cx, cy = (f[1] + f[3]) / 2, (f[2] + f[4]) / 2
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    return min(xs) <= cx <= max(xs) and min(ys) <= cy <= max(ys)


# ------------------------------------------------------------------------------------------ drawing
COL = {"workstation": "#DCE3EA", "seat": "#9AA5B1", "storage": "#E2D3BC", "activity": "#CFE3D4", "equipment": "#D0D0D0",
       "wall": "#3C6E4F", "plant": "#9CC59F", "other": "#EEE"}


def svg_plan(layout, res, path):
    vx0, vy0, vw, vh = 20, -930, 870, 760
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx0} {vy0} {vw} {vh + 70}" width="{vw * 1.6:.0f}" height="{(vh + 70) * 1.6:.0f}" '
         f'font-family="Inter, Helvetica, Arial">', f'<rect x="{vx0}" y="{vy0}" width="{vw}" height="{vh + 70}" fill="#fff"/>']
    for zid in ("Z06", "Z07", "Z09", "Z33", "Z30"):
        if zid in ZPOLY:
            pts = " ".join(f"{x},{y}" for x, y in ZPOLY[zid])
            fill = "#FAFAF7" if zid in ("Z06", "Z07") else "#F0F0F0"
            p.append(f'<polygon points="{pts}" fill="{fill}" stroke="#bbb" stroke-width="0.6"/>')
    # free floor tint (clear width >= 48 in) to show real circulation
    for zid in ("Z06", "Z07"):
        clear = res["zones"][zid]["_clear"]
        core = clear >= 24
        ok = (chessboard(~core) <= 24) & (clear > 0) if core.any() else core
        for i in range(0, ok.shape[0], 4):
            row = ok[i]
            j = 0
            while j < row.size:
                if row[j]:
                    k = j
                    while k < row.size and row[k]:
                        k += 1
                    p.append(f'<rect x="{X0 + j}" y="{Y0 + i}" width="{k - j}" height="4" fill="#E3F1E6"/>')
                    j = k
                else:
                    j += 1
    for w in SV.WALLS:
        if w["axis"] == "h":
            x0, x1, y0, y1 = w["a"], w["b"], w["c0"], w["c1"]
        else:
            x0, x1, y0, y1 = w["c0"], w["c1"], w["a"], w["b"]
        if x1 < X0 - 20 or x0 > X1 + 20 or y1 < Y0 - 20 or y0 > Y1 + 20:
            continue
        p.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="#444"/>')
        for op in w["ops"]:
            if w["axis"] == "h":
                p.append(f'<rect x="{op[2]}" y="{y0 - 1}" width="{op[3] - op[2]}" height="{y1 - y0 + 2}" fill="#fff"/>')
            else:
                p.append(f'<rect x="{x0 - 1}" y="{op[2]}" width="{x1 - x0 + 2}" height="{op[3] - op[2]}" fill="#fff"/>')
    for w in O.NEW_WALLS:
        if w["id"] in ("NP02", "NP03", "NP04", "NP33"):
            x0, x1, y0, y1 = (w["a"], w["b"], w["c0"], w["c1"]) if w["axis"] == "h" else (w["c0"], w["c1"], w["a"], w["b"])
            p.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="#666"/>')
            for op in w["ops"]:
                if w["axis"] == "h":
                    p.append(f'<rect x="{op[2]}" y="{y0 - 1}" width="{op[3] - op[2]}" height="{y1 - y0 + 2}" fill="#fff"/>')
                else:
                    p.append(f'<rect x="{x0 - 1}" y="{op[2]}" width="{x1 - x0 + 2}" height="{op[3] - op[2]}" fill="#fff"/>')
    # half walls (48 in) dashed outline to remind they carry glass above
    for w in layout.walls:
        x0, x1, y0, y1 = (w["a"], w["b"], w["c0"], w["c1"]) if w["axis"] == "h" else (w["c0"], w["c1"], w["a"], w["b"])
        p.append(f'<rect x="{min(x0, x1)}" y="{min(y0, y1)}" width="{abs(x1 - x0)}" height="{abs(y1 - y0)}" fill="#5B8FB9"/>')
        for op in w["ops"]:
            if w["axis"] == "h":
                p.append(f'<rect x="{op[2]}" y="{y0 - 1.5}" width="{op[3] - op[2]}" height="{y1 - y0 + 3}" fill="#fff"/>')
                p.append(f'<path d="M{op[2]},{y0} A{op[3] - op[2]},{op[3] - op[2]} 0 0 1 {op[3]},{y0 - (op[3] - op[2])}" fill="none" stroke="#5B8FB9" stroke-width="0.6"/>')
            else:
                p.append(f'<rect x="{x0 - 1.5}" y="{op[2]}" width="{x1 - x0 + 3}" height="{op[3] - op[2]}" fill="#fff"/>')
    for x, y in SV.COLUMNS:
        if X0 <= x <= X1 and Y0 - 10 <= y <= Y1:
            p.append(f'<rect x="{x - 5}" y="{y - 5}" width="10" height="10" fill="#111"/>')
    for x, y, rot, zid in O.AC_UNITS:
        if zid in ("Z06", "Z07"):
            p.append(f'<rect x="{x - 23.5}" y="{y - 13}" width="47" height="26" fill="none" stroke="#2E6DB4" stroke-width="1" stroke-dasharray="3 2"/>'
                     f'<text x="{x}" y="{y + 3}" font-size="8" text-anchor="middle" fill="#2E6DB4">AC</text>')
    for key, x, y, f, z, zz, lab in layout.items:
        if z not in ("Z06", "Z07"):
            continue
        x0, y0, x1, y1 = footprint(key, x, y, f)
        g = ZO.group_of(key)
        if g == "seat":
            p.append(f'<rect x="{x0 + 3}" y="{y0 + 3}" width="{x1 - x0 - 6}" height="{y1 - y0 - 6}" rx="5" fill="{COL[g]}" stroke="#555" stroke-width="0.5"/>')
        elif g == "plant":
            p.append(f'<circle cx="{x}" cy="{y}" r="{(x1 - x0) / 2}" fill="{COL[g]}" stroke="#4d7a52" stroke-width="0.5"/>')
        elif g == "wall":
            p.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{max(y1 - y0, 2)}" fill="{COL[g]}"/>')
        else:
            p.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="{COL[g]}" stroke="#555" stroke-width="0.6"/>')
            if key.startswith("bench"):
                if (x1 - x0) >= (y1 - y0):
                    p.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#555" stroke-width="0.6"/>')
                    n = ASSETS[key][1].get("n", 3)
                    for k in range(1, n):
                        xx = x0 + (x1 - x0) * k / n
                        p.append(f'<line x1="{xx}" y1="{y0}" x2="{xx}" y2="{y1}" stroke="#888" stroke-width="0.4"/>')
    for lab, x0, y0, x1, y1 in layout.functions:
        p.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="none" stroke="#C0392B" stroke-width="0.7" stroke-dasharray="4 3"/>')
        p.append(f'<text x="{(x0 + x1) / 2}" y="{y0 - 3 if y0 > -900 else y1 + 9}" font-size="7.5" text-anchor="middle" fill="#C0392B">{lab}</text>')
    for zid in ("Z06", "Z07"):
        z = res["zones"][zid]
        cx, cy = O.LABEL_AT[zid]
        cx, cy = (205, -760) if zid == "Z06" else (616, -880)
    p.append(f'<text x="200" y="-905" font-size="13" font-weight="700" text-anchor="middle">Z06 COMMERCIAL &amp; ACCOUNTS</text>')
    p.append(f'<text x="616" y="-905" font-size="13" font-weight="700" text-anchor="middle">Z07 MERCHANDISING</text>')
    # scale bar 10 ft
    p.append('<rect x="40" y="-200" width="120" height="4" fill="#222"/><rect x="40" y="-200" width="60" height="4" fill="#fff" stroke="#222" stroke-width="0.5"/>'
             '<text x="40" y="-185" font-size="8">0</text><text x="96" y="-185" font-size="8">5 ft</text><text x="150" y="-185" font-size="8">10 ft</text>')
    z6, z7 = res["zones"]["Z06"], res["zones"]["Z07"]
    p.append(f'<text x="200" y="-180" font-size="12" font-weight="700">{layout.name}</text>')
    p.append(f'<text x="200" y="-166" font-size="8.5">Z07: {z7["workstations"]} desks, {z7["other_seats"]} other seats, '
             f'storage {z7["storage_linear_in"] / 12:.0f} lin ft / {z7["storage_volume_cuft"]:.0f} cu ft, free floor {z7["free_floor_sft"]:.0f} sft  |  '
             f'Z06: {z6["workstations"]} desks, storage {z6["storage_linear_in"] / 12:.0f} lin ft / {z6["storage_volume_cuft"]:.0f} cu ft, free floor {z6["free_floor_sft"]:.0f} sft</text>')
    p.append('<text x="200" y="-153" font-size="7.5" fill="#555">Green tint: floor with at least 48 in (1220 mm) clear width. Blue: proposed glazed screens. Dashed blue: ceiling AC positions (unchanged). '
             'Black squares: steel columns (positions PHOTO-EST). Plan inches, north up.</text>')
    p.append("</svg>")
    with open(path, "w") as f:
        f.write("\n".join(p))


def main():
    allres = {}
    for key, fn in ZO.OPTIONS.items():
        lay = fn()
        r = analyse(lay)
        svg_plan(lay, r, os.path.join(OUT, f"plan_{key}.svg"))
        for z in r["zones"].values():
            z.pop("_free")
            z.pop("_clear")
        allres[key] = r
        print(key, json.dumps({z: {k: v for k, v in d.items() if k in ("workstations", "seats_total", "free_floor_sft", "storage_linear_in", "seat_access_min_in", "seats_below_36in")} for z, d in r["zones"].items()}))
        for zid, d in r["zones"].items():
            for rt in d["routes"]:
                if not rt["ok"]:
                    print("   ROUTE", zid, rt)
            for k in d["keep_clear"]:
                if not k["ok"]:
                    print("   KEEP", zid, k)
            for c in d["clashes"]:
                print("   CLASH", zid, c)
    with open(os.path.join(OUT, "metrics.json"), "w") as f:
        json.dump(allres, f, indent=1)


if __name__ == "__main__":
    main()
