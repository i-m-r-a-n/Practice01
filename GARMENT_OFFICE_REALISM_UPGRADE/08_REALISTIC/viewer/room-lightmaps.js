// Phase 1: progressive Cycles diffuse atlases. Original scene remains the fallback.
// The bake contains irradiance only; the approved GLB remains the material authority.
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { EXRLoader } from 'three/addons/loaders/EXRLoader.js';
import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';

export async function readLightingManifest(url) {
  try {
    const r = await fetch(url, { cache: 'no-cache' });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const manifest = await r.json();
    if (!Array.isArray(manifest.rooms)) throw new Error('rooms must be an array');
    return { ...manifest, url: new URL(url, location.href).href };
  } catch (error) {
    return { rooms: [], url: new URL(url, location.href).href, error: String(error.message || error) };
  }
}

export class RoomLightmaps {
  constructor({ manifest, model, overhead, renderer, merge, changed, maxResident = 6, maxResidentBytes = 192 * 1024 * 1024 }) {
    Object.assign(this, { manifest, model, overhead, renderer, merge, changed, maxResident, maxResidentBytes });
    this.materials = new Map();
    this.rooms = new Map();
    this.clock = 0;
    this.active = null;
    this.status = { regularAtlasBudgetBytes: maxResidentBytes, phase: 1, manifest: manifest.url, available: manifest.rooms.length, loaded: [],
      requiredShared: manifest.rooms.filter(r => r.alwaysLoad).map(r => r.id), rooms: {}, error: manifest.error || null };
    model.traverse(o => {
      if (o.isMesh) for (const m of (Array.isArray(o.material) ? o.material : [o.material])) {
        if (m?.name && !this.materials.has(m.name)) this.materials.set(m.name, m);
      }
    });
    this.ktx = new KTX2Loader().setTranscoderPath('./textures/codecs/three_r169/examples/jsm/libs/basis/').detectSupport(renderer);
    this.partition();
  }

  partition() {
    const assigned = new Set();
    this.model.updateMatrixWorld(true);
    for (const spec of this.manifest.rooms) {
      const id = spec.id || spec.room;
      const record = { id, spec, state: 'available', fallback: [], originals: [], last: 0 };
      this.rooms.set(id, record);
      this.status.rooms[id] = { state: 'available', sourceObjects: spec.objects?.length || 0 };
      try {
        if (!id || !Array.isArray(spec.objects) || !spec.objects.length) throw new Error('missing room id or exact source object list');
        const nodes = [];
        for (const name of spec.objects) {
          const node = this.model.getObjectByName(name) || this.model.getObjectByName(THREE.PropertyBinding.sanitizeNodeName(name));
          if (!node || node === this.model || node === this.overhead) throw new Error(`source object missing: ${name}`);
          if (assigned.has(node)) throw new Error(`source object assigned twice: ${name}`);
          if (nodes.some(n => n === node)) throw new Error(`duplicate source object: ${name}`);
          nodes.push(node);
        }
        for (const node of nodes) {
          let p = node.parent;
          while (p && p !== this.model) {
            if (nodes.includes(p) || assigned.has(p)) throw new Error(`overlapping source objects: ${node.name}`);
            p = p.parent;
          }
        }
        for (const isOverhead of [false, true]) {
          const group = new THREE.Group();
          group.name = `FALLBACK_${id}_${isOverhead ? 'OVERHEAD' : 'INTERIOR'}`;
          group.userData.lightmapBoundary = true;
          (isOverhead ? this.overhead : this.model).add(group);
          record.fallback.push(group);
        }
        for (const node of nodes) {
          let top = node;
          while (top && top !== this.overhead) top = top.parent;
          record.fallback[top === this.overhead ? 1 : 0].attach(node);
          assigned.add(node);
        }
        record.originals = nodes;
      } catch (error) {
        record.state = 'error';
        this.status.rooms[id] = { state: 'error', error: error.message };
      }
    }
  }

  mergeFallbacks() {
    for (const room of this.rooms.values()) for (const group of room.fallback) this.merge(group);
  }

  async texture(spec) {
    const map = spec.lightMap;
    if (!map?.url) throw new Error('missing lightMap.url');
    const url = new URL(map.url, this.manifest.url).href;
    const ktx = (map.format || '').toLowerCase() === 'ktx2' || /\.ktx2(?:\?|$)/i.test(url);
    const tex = await (ktx ? this.ktx.loadAsync(url) : new EXRLoader().setDataType(THREE.HalfFloatType).loadAsync(url));
    tex.colorSpace = THREE.NoColorSpace;
    tex.channel = 1;
    tex.flipY = false;
    tex.minFilter = THREE.LinearFilter;
    tex.magFilter = THREE.LinearFilter;
    tex.generateMipmaps = false;
    // Actual r169 codec checker: EXRLoader reverses OpenEXR rows; the KTX converter
    // preserves the Blender/glTF atlas convention. Apply transform only to EXR.
    if (!ktx && map.flipY !== false) { tex.repeat.y = -1; tex.offset.y = 1; }
    tex.needsUpdate = true;
    return tex;
  }

