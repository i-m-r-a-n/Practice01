# SUPER PROMPT: game-quality realistic 3D tour of the Stage II / Zara Fashion ground-floor office

Copy everything below the line into ChatGPT (a model/agent that can use the GitHub repository, run code, and deploy the
Cloudflare Worker). Attach the "Asset links" document from the same Drive folder.

---

## 1. Your role and the goal

You are the lead real-time 3D artist, technical artist and WebGL engineer for this project. Your job is to turn the existing
interactive tour at https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/ into a **game-quality, photorealistic,
walkable office**: it should feel like walking through a real, working office in a modern open-world game (the visual bar the
client named is GTA V). Every room must look **finished, used and functional**: real materials you could touch, real light,
real everyday objects on desks and shelves, nothing that looks synthetic, empty or "AI-generated".

The office is a **concept proposal** for the ground floor of Stage II Knitting Apparel Ltd. / Unit-1 / Zara Fashion
(Holding 329/2, Ward 15, Vogra, Bason, Gazipur, Bangladesh). The design itself is approved for presentation and must not change.

## 2. What already exists (use it, do not rebuild it)

Repository `i-m-r-a-n/Practice01` (public). Claude's asset branch `claude/web-tour-assets` (same commit on
`claude/realism-upgrade`); GPT's production branch `chatgpt/stage2-video-ready-client`. Coordination: GitHub issue #12.

| Asset | Path | Notes |
|---|---|---|
| Approved Blender model (source of truth) | `GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/Final_Office_Interior.blend` | 34 rooms, 38 named cameras, 188 lights, full furniture. SHA-256 must stay `fa3ed3d5...`: work on a copy |
| Original GLB export | `GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/Final_Office_Interior.glb` | 41.9 MB, 920k triangles |
| Web GLB with baked Cycles light (current best) | `GARMENT_OFFICE_REALISM_UPGRADE/01_IMPROVED_MODEL/Final_Office_Interior_web_realism.glb` | 19.5 MB; light baked as 16-bit vertex colours on the building shell only; door-rail fix; colour fixes |
| Cameras, rooms, tour, collision grid | `GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/office_web_metadata.json`, `walk_grid.json` | exact render-camera matrices with lens shift; 34 room polygons; 16 tour stops; 0.10 m walk grid |
| Photoreal reference (the target look) | `GARMENT_OFFICE_FINAL_PRESENTATION/02_RENDERED_IMAGES/final/CAM_*.jpg` | 38 Cycles renders from the same cameras |
| CC0 textures and models already used | `GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/assets/` (`textures/`, `models/`, `brand/`, `LICENSES.md`) | ambientCG / Poly Haven, CC0; client logos in `brand/` |
| Design documentation | `GARMENT_OFFICE_FINAL_PRESENTATION/04_DOCUMENTATION/` | room, furniture, material, lighting schedules; dimensional assumptions; unresolved issues |
| Current viewer (simplified UI) | `GARMENT_OFFICE_WALKTHROUGH_FINAL/03_INTERACTIVE_3D/` (source), `08_WORKER_READY_TOUR/` (2-file bundle), `09_MAC_OFFLINE_TOUR/` (one-file offline build) | three.js r169, baked-light display, ambient occlusion (GTAO) on still views, walk with collision, guided tour, no overlapping panels |
| Tests | `GARMENT_OFFICE_WALKTHROUGH_FINAL/05_PRODUCTION/test_viewer.js` (25 checks), `test_layout.js` (overlaps at 7 Mac sizes), `firefox_check/ff_check.mjs` | all passing on the current build |
| Videos | `GARMENT_OFFICE_WALKTHROUGH_FINAL/01_CLIENT_PITCH_VIDEO/`, `02_FULL_FLOOR_TOUR/` | 77 s and 2:01 Cycles walkthroughs (look reference for motion) |

Why the current real-time view still looks less real than the renders: light is baked per vertex (about 0.4 m resolution, so no
crisp shadows), furniture is not in the bake, there are no real reflections (generic environment only), materials are missing
normal / roughness detail at close range, and the rooms have furniture but almost no everyday objects.

## 3. The quality bar, made measurable

"Like GTA V" means, for this project:

