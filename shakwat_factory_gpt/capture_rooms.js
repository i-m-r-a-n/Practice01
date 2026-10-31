// Captures every room of the office virtual tour from several angles (headless Chromium).
// Usage: node capture_rooms.js [output_dir]   (resumable: finished rooms are skipped)
const { chromium } = require('playwright');
const fs = require('fs');
const OUT = process.argv[2] || 'shots';
fs.mkdirSync(OUT, { recursive: true });
const MANIFEST = OUT + '/manifest.json';
const log = (...a) => { const s = new Date().toISOString().slice(11,19) + ' ' + a.join(' '); console.log(s); fs.appendFileSync(OUT + '/capture.log', s + '\n'); };
(async () => {
  const browser = await chromium.launch({ args: ['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => log('PAGEERROR', e.message));
  await page.addInitScript(() => { try { localStorage.setItem('tourQuality','high'); } catch(e){} });
  await page.goto('https://stage2-office-virtual-tour.imranahmedjh611.workers.dev/bengal-earth-lab/?debug=1&stage=5', { waitUntil: 'load', timeout: 120000 });
  await page.waitForFunction(() => window.__viewer && window.__viewer.ready, null, { timeout: 300000, polling: 1000 });
  log('viewer ready');
  const cdp = await page.context().newCDPSession(page);
  const shot = async (file) => {
    await page.evaluate(() => new Promise(r => { let n = 0; const f = () => (++n >= 4 ? r() : requestAnimationFrame(f)); requestAnimationFrame(f); }));
    await page.waitForTimeout(250);
    const { data } = await cdp.send('Page.captureScreenshot', { format: 'jpeg', quality: 92 });
    fs.writeFileSync(file, Buffer.from(data, 'base64'));
  };
  const hideUI = () => page.addStyleTag({ content: '#top,#dock,#side,#disclaimer,#labels,#walkhint,#minimap,#welcome,#photo,#loading{display:none!important}' });
  await hideUI();
  const rooms = await page.evaluate(() => {
    const meta = window.__TOUR_DATA.meta;
    return [...document.querySelectorAll('#roomList .room')].map((el, i) => {
      const zone = el.dataset.zone; const m = meta.rooms.find(r => r.zone === zone) || {};
      return { order: i + 1, zone, name: el.querySelector('span').textContent.trim(), group: (el.previousElementSibling && el.previousElementSibling.classList.contains('grp')) ? el.previousElementSibling.textContent.trim() : null,
        metaName: m.name, polygon: m.polygon_xz, centroid: m.centroid_xz, cameras: m.cameras || [], area_sft: m.area_sft };
    });
  });
  // fill groups forward
  let g = null; for (const r of rooms) { if (r.group) g = r.group; else r.group = g; }
  
  log('rooms', rooms.length);
  const manifest = fs.existsSync(MANIFEST) ? JSON.parse(fs.readFileSync(MANIFEST,'utf8')) : {};
  for (const r of rooms) {
    if (manifest[r.zone] && manifest[r.zone].files && manifest[r.zone].files.length) { log('skip', r.zone); continue; }
    const tag = `${String(r.order).padStart(2,'0')}_${r.zone}`;
    const files = [];
    log('ROOM', r.zone, r.name);
    try {
      // 1. room view via selectRoom (fly)
      const cam = await page.evaluate(z => { const m = window.__TOUR_DATA.meta.rooms.find(x => x.zone === z); return m && m.primary_camera; }, r.zone);
      if (cam) {
        await page.evaluate(c => window.__viewer.api.frameCamera(c), cam).catch(e => log(' frameCamera failed', e.message));
      } else {
        await page.evaluate(z => window.__viewer.api.selectRoom(z), r.zone);
        await page.waitForFunction(() => !window.__viewer.api.state().flying, null, { timeout: 240000, polling: 1000 }).catch(() => log('fly timeout'));
      }
      await page.waitForTimeout(800);
      log(' view ready', cam || 'aerial');
      let f = `${OUT}/${tag}_00_room_view.jpg`; await shot(f); files.push(f);
      // 2. eye positions
      const pts = await page.evaluate(({ polygon, centroid }) => {
        const api = window.__viewer.api;
        const inPoly = (x, z) => { let c = false; for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) { const [xi, zi] = polygon[i], [xj, zj] = polygon[j]; if (((zi > z) !== (zj > z)) && (x < (xj - xi) * (z - zi) / (zj - zi) + xi)) c = !c; } return c; };
        const free = (x, z) => inPoly(x, z) && !api.blocked(x, z);
        const nearest = (x0, z0, maxR = 3) => { if (free(x0, z0)) return [x0, z0]; for (let rr = 0.1; rr <= maxR; rr += 0.1) { const n = Math.max(8, Math.round(rr * 40)); for (let k = 0; k < n; k++) { const a = 2 * Math.PI * k / n; const x = x0 + rr * Math.cos(a), z = z0 + rr * Math.sin(a); if (free(x, z)) return [x, z]; } } return null; };
        const [cx, cz] = centroid; const out = { centre: nearest(cx, cz), corners: [] };
        for (const [vx, vz] of polygon) { const dx = cx - vx, dz = cz - vz, d = Math.hypot(dx, dz) || 1; const ins = Math.min(0.9, d * 0.35); const p = nearest(vx + dx / d * ins, vz + dz / d * ins, 2); if (p && (!out.centre || Math.hypot(p[0]-out.centre[0], p[1]-out.centre[1]) > 0.8) && !out.corners.some(q => Math.hypot(q[0]-p[0], q[1]-p[1]) < 1.0)) out.corners.push(p); }
        out.corners = out.corners.slice(0, 4);
        return out;
      }, r);
      log(' pts', JSON.stringify(pts));
      if (pts.centre) {
        const ok = await page.evaluate(([x, z]) => { try { window.__viewer.api.setWalkQAStart(x, z); return true; } catch (e) { return e.message; } }, pts.centre);
        if (ok === true) {
          for (let deg = 0; deg < 360; deg += 45) {
            await page.evaluate(d => window.__viewer.api.stepWalkQA({ yaw: d * Math.PI / 180, pitch: 0, fov: 72, forward: 0, strafe: 0, dt: 0 }), deg);
            f = `${OUT}/${tag}_centre_${String(deg).padStart(3,'0')}deg.jpg`; await shot(f); files.push(f);
          }
        } else log(' centre walk failed', ok);
      }
      let ci = 0;
      for (const p of pts.corners) {
        ci++;
        const ok = await page.evaluate(([x, z]) => { try { window.__viewer.api.setWalkQAStart(x, z); return true; } catch (e) { return e.message; } }, p);
        if (ok !== true) { log(' corner walk failed', ok); continue; }
        const dx = r.centroid[0] - p[0], dz = r.centroid[1] - p[1]; const yaw = Math.atan2(-dx, -dz);
        await page.evaluate(y => window.__viewer.api.stepWalkQA({ yaw: y, pitch: -0.06, fov: 78, forward: 0, strafe: 0, dt: 0 }), yaw);
        f = `${OUT}/${tag}_corner_${ci}.jpg`; await shot(f); files.push(f);
      }
    } catch (e) { log(' ERROR', e.message); if (/closed/.test(e.message)) throw e; }
    if (files.length) manifest[r.zone] = { ...r, files };
    fs.writeFileSync(MANIFEST, JSON.stringify(manifest, null, 1));
    log(' done', files.length, 'files');
  }
  await browser.close();
  log('ALL DONE');
})().catch(e => { log('FATAL', e.stack || e.message); process.exit(1); });
