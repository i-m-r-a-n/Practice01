"""Mesh building helpers for the Stage II office model (Blender 5.2).

Assets are modelled in INCHES in a local frame: x right, y back, z up, origin at the floor centre of the
footprint. The asset "front" faces local -Y. MB.mesh() converts to metres. Every face gets a box-projected UV
in metres, so tiling textures keep real-world scale (1 texture tile = the material's tile size).
"""
import math

import bmesh
import bpy
from mathutils import Matrix, Vector

IN = 0.0254


class MB:
    """Accumulates geometry (inches) with named materials, then builds one mesh datablock."""

    def __init__(self):
        self.bm = bmesh.new()
        self.mats = []          # material names, index = slot

    def _slot(self, mat):
        if mat not in self.mats:
            self.mats.append(mat)
        return self.mats.index(mat)

    def _add(self, verts, faces, mat, smooth=False):
        bv = [self.bm.verts.new(v) for v in verts]
        out = []
        for f in faces:
            try:
                face = self.bm.faces.new([bv[i] for i in f])
            except ValueError:
                continue
            face.material_index = self._slot(mat)
            face.smooth = smooth
            out.append(face)
        return bv, out

    # ------------------------------------------------------------------ primitives
    def box(self, x0, x1, y0, y1, z0, z1, mat, bevel=0.0, segs=2, rot=0.0, pivot=None):
        x0, x1, y0, y1, z0, z1 = min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1), min(z0, z1), max(z0, z1)
        if x1 - x0 < 1e-3 or y1 - y0 < 1e-3 or z1 - z0 < 1e-3:
            return self
        v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
        bv, faces = self._add(v, f, mat, smooth=bevel > 0)
        b = min(bevel, (x1 - x0) / 2.05, (y1 - y0) / 2.05, (z1 - z0) / 2.05)
        if b > 0.01:
            edges = list({e for fc in faces for e in fc.edges})
            res = bmesh.ops.bevel(self.bm, geom=edges + bv, offset=b, segments=segs, affect='EDGES', profile=0.5,
                                  clamp_overlap=True)
            for fc in res.get('faces', []):
                fc.material_index = self._slot(mat)
                fc.smooth = True
            bv = list({vv for fc in faces + res.get('faces', []) if fc.is_valid for vv in fc.verts})
        if rot:
            c = Vector(pivot or ((x0 + x1) / 2, (y0 + y1) / 2, 0))
            m = Matrix.Translation(c) @ Matrix.Rotation(rot, 4, 'Z') @ Matrix.Translation(-c)
            bmesh.ops.transform(self.bm, matrix=m, verts=[x for x in bv if x.is_valid])
        return self

    def prism(self, pts, z0, z1, mat, smooth=False, bevel=0.0, segs=2):
        """Vertical extrusion of a closed polygon (x, y) between z0 and z1."""
        n = len(pts)
        v = [(x, y, z0) for x, y in pts] + [(x, y, z1) for x, y in pts]
        area = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
        bottom = list(range(n))[::-1] if area > 0 else list(range(n))
        top = [i + n for i in range(n)] if area > 0 else [i + n for i in range(n)][::-1]
        sides = []
        for i in range(n):
            j = (i + 1) % n
            sides.append((i, j, j + n, i + n) if area > 0 else (j, i, i + n, j + n))
        bv, faces = self._add(v, [tuple(bottom), tuple(top)] + sides, mat)
        for fc in faces[2:]:
            fc.smooth = smooth
        if bevel > 0.01:
            cap_edges = list({e for fc in faces[:2] for e in fc.edges})
            res = bmesh.ops.bevel(self.bm, geom=cap_edges, offset=bevel, segments=segs, affect='EDGES', profile=0.5,
                                  clamp_overlap=True)
            for fc in res.get('faces', []):
                fc.material_index = self._slot(mat)
                fc.smooth = True
        return self

    def cyl(self, cx, cy, r, z0, z1, mat, segs=24, r2=None, cap=True, smooth=True):
        """Vertical cylinder / cone frustum."""
        r2 = r if r2 is None else r2
        v = []
        for k in range(segs):
            a = 2 * math.pi * k / segs
            v.append((cx + r * math.cos(a), cy + r * math.sin(a), z0))
        for k in range(segs):
            a = 2 * math.pi * k / segs
            v.append((cx + r2 * math.cos(a), cy + r2 * math.sin(a), z1))
        f = [(k, (k + 1) % segs, (k + 1) % segs + segs, k + segs) for k in range(segs)]
        if cap:
            f += [tuple(range(segs))[::-1], tuple(range(segs, 2 * segs))]
        bv, faces = self._add(v, f, mat)
        for fc in faces[:segs]:
            fc.smooth = smooth
        return self

    def rod(self, p, q, r, mat, segs=12, cap=True):
        """Cylinder between two 3D points (inches)."""
        p, q = Vector(p), Vector(q)
        d = q - p
        L = d.length
        if L < 1e-4:
            return self
        start = len(self.bm.verts)
        tmp = MB()
        tmp.cyl(0, 0, r, 0, L, mat, segs=segs, cap=cap)
        rotq = Vector((0, 0, 1)).rotation_difference(d.normalized())
        m = Matrix.Translation(p) @ rotq.to_matrix().to_4x4()
        self._merge(tmp, m)
        return self

    def lathe(self, profile, mat, segs=32, cx=0.0, cy=0.0, smooth=True, close_bottom=True, close_top=True):
        """Surface of revolution around a vertical axis. profile = [(radius, z), ...] bottom to top."""
        rings = []
        for r, z in profile:
            ring = []
            for k in range(segs):
                a = 2 * math.pi * k / segs
                ring.append((cx + r * math.cos(a), cy + r * math.sin(a), z))
            rings.append(ring)
        v = [p for ring in rings for p in ring]
        f = []
        for i in range(len(rings) - 1):
            for k in range(segs):
                a, b = i * segs + k, i * segs + (k + 1) % segs
                f.append((a, b, b + segs, a + segs))
        if close_bottom and profile[0][0] > 1e-3:
            f.append(tuple(range(segs))[::-1])
        if close_top and profile[-1][0] > 1e-3:
            last = (len(rings) - 1) * segs
            f.append(tuple(range(last, last + segs)))
        bv, faces = self._add(v, f, mat, smooth=smooth)
        return self

    def sphere(self, c, r, mat, segs=16, rings=10, sz=1.0):
        prof = []
        for i in range(rings + 1):
            t = math.pi * i / rings
            prof.append((max(r * math.sin(t), 1e-4), c[2] - r * sz * math.cos(t)))
        return self.lathe(prof, mat, segs=segs, cx=c[0], cy=c[1])

    def quad(self, p0, p1, p2, p3, mat, smooth=False):
        self._add([p0, p1, p2, p3], [(0, 1, 2, 3)], mat, smooth)
        return self

    def _merge(self, other, matrix=None):
        me = bpy.data.meshes.new('_tmp')
        other.bm.to_mesh(me)
        other.bm.free()
        if matrix is not None:
            me.transform(matrix)
        remap = [self._slot(m) for m in other.mats]
        n0 = len(self.bm.faces)
        self.bm.from_mesh(me)
        self.bm.faces.ensure_lookup_table()
        for fc in list(self.bm.faces)[n0:]:
            fc.material_index = remap[fc.material_index] if fc.material_index < len(remap) else 0
        bpy.data.meshes.remove(me)

    def add(self, other, dx=0.0, dy=0.0, dz=0.0, rot=0.0):
        """Merge another MB, rotated about z (radians) then moved (inches)."""
        m = Matrix.Translation((dx, dy, dz)) @ Matrix.Rotation(rot, 4, 'Z')
        self._merge(other, m)
        return self

    # ------------------------------------------------------------------ output
    def mesh(self, name, materials, uv_scale=1.0):
        """Build a Mesh datablock (metres) with box-projected UVs (metres) and smooth-by-angle shading."""
        bm = self.bm
        bmesh.ops.scale(bm, vec=(IN, IN, IN), verts=bm.verts)
        uv = bm.loops.layers.uv.new('UVMap')
        for fc in bm.faces:
            n = fc.normal
            ax = max(range(3), key=lambda i: abs(n[i]))
            for lp in fc.loops:
                co = lp.vert.co
                if ax == 2:
                    lp[uv].uv = (co.x * uv_scale, co.y * uv_scale)
                elif ax == 1:
                    lp[uv].uv = (co.x * uv_scale, co.z * uv_scale)
                else:
                    lp[uv].uv = (co.y * uv_scale, co.z * uv_scale)
        me = bpy.data.meshes.new(name)
        bm.to_mesh(me)
        bm.free()
        for m in self.mats:
            me.materials.append(materials[m])
        try:
            me.set_sharpness_by_angle(angle=math.radians(35))
        except Exception:
            pass
        me.update()
        return me


def place(me, name, coll, x, y, z=0.0, facing=0.0, props=None):
    """Object using mesh `me` at plan inches (x east, y south), facing in degrees: 0 = front looks south,
    90 = east, 180 = north, 270 = west."""
    ob = bpy.data.objects.new(name, me)
    ob.location = (x * IN, -y * IN, z * IN)
    ob.rotation_euler = (0, 0, math.radians(facing))
    coll.objects.link(ob)
    for k, v in (props or {}).items():
        ob[k] = v
    return ob


FACING = {'S': 0.0, 'E': 90.0, 'N': 180.0, 'W': 270.0}


def rounded_rect(x0, x1, y0, y1, r, segs=6):
    """Polygon points of a rounded rectangle (counter-clockwise)."""
    r = min(r, (x1 - x0) / 2 - 1e-3, (y1 - y0) / 2 - 1e-3)
    pts = []
    for cx, cy, a0 in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for k in range(segs + 1):
            a = math.radians(a0 + 90 * k / segs)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def ellipse(cx, cy, rx, ry, segs=48):
    return [(cx + rx * math.cos(2 * math.pi * k / segs), cy + ry * math.sin(2 * math.pi * k / segs)) for k in range(segs)]