  material(base, texture, intensity) {
    const material = base.clone();
    material.name = `${base.name}__cycles_uv1`;
    material.vertexColors = false;
    material.lightMap = texture;
    material.lightMapIntensity = intensity;
    material.userData.cyclesLightmap = true;
    material.userData.sourceMaterial = base.name;
    // Cycles already includes direct+indirect diffuse. Preserve real-time specular,
    // metal/glass reflection and emission without adding another hemisphere/sun diffuse.
    material.onBeforeCompile = shader => {
      shader.fragmentShader = shader.fragmentShader.replace('#include <lights_fragment_begin>',
        '#include <lights_fragment_begin>\nreflectedLight.directDiffuse = vec3(0.0);\n#ifdef RE_IndirectDiffuse\nirradiance = vec3(0.0);\n#endif');
      shader.fragmentShader = shader.fragmentShader.replace('#include <lights_fragment_maps>',
        THREE.ShaderChunk.lights_fragment_maps.replace('iblIrradiance += getIBLIrradiance( geometryNormal );', '/* Diffuse environment is in the Cycles atlas. */'));
    };
    material.customProgramCacheKey = () => 'cycles-diffuse-uv1-r169-v1';
    return material;
  }

  async load(id) {
    const room = this.rooms.get(id);
    if (!room || room.state === 'error') return null;
    room.last = ++this.clock;
    if (room.state === 'loaded') return room;
    if (room.promise) return room.promise;
    if (room.state === 'preview' && room.groups) return room; // full download failed; preserve the genuine HDR preview
    room.state = 'loading';
    this.status.rooms[id] = { ...this.status.rooms[id], state: 'loading' };
    this.changed();
    room.promise = (async () => {
      let texture, replacement;
      const ownedMaterials = new Set();
      const ownedGeometries = new Set(), placeholderMaterials = new Set();
      let groups = [];
      try {
        const preview = room.spec.lightMap.preview;
        const assets = await Promise.allSettled([
          new GLTFLoader().loadAsync(new URL(room.spec.glb, this.manifest.url).href),
          this.texture(preview ? { ...room.spec, lightMap: { ...room.spec.lightMap, ...preview } } : room.spec),
        ]);
        if (assets[0].status === 'fulfilled') replacement = assets[0].value;
        if (assets[1].status === 'fulfilled') texture = assets[1].value;
        replacement?.scene.traverse(o => { if (o.isMesh) { ownedGeometries.add(o.geometry); (Array.isArray(o.material) ? o.material : [o.material]).forEach(m => placeholderMaterials.add(m)); } });
        const failed = assets.find(r => r.status === 'rejected');
        if (failed) throw failed.reason;
        groups = [new THREE.Group(), new THREE.Group()];
        groups.forEach((g, i) => { g.name = `CYCLES_${id}_${i ? 'OVERHEAD' : 'INTERIOR'}`; g.userData.lightmapBoundary = true; });
        let meshes = 0, triangles = 0;
        const converted = new Map();
        replacement.scene.updateMatrixWorld(true);
        const targets = [];
        replacement.scene.traverse(o => { if (o.isMesh) targets.push(o); });
        if (!targets.length) throw new Error('room GLB has no meshes');
        for (const mesh of targets) {
          if (!mesh.geometry.attributes.uv1) throw new Error(`missing uv1: ${mesh.name}`);
          const materials = Array.isArray(mesh.material) ? mesh.material : [mesh.material];
          const next = materials.map(m => {
            const base = this.materials.get(m.name);
            if (!base) throw new Error(`material missing in approved base: ${m.name}`);
            if (!base.isMeshStandardMaterial) throw new Error(`non-PBR approved material: ${m.name}`);
            if (!converted.has(m.name)) {
              const intensity = Number(room.spec.lightMap.intensity ?? 1);
              const mat = this.material(base, texture, intensity);
              converted.set(m.name, mat); ownedMaterials.add(mat);
            }
            return converted.get(m.name);
          });
          mesh.material = Array.isArray(mesh.material) ? next : next[0];
          let n = mesh, isOverhead = false;
          while (n) { if (n.userData.overhead || /_OVERHEAD(?:_|$)/.test(n.name)) isOverhead = true; n = n.parent; }
          groups[isOverhead ? 1 : 0].attach(mesh);
          mesh.castShadow = false; mesh.receiveShadow = false;
          meshes++; triangles += (mesh.geometry.index?.count || mesh.geometry.attributes.position.count) / 3;
        }
        this.onStage?.('atlasDecoded', id);
        // The usable base scene and the irradiance atlas never wait for 2K hero maps.
        // Reference-camera capture may explicitly await this separate promise.
        room.heroPromise = this.prepareRoom ? Promise.resolve(this.prepareRoom({ id, groups, ownedMaterials })) : Promise.resolve();
        room.heroPromise = room.heroPromise.then(() => { this.onStage?.('heroMapsReady', id); this.changed(); }).catch(error => {
          room.heroError = error.message; this.status.rooms[id].heroError = error.message; this.changed();
        });
        this.model.add(groups[0]); this.overhead.add(groups[1]);
        placeholderMaterials.forEach(m => m.dispose()); placeholderMaterials.clear();
        for (const group of room.fallback) group.visible = false;
        Object.assign(room, { state: preview ? 'preview' : 'loaded', groups, texture, ownedMaterials });
        this.status.rooms[id] = { state: room.state, sourceObjects: room.spec.objects.length, meshes, triangles, intensity: room.spec.lightMap.intensity ?? 1, format: room.spec.lightMap.format || 'exr', resolution: preview?.size || room.spec.lightMap.size, heroError: room.heroError || null };
        this.onStage?.('atlasVisible', id);
        this.changed();
        if (preview) {
          try {
            const full = await this.texture(room.spec);
            ownedMaterials.forEach(material => { material.lightMap = full; material.needsUpdate = true; });
            texture.dispose(); texture = full; room.texture = full;
            room.state = 'loaded'; this.status.rooms[id].state = 'loaded'; this.status.rooms[id].resolution = room.spec.lightMap.size;
            this.onStage?.('atlasFullVisible', id);
          } catch (error) {
            this.status.rooms[id].fullResolutionError = error.message;
          }
        }
        this.trim();
        return room;
      } catch (error) {
        texture?.dispose(); ownedMaterials.forEach(m => m.dispose());
        groups.forEach(g => g.removeFromParent());
        ownedGeometries.forEach(g => g.dispose()); placeholderMaterials.forEach(m => m.dispose());
        room.fallback.forEach(g => { g.visible = true; });
        room.state = 'error';
        this.status.rooms[id] = { state: 'error', error: error.message };
        console.error(`Cycles atlas ${id}:`, error);
        return null;
      } finally {
        room.promise = null;
        this.status.loaded = [...this.rooms.values()].filter(r => r.state === 'loaded').map(r => r.id);
        this.changed();
      }
    })();
    return room.promise;
  }

