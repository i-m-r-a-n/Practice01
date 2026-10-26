# Verification results

Generated 2026-10-27 03:39 Asia/Dhaka by `01_EDITABLE_3D/scripts/verify_all.sh` in fresh Blender 5.2.3 LTS processes.

Self-containment test: the .blend was copied alone into an empty temporary folder and reopened there, so every texture it
finds must be packed inside the file.

## .blend reopened: `Final_Office_Interior.blend` (41.6 MB)
- objects 1493, meshes 641, materials 82, lights 188, cameras 38, images 67
- textures packed inside the .blend: 67 of 67; unresolved external textures: 0
- top-level collections (objects incl. children):
  - Structure: 118
  - Walls: 152
  - Doors_Windows: 129
  - Stairs: 11
  - Reception: 3
  - Experience_Center: 1
  - Workstations: 5
  - Meeting_Rooms: 2
  - Executive_Area: 4
  - Design_Development: 6
  - Support_Rooms: 17
  - Prayer_Rooms: 4
  - Washrooms: 4
  - Furniture: 294
  - Ceilings: 174
  - Lighting: 343
  - MEP_Fire_Safety: 46
  - Branding: 10
  - Plants: 37
  - Labels: 34
  - Dimensions: 48
  - Cameras: 38
  - _CC0_Masters: 13 (hidden master copies)
- room / zone floor objects: 34 (each zone has its own floor object with area and finish properties)
- furniture / equipment objects with asset + zone properties: 292
- render engine CYCLES, samples 128, denoise True, view transform AgX

## .glb re-imported: `Final_Office_Interior.glb` (41.8 MB) in 1.8 s
- objects 1149 ({'MESH': 1111, 'CAMERA': 38}), meshes 562, materials 79, images 61
- triangles (unique meshes) about 373,764
- result: PASS (model geometry, materials and cameras load in a fresh Blender session)

## Geometry (checkpoint A)
- `verify_geometry.py` on the delivered .blend: 75 of 75 measurements match the survey values (`04_DOCUMENTATION/geometry_verification.md`).

