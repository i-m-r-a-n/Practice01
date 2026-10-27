"""Placement sanity checks on generated prop bounds, not a visual acceptance substitute."""
import json,math,pathlib
D=pathlib.Path(__file__).resolve().parent
m=json.loads((D/'office-props-manifest.json').read_text());bounds=json.loads((D/'prop-world-bounds.json').read_text())
rooms=json.loads((D.parent/'audit/approved_room_inventory.json').read_text())
polys={r['zone']:[(x*.0254,y*.0254)for x,y in r['polygon_plan_inches']] for r in rooms}
def inside(x,y,p):
 c=False
 for a,b in zip(p,p[1:]+p[:1]):
  if ((a[1]>y)!=(b[1]>y))and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:c=not c
 return c
out=[];below=[];collisions=[]
for p in m['props']:
 b=bounds[p['id']];corners=[(x,z)for x in[b['min'][0],b['max'][0]]for z in[b['min'][2],b['max'][2]]]
 if not all(inside(x,z,polys[p['zone']])for x,z in corners):out.append(p['id'])
 if b['min'][1]<p['position'][1]-.0005:below.append({'id':p['id'],'type':p['type'],'below_surface_m':p['position'][1]-b['min'][1]})
for i,a in enumerate(m['props']):
 for b in m['props'][i+1:]:
  if a['zone']!=b['zone']:continue
  A=bounds[a['id']];B=bounds[b['id']]
  ds=[min(A['max'][j],B['max'][j])-max(A['min'][j],B['min'][j])for j in range(3)]
  if all(v>.0005 for v in ds):collisions.append({'a':a['id'],'b':b['id'],'types':[a['type'],b['type']],'aabb_overlap_m':ds})
r={'props':len(m['props']),'rooms_reviewed':len(rooms),'all_prop_world_bounds_inside_assigned_room':not out,'outside_room_ids':out,'prop_bounds_below_support':below,'prop_pair_aabb_overlaps':collisions,'scope':'Uses generated geometry world-axis bounds and approved room polygons. Pair overlaps are broadphase candidates, not automatically exact mesh intersections. No source component intersection proof, GPU/image or dynamic collision claim.'}
(D/'placement-checks.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
