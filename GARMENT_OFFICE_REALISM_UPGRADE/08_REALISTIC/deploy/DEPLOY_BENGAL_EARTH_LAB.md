# Deploying the Bengal Earth Lab proposal route (prepared by Claude, 30 Oct 2026; updated after the owner chose option C)

## Update 6: update 5 plus the 3D model view of every AI image (1 Nov 2026, prepared, not deployed yet)

This has everything in update 5, and adds one thing. At every stop or room with an AI concept image, the button "3D model view" swaps in a render of the same camera in the 3D model, labelled as a render. "AI concept image" swaps back. There are 12 such renders, in `concept-images/model/`.

If update 5 is not live yet, deploy this one instead. If update 5 is live, this is the next step.

- **Source commit:** `f4346cc98f1d040e83e975b15eb41a4c659b5fd0`
- **Worker file:** `deploy/worker-bengal-earth-lab.js`, 10,742 bytes, SHA-256 `bba1bcc42433bede7904a0b31d0534a683269aecd2c7c475e944a149d4c56d49`. It differs from update 5's file only in the source commit.
- **Checks:**
  - `test_worker_bel.mjs`: 64 checks, against the live `d11321e` and against update 5's Worker. `test_worker.mjs`: 41 checks.
  - Browser checks on desktop and phone, in `qa/bel-20261030/after-1101-*/`:
    - `stills`: the 3D model view switch at stop 2; 38 of 38 images load.
    - `gallery`, `landscape`, `arrows` and `tour-play` (23 stops) pass.
    - `phone-walk`: the phone run passes. The desktop run is being repeated, because the local preview server restarted during it.
  - All 72 requested files exist at `f4346cc` (`after-1101-requests/`).
  - `index.html`, `app.js`, `release-config.json` and three of the images match raw.githubusercontent.com.

## Update 5: walking with a phone, an image at every stop, the new address (31 Oct 2026; prepared, not deployed yet; update 6 includes it)

