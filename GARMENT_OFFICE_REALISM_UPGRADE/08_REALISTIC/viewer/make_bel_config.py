"""Writes viewer/bel-config.json, the configuration of the /bengal-earth-lab/ proposal route (Bengal Earth Lab,
"The Living Bengal Factory"). It starts from the /realistic/ release config and the approved props manifest, so the
items it hides and the drinkware it replaces always match the model. Run: python3 -I make_bel_config.py"""
import json, math
from pathlib import Path

HERE = Path(__file__).resolve().parent
base = json.loads((HERE / 'release-config.json').read_text())
manifest = json.loads((HERE.parent / 'props' / 'office-props-manifest.json').read_text())

RELEASE_ZONES = ['Z01', 'Z02', 'Z08', 'Z30', 'Z12', 'Z18']          # props (small office items) stay in these rooms
CONCEPT_ZONES = ['Z01', 'Z02', 'Z03', 'Z30', 'Z08', 'Z12', 'Z18']    # rooms with Bengal Earth Lab items in this increment
DRINK = {'glass', 'jug', 'teacup', 'tray', 'mug', 'bottle'}
TEA_SET = {'PROP_0006', 'PROP_0008'}                                 # reception tray and teacup: replaced by the clay tea set
drink = [p for p in manifest['props'] if p['zone'] in RELEASE_ZONES and p['type'] in DRINK]

# approved items replaced in place (same footprint) or removed for the Earth-to-Product plinth
HIDE = ['F003_', 'PL003_', 'F004_', 'PL004_',      # lobby potted tree and small planter
        'F015_', 'PL015_', 'F016_', 'PL016_',      # reception potted tree and small planter
        'F022_', 'F023_', 'F024_', 'F025_',        # the four forms on the experience-centre plinth
        'F029_', 'PL029_',                         # experience-centre potted tree
        'F050_', 'PL050_',                         # boardroom planter
        'F186_', 'PL186_']                         # studio potted tree


def look(name, room, zone, pos, target, lens):
    f = [t - p for p, t in zip(pos, target)]; n = math.hypot(*f); f = [v / n for v in f]
    up = [0.0, 1.0, 0.0]
    r = [f[1] * up[2] - f[2] * up[1], f[2] * up[0] - f[0] * up[2], f[0] * up[1] - f[1] * up[0]]; n = math.hypot(*r); r = [v / n for v in r]
    u = [r[1] * f[2] - r[2] * f[1], r[2] * f[0] - r[0] * f[2], r[0] * f[1] - r[1] * f[0]]
    m = [[r[0], u[0], -f[0]], [r[1], u[1], -f[1]], [r[2], u[2], -f[2]]]   # camera axes as columns (three.js looks down -z)
    tr = m[0][0] + m[1][1] + m[2][2]
    if tr > 0:
        s = math.sqrt(tr + 1) * 2; q = [(m[2][1] - m[1][2]) / s, (m[0][2] - m[2][0]) / s, (m[1][0] - m[0][1]) / s, s / 4]
    elif m[0][0] > m[1][1] and m[0][0] > m[2][2]:
        s = math.sqrt(1 + m[0][0] - m[1][1] - m[2][2]) * 2; q = [s / 4, (m[0][1] + m[1][0]) / s, (m[0][2] + m[2][0]) / s, (m[2][1] - m[1][2]) / s]
    elif m[1][1] > m[2][2]:
        s = math.sqrt(1 + m[1][1] - m[0][0] - m[2][2]) * 2; q = [(m[0][1] + m[1][0]) / s, s / 4, (m[1][2] + m[2][1]) / s, (m[0][2] - m[2][0]) / s]
    else:
        s = math.sqrt(1 + m[2][2] - m[0][0] - m[1][1]) * 2; q = [(m[0][2] + m[2][0]) / s, (m[1][2] + m[2][1]) / s, s / 4, (m[1][0] - m[0][1]) / s]
    return {'name': name, 'room': room, 'zone': zone, 'priority': 2, 'type': 'PERSP', 'position': pos, 'direction': f, 'up': u,
            'quaternion_xyzw': [round(v, 6) for v in q], 'clip': [0.05, 300.0], 'shift_x': 0.0, 'shift_y': 0.0,
            'sensor_fit': 'AUTO', 'lens': lens, 'sensor_width': 36.0, 'render': {'file': None, 'width': 1920, 'height': 1080}, 'proposal_view': True}


cameras = [
    look('BEL_CAM_SUN_WALL', 'Visitor passage', 'Z03', [10.42, 1.55, -0.45], [9.32, 1.35, -3.2], 18.0),
    look('BEL_CAM_SUN_SHELF', 'Global Design Studio', 'Z18', [32.45, 1.5, -18.0], [33.4, 0.8, -19.2], 24.0),
]

