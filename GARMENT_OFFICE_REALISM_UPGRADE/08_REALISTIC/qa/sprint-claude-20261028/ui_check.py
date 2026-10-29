"""Local Chromium checks of the /realistic/ toolbar, labels, People toggle and direct drag (based on GPT's verify_ui_drag.py).

LOCAL browser equivalent (serve_preview.py routes), software WebGL. Not live-site, Safari or MacBook proof.
python3 ui_check.py --url http://127.0.0.1:8784/realistic/?room=Z02&welcome=0 --out DIR [--people 27]
"""
import argparse, hashlib, json, time
from pathlib import Path
from playwright.sync_api import sync_playwright

p = argparse.ArgumentParser()
p.add_argument('--url', default='http://127.0.0.1:8784/realistic/?room=Z02&welcome=0')
p.add_argument('--out', required=True)
p.add_argument('--people', type=int, default=27)
p.add_argument('--sizes', default='1440x900,390x844,360x740')
a = p.parse_args()
out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
report = {'scope': 'LOCAL Chromium (SwiftShader) via serve_preview.py; not live, Safari or MacBook proof', 'url': a.url, 'views': [], 'checks': []}
IDS = ['mTour', 'mOverview', 'mRooms', 'mWalk', 'mPeople', 'mHelp', 'mFull']


def check(name, ok, value=None):
    report['checks'].append({'name': name, 'passed': bool(ok), 'value': value})


def luminance(rgb):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def parse(c):
    v = [float(x) for x in c[c.index('(') + 1:c.index(')')].split(',')]
    return v[:3], (v[3] if len(v) > 3 else 1.0)


