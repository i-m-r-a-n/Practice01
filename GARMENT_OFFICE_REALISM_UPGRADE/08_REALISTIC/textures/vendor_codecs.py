"""Vendor the exact Three.js r169 KTX2 reader/transcoder dependencies."""
import hashlib,json,pathlib,urllib.request

ROOT=pathlib.Path(__file__).resolve().parent/'codecs/three_r169'
BASE='https://raw.githubusercontent.com/mrdoob/three.js/r169/'
FILES=['examples/jsm/loaders/KTX2Loader.js','examples/jsm/utils/WorkerPool.js','examples/jsm/libs/ktx-parse.module.js','examples/jsm/libs/zstddec.module.js','examples/jsm/libs/basis/basis_transcoder.js','examples/jsm/libs/basis/basis_transcoder.wasm','examples/jsm/libs/basis/README.md','LICENSE']
def main():
    manifest=[]
    for name in FILES:
        data=urllib.request.urlopen(BASE+name).read();out=ROOT/name;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
        manifest.append({'file':name,'source':BASE+name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    (ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'files':len(manifest),'bytes':sum(x['bytes'] for x in manifest)}))
if __name__=='__main__':main()
