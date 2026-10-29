"""Timeline of the GLB requests (CDP view) next to what the page itself receives (instrumented fetch): status, Content-Length, bytes read.

LOCAL Chromium via serve_preview.py. Written to explain the occasional net::ERR_ABORTED on GLB requests (see r2/abort-probe/).
python3 abort_probe.py [URL] [WxH] > trace.txt
"""
import json, sys, time
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8784/realistic/?room=Z02&welcome=0'
W, H = (int(v) for v in (sys.argv[2] if len(sys.argv) > 2 else '390x844').split('x'))
ev = []; t0 = time.monotonic()
T = lambda: round(time.monotonic() - t0, 2)
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    c = b.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1, has_touch=W < 600)
    c.add_init_script('''(() => { const f = window.fetch; window.__glb = []; window.fetch = async (...args) => { const u = String(args[0] && args[0].url || args[0]); const r = await f(...args);
      if (u.includes('people/assets/')) { const rec = {u: u.split('/').pop(), status: r.status, len: r.headers.get('content-length'), bytes: null}; window.__glb.push(rec); r.clone().arrayBuffer().then(b => rec.bytes = b.byteLength, e => rec.err = String(e)); } return r; }; })()''')
    page = c.new_page()
    keep = lambda u: '.glb' in u or '.ktx2' in u
    page.on('request', lambda q: ev.append([T(), 'start', q.url.split('/realistic/')[-1], q.headers.get('range'), q.resource_type]) if keep(q.url) else None)
    page.on('requestfinished', lambda q: ev.append([T(), 'done', q.url.split('/realistic/')[-1]]) if keep(q.url) else None)
    page.on('requestfailed', lambda q: ev.append([T(), 'FAILED ' + str(q.failure), q.url.split('/realistic/')[-1]]) if keep(q.url) else None)
    page.on('console', lambda m: ev.append([T(), 'console.' + m.type, m.text[:160]]) if m.type in ('error', 'warning') else None)
    page.goto(URL, wait_until='domcontentloaded', timeout=60000)
    page.wait_for_function('window.__viewer?.ready', timeout=180000); ev.append([T(), 'READY'])
    page.wait_for_function('__viewer.api.peopleStats().loaded && __viewer.api.peopleStats().total===27 && !__viewer.api.state().flying', timeout=240000); ev.append([T(), 'PEOPLE LOADED'])
    page.wait_for_timeout(1500); page.screenshot(path='probe.png', timeout=90000); ev.append([T(), 'SCREENSHOT'])
    x, y = (W // 2 + 200, H // 2 - 100) if W > 600 else (W // 2, H // 2 - 40)
    page.mouse.move(x, y); page.mouse.down(); page.mouse.move(x + 2, y, steps=1); page.mouse.up()
    page.mouse.move(x, y); page.mouse.down(); page.mouse.move(x + 60, y + 40, steps=3); page.mouse.up(); ev.append([T(), 'DRAGGED'])
    page.locator('#mPeople').click(); page.wait_for_function('!__viewer.api.peopleStats().enabled', timeout=30000); ev.append([T(), 'PEOPLE OFF'])
    page.locator('#mPeople').click(); page.wait_for_function('__viewer.api.peopleStats().enabled', timeout=30000); ev.append([T(), 'PEOPLE ON'])
    page.locator('#mHelp').click(); page.wait_for_timeout(300); page.keyboard.press('Escape'); page.wait_for_timeout(300); ev.append([T(), 'HELP'])
    page.wait_for_timeout(15000); ev.append([T(), 'after 15 s idle'])
    ev.append([T(), 'JS FETCH VIEW', page.evaluate('window.__glb')])
    c.close(); ev.append([T(), 'CONTEXT CLOSED'])
    b.close()
for e in ev: print(json.dumps(e))
