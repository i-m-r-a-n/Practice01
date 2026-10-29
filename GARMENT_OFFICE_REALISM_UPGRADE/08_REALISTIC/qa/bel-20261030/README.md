# Bengal Earth Lab: 3D proposal route

## Increment 3: the design wing (30 Oct 2026)

These rooms work in every option, including the pilot (option C). Approved furniture stays; the proposal only adds items on existing surfaces and walls.

| Room | Items |
|---|---|
| Design-wing entrance, Z22 north strip | **The making line**, on the only solid wall (face z -21.41). The corridor walls are glass, so the labs behind them are the exhibit. It shows one River to Home basket in six steps on oak ledges: raw material, preparation, technique, prototype, testing (records to be added), collection. It reads 1 to 6 from the hallway door D13. |
| Living materials library Z15 | Eight labelled natural-material boxes on the low shelf under the library glass W04, so they can be seen from the Experience centre: jute, hogla, cane, bamboo, water hyacinth, kaisa grass, coconut shell, terracotta. Material Passport cards on the review table, with "origin to be documented, maker to be identified, tests none yet". The D65 booth and the fabric library stay. |
| Materials lab Z16 | A moisture and mould test set-up on the post-processing bench: four sealed sample boxes, a scale, a moisture meter and an empty test log ("method to agree with an accredited lab, records to be added"). No results are shown. The 3D printers stay. |
| Prototype workshop Z17 | On the pattern table: a cane basket on its mould, split bamboo, a steam-bent hoop and a mallet. Above it, a dust-extraction hood marked "to be engineered". A steam-bending jig sits on the steam station. The sample machines and forms stay. |

- **Measured in the scene:**
  - library low shelf top 0.7112 and review table 0.9144
  - lab post-processing bench 0.7874
  - workshop pattern table 0.9145 and steam station 0.8636
  - the corridor walls are glass; the strip's south wall is solid at z -21.4104; the floor is at 0.0097
- **Tour:** 16 stops. New: the making line, and the labs behind the glass (`BEL_CAM_LAB`). The negotiation suite now ends the visit.
- **Memory:** the whole layer is 46.9 MB of textures at full detail (222 textures; mostly the printed cards), with 1,161 meshes and 13,096 instanced leaves.
- **Walk:** along the making-line strip from the hallway end into the corridor, 4.8 m, with no collisions.
- **Checks:**
  - `after-tour16/`: all 16 stops.
  - `after-inc3/`: the new views, the approved cameras CAM_23, CAM_24, CAM_25 and CAM_32, and a walk along the making-line strip.
  - `before-inc3/`: the same approved cameras on the approved route.
  - `compare/inc3_design_wing.jpg`
  - `visitor/`: `making_line`, `library_boxes`, `workshop_table`.

## Increment 2: the option A rooms (30 Oct 2026)

**Option A only.** Merchandising Z07 and the accounts suite in Z06 are shown as they would be if both teams moved off this floor. That is the owner's decision; the pilot (option C) does not need it.

- **Relocation ledger.** [`OPTION_A_RELOCATION_LEDGER.md`](OPTION_A_RELOCATION_LEDGER.md) is generated from the approved model by `viewer/make_option_a_ledger.py` (data: `viewer/option-a-ledger.json`).
  - 25 groups of approved items (90 model nodes) move with their teams. The route hides them; the approved model is unchanged.
  - Walls, glass partitions, doors, the steel columns, fire extinguishers, air conditioning, smoke detectors and the kept lights stay.
  - The finance archive cabinet in the north corridor stays. The owner decides whether it moves.

