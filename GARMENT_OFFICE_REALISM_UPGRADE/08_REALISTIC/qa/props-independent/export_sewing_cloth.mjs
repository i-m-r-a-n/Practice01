import fs from 'node:fs';import path from 'node:path';import {fileURLToPath}from'node:url';import{buildOfficeProps}from'../../props/office-props.mjs';
const here=path.dirname(fileURLToPath(import.meta.url)),root=path.resolve(here,'../../../..');
const source=fs.readFileSync(path.join(root,'GARMENT_OFFICE_WALKTHROUGH_FINAL/03_INTERACTIVE_3D/vendor/three/build/three.module.js'));
const T=await import('data:text/javascript;base64,'+source.toString('base64'));
globalThis.document={createElement:()=>({width:0,height:0,getContext:()=>new Proxy({},{get:()=>()=>{}})})};
const mf=JSON.parse(fs.readFileSync(path.join(here,'../../props/office-props-manifest.json')));mf.props=mf.props.filter(p=>p.type==='sewingcloth');const r=buildOfficeProps(T,mf),vertices=[],indices=[],M=new T.Matrix4(),v=new T.Vector3();
for(const mesh of r.group.children){const g=mesh.geometry;for(let k=0;k<mesh.count;k++){mesh.getMatrixAt(k,M);const off=vertices.length;for(let i=0;i<g.attributes.position.count;i++){v.fromBufferAttribute(g.attributes.position,i).applyMatrix4(M);vertices.push(v.toArray());}const ix=g.index?Array.from(g.index.array):Array.from({length:g.attributes.position.count},(_,i)=>i);indices.push(...ix.map(i=>i+off));}}
fs.writeFileSync(path.join(here,'sewing-cloth-actual-mesh.json'),JSON.stringify({props:mf.props,vertices,indices,bounds:r.propBounds,stats:r.stats}));console.log(JSON.stringify(r.stats));r.dispose();
