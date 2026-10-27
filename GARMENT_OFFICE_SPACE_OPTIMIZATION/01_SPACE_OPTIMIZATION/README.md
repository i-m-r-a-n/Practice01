# 01 Space optimisation: Z07 Merchandising and Z06 Commercial & Accounts

**Status: proposed revised concept.** This changes only two departments. It is not an approved redesign of the office.
Every figure on this page comes from the project's own source data, measured by `analyze_space.py` on a 1-inch grid. No new site measurements were taken. The sources are:

- `survey.py` (walls, columns, doors)
- `office_layout.py` (zones, AC units)
- `z06_z07_options.py` (furniture layouts)

Raw output is in `metrics.json`. Plans are drawn to scale (1 in = 1 SVG unit), north up: `plan_original` / `plan_A` / `plan_B` / `plan_C` (.svg / .png).

Column positions are estimated from photos (PHOTO-EST). The architect / engineer must verify on site:

- dimensions
- egress
- accessibility
- HVAC, electrical and fire

The width checks below are planning targets only. They are not a statement of code compliance.

## 1. Audit of the existing layout

### Areas

| | Z07 Merchandising | Z06 Commercial & Accounts |
|---|---|---|
| Polygon (model) | 499 x 410 in rectangle | 316 x 509 in, minus the audit-room notch, plus two 151 in legs |
| Gross area | **1,420.8 sft** | **1,282.7 sft** |
| Columns inside | 0 (two sit in the walls) | 3 (x 300 line: y -423, -633, -843) |
| Ceiling AC positions (kept in every option) | 4: (490, -666) (740, -666) (490, -528) (740, -528) | 2: (170, -560) (170, -400) |

**1,421 vs 1,431 sft.** The area label in the owner's screenshot is partly hidden by the column symbol. The model computes 1,420.8 sft from 499 x 410 in (room 6 width measured 499 in; depth 410 in, between the hallway half wall and the display wall). Reaching 1,431 sft would take about 3 in more depth (0.7 %). That is within the survey tolerance, but it should be checked against the native drawing. No conclusion here depends on that difference.

### What the original layout actually does

**Merchandising (Z07)**
- 16 bench desks and an 8-seat team table.
- One 270 in review counter, lockers, low storage under the two windows.
- Storage: **48 lin ft / 207 cu ft**.
- The D11 hallway opening to the D49 experience-centre door is the main route. Its narrowest point is **47 in**.
- There is no sample inspection place, no rail, no buyer review screen and no lockable sample storage. Sample work happens on desks.

**Commercial & Accounts (Z06)**
- 12 bench desks, a manager desk with 2 visitor chairs, one 120 in filing unit and a printer.
- Storage: **10 lin ft / 58 cu ft** for a finance department.

**Key finding:** Z06 is also the **public route** to:
- both washrooms (D08, D09)
- the female prayer room (D22)
- the audit room (D31)
- the hallway

Every visitor to the washrooms walks past the accountants' screens and papers. In the original layout that route is only **41 in** at its narrowest. The ends of the benches and the lobby planter pinch it.

**Is the space wasted?** By floor area per workstation, no. Both rooms already sit at 89 sft (Z07) and 98 sft (Z06) of net floor per workstation, including all circulation. What is missing is **work functions and storage**. The rooms are desks and walkways only, which is exactly the owner's "all I see is chairs and tables". The fix is a better function mix, not more desks.

## 2. Three alternatives (plans to scale: `plan_A.png`, `plan_B.png`, `plan_C.png`)

- **A, operational efficiency.** Open plan, no new partitions.
  - Z07: 20 desks (16 + 4 touchdown), a 6-seat team table, the long review counter, more storage.
  - Z06: 16 desks (12 + 4 growth) on 1200 mm desks, a manager desk, records filing on the east half wall, a processing counter.
- **B, balanced premium (selected).**
  - Z07: 16 desks west of the column line and a sample hub east of it. The hub has an inspection island, 2 rolling rails, 2 dress forms with a fitting mirror, a buyer review table with a 65 in screen, a T&A dashboard, lockable sample storage, a trim / colour approval wall and a dispatch counter.
  - Z06: an accounts suite behind privacy glass with 12 desks and a manager desk, a document processing counter with scanner and printer, lockable records filing, a finance discussion room and an archive cabinet. A 60 in public corridor runs outside the suite.
