"""MD Office increment: two frozen fictional adults in Z12, appended to the cumulative room-release.

- office-person-14 (from the approved source manifest): the MD at the desk on the phone, pose and chair unchanged.
- office-person-36 (new definition, existing CC0 outfit and an existing seat-specific pose): a visitor taking notes in
  the visitor chair F065 (plan 1010, 118 in), facing the MD across the desk.
No furniture, prop, camera or earlier actor is changed. python3 -I prepare_md.py
"""
import copy, hashlib, json
from pathlib import Path
P = Path(__file__).resolve().parents[1]
IN = 0.0254
SOURCE = json.loads((P / 'people-manifest.json').read_text())
LIB = json.loads((P / 'poses.json').read_text())
REL = json.loads((P / 'room-release/people-manifest.json').read_text())
REL_POSES = json.loads((P / 'room-release/poses.json').read_text())
before_actors, before_poses = copy.deepcopy(REL['actors']), copy.deepcopy(REL_POSES)

md = copy.deepcopy(next(a for a in SOURCE['actors'] if a['id'] == 'office-person-14'))
md.update(frozen=True)
md.pop('path', None)
visitor = {
    'id': 'office-person-36', 'zone': 'Z12', 'task': 'notes', 'outfit': 'salwar', 'pose': 'notes__seat_48768',
    'heightScale': 1.0, 'bodyWidth': 0.964, 'skinTint': '#ddbaa4', 'garmentTint': '#8a9bb2', 'lowerTint': '#30363d',
    'phase': 7.1, 'radius': 0.25, 'fictional': True, 'faceMorph': [0.0, 0.5, 0.333],
    'position': [1010 * IN, 0, 118 * IN], 'yaw': 0.0,
    'support': {'sourceObject': 'F065 visitor_leather', 'seatTopY': 0.48768, 'note': 'Pelvis aligned to the approved visitor chair (seat top 19.2 in); existing seat-specific pose.'},
    'seated': True, 'wardrobeMode': 'modest long-sleeve top and trousers; long drape disabled for seated role', 'frozen': True,
}
actors = [md, visitor]
poses = {}
for a in actors:
    poses.setdefault(a['outfit'], {})[a['pose']] = LIB[a['outfit']][a['pose']]

lim = REL['limitations']
mdm = copy.deepcopy(REL)
mdm.update(version='md-static-1', count=2, status='MD Office static people', actors=actors, poses='md/poses.json', activeZones=['Z12'], props=[])
(P / 'md/people-manifest.json').write_text(json.dumps(mdm, indent=2) + '\n')
(P / 'md/poses.json').write_text(json.dumps(poses, separators=(',', ':')))

REL['actors'] = before_actors + actors
REL.update(version='reception4-boardroom6-experience3-md2-static-1', count=len(REL['actors']),
           status='Reception, Boardroom and Experience Centre accepted; MD Office static people added',
           activeZones=REL['activeZones'] + ['Z12'], limitations=lim)
for t, items in poses.items():
    for k, v in items.items():
        REL_POSES.setdefault(t, {})[k] = v
assert REL['actors'][:len(before_actors)] == before_actors
assert all(REL_POSES[t][k] == v for t, items in before_poses.items() for k, v in items.items())
(P / 'room-release/people-manifest.json').write_text(json.dumps(REL, indent=2) + '\n')
(P / 'room-release/poses.json').write_text(json.dumps(REL_POSES, separators=(',', ':')))
for folder in ['md', 'room-release']:
    paths = ['people-layer.js', folder + '/people-manifest.json', folder + '/poses.json'] + [v['file'] for v in SOURCE['assets'].values()]
    (P / folder / 'source-lock.json').write_text(json.dumps({f: hashlib.sha256((P / f).read_bytes()).hexdigest() for f in paths}, indent=2) + '\n')
print('MD_READY', [(a['id'], a['pose'], [round(v, 3) for v in a['position']]) for a in actors], 'total', REL['count'])