| Room | Option A items |
|---|---|
| Merchandising Z07 | **Green Uthan:** a bot-tola seat of handmade terracotta around the steel column; terracotta courtyard tiles; two small fig trees and a banyan bonsai under grow lights (the room has no daylight); split-granite stone seats; an open split-bamboo canopy at 2.34 m, clear of the AC units and smoke detectors. A natural jute carpet over the whole room. |
| | **Artisan corner, by invitation:** a Chakma back-strap loom (bain) and a Marma weaving and basketry stand (thami and angi weaving, Banglapedia), each with a consent card; a nakshi kantha frame; cane basketry on a pira stool; painted terracotta on a sitalpati mat. The fire extinguisher stays clear. |
| | **Room-sets for European buyers:** Bengal Nordic living, River to Home dining, Second Life Bangladesh bedroom and a Future of Bengal hospitality corner. |
| | The main route from door D49 to the hallway opening stays clear along the east side. |
| Accounts suite, Z06 | **Design academy inside the existing glass suite:** 20 seats at 10 mango-wood tables; a demonstration bench with a hands camera; a mobile screen; a pin-up board; a materials shelf. The discussion room becomes the tutor room. The fire engineer sets the capacity. |

### How it works

- **Hiding the approved items.** `make_bel_config.py` reads the ledger: every item that moves becomes a `hideNodes` prefix.
- **Walk grid.** `walkRelease` lists the cells only that furniture blocked: 8,434 cells in 603 row runs.
  - Cells near a wall, glass partition, kept item or steel column stay blocked. The column positions come from the survey (`survey.py COLUMNS`); they are merged into the shell, so they are not model nodes.
  - `viewer/app.js` reads `walkRelease`.
- **Floors and shadows.** The approved carpet's baked light still shows the removed desks. Both rooms therefore get a new unlit floor finish just above the carpet top (measured at y 0.0097). Its occlusion map holds soft wall shadows and the contact shadows of the new furniture.
- **Texture memory.** Weave textures are now shared, and clones reuse one GPU texture. The whole layer, increment 1 included, is 41.6 MB of textures at full detail (44 MB before increment 2).

### Checks (local Chromium, software WebGL)

- `after-tour14/`: all 14 tour stops. No page, console or HTTP errors and no failed requests.
- `after-optA/`: the 4 new tour views and 7 matched approved cameras.
- `before-optA/`: the same 7 approved cameras on the approved route (d5939f9, people on).
- `compare/optA_merchandising.jpg`, `compare/optA_accounts.jpg`: before and after sheets from the same cameras.
- Walks (`room-check.json` in each folder):
  - `after-optA`: from the main route towards the Uthan, 1.15 m, stopping at the stone seat.
  - `after-optA-walk-desks`: 3.45 m straight through where the merchandising benches stood, stopping at the west wall. The hidden desks no longer block.
  - `after-optA-walk-academy`: 10.4 m along the academy's east aisle and through door D51, with no collisions.
- `visitor/`: 8 new eye-level frames (`uthan_*`, `academy_*`). `visitor.json` now lists all 22 frames as stored (JPG), each with its hash.

## Increment 1 (30 Oct 2026)

**Route:** `/bengal-earth-lab/` (local preview, not deployed). **Branch:** `claude/bengal-earth-lab-20261029`.

It is a concept proposal on the approved Stage II floor, "The Living Bengal Factory": a few small trees, bonsai and stones instead of planters, work by rural artists, rural instruments, tea in clay and wood, an honest solar story, and the Earth-to-Product gallery with three illustrative collections.

- `/` and `/realistic/` are untouched: this route has its own page, bundle and config.
- The concept document is the Bengal Earth Lab doc.

### What the route shows

| Room | Proposal items |
|---|---|
| Lobby Z01 | Banyan bonsai on a granite plinth by the glass gate; three split-granite stones; handmade terracotta front on the check-in desk (an open desk: the panel ends under its top); six terracotta plaques by a rural artist (placeholder, to be commissioned and credited) |
| Reception Z02 | Rural instruments above the console (ektara, dotara, banshi on an oak rail, dhol on the console); tea in clay on wooden trays; a small fig tree; ghritokumari in a clay pot on granite |
| Passage Z03 | Sun wall on the solid east wall: sun, generation, use and storage, operations, with grid and backup shown; "Concept demonstration, not live factory data". Terracotta earth band on the solid base of the west wall, which is glazed above 1.22 m, with clay bowls of clay, jute, hogla, cane and rice straw |
| Experience centre Z30 | Earth-to-Product on the plinth (raw material, technique, prototype, testing, collection; the four forms are removed); three collections and the experiments in the four bays (garments and hangers removed); living materials on the table; drinking water from a clay kolshi (client-stated source, no lab results); Future of Bengal lamp by the boardroom door |
| Boardroom Z08 | Clay cups and jug instead of glass; woven samples on wooden trays; bonsai on a jute-wrapped stand |
| Global Design Studio Z18 | Sunning shelf at window W10 (three bonsai, a tulsi pot); a small fig tree by W09; co-creation table with basket prototypes, woven samples, a colour fan and sketches |
| MD office Z12 | Tea in clay cups |

