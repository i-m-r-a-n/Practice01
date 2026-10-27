"""Actual Cycles diffuse irradiance UV2 bake from a disposable approved-scene copy.
Run Blender5.2+ -b /workspace/office-bake-work/approved-copy.blend -t4 --python bake_rooms.py -- --room Z02 --size2048 --samples256
Source .blend is read-only; geometry/layout is never written back.
"""
import argparse, bpy, bmesh, hashlib, json, math, os, sys, time, subprocess, shutil
from pathlib import Path
from mathutils import Vector
import numpy as np


ap=argparse.ArgumentParser();ap.add_argument('--room',default='Z02');ap.add_argument('--size',type=int,default=2048);ap.add_argument('--samples',type=int,default=256);ap.add_argument('--smoke',action='store_true');ap.add_argument('--shared-shell',action='store_true');ap.add_argument('--floor-uv-weight',type=float,default=1.0);ap.add_argument('--export-only',action='store_true');ap.add_argument('--assignment-only',action='store_true');ap.add_argument('--guide-only',action='store_true');ap.add_argument('--preserve-emitter-groups',action='store_true');ap.add_argument('--out',default=None)
a=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
ROOT=Path(os.environ.get('OFFICE_PROJECT_ROOT',str(Path(__file__).resolve().parents[3])))
OUT=Path(a.out) if a.out else Path(__file__).resolve().parents[1]/'lighting-v2'
OUT.mkdir(parents=True,exist_ok=True)
source=ROOT/'GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/Final_Office_Interior.blend'
meta=json.loads((ROOT/'GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/office_web_metadata.json').read_text())
source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
assert source_hash=='fa3ed3d58f6d44c3554e3761307841b96115ff7816e4e541c8e6611cb363810d'
loaded_copy_hash=hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()
assert loaded_copy_hash==source_hash,'Loaded working copy differs from approved bytes'
rooms={r['zone']:r for r in meta['rooms']}
OVERHEAD={'Beams','Ceilings','Light Fixtures','MEP_Fire_Safety'}
start=time.monotonic()
def log(*s):print(*s,flush=True)
def point_inside(p,poly):
 x,y=p;inside=False;j=len(poly)-1
 for i in range(len(poly)):
  xi,yi=poly[i];xj,yj=poly[j]
  if ((yi>y)!=(yj>y)) and x<(xj-xi)*(y-yi)/(yj-yi)+xi:inside=not inside
  j=i
 return inside

def bbox(o):
 v=[o.matrix_world@Vector(p) for p in o.bound_box]
 return [[min(p[i] for p in v) for i in range(3)],[max(p[i] for p in v) for i in range(3)]]
def assign(o):
 import re
 if a.shared_shell:
  # Keep Reception's reviewed local context in its hero atlas; these whole
  # objects are excluded from shared atlases to avoid duplicate ownership.
  if o.name in {'BM008 Room 3 secondary','BM009 Room 3 secondary','BM010 Room 3 secondary','IW04 Room 1 - room 3'}:return 'Z02'
  if o.name.startswith('Floor slab'):return 'SHELL_FLOOR'
  if o.name.startswith('Steel deck'):return 'SHELL_DECK'
  if any(c.name in {'Columns','Beams'} for c in o.users_collection):return 'SHELL_STRUCTURE'
  if any(c.name=='New Partitions' for c in o.users_collection) and 'frame' in o.name.lower():return 'SHELL_STRUCTURE'
  if any(c.name in {'Existing Walls','Existing Partitions','New Partitions'} for c in o.users_collection):return 'SHELL_WALLS'
 match=re.search(r'\bZ\d{2}\b',o.name)
 if match and match[0] in rooms:return match[0]
 b=bbox(o);x=(b[0][0]+b[1][0])/2;y=-(b[0][1]+b[1][1])/2
 if o.name.startswith(('Floor slab','Steel deck')):return 'SHELL' if a.shared_shell else 'GLOBAL'
 found=[r for r in rooms.values() if point_inside((x,y),r['polygon_xz'])]
 if found:return min(found,key=lambda r:r['area_m2'])['zone']
 return min(rooms.values(),key=lambda r:(x-r['centroid_xz'][0])**2+(y-r['centroid_xz'][1])**2)['zone']
