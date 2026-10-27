"""Physically based material library - 'Green Thread' palette for the Stage II / Zara Fashion office.

Palette logic (from the client's own branding: green logos on white, black type; facade = grey + warm wood):
warm white walls, light white-oak joinery, smoked walnut for executive pieces, warm terrazzo for visitor
floors, charcoal carpet tiles for work floors, deep brand green (#26673D from the logo) as the accent,
black-anodised slim aluminium frames, brushed brass in small doses.
Textures: CC0 (Poly Haven / ambientCG), 1K, real-world tiling via metre UVs (see lib_mesh.MB.mesh).
"""
import math
import os

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'GARMENT_OFFICE_FINAL_PRESENTATION', '01_EDITABLE_3D', 'assets'))   # shared, read-only
TEX = os.path.join(ASSETS, 'textures')
BRAND = os.path.join(ASSETS, 'brand')

BRAND_GREEN = '#26673D'      # sampled from the client's logo (average of the green pixels)
DEEP_GREEN = '#1B4A2D'


def srgb(h):
    h = h.lstrip('#')
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)


def kelvin(t):
    """Approximate linear RGB of a blackbody at t kelvin (normalised)."""
    t = t / 100.0
    r = 255 if t <= 66 else 329.698727446 * ((t - 60) ** -0.1332047592)
    g = 99.4708025861 * math.log(t) - 161.1195681661 if t <= 66 else 288.1221695283 * ((t - 60) ** -0.0755148492)
    b = 255 if t >= 66 else (0 if t <= 19 else 138.5177312231 * math.log(t - 10) - 305.0447927307)
    c = [max(0, min(255, v)) / 255 for v in (r, g, b)]
    lin = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    m = max(lin)
    return tuple(x / m for x in lin)


def kelvin_soft(t, mix=0.55):
    """LED colour as seen after camera white balance: kelvin tint pulled toward neutral white."""
    k = kelvin(t)
    return tuple(c * (1 - mix) + mix for c in k)


M = {}


def _new(name):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    try:
        m.use_nodes = True
    except Exception:
        pass
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    out.location = (600, 0)
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (300, 0)
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    M[name] = m
    return m, nt, bsdf


def _img(nt, path, colorspace='sRGB', loc=(-400, 0)):
    n = nt.nodes.new('ShaderNodeTexImage')
    n.location = loc
    img = bpy.data.images.load(path, check_existing=True)
    img.colorspace_settings.name = colorspace
    n.image = img
    return n


def sock(node, name, kind='RGBA', out=False):
    """Socket by name and type (ShaderNodeMix has float/vector/colour sockets with the same names)."""
    for s in (node.outputs if out else node.inputs):
        if s.name == name and s.type == kind:
            return s
    return (node.outputs if out else node.inputs)[name]


def mix_rgb(nt, a, b_sock_or_col, mode='MULTIPLY', fac=1.0, loc=(-150, 0)):
    mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.blend_type = mode; mix.location = loc
    sock(mix, 'Factor', 'VALUE').default_value = fac
    nt.links.new(a, sock(mix, 'A'))
    if isinstance(b_sock_or_col, tuple):
        sock(mix, 'B').default_value = b_sock_or_col
    else:
        nt.links.new(b_sock_or_col, sock(mix, 'B'))
    return sock(mix, 'Result', out=True)


def find(folder, *keys):
    d = os.path.join(TEX, folder)
    for f in sorted(os.listdir(d)):
        if any(k in f for k in keys):
            return os.path.join(d, f)
    return None


