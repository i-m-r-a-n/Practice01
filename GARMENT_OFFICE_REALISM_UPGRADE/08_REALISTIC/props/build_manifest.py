"""Deterministic, additive dressing anchors from approved office_layout.py.
All source files are read-only. Coordinates reference the builder's actual support heights.
"""
import collections,hashlib,json,math,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[3]; HERE=pathlib.Path(__file__).resolve().parent
SRC=ROOT/'GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/scripts';sys.path.insert(0,str(SRC))
import office_layout as O
props=[]
def add(p,kind,lx=0,ly=0,h=29.5,label=None,angle=0,**extra):
 key,x,y,f,zone,z,_=p;a=math.radians(f);xp=x+math.cos(a)*lx-math.sin(a)*ly;yp=y-math.sin(a)*lx-math.cos(a)*ly
 props.append({'id':f'PROP_{len(props)+1:04d}','type':kind,'zone':zone,'position':[round(xp*.0254,6),round((z+h)*.0254,6),round(yp*.0254,6)],'rotationY':round(math.radians(f+angle),8),'label':label,'support':{'asset':key,'origin_plan_inches':[x,y,z],'source_rotation_deg':f,'local_inches':[lx,ly,h]},**extra})
for p in O.PLACEMENTS:
 key,x,y,f,zone,z,_=p
 if key not in O.ASSETS:continue
 builder,kw,foot,desc=O.ASSETS[key]
 if builder=='bench_desk':
  n=kw.get('n',3);w=kw.get('w',55);d=kw.get('d',27.5)
  for k in range(n):
   cx=-n*w/2+w*(k+.5)
   for side in [-1,1]:
    # Source keyboard at |y|20; monitor at |y|10.5; existing paper left at |y|18.
    add(p,'mug',cx+w/2-5,side*7,29.5,angle=side*15)
    add(p,'notebook',cx+w/2-8,side*(d-8),29.5,label='Approvals' if zone=='Z07' else 'Notes',angle=side*5,width=.16,depth=.20)
    add(p,'bottle',cx-w/2+4.5,side*7.5,29.5)
    add(p,'cable',cx+7,side*5.5,29.5,angle=side*20)
 if builder=='single_desk':
  w=kw.get('w',63);d=kw.get('d',31.5)
  add(p,'notebook',-w/2+7,-d/2+8,29.5,label='Visitors' if zone=='Z01' else 'Notes',angle=-6,width=.18,depth=.22)
  add(p,'mug',w/2-5,0,29.5,angle=20)
  if zone!='Z01':add(p,'tray',w/2-9,d/2-6,29.5,label='Approvals',width=.23,depth=.18)
 if builder=='exec_desk':
  w=kw.get('w',78);d=kw.get('d',36)
  add(p,'teacup',w/2-10,-d/2+8,29.5)
  add(p,'tray',w/2-12,d/2-8,29.5,label='Documents',width=.25,depth=.28)
 if builder=='reception_desk':
  add(p,'notebook',22,-10,42,label='Visitors',width=.22,depth=.16,angle=-4)
  add(p,'pen',37,-9,42,angle=8)
  add(p,'phone',-35,4,29.7)
  add(p,'tray',-8,-10,42,label='Visitor badges',width=.21,depth=.15)
 if builder=='boardroom_table':
  for x0 in [-80,-32,32,80]:
   for side in [-1,1]:
    add(p,'notebook',x0,side*16,29.5,label='Meeting notes',angle=side*2,width=.19,depth=.23)
    add(p,'glass',x0+13,side*16,29.5)
  add(p,'conferencephone',0,0,29.5)
  add(p,'jug',-65,0,29.5)
  add(p,'remote',65,0,29.5)
  add(p,'cable',28,0,29.5)
 if builder=='round_table':
  h=kw.get('h',29.5);dia=kw.get('dia',32)
  if dia>=28:add(p,'notebook',-dia*.14,0,h,label='Company profile' if zone=='Z02' else 'Notes',angle=12,width=min(.21,dia*.0254*.4),depth=.22)
  add(p,'teacup',dia*.22,0,h)
 if builder=='table':
  w=kw['w'];d=kw['d'];h=kw.get('h',29.5)
  if key in ['table_pattern','table_layout','table_trend']:
   add(p,'cuttingmat',-w*.12,0,h,width=w*.0254*.50,depth=d*.0254*.60)
   add(p,'patternroll',w*.33,0,h,angle=90)
   add(p,'scissors',w*.06,-d*.12,h+.004/.0254)
   add(p,'swatches',-w*.25,d*.08,h+.004/.0254)
  elif key=='table_review':
   # D65 booth occupies local x +/-16, y[-15,7]; use far corners.
   add(p,'swatches',-23,7,h);add(p,'notebook',22,5,h,label='Fabric approvals',width=.18,depth=.20)
  else:
   for offset in [-w*.28,w*.28]:
    add(p,'notebook',offset,-d*.20,h,label='Samples' if zone in ['Z07','Z18'] else 'Notes',width=.20,depth=.23,angle=5)
    add(p,'mug',offset,d*.23,h)
   if key=='table_dining':add(p,'fruitbowl',0,0,h)
 if builder=='material_table':
  # Existing yarn at left, swatches central, garments right. Narrow north strip remains clear.
  add(p,'notebook',32,14,kw.get('h',34),label='Fabric samples',width=.24,depth=.18,angle=2)
  add(p,'tapemeasure',57,14,kw.get('h',34))
 if builder=='cabinet' and key not in ['mfp','dry_cabinet','tall_cab_90','shoe_rack','shoe_rack_36','printer_bench']:
  w=kw['w'];d=kw['d'];h=kw['h']+(1 if kw.get('top') else 0)
  if key=='ec_counter':
   for offset in [-130,-50,35,125]:add(p,'swatches',offset,0,h)
   add(p,'notebook',-95,0,h,label='Knit samples',width=.22,depth=.24)
  elif key=='review_counter':
   for offset in [-100,-40,30,100]:add(p,'swatches',offset,0,h)
  elif key.startswith('credenza') or key=='console':
   add(p,'books',-w*.30,0,h,label='Reference')
   add(p,'landscapeframe',w*.27,0,h)
  elif key=='post_bench':
   for offset in [-35,-12,12,35]:add(p,'filamentspool',offset,0,h)
  elif key in ['filing_96','filing_120','under_window_110','plan_chest']:
   add(p,'books',-w*.28,0,h,label='Orders' if zone in ['Z06','Z07'] else 'Reference')
   add(p,'tray',w*.25,0,h,label='Approvals',width=.27,depth=.28)
 if builder=='shelving' and zone=='Z19':
  # Keep existing shelf-fill; put a small labelled trim box on the empty top board only.
  add(p,'trimbox',0,0,kw['h'],label='Trims - buttons',width=.28,depth=.23)
 if key=='shoe_rack':
  # Source cabinet is solid despite schedule "shoe rack": shoes on top, no fictitious open shelves.
  add(p,'shoes',-8,0,kw['h']);add(p,'foldedmats',9,0,kw['h'])
 if builder=='pantry_run':
  add(p,'kettle',-37,0,35.5)
  add(p,'canister',-22,2,35.5,label='Tea')
  add(p,'canister',22,2,35.5,label='Sugar')
  add(p,'teacup',33,-5,35.5)
 if builder=='vanity':
  L=kw.get('L',60);D=kw.get('D',21)
  # Source bowls centered x +/-15 (two) or 0 (one), radius7.6. Edge shelf is free.
  add(p,'soap',-L/2+3.5,D/2-4,32)
  add(p,'towels',L/2-3.5,0,32,width=.12,depth=.19)
 if builder=='wudu_station':
  # Dispenser rests on 2-inch deep upper wall ledge, no change to taps/fixtures.
  add(p,'soap',-kw['L']/2+3,16.7,34,depth=.03)
