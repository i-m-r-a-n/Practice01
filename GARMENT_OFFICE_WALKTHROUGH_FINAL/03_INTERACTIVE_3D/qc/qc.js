// Camera QC: renders the GLB from each of the 38 render cameras with the exact metadata (matrix, fov, lens shift).
// qc/index.html?glb=../model/Final_Office_Interior_web.glb   then window.__qc.shot(name, width) from the test runner.
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
const qs = new URLSearchParams(location.search);
const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.AgXToneMapping;
renderer.toneMappingExposure = 1.2;
document.body.appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x101418);
scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture;
scene.environmentIntensity = 0.85;
scene.add(new THREE.HemisphereLight(0xfff3e6, 0x45423d, 0.9));
const sun = new THREE.DirectionalLight(0xfff6ec, 1.1); sun.position.set(25, 50, 15); scene.add(sun);
const meta = await (await fetch('../data/office_web_metadata.json')).json();
const t0 = performance.now();
const gltf = await new GLTFLoader().loadAsync(qs.get('glb') || '../model/Final_Office_Interior_web.glb');
const loadSeconds = (performance.now() - t0) / 1000;
scene.add(gltf.scene);
// baked light (if present): same conversion as the viewer
const BX = parseFloat(qs.get('bx')) || 2.0;
let baked = 0;
gltf.scene.traverse((o) => {
  if (!o.isMesh || !o.geometry.attributes.color) return;
  let n = o, k = 0;
  while (n && !k) { k = (n.userData && n.userData.baked_light_scale) || 0; n = n.parent; }
  if (!k) return;
  const m = o.material;
  if (m.transmission > 0 || (m.transparent && m.opacity < 0.95) || (m.emissiveIntensity > 1 && m.emissive && m.emissive.getHex() !== 0)) { m.vertexColors = false; m.needsUpdate = true; return; }
  const col = o.geometry.attributes.color;
  if (!col.userData.lifted) { const a = col.array, mx = a instanceof Uint16Array ? 65535 : a instanceof Uint8Array ? 255 : 1; for (let i = 0; i < a.length; i++) if ((i % col.itemSize) < 3) a[i] = Math.min(mx, a[i] + 0.012 * mx); col.userData.lifted = true; }
  o.material = new THREE.MeshBasicMaterial({ map: m.map, color: m.color.clone().multiplyScalar(k * BX), vertexColors: true, side: m.side, transparent: m.transparent, opacity: m.opacity, alphaTest: m.alphaTest });
  baked++;
});
if (baked) { scene.environmentIntensity = 0.5; for (const l of scene.children) if (l.isLight) l.intensity *= 0.45; renderer.toneMappingExposure = 1.0; }
const overhead = gltf.scene.getObjectByName('WEB_OVERHEAD');
const overheadSet = new Set(meta.names.overhead_threejs);
const overheadNodes = overhead ? [overhead] : [];
if (!overhead) gltf.scene.traverse((o) => { if (overheadSet.has(o.name)) overheadNodes.push(o); });
let meshes = 0, tris = 0;
gltf.scene.traverse((o) => { if (o.isMesh) { meshes++; tris += (o.geometry.index ? o.geometry.index.count : o.geometry.attributes.position.count) / 3; } });
const persp = new THREE.PerspectiveCamera(50, 16 / 9, 0.05, 300);
const ortho = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.05, 300);
function shot(name, width) {
  const c = meta.cameras.find((x) => x.name === name);
  const W = width, H = Math.round(width * c.render.height / c.render.width);
  renderer.setPixelRatio(1); renderer.setSize(W, H);
  let cam;
  if (c.type === 'ORTHO') {
    cam = ortho;
    const big = c.ortho_scale / 2, aspect = W / H;
    const hw = aspect >= 1 ? big : big * aspect, hh = aspect >= 1 ? big / aspect : big;
    Object.assign(cam, { left: -hw, right: hw, top: hh, bottom: -hh });
  } else {
    cam = persp;
    cam.aspect = W / H; cam.fov = c.vfov_deg_render;
    cam.setViewOffset(W, H, 0, -c.shift_y * Math.max(W, H), W, H);
  }
  cam.position.fromArray(c.position);
  cam.quaternion.set(...c.quaternion_xyzw);
  cam.updateProjectionMatrix(); cam.updateMatrixWorld(true);
  for (const o of overheadNodes) o.visible = c.type !== 'ORTHO';
  renderer.render(scene, cam);
  return { name, W, H };
}
window.__qc = { ready: true, shot, loadSeconds, baked, meshes, tris: Math.round(tris), overheadGroup: !!overhead, overheadNodes: overheadNodes.length,
  info: renderer.info.render, gl: renderer.getContext().getParameter(renderer.getContext().VERSION) };
