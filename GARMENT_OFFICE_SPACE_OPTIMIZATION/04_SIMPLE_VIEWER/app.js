// Stage II - Interactive Office Experience (three.js r169, vendored: no CDN).
// Simple client viewer built on the 03_INTERACTIVE_3D engine: home screen with three choices, one-click room views,
// quick / complete guided tours, natural look-around (drag = grab the view, like a 360 photo), optional walk,
// presentation mode. Model: the space-optimisation web GLB (Z06 / Z07 option B) with Cycles light baked on the shell.
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { GTAOPass } from 'three/addons/postprocessing/GTAOPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

window.__viewerStarted = true;
const $ = (id) => document.getElementById(id);
const qs = new URLSearchParams(location.search);
const CFG = window.__TOUR_CONFIG || {};
const BASE = CFG.base || 'assets/';
const ROOT = CFG.root ?? '../../';                    // repository root: render files are listed relative to it in the metadata
const MODELS = qs.get('model') ? [qs.get('model')] : CFG.models || [BASE + 'Optimized_Office_Interior_web_baked.glb'];
const S = { mode: 'loading', ready: false, room: null, atCam: null, tour: null, errors: [], counts: {}, present: false, view: 'iso' };
window.__viewer = S;

// ------------------------------------------------------------------ photo fallback (no WebGL / model failed)
window.__fallback = async function () {
  try {
    const m = window.__TOUR_DATA ? window.__TOUR_DATA.meta : await (await fetch(BASE + 'office_web_metadata.json')).json();
    const f = $('fallback'); if (f.childElementCount) return;
    const cams = Object.fromEntries(m.cameras.map((c) => [c.name, c]));
    const h = document.createElement('p'); h.style.gridColumn = '1 / -1'; h.style.margin = '0';
    h.textContent = 'Meanwhile, these are the photorealistic Blender renders (still images) of the main rooms:'; f.appendChild(h);
    for (const st of m.quick_tour || m.tour) {
      const c = cams[st.camera]; if (!c || !c.render) continue;
      const fig = document.createElement('figure');
      fig.innerHTML = `<img loading="lazy" alt=""><figcaption></figcaption>`;
      fig.querySelector('img').src = ROOT + c.render.file; fig.querySelector('figcaption').textContent = st.title + ' (still image)';
      f.appendChild(fig);
    }
    f.classList.remove('hidden');
  } catch (e) { /* metadata not reachable either: the error text stays */ }
};

// ------------------------------------------------------------------ renderer
const probe = document.createElement('canvas');
if (!(probe.getContext('webgl2') || probe.getContext('webgl'))) {
  window.__fail('WebGL is not available in this browser, so the interactive 3D model cannot be shown. Turn on hardware acceleration or use a current Safari, Chrome, Edge or Firefox.');
  throw new Error('no WebGL');
}
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
const scale = Math.min(1, Math.max(0.25, parseFloat(qs.get('scale')) || 1));
const QUALITY = { high: 2, balanced: 1.5, low: 1 };
let quality = 'balanced';
try { quality = localStorage.getItem('tourQuality') || (matchMedia('(pointer: coarse)').matches && innerWidth < 900 ? 'low' : 'balanced'); } catch (e) { /* storage blocked */ }
if (!QUALITY[quality]) quality = 'balanced';
function applyQuality(q) {
  quality = q;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, QUALITY[q]) * scale);
  renderer.setSize(innerWidth, innerHeight);
  try { localStorage.setItem('tourQuality', q); } catch (e) { /* storage blocked */ }
  if (aoWanted() && !AO) setupAO(); if (!aoWanted()) AO = null; sizeAO();
  needsRender = true;
}
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, QUALITY[quality]) * scale);
renderer.setSize(innerWidth, innerHeight);
renderer.setClearColor(0x000000, 0);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.AgXToneMapping;          // the renders use Blender's AgX view transform
$('app').appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture;
const hemi = new THREE.HemisphereLight(0xfff1e0, 0x4a4640, 0.5);
const sun = new THREE.DirectionalLight(0xfff3e4, 1.2);
sun.position.set(30, 60, 25);
scene.add(hemi, sun, sun.target);
const camera = new THREE.PerspectiveCamera(35, innerWidth / innerHeight, 0.05, 600);
const controls = new OrbitControls(camera, renderer.domElement);
Object.assign(controls, { enableDamping: true, dampingFactor: 0.08, minDistance: 6, maxDistance: 120, maxPolarAngle: Math.PI * 0.47, screenSpacePanning: true, autoRotateSpeed: 0.35 });
let needsRender = true;
controls.addEventListener('change', () => { needsRender = true; });
let lookPreset = 'outside';
function look(preset) {
  lookPreset = preset;
  const L = BAKED ? (preset === 'inside' ? { exp: 1.0, env: 0.5, hemi: 0.45, sun: 0.35 } : { exp: 0.95, env: 0.5, hemi: 0.5, sun: 0.9 })
    : preset === 'inside' ? { exp: 1.1, env: 0.55, hemi: 0.36, sun: 0.55 } : { exp: 0.95, env: 0.55, hemi: 0.5, sun: 1.35 };
  renderer.toneMappingExposure = L.exp; scene.environmentIntensity = L.env; hemi.intensity = L.hemi; sun.intensity = L.sun;
  needsRender = true;
}

// ------------------------------------------------------------------ loading
function progress(loaded, total, label) {
  const p = total ? Math.min(100, Math.round((loaded / total) * 100)) : 0;
  $('loadBar').style.width = p + '%';
  $('loadText').textContent = `${label}  ${(loaded / 1e6).toFixed(1)} / ${(total / 1e6).toFixed(1)} MB`;
}
async function getJSON(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(`${url}: HTTP ${r.status}`);
  return r.json();
}
function loadModel(url) {
  return new Promise((res, rej) => {
    let last = Date.now();
    const stall = setInterval(() => { if (Date.now() - last > 45000) $('loadText').textContent = 'The connection is slow - still loading the model...'; }, 5000);
    new GLTFLoader().load(url, (g) => { clearInterval(stall); res(g); },
      (e) => { last = Date.now(); progress(e.loaded, e.lengthComputable ? e.total : 20e6, 'Loading the 3D model'); },
      (err) => { clearInterval(stall); rej(err); });
  });
}
let meta, grid, gltf;
try {
  if (window.__TOUR_DATA) ({ meta, grid } = window.__TOUR_DATA);
  else [meta, grid] = await Promise.all([getJSON(BASE + 'office_web_metadata.json'), getJSON(BASE + 'walk_grid.json')]);
  for (let i = 0; i < MODELS.length && !gltf; i++) {
    try { gltf = await loadModel(MODELS[i]); } catch (e) { S.errors.push(`${MODELS[i]}: ${e.message || e}`); if (i === MODELS.length - 1) throw e; }
  }
} catch (err) {
  window.__fail(`Could not load the 3D model (${err.message || err}). Open this page through a web server (see README).`);
  throw err;
}
$('loadTitle').textContent = 'Preparing the scene...';

