import * as THREE from 'three';
import { LightProbeGenerator } from 'three/addons/lights/LightProbeGenerator.js';

// Phase 3: one-time linear HDR room captures with box-projected reflection lookup.
// Not SSR: reflected dynamic subjects do not update continuously.
export function createRoomProbes({ scene, renderer, metadata, lightmaps, overhead, hidden, changed, dynamicLighting = false }) {
  const cache = new Map(), pmrem = new THREE.PMREMGenerator(renderer);
  const originalHooks = new WeakMap();
  const dynamicHooks = new WeakMap();
  const pending = new Map(); let captureTail = Promise.resolve();
  const status = { rooms: {}, errors: [], captureResolution: 256, maxResident: 4, dynamicRoomIrradiance: dynamicLighting };
  function apply(material, texture, min, max, centre) {
    if (!originalHooks.has(material)) originalHooks.set(material, { compile: material.onBeforeCompile, key: material.customProgramCacheKey.bind(material) });
    const { compile: oldCompile, key: oldKey } = originalHooks.get(material);
    material.envMap = texture; material.envMapIntensity = 1;
    material.onBeforeCompile = shader => {
      oldCompile.call(material, shader);
      Object.assign(shader.uniforms, { roomProbeMin: { value: min }, roomProbeMax: { value: max }, roomProbeCentre: { value: centre } });
      const projection = `
uniform vec3 roomProbeMin;
uniform vec3 roomProbeMax;
uniform vec3 roomProbeCentre;
vec3 roomBoxProjection(vec3 direction) {
  vec3 position= cameraPosition-inverseTransformDirection(vViewPosition,viewMatrix)*length(vViewPosition);
  vec3 safeDirection=mix(vec3(-1.0),vec3(1.0),step(vec3(0.0),direction))*max(abs(direction),vec3(0.00001));
  vec3 t1=(roomProbeMax-position)/safeDirection;
  vec3 t2=(roomProbeMin-position)/safeDirection;
  vec3 furthest=max(t1,t2);
  float distanceToBox=min(furthest.x,min(furthest.y,furthest.z));
  return position+direction*max(distanceToBox,0.0)-roomProbeCentre;
}
`;
      const chunk = THREE.ShaderChunk.envmap_physical_pars_fragment.replace(
        'vec4 envMapColor = textureCubeUV( envMap, envMapRotation * reflectVec, roughness );',
        'reflectVec = roomBoxProjection(reflectVec);\nvec4 envMapColor = textureCubeUV( envMap, envMapRotation * reflectVec, roughness );');
      shader.fragmentShader = shader.fragmentShader.replace('#include <envmap_physical_pars_fragment>', projection + chunk);
    };
    material.customProgramCacheKey = () => oldKey() + '|room-box-projection-v1';
    material.needsUpdate = true;
  }
  function ensure(id) {
    if (pending.has(id)) return pending.get(id);
    const task = captureTail.then(() => ensureNow(id));
    pending.set(id, task); captureTail = task.catch(() => null);
    return task.finally(() => { pending.delete(id); });
  }
  async function ensureNow(id) {
    const room = metadata.rooms.find(r => r.zone === id), baked = lightmaps.rooms.get(id);
    if (!room || baked?.state !== 'loaded') return null;
    if (cache.has(id)) {
      const hit = cache.get(id); cache.delete(id); cache.set(id, hit);
      if (![...baked.ownedMaterials].every(m => hit.materials.includes(m))) {
        hit.materials = [...baked.ownedMaterials];
        hit.materials.forEach(m => apply(m, hit.filtered.texture, hit.min, hit.max, hit.centreVector));
      }
      return hit;
    }
    const xs = room.polygon_xz.map(p => p[0]), zs = room.polygon_xz.map(p => p[1]);
    const min = new THREE.Vector3(Math.min(...xs), 0, Math.min(...zs));
    const max = new THREE.Vector3(Math.max(...xs), 2.8956, Math.max(...zs));
    const centre = new THREE.Vector3(room.centroid_xz[0], 1.2, room.centroid_xz[1]);
    const cube = new THREE.WebGLCubeRenderTarget(256, { type: THREE.HalfFloatType, generateMipmaps: false });
    const camera = new THREE.CubeCamera(.05, 150, cube); camera.position.copy(centre);
    const wasCeiling = overhead.visible, hide = hidden?.() || [], visible = hide.map(o => o.visible);
    const oldTone = renderer.toneMapping, oldReset = renderer.info.autoReset;
    try {
      status.capturing = id;
      overhead.visible = true; hide.forEach(o => { o.visible = false; });
      renderer.toneMapping = THREE.NoToneMapping; renderer.info.autoReset = false; renderer.info.reset();
      camera.update(renderer, scene);
      const irradianceProbe = dynamicLighting ? await LightProbeGenerator.fromCubeRenderTarget(renderer, cube) : null;
      const filtered = pmrem.fromCubemap(cube.texture);
      const captureCalls = renderer.info.render.calls, captureTriangles = renderer.info.render.triangles;
      const materials = [...baked.ownedMaterials];
      materials.forEach(m => apply(m, filtered.texture, min, max, centre));
      const result = { filtered, materials, centre: centre.toArray(), centreVector: centre, min, max, irradianceProbe };
      cache.set(id, result);
      status.rooms[id] = { state: 'loaded', position: result.centre, box: [min.toArray(), max.toArray()], captureCalls, captureTriangles };
      while (cache.size > status.maxResident) {
        const key = cache.keys().next().value, old = cache.get(key); cache.delete(key);
        old.materials.forEach(m => { m.envMap = null; m.needsUpdate = true; }); old.filtered.dispose();
        status.rooms[key].state = 'evicted';
      }
      changed(); return result;
    } catch (error) { status.errors.push(`${id}: ${error.message}`); return null; }
    finally {
      status.capturing = null;
      cube.dispose(); renderer.toneMapping = oldTone; renderer.info.autoReset = oldReset;
      overhead.visible = wasCeiling; hide.forEach((o, i) => { o.visible = visible[i]; });
    }
  }
  function applyDynamic(material, id) {
    const room = cache.get(id);
    if (!room?.irradianceProbe || !material.isMeshStandardMaterial || material.userData.cyclesLightmap) return false;
    let state = dynamicHooks.get(material);
    if (!state) {
      const baseCompile = material.onBeforeCompile, baseKey = material.customProgramCacheKey.bind(material);
      state = { coefficients: { value: room.irradianceProbe.sh.coefficients }, room: id };
      dynamicHooks.set(material, state);
      material.onBeforeCompile = shader => {
        baseCompile.call(material, shader);
        shader.uniforms.dynamicRoomSH = state.coefficients;
        shader.fragmentShader = 'uniform vec3 dynamicRoomSH[9];\n' + shader.fragmentShader;
        shader.fragmentShader = shader.fragmentShader.replace('#include <lights_fragment_begin>',
          '#include <lights_fragment_begin>\nreflectedLight.directDiffuse=vec3(0.0);\n#ifdef RE_IndirectDiffuse\nirradiance=max(getLightProbeIrradiance(dynamicRoomSH,geometryNormal),vec3(0.0));\n#endif');
        shader.fragmentShader = shader.fragmentShader.replace('#include <lights_fragment_maps>',
          THREE.ShaderChunk.lights_fragment_maps.replace('iblIrradiance += getIBLIrradiance( geometryNormal );', '/* Room SH already supplies diffuse environment. */'));
      };
      material.customProgramCacheKey = () => baseKey() + '|dynamic-room-sh-v1';
    }
    state.coefficients.value = room.irradianceProbe.sh.coefficients; state.room = id;
    apply(material, room.filtered.texture, room.min, room.max, room.centreVector);
    if (!room.materials.includes(material)) room.materials.push(material);
    material.userData.dynamicProbeRoom = id;
    return true;
  }
  return { ensure, applyDynamic, targets: () => [...cache.values()].map(r => r.filtered), coefficients: id => cache.get(id)?.irradianceProbe?.sh.coefficients || null, status, dispose() { cache.forEach(r => r.filtered.dispose()); pmrem.dispose(); } };
}
