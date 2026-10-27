"""Independent source-GLB triangle vs prop-envelope audit. No Blender or model edits.
A positive hit is a candidate contact, not automatically a prop-mesh intersection.
A zero count proves no source surface crosses that inset prop envelope above support.
"""
import json,struct,pathlib,hashlib,numpy as np
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[3];BASE=ROOT/'GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC'
p=ROOT/'GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/Final_Office_Interior.glb';b=p.read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);binary=memoryview(b)[28+n:]
component={5120:np.int8,5121:np.uint8,5122:np.int16,5123:np.uint16,5125:np.uint32,5126:np.float32};width={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4,'MAT4':16}
def acc(i):
 a=g['accessors'][i];v=g['bufferViews'][a['bufferView']];dtype=component[a['componentType']];w=width[a['type']];offset=v.get('byteOffset',0)+a.get('byteOffset',0);stride=v.get('byteStride',np.dtype(dtype).itemsize*w)
 return np.ndarray((a['count'],w),dtype=dtype,buffer=binary,offset=offset,strides=(stride,np.dtype(dtype).itemsize))
def local(n):
 if 'matrix'in n:return np.array(n['matrix']).reshape((4,4),order='F')
 x,y,z,w=n.get('rotation',[0,0,0,1]);M=np.eye(4);M[:3,:3]=[[1-2*y*y-2*z*z,2*x*y-2*z*w,2*x*z+2*y*w],[2*x*y+2*z*w,1-2*x*x-2*z*z,2*y*z-2*x*w],[2*x*z-2*y*w,2*y*z+2*x*w,1-2*x*x-2*y*y]];M[:3,:3]=M[:3,:3]@np.diag(n.get('scale',[1,1,1]));M[:3,3]=n.get('translation',[0,0,0]);return M
world={}
def walk(i,parent):
 M=parent@local(g['nodes'][i]);world[i]=M
 for k in g['nodes'][i].get('children',[]):walk(k,M)
for i in g['scenes'][g.get('scene',0)]['nodes']:walk(i,np.eye(4))
objs=[];screens=[]
for i,M in world.items():
 node=g['nodes'][i]
 if 'mesh'not in node:continue
 for j,r in enumerate(g['meshes'][node['mesh']]['primitives']):
  if r.get('mode',4)!=4:continue
  v=acc(r['attributes']['POSITION']);v=v@M[:3,:3].T+M[:3,3];ix=acc(r['indices']).reshape(-1) if 'indices'in r else np.arange(len(v));tri=v[ix.reshape(-1,3)];mat=g['materials'][r.get('material',0)];bbox=[tri.min((0,1)),tri.max((0,1))]
  objs.append({'node':node['name'],'zone':node.get('extras',{}).get('zone'),'asset':node.get('extras',{}).get('asset'),'material':mat['name'],'tri':tri,'min':bbox[0],'max':bbox[1]})
  if mat['name'].startswith('screen_'):
   uv=acc(r['attributes']['TEXCOORD_0']) if'TEXCOORD_0'in r['attributes']else None
   screens.append({'node':node['name'],'zone':node.get('extras',{}).get('zone'),'material':mat['name'],'uv_min':uv.min(0).tolist() if uv is not None else None,'uv_max':uv.max(0).tolist()if uv is not None else None,'exported_material':mat})
def tri_box(tris,lo,hi):
 """Separating axis theorem, exact triangle/AABB surface intersection."""
 c=(lo+hi)/2;e=(hi-lo)/2;t=tris-c
 keep=np.ones(len(t),dtype=bool)
 edges=[t[:,1]-t[:,0],t[:,2]-t[:,1],t[:,0]-t[:,2]]
 axes=[np.cross(edges[0],edges[1])]
 for ed in edges:
  for basis in np.eye(3):axes.append(np.cross(ed,basis))
 for axis in axes:
  proj=np.sum(t*axis[:,None,:],axis=2);r=np.sum(np.abs(axis)*e,axis=1);keep&=(proj.min(1)<=r+1e-9)&(proj.max(1)>=-r-1e-9)
 return keep
m=json.loads((BASE/'props/office-props-manifest.json').read_text());bounds=json.loads((BASE/'props/prop-world-bounds.json').read_text());results=[]
for prop in m['props']:
 bb=bounds[prop['id']];lo=np.array(bb['min']);hi=np.array(bb['max']);lo+=.001;hi-=.001;lo[1]=max(lo[1],prop['position'][1]+.002)
 if np.any(hi<=lo):results.append({'id':prop['id'],'type':prop['type'],'zone':prop['zone'],'thin_surface_only':True,'hits':[]});continue
 hits=[]
 for ob in objs:
  if np.any(ob['min']>hi)or np.any(ob['max']<lo):continue
  T=ob['tri'];sel=np.all(T.max(1)>=lo,axis=1)&np.all(T.min(1)<=hi,axis=1);T=T[sel]
  if not len(T):continue
  count=int(tri_box(T,lo,hi).sum())
  if count:hits.append({'node':ob['node'],'material':ob['material'],'asset':ob['asset'],'triangles_crossing_envelope':count})
 results.append({'id':prop['id'],'type':prop['type'],'zone':prop['zone'],'support':prop['support'],'hits':hits})
out={'source_glb_sha256':hashlib.sha256(b).hexdigest(),'prop_manifest_sha256':hashlib.sha256((BASE/'props/office-props-manifest.json').read_bytes()).hexdigest(),'prop_module_sha256':hashlib.sha256((BASE/'props/office-props.mjs').read_bytes()).hexdigest(),'prop_bounds_sha256':hashlib.sha256((BASE/'props/prop-world-bounds.json').read_bytes()).hexdigest(),'method':'Exact source triangle/AABB separating-axis test, against 1mm-inset generated prop envelope above support+2mm. Positive result needs exact prop surface review; empty interior/cup or rotated-space envelope can yield broadphase positives. No source changes.','source_primitives':len(objs),'props':len(results),'props_with_source_surface_hits':sum(bool(r['hits'])for r in results),'results':results}
(HERE/'source-contact-candidates.json').write_text(json.dumps(out,indent=2)+'\n');(HERE/'screen-material-audit.json').write_text(json.dumps({'source_glb_sha256':out['source_glb_sha256'],'screen_primitives':len(screens),'screens':screens,'finding':'screen_ui and screen_brand export with uniform white emission and no map. Source procedural gradient does not export. No readable generic content is present. Replacements need component-local screen UV projection; furniture uses shared meter-scaled UVs rather than independent 0..1 per display.'},indent=2)+'\n')
print(json.dumps({'props':len(results),'surface_hit_candidates':out['props_with_source_surface_hits'],'examples':[r for r in results if r['hits']][:20],'screen_primitives':len(screens)},indent=2))
