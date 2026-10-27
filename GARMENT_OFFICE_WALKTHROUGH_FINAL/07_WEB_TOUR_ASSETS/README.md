# Web tour assets (issue #12 handoff)

Branch `claude/web-tour-assets`. The approved model files in `GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/` are
unchanged (SHA-256 checked); everything here is derived from them by the scripts listed at the end.

| File | What it is |
|---|---|
| `Final_Office_Interior_web.glb` | Web copy of the approved GLB: 16.6 MB instead of 41.9 MB, same 1,150 named objects, 79 materials and 38 cameras, base colours corrected (see below) |
| `office_web_metadata.json` | 38 cameras (exact matrices, fov, lens shift, render file), 34 rooms (name, function group, area, floor polygon, description, camera), 16-stop guided tour, object-name lists |
| `walk_grid.json` | Walk-mode floor map (0.10 m cells, walls + glazing + furniture between 0.10 and 1.90 m, door openings kept free) |
| `walk_grid.png` | QC image of the floor map: dark = obstacles, light green = reachable on foot from the lobby, red dots = render cameras |
| `Final_Office_Interior_web_material_fixes.json` | Which base colours were baked and which sheen weights were applied |
| `tools/` | `make_web_glb.mjs` + `bake_web_colors.py` (rebuild the web GLB) |

## What changed in the web GLB (and why)

1. **Groups.** Root nodes are grouped under `WEB_INTERIOR` (634), `WEB_OVERHEAD` (478: steel deck, beams, ceiling rafts and
   baffles, light fittings, AC and fire devices) and `WEB_CAMERAS` (38). One line hides all ceilings:
   `gltf.scene.getObjectByName('WEB_OVERHEAD').visible = false`.
   (Name matching on the original GLB fails in three.js because GLTFLoader sanitises names: "Steel deck / slab" becomes
   `Steel_deck__slab`. The live viewer reported `ceilingMeshes: 0` for that reason. `names.overhead_threejs` in the metadata
   has the sanitised names if the original GLB is kept.)
2. **Base colours.** The glTF exporter keeps only the raw image of a textured Blender material and drops its colour
   nodes (Hue/Saturation/Value, colour-ramp remap, tint multiply). In three.js the green and sand sofas, the charcoal and
   green carpets, felt, walnut, oak, terrazzo and porcelain therefore showed the raw texture colour (sofas grey, carpet light).
   `bake_web_colors.py` applies the same operations as the Blender material library (`lib_materials.py`) to 22 textures.
   Result: 25 of 38 camera views get closer to the Cycles renders (camera QC below).
3. **Sheen.** The exporter wrote a white sheen colour without the Blender Sheen Weight (0.2-0.5), which washes fabrics out
   in three.js. 16 fabric/garment materials now carry the weighted sheen colour.
4. **Size.** Textures re-encoded to WebP (`EXT_texture_webp`; photos lossy q86-92, the PNG logos lossless) and geometry
   quantized (`KHR_mesh_quantization`). Both are decoded natively by three.js `GLTFLoader` (tested with r169 and with three 0.164.1 from esm.sh as used by the live viewer: loads, 2,306 meshes, 38 cameras, `WEB_OVERHEAD` found, no errors); no Draco,
   Meshopt or KTX2 decoder file is needed. Load + parse in headless Chromium: 2.2 s from a local server.
5. **Extras.** Object nodes carry `extras.zone` (e.g. `Z07`) where the object name has one; camera nodes carry `shift_y`,
   the render file (`/renders/CAM_xx.jpg`) and its size.

Unchanged: geometry, object names, materials' PBR values (other than the base colour / sheen fixes), glass
(transmission 1, IOR 1.45, roughness 0 / 0.32 frosted), emissive fittings (strength 12) and cameras.

## Using the cameras in three.js (exact match with the renders)

