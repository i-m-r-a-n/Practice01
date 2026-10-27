# Lighting: what was missing and what was done

## Why the live 3D view looked flat (audit)

| Cause | Effect in the browser |
|---|---|
| glTF carries no Blender lights: the scene's **188 lights** (area, point, spot, sun) were not in the GLB | the office was lit by one generic environment + hemisphere light: even, washed-out, no light pools, no dark corners |
| No global illumination in real time | no bounce light, no soft shadows, no contact shading under furniture |
| Blender colour nodes dropped by the exporter (fixed earlier in `07_WEB_TOUR_ASSETS`) | sofas grey, carpet light, walnut pale |
| Fabric sheen exported without its weight (fixed earlier) | fabrics washed out |

## Method chosen: baked light in vertex colours (prototype -> full shell)

`bake_shell_lighting.py` (Blender 5.2, Cycles), run on the approved `.blend` without saving it:
1. Shell = 440 objects: floor finishes, walls and partitions, wall finishes, ceilings / rafts / baffles, steel deck,
   beams, columns. Furniture, glazing and light fittings are not baked.
2. Documented model fix before baking: the door-rail cut (see `../01_IMPROVED_MODEL/MODEL_FIXES.md`).
3. Modifiers applied, faces triangulated; only edges of faces larger than 0.3 m2 are split to at most 0.4 m (slats and
   trims keep their mesh). Result: 152,926 triangles, 78,519 vertices for the shell.
4. Objects joined into `WEB_SHELL_INTERIOR` and `WEB_SHELL_OVERHEAD` (Cycles bakes object by object with a full scene sync:
   440 separate objects would have taken hours; two objects bake in about 2.5 minutes).
5. Cycles bakes DIFFUSE light, direct + indirect, without surface colour, 96 samples, into a per-vertex colour attribute;
   stored value = light / 16 (`baked_light_scale` in the node extras; 99.5th percentile of the light = 7.2).
6. Export with the approved export settings + the colour attribute; then the web pipeline (`../01_IMPROVED_MODEL/make_web_glb.mjs`,
   16-bit colour quantization) adds the base-colour fixes, WebP textures and the `WEB_OVERHEAD` group.

**Why vertex colours instead of UV lightmaps:** no second UV set has to be generated for 440 objects, nothing can overlap,
there is no extra texture memory, and three.js reads `COLOR_0` with every version and material (no `lightMap` channel or
`uv1` handling to get right). The price is resolution: light varies at about 0.4 m on large surfaces, so light pools
and furniture shadows are soft, not sharp.

**Prototype first:** 25 objects (8 samples) to verify the export carries `COLOR_0`, then 60 joined objects, then the full
shell compared on 5 cameras against the Cycles renders before it was adopted (`../../GARMENT_OFFICE_WALKTHROUGH_FINAL/05_PRODUCTION/camera_qc/baked_light_comparison.jpg`).

## Display in three.js (tested with the r169 bundle)

Meshes whose node has `userData.baked_light_scale` and a `color` attribute get an unlit material:
`MeshBasicMaterial({ map, color: baseColor x 16 x 2.0, vertexColors: true })` - base colour x baked light x exposure 2.0
(exposure chosen by comparing x2 and x3 against the renders; x2 is closer on 5 of 5 views). Glass (transmission) and
emissive lamps keep their PBR materials. Rooms without any lamp get a small light floor (dark grey, not black).
Furniture keeps real-time light: environment (RoomEnvironment PMREM, 0.5) + hemisphere (0.45) + a weak directional light;
the furniture's own shadows on the floor and walls are already in the bake. AgX tone mapping, exposure 1.0.

## Limits (not hidden)
- Soft, low-resolution light: no crisp shadow edges, small contact shadows (chair legs) are missing.
- Furniture is not baked: it does not darken in dim corners as much as in Cycles.
- Reflections on floors and glass come from a generic environment, not from the room.
- Glossy terrazzo / herringbone highlights are weaker than in Cycles (the baked shell is unlit = no specular).
