"""Bounded Experience Centre review using the accepted furniture SAT checker."""
import argparse,gzip,hashlib,importlib.util,json,pathlib,time
P=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('contacts',P/'props-independent/check_posed_seated_contacts.py');q=importlib.util.module_from_spec(s);s.loader.exec_module(q)
a=argparse.ArgumentParser();a.add_argument('--export',type=pathlib.Path,required=True);a.add_argument('--output',type=pathlib.Path,required=True);args=a.parse_args()
start=time.time();empath=args.export/'export-manifest.json';em=json.loads(empath.read_text());snap=next(x for x in em['snapshots']if x['seconds']==0);prims=q.read_glb(q.SOURCE)
assert len(snap['actors'])==3,'This review is bounded to three new Experience Centre actors'
report={'status':'diagnostic actual frozen Experience Centre contacts','source_glb_sha256':hashlib.sha256(q.SOURCE.read_bytes()).hexdigest(),'export_manifest_sha256':hashlib.sha256(empath.read_bytes()).hexdigest(),'method':'Accepted source furniture triangle-SAT checker against actual browser-deformed visible LOD0 meshes, including held garment props. Intentional fabric touch is reported separately from penetration. No original source furniture moved.','frozen_geometry':em.get('frozen_geometry'),'actors':[]}
for x in snap['actors']:
 p=args.export/x['file'];assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']
 with gzip.open(p,'rt')as f:d=json.load(f)
 r=q.analyze_actor(d,prims);r['export_actor_sha256']=x['sha256'];report['actors'].append(r)
 print(json.dumps({'id':d['id'],'contacts':[{'source':c['source_object'],'material':c['source_material'],'triangles':c['actor_triangles_intersected'],'transverse_pairs':c['transverse_triangle_pairs'],'depth_m':c['max_two_sided_actor_triangle_depth_across_source_plane_m']}for c in r['contacts']]}),flush=True)
report['wall_seconds']=time.time()-start;args.output.parent.mkdir(exist_ok=True,parents=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
