"""Phone-sized check of /bengal-earth-lab/: a 390 x 844 touch viewport (the viewer picks low quality for coarse pointers),
the guided tour's frames at five stops, page and HTTP errors, and the viewer's own GPU-memory estimate.
LOCAL Chromium with software WebGL: it shows the layout and the load works, not real phone speed.
python3 -I bel_mobile_check.py --out DIR [--url URL]"""
import argparse, json, time
from pathlib import Path
from playwright.sync_api import sync_playwright

p = argparse.ArgumentParser()
p.add_argument('--url', default='http://127.0.0.1:8790/bengal-earth-lab/?welcome=0')
p.add_argument('--out', required=True)
a = p.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
R = {'url': a.url, 'scope': 'LOCAL Chromium (SwiftShader), 390 x 844 touch viewport at 2x; layout and load only, not phone speed', 'errors': [], 'http_errors': [], 'failed_requests': [], 'frames': []}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True)
    page = ctx.new_page()
    page.on('pageerror', lambda e: R['errors'].append(str(e)))
    page.on('console', lambda m: R['errors'].append(m.text) if m.type == 'error' else None)
    page.on('response', lambda r: R['http_errors'].append({'url': r.url, 'status': r.status}) if r.status >= 400 else None)
    page.on('requestfailed', lambda q: R['failed_requests'].append({'url': q.url, 'failure': q.failure}))
    t0 = time.monotonic()
    page.goto(a.url, wait_until='domcontentloaded', timeout=60000)
    page.wait_for_function('window.__viewer?.ready', timeout=240000)
    page.wait_for_function('__viewer.dressing && __viewer.dressing.concept', timeout=300000)
    R['load_seconds'] = round(time.monotonic() - t0, 1)
    R['quality'] = page.evaluate('__viewer.counts?.quality ?? null')
    R['concept'] = page.evaluate('({ ...__viewer.dressing.concept, items: undefined })')
    try: R['gpu_memory'] = page.evaluate('__viewer.api.gpuMemoryEstimate()')
    except Exception as e: R['gpu_memory'] = str(e)[:200]
    page.screenshot(path=str(out / 'mobile_start.png'))
    for cam in ['BEL_CAM_UTHAN', 'BEL_CAM_MAKING_LINE', 'BEL_CAM_RECORDS', 'CAM_01_Reception_A', 'CAM_09_Boardroom_A']:
        page.evaluate('n => __viewer.api.frameCamera(n)', cam); page.wait_for_timeout(900)
        f = out / f'mobile_{cam}.png'; page.screenshot(path=str(f)); R['frames'].append(f.name)
    b.close()
R['passed'] = not R['errors'] and not R['http_errors'] and not R['failed_requests']
(out / 'mobile-check.json').write_text(json.dumps(R, indent=2) + '\n')
print(json.dumps({k: R[k] for k in ('passed', 'quality', 'load_seconds')} | {'textureMB': (R['concept'] or {}).get('textureMB'), 'errors': R['errors'][:3]}))
