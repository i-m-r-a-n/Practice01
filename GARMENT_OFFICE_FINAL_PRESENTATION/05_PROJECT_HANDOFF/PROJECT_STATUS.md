# Project status

_Last updated 2026-10-27 (Asia/Dhaka). History: git log of branch `claude/magical-hopper-74q4xq` in `i-m-r-a-n/Practice01`,
folder `GARMENT_OFFICE_FINAL_PRESENTATION`._

## Complete (each item checked; results in `verification_results.md`)

- Survey model of the whole ground floor from the client's hand-measured sketches; geometry check 75 / 75 on the delivered
  `.blend` (`04_DOCUMENTATION/geometry_verification.md`).
- Furnished office design for every room (34 zones), office use only: partitions, doors, finishes, ceilings, lighting, AC
  units, fire-safety devices, client logos, plants and decor. Editable Blender model with named collections; 1,494 objects.
- Delivery files built from the current scripts: `Final_Office_Interior.blend` (41.6 MB, all 67 textures packed inside; a
  lone copy reopened in an empty folder finds every texture) and `Final_Office_Interior.glb` (41.9 MB, re-import PASS).
- Final Cycles renders of all 38 views (33 interior views, 4 isometric views, 1 top view), checked one by one; index and
  contact sheet in `02_RENDERED_IMAGES/README.md` and `02_RENDERED_IMAGES/final_contact_sheet.jpg`.
- Drawings ID-01 furnished + dimensioned plan, ID-02 zoning + routes, ID-03 reflected ceiling + lighting, ID-04 power / data /
  fire (SVG, PNG, A3 PDF).
- Schedules (rooms, furniture, materials, lighting, dimensions), design notes, dimensional assumptions, technical coordination
  notes, unresolved issues, lighting concept, material board.
- 18-slide presentation: `Garment_Office_Design_Pitch.pdf` (opens, 18 pages) and editable `.pptx` (opens, 18 slides). Every
  render in the deck is byte-identical to a final render of this project (24 views); no previews are left in the deck.

## Render times (measured, Blender 5.2.3 Cycles on 4 CPU cores)

| Setting | Views | Average per view |
|---|---|---|
| 1600 x 900, 128 samples (key rooms) | 16 | 405 s (about 6.8 min) |
| 1600 x 900, 96 samples (other rooms) | 15 | 322 s (about 5.4 min) |
| 1920 x 1080, 128 samples (cover and closing images) | 2 | 606 s (about 10 min) |
| 1920 x 1080, 96 samples (isometric views) | 3 | 238 s |
| top view 1240 x 1612 (64 samples), SW isometric 1600 x 1200 (96 samples) | 2 | 125 s / 115 s |

The 38 current final images took 3.74 h of rendering; 51 final renders were made in total (4.99 h), because 13 views were
rendered a second time (the QC fixes below, and the cover and closing images at 1920 x 1080). The first versions are kept in
`02_RENDERED_IMAGES/final/superseded/`. `02_RENDERED_IMAGES/final/render_log.csv` lists every render with its time.

## Fixes made during the final-render QC (before delivery)

- Rugs rendered black (they shared the floor plane): lifted 0.45 in; affected views re-rendered.
- Reception view CAM_02 cut the logo: camera turned so the whole logo is in view.
- Lobby stair showed a stepped underside: plastered sloped soffit added under every flight (treads, risers, landings unchanged).
- Boardroom view CAM_10 had the door pulls of D19 filling the frame: camera moved 25 in into the room.
- Prayer rooms were underlit: wide-beam 3000 K downlights.
- CAD room: brand-green felt pinboard for tech packs on the south wall.
- Design corridor view CAM_32 was blocked by a dark wall: camera moved north of the store.
- Isometric and top views: framing computed from the building outline, so the whole floor fits with margins (the first SW
  isometric cut off the north end); top view re-rendered brighter.
- Drawing ID-02: route legend now fits inside the sheet frame.

## Remaining / next steps (not done; need the client, the site or a professional)

- Site measurements listed in `04_DOCUMENTATION/unresolved_issues.md` (floor-to-deck height, room 8 width, columns, beams,
  stair layouts, true north).
- Client decisions: head count per department, interior budget, HVAC information, use of the name "Global Design Studio".
- Professional reviews: structural (new openings), fire (exits), MEP (HVAC, power), accessibility (ramp, accessible WC).
- After measurements: update `survey.py`, rebuild, re-run `verify_all.sh`, re-render (`render_queue.sh`, `render_queue2.sh`).

## Persistence

- Git: the whole folder (scripts, docs, drawings, renders, presentation, .blend, .glb, CC0 assets) is committed to
  `i-m-r-a-n/Practice01`, branch `claude/magical-hopper-74q4xq`; retrieval is checked through the GitHub API after each push
  (see `verification_results.md`, section Persistence).
- Nothing was uploaded to Google Drive or any other service.
