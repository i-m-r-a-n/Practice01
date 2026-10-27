"""Read-only relational contact checks for four frozen Reception actors only."""
import pathlib,json,gzip,importlib.util,hashlib,argparse,numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--export',type=pathlib.Path,default=pathlib.Path('/workspace/office-reception-static-contact-v1'));ap.add_argument('--label',default='v1');args=ap.parse_args();H=pathlib.Path(__file__).resolve().parent;E=args.export;s=importlib.util.spec_from_file_location('q',H/'check_posed_seated_contacts.py');q=importlib.util.module_from_spec(s);s.loader.exec_module(q)
D={}
for p in sorted((E/'t0').glob('*.json.gz')):
 with gzip.open(p,'rt')as f:d=json.load(f)
 D[d['id']]=d

def tris(m):return np.array(m['vertices'])[np.array(m['indices']).reshape(-1,3)]
def pair_contacts(props,body):
 hits=[]
 for p in props:
  A=tris(p);lo=A.min(1);hi=A.max(1)
  for m in body:
   B=tris(m);sel=np.all(B.max(1)>=A.min((0,1))-1e-7,1)&np.all(B.min(1)<=A.max((0,1))+1e-7,1);count=0
   for b in B[sel]:
    ix=np.flatnonzero(np.all(hi>=b.min(0)-1e-7,1)&np.all(lo<=b.max(0)+1e-7,1))
    if len(ix):count+=int(q.tri_intersections(A[ix],b).sum())
   if count:hits.append({'prop_mesh':p['name'],'body_mesh':m['name'],'triangle_pairs':count})
 return hits

def clip_axis(poly,axis,bound,keep_greater):
 out=[]
 for i,v in enumerate(poly):
  u=poly[i-1];inside=(v[axis]>=bound)if keep_greater else(v[axis]<=bound);prev=(u[axis]>=bound)if keep_greater else(u[axis]<=bound)
  if inside!=prev:
   a=(bound-u[axis])/(v[axis]-u[axis]);out.append(u+(v-u)*a)
  if inside:out.append(v)
 return out

def clipped_max_height(T,lo,hi):
 mx=-float('inf');point=None;num=0
 for t in T:
  if np.any(t[:,[0,2]].max(0)<lo[[0,2]])or np.any(t[:,[0,2]].min(0)>hi[[0,2]]):continue
  poly=list(t)
  for axis in [0,2]:
   poly=clip_axis(poly,axis,lo[axis],True)
   if poly:poly=clip_axis(poly,axis,hi[axis],False)
   if not poly:break
  if poly:
   a=np.array(poly);i=np.argmax(a[:,1]);num+=1
   if a[i,1]>mx:mx=float(a[i,1]);point=a[i].tolist()
 return {'max_y':mx,'point':point,'clipped_triangles':num}
book=[m for m in D['office-person-04']['meshes']if not m.get('skinned')];body04=[m for m in D['office-person-04']['meshes']if m.get('skinned')];V=np.concatenate([np.array(m['vertices'])for m in book]);lo=V.min(0);hi=V.max(0)
trousers=[m for m in body04 if m['name'].startswith('Office_clothing')and m['name'].endswith('_1')];T=np.concatenate([tris(m)for m in trousers]);support=clipped_max_height(T,lo,hi);support['book_bottom_y']=float(lo[1]);support['vertical_gap_at_highest_trousers_point_m']=float(lo[1]-support['max_y'])
badge=[m for m in D.get('office-person-01',{}).get('meshes',[])if not m.get('skinned')];hands=[m for id in ['office-person-01','office-person-02']for m in D.get(id,{}).get('meshes',[])if m.get('skinned')];report={'actor_export_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in(E/'t0').glob('*.json.gz')},'book_world_bounds':{'min':lo.tolist(),'max':hi.tolist()},'book_trousers_support':support,'book_body_triangle_contacts':pair_contacts(book,body04),'checked_actor_ids':sorted(D),'badge_body_triangle_contacts':pair_contacts(badge,hands)if badge else None,'limits':'Triangle surface intersections do not alone distinguish intentional finger contact from clipping. Book support compares its lowest plane with the continuous highest trouser triangle clipped to the book XZ footprint; held-book support would need hands instead. Frozen t0 only; baseline proved0.5s geometry invariance.'}
(H/('reception-static4-'+args.label+'-prop-contacts.json')).write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
