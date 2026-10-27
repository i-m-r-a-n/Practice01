## Current Reception increment

The default build is configured by `release-config.json`. It retains the exact live vertex-lit shared shell from `Final_Office_Interior_web_baked.glb` and overlays only the named Reception furniture/fixture subset from `lighting-v2/manifest-hybrid.json`. This is a hybrid first-room improvement, not a claim that every wall/floor has a new high-resolution lightmap. The old production tour is not modified.

The original Claude HTML/CSS, room list, guided tour, photo comparison and overview are retained. Only a People toggle and “People shown are illustrative” note are added when the accepted static people gate is enabled. Reception has eight additive desk/table objects and readable screen artwork. Native PBR replacement, room reflection probes and post extras are disabled in this release; existing scene lighting is used for added props/static people. The later experimental modules remain archived in source, dormant.

Strict walking retains the existing grid and exact source slab footprint. Because the live shell has joined node names, the eight original floor-top triangles are bundled in `approved-floor-footprint.json`, with the unchanged named-source hash and accessor provenance. No floor geometry is changed.

The Reception-only people gate is enabled after the independent exact-mesh contact pass on poses16bb2498…; this does not enable the archived35-person population. The release uses `people/reception/people-manifest.json` and `reception/poses.json`, with frozen poses, no locomotion and no task animation. The archived35-person manifest is not the release entrypoint. Props/people helper code is statically bundled so offline playback has no native file:// module imports.

# Realistic viewer: phase 1 integration

This directory is an isolated derivative of the approved tour viewer. The original tour source and approved models are unchanged. Phase 1 adds progressive per-room Cycles lightmaps. Later phase features are not implied by this build.

The default remains `stage=1`. Later work is staged behind query flags for separate comparisons; functional implementation is not visual acceptance of the lighting candidates.

## Build and serve

```sh
cd GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/viewer
npm --cache /tmp/office-npm-cache ci
npm run check
npm run build
python3 serve_preview.py --port 8783
```

Open `http://127.0.0.1:8783/realistic/?welcome=0`. The bundle is `dist/index.html` and `dist/app.js`. The Worker must route `/realistic/model_web.glb` to the original **named** 16.6 MB web GLB from `07_WEB_TOUR_ASSETS/Final_Office_Interior_web.glb`; it must not use the older joined vertex-lit shell, whose source object names were removed. Routes below `/realistic/lighting`, `/realistic/textures` map to the corresponding sibling directories under `08_REALISTIC`. `/realistic/renders/` maps to the original approved Cycles JPGs.

## Lighting contract

`lighting/manifest.json` contains a `rooms` array. Each record:

```json
{
  "id": "Z02",
  "objects": ["exact original Blender object name"],
  "glb": "rooms/Z02.glb",
  "lightMap": {"url": "rooms/Z02.ktx2", "format": "ktx2", "intensity": 3.141592653589793}
}
```

URLs resolve relative to the manifest. The exact `objects` list controls replacement: missing or duplicated source objects fail closed, keeping the original objects visible. Replacement GLBs use original material names, preserve world coordinates and UV0, and provide lightmap UV1. Meshes or ancestors tagged `overhead: true`, or named with `_OVERHEAD`, follow the existing ceiling toggle. Original source materials are cloned from the named base GLB, including their textures and corrected colours. Unknown material names or missing UV1 reject the entire room.

Shared building shell records use `id: "SHELL"` (or multiple distinct shell IDs) and `alwaysLoad: true`. They load on startup, remain resident, and are awaited together with every selected room. Each source object belongs to only one record; shared objects must not also appear in a room list. `lighting().requiredShared` lists these records so capture checks can verify their `loaded` status too.

Optional `lightMap.preview: {"url":"previews/Z02-1024.ktx2","format":"ktx2","size":1024}` must be a genuine scene-linear HDR downsample of the same accepted atlas. It appears first with state `preview`; full resolution replaces it asynchronously. Capture APIs wait for the full download, and acceptance checks must require state `loaded`. A failed full download retains the explicitly marked preview and its error. Preview quality never substitutes for final-atlas inspection. No production preview has been accepted yet.

