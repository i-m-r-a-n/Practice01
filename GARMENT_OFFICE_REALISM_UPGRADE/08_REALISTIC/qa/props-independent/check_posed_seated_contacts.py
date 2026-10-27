"""Independent actual posed mesh/source-furniture contact check; no model mutation.
Usage: python check_posed_seated_contacts.py --export /workspace/... --seconds 0
Source geometry is approved GLB; pose geometry is exported by an independent browser.
"""
import argparse, ast, gzip, hashlib, json, pathlib, struct, time
import numpy as np
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE=ROOT/'GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC'
SOURCE=ROOT/'GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/Final_Office_Interior.glb'
# Load only the read-only GLB parsing function; do not execute that audit's reports.
_parser=ast.parse((BASE/'qa/bake-independent/measure_reception.py').read_text())
_func=next(n for n in _parser.body if isinstance(n,ast.FunctionDef) and n.name=='read_glb')
exec(compile(ast.Module(body=[_func],type_ignores=[]),'<read-only GLB parser>','exec'))

def tri_intersections(A,B):
 """Triangle/triangle SAT including coplanar in-plane axes; returns hit mask."""
 ea=np.roll(A,-1,axis=1)-A; eb=np.roll(B,-1,axis=0)-B
 na=np.cross(ea[:,0],ea[:,1]); nb=np.cross(eb[0],eb[1])
 axes=[na,np.broadcast_to(nb,na.shape)]
 for j in range(3):
  for k in range(3):axes.append(np.cross(ea[:,j],eb[k]))
 # These extra axes also disambiguate coplanar triangle projections.
 for j in range(3):axes.append(np.cross(ea[:,j],na))
 for j in range(3):axes.append(np.broadcast_to(np.cross(eb[j],nb),na.shape))
 keep=np.ones(len(A),bool)
 for ax in axes:
  lens=np.linalg.norm(ax,axis=1);active=lens>1e-12
  p=np.sum(A*ax[:,None,:],axis=2);q=B@ax.T;eps=lens*1e-7
  keep&=(~active)|((p.max(1)>=q.min(0)-eps)&(q.max(0)>=p.min(1)-eps))
 return keep

def points_inside_flat_top(points,triangles,y):
 """Exact flat source top-triangle XZ footprints, avoiding bounding-box seat claims."""
 inside=np.zeros(len(points),bool)
 for t in triangles:
  xy=t[:,[0,2]];a,b,c=xy;u=b-a;v=c-a;den=u[0]*v[1]-u[1]*v[0]
  if abs(den)<1e-12:continue
  p=points[:,[0,2]]-a
  aa=(p[:,0]*v[1]-p[:,1]*v[0])/den;bb=(u[0]*p[:,1]-u[1]*p[:,0])/den
  inside|=(aa>1e-5)&(bb>1e-5)&(aa+bb<1-1e-5)
 return inside