Deploy request 5 is on [issue 12](https://github.com/i-m-r-a-n/Practice01/issues/12#issuecomment-6550846984), posted 31 Oct at about 23:58 UTC. It replaces requests 3 and 4.

This replaces updates 3 and 4. Like them, it serves the route at `/stage2-concept/` and redirects the old `/bengal-earth-lab/` there, and it shows the walk arrows on every device. It adds the owner's request of 31 Oct: "make it as beautiful as these images, and make it possible to walk the factory with a phone".

- **Walking with a phone:**
  - slide a finger between the arrows to change direction;
  - tap the floor to walk there;
  - "Look by moving the phone";
  - a help card the first time, and a compact room card;
  - a one-line footer while walking;
  - a phone held sideways gets a one-row header and the arrows under the right thumb.
- **Images at the stops:**
  - An image at every one of the 23 stops: 9 of the owner's AI concept images, 14 Cycles renders of the 3D, and 3 rooms. Each image carries the label of its kind.
  - "Images" shows them all in one grid. `?images=1` opens the grid and `?walk=1` starts walking.
- **Colour:** a slightly warmer grade.

All of it is behind route-config flags that only `bel-config.json` sets, so `/realistic/` and `/` do not change.

- **Source commit:** `3d0e7796dfdf440a2d1e9ccaa25bb710725197b5`
- **Worker file:** `deploy/worker-bengal-earth-lab.js`, 10,742 bytes, SHA-256 `2bbb532500a5d065bab39f6cd50476159f1fb991f3143c264385384324860062`. It differs from update 4's file only in the source commit.
- **Built with:** `python3 build_worker.py d5939f9ef3928340908459efc440259df0d34b6d --bel 3d0e7796dfdf440a2d1e9ccaa25bb710725197b5 --out worker-bengal-earth-lab.js`
- **Checks:**
  - `test_worker_bel.mjs`: 64 checks against the live Worker `d11321e`. They include the redirects, two near-miss prefixes and two stop images. `test_worker.mjs`: 41 checks.
  - Browser checks in local Chromium (software WebGL), on desktop and phone, all passed, in `qa/bel-20261030/after-1031c-*/`:
    - `landscape`: 844 × 390 and 667 × 375;
    - `phone-walk`;
    - `stills`: all 26 images load;
    - `arrows`;
    - `gallery`: 23 cards, the tap to stop 5, `?images=1`;
    - `tour-play`: 23 stops, no page or HTTP errors.
  - All 60 files the page requests exist at `3d0e779` (`after-1031c-requests/`). They include the 26 stop images and their 26 thumbnails.
  - `index.html`, `app.js`, `release-config.json` and three images match raw.githubusercontent.com at `3d0e779` byte for byte.
- **Guard before upload:**
  - `/bengal-earth-lab/health` shows `e198902…`.
  - `/realistic/health` shows `d5939f9…`.
  - `/`, `/app.js` and `/health` keep their hashes.
  - The live script is `d11321e` (`3bb5da83…1d03`).
- **Verify after upload:**
  - `/stage2-concept/health` shows `3d0e779…` with route `/stage2-concept`.
  - `/stage2-concept/concept-images/render_CAM_ISO_SE.jpg` answers 200 as `image/jpeg`.
  - `/bengal-earth-lab/` answers 307 to `/stage2-concept/`.
  - The other routes are unchanged.
- **Rollback:**
  1. Re-upload `d11321e` (`3bb5da83…1d03`).
  2. If that fails, re-upload `35a11c7` (`3424e88b…abd3`).

## Update 4: the new address and the on-screen walk arrows (31 Oct 2026; replaced by update 5 before it was deployed)

This replaces update 3. It has the same new address `/stage2-concept/`, with the old address redirecting there. The page also gets the owner's on-screen walk arrows: the ▲ ◀ ▼ ▶ pad, until now shown only on touch screens while walking, now shows on every device while walking and in a room view at eye level. Pressing an arrow in a room view walks on from there, like W A S D. The route config flag `walkArrows` turns this on; `/realistic/` does not set it.

- **Source commit:** `1d0f4121d689a4f635345fb4dd6ac29edda947ee`
- **Worker file:** `deploy/worker-bengal-earth-lab.js`, 10,742 bytes, SHA-256 `56d4a7494b51560f661e765adc391a43f39c4f38001b644d694b43392276930c`
- **Built with:** `python3 build_worker.py d5939f9ef3928340908459efc440259df0d34b6d --bel 1d0f4121d689a4f635345fb4dd6ac29edda947ee --out worker-bengal-earth-lab.js`
- **Checks:**
  - `test_worker_bel.mjs`: 62 checks against the live Worker `d11321e`. They include the redirects from the old address and two near-miss prefixes.
  - `test_worker.mjs`: 41 checks.
  - `bel_arrows_check.py`, on desktop and phone (`qa/bel-20261030/after-arrows/`):
    - the arrows are hidden in the overview and the tour;
    - they show and work while walking and in a room view;
    - there are no page errors.
  - The 23-stop tour plays (`after-tour-play-arrows/`).
  - All 8 requested files exist at `1d0f412`.
  - `index.html`, `app.js` and `release-config.json` match raw.githubusercontent.com byte for byte.
- **Guard before upload:**
  - `/bengal-earth-lab/health` shows `e198902…`.
  - `/realistic/health` shows `d5939f9…`.
  - `/`, `/app.js` and `/health` keep their hashes.
  - The live script is `d11321e` (`3bb5da83…1d03`).
- **Verify after upload:**
  - `/stage2-concept/health` shows `1d0f412…` with route `/stage2-concept`.
  - `/bengal-earth-lab/` answers 307 to `/stage2-concept/`.
  - The other routes are unchanged.
  - In walk mode, the arrows show on a computer.
- **Rollback:**
  1. Re-upload `d11321e` (`3bb5da83…1d03`).
  2. If that fails, re-upload `35a11c7` (`3424e88b…abd3`).

## Update 3: the new address /stage2-concept/ (31 Oct 2026; replaced by update 4 before it was deployed)

The owner asked for the old name to go from the address too. The proposal is now served at `/stage2-concept/`.

The earlier address keeps working: `/bengal-earth-lab/` and everything under it redirects (307) to the same path under `/stage2-concept/`, so links already shared still open. The page itself is unchanged (source `e198902`). Only the Worker changed.

- **Worker file:** `deploy/worker-bengal-earth-lab.js`, 10,742 bytes, SHA-256 `3ead6824f99aba567eceb14e06c4bcede3eeba8c22493b129f39fea3f4edc7b9`.
- **Built with:** `python3 build_worker.py d5939f9ef3928340908459efc440259df0d34b6d --bel e198902122e565878697d7606d9b4ce2b98b32b7 --out worker-bengal-earth-lab.js`
- **Checks:**
  - `test_worker_bel.mjs`: 62 checks pass. They include the 5 redirects from the old address, the health route at the new address, and two near-miss prefixes (`/stage2-concepts`, `/bengal-earth-labs`) that still go to the original tour unchanged.
  - `test_worker.mjs`: 41 checks pass.
  - The 23-stop tour plays at `/stage2-concept/` locally (`qa/bel-20261030/after-tour-play-path/`).
  - All 8 requested files at the new address exist at `e198902` (`request-list.json`).
- **Guard before upload:**
  - `/bengal-earth-lab/health` shows `e198902…`.
  - `/realistic/health` shows `d5939f9…`.
  - `/`, `/app.js` and `/health` keep `ff75beb5…2675`, `c6af8144…9bc4` and `5118ed49…378b`.
- **Verify after upload:**
  - `/stage2-concept/health` shows `e198902…` with route `/stage2-concept`.
  - `/bengal-earth-lab/` answers 307 to `/stage2-concept/`.
  - The other routes are unchanged.
- **Rollback:**
  1. Re-upload the live Worker from `d11321e` (`3bb5da83…1d03`).
  2. If that fails, re-upload `35a11c7` (`3424e88b…abd3`).

## Update 2: STAGE II · Zara Fashion branding (live since 30 Oct 2026, 17:52 UTC; Cloudflare version `8bef92a5-5acf-42a9-8d82-2a1efcef6b71`; see `LIVE_DEPLOY_2026-10-30.md`)

The owner asked for STAGE II / Zara Fashion branding instead of "Bengal Earth Lab". Only the page labels changed:
- page title: "STAGE II · Zara Fashion - ground floor concept"
- eyebrow: "STAGE II · Zara Fashion"
- headline: "The ground floor, reimagined · concept proposal"
- welcome title: "Explore the ground floor proposal"
- stop 1: "The whole floor"

No 3D item changed, and the URL path stays `/bengal-earth-lab/`.

- **Source commit:** `e198902122e565878697d7606d9b4ce2b98b32b7`
- **Worker file:** `deploy/worker-bengal-earth-lab.js`, 10,363 bytes, SHA-256 `3bb5da83bfe2de517fdc3d7213f646c3298ab943e60e7dc4c9743797f5e61d03`. It differs from the live Worker (`35a11c7`, `3424e88b…abd3`) only in the source commit it names.
- **Built with:** `python3 build_worker.py d5939f9ef3928340908459efc440259df0d34b6d --bel e198902122e565878697d7606d9b4ce2b98b32b7 --out worker-bengal-earth-lab.js`
- **Checks:**
  - `test_worker_bel.mjs`: 54 checks pass.
  - `test_worker.mjs`: 41 checks pass.
  - The 23-stop tour plays locally with no errors (`qa/bel-20261030/after-tour-play-brand/`).
  - All 8 requested files exist at `e198902`.
  - `index.html`, `app.js` and `release-config.json` match raw.githubusercontent.com byte for byte.
- **Guard before upload:**
  - `/bengal-earth-lab/health` shows `109aec2…`.
  - `/realistic/health` shows `d5939f9…`.
  - `/`, `/app.js` and `/health` keep `ff75beb5…2675`, `c6af8144…9bc4` and `5118ed49…378b`.
- **Verify after upload:**
  - `/bengal-earth-lab/health` shows `e198902…`.
  - The other routes are unchanged.
  - The page header reads "STAGE II · Zara Fashion".
- **Rollback:**
  1. Re-upload the live Worker from `35a11c7` (`3424e88b…abd3`).
  2. If that fails, re-upload `01fac69` (`f6e4730f…f922`).

## Update 1: the proposal route (live)

**Status: live since 30 Oct 2026, 09:15 UTC.** ChatGPT deployed it (Cloudflare version `d9f95025-89f6-4e7a-9ae5-071dba5f082a`), and Claude checked it independently. The record is `LIVE_DEPLOY_2026-10-30.md`.

The owner authorised the deploy on 30 Oct 2026 ("C, deploy, if u cant tell chatgpt to deploy"). Claude's Cloudflare token can see the account but has no Workers permission: the script list is empty, and the script's settings return "No access to the specified resource". So the upload was handed to ChatGPT.

## What it adds

- `/bengal-earth-lab/`: the concept proposal, with its own page, bundle and config. Source commit `109aec2942fed6389b01c7b8e8bee0dac724784b`. It contains increment 6 (the approved knitwear dressing restored, the fabric stories, natural indigo, the jhut river, the tea stall, the living wall, the craft pieces) and the option C labels: the pilot comes first, and the option A rooms are shown as a possible later phase. The 23-stop tour is included. Evidence is in `qa/bel-20261030/`.
- `/` stays byte-identical to the preserved production Worker.
- `/realistic/` stays identical to the live Worker. Its source is still `d5939f9ef3928340908459efc440259df0d34b6d`.

## Worker

- **File:** `deploy/worker-bengal-earth-lab.js`, 10,363 bytes, SHA-256 `3424e88b85e1f551d5e558d32510734eb1da864395148543bb4e3035a7e4abd3`
- **Built with:** `python3 build_worker.py d5939f9ef3928340908459efc440259df0d34b6d --bel 109aec2942fed6389b01c7b8e8bee0dac724784b --out worker-bengal-earth-lab.js`
- **Previous builds**, never deployed and replaced by this file: increment 1 (source `60351b0`, SHA-256 `889d0b4f…a2a9`), increment 2 (source `539fc24`, SHA-256 `1a7451d9…eb83`), increment 3 (source `1a838d8`, SHA-256 `dad7a01c…a8bc`), increment 4 (source `1592542`, SHA-256 `e46c06dc…fb4a`), increment 5 (source `1f64305`, SHA-256 `bd8d3504…edfc6`), increment 5 with the presenter polish (source `a83153c`, SHA-256 `0b4c2859…7e7e`), and increment 6b (source `0b239f6`, SHA-256 `19824644…3916`).
- **The builder:** without `--bel`, the modified builder still reproduces the live Worker byte for byte (SHA-256 `f6e4730f…f922`, the file at `01fac69`).

## Checks passed (30 Oct 2026, at `109aec2`)

- `node test_worker_bel.mjs <live worker> worker-bengal-earth-lab.js`: 54 checks.
  - The 28 original-tour requests are byte-identical to the preserved production Worker.
  - 14 `/realistic/` requests (redirect, health, page, bundle, model, renders, Range, POST, path traversal) match the live `/realistic/` Worker. Each makes the same upstream fetch and returns the same status, headers and body.
  - The proposal route maps to `viewer/dist-bel/` and its assets at `109aec2`, with health, redirect, 405, 400, 404 and Range handling. The live Worker for the comparison is `deploy/worker-realistic.js` at `01fac69`.
- `node test_worker.mjs`: 41 checks, unchanged.
- `qa/bel-20261030/request-list.json`: every file the proposal page requests on its 23-stop tour (eight files) exists in `109aec2`.
- The guided tour plays all 23 stops through its own buttons with no errors, and the stills switch stays hidden (`qa/bel-20261030/after-tour-play-c/`). The page loads with no page errors.
- `index.html`, `app.js`, `release-config.json`, `phase-dressing.js` and the concept layer match byte for byte on raw.githubusercontent.com.
- Live, before the deploy: `/realistic/health` shows `d5939f9…`; `/`, `/app.js` and `/health` have the hashes below; `/bengal-earth-lab/health` returns 404.

## Deploy steps (ChatGPT, the owner's desktop session, or Claude once the token has Workers permission)

1. **Guard.**
   - `/realistic/health` must show `d5939f9ef3928340908459efc440259df0d34b6d`. If it shows another source, stop: rebuild with that source as the first argument and `--bel 109aec2942fed6389b01c7b8e8bee0dac724784b`, then rerun both tests.
   - The original routes must keep their SHA-256 values: `/` `ff75beb5…2675`, `/app.js` `c6af8144…9bc4`, `/health` `5118ed49…378b` (check with `verify_release.py`).
2. **Keep the current live Worker** (`01fac69`, SHA-256 `f6e4730f…f922`) at hand for rollback.
3. **Upload.** Take `deploy/worker-bengal-earth-lab.js` from branch `claude/bengal-earth-lab-20261029` (the commit that carries this note) and check its SHA-256 against the value above. Upload it unchanged as the `stage2-office-virtual-tour` script: Cloudflare dashboard → Workers & Pages → stage2-office-virtual-tour → Edit code → replace the whole file → Deploy.
4. **Verify:**
   - `/bengal-earth-lab/health` shows `109aec2942fed6389b01c7b8e8bee0dac724784b`.
   - `/realistic/health` still shows `d5939f9…`.
   - `/`, `/app.js` and `/health` keep the hashes above.
   - `/bengal-earth-lab/` loads in a browser.

## Option A rooms (a later phase)

The owner chose the pilot (option C) first on 30 Oct 2026. The route still shows Merchandising Z07 and the accounts suite in Z06 as **option A, a later phase**: the room names, tour, signs and cards all say so. The relocation ledger is `qa/bel-20261030/OPTION_A_RELOCATION_LEDGER.md`. Deploying the route publishes a proposal, not a decision to move either team.

## Rollback

1. Re-upload the Worker from `01fac69` (SHA-256 `f6e4730f…f922`).
2. If that fails, use the older fallback `cdf0e3e` (SHA-256 `cb62a45f…a623`).

## Note on the separate /realistic/ release

The Lobby and CAD update (`533d698`, source `7257163`) is still a separate, undeployed Worker. To ship both together, build with `python3 build_worker.py 72571634cb78949d81b2bd80b08d4dd4670a0f51 --bel 109aec2942fed6389b01c7b8e8bee0dac724784b --out <file>`, then rerun both tests against the matching live Worker.
