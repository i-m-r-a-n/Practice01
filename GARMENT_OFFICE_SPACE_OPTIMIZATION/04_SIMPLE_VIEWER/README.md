# 04 Simple interactive viewer

A client-first version of the 3D tour, built on the tested 03_INTERACTIVE_3D engine (three.js r169, vendored, no CDN).

It loads the redesigned model: Z06 / Z07 option B, with Cycles light baked onto the shell.

## Open it

Serve the **repository root** with any static web server, then open the viewer:

```
cd Practice01 && python3 -m http.server 8800
# http://localhost:8800/GARMENT_OFFICE_SPACE_OPTIMIZATION/04_SIMPLE_VIEWER/
```

The photorealistic stills are read from their place in the repository: `renders` paths in `assets/office_web_metadata.json`, relative to the root.

A deployment can set `window.__TOUR_CONFIG = { base, root, models }` to serve them from elsewhere.

## What the client sees

- **Opening screen:** "STAGE II — INTERACTIVE OFFICE EXPERIENCE" over the slowly turning model, with three choices.
  - **Start guided tour** opens a short choice, each option labelled with its stop count and length. The length is computed from the configured timings and shown before starting:
    - **Quick presentation:** 9 stops: overview, reception, experience centre, boardroom, MD office, merchandising, commercial & accounts, design studio, closing view. Each view holds 20 s.
    - **Complete office tour:** the approved 16 stops. Merchandising and accounts now show the redesign. Each view holds 13 s.
  - **Explore rooms** opens the room menu.
  - **View floor plan** shows the floor from above, with room names.
- **No tutorial pop-up.** The **?** button has a short help.
- **Tour controls:** only Back, Pause / Resume, Next and Exit tour, plus the room name and a progress bar.
  - Back and Next work while paused.
  - The last stop ends with **Tour complete**: Explore rooms, Play again, Return to overview.
- **Room menu:** 34 rooms in five groups: Arrival & Experience, Executive & Meeting, Merchandising & Operations, Design & Development, Staff Facilities. Plain names, and a small search at the bottom. Choosing a room closes the menu and opens the room on its approved render camera; rooms without one get an aerial view from above.
- **Room card:**
  - name and one or two sentences from the room description
  - **Look around**, **Photorealistic view**, **Back to floor plan**
  - a small **Explore freely (walk)** link
- **Look around:**
  - Drag to look. The room follows the pointer, like a 360° photo or Street View: drag right and the room moves right.
  - Scroll to zoom (field of view limited to 55–120 % of the room view).
  - **Double-click** or **Reset view** returns to the architectural camera.
  - The camera never leaves its standing point.
- **Explore freely:** W A S D / arrow keys and drag. Walls, glass and furniture stop you; on-screen arrows on touch screens; Esc ends it.
- **Transitions:**
  - from above into a room, a short flight that descends from above the walls
  - from one room to another at eye level, a 0.55 s dissolve, so the camera never passes through a wall
- **Photorealistic view:** labelled "Photorealistic Blender render — still image". Renders with people also say "People shown are illustrative". Closing it returns to the same room and camera.
- **Presentation mode:**
  - large controls, only "Exit presentation" in the header
  - full screen on the click
  - no zoom or drag (no accidental moves)
  - runs the quick presentation
- **Keys:** optional, never needed, ignored in text fields.
  - → / ← next / previous stop
  - Space: pause
  - Esc: exit photo / menu / tour / presentation / walk
  - H: overview
- **Floor plan:** room names only from above, never through walls at eye level. Names never overlap each other or the plan bar.
- **Loading failure / no WebGL:** a clear message plus the photorealistic renders of the main rooms, labelled as still images.

Real-time 3D is always the default. A render is shown only when the user asks for it.

## Files

- `index.html`, `style.css`, `app.js`: the viewer
- `vendor/`: three.js r169
- `assets/`:
  - `Optimized_Office_Interior_web_baked.glb` (20.0 MB)
  - `office_web_metadata.json`
  - `walk_grid.json` (+ `.png` QC)
  - logos

The baked-light code keeps the fix for the interleaved `COLOR_0` attribute: colour changes only through `getX` / `setXYZ` and `attribute.data.needsUpdate`. This avoids the earlier displaced-walls bug.
