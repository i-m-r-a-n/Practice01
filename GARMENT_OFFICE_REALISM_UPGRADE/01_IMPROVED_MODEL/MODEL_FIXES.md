# Improved web model: what changed

File: `Final_Office_Interior_web_realism.glb` (19.45 MB). Built from the approved
`GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/Final_Office_Interior.blend`, which is **not modified** (SHA-256
fa3ed3d5..., checked; the fixes are applied to an export copy by script).

| Change | Why | How |
|---|---|---|
| Baked light on the building shell | the GLB had no lights; the browser view was flat | `../02_LIGHTING/bake_shell_lighting.py`, see `../02_LIGHTING/LIGHTING_NOTES.md` |
| Door-rail cut at 6 doorways | the 38 mm aluminium bottom rail of the glazing frame on the 48 in existing walls ran straight across the door openings at 1.22-1.26 m (D10, D11, D12, D18, D19, D21: frames NI01, NI03, NI04, NI07, NI08, NI10). It is a modelling error, not a design element: a door cannot have a rail at chest height | boolean difference with the same hidden door cutters that open the walls; verified: 0 frame vertices left inside the openings at 1.20-1.27 m. No wall, opening size or position changed |
| Base colours of 22 textured materials | glTF export drops Blender's Hue/Saturation/Value, colour-ramp and tint nodes (green / sand sofas came out grey, charcoal carpet light, walnut pale) | `bake_web_colors.py` applies the same node maths to the textures (report: `Final_Office_Interior_web_realism_material_fixes.json`) |
| Fabric sheen | exported white without the Blender Sheen Weight | sheen colour x weight (0.2-0.5) on 16 materials |
| Size / loading | 41.9 MB original | WebP textures, quantized geometry (16-bit vertex light), groups `WEB_INTERIOR` / `WEB_OVERHEAD` / `WEB_CAMERAS` |

Unchanged: room layout, wall positions, openings, furniture, materials' PBR values (other than the base colour / sheen
fixes), glass (transmission 1, IOR 1.45, roughness 0 clear / 0.32 frosted, black aluminium frames), the 38 cameras.
Shell objects are joined (`WEB_SHELL_INTERIOR`, `WEB_SHELL_OVERHEAD`), so individual walls / floors are no longer separate
nodes in this file; furniture and every other object keep their names. Site-estimated dimensions stay as documented in
`GARMENT_OFFICE_FINAL_PRESENTATION/04_DOCUMENTATION/dimensional_assumptions.md`.

Rebuild (from the repository root):
```
blender -b GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/Final_Office_Interior.blend \
  --python GARMENT_OFFICE_REALISM_UPGRADE/02_LIGHTING/bake_shell_lighting.py -- baked.glb --samples 96
QUANT_COLOR=16 node GARMENT_OFFICE_REALISM_UPGRADE/01_IMPROVED_MODEL/make_web_glb.mjs baked.glb \
  GARMENT_OFFICE_REALISM_UPGRADE/01_IMPROVED_MODEL/Final_Office_Interior_web_realism.glb \
  GARMENT_OFFICE_REALISM_UPGRADE/04_CAMERA_AND_TOUR/office_web_metadata.json \
  GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/scripts/lib_materials.py \
  GARMENT_OFFICE_REALISM_UPGRADE/01_IMPROVED_MODEL/bake_web_colors.py
```
(`make_web_glb.mjs` needs `@gltf-transform/core`, `extensions`, `functions` 4.1.1 and Python 3 with Pillow.)
