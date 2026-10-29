"""Bengal Earth Lab route check (copy of qa/interior-20261029/room_check.py for a route without people).
Targeted check after an interior change (LOCAL Chromium via serve_preview.py, software WebGL; not live or MacBook proof).

For one room: frames from its reference cameras, a walk along a given line towards the new work (it must keep moving on
free floor and stop at the wall, not pass through it), a close frame at the end of the walk, and the page errors,
HTTP errors and failed requests of the whole run.
python3 room_check.py --out DIR --cams CAM_01_Reception_A --walk x,z,yaw,steps [--url URL]
"""
import argparse, json, time
from pathlib import Path
from playwright.sync_api import sync_playwright

p = argparse.ArgumentParser()
p.add_argument('--url', default='http://127.0.0.1:8790/bengal-earth-lab/?welcome=0')
p.add_argument('--out', required=True)
p.add_argument('--cams', required=True)
p.add_argument('--walk', help='start x,z, yaw (rad), number of 0.25 s steps')
p.add_argument('--size', default='1440x900')
a = p.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
w, h = map(int, a.size.split('x'))
HIDE = '#top,#side,#info,#viewbar,#tourbar,#disclaimer,#labels,#minimap,#walkhint,#pad,#dock,#welcome,#dissolve,#photo{display:none!important}'
local = a.url.startswith('http://127.0.0.1')
R = {'url': a.url, 'scope': ('LOCAL Chromium (SwiftShader) via serve_preview.py; not live or MacBook proof' if local else
     'LIVE site in Chromium (SwiftShader software WebGL) in this container; not Safari or MacBook proof'), 'checks': [], 'errors': [], 'http_errors': [], 'failed_requests': []}
check = lambda name, ok, detail=None: (R['checks'].append({'name': name, 'passed': bool(ok), 'detail': detail}), print(('PASS ' if ok else 'FAIL ') + name, flush=True))
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    page = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
    page.on('pageerror', lambda e: R['errors'].append(str(e)))
    page.on('console', lambda m: R['errors'].append(m.text) if m.type == 'error' else None)
    page.on('response', lambda r: R['http_errors'].append({'url': r.url, 'status': r.status}) if r.status >= 400 else None)
    page.on('requestfailed', lambda q: R['failed_requests'].append({'url': q.url, 'failure': q.failure}))
    t0 = time.monotonic()
    page.goto(a.url, wait_until='domcontentloaded', timeout=60000)
    page.wait_for_function('window.__viewer?.ready', timeout=180000)
    page.wait_for_function('__viewer.dressing && __viewer.dressing.concept', timeout=240000)   # this route shows no people
    try: page.wait_for_function("__viewer.finishes || __viewer.errors.some(e => e.startsWith('Finishes'))", timeout=60000)
    except Exception: pass
    R['finishes'] = page.evaluate('__viewer.finishes ?? null'); R['interior'] = page.evaluate('__viewer.dressing?.interior ?? null')
    check('interior layer built', R['interior'] and R['interior']['items'], R['interior'] and R['interior'].get('stats'))
    R['concept'] = page.evaluate('__viewer.dressing.concept'); R['hidden_nodes'] = page.evaluate('__viewer.hiddenNodes ?? []')
    check('concept layer built', R['concept'] and R['concept']['items'], {k: v for k, v in (R['concept'] or {}).items() if k != 'items'})
    check('replaced approved items hidden', len(R['hidden_nodes']) >= 18, len(R['hidden_nodes']))
    page.add_style_tag(content=HIDE)
    for cam in a.cams.split(','):
        st = page.evaluate('n => __viewer.api.frameCamera(n)', cam)
        page.evaluate('() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))'); page.wait_for_timeout(600)
        page.screenshot(path=str(out / f'{w}_{cam}.png'), timeout=120000); print('frame', cam, flush=True)
    if a.walk:
        x, z, yaw, n = a.walk.split(','); x, z, yaw, n = float(x), float(z), float(yaw), int(n)
        page.evaluate('([x, z]) => __viewer.api.setWalkQAStart(x, z)', [x, z])
        trail = [page.evaluate('a => __viewer.api.stepWalkQA({yaw: a[0], pitch: 0, forward: 1, dt: .25})', [yaw]) for _ in range(n)]
        end = trail[-1]; R['walk'] = {'start': [x, z], 'yaw': yaw, 'end': end['position'], 'collisions': end['collisions'], 'distance': end['distance'], 'room': end['room']}
        check('walk moves on free floor', end['distance'] > 1 and not end['blocked'], R['walk'])
        check('walk never ends inside geometry or a wall', not any(s['blocked'] for s in trail), [s['position'] for s in trail][-3:])
        page.evaluate('() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))'); page.wait_for_timeout(600)
        page.screenshot(path=str(out / f'{w}_walk_end.png'), timeout=120000)
    check('no page or console errors', not R['errors'], R['errors'][:5])
    check('no HTTP errors', not R['http_errors'], R['http_errors'][:5])
    R['seconds'] = round(time.monotonic() - t0, 1); R['passed'] = all(c['passed'] for c in R['checks'])
    (out / 'room-check.json').write_text(json.dumps(R, indent=2))
    b.close()
print(json.dumps({'passed': R['passed'], 'failed': [c['name'] for c in R['checks'] if not c['passed']], 'failed_requests': len(R['failed_requests']), 'seconds': R['seconds']}))
