"""Bounded garment/body SAT and hand-surface distances for three frozen people."""
import argparse,ast,gzip,hashlib,importlib.util,json,pathlib,numpy as np
P=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('q',P/'props-independent/check_posed_seated_contacts.py');q=importlib.util.module_from_spec(s);s.loader.exec_module(q)
nodes=ast.parse((P/'props-independent/check_reception_static_props.py').read_text()).body;exec(compile(ast.Module(body=[n for n in nodes if isinstance(n,ast.FunctionDef)],type_ignores=[]),'<accepted triangle contact helpers>','exec'))
def nearest_surface(points,T):
 """Exact closest point on target triangles for each sampled skin vertex."""
 a=T[:,0];u=T[:,1]-a;v=T[:,2]-a;n=np.cross(u,v);nn=np.sum(n*n,axis=1);uu=np.sum(u*u,axis=1);uv=np.sum(u*v,axis=1);vv=np.sum(v*v,axis=1);den=uu*vv-uv*uv
 best=(float('inf'),None,None,None)
 for start in range(0,len(points),128):
  pp=points[start:start+128];w=pp[:,None,:]-a[None,:,:];wn=np.sum(w*n[None,:,:],axis=2);f=np.divide(wn,nn,out=np.zeros_like(wn),where=nn>1e-24);project=pp[:,None,:]-f[:,:,None]*n[None,:,:]
  wu=np.sum(w*u[None,:,:],axis=2);wv=np.sum(w*v[None,:,:],axis=2);aa=np.divide(wu*vv-wv*uv,den,out=np.zeros_like(wu),where=abs(den)>1e-24);bb=np.divide(wv*uu-wu*uv,den,out=np.zeros_like(wu),where=abs(den)>1e-24);inside=(aa>=0)&(bb>=0)&(aa+bb<=1)&(nn>1e-24);dist=np.sum((pp[:,None,:]-project)**2,axis=2);dist[~inside]=np.inf;closest=project.copy()
  for k in range(3):
   A=T[:,k];edge=T[:,(k+1)%3]-A;ee=np.sum(edge*edge,axis=1);pa=pp[:,None,:]-A[None,:,:];f=np.clip(np.divide(np.sum(pa*edge[None,:,:],axis=2),ee,out=np.zeros_like(wu),where=ee>1e-24),0,1);candidate=A[None,:,:]+f[:,:,None]*edge[None,:,:];d=np.sum((pp[:,None,:]-candidate)**2,axis=2);better=d<dist;dist[better]=d[better];closest[better]=candidate[better]
  i,j=np.unravel_index(np.argmin(dist),dist.shape)
  if dist[i,j]<best[0]:best=(float(dist[i,j]),pp[i].tolist(),closest[i,j].tolist(),int(j))
 return {'minimum_sampled_skin_vertex_to_surface_m':float(np.sqrt(best[0])),'skin_point':best[1],'surface_point':best[2],'target_triangle_index':best[3],'sampled_vertices':len(points)}
def hand_vertices(d,side):
 V=np.concatenate([np.array(m['vertices'])[np.unique(m['indices'])]for m in d['meshes']if m.get('skinned')and'skin'in m['name'].lower()]);w=np.array(d['bones']['wrist_'+side]);return V[np.linalg.norm(V-w,axis=1)<.20]
p=argparse.ArgumentParser();p.add_argument('--export',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);args=p.parse_args();D={}
for f in sorted((args.export/'t0').glob('*.json.gz')):
 with gzip.open(f,'rt')as stream:d=json.load(stream)
 D[d['id']]=d
buyer=D['office-person-05'];props=[m for m in buyer['meshes']if not m.get('skinned')];body=[m for m in buyer['meshes']if m.get('skinned')];T=np.concatenate([tris(m)for m in props]);prims=q.read_glb(q.SOURCE);source=next(o for o in prims if o['node']=='F020 bay_86b'and o['mat']=='g_sage');touch=D['office-person-07']
report={'status':'bounded static garment contact measurements','held_garment':{'bounds':{'min':T.min((0,1)).tolist(),'max':T.max((0,1)).tolist()},'body_triangle_intersections':pair_contacts(props,body),'hands':{s:nearest_surface(hand_vertices(buyer,s),T)for s in['L','R']}},'rail_touch':{'source_object':source['node'],'source_material':source['mat'],'hands':{s:nearest_surface(hand_vertices(touch,s),source['tri'])for s in['L','R']}},'limits':'Uses accepted full triangle-SAT to detect body/held-garment surface crossings. Distances are sampled actual skin vertices near each wrist to continuous target triangles; they are upper bounds on full surface distance, not a hand-grip, fabric compression or physical load simulation.'}
args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
