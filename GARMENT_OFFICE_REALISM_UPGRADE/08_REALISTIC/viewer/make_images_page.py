"""A light page of the proposal's tour in images, for phones that cannot run the 3D or are on slow data.
- Every tour stop's image (an AI concept image or a render of the 3D) with its stop, title, text and kind label.
- The 3D model view of each AI image, the three room images, and links into the 3D.
- No script is needed; a small one adds a full-screen viewer.
Written to 08_REALISTIC/images.html and served at /stage2-concept/images.html (the page's loading screen links to it).
Run after make_concept_thumbs.py and make_bel_config.py:  python3 -I make_images_page.py"""
import base64, io, json, re
from html import escape
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
cfg = json.loads((HERE / 'bel-config.json').read_text())
stills, tour, b = cfg['conceptStills'], cfg['tour'], cfg.get('branding', {})
KIND = {'ai': ('AI concept image · made from the 3D views · people are fictional · not a photograph', 'ai'),
        'render': ('Rendered from the 3D model · Blender Cycles, simulated light · no people · not a photograph', 'render')}
ROOMS = [('CAM_07_MD_Office_A', 'Z12'), ('CAM_25_Fabric_Library', 'Z15'), ('CAM_23_Sample_Room', 'Z17')]


def logo(name):   # the client logos, 48 px high (sharp at 24 px), inline so the page needs no other file
    im = Image.open(HERE / 'assets' / name).convert('RGBA'); im = im.resize((round(im.width * 48 / im.height), 48), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True); return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()


def card(head, title, text, cam):
    v = stills[cam]; kind = v.get('kind', 'ai'); label, cls = KIND[kind]
    thumb, full = v.get('thumb') or v['src'], v['src']
    alt = f"{'AI concept image' if kind == 'ai' else 'Render of the 3D model'}: {title}"
    model = (f'<a class="model full" href="{escape(v["model"])}" data-label="{escape(KIND["render"][0])}" data-kind="render">'
             '3D model view: the same camera in the 3D</a>') if kind == 'ai' and v.get('model') else ''
    return (f'<article class="card {cls}"><a class="full" href="{escape(full)}" data-label="{escape(label)}" data-kind="{cls}">'
            f'<img src="{escape(thumb)}" loading="lazy" decoding="async" alt="{escape(alt)}" width="640" height="360"></a>'
            f'<div class="txt"><span class="num">{escape(head)}</span><h2>{escape(title)}</h2>'
            + (f'<p>{escape(text)}</p>' if text else '') + f'<span class="kind">{escape(label)}</span>{model}</div></article>')


stops = ''.join(card(f'Stop {i + 1} of {len(tour)}', t['title'], t.get('description', ''), t['camera']) for i, t in enumerate(tour) if t['camera'] in stills)
names = {r['zone']: r['name'] for r in json.loads((HERE.parent / 'revised-model' / 'office_web_metadata.json').read_text())['rooms']}
names.update(cfg.get('roomNames', {}))   # this route's own names first, as on the page
rooms = ''.join(card('Room', names.get(z, cam), '', cam) for cam, z in ROOMS if cam in stills)
note = cfg.get('galleryNote', '').replace('Tap an image to go there in 3D.', 'Tap an image to see it full screen.')
foot = re.sub(r'<[^>]+>', '', b.get('disclaimerHtml', '')).replace('&middot;', '·')
logos = ''.join(f'<img src="{logo(f)}" alt="{a}">' for f, a in (('logo_zara_fashion_profile.png', 'Zara Fashion'), ('logo_stage2_ltd.png', 'Stage II Knitting Apparel Ltd.'),
                                                              ('logo_stage2_unit1.png', 'Stage II Knitting Apparel Unit-1')))
