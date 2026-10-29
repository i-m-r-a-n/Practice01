"""Visitor-eye frames at chosen floor spots through the viewer's walk-QA hooks (LOCAL Chromium, software WebGL).
Each spot must be free walkable floor (the viewer refuses blocked spots). UI hidden. Not live or MacBook proof.
python3 capture_visitor.py --out DIR [--spots name:x:z:yaw:pitch:fov,...]"""
import argparse, hashlib, json, math, time
from pathlib import Path
from playwright.sync_api import sync_playwright
SPOTS = {
    'water_point': (11.45, -6.95, math.pi, -0.42, 62),
    'coconut_story': (15.55, -6.85, math.pi, -0.48, 58),
    'ec_counter_run': (12.4, -7.3, math.pi * 0.70, -0.30, 66),
    'jamdani_panel': (9.65, 2.6, math.pi, 0.05, 60),
    'md_development': (24.4, 4.9, -2.12, -0.3, 62),
    'board_review': (17.25, -0.95, 0.0, -0.55, 64),
    'md_visitor': (24.6, 2.4, -2.09, -0.45, 60),
    'board_people': (21.2, -0.9, 0.99, -0.3, 62),
    'reception_sofa': (9.6, 2.9, math.pi, -0.38, 60),
    'warp_weft': (11.55, 2.5, -2.988, -0.05, 62),
    'sofa_corner': (11.0, 3.6, 2.6, -0.42, 58),
    'ec_library': (16.2, -7.6, -0.661, -0.58, 55),
    'ec_forms': (12.7, -7.3, 0.0, -0.22, 62),
    'ec_ceiling': (10.6, -6.9, -1.45, 0.22, 66),
    'merch_typing': (12.9, -16.2, 0.55, -0.35, 60),
}
p = argparse.ArgumentParser()
p.add_argument('--url', default='http://127.0.0.1:8784/realistic/?welcome=0')
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
    page.wait_for_function('__viewer.api.peopleStats().loaded', timeout=240000)
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
