"""Interaction smoke test of /realistic/ with real clicks and keys (LOCAL Chromium via serve_preview.py, software WebGL).

Covers: welcome card, guided tour (start / next / back / pause / end), the six release rooms from the room list
(camera reached, room lighting loaded), photoreal still (image really loads), walk (button, W key, Escape),
overview tools, and on a phone-sized touch viewport the on-screen walk pad. Not live, Safari or MacBook proof.
python3 smoke.py --out DIR [--url URL] [--size 1440x900]
"""
import argparse, json, time
from pathlib import Path
from playwright.sync_api import sync_playwright

p = argparse.ArgumentParser()
p.add_argument('--url', default='http://127.0.0.1:8784/realistic/')
p.add_argument('--out', required=True)
p.add_argument('--size', default='1440x900')
a = p.parse_args()
out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
w, h = map(int, a.size.split('x')); touch = w < 700
R = {'scope': 'LOCAL Chromium (SwiftShader) via serve_preview.py; real UI events; not live, Safari or MacBook proof', 'url': a.url, 'viewport': [w, h], 'checks': [], 'errors': [], 'failed_requests': [], 'http_errors': []}
ROOMS = {'Z02': 'CAM_01_Reception_A', 'Z30': 'CAM_04_Experience_Centre_A', 'Z08': 'CAM_09_Boardroom_A', 'Z12': 'CAM_07_MD_Office_A', 'Z07': 'CAM_34_Merchandising_Sample_Hub', 'Z18': 'CAM_13_Design_Studio_A'}


def check(name, ok, detail=None):
    R['checks'].append({'name': name, 'passed': bool(ok), 'detail': detail}); print(('PASS ' if ok else 'FAIL ') + name, flush=True)


def settle(page, timeout=180000):
    page.wait_for_function('!__viewer.api.state().flying', timeout=timeout)


