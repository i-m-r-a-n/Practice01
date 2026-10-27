// Web copy of the approved GLB (the original file is only read):
//   node make_web_glb.mjs Final_Office_Interior.glb Final_Office_Interior_web.glb office_web_metadata.json
// - same nodes, names, meshes, materials and 38 cameras; root nodes grouped under WEB_INTERIOR / WEB_OVERHEAD / WEB_CAMERAS
//   so a viewer hides all ceilings, beams, deck and fittings with one node (WEB_OVERHEAD.visible = false)
// - zone id in node extras where the object name carries one, e.g. "(Z07)"; camera nodes carry shift_y and the render file
// - base colours: the Blender colour nodes the glTF exporter drops (Hue/Saturation/Value, colour-ramp remap, tint multiply)
//   are baked into per-material textures by bake_web_colors.py; sheen colour scaled by the Blender Sheen Weight
// - textures re-encoded to WebP (EXT_texture_webp; JPEG sources lossy q86-92, PNG sources lossless), geometry quantized
//   (KHR_mesh_quantization, 14-bit positions / texcoords, 10-bit normals); both are decoded natively by three.js GLTFLoader
// Packages: @gltf-transform/core, extensions, functions 4.1.1; Python 3 with Pillow (WebP).
import { NodeIO, PropertyType } from '@gltf-transform/core';
import { ALL_EXTENSIONS, EXTTextureWebP } from '@gltf-transform/extensions';
import { dedup, prune, quantize } from '@gltf-transform/functions';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const [src, out, metaPath] = process.argv.slice(2);
const meta = JSON.parse(fs.readFileSync(metaPath, 'utf8'));
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS);
const doc = await io.read(src);
const root = doc.getRoot();
const scene = root.getDefaultScene() ?? root.listScenes()[0];
const overhead = new Set(meta.names.overhead);
const camMeta = Object.fromEntries(meta.cameras.map((c) => [c.name, c]));

// ---------------------------------------------------------------- groups + extras
const groups = { WEB_INTERIOR: doc.createNode('WEB_INTERIOR'), WEB_OVERHEAD: doc.createNode('WEB_OVERHEAD'), WEB_CAMERAS: doc.createNode('WEB_CAMERAS') };
const counts = { WEB_INTERIOR: 0, WEB_OVERHEAD: 0, WEB_CAMERAS: 0 };
for (const n of [...scene.listChildren()]) {
  scene.removeChild(n);
  const key = n.getCamera() ? 'WEB_CAMERAS' : overhead.has(n.getName()) || n.getName().startsWith('WEB_SHELL_OVERHEAD') ? 'WEB_OVERHEAD' : 'WEB_INTERIOR';
  groups[key].addChild(n);
  counts[key]++;
  const m = /\((Z\d\d)\)/.exec(n.getName());
  if (m) n.setExtras({ ...n.getExtras(), zone: m[1] });
  const c = camMeta[n.getName()];
  if (c) n.setExtras({ ...n.getExtras(), zone: c.zone, shift_y: c.shift_y, ...(c.render ? { render: c.render.worker_path, render_size: [c.render.width, c.render.height] } : {}) });
}
for (const [k, g] of Object.entries(groups)) {
  g.setExtras({ role: meta.web_glb.groups[k], nodes: counts[k] });
  scene.addChild(g);
}
scene.setExtras({ source: 'Final_Office_Interior.glb (approved model, unchanged); web copy made by make_web_glb.mjs', metadata: 'office_web_metadata.json' });

