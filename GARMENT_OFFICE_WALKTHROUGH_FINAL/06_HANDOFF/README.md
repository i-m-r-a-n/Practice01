# Ground floor walkthrough - handoff

Branch `claude/web-tour-assets` of `i-m-r-a-n/Practice01`, folder `GARMENT_OFFICE_WALKTHROUGH_FINAL/`.
The approved project (`GARMENT_OFFICE_FINAL_PRESENTATION/`, branch `claude/magical-hopper-74q4xq`) is unchanged.
Everything here is a visualization of the proposed design, not a photograph or a construction document.

## Where things are

| Folder | Content |
|---|---|
| `01_CLIENT_PITCH_VIDEO/` | `Client_Pitch_Cinematic_Tour.mp4` (pitch video, see STATUS.md for length and checks) |
| `02_FULL_FLOOR_TOUR/` | `Complete_Ground_Floor_Tour.mp4` (every major space) |
| `03_INTERACTIVE_3D/` | offline real-time 3D tour (three.js, no internet needed) + Mac presentation guide (`README.md`) |
| `04_BLENDER_ANIMATION/` | `Office_Walkthrough_Animation.blend` (the approved model + the 28 animated cameras) and all scripts |
| `05_PRODUCTION/` | storyboard, benchmarks, encoding settings, camera checks, browser tests, video QC |
| `06_HANDOFF/` | this file, `STATUS.md` |
| `07_WEB_TOUR_ASSETS/` | web GLB (16.6 MB), camera/room metadata, walk map - for the live web tour (issue #12) |
| `08_WORKER_READY_TOUR/` | the tour as two static files for the Cloudflare Worker (not deployed; see its README) |

## Play the videos on a Mac

- Download: GitHub -> branch `claude/web-tour-assets` -> folder -> file -> **Download raw file** (or Code -> Download ZIP).
- Open with **QuickTime Player** (double-click). Full screen: View -> Enter Full Screen (Ctrl+Cmd+F).
- Files are H.264 1920 x 1080, 24 fps, BT.709, "fast start" (also plays while downloading); they also play in Keynote and
  PowerPoint (Insert -> Movie) and in any browser.
- They carry a silent audio track; add music in Keynote / iMovie only with a properly licensed track.

## Show the 3D tour on a Mac

See `03_INTERACTIVE_3D/README.md` (Terminal: `python3 -m http.server 8000`, then open the address in Chrome or Safari).

## Rebuild

`05_PRODUCTION/ENCODING_SETTINGS.md` (videos), `07_WEB_TOUR_ASSETS/README.md` (web GLB, metadata),
`08_WORKER_READY_TOUR/README.md` (bundle).
