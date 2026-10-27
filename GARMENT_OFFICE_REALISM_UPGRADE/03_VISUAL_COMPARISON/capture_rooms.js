// Captures the six flagship rooms from a running tour (live site or local build) at the exact render cameras.
// node capture_rooms.js URL LABEL OUT_DIR      (Chromium, WebGL 2 via SwiftShader)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const ROOMS = [['Z02', 'CAM_01_Reception_A'], ['Z30', 'CAM_04_Experience_Centre_A'], ['Z08', 'CAM_09_Boardroom_A'],
  ['Z12', 'CAM_07_MD_Office_A'], ['Z07', 'CAM_11_Merchandising_A'], ['Z18', 'CAM_13_Design_Studio_A']];
(async () => {
  const [url, label, outDir] = process.argv.slice(2);
  const out = path.resolve(outDir); fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const log = { url, label, errors: [], shots: [] };
  page.on('pageerror', (e) => log.errors.push(String(e).slice(0, 300)));
  page.on('console', (m) => { if (m.type() === 'error') log.errors.push(m.text().slice(0, 300)); });
  const t0 = Date.now();
  await page.goto(url, { waitUntil: 'load', timeout: 180000 });
  await page.waitForFunction(() => window.__viewer && window.__viewer.ready, null, { timeout: 600000 });
  log.loadSeconds = (Date.now() - t0) / 1000;
  log.counts = await page.evaluate(() => window.__viewer.counts);
  // hide the interface so only the 3D view is compared (the page itself is unchanged)
  await page.addStyleTag({ content: '#top,#side,#sideOpen,#info,#viewbar,#tourbar,#disclaimer,#labels,#minimap,#walkhint,#pad,#dock,#welcome{display:none!important}' });
  for (const [zone, cam] of ROOMS) {
    await page.evaluate((z) => window.__viewer.api.selectRoom(z), zone);
    await page.waitForFunction((c) => { const s = window.__viewer.api.state(); return !s.flying && s.atCam === c; }, cam, { timeout: 400000 });
    await page.waitForTimeout(2500);
    await page.screenshot({ path: path.join(out, `${label}_${cam}.png`), timeout: 300000 });
    log.shots.push({ zone, cam, state: await page.evaluate(() => window.__viewer.api.state()) });
  }
  fs.writeFileSync(path.join(out, `${label}_capture.json`), JSON.stringify(log, null, 1));
  console.log(JSON.stringify({ label, load: log.loadSeconds, counts: log.counts, errors: log.errors, shots: log.shots.length }));
  await browser.close();
})().catch((e) => { console.error('CAPTURE FAILED', e); process.exit(1); });
