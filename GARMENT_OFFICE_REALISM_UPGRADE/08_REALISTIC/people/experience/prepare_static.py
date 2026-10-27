"""Derive three frozen Experience Centre poses from existing CC0 character sources.

Only this folder and the incremental room-release manifest/poses are written.
The prior ten actors/props/poses are loaded from locked commit039091d inputs.
"""
import bpy, copy, hashlib, json, math
from pathlib import Path
from mathutils import Vector,Quaternion
P=Path(__file__).resolve().parents[1];E=P/'experience'
SOURCE=json.loads((P/'people-manifest.json').read_text());LIB=json.loads((P/'poses.json').read_text())
BASE=json.loads((E/'baseline-people-manifest.json').read_text());BASE_POSES=json.loads((E/'baseline-poses.json').read_text())
actors=copy.deepcopy([a for a in SOURCE['actors'] if a['zone']=='Z30']);poses={};contacts={}
for actor in [actors[0],actors[2]]:actor['hideLongDrape']=True;actor['wardrobeMode']='Modest long-sleeve shirt and trousers; overlapping long drape disabled for this standing pose.'

def apply(p):
 for b in rig.pose.bones:b.rotation_mode='QUATERNION';b.rotation_quaternion=p['bones'][b.name]
 bpy.context.view_layer.update()
def aim(bn,vec):
 pb=rig.pose.bones[bn];bpy.context.view_layer.update();q=(pb.tail-pb.head).normalized().rotation_difference(Vector(vec).normalized());mat=(q@pb.matrix.to_quaternion()).to_matrix().to_4x4();mat.translation=pb.head;pb.matrix=mat;bpy.context.view_layer.update()
def arm(side,W,wristQ):
 S=rig.data.bones['upperarm01_'+side].head_local;E0=rig.data.bones['lowerarm01_'+side].head_local;W0=rig.data.bones['wrist_'+side].head_local;A=(E0-S).length;B=(W0-E0).length;d=W-S;u=d.normalized();D=min(d.length,A+B-.003);W=S+u*D;x=(A*A-B*B+D*D)/(2*D);h=math.sqrt(max(0,A*A-x*x));sgn=1 if side=='L' else -1;v=Vector((sgn*.18,.05,-.12));v=(v-u*v.dot(u)).normalized();bend=S+u*x+v*h
 aim('upperarm01_'+side,bend-S);aim('lowerarm01_'+side,W-bend);pb=rig.pose.bones['wrist_'+side];mat=wristQ.to_matrix().to_4x4();mat.translation=pb.head;pb.matrix=mat;bpy.context.view_layer.update()
def hand_points(side):
 body=bpy.data.objects['LOD0_Adult_skin'];gi=body.vertex_groups['wrist_'+side].index;ii=[v.index for v in body.data.vertices if any(g.group==gi and g.weight>.2 for g in v.groups)]
 ev=body.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();result=[me.vertices[i].co.copy() for i in ii];ev.to_mesh_clear();return result
def save(actor,base,key):
 p=copy.deepcopy(base);p['bones']={b.name:list(b.rotation_quaternion) for b in rig.pose.bones};p['frozen']=True;poses.setdefault(actor['outfit'],{})[key]=p;actor['pose']=key;actor['frozen']=True;actor.pop('path',None)

# Buyer supports the two shoulders of a generic sample tee, without moving a rail.
a=actors[0];typ=a['outfit'];bpy.ops.wm.open_mainfile(filepath=str(P/'assets'/f'{typ}-source.blend'));rig=bpy.data.objects['OfficeAdultRig'];base=LIB[typ]['idle'];apply(LIB[typ]['typing__seat_50292']);flat={s:Quaternion(Vector((1,0,0)),math.radians(30))@rig.pose.bones['wrist_'+s].matrix.to_quaternion() for s in ['L','R']};apply(base)
hand_top=1.3605;contact=[]
for side,sgn in [('L',1),('R',-1)]:
 W=Vector((sgn*.175,-.38,(1.42-.01016)/a['heightScale']-base['rootY']))
 for _ in range(5):
  arm(side,W,flat[side]);pts=hand_points(side);lowest=min(pts,key=lambda p:p.z);world_y=(lowest.z+base['rootY'])*a['heightScale']+.01016;W.z+=(hand_top-world_y)/a['heightScale']
 arm(side,W,flat[side]);low=min(hand_points(side),key=lambda p:p.z);contact.append([low.x*a['bodyWidth'],(low.z+base['rootY'])*a['heightScale']+.01016,-low.y])
