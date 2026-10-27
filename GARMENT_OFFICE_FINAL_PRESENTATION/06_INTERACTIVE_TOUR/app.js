import * as THREE from 'https://esm.sh/three@0.164.1';
import { OrbitControls } from 'https://esm.sh/three@0.164.1/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'https://esm.sh/three@0.164.1/examples/jsm/loaders/GLTFLoader.js';

const $=id=>document.getElementById(id);
const IN=0.0254;
const ROOMS=[
['Z01','Entrance lobby','Arrival','CAM_03_Entrance_Lobby',232,60,'A considered arrival space with security and a branded welcome.'],
['Z02','Reception & waiting','Arrival','CAM_01_Reception_A',400,70,'White-oak reception desk, visitor lounge and architectural feature lighting.'],
['Z30','Experience centre','Arrival','CAM_04_Experience_Centre_A',616,-300,'The centre of the buyer journey: product displays, samples and the brand story.'],
['Z03','Visitor passage','Arrival','CAM_02_Reception_B',394,-120,'A dedicated connection between the front-of-house spaces.'],
['Z08','Boardroom','Meeting','CAM_09_Boardroom_A',676,-190,'15-seat executive boardroom with walnut surfaces and acoustic detailing.'],
['Z10','Executive reception','Executive','CAM_17_Executive_Reception',635,40,'Executive waiting and reception with a restrained material palette.'],
['Z11','Director','Executive','CAM_18_Director',780,100,'Private corporate workspace for directors and visitors.'],
['Z12','Managing director','Executive','CAM_07_MD_Office_A',975,100,'Walnut desk, lounge seating and a warm, premium executive atmosphere.'],
['Z13','Executive corridor','Executive','CAM_31_Executive_Corridor',900,27,'The executive connection to reception, boardroom and leadership offices.'],
['Z05','HR & administration','Operations','CAM_19_HR_Admin',262,-212,'Day-to-day administration and people operations.'],
['Z06','Commercial & accounts','Operations','CAM_16_Commercial_Accounts',175,-560,'Finance and commercial workstations with dedicated storage.'],
['Z07','Merchandising','Operations','CAM_11_Merchandising_A',616,-650,'Merchandising, sample review and collaborative buyer communication.'],
['Z09','Audit room','Operations','CAM_27_Audit_Room',175,-870,'A focused room for records, reports and audit meetings.'],
['Z04','Guest workspace','Operations','CAM_26_Guest_Workspace',25,-130,'Dedicated desks for visiting staff and temporary collaboration.'],
['Z14','CAD & technical','Design','CAM_15_CAD_Room',965,-95,'Digital garment design, large-screen workstations and technical plotting.'],
['Z15','Fabric & trim library','Design','CAM_25_Fabric_Library',958,-300,'A systematic library of material, trim, fabric and colour references.'],
['Z16','3D printing lab','Design','CAM_24_3D_Printing_Lab',958,-520,'Compact prototyping and 3D development support.'],
['Z17','Sample development','Design','CAM_23_Sample_Room',958,-690,'Sample-making and pattern-development support for designers.'],
['Z18','Global Design Studio','Design','CAM_13_Design_Studio_A',1240,-760,'Creative garment design studio with a collection table and inspiration displays.'],
['Z19','Sample & material store','Design','CAM_23_Sample_Room',1215,-480,'Organized storage for garment samples and selected materials.'],
['Z20','Staff cafe & pantry','Staff facilities','CAM_20_Staff_Cafe',975,-1100,'A light, welcoming social space for the team.'],
['Z21','Lounge & training','Staff facilities','CAM_21_Lounge_Training',975,-1380,'A flexible space for learning, meetings and relaxed staff interaction.'],
['Z23','Prayer (male)','Staff facilities','CAM_22_Prayer_Male',1240,-1330,'Quiet, simple prayer space.'],
['Z24','Wudu (male)','Staff facilities','CAM_33_Wudu_Male',1240,-1246,'Dedicated wash space connected to the prayer room.'],
['Z25','Prayer (female)','Staff facilities','CAM_30_Prayer_Female',-7,-820,'Separate prayer space for female staff.'],
['Z34','Wudu (female)','Staff facilities','CAM_30_Prayer_Female',-7,-740,'Dedicated ablution provision.'],
['Z26','Washroom (female)','Staff facilities','CAM_29_Washroom_Female',-7,-600,'Staff washroom provision.'],
['Z27','Washroom (male)','Staff facilities','CAM_28_Washroom_Male',-7,-330,'Staff washroom provision.'],
['Z28','Guest WC','Staff facilities','CAM_02_Reception_B',452,-112,'Guest washrooms off the visitor passage.'],
['Z29','Guest workspace WC','Staff facilities','CAM_26_Guest_Workspace',0,-170,'Support washroom for visiting staff.'],
['Z31','Staff corridor','Circulation','CAM_19_HR_Admin',135,-120,'Staff access to administrative rooms.'],
['Z32','North corridor','Circulation','CAM_32_Design_Corridor',1114,-1100,'Passage connecting design areas and staff facilities.'],
['Z33','Central hallway','Circulation','CAM_32_Design_Corridor',614,-867,'Main connection across the central workspace.'],
['Z22','Design corridor','Circulation','CAM_32_Design_Corridor',988,-872,'Circulation through the creative development wing.']
].map(r=>({id:r[0],name:r[1],group:r[2],camera:r[3],x:r[4]*IN,z:r[5]*IN,desc:r[6]}));
const FEATURED=['Z01','Z02','Z30','Z08','Z12','Z07','Z06','Z05','Z14','Z15','Z17','Z18','Z20','Z21','Z23'];
const TOUR=['Z01','Z02','Z30','Z08','Z10','Z12','Z06','Z07','Z14','Z15','Z17','Z18','Z20','Z21','Z23'];
let renderer,scene,camera,controls,office,box,frame,officeCenter,officeSize,ceilingMeshes=[],savedCameras=new Map(),markers=[],raycaster=new THREE.Raycaster(),pointer=new THREE.Vector2();
let selected=null,viewMode='orbit',walkPitch=0,walkYaw=0,keys={},inTour=false,tourPlaying=false,tourIndex=0,tourElapsed=0,transition=null,prevTime=performance.now(),markerVisible=true,ceilingHidden=false;
const modelPath='./model.glb';
let fallbackMode=false,photosEnabled=true,fallbackTimer=null,collisionMeshes=[];
const finalRender=name=>'/renders/'+encodeURIComponent(name)+'.jpg';
const canvas=$('canvas');
const loaderBox=$('progressBox');
const loadText=$('loadText');
const bar=$('progressBar');