// ------------------------------------------------------------------ model: groups, baked light, draw-call merge
const model = gltf.scene;
scene.add(model);
const overhead = model.getObjectByName('WEB_OVERHEAD') || new THREE.Group();
const interior = model.getObjectByName('WEB_INTERIOR') || model;
const BX = parseFloat(qs.get('bx')) || CFG.bakedExposure || 2.0;
const LIGHT_FLOOR = 0.012;
let BAKED = false;
{
  const cache = new Map(), lifted = new WeakSet();
  model.traverse((o) => {
    if (!o.isMesh || !o.geometry.attributes.color) return;
    let n = o, k = 0;
    while (n && !k) { k = (n.userData && n.userData.baked_light_scale) || 0; n = n.parent; }
    if (!k) return;
    const m = o.material;
    if (m.transmission > 0 || (m.transparent && m.opacity < 0.95) || (m.emissiveIntensity > 1 && m.emissive && m.emissive.getHex() !== 0)) {
      m.vertexColors = false; m.needsUpdate = true; return;
    }
    // COLOR_0 may be interleaved with POSITION / NORMAL (glTF byteStride): only ever touch it through the accessors
    const col = o.geometry.attributes.color;
    if (!lifted.has(col)) {
      const f = (v) => Math.min(1, v + LIGHT_FLOOR);
      for (let i = 0; i < col.count; i++) col.setXYZ(i, f(col.getX(i)), f(col.getY(i)), f(col.getZ(i)));
      lifted.add(col);
      if (col.isInterleavedBufferAttribute) col.data.needsUpdate = true; else col.needsUpdate = true;
    }
    if (!cache.has(m)) {
      cache.set(m, new THREE.MeshBasicMaterial({ name: m.name + '_baked', map: m.map, color: m.color.clone().multiplyScalar(k * BX),
        vertexColors: true, side: m.side, transparent: m.transparent, opacity: m.opacity, alphaTest: m.alphaTest }));
    }
    o.material = cache.get(m);
    BAKED = true;
  });
}
for (const o of collect(model)) if (o.material.transmission > 0) o.material.envMapIntensity = 1.0;
function collect(root) { const a = []; root.traverse((o) => { if (o.isMesh) a.push(o); }); return a; }
function floatGeometry(g) {                           // dequantize (KHR_mesh_quantization) so meshes can be merged
  const out = new THREE.BufferGeometry();
  for (const [name, a] of Object.entries(g.attributes)) {
    const n = a.count, s = a.itemSize, arr = new Float32Array(n * s);
    const get = [a.getX, a.getY, a.getZ, a.getW];
    for (let i = 0; i < n; i++) for (let k = 0; k < s; k++) arr[i * s + k] = get[k].call(a, i);
    out.setAttribute(name, new THREE.BufferAttribute(arr, s));
  }
  if (g.index) out.setIndex(new THREE.BufferAttribute(Uint32Array.from(g.index.array), 1));
  return out;
}
function mergeByMaterial(root) {
  root.updateMatrixWorld(true);
  const inv = new THREE.Matrix4().copy(root.matrixWorld).invert();
  const buckets = new Map();
  root.traverse((o) => {
    if (!o.isMesh || o.isInstancedMesh || Array.isArray(o.material)) return;
    const g = o.geometry;
    const key = `${o.material.uuid}|${Object.keys(g.attributes).sort().join(',')}|${g.index ? 1 : 0}`;
    if (!buckets.has(key)) buckets.set(key, []);
    buckets.get(key).push(o);
  });
  let before = 0, after = 0;
  for (const list of buckets.values()) {
    before += list.length;
    if (list.length < 2) { after += 1; continue; }
    const geos = list.map((o) => floatGeometry(o.geometry).applyMatrix4(new THREE.Matrix4().multiplyMatrices(inv, o.matrixWorld)));
    const merged = mergeGeometries(geos, false);
    if (!merged) { after += list.length; continue; }
    merged.computeBoundingSphere();
    const mesh = new THREE.Mesh(merged, list[0].material);
    mesh.name = 'merged_' + list[0].material.name;
    for (const o of list) o.removeFromParent();
    root.add(mesh);
    after += 1;
  }
  return [before, after];
}
let drawCalls = null;
if (qs.get('merge') !== '0' && interior !== model) {
  try { const a = mergeByMaterial(interior), b = mergeByMaterial(overhead); drawCalls = { before: a[0] + b[0], after: a[1] + b[1] }; }
  catch (e) { S.errors.push('merge skipped: ' + e.message); }
}

// ------------------------------------------------------------------ ambient occlusion on the still view
let AO = null;
const aoWanted = () => (qs.get('ao') ? qs.get('ao') !== '0' : quality !== 'low');
function setupAO() {
  try {
    const size = renderer.getDrawingBufferSize(new THREE.Vector2());
    const rt = new THREE.WebGLRenderTarget(size.x, size.y, { type: THREE.HalfFloatType, samples: 4 });
    const composer = new EffectComposer(renderer, rt);
    composer.setPixelRatio(renderer.getPixelRatio()); composer.setSize(innerWidth, innerHeight);
    composer.addPass(new RenderPass(scene, camera));
    const gtao = new GTAOPass(scene, camera, innerWidth, innerHeight);
    gtao.updateGtaoMaterial({ radius: 0.35, distanceExponent: 1, thickness: 1, scale: 1, samples: 16, distanceFallOff: 1, screenSpaceRadius: false });
    gtao.updatePdMaterial({ lumaPhi: 10, depthPhi: 2, normalPhi: 3, radius: 4, radiusExponent: 1, rings: 2, samples: 16 });
    const hideSeeThrough = gtao.overrideVisibility.bind(gtao);
    gtao.overrideVisibility = function () {
      hideSeeThrough();
      scene.traverse((o) => { if (o.isMesh && o.material && (o.material.transmission > 0 || (o.material.transparent && o.material.opacity < 0.95))) o.visible = false; });
    };
    composer.addPass(gtao);
    composer.addPass(new OutputPass());
    AO = { composer, gtao, pending: false, last: 0 };
  } catch (e) { AO = null; S.errors.push('ambient occlusion off: ' + e.message); }
}
function sizeAO() { if (AO) { AO.composer.setPixelRatio(renderer.getPixelRatio()); AO.composer.setSize(innerWidth, innerHeight); AO.gtao.setSize(innerWidth * renderer.getPixelRatio(), innerHeight * renderer.getPixelRatio()); } }

// ------------------------------------------------------------------ metadata, rooms, walk grid
const cams = Object.fromEntries(meta.cameras.map((c) => [c.name, c]));
const rooms = meta.rooms;
const byZone = Object.fromEntries(rooms.map((r) => [r.zone, r]));
let minX = Infinity, maxX = -Infinity, minZ = Infinity, maxZ = -Infinity;
for (const r of rooms) for (const [x, z] of r.polygon_xz) { minX = Math.min(minX, x); maxX = Math.max(maxX, x); minZ = Math.min(minZ, z); maxZ = Math.max(maxZ, z); }
const C = new THREE.Vector3((minX + maxX) / 2, 0, (minZ + maxZ) / 2);
const RADIUS = Math.hypot(maxX - minX, maxZ - minZ) / 2;
// the five groups of the room menu (all 34 rooms, plain names)
const MENU = [
  ['Arrival & Experience', ['Z01', 'Z02', 'Z30', 'Z03', 'Z28']],
  ['Executive & Meeting', ['Z08', 'Z12', 'Z11', 'Z10', 'Z13', 'Z09']],
  ['Merchandising & Operations', ['Z07', 'Z06', 'Z05', 'Z04', 'Z31']],
  ['Design & Development', ['Z18', 'Z14', 'Z15', 'Z16', 'Z17', 'Z19', 'Z22']],
  ['Staff Facilities', ['Z20', 'Z21', 'Z23', 'Z24', 'Z25', 'Z34', 'Z26', 'Z27', 'Z29', 'Z33', 'Z32']],
];
const gbits = Uint8Array.from(atob(grid.blocked_bits_base64), (ch) => ch.charCodeAt(0));
function blocked(x, z) {
  const col = Math.floor((x - grid.origin_xz[0]) / grid.res), row = Math.floor((z - grid.origin_xz[1]) / grid.res);
  if (col < 0 || row < 0 || col >= grid.cols || row >= grid.rows) return true;
  const i = row * grid.cols + col;
  return ((gbits[i >> 3] >> (i & 7)) & 1) === 1;
}
function pathClear(a, b) {
  const d = Math.hypot(b.x - a.x, b.z - a.z), n = Math.ceil(d / 0.08);
  for (let i = 1; i <= n; i++) if (blocked(a.x + (b.x - a.x) * i / n, a.z + (b.z - a.z) * i / n)) return false;
  return true;
}
function inPoly(x, z, poly) {
  let inside = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const [xi, zi] = poly[i], [xj, zj] = poly[j];
    if ((zi > z) !== (zj > z) && x < ((xj - xi) * (z - zi)) / (zj - zi) + xi) inside = !inside;
  }
  return inside;
}
const roomAt = (x, z) => rooms.find((r) => inPoly(x, z, r.polygon_xz)) || null;
const short = (t, n = 2) => { const s = (t || '').match(/[^.!?]+[.!?]+(\s|$)/g) || [t || '']; return s.slice(0, n).join('').trim(); };

