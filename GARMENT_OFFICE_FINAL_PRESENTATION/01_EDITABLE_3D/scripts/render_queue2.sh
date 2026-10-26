#!/bin/bash
# Second pass after render_queue.sh: re-renders the views listed in rerender_list.txt (views done before later fixes, and the
# full-bleed deck images at 1920 x 1080), then the Cycles top plan. Superseded images are moved to final/superseded/.
# The list is read line by line while this runs, so views can be appended without restarting the queue.
P=/home/user/Practice01/GARMENT_OFFICE_FINAL_PRESENTATION
L=$P/01_EDITABLE_3D/logs/final_renders.log
until grep -q QUEUE_DONE $L; do sleep 30; done
B=$P/01_EDITABLE_3D/work/render_copy.blend
S=$P/01_EDITABLE_3D/scripts/render_views.py
OUT=$P/02_RENDERED_IMAGES/final
LIST=$P/01_EDITABLE_3D/scripts/rerender_list.txt
again() {  # $1 = camera, rest = extra render_views.py arguments
  local cam=$1; shift
  mkdir -p $OUT/superseded && mv -f $OUT/$cam.png $OUT/$cam.jpg $OUT/superseded/ 2>/dev/null
  blender -b $B --python $S -- --out $OUT --quality final "$@" --cams $cam >> $L 2>&1
}
n=1
while [ "$n" -le "$(wc -l < $LIST)" ]; do
  line=$(sed -n "${n}p" $LIST)
  n=$((n + 1))
  case "$line" in ''|'#'*) continue ;; esac
  again $line
done
blender -b $B --python $S -- --out $OUT --quality final --res 1600x1000 --samples 64 --cams CAM_TOP_Plan >> $L 2>&1
echo QUEUE2_DONE >> $L
