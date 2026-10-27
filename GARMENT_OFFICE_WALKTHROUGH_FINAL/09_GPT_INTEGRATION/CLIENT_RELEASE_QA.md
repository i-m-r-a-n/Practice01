# Stage II client presentation — validated release

Date: 27 October 2026 (Asia/Dhaka)

## Single entrypoint

**Presentation control center:** https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/present

This standalone page launches the finished films, live 3D explorer, 18-slide proposal PDF and architectural render book. It uses an original approved project Cycles render (not stock imagery).

## Production routes

| Route | Asset | Validation |
|---|---|---|
| `/` | Stable GPT-patched baked-light interactive 3D viewer | Cloudflare Chromium Browser Rendering HTTP 200, actual canvas, overlay hidden, 19.5 MB GLB loaded |
| `/pitch.mp4` | 720p H.264 cinematic pitch film | HTTP 206 on Range request, MP4 `ftypisom`, Chromium video metadata: 77.013 s, 1280×720 |
| `/tour.mp4` | 720p H.264 full ground-floor tour | HTTP 206 on Range request, MP4 `ftypisom`, Chromium video metadata: 121.002 s, 1280×720 |
| `/presentation.pdf` | Original 18-slide pitch deck | HTTP 206 partial request and `%PDF-1.4` header |
| `/render-book.pdf` | Original 41-page architectural render book | HTTP 206 partial request and `%PDF-1.4` header |
| `/present` | Client presentation control center | HTTP 200, title + intended four primary presentation resources and full-film card visible in Cloudflare Browser Rendering, screen visually inspected |

The Worker proxies immutable GitHub sources:

- Patched production viewer JavaScript: `6a65b7d10982563ee7fdb059b791a67126d98ccb`.
- Baked-light web model and original approved renders/docs: `ddf99eee703600ee722f06595708439560373567`.
- Finished 720p films: `cc2bd270c896adba1a127ad2a2216a8a4cdf10a7`.
- Presentation hub: `809bb9ec05d21aae83e5c525910607cd6956a563` on GPT branch.

**Worker deployment:** `f96a275cb152445dba29e75430d9e85e` (2026-10-27 09:41 UTC; about 15:41 Asia/Dhaka). The live Worker was subsequently checked and still opens the original tested 3D model.

## GitHub source and rollback

- This branch: `chatgpt/stage2-video-ready-client`.
- Worker source: `GARMENT_OFFICE_WALKTHROUGH_FINAL/09_GPT_INTEGRATION/worker_video_delivery.js`.
- Presentation page: `GARMENT_OFFICE_WALKTHROUGH_FINAL/09_GPT_INTEGRATION/client_presentation.html`.
- Prior approved production Worker for rollback: `GARMENT_OFFICE_WALKTHROUGH_FINAL/09_GPT_INTEGRATION/worker.js` on `chatgpt/stage2-baked-integration`; its baked-light 3D GLB and frontend remain unchanged by this release.

## Additional Claude realism branch (not promoted)

Claude's `claude/realism-upgrade` commit `cc2bd270c896adba1a127ad2a2216a8a4cdf10a7` includes a simplified GUI, improved ambient occlusion, a 19.45 MB baked-light model, an offline Mac file and Firefox/Chromium screenshot tests. It is **not yet installed on the live Worker**, because Cloudflare Browser Rendering of the isolated preview repeatedly remained on `Loading the 3D model… Starting…`; a diagnostic observed the module at times starting but never reaching ready after 32 seconds. No definitive production-browser failure is claimed; the discrepancy between Claude's local Firefox tests and Cloudflare software rendering needs further investigation. Preserve the current tested viewer until additional acceptance passes.

## Presentation sequence

1. Open `/present` on the Mac and project the screen to the meeting display.
2. Play the 77 s cinematic pitch movie.
3. Open `/presentation.pdf`: concept, floor plan, zoning.
4. Enter the interactive 3D overview and selected rooms; use original Cycles stills to communicate photorealistic intent.
5. Play `/tour.mp4` if the client wants the continuous walkthrough.
6. Discuss materials, missing site measurements, HVAC/fire/structure, costing and next-step approval.
7. Keep the two MP4 files and the PDFs downloaded locally as a backup for connectivity interruptions. The Mac offline tour package is in Claude's `GARMENT_OFFICE_WALKTHROUGH_FINAL/09_MAC_OFFLINE_TOUR/` branch deliverables, subject to download verification.

## Remaining acceptance

- Safari/Mac GPU visual frame rate and input handling have not been independently verified from ChatGPT tools.
- Exact Cycles realism is not promised in real-time WebGL.
- Site dimensions, egress, structural and MEP details remain concept-stage assumptions pending verification.
- Final new Claude bundle can be integrated only from a tested commit on Claude's asset branch; do not force-push or overwrite the existing production Worker during the client meeting.
