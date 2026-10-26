#!/bin/bash
# Second pass after render_queue.sh: re-render the views that were done before later fixes (rug / exposure: CAM_04, CAM_01,
# CAM_07; reception camera reframed so the whole logo is in view: CAM_02; stair soffit added under the lobby stair: CAM_03),
# the two full-bleed deck images (cover CAM_04, closing CAM_05) at 1920 x 1080, then the Cycles top plan.
# Superseded images are moved to final/superseded/.
P=/home/user/Practice01/GARMENT_OFFICE_FINAL_PRESENTATION
L=$P/01_EDITABLE_3D/logs/final_renders.log
until grep -q QUEUE_DONE $L; do sleep 30; done
B=$P/01_EDITABLE_3D/work/render_copy.blend
S=$P/01_EDITABLE_3D/scripts/render_views.py
OUT=$P/02_RENDERED_IMAGES/final
again() {  # $1 = camera, rest = extra render_views.py arguments
  local cam=$1; shift
  mkdir -p $OUT/superseded && mv -f $OUT/$cam.png $OUT/$cam.jpg $OUT/superseded/ 2>/dev/null
  blender -b $B --python $S -- --out $OUT --quality final "$@" --cams $cam >> $L 2>&1
}
again CAM_01_Reception_A
again CAM_02_Reception_B
again CAM_03_Entrance_Lobby
again CAM_07_MD_Office_A
again CAM_04_Experience_Centre_A --res 1920x1080
again CAM_05_Experience_Centre_B --res 1920x1080
blender -b $B --python $S -- --out $OUT --quality final --res 1600x1000 --samples 64 --cams CAM_TOP_Plan >> $L 2>&1
echo QUEUE2_DONE >> $L