pb=rig.pose.bones['head'];q=Quaternion(Vector((1,0,0)),math.radians(12));mat=(q@pb.matrix.to_quaternion()).to_matrix().to_4x4();mat.translation=pb.head;pb.matrix=mat;bpy.context.view_layer.update()
a['task']='holding_sample';save(a,base,'experience_holding_sample');contacts[a['id']]={'local_shoulder_support_points':contact}
front=sum(p[2] for p in contact)/2
garment={'id':'experience_buyer_sample','owner':a['id'],'type':'held_garment','position':[a['position'][0],1.36,a['position'][2]-front],'yaw':math.pi,'color':'#b39b79','provenance':'Self-made project display tee silhouette with shallow drape; supported at both shoulder edges.'}

# Merchandiser explains from the open aisle, using the existing presenting pose.
a=actors[1];typ=a['outfit'];bpy.ops.wm.open_mainfile(filepath=str(P/'assets'/f'{typ}-source.blend'));rig=bpy.data.objects['OfficeAdultRig'];base=LIB[typ]['presenting'];apply(base)
a.update(position=[20.299,0,-7.3232],yaw=-math.pi/2,task='explaining_sample');save(a,base,'experience_explaining_sample')

# Third buyer reaches the exact front surface of a sage garment on unchanged F020.
a=actors[2];typ=a['outfit'];bpy.ops.wm.open_mainfile(filepath=str(P/'assets'/f'{typ}-source.blend'));rig=bpy.data.objects['OfficeAdultRig'];base=LIB[typ]['idle'];apply(LIB[typ]['typing__seat_50292']);flat=rig.pose.bones['wrist_R'].matrix.to_quaternion();apply(base)
target=Vector((19.7449204,1.3834534,-10.1132237));anchor_z=-9.67;front=anchor_z-target.z-.00075
W=Vector((-.10,-.38,(1.43-.01016)/a['heightScale']-base['rootY']))
for _ in range(7):
 arm('R',W,flat);tip=max(hand_points('R'),key=lambda p:-p.y);W.y+=(-tip.y-front);world_y=(tip.z+base['rootY'])*a['heightScale']+.01016;W.z+=(target.y-world_y)/a['heightScale']
arm('R',W,flat);tip=max(hand_points('R'),key=lambda p:-p.y)
a.update(position=[target.x+tip.x*a['bodyWidth'],0,anchor_z],yaw=math.pi,task='touching_rail_fabric');save(a,base,'experience_touching_rail')
contacts[a['id']]={'source_object':'F020 bay_86b','source_material':'g_sage','source_surface_target':list(target),'actual_pose_tip_local':[tip.x*a['bodyWidth'],(tip.z+base['rootY'])*a['heightScale']+.01016,-tip.y],'initial_normal_gap_m':.00075}

experience=copy.deepcopy(SOURCE);experience.update(version='experience-static-1',count=3,defaultEnabled=False,status='Experience Centre fixed contact review pending',actors=actors,poses='experience/poses.json',frozen=True,activeZones=['Z30'],props=[garment],navigation={'mode':'No actor locomotion or gesture animation; fixed posed people with visitor collision'},limitations=['Frozen illustrative people, not live animation.','Generic sample tee supported at shoulders; no pinching hand-grip simulation.','Native Mac performance has not been tested.'])
(E/'people-manifest.json').write_text(json.dumps(experience,indent=2)+'\n');(E/'poses.json').write_text(json.dumps(poses,separators=(',',':')));(E/'pose-contact-targets.json').write_text(json.dumps(contacts,indent=2)+'\n')
release=copy.deepcopy(BASE);release.update(version='reception4-boardroom6-experience3-static-1',count=13,status='Reception and Boardroom accepted; Experience Centre contact review pending',actors=copy.deepcopy(BASE['actors'])+actors,poses='room-release/poses.json',activeZones=['Z02','Z08','Z30'],props=copy.deepcopy(BASE['props'])+[garment],limitations=experience['limitations'])
combined=copy.deepcopy(BASE_POSES)
for typ,items in poses.items():combined.setdefault(typ,{}).update(items)
assert release['actors'][:10]==BASE['actors'];assert release['props'][:len(BASE['props'])]==BASE['props']
assert all(combined[t][k]==v for t,items in BASE_POSES.items() for k,v in items.items())
(P/'room-release/people-manifest.json').write_text(json.dumps(release,indent=2)+'\n');(P/'room-release/poses.json').write_text(json.dumps(combined,separators=(',',':')))
for folder in ['experience','room-release']:
 paths=['people-layer.js',folder+'/people-manifest.json',folder+'/poses.json']+[v['file'] for v in SOURCE['assets'].values()]
 (P/folder/'source-lock.json').write_text(json.dumps({f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in paths},indent=2)+'\n')
print('EXPERIENCE_READY',[(a['id'],a['pose'],a['position']) for a in actors],contacts,flush=True)
