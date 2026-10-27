"""Render book: every final render on its own A3 landscape page (cover, contents, 38 views, notes).
python3 make_render_book.py PROJECT_ROOT   ->  03_PRESENTATION/Garment_Office_Render_Book.html
PDF: node export_render_book.js PROJECT_ROOT/03_PRESENTATION
Uses only 02_RENDERED_IMAGES/final/<camera>.jpg (Blender Cycles renders of this project's model), shown uncropped.
"""
import csv
import html
import os
import sys

from PIL import Image

ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
OUT = os.path.join(ROOT, "03_PRESENTATION")
FINAL = os.path.join(ROOT, "02_RENDERED_IMAGES", "final")
E = html.escape

# (group, [(camera, title, description)]) - descriptions say only what the render shows
BOOK = [
    ("Whole floor", [
        ("CAM_TOP_Plan", "Whole floor from above", "Top view of the furnished ground floor with the deck, beams and ceilings removed."),
        ("CAM_ISO_SE", "Whole floor from the south-east", "Cut-away isometric view of the furnished floor."),
        ("CAM_ISO_SW", "Whole floor from the south-west", "Cut-away isometric view of the furnished floor."),
        ("CAM_ISO_Front_Zone", "Visitor zone", "Lobby, reception, experience centre, boardroom and executive suite."),
        ("CAM_ISO_Design_Wing", "Design wing and staff support", "Global Design Studio, sample room, corridors, staff cafe and lounge."),
    ]),
    ("Entrance and reception", [
        ("CAM_03_Entrance_Lobby", "Entrance lobby", "Security desk and the brand wall: the group's three logos and tagline on vertical oak slats."),
        ("CAM_01_Reception_A", "Reception and visitor lounge", "Fluted white-oak counter, logo wall, waiting lounge under an oak slat raft and a brass halo."),
        ("CAM_02_Reception_B", "Reception desk and logo wall", "Terrazzo-topped counter with a brass edge; glass view into the experience centre."),
    ]),
    ("Experience centre", [
        ("CAM_04_Experience_Centre_A", "Experience centre", "Mannequin plinth, garment bays with green backs and lit shelves, track lights fixed to the beams."),
        ("CAM_05_Experience_Centre_B", "Experience centre - brand-story wall", "Logos and tagline on the story wall, touch table and garment bays; boardroom behind the glass."),
        ("CAM_06_Experience_Centre_Detail", "Experience centre - display detail", "Dress forms in front of the garment bays."),
    ]),
    ("Executive suite", [
        ("CAM_07_MD_Office_A", "Managing Director's office", "Walnut feature wall with the company logo, walnut desk, cognac leather chair and lounge corner."),
        ("CAM_08_MD_Office_B", "MD office - lounge corner", "Sofa and lounge chair under the brass halo; glass to the director's office and executive corridor."),
        ("CAM_17_Executive_Reception", "Executive reception (PA)", "PA desk and executive waiting chairs."),
        ("CAM_18_Director", "Director's office", "Desk, credenza and visitor chairs; glass partition to the MD office."),
        ("CAM_31_Executive_Corridor", "Executive corridor", "Oak slat wall, glass fronts with brass pulls, herringbone oak floor."),
    ]),
    ("Meeting rooms", [
        ("CAM_09_Boardroom_A", "Boardroom", "15 seats at a walnut table, green felt rafts between the beams, screen on the media wall, glass to the experience centre."),
        ("CAM_10_Boardroom_B", "Boardroom - towards the east", "Walnut acoustic slats on the right; the experience centre behind the glass on the left."),
        ("CAM_27_Audit_Room", "Audit room", "Meeting table for six."),
    ]),
    ("Workspaces", [
        ("CAM_11_Merchandising_A", "Merchandising open office", "Bench desks, team table, grey and green felt baffles between the beams."),
        ("CAM_12_Merchandising_B", "Merchandising - team table", "Team table with green chairs, pinboard wall and bench desks."),
        ("CAM_16_Commercial_Accounts", "Commercial & accounts", "Open office with bench workstations in the same desk family as merchandising."),
        ("CAM_19_HR_Admin", "HR & admin", "Desks and a round interview table behind glass partitions."),
        ("CAM_26_Guest_Workspace", "Guest workspace", "Table for six with a whiteboard."),
    ]),
    ("Design development", [
        ("CAM_13_Design_Studio_A", "Global Design Studio", "Buyer presentation table, collection display and designer desks by the east windows."),
        ("CAM_14_Design_Studio_B", "Design studio - workstations and mood board", "Oak designer benches and the mood-board wall."),
        ("CAM_15_CAD_Room", "CAD / technical design", "Dual-screen desks, plotter, layout table and a green felt pinboard for tech packs."),
        ("CAM_23_Sample_Room", "Sample development", "Dress forms, sample machines and a cutting table."),
        ("CAM_24_3D_Printing_Lab", "3D printing lab", "3D printers on a work counter; window to the merchandising office."),
        ("CAM_25_Fabric_Library", "Fabric, colour & trim library", "Colour booth on the work table, display bay and shelving."),
        ("CAM_32_Design_Corridor", "Design wing corridor", "Glass-lined corridor between the design rooms."),
    ]),
    ("Staff support", [
        ("CAM_20_Staff_Cafe", "Staff cafe and pantry", "Dining tables with green chairs, opal pendants, pantry counter with fridge and water dispenser."),
        ("CAM_21_Lounge_Training", "Staff lounge / training", "Sofa group and workshop table with a screen."),
        ("CAM_22_Prayer_Male", "Prayer room (male)", "Green prayer carpet with row lines, bookshelf, soft 3000 K light."),
        ("CAM_33_Wudu_Male", "Wudu (male)", "Wudu station with seats, tiled walls."),
        ("CAM_30_Prayer_Female", "Prayer room (female)", "Green prayer carpet with row lines and a bookshelf."),
        ("CAM_28_Washroom_Male", "Staff washroom (male)", "Vanity, urinals and WC cubicle, porcelain tiles."),
        ("CAM_29_Washroom_Female", "Staff washroom (female)", "Vanity with two basins and WC cubicles, porcelain tiles."),
    ]),
]
VIEWS = [(g, c, t, d) for g, items in BOOK for c, t, d in items]
log = {r["camera"]: r for r in csv.DictReader(open(os.path.join(FINAL, "render_log.csv")))}
missing = [c for _, c, _, _ in VIEWS if not os.path.exists(os.path.join(FINAL, c + ".jpg"))]
assert not missing, f"missing final renders: {missing}"
assert len(VIEWS) == len({c for _, c, _, _ in VIEWS}) == 38
N_PAGES = len(VIEWS) + 3
FOOT = "STAGE II KNITTING APPAREL / ZARA FASHION &nbsp;|&nbsp; Ground-floor corporate office - interior design proposal"

