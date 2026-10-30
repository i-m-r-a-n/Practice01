# Deploying the Bengal Earth Lab proposal route (prepared by Claude, 30 Oct 2026; updated after increment 6: knitwear first, Bengal craft added)

**Status: prepared and tested locally, not deployed.** Claude does not deploy without the owner's authorisation.

## What it adds

- `/bengal-earth-lab/`: the concept proposal, with its own page, bundle and config. Source commit `0b239f65a0c867740d5b5d92725e938e1aabb1e1`. It contains increment 6: the approved knitwear dressing restored, the fabric stories, natural indigo, the jhut river, the tea stall, the living wall, and the option A circular knitwear studio and craft pieces. The 23-stop tour is included. Evidence is in `qa/bel-20261030/`.
- `/` stays byte-identical to the preserved production Worker.
- `/realistic/` stays identical to the live Worker. Its source is still `d5939f9ef3928340908459efc440259df0d34b6d`.

## Worker

- **File:** `deploy/worker-bengal-earth-lab.js`, 10,363 bytes, SHA-256 `19824644d954137544594ad0faf6d42a8dd1a67fc38afbad5547b22b12ee3916`
- **Built with:** `python3 build_worker.py d5939f9ef3928340908459efc440259df0d34b6d --bel 0b239f65a0c867740d5b5d92725e938e1aabb1e1 --out worker-bengal-earth-lab.js`
- **Previous builds**, never deployed and replaced by this file: increment 1 (source `60351b0`, SHA-256 `889d0b4f…a2a9`), increment 2 (source `539fc24`, SHA-256 `1a7451d9…eb83`) increment 3 (source `1a838d8`, SHA-256 `dad7a01c…a8bc`) increment 4 (source `1592542`, SHA-256 `e46c06dc…fb4a`) increment 5 (source `1f64305`, SHA-256 `bd8d3504…edfc6`), and increment 5 with the presenter polish (source `a83153c`, SHA-256 `0b4c2859…7e7e`).
- **The builder:** without `--bel`, the modified builder still reproduces the live Worker byte for byte (SHA-256 `f6e4730f…f922`, the file at `01fac69`).

## Checks passed

- `node test_worker_bel.mjs <live worker> worker-bengal-earth-lab.js`: 54 checks.
  - The 28 original-tour requests are byte-identical to the preserved production Worker.
  - 14 `/realistic/` requests (redirect, health, page, bundle, model, renders, Range, POST, path traversal) match the live `/realistic/` Worker. Each makes the same upstream fetch and returns the same status, headers and body.
  - The proposal route maps to `viewer/dist-bel/` and its assets at `0b239f6`, with health, redirect, 405, 400, 404 and Range handling. The live Worker for the comparison is `deploy/worker-realistic.js` at `01fac69`.
- `node test_worker.mjs`: 41 checks, unchanged.
- `qa/bel-20261030/request-list.json`: every file the proposal page requests on its 23-stop tour (eight files) exists in `0b239f6`.
- The guided tour plays all 23 stops through its own buttons with no errors (`qa/bel-20261030/after-tour-play-inc6b/`).
- `index.html`, `app.js`, `release-config.json` and the concept layer match byte for byte on raw.githubusercontent.com.

## Deploy steps (desktop session, or Claude once the Cloudflare token can see the account)

1. **Guard.**
   - `/realistic/health` must show `d5939f9ef3928340908459efc440259df0d34b6d`. If it shows another source, stop: rebuild with that source as the first argument and `--bel a83153c…`, then rerun both tests.
   - The original routes must keep their SHA-256 values: `/` `ff75beb5…2675`, `/app.js` `c6af8144…9bc4`, `/health` `5118ed49…378b` (check with `verify_release.py`).
2. **Keep the current live Worker** (`01fac69`, SHA-256 `f6e4730f…f922`) at hand for rollback.
3. **Upload.** Upload `worker-bengal-earth-lab.js` unchanged as the `stage2-office-virtual-tour` script.
4. **Verify:**
   - `/bengal-earth-lab/health` shows `a83153ce5432481f5b9adc17c34892e123e82702`.
   - `/realistic/health` still shows `d5939f9…`.
   - `/`, `/app.js` and `/health` keep the hashes above.
   - `/bengal-earth-lab/` loads in a browser.

## Option A rooms

The route shows Merchandising Z07 and the accounts suite in Z06 as **option A only**. The room names, tour, signs and cards all say so. The relocation ledger is `qa/bel-20261030/OPTION_A_RELOCATION_LEDGER.md`. Deploying the route publishes a proposal, not a decision to move either team.

## Rollback

1. Re-upload the Worker from `01fac69` (SHA-256 `f6e4730f…f922`).
2. If that fails, use the older fallback `cdf0e3e` (SHA-256 `cb62a45f…a623`).

## Note on the separate /realistic/ release

The Lobby and CAD update (`533d698`, source `7257163`) is still a separate, undeployed Worker. To ship both together, build with `python3 build_worker.py 72571634cb78949d81b2bd80b08d4dd4670a0f51 --bel a83153ce5432481f5b9adc17c34892e123e82702 --out <file>`, then rerun both tests against the matching live Worker.
