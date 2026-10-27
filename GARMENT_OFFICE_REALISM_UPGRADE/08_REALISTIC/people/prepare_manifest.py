from pathlib import Path
import json,base64,math,heapq,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
META=json.loads((ROOT/'GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/office_web_metadata.json').read_text());G=json.loads((ROOT/'GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/walk_grid.json').read_text());INV=json.loads((P.parent/'blender/source-inventory.json').read_text())
O={x['name'].split()[0]:x for x in INV['objects'] if x['name'].startswith('F')};rooms={r['zone']:r for r in META['rooms']};EMPTY=['Z23','Z24','Z25','Z26','Z27','Z28','Z29','Z34'];bits=base64.b64decode(G['blocked_bits_base64']);ox,oz=G['origin_xz'];res=G['res'];cols=G['cols'];rows=G['rows']
def inside(x,z,poly):
 yes=False;j=len(poly)-1
 for i,(xi,zi) in enumerate(poly):
  xj,zj=poly[j]
  if ((zi>z)!=(zj>z)) and x<(xj-xi)*(z-zi)/(zj-zi)+xi:yes=not yes
  j=i
 return yes
def empty(x,z):return any(inside(x,z,rooms[q]['polygon_xz']) for q in EMPTY)
def idx(x,z):return math.floor((x-ox)/res),math.floor((z-oz)/res)
def world(c,r):return [round(ox+(c+.5)*res,5),round(oz+(r+.5)*res,5)]
def clear(c,r):
 if c<1 or r<1 or c>=cols-1 or r>=rows-1:return False
 # Existing grid grows static obstacle by .15 m; one .10m ring makes .25m body planning radius.
 for dc,dr in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]:
  n=(r+dr)*cols+c+dc
  if bits[n>>3]>>(n&7)&1:return False
 return not empty(*world(c,r))
def nearest(x,z,zone,maxdist=1):
 c,r=idx(x,z);good=[]
 for dc in range(-int(maxdist/res),int(maxdist/res)+1):
  for dr in range(-int(maxdist/res),int(maxdist/res)+1):
   xx,zz=world(c+dc,r+dr)
   if clear(c+dc,r+dr) and inside(xx,zz,rooms[zone]['polygon_xz']):good.append(((xx-x)**2+(zz-z)**2,(xx,zz)))
 if not good:raise Exception(('No clear stance',zone,x,z))
 return list(min(good)[1])
def route(start,end,zone):
 s=idx(*nearest(*start,zone));t=idx(*nearest(*end,zone));q=[(0,s)];came={s:None};cost={s:0}
 while q:
  _,v=heapq.heappop(q)
  if v==t:break
  for dc,dr in [(1,0),(-1,0),(0,1),(0,-1)]:
   n=(v[0]+dc,v[1]+dr)
   if not clear(*n) or not inside(*world(*n),rooms[zone]['polygon_xz']):continue
   nc=cost[v]+1
   if nc<cost.get(n,1e9):cost[n]=nc;came[n]=v;heapq.heappush(q,(nc+abs(n[0]-t[0])+abs(n[1]-t[1]),n))
 if t not in came:raise Exception(('No route',s,t,zone))
 path=[];v=t
 while v is not None:path.append(world(*v));v=came[v]
 return path[::-1]
actors=[];colors=['#a8bbcd','#a98a76','#637b76','#ad9271','#8a9bb2','#9e7788','#738866','#b9a895']
def add(zone,task,outfit,chair=None,pos=None,yaw=0,seat=None,path=None):
 i=len(actors);a={'id':f'office-person-{i+1:02}','zone':zone,'task':task,'outfit':outfit,'pose':task,'heightScale':1.+((i*7%11)-5)*.008,'bodyWidth':1.+((i*3%7)-3)*.018,'skinTint':['#d5b6a0','#c69d7b','#b88b69','#ddbaa4'][i%4],'garmentTint':colors[i%len(colors)],'lowerTint':['#25313c','#30363d','#424039'][i%3],'phase':round(i*1.618034,5),'radius':.25,'fictional':True,'faceMorph':[round((i*3%13)/14,3),round((i*5%11)/12,3),round((i*7%17)/18,3)]}
 if chair:
  o=O[chair];a.update({'position':[o['location'][0],0,-o['location'][1]],'yaw':o['rotation'][2],'support':{'sourceObject':o['name'],'seatTopY':.4445 if 'sofa' in o['name'] else .48768002 if 'dining' in o['name'] else .49021998 if 'task' in o['name'] else .50291997,'note':'Pelvis aligned to approved chair; contact pose reviewed separately.'},'seated':True})
 else:
  p=nearest(*pos,zone) if not path else path[0];a.update({'position':[p[0],0,p[1]],'yaw':yaw,'seated':False})
 if path:a['path']=path;a['walkSpeed']=.52;a['pose']='idle';a['task']='walking_files' if i%2 else 'walking'
 
 if a['seated']:
  a['heightScale']=1.0
  a['wardrobeMode']='modest long-sleeve shirt and trousers; long drape disabled for seated role'
  if False:a['outfit']='salwar'
  if task=='greeting':a['pose']='greeting_seated'
  a['pose']+='__seat_'+str(int(round(a['support']['seatTopY']*100000)))
  solved=json.loads((P/'poses.json').read_text())[a['outfit']][a['pose']]
  if 'sofa' not in a['support']['sourceObject']:
   forward=solved.get('seatForwardM',0);a['position'][0]+=math.sin(a['yaw'])*forward;a['position'][2]+=math.cos(a['yaw'])*forward;a['support']['forwardOffsetM']=forward
  if 'sofa' in a['support']['sourceObject']:
   a['position'][0]+=math.sin(a['yaw'])*.18;a['position'][2]+=math.cos(a['yaw'])*.18
 actors.append(a);return a