page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(b.get('eyebrow', 'STAGE II · Zara Fashion'))} - the tour in images</title>
<meta name="description" content="The ground floor concept proposal of STAGE II · Zara Fashion: every tour stop as one image, labelled AI concept image or render of the 3D model.">
<!-- Made by viewer/make_images_page.py from viewer/bel-config.json; do not edit by hand. -->
<style>
:root {{ --bg: #141c17; --card: #1d2721; --line: rgba(246, 243, 238, .14); --ink: #f6f3ee; --muted: #b9c4bd; --mint: #a9d8b8; --gold: #e2c48c; --brass: #c29a55 }}
* {{ box-sizing: border-box }}
body {{ margin: 0; background: var(--bg); color: var(--ink); font: 15px/1.5 Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", Arial, sans-serif }}
a {{ color: inherit }}
header, main, footer {{ max-width: 1240px; margin: 0 auto; padding: 0 16px }}
header {{ padding-top: 18px }}
.logos {{ display: inline-flex; gap: 10px; align-items: center; background: #fff; padding: 6px 10px; border-radius: 8px }}
.logos img {{ height: 24px; display: block }}
.eyebrow {{ margin: 16px 0 0; font-size: 11px; letter-spacing: .16em; text-transform: uppercase; color: var(--mint); font-weight: 600 }}
h1 {{ margin: 4px 0 6px; font-size: 28px; line-height: 1.2 }}
.lead {{ margin: 0 0 12px; color: var(--muted) }}
.go {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 12px }}
.go a {{ text-decoration: none; padding: 9px 14px; border-radius: 9px; border: 1px solid var(--line); background: rgba(255, 255, 255, .07); font-weight: 600; font-size: 14px }}
.go a.primary {{ background: var(--brass); border-color: var(--brass); color: #1b1408 }}
.note {{ margin: 0 0 18px; font-size: 13px; color: #efe6d4; background: rgba(194, 154, 85, .12); border-left: 3px solid var(--brass); border-radius: 6px; padding: 8px 10px }}
h3 {{ margin: 22px 0 10px; font-size: 13px; letter-spacing: .14em; text-transform: uppercase; color: var(--brass) }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 14px }}
.card {{ background: var(--card); border: 1px solid var(--line); border-radius: 12px; overflow: hidden; display: flex; flex-direction: column }}
.card img {{ display: block; width: 100%; height: auto; aspect-ratio: 16 / 9; object-fit: cover; background: #0d120f }}
.txt {{ padding: 10px 12px 12px; display: flex; flex-direction: column; gap: 4px }}
.num {{ font-size: 11px; letter-spacing: .14em; text-transform: uppercase; color: var(--mint); font-weight: 650 }}
.card h2 {{ margin: 0; font-size: 17px; line-height: 1.3 }}
.card p {{ margin: 0; font-size: 13.5px; color: #dfe6e1 }}
.kind {{ font-size: 11.5px; color: var(--gold) }}
.card.render .kind {{ color: var(--mint) }}
.model {{ font-size: 12.5px; color: var(--mint) }}
footer {{ margin-top: 26px; padding-bottom: 28px; font-size: 12.5px; color: var(--muted) }}
#view {{ position: fixed; inset: 0; z-index: 10; background: rgba(0, 0, 0, .94); display: none; align-items: center; justify-content: center }}
#view.on {{ display: flex }}
#view img {{ max-width: 100%; max-height: 100%; object-fit: contain }}
#view .tag {{ position: fixed; top: 10px; left: 12px; right: 70px; font-size: 11px; letter-spacing: .1em; text-transform: uppercase; color: var(--gold) }}
#view .tag.render {{ color: var(--mint) }}
#view button {{ position: fixed; top: 8px; right: 10px; width: 44px; height: 44px; border-radius: 10px; border: 1px solid var(--line); background: rgba(255, 255, 255, .1); color: #fff; font-size: 24px }}
</style>
</head>
<body>
<header>
  <div class="logos">{logos}</div>
  <p class="eyebrow">{escape(b.get('eyebrow', 'STAGE II · Zara Fashion'))}</p>
  <h1>{escape(b.get('headline', 'The ground floor, reimagined · concept proposal'))}</h1>
  <p class="lead">The guided tour in images: every stop of the 3D tour as one picture, in tour order.</p>
  <nav class="go"><a class="primary" href="./">Open the 3D tour</a><a href="./?walk=1">Walk through it on your phone</a></nav>
  <p class="note">{escape(note)}</p>
</header>
<main>
  <h3>The guided tour · {len(tour)} stops</h3>
  <div class="grid">{stops}</div>
  <h3>Rooms with their own image</h3>
  <div class="grid">{rooms}</div>
</main>
<footer>{escape(foot)}</footer>
<div id="view" role="dialog" aria-modal="true" aria-label="Image"><p class="tag"></p><img alt=""><button type="button" aria-label="Close">&times;</button></div>
<script>
(function () {{
  var v = document.getElementById('view'), img = v.querySelector('img'), tag = v.querySelector('.tag');
  function close() {{ v.classList.remove('on'); img.removeAttribute('src'); }}
  document.addEventListener('click', function (e) {{
    var a = e.target.closest && e.target.closest('a.full'); if (!a) {{ if (e.target === v || e.target.tagName === 'BUTTON') close(); return; }}
    e.preventDefault(); img.src = a.getAttribute('href'); img.alt = a.dataset.label; tag.textContent = a.dataset.label; tag.className = 'tag ' + a.dataset.kind; v.classList.add('on');
  }});
  document.addEventListener('keydown', function (e) {{ if (e.key === 'Escape') close(); }});
}})();
</script>
</body>
</html>
"""
out = HERE.parent / 'images.html'
out.write_text(page)
print(out, len(page), 'bytes,', stops.count('<article'), 'stops,', rooms.count('<article'), 'rooms')
