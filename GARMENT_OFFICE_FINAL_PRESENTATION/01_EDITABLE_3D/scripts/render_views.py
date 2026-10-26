"""Render camera views from Final_Office_Interior.blend (sequential, one Blender process).

blender -b MODEL.blend --python render_views.py -- --out DIR [--cams A,B | --priority 1] [--quality preview|final|custom]
        [--engine cycles|workbench] [--res 1600x900] [--samples 128] [--exposure 0.0] [--suffix _x]
Writes PNG + a JPEG copy, appends timing to DIR/render_log.csv.
"""
import csv
import json
import os
import sys
import time

import bpy

A = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def arg(k, d=None):
    return A[A.index(k) + 1] if k in A else d


OUT = os.path.abspath(arg("--out", "renders"))
QUALITY = arg("--quality", "preview")
ENGINE = arg("--engine", "cycles")
SUFFIX = arg("--suffix", "")
os.makedirs(OUT, exist_ok=True)
sc = bpy.context.scene

PRESETS = {"preview": dict(res=(960, 540), samples=24, thr=0.05), "final": dict(res=(1600, 900), samples=128, thr=0.02),
           "hero": dict(res=(1920, 1080), samples=192, thr=0.015)}
P = dict(PRESETS.get(QUALITY, PRESETS["preview"]))
if arg("--res"):
    P["res"] = tuple(int(v) for v in arg("--res").split("x"))
if arg("--samples"):
    P["samples"] = int(arg("--samples"))

cams = [o for o in bpy.data.objects if o.type == "CAMERA"]
if arg("--cams"):
    want = arg("--cams").split(",")
    cams = [c for w in want for c in cams if c.name == w or c.name.startswith(w)]
elif arg("--priority"):
    cams = [c for c in cams if c.get("priority") == arg("--priority") and c.data.type != "ORTHO"]
cams = sorted(cams, key=lambda c: c.name)


def coll_hide(names, hide):
    for n in names:
        c = bpy.data.collections.get(n)
        if c:
            c.hide_render = hide


def overhead(hide):
    """Cutaway for plan / isometric views: no deck, beams, ceiling elements, fixtures, AC units."""
    for ob in bpy.data.objects:
        if ob.name.startswith("Steel deck"):
            ob.hide_render = hide
    coll_hide(["Beams", "Ceilings", "Light Fixtures", "MEP_Fire_Safety"], hide)


def setup_engine(cam):
    ortho = cam.data.type == "ORTHO"
    if ENGINE == "workbench":
        sc.render.engine = "BLENDER_WORKBENCH"
        sh = sc.display.shading
        sh.light, sh.color_type = "STUDIO", "TEXTURE"
        sh.show_cavity, sh.cavity_type = True, "BOTH"
        sh.show_object_outline = True
        sh.object_outline_color = (0.2, 0.2, 0.2)
        sh.show_shadows = True
        sh.shadow_intensity = 0.35
        sc.display.render_aa = "8"
        sc.view_settings.view_transform = "Standard"
        sc.view_settings.look = "None"
    else:
        sc.render.engine = "CYCLES"
        cy = sc.cycles
        cy.device = "CPU"
        cy.samples = P["samples"]
        cy.use_adaptive_sampling = True
        cy.adaptive_threshold = P["thr"]
        cy.use_denoising = True
        cy.max_bounces, cy.diffuse_bounces, cy.glossy_bounces = 8, 3, 3
        cy.transmission_bounces, cy.transparent_max_bounces = 8, 8
        cy.sample_clamp_indirect = 8.0
        cy.blur_glossy = 1.0
        sc.render.use_persistent_data = True
        sc.view_settings.view_transform = "AgX"
        try:
            sc.view_settings.look = "AgX - Base Contrast"
        except Exception:
            pass
        sc.view_settings.exposure = float(arg("--exposure", cam.get("exposure") or "0.6"))
    sc.render.film_transparent = False


def main():
    log_path = os.path.join(OUT, "render_log.csv")
    new = not os.path.exists(log_path)
    status = []
    with open(log_path, "a", newline="") as f:
        wr = csv.writer(f)
        if new:
            wr.writerow(["camera", "engine", "quality", "res", "samples", "seconds", "file"])
        for cam in cams:
            ortho = cam.data.type == "ORTHO"
            overhead(ortho)
            coll_hide(["Labels"], not (ortho and cam.name == "CAM_TOP_Plan" and "--labels" in A))
            setup_engine(cam)
            res = P["res"]
            if ortho and cam.name == "CAM_TOP_Plan":
                res = (int(res[0] * 1.0), int(res[0] * 1.3))      # portrait plan
            sc.render.resolution_x, sc.render.resolution_y = res
            sc.render.resolution_percentage = 100
            sc.camera = cam
            path = os.path.join(OUT, f"{cam.name}{SUFFIX}.png")
            sc.render.filepath = path
            sc.render.image_settings.file_format = "PNG"
            t = time.time()
            bpy.ops.render.render(write_still=True)
            dt = time.time() - t
            try:
                img = bpy.data.images.load(path)
                img.file_format = "JPEG"
                sc.render.image_settings.file_format = "JPEG"
                sc.render.image_settings.quality = 92
                img.save_render(path[:-4] + ".jpg", scene=sc)
                sc.render.image_settings.file_format = "PNG"
            except Exception as e:
                print("jpeg copy failed", e)
            wr.writerow([cam.name, ENGINE, QUALITY, f"{res[0]}x{res[1]}", P["samples"] if ENGINE == "cycles" else "", round(dt, 1), path])
            f.flush()
            print(f"RENDERED {cam.name} {res} in {dt:.1f}s -> {path}", flush=True)
            status.append(dict(camera=cam.name, seconds=round(dt, 1), file=path))
            overhead(False)
    with open(os.path.join(OUT, f"render_status_{int(time.time())}.json"), "w") as f:
        json.dump(status, f, indent=1)


main()
