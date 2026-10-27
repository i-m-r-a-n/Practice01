# Static Merchandising people on the option B redesign (Z07)

From this increment on, `/realistic/` loads the **Z06 / Z07 option B model** (`../../revised-model/`, from Claude's `claude/space-optimization`). It is the approved design with only Merchandising and Commercial & Accounts redesigned. The released rooms (Reception, Boardroom, Experience Centre, MD Office) keep the same object names and look the same: re-captured with 1-3 % changed pixels, from the new light-bake noise.

The redesign changes the Merchandising furniture, so the approved-layout items are not used:

- The 76 GPT Z07 props were placed on the old desks. They are listed in `viewer/release-config.json` `excludedProps`. The new model carries its own desk / counter props: tech-pack binders, swatches, sample bags, cartons.
- The six approved-layout Z07 source actors are not used.

Eight new frozen fictional CC0 adults sit on the new layout's real chairs or stand at real work points. They use existing outfits and existing poses only:

| Actor | Where | Pose |
|---|---|---|
| 37, 38 | south chairs of bench 2 | typing / notes (seat 0.490 m) |
| 39 | north chair of bench 1 | typing |
| 40, 41 | either side of the inspection island | show_sample / browsing |
| 42 | buyer review table | listening (seated) |
| 43 | beside the buyer review screen | presenting |
| 44 | at the sample rails | fabric |

`prepare_merch.py` asserts that the earlier 15 actors and their poses are byte-for-byte preserved. Contact review is visual, from browser captures only. Native Mac performance is untested.

The fitting mirror on the column renders dark in WebGL (no real-time reflection).
