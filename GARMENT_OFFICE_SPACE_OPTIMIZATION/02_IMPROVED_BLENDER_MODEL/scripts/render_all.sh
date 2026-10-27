#!/bin/sh
# Renders the redesign views one camera per Blender run (resumable: finished JPGs are skipped).
cd "$(dirname "$0")/.."
R=../03_ROOM_RENDERS
for c in CAM_16_Commercial_Accounts CAM_34_Merchandising_Sample_Hub CAM_36_Accounts_Suite CAM_35_Merchandising_Desks CAM_37_Accounts_Records_Discussion CAM_38_Accounts_Public_Corridor CAM_11_Merchandising_A CAM_12_Merchandising_B; do
  [ -f $R/after_with_people/$c.jpg ] || blender -b Optimized_Office_Interior.blend --python scripts/place_people.py -- --then render_views.py --out $R/after_with_people --cams $c --quality final > logs/r_$c.log 2>&1
done
for c in CAM_11_Merchandising_A CAM_12_Merchandising_B CAM_16_Commercial_Accounts CAM_TOP_Z06_Z07 CAM_ISO_Z06_Z07; do
  [ -f $R/after_no_people/$c.jpg ] || blender -b Optimized_Office_Interior.blend --python scripts/render_views.py -- --out $R/after_no_people --cams $c --quality final > logs/r_clean_$c.log 2>&1
done
echo ALL_RENDERS_DONE
