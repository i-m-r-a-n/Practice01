# Deploying the Bengal Earth Lab proposal route (prepared by Claude, 30 Oct 2026; updated after the owner chose option C)

## Update 2: STAGE II · Zara Fashion branding (30 Oct 2026, prepared, not deployed yet)

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
