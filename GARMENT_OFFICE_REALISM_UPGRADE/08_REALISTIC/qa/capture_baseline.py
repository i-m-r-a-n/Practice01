"""Capture the deployed production scene from all approved cameras, without changing it.

HTTPS responses are fetched through urllib with the managed proxy CA, then passed
byte-for-byte to Chromium. Only app.js receives a documented QA export of its
existing renderer/scene/camera; it does not alter meshes, materials or lighting.
The QA hook permits exact orthographic cameras, which the UI approximates with
perspective. Those five images are scene comparisons, not existing UI screenshots.
"""
import hashlib, json, time, urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).parent/'baseline'
RAW=OUT/'production-responses'
SHOTS=OUT/'shots'
for p in [OUT,RAW,SHOTS]:p.mkdir(parents=True,exist_ok=True)
ORIGIN='https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/'
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
metadata=json.loads((ROOT/'GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/office_web_metadata.json').read_text())
log={'origin':ORIGIN,'viewport':[1280,720],'source':'deployed production bytes; QA-only renderer export appended','shots':[],'errors':[],'responses':[],'not_verified':['Real MacBook GPU','Chrome macOS','Firefox macOS','Safari','60fps target'],'note':'Five orthographic captures use exact metadata projections rather than the current UI perspective stand-ins.'}
HOOK='''\nwindow.__baselineQA={renderer:bt,scene:Hi,camera:xe,cameras:Pn,look:_d,applyPose:Bc,pose:wa,overhead:qt,highlight:ga,freeze:()=>{bt.setAnimationLoop(null);Yt=null;k.tour=null;fn.enabled=false;la=null;}};\n'''
HIDE='#top,#side,#sideOpen,#info,#viewbar,#tourbar,#disclaimer,#labels,#minimap,#walkhint,#pad,#dock,#welcome,#dissolve,#photo{display:none!important}'

with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
 context=browser.new_context(viewport={'width':1280,'height':720},device_scale_factor=1)
 page=context.new_page()
 page.on('pageerror',lambda e:log['errors'].append(str(e)))
 page.on('console',lambda m:log['errors'].append(m.text) if m.type=='error' else None)
 def passthrough(route):
  url=route.request.url
  try:
   name=url.split('workers.dev/')[-1].split('?')[0] or 'index.html'
   cached=Path('/tmp/office_live_mirror')/name
   if cached.exists():
    body=cached.read_bytes();status=200;headers={'content-type':'text/javascript' if name.endswith('.js') else 'model/gltf-binary' if name.endswith('.glb') else 'text/html'}
   else:
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':UA}),timeout=240) as response:
     body=response.read();status=response.status;headers=dict(response.headers)
   for key in list(headers):
    if key.lower() in ['content-length','content-encoding','transfer-encoding']:del headers[key]
   f=RAW/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(body)
   log['responses'].append({'url':url,'status':status,'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'cached_verified_production_response':cached.exists()})
   if name=='app.js':
    source=body.decode()
    for expected in ['var bt=new','bt.render(Hi,xe)','k.api={selectRoom']:
     assert expected in source,'Production bundle changed; inspect before using QA export'
    body=(source+HOOK).encode()
   route.fulfill(status=status,headers=headers,body=body)
  except Exception as e:
   log['errors'].append('fetch '+url+': '+str(e));route.abort()
 page.route(ORIGIN+'**',passthrough)
 start=time.monotonic()
 page.goto(ORIGIN+'?welcome=0',wait_until='domcontentloaded',timeout=240000)
 page.wait_for_function('window.__viewer && window.__viewer.ready && window.__baselineQA',timeout=600000)
 log['load_seconds']=round(time.monotonic()-start,3)
 log['browser']=browser.version
 log['counts']=page.evaluate('window.__viewer.counts')
 log['gpu']=page.evaluate('''()=>{const g=__baselineQA.renderer.getContext(),e=g.getExtension('WEBGL_debug_renderer_info');return {version:g.getParameter(g.VERSION),vendor:e?g.getParameter(e.UNMASKED_VENDOR_WEBGL):g.getParameter(g.VENDOR),renderer:e?g.getParameter(e.UNMASKED_RENDERER_WEBGL):g.getParameter(g.RENDERER)}}''')
 page.add_style_tag(content=HIDE)
 page.evaluate('window.__baselineQA.freeze()')
 for camera in metadata['cameras']:
  result=page.evaluate('''c=>{
   const q=__baselineQA,r=q.renderer,cam=q.camera;
   r.setPixelRatio(1);r.setSize(1280,720);r.setViewport(0,0,1280,720);r.setScissorTest(false);r.setClearColor(0x101511,1);r.clear();
   q.highlight.visible=false;q.overhead.visible=c.type!=='ORTHO';
   cam.position.fromArray(c.position);cam.quaternion.fromArray(c.quaternion_xyzw);cam.updateMatrixWorld(true);
   q.look(c.type==='ORTHO'?'outside':'inside');
   let drawCam=cam,w=1280,h=720;
   if(c.type==='ORTHO'){
     drawCam=cam.clone();drawCam.isPerspectiveCamera=false;drawCam.isOrthographicCamera=true;drawCam.type='OrthographicCamera';
     const a=c.render.width/c.render.height,s=c.ortho_scale,ow=a>=1?s:s*a,oh=a>=1?s/a:s;
     drawCam.projectionMatrix.makeOrthographic(-ow/2,ow/2,oh/2,-oh/2,c.clip[0],c.clip[1]);
     drawCam.projectionMatrixInverse.copy(drawCam.projectionMatrix).invert();
     if(a>1280/720)h=1280/a;else w=720*a;
     r.setViewport((1280-w)/2,(720-h)/2,w,h);r.setScissor((1280-w)/2,(720-h)/2,w,h);r.setScissorTest(true);
   }else q.applyPose(q.pose(c));
   q.scene.updateMatrixWorld(true);drawCam.updateMatrixWorld(true);r.render(q.scene,drawCam);
   const gl=r.getContext();gl.finish();
   return {camera:c.name,type:c.type,position:drawCam.position.toArray(),quaternion:drawCam.quaternion.toArray(),viewport:[w,h],drawCalls:r.info.render.calls,triangles:r.info.render.triangles,textureCount:r.info.memory.textures,geometryCount:r.info.memory.geometries,exposure:r.toneMappingExposure};
  }''',camera)
  name='before_'+camera['name']+'.png'
  page.screenshot(path=str(SHOTS/name),timeout=300000)
  result['file']='shots/'+name
  log['shots'].append(result)
  (OUT/'capture.json').write_text(json.dumps(log,indent=2))
  print(camera['name'],result['drawCalls'],result['triangles'],flush=True)
 log['seconds']=round(time.monotonic()-start,3)
 (OUT/'capture.json').write_text(json.dumps(log,indent=2))
 browser.close()
 print(json.dumps({'shots':len(log['shots']),'errors':log['errors'],'gpu':log['gpu'],'seconds':log['seconds']}),flush=True)
