# Rendered images

All images are Blender Cycles renders of this project's model (`01_EDITABLE_3D/Final_Office_Interior.blend`), except the
drawings in `plans/`, which are drawn from the same survey and layout data. Nothing here is a stock or AI-generated image.

| Folder | Contents |
|---|---|
| `final/` | final renders: PNG (lossless) + JPG copy; `render_log.csv` has the time of each render |
| `previews/` | 960 x 540 preview renders of the 33 interior views |
| `plans/` | drawings ID-01 to ID-04 (SVG, PNG, A3 PDF) |
| `material_board.jpg` | the model's PBR materials rendered in Blender |
| `BENCHMARK_Reception_1600x900_128spp_381s.jpg` | render-time benchmark (reception, 1600 x 900, 128 samples, 381.5 s) |
| `final_contact_sheet.jpg` | all final renders on one sheet |

Final renders: 6 of 38 views, total render time 0.6 h on 4 CPU cores. Views without a final render have a preview only.

| Camera | Room / view | Priority | Final render | Preview |
|---|---|---|---|---|
| `CAM_01_Reception_A` | Reception | 1 | 1600x900, 128 samples, 409 s | yes |
| `CAM_02_Reception_B` | Reception | 1 | - | yes |
| `CAM_03_Entrance_Lobby` | Entrance lobby | 1 | - | yes |
| `CAM_04_Experience_Centre_A` | Experience centre | 1 | 1600x900, 128 samples, 438 s | yes |
| `CAM_05_Experience_Centre_B` | Experience centre | 1 | - | yes |
| `CAM_06_Experience_Centre_Detail` | Experience centre | 1 | - | yes |
| `CAM_07_MD_Office_A` | MD office | 1 | 1600x900, 128 samples, 354 s | yes |
| `CAM_08_MD_Office_B` | MD office | 1 | - | yes |
| `CAM_09_Boardroom_A` | Boardroom | 1 | 1600x900, 128 samples, 408 s | yes |
| `CAM_10_Boardroom_B` | Boardroom | 1 | - | yes |
| `CAM_11_Merchandising_A` | Merchandising (open office) | 1 | 1600x900, 128 samples, 385 s | yes |
| `CAM_12_Merchandising_B` | Merchandising (open office) | 1 | - | yes |
| `CAM_13_Design_Studio_A` | Global Design Studio | 1 | - | yes |
| `CAM_14_Design_Studio_B` | Global Design Studio | 1 | - | yes |
| `CAM_15_CAD_Room` | CAD / technical design | 1 | - | yes |
| `CAM_16_Commercial_Accounts` | Commercial & accounts | 1 | - | yes |
| `CAM_17_Executive_Reception` | Executive reception (PA) | 2 | - | yes |
| `CAM_18_Director` | Director | 2 | - | yes |
| `CAM_19_HR_Admin` | HR & admin | 2 | - | yes |
| `CAM_20_Staff_Cafe` | Staff cafe + pantry | 2 | - | yes |
| `CAM_21_Lounge_Training` | Staff lounge / training | 2 | - | yes |
| `CAM_22_Prayer_Male` | Prayer (male) | 2 | - | yes |
| `CAM_23_Sample_Room` | Sample development | 2 | - | yes |
| `CAM_24_3D_Printing_Lab` | 3D printing lab | 2 | - | yes |
| `CAM_25_Fabric_Library` | Fabric, colour & trim library | 2 | - | yes |
| `CAM_26_Guest_Workspace` | Guest workspace | 2 | - | yes |
| `CAM_27_Audit_Room` | Audit room | 2 | - | yes |
| `CAM_28_Washroom_Male` | Washroom (male) | 2 | - | yes |
| `CAM_29_Washroom_Female` | Washroom (female) | 2 | - | yes |
| `CAM_30_Prayer_Female` | Prayer (female) | 2 | - | yes |
| `CAM_31_Executive_Corridor` | Executive corridor | 2 | - | yes |
| `CAM_32_Design_Corridor` | Corridor (design wing) | 2 | - | yes |
| `CAM_33_Wudu_Male` | Wudu (male) | 2 | - | yes |
| `CAM_TOP_Plan` | Whole floor | 1 | - | - |
| `CAM_ISO_SE` | Whole floor | 1 | 1920x1080, 96 samples, 249 s | - |
| `CAM_ISO_SW` | Whole floor | 1 | - | - |
| `CAM_ISO_Front_Zone` | Visitor zone (lobby, reception, experience centre, boardroom, executive suite) | 1 | - | - |
| `CAM_ISO_Design_Wing` | Design development wing + staff support | 1 | - | - |

## Drawings (`plans/`)

- `ID-01_furnished_plan` (.svg / .png / A3 .pdf)
- `ID-02_zoning_plan` (.svg / .png / A3 .pdf)
- `ID-03_ceiling_lighting_plan` (.svg / .png / A3 .pdf)
- `ID-04_power_data_fire_plan` (.svg / .png / A3 .pdf)
