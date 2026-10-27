/* Client-safe, CDN-independent photorealistic gallery when WebGL cannot load.
   All images are genuine Cycles renders from the approved office Blender model. */
(() => {
  const css='#officeRescue[hidden]{display:none!important}#officeRescue{position:fixed;inset:0;z-index:50000;background:#101912;color:#f6f3ed;font-family:Inter,system-ui,sans-serif;display:flex;flex-direction:column}#officeRescue *{box-sizing:border-box}#rescueTop{padding:15px 22px;background:#173021;border-bottom:1px solid #c8ae785f;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}#rescueTop strong{display:block;font:24px Georgia,serif}#rescueTop small{display:block;color:#dabf8e;font-size:10px;text-transform:uppercase;letter-spacing:.15em}#rescueTop a,#rescueTop button,#rescueBottom button{color:#f3e5c9;background:#21432a;border:1px solid #baab8166;border-radius:8px;padding:9px 12px;text-decoration:none;cursor:pointer;font-size:12px}#rescueTop a:hover,#rescueTop button:hover,#rescueBottom button:hover{background:#356345}#rescueTop nav{display:flex;gap:8px;flex-wrap:wrap}#rescueBody{display:flex;flex:1;min-height:0}#rescueRooms{width:280px;flex-shrink:0;overflow-y:auto;background:#18271e;border-right:1px solid #bca87e45;padding:14px}#rescueSearch{width:100%;padding:10px;margin-bottom:10px;background:#0e1d14;color:white;border:1px solid #ffffff55;border-radius:8px}#rescueList button{width:100%;display:block;text-align:left;padding:10px;border:1px solid transparent;border-radius:8px;background:transparent;color:#e4e9dc;cursor:pointer}#rescueList button:hover,#rescueList button.on{background:#d2b57b22;border-color:#c9af7e55}#rescueList .group{color:#d8bf8c;font-size:10px;margin:18px 8px 6px;text-transform:uppercase;letter-spacing:.13em}#rescueMain{min-width:0;flex:1;position:relative;display:flex;flex-direction:column}#rescueFigure{position:relative;min-height:0;flex:1;display:flex;align-items:center;justify-content:center;background:#0f1811}#rescueImg{width:100%;height:100%;object-fit:contain}#rescueCaption{position:absolute;top:16px;left:16px;max-width:min(430px,80%);border-radius:12px;padding:14px;background:#0c231bde;border:1px solid #c0b18b66;backdrop-filter:blur(12px)}#rescueCaption h2{font:25px Georgia,serif;margin:0 0 8px}#rescueCaption p{font-size:12px;line-height:1.4;margin:0;color:#d0ddce}#rescueBottom{display:flex;justify-content:center;align-items:center;flex-wrap:wrap;gap:10px;padding:13px;background:#16241b}#rescueBottom .primary{background:#c6ad7c;color:#163122;font-weight:750}#rescueProgress{font-size:11px;color:#e3c28c}#rescueNote{padding:7px 15px;color:#b0c0ad;background:#111b14;text-align:center;font-size:10px}@media(max-width:770px){#rescueTop{padding:10px}#rescueTop strong{font-size:18px}#rescueRooms{width:136px;padding:6px}#rescueList button{font-size:10px;padding:7px}#rescueCaption{padding:8px;left:6px;top:6px;max-width:83%}#rescueCaption h2{font-size:17px}#rescueCaption p{font-size:10px}}';
  const style=document.createElement('style');style.textContent=css;document.head.append(style);
  const root=document.createElement('section');root.id='officeRescue';root.hidden=true;
  root.innerHTML='<header id="rescueTop"><div><strong>Stage II · Design Vision</strong><small>Blender Cycles · Photorealistic Gallery</small></div><nav><a href="/pitch.mp4" target="_blank" rel="noopener">▶ Cinematic film</a><a href="/pitch-deck.pdf" target="_blank" rel="noopener">Design pitch</a><button id="rescueRetry">↻ Try interactive 3D</button></nav></header><div id="rescueBody"><aside id="rescueRooms"><input type="search" id="rescueSearch" placeholder="Find a room…" aria-label="Find office rooms"><div id="rescueList"></div></aside><main id="rescueMain"><div id="rescueFigure"><img id="rescueImg" alt="Actual Blender-rendered view of the proposed office"><div id="rescueCaption"><h2 id="rescueTitle">Whole floor</h2><p id="rescueDesc">Explore the proposed office using its original Blender Cycles images.</p></div></div><div id="rescueBottom"><button id="rescuePrev">‹ Previous</button><button class="primary" id="rescueAuto">▶ Guided photo tour</button><button id="rescueNext">Next ›</button><span id="rescueProgress">Overview</span></div></main></div><div id="rescueNote">This is a gallery of actual project renders, not live 3D. Construction dimensions and engineering approvals remain provisional.</div>';
  document.body.append(root);
  const $=id=>root.querySelector('#'+id);
  const approx=new Set(['Z03','Z19','Z34','Z28','Z29','Z31','Z32','Z33']);
  let manifest={rooms:[],tour:[]},active=null,tourStep=0,timer=null,opened=false;
  const img=c=>'/renders/'+(/^CAM_[a-zA-Z0-9_]+$/.test(c||'')?c:'CAM_ISO_SE')+'.jpg';
  function stop(){if(timer){clearInterval(timer);timer=null}$('rescueAuto').textContent='▶ Guided photo tour'}
  function pick(room,istour=false){
    if(!istour)stop();active=room||null;
    $('rescueTitle').textContent=room?.name||'Whole ground floor';
    $('rescueDesc').textContent=(room?.description||'The proposed visitor, executive, workplace and design-development centre.')+(room&&approx.has(room.id)?' Image shows the nearest available room, not this exact space.':'');
    $('rescueImg').src=img(room?.camera);
    $('rescueProgress').textContent=istour?'Stop '+(tourStep+1)+' / '+manifest.tour.length:room?.name||'Full-floor view';
    root.querySelectorAll('#rescueList button').forEach(b=>b.classList.toggle('on',b.dataset.zone===room?.id));
  }
  function fill(){
    const list=$('rescueList');list.replaceChildren();const query=$('rescueSearch').value.toLowerCase();
    for(const group of [...new Set(manifest.rooms.map(r=>r.group))]){
      const arr=manifest.rooms.filter(r=>r.group===group&&(!query||(r.name+' '+r.description+' '+r.id).toLowerCase().includes(query)));
      if(!arr.length)continue;
      const lab=document.createElement('div');lab.className='group';lab.textContent=group;list.append(lab);
      for(const r of arr){const button=document.createElement('button');button.dataset.zone=r.id;button.textContent=r.name;button.onclick=()=>pick(r);list.append(button)}
    }
  }
  function step(n){
    tourStep=Math.max(0,Math.min(manifest.tour.length-1,n));
    const t=manifest.tour[tourStep],room=manifest.rooms.find(r=>r.id===t.zone);
    pick({...(room||{id:null,name:t.title,description:t.description}),camera:t.camera},true);
  }
  $('rescueRetry').onclick=()=>location.reload();
  $('rescueSearch').oninput=fill;
  $('rescuePrev').onclick=()=>{stop();step(tourStep-1)};
  $('rescueNext').onclick=()=>{stop();step(tourStep+1)};
  $('rescueAuto').onclick=()=>{
    if(timer){stop();return}
    step(0);$('rescueAuto').textContent='■ Stop tour';
    timer=setInterval(()=>{if(tourStep+1>=manifest.tour.length){stop();return}step(tourStep+1)},6500);
  };
  async function activate(reason){
    if(opened||window.__viewerReady)return;opened=true;root.hidden=false;
    try{const response=await fetch('/rooms.json',{cache:'no-store'});if(!response.ok)throw Error('Room data unavailable');manifest=await response.json();}
    catch(e){manifest={rooms:[{id:'Z02',name:'Reception',group:'Arrival',camera:'CAM_01_Reception_A',description:'Visitor reception and corporate welcome.'},{id:'Z08',name:'Boardroom',group:'Meeting',camera:'CAM_09_Boardroom_A',description:'Boardroom design.'}],tour:[{zone:null,title:'Whole Floor',camera:'CAM_ISO_SE',description:'Overview'},{zone:'Z02',title:'Reception',camera:'CAM_01_Reception_A'},{zone:'Z08',title:'Boardroom',camera:'CAM_09_Boardroom_A'}]};}
    fill();const query=new URLSearchParams(location.search).get('room');pick(manifest.rooms.find(r=>r.id===query)||null);
    document.body.dataset.rescueActivated='true';
    document.body.dataset.rescueRoomCount=String(manifest.rooms.length);
    document.body.dataset.rescueReason=String(reason||'').slice(0,120);
  }
  window.__rescuePhotoreal=activate;
  if(window.__lastViewerError)activate(window.__lastViewerError);
  setTimeout(()=>{if(!window.__viewerReady)activate('3D initialization exceeded 90 seconds')},90000);
})();