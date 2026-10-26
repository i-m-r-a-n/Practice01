"""Furniture, fixtures and display assets (procedural, real dimensions in inches) + CC0 model import.

Local frame: x right, y back, z up; origin at the floor centre; the user/front side faces local -Y.
Every builder returns an MB; get(name) builds the mesh once and caches it so repeated items share one
mesh datablock (small .blend, instanced in the .glb).
Typical dimensions follow ANSI/BIFMA and common Bangladesh market sizes (desk 1400 x 700 mm, task seat
height 460 mm, table height 740 mm, counter 1050 mm, bench screens 400 mm above the top, etc.).
"""
import math
import os
import random

import bpy

from lib_mesh import MB, ellipse, rounded_rect

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = os.path.abspath(os.path.join(HERE, '..', 'assets', 'models'))
CACHE = {}
MATS = {}


def init(materials):
    MATS.clear()
    MATS.update(materials)
    CACHE.clear()


def get(key, builder, *args, **kw):
    if key not in CACHE:
        CACHE[key] = builder(*args, **kw).mesh('A ' + key, MATS)
    return CACHE[key]


# ===================================================================================== seating
def task_chair(seat='fab_charcoal', back='mesh_black', arms=True):
    m = MB()
    # 5-star base with casters
    for k in range(5):
        a = math.radians(90 + 72 * k)
        ex, ey = 12.5 * math.cos(a), 12.5 * math.sin(a)
        m.rod((0, 0, 3.2), (ex, ey, 2.6), 0.75, 'alu_silver', segs=8)
        m.sphere((ex, ey, 1.1), 1.1, 'rubber', segs=10, rings=6)
    m.cyl(0, 0, 2.2, 2.4, 4.2, 'alu_silver', segs=20)
    m.cyl(0, 0, 1.0, 4.2, 15.5, 'chrome', segs=16)
    m.cyl(0, 0, 1.5, 4.2, 10.0, 'plastic_dark', segs=16)
    m.box(-8, 8, -8, 8, 15.2, 16.4, 'plastic_dark', bevel=0.4)
    m.box(-9.8, 9.8, -9.5, 8.8, 16.4, 19.3, seat, bevel=1.3, segs=3)          # seat cushion
    # backrest: frame + mesh, reclined 10 deg
    back_m = MB()
    back_m.box(-9.3, 9.3, -0.6, 0.6, 0, 20.5, back, bevel=0.5)
    back_m.box(-9.8, -8.8, -0.9, 0.9, 0, 21, 'plastic_dark', bevel=0.35)
    back_m.box(8.8, 9.8, -0.9, 0.9, 0, 21, 'plastic_dark', bevel=0.35)
    back_m.box(-9.8, 9.8, -0.9, 0.9, 20.3, 21.4, 'plastic_dark', bevel=0.4)
    back_m.box(-6, 6, -1.3, 0.2, 2, 8.5, 'plastic_dark', bevel=0.8)          # lumbar
    import mathutils
    m.box(-1.2, 1.2, 8.8, 10.8, 16, 23.5, 'plastic_dark', bevel=0.3)          # spine
    _transform(back_m, mathutils.Matrix.Rotation(math.radians(-10), 4, 'X'), (0, 10.6, 22.5))
    m.add(back_m)
    if arms:
        for s in (-1, 1):
            m.box(s * 10.6 - 0.6, s * 10.6 + 0.6, -1, 1, 16.5, 25.5, 'plastic_dark', bevel=0.3)
            m.box(s * 10.6 - 1.6, s * 10.6 + 1.6, -6, 4, 25.5, 26.7, 'plastic_dark', bevel=0.5)
    return m


def _transform(mb, matrix, offset=(0, 0, 0)):
    import bmesh
    from mathutils import Matrix
    bmesh.ops.transform(mb.bm, matrix=Matrix.Translation(offset) @ matrix, verts=mb.bm.verts)


def exec_chair(cover='leather_black', base='chrome', high=True):
    """High-back executive / boardroom chair with a polished 5-star base."""
    m = MB()
    for k in range(5):
        a = math.radians(90 + 72 * k)
        ex, ey = 13 * math.cos(a), 13 * math.sin(a)
        m.box(-0.9, 0.9, 0, 13.2, 2.0, 3.0, base, bevel=0.35, rot=a - math.pi / 2, pivot=(0, 0, 0))
        m.sphere((ex, ey, 1.0), 1.0, 'rubber', segs=10, rings=6)
    m.cyl(0, 0, 2.4, 2.2, 4.0, base, segs=20)
    m.cyl(0, 0, 1.0, 4.0, 15.8, 'chrome', segs=16)
    m.box(-8.5, 8.5, -8.5, 8.5, 15.6, 16.8, 'plastic_dark', bevel=0.4)
    m.box(-10.5, 10.5, -10, 9.5, 16.8, 19.8, cover, bevel=1.6, segs=3)
    bh = 26 if high else 18
    back_m = MB()
    back_m.box(-10.3, 10.3, -1.6, 1.6, 0, bh, cover, bevel=1.4, segs=3)
    import mathutils
    _transform(back_m, mathutils.Matrix.Rotation(math.radians(-9), 4, 'X'), (0, 10.4, 20.5))
    m.add(back_m)
    for s in (-1, 1):
        m.box(s * 11.3 - 0.5, s * 11.3 + 0.5, -2, 2, 16.8, 25, base, bevel=0.3)
        m.box(s * 11.3 - 1.4, s * 11.3 + 1.4, -7, 6, 25, 26.4, cover, bevel=0.6)
    return m


def side_chair(seat='fab_green', frame='oak', back_h=32):
    """Upholstered dining / visitor chair on four solid oak legs."""
    m = MB()
    for x in (-8, 8):
        for y in (-8, 8):
            m.box(x - 0.7, x + 0.7, y - 0.7, y + 0.7, 0, 17, frame, bevel=0.25)
    m.box(-9, 9, -9, 9, 15.5, 17, frame, bevel=0.3)
    m.box(-9.3, 9.3, -9.6, 9.0, 17, 19.2, seat, bevel=1.0, segs=3)
    m.box(-9, 9, 8, 9.6, 19, back_h - 2, frame, bevel=0.3)
    m.box(-9.3, 9.3, 8.4, 10.6, back_h - 13, back_h, seat, bevel=0.9, segs=3)
    return m


def cantilever_chair(seat='fab_charcoal', frame='chrome'):
    m = MB()
    r = 0.45
    for s in (-1, 1):
        x = s * 8.5
        m.rod((x, -10, 0.45), (x, 8, 0.45), r, frame)
        m.rod((x, -10, 0.45), (x, -9.5, 17), r, frame)
        m.rod((x, -9.5, 17), (x, 8, 17), r, frame)
        m.rod((x, 8, 17), (x, 9.5, 32), r, frame)
    m.box(-9.5, 9.5, -10.5, 8.5, 17, 19.2, seat, bevel=0.9, segs=3)
    m.box(-9.3, 9.3, 8.6, 10.4, 21, 32, seat, bevel=0.8, segs=3)
    return m


