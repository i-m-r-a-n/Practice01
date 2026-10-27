# Approved office assets and additive dressing audit

This is a read-only audit of the approved source and a prepared Phase 4 module. It does not replace the phase-ordered visual acceptance, source-intersection review or Mac browser tests.

The approved Blender SHA-256 remains `fa3ed3d58f6d44c3554e3761307841b96115ff7816e4e541c8e6611cb363810d`. `asset_inventory.json` locks the complete original Blender/GLB, layout, material and builder scripts. `approved_room_inventory.json` records all 34 rooms and 295 scheduled placements with real source origins and orientations. No approved source bytes or fixed-furniture transforms were modified.

## Existing coverage

The source already includes monitors, keyboards, mice, cable trays, pedestals and some paper stacks on bench desks; dual displays on CAD desks; executive writing pads, a closed folio and pen cups; two reception monitors; garments, yarn cones, swatches and folded samples in the Experience Centre; seven dress/display forms; library books; sewing/steam stations; four enclosed 3D printers; pantry microwave, coffee machine, fridge and water dispenser. Those were not duplicated. Existing planters, wall clocks, fire equipment, signs and building services stay at their source positions.

The 14 existing CC0 surface sets contain 42 image maps. Every one is exactly 1024×1024. The original GLB has 79 materials: 37 base-colour maps, 32 normal maps, 24 metallic/roughness maps and no AO texture slots. The current web GLB has 36/32/20/0 respectively. These are actual exported material counts, not a claim every missing slot needs an artificial texture: homogeneous dielectrics legitimately use metalness=0, and plain metals use explicit scalar metalness.

The 12 downloaded model packages are covered by the existing Poly Haven CC0 inventory. Client logo files are project-restricted and hash locked. No new third-party prop was downloaded.

## PBR continuity

Use the same source sets at native 2K for close-view hero surfaces. The texture pipeline owns these downloads, source URLs and exact hashes in `../textures/pbr2k/`. Do not upscale 1K and label it a native 2K asset.

| Materials | Original set | UV tile scale | Appearance that must survive |
|---|---|---:|---|
| oak / oak_slat | white_oak_veneer | 0.5 m | Slat mapping rotated 90 degrees |
| walnut | natural_walnut_veneer | 1.0 m | #6B4A33 tint, source mix factor 0.85 |
| fl_terrazzo | Terrazzo019M | 0.65 m | HSV(.5,.75,1.12), roughness multiplier .55, normal .25 |
| terrazzo_counter | Terrazzo019M | 0.5 m | Roughness .35 multiplier, coat .3 |
| fab_charcoal / green / sand / grey | Fabric030 | 0.25 m | Distinct approved palette tints, roughness about .9 |
| carpet / green carpet | Fabric030 | 0.35 m | Recolour, quarter-turn/repetition and existing prayer-line pattern |
| rug_wool | Fabric030 | 0.6 m | Roughness .95 |
| felt_green / grey | Fabric034 | 0.4 m | Source tint and roughness .95 |

Other existing sets are herringbone_parquet, laminate_floor_02, leather_white, smooth_concrete_floor, Tiles040, Tiles043, Carpet003/004 and Fabric036. Exact source node settings are in the locked `scripts/lib_materials.py`. No brushed-metal source maps exist; the texture agent is preparing a self-made fine micro-normal/roughness pair without changing metal base colours. Source terrazzo grout is 0.8 m, not the prompt's illustrative 600 mm tile example. Preserve the approved appearance and disclose this difference.

## Prepared additive props

`../props/office-props-manifest.json` contains 323 hand-defined, deterministic placements, derived from source builder coordinates and actual top heights. `office-props.mjs` assembles 1,473 components into 49 instanced draw calls and 128,786 triangles, below the 300k prop budget. Labels are short readable generic English on one self-made 2048×2048 atlas. Geometry is self-made: cups, bottles, notebooks, papers, trays, books, generic phones, cables, glasses/jug, sample tools, fabric swatches, filament spools, kettle, tea/sugar pots, towels, soap, shoes and prayer mats. This module contains no people; any separately authorized fictional people layer is independently owned.

All 34 rooms were reviewed; 28 receive new props. The six circulation zones receive no extra floor clutter or invented sockets/fire fixtures. Existing approved signs, lighting and fittings remain. No chairs are moved; randomness is limited to small rotations of loose items. The female source shoe rack straddles its room boundary, so additions on that rack were omitted; its approved geometry remains untouched. The male rack is a closed cabinet in the actual model, so objects are supported on the top instead of inventing shelf voids.

Checks use the assembled geometry, not only nominal centres: all prop world AABBs stay in their room polygons, no prop pair AABBs overlap, no component drops below its recorded support, matrices are finite. Initial rejected placements and bevel bounds were corrected before the final check. Details: `../props/placement-checks.json` and `build-stats.json`.

Still to verify after Phase 4 integration: exact prop/source-component contacts, every key-room view and close-up, label orientation/legibility, shading against Cycles and AO. Props are not in the Phase 1 lightmap bake; grounded ambient occlusion or a new bake is required before claiming baked prop contact shadows. All-item dressing acceptance is not yet achieved: no additional wall sockets, coat rack, umbrella stand, desk lamps, open drawers or replacement screen UI were authored without resolving their support/plan constraints. No live GPU, Mac fps or screenshot acceptance claim is made by this audit.
