"""Writes viewer/bel-config.json, the configuration of the /bengal-earth-lab/ proposal route (Bengal Earth Lab,
"The Living Bengal Factory"). It starts from the /realistic/ release config and the approved props manifest, so the
items it hides and the drinkware it replaces always match the model. Run: python3 -I make_bel_config.py"""
import json, math
from pathlib import Path

HERE = Path(__file__).resolve().parent
base = json.loads((HERE / 'release-config.json').read_text())
manifest = json.loads((HERE.parent / 'props' / 'office-props-manifest.json').read_text())

RELEASE_ZONES = ['Z01', 'Z02', 'Z08', 'Z30', 'Z12', 'Z18']          # props (small office items) stay in these rooms
CONCEPT_ZONES = ['Z01', 'Z02', 'Z03', 'Z30', 'Z08', 'Z12', 'Z18', 'Z22', 'Z15', 'Z16', 'Z17', 'Z21', 'Z20', 'Z09', 'Z04', 'Z07', 'Z06']   # rooms with Bengal Earth Lab items (Z07, Z06: option A only)
DRINK = {'glass', 'jug', 'teacup', 'tray', 'mug', 'bottle'}
TEA_SET = {'PROP_0006', 'PROP_0008'}                                 # reception tray and teacup: replaced by the clay tea set
drink = [p for p in manifest['props'] if p['zone'] in RELEASE_ZONES and p['type'] in DRINK]

# approved items replaced in place (same footprint). The garments, the four forms and the approved knitwear dressing
# stay: this is a knitwear (RMG) factory, and the concept adds the fabric story and Bengal craft around them.
HIDE = ['F003_', 'PL003_', 'F004_', 'PL004_',      # lobby potted tree and small planter
        'F015_', 'PL015_', 'F016_', 'PL016_',      # reception potted tree and small planter
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
    look('BEL_CAM_CIRCULAR', 'Merchandising', 'Z07', [12.25, 1.62, -13.9], [15.8, 0.8, -19.9], 18.0),
    look('BEL_CAM_CRAFT', 'Merchandising', 'Z07', [15.6, 1.5, -13.9], [14.1, 1.05, -11.2], 18.0),
    look('BEL_CAM_SHELF', 'Merchandising', 'Z07', [11.6, 1.35, -17.6], [9.6, 0.65, -18.6], 20.0),
    # experience centre and dining (every option)
    look('BEL_CAM_JHUT', 'Experience centre', 'Z30', [17.0, 1.55, -7.0], [15.2, 0.45, -8.6], 18.0),
    look('BEL_CAM_TEA', 'Staff & artisan dining', 'Z20', [25.0, 1.55, -23.15], [22.4, 1.45, -24.45], 17.0),
    look('BEL_CAM_PLANT_WALL', 'Global Design Studio', 'Z18', [31.6, 1.5, -27.3], [31.6, 1.55, -30.7], 18.0),
    look('BEL_CAM_ACADEMY', 'Commercial & accounts', 'Z06', [6.25, 1.6, -8.05], [4.7, 1.0, -16.8], 18.0),
    # the design wing
    look('BEL_CAM_MAKING_LINE', 'Design-wing corridor', 'Z22', [22.33, 1.6, -22.78], [24.7, 1.15, -21.4], 16.0),   # read from the hallway end: steps 1 to 6
    look('BEL_CAM_LAB', '3D printing lab', 'Z16', [24.0, 1.5, -13.4], [22.5, 0.8, -13.35], 22.0),
    # pilot rooms
    look('BEL_CAM_RECORDS', 'Audit room', 'Z09', [5.7, 1.55, -19.25], [3.9, 1.05, -22.4], 18.0),
    look('BEL_CAM_CAD', 'CAD / technical design', 'Z14', [23.7, 1.55, -1.1], [25.1, 1.3, -6.4], 18.0),
]

