# /realistic/ improvement sprint (Claude): checkpoint

Resume from this file if the session is interrupted. Newest state first.

## Where things are

- **Branch:** `claude/realistic-sprint-20261028` (worktree `/home/user/rs`).
  - Based on GPT's `chatgpt/realistic-sprint-20261028` @ `3ed3b41`, which carries GPT's QA notes and the direct-drag sign fix.
  - Nothing of GPT's was changed or removed.
- **Live release (interior phase), deployed and verified:**
  - **Source:** `d5939f9ef3928340908459efc440259df0d34b6d`.
  - **Worker:** `deploy/worker-realistic.js` from the commit after it; 7621 bytes, SHA-256 `f6e4730f…ffff922`, 41 / 41 worker tests pass.
  - **Status:** the owner deployed it on 29 Oct 2026. Verified at 16:29 UTC, details below under Live. Steps, guard and rollback: `deploy/DEPLOY_RECEPTION_20261029.md`.
  - **Contains:** the sprint release below, plus the interior phase (`qa/interior-20261029/`):
    - Reception, built at `0cda894`
    - Experience Centre, built at `de424c0`
    - MD Office, Boardroom, Merchandising and Design Studio, built at `8643898`
    - Design Studio second pass (fabric mood board, sample-review table), built at `3126dbf`
    - Merchandising second pass (fit toile and knitted body on the dress forms, approval board as pinned cloth), built at `92a5965`
    - Boardroom second pass (khadi desk pads), built at `d5939f9`
  - **Earlier interior workers:** never deployed; each was superseded by the next.
- **Prepared next release (buyer journey, not yet deployed):**
  - source `2a45193` (Entrance Lobby)
  - worker SHA-256 `fde89e17…94e7b4`
  - notes and evidence: `deploy/DEPLOY_RECEPTION_20261029.md` and `qa/journey-20261029/`
  - The next increments are CAD, Sample room, Lounge / Training and Experience Centre, in that order.
- **Sprint release (superseded, never deployed):** source `e98ecb5`, worker `6edce19`, `deploy/DEPLOY_SPRINT_20261029.md`.
- **Checks passed on the release build** (`r2/`, local Chromium, software WebGL):
  - `ui_check`: 34 / 34 at 1440, 390 and 360
  - `layout_probe`: all 16 widths OK
  - `smoke`: 22 / 22 at 1440 × 900 and 23 / 23 at 390 × 844, with no page errors, HTTP errors or failed requests
  - `capture_rooms`: 6 frames; identity props 8; screens 9
  - `capture_visitor`: 9 frames
  - `request_list`: all 19 requested files are in the source commit
  - public bytes of the changed dist files at the source commit match
  - live guard checked at 05:10 UTC: `/realistic/health` shows `bcb92b0`; `/` returns 200 with SHA-256 `ff75beb5…`
- **Live:**
  - `/realistic/` = source `d5939f9ef3928340908459efc440259df0d34b6d`, deployed by the owner on 29 Oct 2026.
    - The previous source was `bcb92b0` (Cloudflare version `bcfea6b5`).
    - The rollback is still the worker from `cdf0e3e`.
  - `/` = original tour, byte-identical, never touched.
  - **Verification at 16:29 UTC:**
    - `/realistic/health` shows `d5939f9…`.
    - `/`, `/health` and `/realistic/` return 200, and `/` keeps SHA-256 `ff75beb5…`.
    - `deploy/public-interior-20261029-verification.json`: 13 / 13 checks pass. The live files match the commit byte for byte, and the original tour is unchanged.
    - **Live browser check** (`qa/interior-20261029/live-d5939f9/`):
      - The live page was loaded in this container's Chromium (software WebGL); the container's NSS store trusts the proxy CA.
      - Interior layer: 19 items.
      - Six tour-stop frames: 5 are pixel-identical to the local build, and Design Studio differs in 95 px.
      - A walk at the Reception hangings works.
      - No page or console errors, HTTP errors or failed requests.
      - Not Safari or MacBook proof.
- **Deploying:** this session cannot deploy, because its Cloudflare account has no Workers. The owner's desktop session deploys by pasting the worker script in the Cloudflare dashboard. Steps, guard and rollback: `deploy/DEPLOY_SPRINT_20261029.md`.

## Cloudflare access for cloud sessions (set up 29 Oct 2026)

