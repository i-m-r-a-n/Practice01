# Prompt for GPT Astra: put Claude's realistic 3D assets into the live Stage II office tour

You own the live web tour: https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/ (Cloudflare Worker
`stage2-office-virtual-tour`, frontend on branch `chatgpt/interactive-office-tour` of `i-m-r-a-n/Practice01`). Claude has
prepared tested assets and a reference implementation on branch `claude/web-tour-assets` (commit
`ddf99eee703600ee722f06595708439560373567`, see GitHub issue #12). Your job: integrate them, fix the live bugs, test in a
real WebGL browser, deploy, and report back on issue #12. Do not change files on `claude/*` branches or in
`GARMENT_OFFICE_FINAL_PRESENTATION/`, and do not force-push.

## 1. Inputs (all on `claude/web-tour-assets`, folder `GARMENT_OFFICE_WALKTHROUGH_FINAL/`)

Raw base (pinned, tested: HTTP 200, the GLB is 19,452,524 bytes):
`https://raw.githubusercontent.com/i-m-r-a-n/Practice01/ddf99eee703600ee722f06595708439560373567/GARMENT_OFFICE_WALKTHROUGH_FINAL/`

| Path | Use |
|---|---|
| `07_WEB_TOUR_ASSETS/Final_Office_Interior_web_baked.glb` | **The model to use** (19.5 MB). Cycles lighting from the scene's 188 lights baked onto floors, walls and ceilings (vertex colours); base colours fixed (the original GLB shows sofas grey, carpet light); WebP + quantized; plain `GLTFLoader`, no decoder files; 38 cameras; ceilings, beams, deck and fittings under one node `WEB_OVERHEAD` |
| `07_WEB_TOUR_ASSETS/Final_Office_Interior_web.glb` | Fallback without baked light (16.6 MB) |
| `07_WEB_TOUR_ASSETS/office_web_metadata.json` | 38 cameras (exact position + quaternion, fov, lens shift, render path `/renders/CAM_xx.jpg`), 34 rooms (name, function group, area, floor polygon, approved description, primary camera), the 16-stop tour, object names |
| `07_WEB_TOUR_ASSETS/walk_grid.json` | Walk-mode collision map (walls, glazing, furniture; door openings free) |
| `07_WEB_TOUR_ASSETS/README.md` | Code snippets for everything below |
| `03_INTERACTIVE_3D/app.js` | Reference implementation (three.js r169) of all features below; copy freely |
| `08_WORKER_READY_TOUR/index.html` + `app.js` | The same tour as 2 static files (no CDN, no import map). Option B below |
| `05_PRODUCTION/live_site_qa/LIVE_SITE_QA.md` | Bugs Claude found on the live site (commit 50923eb) with screenshots |

## 2. Bugs on the live site to fix (seen in a real WebGL browser)

1. Overview shows only the roof; the ceiling button does nothing. Console says `ceilingMeshes: 0` because GLTFLoader renames
   nodes ("Steel deck / slab" becomes `Steel_deck__slab`), so the name regex never matches. Fix: `WEB_OVERHEAD` node.
2. Selecting a room opens the render panel but the 3D camera does not reach the room.
3. Walk mode shows an empty view.
4. Room markers float in front of interiors (visible through walls).
5. The tour has 17 stops; the brief asks for 16 (use `metadata.tour`).

## 3. What to build (choose A or B)

**Option A, keep your frontend** and change it as follows:
- Load `model_web.glb` = the baked GLB (Worker route below); fall back to `model.glb`.
- Baked light: for every mesh whose node (or a parent) has `userData.baked_light_scale` and whose geometry has a `color`
  attribute, replace the material, except glass (`transmission > 0`) and lamps (emissive):
  ```js
  new THREE.MeshBasicMaterial({ map: m.map, color: m.color.clone().multiplyScalar(k * 2.0), vertexColors: true, side: m.side })
  // k = userData.baked_light_scale (16); 2.0 = exposure matched to the Cycles renders
  ```
  Keep real-time light (environment + hemisphere + one directional) only for furniture; AgX tone mapping, exposure about 1.0.
- Ceilings: `gltf.scene.getObjectByName('WEB_OVERHEAD').visible = false` in the overview, `true` at eye level.
- Room views: put the camera exactly on the metadata camera:
  ```js
  camera.position.fromArray(c.position); camera.quaternion.set(...c.quaternion_xyzw);
  const hf = THREE.MathUtils.degToRad(c.hfov_deg_render), a = innerWidth / innerHeight;
  camera.fov = THREE.MathUtils.radToDeg(2 * Math.atan(Math.tan(hf / 2) / a));
  camera.setViewOffset(innerWidth, innerHeight, 0, -c.shift_y * Math.max(innerWidth, innerHeight), innerWidth, innerHeight);
  camera.updateProjectionMatrix();
  ```
  Fly there smoothly (rise above the walls, then descend), time-based so it also finishes on slow machines.
- Walk: one lookup per step in `walk_grid.json` (decoder in the README); move in sub-steps of at most 4 cm; slide along
  obstacles; `Esc` leaves walk mode.
- Tour: the 16 stops of `metadata.tour` with Start, Pause/Resume, Stop, Next, Previous and a progress bar; at each stop the
  title and description from the metadata; optional dissolve into `/renders/<camera>.jpg`, labelled "Photoreal render, still
  image of this viewpoint".
- Markers: only above about 3 m camera height, de-cluttered (no overlaps), clickable.
- Text: title "GROUND FLOOR - INTERACTIVE DESIGN EXPERIENCE"; disclaimer always visible: "Proposed interior visualization.
  Final dimensions and technical details subject to site verification." Room text only from `metadata.rooms[].description`
  (from the approved documents); do not add claims, numbers or names.

**Option B, drop in Claude's bundle:** serve `08_WORKER_READY_TOUR/index.html` at `/` and its `app.js` at `/app.js`
(it needs only `/model_web.glb` and `/renders/<camera>.jpg`). Keep your current pair for rollback.

## 4. Worker

- Add route `/model_web.glb` -> raw URL of `07_WEB_TOUR_ASSETS/Final_Office_Interior_web_baked.glb` at the pinned commit
  above, `Content-Type: model/gltf-binary`; stream it, do not modify it. Keep `/model.glb` and `/renders/*` as they are.
- Cache: the Worker now sends `max-age=1800` for `app.js`; after deploying, use a versioned script URL or purge, so no client
  gets new HTML with an old script.
- Record the Worker version before and after; rollback = previous Worker version + the frontend commit that was live before
  your change (`50923eb` when Claude tested).

## 5. Test before you report "done" (real WebGL, not the gallery fallback)

Use a browser with WebGL. Headless Chromium works with
`--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader --ignore-gpu-blocklist`.
Check and screenshot:
1. Model loads, no console errors, loading overlay gone.
2. Overview shows the rooms (no roof), ceiling toggle works both ways.
3. Boardroom, MD office, reception, design studio: camera lands on the render framing (compare with `/renders/CAM_09_Boardroom_A.jpg` etc.).
4. Walk: W moves; walking into a wall or desk stops; never inside an obstacle; Esc exits.
5. Tour: all 16 stops; pause holds; resume, next, previous, stop work; progress bar moves.
6. Search filters rooms; 390 px phone width has no horizontal scroll.
7. Live URL after deploy: same checks; `model_web.glb` HTTP 200 with 19,452,524 bytes.

## 6. Report on issue #12

Frontend commit SHA, Worker version, the test list above with pass/fail and screenshots, anything not done and why.
Do not claim photoreal equivalence: furniture and reflections are real-time; the Cycles renders and the videos are the
photoreal reference.