SIGNATURE_DATA={}
NORMAL_DATA={}
def mesh_signature(objects):
 rows=[];normal_rows=[]
 for obj in objects:
  if not obj.data.uv_layers:continue
  co=np.empty(len(obj.data.vertices)*3,np.float64);obj.data.vertices.foreach_get('co',co);co=co.reshape(-1,3)
  world=np.c_[co,np.ones(len(co))]@np.asarray(obj.matrix_world,dtype=np.float64).T
  vi=np.empty(len(obj.data.loops),np.int32);obj.data.loops.foreach_get('vertex_index',vi)
  uv=np.empty(len(obj.data.uv_layers[0].data)*2,np.float64);obj.data.uv_layers[0].data.foreach_get('uv',uv)
  rows.append(np.c_[world[vi,:3],uv.reshape(-1,2)])
  normals=np.empty(len(obj.data.loops)*3,np.float64);obj.data.corner_normals.foreach_get('vector',normals)
  normals=normals.reshape(-1,3)@np.asarray(obj.matrix_world.to_3x3().inverted(),dtype=np.float64)
  normals/=np.maximum(np.linalg.norm(normals,axis=1,keepdims=True),1e-20)
  normal_rows.append(normals)
 SIGNATURE_DATA[len(objects)]=np.concatenate(rows)
 NORMAL_DATA[len(objects)]=np.concatenate(normal_rows)
 data=np.round(SIGNATURE_DATA[len(objects)],4)
 data[data==0]=0
 order=np.lexsort(tuple(data[:,i] for i in reversed(range(5))))
 return hashlib.sha256(np.ascontiguousarray(data[order]).tobytes()).hexdigest()
def visible(o):return o.type=='MESH' and not o.hide_render and not any(c.hide_render for c in o.users_collection)
def bakeable(o):
 mats=[m for m in o.data.materials if m]
 return bool(mats) and not all(any(s in m.name.lower() for s in ('glass','mirror','led_','lightbox')) for m in mats)
all_targets=[o for o in bpy.context.scene.objects if visible(o) and bakeable(o)]
assignment={o.name:assign(o) for o in all_targets}
if a.assignment_only:
 visible_objects=[o for o in bpy.context.scene.objects if visible(o)]
 by_atlas={}
 for obj in all_targets:by_atlas.setdefault(assignment[obj.name],[]).append(obj.name)
 report={'source_sha256':source_hash,'shared_shell_assignment':a.shared_shell,'scope':'Exact source object ownership audit across all34 rooms. No claim that any atlas is baked or visually accepted.',
 'counts':{'visible_meshes':len(visible_objects),'bake_targets':len(all_targets),'excluded_transmissive_mirror_emissive_only':len(visible_objects)-len(all_targets),'room_count':len(rooms)},
 'atlases':by_atlas,'source_objects':{o.name:{'atlas':assignment[o.name],'collections':[c.name for c in o.users_collection],'bbox_xyz':bbox(o)} for o in all_targets},
 'excluded_objects':{o.name:[m.name for m in o.data.materials if m] for o in visible_objects if not bakeable(o)},
 'limitations':['All whole source meshes are assigned once; no wall cutting or geometry change.','Objects excluded from diffuse baking retain their original glass/mirror/emissive PBR materials at runtime.','Actual view visibility and completed atlas status require runtime checks.']}
 assert sum(map(len,by_atlas.values()))==len(set(assignment))
 (OUT/'assignment.json').write_text(json.dumps(report,indent=2));log('ASSIGNMENT_COMPLETE',report['counts']);sys.exit(0)
targets=[o for o in all_targets if assignment[o.name]==a.room]
assert targets,'No room targets'
raw_names=[o.name for o in targets]
source_bboxes={o.name:bbox(o) for o in targets}
log('ROOM_TARGETS',a.room,len(targets),sum(len(o.data.polygons) for o in targets))
# Make local single-user geometry and apply existing source modifiers only.
bpy.ops.object.select_all(action='DESELECT')
for o in targets:
 o.hide_set(False);o.hide_viewport=False;o.data=o.data.copy();o.select_set(True)