```js
const c = meta.cameras.find((x) => x.name === 'CAM_09_Boardroom_A');
camera.position.fromArray(c.position);
camera.quaternion.set(...c.quaternion_xyzw);          // or camera.up.fromArray(c.up); camera.lookAt(position + direction)
const W = innerWidth, H = innerHeight;               // keep the render's horizontal field of view on landscape windows
const hf = THREE.MathUtils.degToRad(c.hfov_deg_render);
camera.fov = THREE.MathUtils.radToDeg(2 * Math.atan(Math.tan(hf / 2) / (W / H)));
camera.setViewOffset(W, H, 0, -c.shift_y * Math.max(W, H), W, H);   // the renders use a vertical lens shift (level camera)
camera.updateProjectionMatrix();
```
The renders are in `GARMENT_OFFICE_FINAL_PRESENTATION/02_RENDERED_IMAGES/final/<camera>.jpg` (the Worker already serves
them as `/renders/<camera>.jpg`). Five cameras are orthographic (`CAM_TOP_Plan`, `CAM_ISO_*`): `ortho_scale` is the extent
of the larger image side in metres; the renders were made with `WEB_OVERHEAD` hidden.

## Walk-mode floor map

```js
const g = await (await fetch('walk_grid.json')).json();
const bits = Uint8Array.from(atob(g.blocked_bits_base64), (ch) => ch.charCodeAt(0));
const blocked = (x, z) => {                          // x, z in metres (glTF world)
  const col = Math.floor((x - g.origin_xz[0]) / g.res), row = Math.floor((z - g.origin_xz[1]) / g.res);
  if (col < 0 || row < 0 || col >= g.cols || row >= g.rows) return true;
  const i = row * g.cols + col;
  return (bits[i >> 3] >> (i & 7)) & 1;
};
// move: test the new eye position; if blocked, try the x and z components separately (slides along walls)
```
Obstacles are already grown by 0.15 m, so the eye point needs one lookup. Checked: all 33 rooms with a floor area larger than
the walker are reachable from the lobby; `Z34 Wudu (female)` (27 sft) is too narrow at the 0.15 m clearance.
Door leaves are not obstacles (they open); the hidden boolean door cutters define the openings.

## Camera QC (real browser, WebGL 2)

`05_PRODUCTION/camera_qc/camera_qc_sheet_1-5.jpg`: for each of the 38 cameras the final Cycles render (left) and the web GLB
in three.js r169 from the same camera (right). Framing matches on all 38. Compression-only check (before the colour fix):
web GLB vs original GLB differ by 0.12-0.24 / 255 on average (`camera_qc_summary_compression_only.json`).

## Known limitations (not hidden)

- **Lighting.** Blender lights are not part of glTF here and nothing is baked: real-time views are lit by an environment map
  and are flatter and brighter than the Cycles renders (no light pools, no soft shadows). Baked lightmaps (second UV set +
  Cycles bake of the floors and walls) are the next step if the tour must come closer to the renders; the renders remain
  the photoreal reference (show them as "Photoreal render", labelled as still images).
- Not reproduced in the web textures: the tile-joint lines of the terrazzo / prayer carpet and the quarter-turn carpet-tile
  pattern (they depend on the room UVs).
- Found in the approved model (not changed): the 38 mm aluminium frame rail on top of the 48 in existing walls runs across
  the six doorways cut into those walls (D10, D11, D12, D18, D19, D21) at 1.22-1.26 m. The walk map ignores it so the doors
  stay usable; it should be cut at the doors in the Blender model.

## Rebuild

```
blender -b GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/Final_Office_Interior.blend \
  --python GARMENT_OFFICE_WALKTHROUGH_FINAL/04_BLENDER_ANIMATION/scripts/export_web_metadata.py -- OUT
python3 GARMENT_OFFICE_WALKTHROUGH_FINAL/04_BLENDER_ANIMATION/scripts/make_walk_grid.py OUT/collision_tris.npy OUT/blender_cameras.json OUT/blender_rooms.json OUT/door_boxes.json OUT
python3 GARMENT_OFFICE_WALKTHROUGH_FINAL/04_BLENDER_ANIMATION/scripts/make_web_metadata.py OUT GARMENT_OFFICE_FINAL_PRESENTATION/02_RENDERED_IMAGES/final 07_WEB_TOUR_ASSETS
node tools/make_web_glb.mjs Final_Office_Interior.glb Final_Office_Interior_web.glb office_web_metadata.json   # @gltf-transform/* 4.1.1, Python 3 + Pillow
```
(`door_boxes.json`: `blender -b ... --python 04_BLENDER_ANIMATION/scripts/export_door_boxes.py -- OUT`.)
