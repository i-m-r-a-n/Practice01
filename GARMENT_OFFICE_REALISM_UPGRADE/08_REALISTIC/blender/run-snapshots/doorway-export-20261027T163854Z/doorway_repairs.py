"""Preserve the six existing, documented doorway-rail modelling corrections.

This is the same Boolean DIFFERENCE policy as 02_LIGHTING/bake_shell_lighting.py.
It changes only an export copy; opening positions and sizes remain untouched.
"""
from mathutils import Vector
from mathutils.bvhtree import BVHTree

EXPECTED = {('NI01', 'D10'), ('NI03', 'D11'), ('NI04', 'D12'),
            ('NI07', 'D18'), ('NI08', 'D19'), ('NI10', 'D21')}


def bounds(obj):
    points = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    return ([min(point[i] for point in points) for i in range(3)],
            [max(point[i] for point in points) for i in range(3)])


def portal_rays(cutter):
    low, high = bounds(cutter)
    normal_axis = min(range(2), key=lambda axis: high[axis] - low[axis])
    width_axis = 1 - normal_axis
    rays = []
    for fraction in (.02, .1, .2, .3, .4, .5, .6, .7, .8, .9, .98):
        for height in (1.225, 1.24, 1.255):
            origin = [0., 0., height]
            origin[normal_axis] = low[normal_axis] - .1
            origin[width_axis] = low[width_axis] + fraction * (high[width_axis] - low[width_axis])
            direction = [0., 0., 0.]
            direction[normal_axis] = 1.
            rays.append({'origin': origin, 'direction': direction,
                         'distance': high[normal_axis] - low[normal_axis] + .2})
    return rays


def object_bvh(obj, depsgraph):
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    points = [evaluated.matrix_world @ vertex.co for vertex in mesh.vertices]
    faces = [tuple(polygon.vertices) for polygon in mesh.polygons]
    tree = BVHTree.FromPolygons(points, faces, all_triangles=False)
    evaluated.to_mesh_clear()
    return tree


def hits(tree, rays):
    return sum(tree.ray_cast(Vector(ray['origin']), Vector(ray['direction']),
                             ray['distance'])[0] is not None for ray in rays)


def apply_doorway_repairs(bpy):
    cutters = [obj for obj in bpy.data.collections['Doors'].all_objects
               if obj.type == 'MESH' and 'head cut' not in obj.name]
    frames = [obj for obj in bpy.data.objects
              if obj.type == 'MESH' and ' frame above PW' in obj.name]
    depsgraph = bpy.context.evaluated_depsgraph_get()
    records = []
    for frame in frames:
        frame_low, frame_high = bounds(frame)
        for cutter in cutters:
            low, high = bounds(cutter)
            if not (all(low[i] < frame_high[i] and high[i] > frame_low[i] for i in range(3))
                    and high[2] > 1.25):
                continue
            pair = (frame.name.split()[0], cutter.name.split()[0])
            assert pair in EXPECTED, f'Unexpected frame/cutter intersection: {pair}'
            rays = portal_rays(cutter)
            before_hits = hits(object_bvh(frame, depsgraph), rays)
            if frame.data.users > 1:
                frame.data = frame.data.copy()
            modifier = frame.modifiers.new('preserved doorway repair ' + pair[1], 'BOOLEAN')
            modifier.operation = 'DIFFERENCE'
            modifier.object = cutter
            modifier.solver = 'EXACT'
            records.append({'frame': frame.name, 'cutter': cutter.name,
                            'frameBoundsBefore': [frame_low, frame_high],
                            'cutterBounds': [low, high], 'testRays': rays,
                            'railRayHitsBefore': before_hits})
    assert {(record['frame'].split()[0], record['cutter'].split()[0]) for record in records} == EXPECTED
    bpy.context.view_layer.update()
    depsgraph = bpy.context.evaluated_depsgraph_get()
    for record in records:
        frame = bpy.data.objects[record['frame']]
        record['railRayHitsAfter'] = hits(object_bvh(frame, depsgraph), record['testRays'])
        record['frameBoundsAfter'] = list(bounds(frame))
        assert record['railRayHitsBefore'] > 0, f'Original rail not reproduced: {frame.name}'
        assert record['railRayHitsAfter'] == 0, f'Rail still crosses opening: {frame.name}'
        assert record['frameBoundsAfter'] == record['frameBoundsBefore'], 'Frame extent moved'
    return records
