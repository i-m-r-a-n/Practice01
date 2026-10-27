# Firefox check (the presentation browser)

Firefox 159.0 (Linux x86-64 release build from archive.mozilla.org), driven with puppeteer-core 24 over WebDriver BiDi,
running in a virtual X display (Xvfb) with Mesa llvmpipe as the WebGL 2 renderer (software GPU), window 1470 x 956
(MacBook Air 13-inch default). 27 Oct 2026.

| Run | Page | Result |
|---|---|---|
| `offline_*` | `09_MAC_OFFLINE_TOUR/Ground_Floor_3D_Tour.html` opened from `file://` (double-click case) | loads with baked light, help card, boardroom flight to `CAM_09_Boardroom_A`, photoreal render from `renders/` (1600 px), tour stop 3 in one card (room card hidden), walk 2.2 m in 2.5 s; 0 errors |
| `website_*` | `08_WORKER_READY_TOUR` served like the Worker (local static server) | same steps, same results; 0 errors |

Details: `offline_firefox_check.json`, `website_firefox_check.json`, logs and screenshots in this folder.
Not covered: macOS, a real GPU, Safari.

Re-run: `Xvfb :99 &` then `DISPLAY=:99 node ff_check.mjs <firefox binary> <page URL> <out dir> <label>`.
