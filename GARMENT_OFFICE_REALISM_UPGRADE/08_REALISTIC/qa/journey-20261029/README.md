# Buyer journey increment (29 Oct 2026): Lobby, CAD, Sample room, Lounge / Training, Experience Centre

The brief came from ChatGPT's review: "complete the buyer's design-to-sample journey". The work is on branch `claude/realistic-sprint-20261028`.

## Method
- **Before frames:** `before/` was captured from the verified live build `d5939f9` before any change, through the local preview with UI hidden.
  - The run is `before/room-check.json`: no page, console or HTTP errors.
- **After frames:** each room folder holds its after frames from the same reference camera, framing and viewport.
  - People are on, as in the before frames. None of these rooms has people in the release.
- **Visitor frames:** before and after frames at eye height use the walk-QA hooks (`capture_visitor.py` spots).
  - Their before versions were served from `d5939f9`'s `dist/app.js` and `dist/index.html` with the current assets.
- **Room checks:** each room's `room-check.json` holds:
  - the frames
  - a walk on free floor that must not end inside geometry
  - page, console and HTTP errors
  - failed requests
- **Scope:** local Chromium with software WebGL. Not live, Safari or MacBook proof.

## Tour rooms outside the release zones
- `release-config.json` → `interiorZones` lists rooms that get only the interior layer, with no props, people or screens.
- These rooms are added one by one as they are designed. They stay out of `releaseZones`, so no people appear in them.

## 1. Entrance Lobby (Z01, CAM_03): `lobby/`
- **Brand wall light (`LB_BRAND_LIGHT`):**
  - The three existing track spots LT003–LT005 light the oak slats in warm scallops. This is a position-limited shader on `oak_slat`, inside the brand-wall box only.
  - The gaps stay dark, so the relief reads.
  - The wall falls off a little towards the floor.
  - The white logo panel and the logos are unchanged.
- **Wood warmth (`LB_WOOD_WARMTH`):**
  - the walnut of the check-in desk top (box around F001 only)
  - the oak of doors D02 and D17
  - Same textures. The same materials elsewhere in the building are unchanged.
- **Woven detail (`LB_WOVEN_PIER`):** one narrow handloom hanging (0.36 × 1.42 m) on the only blank pier: the east wall between interior windows W11 and W12, on the route to the Reception door D04.
  - Design reference; maker to be identified.
  - Top on the window-head line, hem near the sill line.
  - 0.15 m and 0.10 m clear of the window frames.
  - It hangs 5 cm off the wall on an oak rod with two brackets. The folds stay at least 2.5 cm off the wall.
  - D04 is 1.4 m away.
- **The north wall has no other blank surface:** the slats run x 4.27–7.51, door D17 ends at x 4.00, and only 0.27 m of wall is left.
- **Checks:**
  - CAM_03 before/after at identical framing
  - A walk on the arrival route, from inside the entrance steps (6.8, 4.4) north past the desk and the hanging: 4.17 m, ending 0.2 m short of the brand wall.
  - No page or HTTP errors. Two `net::ERR_ABORTED` reports (`basecolor.ktx2`, `panjabi.glb`) are the known harness artefact: the terrazzo texture did load (`finishes.refined`).
- **Texture and memory:**
  - One 256 × 1011 canvas, about 1.4 MB with mipmaps at full detail (a quarter of that on low quality).
  - Four shared materials get a position test in their shader: `oak_slat_baked`, `walnut`, `walnut_baked`, `oak`.
- **Bug fixed on the way:** the place-patch program cache key now carries the boxes. Before, two materials of the same type could share one compiled program and apply the wrong box.

## 2. CAD / technical design (Z14, CAM_15): `cad/`
One illustrative development exercise for a knit cardigan runs through the room. All graphics are self-drawn and generic: no software interface, buyer, brand or measurement.
- **Screens (`CAD_SCREENS`):** the six monitors of the three CAD desks and the north wall screen. The overlays sit 3 mm in front of the existing screen faces.
  - Monitors: front and back technical flats with callouts, pattern pieces on a grid, a grading nest, a marker, and a knit stitch chart.
  - The wall screen shows the exercise in four steps: sketch, technical flat, pattern, knit swatch. It is titled "Development exercise: knit cardigan (illustrative)".
- **Pinboard (`CAD_PINBOARD`):** the felt tech-pack board keeps its 18 sheet positions. It reads left to right as the exercise runs: sketch, flats and stitch chart, pattern and grading, marker, fit notes, approval. Knit swatches and a coconut-shell button card are pinned among the sheets.
- **Layout table (`CAD_LAYOUT_TABLE`):**
  - a kraft marker sheet (1.2 × 0.75 m) with an L-square, three pattern weights and a pencil
  - a small folded knit reference set and a header card at the west end
  - the east third stays clear for work
- **Checks:**
  - CAM_15 before/after at identical framing.
  - A walk along the free aisle (x 24.2), north to south: 4.93 m.
  - No page or HTTP errors and no failed requests.
  - Nothing stands on the floor, so chair and desk clearance are unchanged.
- **Tabletop support:**
  - The table-top height was ray-cast in the viewer: 0.9145 m. The GLB query rounds it to 0.91, and at first the sheet sat 3 mm inside the top, unseen.
  - Every flat item now rests on the measured top.
- **Texture and memory, at full detail (half each side on low quality):**

  | Texture | Size | Memory with mipmaps |
  |---|---|---|
  | Screen atlas (all seven screens) | 1536 × 1164 | about 9.5 MB |
  | Pinboard | 1280 × 553 | about 3.8 MB |
  | Kraft sheet | 1024 × 640 | about 3.5 MB |
  | Header card | small | – |

  The knit textures reuse the shared stitch tiles.
- **Bug fixed on the way:** a temporal-dead-zone error (`LIN` / `srgb` used before their declaration) stopped the page loading. A full page-load check caught it, and the constants now sit with the other helpers.
