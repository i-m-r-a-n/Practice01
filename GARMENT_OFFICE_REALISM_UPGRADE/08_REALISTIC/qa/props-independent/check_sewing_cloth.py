import importlib.util,pathlib,json,gzip,hashlib,numpy as np
H=pathlib.Path(__file__).resolve().parent;B=H.parents[1];s=importlib.util.spec_from_file_location('contact',H/'check_posed_seated_contacts.py');q=importlib.util.module_from_spec(s);s.loader.exec_module(q)
C=json.loads((H/'sewing-cloth-actual-mesh.json').read_text());P=np.array(C['vertices']);T=P[np.array(C['indices']).reshape(-1,3)];lo=P.min(0);hi=P.max(0);tlo=T.min(1);thi=T.max(1)
def contacts(objs):
 results=[]
 for ob in objs:
  S=ob['tri'];valid=np.all(S.max(1)>=lo-1e-7,1)&np.all(S.min(1)<=hi+1e-7,1);hits=[]
  for b in S[valid]:
   ix=np.flatnonzero(np.all(thi>=b.min(0)-1e-7,1)&np.all(tlo<=b.max(0)+1e-7,1))
   if not len(ix):continue
   ix=ix[q.tri_intersections(T[ix],b)]
   if len(ix):hits.append(b)
  if hits:results.append({'object':ob['node'],'material':ob.get('mat'),'source_triangles':len(hits),'contact_source_y_min':float(np.min(np.array(hits)[:,:,1])),'contact_source_y_max':float(np.max(np.array(hits)[:,:,1]))})
 return results
source=contacts(q.read_glb(q.SOURCE));actor_path=pathlib.Path('/workspace/office-people-contact-export-v2-preflight/t0/office-person-26.json.gz')
with gzip.open(actor_path,'rt')as f:A=json.load(f)
actor=[]
for m in A['meshes']:
 v=np.array(m['vertices']);actor.append({'node':m['name'],'tri':v[np.array(m['indices']).reshape(-1,3)]})
actor_hits=contacts(actor)
old=json.loads((H/'pre-sewing-cloth-office-props-manifest.json').read_text());new=json.loads((B/'props/office-props-manifest.json').read_text());assert old['props']==new['props'][:-1]
result={'status':'PASS bounded static geometry; integrated image and animated hand/fabric check pending','source_glb_sha256':hashlib.sha256(q.SOURCE.read_bytes()).hexdigest(),'new_manifest_sha256':hashlib.sha256((B/'props/office-props-manifest.json').read_bytes()).hexdigest(),'new_module_sha256':hashlib.sha256((B/'props/office-props.mjs').read_bytes()).hexdigest(),'actual_mesh_sha256':hashlib.sha256((H/'sewing-cloth-actual-mesh.json').read_bytes()).hexdigest(),'actor_v2_t0_sha256':hashlib.sha256(actor_path.read_bytes()).hexdigest(),'existing_323_props_unchanged':True,'bounds':{'min':lo.tolist(),'max':hi.tolist()},'dimensions_m':(hi-lo).tolist(),'triangles':len(T),'source_contacts':source,'source_above_support_crossings':[c for c in source if c['contact_source_y_max']>lo[1]+1e-6],'actor26_v2_t0_contacts':actor_hits,'limits':['One static frozen people v2 snapshot; later poses require the same check.','Touching F206 horizontal bed at the declared support height is intentional. No source geometry moved.','Thin workpiece uses existing self-made fabric material; no physics or actual needle motion claim.']}
assert not result['source_above_support_crossings'];assert not actor_hits
(H/'sewing-cloth-contact-check.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
