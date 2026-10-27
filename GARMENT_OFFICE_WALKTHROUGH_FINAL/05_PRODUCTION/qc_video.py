"""Technical QC of a finished video: python3 qc_video.py VIDEO.mp4 OUT_DIR
Checks container / codec / size / frame rate / duration / pixel format / colour tags / faststart, scans for black or frozen
stretches, decodes the whole file (errors), and writes a contact sheet (one frame every 4 s) + a JSON report."""
import json
import os
import re
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

video, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
name = os.path.splitext(os.path.basename(video))[0]


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


probe = json.loads(sh(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", video]).stdout)
v = next(s for s in probe["streams"] if s["codec_type"] == "video")
a = next((s for s in probe["streams"] if s["codec_type"] == "audio"), None)
dur = float(probe["format"]["duration"])
with open(video, "rb") as f:
    head = f.read(64 * 1024)
moov_first = head.find(b"moov") != -1 and (head.find(b"mdat") == -1 or head.find(b"moov") < head.find(b"mdat"))
dec = sh(["ffmpeg", "-v", "error", "-i", video, "-f", "null", "-"])
black = sh(["ffmpeg", "-i", video, "-vf", "blackdetect=d=0.5:pix_th=0.06", "-an", "-f", "null", "-"]).stderr
freeze = sh(["ffmpeg", "-i", video, "-vf", "freezedetect=n=0.002:d=1.5", "-an", "-f", "null", "-"]).stderr
blacks = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", black)
freezes = re.findall(r"freeze_start: ([\d.]+)", freeze)
fr = v["r_frame_rate"].split("/")
rep = dict(file=video, bytes=os.path.getsize(video), duration_s=round(dur, 3), codec=v["codec_name"], profile=v.get("profile"),
           size=f'{v["width"]}x{v["height"]}', fps=round(int(fr[0]) / int(fr[1]), 3), pix_fmt=v["pix_fmt"],
           color=dict(space=v.get("color_space"), primaries=v.get("color_primaries"), transfer=v.get("color_transfer")),
           bitrate_kbps=round(int(probe["format"]["bit_rate"]) / 1000), audio=a and f'{a["codec_name"]} {a.get("sample_rate")} Hz {a.get("channels")} ch',
           faststart_moov_before_mdat=moov_first, decode_errors=dec.stderr.strip()[:500] or None,
           black_segments=[(float(s), float(e)) for s, e in blacks], frozen_segments_start=[float(x) for x in freezes])
# contact sheet
times = [t for t in range(0, int(dur), 4)]
thumbs = []
for t in times:
    p = os.path.join(out, f"_t{t}.png")
    sh(["ffmpeg", "-v", "error", "-y", "-ss", str(t + 0.5), "-i", video, "-frames:v", "1", "-vf", "scale=384:216", p])
    if os.path.exists(p):
        thumbs.append((t, Image.open(p).convert("RGB")))
        os.remove(p)
cols = 5
rows = (len(thumbs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 394 + 10, rows * 240 + 50), (246, 243, 238))
d = ImageDraw.Draw(sheet)
F = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Regular.otf", 15)
d.text((10, 14), f"{os.path.basename(video)}  -  {rep['size']} {rep['fps']} fps  {dur:.1f} s  - one frame every 4 s", font=F, fill=(30, 30, 28))
for i, (t, im) in enumerate(thumbs):
    x, y = 10 + (i % cols) * 394, 44 + (i // cols) * 240
    sheet.paste(im, (x, y))
    d.text((x, y + 218), f"{t // 60}:{t % 60:02d}", font=F, fill=(60, 60, 58))
sheet.save(os.path.join(out, f"{name}_contact_sheet.jpg"), quality=86)
rep["contact_sheet"] = f"{name}_contact_sheet.jpg"
json.dump(rep, open(os.path.join(out, f"{name}_qc.json"), "w"), indent=1)
print(json.dumps(rep))
