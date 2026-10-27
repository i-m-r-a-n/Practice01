"""Design Studio increment (Z18, furniture unchanged by the redesign):
eight frozen fictional CC0 adults on the redesigned layout's real chairs and work points, appended to the cumulative
room-release: the two approved source actors at their approved chairs plus two standing designers (mood-board wall,
trend table). GPT's 40 Z18 props stay (Z18 furniture is unchanged). Earlier actors / poses are preserved exactly.
python3 -I prepare_studio.py
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
    ('office-person-28', 'shirt', 'typing', 1221.5, -912.5, 180, True, 'F222 task_chair_green (approved source actor position)', '#b88b69', '#738866', '#30363d'),
    ('office-person-29', 'salwar', 'notes', 1284.5, -1007.5, 0, True, 'F225 task_chair_green (approved source actor position)', '#ddbaa4', '#a98a76', '#424039'),
    ('office-person-45', 'salwar_braid', 'browsing', 1185.0, -1055.0, 270, False, 'in front of the mood-board wall', '#c69d7b', '#8a9bb2', '#25313c'),
    ('office-person-46', 'shirt', 'fabric', 1305.0, -800.0, 270, False, 'end of the trend table', '#d5b6a0', '#9e7788', '#424039'),
]
actors, poses = [], {}
for i, (aid, outfit, task, x, y, facing, seated, where, skin, top, lower) in enumerate(ROWS):
    pose = f'{task}__seat_{int(round(SEAT * 1e5))}' if seated else task
    assert pose in LIB[outfit], (outfit, pose)
    a = {'id': aid, 'zone': 'Z18', 'task': task, 'outfit': outfit, 'pose': pose, 'heightScale': 1.0, 'bodyWidth': 1.0,
         'skinTint': skin, 'garmentTint': top, 'lowerTint': lower, 'phase': 3.7 * i, 'radius': 0.25, 'fictional': True,
         'faceMorph': [0.0, 0.5, 0.333], 'position': [x * IN, 0, y * IN], 'yaw': math.radians(facing), 'seated': seated,
         'wardrobeMode': 'modest long-sleeve top and trousers; long drape hidden', 'frozen': True,
         'placement': f'{where} (plan {x}, {y} in)'}
    if seated:
        a['support'] = {'sourceObject': where, 'seatTopY': SEAT, 'note': 'Pelvis on the redesigned layout\'s task chair; existing seat-specific pose.'}
    else:
        a['hideLongDrape'] = True
    actors.append(a)
    poses.setdefault(outfit, {})[pose] = LIB[outfit][pose]

mm = copy.deepcopy(REL)
mm.update(version='studio-static-1', count=len(actors), status='Global Design Studio static people', actors=actors,
          poses='studio/poses.json', activeZones=['Z18'], props=[])
(P / 'studio/people-manifest.json').write_text(json.dumps(mm, indent=2) + '\n')
(P / 'studio/poses.json').write_text(json.dumps(poses, separators=(',', ':')))
REL['actors'] = before_actors + actors
REL.update(version='reception4-boardroom6-experience3-md2-merch8-studio4-static-1', count=len(REL['actors']),
           status='Six-room release: Reception, Boardroom, Experience Centre, MD Office, Merchandising (proposed option B), Global Design Studio',
           activeZones=REL['activeZones'] + ['Z18'])
for t, items in poses.items():
    for k, v in items.items():
        REL_POSES.setdefault(t, {})[k] = v
assert REL['actors'][:len(before_actors)] == before_actors
assert all(REL_POSES[t][k] == v for t, items in before_poses.items() for k, v in items.items())
(P / 'room-release/people-manifest.json').write_text(json.dumps(REL, indent=2) + '\n')
(P / 'room-release/poses.json').write_text(json.dumps(REL_POSES, separators=(',', ':')))
for folder in ['studio', 'room-release']:
    paths = ['people-layer.js', folder + '/people-manifest.json', folder + '/poses.json'] + [v['file'] for v in SOURCE['assets'].values()]
    (P / folder / 'source-lock.json').write_text(json.dumps({f: hashlib.sha256((P / f).read_bytes()).hexdigest() for f in paths}, indent=2) + '\n')
print('STUDIO_READY', len(actors), 'total', REL['count'])
