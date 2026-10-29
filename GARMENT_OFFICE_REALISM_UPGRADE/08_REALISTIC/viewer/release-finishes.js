import * as THREE from 'three';
import { knitTile } from '../props/knit-tiles.mjs';

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

// ------------------------------------------------------------------------------------------------ knitwear and cloth
// The client knits garments: shared garment materials (g_*) get a world-space knit structure, but only inside the
// display boxes below, so a fire extinguisher that shares g_rust is left alone. The four dress forms on the
// Experience Centre plinth each get a chunky stitch (cable, rib, moss, waffle); the bay back panels become a green
// handloom weave. Self-made canvas tiles; only the albedo is modulated, the baked light stays as it is.
const KNIT_BOXES = [            // [x0, y0, z0, x1, y1, z1] in viewer metres
  [9.75, 0, -10.78, 20.57, 2.44, -10.10],     // Experience Centre (Z30): the four display bays (hanging and folded garments)
  [16.50, .86, -9.02, 20.20, 1.10, -8.00],    //   folded garments on the material table
  [15.95, 0, -20.80, 19.50, 1.70, -20.10],    // Merchandising (Z07): rolling sample rails
  [17.15, .74, -17.75, 18.40, 1.10, -15.27],  //   inspection island
  [9.65, .74, -19.10, 15.20, .90, -17.68],    //   samples on the desk benches
  [9.65, .74, -16.17, 15.20, .90, -14.76],
  [17.40, .74, -14.15, 18.08, 1.00, -12.27],  //   buyer review table
  [9.65, 0, -21.30, 15.20, .72, -20.92],      //   swatch shelves
  [9.64, 1.16, -10.92, 17.54, 2.19, -10.86],  //   approval board and pin-up board
  [29.38, .45, -30.49, 29.44, 2.30, -23.10],  // Global Design Studio (Z18): mood-board swatches
  [33.03, 0, -17.28, 33.72, 2.44, -14.21],    //   collection display bay
];
const FORMS = [11.40, .20, -8.78, 14.00, 1.87, -8.34];   // dress forms F022-F025, 0.71 m apart along x
export function refineKnitwear({ root, THREE: T = THREE, anisotropy = 8, changed }) {
  const tex = name => { const t = new T.CanvasTexture(knitTile(name)); t.wrapS = t.wrapT = T.RepeatWrapping; t.colorSpace = T.NoColorSpace; t.anisotropy = anisotropy; t.needsUpdate = true; return t; };
  const maps = Object.fromEntries(['jersey', 'rib', 'moss', 'waffle', 'cable', 'weave'].map(k => [k, tex(k)]));
  const boxes = KNIT_BOXES.map(b => new T.Vector4(...b.slice(0, 3), 0)).concat(KNIT_BOXES.map(b => new T.Vector4(...b.slice(3), 0)));
  const touched = [];
  root.traverse(o => {
    if (!o.isMesh) return;
    for (const m of [o.material].flat()) {
      if (m.userData.knitwear || !/^(g_[a-z]+|paint_green)(_baked)?$/.test(m.name)) continue;   // furniture has no vertex light: plain PBR names
      const cloth = m.name.startsWith('paint_green'); m.userData.knitwear = true; touched.push(m.name);
      m.onBeforeCompile = shader => {
        Object.assign(shader.uniforms, { knitJersey: { value: maps.jersey }, knitRib: { value: maps.rib }, knitMoss: { value: maps.moss }, knitWaffle: { value: maps.waffle }, knitCable: { value: maps.cable }, knitWeave: { value: maps.weave }, knitBoxes: { value: boxes } });
        shader.vertexShader = 'varying vec3 vKnitWorld; varying vec3 vKnitNormal;\n' + shader.vertexShader.replace('#include <project_vertex>',
          '#include <project_vertex>\nvKnitWorld = (modelMatrix * vec4(transformed, 1.0)).xyz; vKnitNormal = normalize(mat3(modelMatrix) * normal);');
        shader.fragmentShader = `varying vec3 vKnitWorld; varying vec3 vKnitNormal;
uniform sampler2D knitJersey, knitRib, knitMoss, knitWaffle, knitCable, knitWeave; uniform vec4 knitBoxes[${KNIT_BOXES.length * 2}];
float knitTri(sampler2D t, vec3 p, vec3 w, vec2 s) { return texture2D(t, p.zy / s).r * w.x + texture2D(t, p.xz / s.xx).r * w.y + texture2D(t, p.xy / s).r * w.z; }
` + shader.fragmentShader.replace('#include <color_fragment>', `#include <color_fragment>
{
  vec3 p = vKnitWorld, w = pow(abs(normalize(vKnitNormal)), vec3(4.0)); w /= (w.x + w.y + w.z);
  ${cloth ? `float k = knitTri(knitWeave, p, w, vec2(.25, .25)); diffuseColor.rgb *= mix(1.0, k * 1.15, .85);` : `
  bool form = p.x > ${FORMS[0].toFixed(2)} && p.x < ${FORMS[3].toFixed(2)} && p.y > ${FORMS[1].toFixed(2)} && p.y < ${FORMS[4].toFixed(2)} && p.z > ${FORMS[2].toFixed(2)} && p.z < ${FORMS[5].toFixed(2)};
  bool shown = form;
  for (int i = 0; i < ${KNIT_BOXES.length}; i++) { vec3 a = knitBoxes[i].xyz, b = knitBoxes[i + ${KNIT_BOXES.length}].xyz; shown = shown || all(greaterThan(p, a)) && all(lessThan(p, b)); }
  if (shown) {
    float k;
    if (form) { int f = int(floor((p.x - ${FORMS[0].toFixed(2)}) / .71));
      if (f == 0) k = knitTri(knitCable, p, w, vec2(.09, .135)); else if (f == 1) k = knitTri(knitRib, p, w, vec2(.05, .05));
      else if (f == 2) k = knitTri(knitMoss, p, w, vec2(.05, .05)); else k = knitTri(knitWaffle, p, w, vec2(.07, .07));
      diffuseColor.rgb *= mix(1.0, k * 1.2, f < 2 ? .75 : .85);
    } else { k = knitTri(knitJersey, p, w, vec2(.026, .03)); diffuseColor.rgb *= mix(1.0, k * 1.15, .5); }
  }`}
}`);
      };
      m.customProgramCacheKey = () => `release-knitwear-v1-${cloth ? 'cloth' : 'garment'}`;
      m.needsUpdate = true;
    }
  });
  changed?.();
  return { knitwear: touched, textures: Object.values(maps) };
}