Existing released doorway repairs are supplied in `manifest.repairs: [{"glb":"doorway-repairs.glb","objects":["exact source node name"]}]`. All replacement names/materials are validated before atomic application, ahead of grouping and walk readiness. Required repair failures stop preparation. This reinstates the previous tour's six Boolean doorway cuts in the named fallback copy; it is not a new opening or layout change.

Only after both geometry and lightmap are ready does the room switch atomically from original objects to the baked replacement. Up to six atlases are resident; eviction restores the original room first. Shared shell surfaces outside an exact room object list retain fallback lighting. The on-screen lighting label distinguishes preview areas from loaded rooms. `window.__viewer.lightmaps` exposes errors and coverage; a loaded room does not imply the entire floor has been baked.

Linear RGBA half-float KTX2 with Zstd is supported by Three r169. EXR uses r169 EXRLoader with a vertical texture transform because the codec check found its decoded row order opposite to the KTX2 converter's top-left row order. No AgX or sRGB transform is baked into the lightmap. `channel = 1` selects UV1. Atlas mipmaps are disabled to avoid unverified island bleeding. Sampling is linear. Real atlas orientation must also be inspected against room geometry.

Three r169 adds `lightMap.rgb * intensity` as irradiance, then applies Lambert `1 / PI`. Cycles diffuse direct+indirect without colour produces diffuse radiance normalized by albedo. Thus PI is the physical starting conversion, with final calibration still requiring camera comparisons. The shader disables additional runtime diffuse on baked materials while retaining direct specular, environment specular and emissive contribution. It does not pretend that the existing generic environment is a room reflection probe.

## Review API

```js
await __viewer.api.frameCamera('CAM_01_Reception_A');
await __viewer.api.loadRoomLightmap('Z02');
__viewer.api.lighting();
__viewer.api.renderStats();
```

`frameCamera` uses the original position, quaternion, sensor/lens and shifts; orthographic cameras use their original orthographic scale. It hides UI only in review capture mode. Normal room navigation, guided tour, comparison photographs, collision grid, client logos and site-verification disclaimer remain available.

Non-16:9 reference cameras are letterboxed using their original render aspect. Blender AUTO orthographic scale is the longer image dimension. Phase 1 capture excludes screen-space AO to isolate the atlas. Stage 5 capture uses the actual post stack; `renderStats().capturePostProcessing` records that distinction.

`__viewer.timings` records the first submitted base view, per-room atlas decode/visible/full-visible time and separate hero-map readiness in milliseconds since navigation. Hero textures do not hold up the first base scene or the atlas swap. These application milestones do not claim GPU presentation timing or network-throttled results; the final CDP bandwidth test remains separate.

## Staged feature modules

- `?stage=2`: native 2K KTX2 normal/roughness/base-colour maps load by room material. Original UV transforms, normal strength, roughness factors, HSV/tint/desaturation recipes and palette are retained. Carpet colour keeps the original processed map so the approved procedural tile pattern is not silently removed. New brushed-metal normals use restrained strength. Not every source procedural shader is identical to Blender.
- `?stage=3`: 256-pixel HDR room reflection captures with room-box projection and a four-probe cache. Captures are one-time, not SSR or continuously updated reflections of moving subjects. Room boxes use the original plan polygon bounds and source soffit height; the box is an approximation for nonrectangular rooms. The module also has spherical-harmonic diffuse lighting for phase4 dynamic subjects (async HDR readback is awaited, and probe captures are serialized).
- `?stage=5`: exact 1.60 m eye height, acceleration/braking, optional mouse capture with drag fallback, and strict collision. The original floor slab's eight top triangles include doorway thresholds that clear-room polygons omit. Static collision still uses the original 0.10 m grid with its inherited 0.15 m player radius. There is no blocked-position noclip escape. Initial room-camera positions snap to a verified free point within the selected room.
- Stage 5 post-processing reuses the main depth texture for GTAO and excludes glass from depth writing. Bloom renders only emissive geometry and depth-tests it against the main scene, avoiding a second opaque-office draw. `renderStats().post` reports all pass calls/triangles. AgX is present; a calibrated per-zone LUT/colour grade is **not** implemented or claimed.
- `&materials=0&probes=0&post=0` isolates movement tests from later visual modules. `&lighting=./lighting-v2/manifest.json` reviews a separate candidate without changing the default manifest.

