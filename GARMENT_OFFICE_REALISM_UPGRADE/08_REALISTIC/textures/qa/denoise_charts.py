"""Diagnostic UV-chart-isolated RTLightmap filter; never changes approved assets.

Triangle connectivity is reconstructed from matching GLB UV1 edges. Each crop
contains only its own chart radiance, nearest-edge padded. Filtered results are
written only to that chart's pixel-centre interior. Final outside padding uses
the nearest chart, never another chart's denoised crop.
"""
import argparse,ctypes as c,hashlib,json,pathlib,time
import numpy as np
import OpenEXR
from scipy.ndimage import distance_transform_edt,find_objects
from analyse_denoise import glb,exr

def chart_labels(meshpath,width,height):
    doc,get=glb(meshpath);triangles=[]
    for mesh in doc['meshes']:
        for p in mesh['primitives']:
            if p.get('mode',4)!=4 or 'TEXCOORD_1' not in p['attributes']:continue
            uv=get(p['attributes']['TEXCOORD_1']);ix=get(p['indices']).reshape(-1,3);triangles.extend(uv[ix])
    tri=np.asarray(triangles,dtype=np.float32);parents=np.arange(len(tri));edges={}
    def root(i):
        while parents[i]!=i:parents[i]=parents[parents[i]];i=parents[i]
        return i
    for i,t in enumerate(tri):
        for a,b in [(0,1),(1,2),(2,0)]:
            va=tuple(np.rint(t[a]*1e7).astype(np.int64));vb=tuple(np.rint(t[b]*1e7).astype(np.int64));key=tuple(sorted([va,vb]))
            if va==vb:continue
            if key in edges:
                ri=root(i);rj=root(edges[key]);parents[ri]=rj
            else:edges[key]=i
    roots=[root(i) for i in range(len(tri))];ids={r:i+1 for i,r in enumerate(sorted(set(roots)))};labels=np.zeros((height,width),dtype=np.int32);overlap=0
    scale=np.array([width,height],dtype=np.float32)
    for t,r in zip(tri,roots):
        a,b,d=t*scale;area=(b[1]-d[1])*(a[0]-d[0])+(d[0]-b[0])*(a[1]-d[1])
        if abs(area)<1e-8:continue
        lo=np.maximum(np.floor(np.min([a,b,d],axis=0)).astype(int),0);hi=np.minimum(np.ceil(np.max([a,b,d],axis=0)).astype(int),[width,height]);x0,y0=lo;x1,y1=hi
        if x1<=x0 or y1<=y0:continue
        y,x=np.mgrid[y0:y1,x0:x1];x=x+.5;y=y+.5
        wa=((b[1]-d[1])*(x-d[0])+(d[0]-b[0])*(y-d[1]))/area;wb=((d[1]-a[1])*(x-d[0])+(a[0]-d[0])*(y-d[1]))/area
        inside=(wa>=-1e-7)&(wb>=-1e-7)&(wa+wb<=1+1e-7);view=labels[y0:y1,x0:x1];identifier=ids[r]
        overlap+=int(np.count_nonzero(inside&(view!=0)&(view!=identifier)));view[inside]=identifier
    return labels,{'triangles':len(tri),'connectedUVCharts':len(ids),'chartsWithPixels':int(np.unique(labels[labels>0]).size),'crossChartPixelOverlap':overlap,'maskPixels':int(np.count_nonzero(labels))}

class Filter:
    def __init__(self,library,threads):
        self.lib=c.CDLL(library);l=self.lib;vp=c.c_void_p;sz=c.c_size_t
        l.oidnNewDevice.argtypes=[c.c_int];l.oidnNewDevice.restype=vp;l.oidnSetDeviceInt.argtypes=[vp,c.c_char_p,c.c_int];l.oidnCommitDevice.argtypes=[vp];l.oidnNewFilter.argtypes=[vp,c.c_char_p];l.oidnNewFilter.restype=vp;l.oidnSetSharedFilterImage.argtypes=[vp,c.c_char_p,vp,c.c_int,sz,sz,sz,sz,sz];l.oidnCommitFilter.argtypes=[vp];l.oidnExecuteFilter.argtypes=[vp];l.oidnGetDeviceError.argtypes=[vp,c.POINTER(c.c_char_p)];l.oidnGetDeviceError.restype=c.c_int;l.oidnReleaseFilter.argtypes=[vp];l.oidnReleaseDevice.argtypes=[vp]
        self.device=l.oidnNewDevice(1);l.oidnSetDeviceInt(self.device,b'numThreads',threads);l.oidnCommitDevice(self.device);self.filter=l.oidnNewFilter(self.device,b'RTLightmap')
    def apply(self,rgb):
        a=np.ascontiguousarray(rgb,dtype=np.float32);out=np.empty_like(a);h,w=a.shape[:2];l=self.lib
        l.oidnSetSharedFilterImage(self.filter,b'color',a.ctypes.data,3,w,h,0,12,w*12);l.oidnSetSharedFilterImage(self.filter,b'output',out.ctypes.data,3,w,h,0,12,w*12);l.oidnCommitFilter(self.filter);l.oidnExecuteFilter(self.filter)
        msg=c.c_char_p();err=l.oidnGetDeviceError(self.device,c.byref(msg))
        if err:raise RuntimeError(f'OIDN {err}: {msg.value}')
        assert np.isfinite(out).all();return np.maximum(out,0)
    def close(self):self.lib.oidnReleaseFilter(self.filter);self.lib.oidnReleaseDevice(self.device)

