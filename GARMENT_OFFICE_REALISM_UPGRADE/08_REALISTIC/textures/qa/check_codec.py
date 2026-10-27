import argparse,json,pathlib,os
from playwright.sync_api import sync_playwright

ROOT=pathlib.Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--pbr2k',action='store_true');parser.add_argument('--port',type=int,default=8786);parser.add_argument('--browser',choices=['chromium','webkit','firefox'],default='chromium');args=parser.parse_args()
test_name='pbr2k' if args.pbr2k else 'codec'
with sync_playwright() as p:
    if args.browser=='webkit':
        b=p.webkit.launch(executable_path='/workspace/tools/playwright/webkit-with-local-libs.sh',headless=True,timeout=30000,env={**os.environ,'LIBGL_ALWAYS_SOFTWARE':'1','WEBKIT_DISABLE_SANDBOX_THIS_IS_DANGEROUS':'1','XDG_CACHE_HOME':'/tmp/office-webkit-cache','XDG_CONFIG_HOME':'/tmp/office-webkit-config'})
    elif args.browser=='firefox':
        b=p.firefox.launch(executable_path='/workspace/tools/playwright/firefox-1538/firefox/firefox',headless=False,timeout=30000,env={**os.environ,'DISPLAY':':88','LD_LIBRARY_PATH':'/workspace/tools/browser-libs/usr/lib/x86_64-linux-gnu','LIBGL_ALWAYS_SOFTWARE':'1','MOZ_DISABLE_CONTENT_SANDBOX':'1','MOZ_DISABLE_RDD_SANDBOX':'1','MOZ_DISABLE_GPU_SANDBOX':'1','XDG_CACHE_HOME':'/tmp/office-firefox-cache','XDG_CONFIG_HOME':'/tmp/office-firefox-config'},firefox_user_prefs={'security.sandbox.content.level':0,'gfx.webrender.software':True,'webgl.force-enabled':True})
    else:
        b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    page=b.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(f'http://127.0.0.1:{args.port}/GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/textures/qa/{test_name}-check.html')
    page.wait_for_function('window.result?.complete',timeout=240000)
    report=page.evaluate('window.result');report['pageErrors']=errors;report['browser']=b.version
    if args.browser=='webkit':report['platformNote']='Playwright WebKit on Debian Linux with LIBGL_ALWAYS_SOFTWARE=1. Renderer string may be privacy-masked as Apple GPU; this is NOT an Apple GPU, macOS or native Safari test.'
    if args.browser=='firefox':report['platformNote']='Playwright Firefox on Debian Linux, local Xvfb headful display and software GL. Not a Mac performance test.'
    suffix=('-'+args.browser+'-linux') if args.browser!='chromium' else ''
    (ROOT/(test_name+'-browser-check'+suffix+'.json')).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    b.close()
    assert report['pass'] and not errors
