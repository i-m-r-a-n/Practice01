"""Bounding boxes of the Doors (hidden boolean cutters = openings) and Door Leaves collections for make_walk_grid.py.
blender -b Final_Office_Interior.blend --python export_door_boxes.py -- OUT_DIR   (writes OUT_DIR/door_boxes.json)"""
import json
import os
import sys

import bpy
from mathutils import Vector
out = []
for cn in ("Doors", "Door Leaves"):
    for o in bpy.data.collections[cn].all_objects:
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
        xs = [v.x for v in bb]; ys = [v.y for v in bb]; zs = [v.z for v in bb]
        out.append(dict(coll=cn, name=o.name, hide_render=o.hide_render, vis=o.visible_get(), x=[min(xs), max(xs)], z_south=[-max(ys), -min(ys)], h=[min(zs), max(zs)]))
json.dump(out, open(os.path.join(sys.argv[sys.argv.index("--") + 1], "door_boxes.json"), "w"), indent=0)
print("DOORS", len(out))
