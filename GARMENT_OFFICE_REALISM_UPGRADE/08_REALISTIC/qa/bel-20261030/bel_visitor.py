"""Bengal Earth Lab visitor-eye frames (copy of qa/sprint-claude-20261028/capture_visitor.py with this route's spots).
Visitor-eye frames at chosen floor spots through the viewer's walk-QA hooks (LOCAL Chromium, software WebGL).
Each spot must be free walkable floor (the viewer refuses blocked spots). UI hidden. Not live or MacBook proof.
python3 capture_visitor.py --out DIR [--spots name:x:z:yaw:pitch:fov,...]"""
import argparse, hashlib, json, math, time
from pathlib import Path
from playwright.sync_api import sync_playwright
SPOTS = {
    'lobby_gate': (4.6, 2.2, -2.404, -0.18, 62),
    'lobby_relief': (2.3, 1.45, 1.5707963267948966, -0.05, 60),
    'reception_instruments': (11.6, 1.7, 0.0, -0.08, 62),
    'reception_tea': (10.9, 3.6, 2.379, -0.55, 58),
    'passage_sun': (10.05, -1.05, -0.34, -0.1, 64),
    'passage_earth': (10.25, -2.2, 0.586, -0.42, 62),
    'ec_plinth': (12.6, -7.0, 0.0, -0.42, 64),
    'ec_bays': (15.6, -8.0, 0.32, -0.12, 70),
    'ec_future': (20.9, -9.2, 0.857, -0.12, 62),
    'ec_water': (13.3, -6.75, 3.141592653589793, -0.42, 58),
    'board_review': (17.25, -0.95, 0.0, -0.55, 64),
    'board_bonsai': (14.2, -1.4, 0.4, -0.25, 60),
    'studio_shelf': (32.35, -18.95, -1.523, -0.35, 62),
    'studio_cocreation': (29.0, -15.4, -0.927, -0.35, 58),
    # option A rooms (increment 2)
    'uthan_botola': (18.6, -16.2, 1.5708, -0.2, 62),
    'uthan_loom': (12.2, -14.25, 0.70, -0.42, 62),
    'uthan_living': (12.2, -14.05, 3.14159, -0.25, 64),
    'uthan_dining': (12.9, -17.9, 0.58, -0.3, 62),
    'uthan_bedroom': (16.1, -17.95, 0.0, -0.3, 64),
    'uthan_hospitality': (16.4, -13.65, 3.14159, -0.12, 64),
    'academy_rows': (5.0, -8.95, 0.0, -0.12, 64),
    'academy_teaching': (8.35, -15.6, 1.5708, -0.18, 66),
}
p = argparse.ArgumentParser()
p.add_argument('--url', default='http://127.0.0.1:8790/bengal-earth-lab/?welcome=0')
p.add_argument('--out', required=True)
p.add_argument('--only', default='')
p.add_argument('--size', default='1280x800')
a = p.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
w, h = map(int, a.size.split('x'))
HIDE = '#top,#side,#info,#viewbar,#tourbar,#disclaimer,#labels,#minimap,#walkhint,#pad,#dock,#welcome,#dissolve,#photo{display:none!important}'
R = {'scope': 'LOCAL Chromium (SwiftShader); viewer walk-QA hooks at visitor eye height 1.6 m; UI hidden; not live or MacBook proof', 'shots': [], 'errors': []}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    page = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
    page.on('pageerror', lambda e: R['errors'].append(str(e)))
    page.on('console', lambda m: R['errors'].append(m.text) if m.type == 'error' else None)
    page.goto(a.url, wait_until='domcontentloaded', timeout=60000)
    page.wait_for_function('window.__viewer?.ready', timeout=180000)
    page.wait_for_function('__viewer.dressing && __viewer.dressing.concept', timeout=240000)   # no people on this route
    page.add_style_tag(content=HIDE)
    for name, (x, z, yaw, pitch, fov) in SPOTS.items():
        if a.only and name not in a.only.split(','): continue
        try:
            page.evaluate('([x, z]) => __viewer.api.setWalkQAStart(x, z)', [x, z])
            st = page.evaluate('a => __viewer.api.stepWalkQA({yaw: a[0], pitch: a[1], fov: a[2], dt: 0})', [yaw, pitch, fov])
            page.evaluate('() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))'); page.wait_for_timeout(700)
            f = out / f'visitor_{name}.png'; page.screenshot(path=str(f), timeout=120000)
            R['shots'].append({'spot': name, 'xz': [x, z], 'yaw': yaw, 'pitch': pitch, 'fov': fov, 'file': f.name, 'sha256': hashlib.sha256(f.read_bytes()).hexdigest(), 'room': st.get('room')}); print(name, st.get('room'), flush=True)
        except Exception as e:
            R['shots'].append({'spot': name, 'error': str(e)[:300]}); print(name, 'ERROR', str(e)[:200], flush=True)
    (out / 'visitor.json').write_text(json.dumps(R, indent=2))
    b.close()
print(json.dumps({'shots': len(R['shots']), 'errors': R['errors'][:5]}))
