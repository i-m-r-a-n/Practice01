"""Pre-deploy check for /bengal-earth-lab/: every file the proposal page requests exists in the release commit
(same path rules as belRoute() in deploy/build_worker.py). Copy of qa/sprint-claude-20261028/request_list.py.

Loads the page through serve_preview.py (LOCAL Chromium), opens the six rooms and their photoreal stills with People on,
records every /realistic/ request, maps it to its repository path and checks it with `git cat-file` at COMMIT.
python3 request_list.py COMMIT --out FILE [--url URL]
"""
import argparse, json, re, subprocess, time
from pathlib import Path
from urllib.parse import urlparse, unquote
from playwright.sync_api import sync_playwright

p = argparse.ArgumentParser()
p.add_argument('commit')
p.add_argument('--url', default='http://127.0.0.1:8790/bengal-earth-lab/')
p.add_argument('--out', required=True)
a = p.parse_args()
A = 'GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/'
ZONES = ['Z01', 'Z02', 'Z03', 'Z30', 'Z08', 'Z12', 'Z18']


def repo_path(rel):   # mirrors belRoute() in deploy/build_worker.py
    rel = rel or 'index.html'
    if rel in ('index.html', 'app.js', 'release-config.json'): return A + 'viewer/dist-bel/' + rel
    if rel == 'model_web.glb': return 'GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/Final_Office_Interior_web.glb'
    if rel == 'model_web_baked.glb': return A + 'revised-model/Optimized_Office_Interior_web_baked.glb'
    return A + rel


seen = {}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    page = b.new_page(viewport={'width': 1280, 'height': 800})
    page.on('request', lambda q: seen.setdefault(unquote(urlparse(q.url).path), q.url) if urlparse(q.url).path.startswith('/bengal-earth-lab/') else None)
    t0 = time.monotonic()
    page.goto(a.url + '?welcome=0', wait_until='domcontentloaded', timeout=60000)
    page.wait_for_function('window.__viewer?.ready', timeout=180000)
    page.wait_for_function('__viewer.dressing && __viewer.dressing.concept', timeout=240000)
    for cam in json.loads(page.evaluate('JSON.stringify((window.__TOUR_CONFIG?.tour || []).map(s => s.camera))')):
        page.evaluate('n => __viewer.api.frameCamera(n)', cam); page.wait_for_timeout(600)   # frameCamera waits for the room's light to load
    page.wait_for_timeout(1500)
    b.close()

rows = []
for path in sorted(seen):
    rel = path[len('/bengal-earth-lab/'):]
    target = repo_path(rel)
    ok = subprocess.run(['git', 'cat-file', '-e', f'{a.commit}:{target}'], capture_output=True).returncode == 0
    rows.append({'request': path, 'repo_path': target, 'in_commit': ok})
report = {'scope': 'LOCAL Chromium via serve_preview.py; request paths checked against the release commit tree',
          'commit': a.commit, 'requests': len(rows), 'missing': [r for r in rows if not r['in_commit']],
          'seconds': round(time.monotonic() - t0, 1), 'rows': rows}
report['passed'] = not report['missing']
Path(a.out).write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'passed': report['passed'], 'requests': len(rows), 'missing': report['missing']}))
