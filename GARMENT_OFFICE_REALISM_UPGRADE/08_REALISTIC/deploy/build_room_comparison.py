"""Create one before/after from unchanged actual browser captures, via HTML."""
from pathlib import Path
import argparse,html,json,hashlib
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('room');p.add_argument('camera');p.add_argument('after');p.add_argument('--label');a=p.parse_args()
r=Path(__file__).resolve().parent.parent
before='qa/baseline/shots/before_'+a.camera+'.png'
for f in [before,a.after]:assert (r/f).is_file(),f
label=html.escape(a.label or a.room.replace('_',' '));slug=a.room.lower()
doc=f'''<!doctype html><meta charset="utf-8"><title>{label} — before / after</title><style>*{{box-sizing:border-box}}body{{margin:0;background:#eceee9;font-family:Arial,sans-serif;color:#173128}}.pair{{display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:12px}}figure{{margin:0;background:white}}figcaption{{padding:12px 16px;font-size:20px;font-weight:bold}}img{{display:block;width:100%}}footer{{padding:0 20px 14px;font-size:14px}}</style><div class="pair"><figure><figcaption>BEFORE · Original {label}</figcaption><img src="../{html.escape(before,quote=True)}"></figure><figure><figcaption>AFTER · {label} increment</figcaption><img src="../{html.escape(a.after,quote=True)}"></figure></div><footer>Actual browser captures • Same approved room and camera • People shown are illustrative</footer>'''
(r/f'review/{slug}-before-after.html').write_text(doc)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':1920,'height':620},device_scale_factor=1)
 page.goto(f'http://127.0.0.1:8783/realistic/review/{slug}-before-after.html',wait_until='networkidle')
 assert page.locator('img').evaluate_all('(items)=>items.every(x=>x.complete&&x.naturalWidth>0)')
 page.screenshot(path=str(r/f'review/{slug}-before-after.png'),full_page=True);b.close()
print(json.dumps({'file':f'review/{slug}-before-after.png','sha256':hashlib.sha256((r/f'review/{slug}-before-after.png').read_bytes()).hexdigest()}))
