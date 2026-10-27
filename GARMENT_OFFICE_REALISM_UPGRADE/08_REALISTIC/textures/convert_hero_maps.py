"""Sequential native 2K PBR conversion; limit CPU during parallel Cycles work."""
import argparse,json,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--ktx',required=True);parser.add_argument('--threads',type=int,default=1);args=parser.parse_args()
    source=json.loads((ROOT/'pbr2k/sources.json').read_text());index={}
    for entry in source:
        src=ROOT/'pbr2k'/entry['file'];dst=ROOT/'pbr2k/ktx2'/entry['set']/(entry['role']+'.ktx2')
        report=dst.with_suffix('.ktx2.json')
        reuse=False
        if report.exists() and dst.exists():
            record=json.loads(report.read_text());reuse=record.get('sourceSha256')==entry['sha256']
        if not reuse:
            process=subprocess.run([sys.executable,str(ROOT/'convert_textures.py'),'--ktx',args.ktx,'pbr','--role',entry['role'],'--threads',str(args.threads),str(src),str(dst)],capture_output=True,text=True)
            if process.returncode:raise RuntimeError(process.stderr or process.stdout)
            record=json.loads(report.read_text())
        index.setdefault(entry['set'],{})[entry['role']]={'file':str(dst.relative_to(ROOT/'pbr2k')),'bytes':record['outputBytes'],'sha256':record['outputSha256'],'width':record['width'],'height':record['height'],'colorSpace':record['colorSpace'],'encoding':record['encoding']}
        (ROOT/'pbr2k/index.json').write_text(json.dumps(index,indent=2)+'\n')
        print(json.dumps({'set':entry['set'],'role':entry['role'],'bytes':record['outputBytes'],'cached':reuse}),flush=True)

if __name__=='__main__':main()
