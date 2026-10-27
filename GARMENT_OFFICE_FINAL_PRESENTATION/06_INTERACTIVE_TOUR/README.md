# Stage II Interactive 3D Office Tour — GPT frontend handoff

**Client-facing URL:** https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/

**GitHub repository:** `i-m-r-a-n/Practice01`  
**Frontend branch:** `chatgpt/interactive-office-tour`  
**Original 3D project branch:** `claude/magical-hopper-74q4xq`  
**Cloudflare Worker:** `stage2-office-virtual-tour`

## Implemented

- Client presentation UI with department-grouped, searchable room list (34 confirmed zones).
- Existing GLB scene loaded via Three.js; 38 saved Blender camera nodes intended for room navigation.
- Whole-floor overview, selected-room camera transitions, orbit, pan, zoom, room markers and ceiling visibility controls.
- WASD-based walk mode with wall raycast collision check and pointer-lock mouse movement (requires real WebGL verification).
- Guided sequence with isometric beginning/end, room cuts, subtle camera movement, previous/next, pause/resume and stop.
- **Genuine architectural render reference**: selected room shows an actual Cycles JPG from `02_RENDERED_IMAGES/final/`, labelled as a rendered still rather than live WebGL.
- Graceful WebGL-unavailable fallback: a working gallery of the actual room renders with room selection and guided image tour. This is NOT represented as true 3D.
- Cloudflare Worker streams the 42 MB GLB and verified Cycles JPG files from the existing public GitHub project.

## Checks performed

Browser-side validation:
- Cloudflare site and /health return HTTP 200.
- JavaScript imports load from pinned `esm.sh/three@0.164.1` URLs (original unresolved bare `three` issue repaired).
- GLB HTTP 200 and valid binary: 41,857,588 bytes, glTF 2.0, 1150 nodes, 563 meshes, 79 materials, 61 images, 38 cameras.
- Test browser has no WebGL graphics context; fallback activates without an infinite loading overlay.
- 34 room buttons render, text filtering works, boardroom selection loads corresponding 1600px Cycles render, and design studio loads corresponding 1600px render.
- The guided fallback tour starts, advances, pauses, resumes and stops; isometric cover image loads at 1920px.
- No page-level JavaScript errors observed during fallback checks.

**Not verified yet:** Real GLB rendering and interactive camera/walk behavior on Chrome/Safari with active GPU/WebGL; collision safety for every doorway; comparable material fidelity to offline Cycles renders. Do not claim these are completed until a GPU-browser test passes.

## Real Mac acceptance test

1. Open live URL in Chrome or Safari with WebGL enabled.
2. Confirm the *actual 3D mesh*, not only the gallery, appears.
3. Select Reception, Boardroom, Managing Director, Merchandising, CAD, Design Studio.
4. Check camera framing and textures; compare each with its reference Cycles preview.
5. Test Hide Ceilings and restore, full-floor view, mouse orbit/zoom.
6. Enter Walk mode; click canvas to lock the pointer; test WASD, wall collision and Escape.
7. Run guided tour; test Previous, Next, Pause/Resume, and Stop.
8. Test fullscreen and reload.

## Collaboration / division of responsibility

**GPT:** frontend application `06_INTERACTIVE_TOUR/{index.html,app.js}`, Cloudflare Worker deployment and QA.

**Claude:** Blender GLB asset quality, PBR materials, verified lighting/export enhancements, camera metadata, optimization; use a new branch, do not overwrite GPT frontend files.

Claude assignment: https://github.com/i-m-r-a-n/Practice01/issues/12

## Known architectural caveats

This is a **proposed** interior with site measurements and technical verifications still outstanding (including ceiling height, stair exits, HVAC, fire strategy). Do not present as construction-approved.

## File entrypoints

- `index.html`: main browser client
- `app.js`: Three.js and navigation code
- GLB: `../01_EDITABLE_3D/Final_Office_Interior.glb`
- Cycles JPGs: `../02_RENDERED_IMAGES/final/CAM_*.jpg`

External ESM dependencies are pinned to Three.js 0.164.1. A tested production bundle on the same domain would improve long-term reliability.