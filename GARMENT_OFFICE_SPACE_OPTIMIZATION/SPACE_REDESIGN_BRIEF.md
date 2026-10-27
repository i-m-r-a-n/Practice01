# Stage II / Zara Fashion — Merchandising + Commercial & Accounts optimization directive

**Status:** Design-change request from the owner, 27 October 2026 (Asia/Dhaka). This is a **new design iteration**, not approval to overwrite the finished client-presentation build.

**Owner feedback, verbatim in meaning:** The Merchandising and Commercial & Accounts areas look disproportionately large and underused; the online 3D model looks dominated by chairs and tables. Improve functional use of floor area, garment-industry relevance, visual richness and presentation quality.

## 1. Authoritative input / what the owner actually provided

Two screenshots show:
- **Merchandising reflected ceiling plan:** approximately **1,431 sq ft** shown in the supplied screenshot (small annotation to be checked against native drawing), four blue **AC** cassette positions, a structural/ceiling grid, many closely spaced north-south baffles, and long linear luminaires.
- **Commercial & Accounts reflected ceiling plan:** **1,283 sq ft** shown, two blue AC cassettes, grid/structural markers and linear fixtures.

**These are reflected ceiling plans, NOT furniture/occupancy plans.** A screenshot alone is not proof that unused circulation is excessive. Determine true usable area using the native plan and furniture footprints.

Base source in `i-m-r-a-n/Practice01`:
- Original: `claude/magical-hopper-74q4xq`, `GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/Final_Office_Interior.blend`
- Editable design: `GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/scripts/office_layout.py`, `survey.py`, builder and camera scripts
- Latest geometry metadata: `claude/web-tour-assets`, `GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/office_web_metadata.json`
- Saved render cameras: **Z07** `CAM_11_Merchandising_A`, `CAM_12_Merchandising_B`; **Z06** `CAM_16_Commercial_Accounts`.

### Current source-reconciled programme

**Z07 Merchandising**
- Metadata says **1,421 sq ft** / 132.0 m², while owner's screenshot seems **1,431 sq ft**. **Reconcile against authoritative geometry; document the difference before claiming improved utilization.**
- Official model description: **16 bench workstations**, **8-seat team table**, sample-review counter with pinboard, lockers, under-window storage, felt baffles.
- Editable source places two 6-seat bench islands (`bench3`) and one 4-seat bench (`bench2`), plus `table_team`, `review_counter`, `pinboard_merch`, printer, lockers, window storage, plants.
- Four AC locations, `Z07`: (490,-666), (740,-666), (490,-528), (740,-528) **in original plan inches**. These are a modeling reference, **not an engineering-approved MEP design**.
- Connection through the display wall to experience centre `Z30`, proposed doorway `D49`. Preserve/use intelligently; do not block it.
- Adjacent dedicated functions already include **fabric and trim library Z15**, **sample development Z17**, **sample/material store Z19**, **experience centre Z30** and **Global Design Studio Z18**. Avoid redundant oversized copies of these departments.

**Z06 Commercial & Accounts**
- Official area **1,283 sq ft** / 119.2 m².
- Programme: **12 bench workstations plus manager desk**, filing/storage, multi-function printer and two visitor chairs.
- Two AC locations, `Z06`: (170,-560), (170,-400) plan inches.
- Irregular, notched polygon rather than a simple rectangle; respect geometry, actual structural obstacles and the adjacent **Audit room Z09 (153 sq ft)**.
- Retain confidentiality and accounting document security. Avoid overly open or exposed finance discussions.

Existing target workplace headcount (whole project, **assumption**, not confirmed staffing): around 54 total work seats across the full office including growth/guest positions. Do **not** convert this to an invented departmental requirement.

## 2. Design intent

**Make the spaces work like real garment-company departments, not office furniture catalogues.** Improve *usable function per square foot*, workflow, visual character, visitor impression and adaptability while keeping easy movement and realistic safety.

