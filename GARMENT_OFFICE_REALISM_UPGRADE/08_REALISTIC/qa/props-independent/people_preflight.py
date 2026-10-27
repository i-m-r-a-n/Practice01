"""Independent actual approved-GLB support and standing-envelope review."""
import contextlib,io,json,runpy,pathlib,numpy as np,hashlib,collections,math
HERE=pathlib.Path(__file__).resolve().parent
with contextlib.redirect_stdout(io.StringIO()): S=runpy.run_path(str(HERE/'source_triangle_audit.py'))
BASE=S['BASE'];objs=S['objs'];mfile=BASE/'people/people-manifest.json';m=json.loads(mfile.read_text())
def ray_y(T,x,z):
 a=T[:,0];u=T[:,1]-a;v=T[:,2]-a;den=u[:,0]*v[:,2]-u[:,2]*v[:,0];ok=np.abs(den)>1e-10;aa=np.zeros(len(T));bb=aa.copy();aa[ok]=((x-a[ok,0])*v[ok,2]-(z-a[ok,2])*v[ok,0])/den[ok];bb[ok]=(u[ok,0]*(z-a[ok,2])-u[ok,2]*(x-a[ok,0]))/den[ok];ok&=(aa>=-1e-6)&(bb>=-1e-6)&(aa+bb<=1.000001);return (a[:,1]+aa*u[:,1]+bb*v[:,1])[ok]
seats=[];standing=[]
for p in m['actors']:
 pos=np.array(p['position']);support=p.get('support')
 if p.get('seated') and support:
  found=[]
  for ob in objs:
   if ob['node']!=support['sourceObject']:continue
   ys=ray_y(ob['tri'],pos[0],pos[2]);found.extend(float(y) for y in ys if .30<y<.65)
  actual=max(found)if found else None
  seats.append({'id':p['id'],'sourceObject':support['sourceObject'],'declaredSeatTopY':support['seatTopY'],'measuredSeatAtActorXZ':actual,'declared_minus_actual_m':support['seatTopY']-actual if actual else None})
 else:
  r=p.get('radius',.25);lo=pos+np.array([-r,.025,-r]);hi=pos+np.array([r,1.75,r]);hits=[]
  for ob in objs:
   if np.any(ob['min']>hi)or np.any(ob['max']<lo):continue
   T=ob['tri'];sel=np.all(T.max(1)>=lo,1)&np.all(T.min(1)<=hi,1);T=T[sel]
   if len(T)and S['tri_box'](T,lo,hi).any():hits.append({'node':ob['node'],'asset':ob['asset'],'material':ob['material']})
  standing.append({'id':p['id'],'zone':p['zone'],'task':p['task'],'position':p['position'],'envelope_radius_m':r,'source_surface_candidates':hits})
variants=[(p['outfit'],p.get('heightScale'),p.get('bodyWidth'),p.get('skinTint'),p.get('garmentTint'),p.get('lowerTint'),p['pose'])for p in m['actors']]
r={'manifest_sha256':hashlib.sha256(mfile.read_bytes()).hexdigest(),'actors':len(m['actors']),'seat_supports':seats,'standing_and_walking_start_envelopes':standing,'unique_style_pose_parameter_sets':len(set(variants)),'parameter_clone_count':len(variants)-len(set(variants)),'limits':['Seat ray uses actual source triangles at actor root XZ; it does not test deformed human pelvis/cloth/feet.','Standing full-envelope positives are candidates, not a body-surface intersection proof; arm gestures must be checked using final skinned vertices.','Different style parameters do not prove different faces or believable diversity; actual renders are required.','Walking paths and person/person interaction are not checked by this starting-position review.']}
(HERE/'people-preflight.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'seated':len(seats),'all_seat_deltas':[{k:q[k]for k in('id','measuredSeatAtActorXZ','declared_minus_actual_m')}for q in seats],'standing_candidates':[q for q in standing if q['source_surface_candidates']],'unique_parameter_sets':r['unique_style_pose_parameter_sets']},indent=2))