with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True,
                           args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    for size in a.sizes.split(','):
        w, h = map(int, size.split('x'))
        c = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1, has_touch=w < 600)
        page = c.new_page()
        v = {'viewport': [w, h], 'errors': [], 'failed_requests': [], 'http_errors': []}
        report['views'].append(v)
        page.on('pageerror', lambda e, v=v: v['errors'].append(str(e)))
        page.on('console', lambda m, v=v: v['errors'].append(m.text) if m.type == 'error' else None)
        page.on('requestfailed', lambda q, v=v: v['failed_requests'].append({'url': q.url, 'failure': q.failure}))
        page.on('response', lambda r, v=v: v['http_errors'].append({'url': r.url, 'status': r.status}) if r.status >= 400 else None)
        t = time.monotonic()
        try:
            page.goto(a.url, wait_until='domcontentloaded', timeout=60000)
            page.wait_for_function('window.__viewer?.ready', timeout=180000)
            v['model_ready_seconds_local'] = round(time.monotonic() - t, 3)
            page.wait_for_function(f'__viewer.api.peopleStats().loaded && __viewer.api.peopleStats().total==={a.people} && !__viewer.api.state().flying', timeout=240000)
            page.wait_for_timeout(1500)
            v['settled_seconds_local'] = round(time.monotonic() - t, 3)
            v['state'] = page.evaluate('__viewer.api.state()')
            v['controls'] = page.evaluate("""ids => Object.fromEntries(ids.map(id => { const e = document.getElementById(id), r = e.getBoundingClientRect(), s = getComputedStyle(e);
              return [id, {x: r.x, y: r.y, width: r.width, height: r.height, right: r.right, bottom: r.bottom, color: s.color, background: s.backgroundColor,
                display: s.display, visibility: s.visibility, pressed: e.getAttribute('aria-pressed'), text: e.textContent.trim()}]; }))""", IDS)
            inside = {k: z['x'] >= -0.1 and z['right'] <= w + .1 and z['width'] >= 30 and z['height'] >= 30 for k, z in v['controls'].items()}
            check(f'{w}: every toolbar control fully inside the viewport and at least 30 px', all(inside.values()), inside)
            boxes = list(v['controls'].items()); overlaps = []
            for i in range(len(boxes)):
                for j in range(i + 1, len(boxes)):
                    A, B = boxes[i][1], boxes[j][1]
                    if A['x'] < B['right'] - 1 and B['x'] < A['right'] - 1 and A['y'] < B['bottom'] - 1 and B['y'] < A['bottom'] - 1:
                        overlaps.append([boxes[i][0], boxes[j][0]])
            check(f'{w}: toolbar controls do not overlap', not overlaps, overlaps)
            pc = v['controls']['mPeople']; fg, _ = parse(pc['color']); bg, alpha = parse(pc['background'])
            if alpha < 0.5:        # translucent: judge against the dark header band behind it
                bg = [bg[i] * alpha + 20 * (1 - alpha) for i in range(3)]
            L1, L2 = sorted([luminance(fg), luminance(bg)], reverse=True)
            ratio = (L1 + .05) / (L2 + .05)
            check(f'{w}: People button text contrast >= 4.5', ratio >= 4.5, round(ratio, 2))
            notes = page.evaluate("""() => { const d = document.getElementById('disclaimer'), r = d.getBoundingClientRect(), s = getComputedStyle(d), n = document.getElementById('peopleNote');
              return {text: d.innerText, fontSize: parseFloat(s.fontSize), visible: r.height > 0 && r.bottom <= innerHeight + 1, peopleNoteHidden: n.hidden}; }""")
            check(f'{w}: concept + illustrative-people notice visible (>= 11 px)', notes['visible'] and notes['fontSize'] >= 11 and not notes['peopleNoteHidden'] and 'illustrative' in notes['text'].lower(), notes)
            target = out / f'{w}_interactive_reception.png'
            page.screenshot(path=str(target), timeout=90000)
            v['screenshot'] = target.name; v['sha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
            if w < 700:   # phones: the room card (with its concept note folded to two lines) must leave most of the room visible
                card = page.evaluate("""() => { const i = document.getElementById('info'), n = document.getElementById('infoNote'), r = i.getBoundingClientRect();
                  return {cardHeight: Math.round(r.height), viewportHeight: innerHeight, share: +(r.height / innerHeight).toFixed(3), noteShown: !n.classList.contains('hidden'),
                    noteLines: Math.round(n.getBoundingClientRect().height / parseFloat(getComputedStyle(n).lineHeight))}; }""")
                check(f'{w}: room card with its concept note uses at most 40% of the screen height', card['noteShown'] and card['share'] <= 0.40, card)
                page.locator('#infoNote').click(); page.wait_for_timeout(250)
                opened = page.evaluate("document.getElementById('infoNote').classList.contains('open')")
                page.locator('#infoNote').click(); page.wait_for_timeout(250)
                check(f'{w}: tapping the concept note opens and folds it', opened and not page.evaluate("document.getElementById('infoNote').classList.contains('open')"))
            x, y = (w // 2 + 200, h // 2 - 100) if w > 600 else (w // 2, h // 2 - 40)
            # the first drag in a room view takes yaw / pitch from the camera; prime it so 'before' is the real look state
            page.mouse.move(x, y); page.mouse.down(); page.mouse.move(x + 2, y, steps=1); page.mouse.up()
            before = page.evaluate('__viewer.api.lookState()')
            page.mouse.move(x, y); page.mouse.down(); page.mouse.move(x + 60, y + 40, steps=3); page.mouse.up()
            after = page.evaluate('__viewer.api.lookState()')
            d = {'yaw': after['yaw'] - before['yaw'], 'pitch': after['pitch'] - before['pitch']}
            check(f'{w}: drag right/down moves the room with the pointer (yaw and pitch increase)', d['yaw'] > 0 and d['pitch'] > 0, d)
            page.locator('#mPeople').click(); page.wait_for_function('!__viewer.api.peopleStats().enabled', timeout=30000)
            check(f'{w}: People off', page.locator('#mPeople').get_attribute('aria-pressed') == 'false')
            page.locator('#mPeople').click(); page.wait_for_function('__viewer.api.peopleStats().enabled', timeout=30000)
            check(f'{w}: People on', page.locator('#mPeople').get_attribute('aria-pressed') == 'true')
            for bid in ['mHelp']:
                page.locator('#' + bid).click(); page.wait_for_timeout(300)
                check(f'{w}: Help opens', page.evaluate("!document.getElementById('welcome').classList.contains('hidden')"))
                page.keyboard.press('Escape'); page.wait_for_timeout(300)
            check(f'{w}: no page/console errors', not v['errors'], v['errors'][:5])
            check(f'{w}: no HTTP errors', not v['http_errors'], v['http_errors'][:5])
            v['status'] = 'checked'
        except Exception as e:
            v['status'] = 'failed'; v['exception'] = str(e); check(f'{w}: completed', False, str(e))
        finally:
            c.close(); (out / 'ui-checks.json').write_text(json.dumps(report, indent=2))
    b.close()
report['passed'] = all(x['passed'] for x in report['checks'])
(out / 'ui-checks.json').write_text(json.dumps(report, indent=2))
print(json.dumps({'passed': report['passed'], 'checks': len(report['checks']), 'failed': [x['name'] for x in report['checks'] if not x['passed']]}, indent=1))
