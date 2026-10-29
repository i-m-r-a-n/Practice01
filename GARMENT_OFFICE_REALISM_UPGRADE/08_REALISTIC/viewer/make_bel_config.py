"""Writes viewer/bel-config.json, the configuration of the /bengal-earth-lab/ proposal route (Bengal Earth Lab,
"The Living Bengal Factory"). It starts from the /realistic/ release config and the approved props manifest, so the
items it hides and the drinkware it replaces always match the model. Run: python3 -I make_bel_config.py"""
import json, math
from pathlib import Path

HERE = Path(__file__).resolve().parent
base = json.loads((HERE / 'release-config.json').read_text())
manifest = json.loads((HERE.parent / 'props' / 'office-props-manifest.json').read_text())

RELEASE_ZONES = ['Z01', 'Z02', 'Z08', 'Z30', 'Z12', 'Z18']          # props (small office items) stay in these rooms
CONCEPT_ZONES = ['Z01', 'Z02', 'Z03', 'Z30', 'Z08', 'Z12', 'Z18', 'Z22', 'Z15', 'Z16', 'Z17', 'Z07', 'Z06']   # rooms with Bengal Earth Lab items (Z07, Z06: option A only)
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
# option A rooms (Merchandising Z07, the Accounts suite in Z06): everything the relocation ledger moves off this floor
ledger = json.loads((HERE / 'option-a-ledger.json').read_text())
OPTION_A_HIDE = [n + '_' for m in ledger['moves_off_this_floor'] for n in m['nodes']]


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
    # option A rooms
    look('BEL_CAM_UTHAN', 'Merchandising', 'Z07', [20.2, 1.55, -11.6], [14.6, 0.9, -16.6], 16.0),
    look('BEL_CAM_ARTISAN', 'Merchandising', 'Z07', [13.55, 1.45, -13.9], [11.0, 0.45, -16.3], 20.0),
    look('BEL_CAM_ROOMSETS', 'Merchandising', 'Z07', [12.25, 1.62, -13.9], [15.8, 0.8, -19.9], 18.0),
    look('BEL_CAM_ACADEMY', 'Commercial & accounts', 'Z06', [6.25, 1.6, -8.05], [4.7, 1.0, -16.8], 18.0),
    # the design wing
    look('BEL_CAM_MAKING_LINE', 'Design-wing corridor', 'Z22', [22.33, 1.6, -22.78], [24.7, 1.15, -21.4], 16.0),   # read from the hallway end: steps 1 to 6
    look('BEL_CAM_LAB', '3D printing lab', 'Z16', [24.0, 1.5, -13.4], [22.5, 0.8, -13.35], 22.0),
]

