"""Read-only Boardroom notebook contacts; reuse Reception triangle/contact helpers."""
import pathlib,json,gzip,importlib.util,hashlib,argparse,ast,numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--export',type=pathlib.Path,required=True);ap.add_argument('--output',type=pathlib.Path,required=True);args=ap.parse_args();P=pathlib.Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('q',P/'props-independent/check_posed_seated_contacts.py');q=importlib.util.module_from_spec(s);s.loader.exec_module(q)
nodes=ast.parse((P/'props-independent/check_reception_static_props.py').read_text()).body
exec(compile(ast.Module(body=[n for n in nodes if isinstance(n,ast.FunctionDef)],type_ignores=[]),'<accepted reception prop helpers>','exec'))
prims=q.read_glb(q.SOURCE);table=np.concatenate([p['tri']for p in prims if p['node']=='F031 board_table']);rows=[]
for p in sorted((args.export/'t0').glob('*.json.gz')):
 with gzip.open(p,'rt')as f:d=json.load(f)
 props=[m for m in d['meshes']if not m.get('skinned')];body=[m for m in d['meshes']if m.get('skinned')]
 if not props:continue
 V=np.concatenate([np.array(m['vertices'])[np.unique(m['indices'])]for m in props]);lo=V.min(0);hi=V.max(0);support=clipped_max_height(table,lo,hi);support['notebook_bottom_y']=float(lo[1]);support['vertical_gap_at_highest_table_point_m']=float(lo[1]-support['max_y'])
 paper=next(m for m in props if m['name']=='Generic_blank_meeting_notes');paper_y=float(np.array(paper['vertices'])[:,1].max());pens=[m for m in props if 'pen'in m['name'].lower()];pen_checks=[{'mesh':m['name'],'bottom_y_m':float(np.array(m['vertices'])[:,1].min()),'gap_above_paper_top_m':float(np.array(m['vertices'])[:,1].min()-paper_y)}for m in pens];pen_book_contacts=pair_contacts(pens,[m for m in props if m not in pens]);
 skin=np.concatenate([tris(m)for m in body if 'skin'in m['name'].lower()]);skin=skin[np.all(skin[:,:,1]>=paper_y-.02,axis=1)].copy();skin[:,:,1]*=-1;near=clipped_max_height(skin,lo,hi);near['minimum_skin_y_m']=-near.pop('max_y');near['gap_above_paper_top_m']=near['minimum_skin_y_m']-paper_y;near['paper_top_y_m']=paper_y;near['point'][1]*=-1;near['method']='Minimum continuous skin surface within notebook footprint; only skin triangles wholly above paperTopY-20mm so thighs below tabletop do not replace hands.'
 r={'id':d['id'],'export_hash':hashlib.sha256(p.read_bytes()).hexdigest(),'prop_meshes':[m['name']for m in props],'world_bounds':{'min':lo.tolist(),'max':hi.tolist()},'notebook_table_support':support,'body_triangle_contacts':pair_contacts(props,body),'skin_above_notebook':near,'pen_paper_clearance':pen_checks,'pen_book_triangle_contacts':pen_book_contacts,'wrist_bones':{k:v for k,v in d['bones'].items()if k.startswith('wrist')}};rows.append(r);print(json.dumps(r),flush=True)
report={'status':'bounded actual notebook/contact review','method':'Accepted Reception exact triangle SAT for book/body; actual source table triangles clipped to notebook XZ footprint for highest supporting surface. Not a physical load or hand grip simulation.','actors':rows}
args.output.parent.mkdir(exist_ok=True,parents=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
