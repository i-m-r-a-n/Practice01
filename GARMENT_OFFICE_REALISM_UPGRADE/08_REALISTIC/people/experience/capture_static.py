"""Existing static review renderer; camera frames only, never source geometry edits."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
P=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);s=b.new_page(viewport={'width':1280,'height':720})
 s.goto('http://127.0.0.1:8791/GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/people/experience/office-preview.html',timeout=180000);s.wait_for_function('window.ready',timeout=180000)
 for name,pos,target in [('Experience-static',None,None),('Buyer-sample-close',[17.3,1.65,-8.8],[18.5,1.12,-7.6]),('Rail-touch-close',[18.6,1.6,-8.9],[19.65,1.25,-10.0])]:
  if pos:s.evaluate("([pos,target])=>{window.frozen=true;camera.clearViewOffset();camera.fov=42;camera.position.fromArray(pos);camera.lookAt(...target);camera.updateProjectionMatrix();people.update(0,{camera,playerPosition:camera.position,quality:'high'});renderer.render(scene,camera);renderer.getContext().finish()}",[pos,target])
  else:s.evaluate("()=>{window.shot('CAM_04_Experience_Centre_A');renderer.getContext().finish()}")
  s.screenshot(path=str(P/(name+'.png')),timeout=180000);print(name,flush=True)
 (P/'runtime.json').write_text(json.dumps(s.evaluate('()=>({stats:people.stats(),actors:people.diagnostics()})'),indent=2));b.close()