bpy.context.view_layer.objects.active=targets[0]
bpy.ops.object.convert(target='MESH')
targets=list(bpy.context.selected_objects)
source_indices={o.name:i for i,o in enumerate(targets)}
source_names=[o.name for o in targets]
def has_emission(mat):
 if not mat or not mat.use_nodes:return False
 for node in mat.node_tree.nodes:
  if node.type=='EMISSION':
   color=node.inputs.get('Color');strength=node.inputs.get('Strength')
  elif node.type=='BSDF_PRINCIPLED':
   color=node.inputs.get('Emission Color');strength=node.inputs.get('Emission Strength')
  else:continue
  if color and strength and (strength.is_linked or strength.default_value>0) and (color.is_linked or max(color.default_value[:3])>0):return True
 return False
emitter_source_ids={i for i,obj in enumerate(targets) if any(has_emission(m) for m in obj.data.materials)}
for o in targets:
 source_attr=o.data.attributes.get('realistic_source_id') or o.data.attributes.new('realistic_source_id','INT','FACE')
 source_attr.data.foreach_set('value',[source_indices[o.name]]*len(source_attr.data))
 overhead=o.name.startswith('Steel deck') or any(c.name in OVERHEAD for c in o.users_collection)
 attr=o.data.attributes.get('realistic_overhead') or o.data.attributes.new('realistic_overhead','INT','FACE')
 attr.data.foreach_set('value',[int(overhead)]*len(attr.data))
 for ca in list(o.data.color_attributes):o.data.color_attributes.remove(ca)
 if not o.data.uv_layers:o.data.uv_layers.new(name='UVMap')
 # Retain source material UV as first layer; SmartProject writes only the lightmap layer.
 while len(o.data.uv_layers)>1:o.data.uv_layers.remove(o.data.uv_layers[-1])
 o.data.uv_layers[0].active_render=True
 o.data.uv_layers.new(name='LightmapUV');o.data.uv_layers.active_index=1
source_evaluated_uv0_signature=mesh_signature(targets)
original_loops=SIGNATURE_DATA[len(targets)].copy()
original_normals=NORMAL_DATA[len(targets)].copy()
bpy.context.view_layer.objects.active=targets[0]
bpy.ops.object.join()
joined=bpy.context.view_layer.objects.active
joined.name='REALISTIC_'+a.room+'_BAKE'
# Pack one shared atlas across the full room. Existing UV0 is untouched.
bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(angle_limit=math.radians(66),island_margin=0.004,area_weight=0.0,correct_aspect=True,scale_to_bounds=True)
bpy.ops.uv.average_islands_scale()
if a.floor_uv_weight!=1.0:
 # A whole source floor object keeps one uniform UV scale. Its islands remain
 # separate and are subsequently repacked, while UV0 and geometry stay untouched.
 bpy.ops.object.mode_set(mode='OBJECT')
 source_ids=joined.data.attributes['realistic_source_id'].data
 uv=joined.data.uv_layers[1].data
 floor_ids={i for i,n in enumerate(source_names) if 'floor finish' in n.lower()}
 for poly in joined.data.polygons:
  if source_ids[poly.index].value in floor_ids:
   for loop in poly.loop_indices:uv[loop].uv*=a.floor_uv_weight
 bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.uv.pack_islands(rotate=True,margin=0.004)
