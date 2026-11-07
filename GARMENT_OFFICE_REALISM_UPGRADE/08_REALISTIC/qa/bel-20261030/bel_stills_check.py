"""The stop images of the proposal route (the owner's AI concept images, 31 Oct 2026, and the Cycles renders), LOCAL Chromium via serve_preview.py.
- the tour's switch reads "Show concept images" and starts on;
- stop 2, the arrival gallery, shows its Woven Earth render (7 Nov 2026) with the render label; stop 4 fades into its AI image with the
  AI label; stop 5 shows its Cycles render with the render label when the route has one, or no image;
- a room view that has an image offers it on its card (the MD office, Z12) and shows it;
- when an AI image has a render of the same view in the 3D model, "3D model view" shows it with the render label and "AI concept image" goes back;
- every configured image loads.
python3 -I bel_stills_check.py --out DIR [--url URL]"""
import argparse, json
from pathlib import Path
from playwright.sync_api import sync_playwright

p = argparse.ArgumentParser()
p.add_argument('--url', default='http://127.0.0.1:8790/stage2-concept/?welcome=0')
p.add_argument('--out', required=True)
a = p.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
R = {'url': a.url, 'scope': 'LOCAL Chromium (SwiftShader) via serve_preview.py', 'runs': {}, 'errors': [], 'http_errors': []}
photo_on = "(() => { const p = document.getElementById('photo'); return !p.classList.contains('hidden') && p.classList.contains('show'); })()"
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    for name, args in (('desktop', {'viewport': {'width': 1440, 'height': 900}}),
                       ('phone', {'viewport': {'width': 390, 'height': 844}, 'is_mobile': True, 'has_touch': True, 'device_scale_factor': 2})):
        ctx = b.new_context(**args); page = ctx.new_page(); run = {}
        page.on('pageerror', lambda e: R['errors'].append(f'{name}: ' + str(e)[:300]))
        page.on('response', lambda r: R['http_errors'].append({'url': r.url, 'status': r.status}) if r.status >= 400 else None)
        page.goto(a.url, wait_until='domcontentloaded', timeout=60000)
        page.wait_for_function('window.__viewer?.ready && __viewer.dressing && __viewer.dressing.concept', timeout=300000)
        run['switch_label'] = page.evaluate("document.getElementById('tPhoto').closest('label').textContent.trim()")
        run['switch_on'] = page.evaluate("document.getElementById('tPhoto').checked")
        stills = page.evaluate("window.__TOUR_CONFIG.conceptStills")
        run['images_load'] = page.evaluate("""async (s) => { const r = {}; for (const [k, v] of Object.entries(s)) for (const [n, u] of [[k, typeof v === 'string' ? v : v.src], [k + ' (3D view)', v?.model]]) if (u)
          r[n] = await new Promise(ok => { const i = new Image(); i.onload = () => ok(i.naturalWidth); i.onerror = () => ok(0); i.src = u; }); return r; }""", stills)
        # tour: stop 2 has its Woven Earth render
        page.evaluate("__viewer.api.startTour(1)")
        try: page.wait_for_function(photo_on, timeout=90000); run['stop2_image'] = True
        except Exception: run['stop2_image'] = False
        run['stop2_src'] = page.evaluate("document.getElementById('photoImg').getAttribute('src')")
        run['stop2_tag'] = page.evaluate("document.querySelector('#photo .photo-tag').textContent")
        page.wait_for_timeout(1200); page.screenshot(path=str(out / f'{name}_stop2_image.png'), timeout=120000)
        # stop 4 has an AI image
        page.evaluate("__viewer.api.goStop(3)")
        try: page.wait_for_function(photo_on + " && document.getElementById('photoImg').getAttribute('src').endsWith('BEL_CAM_SUN_WALL.jpg')", timeout=90000); run['stop4_image'] = True
        except Exception: run['stop4_image'] = False
        run['stop4_src'] = page.evaluate("document.getElementById('photoImg').getAttribute('src')")
        run['tag'] = page.evaluate("document.querySelector('#photo .photo-tag').textContent")
        page.wait_for_timeout(1200); page.screenshot(path=str(out / f'{name}_stop4_ai_image.png'), timeout=120000)
        # an AI image with a render of the same view in the 3D model: the switch shows the render with its own label, and back
        if isinstance(stills.get('BEL_CAM_SUN_WALL'), dict) and stills['BEL_CAM_SUN_WALL'].get('model'):
            paused = page.evaluate("(() => { const t = __viewer.api.state().tour; if (t && t.playing) { __viewer.api.togglePlay(); return true; } return false; })()")
            loaded = "(() => { const i = document.getElementById('photoImg'); return i.complete && i.naturalWidth > 0; })()"
            run['model_button'] = page.evaluate("document.getElementById('photoAlt').textContent")
            page.click('#photoAlt'); page.wait_for_timeout(300)
            try:
                page.wait_for_function("document.getElementById('photoImg').getAttribute('src').includes('model/render_BEL_CAM_SUN_WALL') && " + loaded, timeout=60000)
                run['model_tag'] = page.evaluate("document.querySelector('#photo .photo-tag').textContent"); run['model_button_after'] = page.evaluate("document.getElementById('photoAlt').textContent")
                page.wait_for_timeout(800); page.screenshot(path=str(out / f'{name}_stop4_model_view.png'), timeout=120000)
                page.click('#photoAlt'); page.wait_for_function("document.getElementById('photoImg').getAttribute('src').endsWith('/BEL_CAM_SUN_WALL.jpg') && " + loaded, timeout=60000)
                run['model_switch_ok'] = ('RENDERED FROM THE 3D MODEL' in run['model_tag'] and run['model_button'] == '3D model view' and run['model_button_after'] == 'AI concept image'
                                          and 'AI CONCEPT IMAGE' in page.evaluate("document.querySelector('#photo .photo-tag').textContent"))
            except Exception: run['model_switch_ok'] = False
            if paused: page.evaluate("__viewer.api.togglePlay()")
        else: run['model_switch_ok'] = None   # no 3D view of this AI image yet
        # stop 5: its Cycles render if the route has one, else no image
        page.evaluate("__viewer.api.goStop(4)")
        if 'CAM_04_Experience_Centre_A' in stills:
            try: page.wait_for_function(photo_on + " && document.getElementById('photoImg').getAttribute('src').includes('render_CAM_04')", timeout=90000); run['stop5_ok'] = 'RENDERED FROM THE 3D MODEL' in page.evaluate("document.querySelector('#photo .photo-tag').textContent")
            except Exception: run['stop5_ok'] = False
            page.wait_for_timeout(1000); page.screenshot(path=str(out / f'{name}_stop5_render.png'), timeout=120000)
        else:
            page.wait_for_timeout(12000); run['stop5_ok'] = not page.evaluate(photo_on)
        page.evaluate("__viewer.api.stopTour()"); page.wait_for_timeout(1500)
        # a room view with an image: the MD office
        page.evaluate("__viewer.api.selectRoom('Z12')")
        try:
            page.wait_for_function("!document.getElementById('bPhoto').classList.contains('hidden')", timeout=60000); run['room_button'] = page.evaluate("document.getElementById('bPhoto').textContent")
            page.click('#bPhoto'); page.wait_for_function(photo_on, timeout=60000); run['room_image'] = page.evaluate("document.getElementById('photoImg').getAttribute('src')")
        except Exception as e: run['room_button'] = None; run['room_image'] = None
        ctx.close()
        run['passed'] = (run['switch_label'] == 'Show concept images' and run['switch_on'] and all(v > 0 for v in run['images_load'].values()) and run['stop2_image']
                         and run['stop2_src'].endswith('render_CAM_03_Entrance_Lobby.jpg') and 'RENDERED FROM THE 3D MODEL' in run['stop2_tag']
                         and run['stop4_image'] and 'AI CONCEPT IMAGE' in run['tag'] and run['stop5_ok']
                         and run['room_button'] == 'Concept image' and (run['room_image'] or '').endswith('CAM_07_MD_Office_A.jpg') and run['model_switch_ok'] is not False)
        R['runs'][name] = run; print(name, json.dumps({k: v for k, v in run.items() if k != 'images_load'}), 'images', sum(1 for v in run['images_load'].values() if v > 0), '/', len(run['images_load']), flush=True)
    b.close()
R['passed'] = all(r['passed'] for r in R['runs'].values()) and not R['errors'] and not R['http_errors']
(out / 'stills-check.json').write_text(json.dumps(R, indent=2) + '\n')
print(json.dumps({'passed': R['passed'], 'errors': R['errors'][:5], 'http_errors': R['http_errors'][:5]}))
