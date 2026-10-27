# Static Experience Centre people

This incremental scene uses three existing fictional CC0 adults in Z30: buyer05 supports a sample tee at its shoulders, merchandiser06 explains the sample, and buyer07 touches the front of an existing sage garment on rail F020. Every actor is frozen. No rail, source garment, mannequin, table, counter, logo or camera is moved.

Buyer07 stands 100 mm closer to the rail than the rejected v2 candidate, preserving the existing rear rail/table loop while keeping the same fabric contact point. The corrected route passes the actual viewer collision predicate at intervals of at most 1 cm. `rejected-rear-aisle-v2/` preserves the failed navigation candidate and hashes; `rear-aisle-repair-preservation.json` verifies the other twelve actors/poses and all props remain unchanged.

The sample tee is a small self-made silhouette based on the project's existing `garment_tee` outline, with 4 mm thickness, shallow subdivided folds and a slightly sagging hem. It uses a rough unbranded sand fabric material. Two hands support its shoulder edges; no detailed pinching-grip or live cloth simulation is claimed. No new character asset or external download is required.

Actors05 and07 use the existing modest long-sleeve shirt/trouser layers with their overlapping long drapes hidden. This removes visible self-intersection in these standing poses. The optional `hideLongDrape` flag is set only on these two new actors; prior ten actors and their visible meshes retain the same inputs.

Use `manifestFile: 'experience/people-manifest.json'`, `frozen: true`, `activeZones: ['Z30']` for isolated review. The cumulative runtime entrypoint remains `../room-release/people-manifest.json`, now thirteen people across Z02, Z08 and Z30. Keep the People on/off control and illustrative-person note.

`prepare_static.py` reads existing character-only source blends. The prior ten actor/prop/pose definitions come from `baseline-people-manifest.json` and `baseline-poses.json`, exact bytes from published commit `039091d5d35ea97adf95ff439231f6336ed05381`. `preservation-check.json` records comparisons. Never run the older broad character build script over these accepted GLBs.

`source-lock.json` binds this candidate. Independent actual triangle contacts, shoe support, frozen geometry and viewer checks determine bounded acceptance. Diagnostic captures use the established source-geometry preview lighting; final integrated viewer images are the delivery reference. Native Mac performance remains untested.