bpy.ops.object.mode_set(mode='OBJECT')
joined.data.uv_layers[0].active_render=True;joined.data.uv_layers.active_index=1
joined_uv0_signature=mesh_signature([joined])
# Joining transformsfloat32vertexstorage; comparecorrespondinggeometry+UVwithin20micrometres
# ratherthanincorrectlyrequiringbyteidenticalroundingacrossdifferentlocalorigins.
from mathutils.kdtree import KDTree
original_tree=KDTree(len(original_loops))
for i,row in enumerate(original_loops):original_tree.insert(row[:3],i)
original_tree.balance();max_world_loop_error=0.0;max_normal_angle=0.0
for loop_i,row in enumerate(SIGNATURE_DATA[1]):
 matches=[(i,d) for _,i,d in original_tree.find_range(row[:3],0.00002) if np.max(np.abs(original_loops[i,3:]-row[3:]))<0.000001]
 assert matches,'GeometryorUV0movedbeyondtolerance'
 max_world_loop_error=max(max_world_loop_error,min(d for _,d in matches))
 dot=max(float(np.dot(original_normals[i],NORMAL_DATA[1][loop_i])) for i,_ in matches)
 max_normal_angle=max(max_normal_angle,math.degrees(math.acos(min(1.,max(-1.,dot)))))
joined.data.calc_loop_triangles()
uv1=joined.data.uv_layers[1].data
uv1_values=np.empty(len(uv1)*2,np.float32);uv1.foreach_get('uv',uv1_values)
uv1_hash=hashlib.sha256(uv1_values.tobytes()).hexdigest()
surface_area=0.0;uv_area=0.0;object_areas={}
source_face_ids=joined.data.attributes['realistic_source_id'].data
for tri in joined.data.loop_triangles:
 coords=[joined.matrix_world@joined.data.vertices[i].co for i in tri.vertices]
 face_world_area=(coords[1]-coords[0]).cross(coords[2]-coords[0]).length*.5
 surface_area+=face_world_area
 u=[uv1[i].uv for i in tri.loops]
 face_uv_area=abs((u[1].x-u[0].x)*(u[2].y-u[0].y)-(u[2].x-u[0].x)*(u[1].y-u[0].y))*.5
 uv_area+=face_uv_area
 objname=source_names[source_face_ids[tri.polygon_index].value]
 objareas=object_areas.setdefault(objname,{'world_area_m2':0.,'uv_area':0.})
 objareas['world_area_m2']+=face_world_area;objareas['uv_area']+=face_uv_area
uv_metrics={'uv1_loop_coordinates_sha256':uv1_hash,'uv0_world_loop_signature':joined_uv0_signature,'uv0_and_evaluated_geometry_preserved':True,'max_world_loop_error_m':max_world_loop_error,'max_world_corner_normal_error_degrees':max_normal_angle,'world_surface_area_m2':surface_area,'summed_uv_island_area':uv_area,'mean_linear_texels_per_metre':math.sqrt(max(uv_area,0)*a.size*a.size/surface_area) if surface_area else 0,'floor_uv_weight':a.floor_uv_weight,'packing_margin_uv':.004,'bake_dilation_px':16}
for objareas in object_areas.values():
 objareas['texels_per_metre']=math.sqrt(objareas['uv_area']*a.size*a.size/objareas['world_area_m2']) if objareas['world_area_m2'] else 0.
