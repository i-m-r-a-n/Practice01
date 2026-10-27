# Cycles lightmap pipeline

This pipeline reads a disposable byte-identical copy of the approved Blender scene. It never saves that scene, changes the approved file, moves walls, cuts doors, or changes room geometry. Geometry is evaluated with its existing modifiers, joined for efficient baking, UV-unwrapped on a new second channel, then exported in interior/overhead batches. Runtime materials are exact-name references to the original viewer PBR materials.

## Current evidence and acceptance

- The first `lighting/Z02` and `lighting/Z30` outputs are real 2048px Cycles bakes, configured at 256 samples, but **rejected visual candidates**. They are retained for diagnosis, not accepted lighting or the default of a completed release.
- `lighting-v2/assignment.json` is an exact ownership audit: 1,065 diffuse bake targets across all 34 rooms and four shared atlas groups. Forty-seven entirely transmissive/mirror/emissive objects remain original runtime PBR objects. Assignment is not proof that their bakes are complete.
- `uv-density-plan.json` records measured key-room and shared-shell UV packing, not completed lighting. Initial shared-wall packing measured a 4K atlas at62.57px/m; it must be remeasured after four local context objects return to the Reception hero atlas. whole beams, frames, columns, floor slab and deck use separate 2K atlases. Key floor density is43.86–52.50px/m except the small MD room, which is denser. Merchandising requires 4K and floor UV weighting.
- The ambiguous default target-UV hypothesis was tested with identical geometry/32 samples. Explicit `LightmapUV` and default bake outputs were effectively identical (mean RGB absolute difference 3.98e-10). Future bakes nevertheless name the target UV explicitly.
- Source geometry/UV0 preservation is measured in world space. Original Reception had maximum 1.08 micrometre coordinate change from float32 joining, and 0.1431 degree maximum corner-normal deviation. No normal reversal was found.
- The first denoiser was OIDN RT, intended for images. New candidates use standalone OIDN RTLightmap in a separate process; however its 32-sample diagnostic alone did not solve visible mottling. Chart-isolated filtering is being tested before bulk production. Do not interpret a successful process return or `baked-unreviewed` status as visual acceptance.

## Reproducible tools

The approved file requires Blender 5.2 or newer. This environment uses official Blender 5.2.3 LTS:

- Source: `https://download.blender.org/release/Blender5.2/blender-5.2.3-linux-x64.tar.xz`
- Archive SHA256: `78486c018b4443efe5e75ab54c290ed8c15abafd249b862c2c9ce2530a918eec`
- Local binary: `/workspace/tools/blender-5.2.3-linux-x64/blender`

Standalone OIDN 2.3.3 includes the RTLightmap filter:

- Source: `https://github.com/RenderKit/oidn/releases/download/v2.3.3/oidn-2.3.3.x86_64.linux.tar.gz`
- Archive SHA256: `3c385230d9e6f63527ba72f2229594dbac5051674219d72e0044b5d0b841796f`
- Local library: `/workspace/tools/oidn/oidn-2.3.3.x86_64.linux/lib/libOpenImageDenoise.so`
- The postprocess Python environment needs NumPy and OpenEXR. In this workspace these are available with `PYTHONPATH=/tmp/office-texture-py`.
- Set `OFFICE_OIDN_LIBRARY`, `OFFICE_BAKE_PYTHON`, or `OFFICE_BAKE_PYTHONPATH` to portable equivalents elsewhere. OIDN is run outside Blender to avoid mixing its bundled OIDN with the standalone library.

Approved source SHA256:

`fa3ed3d58f6d44c3554e3761307841b96115ff7816e4e541c8e6611cb363810d`

Create a working copy without modifying the original:

```sh
mkdir -p /workspace/office-bake-work
cp GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/Final_Office_Interior.blend /workspace/office-bake-work/approved-copy.blend
```

Review the bounded batch first:

```sh
python GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/blender/run_rooms.py --rooms all --dry-run
```

Run one room after diagnostic acceptance:

```sh
python GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/blender/run_rooms.py --rooms Z02 --samples 512
```

Run the six key rooms and shared shell, or all 34 rooms, only after the first corrected room passes review:

```sh
python GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/blender/run_rooms.py --resume
python GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/blender/run_rooms.py --rooms all --resume
```

These commands run finite batches; they create no scheduled task or service. A `STOP_BAKES` file in the work directory prevents the next room from starting. The driver uses four threads by default; this container has five effective CPUs and no GPU.

## Data contract

Each completed candidate writes:

- `ROOM_raw.exr`: original linear HDR diffuse direct+indirect lighting, **without albedo**; immutable denoiser input.
- `ROOM.exr`: half-float linear HDR RTLightmap result, no AgX or display transform.
- `ROOM.denoise.json`: isolated filter inputs, timings, hashes, numerical range and clamp evidence.
- `ROOM.glb`: evaluated geometry, original UV0 and packed UV1; material name stubs; `overhead` metadata. There are no baked vertex colours or embedded duplicate PBR textures.
- `ROOM.json`: source hash, exact original object names to replace, per-object UV density, geometry audit and explicit sample settings.
- `manifest.json`: only completed candidate entries. `SHELL_*` entries have `alwaysLoad: true`. A candidate status remains `baked-unreviewed` until separate actual-view review.

The runtime lightmap uses channel 1 and linear HDR. Its initial physical conversion factor is pi because Cycles' diffuse colour-free bake is radiance, while the Three.js lighting code expects irradiance before Lambert's division by pi. Actual Cycles-camera comparison is still required for exposure/calibration.

KTX2 conversion is separate, using `textures/convert_lightmaps.py --output-root .../lighting-v2`. Current KTX2 is lossless half-float RGBA plus Zstd, not GPU block compression: 2K costs 32MiB decoded, 4K costs 128MiB. Four shared atlases cost 224MiB. Room residency must therefore be bounded by actual byte size, not only number of rooms.

`--export-only` writes geometry and audit metadata without claiming a lightmap exists. `--assignment-only` writes source ownership only. `--guide-only` writes a diagnostic normal guide; it does not produce lighting.
