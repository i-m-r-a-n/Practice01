/* CDN-independent rescue viewer. Runs only if the main Three.js module never starts.
   This is a photographed Blender Cycles gallery, clearly not a simulated 3D experience. */
(()=>{
'use strict';
const $=id=>document.getElementById(id);
const near=new Set(['Z03','Z19','Z34','Z28','Z29','Z31','Z32','Z33']);
const featured=['Z01','Z02','Z30','Z08','Z10','Z12','Z06','Z07','Z14','Z15','Z17','Z18','Z20','Z21','Z23'];
let rooms=[],active=null,index=0,interval=null,paused=false,rescuing=false;
const imageUrl=cam=>'/renders/'+encodeURIComponent(cam)+'.jpg';
const note=(r)=>r&&near.has(r.id)
?'Nearest available verified Cycles render. Exact room geometry remains in the Blender model.'
:'Original photorealistic Blender Cycles visualization of the proposed office.';
const caption=txt=>{const el=$('fallbackInfo');if(el){el.querySelector('span').textContent=txt;}};
function showRoom(room){
  active=room||null;
  const camera=room?.camera||'CAM_ISO_SE';
  $('fallbackImg').src=imageUrl(camera);
  $('fallbackInfo').querySelector('strong').textContent=room?.name||'Whole-floor overview';
  caption(note(room));
  $('zoneTag').textContent=room?.group||'Blender Cycles image gallery';
  $('roomTitle').textContent=room?.name||'The complete office, imagined.';
  $('roomDesc').textContent=room
  ?'Photo-real concept view. '+note(room)
  :'Browse all 34 proposed office zones through genuine Blender-rendered images. The interactive WebGL model is unavailable in this browser session.';
  for(const b of document.querySelectorAll('.room'))b.classList.toggle('selected',b.dataset.zone===room?.id);
}
function renderRooms(){
  const list=$('rooms');list.innerHTML='';
  const search=$('search').value.trim().toLowerCase();
  const groups=[...new Set(rooms.map(r=>r.group))];
  for(const group of groups){
    const matches=rooms.filter(r=>r.group===group&&r.name.toLowerCase().includes(search));
    if(!matches.length)continue;
    const label=document.createElement('div');label.className='group';label.textContent=group;list.append(label);
    for(const room of matches){
      const b=document.createElement('button');b.className='room';b.dataset.zone=room.id;
      const dot=document.createElement('span');dot.className='dot';
      const title=document.createElement('strong');title.textContent=room.name;
      const small=document.createElement('small');small.textContent=room.id;
      b.append(dot,title,small);b.onclick=()=>{endTour();showRoom(room);if(innerWidth<781)$('sidebar').classList.add('closed')};
      list.append(b);
    }
  }
}
const steps=()=>[null,...featured.map(id=>rooms.find(r=>r.id===id)).filter(Boolean),null];
function applyStep(){
 const plan=steps();const room=plan[index]||null;
 showRoom(room);$('tourLabel').textContent=room?.name||'Complete Ground Floor';
 $('tourCount').textContent=(index+1)+' / '+plan.length;
 $('tourFill').style.width=100*(index+1)/plan.length+'%';
}
function endTour(){
 if(interval){clearInterval(interval);interval=null;}
 $('tourbar').style.display='none';
 $('tourBtn').textContent='▶ Guided tour';
}
function startTour(){
 endTour();paused=false;index=0;
 $('tourbar').style.display='block';$('tourPause').textContent='Pause';$('tourBtn').textContent='◼ End tour';
 applyStep();
 interval=setInterval(()=>{if(paused)return;const last=steps().length-1;if(index>=last){endTour();return;}index++;applyStep();},6500);
}
async function activate(){
 if(rescuing||window.__stage2MainStarted)return;
 rescuing=true;
 try{
  const res=await fetch('/rooms.json',{cache:'no-cache'});
  if(!res.ok)throw Error('Room manifest unavailable');
  rooms=await res.json();
 }catch(e){rooms=[{id:'Z02',name:'Reception & waiting',group:'Arrival',camera:'CAM_01_Reception_A'},{id:'Z30',name:'Experience centre',group:'Arrival',camera:'CAM_04_Experience_Centre_A'},{id:'Z08',name:'Boardroom',group:'Meeting',camera:'CAM_09_Boardroom_A'},{id:'Z18',name:'Global Design Studio',group:'Design',camera:'CAM_13_Design_Studio_A'}];}
 if(window.__stage2MainStarted)return;
 $('progressBox').style.display='none';$('fallbackStage').hidden=false;
 $('statusPill').textContent='Original Cycles room gallery · 3D temporarily unavailable';
 $('fallbackInfo').querySelector('strong').textContent='Original photorealistic design views';
 caption('The real-time 3D viewer did not start. This gallery shows genuine Blender Cycles renders.');
 $('sidebar').classList.remove('closed');
 $('walkBtn').disabled=true;$('ceilingBtn').disabled=true;$('labelsBtn').disabled=true;
 $('walkBtn').textContent='Walk mode needs WebGL';$('ceilingBtn').textContent='Ceilings need WebGL';
 $('tourBtn').onclick=()=>interval?endTour():startTour();
 $('tourStop').onclick=endTour;
 $('tourPrev').onclick=()=>{index=Math.max(0,index-1);applyStep()};
 $('tourNext').onclick=()=>{index=Math.min(steps().length-1,index+1);applyStep()};
 $('tourPause').onclick=()=>{paused=!paused;$('tourPause').textContent=paused?'Resume':'Pause'};
 $('overviewBtn').onclick=()=>{endTour();showRoom(null)};
 $('resetBtn').onclick=()=>{endTour();showRoom(null);$('search').value='';renderRooms()};
 $('mobileMenu').onclick=()=>$('sidebar').classList.toggle('closed');
 $('search').oninput=renderRooms;
 $('photoBtn').disabled=true;
 $('fullBtn').onclick=()=>{if(!document.fullscreenElement)document.documentElement.requestFullscreen?.().catch(()=>{});else document.exitFullscreen?.()};
 renderRooms();showRoom(null);
}
window.__stage2EmergencyPhoto=activate;
window.__stage2EmergencyStop=()=>{endTour();$('fallbackStage').hidden=true};
$('previewNow')?.addEventListener('click',()=>{if(!window.__stage2MainStarted)activate()});
setTimeout(()=>{if(!window.__stage2MainStarted)activate()},13000);
})();