# Static MD Office people (Z12)

Two frozen fictional CC0 adults, appended to the cumulative `../room-release/people-manifest.json` (now 15 people across Z02, Z08, Z30 and Z12):

- `office-person-14`, the MD at the desk on the phone. This is the approved source actor, chair (F064 exec_chair_cognac) and seat-specific pose, unchanged and only frozen.
- `office-person-36`, a visitor taking notes in visitor chair F065 (plan 1010, 118 in), facing the MD across the desk. It uses the existing `salwar` CC0 outfit and the existing `notes__seat_48768` pose, matched to the visitor chair's 19.2 in seat top.

No furniture, prop, camera, earlier actor or pose was changed. `prepare_md.py` asserts that the earlier 13 actors and all their poses are byte-for-byte preserved. The six existing GPT room props for Z12 are enabled through `releaseZones`.

Made by Claude (branch `claude/realistic-rooms`), continuing GPT's six-room plan after GPT's execution environment became unavailable. Contact review: a visual check of the browser captures only. The finger-level contact measurements GPT made for earlier rooms were not repeated. Native Mac performance is untested.
