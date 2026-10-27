// Camera QC in a real browser (Chromium, WebGL via SwiftShader): node run_camera_qc.js BASE_URL OUT_DIR
// Renders the web GLB from all 38 render cameras (exact metadata), and 6 of them also from the original GLB.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const base = process.argv[2], out = path.resolve(process.argv[3]);
  fs.mkdirSync(out, { recursive: true });
  const meta = JSON.parse(fs.readFileSync(path.join(__dirname, '..', '..', '07_WEB_TOUR_ASSETS', 'office_web_metadata.json')));
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const result = { errors: [], runs: {} };
  for (const [label, glb, names] of [
    ['web', '../model/Final_Office_Interior_web.glb', meta.cameras.map((c) => c.name)],
    ['original', '../model/Final_Office_Interior.glb', ['CAM_01_Reception_A', 'CAM_04_Experience_Centre_A', 'CAM_09_Boardroom_A', 'CAM_13_Design_Studio_A', 'CAM_07_MD_Office_A', 'CAM_ISO_SE']],
  ]) {
    const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
    page.on('pageerror', (e) => result.errors.push(label + ' pageerror: ' + String(e).slice(0, 300)));
    page.on('console', (m) => { if (m.type() === 'error') result.errors.push(label + ' console: ' + m.text().slice(0, 300)); });
    const t0 = Date.now();
    await page.goto(`${base}/qc/index.html?glb=${encodeURIComponent(glb)}`);
    await page.waitForFunction(() => window.__qc && window.__qc.ready, null, { timeout: 600000 });
    const info = await page.evaluate(() => ({ loadSeconds: window.__qc.loadSeconds, meshes: window.__qc.meshes, tris: window.__qc.tris, overheadGroup: window.__qc.overheadGroup, overheadNodes: window.__qc.overheadNodes, gl: window.__qc.gl }));
    result.runs[label] = { ...info, pageSeconds: (Date.now() - t0) / 1000, shots: [] };
    for (const n of names) {
      const s = Date.now();
      const r = await page.evaluate((nm) => window.__qc.shot(nm, 800), n);
      await page.locator('canvas').screenshot({ path: path.join(out, `${label}_${n}.png`), timeout: 300000 });
      result.runs[label].shots.push({ ...r, seconds: (Date.now() - s) / 1000 });
    }
    await page.close();
  }
  fs.writeFileSync(path.join(out, 'camera_qc.json'), JSON.stringify(result, null, 1));
  console.log(JSON.stringify({ errors: result.errors, web: { ...result.runs.web, shots: result.runs.web.shots.length }, original: { ...result.runs.original, shots: result.runs.original.shots.length } }));
  await browser.close();
})().catch((e) => { console.error('QC FAILED', e); process.exit(1); });
