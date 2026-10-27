"""Before / after sheets and a contact sheet from the Cycles renders (same saved cameras, same quality preset).
python3 -I make_comparisons.py   (run from this folder)
before: GARMENT_OFFICE_FINAL_PRESENTATION/02_RENDERED_IMAGES/final/CAM_xx.jpg (approved design, untouched)
after:  after_no_people/ (matched comparison) and after_with_people/ (same cameras with illustrative staff)
"""
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BEFORE = os.path.join(HERE, "..", "..", "GARMENT_OFFICE_FINAL_PRESENTATION", "02_RENDERED_IMAGES", "final")
CLEAN, PEOPLE = os.path.join(HERE, "after_no_people"), os.path.join(HERE, "after_with_people")
OUT = os.path.join(HERE, "comparisons")
os.makedirs(OUT, exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    try:
        return ImageFont.truetype(BOLD if bold else FONT, size)
    except OSError:
        return ImageFont.load_default()


def tile(path, w):
    im = Image.open(path).convert("RGB")
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


def label(im, text, sub=None):
    d = ImageDraw.Draw(im)
    f, fs = font(26, True), font(17)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle((14, 14, 34 + max(tw, d.textlength(sub or "", font=fs)), 58 + (24 if sub else 0)), 8, fill=(18, 25, 21))
    d.text((24, 20), text, font=f, fill=(246, 243, 238))
    if sub:
        d.text((24, 54), sub, font=fs, fill=(185, 196, 189))
    return im


ROOMS = [("CAM_11_Merchandising_A", "Merchandising, saved camera CAM_11"), ("CAM_12_Merchandising_B", "Merchandising, saved camera CAM_12"),
         ("CAM_16_Commercial_Accounts", "Commercial & accounts, saved camera CAM_16")]
NOTE = "Proposed revised concept (option B). Same camera, same Cycles settings. People shown are illustrative."


def pair(cam, title, after_dir, suffix, sub):
    a, b = os.path.join(BEFORE, cam + ".jpg"), os.path.join(after_dir, cam + ".jpg")
    if not (os.path.exists(a) and os.path.exists(b)):
        print("skip", cam, suffix)
        return None
    w = 1200
    A, B = label(tile(a, w), "BEFORE  approved design"), label(tile(b, w), "AFTER  proposed option B", sub)
    sheet = Image.new("RGB", (2 * w + 30, A.height + 110), (12, 17, 14))
    sheet.paste(A, (10, 80)); sheet.paste(B, (w + 20, 80))
    d = ImageDraw.Draw(sheet)
    d.text((12, 18), title, font=font(30, True), fill=(246, 243, 238))
    d.text((12, sheet.height - 28), NOTE, font=font(16), fill=(185, 196, 189))
    p = os.path.join(OUT, f"before_after_{cam}{suffix}.jpg")
    sheet.save(p, quality=88)
    print("wrote", p)
    return p


for cam, title in ROOMS:
    pair(cam, title, CLEAN, "", None)
    pair(cam, title, PEOPLE, "_with_people", "with illustrative staff")

# contact sheet: every after view (people versions where they exist) + the plan / cutaway views
views = ["CAM_11_Merchandising_A", "CAM_12_Merchandising_B", "CAM_34_Merchandising_Sample_Hub", "CAM_35_Merchandising_Desks",
         "CAM_16_Commercial_Accounts", "CAM_36_Accounts_Suite", "CAM_37_Accounts_Records_Discussion", "CAM_38_Accounts_Public_Corridor",
         "CAM_TOP_Z06_Z07", "CAM_ISO_Z06_Z07"]
cells = []
for v in views:
    p = next((os.path.join(d, v + ".jpg") for d in (PEOPLE, CLEAN) if os.path.exists(os.path.join(d, v + ".jpg"))), None)
    if p:
        cells.append((v, p))
cw, cols = 620, 2
ims = []
for v, p in cells:
    im = tile(p, cw)
    if im.height > 349:
        im = im.crop((0, (im.height - 349) // 2, cw, (im.height - 349) // 2 + 349))
    ims.append(label(im, v.replace("CAM_", "").replace("_", " ")))
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * cw + (cols + 1) * 10, rows * 359 + 120), (12, 17, 14))
d = ImageDraw.Draw(sheet)
d.text((12, 16), "Z07 Merchandising + Z06 Commercial & Accounts - proposed option B (Cycles)", font=font(26, True), fill=(246, 243, 238))
d.text((12, 52), "Photorealistic Blender renders, still images. People shown are illustrative. Proposed revised concept, subject to site verification.",
       font=font(15), fill=(185, 196, 189))
for i, im in enumerate(ims):
    sheet.paste(im, (10 + (i % cols) * (cw + 10), 90 + (i // cols) * 359))
sheet.save(os.path.join(OUT, "contact_sheet.jpg"), quality=88)
print("contact sheet", len(ims), "views")
