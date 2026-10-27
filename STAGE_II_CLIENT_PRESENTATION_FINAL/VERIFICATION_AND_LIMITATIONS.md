# Verification and limitations (27 Oct 2026, 15:20 Dhaka)

## Verified
| Item | How it was checked | Result |
|---|---|---|
| Approved design files | SHA-256 of `Final_Office_Interior.blend` / `.glb`; `git diff` of `GARMENT_OFFICE_FINAL_PRESENTATION/` against the approved branch | unchanged (fa3ed3d5... / 3b883c00..., 0 changed lines) |
| Cinematic video | ffprobe + full decode + black / freeze scan + contact sheet; GitHub download compared by SHA-256 | 77.0 s, 1920x1080, 24 fps, H.264 High, BT.709, no errors, no black frames, still only on title / closing cards |
| Full floor tour video | same checks | 2:01 (121.0 s), 1920x1080, 24 fps, H.264 High, 78.9 MB, 28 camera moves, no errors / black frames; re-encoded once at CRF 20 (the CRF 18 edit was over GitHub's 100 MB limit) |
| Pitch PDF / PPTX / render book | `pdfinfo`, PPTX archive test and slide count | 18 pages / 18 slides (archive intact) / 41 pages |
| 3D tour, Mac package, **Firefox 159** (the presentation browser), opened from `file://` | automated browser run: load, help card, boardroom flight to its render camera, photoreal still, guided-tour stop, walk | 0 errors; ambient occlusion and baked light active (`GARMENT_OFFICE_WALKTHROUGH_FINAL/05_PRODUCTION/firefox_check/`) |
| 3D tour layout at Mac window sizes (7 sizes x 6 screens) | automated overlap / overflow check + screenshots | 42 / 42 pass (`05_PRODUCTION/layout_test/`) |
| 3D tour functions (Chromium) | 25-check functional test: rooms, render camera, look around, photoreal, ceilings, walk + collision, 16-stop tour, pause / resume / next / back / end, search, window size | see `05_PRODUCTION/viewer_test_v3/viewer_test.json` (earlier run 23 / 25: the 2 misses were software-GPU timing; the test now waits on state) |
| Six key rooms: Cycles vs live vs improved 3D | same cameras, side by side + colour metric | improved closer to the render in 4 of 6 rooms (`GARMENT_OFFICE_REALISM_UPGRADE/03_VISUAL_COMPARISON/`) |
| Downloads | each link in `README.md` fetched from GitHub | HTTP 200, sizes equal to the repository files |

## Not verified / limitations (stated, not hidden)
- **Live website** (GPT's Cloudflare deployment, frontend `6a65b7d`): at 15:16 Dhaka the room views were broken (walls offset,
  Reception shows a single wall). Cause found and fix sent to GPT on issue #12. Use the offline Mac package for the meeting.
- macOS, Safari and the actual presentation Mac were not available for testing; all browser tests ran on a software GPU in
  a cloud machine (they prove behaviour and layout, not the frame rate).
- Real-time 3D is not identical to the Cycles renders: no glossy reflections, glass reflects a generic environment,
  furniture is not baked (ambient occlusion adds contact shadows on still views), reception and MD office read brighter than
  their renders. The Cycles renders and the videos are the photoreal reference.
- Design status: concept proposal. Dimensions are site-estimated (see
  `GARMENT_OFFICE_FINAL_PRESENTATION/04_DOCUMENTATION/dimensional_assumptions.md`); structural, MEP, fire and authority approvals
  are not done. Furniture and products shown are generic, not specific brands or collections.
- Phone / tablet layout was not part of the final checks (the presentation is on a Mac).

## Approvals still needed
Client approval of concept and layout; site survey of dimensions; structural engineer (new partitions, ceilings, loads);
MEP / fire design and authority approvals; final material and furniture selection and costing.
