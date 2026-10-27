// Builds the offline tour for presenting from a Mac without a web server or internet:
//   node build_offline_html.mjs BUNDLE_DIR MODEL.glb RENDERS_DIR OUT_DIR
// BUNDLE_DIR = the output of build_worker_bundle.mjs (index.html + app.js). OUT_DIR gets:
//   Ground_Floor_3D_Tour.html   one file: page + three.js + tour app + data + the model (base64, turned into a Blob URL)
//   renders/CAM_xx.jpg          the 38 Cycles renders used by the photoreal panel
// Double-clicking the HTML works because nothing is fetched from another file except <img> renders (allowed from file://).
import fs from 'node:fs';
import path from 'node:path';

const [bundle, model, renders, outDir] = process.argv.slice(2).map((p) => path.resolve(p));
fs.mkdirSync(path.join(outDir, 'renders'), { recursive: true });
let html = fs.readFileSync(path.join(bundle, 'index.html'), 'utf8');
const js = fs.readFileSync(path.join(bundle, 'app.js'), 'utf8').replace(/<\/script/gi, '<\\/script');
const glb = fs.readFileSync(model);
const tag = '<script type="module" src="./app.js"></script>';
if (!html.includes(tag)) throw new Error('module script tag not found in ' + bundle);
const data = `<script type="application/octet-stream" id="glbData">${glb.toString('base64')}</script>
<script>
  // the model is inside this file: decoded once into a Blob URL (no data: URL length limit, e.g. 32 MB in Firefox;
  // works when the page is opened by double-click)
  (function () {
    var b = atob(document.getElementById('glbData').textContent), n = b.length, u = new Uint8Array(n);
    for (var i = 0; i < n; i++) u[i] = b.charCodeAt(i);
    window.__TOUR_CONFIG = { models: [URL.createObjectURL(new Blob([u], { type: 'model/gltf-binary' }))], renders: './renders/' };
  })();
</script>
`;
html = html.replace(tag, () => `${data}<script type="module">\n${js}\n</script>`);
fs.writeFileSync(path.join(outDir, 'Ground_Floor_3D_Tour.html'), html);
const meta = JSON.parse(fs.readFileSync(path.join(path.dirname(new URL(import.meta.url).pathname), '../07_WEB_TOUR_ASSETS/office_web_metadata.json'), 'utf8'));
let n = 0;
for (const c of meta.cameras) {
  const f = path.join(renders, c.name + '.jpg');
  if (fs.existsSync(f)) { fs.copyFileSync(f, path.join(outDir, 'renders', c.name + '.jpg')); n++; }
}
console.log(JSON.stringify({ out: outDir, html_bytes: fs.statSync(path.join(outDir, 'Ground_Floor_3D_Tour.html')).size, model_bytes: glb.length, renders: n, cameras: meta.cameras.length }));
