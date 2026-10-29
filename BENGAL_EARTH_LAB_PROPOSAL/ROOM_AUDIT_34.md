# 34-zone floor capability audit — Bengal Earth Lab
**Version:** 30 October 2026. **Status:** measured against the repository *concept metadata*, not the physical building or approved construction survey.

## Source and validation
- Primary geometry: [Claude's 9f2cd3a office_web_metadata.json](https://github.com/i-m-r-a-n/Practice01/blob/9f2cd3a/GARMENT_OFFICE_SPACE_OPTIMIZATION/04_SIMPLE_VIEWER/assets/office_web_metadata.json), file blob `eab165fabf0f0aa7df7559827119317db2697291`. This is an unapproved Z06/Z07 option B concept. Dimensions, walls, window placements and uses still require site verification.
- Newer Claude proposal context (read-only): [claude/bengal-earth-lab-20261029 — bel-config.json](https://github.com/i-m-r-a-n/Practice01/blob/claude/bengal-earth-lab-20261029/GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/viewer/bel-config.json). This proposal currently concentrates on Z01, Z02, Z03, Z30, Z08, Z12 and Z18; its visual/code work is Claude's, not duplicated here.
- Owners' supplied TEAM BRIEF (30 October): **no garden**; a few small trees/bonsai, stones, commissioned rural art and instrument displays; safety/origin proof required. It reports **5 east-facing external windows: 3 in Z18, 2 in Z23**, a **2.90 m** deck underside and existing walls/doors/windows kept. Window report has *not* been independently surveyed.
- Automated geometry audit of all polygon coordinates: **34 unique zones**, **45 named cameras** in option B, **1030.3 m²** summed nominal room area, **11,096 ft²** from individually rounded room labels, all polygon-derived areas within **0.050 m²** of stored nominal zone areas. Values are room polygons, not net free usable area, permitted capacity, floor-area-ratio or an occupancy certificate. Do not compare this model directly to a legal site survey.

### Area by existing group
| Group | Zones | Model area m² |
|---|---:|---:|
| Arrival & visitors | 4 | 103.4 |
| Experience & meeting | 3 | 130.0 |
| Executive suite | 4 | 81.0 |
| Workplace | 5 | 303.3 |
| Design development | 7 | 223.8 |
| Staff facilities | 4 | 120.0 |
| Prayer & wudu | 4 | 34.9 |
| Washrooms | 3 | 33.9 |
| **TOTAL** | **34** | **1030.3** |

## Capability matrix (concepts, not approvals)
| Zone | Existing room | Model m² | Priority | Proposed complementary role / decision |
|---|---|---:|---|---|
| Z01 | Entrance lobby | 47.8 | High | Arrival cultural introduction |
| Z02 | Reception & visitor waiting | 41.4 | High | Original Bengali-designed reception furniture and food-safe tea-service prototypes |
| Z03 | Visitor passage | 7.0 | High | Wall-mounted evidence-led solar story, no planter obstruction |
| Z28 | Guest WCs | 7.2 | Low | Material palette/cleaning upgrade only |
| Z08 | Boardroom | 50.1 | High | Buyer review, prototype trays and document-backed negotiation |
| Z09 | Audit room | 14.2 | Low | No visitor route; possible non-sensitive material details only |
| Z30 | Experience centre | 65.7 | High | Main buyer showroom, rural craft-to-product explanation, QR catalogue |
| Z10 | Executive reception | 20.7 | Low | Subtle artist commission if appropriate |
| Z11 | Director | 19.0 | Low | Culturally inspired furniture details only |
| Z12 | Managing Director | 27.8 | Medium | Curated buyer samples in agreed meeting mode |
| Z13 | Executive corridor | 13.5 | Low | Wall-based craft education only if no projections |
| Z04 | Guest workspace | 17.1 | Low | Occasional product specification work, not public teaching |
| Z05 | HR & admin | 28.0 | Low | No public display or class in operating hours |
| Z06 | Commercial & accounts | 119.2 | Conditional | Owner brief suggests academy+artisan studio as separate conditional reuse ONLY |
| Z07 | Merchandising | 132.0 | Conditional | Owner brief suggests Green Uthan+showroom as separate conditional reuse ONLY |
| Z31 | Staff corridor | 7.0 | Low | No free-standing display |
| Z14 | CAD / technical design | 26.1 | Medium | Digital craft specifications and original furniture CAD workflow |
| Z15 | Fabric & trim library | 18.8 | High | Material passport/swatch evidence centre |
| Z16 | 3D printing lab | 15.9 | Low | Prototype tooling only after process review; no uncontrolled public demonstration or soil |
| Z17 | Sample development | 25.2 | High | Prototype/QA workflow; supervised demonstration only where safe |
| Z18 | Global Design Studio | 87.0 | High | Collaborative design and training demonstration; small validated light-compatible plants |
| Z19 | Sample & material store | 12.5 | Low | Barcode/traceability operations; not a new exhibit |
| Z22 | Design-wing corridor | 38.3 | Medium | Secure wall-mounted rural instrument interpretation only if clearance permits |
| Z20 | Staff cafe & pantry | 43.2 | Medium | Food-safe wood/clay tableware pilot subject to applicable tests; a few maintainable plants |
| Z21 | Staff lounge / training | 36.1 | High | Small-class pilot; larger academy requires seating/egress survey or another room |
| Z32 | North corridor | 25.1 | Low | Do not use as storage or planting overflow |
| Z33 | Hallway | 15.6 | Low | Flush wall story if permitted |
| Z23 | Prayer room (male) | 17.3 | Protect | No repurposing; any greenery should be outside worship clearances |
| Z24 | Wudu (male) | 7.0 | Protect | No soil/standing planters beside ablution |
| Z25 | Prayer room (female) | 8.1 | Protect | No repurposing |
| Z34 | Wudu (female) | 2.5 | Protect | No additional furnishing |
| Z26 | Washroom (female) | 12.1 | Protect | No public exhibition or storage |
| Z27 | Washroom (male) | 17.5 | Protect | No public exhibition or storage |
| Z29 | Guest workspace WC | 4.3 | Protect | No public exhibition or storage |

The editable machine-readable companion [ROOM_AUDIT_34.csv](ROOM_AUDIT_34.csv) preserves the exact per-zone model area, independently calculated polygon area, model centroid, floor-polygon vertex count, camera, current-use protection and proposed role.

## Five spatial findings that change the plan

**1. There is no obvious empty academy room.** Z21 is already a 36.1 m² staff lounge/training room with a six-seat workshop table. It is the logical **small-class pilot**, not proof it can safely seat 20–30 people. A hypothetical 20 learners would leave 1.81 m² gross each and 30 learners 1.20 m² gross each **before** furniture, teaching space, storage and circulation. These ratios are only simple geometry, not occupancy/code or comfort limits. Require a counted furniture plan, seating mock-up and qualified egress/access review.

**2. Z06 (119.2 m²) and Z07 (132.0 m²) are not free space.** Z06 contains a 12-desk finance suite plus sensitive records; Z07 contains 16 merchandising desks plus sample development/approval functions. Claude's option B measured route and storage improvements remain a protected, unapproved alternative. Replacing either with the owner's suggested academy/Green Uthan requires a relocation ledger identifying **every desk, record cabinet, sample rack, HVAC/service constraint, and affected workflow** before any claim of extra usable area. Create a separate scenario; do not overwrite the existing option B.

**3. The showroom already has an anchor.** Z30 is 65.7 m² with four garment display bays; use these with a coherent rural-craft-to-commercial-product display rather than inventing a second large dedicated showroom. Z15 (18.8 m²) is the existing material library, Z17 (25.2 m²) is sample development and Z19 (12.5 m²) is storage. Public access to technical/restricted rooms is subject to physical-route and process-safety verification.

**4. Natural daylight is concentrated.** Per the supplied brief, the only east-façade windows are **3 in Z18** (87.0 m²) and **2 in Z23** (17.3 m², prayer). Respect worship use; do not repurpose it for nursery-like planting. All other rooms need a realistic horticultural test before promising living trees. Limit interior planting to a few protectively located small specimens where light and maintenance work; otherwise use earth finishes, stones, artist-made objects, and views. No large internal garden or blanket claims that plants purify air.

**5. Buyer wayfinding can stay separate from sensitive work.** Candidate sequence: Z01 lobby → Z02 reception → Z03 visitor passage → Z30 experience centre → Z08 buyer discussion. A separate **escorted** visit to Z18 may be possible but requires actual door, access, adjacency, live-operation and route checks. Do not direct visitors through Z06 finance, Z09 audit, storage, labs, prayer rooms, HR or sensitive operations by default. Existing model centroids/adjacent polygons alone do not prove a traversable route.

## Three programme scenarios to take to Claude

| Scenario | Space change | Usable now? | Unresolved gate |
|---|---|---|---|
| **A — Protected functions first** | Z21 remains six-place workshop; Z30 takes curated product displays, Z15 swatch origin, Z18 private co-design; no partitions moved | **Lowest-disruption proposal**, not an approved event layout | Confirm actual staff schedule, furniture clearance and safe visitor transitions |
| **B — Larger academy within floor** | Study Z06 119.2 m² as academy / artisan demonstration in a separate option | **Not yet feasible to approve** | New secured home for 12 finance desks, manager, archive, document flow, fire/MEP and independent circulation |
| **C — Buyer gallery / Green Uthan** | Study Z07 132.0 m² as culture/showroom in a separate option | **Not yet feasible to approve** | Relocate 16 merch desks, sample hub/rails, buyer approval, dispatch, storage, equipment and workflow |

A class-of-20–30 aspiration should **not** be advertised as an approved class capacity under any scenario.

## Material, plant, and visitor display rules from owner's latest brief

- **No garden.** A few high-quality bonsai or small trees, selected stones, traditional instrument displays (ektara, dotara, dhol, banshi, etc.), rural commissioned art and small plants where safe. Do not imply a local-origin or community-authorized craft until verified.
- Every specimen or installation gets a location, photo, dimensions/weight, light conditions, maintenance owner, drip protection and clearance check. Electrical panels, emergency routes and sensitive sample/print/steam zones are excluded from uncontrolled soil or watering.
- Food-contact wood/clay cups and plates require appropriate food-contact tests; do not claim glaze safety, drinkability or certification without independent records.
- Chittagong Hill Tracts (Chakma, Marma and other communities): only consent-based collaboration with paid and credited makers; never replicate restricted/sacred designs as decorative motifs.
- Solar display: **“Designed for a Solar-Powered Future”**, with no implied live readings until generation, demand, battery, grid and backup evidence is available.

## Handoff questions for Claude / design engineers

1. For the owner's **new** proposed reallocation of Z06 and Z07, where will the **12 finance** and **16 merchandising** desks plus secure records/sample storage go? Is this expressly an alternative rather than a replacement?
2. Can Z21's existing 6-seat training layout support two smaller consecutive classes without displacing staff lounge use? What are actual clearances, equipment and schedule?
3. Which rooms are genuinely open to visiting buyers, and where are the controlled door points to Z18?
4. What are verified light levels at each potential plant position, given only 5 reported east exterior windows?
5. Are structural/MEP/fire services and equipment clearances preserved for any new display or wall-mounted musical instrument?
6. Can the 3D team provide **a layout-difference schedule and matched-camera views** for any proposed relocation instead of replacing baseline silently?

**Release discipline:** no architectural approval, no official 3D amendment, no live Worker changes. No budget, local manufacturer, plant species, PV generation or buyer demand invented.

### Reproduction
Read the pinned metadata JSON, enumerate its `rooms` array, compute polygon area with the shoelace formula on `polygon_xz`, and compare with `area_m2`; this document's gate is unique 34 zone IDs and each difference ≤0.05 m². All 34 met the gate in the current metadata. Footprints may still be unsuitable for furniture or accessible routes despite area matching.
