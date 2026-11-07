"""Woven Earth (the owner's entrance brief, 7 Nov 2026) on the proposal route, checked in the running page (?debug=1):
  1. the arrival gallery (Z01) and reception (Z02) hold exactly the brief's items, and none of the retired ones
  2. the woven threshold keeps its headroom (lowest point 2.30 m) and stays in its clear ceiling bay: east of the steel beam and the AC unit,
     west of the east glass, clear of the brand-wall spots, the linear lights and the smoke detector, below the deck
  3. the exit sign over the entrance stays in view from the route under the threshold (ray casts against the real scene)
  4. the bench and the stool block walking, and the route under the threshold, the way in and the space in front of the bench stay free
  5. the terracotta wall sits on the free west wall, the fibre display on the reception console, the three fittings carry their light
  6. no page errors
python3 -I woven_check.py OUT_DIR [BASE_URL]"""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
BASE = sys.argv[2] if len(sys.argv) > 2 else 'http://127.0.0.1:8790'
WANT = {'Z01': ['BEL_WOVEN_THRESHOLD', 'BEL_TERRACOTTA_SURFACE', 'BEL_RECLAIMED_BENCH', 'BEL_ARRIVAL_FIG'], 'Z02': ['BEL_RECEPTION_TREE', 'BEL_FIBRE_DISPLAY', 'BEL_TEA_CLAY']}
RETIRED = ['BEL_GATE_BONSAI', 'BEL_LOBBY_STONES', 'BEL_EARTH_DESK', 'BEL_LOBBY_RELIEF', 'BEL_RECEPTION_ALOE', 'BEL_INSTRUMENTS']
PROBE = r"""() => {
  const { scene, THREE } = window.__dbg(), box = new THREE.Box3(), tmp = new THREE.Box3();
  const under = (o, name) => { for (let p = o; p; p = p.parent) if (p.name === name) return true; return false; };
  const bounds = test => { box.makeEmpty(); let n = 0; scene.traverse(o => { if (o.isMesh && test(o)) { tmp.setFromObject(o); box.union(tmp); n++; } });
    return n ? { n, min: box.min.toArray().map(v => +v.toFixed(3)), max: box.max.toArray().map(v => +v.toFixed(3)) } : { n }; };
  const mat = o => (Array.isArray(o.material) ? o.material[0] : o.material)?.name || '';
  const canopy = new Set(['bel_we_swags', 'bel_we_lam_rail', 'bel_we_culm', 'bel_we_tape']);
  const out = {
    canopy: bounds(o => canopy.has(mat(o))),
    swags: bounds(o => mat(o) === 'bel_we_swags'),
    canopySteel: bounds(o => mat(o) === 'bel_we_steel' && !under(o, 'BEL_TERRACOTTA_SURFACE')),
    terracotta: bounds(o => under(o, 'BEL_TERRACOTTA_SURFACE') && mat(o).startsWith('bel_we_t')),
    bench: bounds(o => under(o, 'BEL_RECLAIMED_BENCH')),
    fibre: bounds(o => under(o, 'BEL_FIBRE_DISPLAY')),
    fig: bounds(o => under(o, 'BEL_ARRIVAL_FIG')),
    lights: [], exitSight: [],
  };
  scene.traverse(o => { if (o.userData?.light) { const p = new THREE.Vector3(); o.getWorldPosition(p); out.lights.push({ name: o.name, type: o.userData.light.type, at: p.toArray().map(v => +v.toFixed(3)) }); } });
  // the exit sign over the entrance (x 5.67-6.02, y 2.24-2.39, z 6.2): what a ray from each point on the route meets first
  const sign = new THREE.Vector3(5.845, 2.315, 6.19), ray = new THREE.Raycaster(), meshes = []; scene.traverse(o => { if (o.isMesh && o.visible) meshes.push(o); });
  for (const p of [[7.3, 1.6, 1.2], [6.9, 1.6, 2.0], [6.9, 1.6, 2.9], [6.8, 1.6, 3.6], [5.8, 1.6, 2.3]]) {
    const from = new THREE.Vector3(...p), dir = sign.clone().sub(from), dist = dir.length(); ray.set(from, dir.normalize()); ray.far = dist - .03;
    const hit = ray.intersectObjects(meshes, false).find(h => h.object.visible);
    out.exitSight.push({ from: p, clear: !hit, first: hit ? { material: mat(hit.object), name: hit.object.name, distance: +hit.distance.toFixed(2), of: +dist.toFixed(2) } : null });
  }
  return out;
}"""
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'])
    pg = b.new_page(viewport={'width': 1280, 'height': 720}); errs = []
    pg.on('pageerror', lambda e: errs.append('pageerror ' + str(e)[:300]))
    pg.on('console', lambda m: errs.append('console ' + m.text[:300]) if m.type == 'error' else None)
    pg.goto(BASE + '/stage2-concept/?welcome=0&debug=1', wait_until='domcontentloaded', timeout=60000)
    pg.wait_for_function('window.__viewer?.ready && __viewer.dressing && __viewer.dressing.concept', timeout=400000)
    items = pg.evaluate('() => __viewer.dressing.concept.items.map(i => [i.id, i.zone])')
    pg.evaluate("n => __viewer.api.frameCamera(n)", 'CAM_03_Entrance_Lobby'); pg.wait_for_function('!__viewer.api.state().flying', timeout=120000); pg.wait_for_timeout(3000)
    geo = pg.evaluate(PROBE)
    walk = {}
    for name, (x, z) in {'bench_seat': (.30, 1.40), 'bench_front': (.60, 1.40), 'stool': (.62, .30), 'fig': (7.115, 4.955),
                         'route_under_threshold_n': (6.9, 1.6), 'route_under_threshold_m': (6.9, 2.6), 'route_under_threshold_s': (6.95, 3.6),
                         'way_in': (6.3, 4.6), 'before_bench': (1.05, 1.4), 'between_bench_and_doors': (1.3, .45), 'reception_door': (7.3, .8)}.items():
        try: pg.evaluate('([x, z]) => __viewer.api.setWalkQAStart(x, z)', [x, z]); walk[name] = 'free'
        except Exception as e: walk[name] = 'blocked' if 'blocked' in str(e) else 'error: ' + str(e)[:120]
    pg.screenshot(path=str(OUT / 'woven_check_last.png'))
    b.close()