### Z07 — proposed functional mix

Evaluate and fit what the geometry supports rather than blindly adding all of these:
1. Ergonomic core merchandising team desks for current 16-seat requirement, ideally flexible modules and integrated cable management.
2. Garment sample-check / flat-lay inspection counter with clear top, nearby neatly labelled rolling sample rails and a full-length mirror.
3. Compact seasonal collection / buyer approval station: colorways, trim approvals, tech packs, sample review board, production milestones or generic time-and-action dashboard.
4. Short huddle / video-buyer-call setting with display, acoustically considerate placement; do **not** duplicate the major boardroom.
5. Selectively enclosed quiet call/focus position if feasible and acoustically justified.
6. Efficient lockable/sample storage along usable wall zones, organized by buyer/season/collection; retain practical handling route to Z30 and related Z15/Z17/Z19.
7. 1–3 garment sample mannequins/rails and coordinated fashion displays **with a work purpose**, not showroom-style excess.
8. Human-scale, believable active office props: labeled sample bags, folded knits, swatch binders, realistic print-outs, fabric rolls (in appropriate quantity), laptop/monitor work, sample tags. No fake confidential client orders or unapproved trademarks.

### Z06 — proposed functional mix

1. Preserve the *working capacity* of 12 staff workstations + manager unless documented workflow analysis supports an alternative.
2. Rationalize desk modules into neat efficient islands with clear circulation and daylight distribution.
3. Add a small confidential finance discussion / checking area or acoustic meeting nook (if area allows), not another oversized meeting room.
4. Create a distinct financial document workflow: in-tray / review / scanning / outgoing documents, a printer/copy zone, locked records cabinet, compact supply store.
5. Optional bank/import–export document-review counter and shared screen **only if functionally justified**.
6. Manager oversight without a visually dominant unused executive suite; appropriate partitions for sensitive finance work.
7. Realistic professional props: invoice folders, generic file labels, stationery, printer trays, well-managed cords and screens with placeholder/fictional dashboard data. **No actual financial documents, account numbers or client data.**
8. Avoid noise-generating or customer-facing functions beside confidential staff zones.

## 3. Three alternatives, then implement the strongest

Develop **three scaled furniture plans**:
- **A — Operational efficiency:** minimize unused floor area, maximize ergonomic workflow, stable seat count.
- **B — Balanced premium (preferred starting point):** efficient seating + sample/finance activity areas + sophisticated visual presentation.
- **C — Flexible growth:** modular rearrangeable benches + multipurpose review/meeting area + documented additional capacity *only if real clearances allow*.

Compare each with the original on:
- Gross zone area, deductions for built-in or immovable obstacles, **net usable area**, furniture footprint, genuinely free functional floor, circulation and accessibility.
- Current vs proposed **staff seats**, team/huddle seats, dedicated functional areas, storage count/volume and key workflow distances.
- Doors, clear paths, turning/accessibility, column/beam interferences, light and AC positions, comfort/acoustics, power/data distribution.
- Estimated scope complexity (reuse vs new partitioning vs major MEP works).
- Source of every dimension; mark site-unverified constraints.

Select the best compromise based on evidence, document tradeoffs and **implement the chosen concept as a separate version**, without waiting for repeated owner clarification. If staffing targets are unknown, explicitly present the assumed counts and adjustable layout.

## 4. Respect hard boundaries

- Keep existing shell, columns, beams, structural walls, stairs, wet services, exterior doors/windows and approved routes. Do not change load-bearing or fire-safety elements.
- Preserve zone identities **Z06** and **Z07** and neighboring departments and intended Z30 connection. Proposed non-structural partitions may change only with clear drawings and change log.
- Respect all four Z07 and both Z06 ceiling AC positions as baseline coordination constraints; do not move them without a separately marked MEP redesign and engineering approval.
- Show any changes to the baffle/linear lighting RCP and ceiling/camera sightlines and avoid obstructing detectors, fire equipment and clear airflows.
- Never maximize seats at the expense of healthy desk ergonomics, unobstructed escape routes, accessibility, daylight, indoor air quality or honest space planning.
- Prior to construction, an architect/engineer should verify dimensions, accessibility, egress, HVAC, electrical, fire, and local authority requirements. Do not invent legal compliance.

