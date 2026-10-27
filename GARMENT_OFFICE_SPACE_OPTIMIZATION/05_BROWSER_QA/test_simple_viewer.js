// Functional + layout test of the simple viewer (real clicks, drags, keys; not just "the button exists").
// node test_simple_viewer.js PAGE_URL OUT_DIR [chromium|firefox]
// Chromium: Playwright with WebGL 2 via SwiftShader. Firefox: puppeteer-core over WebDriver BiDi (see run_firefox.sh).
const fs = require('fs');
const path = require('path');

const [url, outDir, engine = 'chromium'] = process.argv.slice(2);
const out = path.resolve(outDir); fs.mkdirSync(out, { recursive: true });
const SIZES = [[1440, 900], [1920, 1080], [1280, 800], [390, 844]];
const results = []; const errors = [];
const ok = (name, pass, detail = '') => { results.push({ name, pass: !!pass, detail }); console.log((pass ? 'PASS ' : 'FAIL ') + name + (detail ? '  ' + detail : '')); };

async function open() {
  if (engine === 'firefox') {
    const puppeteer = require('puppeteer-core');
    const browser = await puppeteer.launch({ browser: 'firefox', executablePath: process.env.FIREFOX_BIN, headless: false, protocol: 'webDriverBiDi',
      extraPrefsFirefox: { 'webgl.force-enabled': true } });
    const page = await browser.newPage();
    await page.setViewport({ width: 1440, height: 900 });
    const P = {
      browser, raw: page,
      goto: (u) => page.goto(u, { timeout: 240000, waitUntil: 'load' }),
      evaluate: (f, a) => page.evaluate(f, a),
      waitFor: (f, a, t) => page.waitForFunction(f, { timeout: t || 300000, polling: 200 }, a),
      size: (w, h) => page.setViewport({ width: w, height: h }),
      shot: (p) => page.screenshot({ path: p, type: 'jpeg', quality: 78 }),
      click: (sel) => page.click(sel),
      mouse: page.mouse, keyboard: page.keyboard,
      wait: (ms) => new Promise((r) => setTimeout(r, ms)),
    };
    page.on('pageerror', (e) => errors.push('pageerror: ' + String(e).slice(0, 300)));
    page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text().slice(0, 300)); });
    return P;
  }
  const { chromium } = require('playwright');
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  page.on('pageerror', (e) => errors.push('pageerror: ' + String(e).slice(0, 300)));
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text().slice(0, 300)); });
  return {
    browser, raw: page,
    goto: (u) => page.goto(u, { timeout: 240000, waitUntil: 'load' }),
    evaluate: (f, a) => page.evaluate(f, a),
    waitFor: (f, a, t) => page.waitForFunction(f, a, { timeout: t || 300000 }),
    size: (w, h) => page.setViewportSize({ width: w, height: h }),
    shot: (p) => page.screenshot({ path: p, type: 'jpeg', quality: 78, timeout: 300000 }),
    click: (sel) => page.click(sel, { timeout: 30000 }),
    mouse: page.mouse, keyboard: page.keyboard,
    wait: (ms) => page.waitForTimeout(ms),
  };
}

