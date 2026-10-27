"""Blender builder: survey shell + office fit-out -> Final_Office_Interior.blend / .glb.

Run:  blender -b --factory-startup --python build_model.py -- OUT_DIR [--no-glb] [--shell-only]
"""
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bmesh  # noqa: E402
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

import lib_assets as A  # noqa: E402
import lib_materials as LM  # noqa: E402
import office_layout as O  # noqa: E402
import survey as S  # noqa: E402
from lib_mesh import IN, MB, place  # noqa: E402

ARGV = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = os.path.abspath(ARGV[0]) if ARGV and not ARGV[0].startswith("--") else os.getcwd()
SHELL_ONLY = "--shell-only" in ARGV
NO_GLB = "--no-glb" in ARGV
C = {}
MAT = {}
T0 = time.time()


def log(*a):
    print(f"[{time.time() - T0:7.1f}s]", *a, flush=True)


def coll(name, parent=None):
    c = bpy.data.collections.new(name)
    (parent or bpy.context.scene.collection).children.link(c)
    C[name] = c
    return c


def pb(x, y, z=0.0):
    return (x * IN, -y * IN, z * IN)


# ------------------------------------------------------------------------------------------ scene
def setup_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = "METRIC"
    sc.unit_settings.length_unit = "MILLIMETERS"
    MAT.update(LM.build_library())
    A.init(MAT)
    for m in ("led_3000", "led_3500", "led_4000", "led_soft", "lightbox", "screen_brand", "screen_ui"):
        try:
            MAT[m].cycles.emission_sampling = "NONE"     # fixtures glow; Blender lights do the lighting
        except Exception:
            pass
    for name in ("Structure", "Walls", "Doors_Windows", "Stairs", "Reception", "Experience_Center", "Workstations",
                 "Meeting_Rooms", "Executive_Area", "Design_Development", "Support_Rooms", "Prayer_Rooms", "Washrooms",
                 "Furniture", "Ceilings", "Lighting", "MEP_Fire_Safety", "Branding", "Plants", "Labels", "Dimensions", "Cameras"):
        coll(name)
    for sub, parent in (("Columns", "Structure"), ("Beams", "Structure"), ("Existing Walls", "Walls"),
                        ("Existing Partitions", "Walls"), ("New Partitions", "Walls"), ("Wall Finishes", "Walls"),
                        ("Doors", "Doors_Windows"), ("Windows", "Doors_Windows"), ("Door Leaves", "Doors_Windows"),
                        ("Light Fixtures", "Lighting"), ("Light Sources", "Lighting"), ("_CC0_Masters", None)):
        coll(sub, C[parent] if parent else None)
    C["_CC0_Masters"].hide_render = True
    C["_CC0_Masters"].hide_viewport = True
    for z in ("Reception", "Experience_Center", "Workstations", "Meeting_Rooms", "Executive_Area", "Design_Development",
              "Support_Rooms", "Prayer_Rooms", "Washrooms"):
        coll("Furniture_" + z, C["Furniture"])
    world()


def world():
    sc = bpy.context.scene
    w = bpy.data.worlds.new("World")
    sc.world = w
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground")
    sky = nt.nodes.new("ShaderNodeTexSky")
    try:
        sky.sky_type = "NISHITA"
        sky.sun_elevation = math.radians(32)
        sky.sun_rotation = math.radians(100)     # sun from the east-south-east (room 8 windows face east)
        sky.altitude = 50
        sky.air_density = 1.2
        sky.dust_density = 1.5
    except Exception:
        pass
    bg.inputs["Strength"].default_value = 0.35
    nt.links.new(sky.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])
    sd = bpy.data.lights.new("Sun", "SUN")
    sd.energy = 3.2
    sd.angle = math.radians(1.5)
    sd.color = LM.kelvin(5600)
    sun = bpy.data.objects.new("LGT Sun", sd)
    sun.rotation_euler = (math.radians(58), 0, math.radians(100 - 90))
    C["Lighting"].objects.link(sun)


# ------------------------------------------------------------------------------------------ geometry helpers
def box_obj(name, collection, x0, x1, y0, y1, z0, z1, mat, bevel=0.0, **props):
    """Axis-aligned box from plan coordinates; mesh built directly in Blender orientation."""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    hx, hy = abs(x1 - x0) / 2, abs(y1 - y0) / 2
    m = MB().box(-hx, hx, -hy, hy, 0, z1 - z0, mat, bevel=bevel)
    ob = bpy.data.objects.new(name, m.mesh(name, MAT))
    ob.location = pb(cx, cy, z0)
    collection.objects.link(ob)
    for k, v in props.items():
        ob[k] = v
    return ob


def prism_obj(name, collection, pts, z0, z1, mat, **props):
    """Vertical prism from plan polygon (inches) - converted to Blender coordinates (y flipped)."""
    m = MB().prism([(x, -y) for x, y in pts], z0, z1, mat)
    ob = bpy.data.objects.new(name, m.mesh(name, MAT))
    collection.objects.link(ob)
    for k, v in props.items():
        ob[k] = v
    return ob


def cutter(name, collection, wall, a, b, z0, z1):
    c0, c1 = wall["c0"] - 2, wall["c1"] + 2
    ob = box_obj(name, collection, a, b, c0, c1, z0, z1, "cutter") if wall["axis"] == "h" else \
        box_obj(name, collection, c0, c1, a, b, z0, z1, "cutter")
    ob.display_type = "WIRE"
    ob.hide_render = True
    return ob


def boolean(target, cut):
    m = target.modifiers.new("cut " + cut.name, "BOOLEAN")
    m.operation, m.object, m.solver = "DIFFERENCE", cut, "EXACT"


def text(name, collection, body, x, y, z, size, mat="dim", rot=0.0):
    cu = bpy.data.curves.new(name, "FONT")
    cu.body = body
    cu.size = size * IN
    cu.align_x, cu.align_y = "CENTER", "CENTER"
    cu.materials.append(MAT[mat])
    ob = bpy.data.objects.new(name, cu)
    ob.location = pb(x, y, z)
    ob.rotation_euler = (0, 0, rot)
    collection.objects.link(ob)
    return ob