CSS = """
@page { size: 420mm 297mm; margin: 0 }
* { box-sizing: border-box }
html, body { margin: 0; padding: 0; background: #F6F3EE }
body { font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif; color: #1E1E1C }
.page { width: 420mm; height: 297mm; position: relative; overflow: hidden; background: #F6F3EE; page-break-after: always; break-after: page }
.head { position: absolute; left: 12mm; right: 12mm; top: 7mm; display: flex; justify-content: space-between; font-size: 8.5pt;
        letter-spacing: .14em; text-transform: uppercase; color: #6B675F }
.head b { color: #26673D; font-weight: 600 }
.foot { position: absolute; left: 12mm; right: 12mm; bottom: 6.5mm; display: flex; justify-content: space-between; font-size: 8pt; color: #8A867E }
.foot b { color: #26673D; font-weight: 600 }
.img { position: absolute; display: flex; align-items: center; justify-content: center }
.img img { max-width: 100%; max-height: 100%; display: block }
.num { font-size: 30pt; font-weight: 600; color: #26673D; line-height: 1 }
.grp { font-size: 8.5pt; letter-spacing: .16em; text-transform: uppercase; color: #26673D; font-weight: 600 }
.title { font-size: 17pt; font-weight: 600; margin-top: 1.5mm }
.desc { font-size: 10.5pt; color: #3A3935; margin-top: 1.5mm; line-height: 1.4 }
.meta { font-size: 8pt; color: #8A867E; margin-top: 2mm }
.cap { position: absolute; display: flex; gap: 7mm; align-items: flex-start }
.thumbs { position: absolute; left: 12mm; top: 33mm; right: 12mm; display: grid; grid-template-columns: repeat(7, 1fr); gap: 4.5mm 4mm }
.thumb .box { height: 30mm; background: #E4DFD6; display: flex; align-items: center; justify-content: center; overflow: hidden }
.thumb .box img { max-width: 100%; max-height: 100%; display: block }
.thumb .lab { font-size: 7pt; color: #3A3935; margin-top: 1.2mm; line-height: 1.25 }
.thumb .lab b { color: #26673D }
"""


