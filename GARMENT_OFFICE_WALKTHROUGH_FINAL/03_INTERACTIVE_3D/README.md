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

The screen has three parts: the **header** (logos; the ways to explore), the **3D view**, and **one panel row at the bottom**
(room card on the left, tools or the tour card in the middle, floor map on the right). Panels never cover each other.
On the first visit a short card explains the three ways to explore; the **?** button (or `H`) shows it again.

| Header button | What it does | Keys |
|---|---|---|
| **Guided tour** (gold) | 16 stops, plays by itself; the tour card shows the stop, its text and Back / Pause / Next / End tour; with **Photoreal renders** on, each room fades into its Cycles render | `T`, `Space` pause, `<-` `->`, `Esc` end |
| **Overview** | whole floor: drag to turn, Shift + drag (or right-drag with a mouse) to move, scroll / pinch to zoom; click a room or its name; tools: Reset view, Isometric, Plan, Ceilings, Room names | `O`, `C`, `L` |
| **Rooms** | shows / hides the room list (grouped, searchable). Choosing a room flies to the viewpoint of its render; then drag to look around, **Photoreal render** shows the still, **Walk from here** (or `W A S D`) walks on | `R`, `P` |
| **Walk** | eye level from the entrance lobby, collision with walls, glazing and furniture; floor map bottom right (click to go there) | `W A S D` / arrows, drag to look, `Shift`, double-click floor, `Esc` |
| **?** / **full screen** | help card (with display quality: High / Balanced / Low) / full screen for a projector | `H`, `F` |

Links that open a view directly: `?room=Z08` (a room by its zone code, e.g. the boardroom), `?tour=1`, `?walk=1`;
`?welcome=0` hides the help card, `?welcome=1` always shows it.

Suggested 5-minute client sequence: Overview (turn the building, ceilings off) -> Guided tour with Photoreal renders on ->
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
