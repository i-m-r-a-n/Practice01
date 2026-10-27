// Headless test of the interactive viewer: node test_viewer.js URL OUT_DIR
// Loads the page in Chromium, waits for the model, exercises overview / room / walk / ceilings / tour, saves screenshots
// and writes viewer_test.json with console errors and timings.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const url = process.argv[2], out = path.resolve(process.argv[3]);
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 960, height: 540 } });
  const log = { errors: [], console: [], steps: [] };
  page.on('console', (m) => { log.console.push(`${m.type()}: ${m.text()}`.slice(0, 300)); if (m.type() === 'error') log.errors.push(m.text().slice(0, 300)); });
  page.on('pageerror', (e) => log.errors.push('pageerror: ' + String(e).slice(0, 300)));
  const t0 = Date.now();
  await page.goto(url, { waitUntil: 'load' });
  await page.waitForFunction(() => window.__viewer && window.__viewer.ready, null, { timeout: 420000 });
  log.steps.push({ step: 'model loaded', seconds: (Date.now() - t0) / 1000, counts: await page.evaluate(() => window.__viewer.counts) });
  const shot = async (name, wait = 4000) => { await page.waitForTimeout(wait); await page.screenshot({ path: path.join(out, name + '.png'), timeout: 300000 }); log.steps.push({ step: name, mode: await page.evaluate(() => window.__viewer.mode) }); };
  await shot('01_overview', 6000);
  await page.click('.room[data-id="Z30"]');                    // experience centre from the room list
  await shot('02_room_experience_centre', 7000);
  await page.keyboard.down('KeyW'); await page.waitForTimeout(1500); await page.keyboard.up('KeyW');
  await shot('03_walk_forward', 3000);
  await page.click('#btnOverview');
  await page.waitForTimeout(2500);
  await page.click('#btnCeil');                                // ceilings on in overview
  await shot('04_overview_ceilings_on', 5000);
  await page.click('#btnCeil');
  await page.click('#btnTour');                                // guided tour, step 1 (overview orbit)
  await shot('05_tour_step1', 6000);
  await page.click('#btnNext'); await page.click('#btnNext');   // skip to the reception
  await shot('06_tour_step3_reception', 7000);
  await page.click('#btnTour');                                // pause
  const paused = await page.evaluate(() => window.__viewer.tour && !window.__viewer.tour.playing);
  log.steps.push({ step: 'pause works', ok: paused });
  await page.click('#btnTour');                                // resume
  const resumed = await page.evaluate(() => window.__viewer.tour && window.__viewer.tour.playing);
  log.steps.push({ step: 'resume works', ok: resumed });
  log.seconds_total = (Date.now() - t0) / 1000;
  fs.writeFileSync(path.join(out, 'viewer_test.json'), JSON.stringify(log, null, 1));
  console.log(JSON.stringify({ errors: log.errors, steps: log.steps }, null, 1));
  await browser.close();
})().catch((e) => { console.error('TEST FAILED', e); process.exit(1); });
