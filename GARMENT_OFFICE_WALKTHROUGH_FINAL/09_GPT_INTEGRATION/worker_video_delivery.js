// Stage II client presentation production Worker — preserve tested baked 3D, add finished films.
// Source lock: GPT patched bundle + Claude's verified baked assets, later Claude film delivery.
const CODE='https://raw.githubusercontent.com/i-m-r-a-n/Practice01/6be2c0f4a8994681c1327c6a5222340cf249ca67/';
const ASSETS='https://raw.githubusercontent.com/i-m-r-a-n/Practice01/ddf99eee703600ee722f06595708439560373567/';
const FILMS='https://raw.githubusercontent.com/i-m-r-a-n/Practice01/cc2bd270c896adba1a127ad2a2216a8a4cdf10a7/';
const HUB='https://raw.githubusercontent.com/i-m-r-a-n/Practice01/809bb9ec05d21aae83e5c525910607cd6956a563/';
addEventListener('fetch',e=>e.respondWith(route(e.request)));
async function route(req){
  const p=new URL(req.url).pathname;
  let base=ASSETS,path,type;
  if(p==='/'||p==='/index.html'){path='GARMENT_OFFICE_WALKTHROUGH_FINAL/08_WORKER_READY_TOUR/index.html';type='text/html; charset=utf-8'}
  else if(p==='/app.js'){path='GARMENT_OFFICE_WALKTHROUGH_FINAL/08_WORKER_READY_TOUR/app.js';type='text/javascript; charset=utf-8';base=CODE}
  else if(p==='/model_web.glb'){path='GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/Final_Office_Interior_web_baked.glb';type='model/gltf-binary'}
  else if(p==='/model.glb'){path='GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/Final_Office_Interior.glb';type='model/gltf-binary'}
  else if(p==='/present'||p==='/presentation'){path='GARMENT_OFFICE_WALKTHROUGH_FINAL/09_GPT_INTEGRATION/client_presentation.html';type='text/html; charset=utf-8';base=HUB}
  else if(p==='/pitch.mp4'){path='GARMENT_OFFICE_WALKTHROUGH_FINAL/01_CLIENT_PITCH_VIDEO/Client_Pitch_Cinematic_Tour_web720.mp4';type='video/mp4';base=FILMS}
  else if(p==='/tour.mp4'){path='GARMENT_OFFICE_WALKTHROUGH_FINAL/02_FULL_FLOOR_TOUR/Complete_Ground_Floor_Tour_web720.mp4';type='video/mp4';base=FILMS}
  else if(p==='/presentation.pdf'){path='GARMENT_OFFICE_FINAL_PRESENTATION/03_PRESENTATION/Garment_Office_Design_Pitch.pdf';type='application/pdf'}
  else if(p==='/render-book.pdf'){path='GARMENT_OFFICE_FINAL_PRESENTATION/03_PRESENTATION/Garment_Office_Render_Book.pdf';type='application/pdf'}
  else if(/^\/renders\/CAM_[A-Za-z0-9_]+\.jpg$/.test(p)){path='GARMENT_OFFICE_FINAL_PRESENTATION/02_RENDERED_IMAGES/final/'+p.slice(9);type='image/jpeg'}
  else if(p==='/health')return Response.json({ok:true,environment:'production',model:'baked',source:'GPT 6a65b7d + Claude ddf99eee',videos:'Claude cc2bd270',films:['/pitch.mp4','/tour.mp4'],pdfs:['/presentation.pdf','/render-book.pdf']});
  else return new Response('Not found',{status:404});
  if(req.method!=='GET'&&req.method!=='HEAD')return new Response('Method not allowed',{status:405});
  const hasRange=!!req.headers.get('Range');
  const forwarded=new Headers();
  if(hasRange)forwarded.set('Range',req.headers.get('Range'));
  if(req.headers.get('If-Range'))forwarded.set('If-Range',req.headers.get('If-Range'));
  const remote=await fetch(base+path,{method:req.method,headers:forwarded,cf:hasRange?{cacheEverything:false}:{cacheEverything:true,cacheTtl:1800}});
  if(!remote.ok)return new Response('Asset unavailable '+remote.status,{status:502});
  const h=new Headers(remote.headers);
  h.set('content-type',type);h.set('x-content-type-options','nosniff');h.delete('content-security-policy');
  h.set('cache-control',type.startsWith('text/html')?'no-store':'public,max-age=600');
  h.set('access-control-allow-origin','*');
  if(type==='video/mp4'||type==='application/pdf')h.set('accept-ranges','bytes');
  if(type==='video/mp4')h.set('content-disposition','inline');
  if(type.startsWith('text/html') && req.method==='GET'){
    h.delete('content-length');
    let html=await remote.text();
    html=html.replace('src="./app.js"','src="./app.js?v=6a65b7d10982"');
    return new Response(html,{status:200,headers:h});
  }
  return new Response(req.method==='HEAD'?null:remote.body,{status:remote.status,headers:h});
}
