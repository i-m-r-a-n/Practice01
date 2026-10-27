// Builds a 2-file version of the tour for a static host / the Cloudflare Worker (no CDN, no import map):
//   node build_worker_bundle.mjs OUT_DIR          (esbuild 0.24 must be resolvable, e.g. NODE_PATH or a local node_modules)
// OUT_DIR/index.html  page with inline CSS and the three client logos inline (small PNG data URIs)
// OUT_DIR/app.js      one ES module: three.js r169 (vendored) + the app + office_web_metadata.json + walk_grid.json
// The page then needs only:  ./model_web_baked.glb (falls back to ./model_web.glb, then ./model.glb = the original GLB)  and  ./renders/<camera>.jpg
import { build } from 'esbuild';
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const here = process.env.TOUR_SRC || path.dirname(new URL(import.meta.url).pathname);   // TOUR_SRC: run a copy from elsewhere
const assets = path.resolve(here, '../../../GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS');
const out = path.resolve(process.argv[2] || path.join(here, 'dist'));
fs.mkdirSync(out, { recursive: true });
const tmp = fs.mkdtempSync(path.join(out, '.build-'));
fs.writeFileSync(path.join(tmp, 'data.js'), [
  `import meta from ${JSON.stringify(path.join(assets, 'office_web_metadata.json'))};`,
  `import grid from ${JSON.stringify(path.join(assets, 'walk_grid.json'))};`,
  'window.__TOUR_DATA = { meta, grid };',
  "window.__TOUR_CONFIG = Object.assign({ models: ['./model_web.glb'], renders: './renders/', lightmapManifest: './lighting/manifest.json' }, window.__TOUR_CONFIG || {});",
].join('\n'));
fs.writeFileSync(path.join(tmp, 'entry.js'), `import './data.js';\nimport ${JSON.stringify(path.join(here, 'app.js'))};\n`);
const vendor = path.join(here, 'vendor/three');
const threeLocal = {
  name: 'three-local',
  setup(b) {
    b.onResolve({ filter: /^three$/ }, () => ({ path: path.join(vendor, 'build/three.module.js') }));
    b.onResolve({ filter: /^three\/addons\// }, (a) => ({ path: path.join(vendor, 'examples/jsm', a.path.slice('three/addons/'.length)) }));
  },
};
await build({
  entryPoints: [path.join(tmp, 'entry.js')], bundle: true, format: 'esm', minify: true, outfile: path.join(out, 'app.js'),
  target: ['chrome90', 'edge90', 'firefox90', 'safari15'], plugins: [threeLocal], loader: { '.json': 'json' }, legalComments: 'eof',
  banner: { js: '// Ground floor - interactive design experience. Bundle of three.js r169 (MIT, (c) 2010-2024 three.js authors) + tour app + data.' },
});
fs.rmSync(tmp, { recursive: true, force: true });

// page: inline CSS, small inline logos, plain module script
let html = fs.readFileSync(path.join(here, 'index.html'), 'utf8');
const css = fs.readFileSync(path.join(here, 'style.css'), 'utf8');
html = html.replace(/<link rel="stylesheet" href="style.css">/, `<style>\n${css}</style>`);
html = html.replace(/<script type="importmap">[\s\S]*?<\/script>\n/, '');
const py = `
import base64, io, sys
from PIL import Image
im = Image.open(sys.argv[1]).convert('RGBA')
im = im.resize((round(im.width * 48 / im.height), 48), Image.LANCZOS)
b = io.BytesIO(); im.save(b, 'PNG', optimize=True)
sys.stdout.write('data:image/png;base64,' + base64.b64encode(b.getvalue()).decode())`;
html = html.replace(/src="assets\/(logo_[a-z0-9_]+\.png)"/g, (m, f) => `src="${execFileSync('python3', ['-I', '-c', py, path.join(here, 'assets', f)]).toString()}"`);
html = html.replace('<script type="module" src="app.js"></script>', '<script type="module" src="./app.js"></script>');
fs.writeFileSync(path.join(out, 'index.html'), html);
console.log(JSON.stringify({ out, index_html_bytes: fs.statSync(path.join(out, 'index.html')).size, app_js_bytes: fs.statSync(path.join(out, 'app.js')).size }));