names = {
    'Z01': 'Arrival gallery', 'Z02': 'Reception · tea lounge', 'Z03': 'Earth & Sun passage', 'Z30': 'Experience centre · fabric stories',
    'Z08': 'Negotiation suite', 'Z18': 'Collaborative studio', 'Z07': 'Green Uthan · circular knitwear studio (later phase)', 'Z06': 'Design academy (later phase)',
    'Z15': 'Fibre library', 'Z16': 'Fabric lab', 'Z17': 'Sample room · remake and repair', 'Z22': 'Design wing · the making line', 'Z14': 'CAD · knitwear development',
    'Z05': 'Export & order centre (planned)', 'Z04': 'Buyer project room · order desk', 'Z09': 'Records room',
    'Z20': 'Staff & artisan dining', 'Z21': 'Academy annex (pilot academy)', 'Z10': 'Exec reception · tea point',
}
in3d = 'In this 3D proposal: '
notes = {
    'Z01': in3d + 'a banyan bonsai on granite by the glass gate, three stones, handmade terracotta on the check-in desk and six terracotta plaques by a rural artist (placeholder; to be commissioned and credited). The approved logos and brand wall are unchanged.',
    'Z02': in3d + 'tea in clay cups on wooden trays, rural instruments above the console (ektara, dotara, banshi, dhol; makers to be identified), a small fig tree and ghritokumari, with the handloom pieces of the approved redesign.',
    'Z03': in3d + 'the Sun wall (sun, solar generation, use and storage, operations, with grid and backup shown) and a terracotta earth wall whose clay bowls hold the raw side of the fabric story: cotton, jute, recycled fibre and indigo. Concept demonstration, not live factory data: "Designed for a Solar-Powered Future" until measured evidence exists.',
    'Z30': in3d + 'the approved knitwear stays (garments in the four bays, the four forms, sample cards, the materials library and the coconut-shell button story). Each form and bay adds its fabric story: cotton, a jute and cotton blend (research only), cutting waste (jhut) sorted by colour and spun again, used garments taken back and mended in kantha stitch. Drinking water from a clay kolshi (source client-stated; no laboratory results yet). Illustrative stories: fibre origins, recycled shares and tests are still to be documented.',
    'Z08': in3d + 'clay cups at every place and a clay jug instead of glass, the approved knitwear review trays, and a bonsai in the corner by the screen.',
    'Z18': in3d + 'the only room with exterior windows: three bonsai and a tulsi pot take turns on the sunning shelf at window W10, a small fig tree by W09, the approved sample-review table, and a living wall of plant niches on the north wall (no medical claim).',
    'Z12': in3d + 'tea in clay cups. The approved development shelf stays.',
    'Z07': 'Option A, a later phase: the owner chose the pilot (option C) first on 30 Oct 2026; this room changes only if the merchandising team moves later. In this 3D proposal: the Green Uthan, a Bengali courtyard with a bot-tola seat around the column, two small fig trees and a bonsai under grow lights (no daylight here), stone seats and an open bamboo canopy; an artisan corner (Chakma back-strap loom and Marma weaving and basketry, both only with community consent; nakshi kantha, cane, painted terracotta); and a circular knitwear studio in four steps: wear (knitwear on bamboo rails), remake (cutting waste sorted by colour, recycled yarn), repair (kantha mending) and return (take-back bins); a craft corner with rural tools, a shelf of painted clay and drums, and jute curtains on the north glass. Every approved item that moves is in the relocation ledger.',
    'Z06': 'Option A, a later phase: the owner chose the pilot (option C) first on 30 Oct 2026; this room changes only if the accounts team moves later. In this 3D proposal: the design education academy inside the existing glass accounts suite, 20 seats, a demonstration bench with a sewing machine and a hands camera, a mobile screen and a pin-up board; the discussion room becomes the tutor room. The fire engineer sets the capacity.',
    'Z15': in3d + 'eight labelled fibre boxes on the low shelf (cotton, jhut, used garments, jute, banana and pineapple leaf fibre and natural indigo as research only, coconut-shell buttons) and product passport cards on the review table, every field still to be documented, ready for the EU ecodesign rules for apparel that are still being drafted. The D65 colour booth and the approved fabric library stay.',
    'Z16': in3d + 'a fabric lab on the post-processing bench (a GSM cutter, a balance, knit swatches marked for wash shrinkage, a grey scale) with an empty durability log. Methods to be agreed with an accredited laboratory; no results are shown. The 3D printers stay.',
    'Z17': in3d + 'remake and repair on the pattern table: a T-shirt pattern in kraft paper, offcuts sorted by colour, a panel pieced from offcuts and a T-shirt mended in kantha stitch. The sample machines and forms stay. Seen from the Uthan through the interior glass in option A.',
    'Z22': in3d + 'the making line on the only solid wall of the design-wing entrance (the corridor walls are glass, so the labs behind them are the exhibit): one T-shirt in six steps, from fibre (cotton, jute, fibre recovered from cutting waste) to yarn, knit fabric, cut and sew, testing, and wear and return. Illustrative objects.',
    'Z05': 'Planned: the full digital export and order centre beside reception once HR moves (in the pilot the buyer project room holds the order desk).',
    'Z14': 'The approved CAD dressing, as on the live tour: one illustrative knit cardigan from flats to pattern, grading, marker and stitch chart. In the concept every style also carries a product passport (fibre origin, recycled share, durability, repair and recyclability), still to be designed.',
    'Z04': in3d + 'the buyer project room, also the export and order desk in the pilot: knit swatches on a tray, clay water, an order checklist with the product passport, and a project board (brief, fabric, lab dip, fit, tests, order) whose dates are all to be agreed.',
    'Z21': in3d + 'the pilot academy: a class of six at the approved table with knit swatches, yarn cones and a mending kit, and a craft wall of student work. The lounge stays.',
    'Z20': in3d + 'the tong, a Bengali tea stall, on the free west wall: a cart front on two wheels with a painted canopy, tea in clay cups, painted kettles on jute cords, an electric lantern in the hurricane form (no kerosene indoors) and wood-slice stools. Staff and artisan dining has the same care as the buyer rooms: clay plates, cups and jugs on hogla runners. Glazes to be tested before use.',
    'Z09': in3d + 'the records room: the originals behind every claim, fibre origins and recycled content first. Labelled evidence files and an Open Record index whose lines all read "none yet", "to prepare" or "to be collected" until documents arrive.',
}
tour = [
    {'stop': 1, 'zone': None, 'camera': 'CAM_ISO_SE', 'title': 'The Living Bengal Factory',
     'description': 'A knitwear factory whose fabric comes from the earth and from what was already made, with Bengal craft as its signature: a concept proposal on the approved Stage II floor. The owner chose the pilot (option C) first: the front rooms, the design wing, the studio and the pilot rooms. Merchandising and the accounts suite are shown as option A, a possible later phase.'},
    {'stop': 2, 'zone': 'Z01', 'camera': 'CAM_03_Entrance_Lobby', 'title': 'Arrival gallery',
     'description': 'A banyan bonsai on granite by the glass gate, three stones, terracotta on the check-in desk and terracotta plaques by a rural artist (to be commissioned).'},
    {'stop': 3, 'zone': 'Z02', 'camera': 'CAM_01_Reception_A', 'title': 'Reception and Bengali tea',
     'description': 'Tea in clay, rural instruments above the console, handloom on the walls, a small fig tree and ghritokumari.'},
    {'stop': 4, 'zone': 'Z03', 'camera': 'BEL_CAM_SUN_WALL', 'title': 'Earth and Sun passage',
     'description': 'The Sun wall shows the energy story with grid and backup included (concept, not live data); the earth wall holds the raw side of the fabric story: cotton, jute, recycled fibre and indigo beside clay.'},
    {'stop': 5, 'zone': 'Z30', 'camera': 'CAM_04_Experience_Centre_A', 'title': 'Fabric from the earth, and from waste',
     'description': 'The approved knitwear stays. Each form and bay shows where its fabric could come from: cotton, a jute and cotton blend (research), cutting waste sorted by colour and spun again, used garments taken back. Illustrative until records arrive.'},
    {'stop': 6, 'zone': 'Z30', 'camera': 'CAM_06_Experience_Centre_Detail', 'title': 'Second life in the bays',
     'description': 'Jute sacks of offcuts sorted by colour and the yarn spun from them, a take-back crate and a T-shirt mended in kantha stitch, under the approved garments.'},
    {'stop': 7, 'zone': 'Z30', 'camera': 'BEL_CAM_JHUT', 'title': 'The jhut river',
     'description': 'A sewing machine and a river of patchwork pieced from cutting waste, running off the table and across the floor, under natural indigo cloths. An installation: makers to be credited.'},
    {'stop': 8, 'zone': 'Z07', 'camera': 'BEL_CAM_UTHAN', 'title': 'Option A · the Green Uthan',
     'description': 'A later phase, only if the merchandising team moves: a Bengali courtyard around the column, a bot-tola seat, small trees under grow lights, kula and dala over a bamboo canopy, alpana, hurricane-form lanterns (electric) and natural indigo yarn.'},
    {'stop': 9, 'zone': 'Z07', 'camera': 'BEL_CAM_ARTISAN', 'title': 'Option A · artisan corner',
     'description': 'Demonstrations by invitation: a Chakma back-strap loom and Marma weaving and basketry, shown only with the weavers\' consent; nakshi kantha, cane, painted shokher hari pots, tepa putul dolls and drums.'},
    {'stop': 10, 'zone': 'Z07', 'camera': 'BEL_CAM_CIRCULAR', 'title': 'Option A · circular knitwear studio',
     'description': 'Wear, remake, repair and return around the Uthan: knitwear on bamboo rails, cutting waste sorted by colour, kantha mending and take-back bins. Illustrative.'},
    {'stop': 11, 'zone': 'Z07', 'camera': 'BEL_CAM_CRAFT', 'title': 'Option A · craft corner',
     'description': 'A bamboo trellis with a gamchha, a kantha, a kula and a painting by a rural artist (to be commissioned), a cane bowl chair, a jute pouf and bamboo armchairs. Makers to be identified, paid and credited.'},
    {'stop': 12, 'zone': 'Z06', 'camera': 'BEL_CAM_ACADEMY', 'title': 'Option A · design academy',
     'description': 'A later phase, only if the accounts team moves: 20 seats inside the existing glass suite, a demonstration bench with a sewing machine and a tutor room. The fire engineer sets the capacity.'},
    {'stop': 13, 'zone': 'Z22', 'camera': 'BEL_CAM_MAKING_LINE', 'title': 'The making line',
     'description': 'At the entrance to the design wing: one T-shirt in six steps, from fibre to yarn, knit fabric, cut and sew, test, and wear and return. Illustrative objects; real samples and records replace them.'},
    {'stop': 14, 'zone': 'Z16', 'camera': 'BEL_CAM_LAB', 'title': 'The labs behind the glass',
     'description': 'A fabric lab with an empty durability log (no results until tests are done), the fibre library with product passport cards next door, and remake and repair in the sample room.'},
    {'stop': 15, 'zone': 'Z14', 'camera': 'BEL_CAM_CAD', 'title': 'CAD · knitwear development',
     'description': 'The approved CAD room: one illustrative knit cardigan from flats to pattern, grading and marker. In the concept every style also carries a product passport.'},
    {'stop': 16, 'zone': 'Z21', 'camera': 'CAM_21_Lounge_Training', 'title': 'Academy annex (pilot)',
     'description': 'The pilot academy before any room changes: a class of six learning fibre, knit and repair, and a wall of student work.'},
    {'stop': 17, 'zone': 'Z20', 'camera': 'BEL_CAM_TEA', 'title': 'The tong · tea in clay',
     'description': 'Staff and artisan dining with a Bengali tea stall: a cart front on two wheels, tea in clay cups, an electric lantern in the hurricane form (no kerosene indoors) and wood-slice stools.'},
    {'stop': 18, 'zone': 'Z18', 'camera': 'CAM_13_Design_Studio_A', 'title': 'Collaborative studio',
     'description': 'The only room with daylight: the approved sample-review table, and a small fig tree by the window.'},
    {'stop': 19, 'zone': 'Z18', 'camera': 'BEL_CAM_SUN_SHELF', 'title': 'The sunning shelf',
     'description': 'Bonsai and tulsi take turns in the daylight of window W10.'},
    {'stop': 20, 'zone': 'Z18', 'camera': 'BEL_CAM_PLANT_WALL', 'title': 'The living wall',
     'description': 'At the north end of the studio: organic wooden niches with a warm backlight, snake plant, money plant and peace lily, and a small fig tree either side. No medical claim.'},
    {'stop': 21, 'zone': 'Z09', 'camera': 'BEL_CAM_RECORDS', 'title': 'The records room',
     'description': 'The originals behind every claim, fibre origins and recycled content first. Until documents arrive, every line of the Open Record reads none yet, to prepare or to be collected.'},
    {'stop': 22, 'zone': 'Z08', 'camera': 'CAM_09_Boardroom_A', 'title': 'Negotiation suite',
     'description': 'The visit ends here: tea in clay at every place, the approved knitwear review trays, a bonsai in the corner.'},
    {'stop': 23, 'zone': None, 'camera': 'CAM_ISO_SW', 'title': 'Designed for a Solar-Powered Future',
     'description': 'Every claim on this floor waits for its evidence: fibre origins, recycled shares, durability tests, makers, water reports and measured energy. Next: the full export and order centre once HR moves.'},
]

