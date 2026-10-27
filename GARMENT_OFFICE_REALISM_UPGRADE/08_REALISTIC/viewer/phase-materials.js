import * as THREE from 'three';

// Numerical source: approved scripts/lib_materials.py. Native 2K maps, no upscaling.
const recipes = {
  oak: ['white_oak_veneer', .85, 1.12], oak_slat: ['white_oak_veneer', .9, 1.05],
  walnut: ['natural_walnut_veneer', 1, .95, null, ['#6B4A33', .85]],
  fl_terrazzo: ['Terrazzo019M', .75, 1.12], terrazzo_counter: ['Terrazzo019M', .75, 1.15],
  fab_charcoal: ['Fabric030', .5, .75], fab_green: ['Fabric030', 1, 1, ['#2E5A40', '#4E7D60']],
  fab_sand: ['Fabric030', 1, 1, ['#B9A98E', '#DCCFB8']], fab_grey: ['Fabric030', 1, 1, ['#5E5F60', '#8B8C8D']],
  rug_wool: ['Fabric030', 1, 1, ['#8E877B', '#CBC4B7']], felt_green: ['Fabric034', 1, 1, ['#2C5A3F', '#477A5B']],
  felt_grey: ['Fabric034', .5, .95], fl_carpet: ['Fabric030', 1, 1, ['#2B2D2F', '#4A4D50']],
  fl_carpet_green: ['Fabric030', 1, 1, ['#2A5539', '#3F6E50']],
  fl_herringbone: ['herringbone_parquet', .78, 1.08], fl_oak_planks: ['laminate_floor_02', .75, 1.08],
  fl_concrete: ['smooth_concrete_floor', 1, 1, ['#A9A6A0', '#CFCCC6']],
  fl_porcelain: ['Tiles040', .5, 1], wall_porcelain: ['Tiles040', .5, 1.02], stone_white: ['Tiles043', .6, 1],
  leather_cognac: ['leather_white', 1, 1, null, ['#8A5A36', 1]], leather_black: ['leather_white', 1, 1, null, ['#202020', 1]],
};
const vector = hex => { const c = new THREE.Color(hex); return `vec3(${c.r.toFixed(8)},${c.g.toFixed(8)},${c.b.toFixed(8)})`; };

export function createMaterialUpgrade({ renderer, loader, indexUrl = './textures/pbr2k/index.json', changed }) {
  const status = { loaded: [], missing: [], errors: [], nativeResolution: 2048 };
  const ownedByMaterial = new WeakMap();
  const applied = new WeakSet(), cache = new Map(), textures = new Set();
  const indexPromise = fetch(indexUrl).then(r => { if (!r.ok) throw new Error(`PBR index HTTP ${r.status}`); return r.json(); });
  const root = new URL(indexUrl, location.href);
  async function load(spec) {
    const url = new URL(spec.file, root).href;
    if (!cache.has(url)) cache.set(url, loader.loadAsync(url));
    return cache.get(url);
  }
  function transformed(source, original, kind) {
    const t = source.clone();
    if (original) {
      t.offset.copy(original.offset); t.repeat.copy(original.repeat); t.center.copy(original.center); t.rotation = original.rotation;
      t.wrapS = original.wrapS; t.wrapT = original.wrapT; t.channel = original.channel;
    } else { t.wrapS = t.wrapT = THREE.RepeatWrapping; }
    t.flipY = false; t.colorSpace = kind === 'basecolor' ? THREE.SRGBColorSpace : THREE.NoColorSpace;
    t.anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy());
    t.needsUpdate = true; textures.add(t); return t;
  }
  async function apply(material) {
    if (!material.isMeshStandardMaterial || applied.has(material)) return;
    applied.add(material);
    const name = material.userData.sourceMaterial || material.name;
    const recipe = recipes[name];
    const metal = ['brass', 'chrome', 'alu_silver', 'alu_black'].includes(name);
    if (!recipe && !metal) return;
    try {
      const index = await indexPromise, set = index[recipe?.[0] || 'selfmade_brushed_metal'];
      if (!set) { if (!status.missing.includes(name)) status.missing.push(name); return; }
      const loaded = await Promise.all(Object.entries(set).map(async ([key, spec]) => [key, await load(spec)]));
      const maps = Object.fromEntries(loaded);
      const hadNormalMap = !!material.normalMap;
      if (maps.normal) material.normalMap = transformed(maps.normal, material.normalMap || material.map, 'normal');
      if (metal && !hadNormalMap) material.normalScale.set(.15, .15);
      // Approved constant-roughness fabrics remain constant; image-based roughness
      // keeps the existing source multiplier and the original KHR texture transform.
      if (maps.roughness && (material.roughnessMap || metal)) material.roughnessMap = transformed(maps.roughness, material.roughnessMap || material.map, 'roughness');
      if (recipe && maps.basecolor && !['fl_carpet', 'fl_carpet_green'].includes(name)) {
        material.map = transformed(maps.basecolor, material.map, 'basecolor');
        const [, saturation, value, ramp, tint] = recipe;
        const previous = material.onBeforeCompile;
        material.onBeforeCompile = shader => {
          previous.call(material, shader);
          let correction = `float nativeMax = max(sampledDiffuseColor.r,max(sampledDiffuseColor.g,sampledDiffuseColor.b));\nsampledDiffuseColor.rgb = (vec3(nativeMax)+(sampledDiffuseColor.rgb-vec3(nativeMax))*${saturation.toFixed(4)})*${value.toFixed(4)};\n`;
          if (ramp) correction += `sampledDiffuseColor.rgb=mix(${vector(ramp[0])},${vector(ramp[1])},clamp(dot(sampledDiffuseColor.rgb,vec3(.2126,.7152,.0722)),0.0,1.0));\n`;
          if (tint) correction += `sampledDiffuseColor.rgb*=mix(vec3(1.0),${vector(tint[0])},${tint[1].toFixed(4)});\n`;
          if (name === 'fl_terrazzo') correction += 'vec2 tileUV=vec2(vMapUv.x,1.0-vMapUv.y)*.65; vec2 edge=min(fract(tileUV/.8),1.0-fract(tileUV/.8))*.8; float joint=1.0-smoothstep(.002,.006,min(edge.x,edge.y)); sampledDiffuseColor.rgb*=mix(1.0,.72,joint);\n';
          shader.fragmentShader = shader.fragmentShader.replace('#include <map_fragment>', THREE.ShaderChunk.map_fragment.replace('diffuseColor *= sampledDiffuseColor;', correction + 'diffuseColor *= sampledDiffuseColor;'));
        };
        const oldKey = material.customProgramCacheKey.bind(material);
        material.customProgramCacheKey = () => oldKey() + `|native-pbr-${name}`;
      }
      ownedByMaterial.set(material, [material.map, material.normalMap, material.roughnessMap].filter(t => t && textures.has(t)));
      material.userData.nativePBR = true; material.needsUpdate = true;
      if (!status.loaded.includes(name)) status.loaded.push(name);
      changed();
    } catch (error) { status.errors.push(`${name}: ${error.message}`); changed(); }
  }
  return { apply, status, textures: () => [...textures], release(material) { for (const texture of ownedByMaterial.get(material) || []) { texture.dispose(); textures.delete(texture); } ownedByMaterial.delete(material); }, dispose() { textures.forEach(t => t.dispose()); } };
}
