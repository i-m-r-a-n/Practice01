// Real-WebGL QA of the live tour (Chromium + SwiftShader WebGL 2): node qa_live_site.js URL OUT_DIR
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const url = process.argv[2], out = path.resolve(process.argv[3]);
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  const log = { url, console: [], errors: [], failed: [], steps: [] };
  page.on('console', (m) => log.console.push(`${m.type()}: ${m.text()}`.slice(0, 400)));
  page.on('pageerror', (e) => log.errors.push(String(e).slice(0, 400)));
  page.on('requestfailed', (r) => log.failed.push(r.url().slice(0, 160) + ' ' + (r.failure() || {}).errorText));
  const t0 = Date.now();
  const step = async (name, fn, wait = 3000) => {
    const s = { step: name };
    try { const r = fn ? await fn() : undefined; if (r !== undefined) s.result = r; } catch (e) { s.error = String(e).slice(0, 300); }
    await page.waitForTimeout(wait);
    try { await page.screenshot({ path: path.join(out, name + '.jpg'), quality: 80, timeout: 240000 }); } catch (e) { s.shotError = String(e).slice(0, 200); }
    s.t = (Date.now() - t0) / 1000;
    log.steps.push(s);
  };
  const text = (sel) => page.evaluate((q) => { const e = document.querySelector(q); return e ? e.textContent.trim().slice(0, 160) : null; }, sel);
  const visible = (sel) => page.evaluate((q) => { const e = document.querySelector(q); return !!e && getComputedStyle(e).display !== 'none' && e.offsetParent !== null; }, sel);
  await page.goto(url, { waitUntil: 'load', timeout: 180000 });
  await page.waitForFunction(() => { const p = document.getElementById('progressBox'); return p && getComputedStyle(p).display === 'none'; }, null, { timeout: 300000 }).catch(() => log.steps.push({ step: 'loading overlay still visible after 300 s' }));
  await step('01_loaded', async () => ({ seconds: (Date.now() - t0) / 1000, rooms: await page.$$eval('#rooms .room', (b) => b.length), title: await text('#roomTitle') }), 5000);
  await step('02_room_boardroom', async () => { await page.click('#rooms .room:has-text("Boardroom")'); return { title: await text('#roomTitle'), desc: await text('#roomDesc'), renderPanel: await visible('#renderPanel') }; }, 6000);
  await step('03_ceiling_button', async () => { await page.click('#ceilingBtn'); return { button: await text('#ceilingBtn') }; }, 3000);
  await step('04_overview', async () => { await page.click('#overviewBtn'); return { title: await text('#roomTitle') }; }, 5000);
  await step('05_overview_ceiling_button', async () => { await page.click('#ceilingBtn'); return { button: await text('#ceilingBtn') }; }, 3000);
  await step('06_walk_forward', async () => { await page.click('#walkBtn'); await page.waitForTimeout(2500); await page.keyboard.down('KeyW'); await page.waitForTimeout(2000); await page.keyboard.up('KeyW'); return { title: await text('#roomTitle') }; }, 2000);
  await page.keyboard.press('Escape');
  await step('07_tour_start', async () => { await page.click('#tourBtn'); return { tourbar: await visible('#tourbar'), label: await text('#tourLabel'), count: await text('#tourCount') }; }, 7000);
  await step('08_tour_next', async () => { await page.click('#tourNext'); return { label: await text('#tourLabel'), count: await text('#tourCount') }; }, 6000);
  await step('09_tour_pause', async () => { await page.click('#tourPause'); return { pauseButton: await text('#tourPause') }; }, 1500);
  await step('10_tour_stop', async () => { await page.click('#tourStop'); return { tourbarVisible: await visible('#tourbar') }; }, 2000);
  await step('11_search', async () => { await page.fill('#search', 'design'); return { visibleRooms: await page.$$eval('#rooms .room', (b) => b.filter((x) => x.offsetParent !== null).length) }; }, 1000);
  log.seconds = (Date.now() - t0) / 1000;
  fs.writeFileSync(path.join(out, 'qa_live_site.json'), JSON.stringify(log, null, 1));
  console.log(JSON.stringify({ errors: log.errors, failed: log.failed.slice(0, 5), steps: log.steps, consoleInfo: log.console.filter((c) => /Loaded|error|warn/i.test(c)).slice(0, 8) }, null, 1));
  await browser.close();
})().catch((e) => { console.error('QA FAILED', e); process.exit(1); });
