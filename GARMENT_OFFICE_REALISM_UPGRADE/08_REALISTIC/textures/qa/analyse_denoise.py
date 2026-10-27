"""Read-only numeric comparison of same-atlas raw and OIDN lightmap pixels.

UV1 masks come from the matching diagnostic GLB. Statistics describe changes;
they do not prove that every removed/retained spatial feature is noise.
"""
import argparse,hashlib,json,pathlib,struct
import numpy as np
import OpenEXR
from PIL import Image,ImageDraw
from scipy.ndimage import binary_erosion,gaussian_filter,distance_transform_edt

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def exr(p):
    with OpenEXR.File(str(p),separate_channels=True) as f:
        return np.stack([f.channels()[c].pixels.astype(np.float32) for c in 'RGB'],axis=-1)
def glb(p):
    data=p.read_bytes();length=struct.unpack_from('<I',data,12)[0];doc=json.loads(data[20:20+length]);offset=20+length;size=struct.unpack_from('<I',data,offset)[0];binary=data[offset+8:offset+8+size]
    def accessor(i):
        a=doc['accessors'][i];v=doc['bufferViews'][a['bufferView']];dtype={5126:'<f4',5125:'<u4',5123:'<u2',5121:'u1'}[a['componentType']];n={'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[a['type']];item=np.dtype(dtype).itemsize
        return np.ndarray((a['count'],n),dtype=dtype,buffer=binary,offset=v.get('byteOffset',0)+a.get('byteOffset',0),strides=(v.get('byteStride',item*n),item)).copy()
    return doc,accessor
def main():
    parser=argparse.ArgumentParser();parser.add_argument('directory',type=pathlib.Path);parser.add_argument('--room',default='Z02');parser.add_argument('--filtered',type=pathlib.Path);parser.add_argument('--output',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent/'z02-denoise-comparison.json');args=parser.parse_args();d=args.directory
    rawpath=d/(args.room+'_raw.exr');denpath=args.filtered or d/(args.room+'.exr');meshpath=d/(args.room+'.glb');raw=exr(rawpath);den=exr(denpath);assert raw.shape==den.shape
    h,w=raw.shape[:2];doc,get=glb(meshpath);names=[m['name'] for m in doc['materials']];results=[]
    lumraw=raw@np.array([.2126,.7152,.0722],dtype=np.float32);lumden=den@np.array([.2126,.7152,.0722],dtype=np.float32)
    lr=np.log1p(lumraw);ld=np.log1p(lumden);blurraw=gaussian_filter(lr,2);blurden=gaussian_filter(ld,2)
    for material in ['steel_painted','fab_green','fl_terrazzo','paint_white','fab_sand','oak_slat']:
        maskim=Image.new('L',(w,h),0);draw=ImageDraw.Draw(maskim);triangles=0
        for mesh in doc['meshes']:
            for p in mesh['primitives']:
                if names[p.get('material',0)]!=material:continue
                uv=get(p['attributes']['TEXCOORD_1']);ix=get(p['indices']).reshape(-1,3)
                for t in uv[ix]:draw.polygon([(float(x*w),float(y*h)) for x,y in t],fill=255)
                triangles+=len(ix)
        mask=np.array(maskim)>0;interior=binary_erosion(mask,iterations=4);interior&=(lumraw>.001)
        if not interior.any():continue
        a=lumraw[interior];b=lumden[interior];delta=b-a;high_raw=lr[interior]-blurraw[interior];high_den=ld[interior]-blurden[interior];distance=distance_transform_edt(mask);yc,xc=np.unravel_index(np.argmax(distance),distance.shape)
        results.append({'material':material,'triangles':triangles,'maskPixels':int(mask.sum()),'interiorPixels':int(interior.sum()),'rawLuminancePercentiles':dict(zip(['p05','p50','p95'],map(float,np.percentile(a,[5,50,95])))),'oidnLuminancePercentiles':dict(zip(['p05','p50','p95'],map(float,np.percentile(b,[5,50,95])))),'meanLuminanceDelta':float(delta.mean()),'meanAbsLuminanceDelta':float(np.abs(delta).mean()),'relativeAbsDeltaMedian':float(np.median(np.abs(delta)/np.maximum(a,.05))),'rawHighpassLogRMS':float(np.sqrt(np.mean(high_raw**2))),'oidnHighpassLogRMS':float(np.sqrt(np.mean(high_den**2))),'highpassRMSRatio':float(np.sqrt(np.mean(high_den**2))/max(float(np.sqrt(np.mean(high_raw**2))),1e-9)),'smoothLogCorrelation':float(np.corrcoef(blurraw[interior],blurden[interior])[0,1]),'maxInteriorRadiusPx':float(distance[yc,xc]),'exampleInteriorPixelXY':[int(xc),int(yc)]})
    report={'scope':'Same-atlas diagnostic only, 2048 square /32 samples. No production files modified. Four-pixel-eroded UV1 material masks avoid most atlas boundaries ONLY IF the original bake used LightmapUV. The original bake omitted explicit uv_layer; root identified a potential UV0 bake mismatch. Material attribution and spatial conclusions remain UNVERIFIED until that is resolved. Low-variance/low-frequency changes may be genuine illumination or denoiser bias; this is not visual acceptance.','bakeUvLayerVerified':False,'maskUvLayer':'TEXCOORD_1 / LightmapUV','sourceFiles':[{'path':str(p),'sha256':sha(p)} for p in [rawpath,denpath,meshpath]],'rawRange':[float(raw.min()),float(raw.max())],'oidnRange':[float(den.min()),float(den.max())],'shape':list(raw.shape),'materials':results}
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
