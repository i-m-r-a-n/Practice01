"""Title graphics for the walkthrough videos (PNG, 1920 x 1080), drawn with Pillow from the approved project assets only
(client logos and tagline cropped from the client's business card / company profile; project name and address as in the
approved presentation).
python3 make_titles.py OUT_DIR
- title_card.png      opening card (logos, project title, "proposed interior design visualization")
- closing_card.png    closing card (logos, companies, address, tagline, disclaimer)
- opening_overlay.png transparent overlay with the project title for the opening orbit
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = os.path.abspath(sys.argv[1])
os.makedirs(OUT, exist_ok=True)
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "GARMENT_OFFICE_FINAL_PRESENTATION", "03_PRESENTATION", "assets"))
FONT = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
W, H = 1920, 1080
GREEN, DARK, MINT, PAPER = (38, 103, 61), (15, 30, 21), (159, 211, 176), (246, 243, 238)
TITLE = "Premium International Fashion Corporate Headquarters & Design Development Centre"
COMPANIES = "Stage II Knitting Apparel Ltd.  ·  Stage II Knitting Apparel Unit-1  ·  Zara Fashion"
ADDRESS = "Holding 329/2, Ward 15, Vogra, Bason, Gazipur"


def font(weight, size):
    return ImageFont.truetype(FONT.format(weight), size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + [cur]


def logo_plate(height=74):
    logos = [Image.open(os.path.join(ASSETS, f)).convert("RGBA") for f in
             ("logo_zara_fashion_profile.png", "logo_stage2_ltd.png", "logo_stage2_unit1.png")]
    hs = [height, int(height * 0.8), int(height * 0.8)]
    logos = [lg.resize((int(lg.width * h / lg.height), h), Image.LANCZOS) for lg, h in zip(logos, hs)]
    pad, gap = 22, 34
    plate = Image.new("RGBA", (sum(lg.width for lg in logos) + gap * 2 + pad * 2, height + pad * 2), (255, 255, 255, 255))
    x = pad
    for lg, h in zip(logos, hs):
        plate.alpha_composite(lg, (x, pad + (height - h) // 2))
        x += lg.width + gap
    return plate


def background():
    bg = Image.new("RGB", (W, H), DARK)
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse((W * 0.25, H * 0.05, W * 1.15, H * 1.25), fill=120)
    glow = glow.filter(ImageFilter.GaussianBlur(220))
    return Image.composite(Image.new("RGB", (W, H), (34, 72, 48)), bg, glow).convert("RGBA")


def centred(draw, y, text, fnt, fill):
    draw.text(((W - draw.textlength(text, font=fnt)) / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- opening card
img = background()
d = ImageDraw.Draw(img)
plate = logo_plate(78)
img.alpha_composite(plate, ((W - plate.width) // 2, 210))
f_eye, f_title, f_sub = font("SemiBold", 24), font("SemiBold", 62), font("Regular", 30)
centred(d, 410, "INTERIOR DESIGN PROPOSAL  |  GROUND FLOOR", f_eye, MINT)
y = 465
for line in wrap(d, TITLE, f_title, 1500):
    centred(d, y, line, f_title, (255, 255, 255))
    y += 78
centred(d, y + 34, COMPANIES, f_sub, (217, 226, 220))
centred(d, y + 82, ADDRESS, f_sub, (190, 205, 196))
centred(d, H - 120, "Architectural walkthrough of the proposed design  ·  rendered from the project's 3D model", font("Regular", 24), (167, 179, 171))
img.convert("RGB").save(os.path.join(OUT, "title_card.png"))

# ---------------------------------------------------------------- closing card
img = background()
d = ImageDraw.Draw(img)
plate = logo_plate(70)
img.alpha_composite(plate, ((W - plate.width) // 2, 200))
y = 380
for line in wrap(d, TITLE, font("SemiBold", 52), 1500):
    centred(d, y, line, font("SemiBold", 52), (255, 255, 255))
    y += 66
centred(d, y + 30, COMPANIES, font("Regular", 28), (217, 226, 220))
centred(d, y + 74, ADDRESS, font("Regular", 28), (190, 205, 196))
tag = Image.open(os.path.join(ASSETS, "tagline_quality_compliance_commitment.png")).convert("RGBA") if os.path.exists(
    os.path.join(ASSETS, "tagline_quality_compliance_commitment.png")) else None
if tag:
    tag = tag.resize((int(tag.width * 46 / tag.height), 46), Image.LANCZOS)
    tp = Image.new("RGBA", (tag.width + 36, tag.height + 20), (255, 255, 255, 255))
    tp.alpha_composite(tag, (18, 10))
    img.alpha_composite(tp, ((W - tp.width) // 2, y + 150))
centred(d, H - 150, "Proposed interior visualization. Final dimensions and technical details subject to site verification.",
        font("Regular", 23), (167, 179, 171))
centred(d, H - 112, "Rendered from the project's 3D model - not a photograph of a completed space. Furniture is generic.", font("Regular", 23), (167, 179, 171))
img.convert("RGB").save(os.path.join(OUT, "closing_card.png"))

# ---------------------------------------------------------------- opening overlay (over the orbit)
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
grad = Image.new("L", (W, 520), 0)
gd = ImageDraw.Draw(grad)
for i in range(520):
    gd.line([(0, i), (W, i)], fill=int(236 * min(1.0, i / 330) ** 0.9))
shade = Image.new("RGBA", (W, 520), (8, 14, 10, 255))
shade.putalpha(grad)
ov.alpha_composite(shade, (0, H - 520))
d = ImageDraw.Draw(ov)
d.text((96, H - 268), "THE COMPLETE GROUND FLOOR", font=font("SemiBold", 24), fill=MINT)
yy = H - 228
for line in wrap(d, TITLE, font("SemiBold", 50), 1300):
    d.text((96, yy), line, font=font("SemiBold", 50), fill=(255, 255, 255))
    yy += 62
d.text((96, yy + 12), COMPANIES, font=font("Regular", 26), fill=(217, 226, 220))
ov.save(os.path.join(OUT, "opening_overlay.png"))
print("titles written to", OUT)
