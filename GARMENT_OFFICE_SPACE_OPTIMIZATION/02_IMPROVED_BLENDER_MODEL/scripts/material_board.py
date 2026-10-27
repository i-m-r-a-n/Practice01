"""Render a material board from the model's own PBR materials.
blender -b --factory-startup --python material_board.py -- OUT.jpg"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bpy  # noqa: E402

import lib_materials as LM  # noqa: E402
from lib_mesh import MB  # noqa: E402

OUT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "material_board.jpg"
bpy.ops.wm.read_factory_settings(use_empty=True)
M = LM.build_library()
TILES = [("TZ-01", "fl_terrazzo", "Terrazzo floor"), ("WD-01", "fl_herringbone", "Oak herringbone"), ("CP-01", "fl_carpet", "Carpet tile"),
         ("WD-02", "fl_oak_planks", "Oak-look plank"), ("PT-01", "fl_porcelain", "Porcelain tile"),
         ("WO-01", "oak_slat", "White-oak slats"), ("WO-02", "walnut", "Smoked walnut"), ("SS-01", "terrazzo_counter", "Quartz / terrazzo top"),
         ("PA-01", "paint_white", "Warm white paint"), ("PA-02", "paint_green", "Brand green"),
         ("UP-01", "fab_sand", "Sand fabric"), ("UP-01", "fab_green", "Green fabric"), ("UP-02", "leather_cognac", "Cognac leather"),
         ("AC-01", "felt_green", "Acoustic felt"), ("MT-02", "brass", "Brushed brass")]
sc = bpy.context.scene
col = bpy.data.collections.new("Board")
sc.collection.children.link(col)
size, gap, cols = 18, 4, 5                     # inches
for i, (code, mat, name) in enumerate(TILES):
    r, c = divmod(i, cols)
    x = (c - (cols - 1) / 2) * (size + gap)
    y = ((3 - 1) / 2 - r) * (size + gap + 5)
    m = MB()
    if mat == "oak_slat":
        m.box(-size / 2, size / 2, -size / 2, size / 2, 0, 0.6, "plinth")
        k = -size / 2
        while k < size / 2 - 1:
            m.box(k, k + 1.8, -size / 2, size / 2, 0.6, 1.6, mat, bevel=0.15)
            k += 3
    else:
        m.box(-size / 2, size / 2, -size / 2, size / 2, 0, 1.0, mat, bevel=0.12)
    ob = bpy.data.objects.new(code + " " + name, m.mesh(code, M))
    ob.location = (x * 0.0254, y * 0.0254, 0)
    col.objects.link(ob)
    cu = bpy.data.curves.new("t" + str(i), "FONT")
    cu.body = f"{code}  {name}"
    cu.size = 1.7 * 0.0254
    cu.align_x = "CENTER"
    cu.materials.append(M["dim"])
    t = bpy.data.objects.new("label" + str(i), cu)
    t.location = (x * 0.0254, (y - size / 2 - 3.0) * 0.0254, 0.02)
    col.objects.link(t)
bg = MB().box(-80, 80, -60, 60, -1, 0, "paint_white")
bgo = bpy.data.objects.new("bg", bg.mesh("bg", M))
col.objects.link(bgo)
cam = bpy.data.objects.new("cam", bpy.data.cameras.new("cam"))
cam.data.type = "ORTHO"
cam.data.ortho_scale = 2.95
cam.location = (0, -0.05, 3)
col.objects.link(cam)
sc.camera = cam
ld = bpy.data.lights.new("key", "AREA")
ld.energy, ld.size = 260, 2.0
key = bpy.data.objects.new("key", ld)
key.location = (-1.4, -1.0, 2.2)
key.rotation_euler = (math.radians(35), math.radians(-30), 0)
col.objects.link(key)
fd = bpy.data.lights.new("fill", "AREA")
fd.energy, fd.size = 90, 3.0
fill = bpy.data.objects.new("fill", fd)
fill.location = (1.5, 0.8, 2.5)
fill.rotation_euler = (math.radians(-20), math.radians(25), 0)
col.objects.link(fill)
w = bpy.data.worlds.new("w")
sc.world = w
w.use_nodes = True
w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.4
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = 64
sc.cycles.use_denoising = True
sc.view_settings.view_transform = "AgX"
sc.render.resolution_x, sc.render.resolution_y = 1600, 1330
sc.render.image_settings.file_format = "JPEG"
sc.render.image_settings.quality = 92
sc.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("BOARD", OUT)