// Merchandising carpet: the dark tile (fl_carpet) reads heavy under 132 m2 of desks. Inside the Z07 floor only, a lighter,
// warmer heather tone is proposed (same texture and baked light); the CAD room that shares the material keeps its colour.
export function refineCarpet({ root, changed }) {
  const touched = [];
  root.traverse(o => {
    if (!o.isMesh) return;
    for (const m of [o.material].flat()) {
      if (m.userData.carpet || !/^fl_carpet(_baked)?$/.test(m.name)) continue;
      m.userData.carpet = true; touched.push(m.name);
      const previous = m.onBeforeCompile;
      m.onBeforeCompile = (shader, r) => {
        previous?.call(m, shader, r);
        shader.vertexShader = 'varying vec3 vCarpetWorld;\n' + shader.vertexShader.replace('#include <project_vertex>', '#include <project_vertex>\nvCarpetWorld = (modelMatrix * vec4(transformed, 1.0)).xyz;');
        shader.fragmentShader = 'varying vec3 vCarpetWorld;\n' + shader.fragmentShader.replace('#include <map_fragment>', `#include <map_fragment>
if (vCarpetWorld.x > 9.32 && vCarpetWorld.x < 22.0 && vCarpetWorld.z > -21.29 && vCarpetWorld.z < -10.87 && vCarpetWorld.y < .05) diffuseColor.rgb *= vec3(6.2, 5.8, 5.2);`);
      };
      m.customProgramCacheKey = () => 'release-carpet-v1';
      m.needsUpdate = true;
    }
  });
  changed?.();
  return touched;
}
