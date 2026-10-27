"""Verify a normal-guide loop reference against actual exported GLB UV1 vertices."""
import argparse
import hashlib
import json
from pathlib import Path
import struct

import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_glb(path):
    data = path.read_bytes()
    length = struct.unpack_from('<I', data, 12)[0]
    doc = json.loads(data[20:20 + length])
    offset = 20 + length
    size = struct.unpack_from('<I', data, offset)[0]
    binary = data[offset + 8:offset + 8 + size]

    def accessor(index):
        a = doc['accessors'][index]
        view = doc['bufferViews'][a['bufferView']]
        dtype = {5126: '<f4', 5125: '<u4', 5123: '<u2', 5121: 'u1'}[a['componentType']]
        count = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4}[a['type']]
        item = np.dtype(dtype).itemsize
        return np.ndarray((a['count'], count), dtype=dtype, buffer=binary,
                          offset=view.get('byteOffset', 0) + a.get('byteOffset', 0),
                          strides=(view.get('byteStride', item * count), item)).copy()

    rows = []

    def visit(index, parent):
        node = doc['nodes'][index]
        if 'matrix' in node:
            local = np.asarray(node['matrix'], dtype=float).reshape(4, 4, order='F')
        else:
            local = np.eye(4)
            local[:3, :3] = Rotation.from_quat(node.get('rotation', [0, 0, 0, 1])).as_matrix() @ np.diag(node.get('scale', [1, 1, 1]))
            local[:3, 3] = node.get('translation', [0, 0, 0])
        world = parent @ local
        if 'mesh' in node:
            for primitive in doc['meshes'][node['mesh']]['primitives']:
                attributes = primitive['attributes']
                points = accessor(attributes['POSITION']).astype(float)
                points = np.c_[points, np.ones(len(points))] @ world.T
                # glTF Y-up back to source Blender Z-up.
                points = points[:, [0, 2, 1]] * np.array([1., -1., 1.])
                uv0 = accessor(attributes['TEXCOORD_0']).astype(float)
                uv1 = accessor(attributes['TEXCOORD_1']).astype(float)
                uv0[:, 1] = 1 - uv0[:, 1]
                uv1[:, 1] = 1 - uv1[:, 1]
                rows.append(np.c_[points, uv0, uv1])
        for child in node.get('children', []):
            visit(child, world)

    for index in doc['scenes'][doc.get('scene', 0)]['nodes']:
        visit(index, np.eye(4))
    return np.concatenate(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('glb', type=Path)
    parser.add_argument('reference', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    reference = np.load(args.reference)
    source = np.c_[reference['world_and_uv0'], reference['uv1']]
    target = read_glb(args.glb)
    tree = cKDTree(source[:, :3])
    maximum_position = maximum_uv0 = maximum_uv1 = 0.
    failures = []
    for row_number, row in enumerate(target):
        candidates = tree.query_ball_point(row[:3], 0.00002)
        matched = [(index, np.max(np.abs(source[index, 3:] - row[3:]))) for index in candidates]
        matched = [(index, error) for index, error in matched if error <= 0.000002]
        if not matched:
            failures.append(row_number)
            continue
        index, _ = min(matched, key=lambda pair: pair[1])
        maximum_position = max(maximum_position, float(np.linalg.norm(source[index, :3] - row[:3])))
        maximum_uv0 = max(maximum_uv0, float(np.max(np.abs(source[index, 3:5] - row[3:5]))))
        maximum_uv1 = max(maximum_uv1, float(np.max(np.abs(source[index, 5:] - row[5:]))))
    result = {'passed': not failures, 'glbSHA256': sha(args.glb), 'guideReferenceSHA256': sha(args.reference),
              'sourceGuideLoops': len(source), 'exportedVertices': len(target),
              'maxWorldPositionDifferenceMetres': maximum_position, 'maxUV0Difference': maximum_uv0,
              'maxUV1Difference': maximum_uv1, 'unmatchedVertices': failures,
              'scope': 'Actual exported world positions and UV0/UV1 match the normal-guide bake reference; this is not lighting visual acceptance.'}
    args.output.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    assert not failures, 'Normal-guide atlas does not match actual exported geometry'


if __name__ == '__main__':
    main()
