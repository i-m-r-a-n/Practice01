/** Phase 4 only: readable, project-authored display content.
 * Changes cloned screen UV0/materials only; position, normal, index and UV1 stay exact.
 * No viewer integration. Compatible with joined room meshes using material groups.
 */
export function applyOfficeScreenContent(THREE, root, options = {}) {
  root.updateMatrixWorld(true);
  const ownsAtlas=!options.atlasTexture;
  const atlas = options.atlasTexture || createScreenAtlas(THREE, options);
  const touched=[],skipped=[],ownedGeometries=[],ownedMaterials=[];
  const isScreen=m=>/^screen_(ui|brand)(?:$|[_.\s-])/.test(m?.name||'');
  root.traverse(mesh=>{
    if(!mesh.isMesh||mesh.isSkinnedMesh||mesh.userData.officeScreenContentApplied)return;
    const materialList=Array.isArray(mesh.material)?mesh.material:[mesh.material];
    if(!materialList.some(isScreen))return;
    const original=mesh.geometry,position=original.getAttribute('position');
    if(!position)return;
    const index=original.index,groups=original.groups.length?original.groups:[{start:0,count:index?index.count:position.count,materialIndex:0}];
    const selected=[],nonScreen=new Set();
    for(const group of groups){
      const screen=isScreen(materialList[group.materialIndex]);
      for(let k=group.start;k<group.start+group.count;k+=3){const triangle=[0,1,2].map(j=>index?index.getX(k+j):k+j);if(screen)selected.push({ids:triangle,materialIndex:group.materialIndex});else triangle.forEach(i=>nonScreen.add(i));}
    }
    if(!selected.length)return;
    if(selected.some(t=>t.ids.some(i=>nonScreen.has(i)))){skipped.push({mesh:mesh.name,reason:'Screen and physical non-screen faces share UV vertices; do not alter those vertices without splitting only screen data.'});return;}
    // Join triangle islands through quantized physical positions, including UV seam duplicates.
    const parent=selected.map((_,i)=>i),owners=new Map();
    const find=i=>parent[i]===i?i:(parent[i]=find(parent[i]));
    const join=(a,b)=>{a=find(a);b=find(b);if(a!==b)parent[b]=a;};
    for(let i=0;i<selected.length;i++)for(const v of selected[i].ids){const key=[position.getX(v),position.getY(v),position.getZ(v)].map(x=>Math.round(x*1e6)).join(',');if(owners.has(key))join(i,owners.get(key));else owners.set(key,i);}
    const components=new Map();selected.forEach((t,i)=>{const r=find(i);if(!components.has(r))components.set(r,[]);components.get(r).push(t);});
    const geometry=original.clone();ownedGeometries.push(geometry);
    // UV0 may be interleaved. Read through accessors; never touch raw interleaved arrays.
    const oldUV=original.getAttribute('uv'),uv=new THREE.Float32BufferAttribute(position.count*2,2);
    if(oldUV)for(let i=0;i<oldUV.count;i++)uv.setXY(i,oldUV.getX(i),oldUV.getY(i));
    const worldPosition=i=>new THREE.Vector3(position.getX(i),position.getY(i),position.getZ(i)).applyMatrix4(mesh.matrixWorld);
    const zone=options.zone||zoneFor(mesh),up=new THREE.Vector3(0,1,0);
    let cindex=0;
    for(const triangles of components.values()){
      const vertexIds=[...new Set(triangles.flatMap(t=>t.ids))],positions=vertexIds.map(worldPosition),bb=new THREE.Box3().setFromPoints(positions),size=bb.getSize(new THREE.Vector3());
      const planeAxis=size.x<size.z?'x':'z';
      const screenKind=materialList[triangles[0].materialIndex].name.startsWith('screen_brand')?'brand':'ui';
      let tile=screenKind==='brand'&&['Z08','Z18','Z21'].includes(zone)?3:['Z14','Z18'].includes(zone)?2:cindex%2;
      const horizontal=planeAxis==='x'?'z':'x',min=bb.min[horizontal],extent=Math.max(size[horizontal],1e-7),vextent=Math.max(size.y,1e-7);
      if(extent/vextent<.8)tile=4;
      for(const triangle of triangles){
        const [a,b,c]=triangle.ids.map(worldPosition),normal=new THREE.Vector3().subVectors(b,a).cross(new THREE.Vector3().subVectors(c,a)).normalize();
        const front=Math.abs(normal[planeAxis])>.9,sign=planeAxis==='z'?(normal.z>=0?1:-1):(normal.x>=0?-1:1);
        for(const id of triangle.ids){
          if(!front){uv.setXY(id,.999,.001);continue;}
          const p=worldPosition(id);let u=(p[horizontal]-min)/extent;if(sign<0)u=1-u;const v=(p.y-bb.min.y)/vextent;
          const rect=tile===4?[0,640,240,384]:[tile%2*1024,Math.floor(tile/2)*1024,1024,640];uv.setXY(id,(rect[0]+4+u*(rect[2]-8))/2048,1-(rect[1]+4+(1-v)*(rect[3]-8))/2048);
        }
      }
      touched.push({mesh:mesh.name,zone,component:cindex,vertices:vertexIds.length,worldBounds:{min:bb.min.toArray(),max:bb.max.toArray()},content:['sheet','messages','garment-pattern','presentation','portrait-sample-guide'][tile]});cindex++;
    }
    geometry.setAttribute('uv',uv);
    const replacement=materialList.map(source=>{
      if(!isScreen(source))return source;
      const material=source.clone();material.name=source.name;material.map=atlas;material.emissiveMap=atlas;material.color.set('#ffffff');material.emissive.set('#ffffff');material.emissiveIntensity=options.emissiveIntensity??.25;material.roughness=.3;
      // Preserve room RGBM shader hooks attached by the lighting loader.
      material.onBeforeCompile=source.onBeforeCompile;material.customProgramCacheKey=source.customProgramCacheKey;
      material.userData={...source.userData,officeScreenContent:true};material.needsUpdate=true;ownedMaterials.push(material);return material;
    });
    mesh.geometry=geometry;mesh.material=Array.isArray(mesh.material)?replacement:replacement[0];mesh.userData.officeScreenContentApplied=true;
  });
  return {touched,skipped,texture:atlas,dispose(){for(const g of ownedGeometries)g.dispose();for(const m of ownedMaterials)m.dispose();if(ownsAtlas)atlas.dispose();}};
}
function zoneFor(mesh){for(let p=mesh;p;p=p.parent){if(p.userData?.zone)return p.userData.zone;const m=p.name?.match(/(?:^|[_\s-])(Z\d{2})(?:$|[_\s-])/);if(m)return m[1];}return 'Z00';}
function createScreenAtlas(THREE, options){
  const canvas=document.createElement('canvas');canvas.width=canvas.height=2048;const c=canvas.getContext('2d');c.fillStyle='#20292d';c.fillRect(0,0,2048,2048);
  function panel(i,title){const x=i%2*1024,y=Math.floor(i/2)*1024;c.save();c.translate(x,y);c.fillStyle='#f4f3ed';c.fillRect(0,0,1024,640);c.fillStyle='#234f43';c.fillRect(0,0,1024,75);c.fillStyle='#ffffff';c.font='bold 32px Arial, sans-serif';c.textBaseline='middle';c.fillText(title,36,38);c.fillStyle='#77857e';c.font='20px Arial, sans-serif';c.fillText('Sample workspace',36,608);}
  panel(0,'Fabric approvals');const cols=[36,380,610,820];const labels=['Sample','Material','Status','Notes'];c.fillStyle='#203e35';c.font='bold 23px Arial, sans-serif';labels.forEach((s,i)=>c.fillText(s,cols[i],120));c.font='22px Arial, sans-serif';for(let i=0;i<8;i++){const y=178+i*48;c.fillStyle=i%2?'#e8ece7':'#f4f3ed';c.fillRect(22,y-24,980,44);c.fillStyle='#30473f';[`Sample ${String(i+1).padStart(2,'0')}`,['Cotton','Knit','Woven'][i%3],['In review','Pending'][i%2],'Check'].forEach((s,j)=>c.fillText(s,cols[j],y));}c.restore();
  panel(1,'Sample review');c.font='25px Arial, sans-serif';for(let i=0;i<5;i++){const y=135+i*83;c.fillStyle='#e1e8e1';c.fillRect(28,y-25,968,70);c.fillStyle='#263e35';c.fillText(['Fabric selection','Trims and buttons','Size review','Pattern notes','Meeting agenda'][i],48,y);c.fillStyle='#708079';c.font='20px Arial, sans-serif';c.fillText('Draft notes for review',48,y+25);c.font='25px Arial, sans-serif';}c.restore();
  panel(2,'Pattern study');c.strokeStyle='#cbd7d0';c.lineWidth=1;for(let x=30;x<1000;x+=35){c.beginPath();c.moveTo(x,95);c.lineTo(x,560);c.stroke();}for(let y=95;y<570;y+=35){c.beginPath();c.moveTo(30,y);c.lineTo(996,y);c.stroke();}c.strokeStyle='#2a5b4a';c.lineWidth=4;c.beginPath();c.moveTo(240,170);c.lineTo(330,135);c.bezierCurveTo(350,192,400,192,420,135);c.lineTo(510,170);c.lineTo(585,285);c.lineTo(512,325);c.lineTo(470,260);c.lineTo(470,510);c.lineTo(280,510);c.lineTo(280,260);c.lineTo(240,325);c.lineTo(165,285);c.closePath();c.stroke();c.setLineDash([8,6]);c.beginPath();c.moveTo(375,190);c.lineTo(375,505);c.stroke();c.setLineDash([]);c.fillStyle='#33584a';c.font='23px Arial, sans-serif';c.fillText('Plain knit sample',680,200);c.fillText('Front panel',680,244);c.fillText('Draft pattern',680,288);c.restore();
  panel(3,'Design review');c.fillStyle='#274c40';c.font='bold 56px Arial, sans-serif';c.fillText('Samples and materials',60,235);c.font='30px Arial, sans-serif';c.fillText('Fabric  /  Colour  /  Construction',60,320);for(let i=0;i<5;i++){c.fillStyle=['#294e40','#627773','#c6b79c','#b58a72','#263d50'][i];c.fillRect(62+i*134,385,112,85);}const logo=options.clientLogo;if(logo?.image&&/assets\/brand\//.test(logo.provenance||'')){const image=logo.image;const scale=Math.min(180/image.width,75/image.height);c.drawImage(image,790,105,image.width*scale,image.height*scale);}c.restore();
  // Portrait totem occupies otherwise unused atlas padding, preserving letter proportions.
  c.save();c.translate(0,640);c.fillStyle='#f4f3ed';c.fillRect(0,0,240,384);c.fillStyle='#234f43';c.fillRect(0,0,240,70);c.fillStyle='white';c.font='bold 23px Arial, sans-serif';c.fillText('Sample review',15,43);c.fillStyle='#2e5344';c.font='20px Arial, sans-serif';['Fabric','Colour','Construction'].forEach((t,i)=>c.fillText(t,19,115+i*44));['#294e40','#c6b79c','#b58a72'].forEach((col,i)=>{c.fillStyle=col;c.fillRect(19+i*70,250,56,66);});c.fillStyle='#77857e';c.font='14px Arial, sans-serif';c.fillText('Sample workspace',19,355);c.restore();
  const texture=new THREE.CanvasTexture(canvas);texture.name='Self-made generic office display atlas';texture.colorSpace=THREE.SRGBColorSpace;texture.anisotropy=options.anisotropy||4;return texture;
}
