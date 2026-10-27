# Reception bake: independent mechanism review

Status: visual quality still fails. This is a diagnosis record, not a successful bake review. No bake, approved model, or viewer was edited by this audit.

## Measured findings

- Actual 2K UV1 beam-side edges cover only **15.94–16.08 pixels across 0.3048 m height**. Mean source atlas density is ~52.5 texels/m; reported summed UV coverage is ~21.2%. A global 2K image is not evidence of high local texel density.
- Original BM008/009/010 use plain `steel_painted`: no image, procedural normal, or bump nodes. Material noise cannot explain those beam blotches.
- No foreign coplanar triangles overlap the interiors of the long vertical beam sides within the tested 20 micrometre coplanarity tolerance. Local source contacts with slab, slat raft, AC or hanging fixtures are retained source geometry, not introduced by the join. AABB contact alone does not prove mesh intersection.
- Z02 has no source targets with extra UV layers deleted by the bake. UV0 remains active for render shading, with UV1 explicitly selected as bake destination; the baker separately measures position, UV0 and normal preservation.
- Runtime lightmaps are actual linear RGBA16F, losslessly Zstd-compressed. There is no RGBM decode. A uniform pi multiplier can change scale, not introduce spatial blotches. Codec equivalence was independently tested by the texture agent.
- Nine mixed opaque/emissive source objects are joined into the room target. Their emissive shader values remain, and explicit lights remain separate. Mesh-light grouping changes could affect sampling/MIS; this is an **untested hypothesis**, not a confirmed cause.
- Paint-white Object-coordinate micro-bump origins change on join, but its source amplitude is 0.001 m distance × 0.05 strength and plain beams do not use that shader.

## Sampling evidence and limits

`reception-atlas-stats.json` samples actual UV1 triangle interiors, excluding beam horizontal top/bottom faces. At 32 samples the plain beam-side radiance has high spatial variation; RTLightmap reduces it but leaves visible low-frequency mottling. These statistics also contain real shadow/lighting gradients, so variance alone does not distinguish noise from illumination.

The configured 0.004 atlas packing margin nominally corresponds to 8.192 px, while bake dilation is 16 px. This is not a measured overlap proof because Blender packing mode and actual island spacing matter. The baker/texture agent owns the chart-isolated denoising comparison. The measured 16 px beam height makes that comparison meaningful.

Actual inspected image: `/tmp/office-phase1-reception-exr.png`, original 2K/256-sample production bake; visible mottled beams and green chair remain unacceptable. Source contacts, mesh-light grouping, thin charts and Monte Carlo/denoiser interactions remain distinct questions. No new high-cost render or speculative parameter change was performed here.

## Evidence

- `mechanism-review.json`: source hashes, material nodes, coplanar tests, mixed emitters, encoding and margin facts.
- `reception-atlas-stats.json`: source/output hashes and raw/denoised actual triangle samples.
- `beam-texel-resolution.json`: actual world/UV1 beam edge measurements.
- `measure_reception.py` and `mechanism_review.py`: reproducible read-only geometry/statistics checks.
