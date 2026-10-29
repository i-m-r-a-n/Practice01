import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { buildOfficeProps } from '../props/office-props.mjs';
import { applyOfficeScreenContent } from '../props/screen-content.mjs';
import { createPeopleLayer } from '../people/people-layer.js';
import { buildIdentityProps } from '../props/identity-props.mjs';

// Phase 4 is deliberately dormant in stages 1–3. Source objects remain untouched;
// additive props, screen artwork and fictional actors have separate provenance.
export async function createOfficeDressing({ scene, renderer, metadata, grid, probes, staticBlocked, changed, peopleAccepted = false, activeZones = null, frozenPeople = false, peopleManifest = null, excludedProps = [] }) {
  const base = new URL('./', location.href);
  const response = await fetch(new URL('props/office-props-manifest.json', base));
  if (!response.ok) throw new Error(`Props manifest HTTP ${response.status}`);
  const manifest = await response.json();
  if (activeZones) manifest.props = manifest.props.filter(p => activeZones.includes(p.zone));
  if (excludedProps.length) manifest.props = manifest.props.filter(p => !excludedProps.includes(p.id));
  const props = buildOfficeProps(THREE, manifest, { anisotropy: Math.min(8, renderer.capabilities.getMaxAnisotropy()) });
  scene.add(props.group);
  props.group.traverse(mesh => { if (mesh.isMesh) { mesh.castShadow = false; mesh.receiveShadow = false; } });
  // Client-identity items (water point, material stories, development samples): on furniture tops or walls only.
  const identity = buildIdentityProps(THREE, { zones: activeZones, anisotropy: Math.min(8, renderer.capabilities.getMaxAnisotropy()) });
  scene.add(identity.group);
  let atlas, people = null, peoplePromise = null;
  const status = { enabled: true, props: props.stats, identity: { ...identity.stats, items: identity.items }, screens: {}, peopleAccepted, errors: [], dynamicLighting: probes ? 'Room SH for actors; instance SH for additive props; static lightmaps exclude both.' : 'Existing scene hemisphere/directional lighting for added props and static people; not a calibrated dynamic-lighting bake.' };
  const zones = metadata.rooms.map(r => r.zone), rows = new Float32Array(9 * zones.length * 4);
  const shTexture = new THREE.DataTexture(rows, 9, zones.length, THREE.RGBAFormat, THREE.FloatType);
  shTexture.minFilter = shTexture.magFilter = THREE.NearestFilter; shTexture.generateMipmaps = false;
  // Until a real room probe is loaded, retain a declared neutral preview irradiance.
  for (let z = 0; z < zones.length; z++) for (let c = 0; c < 3; c++) rows[(z * 9) * 4 + c] = .55 / .886227;
  shTexture.needsUpdate = true;
  const materialHooks = new WeakSet(), batches = [];
  const frustum = new THREE.Frustum(), projection = new THREE.Matrix4(), matrix = new THREE.Matrix4();
  props.group.traverse(mesh => {
    if (!mesh.isInstancedMesh) return;
    // Geometry is reused across batches: clone only the attribute container so each
    // batch can carry its own room IDs without overwriting another batch's IDs.
    mesh.geometry = mesh.geometry.clone();
    mesh.geometry.setAttribute('officeProbeRow', new THREE.InstancedBufferAttribute(Float32Array.from(mesh.userData.propZones, id => Math.max(0, zones.indexOf(id))), 1));
    mesh.geometry.computeBoundingSphere();
    const spheres = []; for (let i = 0; i < mesh.count; i++) { mesh.getMatrixAt(i, matrix); spheres.push(mesh.geometry.boundingSphere.clone().applyMatrix4(matrix)); }
    batches.push({ mesh, matrices: mesh.instanceMatrix.array.slice(), rows: mesh.geometry.attributes.officeProbeRow.array.slice(), spheres, count: mesh.count });
    const material = mesh.material;
    if (!probes) return;
    if (materialHooks.has(material)) return; materialHooks.add(material);
    const oldCompile = material.onBeforeCompile, oldKey = material.customProgramCacheKey.bind(material);
    material.onBeforeCompile = shader => {
      oldCompile.call(material, shader);
      shader.uniforms.officePropSH = { value: shTexture };
      shader.uniforms.officePropRows = { value: zones.length };
      shader.vertexShader = `uniform sampler2D officePropSH; uniform float officePropRows; attribute float officeProbeRow; varying vec3 officePropIrradiance;
vec3 officeCoefficient(float n){return texture2D(officePropSH,vec2((n+.5)/9.,(officeProbeRow+.5)/officePropRows)).rgb;}
vec3 officeSH(vec3 n){
  vec3 r=officeCoefficient(0.)*.886227;
  r+=officeCoefficient(1.)*(2.*.511664*n.y)+officeCoefficient(2.)*(2.*.511664*n.z)+officeCoefficient(3.)*(2.*.511664*n.x);
  r+=officeCoefficient(4.)*(2.*.429043*n.x*n.y)+officeCoefficient(5.)*(2.*.429043*n.y*n.z);
  r+=officeCoefficient(6.)*(.743125*n.z*n.z-.247708)+officeCoefficient(7.)*(2.*.429043*n.x*n.z)+officeCoefficient(8.)*(.429043*(n.x*n.x-n.y*n.y));
  return max(r,vec3(0.));}
` + shader.vertexShader;
      shader.vertexShader = shader.vertexShader.replace('#include <defaultnormal_vertex>', '#include <defaultnormal_vertex>\nofficePropIrradiance=officeSH(inverseTransformDirection(normalize(transformedNormal),viewMatrix));');
      shader.fragmentShader = 'varying vec3 officePropIrradiance;\n' + shader.fragmentShader;
      shader.fragmentShader = shader.fragmentShader.replace('#include <lights_fragment_begin>', '#include <lights_fragment_begin>\nreflectedLight.directDiffuse=vec3(0.0);\n#ifdef RE_IndirectDiffuse\nirradiance=officePropIrradiance;\n#endif');
      shader.fragmentShader = shader.fragmentShader.replace('#include <lights_fragment_maps>', THREE.ShaderChunk.lights_fragment_maps.replace('iblIrradiance += getIBLIrradiance( geometryNormal );', '/* Additive prop room SH supplies diffuse. */'));
    };
    material.customProgramCacheKey = () => oldKey() + '|office-instanced-room-sh-v1'; material.needsUpdate = true;
  });
  function prepareSourceScreen(root, zone) {
    const review = applyOfficeScreenContent(THREE, root, { zone, atlasTexture: atlas, anisotropy: Math.min(8, renderer.capabilities.getMaxAnisotropy()), emissiveIntensity: .25 });
    atlas ||= review.texture;
    status.screens[zone] = { touched: review.touched, skipped: review.skipped };
  }
  function prepareRoom(room) {
    const previousGeometry = new Set(), previousMaterials = new Set(room.ownedMaterials);
    room.groups.forEach(root => root.traverse(o => { if (o.isMesh) previousGeometry.add(o.geometry); }));
    const reviews = [];
    for (const root of room.groups) { const review = applyOfficeScreenContent(THREE, root, { zone: room.id, atlasTexture: atlas, anisotropy: Math.min(8, renderer.capabilities.getMaxAnisotropy()), emissiveIntensity: .25 }); atlas ||= review.texture; reviews.push(review); }
    // The helper may clone a screen material. Keep atlas refinement, probes and LRU
    // ownership bound to the actual materials now used by the mesh.
    room.ownedMaterials.clear(); const liveGeometry = new Set();
    room.groups.forEach(root => root.traverse(o => { if (o.isMesh) { liveGeometry.add(o.geometry); (Array.isArray(o.material) ? o.material : [o.material]).forEach(m => room.ownedMaterials.add(m)); } }));
    previousMaterials.forEach(m => { if (!room.ownedMaterials.has(m)) m.dispose(); });
    previousGeometry.forEach(g => { if (!liveGeometry.has(g)) g.dispose(); });
    status.screens[room.id] = { touched: reviews.flatMap(r => r.touched), skipped: reviews.flatMap(r => r.skipped) };
  }
  function applyProbe(id) {
    const coefficients = probes?.coefficients(id), row = zones.indexOf(id);
    if (coefficients && row >= 0) { for (let i = 0; i < 9; i++) coefficients[i].toArray(rows, (row * 9 + i) * 4); shTexture.needsUpdate = true; }
    if (people) for (const actor of people.group.children) {
      const definition = people.manifest.actors.find(a => a.id + '_placement' === actor.name);
      if (definition?.zone !== id) continue;
      actor.traverse(mesh => { if (mesh.isMesh) for (const material of (Array.isArray(mesh.material) ? mesh.material : [mesh.material])) probes?.applyDynamic(material, id); });
    }
  }
  function prepareView(camera) {
    if (camera) { camera.updateMatrixWorld(true); frustum.setFromProjectionMatrix(projection.multiplyMatrices(camera.projectionMatrix, camera.matrixWorldInverse)); }
    let visible = 0, calls = 0;
    for (const batch of batches) {
      const { mesh, matrices, rows, spheres, count } = batch; let cursor = 0;
      for (let i = 0; i < count; i++) if (!camera || frustum.intersectsSphere(spheres[i])) { mesh.instanceMatrix.array.set(matrices.subarray(i * 16, i * 16 + 16), cursor * 16); mesh.geometry.attributes.officeProbeRow.array[cursor] = rows[i]; cursor++; }
      mesh.count = cursor; mesh.visible = cursor > 0; mesh.instanceMatrix.needsUpdate = true; mesh.geometry.attributes.officeProbeRow.needsUpdate = true; visible += cursor; if (cursor) calls++;
    }
    status.visiblePropInstances = visible; status.visiblePropBatches = calls;
  }
  // Independent contact review reads the actual generated geometry and original
  // instance matrices, including instances currently culled from the view.
  function propDiagnostics(zone) {
    props.group.updateMatrixWorld(true);
    const meshes = [], world = new THREE.Matrix4(), vertex = new THREE.Vector3();
    for (const batch of batches) {
      const { mesh, matrices, count } = batch, positions = mesh.geometry.attributes.position;
      for (let i = 0; i < count; i++) {
        if (zone && mesh.userData.propZones[i] !== zone) continue;
        world.fromArray(matrices, i * 16).premultiply(mesh.matrixWorld);
        const vertices = Array.from({ length: positions.count }, (_, n) => vertex.fromBufferAttribute(positions, n).applyMatrix4(world).toArray());
        const indices = mesh.geometry.index ? Array.from(mesh.geometry.index.array) : Array.from({ length: positions.count }, (_, n) => n);
        meshes.push({ name: `${mesh.name}_${i}`, zone: mesh.userData.propZones[i], materials: [mesh.material.name], vertices, indices });
      }
    }
    return { props: manifest.props.filter(p => !zone || p.zone === zone), bounds: props.propBounds, meshes };
  }
  async function ensurePeople() {
    if (!peopleAccepted) throw new Error('People assets await the independent contact review; the layer is not enabled.');
    if (!peoplePromise) peoplePromise = (async () => {
      people = await createPeopleLayer({ THREE, loader: new GLTFLoader(), scene, metadata, walkGrid: grid, assetBase: './people/', extraBlocked: staticBlocked, frozen: frozenPeople, activeZones, manifestFile: peopleManifest || (frozenPeople ? 'reception/people-manifest.json' : 'people-manifest.json') });
      return people;
    })();
    return peoplePromise;
  }
  async function setPeopleEnabled(enabled, playerPosition) {
    if (!enabled && !people) return { enabled: false, loaded: false, total: 0, visible: 0, illustrative: true, accepted: peopleAccepted };
    const layer = await ensurePeople(); await layer.setEnabled(enabled, playerPosition);
    if (enabled) zones.forEach(applyProbe);
    changed(); return layer.stats();
  }
  function update(dt, options) { if (people?.stats().enabled) { people.update(frozenPeople ? 0 : dt, options); if (!frozenPeople) changed(); } }
  return { status, props, prepareRoom, prepareSourceScreen, applyProbe, prepareView, propDiagnostics, textures: () => [shTexture, atlas, ...identity.textures()].filter(Boolean), setPeopleEnabled, update,
    peopleStats: () => people?.stats() || { enabled: false, loaded: false, total: 0, visible: 0, illustrative: true, accepted: peopleAccepted },
    peopleDiagnostics: () => people?.diagnostics() || [], peopleContacts: stride => people?.contactDiagnostics(stride) || [], blocksMovement: (x, z, radius) => people?.blocksMovement(x, z, radius) || false,
    hiddenDuringProbe: () => people ? [people.group] : [],
    dispose() { people?.dispose(); props.group.traverse(o => o.geometry?.dispose()); props.dispose(); identity.dispose(); atlas?.dispose(); shTexture.dispose(); },
  };
}
