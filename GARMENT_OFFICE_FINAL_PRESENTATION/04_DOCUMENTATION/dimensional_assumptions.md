# Dimensional assumptions and provisional values

Source of all measured values: the client's hand-measured site sketches (overview + rooms 4, 5, 6, 7, 8) and site photos. Values below were NOT directly measured (or were measured inconsistently) and are used provisionally in the model. Each one is a single parameter in `01_EDITABLE_3D/scripts/survey.py`; change it there and rebuild.

| id | element | written on sketch | value used | status | basis / note |
|---|---|---|---|---|---|
| R1D | Room 1: Depth | 236 (room 1 sketch) / 249 (room 3 sketch) | 247 in (6,274 mm) | RESOLVED | Survey reconstruction - front-row line shared with rooms 3 and 4 |
| R3W | Room 3: Width | 255 / 265 | 260 in (6,604 mm) | RESOLVED | Room 3 sketch - mean of the two sides |
| R3D | Room 3: Depth | 247 - 249 | 247 in (6,274 mm) | RESOLVED | Room 3 sketch |
| R4D | Room 4: Depth | 244 / 242.5 (7.5 + 60 + 175) | 247 in (6,274 mm) | RESOLVED | Room 4 sketch - drawn on the front-row line, 3 - 4.5" over the measured depth |
| R5W | Room 5: Width | 499 (49 + 450) / 504 | 499 in (12,675 mm) | RESOLVED | Room 5 sketch - aligned with room 6 |
| R7WU | Room 7: Width, upper part | 234 (written) | 316 in (8,026 mm) | RESOLVED | Room 7 sketch - 252 + 64" jog; 234 does not fit the hallway (504) and rooms 5 / 6 (499) |
| STW | Washroom row: Width | not measured | 96 in (2,438 mm) | ASSUMED | Survey reconstruction - outer wall in line with room 2 |
| STL | Washroom row: Length | 160 + 30 + 174 + 30 + 134 + 64 + 57 = 649 | 660 in (16,764 mm) | RESOLVED | Room 7 sketch - 11" added to the first piece |
| R8W | Room 8: Width | not measured | 450 in (11,430 mm) | ASSUMED | Survey reconstruction - north-east stair 273 + 5 + 172 |
| NESD | North-east stair: Depth | not measured | 103 in (2,616 mm) | ASSUMED | Survey reconstruction - east wall 1538 minus measured pieces = depth + 2 piers |
| R8G1 | Room 8: Wall between windows 3 and 4 | not written | 86 in (2,184 mm) | ASSUMED | Survey reconstruction |
| R8G2 | Room 8: Wall between windows 4 and 5 | not written | 59 in (1,499 mm) | ASSUMED | Survey reconstruction |
| WT1 | Walls: Inside wall thickness | not measured | 5 in (127 mm) | ASSUMED | Survey reconstruction |
| WT2 | Walls: Outside wall and row wall thickness | not measured | 10 in (254 mm) | ASSUMED | Survey reconstruction |
| H01 | Heights: Floor to underside of steel deck | not measured | 114 in (2,896 mm) | PHOTO-EST | Site photos - 9'-6" |
| H02 | Heights: Door and window head (lintel level) | not measured | 84 in (2,134 mm) | STANDARD |  - 7'-0" |
| H03 | Heights: Main gate head | not measured | 96 in (2,438 mm) | PHOTO-EST | Site photos |
| H04 | Heights: Secondary beam depth below deck | not measured | 12 in (305 mm) | PHOTO-EST | Site photos |
| H05 | Heights: Main beam depth below deck | not measured | 16 in (406 mm) | PHOTO-EST | Site photos |
| H06 | Heights: Floor to floor (stair rise) | not measured | 118 in (2,997 mm) | ASSUMED |  - deck height + deck |
| H07 | Heights: Gate steps (2), heights | not measured | 14 in (356 mm) | PHOTO-EST | Site photos - 7" + 7", treads 12" and 24" |
| ST2 | Stairs: Stair tread | not measured | 11 in (279 mm) | STANDARD |  - risers = floor to floor / count |
| ST3 | Stairs: North-east and south-east stair layouts | not surveyed | 0  | ASSUMED |  - drawn as U-stairs inside the measured stair rooms |
| STR1 | Structure: Room 7 beam line | drawn on the room 7 sketch, not dimensioned | 300 in (7,620 mm) | PHOTO-EST | Room 7 sketch + photos - x position approximate |
| STR2 | Structure: Steel columns | seen in photos of rooms 5, 6, 7, 8 | 10 in (254 mm) | PHOTO-EST | Site photos - 11 columns at estimated positions; measure on site |
| STR3 | Structure: Main beams rooms 6 and 8, secondary beams | seen in photos | 72 in (1,829 mm) | PHOTO-EST | Site photos - secondaries at most 72" apart |

Status key: RESOLVED = sketches disagree, one value chosen (reason given); ASSUMED = not measured, common-sense value; PHOTO-EST = estimated from site photos; STANDARD = standard building dimension used.

Full measurement schedule (all values, incl. MEASURED and DERIVED): `01_EDITABLE_3D/phase1_shell_reference/dimension_schedule.csv`.
