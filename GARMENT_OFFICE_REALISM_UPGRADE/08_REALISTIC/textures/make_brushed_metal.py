"""Self-made, seamless 2K brushed micro-normal and roughness maps.

No external image inputs. Deterministic Fourier abrasion lines run along U.
These maps are an illustrative surface finish, not measured product data.
Metal colour and metalness remain the approved material's own values.
"""
import hashlib,json,pathlib
import numpy as np
from PIL import Image
ROOT=pathlib.Path(__file__).resolve().parent/'pbr2k'

def main():
    n=2048;rng=np.random.default_rng(3292);u=np.arange(n,dtype=np.float32)[None,:]/n;v=np.arange(n,dtype=np.float32)[:,None]/n
    height=np.zeros((n,n),dtype=np.float32)
    # Periodic integer frequencies keep all edges seamless.
    for _ in range(64):
        fv=int(rng.integers(100,720));fu=int(rng.integers(-3,4));phase=float(rng.uniform(0,2*np.pi))
        height+=(1/fv)*np.sin(2*np.pi*(fu*u+fv*v)+phase)
    dx=(np.roll(height,-1,axis=1)-np.roll(height,1,axis=1))*.5
    dy=(np.roll(height,-1,axis=0)-np.roll(height,1,axis=0))*.5
    # Fine 0.10-ish normal perturbation; consumer can reduce normalScale.
    scale=.10/max(float(np.std(dy)),1e-9)
    normal=np.stack([-dx*scale,-dy*scale,np.ones_like(height)],axis=-1)
    normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
    rough=np.clip(.35+.025*height/max(float(np.std(height)),1e-9),.23,.47)
    outputs={'normal':np.round((normal*.5+.5)*255).astype(np.uint8),'roughness':np.repeat(np.round(rough[...,None]*255).astype(np.uint8),3,axis=-1)}
    records=json.loads((ROOT/'sources.json').read_text()) if (ROOT/'sources.json').exists() else []
    records=[r for r in records if r['set']!='selfmade_brushed_metal']
    for role,pixels in outputs.items():
        path=ROOT/'source/selfmade_brushed_metal'/(role+'.png');path.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(pixels).save(path)
        records.append({'set':'selfmade_brushed_metal','role':role,'file':str(path.relative_to(ROOT)),'source':'../make_brushed_metal.py','bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pixels':[n,n],'mode':'RGB','upscaled':False,'normalConvention':'OpenGL +Y' if role=='normal' else None,'licence':'Self-made for this project, no third-party assets','licenceURL':None,'assetURL':None,'seed':3292})
    (ROOT/'sources.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps({'set':'selfmade_brushed_metal','maps':len(outputs),'pixels':[n,n]}))

if __name__=='__main__':main()