# ------------------------------------------------------------------------------------------ shell
def wall_height(w):
    return S.HALF_H if w["kind"] == "half" else S.DECK_H


def wall_box(w):
    return (w["a"], w["b"], w["c0"], w["c1"]) if w["axis"] == "h" else (w["c0"], w["c1"], w["a"], w["b"])


def window_frame(w, a, b, sill, head, glass_mat, oid):
    """Glass pane + slim black aluminium frame in a wall opening."""
    mid = (w["c0"] + w["c1"]) / 2
    if w["axis"] == "h":
        g = box_obj(f"{oid} glass", C["Windows"], a, b, mid - 0.3, mid + 0.3, sill, head, glass_mat, opening_id=oid)
        parts = [(a, a + 1.5, mid - 1, mid + 1, sill, head), (b - 1.5, b, mid - 1, mid + 1, sill, head),
                 (a, b, mid - 1, mid + 1, sill, sill + 1.5), (a, b, mid - 1, mid + 1, head - 1.5, head)]
    else:
        g = box_obj(f"{oid} glass", C["Windows"], mid - 0.3, mid + 0.3, a, b, sill, head, glass_mat, opening_id=oid)
        parts = [(mid - 1, mid + 1, a, a + 1.5, sill, head), (mid - 1, mid + 1, b - 1.5, b, sill, head),
                 (mid - 1, mid + 1, a, b, sill, sill + 1.5), (mid - 1, mid + 1, a, b, head - 1.5, head)]
    fm = MB()
    for x0, x1, y0, y1, z0, z1 in parts:
        fm.box(x0, x1, -y1, -y0, z0, z1, "alu_black")
    ob = bpy.data.objects.new(f"{oid} frame", fm.mesh(f"{oid} frame", MAT))
    C["Windows"].objects.link(ob)
    return g


def build_wall(w, collection=None, mat=None):
    h = wall_height(w)
    mat = mat or {"ext": "paint_white", "int": "paint_white", "half": "paint_white", "part": "paint_white",
                  "new": "paint_white", "glass": "glass_clear"}[w["kind"]]
    collection = collection or (C["Existing Partitions"] if w["kind"] in ("half", "part") else C["Existing Walls"])
    x0, x1, y0, y1 = wall_box(w)
    ob = box_obj(f'{w["id"]} {w["name"]}', collection, x0, x1, y0, y1, 0, h, mat, wall_id=w["id"], kind=w["kind"],
                 status=w["status"], plan_box_in=str([round(v, 2) for v in (x0, x1, y0, y1)]), height_in=h, note=w["note"])
    for op in w["ops"]:
        oid, kind, a, b, label = op[:5]
        if kind == "win":
            hgt = op[5]
            sill = S.LINTEL - hgt
            cut = cutter(f"{oid} {label}", C["Windows"], w, a, b, sill, S.LINTEL)
            cut["opening_id"], cut["width_in"], cut["sill_in"], cut["head_in"] = oid, round(b - a, 2), sill, S.LINTEL
            window_frame(w, a, b, sill, S.LINTEL, "glass_frosted" if oid == "W05" else "glass_clear", oid)
        else:
            top = S.HALF_H + 2 if w["kind"] == "half" else (S.GATE_H if kind == "gate" else S.LINTEL)
            cut = cutter(f"{oid} {label}", C["Doors"], w, a, b, -1, top)
            cut["opening_id"], cut["width_in"] = oid, round(b - a, 2)
        boolean(ob, cut)
    return ob


def build_shell():
    St = C["Structure"]
    prism_obj("Floor slab (existing, finished floor = 0)", St, S.OUTLINE, -S.SLAB_T, 0, "fl_concrete", status="graphic thickness")
    deck = prism_obj("Steel deck / slab above (soffit painted)", St, S.OUTLINE, S.DECK_H, S.DECK_H + S.DECK_T, "paint_ceiling",
                     status="PHOTO-EST", note="underside at 9'-6\" (114 in) estimated from photos - TO VERIFY ON SITE")
    for name, box in (("room 1 stair", (0, 160, 102, S.FRONT)), ("north-east stair", (S.R8_E - 273, S.R8_E, S.R8_N, S.R8_N + S.STAIR_T)),
                      ("south-east stair", (S.R8_E - 277, S.R8_E, S.SE_N, S.MID_S))):
        hole = box_obj(f"Deck opening over {name}", St, box[0], box[1], box[2], box[3], S.DECK_H - 2, S.DECK_H + S.DECK_T + 2, "cutter")
        hole.display_type, hole.hide_render = "WIRE", True
        boolean(deck, hole)
    walls = {w["id"]: w for w in S.WALLS}
    for wid, op in O.NEW_OPENINGS + O.EXTRA_OPENINGS:
        walls[wid]["ops"].append(list(op))
    for wid, ids in O.REMOVED_OPENINGS.items():
        walls[wid]["ops"] = [o for o in walls[wid]["ops"] if o[0] not in ids]
    for w in S.WALLS:
        build_wall(w)
    for i, (x, y) in enumerate(S.COLUMNS, 1):
        box_obj(f"COL{i:02d} steel column (position PHOTO-EST)", C["Columns"], x - S.COL_W / 2, x + S.COL_W / 2, y - S.COL_W / 2,
                y + S.COL_W / 2, 0, S.DECK_H - S.BEAM_MAIN[1], "steel_painted", status="PHOTO-EST", plan_xy_in=str((x, y)))
    for i, (name, x0, x1, y0, y1, d) in enumerate(S.beam_list(), 1):
        box_obj(f"BM{i:03d} {name}", C["Beams"], x0, x1, y0, y1, S.DECK_H - d, S.DECK_H, "steel_painted",
                status="PHOTO-EST" if "sketch" not in name else "SKETCH (approximate)", depth_in=d)
    build_stairs()


