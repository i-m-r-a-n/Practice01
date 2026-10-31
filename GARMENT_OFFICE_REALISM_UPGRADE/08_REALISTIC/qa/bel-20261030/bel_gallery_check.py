"""The tour in images on the proposal route (31 Oct 2026), LOCAL Chromium via serve_preview.py. Desktop and phone (390 x 844, touch):
- the welcome card offers "Images" as a fourth way, and the toolbar has an Images button;
- the grid shows one card per tour stop that has an image, in tour order, each with its stop number, title and kind
  (gold "AI concept image · fictional people" or green "Rendered from the 3D model · no people"), and the note about both kinds;
- every card's thumbnail loads, and on a phone the grid fits the width (two columns, no sideways scroll);
- Esc (desktop) or the close button (phone) closes it; a tap on the stop 5 card starts the tour at stop 5 and shows its render;
- ?images=1 opens the grid straight away.
python3 -I bel_gallery_check.py --out DIR [--url URL]"""
import argparse, json
from pathlib import Path
from playwright.sync_api import sync_playwright

p = argparse.ArgumentParser()
p.add_argument('--url', default='http://127.0.0.1:8790/stage2-concept/')
p.add_argument('--out', required=True)
a = p.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
R = {'url': a.url, 'scope': 'LOCAL Chromium (SwiftShader) via serve_preview.py; touch emulated; not a real phone or Safari', 'runs': {}, 'errors': [], 'http_errors': []}
shown = "id => { const e = document.getElementById(id); return !!e && !e.hidden && !e.classList.contains('hidden') && getComputedStyle(e).display !== 'none' && e.getBoundingClientRect().width > 0; }"
photo_on = "(() => { const p = document.getElementById('photo'); return !p.classList.contains('hidden') && p.classList.contains('show'); })()"
ready = 'window.__viewer?.ready && __viewer.dressing && __viewer.dressing.concept'
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    for name, args in (('desktop', {'viewport': {'width': 1440, 'height': 900}}),
                       ('phone', {'viewport': {'width': 390, 'height': 844}, 'is_mobile': True, 'has_touch': True, 'device_scale_factor': 2})):
        ctx = b.new_context(**args); page = ctx.new_page(); run = {}
        page.on('pageerror', lambda e: R['errors'].append(f'{name}: ' + str(e)[:300]))
        page.on('response', lambda r: R['http_errors'].append({'url': r.url, 'status': r.status}) if r.status >= 400 else None)
        page.goto(a.url + '?welcome=1', wait_until='domcontentloaded', timeout=60000)
        page.wait_for_function(ready, timeout=300000); page.wait_for_timeout(800)
        cfg = page.evaluate("window.__TOUR_CONFIG")
        expected = [i + 1 for i, t in enumerate(cfg['tour']) if t['camera'] in cfg['conceptStills']]
        kinds = {i + 1: cfg['conceptStills'][t['camera']]['kind'] for i, t in enumerate(cfg['tour']) if t['camera'] in cfg['conceptStills']}
        run['welcome_way'] = page.evaluate(f"({shown})('wGallery')") and page.evaluate("document.querySelector('.ways').classList.contains('four')")
        run['toolbar_button'] = page.evaluate(f"({shown})('mGallery')")
        page.screenshot(path=str(out / f'{name}_welcome.png'), timeout=120000)
        page.click('#wGallery'); page.wait_for_timeout(500)
        run['opened_from_welcome'] = page.evaluate(f"({shown})('gallery')") and not page.evaluate(f"({shown})('welcome')")
        cards = page.evaluate("[...document.querySelectorAll('#gGrid .gcard')].map(c => ({ stop: +c.dataset.stop, num: c.querySelector('.gnum').textContent, title: c.querySelector('b').textContent, kind: c.classList.contains('render') ? 'render' : 'ai', tag: c.querySelector('em').textContent, src: c.querySelector('img').getAttribute('src') }))")
        run['cards'] = len(cards); run['stops_with_images'] = len(expected)
        run['order_ok'] = [c['stop'] for c in cards] == expected and all(c['num'] == f"Stop {c['stop']}" for c in cards)
        run['kinds_ok'] = all(c['kind'] == kinds[c['stop']] and c['tag'] == cfg['galleryKinds'][c['kind']] for c in cards)
        run['titles_ok'] = all(c['title'] == cfg['tour'][c['stop'] - 1]['title'] for c in cards)
        run['thumbs_used'] = sum(1 for c in cards if '/thumbs/' in c['src'])
        run['note_ok'] = page.evaluate("document.getElementById('gNote').textContent") == cfg['galleryNote']
        # every card shows its whole image (16:9) and its three text lines inside the card, not cut off
        run['cards_whole'] = page.evaluate("""[...document.querySelectorAll('#gGrid .gcard')].every(c => { const r = c.getBoundingClientRect(), i = c.querySelector('img').getBoundingClientRect(), t = c.querySelector('em').getBoundingClientRect();
          return Math.abs(i.height - i.width * 9 / 16) < 2 && t.height > 0 && t.bottom <= r.bottom + 0.5 && t.top >= i.bottom; })""")
        loaded = page.evaluate("""async () => Promise.all([...document.querySelectorAll('#gGrid img')].map(img => new Promise(ok => { const i = new Image(); i.onload = () => ok(i.naturalWidth); i.onerror = () => ok(0); i.src = img.src; })))""")
        run['thumbs_loaded'] = sum(1 for w in loaded if w > 0)
        page.wait_for_timeout(1500); page.screenshot(path=str(out / f'{name}_gallery.png'), timeout=120000)
        geo = page.evaluate("(() => { const g = document.getElementById('gGrid'); const cols = getComputedStyle(g).gridTemplateColumns.split(' ').length; return { cols, sideways: g.scrollWidth > g.clientWidth + 1, page_sideways: document.documentElement.scrollWidth > innerWidth + 1 }; })()")
        run['grid'] = geo
        if name == 'phone':
            page.evaluate("document.getElementById('gGrid').scrollTop = 99999"); page.wait_for_timeout(1200)
            page.screenshot(path=str(out / f'{name}_gallery_end.png'), timeout=120000)
            page.click('#gClose')
        else:
            page.keyboard.press('Escape')
        page.wait_for_timeout(400)
        run['closed'] = not page.evaluate(f"({shown})('gallery')")
        # the toolbar button opens it again; a tap on stop 5 starts the tour there
        page.click('#mGallery'); page.wait_for_timeout(400)
        run['opened_from_toolbar'] = page.evaluate(f"({shown})('gallery')")
        page.click('#gGrid .gcard[data-stop="5"]')
        page.wait_for_timeout(400)
        run['gallery_closed_on_tap'] = not page.evaluate(f"({shown})('gallery')")
        run['tour_stop'] = page.evaluate("document.getElementById('tCount').textContent")
        run['mode'] = page.evaluate("document.body.dataset.mode")
        try:
            page.wait_for_function(photo_on, timeout=90000)
            run['stop5_image'] = page.evaluate("document.getElementById('photoImg').getAttribute('src')")
            run['stop5_tag'] = page.evaluate("document.querySelector('#photo .photo-tag').textContent")
        except Exception:
            run['stop5_image'] = None; run['stop5_tag'] = None
        page.wait_for_timeout(1000); page.screenshot(path=str(out / f'{name}_stop5_from_gallery.png'), timeout=120000)
        ctx.close()
        # a link straight to the images
        ctx = b.new_context(**args); page = ctx.new_page()
        page.on('pageerror', lambda e: R['errors'].append(f'{name} link: ' + str(e)[:300]))
        page.goto(a.url + '?images=1', wait_until='domcontentloaded', timeout=60000)
        page.wait_for_function(ready, timeout=300000); page.wait_for_timeout(600)
        run['link_opens'] = page.evaluate(f"({shown})('gallery')") and not page.evaluate(f"({shown})('welcome')")
        ctx.close()
        ok = (run['welcome_way'] and run['toolbar_button'] and run['opened_from_welcome'] and run['cards'] == len(expected) > 0 and run['order_ok'] and run['kinds_ok']
              and run['titles_ok'] and run['note_ok'] and run['cards_whole'] and run['thumbs_loaded'] == run['cards'] and run['thumbs_used'] == run['cards'] and not geo['sideways'] and not geo['page_sideways']
              and run['closed'] and run['opened_from_toolbar'] and run['gallery_closed_on_tap'] and run['tour_stop'].startswith('Stop 5 of') and run['mode'] == 'tour'
              and (run['stop5_image'] or '').endswith('render_CAM_04_Experience_Centre_A.jpg') and 'RENDERED FROM THE 3D MODEL' in (run['stop5_tag'] or '') and run['link_opens'])
        if name == 'phone': ok = ok and geo['cols'] == 2
        run['passed'] = bool(ok); R['runs'][name] = run; print(name, json.dumps(run), flush=True)
    b.close()
R['passed'] = all(r['passed'] for r in R['runs'].values()) and not R['errors'] and not R['http_errors']
(out / 'gallery-check.json').write_text(json.dumps(R, indent=2) + '\n')
print(json.dumps({'passed': R['passed'], 'errors': R['errors'][:5], 'http_errors': R['http_errors'][:5]}))
