from playwright.sync_api import sync_playwright
from pathlib import Path
import json
P=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);s=b.new_page(viewport={'width':1280,'height':720});s.goto('http://127.0.0.1:8770/GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/people/review/office-preview.html',timeout=180000);s.wait_for_function('window.ready',timeout=180000)
 for name,pos,target in [('MD-phone-close',[27.1,1.42,3.2],[26.16,1.24,4.95]),('Sofa-close',[10.5,1.15,3.6],[9.7,.85,5.6]),('Sewing-close',[24.8,1.7,-18.7],[23.1,1.0,-19.5])]:
  s.evaluate('''([pos,target])=>{window.frozen=true;camera.clearViewOffset();camera.fov=42;camera.position.fromArray(pos);camera.lookAt(...target);camera.updateProjectionMatrix();people.update(.04,{camera,playerPosition:camera.position,quality:'high'});renderer.render(scene,camera);renderer.getContext().finish()}''',[pos,target]);s.screenshot(path=str(P/(name+'.png')),timeout=180000);print(name,flush=True)
 data=s.evaluate('''()=>{const a=people.diagnostics().find(a=>a.id==='office-person-14');const phone=people.group.getObjectByName('office-person-14_placement').getObjectByName('Generic_phone');return {head:a.bones.head,wrist:a.bones.wrist_R,phonePosition:phone.getWorldPosition(camera.position.clone()).toArray(),assetLock:'people-review-lock.json'}}''');(P/'phone-world-contact.json').write_text(json.dumps(data,indent=2));print(data,flush=True);b.close()
