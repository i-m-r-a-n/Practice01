"""Exercise the rebuilt offline package without Internet requests; capture six rooms."""
import argparse, hashlib, json, threading, time
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from playwright.sync_api import sync_playwright
from capture_phase import HIDE

CAMERAS=['CAM_01_Reception_A','CAM_09_Boardroom_A','CAM_04_Experience_Centre_A',
         'CAM_07_MD_Office_A','CAM_34_Merchandising_Sample_Hub','CAM_14_Design_Studio_B']

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('folder',type=Path);p.add_argument('output',type=Path)
    p.add_argument('--protocol',choices=['file','http'],default='http');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    server=None
    if a.protocol=='http':
        server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(a.folder.resolve())))
        threading.Thread(target=server.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{server.server_address[1]}/'
    else:base=a.folder.resolve().as_uri()+'/'
    report={'status':'running','protocol':a.protocol,'scope':'Linux Chromium software WebGL; not native Mac or Safari acceptance',
            'page_errors':[],'console_errors':[],'outside_requests':[],'failed_requests':[],'http_errors':[],'shots':[]}
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
            page=browser.new_page(viewport={'width':1440,'height':900})
            page.on('pageerror',lambda e:report['page_errors'].append(str(e)))
            page.on('console',lambda m:report['console_errors'].append(m.text) if m.type=='error' else None)
            page.on('requestfailed',lambda r:report['failed_requests'].append({'url':r.url,'failure':r.failure}))
            page.on('response',lambda r:report['http_errors'].append({'url':r.url,'status':r.status}) if r.status>=400 else None)
            def route(r):
                if r.request.url.startswith((base,'blob:','data:')):r.continue_()
                else:report['outside_requests'].append(r.request.url);r.abort()
            page.route('**/*',route);start=time.monotonic()
            page.goto(base+'Office_Realistic_Tour.html?welcome=0',wait_until='domcontentloaded',timeout=30000)
            page.wait_for_function('window.__viewer?.ready',timeout=120000)
            page.wait_for_function('window.__viewer.finishes || window.__viewer.errors.length',timeout=30000)
            report['ready_seconds']=round(time.monotonic()-start,3)
            page.evaluate('async()=>await __viewer.api.setPeopleEnabled(true)')
            page.add_style_tag(content=HIDE)
            for camera in CAMERAS:
                frame=page.evaluate('(name)=>__viewer.api.frameCamera(name)',camera)
                page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
                image=a.output/(camera+'.png');page.screenshot(path=str(image))
                report['shots'].append({'camera':camera,'frame':frame,'sha256':hashlib.sha256(image.read_bytes()).hexdigest()})
            report['people']=page.evaluate('__viewer.api.peopleStats()')
            report['dressing']=page.evaluate('__viewer.dressing')
            report['finishes']=page.evaluate('__viewer.finishes||null')
            report['config']=page.evaluate('window.__TOUR_CONFIG')
            report['offline']=page.evaluate('window.__OFFLINE_STATS')
            report['viewer_errors']=page.evaluate('__viewer.errors||[]')
            assert report['people']['total']==27 and report['people']['frozen']
            assert len(report['dressing']['interior']['items'])>0
            assert report['finishes'] and report['finishes']['refined']
            assert not report['page_errors'] and not report['console_errors'] and not report['viewer_errors']
            assert not report['outside_requests'] and not report['offline']['missing'] and not report['http_errors']
            await_off=page.evaluate('async()=>{await __viewer.api.setPeopleEnabled(false);return __viewer.api.peopleStats()}')
            assert not await_off['enabled'];report['people_toggle_off']=await_off
            page.evaluate('async()=>await __viewer.api.setPeopleEnabled(true)')
            report['status']='passed';browser.close()
    except Exception as e:
        report['status']='failed';report['exception']=str(e)
    finally:
        if server:server.shutdown()
        (a.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['config','dressing','shots']}))
    if report['status']!='passed':raise SystemExit(1)

if __name__=='__main__':main()
