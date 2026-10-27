/** Fictional CC0 MakeHuman adults. No office/layout mutations.
 * `assetBase` is the people directory URL, ending in '/'.
 * Control implementation is owned by the main viewer; this module owns no UI.
 */
function cloneSkeleton(source) {
 const copy=source.clone(true),mapping=new Map();
 function pair(a,b){mapping.set(a,b);for(let i=0;i<a.children.length;i++)pair(a.children[i],b.children[i]);}
 pair(source,copy);
 source.traverse(original=>{if(!original.isSkinnedMesh)return;const mesh=mapping.get(original);const skeleton=original.skeleton.clone();skeleton.bones=original.skeleton.bones.map(b=>mapping.get(b));if(skeleton.bones.some(b=>!b))throw Error('Character bone outside asset hierarchy');mesh.bind(skeleton,original.bindMatrix.clone());mesh.bindMode=original.bindMode;});
 return copy;
}
export async function createPeopleLayer({THREE:T,loader,scene,metadata,walkGrid,assetBase='./people/',extraBlocked=null,frozen=true,activeZones=['Z02'],manifestFile='reception/people-manifest.json'}) {
 const url=p=>new URL(p,new URL(assetBase,location.href)).href;
 const manifest=await fetch(url(manifestFile)).then(r=>{if(!r.ok)throw Error('People manifest HTTP '+r.status);return r.json()});const poses=await fetch(url(manifest.poses||'poses.json')).then(r=>r.json());if(activeZones?.length)manifest.actors=manifest.actors.filter(a=>activeZones.includes(a.zone));manifest.count=manifest.actors.length;frozen=frozen||!!manifest.frozen;
 const group=new T.Group();group.name='Illustrative_office_people';group.userData.disclaimer=manifest.note;scene.add(group);
 let enabled=false,loaded=false,loading=null,clock=0,disposed=false;let actors=[];const originals=[];const colors=[];const axisX=new T.Vector3(1,0,0),axisZ=new T.Vector3(0,0,1),q=new T.Quaternion(),qa=new T.Quaternion(),qb=new T.Quaternion();
 const viewFrustum=new T.Frustum(),viewMatrix=new T.Matrix4(),actorSphere=new T.Sphere();
 const bits=Uint8Array.from(atob(walkGrid.blocked_bits_base64),c=>c.charCodeAt(0)),W=walkGrid.cols,H=walkGrid.rows,R=walkGrid.res,[OX,OZ]=walkGrid.origin_xz;
 function inPoly(x,z,p){let v=false;for(let i=0,j=p.length-1;i<p.length;j=i++){const a=p[i],b=p[j];if((a[1]>z)!=(b[1]>z)&&x<(b[0]-a[0])*(z-a[1])/(b[1]-a[1])+a[0])v=!v}return v}
 const noPeople=(metadata.rooms||[]).filter(r=>manifest.emptyZones.includes(r.zone)).map(r=>r.polygon_xz);
 function blockedGrid(x,z){let c=Math.floor((x-OX)/R),r=Math.floor((z-OZ)/R);if(c<0||r<0||c>=W||r>=H)return true;const i=r*W+c;return !!(bits[i>>3]&(1<<(i&7)))||noPeople.some(p=>inPoly(x,z,p))}
 function capsuleClear(x,z,a){if(extraBlocked&&extraBlocked(x,z,a.def.radius))return false;const grow=Math.max(0,a.def.radius-(walkGrid.walker_radius_m||.15));for(const [dx,dz] of [[0,0],[grow,0],[-grow,0],[0,grow],[0,-grow]])if(blockedGrid(x+dx,z+dz))return false;return true}
 const skinTint=c=>new T.Color(c);
 async function load(){
  if(loaded)return;if(loading)return loading;
  loading=(async()=>{
   const entries=await Promise.all(Object.entries(manifest.assets).map(async([k,v])=>[k,await loader.loadAsync(url(v.file))]));const source=Object.fromEntries(entries);entries.forEach(([,g])=>originals.push(g.scene));
   for(const def of manifest.actors){
    if(disposed)return;const root=cloneSkeleton(source[def.outfit].scene);root.name=def.id;const pivot=new T.Group();pivot.name=def.id+'_placement';pivot.position.fromArray(def.position);pivot.rotation.y=def.yaw;group.add(pivot);pivot.add(root);root.scale.set(def.bodyWidth,def.heightScale,1);const bones={},base={},lod0=[],lod1=[];
    root.traverse(o=>{
     if(o.isBone){bones[o.name]=o;base[o.name]=o.quaternion.clone()}
     if(o.isMesh){
      if(o.morphTargetInfluences){for(let mi=0;mi<Math.min(3,o.morphTargetInfluences.length);mi++)o.morphTargetInfluences[mi]=(def.faceMorph||[])[mi]||0;const grip=o.morphTargetDictionary?.Phone_grip_R;if(grip!==undefined)o.morphTargetInfluences[grip]=def.handGrip??(['phone','phone_seated'].includes(def.task)?1:def.task==='tea'?.65:0);}
      o.castShadow=false;o.receiveShadow=true;o.frustumCulled=true;o.userData.illustrativePerson=def.id;let owner=o;while(owner.parent&&owner!==root&&!/^LOD[01]_/.test(owner.name))owner=owner.parent;const isLow=owner.name.startsWith('LOD1');(isLow?lod1:lod0).push(o);o.userData.peopleLOD=isLow?1:0;o.userData.peopleAllowed=!(def.seated&&owner.name.includes('Long_modest_tunic'));
      const mats=Array.isArray(o.material)?o.material:[o.material];const copies=mats.map(m=>{const n=m.clone();colors.push(n);if(n.name.includes('Skin'))n.color.multiply(skinTint(def.skinTint));if(n.name.includes('Hair'))n.color.multiply(new T.Color(['#6b5547','#29282a','#473931'][Number(def.id.slice(-2))%3]));if(n.name.includes('Garment_top'))n.color.multiply(new T.Color(def.garmentTint));if(n.name.includes('Garment_drape'))n.color.set(def.garmentTint);if(n.name.includes('Garment_trousers'))n.color.multiply(new T.Color(def.lowerTint));n.envMapIntensity=.65;return n});o.material=Array.isArray(o.material)?copies:copies[0];
     }
    });
    // Small self-made generic hand props, with no logos or text.
    const hand=bones.wrist_R;
    if(hand&&['phone','phone_seated'].includes(def.task)){
      const phone=new T.Mesh(new T.BoxGeometry(.058,.114,.009),new T.MeshStandardMaterial({color:0x20252b,roughness:.4}));phone.name='Generic_phone';phone.position.set(0,.10,.025);hand.add(phone);
    }
    if(hand&&def.task==='tea'){
      const cup=new T.Mesh(new T.CylinderGeometry(.033,.027,.067,12),new T.MeshStandardMaterial({color:0xe4ddd1,roughness:.35}));cup.name='Generic_tea_cup';cup.position.set(0,.08,-.025);cup.rotation.x=Math.PI/2;hand.add(cup);
    }
    if(def.task==='walking_files'){
      const folder=new T.Mesh(new T.BoxGeometry(.25,.30,.022),new T.MeshStandardMaterial({color:0x806447,roughness:.85}));folder.name='Generic_file_folder';folder.position.set(0,1.12,.215);root.add(folder);
    }
    const a={def,root,pivot,bones,base,lod0,lod1,pathIndex:0,pathDir:1,wait:0,lastPose:-1,hiddenForVisitor:false,moving:false,walkDistance:0};actors.push(a);applyPose(a,clock,0);
   }
   for(const def of manifest.props||[]){
    const holder=new T.Group();holder.name=def.id;holder.position.fromArray(def.position);holder.rotation.y=def.yaw||0;holder.userData.illustrativeHandProp=true;group.add(holder);
    if(def.type==='badge'){
     const card=new T.Mesh(new T.BoxGeometry(...def.size),new T.MeshStandardMaterial({color:0xe7e9e5,roughness:.45}));card.name='Generic_blank_visitor_badge';holder.add(card);
     const strip=new T.Mesh(new T.BoxGeometry(def.size[0],.0008,.010),new T.MeshStandardMaterial({color:0x326b68,roughness:.6}));strip.position.set(0,def.size[1]/2+.0004,-def.size[2]/2+.007);holder.add(strip);
    }else if(def.type==='notebook'){
     const cover=new T.Mesh(new T.BoxGeometry(...def.size),new T.MeshStandardMaterial({color:0x3e5359,roughness:.86}));cover.name='Generic_meeting_notebook_cover';holder.add(cover);
     const paper=new T.Mesh(new T.BoxGeometry(def.size[0]-.012,.004,def.size[2]-.012),new T.MeshStandardMaterial({color:0xe5dfd1,roughness:.94}));paper.name='Generic_blank_meeting_notes';paper.position.y=def.size[1]/2+.002;holder.add(paper);
     if(def.pen){const pen=new T.Mesh(new T.CylinderGeometry(.0023,.0023,.12,8),new T.MeshStandardMaterial({color:0x303a43,roughness:.55}));pen.name='Generic_unbranded_meeting_pen';pen.rotation.z=Math.PI/2;pen.position.set(0,def.size[1]/2+.0068,.085);holder.add(pen);}
    }else if(def.type==='fabric_book'){
     const cover=new T.Mesh(new T.BoxGeometry(...def.size),new T.MeshStandardMaterial({color:0x465b60,roughness:.85}));holder.add(cover);
     const paper=new T.Mesh(new T.BoxGeometry(def.size[0]-.012,.006,def.size[2]-.012),new T.MeshStandardMaterial({color:0xded8ca,roughness:.95}));paper.position.y=def.size[1]/2+.003;holder.add(paper);
     const spine=new T.Mesh(new T.BoxGeometry(.005,.007,def.size[2]-.015),new T.MeshStandardMaterial({color:0x8c887b,roughness:.9}));spine.position.y=def.size[1]/2+.007;holder.add(spine);
     for(let i=0;i<4;i++){const swatch=new T.Mesh(new T.BoxGeometry(.105,.002,.078),new T.MeshStandardMaterial({color:[0x737d67,0x86705e,0x596d81,0x9a8074][i],roughness:.96}));swatch.name='Unbranded_fabric_swatch_'+i;swatch.position.set(i%2? .095:-.095,def.size[1]/2+.007, i<2?-.055:.055);holder.add(swatch);}
    }
    if(def.owner){group.updateMatrixWorld(true);const owner=group.getObjectByName(def.owner+'_placement');if(owner)owner.attach(holder);}
   }
   loaded=true;group.visible=enabled;
  })();return loading;
 }
 function poseQuat(p,b){const v=p.bones[b];return v?new T.Quaternion(v[1],v[2],v[3],v[0]):new T.Quaternion()}
 function applyPose(a,time,dt){
  const lib=poses[a.def.outfit],p=lib[a.def.pose]||lib.idle;let w0=null,w1=null,blend=0;
  if(a.moving){const phase=((a.walkDistance/.9)*12)%12;const k=Math.floor(phase);blend=phase-k;w0=lib['walk_'+String(k).padStart(2,'0')];w1=lib['walk_'+String((k+1)%12).padStart(2,'0')];}
  for(const [n,b] of Object.entries(a.bones)){
   let v=(w0||p).bones[n];if(a.def.task==='walking_files'&&/arm|wrist/.test(n))v=lib.carry_files.bones[n];if(!v)continue;qa.set(v[1],v[2],v[3],v[0]);
   if(w1&&!(a.def.task==='walking_files'&&/arm|wrist/.test(n))){const w=w1.bones[n];qb.set(w[1],w[2],w[3],w[0]);qa.slerp(qb,blend)}
   b.quaternion.copy(a.base[n]).multiply(qa);
   const t=time+a.def.phase;
   // Small bounded task gestures; no random whole-body wandering.
   if(!frozen&&n==='head'){q.setFromAxisAngle(axisZ,Math.sin(t*.7)*.022);b.quaternion.multiply(q)}
   if(!frozen&&n==='spine01'){q.setFromAxisAngle(axisX,Math.sin(t*1.2)*(a.def.seated?.003:.006));b.quaternion.multiply(q)}
   if(!frozen&&/lowerarm01_[LR]/.test(n)&&['typing','sewing','notes'].includes(a.def.task)){q.setFromAxisAngle(axisX,Math.sin(t*(a.def.task==='sewing'?5:3.2)+(n.endsWith('L')?0:1.5))*.006);b.quaternion.multiply(q)}
   if(!frozen&&n==='wrist_R'&&['greeting','presenting','show_sample'].includes(a.def.task)){q.setFromAxisAngle(axisX,Math.sin(t*.9)*.06);b.quaternion.multiply(q)}
  }
  rootHeight(a,w0?{...p,rootY:w0.rootY+(w1.rootY-w0.rootY)*blend}:p);a.root.updateMatrixWorld(true);a.armSegments=[];for(const side of ['L','R']){const ns=['upperarm01_','lowerarm01_','wrist_'].map(n=>a.bones[n+side]?.getWorldPosition(new T.Vector3()));if(ns.every(Boolean)){const tip=a.bones['wrist_'+side].localToWorld(new T.Vector3(0,.18,0));a.armSegments.push([ns[0],ns[1]],[ns[1],ns[2]],[ns[2],tip]);}}
 }
 function rootHeight(a,p){let y=.01016;if(a.def.seated)y=a.def.support.seatTopY-((p.seatTopY||.49)-(p.rootY||0))*a.def.heightScale;else y+=(p.rootY||0)*a.def.heightScale;a.root.position.y=y;}
 function overlapsActor(a,x,z,r){
  for(const [s,e] of a.armSegments||[]){const dx=e.x-s.x,dz=e.z-s.z,t=Math.max(0,Math.min(1,((x-s.x)*dx+(z-s.z)*dz)/(dx*dx+dz*dz||1)));if((x-s.x-t*dx)**2+(z-s.z-t*dz)**2<(r+.13)**2)return true;}
  const ar=a.def.radius+(a.def.seated?.05:0),dx=x-a.pivot.position.x,dz=z-a.pivot.position.z;if(dx*dx+dz*dz<(r+ar)**2)return true;
  if(a.def.seated){const f=.27,fx=a.pivot.position.x+Math.sin(a.pivot.rotation.y)*f,fz=a.pivot.position.z+Math.cos(a.pivot.rotation.y)*f;if((x-fx)**2+(z-fz)**2<(r+.20)**2)return true;}return false;
 }
 function occupied(x,z,r,except){return actors.some(a=>a!==except&&!a.hiddenForVisitor&&overlapsActor(a,x,z,r));}
 function moveActor(a,dt,player){
  a.moving=false;if(!a.def.path||a.wait>0){a.wait=Math.max(0,a.wait-dt);return}
  const path=a.def.path;const goal=path[Math.max(0,Math.min(path.length-1,a.pathIndex+a.pathDir))];const p=a.pivot.position,dx=goal[0]-p.x,dz=goal[1]-p.z,dist=Math.hypot(dx,dz),step=Math.min(dist,a.def.walkSpeed*dt);if(dist<.005){a.pathIndex+=a.pathDir;if(a.pathIndex>=path.length-1||a.pathIndex<=0){a.pathDir*=-1;a.wait=2.8;}return}
  const nx=p.x+dx/dist*step,nz=p.z+dz/dist*step,look=.25;const lx=p.x+dx/dist*(step+look),lz=p.z+dz/dist*(step+look);
  if(!capsuleClear(nx,nz,a)||occupied(nx,nz,a.def.radius+.06,a)||occupied(lx,lz,a.def.radius+.03,a))return;
  if(player&&(Math.hypot(nx-player.x,nz-player.z)<a.def.radius+.15+.13||Math.hypot(lx-player.x,lz-player.z)<a.def.radius+.15+.13))return;
  p.x=nx;p.z=nz;a.walkDistance+=step;a.moving=step>0;let target=Math.atan2(dx,dz),d=target-a.pivot.rotation.y;while(d>Math.PI)d-=2*Math.PI;while(d<-Math.PI)d+=2*Math.PI;a.pivot.rotation.y+=d*Math.min(1,dt*8);
 }
 function update(dt,{camera,playerPosition,quality='balanced'}={}){
  if(disposed||!enabled||!loaded)return;dt=Math.min(.05,Math.max(0,dt));clock+=dt;const player=playerPosition||camera?.position;if(camera){camera.updateMatrixWorld();viewMatrix.multiplyMatrices(camera.projectionMatrix,camera.matrixWorldInverse);viewFrustum.setFromProjectionMatrix(viewMatrix);}
  for(const a of actors){
   const d=camera?camera.position.distanceTo(a.pivot.position):0;
   // A newly enabled character yields if the visitor already occupies its anchor.
   if(a.hiddenForVisitor&&player&&Math.hypot(a.pivot.position.x-player.x,a.pivot.position.z-player.z)>.62&&!overlapsActor(a,player.x,player.z,.18))a.hiddenForVisitor=false;
   if(!frozen)moveActor(a,dt,player);actorSphere.center.copy(a.pivot.position);actorSphere.center.y+=.85;actorSphere.radius=1.15;a.pivot.visible=!a.hiddenForVisitor&&d<(quality==='low'?14:22)&&(!camera||viewFrustum.intersectsSphere(actorSphere));
   const near=d<(quality==='high'?8:6);for(const o of a.lod0)o.visible=near&&o.userData.peopleAllowed;for(const o of a.lod1)o.visible=!near&&o.userData.peopleAllowed;
   if(!frozen&&a.pivot.visible&&(clock-a.lastPose>(d<7?1/30:1/12))){applyPose(a,clock,dt);a.lastPose=clock}
  }
 }
 async function setEnabled(value,playerPosition){enabled=!!value;group.visible=enabled;if(enabled){await load();if(playerPosition)for(const a of actors)a.hiddenForVisitor=overlapsActor(a,playerPosition.x,playerPosition.z,.18);}return stats()}
 function blocksMovement(x,z,radius=.15){return enabled&&loaded&&occupied(x,z,radius,null)}
 function diagnostics(){return actors.map(a=>({id:a.def.id,zone:a.def.zone,task:a.def.task,radius:a.def.radius,seated:a.def.seated,pathIndex:a.pathIndex,pathDir:a.pathDir,moving:a.moving,hiddenForVisitor:a.hiddenForVisitor,wait:a.wait,walkDistance:a.walkDistance,position:a.pivot.position.toArray(),visible:a.pivot.visible,low:a.lod1.some(o=>o.visible),parts:[...a.lod0,...a.lod1].filter(o=>o.visible).map(o=>({name:o.name,lod:o.userData.peopleLOD,materials:(Array.isArray(o.material)?o.material:[o.material]).map(m=>m.name),skinned:!!o.isSkinnedMesh,vertices:o.geometry.attributes.position.count})),phone:!!a.root.getObjectByName('Generic_phone'),pose:a.def.pose,bones:Object.fromEntries(['root','upperleg01_L','lowerleg01_L','foot_L','head','wrist_R'].map(n=>[n,a.bones[n]?.getWorldPosition(new T.Vector3()).toArray()]))}));}
 function stats(){return{enabled,loaded,frozen,total:manifest.count,visible:actors.filter(a=>a.pivot.visible).length,walkers:manifest.actors.filter(a=>a.path).length,illustrative:true,forbiddenZoneViolations:actors.filter(a=>noPeople.some(p=>inPoly(a.pivot.position.x,a.pivot.position.z,p))).length,status:manifest.status,nativeMacPerformanceTested:false}}
 function dispose(){disposed=true;scene.remove(group);colors.forEach(m=>m.dispose());for(const root of originals)root.traverse(o=>{if(o.geometry)o.geometry.dispose()});actors=[]}
 return{update,setEnabled,blocksMovement,stats,diagnostics,dispose,manifest,group,ready:()=>loading||Promise.resolve()};
}
