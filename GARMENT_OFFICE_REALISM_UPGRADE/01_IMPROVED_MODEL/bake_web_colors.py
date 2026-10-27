"""Bakes the Blender colour nodes of the material library into base-colour textures for the web GLB.
glTF export keeps only the raw image of a textured material: the Hue/Saturation/Value node, the colour-ramp remap
(desat_to) and the tint multiply of lib_materials.textured() are lost, so e.g. the green and sand sofa fabrics and the
charcoal carpet arrive grey / light in three.js. This applies the same operations (scene-linear, as Blender does) to the
image and writes a new texture per material. It also returns the Sheen Weight of each material: the exporter wrote the
sheen tint (white) without the weight, which makes fabrics look washed out in three.js.
python3 -I bake_web_colors.py JOBS.json LIB_MATERIALS.py REPORT.json
Not reproduced (documented): the tile-joint grid and the quarter-turn carpet-tile checker (they need the room UVs).
"""
import ast
import json
import sys

import numpy as np
from PIL import Image

jobs_path, lib_path, report_path = sys.argv[1:4]


def lit(node):
    try:
        return ast.literal_eval(node)
    except ValueError:
        return None


spec, sheen = {}, {}
for node in ast.walk(ast.parse(open(lib_path).read())):
    if isinstance(node, ast.Call) and getattr(node.func, "id", None) in ("textured", "plain") and node.args:
        name = lit(node.args[0])
        kw = {k.arg: lit(k.value) for k in node.keywords}
        if kw.get("sheen"):
            if isinstance(name, str):
                sheen[name] = kw["sheen"]
            else:                                   # the garment loop: plain(k, h, ..., sheen=0.5)
                sheen["g_*"] = kw["sheen"]
        if node.func.id == "textured" and isinstance(name, str):
            spec[name] = dict(hsv=kw.get("hsv") or (0.5, 1.0, 1.0), desat_to=kw.get("desat_to"), tint=kw.get("tint"),
                              tint_mix=kw.get("tint_mix") or 0.0)


def hex_lin(h):
    c = np.array([int(h.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)])
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def to_lin(a):
    a = a / 255.0
    return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)


def to_srgb8(lin):
    lin = np.clip(lin, 0, 1)
    s = np.where(lin <= 0.0031308, lin * 12.92, 1.055 * lin ** (1 / 2.4) - 0.055)
    return np.round(s * 255).astype(np.uint8)


def rgb_to_hsv(rgb):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx, mn = rgb.max(-1), rgb.min(-1)
    d = mx - mn
    s = np.where(mx > 0, d / np.where(mx > 0, mx, 1), 0)
    nz = d > 0
    dd = np.where(nz, d, 1)
    rr = nz & (r == mx)
    gg = nz & ~rr & (g == mx)
    bb = nz & ~rr & ~gg
    h = np.zeros_like(mx)
    h = np.where(rr, ((g - b) / dd) % 6, h)
    h = np.where(gg, (b - r) / dd + 2, h)
    h = np.where(bb, (r - g) / dd + 4, h)
    return np.stack([h / 6.0, s, mx], -1)


def hsv_to_rgb(hsv):
    h, s, v = hsv[..., 0] % 1.0, hsv[..., 1], hsv[..., 2]
    i = np.floor(h * 6).astype(int) % 6
    f = h * 6 - np.floor(h * 6)
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    r = np.choose(i, [v, q, p, p, t, v])
    g = np.choose(i, [t, v, v, q, p, p])
    b = np.choose(i, [p, p, t, v, v, q])
    return np.stack([r, g, b], -1)


report = dict(baked=[], sheen=[], skipped=[])
for j in json.load(open(jobs_path)):
    m = j["material"]
    sw = sheen.get(m, sheen.get("g_*") if m.startswith("g_") else None)
    if sw:
        report["sheen"].append(dict(material=m, weight=sw))
    sp = spec.get(m)
    if not sp or not j.get("src"):
        continue
    hue, sat, val = sp["hsv"]
    if (hue, sat, val) == (0.5, 1.0, 1.0) and not sp["desat_to"] and not sp["tint_mix"]:
        report["skipped"].append(dict(material=m, reason="no colour nodes"))
        continue
    im = Image.open(j["src"]).convert("RGB")
    c = to_lin(np.asarray(im, np.float64))
    if (hue, sat, val) != (0.5, 1.0, 1.0):                     # Hue/Saturation/Value node (scene linear)
        hsv = rgb_to_hsv(c)
        hsv[..., 0] = (hsv[..., 0] + hue + 0.5) % 1.0
        hsv[..., 1] = np.clip(hsv[..., 1] * sat, 0, 1)
        hsv[..., 2] = hsv[..., 2] * val
        c = hsv_to_rgb(hsv)
    if sp["desat_to"]:                                         # RGB to BW -> colour ramp lo..hi
        bw = np.clip(c @ np.array([0.2126, 0.7152, 0.0722]), 0, 1)[..., None]
        lo, hi = hex_lin(sp["desat_to"][0]), hex_lin(sp["desat_to"][1])
        c = lo + (hi - lo) * bw
    if sp["tint"] and sp["tint_mix"]:                          # Mix (multiply) with the tint colour
        c = c * (1 - sp["tint_mix"] + sp["tint_mix"] * hex_lin(sp["tint"]))
    Image.fromarray(to_srgb8(c)).save(j["out"], "WEBP", quality=88, method=4)
    mean = to_srgb8(c.reshape(-1, 3).mean(0))
    report["baked"].append(dict(material=m, out=j["out"], ops=dict(hsv=sp["hsv"], desat_to=sp["desat_to"], tint=sp["tint"], tint_mix=sp["tint_mix"]),
                                mean_srgb="#%02X%02X%02X" % tuple(int(x) for x in mean)))
json.dump(report, open(report_path, "w"), indent=1)
print("BAKED", len(report["baked"]), "textures; sheen weights for", len(report["sheen"]), "materials")
