# Worker-ready tour (deployment-ready alternative, not deployed)

The tour of `03_INTERACTIVE_3D` as **two static files** that load nothing from a CDN and need no import map:

| File | Size | Content |
|---|---|---|
| `index.html` | 63 KB | page, CSS and the three client logos inline |
| `app.js` | 747 KB | one ES module: three.js r169 (vendored) + tour app + `office_web_metadata.json` + `walk_grid.json` |

The page requests only these URLs, relative to itself:

| URL | Serve |
|---|---|
| `./app.js` | this `app.js` |
| `./model_web.glb` | `GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/Final_Office_Interior_web.glb` (16.6 MB). If it is missing, the page falls back to `./model.glb` (the original 41.9 MB GLB the Worker already serves; ceilings still toggle, colours as exported) |
| `./renders/<camera>.jpg` | the 38 Cycles renders (the Worker already serves `/renders/CAM_xx.jpg`) |

## Why it was not deployed from this session

- The live site is GPT's frontend on `chatgpt/interactive-office-tour` (issue #12 and your instruction: do not overwrite it;
  integration is coordinated on GitHub first).
- The Cloudflare credential available in this session lists **0 accounts**, so the Worker `stage2-office-virtual-tour`
  cannot be read or changed from here.

## To publish it (when you and GPT agree)

1. Worker route `/model_web.glb` -> the web GLB above (same way the Worker proxies `model.glb`).
2. Replace the Worker's `index.html` and `app.js` with these two files (keep the old pair for rollback; nothing else changes).
3. Check the live URL in Chrome and Safari: model loads, room list, a room flight, the photoreal button, walk, tour.
Rollback = put the previous `index.html` / `app.js` back; the model and renders are untouched.

Checked with a local static server that serves exactly the URLs above (headless Chromium, WebGL 2): the page requests only
`/`, `/app.js` and `/model_web.glb` (+ `/renders/...` when a render is shown), loads in about 6 s, merges 2,306 meshes into
92 draw calls, no console errors. The full interaction test is in `../05_PRODUCTION/viewer_test/viewer_test.json`.
Rebuild: `node ../03_INTERACTIVE_3D/build_worker_bundle.mjs .` (esbuild 0.24).
