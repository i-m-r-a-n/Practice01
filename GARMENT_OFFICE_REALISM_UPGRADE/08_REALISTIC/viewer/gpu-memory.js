import * as THREE from 'three';

// Conservative allocation estimate, not a browser/driver VRAM query. Counts
// retained invisible fallback buffers and cached textures; excludes driver metadata.
export function estimateGpuMemory({ scene, textures = [], targets = [] }) {
  const tex = new Map(), buffers = new Set();
  let geometryBytes = 0;
  const addBuffer = attribute => {
    if (!attribute) return; const owner = attribute.isInterleavedBufferAttribute ? attribute.data : attribute;
    if (!buffers.has(owner)) { buffers.add(owner); geometryBytes += owner.array?.byteLength || 0; }
  };
  const addTexture = t => { if (t?.isTexture) tex.set(`${t.source?.uuid || t.uuid}|${t.type}|${t.format}|${t.internalFormat || ''}|${t.wrapS}|${t.wrapT}|${t.minFilter}|${t.magFilter}|${t.anisotropy}|${t.colorSpace}|${t.flipY}`, t); };
  scene.traverse(o => {
    if (!o.isMesh && !o.isLine && !o.isPoints) return;
    const g = o.geometry; if (g) { Object.values(g.attributes).forEach(addBuffer); addBuffer(g.index); Object.values(g.morphAttributes).flat().forEach(addBuffer); }
    addBuffer(o.instanceMatrix); addBuffer(o.instanceColor); addTexture(o.skeleton?.boneTexture);
    for (const m of (Array.isArray(o.material) ? o.material : [o.material])) if (m) Object.values(m).forEach(v => { if (v?.isTexture) addTexture(v); });
  });
  addTexture(scene.environment); addTexture(scene.background); textures.forEach(addTexture);
  const uniqueTargets = [...new Set(targets.filter(Boolean))];
  uniqueTargets.forEach(t => { (t.textures || [t.texture]).forEach(addTexture); addTexture(t.depthTexture); });
  function byteSize(t) {
    if (t.mipmaps?.length && t.mipmaps.every(m => m.data?.byteLength)) return t.mipmaps.reduce((sum, m) => sum + m.data.byteLength, 0);
    const images = Array.isArray(t.image) ? t.image : [t.image];
    let result = 0;
    for (const wrapper of images) {
      const image = wrapper?.image || wrapper;
      if (!image) continue;
      const channels = t.format === THREE.RedFormat || t.format === THREE.DepthFormat ? 1 : t.format === THREE.RGFormat ? 2 : 4;
      const component = t.type === THREE.FloatType || t.type === THREE.UnsignedIntType ? 4 : t.type === THREE.HalfFloatType || t.type === THREE.UnsignedShortType ? 2 : 1;
      result += (image.width || 0) * (image.height || 0) * channels * component;
    }
    return Math.ceil(result * (t.generateMipmaps ? 4 / 3 : 1));
  }
  const textureBytes = [...tex.values()].reduce((sum, t) => sum + byteSize(t), 0);
  let attachmentBytes = 0;
  for (const t of uniqueTargets) {
    const samples = t.samples || 0, pixels = t.width * t.height * (t.isWebGLCubeRenderTarget ? 6 : 1);
    if (samples) attachmentBytes += (t.textures || [t.texture]).reduce((sum, texture) => sum + byteSize(texture), 0) * samples;
    if (t.depthBuffer) attachmentBytes += pixels * 4 * (samples || (t.depthTexture ? 0 : 1));
  }
  return { estimatedTotalBytes: geometryBytes + textureBytes + attachmentBytes, geometryBytes, textureBytes, attachmentBytes,
    textureSources: tex.size, attributeBuffers: buffers.size, renderTargets: uniqueTargets.length,
    method: 'Scene/cached allocation estimate including hidden fallback, compressed mip payload and render attachments; not measured driver VRAM. Probe peak allocations and browser overhead are excluded.' };
}
