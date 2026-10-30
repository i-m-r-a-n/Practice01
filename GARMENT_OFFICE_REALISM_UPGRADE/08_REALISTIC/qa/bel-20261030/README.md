# Bengal Earth Lab: 3D proposal route

## Increment 6: knitwear first, Bengal craft added (30 Oct 2026)

The owner, 30 Oct: "its a rmg factory. so the idea is there will be fabric that is sourced from earth and sustainable, reuseable. the kutir shilpo is an addition to the rmg sector to represent bangaldesh", then "even the fabrics could be recycled fabric". The route now puts the knitwear core first. Bengal craft is added around it, following the owner's reference photos.

**The approved knitwear dressing is back on this route.**
- The garments and hangers are back in the four bays: `hideParts` and `trimParts` are gone.
- The four forms are back on the plinth: F022 to F025 are out of `hideNodes`.
- These approved items return:
  - the materials library (yarn cones, knit stitches, coconut-shell buttons)
  - the sample cards and the boardroom review trays
  - the MD development shelf
  - the studio sample-review table
  - the CAD dressing (Z14 is an interior zone again, as on `/realistic/`)
- Two approved items stay off, and something takes each one's place:
  - the water point (the clay kolshi now stands on its spot)
  - the experience-centre cloth fins (natural indigo swags replace them)

**Concept items:**

| Room | Option | Items |
|---|---|---|
| Experience centre Z30 | every | A fibre dish and a fabric-story card at the foot of each form. A low story at the foot of each bay: Earth (cotton), Golden fibre (jute and cotton, research), Second life from cutting waste (jhut in jute sacks, sorted by colour), Second life from used garments (take-back crate, a kantha mend). Natural indigo swags under the deck, clear of the AC unit and smoke detector. The jhut river: a sewing machine and patchwork across the free floor between the plinth and the material table (probed: open terrazzo). A small fig tree on the approved potted tree's footprint. |
| Design wing Z22, Z15, Z16, Z17 | every | The making line: one T-shirt in six steps. A fibre library of eight boxes and product passport cards, "ready for the EU ecodesign rules for apparel, still being drafted". A fabric lab with a GSM cutter, a balance, swatches marked for shrinkage, a grey scale and an empty durability log. Remake and repair: a kraft pattern, sorted offcuts, a pieced panel, a kantha mend. |
| Pilot rooms Z04, Z09, Z21, Z20 | every | Buyer room: knit swatches, product passport on the checklist, a board reading brief, fabric, lab dip, fit, tests, order. Records room: fibre origins, recycled content, durability tests and the product passport first, all "none yet", "to prepare" or "to be collected". Annex: knit swatches, a mending kit. Dining: the tong, a wall-mounted Bengali tea stall on the free west wall (probed clear, floor to ceiling), with "চা CHA · TEA" on its sign, clay cups, an electric lantern in the hurricane form and wood-slice stools. |
| Merchandising Z07 | option A | A circular knitwear studio. Wear: knitwear on bamboo rails. Remake: jhut sorted by colour, a basket lamp hung from the steel (underside 2.59, probed). Repair: a live-edge table, wood-slice stools, a basket lamp. Return: take-back sacks, bamboo armchairs and a bent-bamboo table. The Uthan: kula and dala over the canopy, alpana, four painted bamboo lantern posts, indigo yarn and small pots. A craft corner on the solid south wall. A low bamboo shelf of shokher hari pots, tepa putul and drums on the solid lower west wall (glass above 1.22 m), with a polo beside it. |
| Accounts suite Z06 | option A | The academy: a sewing machine on the demonstration bench, knit swatches, and a lesson on fibre, yarn, knit and reuse. |

**Removed concept items:**
- Earth-to-Product plinth
- craft material table
- the four home-goods collections in the bays
- bamboo lamp
- woven boardroom samples
- co-creation baskets
- Lab B basket screen
- the four home room-sets

**Overhead:** ceiling-hung concept items (the indigo swags) go into the interior overhead group, so they hide with the ceiling in the dollhouse views (`viewer/phase-dressing.js`).

**Tour:** 22 stops. Three are new:
- stop 7: the jhut river
- stop 11: the option A craft corner
- stop 17: the tea stall

