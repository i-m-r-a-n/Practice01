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

## Verified QA release — 2026-10-27

- **Production URL:** https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/
- **Production source revision:** `72f1087e0ce47cb17396174ced2f04cec1d01903` from QA branch `chatgpt/office-viewer-qa-v2`
- **Staging worker:** `stage2-office-tour-preview` on the same Cloudflare account; original Blender scene and Claude's branch remain unchanged.
- The Worker now serves HTML with no-store and revisions both `app.js` and `fallback.js` as cache-busting URLs, preventing stale JavaScript after releases.
- Normal Cloudflare Chromium browser-rendering validation of the **production** URL with `?room=Z08&photo=0`: HTML reported `3D model ready · 34 rooms`, `Boardroom` and 34 clickable sidebar buttons, HTTP 200.
- Browser test of GLTFLoader without a GPU: 41,857,588-byte GLB parsed into a Three.js scene with 34 Blender zone floors, 38 cameras, 2306 mesh instances, 61 embedded images and model bounds about 35.59 × 4.19 × 46.10 m.
- In a no-WebGL test harness, the full model loaded, room selections and guided-tour controls were exercised, and clickable actual floor polygon `Z09` correctly selected **Audit room**.
- A major ceiling matcher bug was fixed: Blender exported names like `CL001_...` instead of `CL001 ...`. New matching correctly identified 172 ceiling objects plus the steel deck; simulated toggle revealed all 173 and hid all 173.
- In a Cloudflare Chromium browser with `esm.sh` requests explicitly blocked, the dependency-independent `fallback.js` displayed all 34 room entries, dismissed the loading overlay and opened the **Boardroom** Cycles render for `?room=Z08`. This fallback is explicitly photographic rather than live 3D.
- Original final Blender render images are clearly labeled as static Cycles references; generic adjacent-room images are identified honestly as nearest available renders.

### Outstanding release limitations

- GPU-enabled **Mac Chrome/Safari** performance and raycast walking through every doorway have not been physically checked on the user's computer; do not mark those as verified.
- WebGL real-time lighting approximates the Blender Cycles output. The original Cycles images remain available for a realistic reference.
- Blender itself includes photo-estimated architectural measurements; the online scene is concept visualization, not construction documentation.
- This update is an interactive viewer, not a generated cinematic MP4. Video deliverables remain under Claude's separate workflow.
- The public GitHub repository serves the viewer assets and GLB. Maintain approved data-visibility policies before sharing new files.

### Claude / GPT integration contract

Claude should work on a distinct **Blender asset branch** and post the optimized GLB and tested camera metadata with a commit reference to GitHub issue #12. Do not force-push the GPT QA frontend branch or change the existing Cloudflare Worker without coordination. GPT can integrate the verified GLB after reviewing its material accuracy and WebGL performance.

### Production visual-polish follow-up

- Removed floating room-name sprites from eye-level interior views; room markers remain available when exploring the overall floor.
- Fixed view-dependent ceiling behavior: whole-floor view hides the steel deck and decorative ceiling pieces to reveal the layout; interior cameras restore the decorative ceiling/raft features while keeping the opaque deck hidden.
- Adjusted WebGL illumination and tone mapping to reduce overexposed white surfaces; still not claimed to be identical to Cycles.
- Live Cloudflare Chromium test after the production update at source revision `72f1087e0ce4` returned `3D model ready · 34 rooms` for the Boardroom deep link.
- Frame screenshots were inspected at the Boardroom viewpoint; live rendering confirmed visually, and the previous distracting interior room markers were absent.
