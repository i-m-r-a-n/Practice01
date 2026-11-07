"""The light images page of the proposal route (images.html, 1 Nov 2026), LOCAL Chromium via serve_preview.py, desktop and phone:
- 23 stop cards in tour order and 3 room cards, each with its title and kind label; every thumbnail loads; each AI image links its 3D model view;
- the Woven Earth set (the owner's entrance brief, 7 Nov 2026) follows in its own grid, in the config's order, renders labelled as renders
  and the materials board as a diagram;
- a tap opens the full image with its label, and Esc (desktop) or the close button (phone) closes it; no sideways scrolling on a phone;
- the 3D page links the images page while it loads, and offers it instead when the 3D cannot be shown.
python3 -I bel_images_page_check.py --out DIR [--base URL]"""
import argparse, json
from pathlib import Path
from playwright.sync_api import sync_playwright

p = argparse.ArgumentParser()
p.add_argument('--base', default='http://127.0.0.1:8790/stage2-concept/')
p.add_argument('--out', required=True)
a = p.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
cfg = json.loads((Path(__file__).resolve().parents[2] / 'viewer' / 'bel-config.json').read_text())
titles = [t['title'] for t in cfg['tour'] if t['camera'] in cfg['conceptStills']]
models = sum(1 for v in cfg['conceptStills'].values() if v.get('kind') == 'ai' and v.get('model'))
woven = cfg.get('wovenEarth', [])
R = {'base': a.base, 'scope': 'LOCAL Chromium via serve_preview.py; touch emulated; not a real phone or Safari', 'runs': {}, 'errors': [], 'http_errors': []}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    for name, args in (('desktop', {'viewport': {'width': 1440, 'height': 900}}),
                       ('phone', {'viewport': {'width': 390, 'height': 844}, 'is_mobile': True, 'has_touch': True, 'device_scale_factor': 2})):
        ctx = b.new_context(**args); page = ctx.new_page(); run = {}
        page.on('pageerror', lambda e: R['errors'].append(f'{name}: ' + str(e)[:300]))
        page.on('response', lambda r: R['http_errors'].append({'url': r.url, 'status': r.status}) if r.status >= 400 else None)
        page.goto(a.base + 'images.html', wait_until='load', timeout=60000)
        cards = page.evaluate("[...document.querySelectorAll('main .grid')].map(g => [...g.querySelectorAll('.card')].map(c => ({ title: c.querySelector('h2').textContent, kind: c.querySelector('.kind').textContent, model: !!c.querySelector('a.model') })))")
        run['stops'], run['rooms'], run['woven'] = len(cards[0]), len(cards[1]), len(cards[2]) if len(cards) > 2 else 0
        run['woven_ok'] = len(cards) > 2 and [c['title'] for c in cards[2]] == [w['title'] for w in woven] and all(
            ('Diagram' in c['kind']) if w['kind'] == 'board' else ('Rendered from the 3D model' in c['kind']) for c, w in zip(cards[2], woven))
        run['order_ok'] = [c['title'] for c in cards[0]] == titles
        run['labels_ok'] = all(('AI concept image' in c['kind']) != ('Rendered from the 3D model' in c['kind']) for c in cards[0] + cards[1])
        run['model_links'] = sum(c['model'] for c in cards[0] + cards[1])
        run['thumbs_loaded'] = page.evaluate("""async () => (await Promise.all([...document.querySelectorAll('.card img')].map(img => new Promise(ok => { const i = new Image(); i.onload = () => ok(i.naturalWidth > 0); i.onerror = () => ok(false); i.src = img.src; })))).filter(Boolean).length""")
        run['sideways'] = page.evaluate("document.documentElement.scrollWidth > innerWidth + 1")
        run['links'] = page.evaluate("[...document.querySelectorAll('.go a')].map(x => x.getAttribute('href'))")
        page.screenshot(path=str(out / f'{name}_images_page.png'), timeout=120000)
        page.click('.card a.full'); page.wait_for_function("document.getElementById('view').classList.contains('on') && document.querySelector('#view img').complete && document.querySelector('#view img').naturalWidth > 0", timeout=30000)
        run['viewer_label'] = page.evaluate("document.querySelector('#view .tag').textContent")
        page.wait_for_timeout(500); page.screenshot(path=str(out / f'{name}_full_view.png'), timeout=120000)
        if name == 'phone': page.click('#view button')
        else: page.keyboard.press('Escape')
        page.wait_for_timeout(300); run['viewer_closed'] = not page.evaluate("document.getElementById('view').classList.contains('on')")
        # the 3D page: the link while it loads, and the offer when the 3D cannot be shown
        page.goto(a.base + '?welcome=0', wait_until='domcontentloaded', timeout=60000)
        page.wait_for_function("window.__viewerStarted", timeout=60000)
        run['loading_link'] = page.evaluate("(() => { const l = document.getElementById('loadAlt'); return !l.classList.contains('hidden') && l.getAttribute('href') === 'images.html' && getComputedStyle(l).display !== 'none'; })()")
        page.screenshot(path=str(out / f'{name}_loading_link.png'), timeout=120000)
        page.evaluate("window.__fail('Test of the failure message')")
        run['fail_offer'] = page.evaluate("(() => { const l = document.getElementById('loadAlt'); return !l.classList.contains('hidden') && l.textContent; })()")
        ctx.close()
        run['passed'] = bool(run['stops'] == len(titles) == 23 and run['rooms'] == 3 and run['order_ok'] and run['labels_ok'] and run['model_links'] == models
                             and run['woven'] == len(woven) >= 9 and run['woven_ok'] and run['thumbs_loaded'] == 23 + 3 + len(woven) and not run['sideways'] and run['links'] == ['./', './?walk=1'] and run['viewer_label'].startswith(('AI concept image', 'Rendered from the 3D model'))
                             and run['viewer_closed'] and run['loading_link'] and run['fail_offer'] == 'See the tour in images instead')
        R['runs'][name] = run; print(name, json.dumps(run), flush=True)
    b.close()
R['passed'] = all(r['passed'] for r in R['runs'].values()) and not R['errors'] and not R['http_errors']
(out / 'images-page-check.json').write_text(json.dumps(R, indent=2) + '\n')
print(json.dumps({'passed': R['passed'], 'errors': R['errors'][:5], 'http_errors': R['http_errors'][:5]}))
