# Stage II office tour — production release notes

Release date: **27 October 2026** (Asia/Dhaka)

## Client-facing URLs

- Main interactive office tour: https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/
- Boardroom example: https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/?room=Z08
- Cinematic film (77 sec, H.264 1080p): https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/pitch.mp4
- 18-slide concept pitch PDF: https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/pitch-deck.pdf
- Full render reference book PDF: https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/render-book.pdf

## GitHub and revisions

- Original verified design remains on `claude/magical-hopper-74q4xq`.
- Claude web-asset work remains on `claude/web-tour-assets`.
- Snapshot branch: `chatgpt/stage2-claude-tour-snapshot-20261027`.
- GPT integration branch: `chatgpt/stage2-integrated-client-tour`.
- Cloudflare Worker: `stage2-office-virtual-tour`.
- **Pinned production source commit:** `47ebc4d29088dd0de0ef7546d453a5d4e90a61a6` (not affected by subsequent commits).

## Included functionality

- Bundled three.js r169 interactive experience, **no third-party CDN imports**.
- Optimized 16.6 MB web GLB (original 41.9 MB), corrected web color baking for furniture and finishes.
- 34 selectable rooms, 38 verified camera viewpoints.
- 16-stop guided tour, next / previous, pause / resume and photorealistic Blender-render reference at each stop.
- Full-floor isometric/orbit navigation, room click selection, searchable room list, roof visibility.
- Walk mode and a 0.1 m occupancy grid with 0.15 m walker margin; 33/34 zones have verified routes from lobby. One very small wudu zone is not traversable at modeled clearance.
- Built-in 77-second cinematic Blender video, including native player and video stream.
- PDF access to the 18-slide concept deck and 41-page render book.
- Shareable room deep links (`?room=Z08`) and video-tour label reset.
- Additional **CDN-free / WebGL-failure photographic fallback gallery**, backed by authentic Cycles renders for 34 rooms and the model-derived 16-stop script. It clearly labels static images as such.

## Live checks (Cloudflare Chromium)

1. Production homepage was updated through the connected Cloudflare Worker API (status 200).
2. Production URL `?room=Z08&scale=0.6` loaded the **real model**; loading overlay hidden; 34 room buttons present; Boardroom title correct; cinematic-film UI present; fallback not active.
3. Staging URL using the identical pinned source: GLB downloaded, room navigation worked; isometric overview screenshot inspected.
4. Guided tour: start showed `Stop 1 / 16`, Next showed `Stop 2 / 16`, Pause changed label to Resume (Chromium QA).
5. Staging MP4 stream returned HTTP **206 Partial Content**, `content-range: bytes 0-511/73813604`, MP4 signature `ftypisom`; native film modal opens and closes.
6. **Forced GLB download failure** in staging: the photographic fallback activated with all 34 rooms, including Boardroom as `?room=Z08`. Loading failure did not strand the client at an endless spinner.
7. Original source files were not rewritten.

## Limitations / open tasks

- Real-time WebGL lighting still differs from offline path-traced Blender Cycles; use the photoreal render stops and video to demonstrate the intended lighting and finishes.
- Independent Mac Chrome/Safari GPU testing has not yet been completed, although headless Chromium WebGL 2 passed.
- Full 2–3 minute extended cinematic tour is still being produced by Claude according to its latest handoff; only the completed 77-second client pitch MP4 is linked here.
- Several architectural measurements remain provisional and must be checked by site survey and engineers before construction.
- Video and GLB currently proxy from the public GitHub repository. For sustained high traffic, migrate large files to a dedicated object-storage/CDN asset host.

## Rollback

Previous Cloudflare Worker script saved at:
`GARMENT_OFFICE_WALKTHROUGH_FINAL/08_WORKER_READY_TOUR/rollback_worker_20261027.js`
on branch `chatgpt/stage2-integrated-client-tour`.

Worker `stage2-office-tour-preview` also retains the prior GPT layout. To roll back, deploy the saved previous script to `stage2-office-virtual-tour` through Cloudflare Workers API.

## Claude / GPT collaboration

Claude maintains Blender model, web GLB export, camera data and cinematic movies on `claude/web-tour-assets`. GPT maintains Cloudflare deployment and this integrated client presentation in a separate branch. Collaborate through GitHub issue #12; do not overwrite either agent's work.
