# Office realism sprint — 2026-10-28

## Result

Review and a bounded direct-drag fix are saved on `chatgpt/realistic-sprint-20261028`, starting exactly at `20a3de996191ee2ecbe57928780b49209a289832`. No deployment or rollback was performed. The existing six-room, 27-person live release remains the target previously verified by the owner. No new Accounts room was added.

The sprint began at 10:48 UTC (16:48 Asia/Dhaka), with a 60-minute stop target of 11:48 UTC (17:48 Asia/Dhaka). A Cloudflare read call remained in flight through the deadline; the root observed 12:09 UTC upon regaining the checkpoint. New feature work was stopped. Only build validation, evidence packaging, commit/push and reporting followed. This was not a completed deployment within 60 minutes.

## Environment and access

- Existing execution environment recovered; Python 3.12.14, Node v24.19.0 and Git 2.52.0 ran.
- Git fetched the requested branch and its exact commit. An isolated worktree preserves the previous interrupted checkout and its uncommitted MD edits.
- Cloudflare API GET succeeded and reported live `REALISTIC_COMMIT` `bcb92b00963fa51906676f8cca22da88f841dc64`. No API mutation was attempted; write/deploy access was not proven by a GET.
- The current Worker response was saved as `deploy/rollback-sprint-20261028.js`; its SHA256 is `9f486691580b101bdd04caa45ef7ecaf9ab62e14f81f5261fabd204098592969`. Do not assume a JSON response serialization or historical byte count equals raw script bytes.

## Changes and checks

- Only the two direct pointer-drag signs in `viewer/app.js` changed: positive yaw and pitch client deltas. Pointer-lock FPS look and keyboard behavior are unchanged.
- `drag-check.mjs` executes the actual extracted handlers: 15 checks pass, including pitch limits and unchanged keyboard source against the requested baseline.
- Existing `npm run check` passes; existing `node build.mjs` rebuilds the config into `viewer/dist/app.js`.
- `node deploy/test_worker.mjs`: 41 checks pass, including 28 unchanged original-route request cases.
- No changes under `GARMENT_OFFICE_FINAL_PRESENTATION/` or `GARMENT_OFFICE_WALKTHROUGH_FINAL/03_INTERACTIVE_3D/`. No Claude branch was pushed or changed.
- A post-build real-browser drag-feel test remains pending. The saved `verify_ui_drag.py` also asserts UI fixes that were not implemented and must not be represented as passing.

## Browser QA

Live Chromium failed before the application loaded with `net::ERR_CERT_AUTHORITY_INVALID`. A task-local Firefox profile with the configured CA trusted, without disabling certificate verification, failed to launch with sandbox/framebuffer errors. The exact failures are in `live/`. Live model-ready time and live six-camera screenshots are therefore unavailable.

The unchanged local baseline was captured in Chromium at 1440×900 and 390×844, using CAM_01, CAM_04, CAM_09, CAM_07, CAM_34 and CAM_13. Local model-ready times were 2.008 and 1.538 seconds. These are not Internet or MacBook performance measurements. 27 frozen people loaded. No console/page errors or HTTP400+ responses were reported in the two camera passes. Aborted requests are retained in the evidence and are not silently counted as successes.

All screenshots in `local-baseline/` are explicitly local baseline images, not deployed after-images. Reference camera API shots hide UI and letterbox portrait views; the separate interactive shots expose UI defects, and were captured near the end of the arrival flight. See `visual-review.md`, `capture.json`, `interactive-ui.json` and `screenshot-hashes.json`.

## Unresolved findings

1. People button has unreadable light-on-light contrast.
2. 390px toolbar clips Help/fullscreen controls.
3. Merchandising monitor faces appear blank.
4. Studio camera foreground dominates, leaving workers distant.
5. Figures remain visibly low-detail; contact shadows and task gestures are weak.
6. No obvious gross body/furniture penetration was seen in the six frames, but exact contact geometry was not revalidated. Inherited MD phone/hand contact needs renewed measurement; previous interrupted diagnostics must not be promoted to a current acceptance.
7. Native MacBook performance, Safari, post-fix browser feel, live screenshots and live load timing remain untested.

Accounts preflight identified possible existing task/meeting chairs and a hazard: enabling Z06 would activate obsolete props `PROP_0132`–`PROP_0184`. No Z06 assets, manifests, furniture, config or people were changed. Continue with the two UI defects and live-browser access before adding this room.

## Publication status

No deploy, no rollback, no claim that this sprint is live. `verify_release.py` was not run for a new release because none was published. Existing `/` was not redeployed; its immutable-source hash expectations remain unchanged in the verifier. A future deploy must repeat the owner's live-source guard, build/test gate and public byte verification, and roll back on failure.
