import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[1];P=json.loads((R/'poses.json').read_text());out={}
for typ in P:
 bpy.ops.wm.open_mainfile(filepath=str(R/'assets'/f'{typ}-source.blend'))
 rig=bpy.data.objects['OfficeAdultRig'];out[typ]={}
 for task in ['idle','typing__seat_49022','listening__seat_50292','listening__seat_44450','phone_seated__seat_50292','sewing__seat_49022']:
  pose=P[typ][task]
  for b in rig.pose.bones:b.rotation_mode='QUATERNION';b.rotation_quaternion=pose['bones'][b.name]
  bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();measure={}
  for ob in bpy.context.scene.objects:
   if ob.type!='MESH' or not ob.name.startswith('LOD0') or 'Long_modest' in ob.name:continue
   ev=ob.evaluated_get(dg);me=ev.to_mesh();vs=[v.co+Vector((0,0,pose['rootY'])) for v in me.vertices];d={'minZ':min(v.z for v in vs),'maxZ':max(v.z for v in vs)}
   if 'Office_clothing' in ob.name:
    ii=set(i for poly in me.polygons if poly.material_index==1 for i in poly.vertices);selected=[vs[i] for i in ii if abs(vs[i].x)<.22 and -.20<vs[i].y<.22];d['seatFootprintMinZ']=min(v.z for v in selected) if selected else None
   if 'Adult_skin' in ob.name:
    for side in ['L','R']:
     gi=ob.vertex_groups['wrist_'+side].index;ii=[v.index for v in ob.data.vertices if any(g.group==gi and g.weight>.2 for g in v.groups)];d['hand'+side]={'min':list(map(min,zip(*[vs[i] for i in ii]))),'max':list(map(max,zip(*[vs[i] for i in ii])))}
   measure[ob.name]=d;ev.to_mesh_clear()
  out[typ][task]=measure
(R/'review/deformation-diagnostic.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
