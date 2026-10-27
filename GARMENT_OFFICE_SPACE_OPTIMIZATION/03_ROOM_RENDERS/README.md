# 03 Realistic room renders (Cycles, proposed option B)

These are photorealistic Blender renders (still images), made with the same "final" preset as the approved renders: 1600 x 900, 128 samples, AgX, denoised. Rendering used CPU Cycles at about 6.5 min per view.

| Folder | Content |
|---|---|
| `after_with_people/` | 8 eye-level views with illustrative staff: Merchandising CAM_11, CAM_12, CAM_34 sample hub, CAM_35 desks; Accounts CAM_16, CAM_36 suite, CAM_37 records + discussion room, CAM_38 public corridor |
| `after_no_people/` | matched before / after views (CAM_11, CAM_12, CAM_16), plus a top view and a cutaway of both departments |
| `comparisons/` | `before_after_CAM_xx.jpg`: same saved camera and settings, approved design vs option B, with and without people; `contact_sheet.jpg` |

- The "before" images are the approved renders in `GARMENT_OFFICE_FINAL_PRESENTATION/02_RENDERED_IMAGES/final/`, unchanged.
- People shown are illustrative (fictional CC0 characters, see `../02_IMPROVED_BLENDER_MODEL/README.md`).
- Props carry no text, logos or real records.
- PNG masters are git-ignored; the JPGs are the delivery files.
- Re-run: `../02_IMPROVED_BLENDER_MODEL/scripts/render_all.sh`, then `python3 -I make_comparisons.py`.
