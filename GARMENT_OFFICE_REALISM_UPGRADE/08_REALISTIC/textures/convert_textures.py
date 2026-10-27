"""Convert lightmaps and ordinary PBR maps without changing their source files.

HDR: linear EXR -> RGBA16F KTX2, losslessly Zstd-supercompressed on disk.
PBR: UASTC for normals/data; ETC1S/BasisLZ for sRGB base colour by default.
This does not claim block-compressed GPU HDR: RGBA16F uses eight bytes/texel.
"""
import argparse, hashlib, json, os, pathlib, shutil, struct, subprocess, sys, tempfile
import numpy as np
import zstandard
from PIL import Image

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def run(args):
    result=subprocess.run([str(a) for a in args],capture_output=True,text=True)
    if result.returncode:raise RuntimeError(result.stderr or result.stdout)
    return result.stdout.strip()
def header(path):
    data=path.read_bytes()
    assert data[:12]==b'\xabKTX 20\xbb\r\n\x1a\n'
    fields=struct.unpack_from('<13I2Q',data,12)
    names=['vkFormat','typeSize','width','height','depth','layerCount','faceCount','levelCount','supercompression','dfdOffset','dfdLength','kvdOffset','kvdLength','sgdOffset','sgdLength']
    return dict(zip(names,fields))
def exr_pixels(path):
    try:import OpenEXR
    except ImportError as exc:raise RuntimeError('Install OpenEXR 3.5.2 (pip), or put its local installation on PYTHONPATH') from exc
    with OpenEXR.File(str(path),separate_channels=True) as image:
        channels=image.channels()
        assert all(c in channels for c in ['R','G','B']), 'EXR needs explicit RGB channels'
        rgb=np.stack([channels[c].pixels.astype(np.float32) for c in ['R','G','B']],axis=-1)
    assert np.isfinite(rgb).all(), 'Non-finite lightmap irradiance'
    assert rgb.min()>=-1e-6, 'Negative lightmap irradiance; inspect the bake instead of clipping it'
    assert rgb.max()<=65504, 'EXR exceeds half-float range; do not silently clamp HDR'
    return rgb

def lightmap(args):
    rgb=exr_pixels(args.input)
    tiny_negative_count=int(np.count_nonzero(rgb<0))
    rgb=np.maximum(rgb,0)
    if args.flip_y:rgb=rgb[::-1].copy()
    height,width=rgb.shape[:2]
    rgba=np.ones((height,width,4),dtype='<f2')
    rgba[...,:3]=rgb.astype('<f2')
    with tempfile.TemporaryDirectory(prefix='office-hdr-') as tmp:
        raw=pathlib.Path(tmp)/'rgba16f.raw'
        raw.write_bytes(rgba.tobytes())
        command=[args.ktx,'create','--raw','--format','R16G16B16A16_SFLOAT','--width',str(width),'--height',str(height),'--assign-tf','linear','--assign-primaries','bt709','--assign-texcoord-origin','top-left','--zstd','9',raw,args.output]
        run(command)
    info=header(args.output)
    assert info['vkFormat']==97 and info['supercompression']==2
    data=args.output.read_bytes()
    offset,length,uncompressed=struct.unpack_from('<3Q',data,80)
    decoded=zstandard.ZstdDecompressor().decompress(data[offset:offset+length],max_output_size=uncompressed)
    assert decoded==rgba.tobytes(), 'KTX2 level bytes differ from the half-float source'
    run([args.ktx,'validate',args.output])
    delta=np.abs(rgba[...,:3].astype(np.float32)-rgb)
    return dict(info,kind='lightmap',encoding='RGBA16F + lossless Zstd',colorSpace='linear-sRGB',origin='top-left',flipSourceRows=args.flip_y,mipLevels=1,gpuBaseLevelBytes=rgba.nbytes,sourceMin=float(rgb.min()),sourceMax=float(rgb.max()),tinyNegativeChannelValuesClamped=tiny_negative_count,halfFloatMaxAbsoluteError=float(delta.max()),halfFloatMeanAbsoluteError=float(delta.mean()),decodedLevelBitExact=True,command=['<temporary RGBA16F raw input>' if str(x)==str(raw) else str(x) for x in command])

def pbr(args):
    with Image.open(args.input) as image:width,height=image.size
    color=args.role=='basecolor'
    codec=args.codec or ('basis-lz' if color else 'uastc')
    command=[args.ktx,'create','--format','R8G8B8A8_SRGB' if color else 'R8G8B8A8_UNORM','--assign-tf','srgb' if color else 'linear','--assign-primaries','bt709' if color else 'none','--assign-texcoord-origin','top-left','--generate-mipmap','--encode',codec,'--threads',str(args.threads)]
    if codec=='uastc':command+=['--uastc-quality','2','--zstd','9']
    else:command+=['--qlevel','192','--clevel','2']
    # Do not use --normal-mode: its XY alpha packing needs a custom normal shader.
    # RGB tangent normals remain RGB here, compatible with MeshStandardMaterial.
    command += [args.input,args.output]
    log=run(command)
    run([args.ktx,'validate',args.output])
    return dict(header(args.output),kind='pbr',role=args.role,encoding=codec,colorSpace='sRGB' if color else 'non-color linear',sourceResolution=[width,height],upscaled=False,normalPacking='RGB tangent-space' if args.role=='normal' else None,command=[str(x) for x in command],encoderOutput=log)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--ktx',default=os.environ.get('OFFICE_KTX_BINARY') or shutil.which('ktx'),required=not(os.environ.get('OFFICE_KTX_BINARY') or shutil.which('ktx')))
    sub=parser.add_subparsers(dest='operation',required=True)
    hdr=sub.add_parser('lightmap');hdr.add_argument('--flip-y',action='store_true')
    maps=sub.add_parser('pbr');maps.add_argument('--role',choices=['basecolor','normal','roughness','metalness','ao','orm'],required=True);maps.add_argument('--codec',choices=['basis-lz','uastc']);maps.add_argument('--threads',type=int,default=2)
    for child in [hdr,maps]:child.add_argument('input',type=pathlib.Path);child.add_argument('output',type=pathlib.Path)
    args=parser.parse_args()
    assert args.input.resolve()!=args.output.resolve(), 'Never overwrite an approved input'
    args.output.parent.mkdir(parents=True,exist_ok=True)
    result=(lightmap if args.operation=='lightmap' else pbr)(args)
    result.update(source=str(args.input),sourceSha256=sha(args.input),output=str(args.output),outputSha256=sha(args.output),outputBytes=args.output.stat().st_size,toolVersion=run([args.ktx,'--version']))
    args.output.with_suffix(args.output.suffix+'.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
