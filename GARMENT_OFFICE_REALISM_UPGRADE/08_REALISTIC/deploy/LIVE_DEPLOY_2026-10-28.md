# Six-room /realistic release: live on 2026-10-28

## Deploy

- **Deployed by:** the owner's desktop Claude session, using the Cloudflare dashboard (paste + Deploy).
- **Cloudflare version:** `bcfea6b5`.
- **Script:** `worker-realistic.js` from commit `cdf0e3e`. 7621 bytes; sha256 starts with `cb62a45f7aca1aec`.
- **Guard:** before the deploy, live `/realistic/health` showed source `102d5e9...` (GPT's release). It matched, so the deploy went ahead.
- **Rollback:** not needed.

## Checks from the cloud session (2026-10-28 09:39 to 10:40 UTC)

- `/realistic/health` shows source `bcb92b00963fa51906676f8cca22da88f841dc64`.
- `/`, `/app.js` and `/health` are byte-identical to before (sha256 in `verify_release.py`).
- `verify_release.py`: 10 of 13 matched in one pass (`public-design_studio-verification.json`). The 3 misses were network read timeouts, not mismatches.
- Rechecked separately, all three match the commit:
  - `/realistic/app.js`: sha256 `0a7c8eea...`, header `x-realistic-source` bcb92b0;
  - `/realistic/review/design_studio-before-after.png`: `9be9c4a6...`;
  - `/realistic/model_web_baked.glb`: 19973644 bytes, `06f13e53...`.

## Notes and limits

- **Slow plain GETs from this network.** From the cloud container, plain GETs of large files were intermittently very slow. This happened for the new GLB and also for the long-cached `/model_web.glb`, while a `Range: bytes=0-` request downloaded the full 20 MB in under 1 s. This looks like a property of this network path, but real visitors' load times were not measured here.
- **No live browser render.** No WebGL screenshot of the live page was taken from the cloud container: the live page does not load in the container's Chromium.