def analyze_actor(data,prims):
 d=data['definition'];support=d.get('support',{});source_name=support.get('sourceObject');seat_top=support.get('seatTopY')
 meshes=[];allpoints=[];alltris=[];tri_names=[];point_names=[]
 for mesh in data['meshes']:
  if mesh.get('visible')is False:continue
  v=np.array(mesh['vertices']);ix=np.array(mesh['indices']).reshape(-1,3)
  used=np.unique(ix);allpoints.append(v[used]);point_names.extend([mesh['name']]*len(used));alltris.append(v[ix]);tri_names.extend([mesh['name']]*len(ix))
  meshes.append(mesh['name'])
 P=np.concatenate(allpoints);T=np.concatenate(alltris);tlo=T.min(1);thi=T.max(1);lo=P.min(0);hi=P.max(0)
 contacts=[]
 for ob in prims:
  if not (ob['node'].startswith('F') and ob['node'][1:4].isdigit()):continue
  S=ob['tri'];slo=S.min((0,1));shi=S.max((0,1))
  if np.any(slo>hi+.000001) or np.any(shi<lo-.000001):continue
  stlo=S.min(1);sthi=S.max(1);valid=np.all(sthi>=lo-1e-7,1)&np.all(stlo<=hi+1e-7,1)
  found=[];hit_actor=set();source_hits=0;crossing_pairs=0;max_two_sided_depth=0
  for b in S[valid]:
   bmin=b.min(0);bmax=b.max(0)
   candidates=np.flatnonzero(np.all(thi>=bmin-1e-7,1)&np.all(tlo<=bmax+1e-7,1))
   if not len(candidates):continue
   hits=candidates[tri_intersections(T[candidates],b)]
   if not len(hits):continue
   source_hits+=1;hit_actor.update(hits.tolist());n=np.cross(b[1]-b[0],b[2]-b[0]);norm=np.linalg.norm(n)
   if norm>1e-10:
    dist=(T[hits]-b[0])@(n/norm);cross=(dist.min(1)<-1e-5)&(dist.max(1)>1e-5)
    crossing_pairs+=int(cross.sum())
    if cross.any():max_two_sided_depth=max(max_two_sided_depth,float(np.minimum(-dist[cross].min(1),dist[cross].max(1)).max()))
   if len(found)<8:found.append({'source_triangle':b.tolist(),'actor_triangle_index':int(hits[0]),'actor_mesh':tri_names[hits[0]],'actor_triangle':T[hits[0]].tolist()})
  if hit_actor:
   ix=list(hit_actor);contacts.append({'source_object':ob['node'],'source_material':ob['mat'],'is_declared_seat_support':ob['node']==source_name,'source_triangles_intersected':source_hits,'actor_triangles_intersected':len(ix),'transverse_triangle_pairs':crossing_pairs,'max_two_sided_actor_triangle_depth_across_source_plane_m':max_two_sided_depth,'intersected_actor_triangle_bounds':{'min':T[ix].min((0,1)).tolist(),'max':T[ix].max((0,1)).tolist()},'examples':found})
 seat={}
 if source_name and seat_top is not None:
  source_T=np.concatenate([p['tri'] for p in prims if p['node']==source_name])
  toptri=source_T[np.all(np.abs(source_T[:,:,1]-seat_top)<.0001,axis=1)]
  # Use an explicit shallow slab below the exact seat-top footprint, not the whole chair box.
  selection=(P[:,1]<seat_top-.015)&(P[:,1]>seat_top-.065);suspect=P[selection];suspect_names=np.array(point_names)[selection]
  inside=points_inside_flat_top(suspect,toptri,seat_top)
  seat={'declared_seat_top_m':seat_top,'exact_source_flat_top_triangles':len(toptri),'vertices_15_to_65mm_below_top_inside_exact_flat_top_footprint':int(inside.sum()),'maximum_depth_in_queried_slab_m':float((seat_top-suspect[inside,1]).max())if inside.any()else 0,'by_mesh':{str(n):int(np.sum(suspect_names[inside]==n))for n in np.unique(suspect_names[inside])},'examples':suspect[inside][:12].tolist(),'limits':'15mm is a review threshold, not an ergonomic or clothing-compression standard. Query samples actual used posed vertices within the top footprint and a 50mm deep slab; it does not test every point of continuous cloth volume.'}
 return {'id':data['id'],'zone':d['zone'],'pose':d['pose'],'support':support,'actual_position':data['actualPosition'],'meshes':meshes,'triangles':len(T),'contacts':contacts,'seat_volume_probe':seat}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--export',type=pathlib.Path,required=True);ap.add_argument('--seconds',default='0');ap.add_argument('--ids',default='');ap.add_argument('--label',default='');args=ap.parse_args();start=time.time()
 manifest_path=args.export/'export-manifest.json';em=json.loads(manifest_path.read_text());t=float(args.seconds);snap=next(s for s in em['snapshots']if s['seconds']==t);prims=read_glb(SOURCE);defs={a['id']:a for a in em['people_manifest']['actors']};wanted=set(args.ids.split(','))if args.ids else None
 report={'status':'diagnostic contact review; no visual acceptance','source_glb_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'export_manifest_sha256':hashlib.sha256(manifest_path.read_bytes()).hexdigest(),'export_sources':em.get('sources'),'seconds':t,'method':'Actual browser-deformed LOD0 triangles versus original source furniture triangles; triangle SAT with coplanar axes. Reports real surface contacts, which require semantic interpretation for intentional cushion/hand contact. No capsule or whole-object AABB substitute. Source furniture limited to F-prefixed objects; other agents own floors/walls/route checks.','actors':[]}
 for a in snap['actors']:
  if not defs[a['id']].get('seated')or(wanted and a['id']not in wanted):continue
  p=args.export/a['file'];content=p.read_bytes()
  if hashlib.sha256(content).hexdigest()!=a['sha256']:raise ValueError('Export hash mismatch: '+str(p))
  with gzip.open(p,'rt')as f:data=json.load(f)
  r=analyze_actor(data,prims);r['export_actor_sha256']=a['sha256'];report['actors'].append(r)
  print(json.dumps({'id':r['id'],'source_contact_primitives':len(r['contacts']),'seat_vertices_15mm_below':r['seat_volume_probe'].get('vertices_15_to_65mm_below_top_inside_exact_flat_top_footprint')}),flush=True)
 report['wall_seconds']=time.time()-start
 out=HERE/((args.label+'-'if args.label else '')+'posed-seated-contacts-t'+str(t).replace('.','_')+'.json');out.write_text(json.dumps(report,indent=2)+'\n');print(str(out),flush=True)
if __name__=='__main__':main()
