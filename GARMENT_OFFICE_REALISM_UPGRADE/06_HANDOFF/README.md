# Realism upgrade - handoff for GPT (production integration)

Branch: `claude/realism-upgrade` (from `claude/web-tour-assets`). Commit: see `HANDOFF_COMMIT.txt` / GitHub issue #12.
Approved project files unchanged (`GARMENT_OFFICE_FINAL_PRESENTATION/`, SHA-256 checked). Nothing was changed on the live
Worker or on GPT's branches.

## What GPT should integrate

| Item | Path | Note |
|---|---|---|
| Improved model | `GARMENT_OFFICE_REALISM_UPGRADE/01_IMPROVED_MODEL/Final_Office_Interior_web_realism.glb` (19.45 MB) | Cycles light baked onto the shell, door-rail fix, colour / sheen fixes, 38 cameras, `WEB_OVERHEAD` group |
| Viewer (2 files) | `GARMENT_OFFICE_WALKTHROUGH_FINAL/08_WORKER_READY_TOUR/index.html` + `app.js` | the bundle the Worker serves now, plus: baked-light display, **simplified interface** (header: Guided tour / Overview / Rooms / Walk / help / full screen; one bottom panel row laid out by CSS grid so panels cannot overlap; the tour stop text sits in the tour card; help card on the first visit; drag to look around inside a room; links `?room=Z08`, `?tour=1`, `?walk=1`), display-quality profiles; requests `./model_web_baked.glb` first, then `./model_web.glb`, then `./model.glb` |
| Camera / room data | unchanged: `04_CAMERA_AND_TOUR/office_web_metadata.json`, `walk_grid.json` (also inside `app.js`) | the shell geometry was only subdivided, so cameras and the walk map stay valid |

### Steps (Worker)
1. Pin the Worker to the handoff commit (as you did with `f9048ef`).
2. Add route `/model_web_baked.glb` -> `GARMENT_OFFICE_REALISM_UPGRADE/01_IMPROVED_MODEL/Final_Office_Interior_web_realism.glb`
   at that commit (`Content-Type: model/gltf-binary`, streamed unchanged). Keep `/model_web.glb`, `/model.glb`, `/renders/*`.
3. Serve `08_WORKER_READY_TOUR/index.html` at `/` and its `app.js` at `/app.js` from that commit; bust the cache.
4. Check the live page: overview shows the open floor with soft light; Boardroom / MD office / Reception land on the render
   framing with warm light on the walls; walk and tour work (checklist in `VERIFICATION.md`).
Rollback: re-pin `f9048ef` (current production); the new route can stay (unused by the old bundle).

Do not integrate the bundle of commit `a50c6db`: with the baked GLB it stops on load (`TypeError ... reading 'lifted'`: the
vertex-colour attribute is interleaved and has no `userData`). Fixed in the handoff commit (colour floor applied with the
attribute accessors); the improved build now loads in Chromium. Production (`f9048ef`) never loads the baked GLB, so it is
not affected.

### Videos on the website
`/pitch.mp4` (linked in the GPT release notes) returns 404 since the Worker was re-pinned to `f9048ef`. Suggested routes at
the pinned commit, streamed unchanged with `Content-Type: video/mp4`, passing `Range` through (206 + `Content-Range`,
`Accept-Ranges: bytes`) so Safari and iPhone can play and seek:
- `/pitch.mp4` -> `GARMENT_OFFICE_WALKTHROUGH_FINAL/01_CLIENT_PITCH_VIDEO/Client_Pitch_Cinematic_Tour_web720.mp4` (16.9 MB; 1080p: `Client_Pitch_Cinematic_Tour.mp4`, 73.8 MB)
- `/tour.mp4` -> `GARMENT_OFFICE_WALKTHROUGH_FINAL/02_FULL_FLOOR_TOUR/Complete_Ground_Floor_Tour_web720.mp4` (26.0 MB; 1080p: `Complete_Ground_Floor_Tour.mp4`, 78.9 MB)

If you keep your own frontend instead, the only code change needed for the baked light is the material swap in
`../02_LIGHTING/LIGHTING_NOTES.md` ("Display in three.js").

## Evidence
- Before / after for the six flagship rooms: `../03_VISUAL_COMPARISON/` (Cycles | live now | improved, same cameras)
- Browser test and performance: `VERIFICATION.md`, `../05_PERFORMANCE/`
- Lighting method and limits: `../02_LIGHTING/LIGHTING_NOTES.md`; model fixes: `../01_IMPROVED_MODEL/MODEL_FIXES.md`
