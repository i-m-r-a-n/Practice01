# Optional illustrative office people layer

This module adds 35 fictional adult characters and 3 conservative corridor routes. It never modifies the approved office source, room boundaries, furniture or the old tour. The current status is **prototype awaiting final contact/visual acceptance**, not a photorealism claim.

The latest user instruction explicitly overrides the old SUPER_PROMPT no-people rule. Every UI that enables this layer must show **People shown are illustrative** and offer **People on/off**. Leave the current route unchanged; integrate only in the new `/realistic` route after root clearance.

## Integration

Serve the contents of this directory as `/realistic/people/`, excluding `source/`, Blender source files and review evidence from the runtime bundle. Runtime needs four GLBs, `people-manifest.json`, `poses.json`, `people-layer.js`.

```js
const people = await createPeopleLayer({
  THREE, loader, scene, metadata: meta, walkGrid: grid,
  assetBase: './people/',
  extraBlocked: (x,z,radius) => props.blocksMovement(x,z,radius)
});
await people.setEnabled(true, camera.position);
// Every animation frame, also during walking:
people.update(dt, { camera, playerPosition: camera.position, quality });
// Add to the existing controller's collision predicate:
const occupiedByPerson = people.blocksMovement(nextX, nextZ, 0.15);
```

The existing static grid already grows walls/furniture by 0.15m. `blocksMovement` adds person–visitor separation; it must be used by real movement controls, not merely by screenshots. The three routes are prevalidated for approximately 0.25m actor radius. The optional `extraBlocked` hook checks additive prop obstacles. Moving actors check static cells, other actors and a visitor lookahead and stop rather than walking through them. No actor or route is allowed into Z23–Z29 or Z34. Original cameras are not silently repositioned for people.

`stats()` exposes loaded/enabled/visible/total, walkers, excluded-zone violations and the explicit native-Mac-test status. `diagnostics()` provides actor positions, LOD parts and selected joint positions for independent QA. `dispose()` removes the layer.

## Assets and animation

- Four licensed generic anatomical bases: shirt/trousers, panjabi, two salwar-kameez/hair variants. No ripped game content or identifiable scans.
- CC0 MakeHuman skin, eyes, hair, shirt, shoes, body and rig. See `LICENSES.md` and `source-sha256.json`.
- Reduced 22-bone skeleton per actor, shared geometry/textures, independent skeletons.
- Two geometry LODs; clothing LOD classification follows parent names because glTF multi-material child mesh names omit LOD prefixes.
- Three per-actor facial morph parameters deform skin, eyes and hair together; varied skin/clothing/hair tint, proportions and task timing. The finite bases do not equal 35 bespoke hero heads.
- Procedural subtle task motion plus a 12-key walking cycle. This is not captured human performance or dynamic cloth simulation.
- Seated support tops are measured from approved GLB triangles. Actual trouser underside, shoe sole and palm surface geometry drive pose solves; resting hands target the clothed lap. Separate seated pose solves cover 0.4445,0.48768,0.49022,0.50292m supports; body height is not varied for seated actors.
- Seated roles use fitted long-sleeve shirts/trousers; standing roles may use the modest tunic extension. Non-sofa female actors sit 5cm forward on unchanged cushions.
- Reception shoe targets include the actual 21.59mm-high rug, not only the 10.16mm floor finish.
- Phone/cup/file props are self-made and unbranded.

A self-made saree experiment was rejected after actual render review because its rigid drape and seated intersections were conspicuous. It is not included in the manifest/runtime. The replacement is a second modest salwar variant, with the limitation explicitly reported.

## Review and reproducibility

- `build_people.py`: builds editable character copies and GLBs from source assets; never opens the office Blender model.
- `prepare_manifest.py`: deterministic placements and conservative route validation against the original walk grid.
- `review/office-preview.html`: isolated geometry/contact preview; baseline lighting, not the new lightmap release.
- `review/capture_office.py`: actual six-room and additional task/private-room screenshots.
- `review/test_people.py`: LOD completeness, on/off collision, route motion and visitor-yield checks under Chromium SwiftShader.
- `review/rejected-lod/`: deliberately retained failed screenshots from a diagnosed multi-material LOD defect; not release evidence.

Remaining acceptance: the current V2 actual deformed furniture/prop and animation-cycle contact review, followed by visual acceptance in the final lit scene. V1 is rejected with exact contact evidence under `review/rejected-contact-v1/` and the separate QA export. Corrected sofa, sewing and phone close-ups have been rendered and inspected, but do not substitute for the independent contact test. Native Apple Silicon Firefox/Chrome/Safari frame rate, thermals and animation quality on the user's device have not been tested. Do not describe browser software-GPU checks as proof of 30fps on a MacBook.
