# Reception release QA acceptance

PASS for the bounded controls and frozen-person collision checks against served app SHA256 `1fa75488491ac301562f03d2e5ce86dcf896120ead7a8a56c0d39bc76875ba1a` (runtime commit `8a01ddc7bd9d8b5acc3b99ef287f1263088f9e52`). Runtime bytes were unchanged.

The [initial controls report](reception-release-controls-final/controls-report.json) retains its 16 passes and one incorrect assertion. The [focused corrected check](reception-release-controls-corrected/controls-report.json) passes: at 1280×720 with a fine pointer, the original `#pad` is hidden and `#minimap` is visible. This matches the original app's pointer-specific control logic.

Both [people collision scenarios](reception-release-collisions/collision-report.json) pass with exactly four frozen people: the visitor stops 0.490546m from the standing actor (combined capsule radii 0.4m, 414 collision responses), and enabling People at an occupied anchor leaves the visitor unblocked. There were no page, console, or viewer errors. The walking-actor scenario was excluded because this scene is frozen.

The existing [static contact acceptance](props-independent/reception-static4-contact-acceptance.json) remains separate evidence. Native Mac FPS and Safari are untested; software camera-request timings are not FPS. [Machine-readable acceptance](reception-release-acceptance.json) records report hashes and source references.