def textured(name, folder, tile_m, tint=None, tint_mix=0.0, hsv=(0.5, 1.0, 1.0), rough=None, rough_mul=1.0,
             normal=0.6, rotate=0.0, metal=0.0, sheen=0.0, coat=0.0, grid=None, quarter=None, desat_to=None):
    """Image-textured PBR material. tile_m = real size of one texture repeat (metres).
    grid = (cell_m, line_m, darken) draws tile joints; quarter = cell_m alternates carpet-tile direction."""
    m, nt, b = _new(name)
    L = nt.links
    tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location = (-1200, 0)
    mp = nt.nodes.new('ShaderNodeMapping'); mp.location = (-1000, 0)
    mp.inputs['Scale'].default_value = (1 / tile_m, 1 / tile_m, 1)
    mp.inputs['Rotation'].default_value = (0, 0, math.radians(rotate))
    L.new(tc.outputs['UV'], mp.inputs['Vector'])
    vec = mp.outputs['Vector']
    col = _img(nt, find(folder, '_diff', '_Color'), 'sRGB', (-700, 250))
    L.new(vec, col.inputs['Vector'])
    c_out = col.outputs['Color']
    hs = nt.nodes.new('ShaderNodeHueSaturation'); hs.location = (-400, 250)
    hs.inputs['Hue'].default_value, hs.inputs['Saturation'].default_value, hs.inputs['Value'].default_value = hsv
    L.new(c_out, hs.inputs['Color'])
    c_out = hs.outputs['Color']
    if desat_to is not None:          # remap to a target colour keeping the texture's variation
        bw = nt.nodes.new('ShaderNodeRGBToBW'); bw.location = (-250, 400)
        L.new(c_out, bw.inputs['Color'])
        ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location = (-100, 400)
        lo, hi = desat_to
        ramp.color_ramp.elements[0].color = (*srgb(lo), 1)
        ramp.color_ramp.elements[1].color = (*srgb(hi), 1)
        L.new(bw.outputs['Val'], ramp.inputs['Fac'])
        c_out = ramp.outputs['Color']
    if tint is not None and tint_mix > 0:
        c_out = mix_rgb(nt, c_out, (*srgb(tint), 1), fac=tint_mix, loc=(-150, 250))
    if quarter:                        # carpet tiles laid quarter-turn: alternate value per tile
        ck = nt.nodes.new('ShaderNodeTexChecker'); ck.location = (-400, -450)
        ck.inputs['Scale'].default_value = 1.0
        mp2 = nt.nodes.new('ShaderNodeMapping'); mp2.location = (-600, -450)
        mp2.inputs['Scale'].default_value = (1 / quarter / 2, 1 / quarter / 2, 1)
        L.new(tc.outputs['UV'], mp2.inputs['Vector'])
        L.new(mp2.outputs['Vector'], ck.inputs['Vector'])
        ck.inputs['Color1'].default_value = (1, 1, 1, 1)
        ck.inputs['Color2'].default_value = (0.86, 0.86, 0.86, 1)
        c_out = mix_rgb(nt, c_out, ck.outputs['Color'], loc=(-100, 50))
    if grid:                           # tile joints (cell_w, line, dark[, cell_h])
        cell, line, dark = grid[:3]
        cell_h = grid[3] if len(grid) > 3 else cell
        br = nt.nodes.new('ShaderNodeTexBrick'); br.location = (-400, -250)
        br.offset, br.offset_frequency, br.squash, br.squash_frequency = 0.0, 1, 1.0, 1
        br.inputs['Scale'].default_value = 1.0
        br.inputs['Mortar Size'].default_value = line
        br.inputs['Brick Width'].default_value = cell
        br.inputs['Row Height'].default_value = cell_h
        br.inputs['Color1'].default_value = (1, 1, 1, 1)
        br.inputs['Color2'].default_value = (1, 1, 1, 1)
        br.inputs['Mortar'].default_value = (dark, dark, dark, 1)
        L.new(tc.outputs['UV'], br.inputs['Vector'])
        c_out = mix_rgb(nt, c_out, br.outputs['Color'], loc=(-100, -100))
    L.new(c_out, b.inputs['Base Color'])
    rp = find(folder, '_rough', '_Roughness')
    if rough is not None:
        b.inputs['Roughness'].default_value = rough
    elif rp:
        r = _img(nt, rp, 'Non-Color', (-700, -50))
        L.new(vec, r.inputs['Vector'])
        mm = nt.nodes.new('ShaderNodeMath'); mm.operation = 'MULTIPLY'; mm.location = (-400, -50)
        mm.inputs[1].default_value = rough_mul
        mm.use_clamp = True
        L.new(r.outputs['Color'], mm.inputs[0])
        L.new(mm.outputs['Value'], b.inputs['Roughness'])
    npth = find(folder, '_nor_gl', '_NormalGL')
    if npth and normal > 0:
        n = _img(nt, npth, 'Non-Color', (-700, -300))
        L.new(vec, n.inputs['Vector'])
        nm = nt.nodes.new('ShaderNodeNormalMap'); nm.location = (-400, -300)
        nm.inputs['Strength'].default_value = normal
        L.new(n.outputs['Color'], nm.inputs['Color'])
        L.new(nm.outputs['Normal'], b.inputs['Normal'])
    b.inputs['Metallic'].default_value = metal
    if sheen:
        b.inputs['Sheen Weight'].default_value = sheen
    if coat:
        b.inputs['Coat Weight'].default_value = coat
        b.inputs['Coat Roughness'].default_value = 0.08
    return m


