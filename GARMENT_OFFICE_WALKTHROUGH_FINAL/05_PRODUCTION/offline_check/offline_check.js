// Opens the offline tour from file:// (as a double-click would), waits for the model, opens the boardroom and its render.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1470, height: 956 } });
  const errors = [];
  p.on('pageerror', (e) => errors.push(String(e).slice(0, 200)));
  p.on('console', (m) => { if (m.type() === 'error') errors.push(m.text().slice(0, 200)); });
  const t0 = Date.now();
  await p.goto('file://' + process.argv[2] + '?scale=0.4', { waitUntil: 'load', timeout: 180000 });
  await p.waitForFunction(() => (window.__viewer && window.__viewer.ready) || !document.getElementById('loadError').classList.contains('hidden'), null, { timeout: 400000 });
  const load = (Date.now() - t0) / 1000;
  const r = await p.evaluate(() => ({ ready: !!window.__viewer.ready, err: document.getElementById('loadError').textContent, counts: window.__viewer.counts, welcome: !document.getElementById('welcome').classList.contains('hidden') }));
  console.log(JSON.stringify({ load, ...r }));
  if (!r.ready) { await b.close(); return; }
  await p.screenshot({ path: process.argv[3] + '/offline_01_welcome.jpg', quality: 80, timeout: 300000 });
  await p.click('#wClose');
  await p.evaluate(() => window.__viewer.api.selectRoom('Z08'));
  await p.waitForFunction(() => { const s = window.__viewer.api.state(); return !s.flying && s.atCam; }, null, { timeout: 400000 });
  await p.waitForTimeout(1500);
  await p.screenshot({ path: process.argv[3] + '/offline_02_boardroom.jpg', quality: 80, timeout: 300000 });
  await p.click('#bPhoto');
  await p.waitForFunction(() => document.getElementById('photo').classList.contains('show'), null, { timeout: 120000 }).catch(() => {});
  const ph = await p.evaluate(() => ({ photo: window.__viewer.api.state().photo, w: document.getElementById('photoImg').naturalWidth, src: document.getElementById('photoImg').src.slice(-40) }));
  await p.waitForTimeout(1000);
  await p.screenshot({ path: process.argv[3] + '/offline_03_boardroom_render.jpg', quality: 80, timeout: 300000 });
  console.log(JSON.stringify({ room: await p.evaluate(() => window.__viewer.api.state()), photo: ph, errors, seconds: (Date.now() - t0) / 1000 }));
  await b.close();
})().catch((e) => { console.error('OFFLINE CHECK FAILED', e); process.exit(1); });
