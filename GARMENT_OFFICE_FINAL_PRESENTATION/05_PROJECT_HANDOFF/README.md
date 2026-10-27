# Ground-floor corporate office - project handoff

Client: Stage II Knitting Apparel Ltd. / Stage II Knitting Apparel Unit-1 / Zara Fashion - Holding 329/2, Ward 15, Vogra, Bason, Gazipur.
Scope: ground floor only, office use only (corporate headquarters + design development centre). Interior design proposal - not for construction.

## Where everything is

| Folder | Contents |
|---|---|
| `01_EDITABLE_3D/Final_Office_Interior.blend` | editable Blender 5.2 model; all 67 textures are packed inside the file (a lone copy reopened in an empty folder finds every texture - `verification_results.md`) |
| `01_EDITABLE_3D/Final_Office_Interior.glb` | glTF binary export (textures embedded, cameras included) |
| `01_EDITABLE_3D/scripts/` | all generation scripts (see below) |
| `01_EDITABLE_3D/assets/` | CC0 textures and models (`LICENSES.md`), client logos cropped from the supplied business card / profile |
| `01_EDITABLE_3D/phase1_shell_reference/` | phase 1 shell model, shell views and the original dimension schedule |
| `02_RENDERED_IMAGES/final/` | final Cycles renders of all 38 views (PNG + JPG), `render_log.csv` with times, `superseded/` first versions; index in `02_RENDERED_IMAGES/README.md`, all finals on `final_contact_sheet.jpg` |
| `02_RENDERED_IMAGES/previews/` | 960 x 540 preview renders of all 33 interior views |
| `02_RENDERED_IMAGES/plans/` | drawings ID-01 to ID-04 as SVG, PNG and A3 PDF |
| `03_PRESENTATION/` | `Garment_Office_Design_Pitch.pdf`, editable `.pptx`, `Garment_Office_Render_Book.pdf` (all 38 renders, A3), HTML sources, `assets/` (renders, drawings, logos, finish swatches cropped from the material board render) |
| `04_DOCUMENTATION/` | schedules (rooms, furniture, materials, lighting, dimensions), design notes, assumptions, technical coordination, geometry verification |
| `05_PROJECT_HANDOFF/` | this README, `PROJECT_STATUS.md`, `verification_results.md` |

## Scripts (run from any folder; Blender 5.2.3)

| Script | Purpose |
|---|---|
| `survey.py` | survey data from the client's hand-measured sketches (all walls, openings, rooms, measurement schedule) - edit values here |
| `office_layout.py` | fit-out data: partitions, doors, zones + finishes, furniture placements, ceilings, lights, AC, fire safety |
| `lib_mesh.py`, `lib_assets.py`, `lib_materials.py` | mesh builder, parametric furniture / fixtures, PBR material library |
| `build_model.py` | builds the whole model: `blender -b --factory-startup --python build_model.py -- OUT_DIR` (add `--no-glb` to skip the export, `--pack` to pack the textures into the .blend for delivery) |
| `cameras.py` | the 38 camera views |
| `render_views.py` | renders cameras: `blender -b MODEL.blend --python render_views.py -- --out DIR --quality preview|final --cams CAM_01_Reception_A,...` |
| `render_queue.sh` | sequential final render queue (resumable, skips finished images) |
| `render_queue2.sh` + `rerender_list.txt` | second pass after the first queue: re-renders the views listed (with the reason) in `rerender_list.txt` |
| `verify_geometry.py` | checkpoint A: measures the model and compares with the survey values |
| `verify_files.py`, `verify_deck.py`, `verify_all.sh` | reopen the delivered .blend (lone copy), re-import the .glb, run the geometry check, check the PDF / PPTX and that every deck image is one of this project's renders; writes `verification_results.md` |
| `make_drawings.py` + `export_drawings.js` | 2D drawings (SVG) and their PNG / PDF export (Node + Playwright) |
| `make_schedules.py`, `material_board.py` | schedules (CSV/MD) and the material board render |
| `make_presentation.py` + `export_presentation.js` | 18-slide deck (HTML -> PDF) and editable PPTX (`deck_manifest.json` lists every render shown and its caption) |
| `make_render_index.py` | `02_RENDERED_IMAGES/README.md` (index of all views) and `final_contact_sheet.jpg` |
| `make_render_book.py` + `export_render_book.js` | render book PDF (A3 landscape): cover, contents, one page per final render, notes |
| `fetch_assets.py` | re-downloads the CC0 assets if the assets folder is missing |

## Resume in a new cloud session

1. Get the files: `git clone` the repository `i-m-r-a-n/Practice01` and check out branch `claude/magical-hopper-74q4xq`; the project is in `GARMENT_OFFICE_FINAL_PRESENTATION/`.
2. Install Blender 5.2.3 (if missing): download the Linux x64 tarball from download.blender.org, extract to `/opt`, link
   `/usr/local/bin/blender`; for Workbench/EEVEE previews install the Mesa EGL libraries (`libegl1 libgl1 libglx-mesa0`).
3. Rebuild: `blender -b --factory-startup --python 01_EDITABLE_3D/scripts/build_model.py -- 01_EDITABLE_3D/work` (working copy);
   delivery files: `... build_model.py -- 01_EDITABLE_3D --pack`, then `01_EDITABLE_3D/scripts/verify_all.sh`
4. Render: `01_EDITABLE_3D/scripts/render_queue.sh` (edit the paths at the top if the folder moved).
5. Drawings / schedules / deck: `python3 make_drawings.py ../../02_RENDERED_IMAGES/plans && node export_drawings.js ../../02_RENDERED_IMAGES/plans`,
   `python3 make_schedules.py ../../04_DOCUMENTATION`, `python3 make_presentation.py ../.. && node export_presentation.js ../../03_PRESENTATION`,
   `python3 make_render_index.py ../..`, then `./verify_all.sh` (checks model files and deck, rewrites `verification_results.md`).

## To change a measurement

Edit the value in `survey.py` (for example `R8_E` for the room 8 width or `DECK_H` for the ceiling height), rebuild, re-run
`verify_geometry.py`, the drawings and the renders. Furniture positions in `office_layout.py` are absolute plan inches, so
check the rooms next to any changed wall.