ids = {z: sorted(i for i, zz in items if zz == z) for z in WANT}
c, s, st = geo['canopy'], geo['swags'], geo['canopySteel']
checks = {
    'items_z01_z02_exactly_the_brief': all(ids[z] == sorted(WANT[z]) for z in WANT),
    'retired_items_absent': not any(i in RETIRED for i, _ in items),
    'threshold_built': c['n'] >= 3 and s['n'] >= 1,
    'lowest_point_at_least_2_30': s['n'] and s['min'][1] >= 2.299,
    'below_the_deck': c['n'] and c['max'][1] <= 2.896 and st['n'] and st['max'][1] <= 2.896,
    'east_of_beam_and_ac_unit': c['min'][0] >= 6.27 and st['min'][0] >= 6.17,                   # beam x 6.03-6.16, AC unit x 5.51-6.17
    'west_of_east_glass': c['max'][0] <= 7.55 and st['max'][0] <= 7.58,                          # bulkhead over the glass at x 7.62
    'clear_of_brand_wall_spots': c['min'][2] >= 1.2,                                             # spots at z 0.86-1.03
    'clear_of_linear_lights_and_detector': c['min'][0] - 5.37 >= .8 and c['min'][0] - 5.95 >= .3,  # pendants x 5.30-5.37; detector x 5.83-5.95, z 2.99-3.11
    'exit_sign_in_view_from_the_route': all(e['clear'] for e in geo['exitSight']),
    'bench_and_stool_block_walking': all(walk[k] == 'blocked' for k in ('bench_seat', 'bench_front', 'stool', 'fig')),
    'route_and_bench_approach_free': all(walk[k] == 'free' for k in ('route_under_threshold_n', 'route_under_threshold_m', 'route_under_threshold_s', 'way_in', 'before_bench', 'between_bench_and_doors', 'reception_door')),
    'terracotta_on_west_wall': geo['terracotta']['n'] > 0 and geo['terracotta']['max'][0] <= .07 and geo['terracotta']['min'][2] >= .25 and geo['terracotta']['max'][2] <= 2.47,
    'bench_off_the_route': geo['bench']['n'] > 0 and geo['bench']['max'][0] <= .9 and geo['bench']['max'][2] <= 2.3,
    'fibre_display_on_console': geo['fibre']['n'] > 0 and geo['fibre']['min'][0] >= 10.69 and geo['fibre']['max'][0] <= 12.53 and geo['fibre']['min'][2] >= .03 and geo['fibre']['max'][2] <= .45 and geo['fibre']['min'][1] >= .786,
    'three_fittings_carry_light': sorted(l['type'] for l in geo['lights']) == ['AREA', 'SPOT', 'SPOT'],
    'no_page_errors': not errs,
}
report = {'checks': checks, 'passed': all(checks.values()), 'items': ids, 'geometry': geo, 'walk': walk, 'errors': errs[:10]}
(OUT / 'woven-check.json').write_text(json.dumps(report, indent=1))
print(json.dumps({'passed': report['passed'], 'failed': [k for k, v in checks.items() if not v]}))
