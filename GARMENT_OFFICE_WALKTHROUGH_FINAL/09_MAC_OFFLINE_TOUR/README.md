# 3D tour for the Mac presentation (offline, no web server)

The interactive 3D tour as **one file**, `Ground_Floor_3D_Tour.html` (26.8 MB: page, three.js, tour app, room data and the
improved model with the baked Cycles light), plus `renders/` (the 38 photoreal Cycles stills shown by the
"Photoreal render" button). No internet, no Terminal, no installation.

## Open it (Mac)

1. Download `Ground_Floor_3D_Tour_Mac.zip` and double-click it: the folder `Ground_Floor_3D_Tour_Mac` appears.
2. Keep `Ground_Floor_3D_Tour.html` and the `renders` folder together in that folder.
3. **Firefox**: right-click `Ground_Floor_3D_Tour.html` -> Open With -> Firefox (or drag the file onto the Firefox window).
   Double-click opens it in the default browser (Safari or Chrome also work). Loading takes a few seconds; a short card
   then shows the three ways to explore.
4. Full screen: press `F` or the full-screen button (top right). Projector: System Settings -> Displays -> mirror the screen.
5. Before the meeting: connect the power adapter, close other tabs and apps, open the file once to check it.

Trackpad: drag to turn, Shift + drag to move, scroll or pinch to zoom. `Esc` returns to the overview. Help: `?` button.

## If it does not open

- "WebGL is not available": Firefox -> Settings -> General -> Performance: tick "Use recommended performance settings"
  (or "Use hardware acceleration when available") and restart Firefox. Chrome -> Settings -> System -> "Use graphics
  acceleration when available". Safari has WebGL on by default.
- The page shows but the photoreal stills stay black: the `renders` folder is not next to the HTML file (unzip the whole
  folder), or use the local server below.
- Local server (works in every browser): open Terminal, then
  ```
  cd ~/Downloads/Ground_Floor_3D_Tour_Mac
  python3 -m http.server 8000
  ```
  and open `http://localhost:8000/Ground_Floor_3D_Tour.html`. Stop it with Ctrl+C.

## What was tested

Opened from `file://`, as a double-click does, in **Firefox 159** and in Chromium (Linux, software GPU, window 1470 x 956 =
MacBook Air): the model loads with the baked light, the help card shows, the boardroom flight lands on its render camera,
the photoreal render opens from `renders/`, the guided tour shows stop 3 in one card, walking moves 2.2 m in 2.5 s; no
errors (`../05_PRODUCTION/firefox_check/`, `../05_PRODUCTION/offline_check/`).
Not tested here: macOS itself, Safari and a real Mac GPU (no Mac in this cloud machine); a real GPU is much faster than
the software rendering used in these tests.

Rebuild: `node ../03_INTERACTIVE_3D/build_offline_html.mjs ../08_WORKER_READY_TOUR <model.glb> <renders dir> .`
(model: `GARMENT_OFFICE_REALISM_UPGRADE/01_IMPROVED_MODEL/Final_Office_Interior_web_realism.glb`,
renders: `GARMENT_OFFICE_FINAL_PRESENTATION/02_RENDERED_IMAGES/final`).