1. **Light**: soft and sharp shadows where Cycles has them; light pools under every fitting; colour bleeding; correct falloff
   into corners; warm 3000-3500 K visitor/executive zones and 4000 K work zones (`lighting_concept.md`); no flat or
   evenly grey walls.
2. **Reflections**: glossy terrazzo and lacquered floors reflect the room; glass partitions show faint reflections of the room
   (Fresnel), brushed brass and black aluminium read as metal.
3. **Materials up close**: at 0.5 m from any surface you can see wood grain, fabric weave, carpet pile, terrazzo aggregate,
   brushed metal lines, leather grain, felt texture; edges are bevelled (no razor-sharp CG edges).
4. **A working office**: every workplace looks like someone works there today, and people are busy everywhere (see Phases 4 and 4b).
5. **Camera feel**: first-person at 1.60 m eye height, smooth acceleration, mouse/trackpad look, collision with walls and
   furniture, no clipping through objects, no floating objects, nothing hovering above the floor.
6. **Image quality**: no aliasing shimmer, no texture blur at normal viewing distance, no light leaks at wall/floor joints,
   no z-fighting, no black or blown-out rooms.
7. **Side-by-side test**: from each of the 38 render cameras, the real-time frame and the Cycles render should be hard to
   tell apart at a glance at 1280 x 720 (same framing, similar exposure, colour, contrast and shadows).

Be honest about the medium: a browser (WebGL2 / WebGPU) can get close to this with baked lighting, reflection probes,
good PBR and post-processing, but it is not identical to offline Cycles or to a native game engine. If the web version cannot
reach a point, say so and offer the engine route (Phase 7).

## 4. Rules you must follow

- **Design accuracy**: do not move or resize walls, openings, columns, beams, ceilings, rooms or fixed furniture; do not add
  windows, doors, stairs or any building feature that is not in the approved model. Dimensions are site estimates
  (`dimensional_assumptions.md`); keep them, and keep the on-screen disclaimer "Proposed interior visualization. Final
  dimensions and technical details subject to site verification."
- **Assets**: CC0 / public-domain or self-made only (Poly Haven, ambientCG, own Blender modelling). Never use ripped game
  assets (nothing from GTA V or any other game), and no paid assets without the owner's written OK. Record every new asset
  with its source and licence in `LICENSES.md`.
- **Brands**: only the client's own logos from `assets/brand/`. All other objects are generic and unbranded: no Apple,
  Dell, HP, Microsoft, Adobe, Pantone, Zara (the Inditex brand) or other third-party marks or UI. Garments are plain samples,
  not real collections; do not label anything as an actual product line.
- **People: illustrative only**: the office is full of animated characters (Phase 4b), but they are generic, fictional
  people: not real or identifiable persons, not the client's actual staff, no celebrities. Show a small note "People shown are
  illustrative". No testimonials, awards, certificates or fake notices.
- **Readable text only**: any visible text (labels, binders, whiteboards, screens, signs) is short, real, generic English
  ("Q4 samples", "Fabric approvals", "Trims - buttons"), never gibberish or AI-looking pseudo-text. Screens show simple
  generic content (spreadsheet grid, CAD line drawing, colour palette, e-mail list without names), not real software logos.
- **Do not break what works**: keep production online. Build on a new route or branch (for example `/realistic`), keep the
  current tour as fallback, never force-push, keep the approved `.blend`/`.glb` unchanged (work on copies), and post every
  release (commit SHA, URL, test results) on issue #12.
- **Report only what you verified**: say exactly what was tested, on which browser and GPU, and what was not.

## 5. Technical plan (do it in this order; each phase ends with screenshots and tests)

### Phase 0: baseline (short)
Clone, run the existing tests, and capture the current real-time frame from all 38 cameras next to the Cycles renders
(reuse `GARMENT_OFFICE_REALISM_UPGRADE/03_VISUAL_COMPARISON/capture_rooms.js` and `make_comparison.py`). This is the
"before" for every later comparison.

