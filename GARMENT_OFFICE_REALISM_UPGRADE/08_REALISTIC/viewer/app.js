// Ground floor - interactive design experience (three.js r169, vendored: no CDN).
// Model: the web copy of the approved GLB; data: office_web_metadata.json + walk_grid.json (07_WEB_TOUR_ASSETS).
// Modes: overview (orbit), rooms (fly to the room's render camera), walk (eye level, collision with walls and furniture),
// guided tour (16 stops; at each stop the real-time view can dissolve into the Cycles render of the same camera).
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { GTAOPass } from 'three/addons/postprocessing/GTAOPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { readLightingManifest, RoomLightmaps } from './room-lightmaps.js';
import { createWalking } from './walk-controller.js';
import { applyDoorwayRepairs } from './doorway-repairs.js';
import { createMaterialUpgrade } from './phase-materials.js';
import { createRoomProbes } from './room-probes.js';
import { createPostProcessing } from './phase-post.js';
import { createOfficeDressing } from './phase-dressing.js';
import { estimateGpuMemory } from './gpu-memory.js';

window.__viewerStarted = true;
const $ = (id) => document.getElementById(id);
const qs = new URLSearchParams(location.search);
// Paths: repository layout by default; a deployment bundle sets window.__TOUR_CONFIG (and window.__TOUR_DATA = { meta, grid }).
const CFG = window.__TOUR_CONFIG || {};
const STAGE = Math.max(1, Math.min(5, Number(qs.get('stage') || CFG.stage || 1)));
const USE_PBR = STAGE >= 2 && qs.get('materials') !== '0', USE_PROBES = STAGE >= 3 && qs.get('probes') !== '0', USE_POST = STAGE >= 5 && qs.get('post') !== '0';
const USE_DRESSING = STAGE >= 4 && qs.get('props') !== '0';
// This flag is set only after the independently reviewed people asset lock is accepted.
const PEOPLE_ACCEPTED = !!CFG.peopleAccepted;
let dressing = null, dressingPromise = null;
const BASE = CFG.base || '../../../GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/';
const MODELS = qs.get('model') ? [qs.get('model')] : CFG.models || [BASE + 'Final_Office_Interior_web.glb'];
const RENDERS = qs.get('renders') || CFG.renders || '../../../GARMENT_OFFICE_FINAL_PRESENTATION/02_RENDERED_IMAGES/final/';
const lightingManifest = await readLightingManifest(qs.get('lighting') || CFG.lightmapManifest || '../lighting/manifest.json');
const S = { mode: 'loading', ready: false, ceilUser: false, labels: true, room: null, atCam: null, tour: null, errors: [], counts: {} };
S.stage = STAGE;
S.features = { materials: USE_PBR, probes: USE_PROBES, post: USE_POST, gameWalking: STAGE >= 5, props: USE_DRESSING, peopleAccepted: PEOPLE_ACCEPTED };
S.timings = { moduleStartedMs: performance.now(), baseFirstViewMs: null, atlasDecodedByRoomMs: {}, atlasVisibleByRoomMs: {}, atlasFullVisibleByRoomMs: {}, heroMapsReadyByRoomMs: {} };
window.__viewer = S;

// ------------------------------------------------------------------ renderer
const probe = document.createElement('canvas');
if (!(probe.getContext('webgl2') || probe.getContext('webgl'))) {
  window.__fail('WebGL is not available in this browser, so the 3D model cannot be shown. Enable hardware acceleration / WebGL or use a current Chrome, Safari or Edge.');
  throw new Error('no WebGL');
}
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
const scale = Math.min(1, Math.max(0.25, parseFloat(qs.get('scale')) || 1));
const QUALITY = { high: 2, balanced: 1.5, low: 1 };                 // device-pixel-ratio cap per quality profile
let quality = 'balanced';
try { quality = localStorage.getItem('tourQuality') || (matchMedia('(pointer: coarse)').matches && innerWidth < 900 ? 'low' : 'balanced'); } catch (e) { /* storage blocked */ }
if (!QUALITY[quality]) quality = 'balanced';
function applyQuality(q) {
  quality = q;
  if (S.ready) lightmaps.setBudget((q === 'high' ? 256 : q === 'low' ? 128 : 192) * 1024 * 1024);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, QUALITY[q]) * scale);
  renderer.setSize(innerWidth, innerHeight);
  try { localStorage.setItem('tourQuality', q); } catch (e) { /* storage blocked */ }
  if (typeof sizeAO === 'function') { if (aoWanted() && !AO) setupAO(); if (!aoWanted()) AO = null; sizeAO(); }
  if (USE_POST && POST) { POST.dispose(); POST = createPostProcessing({ renderer, scene, camera, quality, changed: () => { needsRender = true; } }); S.post = POST.status; }
  needsRender = true;
}
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, QUALITY[quality]) * scale);
renderer.setSize(innerWidth, innerHeight);
renderer.setClearColor(0x000000, 0);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.AgXToneMapping;        // the renders use Blender's AgX view transform
$('app').appendChild(renderer.domElement);
const scene = new THREE.Scene();
scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture;
const hemi = new THREE.HemisphereLight(0xfff1e0, 0x4a4640, 0.5);
const sun = new THREE.DirectionalLight(0xfff3e4, 1.2);
sun.position.set(30, 60, 25);
scene.add(hemi, sun, sun.target);
let SHADOWS = false;                                  // set after loading: real-time shadows only without baked light
function enableShadows() {
  SHADOWS = true;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  sun.shadow.bias = -0.0004;
  sun.shadow.normalBias = 0.025;
}
const camera = new THREE.PerspectiveCamera(35, innerWidth / innerHeight, 0.05, 600);
const controls = new OrbitControls(camera, renderer.domElement);
Object.assign(controls, { enableDamping: true, dampingFactor: 0.08, minDistance: 4, maxDistance: 150, maxPolarAngle: Math.PI * 0.47, screenSpacePanning: true });
let needsRender = true;
let captureCamera = null;
let captureViewport = null;
controls.addEventListener('change', () => { needsRender = true; });
let lookPreset = 'outside';
function look(preset) {                               // inside: light from above with soft shadows; outside: low sun, wall shadows
  lookPreset = preset;
  const L = BAKED ? (preset === 'inside' ? { exp: 1.0, env: 0.5, hemi: 0.45, sun: 0.35 } : { exp: 0.95, env: 0.5, hemi: 0.5, sun: 0.9 })
    : preset === 'inside' ? { exp: 1.1, env: 0.55, hemi: 0.36, sun: SHADOWS ? 1.05 : 0.55 } : { exp: 0.95, env: 0.55, hemi: 0.5, sun: 1.35 };
  renderer.toneMappingExposure = L.exp; scene.environmentIntensity = L.env; hemi.intensity = L.hemi; sun.intensity = L.sun;
  placeSun(); needsRender = true;
}
function placeSun() {
  const sc = sun.shadow.camera;
  if (lookPreset === 'inside') {                      // follows the eye: a 16 m square around the camera
    const p = camera.position;
    sun.position.set(p.x + 1.6, 9.5, p.z + 1.1); sun.target.position.set(p.x, 0, p.z);
    Object.assign(sc, { left: -8, right: 8, top: 8, bottom: -8, near: 0.5, far: 14 });
  } else {
    sun.position.set(C.x + 20, 42, C.z + 26); sun.target.position.copy(C);
    const r = RADIUS * 1.08;
    Object.assign(sc, { left: -r, right: r, top: r, bottom: -r, near: 1, far: 120 });
  }
  sc.updateProjectionMatrix(); sun.target.updateMatrixWorld();
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
      (e) => { last = Date.now(); progress(e.loaded, e.lengthComputable ? e.total : 16.6e6, 'Loading the 3D model'); },
      (err) => { clearInterval(stall); rej(err); });
  });
}
let meta, grid, gltf;
try {
  if (window.__TOUR_DATA) ({ meta, grid } = window.__TOUR_DATA);
  else [meta, grid] = await Promise.all([getJSON(BASE + 'office_web_metadata.json'), getJSON(BASE + 'walk_grid.json')]);
  for (let i = 0; i < MODELS.length && !gltf; i++) {               // e.g. the web GLB first, then the original GLB
    try { gltf = await loadModel(MODELS[i]); } catch (e) { S.errors.push(`${MODELS[i]}: ${e.message || e}`); if (i === MODELS.length - 1) throw e; }
  }
} catch (err) {
  window.__fail(`Could not load the tour data (${err.message || err}). Serve the repository folder with a web server and open GARMENT_OFFICE_WALKTHROUGH_FINAL/03_INTERACTIVE_3D/ (see README).`);
  throw err;
}
$('loadTitle').textContent = 'Preparing the scene...';

