# Reception-only /realistic — public rollout verification

**Scope:** only the Reception (Z02) increment. The approved 34-room tour at `/` remains unchanged.

- Public URL: https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/realistic/?room=Z02&welcome=0
- Release source commit (immutable): `8a01ddc7bd9d8b5acc3b99ef287f1263088f9e52`.
- Worker route: `/realistic` redirects to `/realistic/`; all new resources use the `/realistic/` prefix.
- Original Worker source: `deploy/production-worker-pre-reception.js`.
- The live Worker has a single `/realistic` dispatch added to its previous root-route function. Removing that dispatch and the appended realism router yields the **byte-identical** original Worker (modulo trailing whitespace), verified against this checked-in snapshot. It does not modify `/`, `/app.js`, `/present`, PDFs or MP4 routes.
- Production Worker version at the time of independent confirmation: `1b4a2b4c-f611-415a-9e02-69f8e92b93f5`, created 2026-10-27 18:26 UTC.
- Source of all assets: `GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/` at the pinned commit. `viewer/dist/release-config.json` has `releaseMode: 'reception'`, `releaseZones:['Z02']`, `peopleAccepted:true`.
- One room only: Z02 Reception. Existing 19,452,524-byte baked GLB, plus 1,725,000-byte furniture geometry and 18,938,140-byte KTX2 lightmap.
- Four fictional frozen illustrative occupants with People on/off, 8 additive practical props, source meshes unchanged. The people are not photorealistic and no dynamic movement is claimed.
- Browser evidence from source release: `qa/reception-offline/capture.json` (Chromium/WebGL 154, Z02 captured, lightmap loaded, no reported JS/HTTP errors), plus `review/reception-release.json`.
- Independent production Cloudflare Chromium browser check on `/realistic/?room=Z02&welcome=0`: HTTP 200, WebGL renderer canvas present, `19.5 / 19.5 MB` downloaded, loading overlay hidden, no startup error text.
- Independent public asset HEAD checks: all 12 target paths HTTP 200 including `app.js`, `release-config.json`, `model_web_baked.glb`, `lighting-v2/manifest-hybrid.json`, Z02 lightmap KTX2, Z02 furniture GLB, people JS + manifest, baseline/after images, merged before/after PNG.
- Before/after original same-camera browser composite:
  https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/realistic/review/reception-before-after.png
- Live composite HTML:
  https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/realistic/review/reception-before-after.html
- Browser testing caveat: native Firefox test is handled independently by GitHub Actions workflow `Reception Realistic Firefox QA`, started on test branch `chatgpt/office-realistic-reception-firefox-qa` at run https://github.com/i-m-r-a-n/Practice01/actions/runs/40561080378 . Do not claim Firefox pass until the run passes.
- Future rooms: do not publish Z30/Z08/Z12/Z07/Z18 as 'realistic' before their individual lightmaps, props, complete checks and before/after evidence are ready. Each subsequent release should be individually pinned and individually linked.

## Rollback

The Worker source in `deploy/production-worker-pre-reception.js` restores the exact `/` and other original routes, dropping only the isolated realism route.
Keep the currently verified `/` as stable even if a future /realistic incremental update fails.

## Honest visual limitations

The initial 4 frozen receptionist/visitor figures remain stylized real-time people and may not resemble real employees. Neither identical offline Cycles realism nor Mac GPU frame rate is claimed. User-visible floor paths/doors and material/lighting need per-room acceptance before further rollouts.