names = {
    'Z01': 'Arrival gallery', 'Z02': 'Reception · tea lounge', 'Z03': 'Earth & Sun passage', 'Z30': 'Earth to product',
    'Z08': 'Negotiation suite', 'Z18': 'Collaborative studio', 'Z07': 'Green Uthan (planned)', 'Z06': 'Academy · artisans (planned)',
    'Z15': 'Materials library (planned)', 'Z16': 'Materials lab (planned)', 'Z17': 'Prototype workshop (planned)', 'Z14': 'Digital design lab (planned)',
    'Z05': 'Export & order centre (planned)', 'Z04': 'Buyer project room (planned)', 'Z09': 'Records room (planned)',
    'Z20': 'Staff & artisan dining (planned)', 'Z21': 'Academy annex (planned)', 'Z10': 'Exec reception · tea point',
}
in3d = 'In this 3D proposal: '
notes = {
    'Z01': in3d + 'a banyan bonsai on granite by the glass gate, three stones, handmade terracotta on the check-in desk and six terracotta plaques by a rural artist (placeholder; to be commissioned and credited). The approved logos and brand wall are unchanged.',
    'Z02': in3d + 'tea in clay cups on wooden trays, rural instruments above the console (ektara, dotara, banshi, dhol; makers to be identified), a small fig tree and ghritokumari, with the handloom pieces of the approved redesign.',
    'Z03': in3d + 'the Sun wall (sun, solar generation, use and storage, operations, with grid and backup shown) and a terracotta earth wall. Concept demonstration, not live factory data: "Designed for a Solar-Powered Future" until measured evidence exists.',
    'Z30': in3d + 'the Earth-to-Product gallery on the plinth (raw material, technique, prototype, testing, collection; the four forms are removed), living materials on the table, drinking water from a clay kolshi (source client-stated; no laboratory results yet) and a Future of Bengal lamp prototype by the boardroom door.',
    'Z08': in3d + 'clay cups at every place and a clay jug instead of glass, woven samples on wooden trays, and a bonsai in the corner by the screen.',
    'Z18': in3d + 'the only room with exterior windows: three bonsai and a tulsi pot take turns on the sunning shelf at window W10, a small fig tree by W09, and basket prototypes, woven samples and sketches on the co-creation table.',
    'Z12': in3d + 'tea in clay cups. The office itself is unchanged in this increment.',
    'Z07': 'Planned: the Green Uthan (a courtyard-like gathering place with a small tree, stone seats and rural art) and European living, dining, bedroom and hospitality room-sets. Needs the merchandising team to move first (owner decision).',
    'Z06': 'Planned: the design education academy (20-30 people if the fire capacity allows) and the artisan demonstration studio, with its own entrance from the staff corridor.',
    'Z15': 'Planned: the living materials library, lit as a jewel box behind the experience-centre glass.',
    'Z16': 'Planned: natural-materials lab and testing (sink and concrete floor already here).',
    'Z17': 'Planned: prototype workshop with dust extraction (to be engineered), seen from the showroom through the interior glass.',
    'Z05': 'Planned: digital export and order centre beside reception.',
}
tour = [
    {'stop': 1, 'zone': None, 'camera': 'CAM_ISO_SE', 'title': 'The Living Bengal Factory',
     'description': 'Bengal Earth Lab on the approved Stage II floor, a concept proposal: earth, rural craft, a few living trees, rural art and music, and an honest solar story. This first increment covers the front rooms and the studio.'},
    {'stop': 2, 'zone': 'Z01', 'camera': 'CAM_03_Entrance_Lobby', 'title': 'Arrival gallery',
     'description': 'A banyan bonsai on granite by the glass gate, three stones, terracotta on the check-in desk and terracotta plaques by a rural artist (to be commissioned).'},
    {'stop': 3, 'zone': 'Z02', 'camera': 'CAM_01_Reception_A', 'title': 'Reception and Bengali tea',
     'description': 'Tea in clay, rural instruments above the console, handloom on the walls, a small fig tree and ghritokumari.'},
    {'stop': 4, 'zone': 'Z03', 'camera': 'BEL_CAM_SUN_WALL', 'title': 'Earth and Sun passage',
     'description': 'The Sun wall shows the energy story with grid and backup included. Concept demonstration, not live factory data.'},
    {'stop': 5, 'zone': 'Z30', 'camera': 'CAM_04_Experience_Centre_A', 'title': 'Earth to product',
     'description': 'Raw material, craft technique, prototype, testing and collection on the plinth: illustrative objects until real samples and records arrive.'},
    {'stop': 6, 'zone': 'Z30', 'camera': 'CAM_06_Experience_Centre_Detail', 'title': 'Living materials',
     'description': 'Woven jute, hogla, cane, water hyacinth, bamboo and kaisa samples with terracotta tiles; drinking water from a clay kolshi.'},
    {'stop': 7, 'zone': 'Z08', 'camera': 'CAM_09_Boardroom_A', 'title': 'Negotiation suite',
     'description': 'Tea in clay at every place, woven samples on wooden trays, a bonsai in the corner.'},
    {'stop': 8, 'zone': 'Z18', 'camera': 'CAM_13_Design_Studio_A', 'title': 'Collaborative studio',
     'description': 'The only room with daylight: basket prototypes and form sketches on the co-creation table.'},
    {'stop': 9, 'zone': 'Z18', 'camera': 'BEL_CAM_SUN_SHELF', 'title': 'The sunning shelf',
     'description': 'Bonsai and tulsi take turns in the daylight of window W10.'},
    {'stop': 10, 'zone': None, 'camera': 'CAM_ISO_SW', 'title': 'Designed for a Solar-Powered Future',
     'description': 'Next increments: the Green Uthan and showroom, the academy and artisan studio, the labs and library.'},
]

