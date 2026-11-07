"""The Woven Earth materials board (the brief's optional diagram of materials, sources, artisans and upkeep), for the arrival gallery and
reception as built in this 3D proposal. One A4-landscape-shaped image (2480 x 1754) with a crop of each element from its Cycles render.
Honest by construction: every source, maker, test and certificate reads "to be identified" or "to be tested"; nothing is claimed.
Printed by headless Chromium from a page written next to the images.  python3 -I woven_earth_board.py OUT.jpg"""
import sys
from html import escape
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

R = Path(__file__).resolve().parents[2]
W = R / 'concept-images' / 'woven-earth'
# element, the render it is cropped from and the crop box (fractions of the image), materials, source and maker, upkeep and checks
ROWS = [
    ('The Woven Threshold', 'render_BEL_CAM_WOVEN_CLOSE.jpg', (.18, .05, .82, .78),
     'Six handwoven swags: cleaned cutting waste (jhut) in strips, with natural jute and cotton. Ecru and sand, accents of olive, indigo and a little clay; one strip mended in kantha stitch. A frame of laminated bamboo rails and straight bamboo culms on black steel rods from the deck.',
     'Jhut: traceable, cleaned and sorted by fibre and colour, with a material passport, source to be identified. Weavers: to be identified, paid and credited. Bamboo and steel: suppliers to be identified.',
     'Each swag lifts off its culm for cleaning. Fire suitability of the textile, anchors in the deck, sprinkler and detector coverage, egress and maintenance access: to be confirmed by the fire and structural engineers.'),
    ('Terracotta wall', 'render_BEL_CAM_WOVEN_TOUCH.jpg', (.28, .02, .78, .92),
     'One hand-pressed terracotta surface on the free west wall: 150 mm square tiles in lime joints; raised diamonds follow the repeat logic of Jamdani. A linear wall-washer (3000 K) on the deck draws them in light and shadow.',
     'Local fabricator: to be identified.',
     'Dusting. Tile weight, fixing and anchorage: to be checked.'),
    ('Salvaged bench and bamboo stool', 'render_BEL_CAM_WOVEN_BENCH.jpg', (.1, .05, .9, .95),
     'A salvaged hardwood slab, its end grain, checks and old fixing holes kept, a butterfly key across one check; two laminated-bamboo trestles with through-tenons, hardwood wedges and dowels. A light bamboo stool with a cane seat.',
     'Timber: legally salvaged, seasoned and documented, never fresh-felled; source and moisture content to be documented. Bamboo: verified supplier to be identified.',
     'Low-VOC oil finish, repairable fasteners. Bamboo durability, pest treatment and load test: to be done.'),
    ('One fig tree', 'render_BEL_CAM_WOVEN_REVERSE.jpg', (.08, .3, .45, 1.0),
     'One fig tree in a terracotta planter by the glass entrance, on the approved potted tree\'s footprint.',
     'Grower: to be identified.',
     'Daylight from the existing entrance glass only; watering and turning to a care schedule.'),
    ('From fibre to second life', 'render_CAM_01_Reception_A.jpg', (0.0, .42, .36, .9),
     'On the reception console, one oak tray: raw cotton, jute fibre, cutting waste sorted by colour, recycled yarn and the knit it becomes.',
     'Illustrative samples. Fibre sources and recycled shares: to be documented.',
     'Samples replaced by documented ones as records arrive.'),
]
LIGHT = ('Light: daylight only through the existing entrance glass; the approved linear lights (3500 K) and brand-wall spots (3000 K) stay; '
         'two narrow spots (3000 K) on the threshold and one linear wall-washer (3000 K) on the terracotta are the only additions.')
FOOT = ('Concept proposal on the approved Stage II floor. The geometry is locked: column grid, beams, ceiling height, glazing, doors, '
        'check-in desk, brand wall and circulation are unchanged. Final design requires architect / engineer review, local fire and '
        'building compliance, and actual contractor quotations. Images rendered from the 3D model (Blender Cycles, simulated light, no people).')


