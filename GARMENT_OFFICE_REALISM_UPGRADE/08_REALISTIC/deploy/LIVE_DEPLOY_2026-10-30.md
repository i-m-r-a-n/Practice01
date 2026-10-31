# Bengal Earth Lab proposal route: live on 2026-10-30

## Deploy

- **Authorised by:** the owner, 30 Oct 2026: "C, deploy, if u cant tell chatgpt to deploy". Claude's Cloudflare token has no Workers permission, so the upload was handed to ChatGPT ([issue 12 request](https://github.com/i-m-r-a-n/Practice01/issues/12#issuecomment-6516697858)).
- **Deployed by:** ChatGPT, through the Cloudflare API (`PUT` of the unchanged file), at 09:15:52 UTC (15:15 Dhaka). Its report is in [issue 12](https://github.com/i-m-r-a-n/Practice01/issues/12#issuecomment-6519307394).
- **Cloudflare version:** `d9f95025-89f6-4e7a-9ae5-071dba5f082a`. The deployment is `be54c85f-bc65-4cad-bfb8-9b06fe1b0aeb`, at 100%.
- **Script:** `deploy/worker-bengal-earth-lab.js` from commit `35a11c7`, 10,363 bytes, SHA-256 `3424e88b85e1f551d5e558d32510734eb1da864395148543bb4e3035a7e4abd3`. ChatGPT reports that the SHA-256 matched before the upload and again on the live Worker read back after it.
- **Guard (ChatGPT, 09:10 and 09:15 UTC):** the live Worker matched the `01fac69` baseline (`f6e4730f…f922`). The public route hashes were unchanged and `/bengal-earth-lab/health` returned 404. ChatGPT reports that the Worker settings were identical before and after the upload.
- **Rollback:** not needed. The `01fac69` Worker (`f6e4730f…f922`) and `cdf0e3e` (`cb62a45f…a623`) stay the fallbacks.

## Independent checks from Claude's cloud session (2026-10-30, 12:04 UTC)

- `/bengal-earth-lab/health`: HTTP 200, source `109aec2942fed6389b01c7b8e8bee0dac724784b`, status "concept proposal preview".
- `/realistic/health` still shows source `d5939f9ef3928340908459efc440259df0d34b6d`.
- `/`, `/app.js` and `/health` keep their SHA-256 values: `ff75beb5…2675`, `c6af8144…9bc4`, `5118ed49…378b`.
- The live `/bengal-earth-lab/`, `/bengal-earth-lab/app.js` and `/bengal-earth-lab/release-config.json` match `viewer/dist-bel/` at `109aec2` byte for byte. Their SHA-256 values start `fe6cda03`, `11b0c620` and `2a83bf40`.
- `/bengal-earth-lab` without a slash redirects (307) to `/bengal-earth-lab/`.
- `/bengal-earth-lab/app.js` carries the header `x-bel-source: 109aec2…` and `cache-control: no-cache`.

## Live browser check

ChatGPT, 09:17 UTC, in Cloudflare Chromium at 1440 × 900:
- the page loaded with no uncaught errors and no failed resources;
- all 34 room buttons were present;
- the guided tour started at stop 1 of 23 and showed the option C wording.

It did not play all 23 stops.

Claude's check, 12:05 to 12:12 UTC, in Chromium with software WebGL in the cloud container (`qa/bel-20261030/live-tour-play-20261030/`):
- The guided tour played all 23 stops on the live page through its own buttons, and every stop matched the config.
- There were no page errors and no HTTP errors.
- The stills switch stays hidden.
- The menu lists the two option A rooms under "Option A · later phase".
- Stills of stops 1, 7, 11, 17 and 23 are saved.

## Notes and limits

- No test on Safari, a MacBook or a phone yet.
- The route is a concept proposal. Its labels say that fibre origins, recycled shares, tests, makers, growers and energy data are still to be verified.

## Update 2: STAGE II · Zara Fashion labels, live since 2026-10-30 17:52 UTC

- **Asked by:** the owner ("just use stage ii zara branding", then "update"). Claude's request: [issue 12](https://github.com/i-m-r-a-n/Practice01/issues/12#issuecomment-6524589490).
- **Deployed by:** ChatGPT, through the Cloudflare API, at 17:52:49 UTC (23:52 Dhaka). Its report: [issue 12](https://github.com/i-m-r-a-n/Practice01/issues/12#issuecomment-6529762309).
- **Cloudflare version:** `8bef92a5-5acf-42a9-8d82-2a1efcef6b71`. The deployment is `89cfc999-3217-44f5-841f-a0490cc5c549`, at 100%.
- **Script:** `deploy/worker-bengal-earth-lab.js` from commit `d11321e`, 10,363 bytes, SHA-256 `3bb5da83bfe2de517fdc3d7213f646c3298ab943e60e7dc4c9743797f5e61d03`. It serves source `e198902`.
  - ChatGPT could not fetch the raw file directly. It rebuilt the upload from the live script by changing the one source-commit pin.
  - Before the upload, it required the result to match the authorised file's full SHA-256.
- **Guard:** at 17:48 and 17:52 UTC, the live Worker matched `35a11c7` (`3424e88b…abd3`), and the five public-route guards held.
- **Rollback:** not needed. The fallbacks are `35a11c7` (`3424e88b…abd3`), then `01fac69` (`f6e4730f…f922`).

**Claude's independent checks, 2026-10-31 15:37 UTC:**
- `/bengal-earth-lab/health` shows source `e198902122e565878697d7606d9b4ce2b98b32b7`.
- `/realistic/health` still shows `d5939f9…`.
- `/`, `/app.js` and `/health` keep `ff75beb5…`, `c6af8144…` and `5118ed49…`.
- The live page, bundle and config match `viewer/dist-bel/` at `e198902` byte for byte.
- The live config reads:
  - page title "STAGE II · Zara Fashion - ground floor concept";
  - eyebrow "STAGE II · Zara Fashion";
  - headline "The ground floor, reimagined · concept proposal";
  - welcome title "Explore the ground floor proposal".
- The guided tour plays all 23 stops on the live page with no page or HTTP errors (`qa/bel-20261030/live-tour-play-20261031/`, about 15:40 UTC, Chromium with software WebGL in the cloud container).