def stool(top='oak', h=25):
    m = MB()
    m.cyl(0, 0, 7.5, h - 1.6, h, top, segs=28)
    m.cyl(0, 0, 0.9, 1, h - 1.6, 'metal_black', segs=12)
    m.cyl(0, 0, 8, 0, 1, 'metal_black', segs=28)
    m.lathe([(6.5, 9), (6.8, 9.6), (6.5, 10.2)], 'metal_black', segs=24)
    return m


def sofa(length=84, depth=34, cover='fab_sand', arms=True, back=True, seats=None, legs='metal_black'):
    """Contemporary low sofa: recessed plinth, square arms, split seat and back cushions."""
    m = MB()
    L, D = length, depth
    m.box(-L / 2 + 3, L / 2 - 3, -D / 2 + 3, D / 2 - 3, 0, 4, legs)
    m.box(-L / 2, L / 2, -D / 2, D / 2, 4, 12, cover, bevel=1.0)
    aw = 6 if arms else 0
    if arms:
        for s in (-1, 1):
            x0 = s * L / 2 - (aw if s > 0 else 0)
            m.box(x0, x0 + aw, -D / 2, D / 2, 4, 24, cover, bevel=1.6, segs=3)
    if back:
        m.box(-L / 2 + aw, L / 2 - aw, D / 2 - 8, D / 2, 12, 22, cover, bevel=1.2)
    n = seats or max(1, round((L - 2 * aw) / 30))
    w = (L - 2 * aw) / n
    for i in range(n):
        x0 = -L / 2 + aw + i * w
        m.box(x0 + 0.3, x0 + w - 0.3, -D / 2 + 0.5, D / 2 - (8 if back else 0.5), 12, 17.5, cover, bevel=2.2, segs=3)
        if back:
            m.box(x0 + 0.3, x0 + w - 0.3, D / 2 - 13, D / 2 - 7.6, 17.5, 31, cover, bevel=2.4, segs=3)
    return m


def lounge_chair(cover='fab_green', legs='oak'):
    """Compact lounge armchair (tub form)."""
    m = MB()
    for x in (-11, 11):
        for y in (-10, 11):
            m.cyl(x, y, 0.9, 0, 7, legs, segs=12, r2=0.7)
    m.box(-14, 14, -13, 14, 7, 15, cover, bevel=1.5, segs=3)
    m.box(-14, 14, 8, 14, 15, 30, cover, bevel=2.2, segs=3)
    for s in (-1, 1):
        m.box(s * 14 - (5 if s > 0 else 0), s * 14 + (0 if s > 0 else 5), -12, 13, 15, 24, cover, bevel=2.0, segs=3)
    m.box(-9, 9, -12.5, 8, 15, 19, cover, bevel=2.0, segs=3)
    return m


