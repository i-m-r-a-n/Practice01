"""Create a genuine HDR preview from an explicitly selected accepted atlas.

No scheduling or acceptance inference. The caller must choose a visually
accepted corrected source. Preview pixels use scene-linear box averaging; no
AgX, gamma, albedo or exposure transform. Full-quality review must use the source
atlas, because smaller UV charts may acquire bleed or lose detail when reduced.
"""
import argparse,hashlib,json,pathlib,subprocess,sys
import numpy as np
import OpenEXR
from convert_textures import exr_pixels

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('source',type=pathlib.Path);p.add_argument('output',type=pathlib.Path);p.add_argument('--size',type=int,choices=[512,1024],default=1024);p.add_argument('--ktx',required=True);a=p.parse_args()
    assert a.output.suffix=='.ktx2';assert a.source.resolve()!=a.output.resolve()
    rgb=exr_pixels(a.source);h,w=rgb.shape[:2];assert h==w and h>=a.size and h%a.size==0
    factor=h//a.size;reduced=rgb.reshape(a.size,factor,a.size,factor,3).mean(axis=(1,3),dtype=np.float64).astype(np.float32);half=reduced.astype(np.float16)
    a.output.parent.mkdir(parents=True,exist_ok=True);preview_exr=a.output.with_suffix('.exr');assert preview_exr.resolve()!=a.source.resolve()
    OpenEXR.File({'compression':OpenEXR.ZIP_COMPRESSION,'type':OpenEXR.scanlineimage},{k:np.ascontiguousarray(half[:,:,i]) for i,k in enumerate('RGB')}).write(str(preview_exr))
    result=subprocess.run([sys.executable,str(pathlib.Path(__file__).with_name('convert_textures.py')),'--ktx',a.ktx,'lightmap',str(preview_exr),str(a.output)],capture_output=True,text=True)
    if result.returncode:raise RuntimeError(result.stderr or result.stdout)
    record={'purpose':'Temporary progressive-loading HDR preview, not full-quality acceptance evidence','source':str(a.source),'sourceSHA256':sha(a.source),'sourceSize':[w,h],'previewSize':[a.size,a.size],'linearBoxFactor':factor,'toneMapping':False,'gammaTransform':False,'albedoApplied':False,'sourceRange':[float(rgb.min()),float(rgb.max())],'previewRange':[float(half.min()),float(half.max())],'sourceMeanRGB':rgb.mean(axis=(0,1),dtype=np.float64).tolist(),'previewMeanRGB':half.mean(axis=(0,1),dtype=np.float64).tolist(),'halfFloatMaxAbsoluteError':float(np.abs(half.astype(np.float32)-reduced).max()),'previewEXR':str(preview_exr),'previewEXRSHA256':sha(preview_exr),'output':str(a.output),'outputSHA256':sha(a.output),'outputBytes':a.output.stat().st_size,'limitations':'Box reduction can blend small UV islands or remove contact-shadow detail. Final atlas must replace this and be used for acceptance screenshots.'}
    a.output.with_suffix('.provenance.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
if __name__=='__main__':main()
