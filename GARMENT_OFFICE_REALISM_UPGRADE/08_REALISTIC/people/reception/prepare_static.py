import bpy,json,math
from pathlib import Path
from mathutils import Vector,Quaternion
R=Path(__file__).resolve().parents[1];P=json.loads((R/'poses.json').read_text());M=json.loads((R/'people-manifest.json').read_text());OUT={}
def apply(p):
 for b in rig.pose.bones:b.rotation_mode='QUATERNION';b.rotation_quaternion=p['bones'][b.name]
 bpy.context.view_layer.update()
def aim(bn,vec):
 pb=rig.pose.bones[bn];bpy.context.view_layer.update();q=(pb.tail-pb.head).normalized().rotation_difference(Vector(vec).normalized());mat=(q@pb.matrix.to_quaternion()).to_matrix().to_4x4();mat.translation=pb.head;pb.matrix=mat;bpy.context.view_layer.update()
def arm(side,W,wristQ):
 S=rig.data.bones['upperarm01_'+side].head_local;E0=rig.data.bones['lowerarm01_'+side].head_local;W0=rig.data.bones['wrist_'+side].head_local;A=(E0-S).length;B=(W0-E0).length;d=W-S;D=d.length;u=d.normalized();D=min(D,A+B-.003);W=S+u*D;x=(A*A-B*B+D*D)/(2*D);h=math.sqrt(max(0,A*A-x*x));sgn=1 if side=='L' else -1;v=Vector((sgn*.18,.05,-.12));v=(v-u*v.dot(u)).normalized();E=S+u*x+v*h
 aim('upperarm01_'+side,E-S);aim('lowerarm01_'+side,W-E);pb=rig.pose.bones['wrist_'+side];mat=wristQ.to_matrix().to_4x4();mat.translation=pb.head;pb.matrix=mat;bpy.context.view_layer.update()
def savepose(typ,n,base):
 p=json.loads(json.dumps(base));p['bones']={b.name:list(b.rotation_quaternion) for b in rig.pose.bones};p['frozen']=True;OUT[typ][n]=p
for typ in ['shirt','panjabi','salwar','salwar_braid']:
 bpy.ops.wm.open_mainfile(filepath=str(R/'assets'/f'{typ}-source.blend'));rig=bpy.data.objects['OfficeAdultRig'];OUT[typ]=P[typ]
 if typ in ['shirt','salwar']:
  apply(P[typ]['typing__seat_49022']);flat={side:rig.pose.bones['wrist_'+side].matrix.to_quaternion() for side in ['L','R']}
  base=P[typ]['idle'];apply(base);side='L' if typ=='salwar' else 'R';sgn=1 if side=='L' else -1;root=base['rootY']+.01016
  arm(side,Vector((sgn*.17,-(.43 if typ=='salwar' else .44),1.305-root)),flat[side])
  pb=rig.pose.bones['head'];q=Quaternion(Vector((1,0,0)),math.radians(10));mat=(q@pb.matrix.to_quaternion()).to_matrix().to_4x4();mat.translation=pb.head;pb.matrix=mat
  savepose(typ,'reception_badge_giver' if typ=='salwar' else 'reception_badge_receiver',base)
 if typ=='salwar_braid':
  base=P[typ]['listening__seat_44450'];apply(P[typ]['typing__seat_49022']);flat={side:rig.pose.bones['wrist_'+side].matrix.to_quaternion() for side in ['L','R']};apply(base);root=base['rootY'];bookY=.647
  for side,sgn in [('L',1),('R',-1)]:
   rot=Quaternion(Vector((0,0,1)),-sgn*math.pi/2)@flat[side];W=Vector((sgn*.22,-.31,bookY+.057-root));body=bpy.data.objects['LOD0_Adult_skin'];gi=body.vertex_groups['wrist_'+side].index;ii=[v.index for v in body.data.vertices if any(g.group==gi and g.weight>.2 for g in v.groups)]
   for _ in range(5):
    arm(side,W,rot);ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();lowest=min(me.vertices[i].co.z+root for i in ii);ev.to_mesh_clear();W.z+=bookY+.0205-lowest
   arm(side,W,rot)
  pb=rig.pose.bones['head'];q=Quaternion(Vector((1,0,0)),math.radians(23));mat=(q@pb.matrix.to_quaternion()).to_matrix().to_4x4();mat.translation=pb.head;pb.matrix=mat
  savepose(typ,'reception_fabric_book',base)
a={x['id']:x for x in M['actors']};actors=[]
for i in ['office-person-01','office-person-02','office-person-03','office-person-04']:
 x=a[i];x.pop('path',None);x['frozen']=True
 if i=='office-person-01':
  x.update(position=[13.32,0,3.75],yaw=-math.pi/2,seated=False,heightScale=1,bodyWidth=1,pose='reception_badge_giver',task='badge_giver');x.pop('support',None);x.pop('wardrobeMode',None)
 if i=='office-person-02':x.update(position=[12.08,0,3.75],yaw=math.pi/2,heightScale=1,bodyWidth=1,pose='reception_badge_receiver',task='badge_receiver',handGrip=.12)
 if i=='office-person-04':x.update(pose='reception_fabric_book',task='fabric_book')
 actors.append(x)
M.update(version='reception-static-1',count=4,defaultEnabled=False,status='Reception-only frozen pose contact review pending',actors=actors,poses='reception/poses.json',frozen=True,activeZones=['Z02'],navigation={'mode':'No actor locomotion or gesture animation; fixed posed people with visitor collision'},props=[{'id':'reception_visitor_badge','owner':'office-person-01','type':'badge','position':[12.70,1.2728,3.92],'size':[.085,.003,.055]},{'id':'reception_fabric_book','owner':'office-person-04','type':'fabric_book','position':[actors[3]['position'][0],.647,actors[3]['position'][2]-.31],'yaw':math.pi,'size':[.36,.018,.24]}],limitations=['Frozen illustrative people, not live animation.','Current Reception pose and hand-prop contacts require final review.','Native Mac performance has not been tested.'])
(R/'reception/poses.json').write_text(json.dumps(OUT,separators=(',',':')));(R/'reception/people-manifest.json').write_text(json.dumps(M,indent=2));print('STATIC_READY',[(x['id'],x['pose']) for x in actors])
