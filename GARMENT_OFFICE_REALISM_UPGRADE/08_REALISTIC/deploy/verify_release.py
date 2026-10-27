"""Verify published bytes and unchanged original tour after each room deployment."""
import argparse,concurrent.futures,hashlib,json,urllib.request,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('room');p.add_argument('commit');a=p.parse_args()
here=Path(__file__).resolve().parent;real=here.parent;repo=here.parents[2]
site='https://stage2-office-virtual-tour.imranahmedjh611.workers.dev'
health=[];deadline=time.monotonic()+50
while True:
 try:
  request=urllib.request.Request(site+'/realistic/health?release='+a.commit,headers={'User-Agent':'Mozilla/5.0','Cache-Control':'no-cache'})
  with urllib.request.urlopen(request,timeout=8) as response:
   state=json.load(response);health.append({'status':response.status,'source':state.get('source')})
   if response.status==200 and state.get('source')==a.commit:break
 except Exception as e:health.append({'error':str(e)})
 if time.monotonic()>=deadline:break
 time.sleep(2)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
cfg=json.loads((real/'viewer/dist/release-config.json').read_text())
people='people/'+cfg.get('peopleManifest','reception/people-manifest.json')
poses='people/'+json.loads((real/people).read_text()).get('poses','poses.json')
files={'':real/'viewer/dist/index.html','app.js':real/'viewer/dist/app.js','release-config.json':real/'viewer/dist/release-config.json','model_web_baked.glb':real/'revised-model/Optimized_Office_Interior_web_baked.glb','lighting-v2/manifest-hybrid.json':real/'lighting-v2/manifest-hybrid.json',people:real/people,poses:real/poses,'props/office-props-manifest.json':real/'props/office-props-manifest.json',f'review/{a.room.lower()}-before-after.png':real/f'review/{a.room.lower()}-before-after.png'}
items=[(site+'/realistic/'+path,sha(f),a.commit) for path,f in files.items()]
items += [(site+path,h,None) for path,h in {'/':'ff75beb54b3134b3e1eee7d29d0f6016ed1bf5895777c715f3815ebe3dcd2675','/app.js':'c6af8144c56302bf92a975179d847b89c6e4eac63068ecc16a96c7c0c02e9bc4','/health':'5118ed4955892545f48d6edf7fee295fdd0e8963fe1c7704041534fc04de378b'}.items()]
folder=repo/'GARMENT_OFFICE_WALKTHROUGH_FINAL/09_MAC_OFFLINE_TOUR'/('realistic-'+a.room.lower())
z=folder/(a.room+'_Realistic_Offline.zip')
items.append(('https://raw.githubusercontent.com/i-m-r-a-n/Practice01/'+a.commit+'/'+z.relative_to(repo).as_posix(),sha(z),None))
def check(item):
 url,expected,commit=item
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=120) as r:
   h=hashlib.sha256();n=0
   while b:=r.read(1024*1024):h.update(b);n+=len(b)
   return {'url':url,'status':r.status,'bytes':n,'sha256':h.hexdigest(),'expected_sha256':expected,'source':r.headers.get('x-realistic-source'),'passed':r.status==200 and h.hexdigest()==expected and (commit is None or r.headers.get('x-realistic-source')==commit)}
 except Exception as e:return {'url':url,'passed':False,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(check,items))
report={'room':a.room,'commit':a.commit,'passed':all(r['passed'] for r in results),'deployment_health':health,'checks':results,'limits':'HTTPS/source bytes verified; browser WebGL capture blocked by environment CA trust. Native MacBook performance untested.'}
(here/('public-'+a.room.lower()+'-verification.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'room':a.room,'passed':report['passed'],'checks':len(results),'failures':[r for r in results if not r['passed']]}))
raise SystemExit(0 if report['passed'] else 1)
