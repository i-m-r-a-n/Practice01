"""Phone walking on the proposal route (the owner, 31 Oct: "walk the factory with a phone"), LOCAL Chromium via serve_preview.py.
Phone (390 x 844, touch) and desktop runs:
- the help card shows the first time a phone walks, and "Got it" closes it;
- a finger slides from the up arrow to the right arrow and the held direction follows it;
- a tap (phone) or click (desktop) on the floor ahead sets a walk target and the visitor walks towards it;
- "Look by moving the phone" shows on the phone, turns on, and a device-orientation event turns the view.
Software WebGL draws few frames a second, so distances are small; the checks are the state changes and the direction of movement.
python3 -I bel_phone_walk_check.py --out DIR [--url URL]"""
import argparse, json, math
from pathlib import Path
from playwright.sync_api import sync_playwright

p = argparse.ArgumentParser()
p.add_argument('--url', default='http://127.0.0.1:8790/stage2-concept/?welcome=0')
p.add_argument('--out', required=True)
a = p.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
R = {'url': a.url, 'scope': 'LOCAL Chromium (SwiftShader) via serve_preview.py; touch emulated; not a real phone or Safari', 'runs': {}, 'errors': []}
settle = "(() => { const c = window.__dbg().camera.position; const k = c.toArray().join(); const ok = c.y < 2.4 && window.__lastK === k; window.__lastK = k; return ok; })()"
pos = "window.__dbg().camera.position.toArray()"
shown = "id => { const e = document.getElementById(id); return !!e && !e.classList.contains('hidden') && getComputedStyle(e).display !== 'none' && e.getBoundingClientRect().width > 0; }"
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    for name, args in (('phone', {'viewport': {'width': 390, 'height': 844}, 'is_mobile': True, 'has_touch': True, 'device_scale_factor': 2}),
                       ('desktop', {'viewport': {'width': 1440, 'height': 900}})):
        ctx = b.new_context(**args); page = ctx.new_page(); run = {}
        page.on('pageerror', lambda e: R['errors'].append(f'{name}: ' + str(e)[:300]))
        page.goto(a.url + '&debug=1', wait_until='domcontentloaded', timeout=60000)
        page.wait_for_function('window.__viewer?.ready && __viewer.dressing && __viewer.dressing.concept', timeout=300000)
        page.evaluate("try { localStorage.removeItem('stage2-walk-help'); } catch (e) {}")
        page.evaluate("__viewer.api.startWalk()"); page.wait_for_function("document.body.dataset.mode === 'walk'", timeout=60000)
        page.wait_for_function(settle, polling=700, timeout=90000); page.wait_for_timeout(800)
        run['help_shown'] = page.evaluate(f"({shown})('walkhelp')")
        if run['help_shown']:
            page.screenshot(path=str(out / f'{name}_help.png'), timeout=120000)
            page.click('#whOk'); page.wait_for_timeout(300)
        run['help_closed'] = not page.evaluate(f"({shown})('walkhelp')")
        # slide from the up arrow to the right arrow
        up = page.locator('#pad button[data-k="KeyW"]').bounding_box(); right = page.locator('#pad button[data-k="KeyD"]').bounding_box()
        page.mouse.move(up['x'] + up['width'] / 2, up['y'] + up['height'] / 2); page.mouse.down(); page.wait_for_timeout(400)
        run['held_first'] = page.evaluate("[...document.querySelectorAll('#pad button.on')].map(b => b.dataset.k)")
        page.mouse.move(right['x'] + right['width'] / 2, right['y'] + right['height'] / 2, steps=6); page.wait_for_timeout(400)
        run['held_after_slide'] = page.evaluate("[...document.querySelectorAll('#pad button.on')].map(b => b.dataset.k)")
        page.mouse.up(); page.wait_for_timeout(300)
        run['released'] = page.evaluate("document.querySelectorAll('#pad button.on').length") == 0
        # tap / click the floor low in the middle of the view: the floor just ahead, before the check-in desk the walk starts facing
        p0 = page.evaluate(pos); vw, vh = args['viewport']['width'], args['viewport']['height']
        if name == 'phone': page.touchscreen.tap(vw / 2, vh * 0.62)        # the floor ahead, above the compact walk card
        else: page.mouse.click(vw * 0.62, vh * 0.70)                       # the floor right of the check-in desk, clear of the card and the arrows
        page.wait_for_timeout(300)
        run['target_set'] = page.evaluate("!!window.__viewer.walkTarget")
        tgt = page.evaluate("window.__viewer.walkTarget && [window.__viewer.walkTarget.x, window.__viewer.walkTarget.z]")
        page.wait_for_timeout(4000)
        p1 = page.evaluate(pos)
        run['moved_m'] = round(math.hypot(p1[0] - p0[0], p1[2] - p0[2]), 2)
        if tgt:
            d0 = math.hypot(tgt[0] - p0[0], tgt[1] - p0[2]); d1 = math.hypot(tgt[0] - p1[0], tgt[1] - p1[2])
            run['closer_to_target_m'] = round(d0 - d1, 2)
        page.screenshot(path=str(out / f'{name}_tap_walk.png'), timeout=120000)
        # look by moving the phone
        run['gyro_button_shown'] = page.evaluate(f"({shown})('bGyro')")
        if run['gyro_button_shown']:
            page.click('#bGyro'); page.wait_for_timeout(300)
            run['gyro_on'] = page.evaluate("window.__viewer.gyro.on")
            y0 = page.evaluate("new (window.__dbg().THREE.Euler)().setFromQuaternion(window.__dbg().camera.quaternion, 'YXZ').y")
            page.evaluate("dispatchEvent(new DeviceOrientationEvent('deviceorientation', { alpha: 0, beta: 90, gamma: 0 }))"); page.wait_for_timeout(200)
            page.evaluate("dispatchEvent(new DeviceOrientationEvent('deviceorientation', { alpha: 40, beta: 90, gamma: 0 }))"); page.wait_for_timeout(400)
            y1 = page.evaluate("new (window.__dbg().THREE.Euler)().setFromQuaternion(window.__dbg().camera.quaternion, 'YXZ').y")
            run['gyro_turned_deg'] = round(math.degrees(math.atan2(math.sin(y1 - y0), math.cos(y1 - y0))), 1)
            page.click('#bGyro'); page.wait_for_timeout(200); run['gyro_off_again'] = not page.evaluate("window.__viewer.gyro.on")
        ctx.close()
        ok = run['help_closed'] and run['held_first'] == ['KeyW'] and run['held_after_slide'] == ['KeyD'] and run['released'] and run['target_set'] and run.get('closer_to_target_m', 0) > 0.02
        if name == 'phone': ok = ok and run['help_shown'] and run['gyro_button_shown'] and run.get('gyro_on') and abs(run.get('gyro_turned_deg', 0)) > 20 and run.get('gyro_off_again')
        else: ok = ok and not run['help_shown'] and not run['gyro_button_shown']
        run['passed'] = bool(ok); R['runs'][name] = run; print(name, json.dumps(run), flush=True)
    b.close()
R['passed'] = all(r['passed'] for r in R['runs'].values()) and not R['errors']
(out / 'phone-walk-check.json').write_text(json.dumps(R, indent=2) + '\n')
print(json.dumps({'passed': R['passed'], 'errors': R['errors'][:5]}))
