"""Ray probes against the real scene of the /bengal-earth-lab/ route (debug=1 build hook; LOCAL Chromium, read-only).
Each probe: name, origin [x, y, z], direction [dx, dy, dz]. Reports the first hit on the approved model (concept items ignored).
python3 ray_probe.py --probes probes.json [--url URL]"""
import argparse, json
from playwright.sync_api import sync_playwright

p = argparse.ArgumentParser()
p.add_argument('--url', default='http://127.0.0.1:8790/bengal-earth-lab/?welcome=0&debug=1')
p.add_argument('--probes', required=True)
a = p.parse_args()
probes = json.load(open(a.probes))
JS = """probes => { const { scene, THREE } = window.__dbg(); const rc = new THREE.Raycaster(); rc.far = 20; const out = [];
  scene.updateMatrixWorld(true);
  const isConcept = o => { for (let n = o; n; n = n.parent) if (n.name === 'BENGAL_EARTH_LAB' || n.name === 'INTERIOR_DESIGN' || n.name === 'CLIENT_IDENTITY_PROPS') return true; return false; };
  for (const [name, o, d] of probes) {
    rc.set(new THREE.Vector3(...o), new THREE.Vector3(...d).normalize());
    const hit = rc.intersectObjects(scene.children, true).find(h => h.object.visible && !isConcept(h.object) && h.object.isMesh);
    out.push({ name, hit: hit ? hit.point.toArray().map(v => +v.toFixed(4)) : null, distance: hit ? +hit.distance.toFixed(4) : null, object: hit ? hit.object.name : null, material: hit ? (hit.object.material?.name || null) : null });
  }
  return out; }"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    page = b.new_page(viewport={'width': 800, 'height': 500})
    page.goto(a.url, wait_until='domcontentloaded', timeout=60000)
    page.wait_for_function('window.__viewer?.ready', timeout=180000)
    page.wait_for_function('__viewer.dressing && __viewer.dressing.concept', timeout=240000)
    for r in page.evaluate(JS, probes):
        print(json.dumps(r))
    b.close()