`?stage=4` connects 323 self-made additive props and readable screen artwork. The 49 instanced prop batches receive room SH irradiance through per-instance room indices; dynamic actors use individual room probes. These additions are not included in the static Cycles bake. People remain gated by `__TOUR_CONFIG.peopleAccepted=false` until the independent contact review clears; the People button and illustrative note become available only after that gate. The runtime loads `props/office-props.mjs`, `props/screen-content.mjs` and `people/people-layer.js` from the same route. Their placement/contact and integrated phase screenshots still require acceptance. No earlier source “no people” statement overrides the later user request for clearly labelled illustrative occupants.

Review-only movement hooks `setWalkQAStart(x,z)`, `stepWalkQA({forward,strafe,yaw,dt})`, `walkState()` and `lookState()` use the same controller as real input, report full precision positions/velocities and count starts/substeps. The QA hook pauses automatic RAF movement to avoid hidden double advancement. Normal and QA movement share room/streaming updates. `setBakeIsolation(true)` hides all original fallback meshes to exclude duplicate-geometry artefacts while inspecting replacement lighting.

Actual Chromium/Firefox/WebKit Linux movement-function replay and real-input smoke reports are in the sibling `qa/` directory. The fixed mouse input passed seven real UI behavior checks in each engine; WebKit used drag fallback, so native Safari pointer lock is not claimed. Functional Chromium tests of stages 2/3/5 passed without JS/GLSL errors. These are software-GPU tests, not MacBook frame-rate certification.

The current diagnostic lighting still has visible plain-beam mottling and incomplete shared-shell coverage. `viewer/qa/` records failed raw/denoise/orientation/isolation experiments; those files are evidence, not an accepted final visual release.

GPU statistics from `renderStats()` and the idle on-screen frame counter are not MacBook benchmarks. Mac Safari/Chrome/Firefox performance, 60 fps, accurate probe reflections, full PBR coverage and later set dressing require their own phase tests.

## Dependency provenance

Three r169 and its examples: MIT, Three.js authors. EXRLoader includes the original BSD TinyEXR/OpenEXR notices. fflate, KTX parser, Zstd decoder and KTX2 loader retain their source license headers. Added files are unmodified official r169 dependencies, except the application modules in this directory. Basis runtime assets are served from the codec sibling directory only when a Basis-encoded texture needs transcoding.

Phase 4 functional Chromium smoke loaded 323 props / 1,473 instances / 49 instanced batches with zero page, console or application errors. This low-resolution unbaked-base smoke only verifies integration/shaders; it does not accept lighting or prop contacts. People were disabled.

A second actual Chromium stage4 smoke loaded the full Reception atlas and room SH/probe, projected two readable screen components with zero skipped faces, and rendered 255 calls / 1.771M triangles in its diagnostic frame. The one-time probe capture cost 1,412 calls / 10.525M triangles across all cube/PMREM passes; it is not a per-frame count. Shared-wall coverage was intentionally absent in this functional test, and guided512 remained an unaccepted diagnostic.

Final Reception contact evidence: `../qa/props-independent/reception-static4-final2-prop-contacts.json` reports zero reader hand/book and badge/skin intersections and1.98006mm book/lap clearance. Runtime uses fixed poses; no task gestures or walking actors.