def plain(name, hexcol, rough=0.6, metal=0.0, bump=0.0, bump_scale=200.0, sheen=0.0, coat=0.0, spec=0.5):
    m, nt, b = _new(name)
    b.inputs['Base Color'].default_value = (*srgb(hexcol), 1)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    b.inputs['Specular IOR Level'].default_value = spec
    if sheen:
        b.inputs['Sheen Weight'].default_value = sheen
    if coat:
        b.inputs['Coat Weight'].default_value = coat
        b.inputs['Coat Roughness'].default_value = 0.1
    if bump:
        tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location = (-800, -200)
        nz = nt.nodes.new('ShaderNodeTexNoise'); nz.location = (-550, -200)
        nz.inputs['Scale'].default_value = bump_scale
        nz.inputs['Detail'].default_value = 6
        nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
        bp = nt.nodes.new('ShaderNodeBump'); bp.location = (-250, -200)
        bp.inputs['Strength'].default_value = bump
        bp.inputs['Distance'].default_value = 0.001
        nt.links.new(nz.outputs['Fac'], bp.inputs['Height'])
        nt.links.new(bp.outputs['Normal'], b.inputs['Normal'])
    m.diffuse_color = (*srgb(hexcol), 1)
    return m


def glass(name, rough=0.0, tint='#F4FAF7', ior=1.45):
    m, nt, b = _new(name)
    b.inputs['Base Color'].default_value = (*srgb(tint), 1)
    b.inputs['Roughness'].default_value = rough
    b.inputs['Transmission Weight'].default_value = 1.0
    b.inputs['IOR'].default_value = ior
    m.diffuse_color = (*srgb(tint), 0.25)
    if hasattr(m, 'surface_render_method'):
        m.surface_render_method = 'DITHERED'
    return m


def emission(name, temp_k=3500, strength=6.0, hexcol=None):
    m, nt, b = _new(name)
    col = srgb(hexcol) if hexcol else kelvin_soft(temp_k)
    b.inputs['Base Color'].default_value = (*col, 1)
    b.inputs['Emission Color'].default_value = (*col, 1)
    b.inputs['Emission Strength'].default_value = strength
    b.inputs['Roughness'].default_value = 0.5
    m.diffuse_color = (*col, 1)
    return m


def image_decal(name, filename, emit=0.0, rough=0.4, metal=0.0):
    """Logo / graphic from assets/brand (RGBA). Alpha cut-out; optional backlight glow."""
    m, nt, b = _new(name)
    tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location = (-900, 0)
    im = _img(nt, os.path.join(BRAND, filename), 'sRGB', (-600, 0))
    im.extension = 'CLIP'
    nt.links.new(tc.outputs['UV'], im.inputs['Vector'])
    nt.links.new(im.outputs['Color'], b.inputs['Base Color'])
    nt.links.new(im.outputs['Alpha'], b.inputs['Alpha'])
    b.inputs['Roughness'].default_value = rough
    b.inputs['Metallic'].default_value = metal
    if emit:
        nt.links.new(im.outputs['Color'], b.inputs['Emission Color'])
        b.inputs['Emission Strength'].default_value = emit
    if hasattr(m, 'surface_render_method'):
        m.surface_render_method = 'DITHERED'
    return m


