"""Writes viewer/option-a-ledger.json: the relocation ledger of the Bengal Earth Lab option A rooms (Claude, 30 Oct 2026).

Option A (full conversion) gives Merchandising Z07 to the Green Uthan and the buyer room-sets, and the Accounts suite in
Z06 to the design academy. Before anything is drawn there, this lists every approved item in those rooms from the model:
what the /bengal-earth-lab/ route hides (it moves with its team, off this floor, by the owner's decision) and what stays
(walls, glass partitions, doors, fire safety, air conditioning and lighting). The approved model is never changed.
It also gives the walk-grid cells the hidden furniture blocked, so walk mode does not stop at furniture that is not shown.
Run: python3 -I make_option_a_ledger.py"""
import base64, json, math, re, struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODEL = HERE.parent / 'revised-model'
glb = (MODEL / 'Optimized_Office_Interior_web_baked.glb').read_bytes()
gl = json.loads(glb[20:20 + struct.unpack('<I', glb[12:16])[0]])
meta = json.loads((MODEL / 'office_web_metadata.json').read_text())
grid = json.loads((MODEL / 'walk_grid.json').read_text())

# what the approved items are, by node number (names as in the model); every one listed here is hidden on the route
MOVES = {
    'Z07': [
        ('F237 F246', '16 merchandising workstations (2 benches of 8)'),
        ('F238 F239 F240 F241 F242 F243 F244 F245 F247 F248 F249 F250 F251 F252 F253 F254', '16 task chairs'),
        ('F313 F314', 'desk accessories on the two benches'),
        ('F255 F256', '2 low swatch shelves'),
        ('F257 F258', 'sample approval counter and approval board'),
        ('F259 F260', '2 tall sample cabinets'),
        ('F261', 'multifunction printer'),
        ('F262 F317', 'dispatch counter and its accessories'),
        ('F263 F264', '2 garment rails'),
        ('F265 F266 F267', '2 dress forms and a full-length mirror'),
        ('F268', 'inspection table'),
        ('F269 F270 F271 F272 F273 F274 F275 F318', 'team review table with 6 chairs and its accessories'),
        ('F276 F277', '2 wall screens (65 in and 55 in)'),
        ('F278', 'staff lockers (8)'),
        ('F279 F280', '2 low storage units on the east wall'),
        ('F282 F283 PL282 PL283 PL246', '2 floor planters and a desk plant'),
        ('LT131 LT132 LT133 LT134 LT135', '5 linear pendants over the desks and tables (the lighting designer re-plans them)'),
    ],
    'Z06': [
        ('F284 F291', '12 finance workstations (2 benches of 6)'),
        ('F285 F286 F287 F288 F289 F290 F292 F293 F294 F295 F296 F297', '12 task chairs'),
        ('F315 F316', 'desk accessories on the two benches'),
        ('F298 F299 F319', "manager's desk, chair and accessories"),
        ('F300 F301 F302', '3 runs of filing cabinets (finance records)'),
        ('F303 F304 F320', 'document counter, multifunction printer and accessories'),
        ('F305 F306 F307 F308 F309 F321', 'finance discussion room: round table, 4 chairs and accessories'),
        ('F310', 'tall cabinet in the discussion room'),
    ],
}
STAYS = {
    'Z07': [('F231 F281', '2 fire extinguishers'), ('AC01 AC02 AC03 AC04', '4 air-conditioning units'), ('SD05 SD06', '2 smoke detectors'),
            ('LT136 LT137 LT138 LT139 LT140 LT141 LT142', '7 downlights'), ('', 'walls, the glass above 1.22 m to the hallway and Z06, interior glass W02 and W03, door D49 and the opening to the hallway')],
    'Z06': [('F235 F312', '2 fire extinguishers'), ('F311', 'archive cabinet in the north corridor (stays where it is; the owner decides whether the finance archive moves)'),
            ('AC05 AC06', '2 air-conditioning units'), ('SD07', 'smoke detector'), ('LT143 LT144 LT145 LT146 LT147', '5 linear pendants (they light the class tables)'),
            ('LT148 LT149 LT150 LT151 LT152 LT153 LT154 LT155 LT156 LT157 LT158 LT159 LT160', '13 downlights'),
            ('NP34 NP35 NP36 NP37 NP38 NP39 D50 D51 D52', 'every glass partition and door of the accounts suite and the discussion room'),
            ('', 'the public corridor to the washrooms and female prayer room, and the north corridor to the hallway (kept clear)')],
}

parent = {c: i for i, n in enumerate(gl['nodes']) for c in n.get('children', [])}


def local(n):
    if 'matrix' in n:
        m = n['matrix']; return [[m[c * 4 + r] for c in range(4)] for r in range(4)]
    t, (x, y, z, w), s = n.get('translation', [0, 0, 0]), n.get('rotation', [0, 0, 0, 1]), n.get('scale', [1, 1, 1])
    r = [[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)], [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)], [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]]
    return [[r[i][0] * s[0], r[i][1] * s[1], r[i][2] * s[2], t[i]] for i in range(3)] + [[0, 0, 0, 1]]