names = {
    'Z01': 'Arrival gallery', 'Z02': 'Reception · tea lounge', 'Z03': 'Earth & Sun passage', 'Z30': 'Earth to product',
    'Z08': 'Negotiation suite', 'Z18': 'Collaborative studio', 'Z07': 'Green Uthan · room-sets (option A)', 'Z06': 'Design academy (option A)',
    'Z15': 'Living materials library', 'Z16': 'Materials lab', 'Z17': 'Prototype workshop', 'Z22': 'Design wing · the making line', 'Z14': 'Digital design lab (planned)',
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
    'Z07': 'Option A only (the merchandising team moves first; owner decision). In this 3D proposal: the Green Uthan, a Bengali courtyard with a bot-tola seat around the column, two small fig trees and a bonsai under grow lights (no daylight here), stone seats and an open bamboo canopy; an artisan corner (Chakma back-strap loom and Marma weaving and basketry, both only with community consent; nakshi kantha, cane, painted terracotta); four room-sets for European buyers: living, dining, bedroom and hospitality. Every approved item that moves is in the relocation ledger.',
    'Z06': 'Option A only (the accounts team moves first; owner decision). In this 3D proposal: the design education academy inside the existing glass accounts suite, 20 seats, a demonstration bench with a hands camera, a mobile screen and a pin-up board; the discussion room becomes the tutor room. The fire engineer sets the capacity.',
    'Z15': in3d + 'eight labelled boxes of natural materials on the low shelf (jute, hogla, cane, bamboo, water hyacinth, kaisa grass, coconut shell, terracotta) and Material Passport cards on the review table, their fields still to be documented. The D65 colour booth and the approved fabric library stay.',
    'Z16': in3d + 'a moisture and mould test set-up on the post-processing bench (sealed sample boxes, a scale, a moisture meter) with an empty test log. Methods to be agreed with an accredited laboratory; no results are shown. The 3D printers stay.',
    'Z17': in3d + 'cane and bamboo prototyping on the pattern table under a dust-extraction hood marked "to be engineered", and a steam-bending jig. The sample machines and forms stay. Seen from the Uthan through the interior glass in option A.',
    'Z22': in3d + 'the making line on the only solid wall of the design-wing entrance (the corridor walls are glass, so the labs behind them are the exhibit): one River to Home basket in six steps, from hogla leaves to the collection. Illustrative objects.',
    'Z05': 'Planned: digital export and order centre beside reception.',
}
tour = [
    {'stop': 1, 'zone': None, 'camera': 'CAM_ISO_SE', 'title': 'The Living Bengal Factory',
     'description': 'Bengal Earth Lab on the approved Stage II floor, a concept proposal: earth, rural craft, a few living trees, rural art and music, and an honest solar story. The front rooms, the design wing and the studio work in every option; Merchandising and the accounts suite are shown as option A only.'},
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
    {'stop': 7, 'zone': 'Z07', 'camera': 'BEL_CAM_UTHAN', 'title': 'Option A · the Green Uthan',
     'description': 'Only if the merchandising team moves: a Bengali courtyard around the column, a bot-tola seat, small trees under grow lights, stone seats and an open bamboo canopy.'},
    {'stop': 8, 'zone': 'Z07', 'camera': 'BEL_CAM_ARTISAN', 'title': 'Option A · artisan corner',
     'description': 'Demonstrations by invitation: a Chakma back-strap loom and Marma weaving and basketry, shown only with the weavers\' consent; nakshi kantha, cane and painted terracotta.'},
    {'stop': 9, 'zone': 'Z07', 'camera': 'BEL_CAM_ROOMSETS', 'title': 'Option A · room-sets for European buyers',
     'description': 'Living, dining, bedroom and hospitality settings in mango wood, cane, jute, hogla, kantha and terracotta. Illustrative, not products on sale.'},
    {'stop': 10, 'zone': 'Z06', 'camera': 'BEL_CAM_ACADEMY', 'title': 'Option A · design academy',
     'description': 'Only if the accounts team moves: 20 seats inside the existing glass suite, a demonstration bench and a tutor room. The fire engineer sets the capacity.'},
    {'stop': 11, 'zone': 'Z22', 'camera': 'BEL_CAM_MAKING_LINE', 'title': 'The making line',
     'description': 'At the entrance to the design wing: one basket in six steps, from hogla leaves to the collection. Illustrative objects; real samples and records replace them.'},
    {'stop': 12, 'zone': 'Z16', 'camera': 'BEL_CAM_LAB', 'title': 'The labs behind the glass',
     'description': 'A moisture and mould test bench with an empty log (no results until tests are done), the living materials library next door and the cane and bamboo prototype workshop.'},
    {'stop': 13, 'zone': 'Z18', 'camera': 'CAM_13_Design_Studio_A', 'title': 'Collaborative studio',
     'description': 'The only room with daylight: basket prototypes and form sketches on the co-creation table.'},
    {'stop': 14, 'zone': 'Z18', 'camera': 'BEL_CAM_SUN_SHELF', 'title': 'The sunning shelf',
     'description': 'Bonsai and tulsi take turns in the daylight of window W10.'},
    {'stop': 15, 'zone': 'Z08', 'camera': 'CAM_09_Boardroom_A', 'title': 'Negotiation suite',
     'description': 'The visit ends here: tea in clay at every place, woven samples on wooden trays, a bonsai in the corner.'},
    {'stop': 16, 'zone': None, 'camera': 'CAM_ISO_SW', 'title': 'Designed for a Solar-Powered Future',
     'description': 'Every claim on this floor waits for its evidence: makers, tests, water reports and measured energy. Next: the cafe, the academy annex and the export and order centre.'},
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
    'hideNodes': HIDE + OPTION_A_HIDE, 'walkRelease': ledger['walk_release']['runs'], 'noRenderPhotos': True,
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
        'welcomeTour': 'A guided tour of the proposal, including the option A rooms. Pause, go back or skip at any time.',
        'disclaimerHtml': '<b>Concept proposal</b> on the approved Stage II floor &middot; makers, artists, growers, stone sources, test records and energy data are still to be identified &middot; no people shown.',
    },
}
out = HERE / 'bel-config.json'
out.write_text(json.dumps(config, indent=1, ensure_ascii=False) + '\n')
print(out, len(config['conceptOptions']['drinkware']), 'drinkware replacements,', len(HIDE) + len(OPTION_A_HIDE), 'hidden node prefixes,', len(config['walkRelease']), 'walk release runs')