config = {
    'models': base['models'], 'renders': base['renders'], 'lightmapManifest': base['lightmapManifest'],
    'releaseMode': 'rooms', 'stage': base.get('stage', 4), 'baseModel': base.get('baseModel'),
    'concept': 'bengal-earth-lab', 'conceptZones': CONCEPT_ZONES,
    'conceptOptions': {'drinkware': [{'id': p['id'], 'zone': p['zone'], 'type': p['type'], 'position': p['position'], 'rotationY': p.get('rotationY', 0)}
                                     for p in drink if p['id'] not in TEA_SET]},
    'releaseZones': RELEASE_ZONES, 'interiorZones': [], 'screenZones': [], 'cameraOverrides': {},
    'excludedProps': sorted(set(base.get('excludedProps', [])) | {p['id'] for p in drink}),
    'excludedInterior': ['EC_MATERIALS_LIBRARY', 'MR_FIT_FORMS', 'MR_APPROVAL_BOARD', 'CAD_SCREENS', 'CAD_PINBOARD', 'CAD_LAYOUT_TABLE', 'DS_REVIEW_TABLE'],
    'excludedIdentity': ['ID_WATER_POINT', 'ID_SAMPLE_CARD_1', 'ID_SAMPLE_CARD_2', 'ID_MD_DEVELOPMENT', 'ID_BOARD_REVIEW_1', 'ID_BOARD_REVIEW_2'],
    'peopleManifest': base.get('peopleManifest'), 'peopleAccepted': False,
    'hideNodes': HIDE, 'noRenderPhotos': True,
    'hideParts': [{'nodes': ['F017_', 'F018_', 'F019_', 'F020_'], 'materials': ['g_', 'chrome']}],   # garments and hanger hooks out of the bays; the fixtures stay
    'trimParts': [{'nodes': ['F017_', 'F018_', 'F019_', 'F020_'], 'material': 'oak',                  # the empty wooden hangers under each rail (bay interiors measured in the scene)
                   'boxes': [[9.805, 1.15, -10.715, 12.345, 1.80, -10.145], [12.55, 1.15, -10.715, 15.085, 1.80, -10.145],
                             [16.155, 1.15, -10.715, 18.235, 1.80, -10.145], [18.44, 1.15, -10.715, 20.525, 1.80, -10.145]]}],
    'extraCameras': cameras, 'tour': tour, 'roomNames': names, 'roomNotes': notes,
    'branding': {
        'pageTitle': 'Bengal Earth Lab - concept proposal',
        'eyebrow': 'Bengal Earth Lab · From Rural Hands to Global Homes',
        'headline': 'The Living Bengal Factory · concept proposal',
        'welcomeTitle': 'Explore the Bengal Earth Lab proposal',
        'welcomeTour': 'A short guided tour of the first rooms of the proposal. Pause, go back or skip at any time.',
        'disclaimerHtml': '<b>Concept proposal</b> on the approved Stage II floor &middot; makers, artists, growers, stone sources, test records and energy data are still to be identified &middot; no people shown.',
    },
}
out = HERE / 'bel-config.json'
out.write_text(json.dumps(config, indent=1, ensure_ascii=False) + '\n')
print(out, len(config['conceptOptions']['drinkware']), 'drinkware replacements,', len(HIDE), 'hidden node prefixes')
