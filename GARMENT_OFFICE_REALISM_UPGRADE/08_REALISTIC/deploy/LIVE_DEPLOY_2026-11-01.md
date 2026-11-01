# Proposal route update 7: live on 2026-11-01

## Deploy

- **Authorised by:** the owner. They gave ChatGPT the prompt for [deploy request 7](https://github.com/i-m-r-a-n/Practice01/issues/12#issuecomment-6553087659), then wrote "chatgpt deploy koreche, check koro" ("ChatGPT has deployed, check it").
- **Deployed by:** ChatGPT, through the Cloudflare API. [Its report](https://github.com/i-m-r-a-n/Practice01/issues/12#issuecomment-6556522063) has the details.
- **Cloudflare version:** `a575814a-27dd-4c96-9f15-e529ceac3eca`, at 100%.
- **Time:** live at 2026-11-01 10:05:54 UTC (16:05 Dhaka).
- **Script:** `deploy/worker-bengal-earth-lab.js` from commit `bfab122`, unchanged. It is 10,742 bytes, SHA-256 `126baec4e8e61ac41508cbd952fcb89236c50f156d05c7bcc7d0408c0208d695`, and serves source `a43fd96e2358c3a4e7a6b73bbf77ef18f97844bb`. ChatGPT downloaded the deployed script and confirmed the size and hash.
- **Guard:** case A held. Nothing newer was live, and the live script was `d11321e` (`3bb5da83…1d03`).
- **One rollback, by ChatGPT:**
  - Its first upload, at 09:58:23 UTC, was rolled back at 09:58:52 UTC because ChatGPT's own static-HTML header check failed.
  - That was a false negative. `app.js` sets the header when the page starts, and CSS shows it in capitals.
  - ChatGPT uploaded the same unchanged file again at 10:05:54 UTC.
- **Rollback files:** `d11321e` (`3bb5da83…1d03`), then `35a11c7` (`3424e88b…abd3`).

## Independent checks from Claude's cloud session (2026-11-01, from 15:02 UTC)

- `deploy/verify_bel_live.py a43fd96…` passed all 78 checks (`qa/bel-20261030/live-20261101/verify-live.json`):
  - `/stage2-concept/health` shows `a43fd96…` with route `/stage2-concept`.
  - `/realistic/health` still shows `d5939f9…`.
  - `/`, `/app.js` and `/health` keep `ff75beb5…`, `c6af8144…` and `5118ed49…`.
  - `/bengal-earth-lab/`, `/bengal-earth-lab/app.js` and `/stage2-concept` answer 307 to the matching `/stage2-concept/` address.
  - 68 files match the commit byte for byte, each with the right content type and `x-bel-source`: the page, the bundle, the config, `images.html`, the 26 stop images, their 26 thumbnails and the 12 3D model views.
  - An unknown file type answers 404, and a POST answers 405.
- Browser checks against the live site, in local Chromium with software WebGL: see below.

## Notes and limits

- Not yet tried on a real iPhone or Android phone. The phone checks emulate touch in Chromium.
- The route is a concept proposal. Its labels say what each image is, and the footer says that fibre origins, recycled shares, tests, makers, artists, growers, stone sources and energy data are still to be identified.
