# Performance of the improved model and viewer

Numbers from `glb_inspection.json` (files) and from the browser tests of 27 Oct 2026 (viewer).

| | Original GLB | Web GLB (live now) | Improved GLB (baked light) |
|---|---|---|---|
| File | 41.86 MB | 16.57 MB | 19.45 MB |
| Triangles drawn | 920,497 | 920,497 | 999,775 (shell split for the light bake) |
| Vertices | 338,499 | 296,222 | 363,529 |
| Materials / textures | 79 / 61 | 79 / 67 (WebP) | 79 / 67 (WebP) |
| Texture memory (RGBA8 + mipmaps, estimate) | 325 MB | 358 MB | 358 MB |
| Draw calls in the viewer (after merge by material) | - | 2,306 -> 92 | 1,880 -> 100 |
| Real-time lights / shadow maps | - | environment + 2 lights, 1 shadow map | environment + 2 lights, **no shadow map** (the shadows are in the baked light) |

Measured in the tests (local static server, so download time is near zero):
- Improved build ready (model parsed, merged, first frame) in 1.1 - 2.3 s in Chromium and Firefox 159.
- Offline one-file version (`GARMENT_OFFICE_WALKTHROUGH_FINAL/09_MAC_OFFLINE_TOUR`): ready in 2.2 s in Chromium from
  `file://` (the model is decoded from the page itself).

Not measured (stated, not guessed):
- Frame rate on a real GPU: these tests run on a software GPU (SwiftShader / llvmpipe), which says nothing about a Mac's
  frame rate. The viewer only renders when something changes (camera move, flight, tour), so an idle view costs nothing.
- Download time on the client's connection: 19.45 MB; for example about 8 s at 20 Mbit/s (calculation, not a measurement).

Settings that help on a slow machine: help card (`?`) -> Display quality -> Balanced or Low (caps the pixel ratio at 1.5 / 1);
`?scale=0.6` in the address renders fewer pixels.