# ===================================================================================== tables & desks
def table(w, d, h=29.5, top='oak', base='metal_black', kind='legs', thick=1.2, radius=0.0, edge=None):
    """Rectangular or rounded table. kind: legs | sled | pedestal | panel."""
    m = MB()
    if radius > 0:
        m.prism(rounded_rect(-w / 2, w / 2, -d / 2, d / 2, radius, 8), h - thick, h, top, bevel=0.25)
    else:
        m.box(-w / 2, w / 2, -d / 2, d / 2, h - thick, h, top, bevel=0.2)
    if kind == 'legs':
        for x in (-w / 2 + 3, w / 2 - 3):
            for y in (-d / 2 + 3, d / 2 - 3):
                m.box(x - 0.9, x + 0.9, y - 0.9, y + 0.9, 0, h - thick, base, bevel=0.15)
        m.box(-w / 2 + 3, w / 2 - 3, d / 2 - 3.6, d / 2 - 2.4, h - thick - 3, h - thick, base)
        m.box(-w / 2 + 3, w / 2 - 3, -d / 2 + 2.4, -d / 2 + 3.6, h - thick - 3, h - thick, base)
    elif kind == 'sled':
        for x in (-w / 2 + 6, w / 2 - 6):
            m.box(x - 0.8, x + 0.8, -d / 2 + 4, d / 2 - 4, 0, 1.2, base)
            m.box(x - 0.8, x + 0.8, -d / 2 + 4, d / 2 - 4, h - thick - 1.2, h - thick, base)
            for y in (-d / 2 + 4, d / 2 - 4):
                m.box(x - 0.8, x + 0.8, y - 0.8, y + 0.8, 0, h - thick, base)
        m.box(-w / 2 + 6, w / 2 - 6, -0.6, 0.6, h - thick - 4, h - thick, base)
    elif kind == 'pedestal':
        n = max(1, int(w // 90))
        for i in range(n):
            x = -w / 2 + w * (i + 0.5) / n
            m.box(x - 9, x + 9, -6, 6, 1.5, h - thick, base, bevel=0.8)
            m.box(x - 15, x + 15, -10, 10, 0, 1.5, base, bevel=0.4)
    elif kind == 'panel':
        for x in (-w / 2 + 1.5, w / 2 - 1.5):
            m.box(x - 1.2, x + 1.2, -d / 2 + 2, d / 2 - 2, 0, h - thick, top, bevel=0.2)
        m.box(-w / 2 + 2.7, w / 2 - 2.7, -0.5, 0.5, 8, h - thick, top)
    elif kind == 'round':
        m.cyl(0, 0, 1.6, 1, h - thick, base, segs=16)
        m.cyl(0, 0, 9, 0, 1, base, segs=32)
    if edge:
        m.box(-w / 2, w / 2, -d / 2 - 0.05, -d / 2 + 0.25, h - thick, h, edge)
    return m


def round_table(dia, h=29.5, top='oak', base='metal_black'):
    m = MB()
    m.cyl(0, 0, dia / 2, h - 1.2, h, top, segs=48)
    m.cyl(0, 0, 1.5, 1, h - 1.2, base, segs=16)
    m.cyl(0, 0, min(10, dia / 3), 0, 1, base, segs=40)
    return m


def monitor(w=21.5, h=12.8, mat='screen_off'):
    """24 in class monitor on a stand (front faces -Y)."""
    m = MB()
    m.box(-4, 4, -3, 3, 0, 0.5, 'plastic_dark', bevel=0.2)
    m.box(-0.8, 0.8, 1.2, 2.2, 0.5, 9, 'plastic_dark', bevel=0.3)
    m.box(-w / 2, w / 2, -0.3, 0.6, 5, 5 + h, 'plastic_dark', bevel=0.15)
    m.box(-w / 2 + 0.25, w / 2 - 0.25, -0.35, -0.3, 5.3, 5 + h - 0.25, mat)
    return m


def bench_desk(n=3, w=55, d=27.5, top='plastic_white', edge='oak', screen='felt_green', screens=('screen_ui',),
               with_ped=True, h=29.5):
    """Back-to-back bench: n desks per side (front row faces -Y, back row faces +Y), centre acoustic screen,
    monitors, keyboards, mobile pedestals, cable tray. Footprint: n*w x 2*d."""
    m = MB()
    L = n * w
    m.box(-L / 2, L / 2, -d, d, h - 1, h, top, bevel=0.15)
    m.box(-L / 2, L / 2, -d - 0.05, -d + 0.25, h - 1, h, edge)
    m.box(-L / 2, L / 2, d - 0.25, d + 0.05, h - 1, h, edge)
    for k in range(n + 1):                                   # loop legs
        x = -L / 2 + k * w
        x = min(max(x, -L / 2 + 1), L / 2 - 1)
        for y0, y1 in ((-d + 2, -d + 3.6), (d - 3.6, d - 2)):
            m.box(x - 0.8, x + 0.8, y0, y1, 0, h - 1, 'metal_black')
        m.box(x - 0.8, x + 0.8, -d + 2, d - 2, 0, 1.2, 'metal_black')
        m.box(x - 0.8, x + 0.8, -d + 2, d - 2, h - 2.6, h - 1, 'metal_black')
    m.box(-L / 2 + 2, L / 2 - 2, -3, 3, h - 6, h - 4.5, 'metal_black')               # cable tray
    m.box(-L / 2 + 0.5, L / 2 - 0.5, -0.6, 0.6, h, h + 16, screen, bevel=0.4)       # 400 mm screen
    rnd = random.Random(n * 7 + int(w))
    for side in (-1, 1):
        for k in range(n):
            cx = -L / 2 + w * (k + 0.5)
            mon = monitor(mat=screens[(k + (side > 0)) % len(screens)])
            yb = side * 10.5
            m.add(mon, cx, yb, h, rot=math.pi if side > 0 else 0)
            ky = side * 20
            m.box(cx - 8.5, cx + 8.5, ky - 3, ky + 3, h, h + 0.7, 'plastic_dark', bevel=0.25)   # keyboard
            m.box(cx + 11, cx + 13.5, ky - 2, ky + 2, h, h + 0.9, 'plastic_dark', bevel=0.4)    # mouse
            if rnd.random() < 0.5:
                m.box(cx - 18, cx - 10, side * 18 - 5.5, side * 18 + 5.5, h, h + 0.6, 'paper')  # papers
            if with_ped:
                px = cx + w / 2 - 10
                m.box(px - 8, px + 8, side * 4, side * 24, 1, 25, 'plastic_white', bevel=0.3)
                for z in (8.5, 17):
                    m.box(px - 7.6, px + 7.6, side * 24 - 0.05 * side, side * 24 + 0.15 * side, z - 0.15, z + 0.15, 'plastic_dark')
    return m


def single_desk(w=63, d=31.5, h=29.5, top='oak', base='metal_black', mons=1, screen='screen_ui', ped=True, lamp=False):
    m = table(w, d, h, top=top, base=base, kind='panel' if base == top else 'legs')
    for i in range(mons):
        off = 0 if mons == 1 else (-11.5 if i == 0 else 11.5)
        m.add(monitor(mat=screen), off, d / 2 - 8, h)
    m.box(-8.5, 8.5, -d / 2 + 6, -d / 2 + 12, h, h + 0.7, 'plastic_dark', bevel=0.25)
    m.box(11, 13.5, -d / 2 + 7, -d / 2 + 11, h, h + 0.9, 'plastic_dark', bevel=0.4)
    if ped:
        m.box(w / 2 - 19, w / 2 - 3, -d / 2 + 4, d / 2 - 4, 1, 25, 'plastic_white', bevel=0.3)
    return m


def exec_desk(w=78, d=36, top='walnut', h=29.5):
    """Executive desk: floating walnut top on a side panel + leather-lined drawer pedestal, modesty panel."""
    m = MB()
    m.box(-w / 2, w / 2, -d / 2, d / 2, h - 1.6, h, top, bevel=0.3)
    m.box(-w / 2 + 2, -w / 2 + 3.8, -d / 2 + 2, d / 2 - 2, 0, h - 1.6, top, bevel=0.3)
    m.box(w / 2 - 22, w / 2 - 2, -d / 2 + 4, d / 2 - 2, 0, h - 1.6, top, bevel=0.3)
    m.box(w / 2 - 21.5, w / 2 - 2.5, -d / 2 + 3.9, -d / 2 + 4.1, 1, h - 2, 'leather_cognac')
    for z in (10, 19):
        m.box(w / 2 - 21.5, w / 2 - 2.5, -d / 2 + 3.7, -d / 2 + 3.9, z - 0.2, z + 0.2, 'brass')
    m.box(-w / 2 + 3.8, w / 2 - 22, d / 2 - 7, d / 2 - 6, 8, h - 1.6, top)        # modesty panel (visitor side)
    m.box(-w / 2 + 12, -w / 2 + 36, -d / 2 + 4, -d / 2 + 16, h, h + 0.15, 'leather_cognac')   # writing pad (user side)
    m.add(monitor(w=27, h=15.5, mat='screen_ui'), 6, d / 2 - 9, h)
    m.box(-12, 4, -d / 2 + 4, -d / 2 + 6.5, h, h + 0.6, 'plastic_dark', bevel=0.3)       # closed laptop/folio
    m.cyl(-w / 2 + 6, -d / 2 + 6, 2.2, h, h + 4, 'brass', segs=20, r2=2.0)              # pen cup
    return m


def boardroom_table(L=240, D=54, h=29.5):
    m = MB()
    pts = []
    # boat shape: straight centre, elliptical ends
    seg = 18
    straight = L - D
    for k in range(seg + 1):
        a = -math.pi / 2 + math.pi * k / seg
        pts.append((straight / 2 + D / 2 * math.cos(a) * 1.0, D / 2 * math.sin(a) * (0.86 + 0.14 * math.cos(a))))
    for k in range(seg + 1):
        a = math.pi / 2 + math.pi * k / seg
        pts.append((-straight / 2 + D / 2 * math.cos(a) * 1.0, D / 2 * math.sin(a) * (0.86 + 0.14 * abs(math.cos(a)))))
    m.prism(pts, h - 1.8, h, 'walnut', bevel=0.35)
    m.box(-straight / 2 + 10, straight / 2 - 10, -2.5, 2.5, h - 0.02, h + 0.05, 'alu_black')     # power/data trough lid
    for x in (-L * 0.28, L * 0.28):
        m.box(x - 14, x + 14, -9, 9, 0, 1.2, 'metal_black', bevel=0.3)
        m.box(x - 10, x + 10, -5, 5, 1.2, h - 1.8, 'walnut', bevel=0.6)
        m.box(x - 10.1, x + 10.1, -5.1, 5.1, 1.2, 3.2, 'brass')
    return m


def reception_desk(L=120, D=30):
    """Reception counter: fluted white-oak front, terrazzo transaction top with brass trim, lower
    (accessible, 760 mm) segment at one end, work surface behind. Front faces -Y."""
    m = MB()
    m.box(-L / 2, L / 2, -D / 2 + 2, D / 2, 0, 3.5, 'plinth')                           # recessed plinth
    # fluted front (half-round flutes)
    flute_r = 1.1
    n = int((L - 2) / (2 * flute_r))
    m.box(-L / 2, L / 2, -D / 2 + 1.0, -D / 2 + 3.0, 3.5, 40.5, 'oak')
    for i in range(n):
        x = -L / 2 + 1 + flute_r + i * 2 * flute_r
        m.cyl(x, -D / 2 + 1.1, flute_r, 3.5, 40.5, 'oak', segs=10)
    for s in (-1, 1):
        m.box(s * L / 2 - (2 if s > 0 else 0), s * L / 2 + (0 if s > 0 else 2), -D / 2 + 1, D / 2, 3.5, 40.5, 'oak', bevel=0.3)
    m.box(-L / 2 - 1, L / 2 + 1, -D / 2 - 1.5, -D / 2 + 11, 40.5, 42, 'terrazzo_counter', bevel=0.25)   # transaction ledge
    m.box(-L / 2 - 1, L / 2 + 1, -D / 2 - 1.55, -D / 2 - 1.3, 40.6, 41.9, 'brass')
    m.box(-L / 2 + 2, L / 2 - 2, -D / 2 + 11, D / 2, 28.5, 29.7, 'plastic_white', bevel=0.2)          # work surface
    m.box(-L / 2 + 2, -L / 2 + 34, -D / 2 - 6, -D / 2 + 1, 0, 29.7, 'oak', bevel=0.3)                 # accessible low part
    m.box(-L / 2 + 1, -L / 2 + 35, -D / 2 - 7, -D / 2 + 1, 29.7, 31, 'terrazzo_counter', bevel=0.2)
    m.box(-L / 2 + 2, L / 2 - 2, -D / 2 + 3, -D / 2 + 3.4, 39.6, 40.4, 'led_soft')                   # under-ledge glow
    m.add(monitor(w=21.5, h=12.8, mat='screen_ui'), 18, -D / 2 + 17, 29.7, rot=math.pi)
    m.add(monitor(w=21.5, h=12.8, mat='screen_ui'), -10, -D / 2 + 17, 29.7, rot=math.pi)
    return m


# ===================================================================================== storage
def cabinet(w, d, h, body='plastic_white', front='oak', doors=2, plinth=True, top=None, pulls='alu_black'):
    m = MB()
    z0 = 3 if plinth else 0
    if plinth:
        m.box(-w / 2 + 1, w / 2 - 1, -d / 2 + 2, d / 2 - 1, 0, 3, 'plinth')
    m.box(-w / 2, w / 2, -d / 2 + 0.8, d / 2, z0, h, body, bevel=0.15)
    gap = 0.12
    for i in range(doors):
        x0 = -w / 2 + w * i / doors + gap
        x1 = -w / 2 + w * (i + 1) / doors - gap
        m.box(x0, x1, -d / 2, -d / 2 + 0.8, z0 + gap, h - gap, front, bevel=0.1)
        px = x1 - 1.5 if i % 2 == 0 else x0 + 1.5
        if pulls:
            m.box(px - 0.3, px + 0.3, -d / 2 - 0.9, -d / 2, z0 + (h - z0) * 0.55, z0 + (h - z0) * 0.55 + min(12, h * 0.25), pulls)
    if top:
        m.box(-w / 2 - 0.3, w / 2 + 0.3, -d / 2 - 0.3, d / 2, h, h + 1, top, bevel=0.2)
    return m


def shelving(w, d, h, mat='oak', shelves=5, books=True, seed=1, back=None, mix=('g_white', 'g_heather', 'g_sand', 'g_navy', 'paper', 'g_olive')):
    """Open shelving with procedural books/binders (muted colours, no readable text)."""
    m = MB()
    rnd = random.Random(seed)
    t = 1.0
    for x in (-w / 2, w / 2 - t):
        m.box(x, x + t, -d / 2, d / 2, 0, h, mat, bevel=0.1)
    nb = max(1, round(w / 36))
    for i in range(1, nb):
        x = -w / 2 + w * i / nb
        m.box(x - t / 2, x + t / 2, -d / 2, d / 2, 0, h, mat)
    for j in range(shelves + 1):
        z = 3 + (h - 3 - t) * j / shelves
        m.box(-w / 2, w / 2, -d / 2, d / 2, z, z + t, mat, bevel=0.1)
    if back:
        m.box(-w / 2, w / 2, d / 2 - 0.4, d / 2, 0, h, back)
    if books:
        for j in range(shelves):
            z = 3 + (h - 3 - t) * j / shelves + t
            zz = 3 + (h - 3 - t) * (j + 1) / shelves
            x = -w / 2 + t + 0.5
            while x < w / 2 - 4:
                if rnd.random() < 0.18:
                    x += rnd.uniform(4, 10)
                    if rnd.random() < 0.3:
                        m.cyl(x, 0, 2.3, z, z + rnd.uniform(5, 8), 'ceramic_white', segs=14, r2=1.6)
                        x += 5
                    continue
                bw = rnd.uniform(0.8, 2.2)
                bh = min(zz - z - 0.6, rnd.uniform(7.5, 11.5))
                bd = rnd.uniform(6.5, min(10, d - 1))
                m.box(x, x + bw, -bd / 2, bd / 2, z, z + bh, rnd.choice(mix), bevel=0.1)
                x += bw + 0.05
    return m


def lockers(n=6, w=15, d=18, h=44):
    m = MB()
    m.box(-n * w / 2, n * w / 2, -d / 2 + 0.8, d / 2, 0, h, 'plastic_white')
    for i in range(n):
        x0 = -n * w / 2 + i * w + 0.1
        m.box(x0, x0 + w - 0.2, -d / 2, -d / 2 + 0.8, 3, h - 0.2, 'oak' if i % 3 else 'plastic_white', bevel=0.1)
        m.box(x0 + w - 2.2, x0 + w - 1.6, -d / 2 - 0.6, -d / 2, h * 0.55, h * 0.55 + 5, 'alu_black')
    m.box(-n * w / 2, n * w / 2, -d / 2 + 1, d / 2, 0, 3, 'plinth')
    return m


# ===================================================================================== soft goods / decor
def rug(w, d, mat='fab_grey', t=0.4):
    m = MB()
    m.box(-w / 2, w / 2, -d / 2, d / 2, 0, t, mat, bevel=0.15)
    return m


def planter(r=9, h=18, mat='ceramic_white', soil=True):
    m = MB()
    m.lathe([(r * 0.82, 0), (r * 0.9, 0.6), (r, h * 0.85), (r, h), (r - 0.6, h)], mat, segs=32, close_top=False)
    if soil:
        m.cyl(0, 0, r - 0.6, h - 1.5, h - 1.2, 'soil', segs=24)
    return m


def garment_tee(mat, w=19, L=27, t=1.3):
    """Flat garment silhouette (front view) for hanging displays: body + short sleeves."""
    m = MB()
    pts = [(-w / 2, 0), (w / 2, 0), (w / 2, L - 12), (w / 2 + 2.5, L - 12.5), (w / 2 + 2.0, L - 1.5), (w / 2 - 1, L + 0.3),
           (3.5, L + 0.4), (0, L - 2), (-3.5, L + 0.4), (-w / 2 + 1, L + 0.3), (-w / 2 - 2.0, L - 1.5), (-w / 2 - 2.5, L - 12.5),
           (-w / 2, L - 12)]
    m.prism(pts, -t / 2, t / 2, mat, smooth=True, bevel=0.3)
    return m


def hanging_garment(mat, kind='tee', length=27, seed=0):
    """Garment on a hanger, hanger hook at z = 0 (top of the rail), body hangs below, faces -Y."""
    m = MB()
    g = garment_tee(mat, w=18 if kind == 'tee' else 20, L=length)
    # rotate silhouette from XY plane to XZ plane (stand up), hang below the rail
    import mathutils
    rot = mathutils.Matrix.Rotation(math.radians(90), 4, 'X')
    _transform(g, rot, (0, 0, -length - 3))
    m.add(g)
    m.rod((0, 0, -1.2), (0, 0, 0.8), 0.12, 'chrome', segs=6)
    m.rod((-8.5, 0, -3.3), (0, 0, -1.2), 0.25, 'oak', segs=6)
    m.rod((8.5, 0, -3.3), (0, 0, -1.2), 0.25, 'oak', segs=6)
    return m


def dress_form(cover='mannequin', stand='brass', h_top=64):
    """Dress form torso on a pole and round base (lathed, elliptical section)."""
    m = MB()
    torso = MB()
    prof = [(0.1, 0), (5.5, 0.4), (6.6, 2.5), (6.9, 5), (6.2, 9), (5.2, 12.5), (5.6, 15.5), (6.6, 19), (6.8, 21), (6.0, 23.5),
            (3.2, 25.2), (1.8, 26.2), (1.8, 28.5), (0.1, 28.6)]
    torso.lathe(prof, cover, segs=28)
    import mathutils
    _transform(torso, mathutils.Matrix.Diagonal((1.05, 0.72, 1.0, 1.0)), (0, 0, h_top - 28.6))
    m.add(torso)
    m.cyl(0, 0, 0.55, 3, h_top - 28.4, stand, segs=12)
    m.cyl(0, 0, 7.5, 0, 1.0, stand, segs=36)
    m.cyl(0, 0, 1.6, h_top - 0.2, h_top + 1.2, 'oak', segs=16)
    return m


def mannequin_garment(cover_mat, body='mannequin'):
    """Dress form wearing a garment: the garment is a slightly larger shell over the torso."""
    m = dress_form(body, 'metal_black', 64)
    shell = MB()
    prof = [(7.4, 0), (7.2, 3), (6.6, 8), (6.1, 12.5), (6.4, 15.5), (7.3, 19), (7.4, 21), (6.6, 23.5), (3.8, 25.4), (2.6, 26)]
    shell.lathe(prof, cover_mat, segs=28, close_top=False, close_bottom=False)
    import mathutils
    _transform(shell, mathutils.Matrix.Diagonal((1.07, 0.76, 1.0, 1.0)), (0, 0, 64 - 28.6 - 6))
    m.add(shell)
    return m


def garment_rail_bay(width=96, depth=24, h=96, back='paint_green', seed=1, n=None):
    """Wall display bay: oak frame, coloured back panel, top shelf with folded stacks, rail with garments,
    LED strip under the top shelf. Front faces -Y, back against the wall at y = +depth/2."""
    m = MB()
    rnd = random.Random(seed)
    W2, D2 = width / 2, depth / 2
    m.box(-W2, W2, D2 - 0.75, D2, 0, h, back)
    for x in (-W2, W2 - 1.5):
        m.box(x, x + 1.5, -D2, D2, 0, h, 'oak', bevel=0.15)
    m.box(-W2, W2, -D2, D2, h - 1.5, h, 'oak', bevel=0.15)
    m.box(-W2, W2, -D2, D2, 0, 4, 'oak', bevel=0.15)
    m.box(-W2 + 1.5, W2 - 1.5, -D2 + 1, D2, 72, 73.2, 'oak', bevel=0.1)            # display shelf
    m.box(-W2 + 1.5, W2 - 1.5, -D2 + 2, -D2 + 2.6, 71.4, 72, 'led_3500')            # LED under shelf
    m.rod((-W2 + 1.5, 0, 66), (W2 - 1.5, 0, 66), 0.5, 'brass', segs=12)             # hanging rail
    palette = ['g_navy', 'g_white', 'g_heather', 'g_olive', 'g_sand', 'g_black', 'g_denim', 'g_rust', 'g_sage', 'g_blush', 'g_green']
    k = n or int((width - 10) // 6.5)
    x = -W2 + 6
    base = rnd.randrange(len(palette))
    for i in range(k):
        mat = palette[(base + i // 3) % len(palette)]
        g = hanging_garment(mat, length=rnd.choice((24, 26, 28)), kind=rnd.choice(('tee', 'shirt')))
        m.add(g, x, rnd.uniform(-0.6, 0.6), 66.3, rot=math.radians(90 + rnd.uniform(-6, 6)))
        x += (width - 12) / k
    # folded stacks on the shelf
    for sx in (-W2 / 2, 0, W2 / 2):
        z = 73.2
        for j in range(rnd.randint(3, 5)):
            m.box(sx - 6, sx + 6, -D2 + 3, -D2 + 12, z, z + 1.6, rnd.choice(palette), bevel=0.4)
            z += 1.6
    return m


def plinth_display(w=120, d=48, h=8, top='terrazzo_counter'):
    m = MB()
    m.prism(rounded_rect(-w / 2, w / 2, -d / 2, d / 2, 10, 8), 0, h - 1, 'oak', bevel=0.3)
    m.prism(rounded_rect(-w / 2 + 0.5, w / 2 - 0.5, -d / 2 + 0.5, d / 2 - 0.5, 9.5, 8), h - 1, h, top, bevel=0.2)
    m.prism(rounded_rect(-w / 2 + 2, w / 2 - 2, -d / 2 + 2, d / 2 - 2, 8, 8), 0, 0.6, 'led_soft')
    return m


def material_table(w=144, d=40, h=34, seed=3):
    """Touch-and-feel table: yarn cones -> fabric swatches -> folded garments (the knit story)."""
    m = table(w, d, h, top='oak', base='metal_black', kind='sled', thick=1.6)
    rnd = random.Random(seed)
    palette = ['g_navy', 'g_white', 'g_heather', 'g_olive', 'g_sand', 'g_rust', 'g_sage', 'g_blush', 'g_green', 'g_denim']
    # yarn cones (left third)
    for i in range(10):
        x = -w / 2 + 8 + (i % 5) * 8
        y = -8 + (i // 5) * 12
        col = palette[i % len(palette)]
        m.lathe([(0.6, h), (2.6, h + 0.3), (2.0, h + 6.5), (0.6, h + 6.8)], col, segs=16)
        _shift_last(m, x, y)
    # fabric swatches fanned (middle)
    for i in range(8):
        x = -10 + i * 3.2
        m.box(x - 6, x + 6, -12, 4, h + 0.2 + i * 0.12, h + 0.32 + i * 0.12, palette[(i + 2) % len(palette)], rot=math.radians(-8 + i * 2))
    # folded garments (right third)
    for j, sx in enumerate((w / 2 - 34, w / 2 - 16)):
        z = h
        for k in range(4):
            m.box(sx - 7, sx + 7, -6, 6, z, z + 1.8, palette[(j * 4 + k) % len(palette)], bevel=0.5)
            z += 1.8
    return m


def _shift_last(m, dx, dy):
    """Move the most recently added geometry block (lathe) by dx, dy."""
    m.bm.verts.ensure_lookup_table()
    n = 16 * 4
    for v in m.bm.verts[-n:]:
        v.co.x += dx
        v.co.y += dy


def light_booth(w=32, d=22, h=26):
    """Colour assessment cabinet (D65 viewing booth) on a counter."""
    m = MB()
    m.box(-w / 2, w / 2, -d / 2, d / 2, 0, 1, 'plastic_dark')
    m.box(-w / 2, -w / 2 + 1, -d / 2, d / 2, 0, h, 'plastic_dark')
    m.box(w / 2 - 1, w / 2, -d / 2, d / 2, 0, h, 'plastic_dark')
    m.box(-w / 2, w / 2, d / 2 - 1, d / 2, 0, h, 'paint_warmgrey')
    m.box(-w / 2, w / 2, -d / 2, d / 2, h - 1.5, h, 'plastic_dark')
    m.box(-w / 2 + 1, w / 2 - 1, -d / 2 + 2, d / 2 - 2, h - 1.8, h - 1.5, 'lightbox')
    m.box(-w / 2, w / 2, -d / 2, -d / 2 + 1, h - 4, h, 'plastic_dark')
    return m


def sewing_station():
    """Sample-room industrial lockstitch machine on its table (office-grade sample studio)."""
    m = table(48, 20, 30, top='plastic_white', base='metal_black', kind='legs', thick=1.4)
    m.box(-8, 12, -3, 3, 30, 32.5, 'plastic_white', bevel=0.6)
    m.box(8, 12, -3, 3, 32.5, 43, 'plastic_white', bevel=0.8)
    m.box(-9, 12, -2.5, 2.5, 41, 44.5, 'plastic_white', bevel=0.9)
    m.box(-9, -6, -2, 2, 35, 41, 'plastic_white', bevel=0.5)
    m.cyl(13, 0, 2.8, 37, 37 + 0.01, 'metal_black', segs=16)
    m.box(-2, 6, -9, -4, 7, 13, 'plastic_dark', bevel=0.5)         # motor under table
    m.cyl(-14, 4, 0.2, 30, 46, 'alu_silver', segs=6)              # thread stand
    for i, c in enumerate(('g_navy', 'g_white', 'g_rust')):
        m.cyl(-14 + (i - 1) * 2.5, 4, 0.9, 30, 33, c, segs=10)
    m.box(-1.5, 3.5, -22, -14, 2, 3, 'metal_black')                 # pedal
    return m


def printer_3d(w=20, d=20, h=22):
    m = MB()
    m.box(-w / 2, w / 2, -d / 2, d / 2, 0, 3, 'plastic_dark', bevel=0.4)
    m.box(-w / 2, w / 2, -d / 2, d / 2, h - 3, h, 'plastic_dark', bevel=0.4)
    for x in (-w / 2, w / 2 - 1):
        for y in (-d / 2, d / 2 - 1):
            m.box(x, x + 1, y, y + 1, 3, h - 3, 'alu_black')
    m.box(-w / 2 + 0.6, w / 2 - 0.6, -d / 2 + 0.3, -d / 2 + 0.5, 3, h - 3, 'glass_clear')
    m.box(-w / 2 + 3, w / 2 - 3, -d / 2 + 3, d / 2 - 3, 6, 6.6, 'alu_silver')
    m.box(-2, 2, -2, 2, 12, 15, 'plastic_white', bevel=0.4)
    m.box(-3, 3, -2, 2, 6.6, 9, 'g_green', bevel=0.6)               # part being printed
    m.box(-w / 2 + 2, -w / 2 + 7, -d / 2 - 0.05, -d / 2 + 0.2, 0.6, 2.4, 'screen_ui')
    return m


def plotter(w=62, d=26, h=44):
    m = MB()
    for x in (-w / 2 + 4, w / 2 - 4):
        m.box(x - 1, x + 1, -6, 6, 0, h - 12, 'metal_black')
        m.box(x - 1, x + 1, -10, 10, 0, 1.5, 'metal_black')
    m.box(-w / 2 + 4, w / 2 - 4, -0.6, 0.6, 10, 12, 'metal_black')
    m.box(-w / 2, w / 2, -d / 2, d / 2, h - 12, h, 'plastic_dark', bevel=1.2)
    m.box(-w / 2 + 3, w / 2 - 3, -d / 2 - 0.1, -d / 2 + 0.4, h - 10, h - 9, 'paper')
    m.box(w / 2 - 8, w / 2 - 3, -d / 2 - 0.05, -d / 2 + 0.3, h - 5, h - 2, 'screen_ui')
    return m


def steam_station(w=50, d=18):
    m = table(w, d, 34, top='fab_grey', base='metal_black', kind='legs', thick=2)
    m.box(-w / 2 + 2, -w / 2 + 14, -d / 2 + 2, d / 2 - 2, 2, 20, 'plastic_white', bevel=0.8)    # boiler
    m.box(6, 15, -3, 3, 34, 36.5, 'plastic_white', bevel=0.8)                                    # iron
    return m


def wc_pan():
    """Wall-hung WC with concealed cistern panel (rear at +Y)."""
    m = MB()
    m.box(-9, 9, 9, 13, 0, 44, 'porcelain', bevel=0.3)                       # in-wall frame panel face
    m.box(-3, 3, 9.9, 10.1, 38, 42, 'chrome')                               # flush plate
    m.prism(ellipse(0, -5, 7, 10.5, 32), 9, 15.8, 'porcelain', smooth=True, bevel=1.2)
    m.box(-7, 7, 2, 9, 9, 15.8, 'porcelain', bevel=1.2)
    m.prism(ellipse(0, -5, 7.2, 10.7, 32), 15.8, 16.6, 'plastic_white', smooth=True, bevel=0.3)
    return m


def urinal():
    m = MB()
    m.box(-7, 7, 4, 13, 22, 44, 'porcelain', bevel=2.0, segs=3)
    m.box(-5.5, 5.5, 3, 12, 22, 24, 'porcelain', bevel=0.8)
    return m


def vanity(L=60, D=21, basins=2):
    m = MB()
    m.box(-L / 2, L / 2, -D / 2, D / 2, 30, 32, 'terrazzo_counter', bevel=0.2)
    m.box(-L / 2 + 1, L / 2 - 1, -D / 2 + 1, D / 2, 16, 30, 'oak', bevel=0.2)
    for i in range(basins):
        x = -L / 2 + L * (i + 0.5) / basins
        m.lathe([(5.5, 32), (7.2, 34.5), (7.6, 37), (7.0, 37), (5.2, 34.8)], 'porcelain', segs=32, close_top=False)
        _shift_last_n(m, 32 * 5, x, -1)
        m.rod((x, D / 2 - 2, 32), (x, D / 2 - 2, 42), 0.6, 'chrome', segs=10)
        m.rod((x, D / 2 - 2, 42), (x, D / 2 - 7, 42), 0.5, 'chrome', segs=10)
    m.box(-L / 2, L / 2, D / 2 - 0.3, D / 2 + 0.1, 42, 78, 'mirror')
    m.box(-L / 2, L / 2, D / 2 - 1.2, D / 2 - 0.3, 78, 79, 'led_4000')
    return m


def _shift_last_n(m, n, dx, dy):
    m.bm.verts.ensure_lookup_table()
    for v in m.bm.verts[-n:]:
        v.co.x += dx
        v.co.y += dy


def cubicle(w=36, d=60, h=78, door=True):
    """Compact-laminate WC cubicle side walls + door (front faces -Y)."""
    m = MB()
    for x in (-w / 2, w / 2 - 0.5):
        m.box(x, x + 0.5, -d / 2, d / 2, 6, h, 'plastic_white')
        m.box(x - 0.2, x + 0.7, -d / 2 + 1, -d / 2 + 2, 0, 6, 'chrome')
    if door:
        m.box(-w / 2 + 0.6, w / 2 - 0.6, -d / 2, -d / 2 + 0.5, 6, h, 'oak')
        m.box(w / 2 - 4, w / 2 - 3, -d / 2 - 0.8, -d / 2, 38, 40, 'chrome')
    m.box(-w / 2, w / 2, -d / 2, d / 2, h, h + 1.2, 'alu_silver')
    return m


def wudu_station(L=96, n=4):
    """Wudu (ablution) bench: fixed stools, low trough, wall taps."""
    m = MB()
    m.box(-L / 2, L / 2, 6, 18, 0, 6, 'terrazzo_counter', bevel=0.3)             # trough base
    m.box(-L / 2, L / 2, 8, 18, 6, 8, 'porcelain')
    m.box(-L / 2, L / 2, 16, 18, 8, 34, 'wall_porcelain')
    for i in range(n):
        x = -L / 2 + L * (i + 0.5) / n
        m.cyl(x, -6, 5.5, 0, 14, 'terrazzo_counter', segs=24)
        m.rod((x, 17.5, 30), (x, 13, 30), 0.45, 'chrome', segs=8)
    return m


def pantry_run(L=120, D=25):
    """Pantry counter: base cabinets, terrazzo top, sink, upper cabinets, small appliances. Back at +Y."""
    m = cabinet(L, D, 34.5, body='plastic_white', front='oak', doors=int(L // 18), top='terrazzo_counter')
    m.box(-12, 12, -D / 2 + 4, D / 2 - 4, 35, 35.3, 'alu_silver')
    m.rod((0, D / 2 - 3, 35.5), (0, D / 2 - 3, 48), 0.6, 'chrome', segs=10)
    m.rod((0, D / 2 - 3, 48), (0, D / 2 - 9, 48), 0.55, 'chrome', segs=10)
    up = cabinet(L, 13, 30, body='plastic_white', front='plastic_white', doors=int(L // 18), plinth=False, pulls=None)
    m.add(up, 0, D / 2 - 6.5, 54)
    m.box(-L / 2, L / 2, D / 2 - 13, D / 2 - 12.5, 53.6, 54, 'led_3500')         # under-cabinet light
    m.box(-L / 2, L / 2, D / 2 - 0.5, D / 2, 35.5, 54, 'stone_white')             # splashback
    m.box(L / 2 - 26, L / 2 - 6, -D / 2 + 5, D / 2 - 3, 35.5, 47, 'alu_black', bevel=0.8)   # microwave
    m.box(-L / 2 + 6, -L / 2 + 18, -D / 2 + 6, D / 2 - 4, 35.5, 52, 'metal_black', bevel=0.8)  # coffee machine
    return m


def fridge(w=30, d=28, h=70):
    m = MB()
    m.box(-w / 2, w / 2, -d / 2, d / 2, 0, h, 'alu_silver', bevel=0.8)
    m.box(-w / 2 + 0.2, w / 2 - 0.2, -d / 2 - 0.1, -d / 2 + 0.1, 46, 46.2, 'plastic_dark')
    m.box(-w / 2 + 2, -w / 2 + 2.8, -d / 2 - 1.5, -d / 2, 20, 44, 'chrome')
    return m


def water_dispenser():
    m = MB()
    m.box(-6.5, 6.5, -6.5, 6.5, 0, 38, 'plastic_white', bevel=0.8)
    m.cyl(0, 0, 5.2, 38, 54, 'glass_frosted', segs=24)
    m.box(-3, 3, -6.9, -6.5, 24, 30, 'plastic_dark')
    return m


def wall_screen(w=75, h=42, mat='screen_brand', depth=2.2):
    """Wall-mounted display (86 in class by default). Back at +Y (against the wall)."""
    m = MB()
    m.box(-w / 2, w / 2, -depth / 2, depth / 2, 0, h, 'plastic_dark', bevel=0.3)
    m.box(-w / 2 + 0.4, w / 2 - 0.4, -depth / 2 - 0.05, -depth / 2 + 0.05, 0.4, h - 0.4, mat)
    return m


def whiteboard(w=72, h=40):
    m = MB()
    m.box(-w / 2, w / 2, -0.5, 0.5, 0, h, 'alu_silver', bevel=0.2)
    m.box(-w / 2 + 0.6, w / 2 - 0.6, -0.55, -0.45, 0.6, h - 0.6, 'plastic_white')
    return m


def pinboard_wall(w, h, seed=5):
    """Linen-covered pinboard with mood-board swatches (plain colour cards, no imagery invented)."""
    m = MB()
    rnd = random.Random(seed)
    m.box(-w / 2, w / 2, -0.75, 0.75, 0, h, 'pinboard_linen', bevel=0.2)
    palette = ['g_navy', 'g_white', 'g_heather', 'g_olive', 'g_sand', 'g_rust', 'g_sage', 'g_blush', 'g_green', 'g_denim', 'paper', 'g_black']
    x = -w / 2 + 3
    while x < w / 2 - 10:
        col_w = rnd.uniform(7, 12)
        z = rnd.uniform(4, 9)
        while z < h - 10:
            ch = rnd.uniform(6, 11)
            m.box(x, x + col_w, -0.9, -0.75, z, z + ch, rnd.choice(palette))
            z += ch + rnd.uniform(1, 3)
        x += col_w + rnd.uniform(1.5, 4)
    return m


def fire_extinguisher():
    m = MB()
    m.cyl(0, 0, 3.0, 4, 22, 'g_rust', segs=20)
    m.sphere((0, 0, 22), 3.0, 'g_rust', segs=20, rings=8, sz=0.6)
    m.box(-0.8, 0.8, -0.8, 0.8, 23.5, 27, 'metal_black')
    m.box(-4, 4, 2.6, 4, 2, 26, 'metal_black')
    return m


def exit_sign():
    m = MB()
    m.box(-7, 7, -0.6, 0.6, 0, 6, 'plastic_white', bevel=0.2)
    m.box(-6, 6, -0.65, -0.6, 0.8, 5.2, 'fab_green')
    return m


# ===================================================================================== lighting fixtures (geometry)
def linear_pendant(L=72, drop=12, w=2.6, h=3.2, mat='alu_black', led='led_4000'):
    """Suspended linear LED profile; z = 0 is the BOTTOM of the luminaire, cables go up by `drop`."""
    m = MB()
    m.box(-L / 2, L / 2, -w / 2, w / 2, 0.3, h, mat, bevel=0.2)
    m.box(-L / 2 + 0.6, L / 2 - 0.6, -w / 2 + 0.3, w / 2 - 0.3, 0, 0.3, led)
    for x in (-L / 2 + 6, L / 2 - 6):
        m.cyl(x, 0, 0.06, h, h + drop, 'alu_silver', segs=6)
        m.cyl(x, 0, 1.4, h + drop - 0.4, h + drop, mat, segs=16)
    return m


def halo_pendant(r=24, drop=30, led='led_3000'):
    """Ring luminaire (brass) - z = 0 at the ring bottom."""
    m = MB()
    m.lathe([(r - 1.2, 0), (r + 1.2, 0), (r + 1.2, 1.8), (r - 1.2, 1.8)], 'brass', segs=64, close_bottom=False, close_top=False)
    m.lathe([(r - 1.0, -0.02), (r + 1.0, -0.02)], led, segs=64, close_bottom=False, close_top=False)
    for k in range(3):
        a = 2 * math.pi * k / 3
        m.cyl(r * math.cos(a), r * math.sin(a), 0.05, 1.8, drop, 'alu_silver', segs=6)
    m.cyl(0, 0, 3, drop - 0.6, drop, 'brass', segs=24)
    return m


def downlight(r=3.0, led='led_3500'):
    """Surface-mounted cylinder downlight; z = 0 at the bottom face."""
    m = MB()
    m.cyl(0, 0, r, 0, 6, 'alu_black', segs=24)
    m.cyl(0, 0, r - 0.5, -0.02, 0.4, led, segs=24)
    return m


def track_spot(h_body=5.5, led='led_3000'):
    m = MB()
    m.box(-0.8, 0.8, -0.8, 0.8, -2, 0, 'alu_black')
    m.cyl(0, 0, 1.6, -h_body - 2, -2, 'alu_black', segs=16)
    m.cyl(0, 0, 1.2, -h_body - 2.05, -h_body - 1.9, led, segs=16)
    return m


def track(L):
    m = MB()
    m.box(-L / 2, L / 2, -0.7, 0.7, -1.3, 0, 'alu_black')
    return m


def baffle(L=48, h=12, t=1.8, mat='felt_grey'):
    """Acoustic felt baffle, z = 0 at the bottom edge."""
    m = MB()
    m.box(-L / 2, L / 2, -t / 2, t / 2, 0, h, mat, bevel=0.3)
    return m


def raft(w, d, t=1.6, mat='felt_green'):
    m = MB()
    m.box(-w / 2, w / 2, -d / 2, d / 2, 0, t, mat, bevel=0.4)
    return m


def slat_raft(w, d, slat=1.6, gap=2.4, depth=3.0, mat='oak_slat'):
    """Suspended timber slat ceiling raft, slats run along x; z = 0 at the bottom."""
    m = MB()
    n = int(d // (slat + gap))
    y = -d / 2
    for i in range(n):
        m.box(-w / 2, w / 2, y, y + slat, 0, depth, mat, bevel=0.15)
        y += slat + gap
    m.box(-w / 2, w / 2, -d / 2, d / 2, depth, depth + 0.5, 'plinth')                # black acoustic backing
    return m


def ac_cassette(w=47, d=26, h=9.5):
    """Under-ceiling (ceiling-suspended) VRF indoor unit; z = 0 at its top (fixed to the deck)."""
    m = MB()
    m.box(-w / 2, w / 2, -d / 2, d / 2, -h, 0, 'plastic_white', bevel=1.2, segs=3)
    for i in range(6):
        y = -d / 2 + 1 + i * 0.7
        m.box(-w / 2 + 3, w / 2 - 3, y, y + 0.35, -h - 0.05, -h + 1.5, 'plastic_dark')
    return m


def smoke_detector():
    m = MB()
    m.cyl(0, 0, 2.4, -1.6, 0, 'plastic_white', segs=20)
    return m


# ===================================================================================== signage
def sign_panel(w, h, mat, depth=0.6, back='plastic_white'):
    """Flat sign: a back plate and a decal face with 0..1 UVs (for the client's logo images)."""
    import bmesh
    m = MB()
    if back:
        m.box(-w / 2, w / 2, 0, depth, 0, h, back, bevel=0.1)
    return m, (w, h)


def decal(name, coll, mat_obj, x, y, z, w, h, facing_deg, materials, plan_to_blender):
    """Create a vertical decal plane with UV 0..1 showing an image material (logo)."""
    me = bpy.data.meshes.new(name)
    hw = w / 2 * 0.0254
    hh = h * 0.0254
    verts = [(-hw, 0, 0), (hw, 0, 0), (hw, 0, hh), (-hw, 0, hh)]
    me.from_pydata(verts, [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new(name='UVMap')
    for i, lp in enumerate(me.loops):
        uv.data[i].uv = [(0, 0), (1, 0), (1, 1), (0, 1)][lp.vertex_index]
    me.materials.append(materials[mat_obj])
    ob = bpy.data.objects.new(name, me)
    loc = plan_to_blender(x, y, z)
    ob.location = loc
    ob.rotation_euler = (0, 0, math.radians(facing_deg))
    coll.objects.link(ob)
    return ob


# ===================================================================================== CC0 model import
def import_model(key, coll, objects=None, name=None):
    """Append objects from assets/models/<key>/<key>_1k.blend; returns the list of new objects.
    Texture paths are remapped to the JPG copies when the PNG was converted (size optimisation)."""
    path = os.path.join(MODELS, key, f'{key}_1k.blend')
    with bpy.data.libraries.load(path, link=False) as (src, dst):
        dst.objects = [o for o in src.objects if objects is None or o in objects]
    out = []
    for o in dst.objects:
        if o is None:
            continue
        coll.objects.link(o)
        out.append(o)
    for img in bpy.data.images:
        fp = bpy.path.abspath(img.filepath)
        if fp.endswith('.png') and not os.path.exists(fp) and os.path.exists(fp[:-4] + '.jpg'):
            img.filepath = fp[:-4] + '.jpg'
    return out


class Library:
    """Holds one hidden master copy of each CC0 model; place() makes linked duplicates."""

    def __init__(self, coll):
        self.coll = coll
        self.masters = {}

    def master(self, key, objects=None):
        k = (key, tuple(objects or ()))
        if k not in self.masters:
            obs = import_model(key, self.coll, objects)
            for o in obs:
                o.hide_render = True
                o.hide_viewport = True
            self.masters[k] = obs
        return self.masters[k]

    def place(self, key, coll, x_m, y_m, z_m=0.0, rot_deg=0.0, scale=1.0, objects=None, label=None):
        out = []
        masters = self.master(key, objects)
        # place so that the group's footprint centre sits at the target (masters are near the origin)
        for o in masters:
            if o.type not in ('MESH',):
                continue
            d = o.copy()          # linked duplicate (shares mesh data)
            d.hide_render = False
            d.hide_viewport = False
            d.location = (x_m + o.location.x * scale * math.cos(math.radians(rot_deg)) - o.location.y * scale * math.sin(math.radians(rot_deg)),
                          y_m + o.location.x * scale * math.sin(math.radians(rot_deg)) + o.location.y * scale * math.cos(math.radians(rot_deg)),
                          z_m + o.location.z * scale)
            d.rotation_euler = (o.rotation_euler.x, o.rotation_euler.y, o.rotation_euler.z + math.radians(rot_deg))
            d.scale = (o.scale.x * scale, o.scale.y * scale, o.scale.z * scale)
            d.parent = None
            if label:
                d.name = f'{label} ({o.name})'
            d['source'] = f'Poly Haven CC0: {key}'
            coll.objects.link(d)
            out.append(d)
        return out
