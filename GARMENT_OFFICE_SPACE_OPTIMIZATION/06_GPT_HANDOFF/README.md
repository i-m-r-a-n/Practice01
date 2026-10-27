# 06 Handoff for GPT (integration owner)

- Branch: `claude/space-optimization`, based on `claude/realism-upgrade` / `claude/web-tour-assets`.
- The exact commit SHA is in `HANDOFF_COMMIT.txt` and on GitHub issues #13 and #12.

What I changed:

- I changed nothing on the live Worker `stage2-office-virtual-tour`, on GPT's branches, or on `claude/magical-hopper-74q4xq`.
- I changed nothing in `GARMENT_OFFICE_FINAL_PRESENTATION/` (approved model, renders, PDFs, videos) or in the client presentation package.

## What there is to integrate

| Item | Path | Note |
|---|---|---|
| Redesigned web model | `GARMENT_OFFICE_SPACE_OPTIMIZATION/04_SIMPLE_VIEWER/assets/Optimized_Office_Interior_web_baked.glb` | 20.0 MB, 45 cameras, Cycles light baked on the shell (`baked_light_scale` in the node extras), `WEB_INTERIOR` / `WEB_OVERHEAD` / `WEB_CAMERAS` groups, WebP + quantized like the current production GLB |
| Metadata | `.../04_SIMPLE_VIEWER/assets/office_web_metadata.json` | 45 cameras (38 approved + 7 new), 34 rooms (Z06 / Z07 descriptions updated, primary cameras CAM_36 / CAM_34), `tour` (16 stops), **new** `quick_tour` (9 stops). Render paths are repository-relative (`render.file`) |
| Walk map | `.../04_SIMPLE_VIEWER/assets/walk_grid.json` | rebuilt from the redesigned model (new partitions and furniture); same reachability as before (Z34 wudu too narrow and CAM_03 on the stair, as in production) |
| Simple viewer | `.../04_SIMPLE_VIEWER/index.html`, `style.css`, `app.js`, `vendor/` | the client interface (see its README) |
| New renders | `.../03_ROOM_RENDERS/after_with_people/` (Z06 / Z07 views with illustrative staff), `after_no_people/` (matched before / after) | 1600 x 900 JPG; PNG masters stay out of git |

## Camera / metadata migration

- **Unchanged:** 38 approved cameras (same names and matrices). The other 32 rooms and their descriptions are unchanged.
- **Added:**
  - CAM_34_Merchandising_Sample_Hub
  - CAM_35_Merchandising_Desks
  - CAM_36_Accounts_Suite
  - CAM_37_Accounts_Records_Discussion
  - CAM_38_Accounts_Public_Corridor
  - CAM_TOP_Z06_Z07 and CAM_ISO_Z06_Z07 (ortho)
- **Changed:**
  - Z07 primary camera CAM_11 → CAM_34.
  - Z06 primary camera CAM_16 → CAM_36.
  - Complete tour: Z07 stop uses CAM_34 and Z06 stop uses CAM_36 (before: CAM_11, CAM_16).
- `render.file` for CAM_11 / 12 / 16 and the new cameras points to `GARMENT_OFFICE_SPACE_OPTIMIZATION/03_ROOM_RENDERS/...`; the others still point to `GARMENT_OFFICE_FINAL_PRESENTATION/02_RENDERED_IMAGES/final/`.
- **Keep the old metadata for the original design.** It still matches the approved model, so the 34-zone presentation keeps working until the revision is approved.

## Suggested integration (only after review and the owner's choice)

1. Add a **separate route**, for example `/revised/`, pinned to the handoff commit:
   - `/revised/` → `04_SIMPLE_VIEWER/index.html`
   - `/revised/app.js`, `/revised/style.css`, `/revised/vendor/*`, `/revised/assets/*` → same paths under `04_SIMPLE_VIEWER/`
   - renders: either serve the repository paths, or set `window.__TOUR_CONFIG = { root: '/repo/' }` and map `/repo/<path>` to the pinned raw files
   - `Content-Type: model/gltf-binary` for the GLB, streamed unchanged
2. Leave `/` (production) as it is until the owner approves the revised layout.
3. To make it the main tour later, point `/` to the same files.

**Rollback:** remove the `/revised/` route. Production is never touched by steps 1-2.

## Checks I ran (details in `../05_BROWSER_QA/`)

- Functional and layout test in Chromium (SwiftShader WebGL).
- Firefox check.
- Every room and tour stop was reached on its camera.
- No panel overlaps at 1440x900, 1920x1080, 1280x800 or 390 px wide.
- See `05_BROWSER_QA/README.md` for results and what was **not** tested: Safari (no Safari here) and real-GPU frame rates.

## Rebuild commands (from `GARMENT_OFFICE_SPACE_OPTIMIZATION/02_IMPROVED_BLENDER_MODEL`)

```
blender -b --factory-startup --python scripts/build_model.py -- .
blender -b Optimized_Office_Interior.blend --python scripts/web/export_web_metadata.py -- EXP
blender -b Optimized_Office_Interior.blend --python scripts/web/export_door_boxes.py -- EXP
python3 -I scripts/web/make_walk_grid.py EXP/collision_tris.npy EXP/blender_cameras.json EXP/blender_rooms.json EXP/door_boxes.json EXP
python3 -I scripts/web/make_web_metadata.py EXP ../03_ROOM_RENDERS/after_with_people,../03_ROOM_RENDERS/after_no_people,../../GARMENT_OFFICE_FINAL_PRESENTATION/02_RENDERED_IMAGES/final ../04_SIMPLE_VIEWER/assets
blender -b Optimized_Office_Interior.blend --python scripts/web/bake_shell_lighting.py -- BAKED.glb --samples 96
node scripts/web/make_web_glb.mjs BAKED.glb ../04_SIMPLE_VIEWER/assets/Optimized_Office_Interior_web_baked.glb ../04_SIMPLE_VIEWER/assets/office_web_metadata.json scripts/lib_materials.py scripts/web/bake_web_colors.py
# (make_web_glb.mjs needs @gltf-transform/core, extensions, functions 4.1.1 installed next to it)
```

## Fix for the live site's "left / right" feel (optional, one line, GPT's code)

The live `app.js` turns the view in the direction of the drag ("first-person"): drag right and you look right, so the room slides left under the pointer. Clients used to Street View or 360° photos expect the opposite: the room follows the pointer.

The simple viewer uses that grab behaviour. To match it on the live site, in the walk-mode `pointermove` handler:

- `qe.yaw-=(dx)*.0035` → `qe.yaw+=(dx)*.0035`
- `qe.pitch-(dy)*.0035` → `qe.pitch+(dy)*.0035`

Keyboard turning stays the same: the right arrow turns right.

## Six-room `/realistic/` release (separate branch, not deployed)

- The rooms GPT had left (MD Office, Merchandising on the option B model, Design Studio) are on the branch `claude/realistic-rooms`, commit `cdf0e3e`. That branch is based on GPT's `chatgpt/office-realistic-20261027` at `07d9623`.
- The worker built from source `bcb92b0` is `GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/deploy/worker-realistic.js`. Its `test_worker.mjs` passes 41 of 41 checks; the checks cover both `/` and `/realistic/`.
- Deploy, verification and rollback (back to the `07d9623` worker) are in `GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/deploy/DEPLOY_SIX_ROOMS.md`.
- **It is not deployed.** The Cloudflare account this session can reach has no Workers, so the owner of `stage2-office-virtual-tour` has to run the deploy.
