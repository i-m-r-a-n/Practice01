"""Export the live-equivalent 3D scene of the proposal route (local build, overview camera) to GLB for a Cycles render.
Runs the page from serve_preview.py with ?debug=1 (window.__dbg gives the scene, THREE and camera), loads three.js r169's
own GLTFExporter (downloaded from jsDelivr, rewired to the page's THREE), adds a copy of the camera, and saves the GLB."""
import json, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

CAM = sys.argv[1] if len(sys.argv) > 1 else 'CAM_ISO_SE'
OUT = Path('/home/user/render_work/out'); DL = Path('/home/user/render_work/dl')
exporter_src = (DL / 'exporters/GLTFExporter.js').read_text()
utils_src = (DL / 'utils/TextureUtils.js').read_text()
JS = r"""
async ([exporterSrc, utilsSrc, camName]) => {
  const { scene, THREE, camera } = window.__dbg();
  window.__THREE_EXPORT = THREE;
  const names = Object.keys(THREE).filter(n => /^[A-Za-z_$][\w$]*$/.test(n));
  const shim = names.map(n => `export const ${n} = window.__THREE_EXPORT.${n};`).join('\n');
  const url = s => URL.createObjectURL(new Blob([s], { type: 'text/javascript' }));
  const shimUrl = url(shim);
  const utilsUrl = url(utilsSrc.replace(/from 'three'/g, `from '${shimUrl}'`));
  const expUrl = url(exporterSrc.replace(/from 'three'/g, `from '${shimUrl}'`).replace(`from './../utils/TextureUtils.js'`, `from '${utilsUrl}'`));
  const { GLTFExporter } = await import(expUrl);
  // lights: Blender gets its own; keep the scene's emissive surfaces
  const hidden = [], bad = [];
  scene.traverse(o => { if (o.isLight && o.visible) { o.visible = false; hidden.push(o); } });
  // geometry Blender's importer cannot read: indices past the vertex count (or a draw range cutting the buffer)
  scene.traverseVisible(o => {
    if (!o.isMesh || !o.geometry) return;
    const g = o.geometry, pos = g.attributes.position; if (!pos) return;
    let broken = g.drawRange && (g.drawRange.start > 0 || Number.isFinite(g.drawRange.count));
    if (g.index) { const a = g.index.array; let m = 0; for (let k = 0; k < a.length; k++) if (a[k] > m) m = a[k]; if (m >= pos.count) broken = true; }
    if (broken) bad.push(o);
  });
  bad.forEach(o => { o.visible = false; hidden.push(o); });
  // per-instance attributes (e.g. the room-probe row of instanced props) are not vertex data: leave them out of the file
  const stripped = [];
  scene.traverseVisible(o => {
    const g = o.geometry; if (!g || !g.attributes) return;
    for (const [k, a] of Object.entries(g.attributes)) if (a.isInstancedBufferAttribute || (g.attributes.position && a.count !== g.attributes.position.count)) { stripped.push([g, k, a]); g.deleteAttribute(k); }
  });
  const cam = camera.clone(); cam.name = 'VIEW_' + camName; cam.matrixAutoUpdate = true;
  camera.updateMatrixWorld(); cam.position.setFromMatrixPosition(camera.matrixWorld); cam.quaternion.setFromRotationMatrix(camera.matrixWorld);
  scene.add(cam); cam.updateMatrixWorld(true);
  const info = { fov: camera.fov, aspect: camera.aspect, near: camera.near, far: camera.far, pos: cam.position.toArray(), quat: cam.quaternion.toArray(), isPerspective: !!camera.isPerspectiveCamera };
  let meshes = 0; scene.traverseVisible(o => { if (o.isMesh) meshes++; });
  const t0 = performance.now();
  const glb = await new GLTFExporter().parseAsync(scene, { binary: true, onlyVisible: true, maxTextureSize: 1024 });
  scene.remove(cam); hidden.forEach(o => o.visible = true); stripped.forEach(([g, k, a]) => g.setAttribute(k, a));
  const blob = new Blob([glb], { type: 'model/gltf-binary' });
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'scene_' + camName + '.glb'; document.body.appendChild(a); a.click();
  return { ...info, meshes, bytes: glb.byteLength, seconds: (performance.now() - t0) / 1000, stripped: [...new Set(stripped.map(x => x[1]))], skipped: bad.map(o => (o.name || o.parent?.name || o.type) + ':' + (o.geometry.index ? o.geometry.index.count : 0) + '/' + o.geometry.attributes.position.count + (Number.isFinite(o.geometry.drawRange.count) ? ' dr' + o.geometry.drawRange.count : '')) };
}
"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    ctx = b.new_context(viewport={'width': 1920, 'height': 1080}, accept_downloads=True)
    page = ctx.new_page(); errs = []
    page.on('pageerror', lambda e: errs.append(str(e)[:300]))
    page.on('console', lambda m: errs.append('console ' + m.text[:200]) if m.type == 'error' else None)
    page.goto('http://127.0.0.1:8790/stage2-concept/?welcome=0&debug=1', wait_until='domcontentloaded', timeout=60000)
    page.wait_for_function('window.__viewer?.ready && __viewer.dressing && __viewer.dressing.concept', timeout=300000)
    page.evaluate('n => __viewer.api.frameCamera(n)', CAM); page.wait_for_timeout(4000)
    page.screenshot(path=str(OUT / f'webgl_{CAM}.png'))
    with page.expect_download(timeout=1800000) as d:
        info = page.evaluate(JS, [exporter_src, utils_src, CAM])
    d.value.save_as(str(OUT / f'scene_{CAM}.glb'))
    (OUT / f'camera_{CAM}.json').write_text(json.dumps(info, indent=1))
    print(json.dumps(info)); print('errors:', errs[:8])
    b.close()
