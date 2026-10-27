/** Self-made, unbranded additive dressing. No source mesh is read or modified.
 * Usage: buildOfficeProps(THREE, manifest, { anisotropy: 8 })
 * Viewer integration belongs to Phase 4. Input coordinates are y-up metres.
 */
export function buildOfficeProps(THREE, manifest, options = {}) {
  const root = new THREE.Group(); root.name = 'REALISTIC_SELF_MADE_PROPS';
  const geometries = new Map(), materials = new Map(), batches = new Map(), propBounds = new Map();
  const dummy = new THREE.Object3D(), local = new THREE.Object3D(), world = new THREE.Matrix4();
  const labels = [...new Set(manifest.props.map(p => p.label).filter(Boolean))];
  const atlas = makeAtlas(THREE, labels, options.anisotropy || 4);
  const palette = { ink:'#263239', paper:'#eee9dc', green:'#31594a', clay:'#ac7355', sand:'#b8a78c', white:'#e9e7df', metal:'#8d9393', glass:'#b1c8c5', water:'#4f7275', rubber:'#24282b', fabric:'#718178', yellow:'#bd9a50', red:'#95614d' };
  function mat(name) {
    if (materials.has(name)) return materials.get(name);
    const isMetal=name==='metal', isGlass=name==='glass';
    const m=new THREE.MeshStandardMaterial({name:`selfmade_${name}`,color:name==='label'?'#ffffff':(palette[name]||name),roughness:isMetal?.3:isGlass?.16:name==='paper'?.87:.62,metalness:isMetal?.85:0});
    if (name==='label') {m.map=atlas.texture;m.color.set('white');m.roughness=.9;}
    // Restrained opaque glass avoids per-instance transparent sorting artefacts on low profiles.
    if(isGlass){m.transparent=true;m.opacity=.32;m.depthWrite=false;}
    materials.set(name,m);return m;
  }
  function geo(kind) {
    if(geometries.has(kind))return geometries.get(kind);
    let g;
    if(kind==='box') {
      const s=new THREE.Shape(), r=.025;s.moveTo(-.5+r,-.5);s.lineTo(.5-r,-.5);s.quadraticCurveTo(.5,-.5,.5,-.5+r);s.lineTo(.5,.5-r);s.quadraticCurveTo(.5,.5,.5-r,.5);s.lineTo(-.5+r,.5);s.quadraticCurveTo(-.5,.5,-.5,.5-r);s.lineTo(-.5,-.5+r);s.quadraticCurveTo(-.5,-.5,-.5+r,-.5);
      g=new THREE.ExtrudeGeometry(s,{depth:.95,steps:1,bevelEnabled:true,bevelSegments:1,bevelSize:.025,bevelThickness:.025,curveSegments:2});g.translate(0,0,-.475);g.computeBoundingBox();const size=g.boundingBox.getSize(new THREE.Vector3());g.scale(1/size.x,1/size.y,1/size.z);
    } else if(kind==='cylinder')g=new THREE.CylinderGeometry(1,1,1,16,1);
    else if(kind==='cone')g=new THREE.CylinderGeometry(.4,1,1,16,1);
    else if(kind==='sphere')g=new THREE.SphereGeometry(1,12,8);
    else if(kind==='torus')g=new THREE.TorusGeometry(1,.18,6,16);
    else if(kind==='cup') {
      g=new THREE.LatheGeometry([new THREE.Vector2(.029,0),new THREE.Vector2(.035,.006),new THREE.Vector2(.041,.087),new THREE.Vector2(.036,.089),new THREE.Vector2(.031,.009),new THREE.Vector2(.002,.009)],20);
    } else if(kind.startsWith('label:')) {
      const i=labels.indexOf(kind.slice(6));g=new THREE.PlaneGeometry(1,1);const uv=g.attributes.uv;
      for(let j=0;j<uv.count;j++){const u=uv.getX(j),v=uv.getY(j);uv.setXY(j,((i%4)+u)/4,1-(Math.floor(i/4)+1-v)/8);} uv.needsUpdate=true;
    } else throw new Error(`Unknown self-made geometry ${kind}`);
    geometries.set(kind,g);return g;
  }
  let current;
  function part(kind,material,pos,scale,rotation=[0,0,0]) {
    local.position.set(...pos);local.rotation.set(...rotation);local.scale.set(...scale);local.updateMatrix();
    world.multiplyMatrices(dummy.matrix,local.matrix);
    const key=`${kind}|${material}`;if(!batches.has(key))batches.set(key,{kind,material,matrices:[],zones:[],propIds:[]});
    batches.get(key).matrices.push(world.clone());batches.get(key).zones.push(current.zone);batches.get(key).propIds.push(current.id);
  }
  const box=(m,x,y,z,w,h,d,rot=0)=>part('box',m,[x,y,z],[w,h,d],[0,rot,0]);
  const cyl=(m,x,y,z,r,h)=>part('cylinder',m,[x,y,z],[r,h,r]);
  const label=(txt,x,y,z,w,d,vertical=false)=>txt&&part(`label:${txt}`,'label',[x,y,z],[w,d,1],vertical?[0,0,0]:[-Math.PI/2,0,0]);
  const pen=(x=0,z=0)=>{cyl('metal',x,.004,z,.003,.10);};
  function mug(x=0,z=0,tea=false) {
    if(tea)cyl('white',x,.003,z,.070,.006);
    part('cup','white',[x,tea?.006:0,z],[1,1,1]);
    part('torus','white',[x+.043,.047+(tea?.006:0),z],[.022,.03,.019]);
    cyl('water',x,.070+(tea?.006:0),z,.031,.0015);
  }
  for(const p of manifest.props) {
    current=p;dummy.position.set(...p.position);dummy.rotation.set(0,p.rotationY||0,0);dummy.scale.set(1,1,1);dummy.updateMatrix();
    const w=p.width||.21,d=p.depth||.27;
    switch(p.type) {
      case 'notebook': box('green',0,.011,0,w,.022,d);box('paper',0,.013,0,w-.009,.016,d-.009);label(p.label,0,.0221,0,w*.8,d*.75);box('ink',w*.41,.025,0,.007,.006,d*.7,.05);break;
      case 'pen': part('cylinder','metal',[0,.004,0],[.003,.12,.003],[Math.PI/2,0,0]);break;
      case 'mug':mug();break;
      case 'teacup':mug(0,0,true);break;
      case 'bottle':cyl('green',0,.092,0,.033,.184);cyl('metal',0,.19,0,.026,.02);break;
      case 'glass':part('cup','glass',[0,0,0],[.85,1.4,.85]);cyl('water',0,.058,0,.027,.002);break;
      case 'jug':part('cup','glass',[0,0,0],[1.9,2.65,1.9]);part('torus','glass',[.085,.13,0],[.045,.08,.03]);cyl('water',0,.09,0,.054,.002);break;
      case 'phone':box('ink',0,.018,0,.15,.036,.16);box('rubber',0,.053,-.025,.17,.035,.045);box('green',0,.038,-.005,.07,.002,.04);for(let i=0;i<9;i++)box('sand',(i%3-1)*.018,.038,.035+Math.floor(i/3)*.018,.012,.003,.012);break;
      case 'conferencephone':box('ink',0,.022,0,.24,.044,.18);box('green',0,.045,0,.085,.003,.06);for(let i=0;i<5;i++)box('metal',-.08+i*.04,.046,-.06,.014,.002,.02);break;
      case 'remote':box('ink',0,.009,0,.036,.018,.12);for(let i=0;i<4;i++)cyl('sand',0,.019,-.035+i*.02,.006,.002);break;
      case 'tray':box('metal',0,.004,0,w,.008,d);box('metal',-w/2+.004,.022,0,.008,.044,d);box('metal',w/2-.004,.022,0,.008,.044,d);box('metal',0,.022,-d/2+.004,w,.044,.008);box('paper',0,.016,0,w-.024,.016,d-.024);label(p.label,0,.0241,0,w*.8,d*.6);break;
      case 'books':for(let i=0;i<4;i++) {box(i%2?'sand':'green',.005*i,.014+i*.028,0,.19,.028,.26,(i-1)*.03);box('paper',.005*i,.014+i*.028,.002,.179,.020,.251,(i-1)*.03);}label(p.label,.015,.1121,0,.16,.20);break;
      case 'landscapeframe':box('sand',0,.096,0,.23,.19,.025);box('green',0,.096,.013,.205,.165,.002);box('water',0,.126,.0145,.205,.10,.001);part('sphere','sand',[.06,.14,.016],[.032,.03,.001]);box('ink',0,.022,-.035,.08,.042,.07);break;
      case 'swatches':for(let i=0;i<6;i++)box(['green','sand','clay','ink','fabric','white'][i],i*.008,.002+i*.003,0,.16,.003,.21,(i-2)*.05);break;
      case 'tapemeasure':cyl('yellow',0,.009,0,.033,.018);box('yellow',.065,.002,0,.13,.004,.015);break;
      case 'cuttingmat':box('green',0,.002,0,w,.004,d);for(let i=1;i<8;i++){box('sand',-w/2+w*i/8,.0042,0,.001,.0004,d-.012);box('sand',0,.0042,-d/2+d*i/8,w-.012,.0004,.001);}break;
      case 'patternroll':part('cylinder','paper',[0,.041,0],[.041,.56,.041],[Math.PI/2,0,0]);part('cylinder','sand',[0,.041,.282],[.020,.002,.020],[Math.PI/2,0,0]);break;
      case 'scissors':part('torus','ink',[-.025,.006,.04],[.018,.012,.018],[Math.PI/2,0,0]);part('torus','ink',[.025,.006,.04],[.018,.012,.018],[Math.PI/2,0,0]);box('metal',-.012,.005,-.02,.009,.004,.12,-.18);box('metal',.012,.005,-.02,.009,.004,.12,.18);break;
      case 'filamentspool':cyl('ink',0,.009,0,.095,.018);cyl('clay',0,.042,0,.079,.060);cyl('ink',0,.081,0,.095,.018);cyl('sand',0,.092,0,.020,.004);break;
      case 'trimbox':box('sand',0,.043,0,w,.086,d);box('white',0,.087,0,w+.004,.008,d+.004);label(p.label,0,.0912,0,w*.85,d*.65);break;
      case 'cable':for(let i=0;i<8;i++){const a=i*.32;part('cylinder','rubber',[Math.sin(a)*.052,.003,Math.cos(a)*.052],[.002,.019,.002],[Math.PI/2,0,-a]);}box('ink',0,.005,.059,.012,.01,.025);break;
      case 'soap':box('white',0,.065,0,.055,.13,p.depth||.055);cyl('ink',0,.142,0,.01,.025);box('ink',.014,.156,0,.043,.01,.012);break;
      case 'towels':for(let i=0;i<3;i++)box('white',0,.013+i*.024,0,w,.024,d);break;
      case 'foldedmats':for(let i=0;i<3;i++)box(i%2?'sand':'green',0,.015+i*.03,0,.22,.03,.27);break;
      case 'prayermat':box('fabric',0,.002,0,w,.004,d);for(const x of[-w/2+.025,w/2-.025])box('sand',x,.0042,0,.008,.0004,d-.025);for(const z of[-d/2+.025,d/2-.025])box('sand',0,.0042,z,w-.025,.0004,.008);break;
      case 'shoes':for(const x of[-.065,.065]){part('sphere','rubber',[x,.025,0],[.045,.025,.12]);part('sphere','ink',[x,.055,.015],[.043,.055,.105]);part('sphere','sand',[x,.099,-.04],[.027,.006,.035]);}break;
      case 'kettle':cyl('ink',0,.008,0,.09,.016);part('cone','metal',[0,.123,0],[.09,.23,.09]);part('torus','ink',[.09,.12,0],[.045,.078,.03]);cyl('ink',0,.24,0,.043,.018);part('cone','metal',[-.09,.17,0],[.04,.10,.04],[0,0,.9]);break;
      case 'canister':cyl('sand',0,.07,0,.045,.14);cyl('green',0,.145,0,.047,.014);label(p.label,0,.1519,0,.07,.07);break;
      case 'fruitbowl':part('cup','sand',[0,0,0],[3.2,.7,3.2]);for(let i=0;i<5;i++){const a=i*2.4;part('sphere',i%2?'yellow':'red',[Math.cos(a)*.06,.07,Math.sin(a)*.06],[.038,.035,.038]);}break;
      default:throw new Error(`Unimplemented prop type ${p.type}`);
    }
  }
  let triangles=0,instances=0;
  for(const [key,b] of batches){const g=geo(b.kind),m=mat(b.material),mesh=new THREE.InstancedMesh(g,m,b.matrices.length);mesh.name=`props_${key}`;g.computeBoundingBox();b.matrices.forEach((matrix,i)=>{mesh.setMatrixAt(i,matrix);const bound=g.boundingBox.clone().applyMatrix4(matrix);if(propBounds.has(b.propIds[i]))propBounds.get(b.propIds[i]).union(bound);else propBounds.set(b.propIds[i],bound);});mesh.instanceMatrix.needsUpdate=true;mesh.computeBoundingBox();mesh.computeBoundingSphere();mesh.castShadow=true;mesh.receiveShadow=true;mesh.userData.propZones=b.zones;mesh.userData.selfMade=true;root.add(mesh);triangles+=(g.index?g.index.count:g.attributes.position.count)/3*b.matrices.length;instances+=b.matrices.length;}
  root.userData={sourceLayoutSha256:manifest.source_layout_sha256,licence:'Self-made geometry and canvas artwork, project-authored',propCount:manifest.props.length};
  const stats={props:manifest.props.length,instances,drawCalls:root.children.length,triangles:Math.round(triangles),atlasSize:[2048,2048],rooms:[...new Set(manifest.props.map(p=>p.zone))].length};
  return {group:root,stats,propBounds:Object.fromEntries([...propBounds].map(([id,b])=>[id,{min:b.min.toArray(),max:b.max.toArray()}])),colliders:[],dispose(){for(const g of geometries.values())g.dispose();for(const m of materials.values())m.dispose();atlas.texture.dispose();}};
}
function makeAtlas(THREE, labels, anisotropy) {
  const c=document.createElement('canvas');c.width=c.height=2048;const x=c.getContext('2d');x.fillStyle='#eee9dc';x.fillRect(0,0,2048,2048);
  labels.forEach((s,i)=>{const px=(i%4)*512,py=Math.floor(i/4)*256;x.fillStyle='#233c32';x.fillRect(px+25,py+25,462,5);x.font='bold 30px Arial, sans-serif';x.textAlign='left';x.textBaseline='middle';x.fillText(s,px+30,py+80,450);x.strokeStyle='#c6c3b5';x.lineWidth=2;for(let r=0;r<4;r++){x.beginPath();x.moveTo(px+30,py+125+r*25);x.lineTo(px+480,py+125+r*25);x.stroke();}});
  const texture=new THREE.CanvasTexture(c);texture.colorSpace=THREE.SRGBColorSpace;texture.anisotropy=anisotropy;texture.name='Self-made readable generic labels';return {texture};
}
