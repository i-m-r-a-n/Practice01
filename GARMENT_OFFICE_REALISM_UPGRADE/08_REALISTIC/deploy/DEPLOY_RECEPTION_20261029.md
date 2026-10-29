# Deploying the interior releases (prepared by Claude)

**Live since 29 Oct 2026:** `d5939f9` (the release below), deployed by the owner.
- **Verified at 16:29 UTC:**
  - health source `d5939f9…`
  - `/` unchanged (`ff75beb5…`)
  - `public-interior-20261029-verification.json` 13 / 13
  - live browser frames in `qa/interior-20261029/live-d5939f9/`
- **Rollback:** worker from `cdf0e3e`.

## Prepared, not yet deployed: Entrance Lobby + CAD room (buyer-journey increments 1–2)

`worker-realistic.js` is built for source commit `72571634cb78949d81b2bd80b08d4dd4670a0f51`.

- Size and SHA-256: 7621 bytes, `b17e9b466901fd655b7a495cd83f464c21537b53a8ebafb484c2e2cc92bf6491`.
- **Affected rooms:**
  - Entrance Lobby (Z01, CAM_03): as in the section below
  - CAD / Technical Design (Z14, CAM_15): screens, pinboard and layout table follow one illustrative development exercise
- **Guard, original-route hashes and rollback:** as in the section below. Expected live source: `d5939f9…`. Rollback first to worker `01fac69`.
- **Checks:**
  - `node test_worker.mjs` passes 41 checks
  - all 22 requested files are in the commit
  - the changed dist files match on raw.githubusercontent.com
- **Evidence:** `qa/journey-20261029/cad/` and `lobby/`.

## Superseded before deployment: Entrance Lobby (buyer-journey increment 1)

`worker-realistic.js` is built for source commit `2a451939f48253cdfbb9a85c48f6ec16306389e1`.

- Size and SHA-256: 7621 bytes, `fde89e17b2234e00689ea66480740db07b3e1d133f6b5aca51460ff7be94e7b4`.
- **Affected room:** Entrance Lobby (Z01, CAM_03).
  - warm light on the oak brand wall
  - warmer desk walnut and door oak
  - one woven hanging between the windows W11 and W12
  - Everything else is as in `d5939f9`.
- **Guard:** live `/realistic/health` must show `d5939f9ef3928340908459efc440259df0d34b6d`. The original routes must keep these SHA-256 values (from `verify_release.py`):
  - `/` → `ff75beb5…2675`
  - `/app.js` → `c6af8144…9bc4`
  - `/health` → `5118ed49…378b`
- **Checks:**
  - `node test_worker.mjs` passes 41 checks
  - all 22 requested files are in the commit
  - the changed dist files match on raw.githubusercontent.com
- **Rollback:** the current verified worker from commit `01fac69` (7621 bytes, SHA-256 `f6e4730f…ffff922`). The older fallback is `cdf0e3e` (SHA-256 `cb62a45f…a623`).
- **Evidence:** `qa/journey-20261029/lobby/`.

## Live: Merchandising and Boardroom second passes

`worker-realistic.js` is built for source commit `d5939f9ef3928340908459efc440259df0d34b6d`.

- Size and SHA-256: 7621 bytes, `f6e4730fea0a23ec9d65e57a9c65add85f1b01decbcfec1afe4f556e8ffff922`.
- It contains everything below, plus:
  - **Merchandising:**
    - a calico fit toile and a knitted body sample on the two dress forms
    - the approval board shown as pinned cloth
  - **Boardroom:** khadi desk pads with a kantha-stitched edge at the eight places
- Verify: `/realistic/health` shows `d5939f9ef3928340908459efc440259df0d34b6d`.
- Checks:
  - `node test_worker.mjs` passes 41 checks
  - the changed dist files at that commit match on raw.githubusercontent.com
  - `request-list.json`: all 22 requested files are in the commit
  - Reception, Experience Centre and MD Office frames are unchanged by these passes
- Evidence: `qa/interior-20261029/merchandising-2/` and `boardroom-2/`.

## Design Studio second pass (superseded by the one above)

`worker-realistic.js` was built for source commit `3126dbf2b3a0d5a8fd2d4d2c042024fe8c487b5a`.

- Size and SHA-256: 7621 bytes, `356d21dc1ab3004cf4fdec5147c3ea7e7bf75738b38556d70a10701e2b1af316`.
- It contains everything below, plus, in the Design Studio:
  - **Mood board as pinned cloth:** same swatch layout and colours as the model, lit by its five existing track spots
  - **Sample-review set on the presentation table:** knit sample, pattern pieces, swatch cards, tape, sketchbook, coconut-shell buttons
- Verify: `/realistic/health` shows `3126dbf2b3a0d5a8fd2d4d2c042024fe8c487b5a`.
- Checks:
  - `node test_worker.mjs` passes 41 checks
  - the changed dist files at that commit match on raw.githubusercontent.com
  - `request-list.json`: all 22 requested files are in the commit