def crop(name, box):
    im = Image.open(W / name if (W / name).exists() else R / 'concept-images' / name).convert('RGB')
    x0, y0, x1, y1 = box; im = im.crop((round(x0 * im.width), round(y0 * im.height), round(x1 * im.width), round(y1 * im.height)))
    out = W / ('_crop_' + name); im.save(out, quality=88); return out


def main(dst):
    crops = [crop(r[1], r[2]) for r in ROWS]
    rows = ''.join(f"""<section class="row"><div class="pic"><img src="{c.as_uri()}" alt=""></div>
      <div class="cell name"><h2>{escape(n)}</h2></div><div class="cell"><b>Materials</b><p>{escape(m)}</p></div>
      <div class="cell"><b>Source and makers</b><p>{escape(s)}</p></div><div class="cell"><b>Upkeep and checks</b><p>{escape(u)}</p></div></section>"""
                   for c, (n, _, _, m, s, u) in zip(crops, ROWS))
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><style>
    * {{ box-sizing: border-box }}
    body {{ margin: 0; width: 2480px; height: 1754px; background: #f3efe6; color: #1d2a22; font-family: Inter, "Helvetica Neue", Arial, sans-serif; padding: 70px 90px }}
    .eyebrow {{ margin: 0; font-size: 24px; letter-spacing: .2em; text-transform: uppercase; color: #9a5a3c; font-weight: 700 }}
    h1 {{ margin: 8px 0 6px; font-size: 64px; line-height: 1.05 }}
    .lead {{ margin: 0 0 26px; font-size: 27px; color: #45534a }}
    .row {{ display: grid; grid-template-columns: 330px 300px 1fr 1fr 1fr; gap: 26px; align-items: start; padding: 18px 0; border-top: 2px solid rgba(29, 42, 34, .14) }}
    .pic img {{ width: 330px; height: 186px; object-fit: cover; border-radius: 10px; display: block }}
    h2 {{ margin: 6px 0 0; font-size: 33px; line-height: 1.15 }}
    b {{ font-size: 18px; letter-spacing: .14em; text-transform: uppercase; color: #6a6f47 }}
    p {{ margin: 6px 0 0; font-size: 22px; line-height: 1.38; color: #26332b }}
    .light {{ margin: 16px 0 0; padding: 14px 20px; border-left: 6px solid #c29a55; background: rgba(194, 154, 85, .14); font-size: 23px; line-height: 1.4 }}
    .foot {{ margin: 14px 0 0; font-size: 20px; line-height: 1.45; color: #4b5850 }}
    </style></head><body>
    <p class="eyebrow">STAGE II · Zara Fashion · Woven Earth</p>
    <h1>The arrival in materials: sources, makers and upkeep</h1>
    <p class="lead">What each element of the arrival gallery and reception is made of, where it would come from and how it is kept. Every source, maker and test is still to be identified: nothing here is claimed.</p>
    {rows}
    <p class="light">{escape(LIGHT)}</p>
    <p class="foot">{escape(FOOT)}</p>
    </body></html>"""
    tmp = W / '_board.html'; tmp.write_text(html)
    try:
        with sync_playwright() as pw:
            br = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True)
            pg = br.new_page(viewport={'width': 2480, 'height': 1754}); pg.goto(tmp.as_uri(), wait_until='load')
            pg.wait_for_function("[...document.images].every(i => i.complete && i.naturalWidth > 0)", timeout=60000)
            over = pg.evaluate('document.documentElement.scrollHeight')
            pg.screenshot(path=str(dst.with_suffix('.png')), full_page=False); br.close()
        Image.open(dst.with_suffix('.png')).convert('RGB').save(dst, quality=88, optimize=True); dst.with_suffix('.png').unlink()
    finally:
        tmp.unlink(missing_ok=True); [c.unlink(missing_ok=True) for c in crops]
    print(dst, 'content height', over, '(fits)' if over <= 1754 else '(OVERFLOWS)')


main(Path(sys.argv[1]))
