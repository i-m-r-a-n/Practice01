# Additive working-office props (Phase 4, prepared)

No viewer integration is performed by this folder. The parent release workflow controls the phase order.

```js
import { buildOfficeProps } from './props/office-props.mjs';
const manifest = await fetch('./props/office-props-manifest.json').then(r => r.json());
const props = buildOfficeProps(THREE, manifest, { anisotropy: 8 });
scene.add(props.group);
console.log(props.stats);
// props.dispose() releases geometries, materials and the generic-label atlas.
```

The module takes the viewer's own Three.js namespace to avoid a version mismatch. It adds an independent instanced group and never edits the loaded approved model. All coordinates are metres in the source viewer convention: x east, y up, z south. `support` records in the manifest retain source builder local inches, the furniture origin and rotation. Thin mats are walkable; all other props stay on already-colliding furniture or existing fixture tops, so this module supplies no new walk colliders.

Run from repository root:

```sh
python GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/props/build_manifest.py
node GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/props/check_geometry.mjs
python GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/props/validate_manifest.py
```

These are geometry checks. The Node check uses actual Three.js geometry with a canvas API stub and is not a GPU test. Actual browser screenshots, source-component intersections, contact shadows and readability must be checked on integration. The additions are not in the original or Phase 1 Cycles bake. Do not describe their shading as baked.

324 props, 28 rooms with additions, all 34 zones reviewed, 49 instanced draw calls, 128,878 triangles. One generic-label atlas (2K) is created in the browser. Plastic/glass/metal and cloth proxies are intentionally generic; fine prop textures and bespoke wear are still a visual quality gap. No original furniture was moved to give a false impression of a completed operating fit.

## Generic screen content helper

`applyOfficeScreenContent(THREE, root, options)` in `screen-content.mjs` finds `screen_ui` and `screen_brand` material groups, splits their connected screen components logically, and projects UV0 per front/back display plane. It clones geometry and screen materials; exact positions, normals, indices, UV1 and every non-screen material/UV are retained. It skips unsafe shared screen/non-screen UV vertices and reports them. Reapplication is idempotent. The original material shader hooks are retained for the room lighting decoder.

```js
import { applyOfficeScreenContent } from './props/screen-content.mjs';
const screens = applyOfficeScreenContent(THREE, roomScene, {
  zone: 'Z08', // omit if inherited metadata already contains zone
  anisotropy: 8,
  clientLogo: { image: loadedClientImage, provenance: 'assets/brand/logo_stage2_ltd.png' },
  // Reuse screens.texture as atlasTexture for later streamed rooms.
});
console.log(screens.touched, screens.skipped);
```

The optional client logo must come from the existing project brand folder; no replacement logo is invented. The shared atlas contains four actual Canvas glyph layouts: a sample approval sheet, generic review list, garment-pattern line drawing and neutral presentation slide. Logo use is restricted to the presentation cell used in Boardroom/Design Studio/Training. This is illustrative workspace content, not real records. The 2K atlas can be shared across rooms with `atlasTexture` to avoid duplicate allocations.

Independent checks rebuilt 29 actual source meshes as material-group meshes, identified 57 connected screen components and verified unchanged position/normal/index/UV1 and physical non-screen UV bytes. Actual Chromium Canvas artwork was captured and inspected in `../qa/props-independent/screen-content-atlas.png`; integrated monitor framing, texture sharpness, tone mapping and luminance still need screenshots. Portrait displays use a separate upright sample-guide cell in the same atlas padding, preserving suitable letter proportions.

Contact update: source-triangle SAT audit found 20 cable/monitor-base and 2 soap/wall candidate contacts. The bench cable anchors moved 3 inches sideways; wudu bottles moved 0.3 inches inward with 30 mm depth. The final generated prop envelopes have no approved-source triangle crossings above support +2 mm. Earlier evidence is retained under `qa/props-independent/rejected-prop-*-v1.json`. This check excludes the support-contact tolerance band and does not replace actual image review.

Sewing workpiece: PROP_0324 adds one self-made 0.36×0.11m fabric rectangle,1.2mm thick, on F206's raised bed at y=.8255m. The original323 prop records are unchanged. Actual cloth triangles touch only the intended F206 support plane, with no source crossing above it or frozen people-v2 t0 intersection. This is a static check; later pose cycles and integrated imagery remain required. Exact mesh/hash evidence: `../qa/props-independent/sewing-cloth-contact-check.json`.
