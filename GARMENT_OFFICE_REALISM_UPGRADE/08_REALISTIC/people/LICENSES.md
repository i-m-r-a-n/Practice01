# Office people asset provenance

These are illustrative fictional characters, not employees or portraits of real people. No game assets, proprietary collections, scans of identifiable people, or paid purchases were used.

## MakeHuman bundled assets — CC0 1.0 Universal

- Rights holders named in the files: Data Collection AB, Joel Palmius, Jonas Hauquier / MakeHuman Team.
- Official licensing statement: https://github.com/makehumancommunity/makehuman/blob/master/LICENSE.md
- CC0 legal text: https://github.com/makehumancommunity/makehuman/blob/master/LICENSE.ASSETS.md
- Official system pack catalogue: https://static.makehumancommunity.org/assets/assetpacks/makehuman_system_assets.html
- Official downloaded pack (second official mirror): https://files.makehumancommunity.org/asset_packs/makehuman_system_assets/makehuman_system_assets_cc0.zip
- Downloaded ZIP SHA-256: `b542127a8e25547c7c29c19f2d1d2adb9a664c80396ecd694095dbc8028a0107`
- Pack source: the official MakeHuman website configuration explicitly identifies `files.makehumancommunity.org` as its second file mirror.

The official source and system-pack headers explicitly state that these graphical assets were released under **CC0 in September 2020**. The application source code is AGPL; no application source code is redistributed here. The asset licence and the application licence are separate. The two official licence files are preserved under `source/`.

Used assets:

| Asset | Origin | Use |
| --- | --- | --- |
| hm08 base mesh | MakeHuman `makehuman/data/3dobjs/base.obj` | Anatomical adult body/face, mesh correspondence |
| Asian young adult male/female targets | MakeHuman `makehuman/data/targets/macrodetails/` | Generic adult morphs, subsequently varied in proportions |
| Default skeleton and weights | MakeHuman `makehuman/data/rigs/` | Reduced 22-bone skeleton/weights |
| Low-poly eyes / brown eye texture | MakeHuman `makehuman/data/eyes/` | Generic fictional eyes |
| Young Asian male/female diffuse skin | Official system pack `skins/young_asian_*` | Skin, 2K working copy in exported GLB |
| short02, short04, ponytail01, braid01 | Official system pack `hair/` | Hair meshes/textures |
| male_casualsuit01 | Official system pack `clothes/` | Unbranded long-sleeve shirt and trousers, morph-fitted, re-materialed |
| shoes03 | Official system pack `clothes/` | Generic closed black shoes |

No third-party community asset with a different licence is used. A historical GitHub mirror was inspected during discovery, but its differently labelled assets were **not used**; all system-pack bytes came from the current official CC0 ZIP above.

## Self-made additions

`build_people.py`, `prepare_manifest.py`, `people-layer.js`, tunic extensions, rejected skirt/saree prototypes retained only as build history, procedural task gestures, collision/LOD logic, and the deterministic office placement manifest were authored for this project. No borrowed game motion or copyrighted third-party brand appears. The modest outfit additions are visualization meshes, not garment patterns or an authenticity certification.

## Limitations

The goal is believable fictional room-scale people. These are not photogrammetric hero characters or motion-captured actors. Skin/clothing close-ups, seated contacts, animation and native MacBook frame rate require separate visual/performance acceptance; the existence of licensed assets alone does not establish those qualities.