// ------------------------------------------------------------------ model: groups, draw-call merge
const model = gltf.scene;
scene.add(model);
try { S.repairs = await applyDoorwayRepairs(model, lightingManifest); }
catch (error) { window.__fail('Could not prepare the verified doorway geometry: ' + error.message); throw error; }
// Exact source slab top triangles include door thresholds omitted by clear-room polygons.
// Keep this independent footprint before render batching removes the source node names.
model.updateMatrixWorld(true);
const floorTriangles = [];
const sourceSlab = model.getObjectByName(THREE.PropertyBinding.sanitizeNodeName('Floor slab (existing, finished floor = 0)'));
sourceSlab?.traverse(mesh => {
  if (!mesh.isMesh) return;
  const geometry = mesh.geometry, positions = geometry.attributes.position, index = geometry.index;
  const top = new THREE.Box3().setFromObject(mesh).max.y;
  const a = new THREE.Vector3(), b = new THREE.Vector3(), c = new THREE.Vector3();
  const count = index?.count || positions.count;
  for (let i = 0; i < count; i += 3) {
    a.fromBufferAttribute(positions, index ? index.getX(i) : i).applyMatrix4(mesh.matrixWorld);
    b.fromBufferAttribute(positions, index ? index.getX(i + 1) : i + 1).applyMatrix4(mesh.matrixWorld);
    c.fromBufferAttribute(positions, index ? index.getX(i + 2) : i + 2).applyMatrix4(mesh.matrixWorld);
    if ([a.y, b.y, c.y].every(y => Math.abs(y - top) < 0.002)) floorTriangles.push([a.x, a.z, b.x, b.z, c.x, c.z]);
  }
});
function insideSourceFloor(x, z) {
  return floorTriangles.some(([ax, az, bx, bz, cx, cz]) => {
    const d1 = (x - bx) * (az - bz) - (ax - bx) * (z - bz);
    const d2 = (x - cx) * (bz - cz) - (bx - cx) * (z - cz);
    const d3 = (x - ax) * (cz - az) - (cx - ax) * (z - az);
    return !((d1 < -1e-8 || d2 < -1e-8 || d3 < -1e-8) && (d1 > 1e-8 || d2 > 1e-8 || d3 > 1e-8));
  });
}
let overhead = model.getObjectByName('WEB_OVERHEAD');
if (!overhead) {                                       // original GLB: collect the overhead objects by name
  overhead = new THREE.Group(); overhead.name = 'WEB_OVERHEAD';
  const names = new Set(meta.names.overhead_threejs);
  const found = []; model.traverse((o) => { if (names.has(o.name)) found.push(o); });
  for (const o of found) overhead.attach(o);
  model.add(overhead);
}
const interior = model.getObjectByName('WEB_INTERIOR') || model;