uv_metrics['objects']=object_areas
log('UV_PREPARED',len(joined.data.polygons),time.monotonic()-start,{k:v for k,v in uv_metrics.items() if k!='objects'})
image=bpy.data.images.new('LM_'+a.room,width=a.size,height=a.size,alpha=True,float_buffer=True)
image.colorspace_settings.name='Non-Color'
for mat in joined.data.materials:
 if not mat:continue
 target=mat.node_tree.nodes.new('ShaderNodeTexImage');target.name='REALISTIC_LIGHTMAP_TARGET';target.image=image
 for node in mat.node_tree.nodes:node.select=False
 target.select=True;mat.node_tree.nodes.active=target
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=a.samples
scene.cycles.use_denoising=False
# Use all configured samples for bake evidence, with no unmeasured adaptive shortcut.
scene.cycles.use_adaptive_sampling=False
scene.render.bake.target='IMAGE_TEXTURES';scene.render.bake.use_pass_direct=True;scene.render.bake.use_pass_indirect=True;scene.render.bake.use_pass_color=False
scene.render.bake.use_clear=False;scene.render.bake.margin=16;scene.render.bake.margin_type='EXTEND'
# Keep each original mixed-emissive object as a distinct mesh light during
# the diagnostic bake. The source-face ID partition is disjoint: no coincident
# duplicate faces remain in the scene. The full mesh is restored for export.
full_atlas_mesh=joined.data
emitter_bake_objects=[]
if a.preserve_emitter_groups and emitter_source_ids:
 def subset_mesh(keep_ids):
  mesh=full_atlas_mesh.copy();bm=bmesh.new();bm.from_mesh(mesh)
  layer=bm.faces.layers.int.get('realistic_source_id')
  bmesh.ops.delete(bm,geom=[f for f in bm.faces if int(f[layer]) not in keep_ids],context='FACES')
  bm.to_mesh(mesh);bm.free()
  mesh.uv_layers.active_index=1;mesh.uv_layers[0].active_render=True
  return mesh
 joined.data=subset_mesh(set(range(len(source_names)))-emitter_source_ids)
 for source_id in sorted(emitter_source_ids):
  mesh=subset_mesh({source_id});obj=bpy.data.objects.new('BAKE_EMITTER_'+source_names[source_id],mesh)
  bpy.context.collection.objects.link(obj);obj.matrix_world=joined.matrix_world.copy();obj.select_set(True)
  emitter_bake_objects.append(obj)
 assert sum(len(o.data.polygons) for o in [joined]+emitter_bake_objects)==len(full_atlas_mesh.polygons)
 bpy.context.view_layer.objects.active=joined
 log('SEPARATE_EMITTER_GROUPS',[source_names[i] for i in sorted(emitter_source_ids)])
bake_start=time.monotonic()
if a.guide_only:
 scene.cycles.samples=1
 # A cheap source-shader world-normal guide for diagnostic RT filtering.
 bpy.ops.object.bake(type='NORMAL',normal_space='OBJECT',target='IMAGE_TEXTURES',use_clear=False,margin=16,uv_layer='LightmapUV')
 scene.render.image_settings.file_format='OPEN_EXR';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.color_depth='16';scene.render.image_settings.exr_codec='ZIP'
 image.save_render(str(OUT/(a.room+'_normal.exr')),scene=scene)
 # Save loop-space coordinates for an exact guide/export UV alignment check.
 np.savez_compressed(OUT/(a.room+'_normal_uv_reference.npz'),world_and_uv0=SIGNATURE_DATA[1],uv1=uv1_values.reshape(-1,2))
 (OUT/(a.room+'_normal.json')).write_text(json.dumps({'source_sha256':source_hash,'type':'joined-object-space shader-normal guide','normal_to_world':[list(row) for row in joined.matrix_world.to_3x3().inverted().transposed()],'encoded_range':[0,1],'decode':'rgb*2-1','uv_layer':'LightmapUV','uv_metrics':uv_metrics,'seconds':time.monotonic()-bake_start},indent=2))
 log('NORMAL_GUIDE_COMPLETE',time.monotonic()-bake_start)
 # Actual source diffuse-colour guide, separate from the colour-free lightmap.
 scene.render.bake.use_pass_direct=False;scene.render.bake.use_pass_indirect=False;scene.render.bake.use_pass_color=True
 bpy.ops.object.bake(type='DIFFUSE',pass_filter={'COLOR'},target='IMAGE_TEXTURES',use_clear=True,margin=16,uv_layer='LightmapUV')
 image.save_render(str(OUT/(a.room+'_albedo.exr')),scene=scene)
 (OUT/(a.room+'_albedo.json')).write_text(json.dumps({'source_sha256':source_hash,'type':'actual source DIFFUSE COLOR guide, not lighting','target_uv_layer':'LightmapUV','uv1_loop_coordinates_sha256':uv1_hash,'samples':1},indent=2))
 log('ALBEDO_GUIDE_COMPLETE',time.monotonic()-bake_start);sys.exit(0)