- Evidence: `qa/interior-20261029/design-studio-2/`.

## All six rooms (superseded by the one above)

`worker-realistic.js` was built for source commit `86438989226bcdce59b22e8fadae7a2e822eb974`.

- Size and SHA-256: 7621 bytes, `340d786533628963604a9eb27b2dc79190a757a5f8d0bfc7f2504d4c988f3010`.
- It contains the Reception and Experience Centre releases below, plus:
  - **MD Office:** kantha-inspired panel with a picture light, the lounge rug as an indigo kantha weave (same footprint), stitched cushions
  - **Boardroom:** indigo kantha-inspired panel beside door D20 with a picture light, soft table light
  - **Merchandising:** knit structure on samples and swatches; a lighter carpet shown as a design proposal (not an approved finish)
  - **Design Studio:** the existing east windows W08–W10 read as overcast daylight instead of black glass
- Verify: `/realistic/health` shows `86438989226bcdce59b22e8fadae7a2e822eb974`.
- Checks:
  - `node test_worker.mjs` passes 41 checks
  - the changed dist files at that commit match on raw.githubusercontent.com
  - `request-list.json`: all 22 requested files are in the commit
- Evidence: `qa/interior-20261029/four-rooms/` and the four room folders beside it.

## Reception + Experience Centre (superseded by the one above)

`worker-realistic.js` was built for source commit `de424c0e5161dcc98cbff569cba670bf1c4f677e`.

- Size and SHA-256: 7621 bytes, `bbe5425b372e0152b2c7afee27ec795bdd95fd276c7a83accd732c3b214da862`.
- It adds the Experience Centre redesign:
  - knitwear on the forms
  - handloom fins
  - the materials library on the material table
  - green handloom bay panels
  - gallery light pools
- Verify: `/realistic/health` shows `de424c0e5161dcc98cbff569cba670bf1c4f677e`.
- Checks: `node test_worker.mjs` passes 41 checks, and the changed dist files at that commit match on raw.githubusercontent.com.
- Evidence: `qa/interior-20261029/experience/`.

## Reception release (superseded by the one above)

`worker-realistic.js` in this folder is built for source commit `0cda894f3e4b11edc64f9dc97f481b8e5986f003` (branch `claude/realistic-sprint-20261028`).

- Size and SHA-256: 7621 bytes, `b17b263b8a9d28e2e928e88e03dcf3bcbb691e89a4de0cc492529d51be7db5ab`.
- Its only difference from the live worker is the `REALISTIC_COMMIT` line.
- It includes everything in `DEPLOY_SPRINT_20261029.md` (usability fixes, identity props, people contact shadows) plus the Reception redesign.

## Reception redesign

Design references only: makers and fibres are to be identified and credited.

- **South wall bay:** five "warp and weft" handloom hangings on an oak rail over natural jute grasscloth, with a slim wall-washer and its warm wash.
- **Rug:** the approved rug keeps its footprint and its baked Cycles light. It is redesigned as jute with an indigo border, kantha running stitch and a lotus centre.
- **Soft furnishings:** kantha cushions on the sofa corners and lounge chairs, and an indigo kantha throw over the sofa arm.
- **Lighting:**
  - brass picture light over the Jamdani-inspired panel
  - warm scallops of the four existing track spots on the fluted oak wall
- **Visitor ledge:** fabric rolls and a bowl of coconut-shell buttons.
- **Floor:** the shared terrazzo floor (lobby, reception, experience centre, corridors) takes the approved CC0 Terrazzo019M 2K albedo with 0.8 m joints. The baked light is unchanged.

## Checks (local Chromium, software WebGL; not live, Safari or MacBook proof)

- `node test_worker.mjs`: 41 checks pass. The 28 original-tour requests are byte-identical.
- `qa/interior-20261029/reception/`:
  - `room-check.json`: CAM_01 and CAM_02 frames, and a walk to the new wall that stops 0.15 m short of it. No page errors, HTTP errors or failed requests.
  - visitor frames of the lounge
  - `request-list.json`: all 22 requested files are in the source commit, including the terrazzo KTX2.

## Deploy, verify, rollback

1. **Guard.** Live `/realistic/health` must show `bcb92b00963fa51906676f8cca22da88f841dc64`, or one of this branch's release commits (`e98ecb5…`, `0cda894…`, `de424c0…`, `8643898…`, `3126dbf…`) if an earlier release went live first.
2. **Deploy.** Upload the latest `worker-realistic.js` unchanged as the `stage2-office-virtual-tour` script.
3. **Verify:**
   - `/realistic/health` shows the source commit named in "Latest" above
   - `/`, `/health` and `/realistic/` return 200
   - `/` is byte-identical (SHA-256 `ff75beb5…`)

**Rollback:** `worker-realistic.js` from commit `cdf0e3e` (source `bcb92b0`).
