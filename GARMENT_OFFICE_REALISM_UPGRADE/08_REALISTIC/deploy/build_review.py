"""Publish only evidence explicitly listed in a reviewed-phase JSON manifest.

Usage: python build_review.py reviewed-phases.json
Every referenced image/report must exist. No placeholder comparison images.
"""
from pathlib import Path
import hashlib, html, json, sys

REAL=Path(__file__).resolve().parent.parent
REPO=REAL.parents[1]
config=json.loads(Path(sys.argv[1]).read_text())
OUT=REAL/'review';OUT.mkdir(exist_ok=True)
def esc(x):return html.escape(str(x),quote=True)
files=[]
def checked(path):
    p=((REPO/'GARMENT_OFFICE_FINAL_PRESENTATION/02_RENDERED_IMAGES/final'/path.removeprefix('renders/')) if path.startswith('renders/') else REAL/path).resolve()
    assert p.is_relative_to(REPO) and p.is_file(),f'Missing evidence: {path}'
    files.append({'path':path,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    return '../'+path
sections=[]
for phase in config['phases']:
    rooms=[]
    for room in phase['rooms']:
        figs=[]
        for shot in room['images']:
            url=checked(shot['path'])
            figs.append(f'<figure><a href="{esc(url)}" target="_blank" rel="noopener"><img loading="lazy" src="{esc(url)}" alt="{esc(room["name"]+" — "+shot["label"])}"></a><figcaption>{esc(shot["label"])}</figcaption></figure>')
        rooms.append(f'<article><h3>{esc(room["name"])}</h3><div class="comparison">'+''.join(figs)+f'</div><p class="note">{esc(room.get("note",""))}</p></article>')
    reports=''.join(f'<a href="{esc(checked(r["path"]))}">{esc(r["label"])}</a>' for r in phase.get('reports',[]))
    sections.append(f'<section id="{esc(phase["id"])}"><div class="section-heading"><h2>{esc(phase["title"])}</h2><span>{esc(phase["status"])}</span></div><p>{esc(phase["summary"])}</p><p class="limits">{esc(phase["limits"])}</p><nav class="reports">{reports}</nav>'+''.join(rooms)+'</section>')
nav=''.join(f'<a href="#{esc(p["id"])}">{esc(p["title"])}</a>' for p in config['phases'])
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Office tour · visual review</title><style>
:root{color-scheme:light;--ink:#19251f;--paper:#f5f3ee;--line:#d9ddd5;--accent:#355e45}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 system-ui,sans-serif}header,main,footer{max-width:1500px;margin:auto;padding:32px 28px}header{border-bottom:1px solid var(--line)}.eyebrow{text-transform:uppercase;letter-spacing:.14em;font-size:12px;color:var(--accent)}h1{font-size:clamp(30px,4vw,50px);line-height:1.1;margin:10px 0 18px}h2{font-size:26px;margin:0}h3{font-size:18px;margin:24px 0 12px}a{color:var(--accent);text-underline-offset:4px}nav{display:flex;gap:16px;flex-wrap:wrap}.section-heading{display:flex;align-items:center;justify-content:space-between;gap:18px}.section-heading span{font-size:13px;border:1px solid var(--line);border-radius:20px;padding:5px 12px}section{padding:22px 0 44px;border-bottom:1px solid var(--line)}p{max-width:1040px}.limits,.note{font-size:14px;color:#526157}.reports{font-size:14px;margin:16px 0}.comparison{display:flex;gap:12px;overflow:auto}figure{flex:1;min-width:280px;margin:0;background:#fff;border:1px solid var(--line)}img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:contain;background:#e8ebe6}figcaption{padding:9px 12px;font-size:13px}footer{font-size:13px;color:#526157}.actions{margin-top:22px}.button{display:inline-block;padding:10px 16px;background:var(--accent);color:#fff;text-decoration:none;border-radius:6px}code{font-size:12px;overflow-wrap:anywhere}@media(max-width:650px){header,main,footer{padding:22px 16px}.section-heading{align-items:start;flex-direction:column}.comparison figure{min-width:85vw}}
</style><header><div class="eyebrow">Office tour / evidence</div><h1>Visual review</h1><p>__INTRO__</p><p><code>__COMMIT__</code></p><nav>__NAV__</nav><div class="actions"><a class="button" href="../">Open the tour</a> &nbsp; <a href="/">Original tour</a></div></header><main>__SECTIONS__</main><footer>People shown are illustrative. Proposed interior visualization. Final dimensions and technical details subject to site verification.<br>Browser screenshots are actual captures. Cycles references are offline renders. Platform and test limits are recorded for each phase.</footer></html>'''
page=page.replace('__INTRO__',esc(config['intro'])).replace('__COMMIT__',esc(config['source_commit'])).replace('__NAV__',nav).replace('__SECTIONS__',''.join(sections))
(OUT/'index.html').write_text(page)
(OUT/'evidence-manifest.json').write_text(json.dumps({'config':config,'files':files},indent=2)+'\n')
print(json.dumps({'phases':len(config['phases']),'evidence_files':len(files),'output':str(OUT/'index.html')}))