// ------------------------------------------------------------------ camera poses
const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
function poseFromCamera(c) {
  return { pos: new THREE.Vector3().fromArray(c.position), quat: new THREE.Quaternion(...c.quaternion_xyzw), lens: c.lens, shift: c.shift_y, cam: c.name };
}
function overviewPose(azDeg = -50, elDeg = 38, distScale = 1, target = C, fov = 35) {
  const dist = (RADIUS / Math.tan(THREE.MathUtils.degToRad(fov) / 2)) * 1.05 * distScale;
  const a = THREE.MathUtils.degToRad(azDeg), e = THREE.MathUtils.degToRad(elDeg);
  const pos = new THREE.Vector3(target.x + dist * Math.cos(e) * Math.cos(a), dist * Math.sin(e), target.z - dist * Math.cos(e) * Math.sin(a));
  const m = new THREE.Matrix4().lookAt(pos, target, new THREE.Vector3(0, 1, 0));
  return { pos, quat: new THREE.Quaternion().setFromRotationMatrix(m), fov, shift: 0, target: target.clone() };
}
function orthoCamPose(c, fov = 30) {
  const dir = new THREE.Vector3().fromArray(c.direction);
  const dist = (RADIUS / Math.tan(THREE.MathUtils.degToRad(fov) / 2)) * 1.08;
  const pos = C.clone().addScaledVector(dir, -dist);
  const m = new THREE.Matrix4().lookAt(pos, C, new THREE.Vector3(0, 1, 0));
  return { pos, quat: new THREE.Quaternion().setFromRotationMatrix(m), fov, shift: 0, target: C.clone() };
}
const planPose = () => overviewPose(-90, 89.5, innerWidth < innerHeight ? 1.25 : 0.92);
function roomAerialPose(r) {
  const [cx, cz] = r.centroid_xz;
  let ext = 0; for (const [x, z] of r.polygon_xz) ext = Math.max(ext, Math.hypot(x - cx, z - cz));
  return overviewPose(-55, 58, Math.max(0.16, (ext * 2.6) / RADIUS), new THREE.Vector3(cx, 0, cz), 35);
}
function vfovFor(p) {
  if (!p.lens) return p.fov;
  const big = 2 * Math.atan(18 / p.lens), aspect = innerWidth / innerHeight;
  return THREE.MathUtils.radToDeg(aspect >= 1 ? 2 * Math.atan(Math.tan(big / 2) / aspect) : big);
}
function applyPose(p, fov, shift) {
  camera.position.copy(p.pos);
  camera.quaternion.copy(p.quat);
  camera.fov = fov ?? vfovFor(p);
  const sh = shift ?? p.shift ?? 0;
  if (sh) camera.setViewOffset(innerWidth, innerHeight, 0, -sh * Math.max(innerWidth, innerHeight), innerWidth, innerHeight);
  else camera.clearViewOffset();
  camera.updateProjectionMatrix();
  needsRender = true;
}
function currentPose() {
  return { pos: camera.position.clone(), quat: camera.quaternion.clone(), fov: camera.fov, shift: camera.view && camera.view.enabled ? -camera.view.offsetY / Math.max(innerWidth, innerHeight) : 0 };
}
const isLow = (p) => p.y < 2.4;

// ------------------------------------------------------------------ ceilings + dissolve
const dctx = $('dissolve').getContext('2d');
let pendingSwap = null;
function setOverhead(on, dissolve = false) {
  if (overhead.visible === on) return;
  if (dissolve && S.ready) pendingSwap = () => { overhead.visible = on; };
  else overhead.visible = on;
  needsRender = true;
}
let fade = null;                                     // dissolve driven by the render loop (time-based, never stalls on a slow GPU)
function captureDissolve(ms = 450) {
  const cv = $('dissolve');
  cv.width = renderer.domElement.width; cv.height = renderer.domElement.height;
  dctx.drawImage(renderer.domElement, 0, 0);
  cv.style.transition = 'none'; cv.style.opacity = 1;
  fade = { t: 0, dur: ms / 1000 };
}
function fadeStep(dt) {
  if (!fade) return;
  fade.t += dt;
  const k = Math.min(1, fade.t / fade.dur);
  $('dissolve').style.opacity = String(1 - k * k * (3 - 2 * k));
  if (k >= 1) fade = null;
}

// ------------------------------------------------------------------ transitions: predictable flights from above, dissolves at eye level
let flight = null, cut = null;
function estimateMove(fromPos, toPos) {                // seconds; used for the tour durations shown before starting
  if (isLow(fromPos) && isLow(toPos)) return 0.6;
  const d = fromPos.distanceTo(toPos), lift = isLow(fromPos) || isLow(toPos);
  return THREE.MathUtils.clamp(1.6 + d * 0.06 + (lift ? 0.8 : 0), 1.6, 4.6);
}
function goTo(target, { onDone, inside } = {}) {
  flight = null; cut = null;
  controls.enabled = false; S.atCam = null; look2.drag = null; S.zoomed = false; $('resetView').classList.add('hidden');
  const from = currentPose();
  const ins = inside ?? isLow(target.pos);
  if (isLow(from.pos) && isLow(target.pos)) {          // room to room at eye level: a short dissolve never shows a wall from inside
    renderer.render(scene, camera);
    captureDissolve(550);
    overhead.visible = true;
    applyPose(target);
    cut = { t: 0, dur: 0.6, target, onDone };
    return;
  }
  flyTo(target, { onDone, inside: ins });
}
function flyTo(target, { duration, onDone, inside } = {}) {
  const from = currentPose();
  const p0 = from.pos, p3 = target.pos;
  const dist = p0.distanceTo(p3);
  const lowA = isLow(p0), lowB = isLow(p3);
  const lift = lowA || lowB ? Math.min(16, Math.max(dist > 2.5 ? 5 : 0, dist * 0.42)) : 0;
  const p1 = p0.clone(), p2 = p3.clone();
  if (lift) {                                         // leave / enter a room vertically, travel above the walls
    p1.y = Math.max(p0.y, lowA ? lift : p0.y); if (!lowA) p1.lerp(p3, 0.35).setY(Math.max(p0.y * 0.8, lift));
    p2.y = Math.max(p3.y, lift);
  } else { p1.lerp(p3, 0.33); p2.lerp(p0, 0.33); }
  const fwd0 = new THREE.Vector3(0, 0, -1).applyQuaternion(from.quat), fwd3 = new THREE.Vector3(0, 0, -1).applyQuaternion(target.quat);
  const t0 = p0.clone().addScaledVector(fwd0, p0.y > 3 ? Math.max(4, p0.distanceTo(controls.target)) : 4);
  const t3 = target.target ? target.target.clone() : p3.clone().addScaledVector(fwd3, 4);
  const toFov = target.lens ? vfovFor(target) : target.fov;
  flight = { from, target, p0, p1, p2, p3, t0, t3, toFov, t: 0, dur: duration || estimateMove(p0, p3), onDone, inside: inside ?? lowB };
  if (lift && overhead.visible) setOverhead(false, true);
}
const _q = new THREE.Quaternion(), _m = new THREE.Matrix4(), _p = new THREE.Vector3(), _t = new THREE.Vector3();
function flightStep(dt) {
  const f = flight; if (!f) return;
  f.t = Math.min(1, f.t + dt / f.dur);
  const u = ease(f.t), v = 1 - u;
  _p.set(0, 0, 0).addScaledVector(f.p0, v * v * v).addScaledVector(f.p1, 3 * v * v * u).addScaledVector(f.p2, 3 * v * u * u).addScaledVector(f.p3, u * u * u);
  _t.lerpVectors(f.t0, f.t3, ease(Math.min(1, f.t * 1.15)));
  camera.position.copy(_p);
  _m.lookAt(_p, _t, camera.up); _q.setFromRotationMatrix(_m);
  if (f.t > 0.85) _q.slerp(f.target.quat, (f.t - 0.85) / 0.15);
  camera.quaternion.copy(_q);
  camera.fov = THREE.MathUtils.lerp(f.from.fov, f.toFov, u);
  const sh = THREE.MathUtils.lerp(f.from.shift || 0, f.target.shift || 0, u);
  if (Math.abs(sh) > 1e-4) camera.setViewOffset(innerWidth, innerHeight, 0, -sh * Math.max(innerWidth, innerHeight), innerWidth, innerHeight);
  else camera.clearViewOffset();
  camera.updateProjectionMatrix();
  if (f.inside && f.t > 0.5 && _p.y < 2.35 && !overhead.visible) setOverhead(true, true);
  needsRender = true;
  if (f.t >= 1) {
    flight = null;
    applyPose(f.target, f.toFov);
    if (f.target.cam) S.atCam = f.target.cam;
    if (f.onDone) f.onDone();
  }
}
function cutStep(dt) {
  const c = cut; if (!c) return;
  c.t += dt;
  if (c.t >= c.dur) { cut = null; if (c.target.cam) S.atCam = c.target.cam; if (c.onDone) c.onDone(); }
}
const moving = () => !!(flight || cut || fade);

