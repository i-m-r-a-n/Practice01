# Woven Earth: the arrival gallery and reception (7 Nov 2026)

## The brief

The owner sent the "Woven Earth" entrance reference book (19 pages) with the note "Use this as the prompt and regenerate the files".

- The book is a prompt for an AI image model. None is available in this session, so the brief went into the 3D model of the proposal route itself.
- The files were then regenerated as Cycles renders of that 3D model.
- Only the proposal route `/stage2-concept/` changes. The approved design (`/`, `/realistic/`, `/revised/`) is untouched.

The brief asks for:

- one woven hero piece ("The Woven Threshold");
- one terracotta or mineral surface;
- one salvaged-timber bench with a light bamboo seat;
- one real plant in daylight;
- a minimal check-in desk;
- nothing else.

It also sets three rules: culture as method, not motifs; sustainability as proof, not claims; and a geometry lock.

## What the 3D now holds

### Arrival gallery (Z01)

- **The Woven Threshold:** six handwoven swags on a loom-like frame of laminated bamboo.
  - **Material:** cleaned cutting waste (jhut) in 30 strips per swag, with natural jute and cotton.
  - **Colour:** ecru and sand, with one accent block moving across the swags (olive, olive, indigo, charcoal indigo, a little clay), then a quiet last swag. One strip carries a kantha repair.
  - **Frame:** straight bamboo culms through two laminated-bamboo rails, held by black steel drop rods from deck plates. Each swag is tied with cotton tapes and lifts off its culm for cleaning.
  - **Position:** the clear ceiling bay between the steel beam (x 6.03–6.16, underside 2.59 m) and the bulkhead over the east glass (x 7.62), z 1.27–3.73. This is beside the check-in desk, over the route to reception, as in the brief's arrival diagram.
  - **Headroom:** the lowest point is 2.30 m (deck 2.895 m).
  - **What it stays clear of:** the linear lights (x 5.30–5.37), the AC unit (x 5.51–6.17, z 0.93–2.12) and its service side, the smoke detector (5.89, 3.05) and the brand-wall spots (z 0.86–1.03). The exit sign over the entrance stays in view below it.
  - **Spots:** two narrow spots (3000 K) on the deck light the cloth, one from the arrival side and one from the reception side.
- **Terracotta wall:** one hand-pressed terracotta surface on the free west wall, in place of the six plaques.
  - 14 × 16 square tiles (150 mm, lime joints).
  - Raised diamonds on single tiles follow the half-drop repeat logic of Jamdani.
  - A linear wall-washer (3000 K) on the deck draws them in light and shadow.
- **Salvaged bench:** a salvaged hardwood slab on two laminated-bamboo trestles, along the west wall under the terracotta and off the route.
  - The slab keeps its end grain, checks and old fixing holes; a butterfly key crosses one check.
  - The trestles use through-tenons with hardwood wedges, and dowels fix the slab.
- **Bamboo stool:** a light laminated-bamboo stool with a cane seat, at the corner beside the bench.
- **One fig tree:** by the glass entrance, in its daylight, on the approved potted tree's footprint.
- **Check-in desk:** the approved desk, back to its original face.

### Reception (Z02)

- **The fibre story on the console:** raw cotton, jute fibre, cutting waste sorted by colour, recycled yarn and the knit it becomes, all on one oak tray. These are illustrative samples.
- **Kept:** tea in clay, the small fig tree and the approved handloom pieces.

### Retired

These items are not built, but their code stays (`retired` in `props/bengal-earth-lab.mjs`). Each one returns by deleting that line.

- the bonsai on granite;
- the three stones;
- the terracotta front of the desk;
- the six plaques;
- the aloe;
- the rural instruments, which can return on request.

## The views

All views are rendered from the 3D model in Blender Cycles: simulated light, no people, not photographs.

| # | View | File in `concept-images/` |
|---|---|---|
| 1 | The arrival camera, before and after (the same camera and light; before = the proposal of 1 Nov 2026) | `woven-earth/01_arrival_before_after.jpg` |
| 2 | Back towards the entrance (28 mm) | `render_BEL_CAM_WOVEN_REVERSE.jpg` |
| 3 | The threshold and its fixings (35 mm) | `render_BEL_CAM_WOVEN_CLOSE.jpg` |
| 4 | The bench and its bamboo joint (50 mm) | `render_BEL_CAM_WOVEN_BENCH.jpg` |
| 5 | Reception and its brand wall (the approved reception camera) | `render_CAM_01_Reception_A.jpg` |
| 6 | Night check (the arrival camera, fittings only) | `render_CAM_03_Entrance_Lobby_night.jpg` |
| 7 | Terracotta wall and bench (the brief's second view) | `render_BEL_CAM_WOVEN_TOUCH.jpg` |
| 8 | Materials, sources, makers and upkeep (the brief's optional diagram) | `woven-earth/08_materials_board.jpg` |

- Stops 2 and 3 of the tour now show the renders of CAM_03 and CAM_01.
- The owner's AI images of those two stops show the design before the brief. They stay in `concept-images/`.

## Honesty and compliance

- Nothing here is claimed as made, sourced, tested or certified. That covers the makers, weavers, fabricator, timber and bamboo suppliers, jhut sources, fibre origins and recycled shares, and the fire tests.
- The brief's own condition stands: "Final design requires architect / engineer review, local fire and building compliance, and actual contractor quotations."
- The suspension needs the structural engineer to check the deck anchors.
- The textile needs a fire-suitability test.
- Sprinkler and detector coverage, egress and maintenance access need the fire engineer.

## Files

- **3D:** `props/bengal-earth-lab.mjs` (the Woven Earth section, the `retired` flags and `lightMarker`) and `viewer/make_bel_config.py` (notes, stop texts, the four new cameras, the `wovenEarth` set).
- **Renders:** `qa/bel-20261030/cycles-render/render_cycles.py` has the fitting lights from the model (`userData.light` on marker nodes) and a `night` mode. `render_batch.sh` takes variants and can keep the scene. Their working copies are in `/home/user/render_work/scripts`.
- **Set and board:** `qa/bel-20261030/woven_earth_set.py` (before/after composite, thumbnails) and `qa/bel-20261030/woven_earth_board.py` (the materials board).
- **Check:** `qa/bel-20261030/woven_check.py` (items, headroom and clearances, exit-sign sight lines, walking, page errors).
