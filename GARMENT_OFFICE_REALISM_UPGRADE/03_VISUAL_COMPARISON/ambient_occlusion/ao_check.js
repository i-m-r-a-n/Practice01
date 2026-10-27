// A/B of ambient occlusion: same room camera with ?ao=0 and ?ao=1 (Chromium, software GPU)
const { chromium } = require('playwright');
(async () => {
  const [base, out] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const res = [];
  for (const ao of ['0', '1']) {
    const p = await b.newPage({ viewport: { width: 1470, height: 956 } });
    const errors = [];
    p.on('pageerror', (e) => errors.push(String(e).slice(0, 200)));
    p.on('console', (m) => { if (m.type() === 'error') errors.push(m.text().slice(0, 200)); });
    await p.goto(`${base}?scale=0.5&welcome=0&ao=${ao}`, { waitUntil: 'load', timeout: 180000 });
    await p.waitForFunction(() => window.__viewer && window.__viewer.ready, null, { timeout: 400000 });
    await p.addStyleTag({ content: '#top,#side,#dock,#disclaimer,#labels,#welcome,#dissolve,#walkhint{display:none!important}' });
    for (const [z, cam] of [['Z08', 'CAM_09_Boardroom_A'], ['Z02', 'CAM_01_Reception_A']]) {
      await p.evaluate((zz) => window.__viewer.api.selectRoom(zz), z);
      await p.waitForFunction((c) => { const s = window.__viewer.api.state(); return !s.flying && s.atCam === c; }, cam, { timeout: 400000 });
      if (ao === '1') { const n0 = await p.evaluate(() => window.__viewer.api.state().aoFrames); await p.waitForFunction((n) => window.__viewer.api.state().aoFrames > n, n0, { timeout: 200000 }); }
      await p.waitForTimeout(1500);
      await p.screenshot({ path: `${out}/ao${ao}_${cam}.jpg`, quality: 85, timeout: 300000 });
      res.push({ ao, cam, state: await p.evaluate(() => window.__viewer.api.state()), counts: await p.evaluate(() => window.__viewer.counts), errors: [...errors] });
    }
    await p.close();
  }
  console.log(JSON.stringify(res.map((r) => ({ ao: r.ao, cam: r.cam, aoFrames: r.state.aoFrames, ambientOcclusion: r.counts.ambientOcclusion, errors: r.errors })), null, 0));
  await b.close();
})().catch((e) => { console.error('AO CHECK FAILED', e); process.exit(1); });