  async loadGlobals() {
    return Promise.all(this.manifest.rooms.filter(r => r.alwaysLoad).map(r => this.load(r.id)));
  }

  async previewTexture(id, url, format) {
    const room = this.rooms.get(id);
    if (room?.state !== 'loaded') throw new Error('Load the review room first');
    const next = await this.texture({ ...room.spec, lightMap: { ...room.spec.lightMap, url, format } });
    room.ownedMaterials.forEach(material => { material.lightMap = next; material.needsUpdate = true; });
    room.texture.dispose(); room.texture = next;
    this.status.rooms[id].reviewOverride = { url, format };
    this.changed();
  }

  async request(id) {
    this.active = id;
    const [, room] = await Promise.all([this.loadGlobals(), this.load(id)]);
    return room;
  }

  estimatedBytes(room) { const size = room.texture?.image?.width || room.spec.lightMap?.size || 0; const height = room.texture?.image?.height || size; return size * height * 8; }

  setBudget(bytes) { this.maxResidentBytes = bytes; this.status.regularAtlasBudgetBytes = bytes; this.trim(); }

  trim() {
    const loaded = [...this.rooms.values()].filter(r => (r.state === 'loaded' || r.state === 'preview' && !r.promise) && !r.spec.alwaysLoad).sort((a, b) => a.last - b.last);
    let count = loaded.length, bytes = loaded.reduce((sum, room) => sum + this.estimatedBytes(room), 0);
    for (const room of loaded) {
      if (count <= this.maxResident && bytes <= this.maxResidentBytes) break;
      if (room.id === this.active) continue;
      for (const group of room.groups) { group.removeFromParent(); group.traverse(o => o.geometry?.dispose()); }
      room.ownedMaterials.forEach(m => { this.disposeMaterial?.(m); m.dispose(); }); bytes -= this.estimatedBytes(room); room.texture.dispose();
      room.fallback.forEach(g => { g.visible = true; });
      room.state = 'available'; this.status.rooms[room.id] = { state: 'available', evicted: true };
      count--;
    }
    this.status.residentRegularBytes = bytes;
    this.status.residentSharedBytes = [...this.rooms.values()].filter(r => r.spec.alwaysLoad && r.texture && ['loaded','preview'].includes(r.state)).reduce((sum, room) => sum + this.estimatedBytes(room), 0);
    this.status.activeExceedsBudget = bytes > this.maxResidentBytes;
  }
}
