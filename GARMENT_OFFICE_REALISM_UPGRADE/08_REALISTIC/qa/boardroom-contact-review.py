"""Bounded Boardroom review using accepted source-furniture SAT checker."""
import argparse,gzip,hashlib,importlib.util,json,pathlib,time,ast
import numpy as np
P=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('contacts',P/'props-independent/check_posed_seated_contacts.py');q=importlib.util.module_from_spec(s);s.loader.exec_module(q)
nodes=ast.parse((P/'props-independent/check_reception_static_props.py').read_text()).body
exec(compile(ast.Module(body=[n for n in nodes if isinstance(n,ast.FunctionDef)],type_ignores=[]),'<accepted Reception clipping helpers>','exec'))
a=argparse.ArgumentParser();a.add_argument('--export',type=pathlib.Path,required=True);a.add_argument('--output',type=pathlib.Path,required=True);args=a.parse_args()
start=time.time();empath=args.export/'export-manifest.json';em=json.loads(empath.read_text());snap=next(x for x in em['snapshots']if x['seconds']==0);prims=q.read_glb(q.SOURCE)
report={'status':'diagnostic actual frozen Boardroom contacts','source_glb_sha256':hashlib.sha256(q.SOURCE.read_bytes()).hexdigest(),'export_manifest_sha256':hashlib.sha256(empath.read_bytes()).hexdigest(),'method':'Reuses accepted source furniture triangle-SAT checker against actual browser-deformed visible LOD0 meshes, including standing presenter. Seat underside metric is referenced clothing vertices inside exact top-triangle footprint, above seatTopY-65mm; not a load simulation.','frozen_geometry':em.get('frozen_geometry'),'actors':[]}
for x in snap['actors']:
 p=args.export/x['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']
 with gzip.open(p,'rt')as f:d=json.load(f)
 r=q.analyze_actor(d,prims);r['export_actor_sha256']=x['sha256']
 seat=d['definition'].get('support',{});top=seat.get('seatTopY');name=seat.get('sourceObject')
 if top is not None:
  st=np.concatenate([t['tri']for t in prims if t['node']==name]);tops=st[np.all(np.abs(st[:,:,1]-top)<.0001,axis=1)]
  rows=[]
  for m in d['meshes']:
   if m['name'].startswith('Office_clothing'):
    v=np.array(m['vertices'])[np.unique(m['indices'])];sel=q.points_inside_flat_top(v,tops,top)&(v[:,1]>top-.065)
    if sel.any():rows.append({'mesh':m['name'],'lowest_clothing_y_m':float(v[sel,1].min()),'seat_top_y_m':top,'clearance_m':float(v[sel,1].min()-top)})
  r['seat_support_clothing_clearance']=rows
  trousers=[m for m in d['meshes']if m['name'].startswith('Office_clothing')and m['name'].endswith('_1')];C=np.concatenate([tris(m)for m in trousers]);C=C[np.all(C[:,:,1]>top-.065,axis=1)].copy();C[:,:,1]*=-1;seatlo=tops.min((0,1));seathi=tops.max((0,1));continuous=clipped_max_height(C,seatlo,seathi);continuous['lowest_clothing_y_m']=-continuous.pop('max_y');continuous['clearance_m']=continuous['lowest_clothing_y_m']-top;continuous['point'][1]*=-1;continuous['top_triangle_count']=len(tops);continuous['method']='Continuous trouser triangles clipped to the source seat flat-top rectangle; only triangles entirely above seatTopY-65mm. Two source triangles cover this near-axis-aligned rectangle; yaw roundoff below0.1micrometre.';r['seat_support_continuous_clearance']=continuous
 report['actors'].append(r)
 print(json.dumps({'id':d['id'],'contacts':[{'source':c['source_object'],'material':c['source_material'],'triangles':c['actor_triangles_intersected'],'depth_m':c['max_two_sided_actor_triangle_depth_across_source_plane_m']}for c in r['contacts']],'seat_continuous':r.get('seat_support_continuous_clearance')}),flush=True)
report['wall_seconds']=time.time()-start;args.output.parent.mkdir(exist_ok=True,parents=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
