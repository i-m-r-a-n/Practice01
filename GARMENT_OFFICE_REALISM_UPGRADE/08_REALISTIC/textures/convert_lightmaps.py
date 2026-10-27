"""One-shot conversion of completed room EXRs. No background loop or scheduling.

Run only after the baker finishes saving a room. Never edits its shared manifest.
The adjacent ktx2-index.json can be merged by the manifest's single owner.
"""
import argparse,hashlib,json,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--ktx',required=True);parser.add_argument('--directory','--output-root',dest='directory',type=pathlib.Path,default=ROOT.parent/'lighting',help='Completed EXR staging directory; KTX2 and index are written beside its sources');parser.add_argument('--room');args=parser.parse_args()
    index={}
    for src in sorted(args.directory.glob((args.room or '*')+'.exr')):
        # Auxiliary guides and retained noisy inputs are evidence, not runtime lightmaps.
        if src.stem.endswith(('_raw','_normal','_albedo')):continue
        dst=src.with_suffix('.ktx2');report=dst.with_suffix('.ktx2.json');source_hash=hashlib.sha256(src.read_bytes()).hexdigest()
        record=json.loads(report.read_text()) if report.exists() else {}
        if not dst.exists() or record.get('sourceSha256')!=source_hash:
            result=subprocess.run([sys.executable,str(ROOT/'convert_textures.py'),'--ktx',args.ktx,'lightmap',str(src),str(dst)],capture_output=True,text=True)
            if result.returncode:raise RuntimeError(result.stderr or result.stdout)
            record=json.loads(report.read_text())
        index[src.stem]={'url':dst.name,'format':'ktx2','textureFormat':'RGBA16F','supercompression':'zstd','linear':True,'channel':1,'mipLevels':1,'flipY':False,'sourceRowOrder':'top-left','bytes':record['outputBytes'],'gpuBytes':record['gpuBaseLevelBytes'],'sha256':record['outputSha256'],'sourceEXR':src.name,'sourceEXRSha256':source_hash,'sourceMax':record['sourceMax'],'decodedLevelBitExact':record['decodedLevelBitExact']}
        print(json.dumps({'room':src.stem,'bytes':record['outputBytes'],'max':record['sourceMax']}),flush=True)
    path=args.directory/'ktx2-index.json'
    if args.room and path.exists():
        prior=json.loads(path.read_text());prior.update(index);index=prior
    path.write_text(json.dumps(index,indent=2)+'\n')

if __name__=='__main__':main()
