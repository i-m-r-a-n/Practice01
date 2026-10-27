from playwright.sync_api import sync_playwright
from pathlib import Path
p=Path(__file__).resolve().parent
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
 page=b.new_page(viewport={'width':1200,'height':700});page.on('pageerror',lambda e:print('ERR',e))
 for pose in ['idle','typing','phone_seated']:
  page.goto('http://127.0.0.1:8770/GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/people/review/preview.html?pose='+pose,timeout=120000);page.wait_for_function('window.ready===true',timeout=120000);page.wait_for_timeout(1000);page.screenshot(path=str(p/(pose+'.png')));print(pose,flush=True)
 b.close()
