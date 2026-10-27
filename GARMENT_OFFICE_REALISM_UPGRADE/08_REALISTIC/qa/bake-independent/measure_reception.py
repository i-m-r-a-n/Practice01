"""Read-only geometry/atlas statistics. No Blender process or re-bake."""
import json,struct,pathlib,hashlib,sys,numpy as np
sys.path.insert(0,'/tmp/office-texture-py');import OpenEXR
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[3];BASE=ROOT/'GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC'
def read_glb(path):
 b=path.read_bytes();n=struct.unpack_from('<I',b,12)[0];g=json.loads(b[20:20+n]);binary=memoryview(b)[28+n:];dtype={5121:np.uint8,5123:np.uint16,5125:np.uint32,5126:np.float32};wid={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}
 def acc(i):
  a=g['accessors'][i];v=g['bufferViews'][a['bufferView']];d=dtype[a['componentType']];w=wid[a['type']];return np.ndarray((a['count'],w),dtype=d,buffer=binary,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',np.dtype(d).itemsize*w),np.dtype(d).itemsize))
 def local(n):
  if'matrix'in n:return np.array(n['matrix']).reshape((4,4),order='F')
  x,y,z,w=n.get('rotation',[0,0,0,1]);M=np.eye(4);M[:3,:3]=[[1-2*y*y-2*z*z,2*x*y-2*z*w,2*x*z+2*y*w],[2*x*y+2*z*w,1-2*x*x-2*z*z,2*y*z-2*x*w],[2*x*z-2*y*w,2*y*z+2*x*w,1-2*x*x-2*y*y]];M[:3,:3]=M[:3,:3]@np.diag(n.get('scale',[1,1,1]));M[:3,3]=n.get('translation',[0,0,0]);return M
 world={}
 def walk(i,parent):
  M=parent@local(g['nodes'][i]);world[i]=M
  for j in g['nodes'][i].get('children',[]):walk(j,M)
 for i in g['scenes'][g.get('scene',0)]['nodes']:walk(i,np.eye(4))
 out=[]
 for i,M in world.items():
  node=g['nodes'][i]
  if'mesh'not in node:continue
  for p in g['meshes'][node['mesh']]['primitives']:
   if p.get('mode',4)!=4:continue
   v=acc(p['attributes']['POSITION']);v=v@M[:3,:3].T+M[:3,3];ix=acc(p['indices']).reshape(-1).reshape(-1,3);out.append({'node':node['name'],'mat':g['materials'][p.get('material',0)]['name'],'tri':v[ix],'uv':acc(p['attributes']['TEXCOORD_1'])[ix] if'TEXCOORD_1'in p['attributes']else None})
 return out
work=pathlib.Path('/workspace/office-bake-work/diagnostic-z02');prims=read_glb(work/'Z02.glb')
def exr(p):
 with OpenEXR.File(str(p),separate_channels=True)as f:return np.stack([f.channels()[k].pixels for k in'RGB'],-1).astype(np.float32)
raw=exr(work/'Z02_raw.exr');oidn=exr(work/'Z02.exr');size=raw.shape[0]
z=json.loads((work/'Z02.json').read_text());objbounds=z['bake']['original_object_bboxes'];targets={'BM008 Room 3 secondary':'steel_painted','BM009 Room 3 secondary':'steel_painted','BM010 Room 3 secondary':'steel_painted','F011 lounge_green':'fab_green','F009 sofa_84_sand':'fab_sand','Z02 RECEPTION + VISITOR WAITING - floor finish':'fl_terrazzo'}
def raster(uv,mask):
 xy=np.stack([uv[:,0]*size,uv[:,1]*size],-1);a,b,c=xy;lo=np.maximum(np.floor(xy.min(0)).astype(int),0);hi=np.minimum(np.ceil(xy.max(0)).astype(int),size-1)
 if np.any(hi<lo):return
 xx,yy=np.meshgrid(np.arange(lo[0],hi[0]+1)+.5,np.arange(lo[1],hi[1]+1)+.5);u=b-a;v=c-a;den=u[0]*v[1]-u[1]*v[0]
 if abs(den)<1e-9:return
 aa=((xx-a[0])*v[1]-(yy-a[1])*v[0])/den;bb=(u[0]*(yy-a[1])-u[1]*(xx-a[0]))/den;sel=(aa>.05)&(bb>.05)&(aa+bb<.95)
 mask[lo[1]:hi[1]+1,lo[0]:hi[0]+1]|=sel
results=[]
for name,mat in targets.items():
 B=objbounds[name];lo=np.array([B[0][0],B[0][2],-B[1][1]])-.00001;hi=np.array([B[1][0],B[1][2],-B[0][1]])+.00001;mask=np.zeros((size,size),bool);num=0
 for p in prims:
  if p['mat']!=mat:continue
  inside=np.all(p['tri'].min(1)>=lo,1)&np.all(p['tri'].max(1)<=hi,1)
  for tri,uv in zip(p['tri'][inside],p['uv'][inside]):
   if name.startswith('BM'):
    normal=np.cross(tri[1]-tri[0],tri[2]-tri[0]);normal/=max(np.linalg.norm(normal),1e-10)
    if abs(normal[1])>.5:continue # vertical beam faces only, no beam/deck top contact
   raster(uv,mask);num+=1
 entry={'object':name,'material':mat,'interior_triangle_texels':int(mask.sum()),'triangles':num}
 for key,image in [('raw32',raw),('rtlightmap32',oidn)]:
  samples=image[mask];lum=samples@np.array([.2126,.7152,.0722]);entry[key]={'mean':float(lum.mean()),'std':float(lum.std()),'cv':float(lum.std()/lum.mean()),'percentiles':[float(v)for v in np.percentile(lum,[0,1,5,25,50,75,95,99,100])],'fraction_below_0_01':float(np.mean(lum<.01)),'fraction_above_4':float(np.mean(lum>4))}
 results.append(entry)
inv=json.loads((BASE/'blender/source-inventory.json').read_text());target_mats={r['name']:r for r in inv['materials']if r['name']in["steel_painted","paint_white","fab_green","paint_ceiling"]};report={'source_files':{str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in [work/'Z02.glb',work/'Z02_raw.exr',work/'Z02.exr']},'method':'glTF UV1 already has Blender V flipped; sample EXR top-down rows with y=v*height. Actual exported UV1 triangles, central barycentric interiors (>5%edge margin), image scene-linear luma. Beam samples exclude horizontal top/bottom faces to avoid intentional slab contact. Whole-object spatial light gradients remain in variance.','samples':results,'materials':target_mats,'target_image_shape':list(raw.shape)}
(HERE/'reception-atlas-stats.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(results,indent=2))