### Phase 1: lighting (largest gain)
- Replace vertex-colour light with **UV2 lightmaps baked in Blender Cycles** on a copy of the approved scene: generate
  non-overlapping lightmap UVs (Smart UV project / pack islands with margin), texel density about 40-80 px per metre for
  floors and walls in the key rooms, 20-40 elsewhere; bake **direct + indirect diffuse** (no albedo) for the building shell
  **and the furniture** (so chairs, tables, cabinets get contact shadows); 256-512 samples + OIDN denoise.
- Store HDR light correctly: RGBM/RGBE or half-float EXR converted to KTX2 (UASTC HDR or RGBM in UASTC); per-room atlases
  of 2048 or 4096 px; load per room (progressive).
- In three.js use `material.lightMap` with `channel = 1` (uv1), `lightMapIntensity` calibrated against the renders; keep
  emissive fittings real-time; tone map with AgX (the renders use Blender AgX) and set exposure per zone.
- Fix seams and leaks: dilate islands, avoid lightmaps on very thin geometry, check corners and skirting.

### Phase 2: materials
- Full PBR sets (base colour, normal, roughness, metalness, AO) for every visible surface, from the CC0 sets already in
  `assets/textures/` (Terrazzo019M, herringbone_parquet, Fabric030 / 034, white_oak_veneer, natural_walnut_veneer,
  laminate_floor_02, leather_white, Tiles040, smooth_concrete_floor) at 2K for hero surfaces.
- Correct real-world scale (e.g. 600 mm tiles, 75 mm slat centres), break up repetition (macro variation, decals), add subtle
  wear: scuffs at desk edges, fingerprints and dust on glass, slight roughness variation on floors.
- Bevel hard edges in Blender before export (2-5 mm), weighted normals, real thickness on glass and panels.
- Compress textures to KTX2 (Basis UASTC for normals, ETC1S/UASTC for colour), enable anisotropic filtering.

### Phase 3: reflections and glass
- One **box-projected reflection probe per room** (cube map baked in Blender at room centre at about 1.2 m, or captured once
  at load with a CubeCamera), applied to floors, glass, metal, lacquer; parallax-corrected so reflections line up with walls.
- Optional screen-space reflections for glossy floors on the High quality setting.
- Glass (GL-01): thin-wall, slight green tint at edges, Fresnel reflection, frosted manifestation bands at about 1000 and
  1500 mm as in the material schedule; exclude glass from the AO pass.

### Phase 4: a real, working office (set dressing)
Add **generic, unbranded** everyday objects, placed by hand with slight randomness (chairs pulled out at different angles,
papers not perfectly aligned). Use instancing for repeats. Per zone:

- **Entrance lobby, reception (Z01, Z02)**: visitor sign-in book and pen, a few fabric swatch books and the company profile on
  the coffee table, small plants, reception phone, monitor, keyboard, mouse, desk organiser, umbrella stand, coat rack,
  a printed visitor-badge tray, fresh flowers in a vase.
- **Experience centre (Z30)**: garments on hangers (plain knitwear and tees in the brand palette), folded stacks on tables,
  hang tags with generic text, fabric swatch cards, a sample book, mannequins dressed in plain samples, a steamer, a full-length
  mirror, a small sample table with tape measure and pins.
- **Boardroom (Z08)**: notepads and pens at some seats, water glasses and a jug on a tray, a conference speakerphone,
  HDMI cable in the power trough, a presentation remote, the 86 in screen showing a neutral title slide with the client logo.
- **Executive suite (Z10-Z13)**: desk accessories, closed laptop, documents in trays, a small framed photo (landscape, no
  people), books and binders on the credenza, a pen stand, a tea cup on a saucer, a plant, a wall clock.
- **Workplaces (Z04-Z07, Z31)**: dual monitors with generic spreadsheets/e-mail lists, keyboards, mice, headsets, desk lamps,
  cable trays with visible but tidy cables, chargers, sticky notes, notebooks, files, binders labelled "Orders", "Costing",
  "Approvals", mugs, water bottles, small plants, pedestals with slightly open drawers, a shared printer/copier corner with paper
  reams, a wall-mounted notice board with generic notices, waste bins, lockers.
