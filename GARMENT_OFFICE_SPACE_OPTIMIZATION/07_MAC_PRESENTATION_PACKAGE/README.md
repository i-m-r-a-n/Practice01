# STAGE II — Mac presentation package

**Drive folder:** Imran — Main Folder / STAGE II — Mac Presentation Package (28 Oct 2026)
https://drive.google.com/drive/folders/1D3st0KTuLJ97miG_tyGa4-fS5VV1mBEu

There are 130 files, 453 MB in total. Every file is pinned to an exact commit in `i-m-r-a-n/Practice01` and checked by SHA-256 (`manifest.csv`).

## Folders

| Folder | Contents |
|---|---|
| `01_VIDEOS` | Cinematic opening video (77 s) and complete floor tour (2:01), 1080p plus light 720p copies |
| `02_PRESENTATION` | 18-slide design pitch (PDF + editable PPTX), render book (PDF), 2-page run-of-show PDF, guides |
| `03_3D_TOUR_MAC` | `Ground_Floor_3D_Tour_Mac.zip`: interactive 3D tour of the whole floor, offline. `Realistic_6_Rooms/`: offline realistic tour of Reception, Boardroom, Experience Centre, MD Office, Merchandising and Design Studio, with illustrative people |
| `04_RENDERS` | 38 Cycles renders (JPG + PNG), contact sheet, material board, the 4 plans (PDF + PNG) |
| `05_Z06_Z07_REDESIGN` | Merchandising / Commercial & Accounts concept redesign: plans original / A / B / C, before / after renders, renders with people |
| `06_EDITABLE_MODEL` | Approved Blender model (unchanged) and the Z06 / Z07 option B model |

## On the Mac

**Before the meeting:**
- Copy the whole folder from Drive to the Mac (Downloads), so nothing depends on the internet.
- Install Firefox.

**Videos and PDFs:** double-click; they open in QuickTime and Preview.

**3D tour:**
1. Unzip `Ground_Floor_3D_Tour_Mac.zip`.
2. Right-click `Ground_Floor_3D_Tour.html` → Open With → Firefox.

**Realistic 6 rooms:**
1. Unzip `Design_Studio_Realistic_Offline.zip`.
2. Open `Design_Studio_Realistic_Offline/Office_Realistic_Tour.html` in Firefox.
3. Keep all the extracted files together.

**Backup online:**
- https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/ (launcher: `/present`)
- https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/realistic/

## Status, not to be overstated

- This is a concept proposal. Final dimensions and technical details are subject to site verification. No engineering or authority approval is implied.
- The Z06 / Z07 redesign is a proposal for those two rooms only. It is not an approved redesign of the whole office.
- People in the renders and tours are illustrative.
- Not tested on a MacBook itself (frame rate, file opening). Tested in Firefox 159 and Chromium on Linux.

## Getting the files

- **From Drive:** download the Drive folder.
- **Straight from GitHub:** put `manifest.csv` and a script in one folder, then run it. It downloads everything into `STAGE_II_Presentation/` and checks each SHA-256. If you run it again, it skips the files that are already correct.
  - Mac: `sh get_package_mac.sh`. Tested on Linux: 130 / 130 files downloaded, all hashes matched.
  - Windows: `powershell -ExecutionPolicy Bypass -File .\get_package_windows.ps1`. Not run here; no PowerShell in this environment.
