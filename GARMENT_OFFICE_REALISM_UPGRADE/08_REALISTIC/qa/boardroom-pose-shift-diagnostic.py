"""Diagnostic only: rigid candidate forward translations on saved evaluated meshes."""
import pathlib,json,gzip,copy,importlib.util,numpy as np,math
P=pathlib.Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('q',P/'props-independent/check_posed_seated_contacts.py');q=importlib.util.module_from_spec(s);s.loader.exec_module(q)
E=pathlib.Path('/workspace/office-boardroom-contact-v1b/t0');prims=q.read_glb(q.SOURCE);out=[]
for i in range(8,13):
 with gzip.open(E/f'office-person-{i:02}.json.gz','rt')as f:d=json.load(f)
 yaw=d['actualYaw'];rows=[]
 for mm in range(0,101,10):
  shift=np.array([math.sin(yaw),0,math.cos(yaw)])*(mm/1000);candidate=copy.deepcopy(d)
  for m in candidate['meshes']:m['vertices']=(np.array(m['vertices'])+shift).tolist()
  candidate['actualPosition']=(np.array(candidate['actualPosition'])+shift).tolist();r=q.analyze_actor(candidate,prims);c=r['contacts'];rows.append({'forward_mm':mm,'position':candidate['actualPosition'],'contacts':[{'object':x['source_object'],'material':x['source_material'],'triangles':x['actor_triangles_intersected']}for x in c]})
  if not c:break
 row={'id':d['id'],'candidates':rows,'first_zero_contact_forward_mm':rows[-1]['forward_mm']if not rows[-1]['contacts']else None};out.append(row);print(json.dumps(row),flush=True)
(P/'boardroom-v1/rigid-forward-diagnostic.json').write_text(json.dumps({'status':'diagnostic rigid transforms only; must re-export final actual runtime before acceptance','actors':out},indent=2)+'\n')