- **Design development (Z14-Z19, Z22)**: CAD screens with generic line drawings of a garment pattern, cutting mats, rulers,
  French curves, scissors, pattern paper rolls, pin boards with sketches and fabric swatches, colour-chip fan decks (no brand),
  trim boxes (buttons, zips, labels) on shelves, yarn cones, dress forms with toiles, a sewing machine and an iron in the sample
  room, a 3D printer with a print in progress and filament spools in the 3D lab, sample rails, the D65 colour booth with fabric.
- **Staff cafe, lounge, training (Z20, Z21)**: kettle, microwave, water dispenser, tea and sugar containers, cups on a drying
  rack, fruit bowl, menu/notice board, cushions slightly creased, magazines, training screen with a generic slide, a flip chart.
- **Prayer rooms and wudu (Z23-Z25, Z34)**: prayer mats aligned on the saf lines, a low shelf with folded mats, shoe rack with a
  few pairs of shoes, wall clock; wudu: towels, soap dispensers, slight water marks. Treat these spaces with respect.
- **Washrooms, corridors (Z26-Z29, Z32, Z33)**: paper towel and soap dispensers, mirrors with subtle reflections, bins, signs
  as per the plans, fire extinguishers and exit signs where the fire plan (ID-04) shows them, AC grilles, light switches and
  sockets where the power plan shows them.

Rules for props: real-world scale, resting on surfaces (no floating), shadows from the lightmap or AO, low poly with good
normal maps, total prop budget about 300k triangles, everything instanced or merged by material.

### Phase 4b: a living office (animated characters)
The client wants the office to feel alive, like a game world: **everyone is busy with something**.
- About 25-40 realistic characters across the floor, varied in age, build, skin tone and clothing (modest business wear and
  traditional Bangladeshi office wear such as shirt-trousers, salwar kameez, saree, panjabi), each with a natural looping activity:
  - Reception: receptionist greeting and handing a visitor badge; two visitors waiting on the sofa, one looking at a phone.
  - Experience centre: two buyers browsing garments on the rails with a merchandiser holding a sample and talking.
  - Boardroom: a meeting of 5-7 people, one presenting at the screen, others listening, taking notes, nodding.
  - Executive suite: the MD on a phone call at the desk; an assistant at the executive reception typing.
  - Workplaces (commercial, merchandising, HR): staff typing, on calls with headsets, two discussing a printout, one at the
    printer, one carrying files.
  - Design wing: CAD designers drawing on dual monitors, a designer pinning swatches on a board, a tailor at the sewing
    machine, a technician checking fabric in the colour booth, one person watching the 3D printer.
  - Cafe and lounge: people having tea, chatting at a table, one at the water dispenser.
  - Corridors: a few people walking between rooms along set paths.
  - Keep prayer rooms, wudu and washrooms empty (respect and privacy).
- Natural motion: idle variation, different animation start times, no identical clones next to each other, feet on the
  floor, hands on keyboards and cups; walkers follow paths on the walk grid, avoid furniture and step aside or pause when the
  visitor comes close. No uncanny close-ups: characters face their work, not the camera.
- Assets: free or properly licensed for real-time web use (for example CC0 characters, or royalty-free animation libraries),
  each recorded in `LICENSES.md`. Performance: GPU skinning, LODs (simplified rigs or baked vertex animation far away), at most
  about 15 animated characters drawn at full detail at once, a **"People on/off" toggle**, people off in the Low quality setting.

### Phase 5: camera, post-processing, game feel
- First-person controls: pointer lock with mouse/trackpad look, W A S D / arrows, Shift to walk faster, eye height 1.60 m,
  smooth acceleration and stopping, collision against walls and furniture (extend `walk_grid.json` or use a navmesh), no
  head-bob by default; on-screen hint and Esc to leave. Keep the guided tour and the room list.
- Post stack (three.js EffectComposer or pmndrs/postprocessing): AgX tone mapping with per-zone exposure, colour grading
  LUT matched to the Cycles renders, GTAO/SSAO (exclude glass), subtle bloom on emissive fittings only, SMAA or TAA,
  very light film grain and vignette; depth of field only on guided-tour stills.
- Quality profiles: High (all effects, DPR up to 2), Balanced (DPR 1.5, no SSR), Low (DPR 1, no AO/SSR).

