"""Actual local baseline browser captures; never labelled as live deployment QA."""
import argparse,json,time,hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8784/realistic/?welcome=0');p.add_argument('--output',default='local-baseline');a=p.parse_args()
base=Path(__file__).resolve().parent;out=base/a.output;out.mkdir(parents=True,exist_ok=True)
cameras=['CAM_01_Reception_A','CAM_04_Experience_Centre_A','CAM_09_Boardroom_A','CAM_07_MD_Office_A','CAM_34_Merchandising_Sample_Hub','CAM_13_Design_Studio_A']
hide='#top,#side,#sideOpen,#info,#viewbar,#tourbar,#disclaimer,#labels,#minimap,#walkhint,#pad,#dock,#welcome,#dissolve,#photo{display:none!important}'
report={'url':a.url,'scope':'LOCAL browser equivalent. Not a live-site browser capture or Mac performance claim.','started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'views':[]}
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
 for width,height in [(1440,900),(390,844)]:
  r={'viewport':[width,height],'console_errors':[],'page_errors':[],'failed_requests':[],'http_errors':[],'shots':[],'status':'running'};report['views'].append(r)
  c=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1);page=c.new_page()
  page.on('console',lambda m:r['console_errors'].append(m.text) if m.type=='error' else None);page.on('pageerror',lambda e:r['page_errors'].append(str(e)));page.on('requestfailed',lambda q:r['failed_requests'].append({'url':q.url,'failure':q.failure}));page.on('response',lambda res:r['http_errors'].append({'url':res.url,'status':res.status}) if res.status>=400 else None)
  start=time.monotonic()
  try:
   page.goto(a.url,wait_until='domcontentloaded',timeout=60000);page.wait_for_function("window.__viewer?.ready && typeof __viewer.api?.frameCamera==='function'",timeout=180000)
   r['model_ready_seconds_local']=round(time.monotonic()-start,3);r['gpu']=page.evaluate('__viewer.api.gpuInfo?.() || null');r['browser']=browser.version
   page.evaluate('async()=>{await __viewer.api.setPeopleEnabled(true)}');r['people']=page.evaluate('__viewer.api.peopleStats()')
   if r['people'].get('total')!=27: raise RuntimeError('Expected 27 illustrative figures')
   r['people_ready_seconds_local']=round(time.monotonic()-start,3)
   for name in cameras:
    state=page.evaluate('name=>__viewer.api.frameCamera(name)',name);page.evaluate('()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
    target=out/f'{width}_{name}_ui.png';page.screenshot(path=str(target),timeout=90000)
    shot={'camera':name,'file':target.name,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'state':state};r['shots'].append(shot)
    if width==1440:
     css=page.add_style_tag(content=hide);clean=out/f'{width}_{name}_room.png';page.screenshot(path=str(clean),timeout=90000);css.evaluate('(el)=>el.remove()');shot['clean_file']=clean.name;shot['clean_sha256']=hashlib.sha256(clean.read_bytes()).hexdigest()
    (out/'capture.json').write_text(json.dumps(report,indent=2));print(width,name,flush=True)
   r['status']='captured'
  except Exception as e:r['status']='failed';r['error']=str(e)
  finally:
   r['elapsed_seconds']=round(time.monotonic()-start,3);c.close();(out/'capture.json').write_text(json.dumps(report,indent=2))
 browser.close()
print(json.dumps({'views':[{'viewport':r['viewport'],'status':r['status'],'model_ready_seconds_local':r.get('model_ready_seconds_local'),'shots':len(r['shots']),'errors':r.get('error')} for r in report['views']]}))
