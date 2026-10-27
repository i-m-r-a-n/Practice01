import base64,http.server,pathlib,threading,functools,json
from playwright.sync_api import sync_playwright
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[3]
class Quiet(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)));threading.Thread(target=server.serve_forever,daemon=True).start()
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage']);page=browser.new_page(viewport={'width':1024,'height':1024},device_scale_factor=1);errs=[];page.on('pageerror',lambda e:errs.append(str(e)));page.goto(f'http://127.0.0.1:{server.server_port}/'+str((HERE/'screen-atlas-preview.html').relative_to(ROOT)));page.wait_for_function('window.qaReady===true',timeout=30000);raw=page.evaluate('window.atlasData');(HERE/'screen-content-atlas.png').write_bytes(base64.b64decode(raw.split(',')[1]));page.screenshot(path=str(HERE/'screen-atlas-browser.png'));(HERE/'screen-atlas-browser-check.json').write_text(json.dumps({'browser':browser.version,'runtime':'Linux Chromium headless','page_errors':errs,'canvas_size':[2048,2048],'scope':'Actual glyph/client-logo Canvas artwork capture only, not integrated WebGL screen shading/framing acceptance'},indent=2)+'\n');browser.close()
server.shutdown()