// baked light: shell objects carry Cycles lighting as vertex colours (light / baked_light_scale); show them unlit
const BX = parseFloat(qs.get('bx')) || CFG.bakedExposure || 2.0;     // checked against the Cycles renders (camera QC)
const LIGHT_FLOOR = 0.012;                                         // rooms without any lamp become dark grey, not black
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
      m.vertexColors = false; m.needsUpdate = true; return;          // glass and lamps stay real-time
    }
    const col = o.geometry.attributes.color;            // may be interleaved with position / normal (glTF byteStride): use the accessors
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
if (!BAKED && qs.get('shadows') !== '0') enableShadows();
if (BAKED && qs.get('shadows') === '1') enableShadows();
for (const m of new Set(collectMaterials(model))) {
  if (m.transmission > 0) m.envMapIntensity = 1.0;   // keep glass reflective; transmission pass stays enabled
}
function collectMaterials(root) { const a = []; root.traverse((o) => { if (o.isMesh) a.push(...(Array.isArray(o.material) ? o.material : [o.material])); }); return a; }
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
function mergeByMaterial(root) {                      // ~2,300 draw calls -> about one per material
  root.updateMatrixWorld(true);
  const inv = new THREE.Matrix4().copy(root.matrixWorld).invert();
  const buckets = new Map();
  root.traverse((o) => {
    if (!o.isMesh || o.isInstancedMesh || Array.isArray(o.material)) return;
    for (let p = o.parent; p && p !== root; p = p.parent) if (p.userData.lightmapBoundary || p === overhead) return;
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
// Keep each room's exact original objects separate until its atlas arrives.
const lightmaps = new RoomLightmaps({ manifest: lightingManifest, model, overhead, renderer, merge: mergeByMaterial,
  changed: () => { needsRender = true; updateLightingStatus(); }, maxResident: 6, maxResidentBytes: (quality === 'high' ? 256 : quality === 'low' ? 128 : 192) * 1024 * 1024 });
S.lightmaps = lightmaps.status;
lightmaps.onStage = (event, id) => {
  const key = { atlasDecoded: 'atlasDecodedByRoomMs', atlasVisible: 'atlasVisibleByRoomMs', atlasFullVisible: 'atlasFullVisibleByRoomMs', heroMapsReady: 'heroMapsReadyByRoomMs' }[event];
  if (key && S.timings[key][id] == null) S.timings[key][id] = performance.now();
  if (event === 'atlasDecoded' && S.ready && S.mode === 'rooms' && !flight && !captureCamera) { renderScene(); captureDissolve(); }
  if (['atlasVisible', 'atlasFullVisible'].includes(event) && lightmaps.status.requiredShared.length && lightmaps.status.requiredShared.every(key => lightmaps.status.rooms[key]?.state === 'loaded')) S.timings.sharedLightingReadyMs ??= performance.now();
};
const materialUpgrade = USE_PBR ? createMaterialUpgrade({ renderer, loader: lightmaps.ktx, changed: () => { needsRender = true; } }) : null;
S.pbr = materialUpgrade?.status || { enabled: false };
lightmaps.disposeMaterial = material => materialUpgrade?.release(material);
lightmaps.prepareRoom = async room => {
  if (USE_DRESSING) (await ensureDressing()).prepareRoom(room);
  if (materialUpgrade) await Promise.all([...room.ownedMaterials].map(m => materialUpgrade.apply(m)));
};
const probes = USE_PROBES ? createRoomProbes({ scene, renderer, metadata: meta, lightmaps, overhead, hidden: () => [hiGroup, ...(dressing?.hiddenDuringProbe() || [])], dynamicLighting: USE_DRESSING, changed: () => { needsRender = true; } }) : null;
S.probes = probes?.status || { enabled: false };
async function loadVisualRoom(id) {
  const room = await lightmaps.request(id);
  if (materialUpgrade) await Promise.all([room?.heroPromise, ...lightmaps.status.requiredShared.map(key => lightmaps.rooms.get(key)?.heroPromise)]);
  if (probes) { dressing?.prepareView(null); await probes.ensure(id); dressing?.applyProbe(id); }
  return room;
}
async function ensureDressing() {
  if (!USE_DRESSING) return null;
  if (!dressingPromise) dressingPromise = createOfficeDressing({ scene, renderer, metadata: meta, grid, probes, staticBlocked, changed: () => { needsRender = true; }, peopleAccepted: PEOPLE_ACCEPTED }).then(value => { dressing = value; S.dressing = value.status; return value; });
  return dressingPromise;
}
async function setPeopleEnabled(enabled) {
  if (!USE_DRESSING) { if (enabled) throw new Error('People require stage4 or later.'); return { enabled: false, loaded: false, total: 0, visible: 0 }; }
  const layer = await ensureDressing();
  const state = await layer.setPeopleEnabled(enabled, S.mode === 'walk' ? camera.position : null);
  $('mPeople').classList.toggle('on', state.enabled); $('mPeople').setAttribute('aria-pressed', String(state.enabled));
  $('peopleNote').hidden = !state.enabled; needsRender = true; return state;
}
lightmaps.loadGlobals();
function updateLightingStatus() {
  const element = $('lightingStatus');
  if (!element) return;
  const id = S.room?.zone, room = id && lightmaps.status.rooms[id];
  const sharedReady = lightmaps.status.requiredShared.every(id => lightmaps.status.rooms[id]?.state === 'loaded');
  const sharedError = lightmaps.status.requiredShared.map(id => lightmaps.status.rooms[id]).find(r => r?.state === 'error' || r?.fullResolutionError);
  element.textContent = sharedError ? 'Lighting preview' : room?.state === 'loaded' && sharedReady ? 'Cycles lighting' : room?.state === 'loading' || !sharedReady ? 'Loading room lighting…' : 'Lighting preview';
  element.title = room?.state === 'loaded' && sharedReady ? 'This room uses a Cycles diffuse lightmap; other surfaces may retain preview lighting.'
    : sharedError?.error || (room?.state === 'error' ? room.error : 'This area retains the original geometry with preview lighting until its bake is verified.');
}
let drawCalls = null;
if (qs.get('merge') !== '0') {
  try {
    const a = mergeByMaterial(interior), b = mergeByMaterial(overhead);
    lightmaps.mergeFallbacks();
    drawCalls = { before: a[0] + b[0], after: a[1] + b[1], roomGroupsSeparate: true };
  } catch (e) { S.errors.push('merge skipped: ' + e.message); }
}

if (SHADOWS) {
  interior.traverse((o) => {
    if (!o.isMesh) return;
    const m = o.material, see = m.transmission > 0 || (m.transparent && m.opacity < 0.95), lamp = m.emissiveIntensity > 1 && m.emissive && m.emissive.getHex() !== 0;
    o.castShadow = !see && !lamp; o.receiveShadow = true;
  });
  overhead.traverse((o) => { if (o.isMesh) { o.castShadow = false; o.receiveShadow = true; } });
}

// ------------------------------------------------------------------ ambient occlusion (soft contact shadows), drawn once the view stops moving
// The baked light has no furniture in it; GTAO darkens contact areas (chair and table feet, corners) in screen space.
// Moving frames render directly (smooth on any GPU); 0.25 s after the last movement one AO frame replaces it.
let AO = null;
let POST = null;
const aoWanted = () => STAGE < 5 && (qs.get('ao') ? qs.get('ao') !== '0' : quality !== 'low');
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
    gtao.blendIntensity = 1.0;
    const hideSeeThrough = gtao.overrideVisibility.bind(gtao);          // glass must not cast AO onto what is behind it
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

// ------------------------------------------------------------------ metadata
const cams = Object.fromEntries(meta.cameras.map((c) => [c.name, c]));
const rooms = meta.rooms;
const byZone = Object.fromEntries(rooms.map((r) => [r.zone, r]));
let minX = Infinity, maxX = -Infinity, minZ = Infinity, maxZ = -Infinity;
for (const r of rooms) for (const [x, z] of r.polygon_xz) { minX = Math.min(minX, x); maxX = Math.max(maxX, x); minZ = Math.min(minZ, z); maxZ = Math.max(maxZ, z); }
const C = new THREE.Vector3((minX + maxX) / 2, 0, (minZ + maxZ) / 2);
const RADIUS = Math.hypot(maxX - minX, maxZ - minZ) / 2;

// walk grid
const gbits = Uint8Array.from(atob(grid.blocked_bits_base64), (ch) => ch.charCodeAt(0));
function blocked(x, z) { return staticBlocked(x, z) || !!dressing?.blocksMovement(x, z, .15); }
function staticBlocked(x, z, radius = .15) {
  if (STAGE >= 5) {
    if (!insideSourceFloor(x, z)) return true;
    for (let i = 0; i < 8; i++) if (!insideSourceFloor(x + radius * Math.cos(i * Math.PI / 4), z + radius * Math.sin(i * Math.PI / 4))) return true;
  }
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

// ------------------------------------------------------------------ camera poses
const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
function poseFromCamera(c) {                          // exact render camera (level camera + vertical lens shift)
  return { pos: new THREE.Vector3().fromArray(c.position), quat: new THREE.Quaternion(...c.quaternion_xyzw),
    lens: c.lens, shift: c.shift_y, cam: c.name };
}
function overviewPose(azDeg = -50, elDeg = 38, distScale = 1, target = C, fov = 35) {
  const dist = (RADIUS / Math.tan(THREE.MathUtils.degToRad(fov) / 2)) * 1.05 * distScale;
  const a = THREE.MathUtils.degToRad(azDeg), e = THREE.MathUtils.degToRad(elDeg);
  const pos = new THREE.Vector3(target.x + dist * Math.cos(e) * Math.cos(a), dist * Math.sin(e), target.z - dist * Math.cos(e) * Math.sin(a));
  const m = new THREE.Matrix4().lookAt(pos, target, new THREE.Vector3(0, 1, 0));
  return { pos, quat: new THREE.Quaternion().setFromRotationMatrix(m), fov, shift: 0, target: target.clone() };
}
function orthoCamPose(c, fov = 30) {                  // perspective stand-in for the isometric render cameras
  const dir = new THREE.Vector3().fromArray(c.direction);
  const dist = (RADIUS / Math.tan(THREE.MathUtils.degToRad(fov) / 2)) * 1.08;
  const target = C.clone();
  const pos = target.clone().addScaledVector(dir, -dist);
  const m = new THREE.Matrix4().lookAt(pos, target, new THREE.Vector3(0, 1, 0));
  return { pos, quat: new THREE.Quaternion().setFromRotationMatrix(m), fov, shift: 0, target };
}
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

// ------------------------------------------------------------------ ceilings + dissolve
const dctx = $('dissolve').getContext('2d');
let pendingSwap = null;
function setOverhead(on, dissolve = false) {
  if (overhead.visible === on) return;
  if (dissolve && S.ready) { pendingSwap = () => { overhead.visible = on; }; }
  else overhead.visible = on;
  needsRender = true;
}
function captureDissolve() {
  const cv = $('dissolve');
  cv.width = renderer.domElement.width; cv.height = renderer.domElement.height;
  dctx.drawImage(renderer.domElement, 0, 0);
  cv.style.transition = 'none'; cv.style.opacity = 1;
  requestAnimationFrame(() => requestAnimationFrame(() => { cv.style.transition = 'opacity .45s ease'; cv.style.opacity = 0; }));
}

// ------------------------------------------------------------------ flights (arc over the walls between rooms)
let flight = null;
function flyTo(target, { duration, onDone, inside } = {}) {
  const from = currentPose();
  const p0 = from.pos, p3 = target.pos;
  const dist = p0.distanceTo(p3);
  const lowA = p0.y < 2.4, lowB = p3.y < 2.4;
  const lift = lowA || lowB ? Math.min(16, Math.max(dist > 2.5 ? 5 : 0, dist * 0.42)) : 0;
  const p1 = p0.clone(), p2 = p3.clone();
  if (lift) {
    p1.y = Math.max(p0.y, lowA ? lift : p0.y); if (!lowA) p1.lerp(p3, 0.35).setY(Math.max(p0.y * 0.8, lift));
    p2.y = Math.max(p3.y, lift);
  } else { p1.lerp(p3, 0.33); p2.lerp(p0, 0.33); }
  const fwd0 = new THREE.Vector3(0, 0, -1).applyQuaternion(from.quat), fwd3 = new THREE.Vector3(0, 0, -1).applyQuaternion(target.quat);
  const t0 = p0.clone().addScaledVector(fwd0, from.pos.y > 3 ? Math.max(4, p0.distanceTo(controls.target)) : 4);
  const t3 = target.target ? target.target.clone() : p3.clone().addScaledVector(fwd3, 4);
  const toFov = target.lens ? vfovFor(target) : target.fov;
  flight = { from, target, p0, p1, p2, p3, t0, t3, toFov, t: 0, dur: duration || THREE.MathUtils.clamp(1.6 + dist * 0.06 + (lift ? 0.8 : 0), 1.6, 5.2),
    onDone, inside: inside ?? lowB };
  controls.enabled = false; S.freeLook = false; walk.drag = null;
  if (lift && overhead.visible) setOverhead(false, true);
  S.atCam = null; updateInfoButtons();
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
  if (f.t > 0.85) _q.slerp(f.target.quat, (f.t - 0.85) / 0.15);     // land exactly on the target orientation
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
    updateInfoButtons();
    if (f.onDone) f.onDone();
  }
}

// ------------------------------------------------------------------ highlight + labels
const hiGroup = new THREE.Group(); scene.add(hiGroup);
const hiMat = new THREE.MeshBasicMaterial({ color: 0xc29a55, transparent: true, opacity: 0.2, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -4 });
const hiLine = new THREE.LineBasicMaterial({ color: 0xe0b86e });
function highlight(r) {
  hiGroup.clear();
  if (!r) { needsRender = true; return; }
  const shape = new THREE.Shape(r.polygon_xz.map(([x, z]) => new THREE.Vector2(x, -z)));
  const mesh = new THREE.Mesh(new THREE.ShapeGeometry(shape), hiMat);
  mesh.rotation.x = -Math.PI / 2; mesh.position.y = 0.04;
  const pts = r.polygon_xz.map(([x, z]) => new THREE.Vector3(x, 0.06, z));
  hiGroup.add(mesh, new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(pts), hiLine));
  needsRender = true;
}
const labelEls = rooms.map((r) => {
  const el = document.createElement('div');
  el.className = 'lbl'; el.textContent = r.name; el.dataset.zone = r.zone;
  el.addEventListener('click', () => selectRoom(r));
  $('labels').appendChild(el);
  return { r, el, w: r.name.length * 6.6 + 18, pos: new THREE.Vector3(r.centroid_xz[0], 0.35, r.centroid_xz[1]) };
});
const order = [...labelEls].sort((a, b) => b.r.area_sft - a.r.area_sft);
const _v = new THREE.Vector3();
function placeLabels() {
  const show = S.labels && (S.mode === 'overview' || S.mode === 'rooms') && !flight && camera.position.y > 3;
  $('labels').style.display = show ? 'block' : 'none';
  if (!show) return;
  const W = innerWidth, H = innerHeight, top = $('top').offsetHeight, foot = $('disclaimer').offsetHeight;
  const placed = [];                                   // panels count as taken space: no name hides under the room list or the dock
  for (const id of ['side', 'info', 'viewbar', 'tourbar', 'minimap']) {
    const e = $(id); if (!e.getClientRects().length || (id === 'side' && !e.classList.contains('open'))) continue;
    const b = e.getBoundingClientRect(); placed.push([b.left - 4, b.top - 4, b.right + 4, b.bottom + 4]);
  }
  const list = S.room ? [labelEls.find((l) => l.r === S.room), ...order.filter((l) => l.r !== S.room)] : order;
  for (const l of list) {
    _v.copy(l.pos).project(camera);
    const x = (_v.x * 0.5 + 0.5) * W, y = (-_v.y * 0.5 + 0.5) * H;
    let ok = _v.z < 1 && x > 20 && x < W - 20 && y > top + 12 && y < H - foot - 12;
    const box = [x - l.w / 2 - 3, y - 13, x + l.w / 2 + 3, y + 13];
    if (ok) ok = !placed.some((b) => !(box[2] < b[0] || box[0] > b[2] || box[3] < b[1] || box[1] > b[3]));
    l.el.style.display = ok ? 'block' : 'none';
    if (ok) { placed.push(box); l.el.style.transform = `translate(${x.toFixed(1)}px, ${y.toFixed(1)}px) translate(-50%, -50%)`; }
    l.el.classList.toggle('on', l.r === S.room);
  }
}

// ------------------------------------------------------------------ room list + search
const narrow = () => innerWidth <= 860;              // the list then covers the model, so it closes after a choice
function openSide() { $('side').classList.add('open'); document.body.classList.add('side-open'); needsRender = true; }
function closeSide() { $('side').classList.remove('open'); document.body.classList.remove('side-open'); needsRender = true; }
const groups = meta.room_groups;
function buildList(filter = '') {
  const f = filter.trim().toLowerCase();
  const list = $('roomList'); list.innerHTML = '';
  let n = 0;
  for (const g of groups) {
    const rs = rooms.filter((r) => r.group === g && (!f || `${r.name} ${r.group} ${r.description} ${r.zone}`.toLowerCase().includes(f)));
    if (!rs.length) continue;
    const h = document.createElement('div'); h.className = 'grp'; h.textContent = g; list.appendChild(h);
    for (const r of rs) {
      const b = document.createElement('button');
      b.className = 'room' + (S.room === r ? ' on' : ''); b.dataset.zone = r.zone;
      b.title = r.primary_camera ? 'Go into the room (eye level, with a photoreal render)' : 'Show the room from above';
      b.innerHTML = `<span>${r.name}</span><small>${r.area_sft.toLocaleString('en-US')} sft</small>`;
      b.addEventListener('click', () => selectRoom(r));
      list.appendChild(b); n++;
    }
  }
  if (!n) list.innerHTML = '<div class="nores">No room matches.</div>';
  return n;
}
$('search').addEventListener('input', (e) => buildList(e.target.value));
$('search').addEventListener('keydown', (e) => { if (e.key === 'Enter') { const b = $('roomList').querySelector('.room'); if (b) b.click(); } e.stopPropagation(); });
$('sideClose').onclick = () => closeSide();

// ------------------------------------------------------------------ room card (bottom left)
const COARSE = matchMedia('(pointer: coarse)').matches;
function showInfo(r, kicker, hint = '') {
  if (!r && !kicker) { $('info').classList.add('hidden'); return; }
  $('info').classList.remove('hidden');
  $('infoKicker').textContent = kicker || `${r.group}  ·  approx. ${r.area_sft.toLocaleString('en-US')} sft (${r.area_m2} m²)`;
  $('infoTitle').textContent = r ? r.name : '';
  $('infoText').textContent = r ? r.description : '';
  $('infoHint').textContent = hint;
  updateInfoButtons();
}
const photoCam = () => S.atCam || (S.mode === 'rooms' && !flight && S.room && S.room.primary_camera) || null;
function updateInfoButtons() {
  $('bPhoto').classList.toggle('hidden', !photoCam());
  $('bWalkHere').classList.toggle('hidden', !(S.mode === 'rooms' && !flight && camera.position.y < 2.4));
  $('bBack').innerHTML = S.mode === 'walk' ? '&larr; Leave walk mode' : '&larr; Back to overview';
}

// ------------------------------------------------------------------ modes
const WALK_HINT = STAGE >= 5 && !COARSE ? 'W A S D to walk · click to capture mouse · Shift = faster · Esc releases mouse / leaves walk' : COARSE ? 'Use the arrows below to walk  ·  drag to look around  ·  tap the map to jump'
  : 'W A S D or arrow keys to walk  ·  drag to look  ·  Shift = faster  ·  double-click the floor to go there  ·  Esc to leave';
function setMode(m) {
  if (m !== 'walk' && document.pointerLockElement) document.exitPointerLock();
  S.qaWalking = false;
  captureCamera = null;
  captureViewport = null;
  renderer.setScissorTest(false); renderer.setViewport(0, 0, innerWidth, innerHeight);
  S.mode = m;
  document.body.dataset.mode = m;
  for (const [id, mm] of [['mOverview', 'overview'], ['mRooms', 'rooms'], ['mWalk', 'walk'], ['mTour', 'tour']]) $(id).classList.toggle('on', m === mm);
  $('viewbar').classList.toggle('hidden', m !== 'overview');
  $('tourbar').classList.toggle('hidden', m !== 'tour');
  if (m === 'tour' || m === 'overview') $('info').classList.add('hidden');      // the tour card carries the stop text
  $('walkhint').classList.toggle('hidden', m !== 'walk');
  $('walkhint').textContent = WALK_HINT;
  $('pad').classList.toggle('hidden', !(m === 'walk' && COARSE));
  $('minimap').classList.toggle('hidden', !(m === 'walk' || m === 'tour'));
  if (m === 'tour' || m === 'walk') closeSide();
  controls.enabled = m === 'overview' && !flight;
  closeWelcome();
  needsRender = true;
}
function goOverview(pose = overviewPose()) {
  stopTour(false); hidePhoto();
  setMode('overview'); S.room = null; highlight(null); showInfo(null); buildList($('search').value);
  flyTo(pose, { inside: false, onDone: () => { controls.target.copy(pose.target || C); controls.enabled = S.mode === 'overview'; controls.update(); setOverhead(S.ceilUser, true); } });
}
function selectRoom(r, then) {
  if (!r) return;
  loadVisualRoom(r.zone);
  stopTour(false); hidePhoto();
  setMode('rooms'); S.room = r; highlight(r); buildList($('search').value);
  if (narrow()) closeSide();
  const c = r.primary_camera && cams[r.primary_camera];
  showInfo(r, null, c ? 'Drag to look around  ·  W A S D or arrows to walk on' : 'Drag to turn  ·  Shift + drag to move  ·  scroll or pinch to zoom');
  const target = c ? poseFromCamera(c) : roomAerialPose(r);
  flyTo(target, { onDone: () => {
    if (!c) {                                         // no render camera: orbit around the room from above
      setOverhead(false, true);
      controls.target.set(r.centroid_xz[0], 0, r.centroid_xz[1]); controls.enabled = S.mode === 'rooms'; controls.update();
    }
    updateInfoButtons();
    if (then) then();
  } });
}
$('mOverview').onclick = () => goOverview();
$('mRooms').onclick = () => { closeWelcome(); if ($('side').classList.contains('open')) closeSide(); else { openSide(); if (!narrow()) $('search').focus({ preventScroll: true }); } };
$('mWalk').onclick = () => startWalk();
$('mTour').onclick = () => { if (S.mode !== 'tour') startTour(0); };
$('bBack').onclick = () => goOverview();
$('bWalkHere').onclick = () => startWalk(true);
$('vReset').onclick = () => { S.ceilUser = false; $('vCeil').classList.remove('on'); goOverview(); };
$('vIso').onclick = () => goOverview(orthoCamPose(cams.CAM_ISO_SE, 24));
$('vTop').onclick = () => goOverview(overviewPose(-90, 89.5, 1.0));
$('vCeil').onclick = () => { S.ceilUser = !S.ceilUser; $('vCeil').classList.toggle('on', S.ceilUser); setOverhead(S.ceilUser, true); };
$('vLabels').onclick = () => { S.labels = !S.labels; $('vLabels').classList.toggle('on', S.labels); needsRender = true; };
$('vQuality').value = quality;
$('vQuality').onchange = (e) => applyQuality(e.target.value);
function toggleFullscreen() {
  const d = document;
  try {
    if (d.fullscreenElement || d.webkitFullscreenElement) (d.exitFullscreen || d.webkitExitFullscreen).call(d);
    else (d.documentElement.requestFullscreen || d.documentElement.webkitRequestFullscreen).call(d.documentElement);
  } catch (e) { S.errors.push('fullscreen: ' + e.message); }
}
$('mFull').onclick = toggleFullscreen;

// click a room on the model (overview)
const ray = new THREE.Raycaster(), floor = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0), ndc = new THREE.Vector2();
function floorPoint(ev) {
  ndc.set((ev.clientX / innerWidth) * 2 - 1, -(ev.clientY / innerHeight) * 2 + 1);
  ray.setFromCamera(ndc, camera);
  return ray.ray.intersectPlane(floor, new THREE.Vector3());
}
let down = null;
const el = renderer.domElement;
const eyeLevel = () => !flight && camera.position.y < 2.4;
el.addEventListener('pointerdown', (e) => {
  down = { x: e.clientX, y: e.clientY, t: performance.now() };
  if (STAGE >= 5 && S.mode === 'walk' && !COARSE && !document.pointerLockElement && !S.pointerLockUnavailable && el.requestPointerLock) {
    try {
      const request = el.requestPointerLock();
      request?.catch?.(error => { S.pointerLockUnavailable = true; S.errors.push('Mouse capture unavailable; drag to look: ' + error.message); });
      walk.drag = null;
      return; // pointer lock and pointer capture cannot own the same gesture
    } catch (error) { S.pointerLockUnavailable = true; S.errors.push('Mouse capture unavailable; drag to look: ' + error.message); }
  }
  if (S.mode === 'walk' || (S.mode === 'rooms' && eyeLevel())) {   // drag to look around (inside a room or walking)
    if (S.mode === 'rooms' && !S.freeLook) { lookFromCamera(); S.freeLook = true; }
    walk.drag = { x: e.clientX, y: e.clientY };
    try { el.setPointerCapture(e.pointerId); } catch { /* cancelled gesture: drag remains a safe fallback */ }
  }
});
el.addEventListener('pointerup', (e) => {
  walk.drag = null;
  if (!down || Math.hypot(e.clientX - down.x, e.clientY - down.y) > 5 || performance.now() - down.t > 600) return;
  if (S.mode === 'overview' || (S.mode === 'rooms' && camera.position.y > 3)) {
    const p = floorPoint(e); const r = p && roomAt(p.x, p.z);
    if (r) selectRoom(r);
  }
});
el.addEventListener('pointermove', (e) => {
  if (STAGE >= 5 && document.pointerLockElement === el && S.mode === 'walk') {
    walk.yaw -= e.movementX * 0.0022; walk.pitch = THREE.MathUtils.clamp(walk.pitch - e.movementY * 0.0022, -1.35, 1.35);
    applyWalkLook(); return;
  }
  if ((S.mode === 'walk' || S.mode === 'rooms') && walk.drag) {
    walk.yaw -= (e.clientX - walk.drag.x) * 0.0035;
    walk.pitch = THREE.MathUtils.clamp(walk.pitch - (e.clientY - walk.drag.y) * 0.0035, -1.2, 1.2);
    walk.drag = { x: e.clientX, y: e.clientY };
    applyWalkLook(); S.atCam = null; updateInfoButtons();
  } else if (S.mode === 'overview' && !flight) {
    const p = floorPoint(e); const r = p && roomAt(p.x, p.z);
    el.style.cursor = r ? 'pointer' : 'grab';
    if (r !== S.hover) { S.hover = r; highlight(r || S.room); }
  }
});

// a trackpad pinch must zoom the model, never the page (Firefox / Chrome send ctrl + wheel, Safari gesture events)
addEventListener('wheel', (e) => { if (e.ctrlKey) e.preventDefault(); }, { passive: false });
for (const t of ['gesturestart', 'gesturechange']) document.addEventListener(t, (e) => e.preventDefault(), { passive: false });

// ------------------------------------------------------------------ walk mode
const walk = { yaw: 0, pitch: 0, eye: 1.6, keys: {}, drag: null, glide: null };
const walking = createWalking({ position: camera.position, blocked, eye: 1.6, updateActors: (dt, playerPosition) => dressing?.update(dt, { camera, playerPosition, quality }) });
addEventListener('pointerlockchange', () => { walk.drag = null; walk.keys = {}; });
function applyWalkLook() { camera.quaternion.setFromEuler(new THREE.Euler(walk.pitch, walk.yaw, 0, 'YXZ')); needsRender = true; }
function lookFromCamera() {                           // yaw / pitch from the current view; a lens-shifted view becomes an equivalent up / down look
  const e = new THREE.Euler().setFromQuaternion(camera.quaternion, 'YXZ');
  walk.yaw = e.y;
  const sh = currentPose().shift, f = (innerHeight / 2) / Math.tan(THREE.MathUtils.degToRad(camera.fov) / 2);
  walk.pitch = e.x + Math.atan((sh * Math.max(innerWidth, innerHeight)) / f);
  camera.clearViewOffset(); camera.updateProjectionMatrix();
  applyWalkLook();
}
function enterWalkFromCamera() {
  walk.eye = STAGE >= 5 ? 1.6 : THREE.MathUtils.clamp(camera.position.y, 1.2, 1.7);
  if (STAGE >= 5) {
    const safe = nearestWalkPoint(camera.position.x, camera.position.z, S.room);
    if (!safe) { S.errors.push('No verified walking start in this room.'); goOverview(); return; }
    camera.position.x = safe[0]; camera.position.z = safe[1]; walking.reset();
  }
  camera.position.y = walk.eye;
  lookFromCamera();
}
const walkCard = (r) => { loadVisualRoom(r.zone); showInfo(r, `You are in  ·  ${r.group}  ·  approx. ${r.area_sft.toLocaleString('en-US')} sft`); };
function startWalk(here = false) {
  stopTour(false); hidePhoto();
  if (here && camera.position.y < 2.4) {
    setMode('walk'); enterWalkFromCamera();
    const r = roomAt(camera.position.x, camera.position.z); if (r) { S.room = r; walkCard(r); }
    updateInfoButtons(); return;
  }
  const start = poseFromCamera(cams.CAM_03_Entrance_Lobby);
  S.room = byZone.Z01; highlight(null); walkCard(byZone.Z01);
  setMode('walk');
  flyTo(start, { onDone: () => { setOverhead(true, true); enterWalkFromCamera(); } });
}
function walkStep(dt) {
  if (STAGE >= 5) {
    const k = walk.keys;
    const previousX = camera.position.x, previousZ = camera.position.z;
    walking.step({ forward: (k.KeyW || k.ArrowUp ? 1 : 0) - (k.KeyS || k.ArrowDown ? 1 : 0), strafe: (k.KeyD || k.ArrowRight ? 1 : 0) - (k.KeyA || k.ArrowLeft ? 1 : 0), yaw: walk.yaw, dt, fast: k.ShiftLeft || k.ShiftRight });
    afterWalking();
    if (camera.position.x !== previousX || camera.position.z !== previousZ) needsRender = true;
    return;
  }
  if (walk.glide) {
    const g = walk.glide; g.t = Math.min(1, g.t + dt / g.dur);
    camera.position.lerpVectors(g.from, g.to, ease(g.t)); needsRender = true;
    if (g.t >= 1) walk.glide = null;
    return;
  }
  const k = walk.keys;
  const turn = (k.ArrowRight ? 1 : 0) - (k.ArrowLeft ? 1 : 0);
  if (turn) { walk.yaw -= turn * 1.6 * dt; applyWalkLook(); }
  const f = (k.KeyW || k.ArrowUp ? 1 : 0) - (k.KeyS || k.ArrowDown ? 1 : 0), s = (k.KeyD ? 1 : 0) - (k.KeyA ? 1 : 0);
  if (!f && !s) return;
  S.atCam = null; updateInfoButtons();
  const sp = (k.ShiftLeft || k.ShiftRight ? 3.0 : 1.4) * dt;
  const fx = -Math.sin(walk.yaw), fz = -Math.cos(walk.yaw);
  let dx = (fx * f + -fz * s), dz = (fz * f + fx * s);
  const n = Math.hypot(dx, dz), steps = Math.ceil(sp / 0.04);    // small sub-steps: never jump over a thin wall
  dx = (dx / n) * (sp / steps); dz = (dz / n) * (sp / steps);
  const p = camera.position;
  for (let i = 0; i < steps; i++) {
    const free = !blocked(p.x, p.z);
    if (!free || !blocked(p.x + dx, p.z + dz)) p.set(p.x + dx, walk.eye, p.z + dz);
    else if (!blocked(p.x + dx, p.z)) p.x += dx;                  // slide along the obstacle
    else if (!blocked(p.x, p.z + dz)) p.z += dz;
    else break;
  }
  const r = roomAt(p.x, p.z);                                        // the card follows the room you walk into
  if (r && r !== S.room) { S.room = r; walkCard(r); }
  needsRender = true;
}
el.addEventListener('dblclick', (e) => {
  if (S.mode !== 'walk' || STAGE >= 5) return;
  const p = floorPoint(e); if (!p) return;
  const to = new THREE.Vector3(p.x, walk.eye, p.z);
  if (blocked(to.x, to.z) || !pathClear(camera.position, to)) return;
  walk.glide = { from: camera.position.clone(), to, t: 0, dur: Math.max(0.5, camera.position.distanceTo(to) / 2) };
});
const MOVE_KEYS = new Set(['KeyW', 'KeyA', 'KeyS', 'KeyD', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight']);
addEventListener('keydown', (e) => {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') return;
  if (!$('welcome').classList.contains('hidden')) { if (e.code === 'Escape' || e.code === 'KeyH') closeWelcome(); return; }
  walk.keys[e.code] = true;
  if (e.code === 'Escape') { if (!$('photo').classList.contains('hidden')) { hidePhoto(); if (S.tour) S.tour.photoSkip = true; } else if (S.mode !== 'overview') goOverview(); }
  else if (e.code === 'Space' && S.mode === 'tour') { e.preventDefault(); togglePlay(); }
  else if (S.mode === 'tour' && e.code === 'ArrowRight') nextStop(1);
  else if (S.mode === 'tour' && e.code === 'ArrowLeft') nextStop(-1);
  else if (S.mode === 'rooms' && MOVE_KEYS.has(e.code) && eyeLevel()) startWalk(true);   // walk on from the room view
  else if (e.code === 'KeyF') toggleFullscreen();
  else if (e.code === 'KeyH' || e.key === '?') openWelcome();
  else if (S.mode !== 'walk' && S.mode !== 'tour') {
    if (e.code === 'KeyO') goOverview(); else if (e.code === 'KeyT') startTour(0); else if (e.code === 'KeyW') startWalk();
    else if (e.code === 'KeyR') $('mRooms').click();
    else if (e.code === 'KeyC' && S.mode === 'overview') $('vCeil').click(); else if (e.code === 'KeyL') $('vLabels').click();
    else if (e.code === 'KeyP' && photoCam()) showPhoto(photoCam());
  }
  if ((S.mode === 'walk' || S.mode === 'tour') && e.code.startsWith('Arrow')) e.preventDefault();
});
addEventListener('keyup', (e) => { walk.keys[e.code] = false; });
addEventListener('blur', () => { walk.keys = {}; });
for (const b of document.querySelectorAll('#pad button')) {
  const k = b.dataset.k;
  b.addEventListener('pointerdown', (e) => { e.preventDefault(); walk.keys[k] = true; });
  for (const ev of ['pointerup', 'pointerleave', 'pointercancel']) b.addEventListener(ev, () => { walk.keys[k] = false; });
}

// minimap (walk grid)
const mm = $('minimap'), mctx = mm.getContext('2d');
const mmScale = Math.min((mm.width - 10) / (grid.cols * grid.res), (mm.height - 10) / (grid.rows * grid.res));
const mmBase = document.createElement('canvas');
mmBase.width = mm.width; mmBase.height = mm.height;
{
  const b = mmBase.getContext('2d'), img = b.createImageData(grid.cols, grid.rows);
  for (let i = 0; i < grid.cols * grid.rows; i++) {
    const on = (gbits[i >> 3] >> (i & 7)) & 1;
    img.data.set(on ? [32, 42, 36, 255] : [214, 221, 214, 255], i * 4);
  }
  const t = document.createElement('canvas'); t.width = grid.cols; t.height = grid.rows; t.getContext('2d').putImageData(img, 0, 0);
  b.imageSmoothingEnabled = true;
  b.drawImage(t, 5, 5, grid.cols * grid.res * mmScale, grid.rows * grid.res * mmScale);
}
const toMM = (x, z) => [5 + (x - grid.origin_xz[0]) * mmScale, 5 + (z - grid.origin_xz[1]) * mmScale];
function drawMinimap() {
  if (mm.classList.contains('hidden')) return;
  mctx.clearRect(0, 0, mm.width, mm.height); mctx.drawImage(mmBase, 0, 0);
  if (S.room) {
    mctx.strokeStyle = '#C29A55'; mctx.lineWidth = 1.5; mctx.beginPath();
    S.room.polygon_xz.forEach(([x, z], i) => { const [a, b] = toMM(x, z); i ? mctx.lineTo(a, b) : mctx.moveTo(a, b); }); mctx.closePath(); mctx.stroke();
  }
  const [px, py] = toMM(camera.position.x, camera.position.z);
  const d = new THREE.Vector3(0, 0, -1).applyQuaternion(camera.quaternion);
  const a = Math.atan2(d.z, d.x);
  mctx.fillStyle = 'rgba(38,103,61,.35)'; mctx.beginPath(); mctx.moveTo(px, py); mctx.arc(px, py, 22, a - 0.6, a + 0.6); mctx.closePath(); mctx.fill();
  mctx.fillStyle = '#26673D'; mctx.strokeStyle = '#fff'; mctx.lineWidth = 2; mctx.beginPath(); mctx.arc(px, py, 4.5, 0, 7); mctx.fill(); mctx.stroke();
}
mm.addEventListener('click', (e) => {
  if (S.mode !== 'walk') return;
  const rc = mm.getBoundingClientRect();
  const x = grid.origin_xz[0] + (e.clientX - rc.left - 5) / mmScale, z = grid.origin_xz[1] + (e.clientY - rc.top - 5) / mmScale;
  if (blocked(x, z)) return;
  const to = new THREE.Vector3(x, walk.eye, z);
  if (pathClear(camera.position, to)) walk.glide = { from: camera.position.clone(), to, t: 0, dur: Math.max(0.5, camera.position.distanceTo(to) / 2.2) };
  else flyTo({ pos: to, quat: camera.quaternion.clone(), fov: camera.fov, shift: 0 }, { inside: true, onDone: () => { setMode('walk'); setOverhead(true, true); enterWalkFromCamera(); } });
  S.room = roomAt(x, z); if (S.room) walkCard(S.room);
});

// ------------------------------------------------------------------ photoreal render panel
function showPhoto(camName) {
  const c = cams[camName]; if (!c) return;
  if (!S.photo) S.sideWasOpen = $('side').classList.contains('open');
  closeSide();
  const img = $('photoImg');
  img.onload = () => { $('photo').classList.add('show'); };
  img.onerror = () => { hidePhoto(); S.errors.push('render not found: ' + c.render.file); };
  img.alt = `Photoreal render ${camName}`;
  $('photo').classList.remove('hidden');
  $('photo').classList.remove('show');
  img.src = RENDERS + camName + '.jpg';
  S.photo = camName;
}
function hidePhoto() {
  if ($('photo').classList.contains('hidden')) return;
  $('photo').classList.remove('show');
  S.photo = null;
  if (S.sideWasOpen && S.mode !== 'tour' && S.mode !== 'walk' && !narrow()) openSide();
  S.sideWasOpen = false;
  setTimeout(() => { if (!S.photo) $('photo').classList.add('hidden'); }, 700);
}
$('bPhoto').onclick = () => photoCam() && showPhoto(photoCam());
$('photoClose').onclick = () => { hidePhoto(); if (S.tour) S.tour.photoSkip = true; };
function preload(camName) { if (camName && cams[camName]) { const i = new Image(); i.src = RENDERS + camName + '.jpg'; } }

// ------------------------------------------------------------------ guided tour (16 stops)
const stops = meta.tour;
const HOLD = 6.5;
const segs = stops.map((st, i) => {
  const d = document.createElement('div'); d.title = `${i + 1}. ${st.title}`;
  d.appendChild(document.createElement('i')); d.addEventListener('click', () => S.tour && goStop(i));
  $('tSegs').appendChild(d); return d.firstChild;
});
function stopPose(st, which = 'camera') {
  const c = cams[st[which]];
  if (c.type === 'ORTHO') return orthoCamPose(c, 30);
  return poseFromCamera(c);
}
function startTour(i = 0) {
  hidePhoto(); S.room = null; highlight(null); closeSide(); showInfo(null);
  setMode('tour');
  S.tour = { i: 0, phase: 'fly', t: 0, playing: true, sub: 0 };
  goStop(i);
}
function goStop(i) {
  const T = S.tour; if (!T) return;
  hidePhoto();
  T.i = THREE.MathUtils.clamp(i, 0, stops.length - 1); T.sub = 0; T.phase = 'fly'; T.t = 0; T.photoSkip = false; T.done = false;
  const st = stops[T.i];
  S.room = st.zone ? byZone[st.zone] : null;
  if (S.room) loadVisualRoom(S.room.zone);
  $('tCount').textContent = `Stop ${T.i + 1} of ${stops.length}`;
  $('tKicker').textContent = S.room ? `${S.room.group}  ·  approx. ${S.room.area_sft.toLocaleString('en-US')} sft` : 'The whole floor';
  $('tTitle').textContent = st.title; $('tText').textContent = st.description;
  $('tPrev').disabled = T.i === 0; $('tNext').disabled = T.i === stops.length - 1;
  preload(st.camera); preload(st.also_camera);
  const p = stopPose(st);
  const outside = cams[st.camera].type === 'ORTHO';
  flyTo(p, { inside: !outside, onDone: () => { if (!S.tour) return; if (!outside) setOverhead(true, true); else setOverhead(false, true); S.tour.phase = 'hold'; S.tour.t = 0; } });
  updateSegs(); updatePlay();
}
function nextStop(d) { if (S.tour) goStop(S.tour.i + d); }
function stopTour(toOverview = true) {
  if (!S.tour) return;
  S.tour = null; hidePhoto(); flight = null;
  if (toOverview) goOverview();
}
function togglePlay() {
  if (!S.tour) return;
  if (S.tour.done) { S.tour.playing = true; goStop(0); return; }      // the end card: play the tour again
  S.tour.playing = !S.tour.playing; updatePlay();
}
function updatePlay() {
  const T = S.tour;
  $('tPlay').innerHTML = T && T.done ? '&#8635; Play again' : T && !T.playing ? '&#9654; Resume' : '&#10073;&#10073; Pause';
}
function updateSegs() {
  const T = S.tour; if (!T) return;
  segs.forEach((s, i) => { s.style.width = i < T.i ? '100%' : i > T.i ? '0%' : `${Math.round(Math.min(1, (T.phase === 'hold' ? 0.3 + 0.7 * (T.t / HOLD) : 0.3 * (flight ? flight.t : 0))) * 100)}%`; });
}
function tourStep(dt) {
  const T = S.tour; if (!T) return;
  updateSegs();
  if (T.phase !== 'hold' || !T.playing) return;
  const st = stops[T.i], cam = T.sub ? st.also_camera : st.camera, c = cams[cam];
  T.t += dt;
  if (c.type === 'ORTHO') {                                 // slow orbit on the overview stops
    const e = new THREE.Euler().setFromQuaternion(camera.quaternion, 'YXZ');
    const off = camera.position.clone().sub(C).applyAxisAngle(new THREE.Vector3(0, 1, 0), dt * 0.05);
    camera.position.copy(C).add(off); camera.lookAt(C); needsRender = true; void e;
  } else if ($('tPhoto').checked && !T.photoSkip && T.t > 0.6 && S.photo !== cam && T.t < HOLD - 1.2) showPhoto(cam);
  if (T.t >= HOLD - 0.7 && S.photo) hidePhoto();
  if (T.t >= HOLD) {
    if (st.also_camera && !T.sub) {
      T.sub = 1; T.phase = 'fly'; T.t = 0;
      const z2 = byZone[st.also_zone]; if (z2) { S.room = z2; loadVisualRoom(z2.zone); }
      flyTo(stopPose(st, 'also_camera'), { inside: true, onDone: () => { if (S.tour) { setOverhead(true, true); S.tour.phase = 'hold'; S.tour.t = 0; } } });
    } else if (T.i + 1 < stops.length) goStop(T.i + 1);
    else { T.playing = false; T.done = true; T.t = HOLD; updatePlay(); }       // stay on the final view; End tour / Play again
  }
}
$('tPrev').onclick = () => nextStop(-1);
$('tNext').onclick = () => nextStop(1);
$('tPlay').onclick = () => togglePlay();
$('tStop').onclick = () => stopTour(true);

// ------------------------------------------------------------------ loop
function measureChrome() {                            // header / footer heights drive the panel positions in style.css
  const r = document.documentElement.style;
  r.setProperty('--top-h', $('top').offsetHeight + 'px'); r.setProperty('--foot-h', $('disclaimer').offsetHeight + 'px');
}
let wasNarrow = narrow();
addEventListener('resize', () => {
  if (narrow() && !wasNarrow) closeSide();            // e.g. a tablet turned to portrait: the list would cover the view
  wasNarrow = narrow();
  camera.aspect = innerWidth / innerHeight;
  if (S.atCam && cams[S.atCam].lens) applyPose(poseFromCamera(cams[S.atCam]));
  camera.updateProjectionMatrix(); renderer.setSize(innerWidth, innerHeight); sizeAO(); measureChrome(); needsRender = true;
});
// ------------------------------------------------------------------ welcome / help card
function openWelcome() { $('welcome').classList.remove('hidden'); $('wTour').focus({ preventScroll: true }); }
function closeWelcome() {
  if ($('welcome').classList.contains('hidden')) return;
  $('welcome').classList.add('hidden');
  try { localStorage.setItem('tourWelcomeSeen', '1'); } catch (e) { /* storage blocked */ }
}
$('mHelp').onclick = () => ($('welcome').classList.contains('hidden') ? openWelcome() : closeWelcome());
$('wClose').onclick = () => closeWelcome();
$('wTour').onclick = () => startTour(0);
$('wWalk').onclick = () => startWalk();
$('wRooms').onclick = () => { closeWelcome(); openSide(); };
$('welcome').addEventListener('click', (e) => { if (e.target === $('welcome')) closeWelcome(); });
const clock = new THREE.Clock();
let frames = 0, fpsT = 0;
function renderScene() {
  if (probes?.status.capturing) return;
  dressing?.prepareView(captureCamera || camera);
  if (captureCamera && captureViewport) {
    const { x, y, width, height } = captureViewport;
    renderer.setScissorTest(false); renderer.setViewport(0, 0, innerWidth, innerHeight);
    renderer.setClearColor(0x000000, 1); renderer.clear();
    renderer.setScissor(x, y, width, height); renderer.setViewport(x, y, width, height); renderer.setScissorTest(true);
    if (POST) POST.render(captureCamera, width, height); else renderer.render(scene, captureCamera);
    renderer.setScissorTest(false); renderer.setViewport(0, 0, innerWidth, innerHeight);
    renderer.setClearColor(0x000000, 0);
  } else if (POST) POST.render(camera); else renderer.render(scene, camera);
}
renderer.setAnimationLoop(() => {
  const dt = Math.min(clock.getDelta(), 1.0);             // time-based: flights and tour stops end on time even on slow GPUs
  if (flight) flightStep(dt);                           // Back / Next also fly while the tour is paused; pause stops the stop timer
  if ((S.mode === 'overview' || S.mode === 'rooms') && controls.enabled) controls.update();
  if (S.mode === 'walk' && !flight && !S.qaWalking) walkStep(dt);
  if (S.mode === 'tour') tourStep(dt);
  if (dressing && !S.qaWalking && !captureCamera && (S.mode !== 'walk' || flight)) dressing.update(dt, { camera, playerPosition: S.mode === 'walk' ? camera.position : null, quality });
  if (needsRender && !probes?.status.capturing) {
    const want = camera.position.y < 2.6 ? 'inside' : 'outside';     // lighting follows the camera height
    if (want !== lookPreset) look(want);
    hiGroup.visible = !captureCamera && camera.position.y > 2.6;     // no highlights in reference-camera captures
    if (SHADOWS && lookPreset === 'inside') placeSun();
    renderScene();
    if (S.timings.baseFirstViewMs == null) S.timings.baseFirstViewMs = performance.now();
    if (pendingSwap) { captureDissolve(); pendingSwap(); pendingSwap = null; renderScene(); }
    if (!captureCamera) { placeLabels(); drawMinimap(); }
    updateLightingStatus();
    needsRender = false; frames++;
    if (AO) { AO.pending = !captureCamera; AO.last = performance.now(); }
  } else if (!probes?.status.capturing && AO && AO.pending && !flight && !walk.drag && performance.now() - AO.last > 250) {
    try { AO.composer.render(); AO.pending = false; S.aoFrames = (S.aoFrames || 0) + 1; }  // the still view, with contact shadows
    catch (e) { AO = null; S.errors.push('ambient occlusion off: ' + e.message); needsRender = true; }
  }
  fpsT += dt; if (fpsT > 1) { S.fps = frames / fpsT; frames = 0; fpsT = 0; }
});

// ------------------------------------------------------------------ start
buildList();
measureChrome();
if (aoWanted()) setupAO();
if (USE_POST) { POST = createPostProcessing({ renderer, scene, camera, quality, changed: () => { needsRender = true; } }); S.post = POST.status; }
setMode('overview');
if (!narrow()) openSide();
overhead.visible = false;
const start = overviewPose();
applyPose(start); controls.target.copy(C); controls.update(); look('outside');
$('loading').style.display = 'none';
S.ready = true; window.__viewerReady = true;
$('mPeople').hidden = !(USE_DRESSING && PEOPLE_ACCEPTED);
$('mPeople').onclick = () => setPeopleEnabled(!dressing?.peopleStats().enabled).catch(e => { S.errors.push('People: ' + e.message); });
if (USE_DRESSING) setTimeout(() => ensureDressing().then(() => { if (PEOPLE_ACCEPTED && qs.get('people') !== '0') return setPeopleEnabled(true); }).catch(e => { S.errors.push('Dressing: ' + e.message); }), 0);
// links: ?room=Z08 opens a room, ?tour=1 starts the tour, ?walk=1 starts walking; ?welcome=0 / 1 hides / forces the help card
{
  const z = qs.get('room'), w = qs.get('welcome');
  let seen = false; try { seen = localStorage.getItem('tourWelcomeSeen') === '1'; } catch (e) { /* storage blocked */ }
  if (z && byZone[z]) selectRoom(byZone[z]);
  else if (qs.get('tour') === '1') startTour(0);
  else if (qs.get('walk') === '1') startWalk();
  else if (w === '1' || (w !== '0' && !seen)) openWelcome();
}
let meshes = 0; model.traverse((o) => { if (o.isMesh) meshes++; });
S.counts = { quality, stage: STAGE, floorTopTriangles: floorTriangles.length, meshes, drawCallsMerged: drawCalls, rooms: rooms.length, cameras: meta.cameras.length, stops: stops.length, model: gltf.scene.getObjectByName('WEB_INTERIOR') ? 'web' : 'original', bakedLight: BAKED, shadows: SHADOWS, ambientOcclusion: !!AO };
S.api = { frameCamera, gpuInfo, gpuMemoryEstimate: () => estimateGpuMemory({ scene, textures: [...(materialUpgrade?.textures() || []), ...(dressing?.textures() || [])], targets: [...(POST?.targets() || []), ...(probes?.targets() || []), ...(AO ? [AO.composer.renderTarget1, AO.composer.renderTarget2, ...Object.values(AO.gtao).filter(o => o?.isWebGLRenderTarget)] : [])] }), setPeopleEnabled, peopleStats: () => dressing?.peopleStats() || { enabled: false, loaded: false, total: 0, visible: 0 }, peopleDiagnostics: () => dressing?.peopleDiagnostics() || [], setBakeIsolation, lookState: () => ({ yaw: walk.yaw, pitch: walk.pitch, pointerLocked: document.pointerLockElement === el, eye: walk.eye }), previewLightmap: (id,url,format) => lightmaps.previewTexture(id,url,format), setWalkQAStart, stepWalkQA, walkState: () => walking.state(), loadRoomLightmap: (id) => loadVisualRoom(id), lighting: () => lightmaps.status, renderStats: () => ({ ...renderer.info.render, memory: { ...renderer.info.memory }, phase: STAGE, capturePostProcessing: !!POST, post: POST?.status || null }), setLightmapIntensity: (id, intensity) => { const room = lightmaps.rooms.get(id); if (room?.ownedMaterials) { room.ownedMaterials.forEach(m => { m.lightMapIntensity = intensity; }); needsRender = true; } }, setLightmapFlip: (id, flip) => { const texture = lightmaps.rooms.get(id)?.texture; if (texture) { texture.repeat.y = flip ? -1 : 1; texture.offset.y = flip ? 1 : 0; texture.updateMatrix(); needsRender = true; } }, selectRoom: (z) => selectRoom(byZone[z]), goOverview, startWalk, startTour, goStop, nextStop, togglePlay, stopTour, showPhoto, hidePhoto,
  blocked, state: () => ({ mode: S.mode, room: S.room && S.room.zone, atCam: S.atCam, flying: !!flight, flightT: flight ? +flight.t.toFixed(3) : null, fps: S.fps, overhead: overhead.visible,
    tour: S.tour && { i: S.tour.i, phase: S.tour.phase, playing: S.tour.playing, sub: S.tour.sub, done: !!S.tour.done }, photo: S.photo, aoFrames: S.aoFrames || 0, pos: camera.position.toArray().map((v) => +v.toFixed(3)) }) };


// Review-only exact camera framing, including the five orthographic reference views.
// No screenshot pose is substituted for normal walk/tour navigation.
function gpuInfo() {
  const gl = renderer.getContext(), debug = gl.getExtension('WEBGL_debug_renderer_info');
  return { userAgent: navigator.userAgent, vendor: gl.getParameter(debug ? debug.UNMASKED_VENDOR_WEBGL : gl.VENDOR),
    renderer: gl.getParameter(debug ? debug.UNMASKED_RENDERER_WEBGL : gl.RENDERER),
    webgl: gl.getParameter(gl.VERSION), maxTextureSize: gl.getParameter(gl.MAX_TEXTURE_SIZE),
    pixelRatio: renderer.getPixelRatio(), quality, viewport: [innerWidth, innerHeight] };
}
async function frameCamera(name, { lighting = true } = {}) {
  const c = cams[name];
  if (!c) throw new Error(`Unknown reference camera: ${name}`);
  stopTour(false); hidePhoto(); closeWelcome(); flight = null; pendingSwap = null; controls.enabled = false;
  S.mode = 'capture'; S.atCam = name; S.room = byZone[c.zone] || null;
  document.body.dataset.mode = 'capture';
  if (lighting && c.zone) await loadVisualRoom(c.zone);
  if (POST) await POST.ready;
  const aspect = c.render.width / c.render.height;
  const fitWidth = Math.min(innerWidth, innerHeight * aspect), fitHeight = fitWidth / aspect;
  captureViewport = { x: (innerWidth - fitWidth) / 2, y: (innerHeight - fitHeight) / 2, width: fitWidth, height: fitHeight };
  if (c.type === 'ORTHO') {
    const width = aspect >= 1 ? c.ortho_scale : c.ortho_scale * aspect;
    const height = aspect >= 1 ? c.ortho_scale / aspect : c.ortho_scale;
    captureCamera = new THREE.OrthographicCamera(-width / 2, width / 2, height / 2, -height / 2, c.clip[0], c.clip[1]);
  } else {
    const fov = THREE.MathUtils.radToDeg(2 * Math.atan((c.sensor_width || 36) / (2 * c.lens * Math.max(1, aspect))));
    captureCamera = new THREE.PerspectiveCamera(fov, aspect, c.clip[0], c.clip[1]);
  }
  captureCamera.position.fromArray(c.position); captureCamera.quaternion.fromArray(c.quaternion_xyzw);
  if (c.shift_x || c.shift_y) captureCamera.setViewOffset(c.render.width, c.render.height, (c.shift_x || 0) * Math.max(c.render.width, c.render.height), -(c.shift_y || 0) * Math.max(c.render.width, c.render.height), c.render.width, c.render.height);
  captureCamera.updateProjectionMatrix(); captureCamera.updateMatrixWorld(true);
  dressing?.update(0, { camera: captureCamera, playerPosition: null, quality });
  camera.position.copy(captureCamera.position); camera.quaternion.copy(captureCamera.quaternion);
  setOverhead(c.type !== 'ORTHO'); hiGroup.visible = false;
  look(c.type === 'ORTHO' ? 'outside' : 'inside');
  if (c.zone && lightmaps.rooms.get(c.zone)?.spec.exposure) renderer.toneMappingExposure = lightmaps.rooms.get(c.zone).spec.exposure;
  if (AO) AO.pending = false;
  needsRender = true;
  await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  return { name, type: c.type, lighting: lightmaps.status.rooms[c.zone] || null };
}


function nearestWalkPoint(x, z, room) {
  const allowed = (px, pz) => !blocked(px, pz) && (!room || inPoly(px, pz, room.polygon_xz));
  if (allowed(x, z)) return [x, z];
  let best = null, distance = Infinity;
  for (let row = 0; row < grid.rows; row++) for (let col = 0; col < grid.cols; col++) {
    const px = grid.origin_xz[0] + (col + 0.5) * grid.res, pz = grid.origin_xz[1] + (row + 0.5) * grid.res;
    const d = Math.hypot(px - x, pz - z);
    if (d < distance && allowed(px, pz)) { best = [px, pz]; distance = d; }
  }
  return best;
}
function afterWalking() {
  const room = roomAt(camera.position.x, camera.position.z);
  if (room && room !== S.room) { S.room = room; walkCard(room); }
}
function setWalkQAStart(x, z) {
  if (STAGE < 5) throw new Error('Movement review requires stage=5');
  if (blocked(x, z)) throw new Error('QA start is blocked or outside the floor');
  stopTour(false); hidePhoto(); closeWelcome(); setMode('walk'); flight = null; pendingSwap = null;
  camera.position.set(x, 1.6, z); camera.clearViewOffset(); walking.reset();
  S.qaWalking = true; S.qaStartCount = (S.qaStartCount || 0) + 1;
  setOverhead(true); afterWalking(); needsRender = true;
  return { ...walking.state(), startCount: S.qaStartCount };
}
function stepWalkQA(input) {
  if (STAGE < 5 || !S.qaWalking) throw new Error('Start a stage=5 movement review first');
  walk.yaw = input.yaw || 0; applyWalkLook();
  const state = walking.step(input);
  afterWalking();
  return { ...state, blocked: blocked(camera.position.x, camera.position.z), room: roomAt(camera.position.x, camera.position.z)?.zone || null, startCount: S.qaStartCount };
}


const isolationVisibility = new Map();
function setBakeIsolation(enabled) {
  if (!enabled) { isolationVisibility.forEach((visible, mesh) => { mesh.visible = visible; }); isolationVisibility.clear(); }
  else model.traverse(mesh => {
    if (!mesh.isMesh) return;
    let node = mesh, baked = false;
    while (node) { if (node.name.startsWith('CYCLES_')) baked = true; node = node.parent; }
    if (!baked) { if (!isolationVisibility.has(mesh)) isolationVisibility.set(mesh, mesh.visible); mesh.visible = false; }
  });
  needsRender = true;
}
