# 05 Browser QA: simple viewer (04_SIMPLE_VIEWER)

## Result

| Browser | Version | WebGL | Checks | Time |
|---|---|---|---|---|
| Chromium (Playwright 1.63.0) | Chrome for Testing 153.0.8010.12, headless | SwiftShader (software) | **64 / 64 pass**, no runtime errors | 1862 s |
| Firefox (puppeteer-core, WebDriver BiDi) | Firefox 159.0, in Xvfb | Mesa llvmpipe (software) | **64 / 64 pass**, no runtime errors | 288 s |

- Full logs: `chromium_run.log`, `firefox_run.log`.
- Machine-readable results: `chromium_run/results.json`, `firefox_run/results.json`.
- Screenshots of every state at each tested size are in `chromium_run/` and `firefox_run/`.

## What the 64 checks cover

- **Load:**
  - the model loads with baked light;
  - 102 merged meshes (2072 before merging);
  - 34 rooms, 45 cameras, 9 quick stops, 16 complete stops.
- **Home screen:** the title and the three choices are present. The idle rotation is off with `?motion=0`.
- **Tours:**
  - The quick tour shows "about 3½ min" (196 s); the complete tour shows "about 4½ min" (255 s). Both lengths come from the configured hold times.
  - Pause, Back and Next work while paused, plus → / ← / Space.
  - Every one of the 9 quick stops lands on its camera with no dissolve left on screen.
  - The tour ends with "Tour complete" and its three actions; Exit tour works.
- **Room menu:**
  - 34 rooms in 5 groups;
  - choosing Merchandising closes the menu and lands on CAM_34;
  - **all 34 rooms** open on their approved camera (or an aerial view).
- **Look around:**
  - drag turns the view the "grab" way;
  - scroll zoom stays within limits;
  - Reset view appears after looking;
  - double-click returns to the architectural camera.
- **Photorealistic view:** labelled "Photorealistic Blender render — still image. People shown are illustrative." Closing it returns to the same room and camera.
- **Floor plan:** seen from above with room names; clicking a name opens the room.
- **Explore freely:**
  - W moves forward;
  - the walker never ends inside a blocked cell;
  - Esc returns to the room card.
- **Presentation mode:**
  - runs the quick tour, with the menus hidden and Exit presentation shown;
  - requests full screen on the click;
  - Esc exits.
- **Layout at 1440x900, 1920x1080, 1280x800 and 390x844** (home, tour, menu, room, plan, walk, presentation). Each state is checked for:
  - no overlapping panels;
  - no panel outside the window;
  - no horizontal scroll;
  - no clashing room labels.

## Limits (not tested here)

- **Safari / iPad / iPhone:** not tested. There is no Safari in this environment.
- **Real GPU frame rate:** not measured. Both runs use software WebGL, which draws about 1-14 frames per second, so the times above are not performance figures.
- **Phone:** 390 px is a desktop browser at phone width, not a real phone. The on-screen walk arrows appear only on touch devices, so they were not exercised.
- **Load time:** served from localhost, not a real network.

## Fixes this QA led to

- **Viewer:**
  - dissolve driven by the render loop (no stale frame on slow GPUs);
  - taller tour text;
  - compact walk card;
  - phone walk layout: hint on top, no floor map;
  - Exit presentation button state.
- **Test:**
  - Playwright wheel signature;
  - hold W until the camera moves;
  - exit full screen before resizing;
  - key names for WebDriver BiDi;
  - double-click option `count` for puppeteer.

## Run it again

```
cd Practice01 && python3 -m http.server 8800 &
URL="http://127.0.0.1:8800/GARMENT_OFFICE_SPACE_OPTIMIZATION/04_SIMPLE_VIEWER/?motion=0"
NODE_PATH=$(npm root -g) node GARMENT_OFFICE_SPACE_OPTIMIZATION/05_BROWSER_QA/test_simple_viewer.js "$URL" OUT chromium
FIREFOX_BIN=<firefox> PPTR_MODULES=<dir with puppeteer-core> sh GARMENT_OFFICE_SPACE_OPTIMIZATION/05_BROWSER_QA/run_firefox.sh "$URL" OUT
```
