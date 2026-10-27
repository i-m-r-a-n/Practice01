"""Builds the walkthrough animation on a COPY of the approved model (the original .blend is opened read-only and saved under a
new name; no geometry, material or lamp of the design is changed).

blender -b ORIGINAL.blend --python build_walkthrough.py -- OUT.blend REPORT_DIR
- one camera per shot (WT_<shot>), keyed on every frame of a 24 fps timeline (eased in/out, level cameras with lens shift
  for interiors so verticals stay vertical); timeline markers switch cameras; the overhead elements (deck, beams,
  ceilings, light fittings, AC units) are keyed hidden for the overview shots only
- collision report: clearance around every camera position and along the path (ray casts against the visible geometry)
"""
import csv
import math
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import shots as S  # noqa: E402

ARGV = sys.argv[sys.argv.index("--") + 1:]
OUT_BLEND, REPORT_DIR = os.path.abspath(ARGV[0]), os.path.abspath(ARGV[1])
os.makedirs(REPORT_DIR, exist_ok=True)
IN = 0.0254
FPS = 24
STEP = 24 // S.FPS_RENDER                     # render every STEP-th frame
INTERIOR_EXPOSURE, OVERVIEW_EXPOSURE = 1.6, 0.3
sc = bpy.context.scene
sc.render.fps = FPS


def pb(x, y, z):
    return Vector((x * IN, -y * IN, z * IN))


def ease(t):
    return t * t * (3 - 2 * t)


def lerp(a, b, t):
    return a + (b - a) * t


def overhead_objects():
    names = {"Beams", "Ceilings", "Light Fixtures", "MEP_Fire_Safety"}
    obs = set()
    for c in bpy.data.collections:
        if c.name in names:
            obs.update(c.all_objects)
    obs.update(o for o in bpy.data.objects if o.name.startswith("Steel deck"))
    return sorted(obs, key=lambda o: o.name)


def shot_frames(shot):
    return int(round(shot["dur"] * FPS)) + 1


def sample_shot(shot, n):
    """camera location, rotation (euler), shift_y for n frames"""
    out = []
    for i in range(n):
        t = ease(i / (n - 1))
        if shot["kind"] == "dolly":
            p = lerp(pb(*shot["pos"][0]), pb(*shot["pos"][1]), t)
            g = lerp(pb(*shot["tgt"][0]), pb(*shot["tgt"][1]), t)
            d = g - p
            heading = math.atan2(d.y, d.x) - math.pi / 2
            pitch = math.atan2(d.z, math.hypot(d.x, d.y))
            shift = max(-0.3, min(0.3, math.tan(pitch) * shot["lens"] / 36 * 0.95))
            out.append((p, (math.radians(90), 0.0, heading), shift))
        else:   # orbit / crane around a target (metres)
            tg = shot["target"]
            tgt = lerp(Vector(tg[0]), Vector(tg[1]), t) if isinstance(tg[0], tuple) else Vector(tg)
            dist = lerp(shot["dist"][0], shot["dist"][1], t)
            el = math.radians(lerp(shot["elev"][0], shot["elev"][1], t))
            az = math.radians(lerp(shot["azim"][0], shot["azim"][1], t))
            p = tgt + Vector((math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el))) * dist
            rot = (tgt - p).to_track_quat("-Z", "Y").to_euler()
            out.append((p, tuple(rot), 0.0))
    return out