// ------------------------------------------------------------------ room names on the plan (never at eye level)
const hiGroup = new THREE.Group(); scene.add(hiGroup);
const hiMat = new THREE.MeshBasicMaterial({ color: 0xc29a55, transparent: true, opacity: 0.22, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -4 });
const hiLine = new THREE.LineBasicMaterial({ color: 0xe0b86e });
function highlight(r) {
  hiGroup.clear();
  if (r) {
    const shape = new THREE.Shape(r.polygon_xz.map(([x, z]) => new THREE.Vector2(x, -z)));
    const mesh = new THREE.Mesh(new THREE.ShapeGeometry(shape), hiMat);
    mesh.rotation.x = -Math.PI / 2; mesh.position.y = 0.04;
    hiGroup.add(mesh, new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(r.polygon_xz.map(([x, z]) => new THREE.Vector3(x, 0.06, z))), hiLine));
  }
  needsRender = true;
}
const MAIN = new Set(MENU.flatMap(([, z]) => z).filter((z) => !['Z03', 'Z28', 'Z13', 'Z31', 'Z22', 'Z32', 'Z33', 'Z34', 'Z24', 'Z29'].includes(z)));
const labelEls = rooms.map((r) => {
  const el = document.createElement('div');
  el.className = 'lbl'; el.textContent = r.name; el.dataset.zone = r.zone;
  el.addEventListener('click', () => selectRoom(r));
  $('labels').appendChild(el);
  return { r, el, w: r.name.length * 6.8 + 18, pos: new THREE.Vector3(r.centroid_xz[0], 0.35, r.centroid_xz[1]) };
});
const order = [...labelEls].sort((a, b) => (MAIN.has(b.r.zone) - MAIN.has(a.r.zone)) || b.r.area_sft - a.r.area_sft);
const _v = new THREE.Vector3();
function placeLabels() {
  const show = S.mode === 'plan' && !moving() && camera.position.y > 3;
  $('labels').style.display = show ? 'block' : 'none';
  if (!show) return;
  const W = innerWidth, H = innerHeight, top = $('top').offsetHeight + 4, foot = $('disclaimer').offsetHeight;
  const placed = [];                                   // the plan bar counts as taken space
  const pb = $('planbar').getBoundingClientRect(); placed.push([pb.left - 4, pb.top - 4, pb.right + 4, pb.bottom + 4]);
  for (const l of order) {
    _v.copy(l.pos).project(camera);
    const x = (_v.x * 0.5 + 0.5) * W, y = (-_v.y * 0.5 + 0.5) * H;
    let ok = _v.z < 1 && x > 20 && x < W - 20 && y > top + 12 && y < H - foot - 12;
    const box = [x - l.w / 2 - 3, y - 13, x + l.w / 2 + 3, y + 13];
    if (ok) ok = !placed.some((b) => !(box[2] < b[0] || box[0] > b[2] || box[3] < b[1] || box[1] > b[3]));
    l.el.style.display = ok ? 'block' : 'none';
    if (ok) { placed.push(box); l.el.style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px) translate(-50%, -50%)`; }
    l.el.classList.toggle('on', l.r === S.hover);
  }
}

// ------------------------------------------------------------------ room menu
function buildMenu() {
  const box = $('roomGroups'); box.innerHTML = '';
  for (const [g, zs] of MENU) {
    const h = document.createElement('div'); h.className = 'grp'; h.textContent = g; box.appendChild(h);
    for (const z of zs) {
      const r = byZone[z]; if (!r) continue;
      const b = document.createElement('button');
      b.className = 'room'; b.dataset.zone = z; b.textContent = r.name;
      b.addEventListener('click', () => { closeMenu(); selectRoom(r); });
      box.appendChild(b);
    }
  }
}
function filterMenu(f) {
  f = f.trim().toLowerCase();
  for (const b of document.querySelectorAll('#roomGroups .room')) {
    const r = byZone[b.dataset.zone];
    b.classList.toggle('dim', !!f && !`${r.name} ${r.description}`.toLowerCase().includes(f));
  }
}
function openMenu() {
  for (const b of document.querySelectorAll('#roomGroups .room')) b.classList.toggle('on', S.room && b.dataset.zone === S.room.zone);
  $('menu').classList.add('open'); $('scrim').classList.remove('hidden'); $('nRooms').classList.add('on');
}
function closeMenu() { $('menu').classList.remove('open'); $('scrim').classList.add('hidden'); $('nRooms').classList.remove('on'); }
$('search').addEventListener('input', (e) => filterMenu(e.target.value));
$('search').addEventListener('keydown', (e) => { if (e.key === 'Enter') { const b = document.querySelector('#roomGroups .room:not(.dim)'); if (b) b.click(); } e.stopPropagation(); });
$('menuClose').onclick = closeMenu;
$('scrim').onclick = closeMenu;

// ------------------------------------------------------------------ toast
let toastTimer = 0;
function toast(msg, ms = 3800) {
  const t = $('toast'); t.textContent = msg; t.classList.remove('hidden', 'fade');
  clearTimeout(toastTimer); toastTimer = setTimeout(() => { t.classList.add('fade'); toastTimer = setTimeout(() => t.classList.add('hidden'), 450); }, ms);
}

// ------------------------------------------------------------------ modes
const COARSE = matchMedia('(pointer: coarse)').matches;
function setMode(m) {
  S.mode = m;
  document.body.dataset.mode = m;
  $('home').classList.toggle('hidden', m !== 'home');
  $('card').classList.toggle('hidden', m !== 'room' && m !== 'walk');
  $('planbar').classList.toggle('hidden', m !== 'plan');
  $('tourbar').classList.toggle('hidden', m !== 'tour');
  $('walkhint').classList.toggle('hidden', m !== 'walk');
  $('pad').classList.toggle('hidden', !(m === 'walk' && COARSE));
  $('minimap').classList.toggle('hidden', m !== 'walk');
  $('resetView').classList.add('hidden');
  $('nPlan').classList.toggle('on', m === 'plan');
  controls.autoRotate = m === 'home' && !S.reduceMotion;
  controls.enabled = (m === 'home' || m === 'plan') && !moving();
  if (m !== 'plan') { S.hover = null; highlight(null); }
  needsRender = true;
}
function goHome() {
  stopTour(false); hidePhoto(); closeMenu(); closeModals();
  S.room = null; setMode('home');
  const pose = overviewPose();
  goTo(pose, { inside: false, onDone: () => { controls.target.copy(C); controls.enabled = S.mode === 'home' || S.mode === 'plan'; controls.update(); overhead.visible = false; needsRender = true; } });
}
function showPlan(view = S.view) {
  stopTour(false); hidePhoto(); closeMenu(); closeModals();
  S.view = view; S.room = null; setMode('plan');
  $('pbToggle').textContent = view === 'top' ? '3D view' : 'Plan view';
  $('pbText').textContent = 'Click a room to visit it';
  const pose = view === 'top' ? planPose() : overviewPose();
  goTo(pose, { inside: false, onDone: () => { controls.target.copy(C); controls.enabled = S.mode === 'plan'; controls.update(); overhead.visible = false; needsRender = true; } });
}
function roomCard(r, kicker) {
  $('cKicker').textContent = kicker || `${groupOf(r)}  ·  approx. ${r.area_sft.toLocaleString('en-US')} sft`;
  $('cTitle').textContent = r.name;
  $('cText').textContent = short(r.description, 2);
  const cam = r.primary_camera && cams[r.primary_camera];
  $('cPhoto').classList.toggle('hidden', !(cam && cam.render));
  $('cLook').classList.toggle('hidden', !cam || S.mode === 'walk');
  $('cWalk').textContent = S.mode === 'walk' ? 'Stop walking' : 'Explore freely (walk)';
}
const groupOf = (r) => (MENU.find(([, zs]) => zs.includes(r.zone)) || [r.group])[0];
function selectRoom(r) {
  if (!r) return;
  stopTour(false); hidePhoto(); closeMenu(); closeModals();
  S.room = r; setMode('room'); roomCard(r);
  const c = r.primary_camera && cams[r.primary_camera];
  const target = c ? poseFromCamera(c) : roomAerialPose(r);
  goTo(target, { onDone: () => {
    if (!c) { overhead.visible = false; controls.target.set(r.centroid_xz[0], 0, r.centroid_xz[1]); controls.enabled = S.mode === 'room'; controls.update(); }
    needsRender = true;
  } });
}
function resetRoomView() {
  if (S.mode !== 'room' || !S.room) return;
  const c = S.room.primary_camera && cams[S.room.primary_camera]; if (!c) return;
  look2.drag = null;
  flyTo(poseFromCamera(c), { duration: 0.6, inside: true, onDone: () => { $('resetView').classList.add('hidden'); } });
}
function toggleFullscreen(on) {
  const d = document, fs = d.fullscreenElement || d.webkitFullscreenElement;
  try {
    if (fs && on !== true) (d.exitFullscreen || d.webkitExitFullscreen).call(d);
    else if (!fs && on !== false) (d.documentElement.requestFullscreen || d.documentElement.webkitRequestFullscreen).call(d.documentElement);
  } catch (e) { S.errors.push('fullscreen: ' + e.message); }
}
function closeModals() { for (const id of ['tourPick', 'done', 'help']) $(id).classList.add('hidden'); }

// header + home + card buttons
$('brand').onclick = () => (S.present ? null : goHome());
$('nRooms').onclick = () => ($('menu').classList.contains('open') ? closeMenu() : openMenu());
$('nPlan').onclick = () => showPlan('top');
$('nPresent').onclick = () => startPresentation();
$('exitPresent').onclick = () => endPresentation();
$('nHelp').onclick = () => { closeMenu(); $('help').classList.remove('hidden'); $('helpClose').focus({ preventScroll: true }); };
$('helpClose').onclick = () => $('help').classList.add('hidden');
$('nFull').onclick = () => toggleFullscreen();
$('hTour').onclick = () => openTourPick();
$('hRooms').onclick = () => openMenu();
$('hPlan').onclick = () => showPlan('top');
$('pbToggle').onclick = () => showPlan(S.view === 'top' ? 'iso' : 'top');
$('cLook').onclick = () => { toast(COARSE ? 'Drag to look around  ·  pinch to zoom  ·  double-tap to reset' : 'Drag to look around  ·  scroll to zoom  ·  double-click to reset'); };
$('cPhoto').onclick = () => { const c = S.room && S.room.primary_camera; if (c) showPhoto(c); };
$('cPlan').onclick = () => showPlan('top');
$('cWalk').onclick = () => (S.mode === 'walk' ? stopWalk() : startWalk());
$('resetView').onclick = () => resetRoomView();
$('vQuality').value = quality;
$('vQuality').onchange = (e) => applyQuality(e.target.value);
for (const id of ['tourPick', 'done', 'help']) $(id).addEventListener('click', (e) => { if (e.target === $(id)) $(id).classList.add('hidden'); });

// ------------------------------------------------------------------ pointer: overview orbit, room look-around, plan picking
const ray = new THREE.Raycaster(), floor = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0), ndc = new THREE.Vector2();
function floorPoint(ev) {
  ndc.set((ev.clientX / innerWidth) * 2 - 1, -(ev.clientY / innerHeight) * 2 + 1);
  ray.setFromCamera(ndc, camera);
  return ray.ray.intersectPlane(floor, new THREE.Vector3());
}
const look2 = { yaw: 0, pitch: 0, drag: null, base: null };
function applyLook() { camera.quaternion.setFromEuler(new THREE.Euler(look2.pitch, look2.yaw, 0, 'YXZ')); needsRender = true; }
function lookFromCamera() {                            // yaw / pitch from the current view; a lens-shifted view becomes an equivalent up / down look
  const e = new THREE.Euler().setFromQuaternion(camera.quaternion, 'YXZ');
  look2.yaw = e.y;
  const sh = currentPose().shift, f = (innerHeight / 2) / Math.tan(THREE.MathUtils.degToRad(camera.fov) / 2);
  look2.pitch = e.x + Math.atan((sh * Math.max(innerWidth, innerHeight)) / f);
  camera.clearViewOffset(); camera.updateProjectionMatrix();
  applyLook();
}
const el = renderer.domElement;
const eyeLevel = () => !moving() && camera.position.y < 2.4;
const canLook = () => !S.present && (S.mode === 'walk' || (S.mode === 'room' && eyeLevel()) || (S.mode === 'tour' && !S.tour.playing && eyeLevel()));
let down = null;
el.addEventListener('pointerdown', (e) => {
  down = { x: e.clientX, y: e.clientY, t: performance.now() };
  if (canLook()) {
    if (!S.looking) { lookFromCamera(); S.looking = true; }
    look2.drag = { x: e.clientX, y: e.clientY }; el.setPointerCapture(e.pointerId); el.style.cursor = 'grabbing';
  }
});
el.addEventListener('pointerup', (e) => {
  look2.drag = null; el.style.cursor = '';
  if (!down || Math.hypot(e.clientX - down.x, e.clientY - down.y) > 5 || performance.now() - down.t > 600) return;
  if (S.mode === 'plan' || (S.mode === 'room' && camera.position.y > 3)) {
    const p = floorPoint(e); const r = p && roomAt(p.x, p.z);
    if (r) selectRoom(r);
  }
});
el.addEventListener('pointermove', (e) => {
  if (look2.drag) {
    // grab the view: the room follows the pointer (drag right = the room moves right, as in a 360 photo or map)
    const k = (THREE.MathUtils.degToRad(camera.fov) / innerHeight);
    look2.yaw += (e.clientX - look2.drag.x) * k;
    look2.pitch = THREE.MathUtils.clamp(look2.pitch + (e.clientY - look2.drag.y) * k, -1.1, 1.1);
    look2.drag = { x: e.clientX, y: e.clientY };
    applyLook(); S.atCam = null;
    if (S.mode === 'room') $('resetView').classList.remove('hidden');
  } else if (S.mode === 'plan' && !moving()) {
    const p = floorPoint(e); const r = p && roomAt(p.x, p.z);
    el.style.cursor = r ? 'pointer' : 'grab';
    if (r !== S.hover) { S.hover = r; highlight(r); $('pbText').textContent = r ? `${r.name}  ·  click to visit` : 'Click a room to visit it'; }
  }
});
el.addEventListener('dblclick', (e) => {
  if (S.mode === 'room') { resetRoomView(); return; }
  if (S.mode !== 'walk') return;
  const p = floorPoint(e); if (!p) return;
  const to = new THREE.Vector3(p.x, walk.eye, p.z);
  if (blocked(to.x, to.z) || !pathClear(camera.position, to)) return;
  walk.glide = { from: camera.position.clone(), to, t: 0, dur: Math.max(0.5, camera.position.distanceTo(to) / 2) };
});
el.addEventListener('wheel', (e) => {                 // zoom inside a room: field of view within sensible limits
  if (!(S.mode === 'room' || S.mode === 'walk') || !eyeLevel() || S.present) return;
  e.preventDefault();
  if (!S.looking) { lookFromCamera(); S.looking = true; }
  const base = S.room && S.room.primary_camera && cams[S.room.primary_camera] ? vfovFor(poseFromCamera(cams[S.room.primary_camera])) : 60;
  camera.fov = THREE.MathUtils.clamp(camera.fov * Math.exp(e.deltaY * 0.0012), base * 0.55, Math.min(base * 1.2, 85));
  camera.updateProjectionMatrix(); needsRender = true; S.atCam = null;
  if (S.mode === 'room') $('resetView').classList.remove('hidden');
}, { passive: false });
addEventListener('wheel', (e) => { if (e.ctrlKey || S.present) e.preventDefault(); }, { passive: false });
for (const t of ['gesturestart', 'gesturechange']) document.addEventListener(t, (e) => e.preventDefault(), { passive: false });

// ------------------------------------------------------------------ explore freely (walk)
const walk = { eye: 1.6, keys: {}, glide: null };
const WALK_HINT = COARSE ? 'Move: arrows below  ·  Look: drag  ·  Exit: Stop walking' : 'Move: W A S D or arrow keys  ·  Look: drag the mouse  ·  Exit: Esc';
function startWalk() {
  stopTour(false); hidePhoto(); closeMenu();
  const enter = () => { walk.eye = THREE.MathUtils.clamp(camera.position.y, 1.2, 1.7); camera.position.y = walk.eye; lookFromCamera(); S.looking = true; };
  if (eyeLevel()) {
    setMode('walk'); enter();
    S.room = roomAt(camera.position.x, camera.position.z) || S.room; if (S.room) roomCard(S.room, 'Exploring freely');
  } else {
    S.room = byZone.Z02; setMode('walk'); roomCard(S.room, 'Exploring freely');
    goTo(poseFromCamera(cams.CAM_01_Reception_A), { onDone: () => { overhead.visible = true; enter(); } });
  }
  $('walkhint').textContent = WALK_HINT;
}
function stopWalk() { const r = S.room; walk.keys = {}; if (r) selectRoom(r); else goHome(); }
function walkStep(dt) {
  if (walk.glide) {
    const g = walk.glide; g.t = Math.min(1, g.t + dt / g.dur);
    camera.position.lerpVectors(g.from, g.to, ease(g.t)); needsRender = true;
    if (g.t >= 1) walk.glide = null;
    return;
  }
  const k = walk.keys;
  const turn = (k.ArrowRight ? 1 : 0) - (k.ArrowLeft ? 1 : 0);
  if (turn) { look2.yaw -= turn * 1.4 * dt; applyLook(); }     // right arrow turns right
  const f = (k.KeyW || k.ArrowUp ? 1 : 0) - (k.KeyS || k.ArrowDown ? 1 : 0), s = (k.KeyD ? 1 : 0) - (k.KeyA ? 1 : 0);
  if (!f && !s) return;
  const sp = (k.ShiftLeft || k.ShiftRight ? 2.6 : 1.3) * dt;
  const fx = -Math.sin(look2.yaw), fz = -Math.cos(look2.yaw);
  let dx = fx * f - fz * s, dz = fz * f + fx * s;
  const n = Math.hypot(dx, dz), steps = Math.ceil(sp / 0.04);
  dx = (dx / n) * (sp / steps); dz = (dz / n) * (sp / steps);
  const p = camera.position;
  for (let i = 0; i < steps; i++) {
    const free = !blocked(p.x, p.z);
    if (!free || !blocked(p.x + dx, p.z + dz)) p.set(p.x + dx, walk.eye, p.z + dz);
    else if (!blocked(p.x + dx, p.z)) p.x += dx;
    else if (!blocked(p.x, p.z + dz)) p.z += dz;
    else break;
  }
  const r = roomAt(p.x, p.z);
  if (r && r !== S.room) { S.room = r; roomCard(r, 'Exploring freely'); }
  needsRender = true;
}
for (const b of document.querySelectorAll('#pad button')) {
  const k = b.dataset.k;
  b.addEventListener('pointerdown', (e) => { e.preventDefault(); walk.keys[k] = true; });
  for (const ev of ['pointerup', 'pointerleave', 'pointercancel']) b.addEventListener(ev, () => { walk.keys[k] = false; });
}
const mm = $('minimap'), mctx = mm.getContext('2d');
const mmScale = Math.min((mm.width - 10) / (grid.cols * grid.res), (mm.height - 10) / (grid.rows * grid.res));
const mmBase = document.createElement('canvas');
mmBase.width = mm.width; mmBase.height = mm.height;
{
  const b = mmBase.getContext('2d'), img = b.createImageData(grid.cols, grid.rows);
  for (let i = 0; i < grid.cols * grid.rows; i++) img.data.set(((gbits[i >> 3] >> (i & 7)) & 1) ? [32, 42, 36, 255] : [214, 221, 214, 255], i * 4);
  const t = document.createElement('canvas'); t.width = grid.cols; t.height = grid.rows; t.getContext('2d').putImageData(img, 0, 0);
  b.drawImage(t, 5, 5, grid.cols * grid.res * mmScale, grid.rows * grid.res * mmScale);
}
const toMM = (x, z) => [5 + (x - grid.origin_xz[0]) * mmScale, 5 + (z - grid.origin_xz[1]) * mmScale];
function drawMinimap() {
  if (mm.classList.contains('hidden')) return;
  mctx.clearRect(0, 0, mm.width, mm.height); mctx.drawImage(mmBase, 0, 0);
  const [px, py] = toMM(camera.position.x, camera.position.z);
  const d = new THREE.Vector3(0, 0, -1).applyQuaternion(camera.quaternion), a = Math.atan2(d.z, d.x);
  mctx.fillStyle = 'rgba(38,103,61,.35)'; mctx.beginPath(); mctx.moveTo(px, py); mctx.arc(px, py, 20, a - 0.6, a + 0.6); mctx.closePath(); mctx.fill();
  mctx.fillStyle = '#26673D'; mctx.strokeStyle = '#fff'; mctx.lineWidth = 2; mctx.beginPath(); mctx.arc(px, py, 4.5, 0, 7); mctx.fill(); mctx.stroke();
}
mm.addEventListener('click', (e) => {
  if (S.mode !== 'walk') return;
  const rc = mm.getBoundingClientRect();
  const x = grid.origin_xz[0] + (e.clientX - rc.left - 5) / mmScale, z = grid.origin_xz[1] + (e.clientY - rc.top - 5) / mmScale;
  if (blocked(x, z)) return;
  const to = new THREE.Vector3(x, walk.eye, z);
  if (pathClear(camera.position, to)) walk.glide = { from: camera.position.clone(), to, t: 0, dur: Math.max(0.5, camera.position.distanceTo(to) / 2.2) };
  else { captureDissolve(); camera.position.copy(to); needsRender = true; }
});

// ------------------------------------------------------------------ photorealistic still (optional, labelled, same room afterwards)
function showPhoto(camName) {
  const c = cams[camName]; if (!c || !c.render) return;
  closeMenu();
  const img = $('photoImg');
  img.onload = () => $('photo').classList.add('show');
  img.onerror = () => { hidePhoto(); toast('The photorealistic render could not be loaded.'); S.errors.push('render not found: ' + c.render.file); };
  img.alt = `Photorealistic render ${camName}`;
  $('photoNote').textContent = /after_with_people/.test(c.render.file) ? 'People shown are illustrative.' : '';
  $('photo').classList.remove('hidden', 'show');
  img.src = ROOT + c.render.file;
  S.photo = camName;
}
function hidePhoto() {
  if ($('photo').classList.contains('hidden')) return;
  $('photo').classList.remove('show'); S.photo = null;
  setTimeout(() => { if (!S.photo) $('photo').classList.add('hidden'); }, 500);
}
$('photoClose').onclick = () => hidePhoto();

// ------------------------------------------------------------------ guided tours
const TOURS = {
  quick: { name: 'Quick presentation', stops: meta.quick_tour, hold: 20 },
  full: { name: 'Complete office tour', stops: meta.tour, hold: 13 },
};
function stopPose(st, which = 'camera') {
  const c = cams[st[which]];
  return c.type === 'ORTHO' ? orthoCamPose(c, 30) : poseFromCamera(c);
}
function tourSeconds(key) {                           // the actual configured timings: moves between the poses + hold per view
  const T = TOURS[key];
  let t = 0, from = overviewPose().pos, views = 0;
  for (const st of T.stops) {
    for (const w of ['camera', 'also_camera']) {
      if (!st[w]) continue;
      const p = stopPose(st, w).pos; t += estimateMove(from, p) + T.hold; from = p; views++;
    }
  }
  return { t, views };
}
const minutes = (s) => { const m = Math.round(s / 30) / 2; return `about ${m % 1 ? Math.floor(m) + '½' : m} min`; };
function openTourPick() {
  const q = tourSeconds('quick'), f = tourSeconds('full');
  $('tpQuickInfo').textContent = `${TOURS.quick.stops.length} stops, the key rooms  ·  ${minutes(q.t)}`;
  $('tpFullInfo').textContent = `${TOURS.full.stops.length} stops, the whole office  ·  ${minutes(f.t)}`;
  S.tourSeconds = { quick: Math.round(q.t), full: Math.round(f.t) };
  $('tourPick').classList.remove('hidden'); $('tpQuick').focus({ preventScroll: true });
}
$('tpQuick').onclick = () => startTour('quick');
$('tpFull').onclick = () => startTour('full');
$('tpCancel').onclick = () => $('tourPick').classList.add('hidden');
function buildSegs() {
  $('tSegs').innerHTML = '';
  S.segs = S.tour.def.stops.map((st, i) => {
    const d = document.createElement('div'); d.title = `${i + 1}. ${st.title}`;
    d.appendChild(document.createElement('i')); d.addEventListener('click', () => S.tour && goStop(i));
    $('tSegs').appendChild(d); return d.firstChild;
  });
}
function startTour(key = 'quick', i = 0) {
  closeModals(); hidePhoto(); closeMenu(); S.room = null;
  S.tour = { key, def: TOURS[key], i: 0, phase: 'move', t: 0, playing: true, sub: 0, done: false };
  setMode('tour'); buildSegs(); goStop(i);
}
function goStop(i) {
  const T = S.tour; if (!T) return;
  hidePhoto(); $('done').classList.add('hidden');
  const stops = T.def.stops;
  T.i = THREE.MathUtils.clamp(i, 0, stops.length - 1); T.sub = 0; T.phase = 'move'; T.t = 0; T.done = false; S.looking = false;
  const st = stops[T.i];
  S.room = st.zone ? byZone[st.zone] : null;
  $('tCount').textContent = `${T.i + 1} / ${stops.length}`;
  $('tName').textContent = T.def.name;
  $('tTitle').textContent = st.title; $('tText').textContent = short(st.description, 2);
  $('tPrev').disabled = T.i === 0; $('tNext').disabled = false;
  const outside = cams[st.camera].type === 'ORTHO';
  goTo(stopPose(st), { inside: !outside, onDone: () => { if (!S.tour) return; overhead.visible = !outside; needsRender = true; S.tour.phase = 'hold'; S.tour.t = 0; } });
  updateSegs(); updatePlay();
}
function nextStop(d) {
  const T = S.tour; if (!T) return;
  if (d > 0 && T.i === T.def.stops.length - 1) { finishTour(); return; }
  goStop(T.i + d);
}
function finishTour() {
  const T = S.tour; if (!T) return;
  T.playing = false; T.done = true; updatePlay();
  $('done').classList.remove('hidden'); $('dAgain').focus({ preventScroll: true });
}
function stopTour(toHome = true) {
  if (!S.tour) return;
  S.tour = null; flight = null; cut = null; hidePhoto(); $('done').classList.add('hidden');
  if (S.present && toHome) { endPresentation(); return; }
  if (toHome) goHome();
}
function togglePlay() {
  const T = S.tour; if (!T) return;
  if (T.done) { startTour(T.key, 0); return; }
  T.playing = !T.playing; updatePlay();
  if (T.playing && S.looking) { S.looking = false; goTo(stopPose(T.def.stops[T.i], T.sub ? 'also_camera' : 'camera'), { onDone: () => { if (S.tour) S.tour.phase = 'hold'; } }); }
}
function updatePlay() {
  const T = S.tour;
  $('tPlay').innerHTML = T && !T.playing && !T.done ? '&#9654;&ensp;Resume' : '&#10073;&#10073;&ensp;Pause';
}
function updateSegs() {
  const T = S.tour; if (!T) return;
  const f = flight ? flight.t : cut ? Math.min(1, cut.t / cut.dur) : 1;
  S.segs.forEach((s, i) => { s.style.width = i < T.i ? '100%' : i > T.i ? '0%' : `${Math.round(Math.min(1, T.phase === 'hold' ? 0.15 + 0.85 * (T.t / T.def.hold) : 0.15 * f) * 100)}%`; });
}
function tourStep(dt) {
  const T = S.tour; if (!T) return;
  updateSegs();
  if (T.phase !== 'hold' || !T.playing) return;
  const st = T.def.stops[T.i], cam = cams[T.sub ? st.also_camera : st.camera];
  T.t += dt;
  if (cam.type === 'ORTHO') {                          // slow turn on the whole-floor views
    const off = camera.position.clone().sub(C).applyAxisAngle(new THREE.Vector3(0, 1, 0), dt * 0.04);
    camera.position.copy(C).add(off); camera.lookAt(C); needsRender = true;
  }
  if (T.t >= T.def.hold) {
    if (st.also_camera && !T.sub) {
      T.sub = 1; T.phase = 'move'; T.t = 0;
      if (st.also_zone && byZone[st.also_zone]) S.room = byZone[st.also_zone];
      goTo(stopPose(st, 'also_camera'), { onDone: () => { if (S.tour) { overhead.visible = true; S.tour.phase = 'hold'; S.tour.t = 0; } } });
    } else if (T.i + 1 < T.def.stops.length) goStop(T.i + 1);
    else finishTour();
  }
}
$('tPrev').onclick = () => nextStop(-1);
$('tNext').onclick = () => nextStop(1);
$('tPlay').onclick = () => togglePlay();
$('tExit').onclick = () => stopTour(true);
$('dAgain').onclick = () => startTour(S.tour ? S.tour.key : 'quick', 0);
$('dRooms').onclick = () => { const p = S.present; stopTour(false); if (p) endPresentation(false); goHome(); openMenu(); };
$('dHome').onclick = () => { stopTour(false); if (S.present) endPresentation(); else goHome(); };

// ------------------------------------------------------------------ presentation mode
function startPresentation() {
  S.present = true; document.body.classList.add('present'); $('exitPresent').classList.remove('hidden');
  toggleFullscreen(true);                             // inside the click: browsers allow full screen only on a user gesture
  startTour('quick');
}
function endPresentation(home = true) {
  if (!S.present) return;
  S.present = false; document.body.classList.remove('present'); $('exitPresent').classList.add('hidden');
  if (document.fullscreenElement || document.webkitFullscreenElement) toggleFullscreen(false);
  if (S.tour) { S.tour = null; flight = null; cut = null; $('done').classList.add('hidden'); }
  if (home) goHome();
}

// ------------------------------------------------------------------ keyboard: optional shortcuts, never in text fields
addEventListener('keydown', (e) => {
  const tag = e.target.tagName;
  if (tag === 'INPUT' || tag === 'SELECT' || tag === 'TEXTAREA') return;
  if (S.mode === 'walk') walk.keys[e.code] = true;
  if (e.code === 'Escape') {
    if (!$('photo').classList.contains('hidden')) hidePhoto();
    else if ($('menu').classList.contains('open')) closeMenu();
    else if (!$('help').classList.contains('hidden') || !$('tourPick').classList.contains('hidden')) closeModals();
    else if (S.present) endPresentation();
    else if (S.mode === 'tour') stopTour(true);
    else if (S.mode === 'walk') stopWalk();
    else if (S.mode === 'room' || S.mode === 'plan') goHome();
    return;
  }
  if (S.mode === 'tour') {
    if (e.code === 'ArrowRight') { e.preventDefault(); nextStop(1); } else if (e.code === 'ArrowLeft') { e.preventDefault(); nextStop(-1); }
    else if (e.code === 'Space') { e.preventDefault(); togglePlay(); }
  }
  if (S.mode === 'walk' && (e.code.startsWith('Arrow') || e.code === 'Space')) e.preventDefault();
  if (e.code === 'KeyH' && !S.present && S.mode !== 'walk') goHome();
});
addEventListener('keyup', (e) => { walk.keys[e.code] = false; });
addEventListener('blur', () => { walk.keys = {}; });
document.addEventListener('fullscreenchange', () => { if (!document.fullscreenElement && S.present) toast('Full screen ended  ·  Esc again exits the presentation', 3000); });

// ------------------------------------------------------------------ loop
function measureChrome() {
  const r = document.documentElement.style;
  r.setProperty('--top-h', $('top').offsetHeight + 'px'); r.setProperty('--foot-h', $('disclaimer').offsetHeight + 'px');
}
addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight;
  if (S.atCam && cams[S.atCam].lens && !S.looking) applyPose(poseFromCamera(cams[S.atCam]));
  camera.updateProjectionMatrix(); renderer.setSize(innerWidth, innerHeight); sizeAO(); measureChrome(); needsRender = true;
});
const clock = new THREE.Clock();
let frames = 0, fpsT = 0;
renderer.setAnimationLoop(() => {
  const dt = Math.min(clock.getDelta(), 1.0);         // time-based: transitions and holds end on time even on slow GPUs
  if (flight) flightStep(dt);
  if (cut) cutStep(dt);
  fadeStep(dt);
  if (!moving() && controls.enabled) controls.update();
  if (S.mode === 'walk' && !moving()) walkStep(dt);
  if (S.mode === 'tour') tourStep(dt);
  if (needsRender) {
    const want = camera.position.y < 2.6 ? 'inside' : 'outside';
    if (want !== lookPreset) look(want);
    hiGroup.visible = camera.position.y > 2.6;
    renderer.render(scene, camera);
    if (pendingSwap) { captureDissolve(); pendingSwap(); pendingSwap = null; renderer.render(scene, camera); }
    placeLabels(); drawMinimap();
    needsRender = false; frames++;
    if (AO) { AO.pending = true; AO.last = performance.now(); }
  } else if (AO && AO.pending && !moving() && !look2.drag && performance.now() - AO.last > 250) {
    try { AO.composer.render(); AO.pending = false; S.aoFrames = (S.aoFrames || 0) + 1; }
    catch (e) { AO = null; S.errors.push('ambient occlusion off: ' + e.message); needsRender = true; }
  }
  fpsT += dt; if (fpsT > 1) { S.fps = frames / fpsT; frames = 0; fpsT = 0; }
});

// ------------------------------------------------------------------ start
S.reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches || qs.get('motion') === '0';   // ?motion=0: no idle turning (tests, slow GPUs)
buildMenu();
measureChrome();
if (aoWanted()) setupAO();
overhead.visible = false;
applyPose(overviewPose()); controls.target.copy(C); controls.update(); look('outside');
setMode('home');
$('loading').style.display = 'none';
S.ready = true; window.__viewerReady = true;
// links: ?room=Z07 opens a room, ?tour=quick|full starts a tour, ?plan=1 the floor plan, ?present=1 presentation mode (needs a click for full screen)
{
  const z = qs.get('room'), t = qs.get('tour');
  if (z && byZone[z]) selectRoom(byZone[z]);
  else if (t === 'quick' || t === 'full' || t === '1') startTour(t === 'full' ? 'full' : 'quick');
  else if (qs.get('plan') === '1') showPlan('top');
  else if (qs.get('present') === '1') { S.present = true; document.body.classList.add('present'); $('exitPresent').classList.remove('hidden'); startTour('quick'); }
}
let meshes = 0; model.traverse((o) => { if (o.isMesh) meshes++; });
S.counts = { quality, meshes, drawCallsMerged: drawCalls, rooms: rooms.length, cameras: meta.cameras.length, quickStops: TOURS.quick.stops.length,
  fullStops: TOURS.full.stops.length, bakedLight: BAKED, ambientOcclusion: !!AO };
S.api = { selectRoom: (z) => selectRoom(byZone[z]), goHome, showPlan, startWalk, stopWalk, startTour, goStop, nextStop, togglePlay, stopTour, showPhoto, hidePhoto,
  startPresentation, endPresentation, resetRoomView, openMenu, closeMenu, tourSeconds, blocked,
  state: () => ({ mode: S.mode, room: S.room && S.room.zone, atCam: S.atCam, moving: moving(), fps: S.fps, overhead: overhead.visible, looking: !!S.looking,
    tour: S.tour && { key: S.tour.key, i: S.tour.i, phase: S.tour.phase, playing: S.tour.playing, sub: S.tour.sub, done: !!S.tour.done }, present: S.present,
    photo: S.photo, aoFrames: S.aoFrames || 0, fov: +camera.fov.toFixed(2), yaw: +look2.yaw.toFixed(4), pos: camera.position.toArray().map((v) => +v.toFixed(3)) }) };
