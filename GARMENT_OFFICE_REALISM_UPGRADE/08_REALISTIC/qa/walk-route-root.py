"""Independent grid-connectivity witness; not a browser or construction-clearance test."""
from pathlib import Path
import base64, collections, hashlib, json
import numpy as np
from scipy.ndimage import label, binary_dilation

ROOT = Path(__file__).resolve().parents[3]
ASSETS = ROOT / 'GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS'
grid = json.loads((ASSETS/'walk_grid.json').read_text())
meta = json.loads((ASSETS/'office_web_metadata.json').read_text())
blocked = np.unpackbits(np.frombuffer(base64.b64decode(grid['blocked_bits_base64']), dtype=np.uint8), bitorder='little')[:grid['rows']*grid['cols']].reshape(grid['rows'],grid['cols']).astype(bool)
res = grid['res']; ox, oz = grid['origin_xz']
def xz(rc):
    r,c = rc
    return [round(ox+(c+.5)*res,6), round(oz+(r+.5)*res,6)]
def cell(p):
    return (int((p[1]-oz)//res), int((p[0]-ox)//res))
def inside(x,z,poly):
    hit=False
    for (a,b),(c,d) in zip(poly, poly[1:]+poly[:1]):
        if (b>z)!=(d>z) and x<(c-a)*(z-b)/(d-b)+a: hit=not hit
    return hit
rooms={r['zone']:r for r in meta['rooms']}
cams={c['name']:c for c in meta['cameras']}
start=cell([cams['CAM_01_Reception_A']['position'][i] for i in [0,2]])
structure=np.array([[0,1,0],[1,1,1],[0,1,0]])
components,_=label(~blocked,structure)
component=int(components[start])
assert component>0
connected=components==component
zones=['Z01','Z02','Z30','Z08','Z12','Z07','Z18','Z20','Z23','Z25']
waypoints=[]
for z in zones:
    room=rooms[z]; cam=cams.get(room.get('primary_camera'))
    wanted=[cam['position'][i] for i in [0,2]] if cam else room['centroid_xz']
    candidates=[]
    for r,c in np.argwhere(connected):
        x,y=xz((r,c))
        if inside(x,y,room['polygon_xz']): candidates.append(((x-wanted[0])**2+(y-wanted[1])**2,(int(r),int(c))))
    assert candidates, z
    d,rc=min(candidates)
    waypoints.append({'zone':z,'name':room['name'],'cell':list(rc),'xz':xz(rc),'camera_offset_m':round(d**.5,4)})
def route(a,b):
    a=tuple(a); b=tuple(b); q=collections.deque([a]); parent={a:None}
    while q:
        r,c=q.popleft()
        if (r,c)==b: break
        for nr,nc in [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]:
            n=(nr,nc)
            if 0<=nr<grid['rows'] and 0<=nc<grid['cols'] and connected[n] and n not in parent:
                parent[n]=(r,c); q.append(n)
    assert b in parent
    out=[]; n=b
    while n is not None: out.append(n); n=parent[n]
    return out[::-1]
legs=[]
for a,b in zip(waypoints,waypoints[1:]):
    cells=route(a['cell'],b['cell'])
    assert all(not blocked[p] for p in cells)
    assert all(abs(a[0]-b[0])+abs(a[1]-b[1])==1 for a,b in zip(cells,cells[1:]))
    # Keep every grid centre: no simplification that could cut a corner.
    legs.append({'from':a['zone'],'to':b['zone'],'length_m':round((len(cells)-1)*res,3),'points_xz':[xz(p) for p in cells]})
# A sensitivity probe, not a new collision grid or a certified body-clearance model.
grown=binary_dilation(blocked,structure=structure,iterations=1)
larger,_=label(~grown,structure)
larger_component=int(larger[start])
sensitivity={}
for z in zones:
    poly=rooms[z]['polygon_xz']
    sensitivity[z]=bool(larger_component and any(inside(*xz((r,c)),poly) for r,c in np.argwhere(larger==larger_component)))
out={'status':'static grid witness passes; actual viewer walk and occupied scene not tested here','source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ASSETS/'walk_grid.json',ASSETS/'office_web_metadata.json']},'grid_resolution_m':res,'inherited_walker_radius_m':grid['walker_radius_m'],'connected_component_cells':int(connected.sum()),'waypoints':waypoints,'legs':legs,'total_route_m':round(sum(x['length_m'] for x in legs),3),'one_cell_obstacle_growth_connectivity':sensitivity,'limits':['Uses inherited raster geometry; not a new geometric collision proof.','Four-connected routes avoid diagonal corner cutting. Every grid centre is retained.','No people or new props included; repeat occupied-state checks before acceptance.','Extra one-cell growth is an approximate sensitivity test, not proof of exact 0.25m body clearance.','Native browser walking, door thresholds, visual clipping and full-body clearance need separate tests.']}
target=Path(__file__).with_name('walk-route-witness.json'); target.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','total_route_m','one_cell_obstacle_growth_connectivity']},indent=2))