# ------------------------------------------------------------------ cameras, keys, markers
coll = bpy.data.collections.new("Walkthrough_Cameras")
sc.collection.children.link(coll)
over = overhead_objects()
sc.timeline_markers.clear()
frame = 1
rows = []
order = [s for s in S.SHOTS if s["video"] == "A"] + [s for s in S.SHOTS if s["video"] == "B"]
for shot in order:
    n = shot_frames(shot)
    cd = bpy.data.cameras.new("WT_" + shot["name"])
    cd.lens, cd.sensor_width, cd.clip_start, cd.clip_end = shot["lens"], 36, 0.05, 400
    cam = bpy.data.objects.new("WT_" + shot["name"], cd)
    coll.objects.link(cam)
    samples = sample_shot(shot, n)
    for i, (p, rot, shift) in enumerate(samples):
        f = frame + i
        cam.location, cam.rotation_euler = p, rot
        cd.shift_y = shift
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_euler", frame=f)
        cd.keyframe_insert("shift_y", frame=f)
    for idb in (cam, cd):
        if idb.animation_data and idb.animation_data.action:
            act = idb.animation_data.action
            curves = getattr(act, "fcurves", None)
            if curves is None:      # layered actions (Blender 4.4+)
                curves = [fc for layer in act.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
            for fc in curves:
                for kp in fc.keyframe_points:
                    kp.interpolation = "LINEAR"
    m = sc.timeline_markers.new(shot["name"], frame=frame)
    m.camera = cam
    for k, v in (("shot", shot["name"]), ("video", shot["video"]), ("scene_label", shot["scene"]), ("title", shot["label"]),
                 ("frame_start", frame), ("frame_end", frame + n - 1)):
        cam[k] = v
    is_over = shot["kind"] != "dolly"
    for o in over:              # overhead elements hidden only during overview shots
        o.hide_render = is_over
        o.keyframe_insert("hide_render", frame=frame)
    sc.view_settings.exposure = OVERVIEW_EXPOSURE if is_over else INTERIOR_EXPOSURE
    sc.view_settings.keyframe_insert("exposure", frame=frame)
    rows.append((shot["name"], shot["video"], frame, frame + n - 1, n, len(range(frame, frame + n, STEP))))
    frame += n
sc.frame_start, sc.frame_end, sc.frame_step = 1, frame - 1, STEP
for o in over:                  # constant (stepped) visibility between keys
    if o.animation_data and o.animation_data.action:
        act = o.animation_data.action
        curves = getattr(act, "fcurves", None)
        if curves is None:
            curves = [fc for layer in act.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]
        for fc in curves:
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"
sc.camera = bpy.data.objects["WT_" + order[0]["name"]]
with open(os.path.join(REPORT_DIR, "shot_timeline.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["shot", "video", "frame_start_24fps", "frame_end_24fps", "frames_24fps", "frames_rendered_12fps"])
    w.writerows(rows)

# ------------------------------------------------------------------ collision / clearance check (interior shots)
for o in over:
    o.hide_render = False
dg = bpy.context.evaluated_depsgraph_get()
skip_colls = {"Labels", "Dimensions", "Cameras", "Walkthrough_Cameras", "_CC0_Masters"}


def ignored(ob):
    return ob is None or ob.type != "MESH" or any(c.name in skip_colls for c in ob.users_collection) or ob.hide_render


def cast(o, d, dist):
    hit, loc, nor, idx, ob, mx = sc.ray_cast(dg, o, d, distance=dist)
    while hit and ignored(ob):
        o2 = loc + d * 1e-4
        dist -= (o2 - o).length
        if dist <= 0:
            return None
        hit, loc, nor, idx, ob, mx = sc.ray_cast(dg, o2, d, distance=dist)
        o = o2
    return (loc, ob) if hit else None


dirs = [Vector((x, y, z)).normalized() for x in (-1, 0, 1) for y in (-1, 0, 1) for z in (-1, 0, 1) if (x, y, z) != (0, 0, 0)]
CLEAR = 0.20      # metres of free space required around the lens
report = []
for shot in order:
    if shot["kind"] != "dolly":
        report.append((shot["name"], "overview", "", "", "n/a (outside the building, cut-away view)"))
        continue
    smp = sample_shot(shot, shot_frames(shot))
    worst, worst_ob, path_hits, view_min = 9e9, "", [], 9e9
    for i, (p, rot, shift) in enumerate(smp):
        for d in dirs:
            h = cast(p, d, CLEAR)
            if h:
                dd = (h[0] - p).length
                if dd < worst:
                    worst, worst_ob = dd, h[1].name
        if i:
            seg = p - smp[i - 1][0]
            if seg.length > 1e-6:
                h = cast(smp[i - 1][0], seg.normalized(), seg.length + 0.05)
                if h:
                    path_hits.append(h[1].name)
        fwd = (rot_m := bpy.data.objects["WT_" + shot["name"]].matrix_world)  # noqa: F841 (placeholder)
    # view check at first / last frame: distance to the first surface straight ahead
    for p, rot, shift in (smp[0], smp[-1]):
        from mathutils import Euler
        fwd = Euler(rot).to_matrix() @ Vector((0, 0, -1))
        h = cast(p, fwd, 50)
        if h:
            view_min = min(view_min, (h[0] - p).length)
    status = "PASS" if worst == 9e9 and not path_hits and view_min > 1.0 else "CHECK"
    report.append((shot["name"], status, "none" if worst == 9e9 else f"{worst:.2f} m to {worst_ob}",
                   ", ".join(sorted(set(path_hits))) or "none", f"{view_min:.1f} m"))
with open(os.path.join(REPORT_DIR, "camera_collision_check.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["shot", "result", f"geometry within {CLEAR:.2f} m of the lens", "geometry crossed by the path", "free view ahead (min)"])
    w.writerows(report)
for r in report:
    print("COLLISION", *r)
for o in over:   # restore keyed state of frame 1
    o.hide_render = False
sc.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND, compress=False)
print("SAVED", OUT_BLEND, "frames", sc.frame_end)
