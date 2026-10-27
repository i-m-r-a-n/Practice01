// Verify preservation and streaming dispatch before touching the production Worker.
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const here=new URL('.',import.meta.url);
function sandbox(source){
  const calls=[];
  const context={Response,Request,Headers,URL,console,addEventListener(){},fetch:async(url,options)=>{
    calls.push({url,method:options.method,range:options.headers.get('Range')});
    return new Response(options.method==='HEAD'?null:(url.endsWith('index.html')?'<script src="./app.js"></script>':'fixture-body'),{status:options.headers.has('Range')?206:200,headers:{'x-origin':'fixture','content-type':'application/octet-stream'}});
  }};
  vm.createContext(context);vm.runInContext(source,context);
  return {calls,run:req=>context.route(req)};
}
const a=sandbox(fs.readFileSync(new URL('production-worker-before.js',here),'utf8'));
const b=sandbox(fs.readFileSync(new URL('worker-realistic.js',here),'utf8'));
const routes=['/','/index.html','/app.js','/model_web.glb','/model.glb','/present','/presentation','/pitch.mp4','/tour.mp4','/presentation.pdf','/render-book.pdf','/renders/CAM_01_Reception_A.jpg','/health','/not-found'];
let count=0;
for(const path of routes)for(const method of ['GET','HEAD']){
  const req=new Request('https://tour.example'+path,{method});
  const [oldResp,newResp]=await Promise.all([a.run(req),b.run(req)]);
  assert.equal(newResp.status,oldResp.status,path);
  assert.deepEqual([...newResp.headers],[...oldResp.headers],path);
  assert.equal(await newResp.text(),await oldResp.text(),path);
  count++;
}
assert.equal((await b.run(new Request('https://tour.example/realistic?room=Z02'))).headers.get('location'),'https://tour.example/realistic/?room=Z02');
for(const [path,type] of [['/realistic/','text/html'],['/realistic/app.js','text/javascript'],['/realistic/model_web.glb','model/gltf-binary'],['/realistic/lightmaps/Z02.ktx2','image/ktx2'],['/realistic/viewer/basis_transcoder.wasm','application/wasm'],['/realistic/renders/CAM_01_Reception_A.jpg','image/jpeg']]){
  const res=await b.run(new Request('https://tour.example'+path));assert.equal(res.status,200);assert.ok(res.headers.get('content-type').startsWith(type));assert.equal(res.headers.get('x-realistic-source').length,40);count++;
}
const partial=await b.run(new Request('https://tour.example/realistic/room.glb',{headers:{Range:'bytes=0-31'}}));assert.equal(partial.status,206);assert.equal(b.calls.at(-1).range,'bytes=0-31');count++;
for(const [name,target] of [['model_web_baked.glb','GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/revised-model/Optimized_Office_Interior_web_baked.glb'],['renders/CAM_34_Merchandising_Sample_Hub.jpg','GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/revised-model/renders/CAM_34_Merchandising_Sample_Hub.jpg'],['renders/CAM_09_Boardroom_A.jpg','GARMENT_OFFICE_FINAL_PRESENTATION/02_RENDERED_IMAGES/final/CAM_09_Boardroom_A.jpg'],['release-config.json','GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/viewer/dist/release-config.json']]) {
  const result=await b.run(new Request('https://tour.example/realistic/'+name));
  assert.equal(result.status,200);assert.ok(b.calls.at(-1).url.endsWith(target));count++;
}
assert.equal((await b.run(new Request('https://tour.example/realistic/app.js',{method:'POST'}))).status,405);count++;
assert.equal((await b.run(new Request('https://tour.example/realistic/%2e%2e%2fsecret.txt'))).status,400);count++;
console.log(JSON.stringify({checks:count,unchanged_original_requests:routes.length*2,passed:true}));