The route shows no people. The approved Cycles renders are never shown here, because they depict the approved knitwear design.

### How it works

- `viewer/bel-config.json` is generated by `viewer/make_bel_config.py` from `release-config.json` and the props manifest. It holds:
  - room names, room notes and the 10-stop tour
  - two proposal viewpoints without renders (`BEL_CAM_SUN_WALL`, `BEL_CAM_SUN_SHELF`)
  - the approved items replaced in place (`hideNodes`, 22 nodes)
  - the bay contents removed (`hideParts`: garment and hook primitives; `trimParts`: 2,000 hanger triangles inside the measured bay interiors)
  - the drinkware to replace (31 props)
  - `noRenderPhotos`
- The viewer reads these keys in `viewer/app.js`, which also has a `debug=1` ray-probe hook used only for QA.
- `props/bengal-earth-lab.mjs` builds the layer. All geometry and textures are self-made and procedural.
- Every replacement keeps the approved footprint, so the approved walk grid stays valid. The only new floor item in this increment, the sunning shelf, reports its footprint to the walk controller.
- Build: `RELEASE_CONFIG=bel-config.json node build.mjs viewer/dist-bel`. Local preview: `serve_preview.py`, which routes `/bengal-earth-lab/` to `dist-bel`.

### Measured in the scene (ray casts, `ray_probe.py`)

| Surface | Value |
|---|---|
| Bays | base 0.1016, top shelf 1.8592, green back z -10.7251, front edge z -10.1347, brass rail y 1.676 |
| Passage | west wall solid to 1.22 m and glazed above (face x 9.323); east wall face x 10.6687 |
| Furniture tops | console 0.7874, lounge table 0.4064, counter 0.8889, plinth 0.2032, material table 0.8635, presentation table 0.7493 |
| Walls | lobby west wall x 0.0, reception north wall z 0.0, studio wall at W10 x 33.68 |
| Check-in desk | an open desk with a walnut top at 0.749 |

### Checks (local Chromium, software WebGL; not live, Safari or MacBook proof)

- `after/`: the 10 tour views at 1440 × 900, with no page, console or HTTP errors and no failed requests.
- `before/` and `../journey-20261029/before/`: the same cameras on the approved route (live `d5939f9`). `compare/` holds the before/after sheets.
  - People are on in the approved route and off here, so the frames differ in that too.
- `visitor/`: 14 eye-height frames of every new item.
- `after-walk/`: a walk towards the sunning shelf covers 1.33 m and stops 0.15 m before it.
  - In `after/room-check.json` the "walk moves" check fails only because that walk was started 0.78 m away.
- Texture memory of the layer at full detail is about 44 MB with mipmaps: 114 textures, 533 meshes and 9,410 instanced leaves. On low quality, canvas sizes halve.

### Honest limits

- The plants are procedural, not species-accurate models.
- Still to be identified:
  - the bonsai grower
  - the rural artist
  - the instrument makers
  - the potters
  - the granite source (Maddhapara Granite Mining Company is the documented domestic quarry; Sylhet river stone is excluded)
- Clay tableware needs lead and cadmium release tests before use.
- The Sun wall carries no figures by design. It shows grid and backup, and keeps "Designed for a Solar-Powered Future" until measured data exist.
- Interior plants and bonsai need light. The only exterior windows on this floor are the east windows W06–W10, so the bonsai rotate to the sunning shelf.
