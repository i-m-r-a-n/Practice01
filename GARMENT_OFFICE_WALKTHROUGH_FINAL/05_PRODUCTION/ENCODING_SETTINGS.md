# How the walkthrough videos are made

Method chosen by benchmark (`benchmarks/benchmark_eevee.txt`, `benchmark_cycles.txt`): EEVEE in this cloud machine runs on a
software OpenGL driver (about 240 s per frame and a too-blue interior), so every frame is **path-traced in Cycles** from the
approved model, at low sample count with denoising:

| Stage | Setting |
|---|---|
| Scene | `04_BLENDER_ANIMATION/Office_Walkthrough_Animation.blend` = the approved model + 28 animated cameras (`WT_<shot>`), 24 fps timeline. The approved `.blend` / `.glb` are not modified (SHA-256 before/after in `source_model_sha256_before.txt`) |
| Camera moves | `scripts/shots.py`: dolly, orbit and crane moves, level cameras (verticals stay vertical, lens shift for framing), smoothstep easing; every path checked against walls and furniture (`camera_collision_check.csv`) |
| Render | Cycles CPU, 1280 x 720, 4 samples + OpenImageDenoise (albedo + normal), adaptive threshold 0.08, bounces 4 / diffuse 2 / glossy 2, caustics off, clamp indirect 3, light tree, fixed seed; AgX view transform, exposure +1.6 inside, +0.3 overviews; ceilings, beams and fittings hidden only in the overview shots. Every 2nd frame of the 24 fps timeline is rendered (12 fps) |
| Frame rate | ffmpeg `minterpolate` (motion-compensated: mci, aobmc, bidirectional, vsbmc) 12 -> 24 fps |
| Size | Lanczos 1280 x 720 -> 1920 x 1080, `unsharp 5:5:0.35` |
| Graphics | Title card, closing card and opening overlay (`scripts/make_titles.py`) from the approved logos/tagline in `GARMENT_OFFICE_FINAL_PRESENTATION/03_PRESENTATION/assets`; lower thirds (scene + room) drawn with Inter; "Proposed interior design / 3D visualization" tag on every shot |
| Edit | `scripts/make_video.py`: title card 4 s -> shots -> closing card 6 s, cross-dissolves 0.5 s (pitch) / 0.4 s (full tour) |
| Encode | H.264 High@4.1, CRF 18, preset slow, yuv420p, GOP 48, BT.709 tags, `+faststart`, 24 fps; silent AAC 48 kHz stereo track (no music: no licensed track was supplied) |

Each video has a `.settings.json` next to it with the exact clip list, durations and encoder arguments.

Re-run (from `GARMENT_OFFICE_WALKTHROUGH_FINAL/`):
```
blender -b 04_BLENDER_ANIMATION/Office_Walkthrough_Animation.blend --python 04_BLENDER_ANIMATION/scripts/render_shots.py -- --out work/frames --res 1280x720 --samples 4 --shots ALL
python3 04_BLENDER_ANIMATION/scripts/make_titles.py work/titles
python3 04_BLENDER_ANIMATION/scripts/make_video.py pitch work/frames work/titles 01_CLIENT_PITCH_VIDEO/Client_Pitch_Cinematic_Tour.mp4 --work work/edit_pitch
python3 04_BLENDER_ANIMATION/scripts/make_video.py tour  work/frames work/titles 02_FULL_FLOOR_TOUR/Complete_Ground_Floor_Tour.mp4 --work work/edit_pitch
```

## Delivered files and web copies
| File | Encode | Size |
|---|---|---|
| `01_CLIENT_PITCH_VIDEO/Client_Pitch_Cinematic_Tour.mp4` | as above, CRF 18 | 73.8 MB, 77.0 s |
| `02_FULL_FLOOR_TOUR/Complete_Ground_Floor_Tour.mp4` | the CRF 18 edit (117.9 MB) is over GitHub's 100 MB file limit, so the delivered file is that edit re-encoded once: libx264 preset slow, **CRF 20, max 6 Mbit/s** (buffer 12 Mbit), High@4.1, BT.709, `+faststart`, audio copied | 78.9 MB, 121.0 s |
| `..._web720.mp4` (both videos) | for phones, e-mail links and the website: Lanczos 1280 x 720, CRF 23, max 3 Mbit/s, High@4.0, BT.709, AAC 96 kbit/s, `+faststart` | pitch 16.9 MB, tour 26.0 MB |

QC of every delivered file (`05_PRODUCTION/video_qc/*_qc.json` + contact sheets): no decode errors, no black frames, frozen only
on the intended title (0.8 s) and closing cards. Re-encode commands: `05_PRODUCTION/reencode_videos.sh`.
