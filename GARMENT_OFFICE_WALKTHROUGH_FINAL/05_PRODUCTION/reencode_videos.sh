#!/bin/bash
# GitHub limit is 100 MB per file: the 2-min tour master is re-encoded at CRF 20 (capped 6 Mbit/s); 720p web copies for phones / the website.
set -e
cd "$(dirname "$0")/.."      # GARMENT_OFFICE_WALKTHROUGH_FINAL
mkdir -p work/reenc
T=02_FULL_FLOOR_TOUR/Complete_Ground_Floor_Tour.mp4     # input: the CRF 18 edit written by make_video.py
P=01_CLIENT_PITCH_VIDEO/Client_Pitch_Cinematic_Tour.mp4
nice -n 8 ffmpeg -y -v error -i $T -c:v libx264 -preset slow -crf 20 -maxrate 6M -bufsize 12M -pix_fmt yuv420p -profile:v high -level 4.1 \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a copy -movflags +faststart work/reenc/tour_1080.mp4
echo TOUR1080 $(stat -c %s work/reenc/tour_1080.mp4)
for v in $T $P; do
  n=$(basename $v .mp4)
  nice -n 8 ffmpeg -y -v error -i $v -vf "scale=1280:720:flags=lanczos" -c:v libx264 -preset slow -crf 23 -maxrate 3M -bufsize 6M -pix_fmt yuv420p \
    -profile:v high -level 4.0 -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a aac -b:a 96k -movflags +faststart work/reenc/${n}_web720.mp4
  echo WEB720 $n $(stat -c %s work/reenc/${n}_web720.mp4)
done
echo "REENC_DONE: move work/reenc/tour_1080.mp4 over $T and the _web720 files next to their videos"
