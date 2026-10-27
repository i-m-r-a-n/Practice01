# Live Stage II baked-light tour — GPT integration and QA handoff

Date: 2026-10-27 (Asia/Dhaka). Deployed independently in GPT's connected Cloudflare account and tested via Cloudflare Browser Rendering (Chromium/WebGL).

## Deployments / source pins

- Production: https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/
- Worker name: `stage2-office-virtual-tour`
- Asset source: `claude/web-tour-assets`, immutable commit `ddf99eee703600ee722f06595708439560373567`
- Frontend patch: `chatgpt/stage2-baked-integration`, immutable commit `6a65b7d10982563ee7fdb059b791a67126d98ccb`
- Worker deployment ID: `25395afd1b974ed79c826f438f889b21`
- Worker modified at `2026-10-27T08:39:04.933592Z`
- Production Worker source: `09_GPT_INTEGRATION/worker.js` (this folder)
- Previous production implementation: `f9048ef67bf3a7faddbdfc35e50bc4a516916346`, unbaked 16.6 MB model. Restore its routing if a rollback is required.

## Bug fixed

**Critical runtime exception:** `Cannot read properties of undefined (reading 'lifted')` in bundled `08_WORKER_READY_TOUR/app.js` when first accessing `geometry.attributes.color.userData.lifted` on a `BufferAttribute` without `userData`.

Patch applied in own frontend branch only:

```diff
-if(!r.userData.lifted)
+if(!(r.userData??={}).lifted)
```

This initializes attribute metadata once, avoiding a TypeError while preserving the rest of Claude's baked vertex-colour logic. Claude's branches and original Blender project were not modified. Ask Claude to include the fix in its next generated bundle.

## Evidence and checks

| Acceptance check | Result | Evidence / qualification |
|---|---|---|
| Worker and main URL return successfully | PASS | Production Cloudflare Worker PUT status 200 and Browser Rendering HTTP 200 |
| Baked GLB correctly served | PASS | Browser HEAD HTTP 200; Content-Type `model/gltf-binary`; Content-Length **19,452,524 bytes** |
| Real WebGL viewer launches and model downloads | PASS | Real Cloudflare Chromium browser: loading overlay hidden, `19.5 / 19.5 MB`, blank `loadError` |
| Actual baked-light processing active | PASS | Browser API `window.__viewer.counts.bakedLight === true`, meshes merged to 100 draw calls |
| Room metadata and cameras present | PASS | Runtime `rooms:34`, `cameras:38` |
| Guided tour has 16 stops | PASS | Runtime `stops:16` |
| Actual visible 3D floor (rather than image-gallery fallback) | PASS | Chromium screenshot of baked isometric office preview examined; building geometry visible |
| Camera jump to Boardroom | PARTIAL | Runtime switches to `room:'Z08'`, `mode:'rooms'`, flying true; progress observed `flightT:0.385`. Full end framing was not independently observed on slow Chromium software rendering |
| Guided tour next / pause / resume / stop | PASS (state) | Chromium runtime observed stop index 0→1, playing true→false→true, stop clears tour and restores overview |
| Ceiling toggle two ways | NOT RETESTED on baked build | Claude's local viewer report states working; not independently confirmed after patched deployment |
| First-person walk, wall collision, Esc | NOT RETESTED on baked build | Claude's walk grid and local viewer tests exist; live software-rendering environment too slow for reliable automation |
| Search filtering and 390px responsiveness | NOT RETESTED on baked build | Existing viewer implementation supports them; verify directly on Mac before presenting |
| Safari on Apple Silicon | NOT TESTED | Cloudflare Chromium testing only |
| Frame rate | WARNING | Cloudflare's software-rendered WebGL test reported about 1.5 FPS. This is not representative of Apple Silicon GPU performance; do not infer user-facing FPS without testing it |

## Output quality / remaining realism gap

The baked GLB reuses the original geometry and uses vertex-colour illumination on 440 merged shell objects, while furniture remains real-time. Cycles rendering remains the photoreal reference. Do not claim identical Cycles-level shading in WebGL. Continue testing glass, textures, camera field of view, mobile performance and walking collisions on supported hardware.

## Next task for Claude

1. Take the exact `BufferAttribute.userData` patch upstream into the generator/bundled viewer to avoid the baked runtime crash on future exports.
2. Independently retest walk collisions, ceiling controls, all 38 camera jumps, 16-stop tour and mobile UI in a GPU-enabled browser, saving screenshot and JSON evidence.
3. Finish and verify the 2–3 minute complete ground-floor cinematic video; preserve the already completed 77-second client pitch MP4.
4. Deliver any further realism improvements on a separate Claude asset commit and post it to issue #12. Do not overwrite this production Worker.

## Rollback

The previous unbaked viewer was served with assets pinned at `f9048ef67bf3a7faddbdfc35e50bc4a516916346` and public URL unchanged. A failed release can be rolled back by routing `index.html`, `app.js`, and `model_web.glb` to the previous `08_WORKER_READY_TOUR/` and `07_WEB_TOUR_ASSETS/Final_Office_Interior_web.glb` at that commit, retaining original Cycles render routes. Verify Cloudflare Browser Rendering again after rollback.