## 5. 3D model must feel like an occupied, functioning fashion office

The owner says **"all I see is chairs and tables"**. Solve that in *both* layout and visualization:
- Replace generic rows with convincing zones: fabric/swatches, sample racks, working displays, collaborative moments, storage, document processing, acoustic details, signage and ergonomic accessories.
- Model proper material choices: warm wood, subtle deep green, black slim aluminum/glass, acoustics, clean workstation joinery and tactile textiles while maintaining existing corporate visual identity.
- In **Cycles hero renders**, show a small number of believable staff engaged in real tasks (reviewing garments, discussing tech packs, accounting), natural daylight/interior illumination and everyday office use. Keep people unobtrusive and avoid blocking the layout.
- In **GLB/WebGL**, use optimized static people/props only if they do not damage performance; keep a people on/off toggle if feasible. Do not conflate photoreal staged Cycles renders with real-time 3D.
- Photographically compose at least **3 perspectives of each zone**, including standing eye height and a floor-plan/cutaway. Show the actual functional layouts, not artificially staged empty corners.
- Use same-source cameras for **before/after** (`CAM_11`, `CAM_12`, `CAM_16`) and at least 1 extra view showing new functions clearly.

## 6. Required deliverables / acceptance

Create **new** `GARMENT_OFFICE_SPACE_OPTIMIZATION/` folder and a **new Claude branch**. Never overwrite `claude/magical-hopper-74q4xq`, `GARMENT_OFFICE_FINAL_PRESENTATION/`, or the currently working live Worker.

1. `01_AUDIT/`: dimension cross-check (including 1,421 vs screenshot 1,431 issue), existing furniture/walls/columns/AC/doors annotated, utilization and workflow findings.
2. `02_LAYOUT_OPTIONS/`: properly scaled 2D plan **A/B/C** per zone, workstation/functional-area counts, circulation overlays; user-friendly comparative summary.
3. `03_SELECTED_DESIGN/`: chosen option with Blender editable .blend, reproducible layout script changes, named props and an updated 2D marked-up plan; label as **proposed revised concept**.
4. `04_RENDERED_IMAGES/`: photorealistic Cycles before/after matched-camera views, additional lived-in perspectives and a concise contact sheet.
5. `05_WEB_MODEL/`: web-optimized GLB and camera metadata; prevent regression of known interleaved vertex-colour geometry corruption; check interactive view and ceilings.
6. `06_QA_AND_HANDOFF/`: room/area and seat schedules, workflow gains, model/scene before-after screenshots, changed quantities, measured clear paths where source supports them, known unknowns, GitHub SHA, exact files GPT needs for integration.
7. Optional: concise **client change-presentation** showing the original vs improved two zones and why the new proposal is operationally superior.

**Do not represent a redesign of only Z06/Z07 as an approved redesign of the entire corporate office.** Do not promise that new furniture creates additional usable area without the audited floor plan.

### Workflow / release coordination

- Claude owns architecture/Blender/layout alternatives + approved proposal assets.
- GPT owns independent QA + integrating approved assets with the 3D website and Cloudflare.
- Post commit and before/after evidence on the designated GitHub issue; cross-reference shared integration issue #12.
- Preserve and do not alter the previously delivered cinematic videos, 18-slide pitch, render book or live client-presentation launch page unless a new revision is explicitly selected for integration.

**Success means: a measurable more practical office layout, a distinctive garment-workplace 3D environment, realistic Cycles renders and a safe separate editable asset set—not merely more desks.**
