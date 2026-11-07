"""A phone held sideways on the proposal route (31 Oct 2026), LOCAL Chromium via serve_preview.py, touch emulated (not a real phone or Safari).
Sizes: 844 x 390 (a common phone) and 667 x 375 (a small phone).
- the header is one row and the footer one line, so the 3D keeps most of the height;
- while walking, the room card sits at the left and the arrows at the right, and the view above them is at least 45% of the height;
- a tap on the footer shows the whole note and a second tap folds it;
- the welcome card shows its four ways in two columns; the tour card and the tour in images fit;
- at a stop with an image, the kind label stays clear of the Back to 3D button, and the concept note is one line (a tap opens it);
- no page errors, and nothing makes the page scroll sideways.
python3 -I bel_landscape_check.py --out DIR [--url URL]"""
import argparse, json
from pathlib import Path
from playwright.sync_api import sync_playwright

p = argparse.ArgumentParser()
p.add_argument('--url', default='http://127.0.0.1:8790/stage2-concept/')
p.add_argument('--out', required=True)
a = p.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
R = {'url': a.url, 'scope': 'LOCAL Chromium (SwiftShader) via serve_preview.py; touch emulated; not a real phone or Safari', 'runs': {}, 'errors': []}
box = "id => { const e = document.getElementById(id); if (!e || e.classList.contains('hidden') || getComputedStyle(e).display === 'none') return null; const r = e.getBoundingClientRect(); return r.width ? { left: r.left, right: r.right, top: r.top, bottom: r.bottom, h: r.height } : null; }"
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    for W, H in ((844, 390), (667, 375)):
        name = f'{W}x{H}'
        ctx = b.new_context(viewport={'width': W, 'height': H}, is_mobile=True, has_touch=True, device_scale_factor=2); page = ctx.new_page(); run = {}
        page.on('pageerror', lambda e: R['errors'].append(f'{name}: ' + str(e)[:300]))
        page.goto(a.url + '?welcome=1&debug=1', wait_until='domcontentloaded', timeout=60000)
        page.wait_for_function('window.__viewer?.ready && __viewer.dressing && __viewer.dressing.concept', timeout=300000); page.wait_for_timeout(800)
        page.evaluate("try { localStorage.setItem('stage2-walk-help', '1'); } catch (e) {}")   # the help card has its own check
        run['welcome_cols'] = page.evaluate("getComputedStyle(document.querySelector('.ways')).gridTemplateColumns.split(' ').length")
        page.screenshot(path=str(out / f'{name}_welcome.png'), timeout=120000)
        page.click('#wClose'); page.wait_for_timeout(400)
        run['header_px'] = page.evaluate(f"({box})('top').h")
        page.evaluate("__viewer.api.startWalk()"); page.wait_for_function("document.body.dataset.mode === 'walk'", timeout=60000); page.wait_for_timeout(2500)
        run['footer_px'] = page.evaluate(f"({box})('disclaimer').h")
        info, pad, top = page.evaluate(f"({box})('info')"), page.evaluate(f"({box})('pad')"), page.evaluate(f"({box})('top')")
        run['info'] = info; run['pad'] = pad
        run['arrows_right'] = bool(pad and pad['right'] > W * 0.8)
        run['card_left'] = bool(info and info['left'] < W * 0.1 and (not pad or info['right'] < pad['left']))
        run['free_view_share'] = round((min(x['top'] for x in (info, pad) if x) - top['bottom']) / H, 2)
        run['sideways_scroll'] = page.evaluate("document.documentElement.scrollWidth > innerWidth + 1")
        page.screenshot(path=str(out / f'{name}_walk.png'), timeout=120000)
        page.click('#disclaimer'); page.wait_for_timeout(200); run['footer_open_px'] = page.evaluate(f"({box})('disclaimer').h")
        page.click('#disclaimer'); page.wait_for_timeout(200); run['footer_folded_px'] = page.evaluate(f"({box})('disclaimer').h")
        # the tour at stop 2 (its image: the Woven Earth render since 7 Nov 2026) and the tour in images
        page.evaluate("__viewer.api.startTour(1)"); page.wait_for_timeout(3000)
        try: page.wait_for_function("(() => { const p = document.getElementById('photo'); return !p.classList.contains('hidden') && p.classList.contains('show'); })()", timeout=90000); run['stop2_image'] = True
        except Exception: run['stop2_image'] = False
        page.wait_for_timeout(1500)
        tag, close = page.evaluate("document.querySelector('#photo .photo-tag').getBoundingClientRect().toJSON()"), page.evaluate("document.getElementById('photoClose').getBoundingClientRect().toJSON()")
        run['label_clear_of_back_button'] = tag['right'] <= close['left'] or tag['bottom'] <= close['top'] or tag['top'] >= close['bottom']
        run['tour_note_px'] = page.evaluate("(() => { const n = document.getElementById('tNote'); return n.classList.contains('hidden') ? 0 : n.getBoundingClientRect().height; })()")
        tb = page.evaluate(f"({box})('tourbar')"); run['tour_card'] = tb
        run['tour_card_fits'] = bool(tb and tb['top'] > top['bottom'] and tb['bottom'] <= H)
        page.screenshot(path=str(out / f'{name}_tour_stop2.png'), timeout=120000)
        page.evaluate("__viewer.api.stopTour()"); page.wait_for_timeout(800)
        page.evaluate("__viewer.api.openGallery()"); page.wait_for_timeout(1500)
        run['gallery_cols'] = page.evaluate("getComputedStyle(document.getElementById('gGrid')).gridTemplateColumns.split(' ').length")
        run['gallery_fits'] = page.evaluate("(() => { const r = document.querySelector('.gbox').getBoundingClientRect(); return r.top >= 0 && r.bottom <= innerHeight + 1 && r.right <= innerWidth + 1; })()")
        page.screenshot(path=str(out / f'{name}_gallery.png'), timeout=120000)
        ctx.close()
        run['passed'] = bool(run['header_px'] <= 52 and run['footer_px'] <= 26 and run['arrows_right'] and run['card_left'] and run['free_view_share'] >= 0.45
                             and not run['sideways_scroll'] and run['footer_open_px'] > run['footer_px'] + 8 and run['footer_folded_px'] == run['footer_px']
                             and run['welcome_cols'] == 2 and run['tour_card_fits'] and run['gallery_fits'] and run['gallery_cols'] >= 2
                             and run['stop2_image'] and run['label_clear_of_back_button'] and run['tour_note_px'] < 30)
        R['runs'][name] = run; print(name, json.dumps(run), flush=True)
    b.close()
R['passed'] = all(r['passed'] for r in R['runs'].values()) and not R['errors']
(out / 'landscape-check.json').write_text(json.dumps(R, indent=2) + '\n')
print(json.dumps({'passed': R['passed'], 'errors': R['errors'][:5]}))