add('Z02','greeting','salwar','F007')
add('Z02','idle','shirt',pos=[11.60,3.15],yaw=math.pi/2)
a=add('Z02','listening','panjabi','F009',seat=.43);a['position'][0]-=.40
b=add('Z02','listening','salwar_braid','F009',seat=.43);b['position'][0]+=.42
add('Z30','show_sample','salwar',pos=[18.5,-7.35],yaw=math.pi)
add('Z30','browsing','shirt',pos=[17.25,-9.62],yaw=0)
add('Z30','browsing','panjabi',pos=[20.25,-7.55],yaw=-math.pi/2)
for chair,typ,pose in [('F034','shirt','notes'),('F037','salwar','listening'),('F040','panjabi','listening'),('F043','salwar_braid','notes'),('F046','shirt','listening')]:add('Z08',pose,typ,chair)
add('Z08','presenting','salwar',pos=[13.0,-3.70],yaw=math.pi/2)
add('Z12','phone_seated','shirt','F064',seat=.49)
add('Z05','typing','salwar','F140')
add('Z05','phone_seated','shirt','F143')
add('Z06','typing','panjabi','F113')
add('Z06','notes','salwar_braid','F120')
add('Z07','typing','shirt','F074')
add('Z07','phone_seated','salwar','F089')
add('Z07','notes','panjabi','F094')
add('Z07','show_sample','salwar_braid',pos=[15.1,-16.7],yaw=math.pi/2)
add('Z07','browsing','shirt',pos=[15.8,-16.7],yaw=-math.pi/2)
add('Z07','fabric','shirt',pos=[10.75,-11.82],yaw=-.694)
add('Z14','typing','salwar','F182')
add('Z17','sewing','panjabi','F207')
add('Z15','fabric','salwar_braid',pos=[24.38,-7.95],yaw=math.pi)
add('Z18','typing','shirt','F222')
add('Z18','notes','salwar','F225')
add('Z20','tea','panjabi','F263',seat=.45)
add('Z20','tea','salwar_braid','F266',seat=.45)
add('Z20','listening','shirt','F269',seat=.45)
for zone,start,end,typ in [('Z33',[11.0,-22.0],[19.7,-22.0],'salwar'),('Z22',[27.2,-11.7],[27.2,-19.9],'shirt'),('Z31',[3.4,-.8],[3.4,-4.9],'panjabi')]:add(zone,'walking',typ,path=route(start,end,zone))
assert 25<=len(actors)<=40
for a in actors:
 x,_,z=a['position'];assert not empty(x,z),(a['id'],'forbidden')
 if not a['seated']:assert clear(*idx(x,z)),a
 for pt in a.get('path',[]):assert clear(*idx(*pt)),(a['id'],'blocked path')
manifest={'version':'1.0-prototype','count':len(actors),'note':'People shown are illustrative','defaultEnabled':False,'status':'asset/pose review required before integration','approvedLayoutChanged':False,'axes':'metres; x east, y up, z south; characters face +z at yaw 0','emptyZones':EMPTY,'assets':{t:{'file':f'assets/{t}.glb','license':'CC0-1.0 plus self-made drape','sha256':hashlib.sha256((P/'assets'/f'{t}.glb').read_bytes()).hexdigest()} for t in ['shirt','panjabi','salwar','salwar_braid']},'poses':'poses.json','actors':actors,'navigation':{'source':'walk_grid.json','gridRadius':.15,'planningRadius':.25,'additionalOrthogonalCells':1,'mode':'stationary assigned tasks plus reversible validated single-corridor routes; wait for visitor/actor separation'},'limitations':['Procedural gestures, not motion-captured performance.','No native MacBook/Safari performance measurement available.','Anatomical props and seated contacts require actual in-scene render review.']}
(P/'people-manifest.json').write_text(json.dumps(manifest,indent=2));print('actors',len(actors),'walkers',sum('path'in a for a in actors))