**Measured for placement** (`ray_probe.py`, `node_boxes.py`):
- the forms: x 11.63, 12.34, 13.06, 13.77, z -8.56, bases r 0.19
- the bay garments: from y 0.90 up
- the dining ceiling lamps over both tables: so no new pendants there
- Z07 ceilings:
  - felt at 2.58 over x 10.2 and 13.45
  - steel at 2.59 over the remake table
  - steel at 2.49 over x 15.6, z -20.25

## Presenter polish (30 Oct 2026)

- **Option A in the rooms menu.** Merchandising and the accounts suite now sit under their own rooms-menu group, "Option A · proposed" (`roomGroups` in the config, read by `viewer/app.js`). Their tour cards say so in the line above the title.
- **No stills switch.** The "Show photoreal stills" switch is hidden on this route, which has no approved stills to show (`noRenderPhotos`).
- **`after-tour-play/`** (`bel_tour_play.py`): the guided tour played through its own buttons (Tour, Pause, then Next at each stop). All 19 counters and titles match the config, with no page, console or HTTP errors. The scene is unchanged from `1f64305`, so the frames in `after-tour19/` still apply.

## Increment 5: Lab B and the buyer project room (30 Oct 2026)

These rooms work in every option. Approved furniture stays.

| Room | Items |
|---|---|
| CAD room Z14, Lab B (digital product design) | A natural-fibre basket on the wall screen (face z -6.4707). Its specification panel reads "size: to be set, tests: none yet". The basket's technical drawing lies on the layout table (top 0.9145), with a ruler, pencil and swatch. A pinboard of swatches and colour chips hangs on the south wall. |
| Guest workspace Z04, buyer project room | In the pilot it is also the export and order desk. A sample tray, clay water, an order checklist ("all to be agreed with the buyer") and a project board on the screen: brief, samples, tests, approval and order, each with "date to agree". |

- **Tour:** 19 stops, adding Lab B after the labs.
- **Checks:**
  - `after-tour19/`: all 19 stops, without errors.
  - `after-inc5/` and `before-inc5/`: the same approved cameras CAM_15 and CAM_26.
  - `compare/inc5_lab_b_and_buyer_room.jpg`
- **Memory:** 58 MB of textures at full detail (244 textures). Low quality halves every canvas.
- **Presentation:** `presentation/` holds the contact sheet and a 75-second captioned slideshow of the 19 stops. They are made from these frames by `tour_slideshow.py`.
- **Phone check** (`after-mobile/`, from `bel_mobile_check.py`):
  - A 390 x 844 touch viewport at 2x loads with no page or HTTP errors, and the viewer picks low quality.
  - The layer uses 15.6 MB of textures.
  - The viewer estimates 467 MB of GPU memory for the whole scene, against 734 MB for the live approved `/realistic/` route at the same size. The proposal route shows no people and no render photos.
  - This is software WebGL in Chromium, so it does not measure phone speed.

## Increment 4: pilot rooms (30 Oct 2026)

These rooms work in every option. Approved furniture stays.

| Room | Items |
|---|---|
| Training room Z21, the pilot academy | A class of six at the approved training table (top 0.7493): fibre samples, notebooks, a frame loom and yarn cones. A craft wall of pinned samples and sketches on the solid west wall, clear of the screen. The lounge stays. |
| Staff cafe Z20 | Staff and artisan dining with the same care as the buyer rooms: clay plates, cups, jugs and bowls on hogla runners. Water in a clay kolshi and tea in clay on the pantry counter (top 0.9018). Glazes to be tested before use. |
| Audit room Z09, the records room | Five labelled evidence files and an evidence register on the table. An Open Record index on the solid north wall, listing each claim, its evidence and its status. Every status reads "none yet", "not connected" or "to be collected". |

- **Tour:** 18 stops, adding the academy annex and the records room. The records room comes just before the negotiation suite: evidence before the deal.
- **Checks:**
  - `after-tour18/`: all 18 stops, without errors.
  - `after-inc4/`: CAM_20, CAM_21, CAM_27 and `BEL_CAM_RECORDS`.
  - `before-inc4/`: the same approved cameras.
  - `compare/inc4_pilot_rooms.jpg`
- **Memory:** 53.2 MB of textures at full detail (235 textures, mostly printed cards and panels). Low quality halves every canvas.

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