(async () => {
  const P = await open();
  const st = () => P.evaluate(() => window.__viewer.api.state());
  const still = async () => { await P.waitFor(() => !window.__viewer.api.state().moving); await P.wait(500); };
  const vis = (id) => P.evaluate((i) => { const e = document.getElementById(i); return !!e && !e.classList.contains('hidden') && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden'; }, id);
  const layout = () => P.evaluate(() => {
    const ids = ['top', 'card', 'planbar', 'tourbar', 'walkhint', 'minimap', 'pad', 'resetView', 'toast', 'disclaimer'];
    const R = [];
    for (const id of ids) {
      const e = document.getElementById(id);
      if (!e || e.classList.contains('hidden') || !e.getClientRects().length || getComputedStyle(e).visibility === 'hidden' || +getComputedStyle(e).opacity === 0) continue;
      const b = e.getBoundingClientRect(); if (b.width < 1 || b.height < 1) continue;
      R.push({ id, l: b.left, t: b.top, r: b.right, b: b.bottom });
    }
    const overlaps = [], outside = [];
    for (let i = 0; i < R.length; i++) {
      const a = R[i];
      if (a.l < -1 || a.t < -1 || a.r > innerWidth + 1 || a.b > innerHeight + 1) outside.push(a.id);
      for (let j = i + 1; j < R.length; j++) {
        const c = R[j];
        if ((a.id === 'top' || c.id === 'top' || a.id === 'disclaimer' || c.id === 'disclaimer') && !['card', 'tourbar', 'planbar', 'walkhint', 'resetView', 'minimap', 'pad'].every((x) => x !== a.id && x !== c.id)) {
          // header / footer gradients are transparent bands; only their buttons / text count: check the real content boxes
        }
        const w = Math.min(a.r, c.r) - Math.max(a.l, c.l), h = Math.min(a.b, c.b) - Math.max(a.t, c.t);
        if (w > 1 && h > 1 && !((a.id === 'disclaimer' || c.id === 'disclaimer') && h < 2)) overlaps.push(`${a.id} x ${c.id}`);
      }
    }
    // labels: only on the plan, never over a panel, never two on top of each other
    const L = [...document.querySelectorAll('.lbl')].filter((e) => e.style.display !== 'none' && document.getElementById('labels').style.display !== 'none').map((e) => e.getBoundingClientRect());
    let lblClash = 0;
    for (let i = 0; i < L.length; i++) for (let j = i + 1; j < L.length; j++) { const a = L[i], c = L[j]; if (Math.min(a.right, c.right) - Math.max(a.left, c.left) > 1 && Math.min(a.bottom, c.bottom) - Math.max(a.top, c.top) > 1) lblClash++; }
    return { panels: R.map((p) => p.id), overlaps, outside, hscroll: document.documentElement.scrollWidth > innerWidth + 1, labels: L.length, lblClash, mode: window.__viewer.mode };
  });
  const sweep = async (name, sizes = SIZES) => {
    const rows = [];
    for (const [w, h] of sizes) {
      await P.size(w, h); await P.wait(900);
      const l = await layout();
      // the header gradient band is decorative: report only real overlaps between panels
      const real = l.overlaps.filter((o) => !/^top x |x top$|disclaimer/.test(o));
      rows.push({ size: `${w}x${h}`, ...l, overlaps: real });
      ok(`layout ${name} ${w}x${h}`, !real.length && !l.outside.length && !l.hscroll && !l.lblClash, JSON.stringify({ panels: l.panels, overlaps: real, outside: l.outside, hscroll: l.hscroll, labels: l.labels, lblClash: l.lblClash }));
      await P.shot(path.join(out, `${name}_${w}x${h}.jpg`));
    }
    await P.size(1440, 900); await P.wait(600);
    return rows;
  };

  const t0 = Date.now();
  await P.goto(url);
  await P.waitFor(() => window.__viewer && window.__viewer.ready, null, 600000);
  const counts = await P.evaluate(() => window.__viewer.counts);
  ok('loads without startup errors', !errors.length, `${((Date.now() - t0) / 1000).toFixed(1)} s; ${JSON.stringify(counts)}`);
  ok('baked light active', counts.bakedLight);
  ok('home screen shows three choices', (await vis('home')) && (await P.evaluate(() => document.querySelectorAll('#home .choice').length)) === 3);
  ok('no tutorial pop-up on load', !(await vis('help')));
  await sweep('a_home');

  // ---------------- tours: names + durations from the configured timings
  await P.click('#hTour');
  ok('tour choice opens', await vis('tourPick'));
  const info = await P.evaluate(() => [document.getElementById('tpQuickInfo').textContent, document.getElementById('tpFullInfo').textContent, window.__viewer.tourSeconds]);
  ok('quick tour is 3-5 minutes', info[2].quick >= 180 && info[2].quick <= 300, `${info[0]} (${info[2].quick} s)`);
  ok('complete tour shows 16 stops', /^16 stops/.test(info[1]), `${info[1]} (${info[2].full} s)`);
  await P.shot(path.join(out, 'b_tour_choice_1440x900.jpg'));
  await P.click('#tpQuick');
  await still();
  let s = await st();
  ok('quick tour starts on the overview', s.mode === 'tour' && s.tour.key === 'quick' && s.tour.i === 0, JSON.stringify(s.tour));
  await P.waitFor(() => window.__viewer.api.state().tour.phase === 'hold');
  await P.click('#tPlay');
  s = await st(); ok('pause', s.tour.playing === false);
  await P.click('#tNext'); await still(); await P.waitFor(() => window.__viewer.api.state().tour.phase === 'hold');
  s = await st(); ok('next works while paused (reception)', s.tour.i === 1 && s.atCam === 'CAM_01_Reception_A' && !s.tour.playing, JSON.stringify(s));
  await P.click('#tNext'); await still(); await P.waitFor(() => window.__viewer.api.state().tour.phase === 'hold');
  s = await st(); ok('room to room at eye level ends on the camera (experience centre)', s.tour.i === 2 && s.atCam === 'CAM_04_Experience_Centre_A');
  await P.click('#tPrev'); await still(); await P.waitFor(() => window.__viewer.api.state().tour.phase === 'hold');
  s = await st(); ok('back works', s.tour.i === 1 && s.atCam === 'CAM_01_Reception_A');
  await P.keyboard.press('ArrowRight'); await still();
  s = await st(); ok('right arrow = next', s.tour.i === 2);
  await P.keyboard.press('Space'); s = await st(); ok('space = resume', s.tour.playing === true);
  await P.keyboard.press('Space');
  await sweep('c_tour_paused');
  // every quick stop reaches its camera
  const qn = await P.evaluate(() => window.__viewer.counts.quickStops);
  let qok = 0;
  for (let i = 0; i < qn; i++) {
    await P.evaluate((k) => window.__viewer.api.goStop(k), i); await still(); await P.waitFor(() => window.__viewer.api.state().tour.phase === 'hold');
    const x = await st();
    const want = await P.evaluate(() => document.getElementById('tTitle').textContent);
    const q = await P.evaluate((k) => fetch('assets/office_web_metadata.json').then((r) => r.json()).then((m) => { const c = m.quick_tour[k].camera; return { c, ortho: m.cameras.find((x) => x.name === c).type === 'ORTHO' }; }), i);
    const faded = await P.evaluate(() => +getComputedStyle(document.getElementById('dissolve')).opacity === 0);
    if (x.tour.i === i && (q.ortho || x.atCam === q.c) && faded) qok++; else console.log('  quick stop', i, q.c, x.atCam, 'dissolve gone', faded);
    if (i === 5 || i === 6) await P.shot(path.join(out, `d_quick_stop${i + 1}_${want.replace(/[^A-Za-z]+/g, '_')}.jpg`));
  }
  ok('all quick-tour stops reached', qok === qn, `${qok}/${qn}`);
  await P.click('#tNext'); await P.wait(400);
  ok('Tour complete card after the last stop', await vis('done'));
  ok('tour complete has Explore rooms / Play again / Return to overview', (await P.evaluate(() => [...document.querySelectorAll('#done .choice')].map((b) => b.textContent.trim()).join('|'))).includes('Play again'));
  await P.shot(path.join(out, 'e_tour_complete_1440x900.jpg'));
  await P.click('#dAgain'); await still();
  s = await st(); ok('play again restarts at stop 1', s.mode === 'tour' && s.tour.i === 0 && !s.tour.done);
  await P.click('#tExit'); await still();
  s = await st(); ok('exit tour returns home', s.mode === 'home' && (await vis('home')));
  // complete tour: all 16 stops (+ the two second views) reach their cameras
  await P.evaluate(() => window.__viewer.api.startTour('full')); await still();
  const meta = await P.evaluate(() => fetch('assets/office_web_metadata.json').then((r) => r.json()));
  let fok = 0;
  for (let i = 0; i < meta.tour.length; i++) {
    await P.evaluate((k) => window.__viewer.api.goStop(k), i); await still(); await P.waitFor(() => window.__viewer.api.state().tour.phase === 'hold');
    const x = await st(); const cam = meta.tour[i].camera;
    const isOrtho = meta.cameras.find((c) => c.name === cam).type === 'ORTHO';
    if (x.tour.i === i && (isOrtho || x.atCam === cam)) fok++; else console.log('  stop', i, cam, JSON.stringify(x));
  }
  ok('complete tour: all 16 stops reach their cameras', fok === meta.tour.length, `${fok}/${meta.tour.length}`);
  await P.keyboard.press('Escape'); await still();

  // ---------------- rooms: menu, all 34 rooms, Merchandising redesign
  await P.click('#nRooms'); await P.wait(500);
  const menu = await P.evaluate(() => ({ groups: [...document.querySelectorAll('#roomGroups .grp')].map((g) => g.textContent), rooms: document.querySelectorAll('#roomGroups .room').length }));
  ok('room menu: 5 groups, 34 rooms', menu.groups.length === 5 && menu.rooms === 34, JSON.stringify(menu));
  await sweep('f_menu', [[1440, 900], [390, 844]]);
  await P.click('#roomGroups .room[data-zone="Z07"]'); await still();
  s = await st();
  ok('choosing Merchandising closes the menu and lands on the sample-hub camera', !(await P.evaluate(() => document.getElementById('menu').classList.contains('open'))) && s.atCam === 'CAM_34_Merchandising_Sample_Hub' && s.overhead, JSON.stringify(s));
  await P.wait(1500);
  await sweep('g_room_merchandising');
  // look around: grab convention (drag right -> yaw grows -> the room follows the pointer)
  const y0 = (await st()).yaw;
  await P.mouse.move(700, 450); await P.mouse.down(); await P.mouse.move(800, 450, { steps: 8 }); await P.mouse.up();
  s = await st();
  ok('drag right turns the view so the room follows the pointer (grab, like a 360 photo)', s.looking && s.yaw > y0 + 0.05, `yaw ${y0} -> ${s.yaw}`);
  ok('reset view button appears after looking around', await vis('resetView'));
  const f0 = (await st()).fov;
  if (engine === 'firefox') await P.raw.mouse.wheel({ deltaY: -400 }); else await P.raw.mouse.wheel(0, -400);
  await P.wait(300);
  const f1 = (await st()).fov;
  ok('scroll zooms in within limits', f1 < f0 && f1 > 10 && f1 < 85, `fov ${f0} -> ${f1}`);
  await P.mouse.dblclick ? await P.mouse.dblclick(700, 450) : await P.mouse.click(700, 450, { clickCount: 2 }); await still();
  s = await st(); ok('double-click resets to the architectural camera', s.atCam === 'CAM_34_Merchandising_Sample_Hub', JSON.stringify(s));
  await P.click('#cPhoto'); await P.waitFor(() => document.getElementById('photo').classList.contains('show'), null, 60000);
  const tag = await P.evaluate(() => document.querySelector('.photo-tag').textContent);
  ok('photorealistic view opens, labelled as a still render', /Photorealistic Blender render/.test(tag), tag);
  await P.shot(path.join(out, 'h_photo_merchandising_1440x900.jpg'));
  await P.click('#photoClose'); await P.wait(800);
  s = await st(); ok('back to the same 3D room and camera', !s.photo && s.mode === 'room' && s.room === 'Z07' && s.atCam === 'CAM_34_Merchandising_Sample_Hub');
  await P.evaluate(() => window.__viewer.api.selectRoom('Z06')); await still(); await P.wait(1200);
  s = await st(); ok('Commercial & accounts opens on the finance-suite camera', s.atCam === 'CAM_36_Accounts_Suite');
  await P.shot(path.join(out, 'i_room_accounts_1440x900.jpg'));
  // all 34 rooms reachable from the menu data
  let rok = 0; const bad = [];
  for (const r of meta.rooms) {
    await P.evaluate((z) => window.__viewer.api.selectRoom(z), r.zone); await still();
    const x = await st();
    if (x.mode === 'room' && x.room === r.zone && (r.primary_camera ? x.atCam === r.primary_camera : true)) rok++; else bad.push(r.zone);
  }
  ok('all 34 rooms open with their camera (or an aerial view)', rok === meta.rooms.length, `${rok}/${meta.rooms.length} ${bad.join(',')}`);

  // ---------------- floor plan
  await P.click('#nPlan'); await still(); await P.wait(800);
  s = await st();
  ok('floor plan view from above with room names', s.mode === 'plan' && s.pos[1] > 20 && (await P.evaluate(() => document.querySelectorAll('.lbl:not([style*="none"])').length)) > 10);
  await sweep('j_plan');
  await P.evaluate(() => { const l = [...document.querySelectorAll('.lbl')].find((e) => e.dataset.zone === 'Z08' && e.style.display !== 'none'); if (l) l.click(); }); await still();
  s = await st(); ok('click a room name on the plan opens it', s.room === 'Z08' && s.atCam === 'CAM_09_Boardroom_A');

  // ---------------- explore freely + collisions
  await P.click('#cWalk'); await P.wait(500);
  s = await st(); ok('explore freely: walk mode with a minimal hint', s.mode === 'walk' && /W A S D/.test(await P.evaluate(() => document.getElementById('walkhint').textContent)));
  const pA = s.pos;
  // software WebGL can take several seconds per frame here: hold W until the camera moves (at most 30 s)
  await P.keyboard.down('KeyW');
  let pB = pA;
  for (let t = 0; t < 30 && Math.hypot(pB[0] - pA[0], pB[2] - pA[2]) <= 0.3; t++) { await P.wait(1000); pB = (await st()).pos; }
  await P.keyboard.up('KeyW');
  ok('W moves forward', Math.hypot(pB[0] - pA[0], pB[2] - pA[2]) > 0.3, `${pA} -> ${pB}`);
  await P.keyboard.down('KeyW'); await P.wait(9000); await P.keyboard.up('KeyW');
  const pC = (await st()).pos;
  const inWall = await P.evaluate((p) => window.__viewer.api.blocked(p[0], p[2]), pC);
  ok('walls stop the walker (never inside a blocked cell)', !inWall, `${pC}`);
  await sweep('k_walk');
  await P.keyboard.press('Escape'); await still();
  s = await st(); ok('Esc leaves walk mode to the room card', s.mode === 'room');

  // ---------------- presentation mode
  await P.evaluate(() => window.__viewer.api.goHome()); await still();
  await P.click('#nPresent'); await still();
  s = await st();
  ok('presentation mode: quick tour, menus hidden, exit button shown', s.present && s.mode === 'tour' && !(await vis('nRooms')) && (await vis('exitPresent')));
  const isFull = await P.evaluate(() => !!(document.fullscreenElement || document.webkitFullscreenElement));
  ok('presentation mode asks for full screen on the click', isFull);
  await P.evaluate(() => document.exitFullscreen && document.fullscreenElement ? document.exitFullscreen() : null); await P.wait(1500);   // the test needs a normal window to resize
  await sweep('l_present', [[1920, 1080], [1440, 900]]);
  await P.keyboard.press('Escape'); await P.wait(800); if ((await st()).present) { await P.keyboard.press('Escape'); await P.wait(800); }
  s = await st(); ok('Esc exits the presentation', !s.present && s.mode === 'home');

  ok('no runtime errors during the test', !errors.length, errors.slice(0, 5).join(' | '));
  const report = { url, engine, seconds: (Date.now() - t0) / 1000, counts, results, errors, passed: results.filter((r) => r.pass).length, total: results.length };
  fs.writeFileSync(path.join(out, 'results.json'), JSON.stringify(report, null, 1));
  console.log(`\n${report.passed}/${report.total} passed in ${report.seconds.toFixed(0)} s`);
  await P.browser.close();
  process.exit(report.passed === report.total ? 0 : 1);
})().catch((e) => { console.error('TEST CRASHED', e); process.exit(2); });
