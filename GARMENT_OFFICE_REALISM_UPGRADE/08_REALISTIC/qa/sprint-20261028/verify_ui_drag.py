"""Browser verification of sprint UI and direct-drag fixes using local equivalent routes."""
import argparse,hashlib,json,time,math
from pathlib import Path
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8784/realistic/?room=Z02&welcome=0');a=p.parse_args()
root=Path(__file__).resolve().parent;out=root/'local-after';out.mkdir(exist_ok=True)
report={'scope':'LOCAL Chromium browser checks, not live or MacBook proof','url':a.url,'views':[],'checks':[]}
def check(name,ok,value=None): report['checks'].append({'name':name,'passed':bool(ok),'value':value})
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
 for w,h in [(1440,900),(390,844)]:
  c=b.new_context(viewport={'width':w,'height':h},device_scale_factor=1);page=c.new_page();v={'viewport':[w,h],'errors':[],'failed_requests':[]};report['views'].append(v)
  page.on('pageerror',lambda e:v['errors'].append(str(e)));page.on('console',lambda m:v['errors'].append(m.text) if m.type=='error' else None);page.on('requestfailed',lambda req:v['failed_requests'].append({'url':req.url,'failure':req.failure}))
  t=time.monotonic()
  try:
   page.goto(a.url,wait_until='domcontentloaded',timeout=60000);page.wait_for_function('window.__viewer?.ready',timeout=180000);v['model_ready_seconds_local']=round(time.monotonic()-t,3)
   page.wait_for_function('__viewer.api.peopleStats().loaded && __viewer.api.peopleStats().total===27 && !__viewer.api.state().flying',timeout=180000)
   v['settled_seconds_local']=round(time.monotonic()-t,3);v['state']=page.evaluate('__viewer.api.state()');v['people']=page.evaluate('__viewer.api.peopleStats()');v['controls']=page.evaluate("""()=>Object.fromEntries(['mTour','mOverview','mRooms','mWalk','mPeople','mHelp','mFull'].map(id=>{const e=document.getElementById(id),r=e.getBoundingClientRect(),s=getComputedStyle(e);return[id,{x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom,color:s.color,background:s.backgroundColor,display:s.display,visibility:s.visibility,pressed:e.getAttribute('aria-pressed')}]}))""")
   check(f'{w}:all toolbar controls inside viewport',all(z['x']>=-0.1 and z['right']<=w+.1 and z['width']>=20 and z['height']>=24 for z in v['controls'].values()),v['controls'])
   check(f'{w}:People visible',v['controls']['mPeople']['display']!='none')
   target=out/f'{w}_interactive_reception.png';page.screenshot(path=str(target),timeout=90000);v['screenshot']=target.name;v['sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
   before=page.evaluate('__viewer.api.lookState()');x,y=(950,320) if w>600 else (160,390)
   page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+60,y+40,steps=3);page.mouse.up();after=page.evaluate('__viewer.api.lookState()');d={'yaw':after['yaw']-before['yaw'],'pitch':after['pitch']-before['pitch'],'before':before,'after':after};check(f'{w}:right/down drag increases yaw and pitch',d['yaw']>0 and d['pitch']>0,d)
   page.locator('#mPeople').click();page.wait_for_function('!__viewer.api.peopleStats().enabled');check(f'{w}:People off button',page.locator('#mPeople').get_attribute('aria-pressed')=='false')
   page.locator('#mPeople').click();page.wait_for_function('__viewer.api.peopleStats().enabled');check(f'{w}:People on button',page.locator('#mPeople').get_attribute('aria-pressed')=='true')
   check(f'{w}:no page/console errors',not v['errors'],v['errors']);v['status']='checked'
  except Exception as e:v['status']='failed';v['exception']=str(e);check(f'{w}:completed',False,str(e))
  finally:c.close();(out/'ui-drag-checks.json').write_text(json.dumps(report,indent=2))
 b.close()
report['passed']=all(c['passed'] for c in report['checks']);(out/'ui-drag-checks.json').write_text(json.dumps(report,indent=2));print(json.dumps({'passed':report['passed'],'checks':len(report['checks']),'failed':[x for x in report['checks'] if not x['passed']]}))
