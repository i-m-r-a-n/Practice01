"""Verify the packaged bytes, including inline viewer, against a pinned Git source."""
import argparse, base64, hashlib, json, re, subprocess, zipfile
from pathlib import Path

def digest(data): return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('folder',type=Path); p.add_argument('archive',type=Path); p.add_argument('output',type=Path)
    a=p.parse_args(); repo=Path(__file__).resolve().parents[3]
    m=json.loads((a.folder/'offline-manifest.json').read_text()); source=m['source_commit']
    assert re.fullmatch('[0-9a-f]{40}',source)
    def original(record):
        data=subprocess.check_output(['git','show',source+':'+record['source_path']],cwd=repo)
        assert len(data)==record['bytes'] and digest(data)==record['sha256'],record['path']
        return data
    packs={}
    for name in m['resource_packs']:
        for line in (a.folder/name).read_text().splitlines():
            match=re.fullmatch(r'window\.__OFFLINE_ASSETS\[(.+?)\]=(.+);',line)
            assert match,name
            key=json.loads(match[1]); assert key not in packs,key
            packs[key]=base64.b64decode(json.loads(match[2])[1],validate=True)
    assert set(packs)=={r['path'] for r in m['source_files']}
    for r in m['source_files']: assert packs[r['path']]==original(r),r['path']
    dist={r['path']:original(r) for r in m['viewer_dist']}
    html=(a.folder/'Office_Realistic_Tour.html').read_text()
    inline='<script type="module">\n'+dist['app.js'].decode().replace('</script','<\\/script')+'\n</script>'
    assert html.count(inline)==1,'inline viewer differs from source'
    prefix,suffix=dist['index.html'].decode().split('<script type="module" src="./app.js"></script>')
    assert html.startswith(prefix) and html.endswith(suffix),'page differs outside offline bootstrap'
    assert packs['release-config.json']==dist['release-config.json']
    config=json.loads(packs['release-config.json'])
    assert config['releaseZones']==['Z02','Z08','Z30','Z12','Z07','Z18']
    for r in m['render_files']: assert (a.folder/r['path']).read_bytes()==original(r),r['path']
    for r in m['package_files']:
        data=(a.folder/r['path']).read_bytes()
        assert len(data)==r['bytes'] and digest(data)==r['sha256'],r['path']
    expected={r['path'] for r in m['package_files']}|{'offline-manifest.json'}
    with zipfile.ZipFile(a.archive) as z:
        names={n.split('/',1)[1]:n for n in z.namelist() if not n.endswith('/')}
        assert set(names)==expected,'ZIP contents differ from manifest'
        for name in expected: assert z.read(names[name])==(a.folder/name).read_bytes(),name
    report={'status':'passed','source_commit':source,'packed_assets':len(packs),'viewer_dist':m['viewer_dist'],
        'render_files':len(m['render_files']),'package_files':len(m['package_files']),
        'release_zones':config['releaseZones'],'archive_sha256':digest(a.archive.read_bytes()),
        'archive_bytes':a.archive.stat().st_size,'inline_app_exact':True,'zip_roundtrip_exact':True}
    a.output.write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report))

if __name__=='__main__':main()