// ---------------------------------------------------------------- Blender colour nodes -> baked base colours, sheen weight
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'webglb-'));
const mats = root.listMaterials();
const here = path.dirname(new URL(import.meta.url).pathname);
const lib = process.argv[5] || path.resolve(here, '../../../GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/scripts/lib_materials.py');
const bakeJobs = mats.map((m, i) => {
  const t = m.getBaseColorTexture();
  const src = t && t.getImage() ? path.join(tmp, `bc${i}.img`) : null;
  if (src) fs.writeFileSync(src, t.getImage());
  return { material: m.getName(), src, out: path.join(tmp, `bc${i}.webp`) };
});
const bakeJobsFile = path.join(tmp, 'bake_jobs.json'), bakeReportFile = path.join(tmp, 'bake_report.json');
fs.writeFileSync(bakeJobsFile, JSON.stringify(bakeJobs));
execFileSync('python3', ['-I', process.argv[6] || path.join(here, 'bake_web_colors.py'), bakeJobsFile, lib, bakeReportFile], { stdio: 'inherit' });
const bake = JSON.parse(fs.readFileSync(bakeReportFile, 'utf8'));
for (const b of bake.baked) {
  const m = mats.find((x) => x.getName() === b.material);
  const t = doc.createTexture(`${b.material}_basecolor_web`).setImage(new Uint8Array(fs.readFileSync(b.out))).setMimeType('image/webp');
  m.setBaseColorTexture(t).setBaseColorFactor([1, 1, 1, 1]);
}
for (const s of bake.sheen) {
  const sh = mats.find((x) => x.getName() === s.material)?.getExtension('KHR_materials_sheen');
  if (sh) sh.setSheenColorFactor(sh.getSheenColorFactor().map((v) => v * s.weight));
}
fs.writeFileSync(out.replace(/\.glb$/, '') + '_material_fixes.json', JSON.stringify(bake, (k, v) => (k === 'out' ? undefined : v), 1));

// ---------------------------------------------------------------- textures -> WebP (Pillow)
const textures = root.listTextures();
const jobs = [];
textures.forEach((t, i) => {
  const img = t.getImage();
  if (!img || t.getMimeType() === 'image/webp') return;
  const png = t.getMimeType() === 'image/png';
  const normal = mats.some((m) => m.getNormalTexture() === t);
  const color = mats.some((m) => m.getBaseColorTexture() === t || m.getEmissiveTexture() === t);
  const f = path.join(tmp, `t${i}.${png ? 'png' : 'jpg'}`);
  fs.writeFileSync(f, img);
  jobs.push({ i, f, out: path.join(tmp, `t${i}.webp`), lossless: png, quality: normal ? 92 : color ? 86 : 90 });
});
const jobsFile = path.join(tmp, 'jobs.json');
fs.writeFileSync(jobsFile, JSON.stringify(jobs));
const PY = `
import json, sys
from PIL import Image
for j in json.load(open(sys.argv[1])):
    im = Image.open(j['f'])
    if j['lossless']:
        im.save(j['out'], 'WEBP', lossless=True, quality=100, method=4)
    else:
        im.convert('RGB').save(j['out'], 'WEBP', quality=j['quality'], method=4)
`;
execFileSync('python3', ['-I', '-c', PY, jobsFile], { stdio: 'inherit' });
let before = 0, after = 0;
for (const b of bake.baked) after += fs.statSync(b.out).size;
for (const j of jobs) {
  const t = textures[j.i];
  before += t.getImage().byteLength;
  const webp = new Uint8Array(fs.readFileSync(j.out));
  after += webp.byteLength;
  t.setImage(webp).setMimeType('image/webp');
  if (t.getURI()) t.setURI(t.getURI().replace(/\.(png|jpe?g)$/i, '.webp'));
}
doc.createExtension(EXTTextureWebP).setRequired(true);

// ---------------------------------------------------------------- geometry
await doc.transform(
  dedup({ propertyTypes: [PropertyType.ACCESSOR, PropertyType.MESH, PropertyType.TEXTURE] }),
  quantize({ quantizePosition: 14, quantizeNormal: 10, quantizeTexcoord: 14, quantizeColor: Number(process.env.QUANT_COLOR || 8), quantizeGeneric: 12 }),   // 16 for baked light
  prune({ keepLeaves: true }),
);
await io.write(out, doc);
fs.rmSync(tmp, { recursive: true, force: true });
const r = doc.getRoot();
console.log(JSON.stringify({
  out, bytes: fs.statSync(out).size, textures_bytes_before: before, textures_bytes_after: after,
  nodes: r.listNodes().length, meshes: r.listMeshes().length, materials: r.listMaterials().length, cameras: r.listCameras().length,
  textures: r.listTextures().length, groups: counts,
}));
