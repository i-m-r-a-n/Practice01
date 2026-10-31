# Realistic renders of the 3D proposal (Blender Cycles)

ChatGPT's image tool redraws the floor from words, so its pictures do not follow our 3D. These renders use the 3D itself: the same rooms, furniture, materials and camera, with light simulated by Cycles. They show no people.

The proposal route shows them at the tour stops that have no AI concept image, labelled "RENDERED FROM THE 3D MODEL · Blender Cycles, simulated light · no people · not a photograph" (`concept-images/render_<CAMERA>.jpg`, see `concept-images/README.md`).

## Steps

1. **`export_scene.py` (Playwright):** loads the proposal page from `viewer/serve_preview.py` with `?debug=1` and frames a reference camera with `frameCamera`.
   - It exports the visible scene to GLB with three.js r169's own `GLTFExporter`, downloaded from `cdn.jsdelivr.net/npm/three@0.169.0/examples/jsm/exporters/GLTFExporter.js` and `.../utils/TextureUtils.js` and rewired to the page's THREE.
   - Lights stay out; Blender gets its own.
   - **Instanced meshes with per-instance colours are baked into plain meshes with vertex colours.** These are the leaves of the trees, bonsai and tulsi, and the sorted cutting-waste offcuts. Blender's importer drops instance colours, which made the leaves grey. glTF `COLOR_0` multiplies the base colour, as `instanceColor` does in three.js.
   - Other per-instance attributes stay out: the room-probe row of the instanced props would otherwise break Blender's importer.
   - It saves the WebGL frame for comparison, and writes `camera_<CAMERA>.json` with the approved camera's lens, sensor and shift.
2. **`render_cycles.py` (Blender 5.2, Cycles on the CPU):** imports the GLB and renders it with the same camera.
   - **Overview cameras** are orthographic in `office_web_metadata.json` (for example `CAM_ISO_SE` with ortho_scale 58.6). They get a ground plane, a soft warm sun and a pale sky.
   - **Interior cameras** use the approved lens (18 mm on a 36 mm sensor) and shift. Only the 3D's real light fittings give light: the LED strips and panels, bulbs, lanterns, grow lights, and niche and paper lamps, with their emission multiplied by 6.
     - Screens keep their glow; the web view's other self-lit helpers are switched off.
     - The painted light pools of the web view are hidden, because Cycles makes real ones.
     - A warm, soft fill stands in for light bouncing off the walls.
   - Colour management: AgX, Medium High Contrast.
3. **`render_batch.sh`:** runs both steps for a list of cameras with its own preview server, saves `concept-images/render_<CAMERA>.jpg` and deletes the GLB (about 130 MB each; the GLBs are not kept in the repository).
4. **`contact_sheet.py`:** one sheet of all stop images in tour order, gold titles for AI images and green for renders.

```
./render_batch.sh 8791 BEL_CAM_ACADEMY:interior:1600:900:48 CAM_ISO_SE:overview:1600:1200:64:58.6
blender -b -P render_cycles.py -- scene_CAM_ISO_SE.glb VIEW_CAM_ISO_SE out.png 1920 1080 64 58.6
```

The scripts name this session's working folders (`/home/user/render_work` for the downloads and the GLBs, and the worktree) at the top; change them for another machine. A 1600 × 900 interior at 48 samples takes about 4 minutes on 4 CPU threads.

## What the renders are, and are not

- They show the floor, rooms and furniture exactly as the 3D has them. The materials are the 3D's own, so their realism is the 3D's; the light and shadows are simulated.
- They are not photographs, and they prove no material, maker, test or data.
