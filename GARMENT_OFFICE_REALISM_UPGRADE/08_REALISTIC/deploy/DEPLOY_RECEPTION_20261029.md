# Deploying the Reception interior release (prepared by Claude, not yet deployed)

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

1. **Guard.** Live `/realistic/health` must show `bcb92b00963fa51906676f8cca22da88f841dc64`, or `e98ecb5855c3e2586d4de535ee371e82519aead1` if the sprint release went live first.
2. **Deploy.** Upload this `worker-realistic.js` unchanged as the `stage2-office-virtual-tour` script.
3. **Verify:**
   - `/realistic/health` shows `0cda894f3e4b11edc64f9dc97f481b8e5986f003`
   - `/`, `/health` and `/realistic/` return 200
   - `/` is byte-identical (SHA-256 `ff75beb5…`)

**Rollback:** `worker-realistic.js` from commit `cdf0e3e` (source `bcb92b0`).
