"""Woven Light concept: applies the proposal to a COPY of the Z06 / Z07 option B model.

blender -b ../GARMENT_OFFICE_SPACE_OPTIMIZATION/02_IMPROVED_BLENDER_MODEL/Optimized_Office_Interior.blend \
        --python scripts/woven_light.py -- after|before OUT.blend CARD.png

after  = the proposal (materials, joinery, water point, blinds) + the new water-point camera
before = the unchanged model + only the new water-point camera (for a matched "before" view)
The source .blend is never saved over. Blender axes: x = plan x, y = -plan y (metres).
"""
import bpy, bmesh, math, sys

argv = sys.argv[sys.argv.index('--') + 1:]
MODE, OUT, CARD = argv[0], argv[1], argv[2]
assert MODE in ('after', 'before')
OB = bpy.data.objects

coll = bpy.data.collections.new('Woven_Light_Proposal')
bpy.context.scene.collection.children.link(coll)


def box(name, cx, cy, z0, sx, sy, sz, mat, rz=0.0):
    """Axis-aligned box: centre (cx, cy), from z0 up, size (sx, sy, sz)."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=bm.verts)
    bmesh.ops.translate(bm, vec=(0, 0, sz / 2), verts=bm.verts)
    bm.to_mesh(me); bm.free()
    uv = me.uv_layers.new()
    for p in me.polygons:                      # simple box projection so textures read at real scale
        n = p.normal
        for li in p.loop_indices:
            v = me.vertices[me.loops[li].vertex_index].co
            a, b = ((v.y, v.z) if abs(n.x) > 0.5 else (v.x, v.z) if abs(n.y) > 0.5 else (v.x, v.y))
            uv.data[li].uv = (a + cx, b)
    o = bpy.data.objects.new(name, me)
    o.location = (cx, cy, z0); o.rotation_euler = (0, 0, rz)
    me.materials.append(mat)
    coll.objects.link(o)
    return o


def cyl(name, cx, cy, z0, r, h, mat, seg=24):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=h)
    bmesh.ops.translate(bm, vec=(0, 0, h / 2), verts=bm.verts)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); o.location = (cx, cy, z0)
    me.materials.append(mat); coll.objects.link(o)
    return o


def half_sphere(name, cx, cy, z0, r, mat):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=20, v_segments=10, radius=r)
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.z < -1e-4], context='VERTS')
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); o.location = (cx, cy, z0)
    me.materials.append(mat); coll.objects.link(o)
    return o


def hide(prefixes):
    for o in OB:
        if any(o.name.startswith(p) for p in prefixes):
            o.hide_render = True; o.hide_set(True) if o.name in bpy.context.view_layer.objects else None
            for c in o.children_recursive:
                c.hide_render = True


def swap(old, new):
    for o in OB:
        if o.type == 'MESH':
            for s in o.material_slots:
                if s.material and s.material.name == old:
                    s.material = new


def ramp_material(src, name, dark, light):
    """Copy a textured felt material (image -> BW -> ramp) and recolour its ramp."""
    m = bpy.data.materials[src].copy(); m.name = name
    r = next(n for n in m.node_tree.nodes if n.type == 'VALTORGB')
    r.color_ramp.elements[0].color = (*dark, 1)
    r.color_ramp.elements[-1].color = (*light, 1)
    return m


def flat(name, rgb, rough=0.6, emit=None, strength=0.0, transmission=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*rgb, 1)
    p.inputs['Roughness'].default_value = rough
    if emit:
        p.inputs['Emission Color'].default_value = (*emit, 1)
        p.inputs['Emission Strength'].default_value = strength
    if transmission:
        p.inputs['Transmission Weight'].default_value = transmission
    return m


def image_material(name, path):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; p = nt.nodes['Principled BSDF']
    t = nt.nodes.new('ShaderNodeTexImage'); t.image = bpy.data.images.load(path)
    nt.links.new(t.outputs['Color'], p.inputs['Base Color'])
    p.inputs['Roughness'].default_value = 0.7
    return m


def camera(name, loc, target, lens=18.0):
    cam = bpy.data.cameras.new(name); cam.lens = lens; cam.clip_start = 0.05
    o = bpy.data.objects.new(name, cam); o.location = loc
    dx, dy, dz = (target[i] - loc[i] for i in range(3))
    o.rotation_euler = (math.pi / 2 + math.atan2(dz, math.hypot(dx, dy)), 0, math.atan2(-dx, dy))
    cams = bpy.data.collections.get('Cameras') or coll
    cams.objects.link(o)
    return o


# The water-point camera exists in both versions so the before / after pair matches exactly.
# Visitor passage Z03 spans plan x 367-420 in, y -10 to -214 in -> x 9.32-10.67 m, y 0.25-5.44 m.
camera('CAM_WL_Water_Point', (9.45, 0.62, 1.50), (10.60, 2.95, 1.05))

if MODE == 'after':
    M = bpy.data.materials
    oak, paper, chrome, glass = M['oak'], M['paper'], M['chrome'], M['glass_clear']
    # ---- one timber, woven upholstery, no brass, no leather
    swap('walnut', oak)
    swap('brass', oak)
    swap('leather_black', M['fab_sand'])
    swap('leather_cognac', M['fab_sand'])
    # ---- jute (acoustic + pin-up) and an oat felt replacing the large green ceiling rafts
    jute = ramp_material('felt_green', 'wl_jute', (0.20, 0.13, 0.055), (0.48, 0.36, 0.19))
    oat = ramp_material('felt_green', 'wl_felt_oat', (0.42, 0.37, 0.29), (0.66, 0.60, 0.50))
    swap('paint_green', jute)            # Experience Centre bay backs
    swap('pinboard_linen', jute)          # studio mood-board wall
    swap('felt_green', oat)
    # ---- lighter carpet tile (proposed at the next renewal)
    car = M['fl_carpet'].node_tree.nodes
    rp = next(n for n in car if n.type == 'VALTORGB').color_ramp
    rp.elements[0].color = (0.16, 0.15, 0.13, 1); rp.elements[-1].color = (0.33, 0.31, 0.28, 1)
    stitch = flat('wl_kantha_stitch', (0.62, 0.16, 0.10), 0.8)          # madder-red running stitch
    linen = flat('wl_linen_ground', (0.80, 0.75, 0.66), 0.85)
    light_box = flat('wl_lightbox_d65', (0.9, 0.9, 0.9), 0.4, emit=(0.95, 0.97, 1.0), strength=6.0)
    blind = flat('wl_blind', (0.83, 0.79, 0.71), 0.9, transmission=0.35)
    shell = flat('wl_coconut_shell', (0.16, 0.085, 0.04), 0.55)
    swatches = [M[n] for n in ('g_sand', 'g_navy', 'g_sage', 'g_rust', 'g_heather', 'g_white', 'g_olive', 'g_denim', 'g_blush', 'g_green')]

    # ---- RECEPTION Z02: one story, a Jamdani-inspired screen; halo and extra planters removed
    hide(['FIN03 ', 'LT006 ', 'F004 ', 'PL004 ', 'F015 ', 'PL015 ', 'F016 ', 'PL016 '])
    xs = 14.29                                         # face of the east wall behind the counter
    box('WL Reception screen ground (linen)', xs, -4.06, 0.0, 0.02, 4.06, 2.79, linen)
    n = 120                                            # fine timber warp, like a muslin ground
    for i in range(n):
        y = -6.09 + (i + 0.5) * 4.06 / n
        box(f'WL Reception screen warp {i:03d}', xs - 0.03, y, 0.0, 0.03, 0.014, 2.79, oak)
    motifs = [(-5.70, 0.55), (-4.70, 0.55), (-3.40, 0.55), (-2.40, 0.55), (-5.20, 2.25), (-2.90, 2.25),
              (-6.00, 1.40), (-2.15, 1.40), (-4.06, 2.45)]        # sparse butis, kept clear of the logo
    for k, (y, z) in enumerate(motifs):
        o = box(f'WL Reception buti {k}', xs - 0.06, y, z - 0.06, 0.03, 0.085, 0.085, oak)
        o.rotation_euler = (math.radians(45), 0, 0)
        o.location.z = z
    # ---- EXPERIENCE CENTRE Z30: from showroom to library
    hide(['F021 ', 'F022 ', 'F023 ', 'F024 ', 'F025 ', 'F029 ', 'PL029 '])
    tx, ty = 12.70, 8.51                                # the old plinth's footprint
    box('WL EC handling table top', tx, ty, 0.88, 2.44, 1.00, 0.04, oak)
    for dx in (-1.05, 1.05):
        box(f'WL EC handling table leg {dx:+.0f}', tx + dx, ty, 0.0, 0.06, 0.86, 0.88, oak)
    for k in range(10):                                # swatches laid out for handling
        sx, sy = tx - 1.0 + (k % 5) * 0.34, ty - 0.22 + (k // 5) * 0.36
        box(f'WL EC swatch {k}', sx, sy, 0.92, 0.26, 0.30, 0.006 + 0.002 * (k % 3), swatches[k])
    # component story on a tray: coconut shell -> button blanks -> finished buttons on a garment panel
    box('WL EC component tray', tx + 0.80, ty + 0.05, 0.92, 0.50, 0.34, 0.015, oak)
    half_sphere('WL EC coconut shell half', tx + 0.64, ty + 0.05, 0.935, 0.07, shell)
    for k in range(4):
        cyl(f'WL EC button blank {k}', tx + 0.80, ty - 0.06 + k * 0.05, 0.935, 0.016, 0.006, shell)
    box('WL EC garment panel', tx + 0.95, ty + 0.05, 0.935, 0.14, 0.24, 0.004, M['g_sand'])
    for k in range(3):
        cyl(f'WL EC finished button {k}', tx + 0.95, ty - 0.03 + k * 0.08, 0.939, 0.009, 0.004, shell)
    # colour-assessment lightbox at the table end (separate from the warm ambient light)
    box('WL EC lightbox body', tx + 1.55, ty, 0.0, 0.60, 0.50, 1.40, M['plastic_white'])
    box('WL EC lightbox glow', tx + 1.55, ty - 0.24, 0.95, 0.52, 0.02, 0.40, light_box)
    # ---- BOARDROOM Z08: three joinable tables; jute pin-up wall half hidden by a sliding panel
    hide(['F031 ', 'FIN07 '])
    for k, cx in enumerate((15.12, 17.15, 19.18)):
        box(f'WL Boardroom table {k} top', cx, 2.84, 0.71, 1.98, 1.19, 0.04, oak)
        box(f'WL Boardroom table {k} leg a', cx - 0.80, 2.84, 0.0, 0.06, 0.90, 0.71, oak)
        box(f'WL Boardroom table {k} leg b', cx + 0.80, 2.84, 0.0, 0.06, 0.90, 0.71, oak)
    box('WL Boardroom jute pin-up wall', 19.49, 0.32, 0.0, 4.85, 0.03, 2.74, jute)
    for k in range(5):                                  # neutral critique sheets, no content
        box(f'WL Boardroom pinned sheet {k}', 17.45 + k * 0.42, 0.35, 1.25 + 0.18 * (k % 2), 0.30, 0.004, 0.42, paper)
    box('WL Boardroom sliding oak panel', 20.71, 0.37, 0.0, 2.42, 0.04, 2.74, oak)
    box('WL Boardroom sample trolley', 20.55, 4.65, 0.0, 0.80, 0.48, 0.90, oak)
    for k in range(3):
        box(f'WL Boardroom trolley fabric {k}', 20.55, 4.65, 0.92 + k * 0.03, 0.42, 0.30, 0.028, swatches[k + 2])
    # ---- MD OFFICE Z12: development shelf instead of the feature wall; halo removed
    hide(['FIN08 ', 'LT054 '])
    box('WL MD jute wall', 25.43, -6.27, 0.0, 3.61, 0.03, 2.59, jute)
    for k, z in enumerate((1.05, 1.45, 1.85)):
        box(f'WL MD shelf {k}', 24.30, -6.13, z, 1.10, 0.26, 0.03, oak)
        for j in range(3):
            box(f'WL MD folded sample {k}{j}', 23.95 + j * 0.33, -6.13, z + 0.03, 0.26, 0.22, 0.05 + 0.02 * j, swatches[(k * 3 + j) % 10])
    # ---- GLOBAL DESIGN STUDIO Z18: diffusing blinds on the east windows; kantha seams on the jute wall
    for o in list(OB):
        if o.name[:3] in ('W06', 'W07', 'W08', 'W09', 'W10') and ' glass' in o.name:
            w = o.dimensions.y; top = o.location.z + o.dimensions.z
            box(f'WL Studio blind {o.name[:3]}', o.location.x - 0.10, o.location.y, top - 0.55, 0.01, w, 0.55, blind)
    for k in range(6):                                  # running-stitch seams between jute panels
        for j in range(30):
            box(f'WL Studio kantha stitch {k}-{j:02d}', 29.33, 23.2 + k * 1.22, 0.15 + j * 0.085, 0.006, 0.006, 0.04, stitch)
    # ---- WATER & WELLBEING Z03: niche on the wall shared with the guest WCs
    fx, ny = 10.67, 2.80                                # wall face, niche centre (between the two WC doors)
    box('WL Water niche back (jute)', fx - 0.01, ny, 0.0, 0.02, 1.20, 2.20, jute)
    box('WL Water niche side a', fx - 0.14, ny - 0.62, 0.0, 0.26, 0.04, 2.20, oak)
    box('WL Water niche side b', fx - 0.14, ny + 0.62, 0.0, 0.26, 0.04, 2.20, oak)
    box('WL Water niche head', fx - 0.14, ny, 2.16, 0.26, 1.28, 0.04, oak)
    box('WL Water cabinet', fx - 0.14, ny, 0.0, 0.26, 1.20, 0.90, oak)
    box('WL Water ledge (terrazzo-look)', fx - 0.15, ny, 0.90, 0.30, 1.22, 0.04, M['terrazzo_counter'])
    cyl('WL Water tap column', fx - 0.08, ny - 0.25, 0.94, 0.015, 0.26, chrome)
    box('WL Water tap spout', fx - 0.14, ny - 0.25, 1.17, 0.13, 0.025, 0.025, chrome)
    box('WL Water drip tray', fx - 0.14, ny - 0.25, 0.94, 0.18, 0.22, 0.012, M['alu_silver'])
    box('WL Water glass shelf', fx - 0.12, ny, 1.45, 0.22, 1.10, 0.03, oak)
    for k in range(6):
        cyl(f'WL Water tumbler {k}', fx - 0.12, ny - 0.40 + k * 0.16, 1.48, 0.034, 0.10, glass)
    box('WL Water used-glass tray', fx - 0.15, ny + 0.32, 0.94, 0.26, 0.34, 0.02, oak)
    cyl('WL Water used tumbler', fx - 0.15, ny + 0.28, 0.96, 0.034, 0.10, glass)
    box('WL Water record card frame', fx - 0.015, ny + 0.95, 1.20, 0.025, 0.36, 0.50, oak)
    card = image_material('wl_water_card', CARD)
    o = box('WL Water record card', fx - 0.03, ny + 0.95, 1.225, 0.004, 0.31, 0.45, card)
    me = o.data; uv = me.uv_layers.active                     # map the card image straight onto the -x face
    for p in me.polygons:
        for li in p.loop_indices:
            v = me.vertices[me.loops[li].vertex_index].co
            uv.data[li].uv = (0.5 - v.y / 0.31, v.z / 0.45)
    lamp = bpy.data.lights.new('WL Water niche light', 'AREA'); lamp.size = 0.5; lamp.energy = 25; lamp.color = (1.0, 0.93, 0.84)
    lo = bpy.data.objects.new('WL Water niche light', lamp); lo.location = (fx - 0.35, ny, 2.40); coll.objects.link(lo)

bpy.ops.wm.save_as_mainfile(filepath=OUT, copy=True)
print('SAVED', MODE, OUT, len(coll.objects), 'proposal objects')
