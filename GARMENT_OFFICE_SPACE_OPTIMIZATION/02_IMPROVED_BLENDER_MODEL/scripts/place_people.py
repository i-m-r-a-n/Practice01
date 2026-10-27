"""Illustrative staff for the Cycles stills of the redesigned Z06 / Z07 (render-time only; the editable model and the
web GLB stay without people).

blender -b Optimized_Office_Interior.blend --python place_people.py -- [--save OUT.blend] [--then render_views.py args...]

Characters: fictional CC0 MakeHuman adults prepared by GPT for the realism upgrade (people_assets/, provenance in
LICENSES.md). Poses: people_assets/poses.json, applied exactly like people-layer.js (bone rotation = rest x pose,
seated pelvis on the chair's seat top). Positions come from the option B chairs and work points, so every person
sits on a real chair or stands at a real counter. People shown are illustrative, not employees.
"""
import json
import math
import os
import struct
import sys

import bpy
from mathutils import Matrix, Quaternion, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
PA = os.path.join(HERE, "..", "people_assets")
IN = 0.0254
C = Matrix(((1, 0, 0, 0), (0, 0, -1, 0), (0, 1, 0, 0), (0, 0, 0, 1)))        # glTF (x, y, z) -> Blender (x, -z, y)
SEAT = {"task": 0.49022, "visitor": 0.48768, "exec": 0.50292}                # seat tops of the model's chairs (m)
POSES = json.load(open(os.path.join(PA, "poses.json")))

# (id, outfit, pose, plan x, plan y, facing deg (0 = south, 90 east), seat kind or None, skin, top tint, lower tint)
PEOPLE = [
    # Z07 merchandising
    ("m01", "shirt", "typing", 461.5, -566.0, 180, "task", "#b88b69", "#637b76", "#25313c"),
    ("m02", "salwar", "notes", 571.5, -566.0, 180, "task", "#ddbaa4", "#ad9271", "#30363d"),
    ("m03", "panjabi", "typing", 516.5, -768.0, 0, "task", "#d5b6a0", "#8a9bb2", "#424039"),
    ("m04", "salwar_braid", "show_sample", 652.0, -655.0, 90, None, "#c69d7b", "#9e7788", "#25313c"),
    ("m05", "shirt", "browsing", 748.0, -640.0, 270, None, "#c69d7b", "#9e7788", "#424039"),
    ("m06", "panjabi", "listening", 736.0, -495.0, 270, "task", "#b88b69", "#738866", "#25313c"),
    ("m07", "salwar", "presenting", 664.0, -470.0, 135, None, "#d5b6a0", "#8a9bb2", "#30363d"),
    ("m08", "shirt", "fabric", 700.0, -776.0, 180, None, "#ddbaa4", "#b9a895", "#424039"),
    # Z06 commercial & accounts
    ("a01", "panjabi", "typing", 172.5, -571.5, 180, "task", "#d5b6a0", "#a8bbcd", "#30363d"),
    ("a02", "salwar_braid", "notes", 266.5, -456.5, 180, "task", "#c69d7b", "#a98a76", "#424039"),
    ("a03", "shirt", "typing", 219.5, -658.5, 0, "task", "#b88b69", "#7f8f9e", "#25313c"),
    ("a04", "salwar", "listening", 311.0, -312.0, 0, "visitor", "#ddbaa4", "#9fb3a6", "#30363d"),
    ("a05", "shirt", "notes", 311.0, -256.0, 180, "visitor", "#c69d7b", "#8c8f99", "#25313c"),
    ("a06", "panjabi", "browsing", 217.0, -277.0, 0, None, "#b88b69", "#b9a895", "#424039"),
]


def glb_json(path):
    with open(path, "rb") as f:
        head = f.read(20)
        n = struct.unpack("<I", head[12:16])[0]
        return json.loads(f.read(n))


def trs(node, rot=None):
    t = Vector(node.get("translation", (0, 0, 0)))
    r = rot if rot is not None else node.get("rotation", (0, 0, 0, 1))
    q = Quaternion((r[3], r[0], r[1], r[2]))
    s = node.get("scale", (1, 1, 1))
    return Matrix.Translation(t) @ q.to_matrix().to_4x4() @ Matrix.Diagonal((s[0], s[1], s[2], 1))