def screen_image(name, hexa, hexb, strength=1.2):
    """Lit display: soft vertical gradient between two brand colours (no invented content)."""
    m, nt, b = _new(name)
    tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location = (-900, 0)
    sep = nt.nodes.new('ShaderNodeSeparateXYZ'); sep.location = (-700, 0)
    nt.links.new(tc.outputs['Generated'], sep.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB'); ramp.location = (-500, 0)
    ramp.color_ramp.elements[0].color = (*srgb(hexa), 1)
    ramp.color_ramp.elements[1].color = (*srgb(hexb), 1)
    nt.links.new(sep.outputs['Z'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Emission Color'])
    b.inputs['Emission Strength'].default_value = strength
    b.inputs['Roughness'].default_value = 0.15
    return m


def build_library():
    """All materials used by the model. Names are referenced by the asset builders."""
    W = '#EEEBE4'                       # warm white wall paint (approx. RAL 9010 / NCS S 0502-Y)
    # ---------------- floors
    textured('fl_terrazzo', 'Terrazzo019M', 0.65, hsv=(0.5, 0.75, 1.12), rough_mul=0.55, normal=0.25, grid=(0.8 / 0.65 * 0.65, 0.004, 0.72))
    textured('fl_herringbone', 'herringbone_parquet', 3.4, hsv=(0.5, 0.78, 1.08), rough_mul=1.25, normal=0.5, coat=0.04)
    textured('fl_carpet', 'Fabric030', 0.35, desat_to=('#2B2D2F', '#4A4D50'), rough=0.97, normal=1.0, quarter=0.5)
    textured('fl_carpet_green', 'Fabric030', 0.35, desat_to=('#2A5539', '#3F6E50'), rough=0.97, normal=1.0, grid=(1.22, 0.05, 0.8, 50.0))
    textured('fl_oak_planks', 'laminate_floor_02', 1.7, hsv=(0.5, 0.75, 1.08), rough_mul=0.9, normal=0.4)
    textured('fl_concrete', 'smooth_concrete_floor', 2.0, desat_to=('#A9A6A0', '#CFCCC6'), rough_mul=0.5, normal=0.3)
    textured('fl_porcelain', 'Tiles040', 3.6, hsv=(0.5, 0.5, 1.0), rough_mul=0.5, normal=0.3)
    textured('wall_porcelain', 'Tiles040', 1.8, hsv=(0.5, 0.5, 1.02), rough_mul=0.4, normal=0.3)
    # ---------------- walls / ceiling
    plain('paint_white', W, rough=0.88, bump=0.05)
    plain('paint_ceiling', '#F2F1EC', rough=0.92)
    plain('paint_green', DEEP_GREEN, rough=0.85, bump=0.04)
    plain('paint_warmgrey', '#C9C3B8', rough=0.85, bump=0.04)
    plain('steel_painted', '#E9E8E3', rough=0.6)          # exposed beams / deck painted
    plain('steel_column', '#3A3D3F', rough=0.5, metal=0.2)
    plain('plinth', '#2B2D2C', rough=0.5)
    # ---------------- wood
    textured('oak', 'white_oak_veneer', 0.5, hsv=(0.5, 0.85, 1.12), rough_mul=0.85, normal=0.3, coat=0.1)
    textured('oak_slat', 'white_oak_veneer', 0.5, hsv=(0.5, 0.9, 1.05), rough_mul=0.9, normal=0.3, rotate=90)
    textured('walnut', 'natural_walnut_veneer', 1.0, tint='#6B4A33', tint_mix=0.85, hsv=(0.5, 1.0, 0.95), rough_mul=0.8, normal=0.3, coat=0.25)
    # ---------------- stone / solid surfaces
    textured('stone_white', 'Tiles043', 1.6, hsv=(0.5, 0.6, 1.0), rough_mul=0.35, normal=0.15, coat=0.3)
    textured('terrazzo_counter', 'Terrazzo019M', 0.5, hsv=(0.5, 0.75, 1.15), rough_mul=0.35, normal=0.2, coat=0.3)
    # ---------------- metals
    plain('alu_black', '#1E1F21', rough=0.38, metal=0.75)
    plain('alu_silver', '#BFC2C4', rough=0.3, metal=1.0)
    plain('metal_black', '#151617', rough=0.45, metal=0.4)
    plain('brass', '#B08A4E', rough=0.32, metal=1.0)
    plain('chrome', '#D9DBDD', rough=0.08, metal=1.0)
    # ---------------- glass
    glass('glass_clear', 0.0)
    glass('glass_frosted', 0.32, tint='#F7FAF8')
    plain('mirror', '#E8EAEA', rough=0.02, metal=1.0)
    # ---------------- textiles / upholstery
    textured('fab_charcoal', 'Fabric030', 0.25, hsv=(0.5, 0.5, 0.75), rough=0.9, normal=0.8, sheen=0.4)
    textured('fab_green', 'Fabric030', 0.25, desat_to=('#2E5A40', '#4E7D60'), rough=0.9, normal=0.8, sheen=0.2)
    textured('fab_sand', 'Fabric030', 0.25, desat_to=('#B9A98E', '#DCCFB8'), rough=0.92, normal=0.8, sheen=0.2)
    textured('fab_grey', 'Fabric030', 0.25, desat_to=('#5E5F60', '#8B8C8D'), rough=0.92, normal=0.8, sheen=0.4)
    textured('rug_wool', 'Fabric030', 0.6, desat_to=('#8E877B', '#CBC4B7'), rough=0.95, normal=1.0, sheen=0.5)
    textured('felt_green', 'Fabric034', 0.4, desat_to=('#2C5A3F', '#477A5B'), rough=0.95, normal=0.6)
    textured('felt_grey', 'Fabric034', 0.4, hsv=(0.5, 0.5, 0.95), rough=0.95, normal=0.6)
    textured('leather_cognac', 'leather_white', 0.3, tint='#8A5A36', tint_mix=1.0, hsv=(0.5, 1.0, 1.0), rough_mul=0.8, normal=0.5)
    textured('leather_black', 'leather_white', 0.3, tint='#202020', tint_mix=1.0, rough_mul=0.7, normal=0.5)
    plain('mesh_black', '#1A1A1A', rough=0.7)              # task chair mesh back
    plain('rubber', '#121212', rough=0.8)
    plain('plastic_white', '#F2F2F0', rough=0.45)
    plain('plastic_dark', '#2A2B2C', rough=0.5)
    plain('ceramic_white', '#F4F4F2', rough=0.12, coat=0.4)
    plain('porcelain', '#F7F7F5', rough=0.08, coat=0.5)
    plain('paper', '#F5F3EE', rough=0.9)
    plain('cork', '#B98C5E', rough=0.95, bump=0.4, bump_scale=600)
    plain('pinboard_linen', '#E3DED3', rough=0.95, bump=0.15, bump_scale=900)
    plain('mannequin', '#F1EFEA', rough=0.55)
    plain('soil', '#3A2C22', rough=1.0)
    plain('leaf', '#3F6B3A', rough=0.6, sheen=0.2)
    # garments on display (fabric colours only; no product claims)
    for k, h in (('g_navy', '#26324A'), ('g_white', '#ECEAE4'), ('g_heather', '#9A9A98'), ('g_olive', '#5D6447'),
                 ('g_sand', '#C8B595'), ('g_black', '#1C1C1E'), ('g_denim', '#3D5573'), ('g_rust', '#9A5136'),
                 ('g_sage', '#8EA58F'), ('g_blush', '#D9B4A6'), ('g_green', '#2F6B45')):
        plain(k, h, rough=0.9, sheen=0.5, bump=0.12, bump_scale=1500)
    # ---------------- displays / light emitters / branding
    plain('screen_off', '#0B0C0D', rough=0.08, coat=0.6)
    screen_image('screen_brand', '#0F2E1D', '#2E7A4B', 1.0)
    screen_image('screen_ui', '#E8ECEA', '#C9D6CE', 0.9)
    emission('led_3000', 3000, 12.0)
    emission('led_3500', 3500, 12.0)
    emission('led_4000', 4000, 12.0)
    emission('led_soft', 3500, 3.0)
    emission('lightbox', 5000, 2.5)
    image_decal('logo_zf', 'logo_zara_fashion_profile_sign.png', emit=0.0, rough=0.35)
    image_decal('logo_s2_ltd', 'logo_stage2_ltd_sign.png', emit=0.0, rough=0.35)
    image_decal('logo_s2_unit1', 'logo_stage2_unit1_sign.png', emit=0.0, rough=0.35)
    image_decal('tagline', 'tagline_quality_compliance_commitment_sign.png', emit=0.0, rough=0.4)
    plain('cutter', '#FF2020', rough=1.0)
    plain('dim', '#111111', rough=1.0)
    plain('label', '#0E4A2A', rough=1.0)
    return M
