"""Package one verified cumulative room increment; preserve previous packages."""
from pathlib import Path
import argparse, hashlib, json, re, subprocess, sys, zipfile

here=Path(__file__).resolve().parent
repo=here.parents[2]
p=argparse.ArgumentParser()
p.add_argument('room',help='Completed room name, e.g. Boardroom')
p.add_argument('--staging',type=Path,default=Path('/workspace/office-release-packages'))
a=p.parse_args()
if not re.fullmatch(r'[A-Za-z][A-Za-z_-]*',a.room):p.error('Use a plain room name')
name=a.room+'_Realistic_Offline'
folder=a.staging/name
subprocess.run([sys.executable,str(here/'build_offline.py'),str(folder)],check=True)
manifest=json.loads((folder/'offline-manifest.json').read_text())
model=next(x for x in manifest['source_files'] if x['path']=='model_web_baked.glb')
assert model['sha256']=='faaf09d1a61d2136a96a8b2eb4146be1f29135483dd7f94e67e6f3a54596d20a','Unreviewed baseline model'
used={'Office_Realistic_Tour.html','offline-manifest.json','READ_ME.txt',*manifest['resource_packs']}
out=repo/'GARMENT_OFFICE_WALKTHROUGH_FINAL/09_MAC_OFFLINE_TOUR'/('realistic-'+a.room.lower())
out.mkdir(parents=True,exist_ok=True)
archive=out/(name+'.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for f in sorted(folder.rglob('*')):
        rel=f.relative_to(folder)
        if f.is_file() and (len(rel.parts)>1 or f.name in used):z.write(f,Path(name)/rel)
release={'room_completed':a.room,'file':archive.name,'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'base_model_sha256':model['sha256'],'runtime_manifest':manifest,'validation':'See accompanying room QA; native MacBook performance and file:// opening unverified.'}
(out/'release.json').write_text(json.dumps(release,indent=2)+'\n')
(out/'README.md').write_text(f'# {a.room} cumulative offline increment\n\nExtract the entire ZIP, then open `{name}/Office_Realistic_Tour.html` in Firefox. Keep every extracted file together. Original tour and earlier increment packages remain preserved.\n\nPeople shown are illustrative. Native MacBook FPS and direct file opening have not been verified. See included licences and READ_ME.\n')
print(json.dumps({k:v for k,v in release.items() if k!='runtime_manifest'}))