def meta(cam):
    r = log.get(cam, {})
    res = r.get("res", "").replace("x", " x ")
    return f"Blender Cycles render of the project model, {res} px" if res else "Blender Cycles render of the project model"


def page_view(i, group, cam, title, desc):
    w, h = Image.open(os.path.join(FINAL, cam + ".jpg")).size
    src = f"../02_RENDERED_IMAGES/final/{cam}.jpg"
    num = f'<div class="num">{i:02d}</div>'
    text = (f'<div><div class="grp">{E(group)}</div><div class="title">{E(title)}</div><div class="desc">{E(desc)}</div>'
            f'<div class="meta">{E(meta(cam))} &nbsp;|&nbsp; view {E(cam)}</div></div>')
    if w / h < 1.2:      # portrait (top view): image left, caption right
        body = (f'<div class="img" style="left:12mm;top:16mm;width:230mm;height:266mm"><img src="{src}"></div>'
                f'<div class="cap" style="left:252mm;top:30mm;width:150mm;flex-direction:column">{num}{text}</div>')
    else:
        body = (f'<div class="img" style="left:12mm;top:16mm;width:396mm;height:227mm"><img src="{src}"></div>'
                f'<div class="cap" style="left:12mm;top:249mm;width:396mm">{num}{text}</div>')
    return (f'<section class="page"><div class="head"><span><b>Rendered views</b></span><span>{E(group)}</span></div>{body}'
            f'<div class="foot"><span><b>{FOOT}</b></span><span>{i + 2:02d} / {N_PAGES}</span></div></section>')


cover = (
    '<section class="page" style="background:#14241B">'
    '<div class="img" style="left:0;top:0;width:420mm;height:297mm"><img src="../02_RENDERED_IMAGES/final/CAM_05_Experience_Centre_B.jpg" '
    'style="width:420mm;height:297mm;max-width:none;max-height:none;object-fit:cover"></div>'
    '<div style="position:absolute;inset:0;background:linear-gradient(90deg,rgba(15,30,21,.94) 0%,rgba(15,30,21,.82) 40%,rgba(15,30,21,0) 72%)"></div>'
    '<div style="position:absolute;left:18mm;top:16mm;background:#fff;border-radius:1mm;display:flex;align-items:center;gap:7mm;padding:4mm 6mm">'
    '<img src="assets/logo_zara_fashion_profile.png" style="height:15mm"><img src="assets/logo_stage2_ltd.png" style="height:12mm">'
    '<img src="assets/logo_stage2_unit1.png" style="height:12mm"></div>'
    '<div style="position:absolute;left:18mm;top:78mm;width:200mm;color:#F3F0EA">'
    '<div class="grp" style="color:#9FD3B0;font-size:11pt">Rendered views &nbsp;|&nbsp; Ground floor</div>'
    '<div style="font-size:34pt;font-weight:600;line-height:1.08;margin-top:5mm;color:#fff">Premium International Fashion Corporate '
    'Headquarters &amp; Design Development Centre</div>'
    '<div style="font-size:13pt;color:#D9E2DC;margin-top:8mm">Stage II Knitting Apparel Ltd. &middot; Stage II Knitting Apparel Unit-1 &middot; Zara Fashion</div>'
    '<div style="font-size:13pt;color:#D9E2DC;margin-top:2mm">Holding 329/2, Ward 15, Vogra, Bason, Gazipur</div>'
    f'<div style="font-size:11pt;color:#A7B3AB;margin-top:10mm">{len(VIEWS)} views &middot; Blender Cycles renders of the project&#39;s 3D model &middot; October 2026</div>'
    '</div>'
    '<div style="position:absolute;right:12mm;bottom:7mm;font-size:8pt;color:#C9D3CC">Cover: experience centre, brand-story wall (render)</div>'
    '</section>')

