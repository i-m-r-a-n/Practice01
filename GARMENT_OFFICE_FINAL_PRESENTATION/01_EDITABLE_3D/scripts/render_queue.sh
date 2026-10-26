#!/bin/bash
# Sequential final render queue (one Blender process per batch). Resumable: skips cameras already in final/.
P=/home/user/Practice01/GARMENT_OFFICE_FINAL_PRESENTATION
B=$P/01_EDITABLE_3D/work/render_copy.blend
S=$P/01_EDITABLE_3D/scripts/render_views.py
OUT=$P/02_RENDERED_IMAGES/final
mkdir -p $OUT
run() {  # $1 = quality args, rest = cameras
  local q="$1"; shift
  for cam in "$@"; do
    [ -f "$OUT/$cam.jpg" ] && continue
    blender -b $B --python $S -- --out $OUT $q --cams $cam >> $P/01_EDITABLE_3D/logs/final_renders.log 2>&1
  done
}
run "--quality final --res 1920x1080 --samples 96" CAM_ISO_SE
run "--quality final" CAM_04_Experience_Centre_A CAM_01_Reception_A CAM_09_Boardroom_A CAM_07_MD_Office_A CAM_11_Merchandising_A CAM_13_Design_Studio_A CAM_05_Experience_Centre_B CAM_02_Reception_B CAM_03_Entrance_Lobby CAM_06_Experience_Centre_Detail CAM_08_MD_Office_B CAM_10_Boardroom_B CAM_12_Merchandising_B CAM_14_Design_Studio_B CAM_15_CAD_Room CAM_16_Commercial_Accounts
run "--quality final --samples 96" CAM_17_Executive_Reception CAM_20_Staff_Cafe CAM_21_Lounge_Training CAM_23_Sample_Room CAM_25_Fabric_Library CAM_22_Prayer_Male CAM_28_Washroom_Male CAM_18_Director CAM_19_HR_Admin CAM_24_3D_Printing_Lab CAM_26_Guest_Workspace CAM_27_Audit_Room CAM_29_Washroom_Female CAM_30_Prayer_Female CAM_31_Executive_Corridor CAM_32_Design_Corridor CAM_33_Wudu_Male
run "--quality final --res 1920x1080 --samples 96" CAM_ISO_SW CAM_ISO_Front_Zone CAM_ISO_Design_Wing
echo QUEUE_DONE >> $P/01_EDITABLE_3D/logs/final_renders.log