def fk(js, pose, root_y):
    """World matrices (glTF space) of every named node at rest and posed (root group lifted by root_y)."""
    nodes = js["nodes"]
    rest, posed = {}, {}
    lift = Matrix.Translation((0, root_y, 0))

    def walk(i, wr, wp):
        n = nodes[i]
        name = n.get("name", str(i))
        lr = trs(n)
        if name in pose:
            r = n.get("rotation", (0, 0, 0, 1))
            base = Quaternion((r[3], r[0], r[1], r[2]))
            v = pose[name]
            q = base @ Quaternion((v[0], v[1], v[2], v[3]))
            lp = trs(n, (q.x, q.y, q.z, q.w))
        else:
            lp = lr
        rest[name], posed[name] = wr @ lr, wp @ lp
        for c in n.get("children", []):
            walk(c, rest[name], posed[name])
    for r in js["scenes"][0]["nodes"]:
        walk(r, Matrix.Identity(4), lift)
    return rest, posed


def tint(mat, hexcol):
    if not hexcol:
        return
    col = tuple(int(hexcol[i:i + 2], 16) / 255 for i in (1, 3, 5)) + (1.0,)
    col = tuple(c ** 2.2 if k < 3 else c for k, c in enumerate(col))                  # sRGB -> linear
    nt = mat.node_tree
    bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if not bsdf:
        return
    inp = bsdf.inputs["Base Color"]
    if inp.is_linked:
        src = inp.links[0].from_socket
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type, mix.blend_type = "RGBA", "MULTIPLY"
        mix.inputs[0].default_value = 1.0
        nt.links.new(src, mix.inputs[6])
        mix.inputs[7].default_value = col
        nt.links.new(mix.outputs[2], inp)
    else:
        inp.default_value = tuple(a * b for a, b in zip(inp.default_value, col))


def add_person(pid, outfit, pose_name, x, y, facing, seat, skin, top, lower, coll):
    path = os.path.join(PA, f"{outfit}.glb")
    js = glb_json(path)
    lib = POSES[outfit]
    key = f"{pose_name}__seat_{int(round(SEAT[seat] * 1e5))}" if seat else pose_name
    p = lib.get(key) or lib[pose_name]
    root_y = (SEAT[seat] - (p.get("seatTopY", .49) - p.get("rootY", 0))) if seat else 0.01016 + p.get("rootY", 0)
    rest, posed = fk(js, p["bones"], root_y)
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    for o in list(new):
        if (o.name.startswith("LOD1_") or "Long_modest_tunic" in o.name    # tunic drape is not skinned for these poses
                or (o.type == "MESH" and o.parent is None)):              # the importer's bone-display icosphere
            bpy.data.objects.remove(o, do_unlink=True)
            new.remove(o)
    arm = next(o for o in new if o.type == "ARMATURE")
    bpy.context.view_layer.update()
    # pose: world-space delta of every bone (glTF FK) applied to the imported rest bones, parents first
    order = sorted(arm.pose.bones, key=lambda b: len(b.parent_recursive))
    for pb in order:
        nm = pb.name
        if nm not in rest:
            continue
        d = C @ posed[nm] @ rest[nm].inverted() @ C.inverted()
        target = d @ arm.matrix_world @ pb.bone.matrix_local
        pb.matrix = arm.matrix_world.inverted() @ target
        bpy.context.view_layer.update()
    # whole-figure lift (pelvis on the seat) is the root group translation in people-layer.js
    holder = bpy.data.objects.new(f"Person {pid} ({pose_name}, illustrative)", None)
    coll.objects.link(holder)
    for o in new:
        for c in o.users_collection:
            c.objects.unlink(o)
        coll.objects.link(o)
        if o.parent is None:
            o.parent = holder
        if o.type == "MESH":
            mats = []
            for slot in o.material_slots:
                m = slot.material.copy()
                m.name = f"{slot.material.name} {pid}"
                if "Skin" in m.name:
                    tint(m, skin)
                elif "Garment_top" in m.name:
                    tint(m, top)
                elif "trousers" in m.name:
                    tint(m, lower)
                slot.material = m
                mats.append(m)
    holder.location = (x * IN, -y * IN, 0)
    holder.rotation_euler = (0, 0, math.radians(facing))
    holder["illustrative_person"] = True
    return holder


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    coll = bpy.data.collections.get("People (illustrative)") or bpy.data.collections.new("People (illustrative)")
    if coll.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(coll)
    only = os.environ.get("PEOPLE_ONLY")
    for row in PEOPLE:
        if only and row[0] not in only.split(","):
            continue
        add_person(*row, coll)
        print("PERSON", row[0], row[1], row[2], flush=True)
    if "--save" in argv:
        bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(argv[argv.index("--save") + 1]), compress=True)
    if "--then" in argv:
        rest_args = argv[argv.index("--then") + 1:]
        script = os.path.join(HERE, rest_args[0])
        sys.argv = [sys.argv[0], "--"] + rest_args[1:]
        exec(compile(open(script).read(), script, "exec"), {"__name__": "__main__", "__file__": script})


main()
