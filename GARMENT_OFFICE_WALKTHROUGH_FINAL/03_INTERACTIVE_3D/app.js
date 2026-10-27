// Interactive 3D tour of the proposed ground-floor office (three.js r169, local files only).
// Model: model/Final_Office_Interior.glb (the approved Blender model, unchanged). Data: data/office_tour.json.
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { CSS2DRenderer, CSS2DObject } from 'three/addons/renderers/CSS2DRenderer.js';

const $ = (id) => document.getElementById(id);
const state = { mode: 'loading', ceilings: false, labels: true, tour: null, ready: false, errors: [] };
window.__viewer = state;

// ------------------------------------------------------------------ renderer, scene, lights
const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
const qs = new URLSearchParams(location.search);            // ?scale=0.5 renders fewer pixels (slow / software GPUs)
renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75) * Math.min(1, Math.max(0.25, parseFloat(qs.get('scale')) || 1)));
renderer.setSize(innerWidth, innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.AgXToneMapping;          // same view transform family as the Blender renders
renderer.toneMappingExposure = 1.2;
$('app').appendChild(renderer.domElement);
const labelRenderer = new CSS2DRenderer();
labelRenderer.setSize(innerWidth, innerHeight);
Object.assign(labelRenderer.domElement.style, { position: 'fixed', inset: '0', pointerEvents: 'none' });
$('app').appendChild(labelRenderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0b1018);
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
scene.environmentIntensity = 0.85;
scene.add(new THREE.HemisphereLight(0xfff3e6, 0x45423d, 0.9));
const sun = new THREE.DirectionalLight(0xfff6ec, 1.1);
sun.position.set(25, 50, 15);
scene.add(sun);

const camera = new THREE.PerspectiveCamera(40, innerWidth / innerHeight, 0.05, 600);
const controls = new OrbitControls(camera, renderer.domElement);
Object.assign(controls, { enableDamping: true, dampingFactor: 0.08, maxPolarAngle: Math.PI * 0.47, minDistance: 3, maxDistance: 160, screenSpacePanning: true });

// ------------------------------------------------------------------ data + model
const data = await (await fetch('data/office_tour.json')).json();
const C = new THREE.Vector3(...data.centre);
const views = Object.fromEntries(data.views.map((v) => [v.id, v]));
let model, overhead = [], solid = [], everything = [];

function progress(e) {
  const total = e.lengthComputable ? e.total : 41.9e6;
  const p = Math.min(100, Math.round((e.loaded / total) * 100));
  $('loadBar').style.width = p + '%';
  $('loadText').textContent = `${p} %  (${(e.loaded / 1e6).toFixed(1)} MB)`;
}
try {
  const gltf = await new Promise((res, rej) => new GLTFLoader().load('model/Final_Office_Interior.glb', res, progress, rej));
  model = gltf.scene;
} catch (err) {
  $('loadText').textContent = 'Could not load the model. Start the viewer through a local web server (see README).';
  state.errors.push(String(err));
  throw err;
}
const sanitize = THREE.PropertyBinding.sanitizeNodeName;
const overheadNames = new Set(data.overhead.map(sanitize));
const solidNames = new Set(data.solid.map(sanitize));
const maxAniso = renderer.capabilities.getMaxAnisotropy();
model.traverse((o) => {
  if (overheadNames.has(o.name)) overhead.push(o);
  if (solidNames.has(o.name)) o.traverse((m) => m.isMesh && solid.push(m));
  if (o.isMesh) {
    everything.push(o);
    for (const m of Array.isArray(o.material) ? o.material : [o.material]) {
      if (m.transmission > 0 || (m.transparent && m.opacity < 1)) {     // glass: cheap see-through instead of a transmission pass
        m.transmission = 0; m.transparent = true; m.opacity = Math.min(m.opacity ?? 1, 0.25); m.depthWrite = false;
        m.roughness = 0.05; m.metalness = 0;
      }
      for (const k of ['map', 'normalMap', 'roughnessMap']) if (m[k]) m[k].anisotropy = maxAniso;
    }
  }
  o.matrixAutoUpdate = false;
  o.updateMatrix();
});
scene.add(model);
model.updateMatrixWorld(true);

// ------------------------------------------------------------------ labels + room list
const labels = [];
for (const r of data.rooms) {
  const div = document.createElement('div');
  div.className = 'label3d';
  div.textContent = r.name;
  div.style.pointerEvents = 'auto';
  div.addEventListener('click', () => goRoom(r));
  const obj = new CSS2DObject(div);
  obj.position.set(r.centre[0], 3.2, r.centre[2]);
  scene.add(obj);
  labels.push(obj);
}
const groups = {};
for (const r of data.rooms) (groups[r.group] ||= []).push(r);
const list = $('roomList');
const order = ['Reception', 'Experience Center', 'Meeting Rooms', 'Executive Area', 'Workstations', 'Design Development', 'Support Rooms', 'Prayer Rooms', 'Washrooms'];
const names = { 'Experience Center': 'Experience centre', 'Meeting Rooms': 'Meeting', 'Executive Area': 'Executive', 'Workstations': 'Workspaces',
  'Design Development': 'Design & development', 'Support Rooms': 'Staff support & circulation', 'Prayer Rooms': 'Prayer' };
for (const gname of [...order, ...Object.keys(groups).filter((k) => !order.includes(k))]) {
  if (!groups[gname]) continue;
  const h = document.createElement('div'); h.className = 'grp'; h.textContent = names[gname] || gname; list.appendChild(h);
  for (const r of groups[gname]) {
    const b = document.createElement('button'); b.className = 'room'; b.dataset.id = r.id;
    b.innerHTML = `<span>${r.name}</span><small>${r.area_sft} sft</small>`;
    b.addEventListener('click', () => goRoom(r));
    list.appendChild(b);
  }
}
$('panelToggle').onclick = () => $('panel').classList.toggle('min');

// ------------------------------------------------------------------ helpers
const ease = (t) => t * t * (3 - 2 * t);
function fovFromLens(lens) {   // Blender lens on a 36 mm wide sensor -> vertical fov for this window
  const h = 2 * Math.atan(18 / lens);
  return THREE.MathUtils.radToDeg(2 * Math.atan(Math.tan(h / 2) / camera.aspect));
}
function setCeilings(on) {
  state.ceilings = on;
  for (const o of overhead) o.visible = on;
  $('btnCeil').classList.toggle('on', on);
}
function setLabels(on) {
  state.labels = on;
  for (const l of labels) l.visible = on && state.mode === 'overview';
  $('btnLabels').classList.toggle('on', on);
}
function fade(fn) {
  $('fade').style.opacity = 1;
  setTimeout(() => { fn(); setTimeout(() => { $('fade').style.opacity = 0; }, 80); }, 480);
}
function setMode(m) {
  state.mode = m;
  controls.enabled = m === 'overview';
  $('btnOverview').classList.toggle('on', m === 'overview');
  $('btnWalk').classList.toggle('on', m === 'walk');
  $('btnTour').classList.toggle('on', m === 'tour');
  $('btnPrev').disabled = $('btnNext').disabled = m !== 'tour';
  for (const l of labels) l.visible = state.labels && m === 'overview';
  if (m !== 'tour') { $('btnTour').innerHTML = '&#9654; Guided tour'; $('caption').classList.remove('show'); }
}
function showRoomInfo(text) {
  $('roomInfo').style.display = text ? 'block' : 'none';
  $('roomInfo').textContent = text || '';
  document.querySelectorAll('.room').forEach((b) => b.classList.toggle('active', text && b.textContent.startsWith(text.split(' · ')[0])));
}

// ------------------------------------------------------------------ overview
function overviewPose(az = -50, el = 40, dist = 78, target = C) {
  const a = THREE.MathUtils.degToRad(az), e = THREE.MathUtils.degToRad(el);
  // Blender azimuth (x east, y north) -> glTF (x east, z south)
  return { pos: new THREE.Vector3(target.x + dist * Math.cos(e) * Math.cos(a), target.y + dist * Math.sin(e), target.z - dist * Math.cos(e) * Math.sin(a)), target: target.clone() };
}
function goOverview(target = C, dist = 78) {
  stopTour();
  fade(() => {
    setMode('overview');
    setCeilings(false);
    camera.fov = 40; camera.updateProjectionMatrix();
    const p = overviewPose(-50, 40, dist, target);
    camera.position.copy(p.pos); controls.target.copy(p.target); controls.update();
    showRoomInfo('');
  });
}

// ------------------------------------------------------------------ walk mode (eye level)
const walk = { yaw: 0, pitch: 0, keys: {}, drag: null, glide: null, eye: data.eye_height };
function lookFrom(pos, target, lens) {
  camera.position.set(...pos);
  const d = new THREE.Vector3(...target).sub(camera.position);
  walk.yaw = Math.atan2(-d.x, -d.z);
  walk.pitch = Math.atan2(d.y, Math.hypot(d.x, d.z));
  walk.eye = pos[1];
  camera.fov = fovFromLens(lens || 20); camera.updateProjectionMatrix();
  applyLook();
}
function applyLook() { camera.rotation.set(walk.pitch, walk.yaw, 0, 'YXZ'); }
function startWalk(pos, target, lens, info) {
  stopTour();
  fade(() => { setMode('walk'); setCeilings(true); lookFrom(pos, target, lens); showRoomInfo(info || ''); });
}
function goRoom(r) {
  if (r.view && views[r.view]) {
    const v = views[r.view];
    startWalk(v.pos, v.target, v.lens, `${r.name} · ${r.area_sft} sft`);
  } else {
    goOverview(new THREE.Vector3(r.centre[0], 0, r.centre[2]), 22);
    setTimeout(() => showRoomInfo(`${r.name} · ${r.area_sft} sft`), 600);
  }
}
const ray = new THREE.Raycaster();
function blocked(from, dir, dist) {
  for (const h of [0.45, 1.25]) {
    ray.set(new THREE.Vector3(from.x, h, from.z), dir);
    ray.far = dist + 0.35;
    if (ray.intersectObjects(solid, false).length) return true;
  }
  return false;
}
function walkStep(dt) {
  if (walk.glide) {
    const g = walk.glide; g.t = Math.min(1, g.t + dt / g.dur);
    camera.position.lerpVectors(g.from, g.to, ease(g.t));
    if (g.t >= 1) walk.glide = null;
    return;
  }
  const k = walk.keys, f = (k.KeyW || k.ArrowUp ? 1 : 0) - (k.KeyS || k.ArrowDown ? 1 : 0);
  const s = (k.KeyD || k.ArrowRight ? 1 : 0) - (k.KeyA || k.ArrowLeft ? 1 : 0);
  if (!f && !s) return;
  const speed = (k.ShiftLeft || k.ShiftRight ? 3.2 : 1.5) * dt;
  const fwd = new THREE.Vector3(-Math.sin(walk.yaw), 0, -Math.cos(walk.yaw));
  const right = new THREE.Vector3(Math.cos(walk.yaw), 0, -Math.sin(walk.yaw));
  const mv = fwd.multiplyScalar(f).add(right.multiplyScalar(s)).normalize().multiplyScalar(speed);
  for (const axis of [mv, new THREE.Vector3(mv.x, 0, 0), new THREE.Vector3(0, 0, mv.z)]) {   // slide along walls
    const len = axis.length();
    if (len > 1e-6 && !blocked(camera.position, axis.clone().normalize(), len)) { camera.position.add(axis); break; }
  }
  camera.position.y = walk.eye;
}
const el = renderer.domElement;
el.addEventListener('pointerdown', (e) => { if (state.mode === 'walk') { walk.drag = { x: e.clientX, y: e.clientY }; el.setPointerCapture(e.pointerId); } });
el.addEventListener('pointermove', (e) => {
  if (state.mode !== 'walk' || !walk.drag) return;
  walk.yaw -= (e.clientX - walk.drag.x) * 0.0035;
  walk.pitch = THREE.MathUtils.clamp(walk.pitch - (e.clientY - walk.drag.y) * 0.0035, -1.2, 1.2);
  walk.drag = { x: e.clientX, y: e.clientY };
  applyLook();
});
el.addEventListener('pointerup', () => { walk.drag = null; });
el.addEventListener('dblclick', (e) => {
  if (state.mode !== 'walk') return;
  const m = new THREE.Vector2((e.clientX / innerWidth) * 2 - 1, -(e.clientY / innerHeight) * 2 + 1);
  ray.setFromCamera(m, camera); ray.far = 60;
  const hit = ray.intersectObjects(everything, false).find((h) => h.object.visible);
  if (!hit || !hit.face) return;
  const n = hit.face.normal.clone().transformDirection(hit.object.matrixWorld);
  if (n.y < 0.7 || hit.point.y > 0.3) return;                       // only floor points
  const to = new THREE.Vector3(hit.point.x, walk.eye, hit.point.z);
  const d = to.clone().sub(camera.position); d.y = 0;
  const dist = d.length();
  if (dist < 0.3 || blocked(camera.position, d.normalize(), Math.max(0, dist - 0.4))) return;
  walk.glide = { from: camera.position.clone(), to, t: 0, dur: Math.max(0.6, dist / 1.8) };
});
addEventListener('keydown', (e) => { walk.keys[e.code] = true; if (e.code === 'Space' && state.mode === 'tour') { e.preventDefault(); toggleTour(); } });
addEventListener('keyup', (e) => { walk.keys[e.code] = false; });

// ------------------------------------------------------------------ guided tour (same shots as the walkthrough video)
const SLOW = 1.6;            // the interactive tour runs a little slower than the video
function startTour(i = 0) {
  state.tour = { i, t: 0, playing: true };
  $('btnTour').innerHTML = '&#10073;&#10073; Pause';
  enterStep(i);
}
function stopTour() { state.tour = null; }
function toggleTour() {
  if (!state.tour) return startTour(0);
  state.tour.playing = !state.tour.playing;
  $('btnTour').innerHTML = state.tour.playing ? '&#10073;&#10073; Pause' : '&#9654; Resume';
}
function enterStep(i) {
  const st = data.tour[i];
  fade(() => {
    setMode('tour');
    $('btnTour').innerHTML = state.tour && state.tour.playing ? '&#10073;&#10073; Pause' : '&#9654; Resume';
    state.tour.i = i; state.tour.t = 0;
    setCeilings(st.kind !== 'overview');
    camera.fov = st.kind === 'overview' ? 40 : fovFromLens(st.lens);
    camera.updateProjectionMatrix();
    poseTour(st, 0);
    const cap = $('caption');
    cap.querySelector('.scene').textContent = `${String(i + 1).padStart(2, '0')} / ${data.tour.length} · ${st.scene}`;
    cap.querySelector('.label').textContent = st.label;
    cap.classList.add('show');
  });
}
function poseTour(st, u) {
  const e = ease(u);
  if (st.kind === 'overview') {
    const final = st.id.includes('final');
    const p = overviewPose(final ? -58 + 10 * e : -74 + 36 * e, final ? 50 - 10 * e : 41 - 2 * e, final ? 34 + 46 * e : 84 - 6 * e, C);
    camera.position.copy(p.pos); camera.lookAt(p.target);
  } else {
    const p = new THREE.Vector3().lerpVectors(new THREE.Vector3(...st.pos[0]), new THREE.Vector3(...st.pos[1]), e);
    const t = new THREE.Vector3().lerpVectors(new THREE.Vector3(...st.target[0]), new THREE.Vector3(...st.target[1]), e);
    t.y = p.y;                                                         // level camera: verticals stay vertical
    camera.position.copy(p); camera.lookAt(t);
  }
}
function tourStep(dt) {
  const T = state.tour; if (!T || state.mode !== 'tour') return;
  const st = data.tour[T.i];
  if (T.playing) T.t += dt;
  const dur = st.dur * SLOW;
  poseTour(st, Math.min(1, T.t / dur));
  if (T.t >= dur + 0.15 && T.playing) {
    T.t = -1e9;                                                        // wait for the fade
    if (T.i + 1 < data.tour.length) enterStep(T.i + 1);
    else { stopTour(); goOverview(); }
  }
}
$('btnTour').onclick = () => toggleTour();
$('btnNext').onclick = () => { if (state.tour) enterStep(Math.min(data.tour.length - 1, state.tour.i + 1)); };
$('btnPrev').onclick = () => { if (state.tour) enterStep(Math.max(0, state.tour.i - 1)); };
$('btnOverview').onclick = () => goOverview();
$('btnWalk').onclick = () => { const v = views.CAM_03_Entrance_Lobby; startWalk(v.pos, v.target, v.lens, 'Entrance Lobby'); };
$('btnCeil').onclick = () => setCeilings(!state.ceilings);
$('btnLabels').onclick = () => setLabels(!state.labels);

// ------------------------------------------------------------------ loop
addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight); labelRenderer.setSize(innerWidth, innerHeight);
});
const clock = new THREE.Clock();
renderer.setAnimationLoop(() => {
  const dt = Math.min(clock.getDelta(), 0.05);
  if (state.mode === 'overview') controls.update();
  else if (state.mode === 'walk') walkStep(dt);
  else if (state.mode === 'tour') tourStep(dt);
  renderer.render(scene, camera);
  labelRenderer.render(scene, camera);
});
setMode('overview');
setCeilings(false);
const p0 = overviewPose(-50, 40, 78);
camera.position.copy(p0.pos); controls.target.copy(C); controls.update();
$('loading').style.display = 'none';
state.ready = true;
state.counts = { meshes: everything.length, overhead: overhead.length, solid: solid.length, labels: labels.length };
