#!/bin/bash
# Second pass after render_queue.sh: re-render the views that were done before later fixes (rug / exposure: CAM_04, CAM_01,
# CAM_07; reception camera reframed so the whole logo is in view: CAM_02), then the Cycles top plan.
# Superseded images are moved to final/superseded/.
P=/home/user/Practice01/GARMENT_OFFICE_FINAL_PRESENTATION
L=$P/01_EDITABLE_3D/logs/final_renders.log
until grep -q QUEUE_DONE $L; do sleep 30; done
B=$P/01_EDITABLE_3D/work/render_copy.blend
S=$P/01_EDITABLE_3D/scripts/render_views.py
OUT=$P/02_RENDERED_IMAGES/final
for cam in CAM_01_Reception_A CAM_02_Reception_B CAM_04_Experience_Centre_A CAM_07_MD_Office_A; do
  mkdir -p $OUT/superseded && mv -f $OUT/$cam.png $OUT/$cam.jpg $OUT/superseded/ 2>/dev/null
  blender -b $B --python $S -- --out $OUT --quality final --cams $cam >> $L 2>&1
done
blender -b $B --python $S -- --out $OUT --quality final --res 1600x1000 --samples 64 --cams CAM_TOP_Plan >> $L 2>&1
echo QUEUE2_DONE >> $L
