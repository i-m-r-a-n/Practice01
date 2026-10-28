"""Header toolbar layout probe at many widths (LOCAL Chromium): overlaps, controls outside the viewport, clipped labels.
python3 layout_probe.py [URL] > layout-probe.json"""
import json, sys
from playwright.sync_api import sync_playwright
URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8784/realistic/?room=Z02&welcome=0'
SIZES = [(320, 568), (360, 740), (390, 844), (414, 896), (600, 900), (640, 900), (700, 900), (768, 1024), (820, 1180), (860, 900), (861, 900), (1024, 768), (1180, 820), (1280, 800), (1440, 900), (1920, 1080)]
res = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    pg = b.new_page(viewport={'width': 1280, 'height': 800})
    pg.goto(URL); pg.wait_for_function('window.__viewer?.ready', timeout=180000)
    pg.evaluate("document.getElementById('mPeople').hidden=false")
    for w, h in SIZES:
        pg.set_viewport_size({'width': w, 'height': h}); pg.wait_for_timeout(250)
        res[f'{w}x{h}'] = pg.evaluate("""()=>{const ids=['logos','mTour','mOverview','mRooms','mWalk','mPeople','mHelp','mFull'];const el=id=>id==='logos'?document.querySelector('.logos'):document.getElementById(id);
          const bx=Object.fromEntries(ids.map(i=>{const q=el(i).getBoundingClientRect();return [i,[Math.round(q.left),Math.round(q.top),Math.round(q.right),Math.round(q.bottom)]]}));
          const bad=[];for(let i=0;i<ids.length;i++)for(let j=i+1;j<ids.length;j++){const A=bx[ids[i]],B=bx[ids[j]];if(A[0]<B[2]-1&&B[0]<A[2]-1&&A[1]<B[3]-1&&B[1]<A[3]-1)bad.push(ids[i]+'/'+ids[j]);}
          const out=ids.filter(i=>bx[i][0]<0||bx[i][2]>innerWidth);
          const clip=['mOverview','mRooms','mWalk','mPeople','mTour'].filter(i=>el(i).scrollWidth>el(i).clientWidth+1);
          const small=ids.filter(i=>i!=='logos'&&(bx[i][2]-bx[i][0]<30||bx[i][3]-bx[i][1]<28));
          return {ok:!bad.length&&!out.length&&!clip.length&&!small.length,bad,out,clip,small,top:document.getElementById('top').offsetHeight}}""")
    b.close()
print(json.dumps({'url': URL, 'all_ok': all(v['ok'] for v in res.values()), 'sizes': res}, indent=1))
