OFFICE REALISM TEXTURE PIPELINE
==============================

Scope
-----
This directory contains a reproducible texture codec pipeline, exact Three.js
r169 loader dependencies, diagnostic checks, and newly downloaded native 2K
copies of approved CC0 material sets. Approved source assets are never modified.

HDR lightmaps
-------------
convert_textures.py lightmap reads genuine scene-linear RGB EXR channels with
OpenEXR 3.5.2. It does not apply AgX, exposure, gamma, an albedo multiplier or an
LDR clamp. It writes VK_FORMAT_R16G16B16A16_SFLOAT (RGBA16F), linear BT.709/sRGB
primaries, one level, Zstandard supercompression. Values above 1 survive.
EXR values outside finite nonnegative half-float range fail; only tiny negative
values in [-1e-6,0) are clamped and counted in the JSON conversion report.
Every converted level is decompressed and compared bit-for-bit with the input
half-float array, and Khronos ktx validate is run.

This is NOT GPU block-compressed HDR. Zstandard reduces transfer bytes; each
2048-square RGBA16F atlas consumes 32 MiB on the GPU (4096-square: 128 MiB).
Room streaming and eviction
are needed for a bounded working set. Avoid automatic mip generation for these
atlases: it creates extra inter-island leakage without separately dilated mips.

Command (paths are examples; pass a real Cycles EXR):
  PYTHONPATH=/tmp/office-texture-py python convert_textures.py \
    --ktx /path/to/ktx lightmap input.exr output.ktx2

Dependencies: Python, numpy, Pillow, zstandard, OpenEXR 3.5.2.
Install the Khronos CLI with:
  python install_ktx_tools.py --directory /tmp/office-ktx-tools
The downloader pins official KTX Software 4.4.2's Linux archive by SHA-256.
Do not include that local binary in the public website.

