"""List what occupies a box of space in an exported scene GLB: for each mesh, the vertices inside the box (viewer coordinates
x east, y up, z south), grouped into connected clusters by a coarse grid, with each cluster's extent.
blender -b -P region_objects.py -- GLB X0 X1 Y0 Y1 Z0 Z1 [CELL_M]"""
import bpy, sys, numpy as np
argv = sys.argv[sys.argv.index('--') + 1:]
glb = argv[0]; x0, x1, y0, y1, z0, z1 = map(float, argv[1:7]); cell = float(argv[7]) if len(argv) > 7 else 0.12
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=glb)
for o in bpy.context.scene.objects:
    if o.type != 'MESH': continue
    me = o.data; n = len(me.vertices)
    if not n: continue
    co = np.empty(n * 3, dtype=np.float32); me.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
    M = np.array(o.matrix_world, dtype=np.float32); w = co @ M[:3, :3].T + M[:3, 3]
    v = np.stack([w[:, 0], w[:, 2], -w[:, 1]], 1)   # Blender (x, y, z) -> viewer (x, z_up -> y, -y -> z)
    m = (v[:, 0] >= x0) & (v[:, 0] <= x1) & (v[:, 1] >= y0) & (v[:, 1] <= y1) & (v[:, 2] >= z0) & (v[:, 2] <= z1)
    if not m.any(): continue
    p = v[m]; keys = np.floor(p / cell).astype(int); cells = {}
    for k, q in zip(map(tuple, keys), p): cells.setdefault(k, []).append(q)
    seen, clusters = set(), []
    for k in cells:
        if k in seen: continue
        stack, members = [k], []; seen.add(k)
        while stack:
            c = stack.pop(); members.append(c)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for dz in (-1, 0, 1):
                        nb = (c[0] + dx, c[1] + dy, c[2] + dz)
                        if nb in cells and nb not in seen: seen.add(nb); stack.append(nb)
        pts = np.array([q for c in members for q in cells[c]]); clusters.append((pts.min(0), pts.max(0), len(pts)))
    for lo, hi, cnt in sorted(clusters, key=lambda c: (c[0][0], c[0][2])):
        print(f'OBJ {o.name[:34]:34s} mat {(o.active_material.name if o.active_material else "-")[:22]:22s} x {lo[0]:6.2f}..{hi[0]:6.2f}  y {lo[1]:5.2f}..{hi[1]:5.2f}  z {lo[2]:6.2f}..{hi[2]:6.2f}  n {cnt}')
