"""Read-only approved-source audit; outputs only sibling audit JSON, never models."""
import collections, hashlib, json, pathlib, struct, sys
from PIL import Image
ROOT=pathlib.Path(__file__).resolve().parents[3]
OUT=pathlib.Path(__file__).resolve().parent
SOURCE=ROOT/'GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D'
sys.path.insert(0,str(SOURCE/'scripts'))
import office_layout as O
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data): (OUT/name).write_text(json.dumps(data,indent=2)+'\n')
def glb(p):
 b=p.read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]); mats=[]
 for m in g.get('materials',[]):
  q=m.get('pbrMetallicRoughness',{});mats.append({'name':m.get('name'),'basecolor':bool(q.get('baseColorTexture')),'normal':bool(m.get('normalTexture')),'metallic_roughness':bool(q.get('metallicRoughnessTexture')),'occlusion':bool(m.get('occlusionTexture')),'metallic_factor':q.get('metallicFactor',1),'roughness_factor':q.get('roughnessFactor',1),'extensions':list(m.get('extensions',{}))})
 triangles=sum(g['accessors'][r['indices']]['count']//3 if 'indices'in r else g['accessors'][r['attributes']['POSITION']]['count']//3 for m in g.get('meshes',[]) for r in m.get('primitives',[]) if r.get('mode',4)==4)
 return {'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':len(b),'nodes':len(g.get('nodes',[])),'meshes':len(g.get('meshes',[])),'mesh_triangles_before_instances':triangles,'scene_triangles_from_mesh_nodes':sum(sum(g['accessors'][r['indices']]['count']//3 if 'indices' in r else g['accessors'][r['attributes']['POSITION']]['count']//3 for r in g['meshes'][node['mesh']]['primitives'] if r.get('mode',4)==4) for node in g.get('nodes',[]) if 'mesh' in node),'materials':mats,'map_counts':{k:sum(m[k] for m in mats) for k in ('basecolor','normal','metallic_roughness','occlusion')},'images':len(g.get('images',[]))}
tex=[]
for folder in sorted((SOURCE/'assets/textures').iterdir()):
 if not folder.is_dir():continue
 maps=[]
 for p in sorted(folder.rglob('*')):
  if not p.is_file():continue
  try:
   with Image.open(p) as im: dims=list(im.size);mode=im.mode
  except Exception:continue
  maps.append({'file':str(p.relative_to(ROOT)),'size':dims,'mode':mode,'bytes':p.stat().st_size,'sha256':sha(p)})
 tex.append({'set':folder.name,'licence':'CC0 1.0; existing assets/LICENSES.md','maps':maps})
models=[{'asset':p.name,'files':len([f for f in p.rglob('*') if f.is_file()]),'licence':'CC0 1.0; existing assets/LICENSES.md'} for p in sorted((SOURCE/'assets/models').iterdir()) if p.is_dir()]
locked=[SOURCE/'Final_Office_Interior.blend',SOURCE/'Final_Office_Interior.glb',ROOT/'GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/office_web_metadata.json',SOURCE/'scripts/office_layout.py',SOURCE/'scripts/lib_assets.py',SOURCE/'scripts/lib_materials.py']
inv={'coordinate_contract':{'plan':'inches, x east, y south','blender':'[plan_x*.0254, -plan_y*.0254, height*.0254]','viewer':'[plan_x*.0254, height*.0254, plan_y*.0254]','local':'Builder local y is Blender north; local z vertical; facing rotation around Blender Z becomes viewer Y'},'source_locks':{str(p.relative_to(ROOT)):sha(p) for p in locked},'texture_sets':tex,'model_packages':models,'brand_files': [{'file':p.name,'sha256':sha(p),'licence':'Client supplied; project use only'} for p in sorted((SOURCE/'assets/brand').glob('*')) if p.is_file()],'glbs':[glb(SOURCE/'Final_Office_Interior.glb'),glb(ROOT/'GARMENT_OFFICE_REALISM_UPGRADE/01_IMPROVED_MODEL/Final_Office_Interior_web_realism.glb')],'rooms':len(O.ZONES),'scheduled_placements':len(O.PLACEMENTS),'existing_asset_type_counts':dict(collections.Counter(p[0] for p in O.PLACEMENTS))}
write('asset_inventory.json',inv)
rooms=[]
for z in O.ZONES:
 rooms.append({'zone':z[1],'name':z[2].replace('\n',' '),'polygon_plan_inches':z[3],'floor_material':z[4],'placements':[{'key':p[0],'builder':O.ASSETS.get(p[0],[None])[0],'parameters':O.ASSETS.get(p[0],[None,{}])[1],'origin_viewer_m':[p[1]*.0254,p[5]*.0254,p[2]*.0254],'rotation_y_degrees':p[3],'source_plan_inches':list(p[1:4]),'label':p[6]} for p in O.PLACEMENTS if p[4]==z[1]]})
write('approved_room_inventory.json',rooms)
print(json.dumps({'locked_blend':inv['source_locks'][str(locked[0].relative_to(ROOT))],'texture_sets':len(tex),'images':sum(len(s['maps'])for s in tex),'all_sizes':sorted({tuple(m['size']) for s in tex for m in s['maps']}),'glbs':[{k:g[k]for k in('nodes','meshes','mesh_triangles_before_instances','map_counts')}for g in inv['glbs']]},indent=2))
