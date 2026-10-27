"""Reuse existing people assets; write only Boardroom and cumulative room release data.

Run with Blender --background --python this_file.py. The accepted Reception
source files are read and hashed, never rewritten. No GLB or office model edits.
"""
import bpy, copy, hashlib, json, math
from pathlib import Path
from mathutils import Vector, Quaternion

PEOPLE=Path(__file__).resolve().parents[1]
SOURCE=json.loads((PEOPLE/'people-manifest.json').read_text())
POSES=json.loads((PEOPLE/'poses.json').read_text())
OUT={}
FORWARD={8:.03,9:.05,10:.03,11:.05,12:.03}

def apply(p):
 for b in rig.pose.bones:
  b.rotation_mode='QUATERNION';b.rotation_quaternion=p['bones'][b.name]
 bpy.context.view_layer.update()

def aim(bn,vec):
 pb=rig.pose.bones[bn];bpy.context.view_layer.update()
 q=(pb.tail-pb.head).normalized().rotation_difference(Vector(vec).normalized())
 mat=(q@pb.matrix.to_quaternion()).to_matrix().to_4x4();mat.translation=pb.head
 pb.matrix=mat;bpy.context.view_layer.update()

def arm(side,W,wristQ):
 S=rig.data.bones['upperarm01_'+side].head_local
 E0=rig.data.bones['lowerarm01_'+side].head_local
 W0=rig.data.bones['wrist_'+side].head_local
 A=(E0-S).length;B=(W0-E0).length;d=W-S;u=d.normalized();D=min(d.length,A+B-.003)
 W=S+u*D;x=(A*A-B*B+D*D)/(2*D);h=math.sqrt(max(0,A*A-x*x))
 sgn=1 if side=='L' else -1;v=Vector((sgn*.18,.05,-.12));v=(v-u*v.dot(u)).normalized();E=S+u*x+v*h
 aim('upperarm01_'+side,E-S);aim('lowerarm01_'+side,W-E)
 pb=rig.pose.bones['wrist_'+side];mat=wristQ.to_matrix().to_4x4();mat.translation=pb.head;pb.matrix=mat;bpy.context.view_layer.update()

actors=copy.deepcopy([a for a in SOURCE['actors'] if a['zone']=='Z08'])
for actor in actors:
 actor['frozen']=True;actor.pop('path',None)
 n=int(actor['id'][-2:]);offset=FORWARD.get(n,0)
 actor['position'][0]+=math.sin(actor['yaw'])*offset
 actor['position'][2]+=math.cos(actor['yaw'])*offset
 typ=actor['outfit'];OUT.setdefault(typ,{})[actor['pose']]=copy.deepcopy(POSES[typ][actor['pose']])

# One standing presenter faces the unchanged screen and extends a hand toward it.
typ='salwar';bpy.ops.wm.open_mainfile(filepath=str(PEOPLE/'assets'/f'{typ}-source.blend'))
rig=bpy.data.objects['OfficeAdultRig'];apply(POSES[typ]['typing__seat_50292'])
flat=rig.pose.bones['wrist_L'].matrix.to_quaternion();base=POSES[typ]['idle'];apply(base)
root=base['rootY']+.01016
arm('L',Vector((.20,-.56,1.55-root)),flat)
presenter=copy.deepcopy(base);presenter['bones']={b.name:list(b.rotation_quaternion) for b in rig.pose.bones};presenter['frozen']=True
OUT[typ].pop('presenting',None);OUT[typ]['boardroom_presenting']=presenter
actors[-1].update(pose='boardroom_presenting',yaw=-math.pi/2)

# Notes rest at the actual notebook paper, with the original chair-contact legs.
for actor in actors:
 if actor['task']!='notes':continue
 typ=actor['outfit'];base=POSES[typ][actor['pose']]
 bpy.ops.wm.open_mainfile(filepath=str(PEOPLE/'assets'/f'{typ}-source.blend'));rig=bpy.data.objects['OfficeAdultRig'];apply(base)
 wrists={side:(rig.pose.bones['wrist_'+side].head.copy(),rig.pose.bones['wrist_'+side].matrix.to_quaternion()) for side in ['L','R']}
 for side,(W,rotation) in wrists.items():
  W.z-=.00443;arm(side,W,rotation)
 pb=rig.pose.bones['head'];rotation=Quaternion(Vector((1,0,0)),math.radians(12))
 mat=(rotation@pb.matrix.to_quaternion()).to_matrix().to_4x4();mat.translation=pb.head;pb.matrix=mat;bpy.context.view_layer.update()
 newpose=copy.deepcopy(base);newpose['bones']={b.name:list(b.rotation_quaternion) for b in rig.pose.bones};newpose['frozen']=True
 OUT[typ].pop(actor['pose'],None);OUT[typ]['boardroom_notes']=newpose;actor['pose']='boardroom_notes'