- **Token:** the owner created an API token, `claude-cloud-deploy-stage2`, for the account that owns `stage2-office-virtual-tour`.
  - Intended scope: Account → Workers Scripts → Edit, on that one account only.
  - It is stored in the cloud environment **Imran** as a Network secret: Bearer token for `api.cloudflare.com`, path `/client/v4/`.
  - The value is never written in the repo, the chat or any file.
- **New sessions only:** the proxy picks up the token in sessions started after that. In the session that set it up, `GET /client/v4/accounts/` still returned 0 accounts, because that session's earlier connector credential overrode any Authorization header.
- **Old connector:** the deprecated "Cloudflare Developer Platform" connector was disconnected. Do not reconnect it: its credential would override the token again.
- **First step in a new session (read only):**
  1. `GET /client/v4/accounts/` must list the account.
  2. `GET /client/v4/accounts/{id}/workers/scripts` must list `stage2-office-virtual-tour`.
- **Deploy from the session:**
  - **Script format:** `deploy/worker-realistic.js` is a service-worker script that uses `addEventListener('fetch')`.
  - **Before uploading:**
    - Read the current script's settings (compatibility date, flags, bindings) and keep them.
    - Keep a copy of the current live script as the rollback.
  - **Upload:** `PUT /client/v4/accounts/{id}/workers/scripts/stage2-office-virtual-tour` with multipart:
    - metadata `{"body_part": "script", ...current settings}`
    - the part `script` (`application/javascript`)
  - **Around the upload:**
    - Before: the same guard and `node deploy/test_worker.mjs` as the owner prompt.
    - After: `deploy/verify_release.py` and live browser frames.
    - If anything fails, roll back to the worker from `cdf0e3e`, or to the saved previous script.

## Local test harness

- **Serve:** `python3 viewer/serve_preview.py --port 8784` (same routing as the Worker).
- **Build:** copy `viewer/build.mjs` next to a node_modules that holds esbuild 0.24.0, then run `TOUR_SRC=<viewer dir> node build.mjs <viewer dir>/dist`.
  - A rebuild of GPT's 3ed3b41 source reproduced its committed dist byte-for-byte.
  - A rebuild of this release's source reproduces its dist too.
- **QA scripts** (this folder). They use LOCAL Chromium with software WebGL, so they are not live, Safari or MacBook proof.
  - `ui_check.py`: toolbar inside the viewport at 1440 / 390 / 360; no overlaps; People contrast ≥ 4.5; concept notice ≥ 11 px; drag direction; People on / off; Help. On phones it also checks that the room card uses ≤ 40% of the screen and that the folded note opens and folds.
  - `layout_probe.py`: the header at 16 widths, 320–1920 px.
  - `smoke.py`: welcome card, tour, the 6 rooms, photoreal still, walk (keys / touch pad), overview tools, errors and failed requests.
  - `capture_rooms.py`: frames from the reference cameras.
  - `capture_visitor.py`: visitor-eye frames at chosen floor spots, using the walk-QA hooks.
  - `request_list.py COMMIT`: every file the page requests exists in the release commit, using the Worker's path rules.
  - `abort_probe.py`: request timeline next to the bytes the page really receives (see the open items).
  - People contact numbers: `__viewer.api.peopleContacts(1)`.
- **Evidence:**
  - `baseline/`: live source plus GPT's drag fix.
  - `r1/`: R1 build.
  - `r2/`: the final release build.

## Done and verified locally

### R1: usability

- **People button.** Readable glass toggle with an on-state dot; contrast 6.14 (was 1.04).
- **Header ≤ 860 px.** Two-row grid: logos, Help and Full screen on the first row; Tour, the modes and People on the second. All controls are reachable and none overlap from 320 to 1920 px. Before, Help and Full screen were cut off at 390 and 360 px.
- **Footer notice.** "Concept proposal · … People shown are illustrative, not real staff", 12 px on desktop and 11 px on phones (was 10 px).
- **Direct drag.** GPT's sign fix is verified in a browser: dragging right or down moves the room with the pointer.
- **Phone room card.**
  - On phones the new concept note is folded to two lines, and a tap opens or folds it. The bottom spacing is a transparent border, so no part of a third line peeks out.
  - On touch devices the room hint says "tap Walk from here to move" instead of "W A S D or arrows".
  - The card uses 33.5% of a 390 × 844 screen and 40% of a 360 × 740 screen.

### R2: client identity in the tour

Everything is additive and self-made. Nothing stands on the floor, so walk paths are unchanged. Source: `props/identity-props.mjs`, wired in through `phase-dressing.js`.

