# Static Boardroom people

This incremental candidate contains six fictional adults in Z08: five seated meeting participants and one standing presenter indicating the unchanged screen. Two participants have unbranded notebooks and resting pens. The three listeners look toward the screen/presenter. All actors are frozen, with no walking or gesture animation.

The five actor anchors move only 30–50 mm forward from the earlier people experiment to clear the original chair front edges. Original furniture, architecture, room dimensions, logos and screen geometry remain unchanged. Four existing CC0 character GLBs are reused byte-for-byte. Modest clothing and the accepted illustrative-person disclaimer remain in place.

Load `manifestFile: 'boardroom/people-manifest.json'` with `frozen: true` and `activeZones: ['Z08']` for isolated review. The cumulative deliverable is `../room-release/people-manifest.json`, containing the accepted Reception four plus these six actors. Runtime delivery needs the manifest, minimal poses, `../people-layer.js`, and the four existing GLBs. Do not publish the Blender source files or review scripts as runtime assets.

`prepare_static.py` reads the existing character-only source blends using Blender 5.2.3. It never opens the approved office blend, writes assets, or modifies Reception data. It retains the original leg poses and derives only presenter, note-hand, and listener-head rotations. Do not run the broad `../build_people.py`; its interrupted solver experiment is not the accepted character source.

`source-lock.json` records candidate runtime hashes. Separate independent QA controls acceptance; pending wording inside the locked manifest records candidate creation and must not be mistaken for an acceptance report. Diagnostic PNGs use the existing baseline-lighting preview; final viewer captures retain the approved warm runtime lighting.

Faces remain modest game-character quality. Notebook hand support is a fixed pose approximation, not handwriting animation. Native MacBook browser performance remains untested. Provenance is recorded in `../LICENSES.md`.