def flight(m, x0, x1, y0, y1, axis, direction, z0, risers, rise):
    for i in range(risers):
        top = z0 + rise * (i + 1)
        if axis == "y":
            a = y0 + i * S.TREAD if direction > 0 else y1 - (i + 1) * S.TREAD
            m.box(x0, x1, -(a + S.TREAD), -a, max(0, top - 8), top, "terrazzo_counter")
        else:
            a = x0 + i * S.TREAD if direction > 0 else x1 - (i + 1) * S.TREAD
            m.box(a, a + S.TREAD, -y1, -y0, max(0, top - 8), top, "terrazzo_counter")
    # plastered waist slab under the steps (smooth sloped soffit instead of the stepped underside of the tread blocks);
    # its top runs through the front-bottom corners of the treads, its underside 2 in below their back-bottom corners
    # (0.5 in wider and longer than the treads, so no face is coplanar with a tread block: coplanar faces render black)
    L, slope, e = risers * S.TREAD, rise / S.TREAD, 0.5
    zu = (z0 + rise - 8 - slope * e, z0 + rise - 8 + slope * (L + e))
    zl = (zu[0] - rise - 2, zu[1] - rise - 2)
    if axis == "y":
        p = (y0 - e, y0 + L + e) if direction > 0 else (y1 + e, y1 - L - e)
        P_ = lambda c, k, z: (c, -p[k], z)                       # noqa: E731  c = across-flight coordinate
        ca, cb = x0 - e, x1 + e
    else:
        p = (x0 - e, x0 + L + e) if direction > 0 else (x1 + e, x1 - L - e)
        P_ = lambda c, k, z: (p[k], -c, z)                       # noqa: E731
        ca, cb = y0 - e, y1 + e
    v = [P_(ca, 0, zl[0]), P_(cb, 0, zl[0]), P_(cb, 0, zu[0]), P_(ca, 0, zu[0]),
         P_(ca, 1, zl[1]), P_(cb, 1, zl[1]), P_(cb, 1, zu[1]), P_(ca, 1, zu[1])]
    _, faces = m._add(v, [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (3, 2, 6, 7), (0, 3, 7, 4), (1, 5, 6, 2)], "paint_white")
    bmesh.ops.recalc_face_normals(m.bm, faces=faces)


def build_stairs():
    st = C["Stairs"]
    n = round(S.FLOOR_TO_FLOOR / 7)
    rise = S.FLOOR_TO_FLOOR / n
    up1 = n // 2 + 1
    up2 = n - up1
    land_z = up1 * rise

    def emit(name, m, **props):
        ob = bpy.data.objects.new(name, m.mesh(name, MAT))
        st.objects.link(ob)
        for k, v in props.items():
            ob[k] = v
        return ob

    m = MB()
    flight(m, 2, 78, 102, 102 + up1 * S.TREAD, "y", 1, 0, up1, rise)
    emit("ST1 room 1 stair, flight 1 (from the back along the outer wall)", m, status="configuration confirmed by owner; risers ASSUMED")
    m = MB().box(2, 158, -S.FRONT, -(102 + up1 * S.TREAD), land_z - 8, land_z, "terrazzo_counter")
    emit("ST1 room 1 stair, landing at the front wall", m)
    m = MB()
    flight(m, 82, 158, 102 + up1 * S.TREAD - up2 * S.TREAD, 102 + up1 * S.TREAD, "y", -1, land_z, up2, rise)
    emit("ST1 room 1 stair, flight 2 (return to the floor above)", m)
    # handrails (black steel, 900 mm above pitch line)
    m = MB()
    y_start, y_end = 102, 102 + up1 * S.TREAD
    m.rod((79.5, -y_start, 36), (79.5, -y_end, land_z + 36), 0.8, "metal_black")
    for k in range(0, up1 + 1, 3):
        yy = y_start + k * S.TREAD
        m.rod((79.5, -yy, k * rise), (79.5, -yy, k * rise + 36), 0.6, "metal_black")
    m.rod((80.5, -(y_end - up2 * S.TREAD), land_z + up2 * rise + 36), (80.5, -y_end, land_z + 36), 0.8, "metal_black")
    emit("ST1 handrail (proposed)", m, status="PROPOSED")
    for tag, x0, x1, y0, y1, wide in (("ST2 north-east stair", S.R8_E - 273, S.R8_E, S.R8_N, S.R8_N + S.STAIR_T, 48),
                                      ("ST3 south-east stair", S.R8_E - 277, S.R8_E, S.SE_N, S.MID_S, 54)):
        run1 = up1 * S.TREAD
        xs = x1 - 50 - run1
        m = MB()
        flight(m, xs, xs + run1, y1 - wide, y1, "x", 1, 0, up1, rise)
        emit(f"{tag}, flight 1 (layout ASSUMED)", m, status="ASSUMED")
        m = MB().box(x1 - 50, x1, -y1, -(y1 - 2 * wide - 4), land_z - 8, land_z, "terrazzo_counter")
        emit(f"{tag}, landing (layout ASSUMED)", m, status="ASSUMED")
        m = MB()
        flight(m, x1 - 50 - up2 * S.TREAD, x1 - 50, y1 - 2 * wide - 4, y1 - wide - 4, "x", -1, land_z, up2, rise)
        emit(f"{tag}, flight 2 (layout ASSUMED)", m, status="ASSUMED")
    m = MB().box(160, 300, -S.FRONT + 24, -(S.FRONT - 36), 0, 7, "terrazzo_counter").box(160, 300, -S.FRONT, -(S.FRONT - 24), 0, 14, "terrazzo_counter")
    emit("ST4 entrance steps inside room 1 (2 steps, PHOTO-EST)", m, status="PHOTO-EST")