### Phase 6: performance and delivery
- Targets on an Apple Silicon MacBook (M1 or newer) in Firefox, Chrome and Safari: 60 fps while walking at 1470 x 956,
  at least 30 fps at 1920 x 1080 on High; first view in under 10 s on a 50 Mbit/s connection; rooms stream in as you approach.
- Budgets: under 300 draw calls per view, under 3M triangles in view, GPU memory under 1.5 GB; meshopt or Draco geometry,
  KTX2 textures, LODs for props.
- Deliver on a new route (for example `/realistic`) of the same Worker, with the current tour kept as fallback; plus an
  offline package for presenting from a Mac (one HTML file or a folder that opens without a server, as in
  `09_MAC_OFFLINE_TOUR/`). Do not inline more than about 30 MB as a data URL (Firefox limit 32 MB); use a Blob URL instead.

### Phase 7 (optional, maximum realism): native engine version
If the client wants a true game-engine result, rebuild the lighting in Unreal Engine 5 (Lumen, Nanite, virtual shadow maps)
from the same Blender model and props, package it for Apple Silicon macOS (or Pixel Streaming for the browser), and keep the
web tour as the lightweight version. Plan this as a separate deliverable with its own timeline.

## 6. Acceptance checklist (all must pass before you call it done)

1. 38 side-by-side sheets (real-time vs Cycles) with the same framing; key rooms (Reception, Experience centre, Boardroom,
   MD office, Merchandising, Global Design Studio) reviewed one by one, differences listed honestly.
2. Close-up checks at 0.5 m in each key room: textures sharp, no stretching, bevelled edges, readable generic labels.
3. Functional-office check: every desk, counter and shelf in the key rooms carries realistic everyday objects; no empty
   showroom look; nothing floating, intersecting or duplicated in an obviously repeated way.
4. Walk test: walk the full route lobby -> reception -> experience centre -> boardroom -> executive suite -> merchandising ->
   design wing -> cafe -> prayer rooms with no clipping through walls or furniture, no falling through the floor.
5. Existing tests updated and passing (`test_viewer.js`, `test_layout.js`, Firefox check), zero console errors, no
   overlapping interface panels.
6. Performance numbers measured on a real Mac (fps, load time, memory) in Firefox, Chrome and Safari; if you cannot test on
   a real Mac, say so and list what remains to verify.
7. Living-office check: in each key room the characters are doing their activity, look natural from 2 m and from the tour
   cameras, never walk through walls, furniture or the visitor, and the "People on/off" toggle works; the frame rate is
   measured with people on and off.
8. Licence list complete (props and characters); design unchanged (approved file hashes unchanged); disclaimer and
   "People shown are illustrative" note visible.

## 7. Known pitfalls in this project (avoid them)

- The baked GLB stores `COLOR_0` **interleaved** with `POSITION` and `NORMAL`. Never write through `attribute.array`
  on an interleaved attribute: use `getX/getY/getZ` + `setXYZ` and `attribute.data.needsUpdate` (a raw-array loop already
  displaced the walls once in production).
- GLTFLoader sanitises names ("Steel deck / slab" -> `Steel_deck__slab`); use the `WEB_OVERHEAD` group or
  `names.overhead_threejs` from the metadata for the ceiling switch.
- Render cameras use a vertical lens shift: use `camera.setViewOffset` as in the current viewer, or the framing will not
  match the renders.
- Keep interface panels in one bottom row (the tour bar once covered the room card); test at all Mac window sizes.
- Exclude glass from AO; cap device pixel ratio; Safari needs WebGL2 + KTX2 transcoder files served with the right MIME type;
  Firefox data-URL limit is 32 MB.
- Software-GPU test machines are slow: wait for state in tests, never for fixed times.

## 8. How to report

At each phase: commit SHA, changed files, the live or preview URL, side-by-side images for the six key rooms, test results,
performance numbers, and a short "not verified yet" list. Post the summary on GitHub issue #12. At the end: a one-page
client note in plain language (what changed, how to open it, what is still a concept).

## 9. Start now

Begin with Phase 0 and Phase 1 for the six key rooms, show me the before/after sheets, then continue room by room. Ask me
only when a decision changes the design or needs the client (for example, a different material).
