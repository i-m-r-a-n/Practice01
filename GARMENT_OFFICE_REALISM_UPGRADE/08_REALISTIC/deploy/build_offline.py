"""Build a double-clickable offline folder without data-URL size limits.

Runtime binary assets are split into ordinary local JS resource packs. Fetches
resolve to lazy Blob-backed Responses; screenshots remain ordinary local JPGs.
The generated package must still pass file:// browser QA before delivery.
Usage: python build_offline.py /absolute/output/folder
"""
from pathlib import Path
import base64, hashlib, json, mimetypes, shutil, sys

HERE=Path(__file__).resolve().parent
REAL=HERE.parent
REPO=REAL.parents[1]
OUT=Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True,exist_ok=True)
bundle=REAL/'viewer/dist'
html=(bundle/'index.html').read_text()
app=(bundle/'app.js').read_text().replace('</script','<\\/script')
assets={'model_web.glb':REPO/'GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/Final_Office_Interior_web.glb'}
for folder in ['lighting','textures','people','props']:
    for p in (REAL/folder).rglob('*'):
        if not p.is_file(): continue
        rel=p.relative_to(REAL).as_posix()
        if any(v in p.relative_to(REAL).parts for v in ['qa','source','sources','smoke','node_modules','__pycache__']): continue
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
    manifest.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
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
 window.__TOUR_CONFIG=Object.assign({},window.__TOUR_CONFIG,{models:['./model_web.glb'],renders:'./renders/',lightmapManifest:'./lighting/manifest.json'});
})();
</script>'''.replace('__PACKS__','\n'.join(f'<script src="./{p}"></script>' for p in packs))
tag='<script type="module" src="./app.js"></script>'
assert tag in html,'expected built module script not found'
html=html.replace(tag,bootstrap+'\n<script type="module">\n'+app+'\n</script>')
(OUT/'Office_Realistic_Tour.html').write_text(html)
renderdir=REPO/'GARMENT_OFFICE_FINAL_PRESENTATION/02_RENDERED_IMAGES/final'
(OUT/'renders').mkdir(exist_ok=True)
meta=json.loads((REPO/'GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/office_web_metadata.json').read_text())
for c in meta['cameras']:
    p=renderdir/(c['name']+'.jpg');assert p.exists(),p
    shutil.copyfile(p,OUT/'renders'/p.name)
(OUT/'offline-manifest.json').write_text(json.dumps({'source_files':manifest,'source_bytes':total,'resource_packs':packs,'camera_renders':len(meta['cameras']),'status':'Built package; see external file-protocol QA before claiming acceptance.'},indent=2)+'\n')
(OUT/'READ_ME.txt').write_text('OFFICE REALISTIC TOUR — OFFLINE\n\nExtract the entire folder, then double-click Office_Realistic_Tour.html.\nKeep the asset-pack files and renders folder beside it. No server is needed.\n\nPeople shown are illustrative.\nProposed interior visualization. Final dimensions and technical details subject to site verification.\n\nThis package uses local JavaScript packs and Blob-backed fetch responses, not oversized data URLs.\nPhysical MacBook Firefox/Chrome/Safari performance requires separate validation; do not infer it from Linux software-GPU tests.\n')
print(json.dumps({'output':str(OUT),'assets':len(assets),'source_bytes':total,'packs':len(packs),'renders':len(meta['cameras'])}))