# ------------------------------------------------------------------------------------------ fit-out
def glass_partition(w):
    """Slim black-aluminium framed glass partition with mullions; door openings cut by booleans."""
    x0, x1, y0, y1 = wall_box(w)
    mid = (w["c0"] + w["c1"]) / 2
    pane = dict(w, c0=mid - 0.25, c1=mid + 0.25)
    ob = build_wall(dict(pane, kind="glass"), C["New Partitions"], "glass_clear")
    fm = MB()
    if w["axis"] == "h":
        fm.box(x0, x1, -(mid + 1), -(mid - 1), 0, 2.5, "alu_black").box(x0, x1, -(mid + 1), -(mid - 1), S.DECK_H - 2, S.DECK_H, "alu_black")
    else:
        fm.box(mid - 1, mid + 1, -y1, -y0, 0, 2.5, "alu_black").box(mid - 1, mid + 1, -y1, -y0, S.DECK_H - 2, S.DECK_H, "alu_black")
    doors = [(op[2], op[3]) for op in w["ops"] if op[1] == "door"]
    a, b = w["a"], w["b"]
    pos = a
    while pos <= b + 0.01:
        if not any(da - 2 < pos < db + 2 for da, db in doors):
            if w["axis"] == "h":
                fm.box(pos - 0.75, pos + 0.75, -(mid + 1), -(mid - 1), 0, S.DECK_H, "alu_black")
            else:
                fm.box(mid - 1, mid + 1, -(pos + 0.75), -(pos - 0.75), 0, S.DECK_H, "alu_black")
        pos += 48 if (b - a) > 60 else (b - a)
    for da, db in doors:                       # door frame jambs + transom
        for p in (da, db):
            if w["axis"] == "h":
                fm.box(p - 1, p + 1, -(mid + 1.2), -(mid - 1.2), 0, S.DECK_H, "alu_black")
            else:
                fm.box(mid - 1.2, mid + 1.2, -(p + 1), -(p - 1), 0, S.DECK_H, "alu_black")
        if w["axis"] == "h":
            fm.box(da, db, -(mid + 1.2), -(mid - 1.2), S.LINTEL, S.LINTEL + 2, "alu_black")
        else:
            fm.box(mid - 1.2, mid + 1.2, -db, -da, S.LINTEL, S.LINTEL + 2, "alu_black")
    # privacy / safety manifestation band
    fob = bpy.data.objects.new(f'{w["id"]} frame + mullions', fm.mesh(f'{w["id"]} frame', MAT))
    C["New Partitions"].objects.link(fob)
    band = MB()
    for lo, hi in ((40, 44), (58, 60)):
        segs = [(a, b)]
        for da, db in doors:
            segs = [s for seg in segs for s in ((seg[0], min(seg[1], da)), (max(seg[0], db), seg[1])) if s[1] - s[0] > 1]
        for sa, sb in segs:
            if w["axis"] == "h":
                band.box(sa, sb, -(mid + 0.32), -(mid - 0.32), lo, hi, "glass_frosted")
            else:
                band.box(mid - 0.32, mid + 0.32, -sb, -sa, lo, hi, "glass_frosted")
    bob = bpy.data.objects.new(f'{w["id"]} manifestation band', band.mesh(f'{w["id"]} band', MAT))
    C["New Partitions"].objects.link(bob)
    return ob


def build_partitions():
    walls = {w["id"]: w for w in S.WALLS}
    for k, (wid, a, b, treat) in enumerate(O.HALF_TREAT, 1):
        w = walls[wid]
        x0, x1, y0, y1 = (a, b, w["c0"], w["c1"]) if w["axis"] == "h" else (w["c0"], w["c1"], a, b)
        if treat == "glass":
            mid = (w["c0"] + w["c1"]) / 2
            gx0, gx1, gy0, gy1 = (a, b, mid - 0.25, mid + 0.25) if w["axis"] == "h" else (mid - 0.25, mid + 0.25, a, b)
            ob = box_obj(f"NI{k:02d} glass above 48in wall {wid}", C["New Partitions"], gx0, gx1, gy0, gy1, S.HALF_H, S.DECK_H, "glass_clear", status="PROPOSED")
            fm = MB()
            fm.box(x0, x1, -y1, -y0, S.HALF_H, S.HALF_H + 1.5, "alu_black").box(x0, x1, -y1, -y0, S.DECK_H - 2, S.DECK_H, "alu_black")
            pos = a + 48
            while pos < b - 6:
                if not any(op[1] == "door" and op[2] - 3 < pos < op[3] + 3 for op in w["ops"]):
                    if w["axis"] == "h":
                        fm.box(pos - 0.75, pos + 0.75, -(mid + 1), -(mid - 1), S.HALF_H, S.DECK_H, "alu_black")
                    else:
                        fm.box(mid - 1, mid + 1, -(pos + 0.75), -(pos - 0.75), S.HALF_H, S.DECK_H, "alu_black")
                pos += 48
            fo = bpy.data.objects.new(f"NI{k:02d} frame above {wid}", fm.mesh(f"NI{k:02d} frame", MAT))
            C["New Partitions"].objects.link(fo)
        else:
            ob = box_obj(f"NI{k:02d} solid infill above 48in wall {wid}", C["New Partitions"], x0, x1, y0, y1, S.HALF_H, S.DECK_H, "paint_white", status="PROPOSED")
        for op in w["ops"]:
            if op[1] == "door" and a < op[3] and op[2] < b:
                boolean(ob, cutter(f"{op[0]} head cut {wid}", C["Doors"], w, op[2], op[3], S.HALF_H - 1, S.LINTEL))
        # glass coping on top of the 48" wall
    for w in O.NEW_WALLS:
        if w["kind"] == "glass":
            glass_partition(w)
        else:
            build_wall(w, C["New Partitions"], "paint_white")


