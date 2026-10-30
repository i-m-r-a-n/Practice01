"""Build a double-clickable offline folder without data-URL size limits.

Runtime binary assets are split into ordinary local JS resource packs. Fetches
resolve to lazy Blob-backed Responses; screenshots remain ordinary local JPGs.
The generated package must still pass file:// browser QA before delivery.
Usage: python build_offline.py /absolute/output/folder
"""
from pathlib import Path
import argparse, base64, hashlib, json, mimetypes, re, shutil, subprocess, sys

HERE=Path(__file__).resolve().parent
REAL=HERE.parent
REPO=REAL.parents[1]
p=argparse.ArgumentParser()
p.add_argument('output',type=Path)
p.add_argument('--source-commit',help='Pin and verify all bundled inputs against this Git commit')
args=p.parse_args()
if args.source_commit and not re.fullmatch(r'[0-9a-f]{40}',args.source_commit):p.error('source-commit must be a full SHA')
OUT=args.output.resolve()
OUT.mkdir(parents=True,exist_ok=True)
def source_record(path, name):
    data=path.read_bytes()
    relative=path.relative_to(REPO).as_posix()
    if args.source_commit:
        expected=subprocess.check_output(['git','show',args.source_commit+':'+relative],cwd=REPO)
        if data!=expected:raise ValueError('Input differs from pinned source: '+relative)
    return {'path':name,'source_path':relative,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
bundle=REAL/'viewer/dist'
viewer_dist=[source_record(bundle/name,name) for name in ['index.html','app.js','release-config.json']]
html=(bundle/'index.html').read_text()
app=(bundle/'app.js').read_text().replace('</script','<\\/script')
hybrid=(REAL/'lighting-v2/manifest-hybrid.json').exists()
model_name='model_web_baked.glb' if hybrid else 'model_web.glb'
model_path='GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/revised-model/Optimized_Office_Interior_web_baked.glb' if hybrid else 'GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/Final_Office_Interior_web.glb'
assets={model_name:REPO/model_path}
lighting_folder='lighting-v2' if (REAL/'lighting-v2/manifest.json').exists() else 'lighting'
manifest_rel=lighting_folder+('/manifest-hybrid.json' if hybrid else '/manifest.json')
lighting=json.loads((REAL/manifest_rel).read_text())
assets[manifest_rel]=REAL/manifest_rel
for room in lighting['rooms']:
    names=[room['glb'],room['lightMap']['url']]
    if room['lightMap'].get('fallbackUrl'):names.append(room['lightMap']['fallbackUrl'])
    for name in names:
        rel=lighting_folder+'/'+name;assets[rel]=REAL/rel
release=json.loads((REAL/'viewer/dist/release-config.json').read_text())
assets['release-config.json']=REAL/'viewer/dist/release-config.json'
people_rel='people/'+release.get('peopleManifest','reception/people-manifest.json')
people_manifest=json.loads((REAL/people_rel).read_text())
assets[people_rel]=REAL/people_rel
for name in [people_manifest.get('poses','poses.json')]+[v['file'] for v in people_manifest['assets'].values()]:
    rel='people/'+name;assets[rel]=REAL/rel
assets['props/office-props-manifest.json']=REAL/'props/office-props-manifest.json'
# Release finish refinements fetch textures directly from the shipped bundle,
# outside the lighting and people manifests (e.g. the six-room terrazzo albedo).
# Include those exact inputs, without pulling in unused full-phase PBR sets.
for rel in sorted(set(re.findall(r'''["']\./(textures/[^"']+\.(?:ktx2|png|jpg|webp|json))["']''',app))):
    assets[rel]=REAL/rel
for folder in ['textures/codecs']:
    for p in (REAL/folder).rglob('*'):
        if not p.is_file(): continue
        rel=p.relative_to(REAL).as_posix()
        if any(v in p.relative_to(REAL).parts for v in ['qa','source','sources','smoke','review','node_modules','__pycache__']): continue
        if 'reception' in p.relative_to(REAL).parts and p.suffix.lower() in ['.png','.jpg']: continue
        if p.suffix.lower() not in ['.glb','.bin','.ktx2','.wasm','.js','.json','.exr','.hdr','.png','.jpg','.webp']: continue
        if p.suffix=='.exr' and p.with_suffix('.ktx2').exists(): continue
        assets[rel]=p
manifest=[]; packs=[]; text=''; total=0
for name,p in sorted(assets.items()):
    data=p.read_bytes(); total+=len(data)
    mime={'.glb':'model/gltf-binary','.ktx2':'image/ktx2','.wasm':'application/wasm','.exr':'image/x-exr'}.get(p.suffix,mimetypes.guess_type(p.name)[0] or 'application/octet-stream')
    line='window.__OFFLINE_ASSETS['+json.dumps(name)+']=['+json.dumps(mime)+','+json.dumps(base64.b64encode(data).decode())+'];\n'
    if text and len(text)+len(line)>24*1024*1024:
        target=f'asset-pack-{len(packs):03}.js';(OUT/target).write_text(text);packs.append(target);text=''
    text+=line
    manifest.append(source_record(p,name))
if text:
    target=f'asset-pack-{len(packs):03}.js';(OUT/target).write_text(text);packs.append(target)
bootstrap=r'''<script>
window.__OFFLINE_ASSETS=Object.create(null);
</script>
__PACKS__
<script>
(()=>{
 const assets=window.__OFFLINE_ASSETS, originalFetch=window.fetch.bind(window);
 const base=new URL('.',location.href).href;
 window.__OFFLINE_STATS={requests:0,decodedBytes:0,missing:[]};
 window.fetch=async(input,init)=>{
  const raw=typeof input==='string'?input:input instanceof URL?input.href:input.url;
  const url=new URL(raw,location.href);
  let key=url.href.startsWith(base)?decodeURIComponent(url.href.slice(base.length).split('?')[0]):null;
  if(key&&assets[key]){
   const item=assets[key];
   window.__OFFLINE_STATS.requests++;
   if(typeof item[1]==='string'){
    const s=atob(item[1]),bytes=new Uint8Array(s.length);
    for(let i=0;i<s.length;i++)bytes[i]=s.charCodeAt(i);
    item[1]=new Blob([bytes],{type:item[0]});
    window.__OFFLINE_STATS.decodedBytes+=bytes.byteLength;
   }
   return new Response(item[1],{status:200,headers:{'Content-Type':item[0]}});
  }
  if(url.protocol==='file:')window.__OFFLINE_STATS.missing.push(key||url.pathname);
  return originalFetch(input,init);
 };
 window.__TOUR_CONFIG=Object.assign({},window.__TOUR_CONFIG,{models:['./__MODEL__'],renders:'./renders/',lightmapManifest:'./__MANIFEST__'});
})();
</script>'''.replace('__PACKS__','\n'.join(f'<script src="./{p}"></script>' for p in packs)).replace('__MODEL__',model_name).replace('__MANIFEST__',manifest_rel)
tag='<script type="module" src="./app.js"></script>'
assert tag in html,'expected built module script not found'
html=html.replace(tag,bootstrap+'\n<script type="module">\n'+app+'\n</script>')
(OUT/'Office_Realistic_Tour.html').write_text(html)
renderdir=REPO/'GARMENT_OFFICE_FINAL_PRESENTATION/02_RENDERED_IMAGES/final'
(OUT/'renders').mkdir(exist_ok=True)
meta=json.loads((REAL/'revised-model/office_web_metadata.json').read_text())
render_files=[]
for c in meta['cameras']:
    p=REAL/'revised-model/renders'/(c['name']+'.jpg')
    if not p.exists():p=renderdir/(c['name']+'.jpg')
    if not p.exists() and c['name'].endswith('Z06_Z07'):continue   # plan / cutaway of the redesign: no still in the tour
    assert p.exists(),p
    render_files.append(source_record(p,'renders/'+p.name))
    shutil.copyfile(p,OUT/'renders'/p.name)
license_paths=[
    REAL/'viewer/vendor/three/LICENSE',REAL/'textures/LICENSES.md',
    REAL/'people/LICENSES.md',REAL/'people/source/LICENSE.ASSETS.md',REAL/'props/LICENSES.md',
    REPO/'GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/assets/LICENSES.md',
]
license_paths+=sorted((REAL/'textures/codecs/third_party_licenses').glob('*'))
for p in license_paths:
    if not p.is_file():raise FileNotFoundError(f'Required licence missing: {p}')
    relative=p.relative_to(REPO)
    source_record(p,relative.as_posix())
    target=OUT/'licenses'/relative
    target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
(OUT/'READ_ME.txt').write_text('OFFICE REALISTIC TOUR — OFFLINE\n\nExtract the entire folder, then double-click Office_Realistic_Tour.html.\nKeep the asset-pack files and renders folder beside it. No server is needed by the package.\n\nPeople shown are illustrative.\nProposed interior visualization. Final dimensions and technical details subject to site verification.\n\nThis package uses local JavaScript packs and Blob-backed fetch responses, not oversized data URLs.\nLicence notices and asset provenance are retained in the licenses folder.\nPhysical MacBook Firefox/Chrome/Safari performance requires separate validation; do not infer it from Linux software-GPU tests.\nThe managed test browser blocked file:// navigation by administrator policy; local double-click opening still needs verification on the target Mac.\n')
readme=OUT/'READ_ME.txt'
readme.write_text(readme.read_text().replace('The managed test browser blocked file:// navigation by administrator policy; local double-click opening still needs verification on the target Mac.','See the accompanying package QA for the browsers actually tested; direct opening on the target Mac remains unverified.'))
package_files=[{'path':f.relative_to(OUT).as_posix(),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(OUT.rglob('*')) if f.is_file() and f.name!='offline-manifest.json']
(OUT/'offline-manifest.json').write_text(json.dumps({'source_commit':args.source_commit,'viewer_dist':viewer_dist,'source_files':manifest,'source_bytes':total,'resource_packs':packs,'render_files':render_files,'camera_renders':len(render_files),'package_files':package_files,'status':'Built package; see external file-protocol QA before claiming acceptance.'},indent=2)+'\n')
print(json.dumps({'output':str(OUT),'assets':len(assets),'source_bytes':total,'packs':len(packs),'renders':len(render_files),'source_commit':args.source_commit}))
