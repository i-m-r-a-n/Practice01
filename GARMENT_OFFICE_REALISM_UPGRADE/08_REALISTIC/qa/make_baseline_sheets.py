"""Measured screenshot comparison sheets; no synthetic after images."""
import hashlib,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import numpy as np

ROOT=Path(__file__).resolve().parents[3]
BASE=Path(__file__).parent/'baseline'
SHEETS=BASE/'comparisons';SHEETS.mkdir(exist_ok=True)
META=json.loads((ROOT/'GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/office_web_metadata.json').read_text())
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
f=ImageFont.truetype(FONT,25);small=ImageFont.truetype(FONT,19)
keys=['CAM_01_Reception_A','CAM_04_Experience_Centre_A','CAM_09_Boardroom_A','CAM_07_MD_Office_A','CAM_11_Merchandising_A','CAM_13_Design_Studio_A']
log={'description':'Same camera comparisons. RGB MAE is a coarse tonal diagnostic, not a photorealism score. Orthographic images use exact metadata projections in a QA-only production scene harness.','cameras':[]}
rows=[]
for c in META['cameras']:
 name=c['name'];reference=ROOT/c['render']['file'];before=BASE/'shots'/('before_'+name+'.png')
 if not before.exists():raise RuntimeError('Missing capture: '+name)
 target=Image.new('RGB',(1280,720),(16,21,17));a=ImageOps.contain(Image.open(reference).convert('RGB'),(1280,720),Image.Resampling.LANCZOS);target.paste(a,((1280-a.width)//2,(720-a.height)//2))
 live=Image.open(before).convert('RGB')
 sheet=Image.new('RGB',(2608,832),(244,245,246));d=ImageDraw.Draw(sheet)
 d.text((16,12),f"{c['room']} | {name}",font=f,fill=(25,35,45))
 d.text((16,53),'Approved Cycles render (offline reference)',font=small,fill=(60,70,80))
 d.text((1312,53),'Current live WebGL — BEFORE (Chromium / SwiftShader)',font=small,fill=(60,70,80))
 sheet.paste(target,(16,92));sheet.paste(live,(1312,92))
 out=SHEETS/(name+'.jpg');sheet.save(out,quality=90)
 aa=np.asarray(target.resize((64,36),Image.Resampling.BOX),dtype=np.float32);bb=np.asarray(live.resize((64,36),Image.Resampling.BOX),dtype=np.float32)
 log['cameras'].append({'camera':name,'room':c['room'],'type':c['type'],'reference':str(reference.relative_to(ROOT)),'before':str(before.relative_to(ROOT)),'rgb_mae_64x36':round(float(np.abs(aa-bb).mean()),3),'reference_mean_rgb':[round(float(x),2) for x in aa.mean(axis=(0,1))],'before_mean_rgb':[round(float(x),2) for x in bb.mean(axis=(0,1))],'sheet':str(out.relative_to(ROOT)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
 if name in keys:rows.append((keys.index(name),sheet))
rows.sort(key=lambda x:x[0]);thumbs=[im.resize((1600,510),Image.Resampling.LANCZOS) for _,im in rows]
contact=Image.new('RGB',(1600,510*len(thumbs)),(244,245,246))
for i,im in enumerate(thumbs):contact.paste(im,(0,510*i))
contact.save(BASE/'six-key-rooms-before-contact.jpg',quality=88)
(BASE/'comparison-metrics.json').write_text(json.dumps(log,indent=2))
print(json.dumps({'sheets':len(log['cameras']),'key_room_sheets':len(rows),'mean_rgb_mae':round(sum(x['rgb_mae_64x36'] for x in log['cameras'])/len(log['cameras']),3)}))