if not a.export_only:
 bpy.ops.object.bake(type='DIFFUSE',pass_filter={'DIRECT','INDIRECT'},target='IMAGE_TEXTURES',use_clear=False,margin=16,uv_layer='LightmapUV')
 log('BAKE_FINISHED',a.room,a.size,a.samples,time.monotonic()-bake_start)
 pixels=np.empty(a.size*a.size*4,dtype=np.float32);image.pixels.foreach_get(pixels)
 finite=bool(np.isfinite(pixels).all());rgb=pixels.reshape(-1,4)[:,:3];positive=rgb.max(1)>0
 stats={'min':float(rgb.min()),'max':float(rgb.max()),'p99':float(np.percentile(rgb[positive],99)) if positive.any() else 0,'covered_nonzero_pixels':int(positive.sum()),'finite':finite}
 assert finite and positive.any(),stats
 # Retain the actual pre-denoise bake for visual A/B and future denoiser improvements.
 scene.render.image_settings.file_format='OPEN_EXR';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.color_depth='16';scene.render.image_settings.exr_codec='ZIP'
 image.save_render(str(OUT/(a.room+'_raw.exr')),scene=scene)
 stats['raw_exr']=a.room+'_raw.exr'
 if not a.smoke:
  # OIDN is isolated because Blender already loads a different bundled OIDN build.
  env=os.environ.copy()
  env['PYTHONPATH']=os.environ.get('OFFICE_BAKE_PYTHONPATH','/tmp/office-texture-py')
  cmd=[os.environ.get('OFFICE_BAKE_PYTHON') or shutil.which('python') or shutil.which('python3'),str(Path(__file__).with_name('denoise_lightmap.py')),str(OUT/(a.room+'_raw.exr')),str(OUT/(a.room+'.exr')),'--library',os.environ.get('OFFICE_OIDN_LIBRARY','/workspace/tools/oidn/oidn-2.3.3.x86_64.linux/lib/libOpenImageDenoise.so'),'--threads',str(scene.render.threads)]
  denoise_start=time.monotonic();subprocess.run(cmd,env=env,check=True)
  report=json.loads((OUT/(a.room+'.denoise.json')).read_text())
  stats['denoised_max']=report['outputMax'];stats['denoised_finite']=True
  log('RTLIGHTMAP_FINISHED',time.monotonic()-denoise_start)
 else:
  import shutil
  shutil.copyfile(OUT/(a.room+'_raw.exr'),OUT/(a.room+'.exr'))

else:stats={}
# Restore the identical full atlas mesh before exporting runtime geometry.
if emitter_bake_objects:
 bake_main_mesh=joined.data;joined.data=full_atlas_mesh
 for obj in emitter_bake_objects:
  mesh=obj.data;bpy.data.objects.remove(obj,do_unlink=True);bpy.data.meshes.remove(mesh)
 bpy.data.meshes.remove(bake_main_mesh)
# Export two stable batches with an explicit overhead marker, retaining packed UVs.
base_mesh=joined.data
exports=[]
for overhead,label in ((0,'INTERIOR'),(1,'OVERHEAD')):
 mesh=base_mesh.copy();bm=bmesh.new();bm.from_mesh(mesh);layer=bm.faces.layers.int.get('realistic_overhead')
 remove=[f for f in bm.faces if int(f[layer])!=overhead]
 bmesh.ops.delete(bm,geom=remove,context='FACES');bmesh.ops.remove_doubles(bm,verts=[],dist=0.0)
 bm.to_mesh(mesh);bm.free()
 if not len(mesh.polygons):bpy.data.meshes.remove(mesh);continue
 obj=bpy.data.objects.new('REALISTIC_'+a.room+'_'+label,mesh);bpy.context.collection.objects.link(obj);obj.matrix_world=joined.matrix_world.copy()
 obj['room_id']=a.room;obj['overhead']=bool(overhead);obj['lightmap_channel']=1
 mesh.uv_layers.active_index=0;mesh.uv_layers[0].active_render=True
 exports.append(obj)