def door_leaves():
    """Door leaves / frames for every door opening, closed position, per DOOR_TYPES."""
    allw = S.WALLS + O.NEW_WALLS
    n = 0
    for w in allw:
        for op in w["ops"]:
            oid, kind, a, b = op[:4]
            if kind not in ("door", "gate") or oid not in O.DOOR_TYPES:
                continue
            typ, fin = O.DOOR_TYPES[oid]
            if typ == "none":
                continue
            head = S.GATE_H if kind == "gate" else S.LINTEL
            mid = (w["c0"] + w["c1"]) / 2
            m = MB()
            leaves = 2 if typ in ("glass2", "solid2") else 1
            wid = (b - a - 1.0) / leaves
            for i in range(leaves):
                la = a + 0.5 + i * wid
                lb = la + wid
                if typ.startswith("glass") or typ == "slide":
                    m.box(la + 0.2, lb - 0.2, -0.25, 0.25, 2.5, head - 2.5, "glass_clear")
                    m.box(la, lb, -0.9, 0.9, 0, 2.5, "alu_black").box(la, lb, -0.9, 0.9, head - 2.5, head - 0.2, "alu_black")
                    hx = la + 3 if (leaves == 2 and i == 1) else lb - 3
                    for sd in (-1, 1):
                        m.box(hx - 0.6, hx + 0.6, sd * 1.6 - 0.6, sd * 1.6 + 0.6, 30, 66, "brass")
                else:
                    mat = fin if fin in MAT else "oak"
                    m.box(la, lb, -0.9, 0.9, 0.3, head - 0.2, mat, bevel=0.1)
                    hx = la + 3 if (leaves == 2 and i == 1) else lb - 3
                    right = hx > (la + lb) / 2
                    for sd in (-1, 1):
                        m.box(hx - 4.0 if right else hx - 0.4, hx + 0.4 if right else hx + 4.0,
                              sd * 2.0 - 0.35, sd * 2.0 + 0.35, 38, 39, "alu_black")
                        m.box(hx - 0.4, hx + 0.4, sd * 1.2 - 0.8, sd * 1.2 + 0.8, 37, 40, "alu_black")
            if typ in ("solid", "solid2", "fire"):           # slim frame (architrave) both faces
                t = (w["c1"] - w["c0"]) / 2 + 0.6
                for s in (-1, 1):
                    m.box(a - 1.5, a, s * t - 0.6, s * t + 0.6, 0, head + 1.5, "alu_black")
                    m.box(b, b + 1.5, s * t - 0.6, s * t + 0.6, 0, head + 1.5, "alu_black")
                    m.box(a - 1.5, b + 1.5, s * t - 0.6, s * t + 0.6, head, head + 1.5, "alu_black")
            me = m.mesh(f"{oid} door leaf", MAT)
            ob = bpy.data.objects.new(f"{oid} door ({typ}) {op[4]}", me)
            C["Door Leaves"].objects.link(ob)
            if w["axis"] == "h":
                ob.location = pb(0, mid, 0)
                # mesh x = plan x already; local y = across the wall
            else:
                ob.location = pb(mid, 0, 0)
                ob.rotation_euler = (0, 0, math.radians(-90))
                # rotate: local x (along the wall) -> plan +y (Blender -y)
            ob["opening_id"], ob["door_type"] = oid, typ
            n += 1
    log("door leaves", n)


def zone_floors_and_labels():
    for coll_name, zid, label, pts, fin, ceiling in O.ZONES:
        prism_obj(f"{zid} {label.splitlines()[0]} - floor finish", C[coll_name], pts, 0, 0.4, fin, zone_id=zid,
                  function=label.replace("\n", " "), floor_finish=fin, ceiling=ceiling, area_sft=round(S.poly_area_sft(pts), 1))
        x, y = O.LABEL_AT[zid]
        area = S.poly_area_sft(pts)
        body = f"{label}\n{area:,.0f} sft" if zid not in O.SMALL_LABELS else label.splitlines()[0]
        size = 12 if (zid in O.VERTICAL_LABELS or zid in O.SMALL_LABELS or area < 200) else 17
        text(f"{zid} label", C["Labels"], body, x, y, 150, size, "label", rot=math.pi / 2 if zid in O.VERTICAL_LABELS else 0)
    C["Labels"].hide_render = True


