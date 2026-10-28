# Sprint visual QA —2026-10-28

## Scope and limits

The live browser test was blocked before application load; see `live/`. This review inspected actual local Chromium frames from the20a3de9 baseline at1440×900 and390×844. All six reference cameras were captured and viewed: CAM_01, CAM_04, CAM_09, CAM_07, CAM_34, CAM_13. The reference-camera API intentionally hides UI and fits the original16:9 camera inside the viewport, producing letterboxing on portrait screens. This is documented capture behavior, not evidence of a broken mobile interactive layout.

Separate ordinary interactive-room screenshots include the responsive controls. Their initial captures were still near the end of the arrival flight (flightT0.944 desktop,0.788 mobile); recapture after a completed flight is needed after any UI fixes. No synthetic render or AI image was substituted.

## Measured local results

- Model ready:2.008seconds at1440×900;1.538seconds at390×844. These are local software-GPU measurements, not live or MacBook load times.
- People API reports27loaded,frozen figures and0forbidden-zone violations.
- No console errors, uncaught page errors, or HTTP400+responses in either six-camera pass.
- One desktop `panjabi.glb` request reported `net::ERR_ABORTED`; the mobile camera pass had no request failures. Ordinary-room UI sessions also logged aborted people/lightmap requests. All27figures still reported loaded. Cause/impact is not established; the harness explicitly enables people while the application also starts them automatically, and context close can cancel outstanding requests. Do not mislabel these as HTTP404s or silently omit them.
- Document scroll width matched1440and390respectively. This did not detect the mobile toolbar's clipped rightmost controls.
- No native Mac, Safari or MacBook FPS test was performed.

## Defects and visual limitations found

1. **People toggle contrast (small safe fix).** The standalone `#mPeople` button has white/light text on a nearly white button. It is effectively unreadable at both viewport widths. Evidence: `local-baseline/1440_interactive_reception.png`, `390_interactive_reception.png`.
2. **Mobile toolbar clipping (small safe fix).** At390px the top row extends off the right edge: Help/fullscreen controls are clipped and narrow. The rest of the page does not horizontally scroll. Evidence: `390_interactive_reception.png`.
3. **Blank merchandising screen faces.** CAM_34 shows numerous bright blank monitor faces and a blank wall display. They read as placeholder screens. No invented business data should be added merely to fill them.
4. **Studio presentation framing.** CAM_13 foreground meeting furniture dominates the frame and working people are distant/small. This is a presentation tradeoff, not proof of incorrect furniture positioning. A camera-only improvement would need comparison and owner design constraints preserved.
5. **People remain visibly low-detail.** Faces, hair and hands look like simple game figures rather than photographs, especially at Reception. The models are illustrative; no photoreal claim is justified.
6. **Weak contact shadows.** Some chair/people contacts have little visible grounding shadow. The MD visitor's shoes can consequently read as slightly elevated in the camera image. The screenshot alone cannot prove millimetre floor penetration/gap; a geometric contact check is still required before any pose change.
7. **Task gestures are not always legible from the chosen camera.** The Boardroom presenter and Studio workers are distant; hand/object activity is difficult to verify visually. This does not justify claiming exact hand contact from the screenshots.

No obvious gross body-through-desk/chair intersection was visible in the six inspected camera frames. This is a scoped image observation, not an exhaustive mesh collision certification. Room/wall/furniture geometry was not edited by this QA task. Existing source logos were preserved.
