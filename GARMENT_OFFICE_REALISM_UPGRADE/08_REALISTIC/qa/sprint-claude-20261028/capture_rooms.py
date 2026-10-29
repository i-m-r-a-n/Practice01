"""Reference-camera frames of the release rooms through the viewer's own frameCamera API (LOCAL Chromium, software WebGL).
UI is hidden for the clean frames. Actual viewer frames, not renders or AI images. Not live or MacBook proof.
python3 capture_rooms.py --out DIR [--cams CAM_01_Reception_A,...] [--size 1440x900]"""
import argparse, hashlib, json, time
from pathlib import Path
from playwright.sync_api import sync_playwright
p = argparse.ArgumentParser()
p.add_argument('--url', default='http://127.0.0.1:8784/realistic/?welcome=0')
p.add_argument('--out', required=True)
p.add_argument('--cams', default='CAM_01_Reception_A,CAM_04_Experience_Centre_A,CAM_09_Boardroom_A,CAM_07_MD_Office_A,CAM_34_Merchandising_Sample_Hub,CAM_14_Design_Studio_B')
p.add_argument('--size', default='1440x900')
a = p.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
w, h = map(int, a.size.split('x'))
HIDE = '#top,#side,#info,#viewbar,#tourbar,#disclaimer,#labels,#minimap,#walkhint,#pad,#dock,#welcome,#dissolve,#photo{display:none!important}'
R = {'scope': 'LOCAL Chromium (SwiftShader) via serve_preview.py; viewer frameCamera API; UI hidden; not live or MacBook proof', 'url': a.url, 'shots': [], 'errors': [], 'http_errors': []}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    page = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
    page.on('pageerror', lambda e: R['errors'].append(str(e)))
    page.on('console', lambda m: R['errors'].append(m.text) if m.type == 'error' else None)
    page.on('response', lambda r: R['http_errors'].append({'url': r.url, 'status': r.status}) if r.status >= 400 else None)
    t0 = time.monotonic()
    page.goto(a.url, wait_until='domcontentloaded', timeout=60000)
    page.wait_for_function('window.__viewer?.ready', timeout=180000)
    page.wait_for_function('__viewer.api.peopleStats().loaded', timeout=240000)
    try:   # release floor finish (2K terrazzo albedo) arrives asynchronously; frames wait for it when the build has it
        page.wait_for_function("__viewer.finishes || __viewer.errors.some(e => e.startsWith('Finishes')) || !__viewer.lightmaps", timeout=60000)
    except Exception:
        pass
    R['finishes'] = page.evaluate('__viewer.finishes ?? null')
    R['people'] = page.evaluate('__viewer.api.peopleStats()'); R['dressing'] = page.evaluate('__viewer.dressing && {identity: __viewer.dressing.identity, interior: __viewer.dressing.interior, screens: __viewer.dressing.screens}')
    R['screenRoots'] = page.evaluate('__viewer.screenRoots ?? null')
    css = page.add_style_tag(content=HIDE)
    for cam in a.cams.split(','):
        st = page.evaluate('n => __viewer.api.frameCamera(n)', cam)
        page.evaluate('() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))'); page.wait_for_timeout(600)
        f = out / f'{w}_{cam}.png'; page.screenshot(path=str(f), timeout=120000)
        R['shots'].append({'camera': cam, 'file': f.name, 'sha256': hashlib.sha256(f.read_bytes()).hexdigest(), 'state': st}); print(cam, flush=True)
    R['seconds'] = round(time.monotonic() - t0, 1)
    (out / 'capture.json').write_text(json.dumps(R, indent=2))
    b.close()
print(json.dumps({'shots': len(R['shots']), 'errors': R['errors'][:5], 'http_errors': R['http_errors'][:5], 'identity': (R['dressing'] or {}).get('identity', {}).get('items') and len(R['dressing']['identity']['items']), 'screenRoots': R['screenRoots']}))