def finishes_and_branding():
    for i, (kind, x0, x1, y0, y1, z0, z1, mat, label, facing) in enumerate(O.FINISHES, 1):
        if kind == "slatwall":
            m = MB()
            t = min(x1 - x0, y1 - y0)
            L = max(x1 - x0, y1 - y0)
            n = int((L - 1.8) // 3.0) + 1
            m.box(-L / 2, L / 2, t / 2 - 0.5, t / 2, z0, z1, "plinth")       # black acoustic backing (rear)
            for k in range(n):
                p = -L / 2 + k * 3.0
                m.box(p, p + 1.8, -t / 2, t / 2 - 0.5, z0, z1, mat, bevel=0.15)
            place(m.mesh(f"FIN{i:02d} {label}", MAT), f"FIN{i:02d} {label}", C["Wall Finishes"],
                  (x0 + x1) / 2, (y0 + y1) / 2, 0, facing)
        else:
            box_obj(f"FIN{i:02d} {label}", C["Wall Finishes"], x0, x1, y0, y1, z0, z1, mat, bevel=0.1)
    for i, (mat, x, y, z, wdt, facing) in enumerate(O.LOGOS, 1):
        img = MAT[mat].node_tree.nodes.get("Image Texture")
        aspect = img.image.size[1] / img.image.size[0] if img and img.image and img.image.size[0] else 0.3
        A.decal(f"BR{i:02d} client logo ({mat})", C["Branding"], mat, x, y, z, wdt, wdt * aspect, facing, MAT,
                lambda px, py, pz: pb(px, py, pz))


def furniture():
    lib = A.Library(C["_CC0_Masters"])
    zone_coll = {z[1]: z[0] for z in O.ZONES}
    counts = {}
    for idx, (key, x, y, facing, zone, z, label) in enumerate(O.PLACEMENTS, 1):
        area = zone_coll.get(zone, "Support_Rooms")
        target = C["Furniture_" + area] if ("Furniture_" + area) in C else C["Furniture"]
        if key.startswith("cc0:"):
            name = key[4:]
            obs = lib.place(name, target, x * IN, -y * IN, z * IN, facing, label=f"F{idx:03d} {name} (CC0)")
            for o in obs:
                o["zone"] = zone
            counts[key] = counts.get(key, 0) + 1
            continue
        builder, kw, fp, desc = O.ASSETS[key]
        me = A.get(key, getattr(A, builder), **kw)
        ob = place(me, f"F{idx:03d} {key}", target, x, y, z, facing, {"zone": zone, "asset": key, "description": desc,
                                                                   "footprint_in": str(fp)})
        counts[key] = counts.get(key, 0) + 1
        if label and label.startswith("PLANT:"):
            plant = label.split(":")[1]
            h = 20 if key == "planter_l" else 16
            if plant == "pachira":
                lib.place("pachira_aquatica_01", C["Plants"], x * IN, -y * IN, (z + h - 1) * IN, facing * 0 + (idx * 47) % 360,
                          scale=0.95, objects=["pachira_aquatica_01_leaves_a", "pachira_aquatica_01_bark_a"], label=f"PL{idx:03d} pachira (CC0)")
            else:
                lib.place("calathea_orbifolia_01", C["Plants"], x * IN, -y * IN, (z + h - 1.5) * IN, (idx * 61) % 360,
                          scale=1.0, objects=["calathea_orbifolia_01_a"], label=f"PL{idx:03d} calathea (CC0)")
    # desk plants (small succulents) on some workstation benches
    for idx, (key, x, y, facing, zone, z, label) in enumerate(O.PLACEMENTS, 1):
        if key in ("bench3", "bench_design") and idx % 2 == 0:
            lib.place("potted_plant_04", C["Plants"], (x - 20) * IN, -(y + 2) * IN, 30.2 * IN, 0, label=f"PL{idx:03d} desk plant (CC0)")
    log("furniture placed", sum(counts.values()), "items,", len(counts), "types; mesh assets", len(A.CACHE))
    return counts, lib


def ceilings():
    n = 0
    for kind, cx, cy, z, kw, zone in O.CEILING:
        if kind == "slat_raft":
            key = f"slat_{kw['w']}x{kw['d']}"
            me = A.get(key, A.slat_raft, kw["w"], kw["d"])
        elif kind == "raft":
            key = f"raft_{round(kw['w'])}x{kw['d']}_{kw['mat']}"
            me = A.get(key, A.raft, kw["w"], kw["d"], mat=kw["mat"])
        else:
            key = f"baffle_{round(kw['L'])}_{kw['mat']}"
            me = A.get(key, A.baffle, round(kw["L"]), 12, 1.8, kw["mat"])
        rot = 90 if kind == "baffle" else 0
        place(me, f"CL{n:03d} {kind} ({zone})", C["Ceilings"], cx, cy, z, rot, {"zone": zone})
        n += 1
    log("ceiling elements", n)


def lights_and_fixtures(lib):
    LF, LS = C["Light Fixtures"], C["Light Sources"]
    n = 0

    def add_light(name, kind, loc, rot=(0, 0, 0), power=10, size=(0.1, 0.1), temp=3500, spot=None):
        ld = bpy.data.lights.new(name, kind)
        ld.energy = power
        ld.color = LM.kelvin_soft(temp)
        if kind == "AREA":
            ld.shape = "RECTANGLE" if size[0] != size[1] else "DISK"
            ld.size, ld.size_y = size
        if kind == "SPOT":
            ld.spot_size = math.radians(spot or 60)
            ld.spot_blend = 0.6
            ld.shadow_soft_size = 0.03
        if kind == "POINT":
            ld.shadow_soft_size = 0.05
        ob = bpy.data.objects.new(name, ld)
        ob.location = loc
        ob.rotation_euler = rot
        LS.objects.link(ob)
        return ob

    for kind, x, y, z, kw, zone in O.LIGHTS:
        n += 1
        temp = kw.get("temp", 3500)
        led = {3000: "led_3000", 3500: "led_3500", 4000: "led_4000"}.get(temp, "led_3500")
        if kind == "lin":
            L = kw.get("L", 72)
            me = A.get(f"lin_{L}_{led}", A.linear_pendant, L, S.DECK_H - z - 3.2, led=led)
            rot = kw.get("rot", 0)
            place(me, f"LT{n:03d} linear pendant {L}in ({zone})", LF, x, y, z, rot, {"zone": zone, "cct_K": temp})
            add_light(f"LS{n:03d} linear {zone}", "AREA", pb(x, y, z - 0.3), (0, 0, math.radians(rot)),
                      power=1.1 * L, size=(L * IN, 3 * IN), temp=temp)
            add_light(f"LS{n:03d} linear up {zone}", "AREA", pb(x, y, z + 3.6), (math.pi, 0, math.radians(rot)),
                      power=0.35 * L, size=(L * IN, 3 * IN), temp=temp)
        elif kind == "halo":
            r = kw.get("r", 20)
            me = A.get(f"halo_{r}", A.halo_pendant, r, S.DECK_H - z, led)
            place(me, f"LT{n:03d} halo pendant ({zone})", LF, x, y, z, 0, {"zone": zone})
            add_light(f"LS{n:03d} halo {zone}", "AREA", pb(x, y, z - 0.3), power=4.0 * r, size=(2 * r * IN, 2 * r * IN), temp=temp)
            add_light(f"LS{n:03d} halo up {zone}", "AREA", pb(x, y, z + 2), (math.pi, 0, 0), power=1.2 * r, size=(2 * r * IN, 2 * r * IN), temp=temp)
        elif kind == "down":
            me = A.get(f"down_{led}", A.downlight, 3.0, led)
            zz = S.DECK_H - 6
            place(me, f"LT{n:03d} downlight ({zone})", LF, x, y, zz, 0, {"zone": zone})
            add_light(f"LS{n:03d} down {zone}", "SPOT", pb(x, y, zz - 0.5), power=kw.get("power", 55), temp=temp, spot=kw.get("beam", 80))
        elif kind == "spot":
            me = A.get(f"spot_{led}", A.track_spot, 5.5, led)
            ob = place(me, f"LT{n:03d} track spot ({zone})", LF, x, y, z, 0, {"zone": zone})
            tx, ty, tz = kw["aim"]
            src = Vector(pb(x, y, z - 6))
            tgt = Vector(pb(tx, ty, tz))
            d = (tgt - src).normalized()
            rq = Vector((0, 0, -1)).rotation_difference(d)
            ob.rotation_mode = "QUATERNION"
            ob.rotation_quaternion = rq
            lo = add_light(f"LS{n:03d} spot {zone}", "SPOT", tuple(src), power=40, temp=temp, spot=kw.get("w", 40))
            lo.rotation_mode = "QUATERNION"
            lo.rotation_quaternion = rq
        elif kind == "track":
            L = kw.get("L", 120)
            me = A.get(f"track_{L}", A.track, L)
            place(me, f"LT{n:03d} track rail ({zone})", LF, x, y, z, kw.get("rot", 0), {"zone": zone})
        elif kind == "pendant_cc0":
            obs = lib.place("modern_ceiling_lamp_01", LF, x * IN, -y * IN, S.DECK_H * IN - 1.173, 0, label=f"LT{n:03d} cafe pendant (CC0)")
            add_light(f"LS{n:03d} cafe pendant", "POINT", pb(x, y, S.DECK_H - 36.0), power=60, temp=3000)
    log("light fixtures", n, "; light objects", len(LS.objects))


def mep():
    M_ = C["MEP_Fire_Safety"]
    me = A.get("ac", A.ac_cassette)
    for i, (x, y, rot, zone) in enumerate(O.AC_UNITS, 1):
        place(me, f"AC{i:02d} VRF indoor unit, under-ceiling ({zone}) - capacity by MEP", M_, x, y, S.DECK_H, rot, {"zone": zone})
    me = A.get("smoke", A.smoke_detector)
    for i, (x, y) in enumerate(O.SMOKE_DETECTORS, 1):
        place(me, f"SD{i:02d} smoke detector", M_, x, y, S.DECK_H, 0)
    me = A.get("exit", A.exit_sign)
    for i, (x, y, f) in enumerate(O.EXIT_SIGNS, 1):
        place(me, f"EX{i:02d} exit sign", M_, x, y, 88, f)


def tile_linings():
    """Porcelain wall tiles (to 96 in) along every edge of the wet-room zones, leaving door openings free."""
    allw = S.WALLS + O.NEW_WALLS
    doors = []
    for w in allw:
        for op in w["ops"]:
            if op[1] == "door":
                doors.append((w["axis"], w["c0"], w["c1"], op[2], op[3]))
    for wid, op in O.EXTRA_OPENINGS + O.NEW_OPENINGS:
        if op[1] == "door":
            w = next(x for x in allw if x["id"] == wid)
            doors.append((w["axis"], w["c0"], w["c1"], op[2], op[3]))
    zones = {z[1]: z for z in O.ZONES}
    n = 0
    for zid in O.TILED_ZONES:
        pts = zones[zid][3]
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
        for i in range(len(pts)):
            (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % len(pts)]
            if abs(y0 - y1) < 0.01:          # horizontal edge
                axis, c, lo, hi = "h", y0, min(x0, x1), max(x0, x1)
                inward = 1 if cy > c else -1
            elif abs(x0 - x1) < 0.01:
                axis, c, lo, hi = "v", x0, min(y0, y1), max(y0, y1)
                inward = 1 if cx > c else -1
            else:
                continue
            segs = [(lo, hi)]
            for ax, c0, c1, a, b in doors:
                if ax == axis and (abs(c0 - c) < 1.0 or abs(c1 - c) < 1.0):
                    segs = [t for sg in segs for t in ((sg[0], min(sg[1], a)), (max(sg[0], b), sg[1])) if t[1] - t[0] > 0.5]
            for a, b in segs:
                t0, t1 = sorted((c, c + inward * 0.5))
                if axis == "h":
                    box_obj(f"TL{n:03d} wall tiles {zid}", C["Wall Finishes"], a, b, t0, t1, 0.4, 96, "wall_porcelain")
                else:
                    box_obj(f"TL{n:03d} wall tiles {zid}", C["Wall Finishes"], t0, t1, a, b, 0.4, 96, "wall_porcelain")
                n += 1
    log("tile linings", n)


def wall_clocks(lib):
    for i, (x, y, z, f) in enumerate(O.WALL_CLOCKS, 1):
        lib.place("wall_clock", C["Support_Rooms"], x * IN, -y * IN, z * IN, f, label=f"CLK{i:02d} wall clock (CC0)")


def window_blinds():
    """Roller blinds on the room 8 east windows (sheer, 40 % down)."""
    for w in S.WALLS:
        if w["id"] != "EW10":
            continue
        for op in w["ops"]:
            oid, kind, a, b = op[:4]
            if kind != "win":
                continue
            box_obj(f"{oid} roller blind", C["Windows"], w["c0"] - 2.5, w["c0"] - 2.2, a + 1, b - 1, S.LINTEL - 22, S.LINTEL + 2, "fab_sand")
            box_obj(f"{oid} blind cassette", C["Windows"], w["c0"] - 3.5, w["c0"] - 1, a, b, S.LINTEL + 2, S.LINTEL + 5, "alu_black")



# ------------------------------------------------------------------------------------------ 3D dimensions (hidden in renders)
def ftin(v):
    v = round(v)
    return f"{v // 12}'-{v % 12}\""


def dim3d(tag, p, q, off, label, z=150):
    D = C["Dimensions"]
    t = 2.5
    if abs(p[1] - q[1]) < 1e-6:
        y = p[1] + off
        box_obj(f"DIM {tag}", D, p[0], q[0], y - t / 2, y + t / 2, z, z + 1, "dim")
        for x in (p[0], q[0]):
            box_obj(f"DIM {tag} tick", D, x - t / 2, x + t / 2, y - 14, y + 14, z, z + 1, "dim")
        text(f"DIM {tag} text", D, label, (p[0] + q[0]) / 2, y - 22, z, 20)
    else:
        x = p[0] + off
        box_obj(f"DIM {tag}", D, x - t / 2, x + t / 2, p[1], q[1], z, z + 1, "dim")
        for y in (p[1], q[1]):
            box_obj(f"DIM {tag} tick", D, x - 14, x + 14, y - t / 2, y + t / 2, z, z + 1, "dim")
        text(f"DIM {tag} text", D, label, x - 24, (p[1] + q[1]) / 2, z, 20, rot=math.pi / 2)


def dimensions():
    lab = lambda v, a=False: f'{ftin(v)} ({v:g}" = {v * 25.4:,.0f} mm)' + ("  ASSUMED" if a else "")
    F = S.FRONT
    dim3d("room 1 width", (0, F), (300, F), 70, lab(300))
    dim3d("room 3 width", (305, F), (565, F), 70, lab(260))
    dim3d("room 4 width", (570, F), (1088, F), 70, lab(518))
    dim3d("front overall", (-10, F + 10), (1098, F + 10), 140, lab(1108))
    dim3d("front row depth", (-10, 0), (-10, F), -110, lab(247))
    dim3d("middle block depth", (-65, S.MID_N), (-65, S.MID_S), -60, lab(881))
    dim3d("west overall", (-65, S.MID_N - 10), (-65, F + 10), -150, lab(1158))
    dim3d("room 8 length", (S.R8_E + 10, S.R8_N), (S.R8_E + 10, S.MID_S), 70, lab(1538))
    dim3d("east overall", (S.R8_E + 10, S.R8_N - 10), (S.R8_E + 10, F + 10), 150, lab(1815))
    dim3d("room 8 width", (S.R8_W, S.R8_N - 10), (S.R8_E, S.R8_N - 10), -70, lab(450, True))
    dim3d("rooms 5 6 width", (367, S.MID_N - 10), (866, S.MID_N - 10), -70, lab(499))
    dim3d("room 7 upper width", (46, S.MID_N - 10), (S.R7_E, S.MID_N - 10), -150, lab(316))
    C["Dimensions"].hide_render = True

# ------------------------------------------------------------------------------------------ cameras
def cameras():
    import cameras as CAM
    out = {}
    for c in CAM.CAMERAS:
        cd = bpy.data.cameras.new(c["name"])
        cd.clip_start, cd.clip_end = 0.05, 300
        ob = bpy.data.objects.new(c["name"], cd)
        C["Cameras"].objects.link(ob)
        if c.get("ortho"):
            cd.type = "ORTHO"
            cd.ortho_scale = c["ortho"]
            ob.location = c["loc_m"]
            ob.rotation_euler = tuple(math.radians(v) for v in c["rot_deg"])
        else:
            cd.lens = c.get("lens", 20)
            cd.sensor_width = 36
            px, py, pz = c["pos"]
            tx, ty, tz = c["target"]
            loc = Vector(pb(px, py, pz))
            tgt = Vector(pb(tx, ty, tz))
            d = tgt - loc
            heading = math.atan2(d.y, d.x) - math.pi / 2
            ob.location = loc
            ob.rotation_euler = (math.radians(90), 0, heading)       # level camera = vertical lines stay vertical
            dist = math.hypot(d.x, d.y)
            pitch = math.atan2(d.z, dist)
            cd.shift_y = max(-0.3, min(0.3, math.tan(pitch) * cd.lens / cd.sensor_width * 0.95))
        for k, v in c.items():
            if k in ("room", "priority", "res", "exposure"):
                ob[k] = str(v)
        out[c["name"]] = ob
    return out


def render_settings():
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    cy = sc.cycles
    cy.device = "CPU"
    cy.samples = 128
    cy.use_adaptive_sampling = True
    cy.adaptive_threshold = 0.02
    cy.use_denoising = True
    try:
        cy.denoiser = "OPENIMAGEDENOISE"
    except Exception:
        pass
    cy.max_bounces, cy.diffuse_bounces, cy.glossy_bounces = 8, 3, 3
    cy.transmission_bounces, cy.transparent_max_bounces = 8, 8
    cy.sample_clamp_indirect = 8.0
    cy.blur_glossy = 1.0
    cy.caustics_reflective = cy.caustics_refractive = False
    try:
        cy.use_light_tree = True
    except Exception:
        pass
    sc.render.use_persistent_data = True
    sc.render.resolution_x, sc.render.resolution_y = 1600, 900
    sc.render.image_settings.file_format = "PNG"
    sc.view_settings.view_transform = "AgX"
    try:
        sc.view_settings.look = "AgX - Medium High Contrast"
    except Exception:
        pass
    sc.view_settings.exposure = 0.0


# ------------------------------------------------------------------------------------------ main
def main():
    os.makedirs(OUT, exist_ok=True)
    setup_scene()
    log("materials", len(MAT))
    build_shell()
    log("shell built")
    if not SHELL_ONLY:
        build_partitions()
        door_leaves()
        zone_floors_and_labels()
        finishes_and_branding()
        counts, lib = furniture()
        ceilings()
        lights_and_fixtures(lib)
        mep()
        window_blinds()
        tile_linings()
        wall_clocks(lib)
    dimensions()
    cams = cameras()
    render_settings()
    sc = bpy.context.scene
    sc.camera = next(iter(cams.values())) if cams else None
    C["Dimensions"].hide_render = True
    stem = "Final_Office_Interior" if not SHELL_ONLY else "Shell_Verified"
    blend = os.path.join(OUT, stem + ".blend")
    if "--pack" in ARGV:                 # self-contained delivery file (all textures inside the .blend)
        bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=blend, compress=True, relative_remap=True)
    log("saved", blend, round(os.path.getsize(blend) / 1e6, 1), "MB")
    if not NO_GLB:
        glb = os.path.join(OUT, stem + ".glb")
        bpy.ops.export_scene.gltf(filepath=glb, export_format="GLB", use_renderable=True, export_apply=True,
                                  export_extras=True, export_cameras=True, export_lights=False, export_yup=True,
                                  export_image_format="JPEG", export_jpeg_quality=85)
        log("glb", glb, round(os.path.getsize(glb) / 1e6, 1), "MB")
    print("OBJECTS", len(bpy.data.objects), "MESHES", len(bpy.data.meshes), "MATERIALS", len(bpy.data.materials))


main()
