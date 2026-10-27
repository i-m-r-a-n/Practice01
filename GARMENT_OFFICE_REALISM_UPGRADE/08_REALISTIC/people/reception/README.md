# Reception frozen people

The current release candidate is exactly four fictional adults in Z02: a standing receptionist handing a blank visitor badge to a standing visitor, plus two sofa visitors, one reading an unbranded fabric-swatch book. Existing room, furniture and circulation geometry is unchanged.

Use `createPeopleLayer({ THREE, loader, scene, metadata, walkGrid, assetBase: './people/', manifestFile: 'reception/people-manifest.json', frozen: true, activeZones: ['Z02'] })`. Keep People on/off and the visible note “People shown are illustrative”. `update()` may cull/select LOD and manage visitor separation; it never moves or reposes a frozen actor.

Runtime files are `people-layer.js`, this manifest and pose JSON, and four existing CC0 GLBs under `assets/`. Do not publish Blender/source/review files as runtime assets. The archived 35-person manifest is not this release's entrypoint.

The broad `../build_people.py` contains an interrupted, unaccepted chair-solver experiment and must not overwrite the frozen GLBs. This release reuses the reviewed V2 character bytes.

`prepare_static.py` loads character-only source copies and derives the static arm/head poses; it does not open or edit the approved office. `source-lock.json` binds the exact candidate. Actual image evidence is `Reception-static.png`, `Badge-close.png`, and `Book-close.png`. These isolated previews use baseline lighting; final-host lighting and the independent four-actor contact/frozen-state check must be reviewed before publication.

No animation or walking people are included. Native MacBook Safari/Firefox/Chrome frame rates remain untested. CC0 asset provenance is in `../LICENSES.md`.
