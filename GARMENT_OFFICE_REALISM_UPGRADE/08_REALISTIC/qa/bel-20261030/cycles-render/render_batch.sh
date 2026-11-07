#!/bin/bash
# Export each reference camera's view from the local proposal page and render it in Cycles.
# render_batch.sh PORT CAM:MODE:W:H:SAMPLES[:ORTHO[:SUFFIX]] ...
#   SUFFIX names a variant of the same camera (e.g. CAM_03_Entrance_Lobby:night:1600:900:256:0:night -> render_CAM_03_Entrance_Lobby_night.jpg)
#   KEEP_GLB=1 keeps each exported scene and reuses one already exported (a second mode of the same camera exports nothing)
#   LIGHT_GAIN scales the light of the proposal layer's own fittings (render_cycles.py)
PORT=$1; shift
W=/home/user/render_work; R=/home/user/bel/GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC
OUT_DIR=${OUT_DIR:-$R/concept-images}   # e.g. concept-images/model for the 3D views of the AI-image stops
mkdir -p $OUT_DIR
(cd $R/viewer && exec python3 serve_preview.py --port $PORT > $W/out/server_$PORT.log 2>&1) &
SRV=$!
until curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:$PORT/stage2-concept/ | grep -q 200; do sleep 1; done
cd $W
for spec in "$@"; do
  IFS=: read CAM MODE RW RH SAMPLES ORTHO SUFFIX <<< "$spec"
  NAME=$CAM${SUFFIX:+_$SUFFIX}
  t0=$(date +%s)
  if [ -n "$KEEP_GLB" ] && [ -s out/scene_$CAM.glb ]; then echo "REUSE $CAM"; else
    PORT=$PORT timeout 1200 python3 -I scripts/export_scene.py $CAM > out/export_$CAM.log 2>&1 || { echo "EXPORT_FAIL $CAM"; continue; }
  fi
  timeout 3000 blender -b -P scripts/render_cycles.py -- out/scene_$CAM.glb VIEW_$CAM out/render_$NAME.png $RW $RH $SAMPLES ${ORTHO:-0} $MODE 6 > out/render_$NAME.log 2>&1 || { echo "RENDER_FAIL $NAME"; continue; }
  python3 -I -c "from PIL import Image; Image.open('out/render_$NAME.png').convert('RGB').save('$OUT_DIR/render_$NAME.jpg', quality=86, optimize=True, progressive=True)"
  [ -n "$KEEP_GLB" ] || rm -f out/scene_$CAM.glb
  echo "DONE $NAME $(( $(date +%s) - t0 ))s"
done
kill $SRV
