import * as THREE from 'three';

// Release-mode finish refinement on the vertex-lit base model. The shared terrazzo floor (lobby, reception, visitor
// passage, experience centre, corridors) takes the approved CC0 Terrazzo019M basecolour at its native 2K, with the
// approved colour correction and 0.8 m joints of phase-materials.js (scripts/lib_materials.py), as in the Cycles
// renders. Only the albedo changes: the baked Cycles light (vertex colours) and the UV transform stay as they are.
export async function refineReleaseFinishes({ root, ktx, anisotropy = 8, changed, url = './textures/pbr2k/ktx2/Terrazzo019M/basecolor.ktx2' }) {
  const targets = new Set();
  root.traverse(o => { if (o.isMesh) for (const m of [o.material].flat()) if (m.name === 'fl_terrazzo_baked' && m.map) targets.add(m); });
  if (!targets.size) return { refined: [] };
  const source = await ktx.loadAsync(new URL(url, location.href).href);
  for (const material of targets) {
    const t = source.clone(), o = material.map;
    t.offset.copy(o.offset); t.repeat.copy(o.repeat); t.center.copy(o.center); t.rotation = o.rotation;
    t.wrapS = o.wrapS; t.wrapT = o.wrapT; t.channel = o.channel;
    t.flipY = false; t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = anisotropy; t.needsUpdate = true;
    material.map = t;
    material.onBeforeCompile = shader => {
      shader.fragmentShader = shader.fragmentShader.replace('#include <map_fragment>', THREE.ShaderChunk.map_fragment.replace('diffuseColor *= sampledDiffuseColor;',
        'float nativeMax = max(sampledDiffuseColor.r, max(sampledDiffuseColor.g, sampledDiffuseColor.b));\n' +
        'sampledDiffuseColor.rgb = (vec3(nativeMax) + (sampledDiffuseColor.rgb - vec3(nativeMax)) * .75) * 1.12;\n' +
        'vec2 tileUV = vec2(vMapUv.x, 1.0 - vMapUv.y) * .65; vec2 edge = min(fract(tileUV / .8), 1.0 - fract(tileUV / .8)) * .8;\n' +
        'float joint = 1.0 - smoothstep(.002, .006, min(edge.x, edge.y)); sampledDiffuseColor.rgb *= mix(1.0, .72, joint);\n' +
        'diffuseColor *= sampledDiffuseColor;'));
    };
    material.customProgramCacheKey = () => 'release-terrazzo-v1';
    material.needsUpdate = true;
  }
  changed?.();
  return { refined: [...targets].map(m => m.name), source: url };
}
