"""Plays the /bengal-earth-lab/ guided tour through its own UI, as a presenter would: the Tour button, Pause, then Next
at every stop after the camera flight lands. Checks that each stop's counter and title match the route config and that no page,
console or HTTP error appears. LOCAL Chromium with software WebGL; flights are slower than on a real GPU.
python3 -I bel_tour_play.py --out DIR [--url URL]"""
import argparse, json, time
from pathlib import Path
from playwright.sync_api import sync_playwright

p = argparse.ArgumentParser()
p.add_argument('--url', default='http://127.0.0.1:8790/bengal-earth-lab/?welcome=0')
p.add_argument('--out', required=True)
a = p.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
cfg = json.loads((Path(__file__).resolve().parents[2] / 'viewer' / 'bel-config.json').read_text())
R = {'url': a.url, 'scope': 'LOCAL Chromium (SwiftShader); the tour played through its own buttons', 'stops': [], 'errors': [], 'http_errors': []}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    page = b.new_page(viewport={'width': 1280, 'height': 800})
    page.on('pageerror', lambda e: R['errors'].append(str(e)))
    page.on('console', lambda m: R['errors'].append(m.text) if m.type == 'error' else None)
    page.on('response', lambda r: R['http_errors'].append({'url': r.url, 'status': r.status}) if r.status >= 400 else None)
    page.goto(a.url, wait_until='domcontentloaded', timeout=60000)
    page.wait_for_function('window.__viewer?.ready', timeout=240000)
    page.wait_for_function('__viewer.dressing && __viewer.dressing.concept', timeout=300000)
    page.evaluate("[...document.querySelectorAll('button')].find(x => /Tour$/.test(x.textContent.trim())).click()")
    page.wait_for_function('__viewer.api.state().tour', timeout=30000)
    page.evaluate("document.getElementById('tPlay').click()")   # pause auto-advance: the presenter steps with Next (software WebGL is slower than the hold time)
    page.wait_for_function('__viewer.api.state().tour.playing === false', timeout=10000)
    for k, st in enumerate(cfg['tour']):
        if k: page.evaluate("document.getElementById('tNext').click()")   # in-page clicks: the busy software renderer stalls Playwright's post-click waits
        t0 = time.monotonic()
        page.wait_for_function('__viewer.api.state().tour && __viewer.api.state().tour.phase === "hold"', timeout=120000)
        count, title, kicker = page.inner_text('#tCount'), page.inner_text('#tTitle'), page.inner_text('#tKicker')
        ok = count == f"Stop {k + 1} of {len(cfg['tour'])}" and title == st['title']
        R['stops'].append({'stop': k + 1, 'camera': st['camera'], 'counter': count, 'title': title, 'kicker': kicker, 'matches_config': ok, 'flight_seconds': round(time.monotonic() - t0, 1)})
        if k in (0, 6, 10, 16, len(cfg['tour']) - 1): page.screenshot(path=str(out / f'tour_stop_{k + 1:02d}.png'))
        print(k + 1, ok, title, flush=True)
    R['stills_switch_hidden'] = page.evaluate("getComputedStyle(document.getElementById('tPhoto').closest('label')).display === 'none'")   # what the presenter sees, not the attribute
    R['menu_groups'] = page.evaluate("[...document.querySelectorAll('#roomList .grp')].map(x => x.textContent)")
    R['option_a_rooms_in_menu'] = page.evaluate("[...document.querySelectorAll('#roomList .room')].filter(b => ['Z07','Z06'].includes(b.dataset.zone)).map(b => b.textContent)")
    b.close()
R['passed'] = all(s['matches_config'] for s in R['stops']) and len(R['stops']) == len(cfg['tour']) and not R['errors'] and not R['http_errors'] and R['stills_switch_hidden']
(out / 'tour-play.json').write_text(json.dumps(R, indent=2) + '\n')
print(json.dumps({'passed': R['passed'], 'stops': len(R['stops']), 'errors': R['errors'][:3]}))
