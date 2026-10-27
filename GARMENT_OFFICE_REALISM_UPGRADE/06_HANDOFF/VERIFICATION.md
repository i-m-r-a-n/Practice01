# Verification (27 Oct 2026)

All browser tests run in this cloud machine on a software GPU (Chromium + SwiftShader, Firefox 159 + Mesa llvmpipe in a
virtual display). They prove behaviour and layout, not the frame rate of a real Mac. No macOS / Safari test was possible here.

| Check | Result | Evidence |
|---|---|---|
| Approved project unchanged | 0 changed lines in `GARMENT_OFFICE_FINAL_PRESENTATION/` against `claude/magical-hopper-74q4xq`; `.blend` fa3ed3d5..., `.glb` 3b883c00... | `git diff` |
| Improved model loads in the viewer | yes, after the fix of the `lifted` load error (the `a50c6db` bundle stopped on load with this model) | `firefox_check/*_firefox_check.json` |
| Firefox 159 (presentation browser), Mac offline file from `file://` | model + baked light + ambient occlusion, help card, boardroom flight to `CAM_09_Boardroom_A`, photoreal still from `renders/`, tour stop 3 in one card, walk 2.2 m; **0 errors** | `GARMENT_OFFICE_WALKTHROUGH_FINAL/05_PRODUCTION/firefox_check/` |
| Firefox 159, website build (served like the Worker) | same steps, 0 errors | same folder |
| Layout at Mac sizes (2000x1093, 1920x1080, 1728x1117, 1512x982, 1470x956, 1440x900, 1280x800) x 6 screens (help, overview, room, tour + still, tour 3D, walk) | **42 / 42**: no overlapping panels, nothing outside the window, no sideways scroll; 0 console errors | `.../05_PRODUCTION/layout_test/` |
| Full functional test (Chromium, 1280x720): 25 checks incl. room camera, look around, photoreal, ceilings, walk + collision, tour pause / next / back while paused / end / Play again, search | **25 / 25, 0 errors** on the final build | `.../05_PRODUCTION/viewer_test_v3/` |
| Ambient occlusion A/B | contact shadows visible, no glass artefacts | `../03_VISUAL_COMPARISON/ambient_occlusion/` |
| Six-room comparison Cycles / live / improved | improved closer to the render in 4 of 6 rooms, about the same in 1, further in 1 (reception brighter) | `../03_VISUAL_COMPARISON/` |
| Videos | QC: no decode errors, no black frames, still only on title / closing cards, faststart; GitHub downloads byte-identical (SHA-256) | `.../05_PRODUCTION/video_qc/`, `../../GARMENT_OFFICE_WALKTHROUGH_FINAL/06_HANDOFF/STATUS.md` |
| Mac ZIP on GitHub | downloaded, SHA-256 identical, unzips to the HTML + README + 38 renders | this file's commit |

Open items (not done or not verifiable here): Safari and macOS itself; frame rate on the client's Mac; the live website
(frontend `6a65b7d`, assets `ddf99ee`, checked 09:16 UTC) shows offset walls in room views because its light-floor loop writes
into the interleaved position / normal data (evidence `GARMENT_OFFICE_WALKTHROUGH_FINAL/05_PRODUCTION/live_site_qa/run_6a65b7d/`,
fix on issue #12; the Worker is GPT's, nothing was changed on it from here); `/pitch.mp4` and `/tour.mp4` return 404 on the live
site until the video routes are added (see `README.md`).
