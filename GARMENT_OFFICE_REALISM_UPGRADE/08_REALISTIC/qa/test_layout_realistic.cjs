// QA copy: original source SHA256 90a1e2952dc651633408e4d2e9937a97653e28d6958cee0b5dd90c64f21009b8
// Original viewer/source remains unchanged. Deterministic photo state; incremental evidence.
// Layout test of the tour interface: node test_layout.js PAGE_URL OUT_DIR
// For each screen (welcome, overview, room, guided tour, tour + photoreal render, walk) and each window size it checks that no
// two visible panels overlap, that nothing sticks out of the window, and saves a screenshot. Chromium, WebGL 2 via SwiftShader.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
// Mac presentation sizes (CSS pixels): projector 1920x1080, the reported 2000x1093 window, MacBook Pro 16 / 14, MacBook Air 13 / 15-inch defaults, older 13-inch
const SIZES = [[2000, 1093], [1920, 1080], [1728, 1117], [1512, 982], [1470, 956], [1440, 900], [1280, 800]];
(async () => {
  const [url, outDir, screenshotMode = "all"] = process.argv.slice(2);
  if (!["all", "representative", "none"].includes(screenshotMode)) throw new Error("screenshot mode must be all, representative or none");
  const out = path.resolve(outDir); fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const log = { url, errors: [], results: [], screenshotMode, status: 'running', note: 'Deterministic QA copy; CSS viewport sizes are not evidence of Mac hardware testing.' };
  const save = () => fs.writeFileSync(path.join(out, 'layout_test.json'), JSON.stringify(log, null, 1));
  page.on('pageerror', (e) => log.errors.push('pageerror: ' + String(e).slice(0, 300)));
  page.on('console', (m) => { if (m.type() === 'error') log.errors.push(m.text().slice(0, 300)); });
  const api = (fn, arg) => page.evaluate(([f, a]) => window.__viewer.api[f](a), [fn, arg]);
  const st = () => page.evaluate(() => window.__viewer.api.state());
  const idle = async () => { await page.waitForFunction(() => !window.__viewer.api.state().flying, null, { timeout: 420000 }); await page.waitForTimeout(600); };
  const panels = () => page.evaluate(() => {
    const ids = ['top', 'side', 'info', 'viewbar', 'tourbar', 'minimap', 'pad', 'walkhint', 'disclaimer', 'photoClose', 'welcome'];
    const R = [];
    for (const id of ids) {
      const e = document.getElementById(id);
      if (!e || !e.getClientRects().length || getComputedStyle(e).visibility === 'hidden') continue;
      if (id === 'photoClose' && document.getElementById('photo').classList.contains('hidden')) continue;
      const b = e.getBoundingClientRect(); if (b.width < 1 || b.height < 1) continue;
      R.push({ id, l: Math.round(b.left), t: Math.round(b.top), r: Math.round(b.right), b: Math.round(b.bottom) });
    }
    const overlaps = [], outside = [];
    for (let i = 0; i < R.length; i++) {
      const a = R[i];
      if (a.l < -1 || a.t < -1 || a.r > innerWidth + 1 || a.b > innerHeight + 1) outside.push(a.id);
      for (let j = i + 1; j < R.length; j++) {
        const c = R[j];
        if (a.id === 'welcome' || c.id === 'welcome') continue;              // the help card is a dialog over everything
        const w = Math.min(a.r, c.r) - Math.max(a.l, c.l), h = Math.min(a.b, c.b) - Math.max(a.t, c.t);
        if (w > 1 && h > 1) overlaps.push(`${a.id} x ${c.id}`);
      }
    }
    return { panels: R.map((p) => p.id), overlaps, outside, hscroll: document.documentElement.scrollWidth > innerWidth + 1 };
  });
  const sweep = async (name) => {
    for (const [w, h] of SIZES) {
      await page.setViewportSize({ width: w, height: h }); await page.waitForTimeout(900);
      const p = await panels();
      const ok = !p.overlaps.length && !p.outside.length && !p.hscroll;
      log.results.push({ screen: name, size: `${w}x${h}`, ok, ...p });
      save();
      if (screenshotMode === 'all' || (screenshotMode === 'representative' && w === 1280)) await page.screenshot({ path: path.join(out, `${name}_${w}x${h}.jpg`), quality: 80, timeout: 300000 });
    }
    await page.setViewportSize({ width: 1280, height: 720 }); await page.waitForTimeout(600);
  };
  const t0 = Date.now();
  await page.goto(url, { waitUntil: 'load', timeout: 180000 });
  await page.waitForFunction(() => window.__viewer && window.__viewer.ready, null, { timeout: 600000 });
  log.loadSeconds = (Date.now() - t0) / 1000;
  log.counts = await page.evaluate(() => window.__viewer.counts);
  log.welcomeShown = await page.evaluate(() => !document.getElementById('welcome').classList.contains('hidden'));
  await sweep('a_welcome');
  await page.click('#wClose'); await page.waitForTimeout(500);
  await sweep('b_overview');
  await page.click('.room[data-zone="Z02"]'); await idle();
  log.room = await st();
  await sweep('c_room_reception');
  await page.check('#tPhoto'); // optional stills default OFF; original layout test omitted this
  await api('startTour', 0);
  if ((await st()).tour.playing) await api('togglePlay'); // pause before costly software-GPU operations
  await idle();
  await api('goStop', 2); await idle();
  await page.waitForFunction(() => window.__viewer.api.state().atCam === 'CAM_01_Reception_A' && !window.__viewer.api.state().tour.playing, null, { timeout: 200000 });
  await api('showPhoto', 'CAM_01_Reception_A');
  await page.waitForFunction(() => window.__viewer.api.state().photo === 'CAM_01_Reception_A' && document.getElementById('photoImg').complete && document.getElementById('photoImg').naturalWidth > 0 && document.getElementById('photo').classList.contains('show'), null, { timeout: 200000 });
  await page.waitForTimeout(800); // allow only the image dissolve to settle, not tour state
  log.tour = await st();
  await sweep('d_tour_stop3_photoreal');
  await page.click('#photoClose');
  await page.waitForFunction(() => !window.__viewer.api.state().photo && document.getElementById('photo').classList.contains('hidden'), null, { timeout: 200000 });
  await sweep('e_tour_stop3_3d');
  await api('stopTour', true); await idle();
  await api('startWalk'); await idle();
  log.walk = await st();
  await sweep('f_walk');
  log.seconds = (Date.now() - t0) / 1000;
  log.failed = log.results.filter((r) => !r.ok);
  log.status = log.failed.length ? 'failed' : 'passed';
  save();
  console.log(JSON.stringify({ checks: log.results.length, failed: log.failed.map((r) => `${r.screen} ${r.size}: ${[...r.overlaps, ...r.outside.map((o) => o + ' outside'), r.hscroll ? 'hscroll' : ''].join(', ')}`), errors: log.errors, welcome: log.welcomeShown, seconds: log.seconds }, null, 1));
  await browser.close();
})().catch((e) => { console.error('LAYOUT TEST FAILED', e); process.exit(1); });