def world(i):
    m = local(gl['nodes'][i])
    while i in parent:
        i = parent[i]; a = local(gl['nodes'][i]); m = [[sum(a[r][k] * m[k][c] for k in range(4)) for c in range(4)] for r in range(4)]
    return m


def bbox(i):
    m, lo, hi = world(i), [1e9] * 3, [-1e9] * 3
    for p in gl['meshes'][gl['nodes'][i]['mesh']]['primitives']:
        acc = gl['accessors'][p['attributes']['POSITION']]; a, b = acc['min'], acc['max']
        if acc.get('normalized'):
            d = {5120: 127, 5121: 255, 5122: 32767, 5123: 65535}[acc['componentType']]; a, b = [v / d for v in a], [v / d for v in b]
        for c in [(x, y, z) for x in (a[0], b[0]) for y in (a[1], b[1]) for z in (a[2], b[2])]:
            v = [sum(m[r][k] * u for k, u in enumerate((*c, 1))) for r in range(3)]
            lo = [min(lo[k], v[k]) for k in range(3)]; hi = [max(hi[k], v[k]) for k in range(3)]
    return lo, hi


nodes = {}   # node number (F237, PL246, LT131, ...) -> [(name, lo, hi)]
for i, n in enumerate(gl['nodes']):
    m = re.match(r'([A-Z]+\d+) ', n.get('name', ''))
    if m and 'mesh' in n:
        nodes.setdefault(m.group(1), []).append((n['name'],) + bbox(i))


def entry(ids, what, zone):
    found = [k for k in ids.split()]
    missing = [k for k in found if k not in nodes]
    assert not missing, f'not in the model: {missing}'
    parts = [p for k in found for p in nodes[k]]
    lo = [min(p[1][a] for p in parts) for a in range(3)]; hi = [max(p[2][a] for p in parts) for a in range(3)]
    return {'zone': zone, 'what': what, 'nodes': found, 'names': sorted({p[0] for p in parts}),
            'bbox': {'min': [round(v, 3) for v in lo], 'max': [round(v, 3) for v in hi]},
            'parts': [{'name': p[0], 'min': [round(v, 3) for v in p[1]], 'max': [round(v, 3) for v in p[2]]} for p in parts]}


moves = [entry(ids, what, z) for z, rows in MOVES.items() for ids, what in rows]
stays = [dict(entry(ids, what, z), parts=None) if ids else {'zone': z, 'what': what, 'nodes': []} for z, rows in STAYS.items() for ids, what in rows]
for s in stays: s.pop('parts', None)

# the hidden furniture still blocks the approved walk grid: release the cells it alone blocked, never cells near a wall,
# a glass partition or a kept item (the walker radius plus one cell)
R = grid['walker_radius_m'] + grid['res']
polys = {r['zone']: r['polygon_xz'] for r in meta['rooms']}
segments = []
for z in MOVES:
    p = polys[z]; segments += [(p[i], p[(i + 1) % len(p)]) for i in range(len(p))]
for k in 'NP34 NP35 NP36 NP37 NP38 NP39'.split():           # glass partitions: thin boxes -> centre lines
    for name, lo, hi in nodes[k]:
        if 'manifestation' in name: continue
        if hi[0] - lo[0] < hi[2] - lo[2]: x = (lo[0] + hi[0]) / 2; segments.append(((x, lo[2]), (x, hi[2])))
        else: z = (lo[2] + hi[2]) / 2; segments.append(((lo[0], z), (hi[0], z)))
kept = [(lo, hi) for s in stays for k in s['nodes'] for name, lo, hi in nodes[k] if hi[1] > .1 and lo[1] < 1.9]   # kept items inside the walker's slab
# the steel columns are merged into the shell, so they come from the survey (GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/
# scripts/survey.py COLUMNS, plan inches, 10 in square; viewer x = 0.0254 x, z = 0.0254 y)
COLUMNS_IN = [(300, -217), (300, -423), (300, -633), (300, -843), (616, -217), (616, -423), (616, -633), (616, -843), (1101, -423), (1101, -633), (1101, -843)]
half = 5 * .0254
kept += [([x * .0254 - half, 0, y * .0254 - half], [x * .0254 + half, 2.9, y * .0254 + half]) for x, y in COLUMNS_IN]


def seg_dist(px, pz, a, b):
    (ax, az), (bx, bz) = a, b; dx, dz = bx - ax, bz - az; L = dx * dx + dz * dz
    t = 0 if L == 0 else max(0, min(1, ((px - ax) * dx + (pz - az) * dz) / L))
    return math.hypot(px - ax - t * dx, pz - az - t * dz)


