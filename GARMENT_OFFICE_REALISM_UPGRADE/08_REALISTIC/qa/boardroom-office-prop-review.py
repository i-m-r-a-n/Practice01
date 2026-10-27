"""Check integrated Z08 office props against final six frozen actor/hand-prop meshes."""
import argparse,ast,gzip,hashlib,importlib.util,json,pathlib,numpy as np
P=pathlib.Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('q',P/'props-independent/check_posed_seated_contacts.py');q=importlib.util.module_from_spec(s);s.loader.exec_module(q)
nodes=ast.parse((P/'props-independent/check_reception_static_props.py').read_text()).body;exec(compile(ast.Module(body=[n for n in nodes if isinstance(n,ast.FunctionDef)],type_ignores=[]),'<accepted contact helpers>','exec'))
p=argparse.ArgumentParser();p.add_argument('--export',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);args=p.parse_args();src=args.export/'office-props.json';office=json.loads(src.read_text());rows=[]
for source in sorted((args.export/'t0').glob('*.json.gz')):
 with gzip.open(source,'rt')as stream:a=json.load(stream)
 row={'id':a['id'],'actor_export_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'triangle_intersections':pair_contacts(office['meshes'],a['meshes'])};rows.append(row);print(json.dumps(row),flush=True)
report={'status':'passed'if not any(r['triangle_intersections']for r in rows)else'blocked','scope':'Actual integrated generated Z08 office-prop triangles (including original instance transforms regardless of view culling) against six actual runtime evaluated body/clothing/handprops. Reuses accepted triangle-SAT narrow phase.','office_props_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'prop_ids':[p['id']for p in office['props']],'excluded_conflicting_glass_21':'PROP_0021'not in[p['id']for p in office['props']],'generated_mesh_count':len(office['meshes']),'actors':rows}
args.output.write_text(json.dumps(report,indent=2)+'\n')
