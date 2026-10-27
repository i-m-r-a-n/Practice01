"""Edits a walkthrough video from the rendered Cycles frames (ffmpeg). Resumable: finished shot clips are reused.
python3 make_video.py pitch|tour FRAMES_DIR TITLES_DIR OUT.mp4 --work WORK_DIR
- every shot: 12 fps render -> 24 fps motion-compensated interpolation (minterpolate), Lanczos to 1920 x 1080, mild sharpening,
  lower third (scene + room) fading in/out, small "proposed design" tag; the opening orbit carries the title overlay
- title card + shots + closing card joined with cross-dissolves; H.264 High, yuv420p, BT.709, +faststart, silent AAC track
Encoding settings are written next to the video (OUT.settings.json).
"""
import argparse
import glob
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shots as S  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("video", choices=["pitch", "tour"])
ap.add_argument("frames")
ap.add_argument("titles")
ap.add_argument("out")
ap.add_argument("--work", required=True)
ap.add_argument("--only", default="", help="comma-separated shot names: build these clips only (tests)")
a = ap.parse_args()
a.frames, a.titles, a.work, a.out = (os.path.abspath(p) for p in (a.frames, a.titles, a.work, a.out))
os.makedirs(a.work, exist_ok=True)
FS = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
FR = "/usr/share/fonts/opentype/inter/Inter-Regular.otf"
W, H, FPS = 1920, 1080, 24
XF = 0.5 if a.video == "pitch" else 0.4                       # cross-dissolve length
TITLE_S, CLOSE_S = (4.0, 6.0) if a.video == "pitch" else (4.0, 6.0)
order = S.PITCH_ORDER if a.video == "pitch" else S.TOUR_ORDER
by = {s["name"]: s for s in S.SHOTS}
X264_CLIP = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p"]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffmpeg failed: " + " ".join(cmd)[:400] + "\n" + r.stderr[-2000:])


def duration(path):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).strip())


def esc(t):
    return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "’").replace("%", "\\%")


shade = os.path.join(a.work, "lower_shade.png")
if not os.path.exists(shade):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = Image.new("L", (W, 330), 0)
    d = ImageDraw.Draw(g)
    for i in range(330):
        d.line([(0, i), (W, i)], fill=int(190 * (i / 330) ** 1.3))
    band = Image.new("RGBA", (W, 330), (8, 14, 10, 255))
    band.putalpha(g)
    im.alpha_composite(band, (0, H - 330))
    im.save(shade)


def shot_clip(name):
    s = by[name]
    out = os.path.join(a.work, f"clip_{name}.mp4")
    files = sorted(glob.glob(os.path.join(a.frames, name, "f_*.png")))
    need = S.frames(s)
    if len(files) != need or any(os.path.getsize(f) < 1000 for f in files):
        sys.exit(f"{name}: {len(files)} of {need} frames rendered - not ready")
    if os.path.exists(out) and os.path.getmtime(out) > max(os.path.getmtime(f) for f in files):
        return out
    lst = os.path.join(a.work, f"frames_{name}.txt")
    with open(lst, "w") as f:
        for p in files:
            f.write(f"file '{p}'\nduration {1 / 12:.6f}\n")
        f.write(f"file '{files[-1]}'\n")
    D = len(files) / 12
    base = (f"[0:v]fps=12,minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,"
            f"scale={W}:{H}:flags=lanczos,unsharp=5:5:0.35:5:5:0,format=rgba[v0]")
    tag = (f"drawtext=fontfile={FR}:text='{esc('Proposed interior design  |  3D visualization')}':fontsize=21:"
           f"fontcolor=white@0.72:x=w-tw-56:y=h-56:shadowcolor=black@0.5:shadowx=1:shadowy=1")
    if name == "A01_overview_orbit":                          # title overlay over the opening orbit
        ov = os.path.join(a.titles, "opening_overlay.png")
        fc = (f"{base};[1:v]format=rgba,fade=t=in:st=0.9:d=0.9:alpha=1,fade=t=out:st={D - 1.6:.2f}:d=0.9:alpha=1[o];"
              f"[v0][o]overlay=0:0:shortest=1,{tag},format=yuv420p[v]")
        inputs = ["-f", "concat", "-safe", "0", "-i", lst, "-loop", "1", "-framerate", str(FPS), "-t", f"{D:.3f}", "-i", ov]
    elif s["label"]:
        t_in, t_out = 0.5, D - 0.9
        alpha = f"if(lt(t\\,{t_in})\\,0\\,if(lt(t\\,{t_in + 0.6})\\,(t-{t_in})/0.6\\,if(lt(t\\,{t_out})\\,1\\,if(lt(t\\,{t_out + 0.6})\\,({t_out + 0.6}-t)/0.6\\,0))))"
        scene = esc(s["scene"].upper())
        label = esc(s["label"])
        fc = (f"{base};[1:v]format=rgba,fade=t=in:st={t_in}:d=0.6:alpha=1,fade=t=out:st={t_out:.2f}:d=0.6:alpha=1[o];"
              f"[v0][o]overlay=0:0:shortest=1,"
              f"drawtext=fontfile={FS}:text='{scene}':fontsize=24:fontcolor=0x9FD3B0:alpha='{alpha}':x=96:y=h-196,"
              f"drawtext=fontfile={FS}:text='{label}':fontsize=50:fontcolor=white:alpha='{alpha}':x=96:y=h-158:"
              f"shadowcolor=black@0.45:shadowx=1:shadowy=2,{tag},format=yuv420p[v]")
        inputs = ["-f", "concat", "-safe", "0", "-i", lst, "-loop", "1", "-framerate", str(FPS), "-t", f"{D:.3f}", "-i", shade]
    else:
        fc = f"{base},{tag},format=yuv420p[v]"
        inputs = ["-f", "concat", "-safe", "0", "-i", lst]
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", fc, "-map", "[v]", "-r", str(FPS), *X264_CLIP, out])
    return out


