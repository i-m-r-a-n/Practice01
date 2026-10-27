# Live tour - real-WebGL check (GPT frontend, commit 50923eb)

URL: https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/ - checked 27 Oct 2026, 10:51-11:08 Asia/Dhaka.
Browser: headless Chromium (Playwright) with WebGL 2 through SwiftShader (software GPU, about 1 frame per second on this
shared machine). Script: `qa_live_site.js`; screenshots in `run_50923eb/`. The live viewer was not changed.

| Step | Screenshot | What happened |
|---|---|---|
| Load | `01_loaded.jpg` | Loads: overlay hides, 34 rooms listed. Console: `Loaded office model: {nodes: 1150, cameras: 38, ceilingMeshes: 0}` |
| Overview | `01_loaded.jpg`, `04_overview.jpg` | The floor is covered by the white steel deck: no rooms visible from above; room markers sit on the roof, too small to read |
| Room "Boardroom" | `02_room_boardroom.jpg` | The Cycles render panel opens (works). The 3D camera was still above the roof 6 s later |
| Ceiling button | `03_ceiling_button.jpg`, `05_overview_ceiling_button.jpg` | No visible change in the overview (deck stays); after the room click the 3D view showed grey geometry with floating markers |
| Walk mode + W | `06_walk_forward.jpg` | Empty view (no geometry in front of the camera) |
| Guided tour start / next | `07_tour_start.jpg`, `08_tour_next.jpg` | Works: stop 2/17 "Entrance lobby" shows the lobby interior. Room markers float in front of the interior (seen through walls); tour bar overlaps the room card; 17 stops (brief: 16) |
| Pause / stop / search | - | Not run: the check was stopped to give the CPU back to the video render |

## Causes found and fixes available on `claude/web-tour-assets`

1. **`ceilingMeshes: 0`** - three.js `GLTFLoader` sanitises node names (whitespace -> `_`, `[ ] . : /` removed):
   "Steel deck / slab" arrives as `Steel_deck__slab`, so the name regex finds nothing and the deck/ceilings never hide.
   Fix: load `07_WEB_TOUR_ASSETS/Final_Office_Interior_web.glb` and toggle one node
   (`gltf.scene.getObjectByName('WEB_OVERHEAD').visible = false`), or match `names.overhead_threejs` from
   `office_web_metadata.json` with the original GLB.
2. **Room cameras** - `office_web_metadata.json` has the exact position + quaternion + fov + lens shift of all 38 render
   cameras (checked: `05_PRODUCTION/camera_qc/`), so a room view can land exactly on the render's framing.
3. **Walk collision** - `walk_grid.json` (walls, glazing and furniture; door openings free; one lookup per step).
4. **Markers through walls** - hide room markers at eye level (the reference viewer shows them only above 3 m, de-cluttered).

Caveat: with a software GPU animations run at about 1 fps; if a transition is frame-based rather than time-based it may
simply not have finished in the waiting time (rows "Room" and "Overview"). The deck covering the overview and
`ceilingMeshes: 0` do not depend on speed.