# Two side listeners glance toward the presenter; the head-of-table listener
# already faces the screen. Only head orientation changes in these reused poses.
for actor,degrees in [(actors[1],45),(actors[2],-45)]:
 typ=actor['outfit'];base=POSES[typ][actor['pose']]
 bpy.ops.wm.open_mainfile(filepath=str(PEOPLE/'assets'/f'{typ}-source.blend'));rig=bpy.data.objects['OfficeAdultRig'];apply(base)
 pb=rig.pose.bones['head'];rotation=Quaternion(Vector((0,0,1)),math.radians(degrees))
 mat=(rotation@pb.matrix.to_quaternion()).to_matrix().to_4x4();mat.translation=pb.head;pb.matrix=mat;bpy.context.view_layer.update()
 newpose=copy.deepcopy(base);newpose['bones']={b.name:list(b.rotation_quaternion) for b in rig.pose.bones};newpose['frozen']=True
 OUT[typ].pop(actor['pose'],None);OUT[typ]['boardroom_listening']=newpose;actor['pose']='boardroom_listening'

props=[]
for actor in actors:
 if actor['task']!='notes':continue
 x,y,z=actor['position'];yaw=actor['yaw'];f=.54
 props.append({'id':'boardroom_notes_'+actor['id'][-2:],'owner':actor['id'],'type':'notebook','position':[x+math.sin(yaw)*f,.75707,z+math.cos(yaw)*f],'yaw':yaw,'size':[.40,.012,.25],'pen':True})

board=copy.deepcopy(SOURCE)
board.update(version='boardroom-static-2',count=6,defaultEnabled=False,status='Boardroom six fixed actors: contact review pending',actors=actors,poses='boardroom/poses.json',frozen=True,activeZones=['Z08'],navigation={'mode':'No locomotion or gesture animation; fixed posed people with visitor collision'},props=props,limitations=['Frozen fictional illustrative people.','Bounded Boardroom contact review pending.','Native Mac performance has not been tested.'])
(PEOPLE/'boardroom/people-manifest.json').write_text(json.dumps(board,indent=2)+'\n')
(PEOPLE/'boardroom/poses.json').write_text(json.dumps(OUT,separators=(',',':')))

reception=json.loads((PEOPLE/'reception/people-manifest.json').read_text())
reception_poses=json.loads((PEOPLE/'reception/poses.json').read_text())
combined=copy.deepcopy(reception)
combined.update(version='reception4-boardroom6-static-1',count=10,status='Reception accepted; Boardroom fixed contact review pending',actors=copy.deepcopy(reception['actors'])+actors,poses='room-release/poses.json',activeZones=['Z02','Z08'],props=copy.deepcopy(reception.get('props',[]))+props,limitations=['Frozen fictional illustrative people.','Reception accepted; bounded Boardroom review pending.','Native Mac performance has not been tested.'])
minimal=copy.deepcopy(OUT)
for actor in reception['actors']:
 minimal.setdefault(actor['outfit'],{})[actor['pose']]=copy.deepcopy(reception_poses[actor['outfit']][actor['pose']])
assert combined['actors'][:4]==reception['actors']
assert combined['props'][:len(reception.get('props',[]))]==reception.get('props',[])
(PEOPLE/'room-release/people-manifest.json').write_text(json.dumps(combined,indent=2)+'\n')
(PEOPLE/'room-release/poses.json').write_text(json.dumps(minimal,separators=(',',':')))
for folder in ['boardroom','room-release']:
 paths=['people-layer.js',folder+'/people-manifest.json',folder+'/poses.json','reception/people-manifest.json','reception/poses.json']+[v['file'] for v in SOURCE['assets'].values()]
 lock={p:hashlib.sha256((PEOPLE/p).read_bytes()).hexdigest() for p in paths}
 (PEOPLE/folder/'source-lock.json').write_text(json.dumps(lock,indent=2)+'\n')
print('BOARDROOM_AND_CUMULATIVE_READY',[(a['id'],a['pose']) for a in actors],flush=True)
