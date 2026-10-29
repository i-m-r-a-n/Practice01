"""Add an isolated /realistic route to the byte-preserved production Worker.

Usage: python build_worker.py <pushed 40-character source commit> [--bel <pushed commit>] [--out FILE]
The existing root tour, PDFs, videos and health route remain unchanged.
--bel also adds the isolated /bengal-earth-lab/ proposal route, served from that commit's viewer/dist-bel.
"""
from pathlib import Path
import argparse, re

here = Path(__file__).resolve().parent
ap = argparse.ArgumentParser(); ap.add_argument('commit'); ap.add_argument('--bel'); ap.add_argument('--out', default='worker-realistic.js')
args = ap.parse_args(); commit = args.commit
if not re.fullmatch(r'[0-9a-f]{40}', commit) or (args.bel and not re.fullmatch(r'[0-9a-f]{40}', args.bel)):
    raise SystemExit('Complete, pushed commit SHAs are required.')
original = (here/'production-worker-before.js').read_text()
hook = "  const p=new URL(req.url).pathname;"
assert original.count(hook) == 1
original = original.replace(hook, hook+"\n  if(p==='/realistic'||p.startsWith('/realistic/'))return realisticRoute(req);"+("\n  if(p==='/bengal-earth-lab'||p.startsWith('/bengal-earth-lab/'))return belRoute(req);" if args.bel else ''),1)
addition = r'''
// Isolated realism preview. The original route function above is preserved apart from its prefix dispatch.
const REALISTIC_COMMIT = '__COMMIT__';
const REALISTIC_ROOT = 'https://raw.githubusercontent.com/i-m-r-a-n/Practice01/'+REALISTIC_COMMIT+'/';
const REALISTIC_ASSETS = 'GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/';
const REALISTIC_TYPES = {
  html:'text/html; charset=utf-8', js:'text/javascript; charset=utf-8', mjs:'text/javascript; charset=utf-8', css:'text/css; charset=utf-8',
  json:'application/json', glb:'model/gltf-binary', gltf:'model/gltf+json', bin:'application/octet-stream',
  ktx2:'image/ktx2', exr:'image/x-exr', hdr:'image/vnd.radiance',
  wasm:'application/wasm', png:'image/png', jpg:'image/jpeg', jpeg:'image/jpeg', webp:'image/webp',
  svg:'image/svg+xml', zip:'application/zip', txt:'text/plain; charset=utf-8', md:'text/plain; charset=utf-8'
};
async function realisticRoute(req) {
  if(req.method!=='GET'&&req.method!=='HEAD')return new Response('Method not allowed',{status:405,headers:{Allow:'GET, HEAD'}});
  const url=new URL(req.url);
  if(url.pathname==='/realistic') {
    url.pathname='/realistic/';
    return Response.redirect(url.href,307);
  }
  if(url.pathname==='/realistic/health')return Response.json({ok:true,source:REALISTIC_COMMIT,route:'/realistic',fallback:'/',status:'review preview; see acceptance report'});
  let rel;
  try { rel=decodeURIComponent(url.pathname.slice('/realistic/'.length)) || 'index.html'; }
  catch { return new Response('Bad path',{status:400}); }
  if(!/^[A-Za-z0-9_./-]+$/.test(rel)||rel.split('/').some(s=>s==='.'||s==='..'))return new Response('Bad path',{status:400});
  const ext=rel.split('.').pop().toLowerCase();
  const type=REALISTIC_TYPES[ext];
  if(!type)return new Response('Not found',{status:404});
  let path;
  if(rel==='index.html'||rel==='app.js'||rel==='release-config.json')path=REALISTIC_ASSETS+'viewer/dist/'+rel;
  else if(rel==='model_web.glb')path='GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/Final_Office_Interior_web.glb';
  else if(rel==='model_web_baked.glb')path=REALISTIC_ASSETS+'revised-model/Optimized_Office_Interior_web_baked.glb';   // Z06/Z07 option B base model
  else if(/^renders\/CAM_(11|12|16|3[4-8])_[A-Za-z0-9_]+\.jpg$/.test(rel))path=REALISTIC_ASSETS+'revised-model/'+rel;   // redesign renders
  else if(/^renders\/CAM_[A-Za-z0-9_]+\.jpg$/.test(rel))path='GARMENT_OFFICE_FINAL_PRESENTATION/02_RENDERED_IMAGES/final/'+rel.slice(8);
  else path=REALISTIC_ASSETS+rel;
  const forward=new Headers();
  for(const h of ['Range','If-Range','If-None-Match'])if(req.headers.has(h))forward.set(h,req.headers.get(h));
  let remote;
  try {
    remote=await fetch(REALISTIC_ROOT+path,{method:req.method,headers:forward,cf:forward.has('Range')?{cacheEverything:false}:{cacheEverything:true,cacheTtl:3600}});
  } catch {
    return new Response('Preview asset temporarily unavailable. The original tour is available at /.',{status:502});
  }
  if(!remote.ok&&remote.status!==304)return new Response(remote.status===404?'Not found':'Preview asset unavailable',{status:remote.status===404?404:502});
  const h=new Headers(remote.headers);
  h.set('content-type',type);
  h.set('x-content-type-options','nosniff');
  h.set('x-realistic-source',REALISTIC_COMMIT);
  h.set('access-control-allow-origin','*');
  h.set('cache-control',ext==='html'||ext==='json'||ext==='js'?'no-cache':'public, max-age=600');
  h.delete('content-security-policy');
  return new Response(req.method==='HEAD'||remote.status===304?null:remote.body,{status:remote.status,headers:h});
}
'''.replace('__COMMIT__',commit)
bel = r'''
// Isolated Bengal Earth Lab concept proposal (its own page, bundle and config; the routes above are unchanged).
const BEL_COMMIT = '__BEL__';
const BEL_ROOT = 'https://raw.githubusercontent.com/i-m-r-a-n/Practice01/'+BEL_COMMIT+'/';
async function belRoute(req) {
  if(req.method!=='GET'&&req.method!=='HEAD')return new Response('Method not allowed',{status:405,headers:{Allow:'GET, HEAD'}});
  const url=new URL(req.url);
  if(url.pathname==='/bengal-earth-lab') {
    url.pathname='/bengal-earth-lab/';
    return Response.redirect(url.href,307);
  }
  if(url.pathname==='/bengal-earth-lab/health')return Response.json({ok:true,source:BEL_COMMIT,route:'/bengal-earth-lab',fallback:'/',status:'concept proposal preview'});
  let rel;
  try { rel=decodeURIComponent(url.pathname.slice('/bengal-earth-lab/'.length)) || 'index.html'; }
  catch { return new Response('Bad path',{status:400}); }
  if(!/^[A-Za-z0-9_./-]+$/.test(rel)||rel.split('/').some(s=>s==='.'||s==='..'))return new Response('Bad path',{status:400});
  const ext=rel.split('.').pop().toLowerCase();
  const type=REALISTIC_TYPES[ext];
  if(!type)return new Response('Not found',{status:404});
  let path;
  if(rel==='index.html'||rel==='app.js'||rel==='release-config.json')path=REALISTIC_ASSETS+'viewer/dist-bel/'+rel;
  else if(rel==='model_web.glb')path='GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/Final_Office_Interior_web.glb';
  else if(rel==='model_web_baked.glb')path=REALISTIC_ASSETS+'revised-model/Optimized_Office_Interior_web_baked.glb';
  else path=REALISTIC_ASSETS+rel;
  const forward=new Headers();
  for(const h of ['Range','If-Range','If-None-Match'])if(req.headers.has(h))forward.set(h,req.headers.get(h));
  let remote;
  try {
    remote=await fetch(BEL_ROOT+path,{method:req.method,headers:forward,cf:forward.has('Range')?{cacheEverything:false}:{cacheEverything:true,cacheTtl:3600}});
  } catch {
    return new Response('Preview asset temporarily unavailable. The original tour is available at /.',{status:502});
  }
  if(!remote.ok&&remote.status!==304)return new Response(remote.status===404?'Not found':'Preview asset unavailable',{status:remote.status===404?404:502});
  const h=new Headers(remote.headers);
  h.set('content-type',type);
  h.set('x-content-type-options','nosniff');
  h.set('x-bel-source',BEL_COMMIT);
  h.set('access-control-allow-origin','*');
  h.set('cache-control',ext==='html'||ext==='json'||ext==='js'?'no-cache':'public, max-age=600');
  h.delete('content-security-policy');
  return new Response(req.method==='HEAD'||remote.status===304?null:remote.body,{status:remote.status,headers:h});
}
'''.replace('__BEL__',args.bel or '') if args.bel else ''
(here/args.out).write_text(original+addition+bel)
print(here/args.out)