- **Experience Centre counter:**
  - Water & Wellbeing refill point: a profile tap on a drip tray, clean tumblers, a tray for used glasses, and an "Our water" sign. Every result reads *Pending*; the deep tube well is marked *client-stated*.
  - Coconut-shell button story: shell → blanks → buttons on a garment panel. Its card says supplier data is pending.
  - Two sample cards whose fields read *pending*.
- **Reception:** a Jamdani-inspired textile panel above the sofa. The motifs are drawn square by square on the loom grid. It is described as a design reference, with the maker to be identified.
- **MD credenza:** development samples and a swatch study.
- **Boardroom:** two fabric review trays.
- **Screens:** generic placeholder content on the Merchandising, MD and Studio screens. They were blank faces before; no invented data is shown.
- **Room and tour cards:** a "Concept" note per room (`release-config.json` → `roomNotes`). The solar statement is client-stated; figures are promised only with real monitoring data.
- **Design Studio:** now opens, in the room list and on its tour stop, on its existing camera `CAM_14_Design_Studio_B`, which shows the desks, the screens and the colour wall. It used to open on `CAM_13_Design_Studio_A`, which shows the long table and the rail. The change is in `release-config.json` → `cameraOverrides`; deleting that entry restores `CAM_13`.

### R3: people

- **Measured** on the actual skinned vertices, for all 27 people:
  - Lowest point is 0.0107 m against a floor finish top of 0.0102 m, so shoes stand 0.5 mm above the floor. Nobody floats or sinks.
  - Seated people sit 0.2–3.4 cm above the documented seat tops.
  - No vertex is below the floor.
- **Contact shadows:** soft static shadows were added (42 in total), one under each person's feet, placed from the posed foot bones, and one under each seated person's chair. They toggle with People.

## Release steps

All six steps are done for H = `d5939f9`: the owner deployed it, and it was verified at 16:29 UTC. **Next action:**

- Continue the interior design on this branch.
- The Entrance Lobby (the first tour stop, outside the six rooms) is proposed next, only if the client asks for it.
- Each new release repeats steps 1–6.

1. Commit and push the source + dist. That gives source commit H.
2. Run `python3 qa/sprint-claude-20261028/request_list.py H` and `python3 deploy/build_worker.py H`.
3. `node deploy/test_worker.mjs` must pass.
4. Commit and push the worker.
5. The owner deploys `deploy/worker-realistic.js` from that commit, after checking that live `/realistic/health` still shows `bcb92b0…`.
6. Run `python3 deploy/verify_release.py Design_Studio H --report public-sprint-20261029-verification.json` and confirm `/` is unchanged.

**Rollback:** paste `deploy/worker-realistic.js` from commit `cdf0e3e`. That is the current live worker (source bcb92b0).

## Open items

- **Live browser QA.** It is now possible from this container: Chromium trusts the proxy CA through the NSS store, which was not the case earlier. It is still software WebGL.
- **Not tested:** Safari, a real MacBook GPU, live load time.
- **People detail.** People are low-detail game-style figures, an inherent asset limit. Seated gaps of up to 3.4 cm are not visible at tour distances.
- **ERR_ABORTED reports.** With the local Python preview server, Chromium sometimes reports `net::ERR_ABORTED` for a GLB request, for example `panjabi.glb`, `shirt.glb` or `model_web_baked.glb`.
  - `abort_probe.py` shows the page still receives every byte (status 200, bytes equal to the file size) and the model and all 27 people load.
  - So this is a reporting artefact of the local harness, not a load failure. Traces: `r2/abort-probe/`.
- **Phone room card size:** at 360 × 740 the card uses 40% of the screen height (296 px), against about 33% before the sprint. At 390 × 844 it uses 33.5%.
- **Visitor frames:** the `merch_typing` spot in `capture_visitor.py` is not on free floor, so the viewer refuses it. This is a capture-spot error, not a tour defect.
- **Next candidates:**
  - **Coconut-shell story placement.** Seen from the passage, a white vertical element in front of the counter hides part of the card. A quick GLB query near that spot found no model geometry, so it may be a runtime prop. Check what it is before moving anything.
  - A lighter carpet in Merchandising. Correction: an earlier note said the concept proposes this "at renewal", but no document in the repository says so. The interior phase (`qa/interior-20261029/`) now shows it as a design proposal.
  - More rooms, only after this release is live and verified.
