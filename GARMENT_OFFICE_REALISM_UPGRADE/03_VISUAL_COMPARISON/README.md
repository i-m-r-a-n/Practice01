# Visual comparison: Cycles render | live tour now | improved build

Same six render cameras, 1280 x 720 browser window, interface hidden, Chromium (software GPU) on 27 Oct 2026.
- Left: the approved Cycles render (offline, photoreal reference).
- Middle: the live site now (`f9048ef`, web GLB without baked light), captured from the live URL.
- Right: the improved build (`08_WORKER_READY_TOUR` bundle + `Final_Office_Interior_web_realism.glb`, baked light), served locally.

Files: `comparison_<camera>.jpg` (full size), `comparison_contact_sheet.jpg` (all six), `shots/` (raw captures + camera state),
`metrics.json`. Script: `capture_rooms.js` (captures), `make_comparison.py` (sheets + metric).

| Room | Live vs render | Improved vs render | Closer? |
|---|---|---|---|
| Reception | 26.4 | 29.3 | no (brighter than the render) |
| Experience centre | 77.1 | 71.4 | yes |
| Boardroom | 51.8 | 40.4 | yes |
| Managing Director's office | 30.6 | 31.8 | about the same |
| Merchandising | 35.2 | 25.3 | yes |
| Global Design Studio | 38.7 | 32.8 | yes |

Metric: mean absolute RGB difference (0-255) to the render with all images reduced to 64 x 36 (overall light and colour,
not detail); lower = closer. It is a rough guide only; the sheets are the evidence.

What changed (visible on the sheets): walls and ceilings now carry the Cycles light: light pools under the linear and halo
fittings, light falling off towards corners and under the boardroom rafts, warmer whites instead of flat grey; the open-plan
merchandising and studio floors read much closer to the renders.

What is still different (not hidden): no reflections on glossy floors and glass (generic environment only), furniture keeps
real-time light (no contact shadows under chairs and tables), smaller contrast than Cycles, and the reception and MD office
come out brighter than their renders. The Cycles renders remain the photoreal reference; the tour shows them with the
"Photoreal render" button and at every guided-tour stop.

Note: the first capture of the improved build (08:28 UTC) was rejected and redone: the machine was busy, and the overlay
that fades between "ceilings off" and "ceilings on" still held a frame from the flight when the screenshot was taken
(pendant lights looked missing). The capture script now hides that overlay; the shots here are the clean second run.

## Ambient occlusion (added after the comparison above)
`ambient_occlusion/ambient_occlusion_ab.jpg`: boardroom and reception, same camera, baked light only (left) and baked light +
screen-space ambient occlusion (right): contact shadows under the sofa, armchairs, desk and chairs, depth in the ceiling
corners and slats, no artefacts on the glass (glass is left out of the occlusion pass). It is drawn once the view stops moving,
so movement stays smooth. Checked in Chromium and Firefox 159 (software GPU); the sheets in the table above were captured
before it was added, so the improved column there is without it.