function init(){
 bindExtras();
 try{renderer=new THREE.WebGLRenderer({canvas,antialias:true,powerPreference:'high-performance'});}catch(err){activateFallback(err);return;}
 renderer.setPixelRatio(Math.min(devicePixelRatio,1.7));
 renderer.setSize(innerWidth,innerHeight);
 renderer.outputColorSpace=THREE.SRGBColorSpace;
 renderer.toneMapping=THREE.ACESFilmicToneMapping;
 renderer.toneMappingExposure=1.05;
 renderer.setClearColor(0x15241f,1);
 scene=new THREE.Scene();
 scene.background=new THREE.Color('#182a25');
 camera=new THREE.PerspectiveCamera(55,innerWidth/innerHeight,.04,550);
 camera.position.set(50,39,55);
 controls=new OrbitControls(camera,canvas);
 controls.enableDamping=true;
 controls.dampingFactor=.065;
 controls.minDistance=.25;
 controls.maxDistance=130;
 controls.maxPolarAngle=Math.PI*.495;
 scene.add(new THREE.HemisphereLight(0xfdf7ed,0x7f9589,1.15));
 const ambient=new THREE.AmbientLight(0xffffff,.52);scene.add(ambient);
 const sunlight=new THREE.DirectionalLight(0xfff2dc,2.35);sunlight.position.set(20,44,-14);scene.add(sunlight);
 const fill=new THREE.DirectionalLight(0xdceaff,.8);fill.position.set(-20,25,35);scene.add(fill);
 // A neutral studio environment adds realistic reflections to metal, glass and wood PBR surfaces.
 import('https://esm.sh/three@0.164.1/examples/jsm/environments/RoomEnvironment.js').then(({RoomEnvironment})=>{
   try{const pmrem=new THREE.PMREMGenerator(renderer);scene.environment=pmrem.fromScene(new RoomEnvironment(),.045).texture;pmrem.dispose();}catch(e){console.warn('Environment reflection fallback:',e.message);}
 }).catch(e=>console.warn('Optional reflections unavailable:',e.message));
 window.addEventListener('resize',onResize);
 canvas.addEventListener('pointerdown',onCanvasPointer);
 canvas.addEventListener('click',()=>{if(viewMode==='walk'&&document.pointerLockElement!==canvas)canvas.requestPointerLock?.().catch(()=>{});});
 document.addEventListener('mousemove',e=>{if(viewMode==='walk'&&document.pointerLockElement===canvas){walkYaw-=e.movementX*.002;walkPitch=Math.max(-1.3,Math.min(1.3,walkPitch-e.movementY*.002));}});
 document.addEventListener('keydown',e=>{keys[e.code]=true;if(e.code==='Escape'){if(inTour)stopTour();if(viewMode==='walk')setWalk(false)}});
 document.addEventListener('keyup',e=>keys[e.code]=false);
 $('tourBtn').onclick=startTour;
 $('tourStop').onclick=stopTour;
 $('overviewBtn').onclick=overview;
 $('walkBtn').onclick=()=>setWalk(viewMode!=='walk');
 $('ceilingBtn').onclick=toggleCeiling;
 $('resetBtn').onclick=()=>{stopTour();setWalk(false);showMarkers(true);toggleCeiling(false);overview()};
 $('labelsBtn').onclick=()=>showMarkers(!markerVisible);
 $('mobileMenu').onclick=()=>{$('sidebar').classList.toggle('closed')};
 $('search').oninput=renderRooms;
 onResize();
 animate();
 new GLTFLoader().load(modelPath,onLoaded,ev=>{if(ev.total){const pct=Math.min(97,100*ev.loaded/ev.total);bar.style.width=pct+'%';loadText.textContent='Downloading the 3D office… '+Math.round(pct)+'%';}else{loadText.textContent='Downloading the 3D office… '+(ev.loaded/1048576).toFixed(1)+' MB';}},err=>{console.error(err);activateFallback(err);});
}
function onLoaded(gltf){
 office=gltf.scene;
 scene.add(office);
 office.updateMatrixWorld(true);
 box=new THREE.Box3().setFromObject(office);
 officeSize=box.getSize(new THREE.Vector3());
 officeCenter=box.getCenter(new THREE.Vector3());
 // The generated model includes scene cameras; these represent verified camera framing.
 office.traverse(o=>{
   if(o.isCamera){savedCameras.set(o.name,o);o.visible=false;}
   if(o.isMesh){
     const n=o.name.toLowerCase();
     if(/^cl\d{3}\b|ceiling|ceil |clg |steel deck \/ slab|acoustic raft|felt baffle|wood raft|oak raft|slat[_ ]raft/.test(n))ceilingMeshes.push(o);
     if(/\bwall\b|partition|glass|steel column|^(?:iw|pw|np|col)\d{2}/.test(n))collisionMeshes.push(o);
     if(o.material && o.material.isMeshStandardMaterial){o.material.envMapIntensity=1.15;}
   }
 });
 frame=Math.max(officeSize.x,officeSize.z);
 controls.maxDistance=Math.max(90,frame*2.7);
 addMarkers();
 renderRooms();
 toggleCeiling(true);
 overview(true);
 loaderBox.style.display='none';
 $('sidebar').classList.remove('closed');
 updateHUD(null);
 console.info('Loaded office model:',{nodes:office.children.length,cameras:savedCameras.size,ceilingMeshes:ceilingMeshes.length,bounds:officeSize.toArray()});
}
function onResize(){
 camera.aspect=innerWidth/innerHeight;
 camera.updateProjectionMatrix();
 renderer.setSize(innerWidth,innerHeight);
}
function animate(now=performance.now()){
 requestAnimationFrame(animate);
 const dt=Math.min(.075,(now-prevTime)/1000||.016);prevTime=now;
 if(transition && !inTour){transition.t+=dt;const t=Math.min(1,transition.t/transition.d);const smooth=t*t*(3-2*t);
    camera.position.copy(transition.a).lerp(transition.b,smooth);
    controls.target.copy(transition.ta).lerp(transition.tb,smooth);
    camera.quaternion.slerpQuaternions(transition.qa,transition.qb,smooth);
    if(t>=1){transition=null;}
 }
 if(viewMode==='walk' && !inTour){
   const speed=(keys.ShiftLeft||keys.ShiftRight?5.5:2.6)*dt;
   const dir=new THREE.Vector3();
   camera.getWorldDirection(dir);dir.y=0;dir.normalize();
   const right=new THREE.Vector3().crossVectors(dir,new THREE.Vector3(0,1,0)).normalize();
   if(keys.KeyW||keys.ArrowUp)moveWalk(dir.clone().multiplyScalar(speed));
   if(keys.KeyS||keys.ArrowDown)moveWalk(dir.clone().multiplyScalar(-speed));
   if(keys.KeyA)moveWalk(right.clone().multiplyScalar(-speed));
   if(keys.KeyD)moveWalk(right.clone().multiplyScalar(speed));
   if(keys.ArrowLeft)walkYaw+=dt*1.3;
   if(keys.ArrowRight)walkYaw-=dt*1.3;
   camera.rotation.set(walkPitch,walkYaw,0,'YXZ');
   camera.position.y=1.62;
 }else if(inTour){tickTour(dt)}else{controls.update();}
 markers.forEach(m=>{const distant=camera.position.distanceTo(m.position)>10;m.visible=markerVisible&&distant;});
 renderer.render(scene,camera);
}
function updateHUD(room){
 $('zoneTag').textContent=room?room.group:'Entire ground floor';
 $('roomTitle').textContent=room?room.name:'A new vision of work.';
 $('roomDesc').textContent=room?room.desc:'Orbit the model, choose a room, or press Guided tour to experience the complete proposed office.';
}
function renderRooms(){
 const s=$('search').value.trim().toLowerCase();
 const groups=[...new Set(ROOMS.map(r=>r.group))];
 const el=$('rooms');
 el.innerHTML='';
 for(const g of groups){
  const rooms=ROOMS.filter(r=>r.group===g&&(!s||(r.name+' '+r.desc).toLowerCase().includes(s)));
  if(!rooms.length)continue;
  const h=document.createElement('div');h.className='group';h.textContent=g;el.append(h);
  for(const r of rooms){
    const b=document.createElement('button');b.className='room'+(selected?.id===r.id?' selected':'');
    b.innerHTML='<span class="dot"></span><strong></strong><small>'+r.id+'</small>';b.querySelector('strong').textContent=r.name;
    b.onclick=()=>selectRoom(r);
    el.append(b);
  }
 }
}
function cameraPose(r){
 const cam=savedCameras.get(r.camera);
 if(cam){
   cam.updateWorldMatrix(true,false);
   const pos=new THREE.Vector3();const q=new THREE.Quaternion();
   cam.getWorldPosition(pos);cam.getWorldQuaternion(q);
   const forward=new THREE.Vector3(0,0,-1).applyQuaternion(q).normalize();
   const target=pos.clone().addScaledVector(forward,3.6);
   return {pos,q,target};
 }
 const target=new THREE.Vector3(r.x,1.4,r.z);
 const pos=target.clone().add(new THREE.Vector3(-1.8,.32,2.5));
 const q=new THREE.Quaternion().setFromRotationMatrix(new THREE.Matrix4().lookAt(pos,target,new THREE.Vector3(0,1,0)));
 return {pos,q,target};
}
function goToPose(pose,instant=false){
 setWalk(false);
 controls.enabled=true;
 if(instant){camera.position.copy(pose.pos);camera.quaternion.copy(pose.q);controls.target.copy(pose.target);controls.update();return;}
 transition={a:camera.position.clone(),b:pose.pos.clone(),ta:controls.target.clone(),tb:pose.target.clone(),qa:camera.quaternion.clone(),qb:pose.q.clone(),t:0,d:1.35};
}
function selectRoom(r,fromTour=false){
 if(!office&&!fallbackMode)return;
 if(!fromTour)stopTour();
 selected=r;
 updateHUD(r);
 renderRooms();
 if(office){const p=cameraPose(r);goToPose(p,false);}
 if(fallbackMode)showFallback(r);
 else if(photosEnabled&&!fromTour)showReference(r);
 if(innerWidth<781)$('sidebar').classList.add('closed');
}
function overview(instant=false){
 if(!office&&!fallbackMode)return;
 stopTour();if(office)setWalk(false);
 selected=null;renderRooms();updateHUD(null);
 if(fallbackMode){showFallback(null);return;}
 $('renderPanel').hidden=true;
 const centre=officeCenter.clone();
 const diag=Math.max(frame,30);
 const pos=centre.clone().add(new THREE.Vector3(diag*.63,diag*.64,diag*.74));
 const target=centre.clone();
 const q=new THREE.Quaternion().setFromRotationMatrix(new THREE.Matrix4().lookAt(pos,target,new THREE.Vector3(0,1,0)));
 goToPose({pos,target,q},instant===true);
}
function setWalk(v){
 if(v && !office)return;
 if(v && !selected){const r=ROOMS.find(x=>x.id==='Z02');selectRoom(r);}
 viewMode=v?'walk':'orbit';
 controls.enabled=!v;
 if(v){
  const e=new THREE.Euler().setFromQuaternion(camera.quaternion,'YXZ');walkYaw=e.y;walkPitch=e.x;
  transition=null;
  $('renderPanel').hidden=true;
  $('walkBtn').classList.add('active');
  $('walkBtn').textContent='✓ Walk mode';
  $('roomDesc').textContent='Use W A S D to move through the design. Arrow keys turn your view. Press Esc to leave walk mode.';
 }else{
  if(document.pointerLockElement===canvas)document.exitPointerLock?.();
  $('walkBtn').classList.remove('active');$('walkBtn').textContent='♙ Walk mode';
  if(selected)updateHUD(selected);
 }
}
function toggleCeiling(force){
 if(!office)return;
 ceilingHidden=typeof force==='boolean'?force:!ceilingHidden;
 ceilingMeshes.forEach(x=>x.visible=!ceilingHidden);
 $('ceilingBtn').textContent=ceilingHidden?'▤ Show ceilings':'◱ Hide ceilings';
 $('ceilingBtn').classList.toggle('active',ceilingHidden);
}
function showMarkers(v){
 markerVisible=v;markers.forEach(m=>m.visible=v);
 $('labelsBtn').textContent=v?'◉ Room markers':'◎ Show markers';
 $('labelsBtn').classList.toggle('active',v);
}
function addMarkers(){
 // Key-space room markers provide direct click-through; every room also appears in the sidebar.
 for(const r of ROOMS.filter(r=>FEATURED.includes(r.id))){
  const c=document.createElement('canvas');c.width=320;c.height=94;
  const ctx=c.getContext('2d');ctx.fillStyle='rgba(17,39,31,.89)';ctx.beginPath();ctx.roundRect(4,6,312,81,18);ctx.fill();
  ctx.strokeStyle='rgba(215,189,137,.85)';ctx.lineWidth=3;ctx.stroke();
  ctx.fillStyle='#f3e9d2';ctx.font='bold 24px system-ui';ctx.textAlign='center';
  const label=r.name.length>21?r.name.slice(0,21)+'…':r.name;
  ctx.fillText(label,160,58);
  const texture=new THREE.CanvasTexture(c);texture.colorSpace=THREE.SRGBColorSpace;
  const spr=new THREE.Sprite(new THREE.SpriteMaterial({map:texture,depthTest:false,transparent:true,opacity:.94}));
  spr.scale.set(2.8,.82,1);spr.position.set(r.x,3.3,r.z);
  spr.userData.roomId=r.id;spr.renderOrder=500;
  scene.add(spr);markers.push(spr);
 }
}
function onCanvasPointer(event){
 if(viewMode==='walk')return;
 if(!office)return;
 const rect=canvas.getBoundingClientRect();pointer.set((event.clientX-rect.left)/rect.width*2-1,-(event.clientY-rect.top)/rect.height*2+1);
 raycaster.setFromCamera(pointer,camera);
 const hits=raycaster.intersectObjects(markers.filter(x=>x.visible),false);
 if(hits.length){const r=ROOMS.find(x=>x.id===hits[0].object.userData.roomId);if(r)selectRoom(r);}
}
function startTour(){
 if(!office&&!fallbackMode)return;
 if(office)setWalk(false);
 inTour=true;tourPlaying=true;tourIndex=0;tourElapsed=0;transition=null;
 $('renderPanel').hidden=true;
 $('tourPause').textContent='Pause';
 $('tourbar').style.display='block';
 $('sidebar').classList.add('closed');
 $('tourBtn').textContent='◼ End tour';
 $('tourBtn').onclick=stopTour;
 setTourStep(0);
 if(fallbackMode){clearInterval(fallbackTimer);fallbackTimer=setInterval(()=>{if(!inTour||!tourPlaying)return;tourElapsed+=.25;$('tourFill').style.width=((tourIndex+Math.min(tourElapsed/6,1))/TOUR.length*100)+'%';if(tourElapsed>6){if(tourIndex>=TOUR.length-1)stopTour();else setTourStep(tourIndex+1);}},250);}
}
function setTourStep(i){
 tourIndex=i;
 const id=TOUR[i],r=ROOMS.find(x=>x.id===id);
 selected=r;renderRooms();updateHUD(r);
 if(office){const pose=cameraPose(r);camera.position.copy(pose.pos);camera.quaternion.copy(pose.q);controls.target.copy(pose.target);}
 if(fallbackMode)showFallback(r);
 $('tourLabel').textContent=r.name;
 $('tourCount').textContent=(i+1)+' / '+TOUR.length;
 $('tourFill').style.width=(((i)/TOUR.length)*100)+'%';
 tourElapsed=0;
}
function tickTour(dt){
 if(!tourPlaying)return;
 tourElapsed+=dt;
 const room=ROOMS.find(x=>x.id===TOUR[tourIndex]);
 const pose=cameraPose(room);
 // Move gently within the saved room camera's viewing direction while keeping a fixed aim.
 const t=Math.min(1,tourElapsed/6.6),ease=.5-.5*Math.cos(Math.PI*t);
 const right=new THREE.Vector3(1,0,0).applyQuaternion(pose.q);
 camera.position.copy(pose.pos).addScaledVector(right,(ease-.5)*.23);
 camera.quaternion.copy(pose.q);
 $('tourFill').style.width=(((tourIndex+t)/TOUR.length)*100)+'%';
 if(tourElapsed>7.1){
  if(tourIndex+1>=TOUR.length){stopTour();return;}
  const f=document.getElementById('tourfade');
  if(!f){const div=document.createElement('div');div.id='tourfade';Object.assign(div.style,{position:'fixed',inset:'0',zIndex:'8',pointerEvents:'none',background:'#0c1615',opacity:'0',transition:'opacity .28s'});document.body.append(div);}
  const fade=document.getElementById('tourfade');fade.style.opacity='1';
  tourPlaying=false;
  setTimeout(()=>{if(!inTour)return;setTourStep(tourIndex+1);fade.style.opacity='0';tourPlaying=true;},320);
 }
}
function stopTour(){
 if(!inTour)return;
 inTour=false;tourPlaying=false;
 clearInterval(fallbackTimer);fallbackTimer=null;
 $('tourbar').style.display='none';
 $('tourBtn').textContent='▶ Guided tour';$('tourBtn').onclick=startTour;
 const fade=document.getElementById('tourfade');if(fade)fade.style.opacity='0';
 if(controls)controls.enabled=viewMode!=='walk';
}
function moveWalk(delta){
 if(!office||delta.lengthSq()<1e-8)return;
 const length=delta.length();const direction=delta.clone().normalize();
 // Respect actual wall meshes and door openings instead of blocking entire room bounds.
 for(const h of [1.45,.73]){
   const origin=camera.position.clone();origin.y=h;
   raycaster.set(origin,direction);raycaster.far=length+.30;
   const hits=raycaster.intersectObjects(collisionMeshes,false);
   if(hits.length&&hits[0].distance<length+.30)return;
 }
 camera.position.add(delta);
}
function showReference(room){
 const cam=room?.camera||'CAM_ISO_SE';
 $('renderTitle').textContent=room?.name||'The complete office';
 $('renderImg').src=finalRender(cam);
 $('renderPanel').hidden=false;
}
function showFallback(room){
 $('fallbackStage').hidden=false;
 $('fallbackImg').src=finalRender(room?.camera||'CAM_ISO_SE');
 $('fallbackInfo').querySelector('strong').textContent=room?.name||'Photorealistic design gallery';
 $('roomDesc').textContent=room?room.desc:'Browse genuine Cycles images from this architectural model. For the full interactive 3D viewer, open this page in a WebGL-enabled Chrome or Safari browser.';
}
function activateFallback(error){
 console.warn('Live WebGL unavailable, switching to original Cycles-rendered image gallery.',error?.message||error);
 fallbackMode=true;
 $('progressBox').style.display='none';
 renderRooms();showFallback(null);
 $('sidebar').classList.remove('closed');
 $('tourBtn').onclick=startTour;
 $('overviewBtn').onclick=()=>overview();
 $('walkBtn').disabled=true;$('walkBtn').textContent='Walk needs WebGL';
 $('ceilingBtn').disabled=true;$('ceilingBtn').textContent='Ceiling toggle needs WebGL';
 $('resetBtn').onclick=()=>overview();$('labelsBtn').disabled=true;
 $('search').oninput=renderRooms;
 $('mobileMenu').onclick=()=>$('sidebar').classList.toggle('closed');
}
function bindExtras(){
 $('photoBtn').onclick=()=>{photosEnabled=!photosEnabled;$('photoBtn').classList.toggle('active',photosEnabled);if(photosEnabled)showReference(selected);else $('renderPanel').hidden=true;};
 $('photoBtn').classList.add('active');
 $('closeRender').onclick=()=>{$('renderPanel').hidden=true;photosEnabled=false;$('photoBtn').classList.remove('active');};
 $('fullBtn').onclick=()=>{if(!document.fullscreenElement)document.documentElement.requestFullscreen?.().catch(()=>{});else document.exitFullscreen?.();};
 $('tourPrev').onclick=()=>{if(inTour)setTourStep(Math.max(0,tourIndex-1));};
 $('tourNext').onclick=()=>{if(inTour){if(tourIndex>=TOUR.length-1)stopTour();else setTourStep(tourIndex+1);}};
 $('tourPause').onclick=()=>{tourPlaying=!tourPlaying;$('tourPause').textContent=tourPlaying?'Pause':'Resume';};
}
init();