cells = "".join(
    f'<div class="thumb"><div class="box"><img src="../02_RENDERED_IMAGES/final/{c}.jpg"></div>'
    f'<div class="lab"><b>{i:02d}</b> {E(t)}</div></div>' for i, (g, c, t, d) in enumerate(VIEWS, 1))
groups = " &nbsp;&middot;&nbsp; ".join(
    f"<b>{VIEWS.index(next(v for v in VIEWS if v[0] == g)) + 1:02d}</b> {E(g)}" for g, _ in BOOK)
contents = (
    '<section class="page"><div class="head"><span><b>Rendered views</b></span><span>Contents</span></div>'
    '<div style="position:absolute;left:12mm;top:15mm;right:12mm"><div style="font-size:20pt;font-weight:600">Contents</div>'
    f'<div style="font-size:9pt;color:#3A3935;margin-top:2mm">{groups}</div></div>'
    f'<div class="thumbs">{cells}</div>'
    f'<div class="foot"><span><b>{FOOT}</b></span><span>02 / {N_PAGES}</span></div></section>')

notes_items = [
    f"All {len(VIEWS)} images are Blender 5.2 Cycles renders of this project's 3D model (01_EDITABLE_3D/Final_Office_Interior.blend), "
    "not photographs. Materials and plants use CC0 textures and models listed in 01_EDITABLE_3D/assets/LICENSES.md; no stock photos "
    "or AI-generated images are used.",
    "Resolution and samples of every view are listed in 02_RENDERED_IMAGES/final/render_log.csv; the PNG files in the same folder are the lossless originals.",
    "Furniture is parametric and generic (no specific manufacturer). Screens, garments, mood-board cards and book spines are neutral "
    "placeholder colours, not real products or content.",
    "Views through the windows show a sky model, not the real surroundings.",
    "Floor-to-deck height (114 in, estimated from photos), the width of room 8 and the column and beam positions are provisional until "
    "measured on site (04_DOCUMENTATION/unresolved_issues.md).",
    "\"Global Design Studio\" is the name proposed in the master plan, used here for wayfinding only.",
    "Interior design proposal - not for construction.",
]
notes = (
    '<section class="page"><div class="head"><span><b>Rendered views</b></span><span>Notes</span></div>'
    '<div style="position:absolute;left:12mm;top:30mm;width:260mm"><div style="font-size:20pt;font-weight:600">About these images</div>'
    '<ul style="margin:8mm 0 0;padding-left:6mm">'
    + "".join(f'<li style="font-size:11.5pt;line-height:1.5;color:#3A3935;margin-bottom:3mm">{E(t)}</li>' for t in notes_items)
    + '</ul></div>'
    f'<div class="foot"><span><b>{FOOT}</b></span><span>{N_PAGES:02d} / {N_PAGES}</span></div></section>')

doc = (f'<!doctype html><html><head><meta charset="utf-8"><title>Garment Office Render Book</title><style>{CSS}</style></head><body>'
       + cover + contents + "".join(page_view(i, *v) for i, v in enumerate(VIEWS, 1)) + notes + "</body></html>")
with open(os.path.join(OUT, "Garment_Office_Render_Book.html"), "w") as f:
    f.write(doc)
print("render book:", len(VIEWS), "views,", N_PAGES, "pages")