- **C, flexible growth.**
  - Z07: 16 desks on mobile benches; 4 flip-top tables that serve as 8 meeting seats or 8 growth desks.
  - Z06: mobile benches, one privacy screen to the corridor, a flexible table that can take 4 growth desks.

### Comparison (measured)

**Z07 Merchandising (gross 1,420.8 sft)**

| | Original | A | **B** | C |
|---|---|---|---|---|
| Workstations | 16 | 20 | **16** | 16 (+8 growth possible) |
| Other seats (team / review) | 8 | 6 | **6** + 4 standing places at the island | 8 |
| Dedicated work functions (beyond desks) | 1 (review counter) | 3 | **8** | 3 |
| Storage, linear / volume | 48 ft / 207 cu ft | 72 ft / 338 cu ft | **66 ft / 381 cu ft** | 61 ft / 351 cu ft |
| Main route D11 - D49, narrowest | 47 in | 67 in | **67 in** | 67 in |
| Seat access, narrowest | 47 in | 47 in | **41 in** | 37 in |
| Net floor per workstation | 89 sft | 71 sft | **89 sft** | 89 sft |

**Z06 Commercial & Accounts (gross 1,282.7 sft)**

| | Original | A | **B** | C |
|---|---|---|---|---|
| Workstations | 12 + manager | 16 + manager | **12 + manager** | 12 + manager (+4 growth) |
| Confidential discussion seats | 2 (visitor chairs at the manager desk) | 0 | **4** (glass room) | 2 |
| Storage, linear / volume | 10 ft / 58 cu ft | 42 ft / 243 cu ft | **42 ft / 283 cu ft** | 32 ft / 185 cu ft |
| Public route to washrooms / prayer, narrowest | **41 in** | 49 in | **49 in**, outside the finance area | 49 in |
| Staff corridor to hallway | 47 in | 57 in | **49 in** | 53 in |
| Finance work separated from the public route | no | no | **yes** (privacy glass 30-72 in frosted) | partly (one screen) |
| New partitions | none | none | 6 glazed screens, 3 doors (D50 42 in, D51 42 in, D52 40 in sliding) | 1 screen |

Door approach zones (D08, D09, D22, D31, staff corridor) and the D49 door swing are clear in every option. No item collides with another or with a column.

### Why B

- **A** adds desks the brief did not ask for (headcount is an assumption). It is still "rows of desks" and does nothing for the finance room's confidentiality.
- **C** keeps open floor for growth that has not been confirmed.
- **B** keeps the confirmed capacity (16 / 12 + manager). It then turns the floor that was only walkway into the work merchandising and accounts actually do:
  - sample inspection, review and dispatch, in the order samples come from the hallway / sample development (D11) and go to the experience centre (D49)
  - document intake, processing, approval, filing and archive in accounts

  It also takes the public washroom route out of the finance work area.
- **Construction scope for B:**
  - furniture, joinery and six glazed non-structural screens
  - no change to the shell, columns, beams, existing doors, AC positions or fire equipment
  - lighting is re-laid with the same fixture family
- **Trade-offs:**
  - the 4 discussion-room seats have 33 in seat access (a meeting room, not a route)
  - the Z06 hallway route narrows from 57 in (A) to 49 in, still above the 48 in target
  - frosted glass reduces through-views

## 3. Selected design: B

See `plan_B.png`. The layout data is `../02_IMPROVED_BLENDER_MODEL/scripts/z06_z07_options.py` (`option_b`), the same data that builds the Blender model.

**Z07**
- Benches 2 x (2 x 4), 1400 x 700 mm desks, centred at x 489, y -724.5 / -609.5.
- The column (616, -633) sits beside the end of the second bench, not in an aisle.
- Spine x 780-848 between D11 and D49.

**Z06**
- Suite x 109-362, y -687 to -231/-290.
- Public corridor x 46-106 (60 in) and y -740 to -690 (50 in).
- Discussion room x 260-362, y -335 to -231 (about 74 sft).
- Archive cabinet against the audit-room wall in the hallway bay.

Measurements are in plan inches, x east, y south (the project's survey system). The plans carry a 10 ft scale bar.
