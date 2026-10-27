"""Diagnostic views using the existing people preview and source geometry."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
P=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
 s=b.new_page(viewport={'width':1280,'height':720})
 s.goto('http://127.0.0.1:8791/GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/people/boardroom/office-preview.html',timeout=180000)
 s.wait_for_function('window.ready',timeout=180000)
 for name,pos,target in [('Boardroom-static',None,None),('Presenter-close',[15.0,1.85,-1.4],[12.9,1.30,-3.15]),('Notes08-close',[16.8,1.35,-2.8],[15.5194,.85,-3.45]),('Notes11-close',[17.6,1.35,-3.1],[18.7706,.85,-2.2])]:
  if pos:
   s.evaluate("([pos,target])=>{window.frozen=true;camera.clearViewOffset();camera.fov=42;camera.position.fromArray(pos);camera.lookAt(...target);camera.updateProjectionMatrix();people.update(0,{camera,playerPosition:camera.position,quality:'high'});renderer.render(scene,camera);renderer.getContext().finish()}",[pos,target])
  else:s.evaluate("()=>{window.shot('CAM_09_Boardroom_A');renderer.getContext().finish()}")
  s.screenshot(path=str(P/(name+'.png')),timeout=180000);print(name,flush=True)
 (P/'runtime.json').write_text(json.dumps(s.evaluate('()=>({stats:people.stats(),actors:people.diagnostics()})'),indent=2))
 b.close()
