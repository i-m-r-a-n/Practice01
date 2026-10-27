"""Merchandising increment on the Z06 / Z07 option B model (Claude, claude/space-optimization):
eight frozen fictional CC0 adults on the redesigned layout's real chairs and work points, appended to the cumulative
room-release. The approved-layout Z07 actors and Z07 GPT props were placed for the old desks, so they are not used
(the old Z07 props are listed in release-config excludedProps). Earlier actors / poses are preserved exactly.
python3 -I prepare_merch.py
"""
import copy, hashlib, json, math
from pathlib import Path
P = Path(__file__).resolve().parents[1]
IN = 0.0254
SEAT = 0.49022                                                 # task chair seat top in both models
SOURCE = json.loads((P / 'people-manifest.json').read_text())
LIB = json.loads((P / 'poses.json').read_text())
REL = json.loads((P / 'room-release/people-manifest.json').read_text())
REL_POSES = json.loads((P / 'room-release/poses.json').read_text())
before_actors, before_poses = copy.deepcopy(REL['actors']), copy.deepcopy(REL_POSES)

# id, outfit, task / pose, plan x, plan y (in), facing deg (0 south, 90 east), seated, chair, skin, top, lower
ROWS = [
    ('office-person-37', 'shirt', 'typing', 461.5, -566.0, 180, True, 'bench 2 south chair', '#b88b69', '#637b76', '#25313c'),
    ('office-person-38', 'salwar', 'notes', 571.5, -566.0, 180, True, 'bench 2 south chair', '#ddbaa4', '#ad9271', '#30363d'),
    ('office-person-39', 'panjabi', 'typing', 516.5, -768.0, 0, True, 'bench 1 north chair', '#d5b6a0', '#8a9bb2', '#424039'),
    ('office-person-40', 'salwar_braid', 'show_sample', 652.0, -655.0, 90, False, 'inspection island (west side)', '#c69d7b', '#9e7788', '#25313c'),
    ('office-person-41', 'shirt', 'browsing', 748.0, -640.0, 270, False, 'inspection island (east side)', '#c69d7b', '#9e7788', '#424039'),
    ('office-person-42', 'panjabi', 'listening', 736.0, -495.0, 270, True, 'buyer review table, east chair', '#b88b69', '#738866', '#25313c'),
    ('office-person-43', 'salwar', 'presenting', 664.0, -470.0, 135, False, 'beside the buyer review screen', '#d5b6a0', '#8a9bb2', '#30363d'),
    ('office-person-44', 'shirt', 'fabric', 700.0, -776.0, 180, False, 'sample rails', '#ddbaa4', '#b9a895', '#424039'),
]
actors, poses = [], {}
for i, (aid, outfit, task, x, y, facing, seated, where, skin, top, lower) in enumerate(ROWS):
    pose = f'{task}__seat_{int(round(SEAT * 1e5))}' if seated else task
    assert pose in LIB[outfit], (outfit, pose)
    a = {'id': aid, 'zone': 'Z07', 'task': task, 'outfit': outfit, 'pose': pose, 'heightScale': 1.0, 'bodyWidth': 1.0,
         'skinTint': skin, 'garmentTint': top, 'lowerTint': lower, 'phase': 3.7 * i, 'radius': 0.25, 'fictional': True,
         'faceMorph': [0.0, 0.5, 0.333], 'position': [x * IN, 0, y * IN], 'yaw': math.radians(facing), 'seated': seated,
         'wardrobeMode': 'modest long-sleeve top and trousers; long drape hidden', 'frozen': True,
         'placement': f'Option B layout: {where} (plan {x}, {y} in)'}
    if seated:
        a['support'] = {'sourceObject': where, 'seatTopY': SEAT, 'note': 'Pelvis on the redesigned layout\'s task chair; existing seat-specific pose.'}
    else:
        a['hideLongDrape'] = True
    actors.append(a)
    poses.setdefault(outfit, {})[pose] = LIB[outfit][pose]

mm = copy.deepcopy(REL)
mm.update(version='merch-optionB-static-1', count=len(actors), status='Merchandising (option B redesign) static people', actors=actors,
          poses='merch/poses.json', activeZones=['Z07'], props=[])
(P / 'merch/people-manifest.json').write_text(json.dumps(mm, indent=2) + '\n')
(P / 'merch/poses.json').write_text(json.dumps(poses, separators=(',', ':')))
REL['actors'] = before_actors + actors
REL.update(version='reception4-boardroom6-experience3-md2-merch8-static-1', count=len(REL['actors']),
           status='Reception, Boardroom, Experience Centre, MD Office; Merchandising shown as the proposed option B redesign',
           activeZones=REL['activeZones'] + ['Z07'])
for t, items in poses.items():
    for k, v in items.items():
        REL_POSES.setdefault(t, {})[k] = v
assert REL['actors'][:len(before_actors)] == before_actors
assert all(REL_POSES[t][k] == v for t, items in before_poses.items() for k, v in items.items())
(P / 'room-release/people-manifest.json').write_text(json.dumps(REL, indent=2) + '\n')
(P / 'room-release/poses.json').write_text(json.dumps(REL_POSES, separators=(',', ':')))
for folder in ['merch', 'room-release']:
    paths = ['people-layer.js', folder + '/people-manifest.json', folder + '/poses.json'] + [v['file'] for v in SOURCE['assets'].values()]
    (P / folder / 'source-lock.json').write_text(json.dumps({f: hashlib.sha256((P / f).read_bytes()).hexdigest() for f in paths}, indent=2) + '\n')
print('MERCH_READY', len(actors), 'total', REL['count'])