with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    ctx = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, has_touch=touch, is_mobile=touch)
    page = ctx.new_page()
    page.on('pageerror', lambda e: R['errors'].append(str(e)))
    page.on('console', lambda m: R['errors'].append(m.text) if m.type == 'error' else None)
    page.on('requestfailed', lambda q: R['failed_requests'].append({'url': q.url, 'failure': q.failure}))
    page.on('response', lambda r: R['http_errors'].append({'url': r.url, 'status': r.status}) if r.status >= 400 else None)
    t0 = time.monotonic()
    tap = (lambda sel: page.locator(sel).tap()) if touch else (lambda sel: page.locator(sel).click())
    try:
        page.goto(a.url + ('&' if '?' in a.url else '?') + 'welcome=1', wait_until='domcontentloaded', timeout=60000)
        page.wait_for_function('window.__viewer?.ready', timeout=180000)
        R['model_ready_seconds_local'] = round(time.monotonic() - t0, 2)
        check('welcome card shows on first visit', page.evaluate("!document.getElementById('welcome').classList.contains('hidden')"))
        tap('#wClose'); page.wait_for_timeout(300)
        check('welcome closes', page.evaluate("document.getElementById('welcome').classList.contains('hidden')"))
        page.wait_for_function('__viewer.api.peopleStats().loaded', timeout=240000)
        R['people'] = page.evaluate('__viewer.api.peopleStats()')
        # guided tour
        tap('#mTour'); page.wait_for_function("__viewer.api.state().mode==='tour'", timeout=30000); settle(page)
        s = page.evaluate('__viewer.api.state()'); check('tour starts at stop 1', s['tour'] and s['tour']['i'] == 0, s['tour'])
        tap('#tNext'); settle(page); s = page.evaluate('__viewer.api.state()'); check('tour Next', s['tour']['i'] == 1, s['tour'])
        tap('#tPrev'); settle(page); s = page.evaluate('__viewer.api.state()'); check('tour Back', s['tour']['i'] == 0, s['tour'])
        tap('#tPlay'); s = page.evaluate('__viewer.api.state()'); check('tour Pause', s['tour']['playing'] is False, s['tour'])
        page.screenshot(path=str(out / f'{w}_tour.png'))
        tap('#tStop'); settle(page); s = page.evaluate('__viewer.api.state()'); check('tour End returns to overview', s['mode'] == 'overview', s['mode'])
        # rooms
        for zone, cam in ROOMS.items():
            if not page.evaluate("document.getElementById('side').classList.contains('open')"):
                tap('#mRooms'); page.wait_for_timeout(400)
            tap(f'#roomList .room[data-zone="{zone}"]'); settle(page)
            lit = page.evaluate(f"!!__viewer.api.lighting().rooms['{zone}']")       # only rooms in the lightmap manifest have an atlas
            if lit: page.wait_for_function(f"__viewer.api.lighting().rooms['{zone}'].state==='loaded'", timeout=180000)
            s = page.evaluate('__viewer.api.state()')
            check(f'room {zone} opens on {cam}' + (' with its room lightmap' if lit else ' (vertex-lit room)'), s['room'] == zone and s['atCam'] == cam, s)
            page.wait_for_timeout(1200)
            page.screenshot(path=str(out / f'{w}_{zone}.png'))
        # photoreal still for the last room
        tap('#bPhoto'); page.wait_for_function("document.getElementById('photo').classList.contains('show')", timeout=60000)
        nat = page.evaluate("document.getElementById('photoImg').naturalWidth"); check('photoreal still loads', nat > 0, nat)
        tap('#photoClose'); page.wait_for_timeout(900); check('photoreal closes', page.evaluate("document.getElementById('photo').classList.contains('hidden')"))
        # walk
        tap('#mWalk'); page.wait_for_function("__viewer.api.state().mode==='walk'", timeout=30000); settle(page, 240000)
        p0 = page.evaluate('__viewer.api.walkState().position')
        if touch:
            pad = page.locator('#pad button[data-k="KeyW"]'); check('touch walk pad visible', pad.is_visible())
            box = pad.bounding_box(); page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
            page.dispatch_event('#pad button[data-k="KeyW"]', 'pointerdown')
        else:
            page.keyboard.down('KeyW')
        try:   # software WebGL draws about one frame a second: hold until the walker has moved (at most 60 s)
            page.wait_for_function('p => { const n = __viewer.api.walkState().position; return Math.hypot(n[0] - p[0], n[2] - p[2]) > .3; }', arg=p0, timeout=60000)
        except Exception:
            pass
        if touch: page.dispatch_event('#pad button[data-k="KeyW"]', 'pointerup')
        else: page.keyboard.up('KeyW')
        page.wait_for_timeout(800)
        p1 = page.evaluate('__viewer.api.walkState().position')
        moved = ((p1[0] - p0[0]) ** 2 + (p1[2] - p0[2]) ** 2) ** .5
        check('walk forward moves the eye', moved > .25, {'from': p0, 'to': p1})
        check('walk stays on free floor', not page.evaluate('p=>__viewer.api.blocked(p[0],p[2])', p1))
        page.screenshot(path=str(out / f'{w}_walk.png'))
        page.keyboard.press('Escape'); page.wait_for_timeout(600)
        if page.evaluate('__viewer.api.state().mode') == 'walk': page.keyboard.press('Escape'); page.wait_for_timeout(600)
        settle(page); check('Escape leaves walk', page.evaluate('__viewer.api.state().mode') == 'overview')
        # overview tools
        for bid in ['vIso', 'vTop', 'vCeil', 'vLabels', 'vReset']:
            tap('#' + bid); settle(page)
        check('overview tools run', page.evaluate('__viewer.api.state().mode') == 'overview')
        page.screenshot(path=str(out / f'{w}_overview.png'))
        check('no page or console errors', not R['errors'], R['errors'][:5])
        check('no HTTP errors', not R['http_errors'], R['http_errors'][:5])
        check('no failed requests', not R['failed_requests'], R['failed_requests'][:5])
    except Exception as e:
        R['exception'] = str(e); check('completed', False, str(e))
    finally:
        R['seconds'] = round(time.monotonic() - t0, 1)
        R['passed'] = all(c['passed'] for c in R['checks'])
        (out / f'smoke-{w}x{h}.json').write_text(json.dumps(R, indent=2))
        b.close()
print(json.dumps({'passed': R['passed'], 'failed': [c['name'] for c in R['checks'] if not c['passed']], 'seconds': R['seconds']}))
