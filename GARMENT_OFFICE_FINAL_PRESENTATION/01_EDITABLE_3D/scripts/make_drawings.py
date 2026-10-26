"""2D drawings from the same data as the 3D model (survey.py + office_layout.py), as SVG.
python3 make_drawings.py OUT_DIR   ->  ID-01_furnished_plan.svg, ID-02_zoning_plan.svg, ID-03_ceiling_lighting_plan.svg,
                                      ID-04_power_data_fire_plan.svg  (convert with export_drawings.js / Chromium)
Plan inches map 1:1 to SVG units (x east, y south = SVG down)."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import office_layout as O  # noqa: E402
import survey as S  # noqa: E402

OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
os.makedirs(OUT, exist_ok=True)
X0, X1, Y0, Y1 = -300, 1600, -1800, 890          # A3 portrait frame (inches of plan, 1900 x 2690)
GREEN = "#26673D"

ZONE_GROUP = {"Reception": ("Visitor & reception", "#E9DCC3"), "Experience_Center": ("Experience centre", "#F1D3B5"),
              "Meeting_Rooms": ("Meeting", "#D9E4D1"), "Executive_Area": ("Executive", "#E7D2C4"),
              "Workstations": ("Administration & workspaces", "#DCE3EA"), "Design_Development": ("Design & development", "#D4E6DC"),
              "Support_Rooms": ("Staff support & circulation", "#ECE9E2"), "Prayer_Rooms": ("Prayer", "#D6E5D9"),
              "Washrooms": ("Washrooms", "#DDE9EE")}
FIN = {"fl_terrazzo": "TZ terrazzo", "fl_herringbone": "WD oak herringbone", "fl_carpet": "CP carpet tile", "fl_carpet_green": "CP prayer carpet",
       "fl_oak_planks": "WD oak planks", "fl_concrete": "PC polished concrete", "fl_porcelain": "PT porcelain tile"}

# door swings: hinge end ('a' or 'b' along the wall) and side (+1 = towards +y / +x)
SWING = {"D02": ("b", -1), "D04": ("a", 1), "D05": ("a", 1), "D06": ("b", 1), "D08": ("a", -1), "D09": ("b", -1), "D10": ("b", -1),
         "D13": ("a", 1), "D14": ("a", 1), "D15": ("b", -1), "D16": ("a", 1), "D17": ("a", -1), "D18": ("a", -1), "D19": ("b", -1),
         "D20": ("a", -1), "D21": ("b", -1), "D22": ("a", -1), "D32": ("a", -1), "D33": ("b", -1), "D34": ("a", -1), "D35": ("a", -1),
         "D36": ("a", -1), "D37": ("b", -1), "D39": ("a", 1), "D41": ("a", -1), "D42": ("b", -1), "D43": ("a", 1), "D44": ("b", 1),
         "D46": ("a", 1), "D47": ("b", 1), "D48": ("a", 1), "D49": ("b", -1), "D01": ("a", -1), "D03": ("a", -1), "D38": ("a", -1),
         "D40": ("a", -1)}


def ftin(v):
    v = round(v)
    return f"{v // 12}'-{v % 12}\""


class Svg:
    def __init__(self, title, sheet):
        self.title, self.sheet = title, sheet
        self.parts = []

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, size=9, anchor="middle", weight=400, fill="#222", rot=0, family="Inter, Helvetica, Arial"):
        tr = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot else ""
        s = s.replace("&", "&amp;").replace("<", "&lt;")
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
                 f'text-anchor="{anchor}" fill="{fill}"{tr}>{s}</text>')

    def rect(self, x0, y0, x1, y1, fill="none", stroke="#222", sw=1.0, extra=""):
        x0, x1 = min(x0, x1), max(x0, x1)
        y0, y1 = min(y0, y1), max(y0, y1)
        self.add(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{x1 - x0:.2f}" height="{y1 - y0:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

    def line(self, x0, y0, x1, y1, stroke="#222", sw=1.0, extra=""):
        self.add(f'<line x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y1:.2f}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

    def poly(self, pts, fill="none", stroke="#222", sw=1.0, extra=""):
        p = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
        self.add(f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

    def circle(self, x, y, r, fill="none", stroke="#222", sw=1.0, extra=""):
        self.add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

    def save(self, name, legend=None, notes=()):
        w, h = X1 - X0, Y1 - Y0
        tb = self.title_block(legend, notes)
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{X0} {Y0} {w} {h}" width="{w * 0.7:.0f}" height="{h * 0.7:.0f}">'
               f'<rect x="{X0}" y="{Y0}" width="{w}" height="{h}" fill="#FFFFFF"/>' + "".join(self.parts) + tb + "</svg>")
        with open(os.path.join(OUT, name), "w") as f:
            f.write(svg)
        return name

    def title_block(self, legend, notes):
        s = []
        x, y, w, h = -270, 470, 1840, 400
        s.append(f'<rect x="{X0 + 12}" y="{Y0 + 12}" width="{X1 - X0 - 24}" height="{Y1 - Y0 - 24}" fill="none" stroke="#222" stroke-width="2"/>')
        s.append(f'<line x1="{X0 + 12}" y1="{y}" x2="{X1 - 12}" y2="{y}" stroke="#222" stroke-width="1.5"/>')
        s.append(f'<text x="{x}" y="{y + 56}" font-family="Inter, Arial" font-size="40" font-weight="700" fill="{GREEN}">{self.sheet}</text>')
        s.append(f'<text x="{x + 120}" y="{y + 56}" font-family="Inter, Arial" font-size="30" font-weight="600" fill="#222">{self.title}</text>')
        s.append(f'<text x="{x}" y="{y + 92}" font-family="Inter, Arial" font-size="16" fill="#444">Ground-floor corporate office - Stage II Knitting Apparel Ltd. / Unit-1 / Zara Fashion - Holding 329/2, Ward 15, Vogra, Bason, Gazipur</text>')
        s.append(f'<text x="{x}" y="{y + 114}" font-family="Inter, Arial" font-size="16" fill="#444">Interior design proposal - not for construction - all dimensions to be verified on site</text>')
        yy = y + 150
        for n in notes:
            s.append(f'<text x="{x}" y="{yy}" font-family="Inter, Arial" font-size="14" fill="#333">{n.replace("&", "&amp;")}</text>')
            yy += 21
        if legend:
            lx, ly = x + 960, y + 150
            for i, (sym, label) in enumerate(legend):
                cx = lx - 120 + (i // 9) * 520
                cy = ly + (i % 9) * 24
                s.append(sym.replace("{x2}", str(cx + 24)).replace("{x}", str(cx)).replace("{y}", str(cy - 5)))
                s.append(f'<text x="{cx + 32}" y="{cy}" font-family="Inter, Arial" font-size="13.5" fill="#222">{label.replace("&", "&amp;")}</text>')
        sx, sy = -270, Y0 + 60
        for i in range(5):
            s.append(f'<rect x="{sx + i * 120}" y="{sy}" width="120" height="10" fill="{"#222" if i % 2 == 0 else "#FFF"}" stroke="#222" stroke-width="1"/>')
            s.append(f'<text x="{sx + i * 120}" y="{sy + 30}" font-family="Inter, Arial" font-size="14" text-anchor="middle">{i * 10} ft</text>')
        s.append(f'<text x="{sx + 600}" y="{sy + 30}" font-family="Inter, Arial" font-size="14" text-anchor="middle">50 ft</text>')
        nx, ny = -200, Y0 + 170
        s.append(f'<polygon points="{nx},{ny - 50} {nx - 18},{ny + 10} {nx},{ny - 2} {nx + 18},{ny + 10}" fill="#222"/>')
        s.append(f'<text x="{nx}" y="{ny + 36}" font-family="Inter, Arial" font-size="15" font-weight="700" text-anchor="middle">PLAN NORTH</text>')
        s.append(f'<text x="{nx}" y="{ny + 54}" font-family="Inter, Arial" font-size="11" text-anchor="middle">sketch orientation;</text>')
        s.append(f'<text x="{nx}" y="{ny + 68}" font-family="Inter, Arial" font-size="11" text-anchor="middle">true north to verify</text>')
        return "".join(s)


def openings_of(w):
    return sorted([(op[2], op[3], op) for op in w["ops"]])


def wall_segments(w):
    """Remaining wall pieces after the openings (doors full height; windows drawn separately)."""
    segs, pos = [], w["a"]
    for a, b, op in openings_of(w):
        if a > pos:
            segs.append((pos, a))
        pos = max(pos, b)
    if pos < w["b"]:
        segs.append((pos, w["b"]))
    return segs


def all_walls():
    walls = {w["id"]: dict(w, ops=[list(o) for o in w["ops"]]) for w in S.WALLS}
    for wid, op in O.NEW_OPENINGS + O.EXTRA_OPENINGS:
        walls[wid]["ops"].append(list(op))
    for wid, ids in O.REMOVED_OPENINGS.items():
        walls[wid]["ops"] = [o for o in walls[wid]["ops"] if o[0] not in ids]
    return list(walls.values()), [dict(w) for w in O.NEW_WALLS]


def draw_walls(svg, glass_color="#3E8FA8", light=False):
    existing, new = all_walls()
    half_treat = {}
    for wid, a, b, t in O.HALF_TREAT:
        half_treat.setdefault(wid, []).append((a, b, t))
    for w in existing + new:
        kind = w["kind"]
        if kind == "glass":
            c = (w["c0"] + w["c1"]) / 2
            for a, b in wall_segments(w):
                if w["axis"] == "h":
                    svg.line(a, c - 1, b, c - 1, glass_color, 1.0)
                    svg.line(a, c + 1, b, c + 1, glass_color, 1.0)
                    k = a
                    while k <= b:
                        svg.line(k, c - 2.2, k, c + 2.2, "#222", 1.4)
                        k += 48
                else:
                    svg.line(c - 1, a, c - 1, b, glass_color, 1.0)
                    svg.line(c + 1, a, c + 1, b, glass_color, 1.0)
                    k = a
                    while k <= b:
                        svg.line(c - 2.2, k, c + 2.2, k, "#222", 1.4)
                        k += 48
        else:
            fill = {"ext": "#1E1E1E", "int": "#3A3A3A", "half": "#8C8C8C", "part": "#6A6A6A", "new": "#B9B4AA"}[kind]
            if light:
                fill = {"ext": "#444", "int": "#666", "half": "#AAA", "part": "#999", "new": "#C8C4BC"}[kind]
            for a, b in wall_segments(w):
                if w["axis"] == "h":
                    svg.rect(a, w["c0"], b, w["c1"], fill, "#111", 0.6)
                else:
                    svg.rect(w["c0"], a, w["c1"], b, fill, "#111", 0.6)
            for a, b, t in half_treat.get(w["id"], []):
                c = (w["c0"] + w["c1"]) / 2
                if t == "glass":
                    if w["axis"] == "h":
                        svg.line(a, c, b, c, glass_color, 1.6, 'stroke-dasharray="6 3"')
                    else:
                        svg.line(c, a, c, b, glass_color, 1.6, 'stroke-dasharray="6 3"')
        for op in w["ops"]:
            oid, kind_o, a, b = op[:4]
            c0, c1 = w["c0"], w["c1"]
            c = (c0 + c1) / 2
            if kind_o == "win":
                if w["axis"] == "h":
                    svg.rect(a, c0, b, c1, "#FFFFFF", "#111", 0.6)
                    svg.line(a, c, b, c, glass_color, 1.4)
                else:
                    svg.rect(c0, a, c1, b, "#FFFFFF", "#111", 0.6)
                    svg.line(c, a, c, b, glass_color, 1.4)
            else:
                typ = O.DOOR_TYPES.get(oid, ("solid", ""))[0]
                hinge, side = SWING.get(oid, ("a", 1))
                leaves = 2 if typ in ("glass2", "solid2") else 1
                width = (b - a) / leaves
                if typ == "none":
                    if w["axis"] == "h":
                        svg.line(a, c0, b, c0, "#777", 0.8, 'stroke-dasharray="4 3"')
                        svg.line(a, c1, b, c1, "#777", 0.8, 'stroke-dasharray="4 3"')
                    else:
                        svg.line(c0, a, c0, b, "#777", 0.8, 'stroke-dasharray="4 3"')
                        svg.line(c1, a, c1, b, "#777", 0.8, 'stroke-dasharray="4 3"')
                    continue
                if typ == "slide":
                    if w["axis"] == "h":
                        svg.line(a, c - 2, (a + b) / 2 + 4, c - 2, "#222", 1.4)
                    else:
                        svg.line(c - 2, a, c - 2, (a + b) / 2 + 4, "#222", 1.4)
                    continue
                for i in range(leaves):
                    if leaves == 2:
                        hp, sign = (a, 1) if i == 0 else (b, -1)
                    else:
                        hp, sign = (a, 1) if hinge == "a" else (b, -1)
                    face = c1 if side > 0 else c0
                    r = width
                    if w["axis"] == "h":
                        ex, ey = hp, face + side * r
                        svg.line(hp, face, ex, ey, "#222", 1.3)
                        sweep = 1 if (sign * side) > 0 else 0
                        svg.add(f'<path d="M {ex:.1f} {ey:.1f} A {r:.1f} {r:.1f} 0 0 {sweep} {hp + sign * r:.1f} {face:.1f}" fill="none" stroke="#666" stroke-width="0.7" stroke-dasharray="3 2"/>')
                    else:
                        ex, ey = face + side * r, hp
                        svg.line(face, hp, ex, ey, "#222", 1.3)
                        sweep = 0 if (sign * side) > 0 else 1
                        svg.add(f'<path d="M {ex:.1f} {ey:.1f} A {r:.1f} {r:.1f} 0 0 {sweep} {face:.1f} {hp + sign * r:.1f}" fill="none" stroke="#666" stroke-width="0.7" stroke-dasharray="3 2"/>')


def draw_structure(svg, beams=False):
    for x, y in S.COLUMNS:
        svg.rect(x - 5, y - 5, x + 5, y + 5, "#000", "#000", 0.5)
    if beams:
        for name, x0, x1, y0, y1, d in S.beam_list():
            svg.rect(x0, y0, x1, y1, "none", "#9A9A9A", 0.6, 'stroke-dasharray="8 4"')


def draw_stairs(svg):
    n = round(S.FLOOR_TO_FLOOR / 7)
    up1 = n // 2 + 1
    for x0, x1, y_start, count, direction in ((2, 78, 102, up1, 1), (82, 158, 102 + up1 * S.TREAD, n - up1, -1)):
        for i in range(count + 1):
            y = y_start + direction * i * S.TREAD
            svg.line(x0, y, x1, y, "#555", 0.6)
        svg.line(x0, y_start, x0, y_start + direction * count * S.TREAD, "#555", 0.6)
        svg.line(x1, y_start, x1, y_start + direction * count * S.TREAD, "#555", 0.6)
    svg.add('<path d="M 40 110 L 40 226 L 120 226 L 120 120" fill="none" stroke="#222" stroke-width="1" marker-end="url(#arr)"/>')
    svg.text(40, 98, "UP", 9, weight=700)
    for tag, x0, x1, y0, y1 in (("NE STAIR (layout assumed)", S.R8_E - 273, S.R8_E, S.R8_N, S.R8_N + S.STAIR_T),
                                ("SE STAIR (layout assumed)", S.R8_E - 277, S.R8_E, S.SE_N, S.MID_S)):
        k = x0 + 30
        while k < x1 - 50:
            svg.line(k, y0 + 4, k, y1 - 4, "#888", 0.5)
            k += S.TREAD
        svg.text((x0 + x1) / 2, (y0 + y1) / 2, tag, 10, weight=600, fill="#555")
    for yy in (S.FRONT - 36, S.FRONT - 24):
        svg.line(160, yy, 300, yy, "#555", 0.8)
    svg.text(230, S.FRONT - 6, "2 STEPS UP TO GATE (est.)", 8, fill="#555")


def furniture_symbol(svg, key, x, y, facing, fill="#F7F5F0", stroke="#6F6A62"):
    if key.startswith("cc0:"):
        w, d = (32, 39) if "arm_chair" in key else (40, 47)
        desc = "chair"
    else:
        w, d = O.ASSETS[key][2]
        desc = O.ASSETS[key][0]
    a = math.radians(facing)

    def tr(px, py):            # local (x right, y back/up) -> plan; local -Y faces the 'facing' direction
        X = px * math.cos(a) - (-py) * math.sin(a)
        Y = px * math.sin(a) + (-py) * math.cos(a)
        return x + X, y - Y

    def rect_local(x0, y0, x1, y1, f=fill, s=stroke, sw=0.7):
        svg.poly([tr(x0, y0), tr(x1, y0), tr(x1, y1), tr(x0, y1)], f, s, sw)

    if "chair" in desc or desc in ("stool",) or key.startswith("cc0:"):
        if desc == "stool" or key == "stool":
            cx, cy = tr(0, 0)
            svg.circle(cx, cy, 7.5, fill, stroke, 0.7)
        else:
            rect_local(-w / 2 + 1, -d / 2 + 1, w / 2 - 1, d / 2 - 1)
            rect_local(-w / 2 + 1, d / 2 - 5, w / 2 - 1, d / 2 - 1, "#D8D2C6")
        return
    if desc in ("bench_desk",):
        rect_local(-w / 2, -d / 2, w / 2, d / 2, "#FFFFFF")
        svg.poly([tr(-w / 2, -0.6), tr(w / 2, -0.6), tr(w / 2, 0.6), tr(-w / 2, 0.6)], GREEN, GREEN, 0.4)
        n = O.ASSETS[key][1].get("n", 2)
        for k in range(1, n):
            xx = -w / 2 + w * k / n
            p, q = tr(xx, -d / 2), tr(xx, d / 2)
            svg.line(p[0], p[1], q[0], q[1], stroke, 0.5)
        return
    if desc == "sofa":
        rect_local(-w / 2, -d / 2, w / 2, d / 2, "#EDE6D8")
        rect_local(-w / 2, d / 2 - 8, w / 2, d / 2, "#D9CFBC")
        return
    if desc in ("round_table", "planter"):
        cx, cy = tr(0, 0)
        svg.circle(cx, cy, w / 2, fill if desc != "planter" else "#E3EDDF", stroke, 0.7)
        return
    if desc in ("boardroom_table",):
        rect_local(-w / 2 + d / 2, -d / 2, w / 2 - d / 2, d / 2, "#E8DCCB", "none", 0)
        for sx in (-1, 1):
            cx, cy = tr(sx * (w / 2 - d / 2), 0)
            svg.circle(cx, cy, d / 2, "#E8DCCB", stroke, 0.7)
        rect_local(-w / 2 + d / 2, -d / 2, w / 2 - d / 2, d / 2, "#E8DCCB", "none", 0)
        p0, p1 = tr(-w / 2 + d / 2, -d / 2), tr(w / 2 - d / 2, -d / 2)
        svg.line(p0[0], p0[1], p1[0], p1[1], stroke, 0.7)
        p0, p1 = tr(-w / 2 + d / 2, d / 2), tr(w / 2 - d / 2, d / 2)
        svg.line(p0[0], p0[1], p1[0], p1[1], stroke, 0.7)
        return
    if desc == "wc_pan":
        cx, cy = tr(0, -5)
        svg.add(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="7" ry="10" fill="#FFF" stroke="{stroke}" stroke-width="0.7" transform="rotate({facing} {cx:.1f} {cy:.1f})"/>')
        rect_local(-9, 9, 9, 13, "#FFF")
        return
    if desc in ("rug",):
        rect_local(-w / 2, -d / 2, w / 2, d / 2, "none", "#B9AE9C", 0.6)
        return
    shade = {"garment_rail_bay": "#E4EDE6", "cabinet": "#F1EEE8", "shelving": "#EFE8DC", "wall_screen": "#333", "pinboard_wall": "#E8E2D6",
             "reception_desk": "#E3D3BC", "exec_desk": "#DCC7B0", "plinth_display": "#E9DCC3", "material_table": "#E3D3BC"}.get(desc, fill)
    rect_local(-w / 2, -d / 2, w / 2, d / 2, shade)


def dims(svg):
    def hdim(x0, x1, y, label, below=True):
        svg.line(x0, y, x1, y, "#333", 0.8)
        for x in (x0, x1):
            svg.line(x - 4, y + 4, x + 4, y - 4, "#333", 1.0)
            svg.line(x, y - 10, x, y + 10, "#333", 0.6)
        svg.text((x0 + x1) / 2, y + (16 if below else -6), label, 10.5)

    def vdim(x, y0, y1, label):
        svg.line(x, y0, x, y1, "#333", 0.8)
        for y in (y0, y1):
            svg.line(x - 4, y + 4, x + 4, y - 4, "#333", 1.0)
            svg.line(x - 10, y, x + 10, y, "#333", 0.6)
        svg.text(x - 8, (y0 + y1) / 2, label, 10.5, rot=-90)

    F = S.FRONT
    hdim(0, 300, F + 40, f"ROOM 1  {ftin(300)}")
    hdim(305, 565, F + 40, f"ROOM 3  {ftin(260)}")
    hdim(570, 1088, F + 40, f"ROOM 4  {ftin(518)}")
    hdim(-10, 1098, F + 90, f"OVERALL FRONT  {ftin(1108)} (outside faces)")
    vdim(-110, 0, F, f"{ftin(247)}")
    vdim(-110, S.MID_N, S.MID_S, f"MIDDLE BLOCK {ftin(881)}")
    vdim(-170, S.MID_N - 10, F + 10, f"OVERALL WEST DEPTH {ftin(1158)}")
    vdim(S.R8_E + 70, S.R8_N, S.MID_S, f"ROOM 8 {ftin(1538)}")
    vdim(S.R8_E + 130, S.R8_N - 10, F + 10, f"OVERALL EAST DEPTH {ftin(1815)}")
    hdim(S.R8_W, S.R8_E, S.R8_N - 60, f"ROOM 8  {ftin(450)}  (ASSUMED - measure on site)", below=False)
    hdim(367, 866, S.MID_N - 60, f"ROOMS 5 / 6  {ftin(499)}", below=False)
    hdim(46, S.R7_E, S.MID_N - 60, f"ROOM 7  {ftin(316)}", below=False)
    vdim(905, S.R6_N, S.R6_S, "")


def zone_labels(svg, finish=True, size_scale=1.0):
    svg.text(1243, -330, "SUB-STATION", 11 * size_scale, weight=700, fill="#555")
    svg.text(1243, -316, "(existing, utility)", 8.5 * size_scale, fill="#555")
    for coll_name, zid, label, pts, fin, ceiling in O.ZONES:
        x, y = O.LABEL_AT[zid]
        area = S.poly_area_sft(pts)
        lines = label.splitlines()
        rot = -90 if zid in O.VERTICAL_LABELS else 0
        big = 13 * size_scale if area > 250 else 10 * size_scale
        svg.text(x, y, lines[0], big, weight=700, rot=rot, fill="#1B1B1B")
        if zid not in O.SMALL_LABELS:
            svg.text(x + (0 if not rot else 14), y + (14 if not rot else 0), f"{area:,.0f} sft" + (f"  |  {FIN[fin]}" if finish else ""),
                     8.5 * size_scale, rot=rot, fill="#444")


def furnished_plan():
    svg = Svg("Furnished floor plan with dimensions", "ID-01")
    svg.add('<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#222"/></marker></defs>')
    for coll_name, zid, label, pts, fin, ceiling in O.ZONES:
        tint = {"fl_terrazzo": "#F3EEE4", "fl_herringbone": "#EFE3D2", "fl_carpet": "#E9EAEC", "fl_carpet_green": "#E3ECE4",
                "fl_oak_planks": "#F1E8DA", "fl_concrete": "#EEEEEC", "fl_porcelain": "#EDF2F4"}[fin]
        svg.poly(pts, tint, "none", 0)
    for key, x, y, facing, zone, z, label in O.PLACEMENTS:
        if key in ("fire_ext",) or key.startswith("screen") or key in ("pinboard_merch", "moodboard", "totem", "whiteboard"):
            continue
        furniture_symbol(svg, key, x, y, facing)
    draw_structure(svg)
    draw_stairs(svg)
    draw_walls(svg)
    zone_labels(svg)
    dims(svg)
    legend = [('<rect x="{x}" y="{y}" width="22" height="8" fill="#1E1E1E"/>', "Existing wall (survey)"),
              ('<rect x="{x}" y="{y}" width="22" height="8" fill="#8C8C8C"/>', "Existing 48 in wall (+ glass or solid infill above, dashed = glass)"),
              ('<rect x="{x}" y="{y}" width="22" height="8" fill="#B9B4AA"/>', "New partition (proposed)"),
              ('<line x1="{x}" y1="{y}" x2="{x2}" y2="{y}" stroke="#3E8FA8" stroke-width="3"/>', "Glass partition, slim black aluminium frame"),
              ('<rect x="{x}" y="{y}" width="8" height="8" fill="#000"/>', "Steel column (position estimated from photos)")]
    notes = ["All dimensions in feet-inches from the client's hand-measured sketches (see dimension_schedule.csv).",
             "Room 8 width, stair layouts, wall thicknesses, column positions and ceiling height are ASSUMED / PHOTO-EST.",
             "Door swings indicative; fire-exit doors to open in the direction of escape (to be confirmed).",
             "Furniture shown to scale from the 3D model; work seats: 54 incl. growth and guest seats."]
    return svg.save("ID-01_furnished_plan.svg", legend, notes)


def zoning_plan():
    svg = Svg("Space zoning and visitor / staff routes", "ID-02")
    svg.add('<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#B5462E"/></marker>'
            '<marker id="arrg" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#26673D"/></marker></defs>')
    for coll_name, zid, label, pts, fin, ceiling in O.ZONES:
        svg.poly(pts, ZONE_GROUP[coll_name][1], "#FFFFFF", 1.5)
    draw_structure(svg)
    draw_walls(svg, light=True)
    zone_labels(svg, finish=False)
    visitor = [(230, 236), (230, 150), (290, 40), (340, 40), (393, 20), (393, -200), (393, -250), (600, -300), (826, -250), (826, -200), (700, -150)]
    staff = [(230, 236), (180, 150), (135, 20), (135, -200), (200, -300), (330, -600), (330, -860), (600, -867), (809, -860), (809, -700),
             (871, -867), (1000, -872), (1072, -872), (1072, -500)]
    svg.add('<polyline points="' + " ".join(f"{x},{y}" for x, y in visitor) + '" fill="none" stroke="#B5462E" stroke-width="5" stroke-dasharray="14 7" marker-end="url(#arr)" opacity="0.9"/>')
    svg.add('<polyline points="' + " ".join(f"{x},{y}" for x, y in staff) + '" fill="none" stroke="#26673D" stroke-width="5" stroke-dasharray="14 7" marker-end="url(#arrg)" opacity="0.9"/>')
    exe = [(450, 40), (560, 37), (640, 40), (640, -30)]
    svg.add('<polyline points="' + " ".join(f"{x},{y}" for x, y in exe) + '" fill="none" stroke="#7A4E2D" stroke-width="4" stroke-dasharray="6 6" opacity="0.9"/>')
    legend = [(f'<rect x="{{x}}" y="{{y}}" width="22" height="12" fill="{c}"/>', n) for n, c in
              [(v[0], v[1]) for v in ZONE_GROUP.values()]]
    legend += [('<line x1="{x}" y1="{y}" x2="{x2}" y2="{y}" stroke="#B5462E" stroke-width="6"/>', "Visitor route: gate - lobby - reception - passage - experience centre - boardroom"),
               ('<line x1="{x}" y1="{y}" x2="{x2}" y2="{y}" stroke="#26673D" stroke-width="6"/>', "Staff route: gate - staff corridor - offices - hallway - design wing"),
               ('<line x1="{x}" y1="{y}" x2="{x2}" y2="{y}" stroke="#7A4E2D" stroke-width="6"/>', "Executive link: reception - executive suite - boardroom")]
    return svg.save("ID-02_zoning_plan.svg", legend, ["Zoning follows the client's office programme, the company profile departments and",
                                                      "the Global Design Studio master plan (studio zones about 1,400 sft)."])


def ceiling_plan():
    svg = Svg("Reflected ceiling + lighting plan (looking up)", "ID-03")
    svg.add('<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#222"/></marker></defs>')
    for coll_name, zid, label, pts, fin, ceiling in O.ZONES:
        svg.poly(pts, "#FAFAF8", "none", 0)
    draw_structure(svg, beams=True)
    draw_walls(svg, light=True)
    for kind, cx, cy, z, kw, zone in O.CEILING:
        if kind == "baffle":
            L = kw["L"]
            svg.line(cx, cy - L / 2, cx, cy + L / 2, GREEN if kw["mat"] == "felt_green" else "#8A8F93", 1.6)
        elif kind == "raft":
            svg.rect(cx - kw["w"] / 2, cy - kw["d"] / 2, cx + kw["w"] / 2, cy + kw["d"] / 2, "#C9DCCF", GREEN, 1.0)
        else:
            svg.rect(cx - kw["w"] / 2, cy - kw["d"] / 2, cx + kw["w"] / 2, cy + kw["d"] / 2, "#EADBC6", "#9C7B55", 1.0)
            k = cy - kw["d"] / 2
            while k < cy + kw["d"] / 2:
                svg.line(cx - kw["w"] / 2, k, cx + kw["w"] / 2, k, "#B89A74", 0.5)
                k += 4
    for kind, x, y, z, kw, zone in O.LIGHTS:
        temp = kw.get("temp", 3500)
        col = {3000: "#C77B20", 3500: "#D49A2A", 4000: "#4E7FA6"}.get(temp, "#D49A2A")
        if kind == "lin":
            L = kw.get("L", 72)
            if kw.get("rot", 0) == 90:
                svg.rect(x - 1.8, y - L / 2, x + 1.8, y + L / 2, col, "#222", 0.6)
            else:
                svg.rect(x - L / 2, y - 1.8, x + L / 2, y + 1.8, col, "#222", 0.6)
        elif kind == "halo":
            svg.circle(x, y, kw.get("r", 20), "none", col, 3)
        elif kind == "down":
            svg.circle(x, y, 4, col, "#222", 0.6)
        elif kind == "spot":
            svg.circle(x, y, 3, "#FFF", col, 1.6)
            tx, ty, tz = kw["aim"]
            dx, dy = tx - x, ty - y
            L = math.hypot(dx, dy) or 1
            svg.line(x, y, x + dx / L * 10, y + dy / L * 10, col, 1.2)
        elif kind == "track":
            L = kw.get("L", 120)
            if kw.get("rot", 0) == 90:
                svg.line(x, y - L / 2, x, y + L / 2, "#222", 2.2)
            else:
                svg.line(x - L / 2, y, x + L / 2, y, "#222", 2.2)
        elif kind == "pendant_cc0":
            svg.circle(x, y, 8, "#FFF", "#222", 1.0)
            svg.line(x - 6, y - 6, x + 6, y + 6, "#222", 0.8)
            svg.line(x - 6, y + 6, x + 6, y - 6, "#222", 0.8)
    for x, y, rot, zone in O.AC_UNITS:
        if rot == 90:
            svg.rect(x - 13, y - 23.5, x + 13, y + 23.5, "#FFF", "#1F5FA0", 1.2)
        else:
            svg.rect(x - 23.5, y - 13, x + 23.5, y + 13, "#FFF", "#1F5FA0", 1.2)
        svg.text(x, y + 3.5, "AC", 9, weight=700, fill="#1F5FA0")
    for x, y in O.SMOKE_DETECTORS:
        svg.circle(x, y, 4.5, "#FFF", "#B5462E", 1.2)
        svg.text(x, y + 2.5, "S", 6.5, weight=700, fill="#B5462E")
    for x, y, f in O.EXIT_SIGNS:
        svg.rect(x - 9, y - 4, x + 9, y + 4, GREEN, "#111", 0.6)
    zone_labels(svg, finish=False, size_scale=0.85)
    legend = [('<rect x="{x}" y="{y}" width="24" height="4" fill="#4E7FA6"/>', "Suspended linear LED 4000K, direct/indirect (offices, studio, CAD)"),
              ('<rect x="{x}" y="{y}" width="24" height="4" fill="#D49A2A"/>', "Suspended linear LED 3500K (reception, boardroom, executive)"),
              ('<circle cx="{x}" cy="{y}" r="5" fill="#D49A2A" stroke="#222"/>', "Surface cylinder downlight"),
              ('<circle cx="{x}" cy="{y}" r="4" fill="#FFF" stroke="#C77B20" stroke-width="2"/>', "Track / accent spot 3000K (aim shown)"),
              ('<circle cx="{x}" cy="{y}" r="8" fill="none" stroke="#C77B20" stroke-width="3"/>', "Brass halo pendant 3000K"),
              ('<rect x="{x}" y="{y}" width="24" height="8" fill="#EADBC6" stroke="#9C7B55"/>', "Suspended oak slat raft"),
              ('<rect x="{x}" y="{y}" width="24" height="8" fill="#C9DCCF" stroke="#26673D"/>', "Acoustic felt raft (boardroom)"),
              ('<line x1="{x}" y1="{y}" x2="{x2}" y2="{y}" stroke="#8A8F93" stroke-width="4"/>', "Acoustic felt baffles between beams (merchandising)"),
              ('<rect x="{x}" y="{y}" width="24" height="8" fill="none" stroke="#9A9A9A" stroke-dasharray="4 2"/>', "Exposed steel beam (kept, painted; layout PHOTO-EST)"),
              ('<rect x="{x}" y="{y}" width="24" height="10" fill="#FFF" stroke="#1F5FA0"/>', "VRF under-ceiling indoor unit (sizes by MEP engineer)"),
              ('<circle cx="{x}" cy="{y}" r="5" fill="#FFF" stroke="#B5462E"/>', "Smoke detector (to existing fire system)"),
              ('<rect x="{x}" y="{y}" width="20" height="8" fill="#26673D"/>', "Exit sign with emergency battery")]
    notes = ["Ceiling: existing steel deck and beams kept exposed and painted warm white (client instruction: beams stay).",
             "Underside of deck 9'-6\" (114 in) is a photo estimate - verify before ordering suspension lengths.",
             "Pendant bottoms: offices 80 in, reception/boardroom 80-84 in, halo 80-82 in above finished floor."]
    return svg.save("ID-03_ceiling_lighting_plan.svg", legend, notes)


def power_plan():
    svg = Svg("Power, data + fire safety layout (indicative)", "ID-04")
    svg.add('<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="#222"/></marker></defs>')
    for coll_name, zid, label, pts, fin, ceiling in O.ZONES:
        svg.poly(pts, "#FAFAF8", "none", 0)
    for key, x, y, facing, zone, z, label in O.PLACEMENTS:
        if key in ("fire_ext",):
            continue
        furniture_symbol(svg, key, x, y, facing, "#FBFBFB", "#C9C5BD")
    draw_structure(svg)
    draw_walls(svg, light=True)
    n_fb = n_dp = 0
    for key, x, y, facing, zone, z, label in O.PLACEMENTS:
        desc = O.ASSETS.get(key, ("",))[0] if not key.startswith("cc0:") else ""
        if desc == "bench_desk":
            n = O.ASSETS[key][1].get("n", 2)
            w = O.ASSETS[key][1].get("w", 55)
            for k in range(n):
                fx = x - n * w / 2 + w * (k + 0.5)
                svg.rect(fx - 5, y - 5, fx + 5, y + 5, "#FFF", "#1F5FA0", 1.4)
                svg.line(fx - 5, y - 5, fx + 5, y + 5, "#1F5FA0", 0.8)
                n_fb += 1
        elif desc in ("single_desk", "exec_desk", "reception_desk", "boardroom_table") or key in ("table_team", "table_present", "table_guest", "table_audit", "table_training"):
            svg.rect(x - 5, y - 5, x + 5, y + 5, "#FFF", "#1F5FA0", 1.4)
            svg.line(x - 5, y - 5, x + 5, y + 5, "#1F5FA0", 0.8)
            n_fb += 1
        elif desc in ("wall_screen", "cabinet", "fridge", "water_dispenser", "plotter", "printer_3d", "sewing_station", "steam_station", "pantry_run") and key not in ("credenza_oak", "credenza_72", "console", "filing_96", "filing_120", "tall_cab_90", "shoe_rack", "shoe_rack_36", "under_window_110", "ec_counter", "review_counter", "lockers8"):
            svg.add(f'<path d="M {x - 6:.1f} {y:.1f} a 6 6 0 0 1 12 0 z" fill="#FFF" stroke="#B5462E" stroke-width="1.3"/>')
            n_dp += 1
    for key, x, y, facing, zone, z, label in O.PLACEMENTS:
        if key == "fire_ext":
            svg.circle(x, y, 6, "#D2412B", "#111", 0.8)
            svg.text(x, y + 2.5, "FE", 6, weight=700, fill="#FFF")
    for x, y in O.SMOKE_DETECTORS:
        svg.circle(x, y, 4.5, "#FFF", "#B5462E", 1.2)
    for x, y, f in O.EXIT_SIGNS:
        svg.rect(x - 9, y - 4, x + 9, y + 4, GREEN, "#111", 0.6)
    for x, y in ((295, 230), (1101, -224), (1100, -1436), (365, -846), (6, 6)):
        svg.rect(x - 5, y - 5, x + 5, y + 5, "#D2412B", "#111", 0.8)          # manual call points
    svg.rect(1105, -300, 1125, -270, "#222", "#111", 0.8)
    svg.text(1140, -282, "DB (location TBC)", 8, anchor="start", weight=700)
    zone_labels(svg, finish=False, size_scale=0.85)
    legend = [('<rect x="{x}" y="{y}" width="10" height="10" fill="#FFF" stroke="#1F5FA0" stroke-width="1.5"/>', f"Floor box: 2 x 13A power + 2 x data (Cat6) - {n_fb} nos"),
              ('<path d="M {x} {y} a 6 6 0 0 1 12 0 z" fill="#FFF" stroke="#B5462E"/>', f"Dedicated socket at equipment - {n_dp} nos"),
              ('<circle cx="{x}" cy="{y}" r="6" fill="#D2412B"/>', "Fire extinguisher (CO2 / ABC powder, type by fire consultant)"),
              ('<rect x="{x}" y="{y}" width="10" height="10" fill="#D2412B"/>', "Manual call point (link to existing fire alarm)"),
              ('<circle cx="{x}" cy="{y}" r="5" fill="#FFF" stroke="#B5462E"/>', "Smoke detector"),
              ('<rect x="{x}" y="{y}" width="20" height="8" fill="#26673D"/>', "Exit sign / emergency light")]
    notes = ["Indicative only: circuits, cable sizes, UPS for IT, earthing and DB location by a licensed electrical engineer.",
             "Existing installed fire-safety systems (company profile) to be surveyed and extended by the fire consultant.",
             "Wall sockets at 450 mm AFF along walls every 3 m in offices are additional to the points shown."]
    return svg.save("ID-04_power_data_fire_plan.svg", legend, notes)


if __name__ == "__main__":
    for f in (furnished_plan(), zoning_plan(), ceiling_plan(), power_plan()):
        print("wrote", os.path.join(OUT, f))
