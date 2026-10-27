# Deploying the six-room /realistic release (prepared by Claude, not yet deployed)

`worker-realistic.js` in this folder is built for source commit `bcb92b00963fa51906676f8cca22da88f841dc64` (branch `claude/realistic-rooms`):

- Reception, Boardroom, Experience Centre (GPT, unchanged)
- MD Office
- Merchandising on the Z06 / Z07 option B model
- Global Design Studio

27 frozen illustrative people.

**Checks run:**
- `node test_worker.mjs`: 41 checks pass. The 28 original-tour requests (`/`, `/app.js`, `/present`, videos, PDFs, `/health`, ...) are byte-identical to `production-worker-before.js`.
- Every file the route fetches exists at that commit on raw.githubusercontent.com. The GLB SHA-256 matches.

**Why it is not live yet:** Claude's session has no access to the Cloudflare account that owns `stage2-office-virtual-tour`.

## Deploy (Worker owner)

1. **Guard.** The live script must still be GPT's last release: `worker-realistic.js` at commit `07d9623`, `REALISTIC_COMMIT = '102d5e9...'`. If it differs, stop and reconcile first.
2. **Deploy.** Upload this `worker-realistic.js` unchanged as the `stage2-office-virtual-tour` script, using the same method GPT used (Cloudflare API PUT).
   - Without the API: Cloudflare dashboard → Workers & Pages → stage2-office-virtual-tour → Edit code → replace the whole file → Deploy.
3. **Verify.** `python3 verify_release.py Design_Studio bcb92b00963fa51906676f8cca22da88f841dc64`. It checks:
   - public bytes, `/realistic/health` source
   - the unchanged `/`, `/app.js`, `/health`
   - the offline zip

**Rollback:** upload `worker-realistic.js` from commit `07d9623` (the current live version). The original tour at `/` is unaffected either way.

## Room before / after images

- `../review/md_office-before-after.png`
- `../review/merchandising-before-after.png`
- `../review/design_studio-before-after.png`

Per-room release notes: `../review/*-release.json`. Offline packages: `GARMENT_OFFICE_WALKTHROUGH_FINAL/09_MAC_OFFLINE_TOUR/realistic-{md_office,merchandising,design_studio}/`.
