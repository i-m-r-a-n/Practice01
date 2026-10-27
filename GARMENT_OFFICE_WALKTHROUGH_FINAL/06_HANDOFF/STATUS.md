# Status - 27 Oct 2026

(work in progress - this file is updated when each video is finished and checked)

## Done and checked
- Web GLB, metadata, walk map, 38-camera browser check - `07_WEB_TOUR_ASSETS/`, `05_PRODUCTION/camera_qc/`
- Real-WebGL check of the live GPT tour (commit 50923eb) - `05_PRODUCTION/live_site_qa/LIVE_SITE_QA.md`, posted on issue #12
- Offline 3D tour + Mac guide - `03_INTERACTIVE_3D/` (load + first steps checked; full 20-check browser test pending)
- Worker-ready 2-file bundle (not deployed; load checked) - `08_WORKER_READY_TOUR/`
- Blender animation file + scripts, storyboard, benchmarks, encoding settings

## Videos
- `01_CLIENT_PITCH_VIDEO/Client_Pitch_Cinematic_Tour.mp4` - **done**: 77.0 s, 1920 x 1080, 24 fps, H.264 High, BT.709, 73.8 MB,
  12 path-traced camera moves + title / closing cards. QC (`05_PRODUCTION/video_qc/`): no decode errors, no black frames,
  only intended still frames (title and closing cards), faststart. Download from GitHub tested: identical file
  (SHA-256 b54b173ee41fe497a1a293d8cf61a33a75e36a84147702dbcaa66ac36488dad5).
- `Complete_Ground_Floor_Tour.mp4`: the 16 additional shots are rendering (pitch shots reused). Not yet available.

## Not done / open
- Live website: unchanged by Claude (GPT owns the frontend and the Worker; integration via issue #12)
- Baked lighting for the real-time model (the Cycles renders remain the photoreal reference)
