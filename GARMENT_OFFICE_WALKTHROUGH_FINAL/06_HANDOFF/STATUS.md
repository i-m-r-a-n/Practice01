# Status - 27 Oct 2026

(updated when each item is finished and checked)

## Done and checked
- Web GLB, metadata, walk map, 38-camera browser check - `07_WEB_TOUR_ASSETS/`, `05_PRODUCTION/camera_qc/`
- Real-WebGL check of the live GPT tour (commit 50923eb) - `05_PRODUCTION/live_site_qa/LIVE_SITE_QA.md`, posted on issue #12
- Offline 3D tour + Mac guide - `03_INTERACTIVE_3D/`: simplified interface (one bottom panel row, no overlapping panels, help card),
  layout test of 6 screens x 7 window sizes in `05_PRODUCTION/layout_test/`
- Worker-ready 2-file bundle (not deployed; load checked) - `08_WORKER_READY_TOUR/`
- Blender animation file + scripts, storyboard, benchmarks, encoding settings

## Videos
- `01_CLIENT_PITCH_VIDEO/Client_Pitch_Cinematic_Tour.mp4` - **done**: 77.0 s, 1920 x 1080, 24 fps, H.264 High, BT.709, 73.8 MB,
  12 path-traced camera moves + title / closing cards. QC (`05_PRODUCTION/video_qc/`): no decode errors, no black frames,
  only intended still frames (title and closing cards), faststart. Download from GitHub tested: identical file
  (SHA-256 b54b173ee41fe497a1a293d8cf61a33a75e36a84147702dbcaa66ac36488dad5).
- `02_FULL_FLOOR_TOUR/Complete_Ground_Floor_Tour.mp4` - **done**: 121.0 s (2:01), 1920 x 1080, 24 fps, H.264 High, BT.709,
  78.9 MB, 28 path-traced camera moves (lobby, reception, experience centre, boardroom, executive suite, MD office, HR,
  commercial, merchandising, CAD, fabric library, 3D lab, sample room, design corridor and studio, cafe, lounge, prayer room,
  final overview) + title / closing cards. The CRF 18 edit was 117.9 MB, over GitHub's 100 MB limit, so it was re-encoded
  once at CRF 20 (settings in `05_PRODUCTION/ENCODING_SETTINGS.md`). QC (`05_PRODUCTION/video_qc/`): no decode errors,
  no black frames, still only on the title and closing cards, faststart. SHA-256 bdd63a572d460f8c99012751e380feb3cfa38140b7646381f2ca71fc1a4ebc3a.
- Light copies for phones, e-mail and the website (1280 x 720, same QC): `01_CLIENT_PITCH_VIDEO/Client_Pitch_Cinematic_Tour_web720.mp4`
  (16.9 MB) and `02_FULL_FLOOR_TOUR/Complete_Ground_Floor_Tour_web720.mp4` (26.0 MB).
- Website video link: `https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/pitch.mp4` returns 404 since the
  Worker was re-pinned to f9048ef (the route is not in that release). The Worker is GPT's; the route fix is posted on issue #12.

## Not done / open
- Live website: unchanged by Claude (GPT owns the frontend and the Worker; integration via issue #12)
- Baked lighting for the real-time model (the Cycles renders remain the photoreal reference)
