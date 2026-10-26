# Project status

_Last updated: see the git log of branch `claude/magical-hopper-74q4xq` in `i-m-r-a-n/Practice01` (folder `GARMENT_OFFICE_FINAL_PRESENTATION`)._

## Complete

- Survey model of the whole ground floor from the client's hand-measured sketches; geometry check 75 / 75 PASS
  (`04_DOCUMENTATION/geometry_verification.md`).
- Furnished office design for every room (34 zones), office use only, with partitions, doors, finishes, ceilings, lighting,
  AC units, fire-safety devices, client logos, plants and decor; editable Blender model with named collections.
- Delivery files rebuilt from the current scripts: packed `.blend` (67 of 67 textures inside, reopened as a lone copy) and
  `.glb` (re-import PASS); geometry 75 / 75 on the delivered `.blend` (`verification_results.md`).
- Drawings ID-01 furnished + dimensioned plan, ID-02 zoning + routes, ID-03 reflected ceiling + lighting, ID-04 power / data
  / fire (SVG, PNG, A3 PDF).
- Schedules: rooms, furniture, materials, lighting, dimensions; design notes; dimensional assumptions; technical coordination;
  unresolved issues; lighting concept; material board render.
- Previews of all 33 interior views; render benchmark (reception, 1600 x 900, 128 samples: 381.5 s on 4 CPU cores).
- 18-slide presentation (PDF from HTML) + editable PPTX, built only from this project's renders and drawings.

## Render status

`02_RENDERED_IMAGES/final/render_log.csv` has one row per finished final render (camera, resolution, samples, seconds).
Final renders come from `01_EDITABLE_3D/scripts/render_queue.sh` (overall isometric, 16 key views, 17 other room views,
3 more isometric views), then `render_queue2.sh` (re-renders CAM_04, CAM_01 and CAM_07, which were rendered before the
rug and exposure fixes, and the Cycles top plan). Superseded images are moved to `02_RENDERED_IMAGES/final/superseded/`.
Views without a final render use the preview image, and the deck captions those "(preview render)".

## Remaining / next steps

- Site measurements listed in `04_DOCUMENTATION/unresolved_issues.md` (ceiling height, room 8 width, columns, beams, true north).
- Professional reviews: structural (new openings), fire (exits), MEP (HVAC, power), accessibility (ramp, accessible WC).
- After measurements: update `survey.py`, rebuild, re-verify, re-render.

## Persistence

- Git: the whole folder (scripts, docs, drawings, renders, presentation, .blend, .glb, CC0 assets) is committed to
  `i-m-r-a-n/Practice01`, branch `claude/magical-hopper-74q4xq`. Retrieval was checked through the GitHub API (file listing of the
  pushed folder, including the .blend and .glb).
- Chat: key files were also sent as downloadable attachments in the Claude conversation.