Three.js integration and orientation
-----------------------------------
Copy codecs/three_r169/examples/jsm/{loaders/KTX2Loader.js,utils/WorkerPool.js,
libs/ktx-parse.module.js,libs/zstddec.module.js,libs/basis/*} into the same layout
under the viewer's Three.js vendor tree. Keep its Three core at r169.

  const loader = new KTX2Loader()
    .setTranscoderPath('./vendor/three/examples/jsm/libs/basis/')
    .setWorkerLimit(2)
    .detectSupport(renderer);
  const lightMap = await loader.loadAsync(url);
  lightMap.channel = 1;
  lightMap.minFilter = lightMap.magFilter = THREE.LinearFilter;
  lightMap.generateMipmaps = false;
  lightMap.flipY = false;

The half-float path uses the Zstd decoder directly. Basis transcoding is used for
ordinary PBR maps. Serve WASM with application/wasm and KTX2 with image/ktx2.
Do not manually mark a linear lightmap as SRGBColorSpace.

KTX conversion preserves the EXR file's top-left row order. glTF exported UVs
normally account for this. Three r169 EXRLoader itself reverses EXR scanlines,
while its flipY is false. Thus a plain EXRLoader fallback is vertically different
from this KTX path: use repeat.y=-1/offset.y=1 for that fallback if the glTF uses
the same UVs. Verify actual baked geometry against its Cycles camera before
delivery. Actual Reception comparison now verifies the rule: corrected EXR
versus default KTX differs by only 0.000800 mean RGB byte levels (maximum 2),
whereas the extra-flipped KTX visibly scrambles the atlas. Exact image hashes
and metrics are in qa/room-orientation-check.json. This verifies orientation,
not Cycles visual parity or the remaining room bakes.

PBR material sources and encodings
---------------------------------
fetch_hero_sources.py obtains actual 2048x2048 provider images. No upscaling.
New paths are pbr2k/source; approved assets/textures remains byte-identical.
pbr2k/sources.json records actual downloaded URLs, pixel sizes and SHA-256.
Some Poly Haven API/license web requests returned 403 in this environment; its
official dl.polyhaven.org files returned 200. Their CC0 status is also recorded
in the approved assets/LICENSES.md; the provider licence link is retained.
ambientCG metadata is saved beside the source manifest.

  python fetch_hero_sources.py white_oak_veneer natural_walnut_veneer \
    Terrazzo019M Fabric030 Fabric034
  python fetch_hero_sources.py herringbone_parquet laminate_floor_02 \
    leather_white Tiles040 smooth_concrete_floor Tiles043
  python make_brushed_metal.py
  python convert_hero_maps.py --ktx /path/to/ktx --threads 1

Basecolour: ETC1S/BasisLZ, qlevel192, clevel2, sRGB, mipmaps.
Normal: UASTC quality2 + Zstd9, linear data, RGB tangent-space/OpenGL +Y.
Roughness: UASTC quality2 + Zstd9, linear data, mipmaps.
No --normal-mode XY-to-alpha repacking is used. Standard Three.js normal maps
can consume these RGB files. Enable bounded anisotropic filtering in viewer.
pbr2k/index.json lists the runtime files and sizes. Reports beside each KTX2
record exact commands, source/output hashes, source resolution and encoding.
The expanded index contains 35 maps across 12 sets, 99,694,673 KTX2 bytes.
Do not fetch all maps during the first-view critical path; request room materials
progressively and retain the original maps while higher-resolution maps load.

These dielectric sets supply basecolour, normal and roughness. Metalness is 0
for them; no measured AO or metalness images are invented. Keep actual baked
lighting/AO separate. All approved tint, HSV, UV scale and material factors must
be retained; loading a generic diffuse image alone loses the approved palette.
The self-made metal micro-normal/roughness uses deterministic Fourier abrasion
lines, has no external inputs, and keeps each metal material's approved colour
and metalness. It is a finish illustration, not measured product data.

Exact hero mapping from approved material code:
  oak/oak_slat -> white_oak_veneer, tile 0.5 m, slats rotated 90 degrees.
  walnut -> natural_walnut_veneer, tile 1 m, #6B4A33 tint .85.
  fl_terrazzo -> Terrazzo019M .65m, HSV(.5,.75,1.12), roughness multiplier .55.
  terrazzo_counter -> Terrazzo019M .5m.
  fab_* / rug_wool / fl_carpet* -> Fabric030; retain palette tint;
      tile .25m / .6m / .35m respectively.
  felt_green/felt_grey -> Fabric034 .4m; retain palette tint.

Verification and limits
-----------------------
qa/codec-browser-check.json records a real Three r169 + Chromium 154 WebGL2
software-GPU test (ANGLE Vulkan SwiftShader), not a Mac performance result.
It decodes and renders the diagnostic HDR atlas, performs GPU pixel readback,
and decodes/uploads/renders UASTC normals plus ETC1S basecolour. All passed with
no page errors. HDR readback confirms values 16, 32, 64 survive above1.
qa/hdr-diagnostic.exr is SELF-MADE TEST DATA, not a Cycles light bake.
qa/cycles-z02-smoke.ktx2 is a genuine Cycles 256 px / 16 sample smoke conversion,
NOT delivery quality. Source EXR max 40.53125 agrees with the baker's raw
float max 40.544891 within half-float quantization and stays bit-exact in KTX.
The initial Reception candidate (lighting/Z02.ktx2) is 2048 px / 256 samples,
retains the denoised EXR max 28.40625 bit-for-bit, and is 15,673,981 download bytes.
It was rejected in actual-image review for visible mottling; codec validation
does not make it an accepted lighting result. Corrected work is staged separately.
Later bakes can be converted once each with convert_lightmaps.py; it updates a
separate lighting/ktx2-index.json and never edits the baker's shared manifest.
Pass --output-root for another staging directory. Retained _raw EXRs and actual
_normal/_albedo guide EXRs are skipped; they are not runtime illumination maps.
The corrected Reception 512-sample RTLightmap candidate is still provisional
pending shared-lit visual review. The separate RT candidate using actual albedo
and normal guides was rejected for residual/mottled furniture texture. OIDN RT
is documented as a beauty-image filter with texture-preserving guides; RTLightmap
is the HDR lightmap filter and does not accept these auxiliary guides. A clean
codec conversion is not visual acceptance of either denoiser output. See
qa/diagnostic-status.json for the bounded tests and their limits.
qa/pbr2k-browser-check.json additionally records successful sequential decode,
GPU upload and render of all 35 new 2048 px material maps, with no page errors.

Run a server at repository root, then:
  python qa/check_codec.py
  python qa/check_codec.py --pbr2k
  python qa/check_codec.py --browser webkit
  python qa/check_codec.py --browser firefox
The default server port is 8786; --port accepts an alternate.
The HDR/normal/basecolour codec test also passes in Playwright WebKit 26.5 Linux
and Firefox 153 Linux. Firefox uses local Xvfb display:88 and software GL.
WebKit reports a privacy-masked Apple GPU string on this Debian machine; that
is not evidence of Apple hardware. Local launch settings are in check_codec.py.
No MacBook, native Safari, Apple-GPU texture format or 60 fps test is claimed
by this codec evidence. Full-scene material appearance and remaining atlas
orientation remain integration checks. Tests do not establish visual parity
with the offline Cycles renders.

Licences
--------
Image sources: existing approved CC0 Poly Haven and ambientCG sets; new copies
are recorded in pbr2k/sources.json. Self-made metal maps are project-created.
Runtime implementation: Three.js MIT, Basis Universal Apache 2.0, ktx-parse
MIT, zstddec MIT, embedded Zstandard BSD. Texts/source hashes are under codecs/.
These open-source code licences are separate from the CC0-only art rule.
