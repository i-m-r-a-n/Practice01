"""Index of the rendered images -> 02_RENDERED_IMAGES/README.md and 02_RENDERED_IMAGES/final_contact_sheet.jpg
python3 make_render_index.py PROJECT_ROOT
Lists every camera of cameras.py with its final render (from final/render_log.csv) or preview, and the drawings."""
import csv
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
sys.path.insert(0, os.path.join(ROOT, "01_EDITABLE_3D", "scripts"))
import cameras as C  # noqa: E402

IMG = os.path.join(ROOT, "02_RENDERED_IMAGES")
FINAL, PREV, PLANS = (os.path.join(IMG, d) for d in ("final", "previews", "plans"))
log = {}
if os.path.exists(os.path.join(FINAL, "render_log.csv")):
    with open(os.path.join(FINAL, "render_log.csv")) as f:
        for r in csv.DictReader(f):
            if os.path.exists(os.path.join(FINAL, r["camera"] + ".jpg")):
                log[r["camera"]] = r                       # last row of a camera = its current image

rows, finals, secs = [], [], 0.0
for c in C.CAMERAS:
    n = c["name"]
    fin = log.get(n)
    prev = os.path.exists(os.path.join(PREV, n + ".jpg"))
    if fin:
        finals.append((n, c["room"]))
        secs += float(fin["seconds"])
    rows.append((n, c["room"], c["priority"], f"{fin['res']}, {fin['samples']} samples, {float(fin['seconds']):.0f} s" if fin else "-",
                 "yes" if prev else "-"))

lines = ["# Rendered images", "",
         "All images are Blender Cycles renders of this project's model (`01_EDITABLE_3D/Final_Office_Interior.blend`), except the",
         "drawings in `plans/`, which are drawn from the same survey and layout data. Nothing here is a stock or AI-generated image.", "",
         "| Folder | Contents |", "|---|---|",
         f"| `final/` | final renders: PNG (lossless) + JPG copy; `render_log.csv` has the time of each render |",
         "| `previews/` | 960 x 540 preview renders of the 33 interior views |",
         "| `plans/` | drawings ID-01 to ID-04 (SVG, PNG, A3 PDF) |",
         "| `material_board.jpg` | the model's PBR materials rendered in Blender |",
         "| `BENCHMARK_Reception_1600x900_128spp_381s.jpg` | render-time benchmark (reception, 1600 x 900, 128 samples, 381.5 s) |",
         "| `final_contact_sheet.jpg` | all final renders on one sheet |", "",
         f"Final renders: {len(finals)} of {len(C.CAMERAS)} views, total render time {secs / 3600:.1f} h on 4 CPU cores. "
         "Views without a final render have a preview only.", "",
         "| Camera | Room / view | Priority | Final render | Preview |", "|---|---|---|---|---|"]
lines += [f"| `{n}` | {room} | {pr} | {fin} | {pv} |" for n, room, pr, fin, pv in rows]
lines += ["", "## Drawings (`plans/`)", ""]
for f in sorted(os.listdir(PLANS)) if os.path.isdir(PLANS) else []:
    if f.endswith(".pdf"):
        lines.append(f"- `{f[:-4]}` (.svg / .png / A3 .pdf)")
with open(os.path.join(IMG, "README.md"), "w") as f:
    f.write("\n".join(lines) + "\n")

# contact sheet of the final renders
if finals:
    tw, th, cols, pad, lab = 480, 270, 4, 12, 30
    rws = (len(finals) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + pad) + pad, rws * (th + lab + pad) + pad), (246, 243, 238))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 15)
    except OSError:
        font = ImageFont.load_default()
    for i, (n, room) in enumerate(finals):
        im = Image.open(os.path.join(FINAL, n + ".jpg")).convert("RGB")
        im.thumbnail((tw, th))
        x, y = pad + (i % cols) * (tw + pad), pad + (i // cols) * (th + lab + pad)
        sheet.paste(im, (x + (tw - im.width) // 2, y + (th - im.height) // 2))
        d.text((x, y + th + 6), f"{n}  |  {room}"[:62], fill=(40, 40, 36), font=font)
    sheet.save(os.path.join(IMG, "final_contact_sheet.jpg"), quality=86)
print(f"index: {len(finals)} finals of {len(C.CAMERAS)} views, {secs / 3600:.2f} h")
