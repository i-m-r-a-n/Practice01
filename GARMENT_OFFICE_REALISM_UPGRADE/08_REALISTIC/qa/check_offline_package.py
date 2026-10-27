"""Check the actual offline resource resolver through loopback HTTP, not file://."""
import argparse,hashlib,json,threading
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
from capture_phase import HIDE

p=argparse.ArgumentParser()
p.add_argument('folder',type=Path);p.add_argument('camera');p.add_argument('people',type=int);p.add_argument('output',type=Path)
a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(a.folder.resolve())))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_address[1]}/'
report={'status':'running','scope':'Loopback HTTP offline-resource resolver; not native Mac/file protocol acceptance','errors':[],'outside_requests':[]}
try:
 with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    page=browser.new_page(viewport={'width':1280,'height':720})
    page.on('pageerror',lambda e:report['errors'].append(str(e)))
    page.on('console',lambda m:report['errors'].append(m.text) if m.type=='error' else None)
    def route(r):
        if r.request.url.startswith((base,'blob:','data:')):r.continue_()
        else:report['outside_requests'].append(r.request.url);r.abort()
    page.route('**/*',route)
    page.goto(base+'Office_Realistic_Tour.html?welcome=0',wait_until='domcontentloaded',timeout=120000)
    page.wait_for_function('window.__viewer?.ready',timeout=180000)
    page.evaluate('async()=>await __viewer.api.setPeopleEnabled(true)')
    report['frame']=page.evaluate('(name)=>__viewer.api.frameCamera(name)',a.camera)
    page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
    report['people']=page.evaluate('__viewer.api.peopleStats()')
    report['offline']=page.evaluate('window.__OFFLINE_STATS')
    report['errors']+=page.evaluate('__viewer.errors||[]')
    assert report['people']['total']==a.people and report['people']['frozen']
    assert not report['errors'] and not report['outside_requests'] and not report['offline']['missing']
    page.add_style_tag(content=HIDE);page.screenshot(path=str(a.output/'room.png'))
    report['image_sha256']=hashlib.sha256((a.output/'room.png').read_bytes()).hexdigest()
    report['offline_manifest_sha256']=hashlib.sha256((a.folder/'offline-manifest.json').read_bytes()).hexdigest()
    report['status']='passed';browser.close()
finally:
 server.shutdown();(a.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
