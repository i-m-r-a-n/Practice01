// Browser test of the offline 3D tour (Chromium, WebGL 2 via SwiftShader): node test_viewer.js BASE_URL OUT_DIR [WIDTHxHEIGHT] [PAGE_PATH]
// BASE_URL = the repository root served over http, e.g. http://127.0.0.1:8770
// Checks: loading, overview, room selection (camera = render camera), photoreal panel, ceilings, walk + collision,
// minimap, guided tour (start, pause, resume, next, previous, stop), search, resize, console errors.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const base = process.argv[2], out = path.resolve(process.argv[3]);
  const [vw, vh] = (process.argv[4] || '1280x720').split('x').map(Number);
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: vw, height: vh } });
  const log = { viewport: [vw, vh], errors: [], console: [], checks: [] };
  page.on('console', (m) => { log.console.push(`${m.type()}: ${m.text()}`.slice(0, 300)); if (m.type() === 'error') log.errors.push(m.text().slice(0, 300)); });
  page.on('pageerror', (e) => log.errors.push('pageerror: ' + String(e).slice(0, 300)));
  const t0 = Date.now();
  const st = () => page.evaluate(() => window.__viewer.api.state());
  const check = (name, ok, detail) => { log.checks.push({ name, ok: !!ok, detail }); };
  const shot = (n) => page.screenshot({ path: path.join(out, n + '.jpg'), quality: 82, timeout: 300000 });
  const idle = async (ms = 420000) => { await page.waitForFunction(() => !window.__viewer.api.state().flying, null, { timeout: ms }); await page.waitForTimeout(700); };

  const pagePath = process.argv[5] || '/GARMENT_OFFICE_WALKTHROUGH_FINAL/03_INTERACTIVE_3D/index.html';
  log.page = pagePath;
  await page.goto(`${base}${pagePath}?scale=0.3`, { waitUntil: 'load' });
  await page.waitForFunction(() => window.__viewer && window.__viewer.ready, null, { timeout: 400000 });
  const counts = await page.evaluate(() => window.__viewer.counts);
  check('model loaded, loading screen gone', await page.evaluate(() => getComputedStyle(document.getElementById('loading')).display === 'none'), { seconds: (Date.now() - t0) / 1000, counts });
  check('help card shown on the first visit', await page.evaluate(() => !document.getElementById('welcome').classList.contains('hidden')));
  await page.click('#wClose'); await page.waitForTimeout(500);
  check('help card closes', await page.evaluate(() => document.getElementById('welcome').classList.contains('hidden')));
  await page.waitForTimeout(1500); await shot('01_overview');
  check('room list: 34 rooms in 8 groups', (await page.$$eval('.room', (b) => b.length)) === 34 && (await page.$$eval('.grp', (g) => g.length)) === 8);

  await page.click('.room[data-zone="Z08"]'); await idle();
  let s = await st();
  check('room selection flies to the boardroom render camera', s.room === 'Z08' && s.atCam === 'CAM_09_Boardroom_A' && s.overhead, s);
  await shot('02_room_boardroom');
  const q0 = await page.evaluate(() => window.__viewer.api.state().pos);
  await page.mouse.move(640, 360); await page.mouse.down(); await page.mouse.move(520, 360, { steps: 6 }); await page.mouse.up(); await page.waitForTimeout(800);
  s = await st();
  check('room: drag looks around without moving or leaving the room', s.mode === 'rooms' && s.atCam === null && Math.hypot(s.pos[0] - q0[0], s.pos[2] - q0[2]) < 0.01, s);
  await page.click('#bPhoto'); await page.waitForFunction(() => document.getElementById('photo').classList.contains('show'), null, { timeout: 120000 }).catch(() => {});
  check('photoreal render shown for the same camera', (await st()).photo === 'CAM_09_Boardroom_A' && await page.evaluate(() => document.getElementById('photoImg').naturalWidth === 1600));
  await shot('03_photoreal_boardroom');
  await page.click('#photoClose'); await page.waitForTimeout(1000);

  await page.click('#bBack'); await idle();
  await page.click('#vCeil'); await page.waitForTimeout(1200);
  check('ceilings on in overview', (await st()).overhead === true);
  await shot('04_overview_ceilings_on');
  await page.click('#vCeil'); await page.waitForTimeout(800);
  check('ceilings off again', (await st()).overhead === false);
  await page.click('#vIso'); await idle(); await shot('05_isometric');
  await page.click('#vTop'); await idle(); await shot('06_plan');

  await page.click('#mWalk'); await idle(); await page.waitForTimeout(800);
  const p0 = (await st()).pos;
  await page.keyboard.down('KeyW'); await page.waitForTimeout(2500); await page.keyboard.up('KeyW');
  const p1 = (await st()).pos;
  check('walk: W moves forward at eye height', Math.hypot(p1[0] - p0[0], p1[2] - p0[2]) > 0.5 && Math.abs(p1[1] - p0[1]) < 0.01, { p0, p1 });
  await shot('07_walk_forward');
  // walk straight into the lobby wall for 8 s: the eye point must stay in free floor cells
  await page.keyboard.down('KeyW'); await page.waitForTimeout(8000); await page.keyboard.up('KeyW');
  const p2 = (await st()).pos;
  const inWall = await page.evaluate(([x, z]) => window.__viewer.api.blocked(x, z), [p2[0], p2[2]]);
  check('walk: collision stops at walls / furniture (eye point never inside an obstacle)', !inWall, { p2 });
  await shot('08_walk_collision');
  await page.keyboard.press('Escape'); await idle();
  check('Esc leaves walk mode', (await st()).mode === 'overview');

  await page.click('#mTour'); await page.waitForTimeout(1000);
  s = await st();
  check('tour starts at stop 1', s.mode === 'tour' && s.tour && s.tour.i === 0, s);
  await idle();
  // navigation is checked with the tour paused, so the 6.5 s stop timer cannot move on while a slow test machine takes screenshots
  await page.click('#tPlay');
  const paused = await st();
  await page.waitForTimeout(3000);
  const stillPaused = await st();
  check('pause holds the tour', paused.tour.playing === false && stillPaused.tour.i === paused.tour.i && stillPaused.tour.phase === paused.tour.phase, stillPaused.tour);
  await shot('09_tour_stop01_overview');
  await page.click('#tNext'); await idle();
  s = await st();
  check('next while paused: flies to stop 2, entrance lobby, at its render camera', s.tour.i === 1 && s.atCam === 'CAM_03_Entrance_Lobby' && !s.tour.playing, s);
  check('tour card shows the stop; no separate room card on top of it', await page.evaluate(() => document.getElementById('tTitle').textContent.length > 3
    && document.getElementById('tText').textContent.length > 20 && document.getElementById('info').classList.contains('hidden')));
  await shot('10_tour_stop02_lobby');
  await page.check('#tPhoto');                                  // the photoreal stills are optional (off by default)
  await page.click('#tPlay');
  check('resume', (await st()).tour.playing === true);
  const ph = await page.waitForFunction(() => window.__viewer.api.state().photo === 'CAM_03_Entrance_Lobby', null, { timeout: 120000 }).then(() => true, () => false);
  check('photoreal stop: the render dissolves in at the stop', ph);
  await page.click('#tPlay');                                   // pause again for the next checks
  await page.waitForTimeout(1200); await shot('11_tour_stop02_photoreal');
  s = await st();
  await page.click('#tNext'); await idle(); await page.click('#tNext'); await idle();
  const s4 = await st();
  check('next x2 (from the stop shown): two stops further', s4.tour.i === Math.min(15, s.tour.i + 2) && !s4.flying, { from: s.tour, to: s4.tour, atCam: s4.atCam });
  await shot('12_tour_two_stops_on');
  await page.click('#tPrev'); await idle();
  check('back: one stop earlier', (await st()).tour.i === s4.tour.i - 1);
  await page.evaluate(() => window.__viewer.api.goStop(15)); await idle(); await page.waitForTimeout(1500);
  check('last stop (16) final reveal', (await st()).tour.i === 15);
  await shot('13_tour_stop16_final');
  await page.click('#tPlay');                                   // let the last stop run out
  const ended = await page.waitForFunction(() => { const t = window.__viewer.api.state().tour; return t && t.done; }, null, { timeout: 180000 }).then(() => true, () => false);
  check('tour ends on the final view with Play again (no jump away)', ended && (await st()).mode === 'tour'
    && (await page.evaluate(() => document.getElementById('tPlay').textContent)).includes('Play again'));
  await page.click('#tStop'); await idle();
  check('stop ends the tour', (await st()).mode === 'overview' && !(await st()).tour);

  if (!(await page.evaluate(() => document.getElementById('side').classList.contains('open')))) await page.click('#mRooms');
  await page.waitForTimeout(600);
  await page.fill('#search', 'prayer');
  const found = await page.$$eval('.room', (b) => b.map((x) => x.textContent));
  // 5 rooms mention prayer (the two prayer rooms, the two wudu rooms, the north corridor that leads to them)
  check('search filters the room list', found.length === 5 && found.some((t) => t.includes('Prayer room (male)')) && found.some((t) => t.includes('Prayer room (female)')), found);
  await page.fill('#search', '');
  await page.setViewportSize({ width: 1470, height: 956 }); await page.waitForTimeout(1500);
  check('MacBook Air size (1470 x 956): no horizontal overflow', await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
  await shot('14_macbook_air_1470');
  await page.setViewportSize({ width: vw, height: vh });

  log.seconds = (Date.now() - t0) / 1000;
  log.passed = log.checks.filter((c) => c.ok).length; log.total = log.checks.length;
  fs.writeFileSync(path.join(out, 'viewer_test.json'), JSON.stringify(log, null, 1));
  console.log(JSON.stringify({ passed: `${log.passed}/${log.total}`, failed: log.checks.filter((c) => !c.ok), errors: log.errors, seconds: log.seconds }, null, 1));
  await browser.close();
})().catch((e) => { console.error('TEST FAILED', e); process.exit(1); });