joined.hide_render=True;joined.hide_set(True)
bpy.ops.object.select_all(action='DESELECT')
for o in exports:o.select_set(True)
bpy.context.view_layer.objects.active=exports[0]
# Flat material stubs preserve names without duplicatingmaps. Webloader replaces each
# with the colour-corrected baselinePBRmaterial byexactname/sourceMaterial.
source_material_names=[m.name for m in base_mesh.materials if m]
stubs={}
for obj in exports:
 for slot in obj.material_slots:
  mat=slot.material
  if not mat:continue
  original=mat.get('realistic_original_name',mat.name)
  if original not in stubs:
   mat['realistic_original_name']=original;mat.name=original+'__CYCLES_SOURCE'
   stub=bpy.data.materials.new(name=original);stub['sourceMaterial']=original;stub.diffuse_color=(.8,.8,.8,1)
   stubs[original]=stub
  slot.material=stubs[original]
bpy.ops.export_scene.gltf(filepath=str(OUT/(a.room+'.glb')),export_format='GLB',use_selection=True,export_apply=True,export_extras=True,export_cameras=False,export_lights=False,export_yup=True,export_materials='EXPORT',export_texcoords=True,export_normals=True)
room=rooms.get(a.room,{'name':'Shared shell','polygon_xz':[]})
entry={'id':a.room,'name':room['name'],'glb':a.room+'.glb','lightMap':{'url':a.room+'.exr','format':'exr','channel':1,'intensity':math.pi,'linear':True,'samples':a.samples,'size':a.size,'denoised':not a.smoke,'denoiser':'OIDN2.3.3 RTLightmap HDR' if not a.smoke else None},'objects':raw_names,'materials':source_material_names,'bounds':room['polygon_xz'],'bake':{'type':'DIFFUSE','passes':['DIRECT','INDIRECT'],'target_uv_layer':'LightmapUV','source_shader_uv_layer':'UVMap','albedo_included':False,'source_sha256':source_hash,'loaded_copy_sha256':loaded_copy_hash,'executed_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'postprocess_script_sha256':hashlib.sha256(Path(__file__).with_name('denoise_lightmap.py').read_bytes()).hexdigest(),'blender':bpy.app.version_string,'cpu_threads':scene.render.threads,'adaptive_sampling':scene.cycles.use_adaptive_sampling,'preserved_emitter_groups':a.preserve_emitter_groups,'emitter_source_objects':[source_names[i] for i in sorted(emitter_source_ids)],'seconds':time.monotonic()-bake_start,'total_seconds':time.monotonic()-start,'stats':stats,'uv_metrics':uv_metrics,'smoke_only':a.smoke,'original_object_bboxes':source_bboxes},'status':'smoke-only' if a.smoke else 'baked-unreviewed'}
if a.export_only:
 entry['status']='geometry-only-no-lightmap';entry['bake']['export_only']=True
if a.room.startswith('SHELL'):entry['alwaysLoad']=True
(OUT/(a.room+'.json')).write_text(json.dumps(entry,indent=2))
if a.export_only:
 log('GEOMETRY_EXPORT_COMPLETE',a.room,'TOTAL_SECONDS',time.monotonic()-start);sys.exit(0)
manifest_path=OUT/'manifest.json';manifest=json.loads(manifest_path.read_text()) if manifest_path.exists() else {'version':1,'source_sha256':source_hash,'rooms':[],'limitations':['Shared shell and pending room geometry keep baseline materials until their own atlases are ready.','Bakes use source geometry; new props require their own bake or contact AO.']}
manifest['rooms']=[r for r in manifest['rooms'] if r['id']!=a.room]+[entry]
for item in manifest['rooms']:
 ktx=OUT/(item['id']+'.ktx2')
 if ktx.exists() and (OUT/(item['id']+'.ktx2.json')).exists():
  item['lightMap'].update(url=ktx.name,format='ktx2',textureFormat='RGBA16F',compression='zstd',fallbackUrl=item['id']+'.exr')
tmp=manifest_path.with_suffix('.tmp');tmp.write_text(json.dumps(manifest,indent=2));os.replace(tmp,manifest_path)
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
log('ROOM_COMPLETE',a.room,'TOTAL_SECONDS',time.monotonic()-start,'OUTPUT',OUT)