# Floor mats aligned with existing local room axes; no declaration of verified Qibla.
for zone,centres in [('Z23',[(1200,-1380),(1250,-1380),(1300,-1380)]),('Z25',[(-27,-834),(14,-834)])]:
 for x,y in centres:
  add(('approved_floor',x,y,0,zone,0,None),'prayermat',0,0,.4,width=.60,depth=1.08)
# One thin fabric workpiece on the active F206 sewing bed; existing prop IDs remain stable.
# Actual flat bed is bounded by local x[-7.4,11.4], y[-2.4,2.4] inches;
# keep short of the solid machine column at x8in and clear of bevels.
sewing_active=next(p for p in O.PLACEMENTS if p[0]=='sewing' and p[1:3]==(900,-770))
add(sewing_active,'sewingcloth',0,0,32.5,width=.36,depth=.11,thickness=.0012)
# Every room explicitly covered. Empty circulation zones keep approved signs/fire equipment only.
counts=collections.Counter(p['zone']for p in props)
rooms=[{'zone':z[1],'name':z[2].replace('\n',' '),'additional_props':counts[z[1]],'treatment':'Add surface-anchored everyday objects' if counts[z[1]] else 'Retain approved corridor signs, fittings and clear walking route; no unapproved wall fixtures or floor clutter','existing_placement_count':sum(p[4]==z[1]for p in O.PLACEMENTS)}for z in O.ZONES]
out={'version':1,'status':'Prepared additive Phase 4 manifest; geometry audit only, integration and visual checks pending','units':'metres; viewer y-up, original approved coordinate origin','source_layout_sha256':hashlib.sha256((SRC/'office_layout.py').read_bytes()).hexdigest(),'seed':20261027,'source_rules':'No original mesh transforms, chairs, doors, lighting or furniture altered. All additions rest on recorded source surfaces. No staff, game assets or third-party brands.','props':props,'room_coverage':rooms,'limitations':['No source vertex/UV edits','Visual framing, prop/source component collisions and AO must be verified after integration','New props are not included in the Phase 1 atlas; use grounded AO or rebake before claiming baked prop contact shadows','Wall accessories, new sockets, switches and fire equipment deferred without source plan positions','Existing source shoe racks are solid cabinets; male top used, female additions omitted because source rack straddles room boundary','All surfaces use declared actual builder heights; floor finish top is 0.01016m, not zero']}
(HERE/'office-props-manifest.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'props':len(props),'rooms_with_additions':len(counts),'all_rooms_reviewed':len(rooms),'types':dict(collections.Counter(p['type']for p in props))},indent=2))
