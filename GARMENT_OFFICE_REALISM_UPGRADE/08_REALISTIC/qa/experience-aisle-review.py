"""One rear-aisle before/after witness using actual viewer blocked()."""
import argparse,json,pathlib,time
from playwright.sync_api import sync_playwright
parser=argparse.ArgumentParser();parser.add_argument('--output',type=pathlib.Path,required=True);args=parser.parse_args();P=args.output;P.mkdir(exist_ok=True,parents=True)
R={'status':'running','scope':'Only existing rear rail/table aisle, Z30. Five-centimetre four-neighbour search using actual viewer blocked(), including visitor radius and actor blockers. Front-aisle detours excluded.','url':'http://127.0.0.1:8783/realistic/?welcome=0','errors':[]};started=time.time()
with sync_playwright()as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']);page=b.new_page(viewport={'width':1280,'height':720},device_scale_factor=1);page.on('pageerror',lambda e:R['errors'].append(str(e)))
 try:
  page.goto(R['url'],wait_until='domcontentloaded',timeout=60000);page.wait_for_function("window.__viewer?.ready && typeof __viewer.api?.frameCamera==='function'",timeout=90000);print('viewer ready; checking only rear aisle',flush=True)
  R['comparison']=page.evaluate('''async()=>{
    const api=__viewer.api,origin=[16.1,-10],res=.05,cols=97,rows=19,targets={west:[17,-9.55],east:[20.7,-9.55]},tests=[];
    for(const enabled of[false,true]){
      await api.setPeopleEnabled(enabled);
      const free=new Uint8Array(cols*rows),point=i=>[origin[0]+i%cols*res,origin[1]+Math.floor(i/cols)*res];
      for(let i=0;i<free.length;i++)free[i]=!api.blocked(...point(i));
      const nearest=target=>{let best=-1,d=Infinity;for(let i=0;i<free.length;i++)if(free[i]){const p=point(i),n=Math.hypot(p[0]-target[0],p[1]-target[1]);if(n<d){best=i;d=n}}return{index:best,point:point(best),offset:d}};
      const anchors=Object.fromEntries(Object.entries(targets).map(([n,p])=>[n,nearest(p)]));
      const start=anchors.west.index,queue=[start],previous=new Int32Array(free.length).fill(-2);previous[start]=-1;
      for(let j=0;j<queue.length;j++){const i=queue[j],x=i%cols,z=Math.floor(i/cols);for(const[dx,dz]of[[1,0],[-1,0],[0,1],[0,-1]]){const a=x+dx,c=z+dz;if(a<0||c<0||a>=cols||c>=rows)continue;const n=c*cols+a;if(free[n]&&previous[n]===-2){previous[n]=i;queue.push(n)}}}
      let i=anchors.east.index,path=[];if(previous[i]!==-2){while(i!==-1){path.push(point(i));i=previous[i]}path.reverse()}
      const actor=api.peopleDiagnostics().find(a=>a.id==='office-person-07'),edgeChecks={maximum_spacing_m:.01,samples:0,blocked_samples:[],minimum_actor07_center_distance_m:null};let minimum=Infinity;for(let j=1;j<path.length;j++){const a=path[j-1],b=path[j],n=Math.ceil(Math.hypot(b[0]-a[0],b[1]-a[1])/.01);for(let k=0;k<=n;k++){const p=[a[0]+(b[0]-a[0])*k/n,a[1]+(b[1]-a[1])*k/n];edgeChecks.samples++;if(api.blocked(...p))edgeChecks.blocked_samples.push(p);if(actor)minimum=Math.min(minimum,Math.hypot(p[0]-actor.position[0],p[1]-actor.position[2]));}}if(Number.isFinite(minimum))edgeChecks.minimum_actor07_center_distance_m=minimum;
      tests.push({people_enabled:enabled,stats:api.peopleStats(),actor07:actor,anchors,edge_checks:edgeChecks,rear_aisle_connected:!!path.length,length_m:Math.max(0,path.length-1)*res,path,free_rows:Array.from({length:rows},(_,z)=>Array.from(free.slice(z*cols,(z+1)*cols)).join('')),connected_samples:queue.length});
    }return{origin,res,cols,rows,targets,tests}
  }''');R['viewer_errors']=page.evaluate('__viewer.errors');R['browser']=b.version;T=R['comparison']['tests'];source=json.loads((pathlib.Path(__file__).resolve().parent.parent/'people/room-release/people-manifest.json').read_text());expected=next(a for a in source['actors']if a['id']=='office-person-07');R['actual_actor_position_matches_current_source']=T[1]['actor07']['position']==expected['position'];R['status']='passed'if not R['errors']and not R['viewer_errors']and all(a['offset']<.08 for t in T for a in t['anchors'].values())and all(t['rear_aisle_connected']and not t['edge_checks']['blocked_samples']for t in T)and T[1]['stats']['total']==13 and R['actual_actor_position_matches_current_source'] else'blocked'
 except Exception as e:R['status']='failed';R['exception']=str(e);R['diagnostic']=page.evaluate('()=>({ready:window.__viewer?.ready,errors:window.__viewer?.errors,text:document.body.innerText.slice(-1000)})');raise
 finally:
  R['wall_seconds']=round(time.time()-started,3);(P/'aisle-connectivity.json').write_text(json.dumps(R,indent=2)+'\n');b.close()
print(json.dumps({'status':R['status'],'comparison':[{'people_enabled':t['people_enabled'],'rear_aisle_connected':t['rear_aisle_connected'],'length_m':t['length_m'],'edge_samples':t['edge_checks']['samples'],'blocked_edge_samples':len(t['edge_checks']['blocked_samples'])}for t in R['comparison']['tests']]}))
