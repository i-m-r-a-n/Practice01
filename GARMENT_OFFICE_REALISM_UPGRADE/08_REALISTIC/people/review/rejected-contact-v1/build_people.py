"""CC0 MakeHuman base + official CC0 assets; self-made modest draping.
Run with Blender >=4.3; never opens or edits approved office source.
"""
import bpy,json,math,os,hashlib
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
from mathutils.kdtree import KDTree
ROOT=Path(__file__).resolve().parent; SRC=ROOT/'source'; SYS=SRC/'system-assets'; OUT=ROOT/'assets'; OUT.mkdir(exist_ok=True)

def objread(path):
 v=[];uv=[];faces=[];group='body'
 for s in path.read_text().splitlines():
  a=s.split()
  if not a:continue
  if a[0]=='v':v.append(Vector([float(x) for x in a[1:4]]))
  if a[0]=='vt':uv.append([float(x) for x in a[1:3]])
  if a[0]=='g':group=a[1]
  if a[0]=='f':
   vi=[];ti=[]
   for c in a[1:]:
    d=c.split('/');vi.append(int(d[0])-1);ti.append(int(d[1])-1 if len(d)>1 and d[1] else 0)
   faces.append((vi,ti,group))
 return v,uv,faces
BASE,BUV,BF=objread(SRC/'base.obj'); SK=json.loads((SRC/'default.mhskel').read_text());WEIGHTS=json.loads((SRC/'default_weights.mhw').read_text())['weights']
KEEP=['root','spine05','spine04','spine03','spine02','spine01','neck01','head']
for side in ['L','R']:
 KEEP += [b+'.'+side for b in ['clavicle','upperarm01','lowerarm01','wrist','upperleg01','lowerleg01','foot']]
def ancestor(n):
 while n not in KEEP:
  n=SK['bones'][n]['parent']
  if n is None:return 'root'
 return n
BW=[{} for _ in BASE]
for n,items in WEIGHTS.items():
 bn=ancestor(n)
 for vi,w in items: BW[vi][bn]=BW[vi].get(bn,0)+w

def name(n):return n.replace('.','_')
def transform(p):return Vector((p.x*.1,-p.z*.1,(p.y-FLOOR)*.1))
def joint(n):
 a=SK['joints'][n];return transform(sum((MORPH[i] for i in a),Vector())/len(a))
def mat(n,color=(1,1,1,1),tex=None,normal=None,rough=.7,alpha=False):
 m=bpy.data.materials.new(n);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=rough
 if tex:
  im=bpy.data.images.load(str(tex)); im.scale(2048 if n.startswith('Skin') else 1024,2048 if n.startswith('Skin') else 1024)
  node=m.node_tree.nodes.new('ShaderNodeTexImage');node.image=im;m.node_tree.links.new(node.outputs['Color'],p.inputs['Base Color'])
  if alpha:m.node_tree.links.new(node.outputs['Alpha'],p.inputs['Alpha']);m.surface_render_method='DITHERED'
 if normal:
  im=bpy.data.images.load(str(normal));im.scale(2048 if n.startswith('Skin') else 1024,2048 if n.startswith('Skin') else 1024);im.colorspace_settings.name='Non-Color';node=m.node_tree.nodes.new('ShaderNodeTexImage');node.image=im;nm=m.node_tree.nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.35;m.node_tree.links.new(node.outputs['Color'],nm.inputs['Color']);m.node_tree.links.new(nm.outputs['Normal'],p.inputs['Normal'])
 return m

def mesh(n,verts,uvs,faces,weights,mats,assign=None):
 obj=bpy.data.objects.new(n,bpy.data.meshes.new(n));bpy.context.collection.objects.link(obj);obj.data.from_pydata(verts,[],[f[0] for f in faces]);obj.data.update()
 for m in mats:obj.data.materials.append(m)
 if uvs:
  l=obj.data.uv_layers.new(name='UVMap')
  for poly,(_,tis,g) in zip(obj.data.polygons,faces):
   for li,ti in zip(poly.loop_indices,tis):l.data[li].uv=uvs[ti]
 for poly,f in zip(obj.data.polygons,faces):
  poly.use_smooth=True
  if assign:poly.material_index=assign(poly,f)
 for bn in KEEP:
  vg=obj.vertex_groups.new(name=name(bn))
  for i,w in enumerate(weights):
   if w.get(bn,0)>.0001:vg.add([i],w[bn],'REPLACE')
 arm=obj.modifiers.new('Anatomical rig','ARMATURE');arm.object=RIG;obj.parent=RIG
 return obj

