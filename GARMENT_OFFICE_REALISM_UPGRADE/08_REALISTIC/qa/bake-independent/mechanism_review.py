import pathlib,json,hashlib,runpy,contextlib,io,numpy as np
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[3];BASE=ROOT/'GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC'
with contextlib.redirect_stdout(io.StringIO()):M=runpy.run_path(str(HERE/'measure_reception.py'))
source=M['read_glb'](ROOT/'GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/Final_Office_Interior.glb')
inv=json.loads((BASE/'blender/source-inventory.json').read_text());entry=json.loads((BASE/'lighting/Z02.json').read_text());names=set(entry['objects']);obj={o['name']:o for o in inv['objects']};mats={m['name']:m for m in inv['materials']}
beam=[]
for name in ['BM008 Room 3 secondary','BM009 Room 3 secondary','BM010 Room 3 secondary']:
 o=obj[name];B=o['bbox'];lo=np.array([B[0][0],B[0][2],-B[1][1]]);hi=np.array([B[1][0],B[1][2],-B[0][1]]);foreign=[]
 for p in source:
  if p['node']==name:continue
  T=p['tri'];bbmin=T.min((0,1));bbmax=T.max((0,1))
  if np.any(bbmin>hi+.00002)or np.any(bbmax<lo-.00002):continue
  for plane in [lo[0],hi[0]]:
   # Long vertical beam sides. Require a coplanar triangle with nonzero YZ area and interior overlap.
   sel=np.max(np.abs(T[:,:,0]-plane),1)<.00002
   for t in T[sel]:
    area=abs(np.cross(t[1]-t[0],t[2]-t[0])[0])*.5
    overlaps=min(t[:,1].max(),hi[1])-max(t[:,1].min(),lo[1])>.001 and min(t[:,2].max(),hi[2])-max(t[:,2].min(),lo[2])>.001
    if area>.00001 and overlaps:foreign.append({'node':p['node'],'material':p['mat'],'area_m2':float(area)})
 contacts=[]
 for q in inv['objects']:
  if q.get('hide_render')or not q.get('bbox')or q['name']==name:continue
  C=q['bbox'];overlap=[min(B[1][k],C[1][k])-max(B[0][k],C[0][k])for k in range(3)]
  if all(v>=-.00001 for v in overlap):contacts.append({'object':q['name'],'bbox_overlap_xyz_m':overlap,'kind':'volume_bbox_overlap'if all(v>.00001 for v in overlap)else'touching_boundaries'})
 beam.append({'name':name,'material':o['materials'],'source_nodes':mats['steel_painted']['nodes'],'foreign_coplanar_long_side_triangles':foreign,'source_bbox_contacts':contacts})
joined_emission=[{'object':n,'materials':obj[n].get('materials',[])}for n in names if any('led_'in s or'lightbox'in s for s in obj[n].get('materials',[]))]
report={'source_sha256':entry['bake']['source_sha256'],'source_material_script_sha256':hashlib.sha256((ROOT/'GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/scripts/lib_materials.py').read_bytes()).hexdigest(),'bake_script_sha256':hashlib.sha256((BASE/'blender/bake_rooms.py').read_bytes()).hexdigest(),'beams':beam,'material_coordinate_mechanisms':{'source_material_UV0':'All ordinary PBR textures use Texture Coordinate UV through mapped UV0; bake sets active_render layer0 and explicit target LightmapUV. Geometry+UV0 preservation is measured by baker.','source_multiple_uv_targets':[n for n in names if len(obj[n].get('uv_layers',[]))>1],'paint_Object_coordinates':'Joining changes object-coordinate origin for paint_white noise, but source strength .05 and distance .001m with Noise scale200/detail6; no Object/Generated node on the plain beam material.','fabric_normal':'Fabric030 tile0.25m, strength0.8, roughness0.9 and sheen0.2. It cannot explain noise on steel_painted.'},'mixed_emissive_bake_objects':joined_emission,'sampling_hypothesis':'Join changes mesh-light grouping when emitter material and diffuse receiver become one mesh. That could alter light-tree/MIS behaviour despite position/normal preservation; this is untested, not a diagnosis. Separate explicit source area/spot lights remain.','runtime_encoding':{'actual':'RGBA16F+lossless Zstd, not RGBM','noColorSpace':True,'lightmapIntensity':entry['lightMap']['intensity'],'interpretation':'Constant pi scale plus no extra diffuse term cannot generate spatial blotches. Codec reports bit-exact decoded float16 pixels; source max28.40625 is representable.','codec_report':json.loads((BASE/'lighting/Z02.ktx2.json').read_text())},'packing':{'atlas_size':entry['lightMap']['size'],'reported_margin_uv':entry['bake']['uv_metrics']['packing_margin_uv'],'nominal_uv_margin_texels':entry['bake']['uv_metrics']['packing_margin_uv']*entry['lightMap']['size'],'bake_dilation_px':entry['bake']['uv_metrics']['bake_dilation_px'],'note':'Configured nominal margin8.192px is smaller than16px dilation; actual pairwise chart distances depend on packing semantics. Chart-isolated denoising is already under test by bake/codec agents. Do not infer overlap from configured margin alone.'},'limitations':['No scene changes or new bake performed','Coplanar long-side test rules out exact foreign overlays on visible long beam faces, not all object intersections','Some original fixture/beam volumes overlap in source; those localized overlaps are inherited and not evidence that joining introduced them','Noise statistics include real spatial illumination gradients and cannot alone prove a sampling bug']}
(HERE/'mechanism-review.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'beam_coplanar_counts':{b['name']:len(b['foreign_coplanar_long_side_triangles'])for b in beam},'mixed_emitters':len(joined_emission),'multiple_uv_targets':report['material_coordinate_mechanisms']['source_multiple_uv_targets'],'codec':'RGBA16F lossless'},indent=2))
