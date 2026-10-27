# People v1 contact review — rejected candidate

The browser exported actual runtime skinning, morphs and world transforms for all 35 visible characters at 0, 3, 6 and 9 seconds, with three walkers also exported at 0.35, 0.75 and 1.3 seconds. All 149 compressed geometry files were checksummed before this independent review.

All 35 characters have shoe penetration greater than 2 mm in one or more sampled poses; 148 of 149 snapshots fail that visual QA threshold. The worst is Reception visitor 03: a visible sole vertex lies 40.377 mm below the approved rug top. Visitor 04 penetrates that rug by 16.288 mm. Seated salwar, shirt and panjabi soles typically lie 4.9, 28.8 and 28.9 mm below the finished floor respectively. These are measured mesh defects, not just misplaced character anchors. Corrections must preserve seated contact with the approved chairs.

The separate exact source-furniture review also rejects this candidate: 21 of 23 seated characters have vertices more than 15 mm below their actual cushion-top footprint at all four sampled times. Some typing arms, hands and clothes cross desk surfaces. See `../props-independent/POSED-SEATED-REVIEW.md` and its detailed triangle reports.

The full projected convex hull of every visible mesh, including hand props, remains outside all eight designated empty zones in all 149 snapshots. The minimum measured hull-to-zone gap is 0.827 m. This conservative hull test covers every displayed triangle at those times; it does not prove continuous animation or every walking-path location. The separate authored capsule-path audit supplies complementary path evidence.

`floor-privacy-review.json` records per-character/task measurements, coordinates, source floor/rug references, source hashes and limitations. The large actual geometry exports remain at `/workspace/office-people-contact-export-v1`; their manifest binds the frozen v1 sources. Furniture authoring, hair/scalp and eye appearance, rendered realism, mutual visitor/actor movement, and Mac performance require subsequent review after corrections.
