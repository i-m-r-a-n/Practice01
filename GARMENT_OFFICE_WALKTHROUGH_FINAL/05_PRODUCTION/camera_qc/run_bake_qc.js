// Baked-light check: renders a few render cameras from a GLB with baked light at several exposure factors (bx).
// node run_bake_qc.js BASE_URL OUT_DIR GLB_PATH(relative to qc/) bx1,bx2,... CAM1,CAM2,...
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const [base, outDir, glb, bxs, camList] = process.argv.slice(2);
  const out = path.resolve(outDir); fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const res = { errors: [], runs: [] };
  for (const bx of bxs.split(',')) {
    const page = await browser.newPage({ viewport: { width: 800, height: 600 } });
    page.on('pageerror', (e) => res.errors.push(String(e).slice(0, 300)));
    await page.goto(`${base}/qc/index.html?glb=${encodeURIComponent(glb)}&bx=${bx}`);
    await page.waitForFunction(() => window.__qc && window.__qc.ready, null, { timeout: 600000 });
    const info = await page.evaluate(() => ({ baked: window.__qc.baked, meshes: window.__qc.meshes, load: window.__qc.loadSeconds }));
    for (const cam of camList.split(',')) {
      await page.evaluate((c) => window.__qc.shot(c, 800), cam);
      await page.locator('canvas').screenshot({ path: path.join(out, `bx${bx}_${cam}.png`), timeout: 300000 });
    }
    res.runs.push({ bx, ...info });
    await page.close();
  }
  fs.writeFileSync(path.join(out, 'bake_qc.json'), JSON.stringify(res, null, 1));
  console.log(JSON.stringify(res));
  await browser.close();
})().catch((e) => { console.error('BAKE QC FAILED', e); process.exit(1); });
