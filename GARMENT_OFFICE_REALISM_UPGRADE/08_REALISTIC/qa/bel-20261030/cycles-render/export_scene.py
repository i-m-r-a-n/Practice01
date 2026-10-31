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
  // instanced meshes with per-instance colours (leaves, cutting-waste offcuts): Blender's importer drops instance colours, so bake
  // them into one plain mesh with vertex colours (glTF COLOR_0 multiplies the base colour, as instanceColor does in three.js)
  const baked = [];
  scene.traverseVisible(o => { if (o.isInstancedMesh && o.instanceColor && o.count > 0) baked.push(o); });
  const added = [];
  for (const o of baked) {
    const src = o.geometry.index ? o.geometry.toNonIndexed() : o.geometry, P = src.attributes.position, N = src.attributes.normal, U = src.attributes.uv, vc = P.count, n = o.count;
    const pos = new Float32Array(vc * n * 3), nor = N ? new Float32Array(vc * n * 3) : null, uv = U ? new Float32Array(vc * n * 2) : null, col = new Float32Array(vc * n * 3);
    const m4 = new THREE.Matrix4(), nm = new THREE.Matrix3(), c = new THREE.Color(), v = new THREE.Vector3();
    for (let i = 0; i < n; i++) {
      o.getMatrixAt(i, m4); o.getColorAt(i, c); nm.getNormalMatrix(m4);
      for (let j = 0; j < vc; j++) {
        const k = i * vc + j;
        v.fromBufferAttribute(P, j).applyMatrix4(m4); pos[k * 3] = v.x; pos[k * 3 + 1] = v.y; pos[k * 3 + 2] = v.z;
        if (nor) { v.fromBufferAttribute(N, j).applyMatrix3(nm).normalize(); nor[k * 3] = v.x; nor[k * 3 + 1] = v.y; nor[k * 3 + 2] = v.z; }
        if (uv) { uv[k * 2] = U.getX(j); uv[k * 2 + 1] = U.getY(j); }
        col[k * 3] = c.r; col[k * 3 + 1] = c.g; col[k * 3 + 2] = c.b;
      }
    }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    if (nor) g.setAttribute('normal', new THREE.BufferAttribute(nor, 3)); if (uv) g.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
    g.setAttribute('color', new THREE.BufferAttribute(col, 3));
    const mat = o.material.clone(); mat.vertexColors = true;
    const mesh = new THREE.Mesh(g, mat); mesh.name = (o.name || o.material.name || 'instanced') + '_baked';
    o.matrix.decompose(mesh.position, mesh.quaternion, mesh.scale); o.parent.add(mesh); o.visible = false; added.push([o, mesh]);
  }
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
  added.forEach(([o, mesh]) => { mesh.parent.remove(mesh); mesh.geometry.dispose(); mesh.material.dispose(); o.visible = true; });
  const blob = new Blob([glb], { type: 'model/gltf-binary' });
  const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'scene_' + camName + '.glb'; document.body.appendChild(a); a.click();
  return { ...info, meshes, bytes: glb.byteLength, seconds: (performance.now() - t0) / 1000, stripped: [...new Set(stripped.map(x => x[1]))], baked: added.map(([o]) => (o.material.name || o.name) + ':' + o.count), skipped: bad.map(o => (o.name || o.parent?.name || o.type) + ':' + (o.geometry.index ? o.geometry.index.count : 0) + '/' + o.geometry.attributes.position.count + (Number.isFinite(o.geometry.drawRange.count) ? ' dr' + o.geometry.drawRange.count : '')) };
}
"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    ctx = b.new_context(viewport={'width': 1920, 'height': 1080}, accept_downloads=True)
    page = ctx.new_page(); errs = []
    page.on('pageerror', lambda e: errs.append(str(e)[:300]))
    page.on('console', lambda m: errs.append('console ' + m.text[:200]) if m.type == 'error' else None)
    import os
    page.goto(f"http://127.0.0.1:{os.environ.get('PORT', '8790')}/stage2-concept/?welcome=0&debug=1", wait_until='domcontentloaded', timeout=60000)
    page.wait_for_function('window.__viewer?.ready && __viewer.dressing && __viewer.dressing.concept', timeout=300000)
    page.evaluate('n => __viewer.api.frameCamera(n)', CAM); page.wait_for_timeout(4000)
    page.screenshot(path=str(OUT / f'webgl_{CAM}.png'))
    with page.expect_download(timeout=1800000) as d:
        info = page.evaluate(JS, [exporter_src, utils_src, CAM])
    d.value.save_as(str(OUT / f'scene_{CAM}.glb'))
    R = Path('/home/user/bel/GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC')
    ref = {x['name']: x for x in json.loads((R / 'viewer/bel-config.json').read_text())['extraCameras']}
    ref.update({x['name']: x for x in json.loads((R / 'revised-model/office_web_metadata.json').read_text())['cameras'] if x['name'] not in ref})
    c = ref.get(CAM, {})
    info['ref'] = {k: c.get(k) for k in ('type', 'lens', 'sensor_width', 'sensor_fit', 'shift_x', 'shift_y', 'ortho_scale', 'clip')}
    info['ref']['width'], info['ref']['height'] = (c.get('render') or {}).get('width', 1920), (c.get('render') or {}).get('height', 1080)
    (OUT / f'camera_{CAM}.json').write_text(json.dumps(info, indent=1))
    print(json.dumps(info)); print('errors:', errs[:8])
    b.close()
