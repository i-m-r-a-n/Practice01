import * as THREE from 'three';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { GTAOPass } from 'three/addons/postprocessing/GTAOPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { SMAAPass } from 'three/addons/postprocessing/SMAAPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { Pass } from 'three/addons/postprocessing/Pass.js';

// Phase 5: reuse the actual colour pass depth for AO. Glass does not write AO depth.
// Bloom renders emissive geometry only and depth-tests against the main scene texture,
// avoiding a second draw of every opaque office object as a black bloom occluder.
export function createPostProcessing({ renderer, scene, camera, quality, changed = () => {} }) {
  const target = new THREE.WebGLRenderTarget(1, 1, { type: THREE.HalfFloatType, samples: quality === 'high' ? 4 : 0 });
  target.depthTexture = new THREE.DepthTexture(1, 1, THREE.UnsignedIntType);
  const composer = new EffectComposer(renderer, target);
  composer.renderTarget2.depthTexture = new THREE.DepthTexture(1, 1, THREE.UnsignedIntType);
  const render = new RenderPass(scene, camera);
  const ao = new GTAOPass(scene, camera, 1, 1);
  ao.updateGtaoMaterial({ radius: .22, thickness: .5, scale: .7, samples: quality === 'high' ? 16 : 8, screenSpaceRadius: false });
  ao.updatePdMaterial({ radius: 3, samples: 8, rings: 2 }); ao.blendIntensity = .28;
  const originalRender = render.render.bind(render);
  let depth = target.depthTexture, width = 1, height = 1;
  render.render = (r, write, read, ...args) => {
    originalRender(r, write, read, ...args); depth = read.depthTexture;
    ao.setGBuffer(depth, undefined);
  };
  const bloomTarget = new THREE.WebGLRenderTarget(1, 1, { type: THREE.HalfFloatType });
  const bloomComposer = new EffectComposer(renderer, bloomTarget); bloomComposer.renderToScreen = false;
  const bloomScene = new RenderPass(scene, camera), bloom = new UnrealBloomPass(new THREE.Vector2(1, 1), .16, .35, 1.0);
  bloomComposer.addPass(bloomScene); bloomComposer.addPass(bloom);
  const cache = new WeakMap(), owned = new Set();
  const invisible = new THREE.MeshBasicMaterial({ visible: false }); owned.add(invisible);
  const depthUniform = { value: depth }, resolutionUniform = { value: new THREE.Vector2(1, 1) };
  function emitter(source) {
    if (!source.emissive || source.emissive.getHex() === 0 || source.emissiveIntensity <= 0) return invisible;
    if (!cache.has(source)) {
      const m = new THREE.MeshBasicMaterial({ color: source.emissive.clone().multiplyScalar(source.emissiveIntensity),
        map: source.emissiveMap, side: source.side, depthWrite: false, toneMapped: false, alphaTest: source.alphaTest });
      m.onBeforeCompile = shader => {
        shader.uniforms.mainDepth = depthUniform; shader.uniforms.bloomResolution = resolutionUniform;
        shader.fragmentShader = 'uniform sampler2D mainDepth; uniform vec2 bloomResolution;\n' + shader.fragmentShader;
        shader.fragmentShader = shader.fragmentShader.replace('#include <clipping_planes_fragment>', '#include <clipping_planes_fragment>\nif(gl_FragCoord.z>texture2D(mainDepth,gl_FragCoord.xy/bloomResolution).x+0.00002) discard;');
      };
      m.customProgramCacheKey = () => 'emissive-only-depth-bloom-v1';
      cache.set(source, m); owned.add(m);
    }
    return cache.get(source);
  }
  class BloomCapture extends Pass {
    constructor() { super(); this.needsSwap = false; }
    render() {
      const restore = [];
      depthUniform.value = depth;
      scene.traverse(mesh => {
        if (!mesh.isMesh) return;
        restore.push([mesh, mesh.material]);
        mesh.material = Array.isArray(mesh.material) ? mesh.material.map(emitter) : emitter(mesh.material);
      });
      try { bloomComposer.render(); }
      finally { restore.forEach(([mesh, material]) => { mesh.material = material; }); }
      combine.uniforms.bloomTexture.value = bloomComposer.readBuffer.texture;
    }
  }
  const combine = new ShaderPass({ uniforms: { tDiffuse: { value: null }, bloomTexture: { value: null } },
    vertexShader: 'varying vec2 vUv; void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}',
    fragmentShader: 'uniform sampler2D tDiffuse; uniform sampler2D bloomTexture; varying vec2 vUv; void main(){vec4 base=texture2D(tDiffuse,vUv);gl_FragColor=vec4(base.rgb+texture2D(bloomTexture,vUv).rgb,base.a);}' });
  composer.addPass(render);
  if (quality !== 'low') { composer.addPass(ao); composer.addPass(new BloomCapture()); composer.addPass(combine); }
  composer.addPass(new OutputPass());
  const smaa = new SMAAPass(1, 1); composer.addPass(smaa);
  const status = { enabled: true, quality, ao: quality !== 'low', emissiveBloom: quality !== 'low', depthReused: true, antialiasing: 'SMAA', allPassCalls: 0, allPassTriangles: 0 };
  const ready = Promise.all([smaa.areaTexture.image, smaa.searchTexture.image].map(image => image.complete ? Promise.resolve() : image.decode())).then(() => { status.antialiasingReady = true; changed(); });
  function resize(w, h) {
    if (width === w && height === h) return;
    width = w; height = h;
    const ratio = renderer.getPixelRatio();
    composer.setPixelRatio(ratio); composer.setSize(w, h);
    bloomComposer.setPixelRatio(ratio * .5); bloomComposer.setSize(w, h);
    resolutionUniform.value.set(Math.max(1, Math.floor(w * ratio * .5)), Math.max(1, Math.floor(h * ratio * .5)));
  }
  return {
    status, ready,
    targets: () => [...new Set([composer, bloomComposer, ao, bloom, smaa].flatMap(o => Object.values(o).flat()).filter(o => o?.isWebGLRenderTarget))],
    render(activeCamera, w = innerWidth, h = innerHeight) {
      resize(w, h); render.camera = activeCamera; ao.camera = activeCamera; bloomScene.camera = activeCamera;
      ao.gtaoMaterial.defines.PERSPECTIVE_CAMERA = activeCamera.isPerspectiveCamera ? 1 : 0;
      // Transmissive/frosted glass still renders colour and reflections, but does not
      // become an opaque AO wall. Other alpha-tested cutout geometry keeps its depth.
      scene.traverse(o => { if (o.isMesh) for (const m of (Array.isArray(o.material) ? o.material : [o.material])) {
        if (m.transmission > 0 || m.transparent && m.opacity < .95) m.depthWrite = false;
      } });
      const oldReset = renderer.info.autoReset; renderer.info.autoReset = false; renderer.info.reset();
      try { composer.render(); status.allPassCalls = renderer.info.render.calls; status.allPassTriangles = renderer.info.render.triangles; }
      finally { renderer.info.autoReset = oldReset; }
    },
    dispose() { composer.dispose(); bloomComposer.dispose(); ao.dispose(); bloom.dispose(); smaa.dispose(); owned.forEach(m => m.dispose()); },
  };
}
