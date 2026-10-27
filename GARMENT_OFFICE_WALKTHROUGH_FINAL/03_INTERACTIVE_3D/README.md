# Ground floor - interactive design experience (offline 3D tour)

A real-time 3D tour of the approved model, made with three.js r169 (included in `vendor/`, no internet needed).
Model: `../07_WEB_TOUR_ASSETS/Final_Office_Interior_web_baked.glb` (web copy of the approved model with the Cycles lighting
baked onto walls, floors and ceilings, colours matched to the Blender materials; falls back to `Final_Office_Interior_web.glb`).
Data: `../07_WEB_TOUR_ASSETS/office_web_metadata.json` and `walk_grid.json`.
Photoreal stills: `../../GARMENT_OFFICE_FINAL_PRESENTATION/02_RENDERED_IMAGES/final/` (the 38 Cycles renders).

## Open it on a Mac (2 minutes)

1. Download the repository branch `claude/web-tour-assets` (GitHub: Code -> Download ZIP) and unzip it, or `git clone`.
2. Open **Terminal**, go into the unzipped folder and start the built-in web server:
   ```
   cd ~/Downloads/Practice01-claude-web-tour-assets
   python3 -m http.server 8000
   ```
3. Open **Chrome or Safari** at
   `http://localhost:8000/GARMENT_OFFICE_WALKTHROUGH_FINAL/03_INTERACTIVE_3D/`
   (double-clicking `index.html` does not work: browsers block loading the model from a file).
4. For the meeting: press **Ctrl+Cmd+F** (Safari / Chrome full screen) and close other tabs. Power adapter connected.
5. Stop the server afterwards with **Ctrl+C** in Terminal.

## Presenting

| Mode | How | Keys |
|---|---|---|
| Overview | drag to orbit, right-drag (two-finger drag) to pan, scroll / pinch to zoom; click a room on the model or its name | `O`, `C` ceilings, `L` labels |
| Rooms | room list on the left (grouped by function, searchable); the camera flies into the room to the exact viewpoint of the render | `R` |
| Photoreal render | button on the room card: the offline Cycles render of exactly that viewpoint, labelled as a still image | `P`, `Esc` back |
| Walk | eye-level walk with collision against walls, glazing and furniture; minimap bottom right (click to go there) | `W A S D` / arrows, drag to look, `Shift` faster, double-click floor, `Esc` |
| Guided tour | 16 stops (overview, lobby, reception, experience centre, boardroom, executive suite, commercial, HR, merchandising, CAD, design studio, sample room, cafe, lounge, prayer, final reveal); with **Photoreal stops** on, each room dissolves into its render | `Space` pause, `<-` `->` previous / next, `Esc` stop |

Suggested 5-minute client sequence: Overview (turn the building, ceilings off) -> Guided tour with Photoreal stops ->
pause at the boardroom and MD office for questions -> Walk from the reception to the experience centre -> Plan view.

What to say: "This is the proposed design. The moving 3D model is real-time; the still images are photoreal renders
of the same model. Final dimensions and technical details are subject to site verification."

## Notes

- Tested in headless Chromium (WebGL 2, software GPU): see `../05_PRODUCTION/viewer_test/viewer_test.json`.
  A real GPU runs it much faster than this software test; on a slow machine add `?scale=0.6` to the address.
- The light on walls, floors and ceilings is baked from Cycles (light pools, soft shadows under furniture, darker corners);
  furniture, glass and reflections are still real-time and simpler than in the renders - use the photoreal renders for
  material questions.
- `qc/` holds the camera check page used to compare the 38 render cameras with the model.
