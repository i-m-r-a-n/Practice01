"""Diagnostic-only RTLightmap filter comparison. Never rewrites input EXRs."""
import argparse,ctypes as c,hashlib,json,pathlib,time
import numpy as np
import OpenEXR

def main():
    p=argparse.ArgumentParser();p.add_argument('source',type=pathlib.Path);p.add_argument('output',type=pathlib.Path);p.add_argument('--library',default='/workspace/tools/blender-5.2.3-linux-x64/lib/libOpenImageDenoise.so');p.add_argument('--threads',type=int,default=2);p.add_argument('--normal',type=pathlib.Path);group=p.add_mutually_exclusive_group();group.add_argument('--albedo',type=pathlib.Path);group.add_argument('--unit-albedo',action='store_true',help='Diagnostic constant-white reflectance for no-albedo illumination, not a measured or baked material guide');a=p.parse_args()
    assert a.source.resolve()!=a.output.resolve()
    with OpenEXR.File(str(a.source),separate_channels=True) as image:rgb=np.stack([image.channels()[k].pixels.astype(np.float32) for k in 'RGB'],axis=-1)
    height,width=rgb.shape[:2];arr=np.ascontiguousarray(rgb);out=np.empty_like(arr);lib=c.CDLL(a.library);vp=c.c_void_p;sz=c.c_size_t
    lib.oidnNewDevice.argtypes=[c.c_int];lib.oidnNewDevice.restype=vp;lib.oidnSetDeviceInt.argtypes=[vp,c.c_char_p,c.c_int];lib.oidnCommitDevice.argtypes=[vp]
    lib.oidnNewFilter.argtypes=[vp,c.c_char_p];lib.oidnNewFilter.restype=vp;lib.oidnSetSharedFilterImage.argtypes=[vp,c.c_char_p,vp,c.c_int,sz,sz,sz,sz,sz]
    lib.oidnCommitFilter.argtypes=[vp];lib.oidnExecuteFilter.argtypes=[vp];lib.oidnGetDeviceError.argtypes=[vp,c.POINTER(c.c_char_p)];lib.oidnGetDeviceError.restype=c.c_int;lib.oidnReleaseFilter.argtypes=[vp];lib.oidnReleaseDevice.argtypes=[vp]
    filter_type='RT' if a.normal or a.albedo or a.unit_albedo else 'RTLightmap'
    device=lib.oidnNewDevice(1);lib.oidnSetDeviceInt(device,b'numThreads',a.threads);lib.oidnCommitDevice(device);f=lib.oidnNewFilter(device,filter_type.encode())
    lib.oidnSetSharedFilterImage(f,b'color',arr.ctypes.data,3,width,height,0,12,width*12);lib.oidnSetSharedFilterImage(f,b'output',out.ctypes.data,3,width,height,0,12,width*12)
    if a.normal:
        with OpenEXR.File(str(a.normal),separate_channels=True) as im:encoded=np.stack([im.channels()[k].pixels.astype(np.float32) for k in 'RGB'],axis=-1)
        assert encoded.shape==rgb.shape
        meta=json.loads(a.normal.with_suffix('.json').read_text());transform=np.array(meta['normal_to_world'],dtype=np.float32);normal=(encoded*2-1)@transform.T;normal[np.all(encoded==0,axis=-1)]=0;normal/=np.maximum(np.linalg.norm(normal,axis=-1,keepdims=True),1e-8);normal=np.ascontiguousarray(normal)
        lib.oidnSetSharedFilterImage(f,b'normal',normal.ctypes.data,3,width,height,0,12,width*12);lib.oidnSetFilterBool.argtypes=[vp,c.c_char_p,c.c_bool];lib.oidnSetFilterBool(f,b'hdr',True);lib.oidnSetFilterBool(f,b'cleanAux',True)
    albedo_range=None;albedo_clamps=0
    if a.albedo:
        with OpenEXR.File(str(a.albedo),separate_channels=True) as im:albedo=np.stack([im.channels()[k].pixels.astype(np.float32) for k in 'RGB'],axis=-1)
        assert albedo.shape==rgb.shape and np.isfinite(albedo).all()
        assert albedo.min()>=0 and albedo.max()<=1.001,'Actual albedo guide outside supported [0,1] range; inspect rather than silently changing it'
        albedo_range=[float(albedo.min()),float(albedo.max())];albedo_clamps=int(np.count_nonzero(albedo>1));albedo=np.ascontiguousarray(np.clip(albedo,0,1));lib.oidnSetSharedFilterImage(f,b'albedo',albedo.ctypes.data,3,width,height,0,12,width*12);lib.oidnSetFilterBool.argtypes=[vp,c.c_char_p,c.c_bool];lib.oidnSetFilterBool(f,b'hdr',True);lib.oidnSetFilterBool(f,b'cleanAux',True)
    if a.unit_albedo:
        albedo=np.ones_like(arr);albedo_range=[1.0,1.0];lib.oidnSetSharedFilterImage(f,b'albedo',albedo.ctypes.data,3,width,height,0,12,width*12);lib.oidnSetFilterBool.argtypes=[vp,c.c_char_p,c.c_bool];lib.oidnSetFilterBool(f,b'hdr',True);lib.oidnSetFilterBool(f,b'cleanAux',True)
    # RTLightmap is HDR-only by definition. It has no RT filter's `hdr` toggle.
    start=time.monotonic();lib.oidnCommitFilter(f);lib.oidnExecuteFilter(f);seconds=time.monotonic()-start
    message=c.c_char_p();err=lib.oidnGetDeviceError(device,c.byref(message));error_text=message.value.decode() if message.value else None;lib.oidnReleaseFilter(f);lib.oidnReleaseDevice(device)
    if err:raise RuntimeError(f'OIDN error {err}: {error_text}')
    assert np.isfinite(out).all();neg=int(np.count_nonzero(out<0));out=np.maximum(out,0).astype(np.float16)
    a.output.parent.mkdir(parents=True,exist_ok=True);OpenEXR.File({'compression':OpenEXR.ZIP_COMPRESSION,'type':OpenEXR.scanlineimage},{k:np.ascontiguousarray(out[:,:,i]) for i,k in enumerate('RGB')}).write(str(a.output))
    result={'purpose':'Diagnostic postprocess of retained raw scene-linear EXR, not adopted production replacement','filter':filter_type,'directional':False,'inputScale':'automatic','normalGuide':str(a.normal) if a.normal else None,'normalGuideSHA256':hashlib.sha256(a.normal.read_bytes()).hexdigest() if a.normal else None,'normalGuideDescription':'Actual deterministic Cycles NORMAL bake, decoded RGB*2-1 and transformed to world space' if a.normal else None,'albedoGuide':str(a.albedo) if a.albedo else None,'albedoGuideSHA256':hashlib.sha256(a.albedo.read_bytes()).hexdigest() if a.albedo else None,'albedoGuideDescription':'Actual Cycles DIFFUSE/COLOR guide, not multiplied into input irradiance' if a.albedo else None,'cleanAux':bool(a.normal or a.albedo),'source':str(a.source),'sourceSHA256':hashlib.sha256(a.source.read_bytes()).hexdigest(),'output':str(a.output),'outputSHA256':hashlib.sha256(a.output.read_bytes()).hexdigest(),'shape':list(out.shape),'sourceMax':float(rgb.max()),'outputMax':float(out.max()),'negativeOutputChannelsClamped':neg,'seconds':seconds,'threads':a.threads,'documentation':'https://github.com/RenderKit/oidn/blob/v2.3.3/README.md#rtlightmap','library':a.library}
    result.update(albedoSourceRange=albedo_range,albedoGuideChannelValuesClamped=albedo_clamps,unitAlbedoDiagnostic=a.unit_albedo)
    if a.unit_albedo:result.update(albedoGuideDescription='Constant RGB1 unit-reflectance diagnostic for no-albedo irradiance; not an actual material albedo bake',cleanAux=True)
    a.output.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