config = {
    'models': base['models'], 'renders': base['renders'], 'lightmapManifest': base['lightmapManifest'],
    'releaseMode': 'rooms', 'stage': base.get('stage', 4), 'baseModel': base.get('baseModel'),
    'concept': 'bengal-earth-lab', 'conceptZones': CONCEPT_ZONES,
    'conceptOptions': {'drinkware': [{'id': p['id'], 'zone': p['zone'], 'type': p['type'], 'position': p['position'], 'rotationY': p.get('rotationY', 0)}
                                     for p in drink if p['id'] not in TEA_SET]},
    'releaseZones': RELEASE_ZONES, 'interiorZones': ['Z14'], 'screenZones': [], 'cameraOverrides': {},   # Z14: the approved CAD knitwear dressing, as on /realistic/
    'excludedProps': sorted(set(base.get('excludedProps', [])) | {p['id'] for p in drink}),
    'excludedInterior': ['MR_FIT_FORMS', 'MR_APPROVAL_BOARD',     # Merchandising items: they move with the team in option A
                         'EC_TEXTILE_BAFFLES'],                    # the cloth fins: natural indigo swags take their place on this route
    'excludedIdentity': ['ID_WATER_POINT'],                      # replaced in place by the clay kolshi
    'peopleManifest': base.get('peopleManifest'), 'peopleAccepted': False,
    'hideNodes': HIDE + OPTION_A_HIDE, 'walkRelease': ledger['walk_release']['runs'], 'noRenderPhotos': True,
    'extraCameras': cameras, 'tour': tour, 'roomNames': names, 'roomNotes': notes,
    'roomGroups': {'Z07': 'Option A · later phase', 'Z06': 'Option A · later phase'},   # their own menu group and tour-card kicker (option C, the pilot, was chosen first)
    'branding': {
        'pageTitle': 'Bengal Earth Lab - concept proposal',
        'eyebrow': 'Bengal Earth Lab · Earth and recycled fabric, Bengal craft',
        'headline': 'The Living Bengal Factory · concept proposal',
        'welcomeTitle': 'Explore the Bengal Earth Lab proposal',
        'welcomeTour': 'A guided tour of the proposal: the pilot first, then the option A rooms as a possible later phase. Pause, go back or skip at any time.',
        'disclaimerHtml': '<b>Concept proposal</b> on the approved Stage II floor &middot; fibre origins, recycled shares, tests, makers, artists, growers, stone sources and energy data are still to be identified &middot; no people shown.',
    },
}
out = HERE / 'bel-config.json'
out.write_text(json.dumps(config, indent=1, ensure_ascii=False) + '\n')
print(out, len(config['conceptOptions']['drinkware']), 'drinkware replacements,', len(HIDE) + len(OPTION_A_HIDE), 'hidden node prefixes,', len(config['walkRelease']), 'walk release runs')