def fitted(rel,n,material,filterface=None):
 p=SYS/rel;v,u,f=objread(p.with_suffix('.obj'));defs=p.with_suffix('.mhclo').read_text().splitlines();data=False;mapping=[];scales=[1.,1.,1.]
 for line in defs:
  a=line.split()
  if not a:continue
  if a[0] in ['x_scale','y_scale','z_scale']:
   ax='xyz'.index(a[0][0]);scales[ax]=abs(MORPH[int(a[1])][ax]-MORPH[int(a[2])][ax])/float(a[3])
  elif a[0]=='verts':data=True
  elif data:
   if not a[0][0].isdigit():
    if mapping:break
    else:continue
   try:
    if len(a)==1:
     i=int(a[0]);mapping.append((MORPH[i],BW[i]))
    elif len(a)>=9:
     ids=[int(x) for x in a[:3]];ws=[float(x) for x in a[3:6]];off=Vector([float(x)*scales[i] for i,x in enumerate(a[6:9])]);pt=sum((MORPH[i]*w for i,w in zip(ids,ws)),Vector())+off
     mapping.append((pt,None))
    else:break
   except ValueError:break
 if len(mapping)!=len(v):raise ValueError((n,len(mapping),len(v)))
 vv=[transform(x[0]) for x in mapping]; ww=[]
 for pt,w in mapping:
  if not w:
   _,idx,_=TREE.find(transform(pt));w=BW[idx]
  ww.append(w or {'root':1})
 if filterface:f=[x for x in f if filterface([vv[i] for i in x[0]])]
 return mesh(n,vv,u,f,ww,[material])

def cloak(n,top,bottom,rx1,rx2,ry1,ry2,material,side_slit=False):
 # Self-made closed modest drape, pleated at hem; body-local horizontal rings.
 verts=[];weights=[];uv=[];faces=[];N=40;R=12
 for j in range(R):
  t=j/(R-1);z=top+(bottom-top)*t;rx=rx1+(rx2-rx1)*t;ry=ry1+(ry2-ry1)*t
  if bottom>.4:rx+=.016*math.sin(t*math.pi);ry+=.013*math.sin(t*math.pi)
  for i in range(N):
   a=2*math.pi*i/N;pleat=.010*(t**1.5)*math.cos(a*14)
   p=Vector(((rx+pleat)*math.sin(a),(ry+pleat)*math.cos(a),z));verts.append(p);uv.append([i/N,t]);_,idx,_=TREE.find(p);weights.append({k:v for k,v in BW[idx].items() if not any(b in k for b in ['arm','wrist','clavicle','head','neck'])} or {'root':1})
 for j in range(R-1):
  for i in range(N):
   ids=[j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i];faces.append((ids,ids,'cloth'))
 o=mesh(n,verts,uv,faces,weights,[material]);return o

def drape(material):
 # Saree pallu from front right waist to left shoulder and behind; entirely self-made.
 verts=[];uv=[];ws=[];faces=[];N=10;R=18
 for j in range(R):
  t=j/(R-1);z=.91+.42*t;cx=.12-.27*t
  for i in range(N):
   a=i/(N-1);x=cx+(a-.5)*.20;zz=z+.008*math.sin(a*math.pi)
   nearby=sorted(((((transform(v).x-x)**2+(transform(v).z-zz)**2),transform(v).y) for v in MORPH[:13380] if transform(v).y<.03),key=lambda q:q[0])[:12]
   y=min(q[1] for q in nearby)-.017
   p=Vector((x,y-.004*math.sin(a*math.pi*6),zz))
   verts.append(p);uv.append((a,t));_,idx,_=TREE.find(p);ws.append({'spine01':min(1,max(0,(z-1.0)/.45)),'spine04':1-min(1,max(0,(z-1.0)/.45))})
 for j in range(R-1):
  for i in range(N-1):
   v=[j*N+i,j*N+i+1,(j+1)*N+i+1,(j+1)*N+i];faces.append((v,v,'drape'))
 return mesh('Saree_pallu',verts,uv,faces,ws,[material])

