from pathlib import Path
from playwright.sync_api import sync_playwright
import json
P=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);page=b.new_page(viewport={'width':1280,'height':720});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:8770/GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/people/review/office-preview.html',timeout=180000);page.wait_for_function('window.ready',timeout=180000)
 result=page.evaluate('''async()=>{
 const layer=window.people,checks=[];const check=(name,ok,detail={})=>checks.push({name,pass:!!ok,detail});window.frozen=true;
 check('25–40 loaded fictional adults',layer.stats().total>=25&&layer.stats().total<=40&&layer.stats().loaded,layer.stats());
 const actor=layer.manifest.actors[0],p=actor.position;
 for(const d of [2,8.5,18]){
  window.camera.position.set(p[0],1.6,p[2]+d);layer.update(1/30,{camera:window.camera,playerPosition:{x:-100,z:-100},quality:'high'});
  const a=layer.diagnostics()[0],materials=a.parts.flatMap(p=>p.materials);check('Complete head/torso/legs/feet at '+d+'m',a.visible&&materials.some(x=>x.includes('Skin'))&&materials.some(x=>x.includes('Garment'))&&materials.some(x=>x.includes('trousers'))&&materials.some(x=>x.includes('Shoes')),{lod:a.low?'LOD1':'LOD0',materials});
 }
 const start=layer.diagnostics().filter(a=>layer.manifest.actors.find(d=>d.id===a.id).path).map(a=>({id:a.id,position:a.position}));
 for(let i=0;i<900;i++)layer.update(1/30,{camera:window.camera,playerPosition:{x:-100,z:-100},quality:'low'});
 const end=layer.diagnostics();
 for(const a of start){const e=end.find(x=>x.id===a.id);check(a.id+' moves on validated corridor route',Math.hypot(e.position[0]-a.position[0],e.position[2]-a.position[2])>.2,{start:a.position,end:e.position})}
 check('No prayer/washroom occupants after motion',layer.stats().forbiddenZoneViolations===0);
 const target=layer.manifest.actors.find(a=>a.path),current=layer.diagnostics().find(a=>a.id===target.id);const path=target.path;let nearest=0,dist=Infinity;for(let i=0;i<path.length;i++){const d=Math.hypot(path[i][0]-current.position[0],path[i][1]-current.position[2]);if(d<dist){dist=d;nearest=i}}
 const ahead=path[Math.min(path.length-1,nearest+8)],visitor={x:ahead[0],z:ahead[1]};let min=Infinity;
 for(let i=0;i<300;i++){layer.update(1/30,{camera:window.camera,playerPosition:visitor,quality:'low'});const a=layer.diagnostics().find(a=>a.id===target.id);min=Math.min(min,Math.hypot(a.position[0]-visitor.x,a.position[2]-visitor.z));}
 check('Walker yields before visitor overlap',min>=.4,{minimumCentreDistance:min,combinedPhysicalRadius:.4});
 const occupied=layer.diagnostics()[0].position;check('People on blocks visitor movement',layer.blocksMovement(occupied[0],occupied[2],.15));await layer.setEnabled(false);check('People off removes dynamic collision',!layer.blocksMovement(occupied[0],occupied[2],.15));await layer.setEnabled(true);
 check('MD has generic phone attached',layer.diagnostics().find(a=>a.id==='office-person-14').phone);
 return{checks,allPassed:checks.every(c=>c.pass),stats:layer.stats(),scope:'Chromium SwiftShader functional prototype checks; not native Mac FPS or photorealism certification'};
 }''')
 result['pageErrors']=errors;result['allPassed']=result['allPassed'] and not errors;(P/'people-functional-checks.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2),flush=True);b.close()
