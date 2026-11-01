"""A PDF of the guided tour in images, to send to buyers: one A4 landscape page per stop, then the three rooms.
Each page has the image, the stop number, title and text, and the kind label. Each AI concept image has a small inset of the same
camera rendered from the 3D model, so the reader sees where it differs. A cover page and a closing page carry the honesty note and the link.
Printed by headless Chromium from a page written next to the images. Nothing is retouched.
python3 -I tour_pdf.py OUT.pdf"""
import json, re, sys
from html import escape
from pathlib import Path
from playwright.sync_api import sync_playwright

R = Path(__file__).resolve().parents[2]
cfg = json.loads((R / 'viewer' / 'bel-config.json').read_text())
stills, tour, b = cfg['conceptStills'], cfg['tour'], cfg.get('branding', {})
names = {r['zone']: r['name'] for r in json.loads((R / 'revised-model' / 'office_web_metadata.json').read_text())['rooms']}
names.update(cfg.get('roomNames', {}))
LABEL = {'ai': 'AI concept image · made from the 3D views · people are fictional · not a photograph',
         'render': 'Rendered from the 3D model · Blender Cycles, simulated light · no people · not a photograph'}
LINK = 'stage2-office-virtual-tour.imranahmedjh611.workers.dev/stage2-concept/'
logos = ''.join(f'<img src="viewer/assets/{f}" alt="">' for f in ('logo_zara_fashion_profile.png', 'logo_stage2_ltd.png', 'logo_stage2_unit1.png'))


def page(head, title, text, cam):
    v = stills[cam]; kind = v.get('kind', 'ai')
    inset = (f'<figure class="inset"><img src="{escape(v["model"])}" alt=""><figcaption>The same camera in the 3D model (render, no people)</figcaption></figure>'
             if kind == 'ai' and v.get('model') else '')
    return (f'<section class="stop"><div class="pic"><img src="{escape(v["src"])}" alt="">{inset}</div>'
            f'<div class="cap"><span class="num">{escape(head)}</span><h2>{escape(title)}</h2>'
            + (f'<p>{escape(text)}</p>' if text else '') + f'<span class="kind {kind}">{escape(LABEL[kind])}</span></div></section>')


pages = [page(f'Stop {i + 1} of {len(tour)}', t['title'], t.get('description', ''), t['camera']) for i, t in enumerate(tour) if t['camera'] in stills]
pages += [page('Room', names.get(z, cam), '', cam) for cam, z in (('CAM_07_MD_Office_A', 'Z12'), ('CAM_25_Fabric_Library', 'Z15'), ('CAM_23_Sample_Room', 'Z17')) if cam in stills]
foot = re.sub(r'<[^>]+>', '', b.get('disclaimerHtml', '')).replace('&middot;', '·')
html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>STAGE II · Zara Fashion - the tour in images</title><style>
@page {{ size: A4 landscape; margin: 0 }}
* {{ box-sizing: border-box }}
body {{ margin: 0; font-family: Inter, "Helvetica Neue", Arial, sans-serif; color: #f6f3ee; background: #141c17; -webkit-print-color-adjust: exact; print-color-adjust: exact }}
section {{ width: 297mm; height: 210mm; page-break-after: always; break-after: page; overflow: hidden; position: relative; background: #141c17 }}
.cover, .end {{ display: flex; flex-direction: column; justify-content: center; padding: 0 24mm }}
.logos {{ display: inline-flex; gap: 6mm; align-items: center; background: #fff; padding: 3mm 5mm; border-radius: 3mm; align-self: flex-start }}
.logos img {{ height: 10mm }}
.eyebrow {{ margin: 10mm 0 0; font-size: 11pt; letter-spacing: .18em; text-transform: uppercase; color: #a9d8b8; font-weight: 600 }}
h1 {{ margin: 3mm 0 4mm; font-size: 30pt; line-height: 1.15 }}
.lead {{ margin: 0 0 6mm; font-size: 14pt; color: #d6dfd9 }}
.legend {{ font-size: 11pt; line-height: 1.5; color: #efe6d4; border-left: 1mm solid #c29a55; padding: 2mm 4mm; background: rgba(194, 154, 85, .12); max-width: 210mm }}
.link {{ margin-top: 6mm; font-size: 12pt; color: #a9d8b8 }}
.stop .pic {{ position: absolute; left: 0; top: 0; width: 297mm; height: 167mm; background: #0d120f }}
.stop .pic > img {{ width: 100%; height: 100%; object-fit: cover; display: block }}
.inset {{ position: absolute; right: 5mm; bottom: 5mm; width: 78mm; margin: 0; background: rgba(13, 18, 15, .92); border: .4mm solid #a9d8b8; border-radius: 2mm; overflow: hidden }}
.inset img {{ width: 100%; aspect-ratio: 16 / 9; object-fit: cover; display: block }}
.inset figcaption {{ font-size: 7.5pt; color: #a9d8b8; padding: 1.2mm 2mm }}
.cap {{ position: absolute; left: 0; right: 0; bottom: 0; height: 43mm; padding: 4mm 10mm; display: flex; flex-direction: column; gap: 1.2mm }}
.num {{ font-size: 8.5pt; letter-spacing: .16em; text-transform: uppercase; color: #a9d8b8; font-weight: 650 }}
.cap h2 {{ margin: 0; font-size: 17pt }}
.cap p {{ margin: 0; font-size: 9.5pt; line-height: 1.4; color: #dfe6e1; max-height: 14mm; overflow: hidden }}
.kind {{ font-size: 8pt; letter-spacing: .06em; text-transform: uppercase }}
.kind.ai {{ color: #e2c48c }} .kind.render {{ color: #a9d8b8 }}
.end p {{ font-size: 11pt; line-height: 1.55; color: #d6dfd9; max-width: 230mm }}
</style></head><body>
<section class="cover"><div class="logos">{logos}</div><p class="eyebrow">{escape(b.get('eyebrow', 'STAGE II · Zara Fashion'))}</p>
<h1>{escape(b.get('headline', 'The ground floor, reimagined · concept proposal'))}</h1>
<p class="lead">The guided tour in images: {len(tour)} stops and 3 rooms, one page each.</p>
<p class="legend">Gold label: an AI concept image made from the 3D views. The people in it are fictional and details can differ from the 3D, so each one carries a small render of the same camera in the 3D model. Green label: rendered from the 3D model itself, with simulated light and no people. None of the images is a photograph.</p>
<p class="link">Walk through it in 3D, on a computer or a phone: {LINK}</p></section>
{''.join(pages)}
<section class="end"><p class="eyebrow">Concept proposal</p><h1>Walk through it in 3D</h1><p class="link">{LINK}</p><p>{escape(foot)}</p></section>
</body></html>"""
tmp = R / '_tour_pdf.html'
tmp.write_text(html)
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True)
        pg = br.new_page(); pg.goto(tmp.as_uri(), wait_until='load', timeout=120000)
        pg.wait_for_function("[...document.images].every(i => i.complete && i.naturalWidth > 0)", timeout=120000)
        pg.pdf(path=sys.argv[1], format='A4', landscape=True, print_background=True, margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'})
        n = pg.evaluate("document.querySelectorAll('section').length"); br.close()
finally:
    tmp.unlink(missing_ok=True)
print(sys.argv[1], n, 'pages')