def armature():
 rig=bpy.data.objects.new('OfficeAdultRig',bpy.data.armatures.new('OfficeAdultSkeleton'));bpy.context.collection.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
 for bn in KEEP:
  b=rig.data.edit_bones.new(name(bn));d=SK['bones'][bn];b.head=joint(d['head']);b.tail=joint(d['tail']);b.roll=0
  for src,dst in [('upperarm01.','lowerarm01.'),('lowerarm01.','wrist.'),('upperleg01.','lowerleg01.'),('lowerleg01.','foot.')]:
   if bn.startswith(src):b.tail=joint(SK['bones'][dst+bn[-1]]['head'])
 for bn in KEEP:
  par=SK['bones'][bn]['parent'];par=ancestor(par) if par else None
  if par:rig.data.edit_bones[name(bn)].parent=rig.data.edit_bones[name(par)]
 bpy.ops.object.mode_set(mode='OBJECT');rig.select_set(False);return rig

def aim(bn,vec):
 pb=RIG.pose.bones[name(bn)];bpy.context.view_layer.update();cur=(pb.tail-pb.head).normalized();q=cur.rotation_difference(Vector(vec).normalized());m=(q@pb.matrix.to_quaternion()).to_matrix().to_4x4();m.translation=pb.head;pb.matrix=m;bpy.context.view_layer.update()
def pose(kind):
 kind,_,seatkey=kind.partition('__seat_');seatTop=float(seatkey)/100000 if seatkey else .49
 for p in RIG.pose.bones:p.rotation_mode='QUATERNION';p.rotation_quaternion=(1,0,0,0);p.location=(0,0,0)
 bpy.context.view_layer.update()
 # standing arms hang beside torso; all coordinates Blender Z-up, face -Y.
 seated=kind in ['typing','listening','notes','phone_seated','tea','sewing','greeting_seated']
 hipRest=joint(SK['bones']['upperleg01.L']['head']).z
 shinLen=(joint(SK['bones']['lowerleg01.L']['tail'])-joint(SK['bones']['lowerleg01.L']['head'])).length
 # lowerleg01 ends halfway down shin; parent omitted lowerleg02 must count through ankle.
 shinLen=(joint(SK['bones']['foot.L']['head'])-joint(SK['bones']['lowerleg01.L']['head'])).length
 kneeGoal=joint(SK['bones']['foot.L']['head']).z+shinLen+.01016
 hipGoal=seatTop+.09
 thighLen=(joint(SK['bones']['lowerleg01.L']['head'])-joint(SK['bones']['upperleg01.L']['head'])).length
 dz=kneeGoal-hipGoal
 forward=math.sqrt(max(.02,thighLen*thighLen-dz*dz))
 for side,sgn in [('L',1),('R',-1)]:
  if seated:
   aim('upperleg01.'+side,(sgn*.015,-forward,dz));aim('lowerleg01.'+side,(0,.02,-.43));aim('foot.'+side,(0,-.22,-.025))
  aim('upperarm01.'+side,(sgn*.055,-.015,-.29));aim('lowerarm01.'+side,(sgn*.01,-.025,-.25));aim('wrist.'+side,(0,-.015,-.12))
 if kind.startswith('walk_'):
  phase=int(kind.split('_')[1])*math.tau/12
  for side,sgn in [('L',1),('R',-1)]:
   wave=math.sin(phase+(0 if side=='L' else math.pi));swing=wave*.34
   aim('upperleg01.'+side,(sgn*.035,-math.sin(swing),-math.cos(swing)))
   knee=max(0,-wave)*.48
   aim('lowerleg01.'+side,(0,math.sin(knee+swing),-math.cos(knee+swing)))
   aim('foot.'+side,(0,-.22,-.02))
   aim('upperarm01.'+side,(sgn*.055,math.sin(swing)*.5,-.3))
   aim('lowerarm01.'+side,(sgn*.01,math.sin(swing)*.25-.04,-.25))
 elif kind in ['typing','notes','sewing']:
  for side,sgn in [('L',1),('R',-1)]:
   S=joint(SK['bones']['upperarm01.'+side]['head']);E0=joint(SK['bones']['lowerarm01.'+side]['head']);W0=joint(SK['bones']['wrist.'+side]['head']);tx=(.17 if side=='L' else -.01) if kind=='sewing' else sgn*.16;wy=.842 if kind=='sewing' else .782;W=Vector((tx,-.445 if kind=='sewing' else -.38,wy-(hipGoal-hipRest)))
   A=(E0-S).length;B=(W0-E0).length;D=(W-S).length;direction=(W-S).normalized()
   if D>A+B-.002:W=S+direction*(A+B-.002);D=(W-S).length
   along=(A*A-B*B+D*D)/(2*D);height=math.sqrt(max(0,A*A-along*along));bend=Vector((sgn*.16,.05,-.2));bend=(bend-direction*bend.dot(direction)).normalized();E=S+direction*along+bend*height
   aim('upperarm01.'+side,E-S);aim('lowerarm01.'+side,W-E);aim('wrist.'+side,(0,-.13,-.012))
 elif kind in ['phone_seated','phone']:
  S=joint(SK['bones']['upperarm01.R']['head']);E0=joint(SK['bones']['lowerarm01.R']['head']);W0=joint(SK['bones']['wrist.R']['head']);W=joint(SK['bones']['head']['head'])+Vector((-.105,0.0,-.065))
  A=(E0-S).length;B=(W0-E0).length;D=(W-S).length;direction=(W-S).normalized();along=(A*A-B*B+D*D)/(2*D);height=math.sqrt(max(0,A*A-along*along));bend=Vector((-.06,-.25,-.20));bend=(bend-direction*bend.dot(direction)).normalized();E=S+direction*along+bend*height
  aim('upperarm01.R',E-S);aim('lowerarm01.R',W-E);aim('wrist.R',(0,-.01,.12))
 elif kind in ['greeting','greeting_seated','presenting','show_sample']:
  aim('upperarm01.R',(-.17,-.13,-.13));aim('lowerarm01.R',(-.11,-.24,.12));aim('wrist.R',(-.06,-.10,.04))
  if kind=='show_sample':aim('upperarm01.L',(.1,-.12,-.24));aim('lowerarm01.L',(-.08,-.22,.04))
 elif kind in ['carry_files','browsing','fabric','tea']:
  for side,sgn in [('L',1),('R',-1)]:aim('upperarm01.'+side,(sgn*.09,-.09,-.23));aim('lowerarm01.'+side,(-sgn*.10,-.18,.10));aim('wrist.'+side,(-sgn*.04,-.11,.02))
 elif kind=='listening':
  for side,sgn in [('L',1),('R',-1)]:aim('lowerarm01.'+side,(-sgn*.05,-.18,-.12))
 bpy.context.view_layer.update()
 return {'bones':{p.name:list(p.rotation_quaternion) for p in RIG.pose.bones},'rootY':hipGoal-hipRest if seated else 0,'seatTopY':seatTop if seated else None,'seated':seated}

