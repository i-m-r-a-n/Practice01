# Deploying the /realistic sprint release (prepared by Claude, not yet deployed)

`worker-realistic.js` in this folder is built for source commit `9acdeafd3bb91100572dfded7b677dee12e9dc40` (branch `claude/realistic-sprint-20261028`).

- Size and SHA-256: 7621 bytes, `83e427458192a72efd713e34bf632ea9e82d2699d1e3bb01e7d5ed5c12337975`.
- Its only difference from the live worker is the `REALISTIC_COMMIT` line.

It serves the same six rooms as the live release, plus the sprint changes:

- **R1 usability:**
  - readable People toggle
  - two-row phone header (Help and Full screen no longer cut off)
  - larger concept / illustrative-people notice
  - GPT's direct-drag sign fix
  - on phones the room notes fold to two lines; a tap opens them
- **R2 client identity**, all self-made and on furniture or walls:
  - water & wellbeing refill point with every result *pending*
  - coconut-shell button story with supplier data *pending*
  - sample cards
  - Jamdani-inspired panel
  - MD development samples and boardroom fabric trays
  - generic screen content
  - a "Concept" note per room
  - the Design Studio opens on its existing camera `CAM_14_Design_Studio_B` (desks, screens and colour wall) instead of `CAM_13`
- **R3 people:** soft contact shadows under feet and chairs. Measured on the skinned vertices: no one floats or sinks.

Nothing structural moved: walls, doors, windows, existing furniture, walk grid and the people manifest are unchanged.

## Checks run before release (local Chromium, software WebGL; not live, Safari or MacBook proof)

- `node test_worker.mjs`: 41 checks pass. The 28 original-tour requests are byte-identical to `production-worker-before.js`.
- `qa/sprint-claude-20261028/r2/`:
  - smoke tests at 1440 × 900 and 390 × 844
  - toolbar / contrast / drag / People checks at 1440, 390 and 360
  - a header layout probe at 16 widths
  - room and visitor-eye frames
- Every file the route fetches exists at the source commit on raw.githubusercontent.com: the three changed files (`viewer/dist/index.html`, `app.js`, `release-config.json`) were fetched back at that commit and match byte-for-byte; every other file the page loads is unchanged since the live source `bcb92b0`.

## Deploy (Worker owner)

1. **Guard.** Live `/realistic/health` must still show `"source":"bcb92b00963fa51906676f8cca22da88f841dc64"` (Cloudflare version `bcfea6b5`). If it shows anything else, stop and reconcile first.
2. **Deploy.** Upload this `worker-realistic.js` unchanged as the `stage2-office-virtual-tour` script: Cloudflare dashboard → Workers & Pages → stage2-office-virtual-tour → Edit code → replace the whole file → Deploy.
3. **Verify.**
   - `/realistic/health` shows `"source":"9acdeafd3bb91100572dfded7b677dee12e9dc40"`.
   - `/`, `/health` and `/realistic/` answer 200.
   - Then run `python3 verify_release.py Design_Studio 9acdeafd3bb91100572dfded7b677dee12e9dc40 --report public-sprint-20261029-verification.json`.

**Rollback:** upload `worker-realistic.js` from commit `cdf0e3e` (identical to `rollback-sprint-20261028.js` apart from a final newline). That is the current live worker, source `bcb92b0`. The original tour at `/` is unaffected either way.
