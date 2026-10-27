from playwright.sync_api import sync_playwright
from pathlib import Path
import json
P=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);s=b.new_page(viewport={'width':1280,'height':720});s.goto('http://127.0.0.1:8770/GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/people/review/office-preview.html',timeout=180000);s.wait_for_function('window.ready',timeout=180000)
 for name,pos,target in [('Reception-static',None,None),('Badge-close',[11.3,1.8,5.6],[12.7,1.15,3.75]),('Book-close',[10.7,1.3,3.8],[10,.8,5.45])]:
  if pos:s.evaluate("([pos,target])=>{window.frozen=true;camera.clearViewOffset();camera.fov=42;camera.position.fromArray(pos);camera.lookAt(...target);camera.updateProjectionMatrix();people.update(.04,{camera,playerPosition:camera.position,quality:'high'});renderer.render(scene,camera);renderer.getContext().finish()}",[pos,target])
  else:s.evaluate("()=>{window.shot('CAM_01_Reception_A');renderer.getContext().finish()}")
  s.screenshot(path=str(P/(name+'.png')),timeout=180000);print(name,flush=True)
 (P/'runtime.json').write_text(json.dumps(s.evaluate('()=>({stats:people.stats(),actors:people.diagnostics()})'),indent=2));b.close()