def inside(poly, x, z):
    ok = False
    for i in range(len(poly)):
        (x1, z1), (x2, z2) = poly[i], poly[(i + 1) % len(poly)]
        if (z1 > z) != (z2 > z) and x < (x2 - x1) * (z - z1) / (z2 - z1) + x1: ok = not ok
    return ok


bits = base64.b64decode(grid['blocked_bits_base64']); ox, oz, res, cols = grid['origin_xz'][0], grid['origin_xz'][1], grid['res'], grid['cols']
grown = [(p['min'], p['max']) for m in moves for p in m['parts'] if p['max'][1] > .1 and p['min'][1] < 1.9]
runs, released = [], 0
for row in range(grid['rows']):
    cz = oz + (row + .5) * res; run = None
    for col in range(cols):
        cx = ox + (col + .5) * res; i = row * cols + col; ok = False
        if (bits[i >> 3] >> (i & 7)) & 1 and any(inside(polys[z], cx, cz) for z in MOVES):
            ok = (any(lo[0] - R <= cx <= hi[0] + R and lo[2] - R <= cz <= hi[2] + R for lo, hi in grown)
                  and all(seg_dist(cx, cz, a, b) >= R for a, b in segments)
                  and not any(lo[0] - R <= cx <= hi[0] + R and lo[2] - R <= cz <= hi[2] + R for lo, hi in kept))
        if ok:
            released += 1; run = [row, col, col] if run is None else [row, run[1], col]
        elif run: runs.append(run); run = None
    if run: runs.append(run)

ledger = {
    'title': 'Bengal Earth Lab, option A: relocation ledger for Merchandising Z07 and the Accounts suite Z06',
    'scope': 'Proposal route /bengal-earth-lab/ only. The approved model and the other routes are unchanged. Nothing moves until the owner decides on option A and a new home for both teams is agreed.',
    'source': 'revised-model/Optimized_Office_Interior_web_baked.glb (approved Stage II model), world boxes in viewer metres (x east, y up, z south)',
    'moves_off_this_floor': moves, 'stays': stays,
    'walk_release': {'note': 'Walk-grid cells blocked only by the hidden furniture: [row, first column, last column], inclusive. Cells within the walker radius plus one cell of a wall, glass partition or kept item stay blocked.',
                     'cells': released, 'runs': runs},
}
out = HERE / 'option-a-ledger.json'
out.write_text(json.dumps(ledger, indent=1) + '\n')

# the same ledger for people: qa/bel-20261030/OPTION_A_RELOCATION_LEDGER.md
ROOM = {'Z07': 'Merchandising Z07 (132.0 m²)', 'Z06': 'Accounts suite in Z06 (119.2 m² room)'}
md = ['# Bengal Earth Lab, option A: relocation ledger', '',
      'Generated by `viewer/make_option_a_ledger.py` from the approved model; the data file is `viewer/option-a-ledger.json`.', '',
      '**Option A only.** The `/bengal-earth-lab/` route shows the Green Uthan and room-sets in Merchandising and the design academy in the accounts suite.',
      'That needs both teams to move off this floor, so it is the owner\'s decision. Nothing moves until a new home for both teams is agreed.',
      'The approved model and the other routes are unchanged: the route only hides these items.', '']
for z in MOVES:
    md += [f'## {ROOM[z]}', '', '### Moves with its team (hidden on the route)', '', '| Item | Model nodes | Footprint (x, z in m) |', '|---|---|---|']
    for m in moves:
        if m['zone'] == z:
            lo, hi = m['bbox']['min'], m['bbox']['max']
            md.append(f"| {m['what']} | {', '.join(m['nodes'])} | x {lo[0]:.2f} to {hi[0]:.2f}, z {lo[2]:.2f} to {hi[2]:.2f} |")
    md += ['', '### Stays as approved', '']
    md += [f"- {s['what']}" + (f" ({', '.join(s['nodes'])})" if s['nodes'] else '') for s in stays if s['zone'] == z]
    md.append('')
md += ['## Walk mode', '', f"{released} walk-grid cells (0.1 m) were blocked only by the hidden furniture and are released on the route. Cells within",
       f"{R:.2f} m (walker radius plus one cell) of a wall, glass partition, steel column or kept item stay blocked. The new furniture",
       'reports its own footprint, so walkers stop at it.', '',
       '## Still to decide (owner)', '',
       '- Where the merchandising team (16 desks, sample approval, dispatch, rails, lockers) and the accounts team (12 desks, manager, records, discussion room) go.',
       '- Whether the finance archive cabinet in the north corridor moves with the accounts team.',
       '- The lighting plan for both rooms once the desk pendants in Merchandising are removed.', '']
(HERE.parent / 'qa' / 'bel-20261030' / 'OPTION_A_RELOCATION_LEDGER.md').write_text('\n'.join(md))
print(out, len(moves), 'groups move,', sum(len(m['nodes']) for m in moves), 'nodes;', len(stays), 'groups stay;', released, 'walk cells released in', len(runs), 'runs')
