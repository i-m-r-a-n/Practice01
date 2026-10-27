// Firefox check of the live site (GPT frontend): load, Reception, Boardroom, guided tour stop 3; screenshots
import puppeteer from 'puppeteer-core';
const [bin, url, out] = process.argv.slice(2);
const b = await puppeteer.launch({ browser: 'firefox', executablePath: bin, headless: !process.env.DISPLAY, protocol: 'webDriverBiDi', env: { ...process.env, LIBGL_ALWAYS_SOFTWARE: '1' } });
const errors = [];
try {
  const p = await b.newPage(); await p.setViewport({ width: 1470, height: 956 });
  p.on('pageerror', (e) => errors.push(String(e.message || e).slice(0, 200)));
  await p.goto(url, { waitUntil: 'load', timeout: 180000 });
  await p.waitForFunction(() => window.__viewer && window.__viewer.ready, { timeout: 600000, polling: 1000 });
  const counts = await p.evaluate(() => window.__viewer.counts);
  const res = { version: await b.version(), counts, rooms: {} };
  for (const [z, cam] of [['Z02', 'CAM_01_Reception_A'], ['Z08', 'CAM_09_Boardroom_A']]) {
    await p.evaluate((zz) => window.__viewer.api.selectRoom(zz), z);
    await p.waitForFunction((c) => { const s = window.__viewer.api.state(); return !s.flying && s.atCam === c; }, { timeout: 600000, polling: 1000 }, cam);
    await new Promise((r) => setTimeout(r, 2500));
    await p.screenshot({ type: 'jpeg', quality: 84, path: `${out}/firefox_live_${cam}.jpg` });
    res.rooms[z] = await p.evaluate(() => window.__viewer.api.state());
  }
  await p.evaluate(() => window.__viewer.api.startTour(0));
  await p.evaluate(() => window.__viewer.api.goStop(2));
  await p.waitForFunction(() => { const s = window.__viewer.api.state(); return !s.flying && s.tour && s.tour.phase === 'hold'; }, { timeout: 600000, polling: 1000 });
  await p.evaluate(() => { window.__viewer.api.togglePlay(); window.__viewer.api.hidePhoto(); });
  await new Promise((r) => setTimeout(r, 1500));
  await p.screenshot({ type: 'jpeg', quality: 84, path: `${out}/firefox_live_tour_stop3.jpg` });
  res.overlap = await p.evaluate(() => { const a = document.getElementById('info'), c = document.getElementById('tourbar'); if (!a || !c || !a.getClientRects().length || !c.getClientRects().length) return 'n/a'; const x = a.getBoundingClientRect(), y = c.getBoundingClientRect(); return Math.min(x.right, y.right) > Math.max(x.left, y.left) && Math.min(x.bottom, y.bottom) > Math.max(x.top, y.top) ? 'info card overlaps tour bar' : 'no overlap'; });
  console.log(JSON.stringify({ ...res, errors }));
} catch (e) { console.log('FF LIVE ERROR', e.message, JSON.stringify(errors)); } finally { await b.close(); }