VARIANTS=[('shirt','male','short02'),('panjabi','male','short04'),('salwar','female','ponytail01'),('salwar_braid','female','braid01')]
allstats={};pose_library={}
for typ,sex,hair in VARIANTS:
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 MORPH=[v.copy() for v in BASE]
 for l in (SRC/f'asian-{sex}-young.target').read_text().splitlines():
  a=l.split()
  if a and not a[0].startswith('#'):MORPH[int(a[0])]+=Vector([float(x) for x in a[1:4]])
 # Small shape variation by outfit is fictional; no real portrait source.
 if typ=='panjabi':
  for v in MORPH:v.x*=1.065
 lo=min(v.y for v in MORPH[:13380]);hi=max(v.y for v in MORPH[:13380]);factor=(17.0 if sex=='male' else 16.2)/(hi-lo)
 MORPH=[Vector((v.x*factor,(v.y-lo)*factor,v.z*factor)) for v in MORPH]
 FLOOR=0;TREE=KDTree(13380)
 for i,v in enumerate(MORPH[:13380]):TREE.insert(transform(v),i)
 TREE.balance();RIG=armature()
 skinfile=next((SYS/f'skins/young_asian_{sex}').glob('*diffuse*.png'))
 skin=mat('Skin_CC0_MakeHuman',(1,1,1,1),skinfile,rough=.64)
 hairdir=SYS/'hair'/hair;hairmat=mat('Hair_CC0',(1,1,1,1),hairdir/f'{hair}_diffuse.png',rough=.75,alpha=True)
 outfitdir=SYS/'clothes/male_casualsuit01'
 shirtmat=mat('Garment_top',(1,1,1,1),outfitdir/'male_casualsuit01_diffuse.png',outfitdir/'male_casualsuit01_normal.png',rough=.83)
 legmat=mat('Garment_trousers',(.12,.14,.17,1),normal=outfitdir/'male_casualsuit01_normal.png',rough=.86)
 tunicmat=mat('Garment_drape',(.09,.25,.29,1) if sex=='female' else (.62,.56,.43,1),normal=outfitdir/'male_casualsuit01_normal.png',rough=.88)
 eye=mat('Eyes_CC0',(1,1,1,1),SRC/'brown_eye.png',rough=.32)
 shoemat=mat('Shoes_CC0',(1,1,1,1),SYS/'clothes/shoes03/shoes03_diffuse.png',rough=.6)
 # Head/neck/hands visible; clothed torso and legs removed to prevent skin bleed.
 bodyfaces=[]
 for f in BF:
  if f[2]!='body':continue
  c=sum((transform(MORPH[i]) for i in f[0]),Vector())/len(f[0])
  visible=[sum(w for n,w in BW[i].items() if n in ['head','neck01','wrist.L','wrist.R']) for i in f[0]]
  if max(visible)>.30 or (c.z>(1.70 if sex=='male' else 1.62)-.35 and abs(c.x)<.075):bodyfaces.append(f)
 body=mesh('Adult_skin',list(map(transform,MORPH)),BUV,bodyfaces,BW,[skin])
 fitted(Path(f'hair/{hair}/{hair}'),'Hair',hairmat)
 # Eye mesh uses explicit single-vertex associations from the official proxy.
 v,u,ff=objread(SRC/'low-poly.obj');maps=[int(l) for l in (SRC/'low-poly.mhclo').read_text().split('verts 0')[1].splitlines() if l.strip().isdigit()]
 mesh('Eyes',[transform(MORPH[i]) for i in maps],u,ff,[{'head':1} for i in maps],[eye])
 def keepcloth(vs):
  z=sum(v.z for v in vs)/len(vs)
  if typ=='saree':return z>.95
  if typ in ['panjabi','salwar','salwar_braid']:return True
  return True
 clothes=fitted(Path('clothes/male_casualsuit01/male_casualsuit01'),'Office_clothing',shirtmat,keepcloth)
 clothes.data.materials.append(legmat)
 if typ!='shirt':clothes.data.materials[0]=tunicmat
 if typ in ['salwar','salwar_braid','saree']:clothes.data.materials[1]=mat('Garment_trousers',(.16,.19,.23,1),rough=.85)
 for poly in clothes.data.polygons:
  c=sum((clothes.data.vertices[i].co for i in poly.vertices),Vector())/len(poly.vertices);poly.material_index=1 if c.z<.92 else 0
 if typ in ['panjabi','salwar','salwar_braid']:
  cloak('Long_modest_tunic',1.06,.57 if typ=='panjabi' else .55,.185,.24,.13,.17,tunicmat)
 if typ=='saree':
  cloak('Saree_pleated_skirt',.98,.07,.205,.28,.15,.195,tunicmat);drape(tunicmat)
 fitted(Path('clothes/shoes03/shoes03'),'Closed_shoes',shoemat)
 # Vertex data beyond body group is present for correspondence only; drop unused vertices.
 for o in list(bpy.context.scene.objects):
  if o.type=='MESH':
   bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='DESELECT');bpy.ops.mesh.select_loose();bpy.ops.mesh.delete(type='VERT');bpy.ops.object.mode_set(mode='OBJECT');o.select_set(False)
 poses={k:pose(k) for k in ['idle','greeting','presenting','show_sample','browsing','fabric','carry_files','phone','typing','listening','notes','phone_seated','tea','sewing','greeting_seated']+[f'walk_{i:02}' for i in range(12)]+[f'{k}__seat_{int(round(top*100000))}' for k in ['typing','listening','notes','phone_seated','tea','sewing','greeting_seated'] for top in [.4445,.48768,.49022,.50292]]};pose_library[typ]=poses
 pose('idle')
 # Neutral upright relaxed-arm pose becomes bind-pose for export? Keep original bind and store posed state as animation library.
 for p in RIG.pose.bones:p.rotation_quaternion=(1,0,0,0);p.location=(0,0,0)
 bpy.context.view_layer.update()
 # Mesh LOD copies share one skeleton. Low-detail meshes retain the authored skin/UVs.
 originals=[o for o in bpy.context.scene.objects if o.type=='MESH']
 stats={}
 bpy.context.scene.render.film_transparent=False
 for lod,ratio in [('LOD0',1.),('LOD1',.38)]:
  objs=[]
  for o in originals:
   if lod=='LOD0':ob=o;ob.name=f'{lod}_{o.name}'
   else:
    ob=o.copy();ob.data=o.data.copy();bpy.context.collection.objects.link(ob);ob.name=o.name.replace('LOD0','LOD1');bpy.context.view_layer.objects.active=ob;mod=ob.modifiers.new('LOD simplification','DECIMATE');mod.ratio=ratio
    # Modifier must precede armature; rest shape is used.
    bpy.ops.object.modifier_move_up(modifier=mod.name)
    bpy.ops.object.modifier_apply(modifier=mod.name)
   objs.append(ob)
  stats[lod]={'vertices':sum(len(o.data.vertices) for o in objs),'triangles':sum(sum(len(p.vertices)-2 for p in o.data.polygons) for o in objs),'drawMeshes':len(objs)}
 # GPU morph targets vary generic fictional faces without duplicating actor geometry.
 for ob in list(bpy.context.scene.objects):
  if ob.type!='MESH' or 'Adult_skin' not in ob.name:continue
  ob.shape_key_add(name='Basis')
  h=1.70 if sex=='male' else 1.62
  for keyname in ['Face_width','Face_length','Nose_profile']:
   key=ob.shape_key_add(name=keyname)
   for i,vert in enumerate(ob.data.vertices):
    x,y,z=vert.co;u=max(0,min(1,(z-h+.28)/.28));mask=math.sin(u*math.pi)
    if z<h-.28:continue
    if keyname=='Face_width':key.data[i].co.x=x*(1+.06*mask)
    elif keyname=='Face_length':key.data[i].co.z=z+(z-(h-.14))*.10*mask
    else:key.data[i].co.y=y-.007*math.exp(-(x/.045)**2-((z-(h-.13))/.05)**2)
 # Anatomical finger curl morph for a generic phone/cup grip. Original finger weights,
 # not box hands, define the deformation; the runtime chooses it only for hand-held tasks.
 fingerweights={}
 for bn,items in WEIGHTS.items():
  if bn.startswith('finger') and bn.endswith('.R'):
   for vi,w in items:fingerweights.setdefault(vi,[]).append((bn,w))
 axis=(joint(SK['bones']['finger2-1.R']['head'])-joint(SK['bones']['finger5-1.R']['head'])).normalized();fm={}
 for finger in range(1,6):
  cumulative=Matrix.Identity(4)
  for seg in range(1,4):
   bn=f'finger{finger}-{seg}.R'
   if bn not in SK['bones']:continue
   pivot=joint(SK['bones'][bn]['head']);ang=math.radians(([20,25,25] if finger==1 else [48,62,48])[seg-1]);rotation=Quaternion(axis,ang).to_matrix().to_4x4();cumulative=cumulative@Matrix.Translation(pivot)@rotation@Matrix.Translation(-pivot);fm[bn]=cumulative.copy()
 for ob in list(bpy.context.scene.objects):
  if ob.type!='MESH' or 'Adult_skin' not in ob.name:continue
  key=ob.shape_key_add(name='Phone_grip_R')
  for i,vert in enumerate(ob.data.vertices):
   _,vi,_=TREE.find(vert.co);items=fingerweights.get(vi,[])
   if not items:continue
   delta=Vector()
   for bn,w in items:
    if bn in fm:delta+=(fm[bn]@vert.co-vert.co)*w
   key.data[i].co=vert.co+delta
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/f'{typ}-source.blend'))
 bpy.ops.export_scene.gltf(filepath=str(OUT/f'{typ}.glb'),export_format='GLB',export_yup=True,export_animations=False,export_skins=True,export_materials='EXPORT',export_image_format='JPEG',export_jpeg_quality=88,export_extras=True)
 stats['bytes']=(OUT/f'{typ}.glb').stat().st_size;allstats[typ]=stats
 (ROOT/'poses.json').write_text(json.dumps(pose_library,separators=(',',':')))
 print('BUILT',typ,stats,flush=True)
(ROOT/'poses.json').write_text(json.dumps(pose_library,separators=(',',':')))
(ROOT/'asset-stats.json').write_text(json.dumps(allstats,indent=2))
print('ALL_DONE',json.dumps(allstats),flush=True)
