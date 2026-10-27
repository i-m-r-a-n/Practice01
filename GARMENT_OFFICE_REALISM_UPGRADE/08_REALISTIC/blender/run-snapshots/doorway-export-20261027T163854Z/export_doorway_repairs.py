"""Export six named repaired frame nodes from the unchanged approved-file copy."""
import argparse
import bpy
import hashlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from doorway_repairs import apply_doorway_repairs

parser = argparse.ArgumentParser()
parser.add_argument('--output-root', type=Path)
args = parser.parse_args(sys.argv[sys.argv.index('--') + 1:])
root = Path(os.environ.get('OFFICE_PROJECT_ROOT', str(Path(__file__).resolve().parents[3])))
out = args.output_root or root / 'GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/lighting-v2'
out.mkdir(parents=True, exist_ok=True)
source = root / 'GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/Final_Office_Interior.blend'
source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
assert source_hash == 'fa3ed3d58f6d44c3554e3761307841b96115ff7816e4e541c8e6611cb363810d'
assert hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest() == source_hash
repairs = apply_doorway_repairs(bpy)
names = [record['frame'] for record in repairs]
bpy.ops.object.select_all(action='DESELECT')
for name in names:
    obj = bpy.data.objects[name]
    obj.data = obj.data.copy()
    obj.hide_set(False)
    obj.hide_viewport = False
    obj.select_set(True)
bpy.context.view_layer.objects.active = bpy.data.objects[names[0]]
bpy.ops.object.convert(target='MESH')
materials = {}
for name in names:
    obj = bpy.data.objects[name]
    obj['sourceObject'] = name
    obj['preservedDoorwayRepair'] = True
    for attribute in list(obj.data.color_attributes):
        obj.data.color_attributes.remove(attribute)
    for slot in obj.material_slots:
        mat = slot.material
        if not mat:
            continue
        original = mat.get('originalRepairMaterial', mat.name)
        if original not in materials:
            mat['originalRepairMaterial'] = original
            mat.name = original + '__REPAIR_SOURCE'
            stub = bpy.data.materials.new(original)
            stub['sourceMaterial'] = original
            stub.diffuse_color = (.8, .8, .8, 1)
            materials[original] = stub
        slot.material = materials[original]
output = out / 'doorway-repairs.glb'
bpy.ops.export_scene.gltf(filepath=str(output), export_format='GLB', use_selection=True,
                          export_apply=True, export_extras=True, export_cameras=False,
                          export_lights=False, export_yup=True, export_materials='EXPORT')
reference = root / 'GARMENT_OFFICE_REALISM_UPGRADE/01_IMPROVED_MODEL/MODEL_FIXES.md'
report = {'source_sha256': source_hash, 'glb': output.name, 'glb_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
          'objects': names, 'materials': list(materials), 'repairs': repairs,
          'reference': str(reference.relative_to(root)), 'reference_sha256': hashlib.sha256(reference.read_bytes()).hexdigest(),
          'scope': 'Existing six documented doorway-rail corrections, preserved on export copy only. No wall/opening position or size changed. Original approved source remains byte-identical.',
          'derivative_geometry_exception': 'Only the modelling-error rail faces within the six pre-existing door cutters are removed.',
          'live_mesh_parity': 'Pending independent portal ray comparison against the retained live19.45MB model.'}
(out / 'doorway-repairs.json').write_text(json.dumps(report, indent=2))
manifest_path = out / 'manifest.json'
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {'version': 1, 'source_sha256': source_hash, 'rooms': []}
manifest['repairs'] = [{'glb': output.name, 'objects': names, 'source_sha256': source_hash,
                        'report': 'doorway-repairs.json'}]
tmp = manifest_path.with_suffix('.tmp')
tmp.write_text(json.dumps(manifest, indent=2))
os.replace(tmp, manifest_path)
assert hashlib.sha256(source.read_bytes()).hexdigest() == source_hash
print('DOORWAY_REPAIRS_COMPLETE', names, flush=True)
