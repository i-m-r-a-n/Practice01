# Verification results

Generated 2026-10-27 08:03 Asia/Dhaka by `01_EDITABLE_3D/scripts/verify_all.sh` in fresh Blender 5.2.3 LTS processes.

Self-containment test: the .blend was copied alone into an empty temporary folder and reopened there, so every texture it
finds must be packed inside the file.

## .blend reopened: `Final_Office_Interior.blend` (41.6 MB)
- objects 1494, meshes 642, materials 82, lights 188, cameras 38, images 67
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
  - Furniture: 295
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
- furniture / equipment objects with asset + zone properties: 293
- render engine CYCLES, samples 128, denoise True, view transform AgX

## .glb re-imported: `Final_Office_Interior.glb` (41.9 MB) in 1.8 s
- objects 1150 ({'MESH': 1112, 'CAMERA': 38}), meshes 563, materials 79, images 61
- triangles (unique meshes) about 374,160
- result: PASS (model geometry, materials and cameras load in a fresh Blender session)

## Geometry (checkpoint A)
- `verify_geometry.py` on the delivered .blend: 75 of 75 measurements match the survey values (`04_DOCUMENTATION/geometry_verification.md`).

## Presentation (`03_PRESENTATION`)
- PDF `Garment_Office_Design_Pitch.pdf` (5.9 MB): opens, 18 pages, page size 1440 x 810 pts - PASS
- PPTX `Garment_Office_Design_Pitch.pptx` (6.4 MB): opens in python-pptx, 18 slides, 61 pictures, all text in editable text boxes and tables
- PPTX opened and converted by LibreOffice: 18 pages - PASS
- render images used by the deck: 24 views in 29 places; byte-identical to `02_RENDERED_IMAGES/final`: 24, to `02_RENDERED_IMAGES/previews`: 0, anything else: 0 - PASS
- every preview image is captioned '(preview render)' where it is shown: PASS (no previews left in the deck)
- other images in the deck: ID-01_furnished_plan.svg, ID-02_zoning_plan.svg, ID-03_ceiling_lighting_plan.svg, logo_stage2_ltd.png, logo_stage2_unit1.png, logo_zara_fashion_profile.png, material_board.jpg, swatches/swatch_AC-01.jpg, swatches/swatch_CP-01.jpg, swatches/swatch_MT-02.jpg, swatches/swatch_PA-01.jpg, swatches/swatch_PA-02.jpg, swatches/swatch_SS-01.jpg, swatches/swatch_TZ-01.jpg, swatches/swatch_UP-01g.jpg, swatches/swatch_UP-01s.jpg, swatches/swatch_UP-02.jpg, swatches/swatch_WD-01.jpg, swatches/swatch_WD-02.jpg, swatches/swatch_WO-01.jpg, swatches/swatch_WO-02.jpg, tagline_quality_compliance_commitment.png (drawings ID-01..03, material board and swatches from this project, client logos and tagline cropped from the client's business card and company profile)