def card_clip(png, seconds, name, fade_in, fade_out):
    out = os.path.join(a.work, f"{name}.mp4")
    if os.path.exists(out) and os.path.getmtime(out) > os.path.getmtime(png):
        return out
    vf = f"scale={W}:{H},format=yuv420p"
    if fade_in:
        vf += ",fade=t=in:st=0:d=0.8"
    if fade_out:
        vf += f",fade=t=out:st={seconds - 1.0}:d=1.0"
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS), "-t", str(seconds), "-i", png, "-vf", vf, "-r", str(FPS), *X264_CLIP, out])
    return out


if a.only:
    for n in a.only.split(","):
        print("clip", shot_clip(n))
    sys.exit(0)

clips = [card_clip(os.path.join(a.titles, "title_card.png"), TITLE_S, f"title_{a.video}", True, False)]
clips += [shot_clip(n) for n in order]
clips.append(card_clip(os.path.join(a.titles, "closing_card.png"), CLOSE_S, f"closing_{a.video}", False, True))
durs = [duration(c) for c in clips]
inputs, parts, prev, off = [], [], "[0:v]", 0.0
for c in clips:
    inputs += ["-i", c]
for i in range(1, len(clips)):
    off += durs[i - 1] - XF
    lab = f"[x{i}]" if i < len(clips) - 1 else "[vout]"
    parts.append(f"{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}{lab}")
    prev = lab
total = sum(durs) - XF * (len(clips) - 1)
enc = ["-c:v", "libx264", "-preset", "slow", "-crf", "18", "-profile:v", "high", "-level", "4.1", "-pix_fmt", "yuv420p",
       "-g", "48", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-movflags", "+faststart",
       "-c:a", "aac", "-b:a", "96k", "-ar", "48000"]
run(["ffmpeg", "-y", "-v", "error", *inputs, "-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=r=48000:cl=stereo",
     "-filter_complex", ";".join(parts), "-map", "[vout]", "-map", f"{len(clips)}:a", "-r", str(FPS), *enc, "-shortest", a.out])
json.dump(dict(video=a.out, shots=order, clip_seconds=dict(zip([os.path.basename(c) for c in clips], durs)), crossfade_s=XF,
               duration_s=round(duration(a.out), 3), render="Cycles 1280x720, 4 spp + OpenImageDenoise, every 2nd frame of 24 fps (12 fps)",
               interpolation="ffmpeg minterpolate mci/aobmc/bidir/vsbmc to 24 fps", scale="Lanczos to 1920x1080, unsharp 0.35",
               encode=" ".join(enc)), open(a.out + ".settings.json", "w"), indent=1)
print("VIDEO", a.out, round(duration(a.out), 2), "s")
