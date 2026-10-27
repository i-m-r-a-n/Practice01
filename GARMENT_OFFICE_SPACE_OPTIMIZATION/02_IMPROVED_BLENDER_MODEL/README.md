# 02 Improved Blender model (proposed revised concept, Z06 / Z07 option B)

`Optimized_Office_Interior.blend` is a **separate** editable model. It contains the approved design with only Z07 Merchandising and Z06 Commercial & Accounts replaced by option B (see `../01_SPACE_OPTIMIZATION/`).

The approved master `GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/Final_Office_Interior.blend` is not modified. Neither are its scripts, renders, videos and PDFs, or the original branch `claude/magical-hopper-74q4xq`.

## Rebuild

```
cd GARMENT_OFFICE_SPACE_OPTIMIZATION/02_IMPROVED_BLENDER_MODEL
blender -b --factory-startup --python scripts/build_model.py -- .        # -> Optimized_Office_Interior.blend (+ .glb, full size)
```

The scripts are a copy of the approved builder. The textures and CC0 models are read from the approved `assets/` folder (shared, read-only, nothing duplicated).

## Changes against the approved scripts

| File | Change |
|---|---|
| `scripts/z06_z07_options.py` | **New.** Layouts original / A / B / C in the placement format, new asset definitions, partitions |
| `scripts/office_layout.py` | Appended block: removes the original Z06 / Z07 placements and lights, adds option B placements, props, 6 glazed privacy screens (NP34-NP39), doors D50-D52, zone labels and the re-laid lights. Set `OFFICE_LAYOUT_ORIGINAL=1` for the original data |
| `scripts/lib_assets.py` | New builders: `inspection_table`, `rolling_rail`, `mirror_panel`, `screen_stand`, and props (`bench_props`, `counter_props`, `folded_garment`, `binder`, `swatch_fan`, `sample_bag`, `doc_tray`, `lever_files`, `calculator`, `laptop`, `carton`, `mug`). Props carry **no text, logos or numbers**: no invented records, orders or brands |
| `scripts/build_model.py` | Output name `Optimized_Office_Interior`; privacy glass (frosted 30-72 in band); desk plants also on the new benches |
| `scripts/cameras.py` | New cameras: CAM_34 sample hub, CAM_35 merchandising desks, CAM_36 accounts suite, CAM_37 records + discussion room, CAM_38 public corridor, CAM_TOP / CAM_ISO_Z06_Z07. The saved cameras CAM_11, CAM_12 and CAM_16 are unchanged, for matched before / after |
| `scripts/render_views.py` | Frame for the Z06 / Z07 plan camera |
| `scripts/place_people.py` | **New.** Render-time illustrative staff (see below) |
| `scripts/web/` | Web pipeline copies: metadata export, walk map, light bake, web GLB. Paths point to this model |

**Unchanged:**
- shell, columns, beams, existing walls and doors
- the four Z07 and two Z06 AC positions
- smoke detectors
- fire extinguishers (the original lobby planter in Z06 was removed because it narrowed the washroom route to 37 in)

## People in the renders (illustrative)

`place_people.py` adds 14 fictional people to the Cycles stills only. They are not in the `.blend` or the web GLB.

- **Source:** the CC0 MakeHuman characters prepared by GPT for the realism upgrade (`people_assets/`, provenance in `LICENSES.md`).
- **Poses:** `poses.json`, applied the same way as `people-layer.js`. Seated figures sit on the model's chairs (seat top 0.49 m task / 0.488 m visitor) and standing figures stand at real counters.
- The long tunic mesh and the importer's bone-display sphere are removed: they are not skinned for these poses.

```
blender -b Optimized_Office_Interior.blend --python scripts/place_people.py -- --then render_views.py --out OUT --cams CAM_34 --quality final
```

## Web model

Built by `scripts/web/` into `../04_SIMPLE_VIEWER/assets/`:

- `Optimized_Office_Interior_web_baked.glb`
- `office_web_metadata.json` (45 cameras, 34 rooms, 16-stop complete tour, 9-stop quick tour)
- `walk_grid.json`

See `../06_GPT_HANDOFF/README.md` for the commands and checks.
