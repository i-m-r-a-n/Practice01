#!/bin/bash
# Export each reference camera's view from the local proposal page and render it in Cycles.
# render_batch.sh PORT CAM:MODE:W:H:SAMPLES[:ORTHO] ...
PORT=$1; shift
W=/home/user/render_work; R=/home/user/bel/GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC
(cd $R/viewer && exec python3 serve_preview.py --port $PORT > $W/out/server_$PORT.log 2>&1) &
SRV=$!
until curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:$PORT/stage2-concept/ | grep -q 200; do sleep 1; done
cd $W
for spec in "$@"; do
  IFS=: read CAM MODE RW RH SAMPLES ORTHO <<< "$spec"
  t0=$(date +%s)
  PORT=$PORT timeout 1200 python3 -I scripts/export_scene.py $CAM > out/export_$CAM.log 2>&1 || { echo "EXPORT_FAIL $CAM"; continue; }
  timeout 3000 blender -b -P scripts/render_cycles.py -- out/scene_$CAM.glb VIEW_$CAM out/render_$CAM.png $RW $RH $SAMPLES ${ORTHO:-0} $MODE 6 > out/render_$CAM.log 2>&1 || { echo "RENDER_FAIL $CAM"; continue; }
  python3 -I -c "from PIL import Image; Image.open('out/render_$CAM.png').convert('RGB').save('$R/concept-images/render_$CAM.jpg', quality=86, optimize=True, progressive=True)"
  rm -f out/scene_$CAM.glb
  echo "DONE $CAM $(( $(date +%s) - t0 ))s"
done
kill $SRV
