from playwright.sync_api import sync_playwright
from pathlib import Path
import json
p=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']);page=b.new_page(viewport={'width':1280,'height':720});errors=[];page.on('pageerror',lambda e:(errors.append(str(e)),print('JS_ERROR',str(e),flush=True)))
 page.goto('http://127.0.0.1:8770/GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/people/review/office-preview.html',timeout=180000);page.wait_for_function('window.ready===true',timeout=180000)
 for cam in ['CAM_01_Reception_A','CAM_04_Experience_Centre_A','CAM_09_Boardroom_A','CAM_07_MD_Office_A','CAM_11_Merchandising_A','CAM_13_Design_Studio_A','CAM_22_Prayer_Male','CAM_20_Staff_Cafe','CAM_32_Design_Corridor','CAM_15_CAD_Room','CAM_23_Sample_Room']:
  page.evaluate('(n)=>{window.shot(n);window.frozen=true}',cam);page.wait_for_timeout(500);page.screenshot(path=str(p/(cam+'-people.png')),timeout=120000);print(cam,flush=True)
 result=page.evaluate('({stats:window.people.stats(),render:window.renderer.info.render,actors:window.people.diagnostics()})');result['errors']=errors;(p/'office-runtime.json').write_text(json.dumps(result,indent=2));print(result,flush=True)
 b.close()
