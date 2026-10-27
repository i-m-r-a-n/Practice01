# Realism upgrade - handoff for GPT (production integration)

Branch: `claude/realism-upgrade` (from `claude/web-tour-assets`). Commit: see `HANDOFF_COMMIT.txt` / GitHub issue #12.
Approved project files unchanged (`GARMENT_OFFICE_FINAL_PRESENTATION/`, SHA-256 checked). Nothing was changed on the live
Worker or on GPT's branches.

## What GPT should integrate

| Item | Path | Note |
|---|---|---|
| Improved model | `GARMENT_OFFICE_REALISM_UPGRADE/01_IMPROVED_MODEL/Final_Office_Interior_web_realism.glb` (19.45 MB) | Cycles light baked onto the shell, door-rail fix, colour / sheen fixes, 38 cameras, `WEB_OVERHEAD` group |
| Viewer (2 files) | `GARMENT_OFFICE_WALKTHROUGH_FINAL/08_WORKER_READY_TOUR/index.html` + `app.js` | same bundle the Worker serves now, plus: baked-light display, full-screen button, quality profiles; requests `./model_web_baked.glb` first, then `./model_web.glb`, then `./model.glb` |
| Camera / room data | unchanged: `04_CAMERA_AND_TOUR/office_web_metadata.json`, `walk_grid.json` (also inside `app.js`) | the shell geometry was only subdivided, so cameras and the walk map stay valid |

### Steps (Worker)
1. Pin the Worker to the handoff commit (as you did with `f9048ef`).
2. Add route `/model_web_baked.glb` -> `GARMENT_OFFICE_REALISM_UPGRADE/01_IMPROVED_MODEL/Final_Office_Interior_web_realism.glb`
   at that commit (`Content-Type: model/gltf-binary`, streamed unchanged). Keep `/model_web.glb`, `/model.glb`, `/renders/*`.
3. Serve `08_WORKER_READY_TOUR/index.html` at `/` and its `app.js` at `/app.js` from that commit; bust the cache.
4. Check the live page: overview shows the open floor with soft light; Boardroom / MD office / Reception land on the render
   framing with warm light on the walls; walk and tour work (checklist in `VERIFICATION.md`).
Rollback: re-pin `f9048ef` (current production); the new route can stay (unused by the old bundle).

If you keep your own frontend instead, the only code change needed for the baked light is the material swap in
`../02_LIGHTING/LIGHTING_NOTES.md` ("Display in three.js").

## Evidence
- Before / after for the six flagship rooms: `../03_VISUAL_COMPARISON/` (Cycles | live now | improved, same cameras)
- Browser test and performance: `VERIFICATION.md`, `../05_PERFORMANCE/`
- Lighting method and limits: `../02_LIGHTING/LIGHTING_NOTES.md`; model fixes: `../01_IMPROVED_MODEL/MODEL_FIXES.md`
