# Texture and codec licences

All art added by this pipeline is CC0 or made specifically for this project.
Provider originals are retained in `pbr2k/source`; exact download URLs, native
pixel sizes and SHA-256 values are recorded in `pbr2k/sources.json`. Compressed
derivatives are in `pbr2k/ktx2`, with conversion reports beside each file.

| Art asset | Source | Licence | Added maps |
| --- | --- | --- | --- |
| White oak veneer | [Poly Haven](https://polyhaven.com/a/white_oak_veneer) | [CC0](https://polyhaven.com/license) | Native 2K basecolour, OpenGL normal, roughness |
| Natural walnut veneer | [Poly Haven](https://polyhaven.com/a/natural_walnut_veneer) | [CC0](https://polyhaven.com/license) | Native 2K basecolour, OpenGL normal, roughness |
| Terrazzo019M | [ambientCG](https://ambientcg.com/a/Terrazzo019M) | [CC0](https://docs.ambientcg.com/license/) | Native 2K basecolour, OpenGL normal, roughness |
| Fabric030 | [ambientCG](https://ambientcg.com/a/Fabric030) | [CC0](https://docs.ambientcg.com/license/) | Native 2K basecolour, OpenGL normal, roughness |
| Fabric034 | [ambientCG](https://ambientcg.com/a/Fabric034) | [CC0](https://docs.ambientcg.com/license/) | Native 2K basecolour, OpenGL normal, roughness |
| Herringbone parquet | [Poly Haven](https://polyhaven.com/a/herringbone_parquet) | [CC0](https://polyhaven.com/license) | Native 2K basecolour, OpenGL normal, roughness |
| Laminate floor02 | [Poly Haven](https://polyhaven.com/a/laminate_floor_02) | [CC0](https://polyhaven.com/license) | Native 2K basecolour, OpenGL normal, roughness |
| White leather | [Poly Haven](https://polyhaven.com/a/leather_white) | [CC0](https://polyhaven.com/license) | Native 2K basecolour, OpenGL normal, roughness |
| Smooth concrete floor | [Poly Haven](https://polyhaven.com/a/smooth_concrete_floor) | [CC0](https://polyhaven.com/license) | Native 2K basecolour, OpenGL normal, roughness |
| Tiles040 | [ambientCG](https://ambientcg.com/a/Tiles040) | [CC0](https://docs.ambientcg.com/license/) | Native 2K basecolour, OpenGL normal, roughness |
| Tiles043 | [ambientCG](https://ambientcg.com/a/Tiles043) | [CC0](https://docs.ambientcg.com/license/) | Native 2K basecolour, OpenGL normal, roughness |
| Brushed metal micro-surface | `make_brushed_metal.py`, deterministic seed3292 | Self-made for this project; no external input | 2K OpenGL normal and roughness |
| HDR codec diagnostic | `qa/hdr-diagnostic.exr` | Self-made test data; no external input | Linear four-quadrant HDR test, not a bake |
| Terrazzo codec smoke fixtures | Existing approved Terrazzo019M 1K source | CC0, as recorded above and in approved `assets/LICENSES.md` | KTX2 diagnostic derivatives only |
| Cycles Z02 smoke atlas | Approved office model, copy baked by this project | Client project work | Diagnostic lightmap, not final delivery quality |

Poly Haven's API and licence web pages returned HTTP403 in this environment;
its official download host returned HTTP200 for the 2K source files. Their CC0
status is also recorded in the approved asset licence list. ambientCG's API
metadata and licence page were accessible. No source is taken from a game.

Code dependencies have their own open-source licences; they are not art assets:

| Dependency | Licence text |
| --- | --- |
| Three.js r169 / KTX2Loader / WorkerPool | `codecs/three_r169/LICENSE` (MIT) |
| Basis Universal transcoder | `codecs/third_party_licenses/basis-universal-Apache-2.0.txt` |
| ktx-parse | `codecs/third_party_licenses/ktx-parse-MIT.txt` |
| zstddec | `codecs/third_party_licenses/zstddec-MIT.txt` |
| Embedded Zstandard implementation | `codecs/third_party_licenses/zstd-BSD.txt` |

Exact vendor file URLs and hashes are in `codecs/three_r169/manifest.json`.
Supplemental licence text sources and hashes are recorded in
`codecs/third_party_licenses/sources.json`. KTX Software is only a local build
tool; its downloaded binary is not redistributed with the tour.
