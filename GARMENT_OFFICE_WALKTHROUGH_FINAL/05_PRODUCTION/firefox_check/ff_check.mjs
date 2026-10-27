// Firefox check of the tour (headless Firefox, WebDriver BiDi via puppeteer-core): node ff_check.mjs FIREFOX_BIN URL OUT_DIR LABEL
import puppeteer from 'puppeteer-core';
import fs from 'node:fs';
import path from 'node:path';

const [bin, url, outDir, label] = process.argv.slice(2);
fs.mkdirSync(outDir, { recursive: true });
const log = { url, label, errors: [], steps: [] };
const step = (name, data) => { log.steps.push({ name, t: +((Date.now() - t0) / 1000).toFixed(1), ...data }); console.log(name, JSON.stringify(data || {})); };
const t0 = Date.now();
const browser = await puppeteer.launch({
  browser: 'firefox', executablePath: bin, headless: !process.env.DISPLAY, protocol: 'webDriverBiDi',
  extraPrefsFirefox: { 'webgl.force-enabled': true, 'webgl.disabled': false, 'layers.acceleration.force-enabled': true },
  env: { ...process.env, LIBGL_ALWAYS_SOFTWARE: '1' },
});
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1470, height: 956 });
  page.on('pageerror', (e) => log.errors.push('pageerror: ' + String(e.message || e).slice(0, 300)));
  page.on('console', (m) => { if (m.type() === 'error') log.errors.push(m.text().slice(0, 300)); });
  step('browser', { version: await browser.version() });
  await page.goto(url, { waitUntil: 'load', timeout: 180000 });
  step('webgl', await page.evaluate(() => { const c = document.createElement('canvas'); const g = c.getContext('webgl2'); return { webgl2: !!g, renderer: g ? g.getParameter(g.RENDERER) : null }; }));
  await page.waitForFunction(() => (window.__viewer && window.__viewer.ready) || !document.getElementById('loadError').classList.contains('hidden'), { timeout: 600000, polling: 1000 });
  const s0 = await page.evaluate(() => ({ ready: !!(window.__viewer && window.__viewer.ready), err: document.getElementById('loadError').textContent, counts: window.__viewer && window.__viewer.counts, welcome: !document.getElementById('welcome').classList.contains('hidden') }));
  step('loaded', s0);
  await page.screenshot({ type: 'jpeg', quality: 84, path: path.join(outDir, `${label}_01_welcome.jpg`) });
  if (s0.ready) {
    await page.click('#wClose');
    await page.evaluate(() => window.__viewer.api.selectRoom('Z08'));
    await page.waitForFunction(() => { const s = window.__viewer.api.state(); return !s.flying && s.atCam; }, { timeout: 600000, polling: 1000 });
    await new Promise((r) => setTimeout(r, 2000));
    step('room', await page.evaluate(() => window.__viewer.api.state()));
    await page.screenshot({ type: 'jpeg', quality: 84, path: path.join(outDir, `${label}_02_boardroom.jpg`) });
    await page.click('#bPhoto');
    await page.waitForFunction(() => document.getElementById('photo').classList.contains('show'), { timeout: 120000, polling: 500 }).catch(() => {});
    await new Promise((r) => setTimeout(r, 1500));
    step('photo', await page.evaluate(() => ({ photo: window.__viewer.api.state().photo, w: document.getElementById('photoImg').naturalWidth })));
    await page.screenshot({ type: 'jpeg', quality: 84, path: path.join(outDir, `${label}_03_boardroom_render.jpg`) });
    await page.click('#photoClose');
    await page.evaluate(() => window.__viewer.api.startTour(0));
    await page.evaluate(() => window.__viewer.api.goStop(2));
    await page.waitForFunction(() => { const s = window.__viewer.api.state(); return !s.flying && s.tour && s.tour.phase === 'hold'; }, { timeout: 600000, polling: 1000 });
    await page.evaluate(() => window.__viewer.api.togglePlay());
    await page.evaluate(() => window.__viewer.api.hidePhoto());
    await new Promise((r) => setTimeout(r, 1500));
    step('tour', await page.evaluate(() => ({ ...window.__viewer.api.state(), card: document.getElementById('tTitle').textContent, info: document.getElementById('info').classList.contains('hidden') ? 'hidden' : 'shown' })));
    await page.screenshot({ type: 'jpeg', quality: 84, path: path.join(outDir, `${label}_04_tour_stop3.jpg`) });
    await page.evaluate(() => window.__viewer.api.stopTour(true));
    await page.waitForFunction(() => !window.__viewer.api.state().flying, { timeout: 600000, polling: 1000 });
    await page.evaluate(() => window.__viewer.api.startWalk());
    await page.waitForFunction(() => { const s = window.__viewer.api.state(); return !s.flying && s.mode === 'walk'; }, { timeout: 600000, polling: 1000 });
    const p0 = (await page.evaluate(() => window.__viewer.api.state())).pos;
    await page.keyboard.down('w'); await new Promise((r) => setTimeout(r, 2500)); await page.keyboard.up('w');
    const p1 = (await page.evaluate(() => window.__viewer.api.state())).pos;
    step('walk', { p0, p1, moved: +Math.hypot(p1[0] - p0[0], p1[2] - p0[2]).toFixed(2) });
    await page.screenshot({ type: 'jpeg', quality: 84, path: path.join(outDir, `${label}_05_walk.jpg`) });
  }
} catch (e) {
  log.errors.push('TEST: ' + String(e.message || e).slice(0, 300));
  console.log('FF CHECK ERROR', e.message);
} finally {
  log.seconds = (Date.now() - t0) / 1000;
  fs.writeFileSync(path.join(outDir, `${label}_firefox_check.json`), JSON.stringify(log, null, 1));
  console.log('FF_CHECK_END', JSON.stringify({ errors: log.errors, seconds: log.seconds }));
  await browser.close();
}
