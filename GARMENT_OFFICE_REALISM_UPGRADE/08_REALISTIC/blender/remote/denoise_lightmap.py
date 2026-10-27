"""Production RTLightmap postprocess in an isolated process. Input raw EXRs are immutable."""
import argparse,ctypes as c,hashlib,json,pathlib,time
import numpy as np
import OpenEXR

def main():
    p=argparse.ArgumentParser();p.add_argument('source',type=pathlib.Path);p.add_argument('output',type=pathlib.Path);p.add_argument('--library',default='/workspace/tools/oidn/oidn-2.3.3.x86_64.linux/lib/libOpenImageDenoise.so');p.add_argument('--threads',type=int,default=2);a=p.parse_args()
    assert a.source.resolve()!=a.output.resolve()
    with OpenEXR.File(str(a.source),separate_channels=True) as image:rgb=np.stack([image.channels()[k].pixels.astype(np.float32) for k in 'RGB'],axis=-1)
    height,width=rgb.shape[:2];arr=np.ascontiguousarray(rgb);out=np.empty_like(arr);lib=c.CDLL(a.library);vp=c.c_void_p;sz=c.c_size_t
    lib.oidnNewDevice.argtypes=[c.c_int];lib.oidnNewDevice.restype=vp;lib.oidnSetDeviceInt.argtypes=[vp,c.c_char_p,c.c_int];lib.oidnCommitDevice.argtypes=[vp]
    lib.oidnNewFilter.argtypes=[vp,c.c_char_p];lib.oidnNewFilter.restype=vp;lib.oidnSetSharedFilterImage.argtypes=[vp,c.c_char_p,vp,c.c_int,sz,sz,sz,sz,sz]
    lib.oidnCommitFilter.argtypes=[vp];lib.oidnExecuteFilter.argtypes=[vp];lib.oidnGetDeviceError.argtypes=[vp,c.POINTER(c.c_char_p)];lib.oidnGetDeviceError.restype=c.c_int;lib.oidnReleaseFilter.argtypes=[vp];lib.oidnReleaseDevice.argtypes=[vp]
    device=lib.oidnNewDevice(1);lib.oidnSetDeviceInt(device,b'numThreads',a.threads);lib.oidnCommitDevice(device);f=lib.oidnNewFilter(device,b'RTLightmap')
    lib.oidnSetSharedFilterImage(f,b'color',arr.ctypes.data,3,width,height,0,12,width*12);lib.oidnSetSharedFilterImage(f,b'output',out.ctypes.data,3,width,height,0,12,width*12)
    # RTLightmap is HDR-only by definition. It has no RT filter's `hdr` toggle.
    start=time.monotonic();lib.oidnCommitFilter(f);lib.oidnExecuteFilter(f);seconds=time.monotonic()-start
    message=c.c_char_p();err=lib.oidnGetDeviceError(device,c.byref(message));error_text=message.value.decode() if message.value else None;lib.oidnReleaseFilter(f);lib.oidnReleaseDevice(device)
    if err:raise RuntimeError(f'OIDN error {err}: {error_text}')
    assert np.isfinite(out).all();neg=int(np.count_nonzero(out<0));out=np.maximum(out,0).astype(np.float16)
    a.output.parent.mkdir(parents=True,exist_ok=True);OpenEXR.File({'compression':OpenEXR.ZIP_COMPRESSION,'type':OpenEXR.scanlineimage},{k:np.ascontiguousarray(out[:,:,i]) for i,k in enumerate('RGB')}).write(str(a.output))
    result={'purpose':'RTLightmap postprocess of retained raw scene-linear EXR; visual acceptance is a separate review','filter':'RTLightmap','directional':False,'inputScale':'automatic','source':str(a.source),'sourceSHA256':hashlib.sha256(a.source.read_bytes()).hexdigest(),'output':str(a.output),'outputSHA256':hashlib.sha256(a.output.read_bytes()).hexdigest(),'shape':list(out.shape),'sourceMax':float(rgb.max()),'outputMax':float(out.max()),'negativeOutputChannelsClamped':neg,'seconds':seconds,'threads':a.threads,'documentation':'https://github.com/RenderKit/oidn/blob/v2.3.3/README.md#rtlightmap','library':a.library,'librarySHA256':hashlib.sha256(pathlib.Path(a.library).read_bytes()).hexdigest(),'numpyVersion':np.__version__,'openEXRVersion':getattr(OpenEXR,'__version__',None)}
    a.output.with_suffix('.denoise.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
