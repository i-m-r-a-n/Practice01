"""On-screen walk arrows of the proposal route (the owner, 31 Oct: arrows on every device), LOCAL Chromium via serve_preview.py.
Desktop (fine pointer) and phone (touch): the arrows are hidden in the overview and the tour, shown when walking and in a room
view at eye level; holding an arrow walks (the back arrow from the walk start, which faces the check-in desk; the walking speed while held), and in a room view it walks on from there.
Distances are small here because software WebGL draws few frames a second; the speed while held is the check.
python3 -I bel_arrows_check.py --out DIR [--url URL]"""
import argparse, json
from pathlib import Path
from playwright.sync_api import sync_playwright

p = argparse.ArgumentParser()
p.add_argument('--url', default='http://127.0.0.1:8790/stage2-concept/?welcome=0')
p.add_argument('--out', required=True)
a = p.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
R = {'url': a.url, 'scope': 'LOCAL Chromium (SwiftShader) via serve_preview.py; not live, Safari or phone hardware proof', 'runs': {}, 'errors': []}
visible = "(() => { const e = document.getElementById('pad'); return !e.classList.contains('hidden') && getComputedStyle(e).display !== 'none' && e.getBoundingClientRect().width > 0; })()"
pos = "window.__dbg().camera.position.toArray().map(v => +v.toFixed(3))"
def hold(page, sel):
    box = page.locator(sel).bounding_box()
    if not box: return 0.0
    page.mouse.move(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2); page.mouse.down(); top = 0.0
    for _ in range(6):
        page.wait_for_timeout(500); top = max(top, page.evaluate("Math.hypot(...__viewer.api.walkState().velocity)"))
    page.mouse.up(); page.wait_for_timeout(400)
    return round(top, 2)


with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    for name, ctx_args in (('desktop', {'viewport': {'width': 1440, 'height': 900}}),
                           ('phone', {'viewport': {'width': 390, 'height': 844}, 'is_mobile': True, 'has_touch': True, 'device_scale_factor': 2})):
        ctx = b.new_context(**ctx_args); page = ctx.new_page(); run = {}
        page.on('pageerror', lambda e: R['errors'].append(f'{name}: ' + str(e)[:300]))
        page.goto(a.url + '&debug=1', wait_until='domcontentloaded', timeout=60000)
        page.wait_for_function('window.__viewer?.ready && __viewer.dressing && __viewer.dressing.concept', timeout=300000)
        page.wait_for_timeout(1500)
        run['overview_hidden'] = not page.evaluate(visible)
        page.evaluate("__viewer.api.startWalk()"); page.wait_for_function("document.body.dataset.mode === 'walk'", timeout=60000)
        page.wait_for_function("(() => { const c = window.__dbg().camera.position; const k = c.toArray().join(); const ok = c.y < 2.4 && window.__lastK === k; window.__lastK = k; return ok; })()", polling=700, timeout=90000); page.wait_for_timeout(1000)
        run['walk_shown'] = page.evaluate(visible)
        p0 = page.evaluate(pos); btn = page.locator('#pad button[data-k="KeyS"]')   # back: the walk starts facing the check-in desk
        run['walk_speed_while_held'] = hold(page, '#pad button[data-k="KeyS"]')
        p1 = page.evaluate(pos); run['walk_moved_m'] = round(((p1[0] - p0[0]) ** 2 + (p1[2] - p0[2]) ** 2) ** .5, 2)
        page.screenshot(path=str(out / f'{name}_walk.png'))
        page.evaluate("__viewer.api.goOverview()"); page.wait_for_timeout(3000)
        run['overview_again_hidden'] = not page.evaluate(visible)
        page.evaluate("__viewer.api.selectRoom('Z30')"); page.wait_for_timeout(1500)
        page.wait_for_function("(() => { const c = window.__dbg().camera.position; const k = c.toArray().join(); const ok = c.y < 2.4 && window.__lastK === k; window.__lastK = k; return ok; })()", polling=700, timeout=90000); page.wait_for_timeout(1000)
        run['room_mode'] = page.evaluate("document.body.dataset.mode")
        try: page.wait_for_function(visible, timeout=8000); run['room_shown'] = True   # the arrows appear when the camera lands at eye level
        except Exception: run['room_shown'] = False
        page.screenshot(path=str(out / f'{name}_room.png'))
        p0 = page.evaluate(pos); run['room_speed_while_held'] = hold(page, '#pad button[data-k="KeyW"]')
        p1 = page.evaluate(pos); run['room_moved_m'] = round(((p1[0] - p0[0]) ** 2 + (p1[2] - p0[2]) ** 2) ** .5, 2)
        run['after_room_press_mode'] = page.evaluate("document.body.dataset.mode")
        page.evaluate("__viewer.api.startTour(0)"); page.wait_for_timeout(3000)
        run['tour_hidden'] = not page.evaluate(visible)
        page.evaluate("__viewer.api.stopTour()"); ctx.close()
        run['passed'] = run['overview_hidden'] and run['walk_shown'] and run['walk_speed_while_held'] > 0.05 and run['overview_again_hidden'] and run['room_shown'] and run['room_speed_while_held'] > 0.05 and run['after_room_press_mode'] == 'walk' and run['tour_hidden']
        R['runs'][name] = run; print(name, json.dumps(run), flush=True)
    b.close()
R['passed'] = all(r['passed'] for r in R['runs'].values()) and not R['errors']
(out / 'arrows-check.json').write_text(json.dumps(R, indent=2) + '\n')
print(json.dumps({'passed': R['passed'], 'errors': R['errors'][:5]}))
