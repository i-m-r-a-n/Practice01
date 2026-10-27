"""Compare actual retained live and new repair GLBs at six documented portals."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

import numpy as np
from mathutils import Quaternion, Vector
from mathutils.bvhtree import BVHTree


def read_tree(path, node_filter):
    blob = path.read_bytes()
    size = struct.unpack_from('<I', blob, 12)[0]
    doc = json.loads(blob[20:20 + size])
    offset = 20 + size
    binary_size = struct.unpack_from('<I', blob, offset)[0]
    binary = blob[offset + 8:offset + 8 + binary_size]
    dtype_map = {5120: '<i1', 5121: '<u1', 5122: '<i2', 5123: '<u2', 5125: '<u4', 5126: '<f4'}

    def accessor(index):
        accessor = doc['accessors'][index]
        view = doc['bufferViews'][accessor['bufferView']]
        dtype = np.dtype(dtype_map[accessor['componentType']])
        components = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4}[accessor['type']]
        values = np.ndarray((accessor['count'], components), dtype=dtype, buffer=binary,
                            offset=view.get('byteOffset', 0) + accessor.get('byteOffset', 0),
                            strides=(view.get('byteStride', dtype.itemsize * components), dtype.itemsize)).copy()
        if accessor.get('normalized'):
            maximum = np.iinfo(dtype).max
            values = np.maximum(values.astype(float) / maximum, -1.)
        return values

    points, faces, node_names = [], [], []
    count = 0

    def visit(index, parent):
        nonlocal count
        node = doc['nodes'][index]
        if 'matrix' in node:
            local = np.asarray(node['matrix'], dtype=float).reshape(4, 4, order='F')
        else:
            x, y, z, w = node.get('rotation', [0, 0, 0, 1])
            local = np.eye(4)
            local[:3, :3] = np.asarray(Quaternion((w, x, y, z)).to_matrix()) @ np.diag(node.get('scale', [1, 1, 1]))
            local[:3, 3] = node.get('translation', [0, 0, 0])
        world = parent @ local
        if 'mesh' in node and node_filter(node.get('name', '')):
            node_names.append(node.get('name'))
            for primitive in doc['meshes'][node['mesh']]['primitives']:
                vertices = accessor(primitive['attributes']['POSITION']).astype(float)
                vertices = np.c_[vertices, np.ones(len(vertices))] @ world.T
                vertices = vertices[:, [0, 2, 1]] * [1., -1., 1.]
                triangles = accessor(primitive['indices']).reshape(-1, 3).astype(int)
                points.extend(map(tuple, vertices))
                faces.extend(map(tuple, triangles + count))
                count += len(vertices)
        for child in node.get('children', []):
            visit(child, world)

    for index in doc['scenes'][doc.get('scene', 0)]['nodes']:
        visit(index, np.eye(4))
    assert points and faces
    return BVHTree.FromPolygons(points, faces, all_triangles=True), node_names, len(points), len(faces)


def count_hits(tree, rays):
    return sum(tree.ray_cast(Vector(ray['origin']), Vector(ray['direction']), ray['distance'])[0] is not None
               for ray in rays)


parser = argparse.ArgumentParser()
parser.add_argument('live', type=Path)
parser.add_argument('repaired', type=Path)
parser.add_argument('report', type=Path)
args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
report = json.loads(args.report.read_text())
live_tree, live_nodes, live_vertices, live_faces = read_tree(args.live, lambda name: name == 'WEB_SHELL_INTERIOR')
new_tree, new_nodes, new_vertices, new_faces = read_tree(args.repaired, lambda name: name in report['objects'])
checks = []
for repair in report['repairs']:
    live_hits = count_hits(live_tree, repair['testRays'])
    new_hits = count_hits(new_tree, repair['testRays'])
    check = {'frame': repair['frame'], 'door': repair['cutter'], 'rays': len(repair['testRays']),
             'originalSourceFrameHits': repair['railRayHitsBefore'], 'retainedLiveShellHits': live_hits,
             'newRepairedFrameHits': new_hits, 'pass': live_hits == new_hits == 0}
    checks.append(check)
result = {'passed': all(check['pass'] for check in checks),
          'liveReferenceFile': str(args.live), 'liveReferenceSHA256': hashlib.sha256(args.live.read_bytes()).hexdigest(),
          'repairedSHA256': hashlib.sha256(args.repaired.read_bytes()).hexdigest(),
          'liveNodes': live_nodes, 'newNodes': new_nodes, 'liveVertices': live_vertices, 'liveTriangles': live_faces,
          'newVertices': new_vertices, 'newTriangles': new_faces, 'checks': checks,
          'scope': 'All198 actual GLB ray probes reproduce the existing six live doorway clearances at the former rail heights. This checks the retained live file bytes, not a new network fetch or general building compliance.'}
output = args.report.with_name('doorway-live-parity.json')
output.write_text(json.dumps(result, indent=2))
report['live_mesh_parity'] = {'passed': result['passed'], 'report': output.name, 'liveReferenceSHA256': result['liveReferenceSHA256']}
args.report.write_text(json.dumps(report, indent=2))
print(json.dumps(result, indent=2))
assert result['passed'], 'Live and repaired doorway clearances differ'
