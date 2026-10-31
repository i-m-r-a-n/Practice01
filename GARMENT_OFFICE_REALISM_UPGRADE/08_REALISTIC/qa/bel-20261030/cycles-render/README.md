# Realistic render of the 3D proposal (Blender Cycles)

ChatGPT's image tool redraws the floor from the words, so its pictures do not follow our 3D. These renders use the 3D itself.

1. **`export_scene.py` (Playwright):** loads the proposal page from `viewer/serve_preview.py` with `?debug=1` and frames a reference camera with `frameCamera`.
   - It exports the visible scene to GLB with three.js r169's own `GLTFExporter`, downloaded from `cdn.jsdelivr.net/npm/three@0.169.0/examples/jsm/exporters/GLTFExporter.js` and `.../utils/TextureUtils.js` and rewired to the page's THREE.
   - Lights stay out; Blender gets its own.
   - Per-instance attributes stay out too: the room-probe row of the instanced props would otherwise break Blender's importer.
   - It also saves the WebGL frame for comparison.
2. **`render_cycles.py` (Blender 5.2, Cycles CPU):** imports the GLB, adds a ground plane, a soft warm sun and a pale sky, and renders.
   - It uses the same camera: the overview cameras are orthographic in `office_web_metadata.json`, for example `CAM_ISO_SE` with ortho_scale 58.6.

```
python3 -I export_scene.py CAM_ISO_SE
blender -b -P render_cycles.py -- scene_CAM_ISO_SE.glb VIEW_CAM_ISO_SE out.png 1920 1080 64 58.6
```

The GLB (about 126 MB) is not kept in the repository.

The render shows the floor, rooms and furniture exactly as the 3D has them. Materials are the 3D's own, so their realism is the 3D's; the light and shadows are real.
