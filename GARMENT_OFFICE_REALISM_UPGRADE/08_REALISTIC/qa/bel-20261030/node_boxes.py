"""Bounding boxes of approved model nodes by name prefix, read from the real scene of a local route (debug=1 build hook;
LOCAL Chromium, read-only). Hidden nodes are measured too. For each prefix: the union box and, per material, its own box.
python3 -I node_boxes.py F022_ F017_ ... [--url URL]"""
import argparse, json
from playwright.sync_api import sync_playwright

p = argparse.ArgumentParser()
p.add_argument('prefixes', nargs='+')
p.add_argument('--url', default='http://127.0.0.1:8790/realistic/?welcome=0&debug=1')
a = p.parse_args()
JS = """prefixes => { const { scene, THREE } = window.__dbg(); scene.updateMatrixWorld(true); const out = {};
  const r4 = v => +v.toFixed(4), box = b => [b.min.x, b.min.y, b.min.z, b.max.x, b.max.y, b.max.z].map(r4);
  for (const pre of prefixes) {
    const all = new THREE.Box3(), mats = {}; let n = 0;
    scene.traverse(o => { if (!o.isMesh) return; let hit = false; for (let q = o; q; q = q.parent) if ((q.name || '').startsWith(pre)) { hit = true; break; }
      if (!hit) return; n++; const b = new THREE.Box3().setFromObject(o); all.union(b);
      for (const m of (Array.isArray(o.material) ? o.material : [o.material])) { const k = m?.name || '?'; (mats[k] ||= new THREE.Box3()).union(b); } });
    out[pre] = { meshes: n, box: n ? box(all) : null, materials: Object.fromEntries(Object.entries(mats).map(([k, b]) => [k, box(b)])) };
  }
  return out; }"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    page = b.new_page(viewport={'width': 800, 'height': 500})
    page.goto(a.url, wait_until='domcontentloaded', timeout=60000)
    page.wait_for_function('window.__viewer?.ready', timeout=180000)
    print(json.dumps(page.evaluate(JS, a.prefixes), indent=1))
    b.close()