def main():
    p=argparse.ArgumentParser();p.add_argument('raw',type=pathlib.Path);p.add_argument('glb',type=pathlib.Path);p.add_argument('output',type=pathlib.Path);p.add_argument('--measure',action='store_true');p.add_argument('--library',default='/workspace/tools/oidn/oidn-2.3.3.x86_64.linux/lib/libOpenImageDenoise.so');p.add_argument('--threads',type=int,default=2);p.add_argument('--padding',type=int,default=32);p.add_argument('--dilation',type=int,default=16);a=p.parse_args();assert a.output.resolve()!=a.raw.resolve()
    start=time.monotonic();rgb=exr(a.raw);h,w=rgb.shape[:2];labels,stats=chart_labels(a.glb,w,h);counts=np.bincount(labels.ravel());stats.update(pixelCountPercentiles={str(n):float(np.percentile(counts[1:][counts[1:]>0],n)) for n in [0,10,50,90,100]},chartsBelow8Pixels=int(np.count_nonzero((counts[1:]>0)&(counts[1:]<8))),pixelsInChartsBelow8=int(counts[1:][counts[1:]<8].sum()),maskBuildSeconds=time.monotonic()-start)
    stats['chartsWithoutPixelCentres']=stats['connectedUVCharts']-stats['chartsWithPixels']
    report={'purpose':'Diagnostic per-chart RTLightmap, not production acceptance','source':str(a.raw),'sourceSHA256':hashlib.sha256(a.raw.read_bytes()).hexdigest(),'geometry':str(a.glb),'geometrySHA256':hashlib.sha256(a.glb.read_bytes()).hexdigest(),'filter':'RTLightmap','padding':a.padding,'finalDilation':a.dilation,'stats':stats,'inputUnchanged':True,'scopeLimit':'Charts with1–7 pixel centres retain raw values. Charts without any pixel centres have no independent raster interior and may sample nearest-chart dilation; they require better UV allocation, not a denoising claim. No denoiser can recover missing spatial resolution. Pixel-centre rasterization does not certify UV uniqueness below pixel resolution.'}
    if not a.measure:
        assert not stats['crossChartPixelOverlap'],'Refusing to overwrite conflicting UV charts'
        output=np.zeros_like(rgb);denoiser=Filter(a.library,a.threads);filtered=0;passed=0
        for cid,sl in enumerate(find_objects(labels),start=1):
            if sl is None:continue
            ys,xs=sl;mask=labels[ys,xs]==cid
            if counts[cid]<8:
                output[ys,xs][mask]=rgb[ys,xs][mask];passed+=1;continue
            # Crop in local coordinates. The pad may extend beyond the atlas;
            # nearest-edge extension only samples this chart's valid pixels.
            local=np.pad(mask,a.padding);source=np.pad(rgb[ys,xs],((a.padding,a.padding),(a.padding,a.padding),(0,0)))
            nearest=distance_transform_edt(~local,return_distances=False,return_indices=True);extended=source[nearest[0],nearest[1]];result=denoiser.apply(extended)
            cropped=result[a.padding:a.padding+mask.shape[0],a.padding:a.padding+mask.shape[1]];output[ys,xs][mask]=cropped[mask];filtered+=1
            if filtered%100==0:print(json.dumps({'filteredCharts':filtered,'seconds':time.monotonic()-start}),flush=True)
        denoiser.close();distance,nearest=distance_transform_edt(labels==0,return_indices=True);pad=(labels==0)&(distance<=a.dilation);output[pad]=output[nearest[0][pad],nearest[1][pad]]
        out=output.astype(np.float16);OpenEXR.File({'compression':OpenEXR.ZIP_COMPRESSION,'type':OpenEXR.scanlineimage},{k:np.ascontiguousarray(out[:,:,i]) for i,k in enumerate('RGB')}).write(str(a.output))
        report.update(output=str(a.output),outputSHA256=hashlib.sha256(a.output.read_bytes()).hexdigest(),filteredCharts=filtered,rawPassthroughCharts=passed,outputMax=float(out.max()),dilationPixels=int(pad.sum()))
    report['seconds']=time.monotonic()-start;a.output.with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
