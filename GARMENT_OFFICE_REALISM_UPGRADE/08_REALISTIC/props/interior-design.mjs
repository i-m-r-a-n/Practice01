/** Interior design layer for the /realistic/ release (Claude, 2026-10-29). Reception first, room by room after.
 * Self-made geometry and canvas textiles only; no external art. Nothing structural or approved moves: textiles hang on
 * existing walls or lie on the approved furniture, and the approved rug keeps its footprint and its baked Cycles light
 * (only its woven design changes, through prepareRoom). Everything is a design reference: no maker, fibre origin or
 * craft claim is made until the client identifies and credits the makers.
 * Usage: buildInteriorDesign(THREE, { zones, anisotropy, detail }) -> { group, items, stats, textures, prepareRoom(room), dispose }
 * Coordinates: viewer metres, x east, y up, z south (as office-props-manifest.json).
 */
import { knitTile } from './knit-tiles.mjs';

export const INTERIOR_ITEMS = [
  { id: 'RC_WARP_WEFT', zone: 'Z02', note: 'Warp & weft: five handloom hangings (khadi with Jamdani-style butis, indigo with kantha running stitch, undyed jute, madder, striped khadi) on an oak rail, washed with warm light.' },
  { id: 'RC_RUG_KANTHA', zone: 'Z02', note: 'The approved rug, redesigned as jute with an indigo border, kantha-style running stitch and a lotus centre. Same footprint and baked light.' },
  { id: 'RC_SOFTS', zone: 'Z02', note: 'Kantha-stitched cushions on the sofa corners and lounge chairs, a stitched throw over the sofa arm.' },
  { id: 'RC_PANEL_LIGHT', zone: 'Z02', note: 'Brass picture light over the Jamdani-inspired panel.' },
  { id: 'RC_WELCOME_SWATCHES', zone: 'Z02', note: 'Fabric rolls and a bowl of coconut-shell buttons on the visitor ledge, for buyers to touch on arrival.' },
  { id: 'RC_SCALLOPS', zone: 'Z02', note: 'Warm scallops of the four existing track spots on the fluted oak wall, as in the Cycles render (vertex light cannot hold them).' },
  { id: 'EC_MATERIALS_LIBRARY', zone: 'Z30', note: 'Tactile materials library on the west end of the material table: yarn cones, knit stitch swatches, and coconut-shell buttons from shell to blank to finished button. Fibre, origin, weight and test data: pending supplier records.' },
  { id: 'EC_TEXTILE_BAFFLES', zone: 'Z30', note: 'Handloom cloth fins under the deck between the two track rails (khadi and jute with woven indigo and madder bands), clear of the spot beams, the AC unit and the smoke detector.' },
  { id: 'EC_GALLERY_LIGHT', zone: 'Z30', note: 'Warm pools of the existing track spots on the plinth and of the linear pendant on the material table.' },
];

const PAL = { khadi: '#e6dccb', khadiShade: '#cfc1a8', jute: '#b39867', juteDark: '#7e6440', indigo: '#33486a', indigoDeep: '#24344f',
  madder: '#8f4a3a', ochre: '#b98a45', thread: '#efe7d6', oak: '#b88e5f', brass: '#a57c3c' };

export function buildInteriorDesign(THREE, { zones = null, anisotropy = 4, detail = 1 } = {}) {
  const group = new THREE.Group(); group.name = 'INTERIOR_DESIGN';
  const geometries = [], materials = [], textures = [];
  const items = INTERIOR_ITEMS.filter(i => !zones || zones.includes(i.zone));
  const want = id => items.some(i => i.id === id);
  const px = n => Math.max(64, Math.round(n * detail));
  // ---------------------------------------------------------------- canvas helpers (deterministic, self-made)
  const rng = seed => () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const canvas = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
  function texture(c, { srgb = true, repeat = null, clamp = false } = {}) {
    const t = new THREE.CanvasTexture(c); t.colorSpace = srgb ? THREE.SRGBColorSpace : THREE.NoColorSpace; t.anisotropy = anisotropy;
    t.wrapS = t.wrapT = clamp ? THREE.ClampToEdgeWrapping : THREE.RepeatWrapping; if (repeat) t.repeat.set(...repeat); textures.push(t); return t;
  }
  function std(name, props) { const m = new THREE.MeshStandardMaterial({ name: 'interior_' + name, ...props }); materials.push(m); return m; }
  function mesh(parent, geometry, material, x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0) {
    geometries.push(geometry); const m = new THREE.Mesh(geometry, material); m.position.set(x, y, z); m.rotation.set(rx, ry, rz);
    m.castShadow = false; m.receiveShadow = false; parent.add(m); return m;
  }
  // plain-weave tile: grey over/under floats between `lo` and `hi`; dark gaps for the normal-map height, a bright
  // tile (lo ~210) for multiply shading so a cloth keeps its dyed colour instead of turning grey
  function weaveTile(size, cells, lo = 76, hi = 220) {
    const c = canvas(size, size), x = c.getContext('2d'), u = size / cells; x.fillStyle = `rgb(${lo},${lo},${lo})`; x.fillRect(0, 0, size, size);
    for (let i = 0; i < cells; i++) for (let j = 0; j < cells; j++) {
      const over = (i + j) % 2 === 0, g = x.createLinearGradient(over ? 0 : i * u, over ? j * u : 0, over ? 0 : (i + 1) * u, over ? (j + 1) * u : 0);
      g.addColorStop(0, `rgb(${lo},${lo},${lo})`); g.addColorStop(.5, `rgb(${hi},${hi},${hi})`); g.addColorStop(1, `rgb(${lo},${lo},${lo})`);
      x.fillStyle = g; if (over) x.fillRect(i * u, j * u + u * .1, u, u * .8); else x.fillRect(i * u + u * .1, j * u, u * .8, u);
    }
    return c;
  }
  function normalFromHeight(src, strength = 2) {
    const w = src.width, h = src.height, d = src.getContext('2d').getImageData(0, 0, w, h).data, out = canvas(w, h), o = out.getContext('2d'), img = o.createImageData(w, h);
    const H = (x, y) => d[(((y + h) % h) * w + ((x + w) % w)) * 4] / 255;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const dx = (H(x + 1, y) - H(x - 1, y)) * strength, dy = (H(x, y + 1) - H(x, y - 1)) * strength, l = Math.hypot(dx, dy, 1), i = (y * w + x) * 4;
      img.data[i] = (-dx / l * .5 + .5) * 255; img.data[i + 1] = (dy / l * .5 + .5) * 255; img.data[i + 2] = (1 / l * .5 + .5) * 255; img.data[i + 3] = 255;
    }
    o.putImageData(img, 0, 0); return out;
  }
  const weaveNormal = texture(normalFromHeight(weaveTile(128, 16), 2.4), { srgb: false });
  // cloth: base colour, woven texture (multiply), slubs and a soft mottle, so the colour is never a flat fill
  function cloth(x, X, Y, W, H, base, { cell = 6, seed = 1, slub = .1, mottle = .06, contrast = .55 } = {}) {
    x.save(); x.beginPath(); x.rect(X, Y, W, H); x.clip();
    x.fillStyle = base; x.fillRect(X, Y, W, H);
    const tile = weaveTile(Math.max(8, cell * 4), 4, Math.round(255 - 50 * contrast), 255); x.globalCompositeOperation = 'multiply';
    x.fillStyle = x.createPattern(tile, 'repeat'); x.fillRect(X, Y, W, H); x.globalCompositeOperation = 'source-over';
    const r = rng(seed);
    for (let i = 0; i < W * H / 900 * slub * 10; i++) {          // slub yarns: short, slightly thicker weft runs
      const sx = X + r() * W, sy = Y + r() * H, len = cell * (3 + r() * 9), light = r() > .5;
      x.fillStyle = light ? `rgba(255,250,238,${.10 + r() * .12})` : `rgba(40,28,16,${.06 + r() * .1})`; x.fillRect(sx, sy, len, Math.max(1, cell * .45));
    }
    for (let i = 0; i < 26; i++) {                                 // dye mottle, as in hand-dyed yarn
      const g = x.createRadialGradient(0, 0, 0, 0, 0, 1), cx = X + r() * W, cy = Y + r() * H, rr = (.08 + r() * .22) * Math.max(W, H);
      g.addColorStop(0, r() > .5 ? `rgba(255,255,255,${mottle})` : `rgba(0,0,0,${mottle})`); g.addColorStop(1, 'rgba(0,0,0,0)');
      x.setTransform(rr, 0, 0, rr, cx, cy); x.fillStyle = g; x.fillRect(-1, -1, 2, 2); x.setTransform(1, 0, 0, 1, 0, 0);
    }
    x.restore();
  }
  // kantha running stitch along a polyline: short raised dashes, a slight irregular rhythm like hand work
  function stitch(x, pts, { dash = 7, gap = 5, width = 2.2, color = PAL.thread, seed = 3, wobble = .8 } = {}) {
    const r = rng(seed), acc = [0];
    for (let i = 1; i < pts.length; i++) acc.push(acc[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
    const total = acc[acc.length - 1]; let k = 1;
    const at = s => { while (k < acc.length - 1 && acc[k] < s) k++; const a = pts[k - 1], b = pts[k], f = (s - acc[k - 1]) / ((acc[k] - acc[k - 1]) || 1); return [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f]; };
    x.strokeStyle = color; x.lineWidth = width; x.lineCap = 'round'; x.beginPath();
    for (let t = r() * gap, on = true; t < total; on = !on) {
      const seg = (on ? dash : gap) * (.8 + r() * .4);
      if (on) { const a = at(t), b = at(Math.min(total, t + seg)), w = (r() - .5) * wobble; x.moveTo(a[0], a[1] + w); x.lineTo(b[0], b[1] + w); }
      t += seg;
    }
    x.stroke();
  }
  const line = (x0, y0, x1, y1, n = 2) => Array.from({ length: n }, (_, i) => [x0 + (x1 - x0) * i / (n - 1), y0 + (y1 - y0) * i / (n - 1)]);
  const wave = (x0, x1, y, amp, period, n = 120) => Array.from({ length: n }, (_, i) => { const t = x0 + (x1 - x0) * i / (n - 1); return [t, y + amp * Math.sin((t - x0) / period * Math.PI * 2)]; });
  const ring = (cx, cy, rx, ry = rx, n = 96) => Array.from({ length: n + 1 }, (_, i) => [cx + rx * Math.cos(i / n * Math.PI * 2), cy + ry * Math.sin(i / n * Math.PI * 2)]);
  const rect = (x0, y0, x1, y1) => [[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]];
  // Jamdani-style buti on the weaving grid: every '1' / '2' cell is one supplementary-weft float
  const BUTI = ['....1....', '...111...', '..1.1.1..', '.1112111.', '1.12221.1', '.1112111.', '..1.1.1..', '...111...', '....1....'];
  const LEAF = ['...1...', '..121..', '.12221.', '1222221', '.12221.', '..121..', '...1...'];
  function buti(x, grid, cx, cy, u, inks) {
    const rows = grid.length, cols = grid[0].length;
    grid.forEach((row, r) => [...row].forEach((v, c) => {
      if (!inks[v]) return; x.fillStyle = inks[v]; const X = cx + (c - cols / 2) * u, Y = cy + (r - rows / 2) * u + u * .12;
      if (x.roundRect) { x.beginPath(); x.roundRect(X, Y, u * .96, u * .76, u * .3); x.fill(); } else x.fillRect(X, Y, u * .96, u * .76);   // older Safari
    }));
  }
  // lotus (padma) in running stitch: rings and petal outlines, the classic centre of a nakshi kantha
  function lotus(x, cx, cy, R, colors, seed = 7, dash = 7) {
    stitch(x, ring(cx, cy, R * .22), { color: colors[0], seed, dash, gap: dash * .6 });
    stitch(x, ring(cx, cy, R * .34), { color: colors[1], seed: seed + 1, dash, gap: dash * .6 });
    for (let k = 0; k < 12; k++) {
      const a = k / 12 * Math.PI * 2;
      // two arcs per petal: out on one side, back on the other
      const side = sgn => Array.from({ length: 25 }, (_, i) => { const t = i / 24, w = Math.sin(t * Math.PI) * .2 * sgn, r = R * (.36 + .62 * t); return [cx + r * Math.cos(a + w), cy + r * Math.sin(a + w)]; });
      stitch(x, side(1), { color: colors[2], seed: seed + 3 + k, dash: dash * .9, gap: dash * .55 });
      stitch(x, side(-1), { color: colors[2], seed: seed + 30 + k, dash: dash * .9, gap: dash * .55 });
    }
    stitch(x, ring(cx, cy, R * 1.04), { color: colors[1], seed: seed + 60, dash, gap: dash * .7 });
  }
  function fringe(x, X, Y, W, H, color, seed = 11) {
    x.clearRect(X, Y, W, H); const r = rng(seed);
    for (let s = X + 2; s < X + W - 2; s += 5) { x.strokeStyle = color; x.lineWidth = 2.6; x.beginPath(); x.moveTo(s, Y); x.lineTo(s + (r() - .5) * 4, Y + H * (.82 + r() * .18)); x.stroke(); }
  }
  function lightFalloff(x, X, Y, W, H, top = 1.06, bottom = .86) {   // a wall-washer from above: brighter top, softer foot
    const g = x.createLinearGradient(0, Y, 0, Y + H); g.addColorStop(0, `rgba(255,236,206,${(top - 1) * 2})`); g.addColorStop(.35, 'rgba(255,236,206,0)'); g.addColorStop(1, `rgba(0,0,0,${1 - bottom})`);
    x.fillStyle = g; x.fillRect(X, Y, W, H);
  }
  // pillow: puffed front and back that meet at a thin seam, with pinched corners
  function pillowGeometry(w, h, t, seg = 18) {
    const pos = [], uv = [], index = [];
    for (const side of [1, -1]) for (let j = 0; j <= seg; j++) for (let i = 0; i <= seg; i++) {
      const u = i / seg, v = j / seg, a = 1 - Math.pow(Math.abs(2 * u - 1), 2.6), b = 1 - Math.pow(Math.abs(2 * v - 1), 2.6);
      const pinch = 1 - .08 * (1 - a) * (1 - b);
      pos.push((u - .5) * w * pinch, (v - .5) * h * pinch, side * t / 2 * Math.pow(a * b, .55)); uv.push(side > 0 ? u : 1 - u, v);
    }
    const n = seg + 1;
    for (let s = 0; s < 2; s++) for (let j = 0; j < seg; j++) for (let i = 0; i < seg; i++) {
      const a = s * n * n + j * n + i, b = a + 1, c = a + n, d = c + 1;
      if (s === 0) index.push(a, b, d, a, d, c); else index.push(a, d, b, a, c, d);
    }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
    g.setIndex(index); g.computeVertexNormals(); return g;
  }
  // hanging cloth: soft vertical folds, a little fuller at the hem; uv mapped into a column of the shared atlas
  function hangingGeometry(w, h, u0, u1, v0, folds, seed) {
    const r = rng(seed), cols = 28, rows = 18, phase = r() * 6.28, g = new THREE.PlaneGeometry(w, h, cols, rows), p = g.attributes.position, uv = g.attributes.uv;
    for (let i = 0; i < p.count; i++) {
      const x = p.getX(i), y = p.getY(i), down = .5 - y / h;                      // 0 at the rail, 1 at the hem
      p.setZ(i, (.009 + .016 * down) * Math.sin((x / w + .5) * folds * Math.PI * 2 + phase) + .004 * Math.sin(y * 9 + phase));
      uv.setXY(i, u0 + (u1 - u0) * uv.getX(i), 1 - (1 - uv.getY(i)) * v0);
    }
    g.computeVertexNormals(); return g;
  }
  // additive warm light pool (a wall-wash or picture-light glow); never a light source, just the visible pool.
  // The intensity lives in the RGB of an opaque canvas (white on black): emissive maps read RGB, not alpha.
  function glowMaterial(name, w, h, shape = 'wash', color = '#ffd2a0', opacity = .3) {
    const c = canvas(256, 256), x = c.getContext('2d'); x.fillStyle = '#000'; x.fillRect(0, 0, 256, 256);
    if (shape === 'wash') { const g = x.createLinearGradient(0, 0, 0, 256); g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(.45, 'rgba(255,255,255,.45)'); g.addColorStop(1, 'rgba(255,255,255,0)'); x.fillStyle = g; x.fillRect(0, 0, 256, 256);
      const e = x.createLinearGradient(0, 0, 256, 0); e.addColorStop(0, 'rgba(0,0,0,1)'); e.addColorStop(.14, 'rgba(0,0,0,0)'); e.addColorStop(.86, 'rgba(0,0,0,0)'); e.addColorStop(1, 'rgba(0,0,0,1)');
      x.fillStyle = e; x.fillRect(0, 0, 256, 256); }
    else { const g = x.createRadialGradient(128, 30, 4, 128, 60, 200); g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(.5, 'rgba(255,255,255,.35)'); g.addColorStop(1, 'rgba(255,255,255,0)'); x.fillStyle = g; x.fillRect(0, 0, 256, 256); }
    return std(name, { color: '#000000', emissive: color, emissiveMap: texture(c, { clamp: true }), transparent: true, opacity, depthWrite: false, blending: THREE.AdditiveBlending, roughness: 1, metalness: 0, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 });
  }

  // ---------------------------------------------------------------- Reception (Z02): south wall face z 6.2738, room on its -z side
  const WALL_S = 6.2738;
  let rugTexture = null;
  if (want('RC_RUG_KANTHA')) {
    // rug F013: 2.74 x 1.98 m (x 8.28-11.02, z 3.96-5.94); its UV0 is metric (u -1.37..1.37, v 0.011..1.989) -> normalised below
    const W = px(2048), H = Math.round(W * 1.978 / 2.74), c = canvas(W, H), x = c.getContext('2d'), m = W / 2.74;   // pixels per metre
    cloth(x, 0, 0, W, H, PAL.jute, { cell: Math.max(3, Math.round(m * .006)), seed: 21, slub: .16, mottle: .07, contrast: .8 });
    const band = (d0, d1, color, seed) => { const a = d0 * m, b = d1 * m; x.save(); x.beginPath(); x.rect(a, a, W - 2 * a, H - 2 * a); x.rect(b, H - b, W - 2 * b, -(H - 2 * b)); x.clip('evenodd'); cloth(x, 0, 0, W, H, color, { cell: Math.max(3, Math.round(m * .005)), seed, slub: .08, mottle: .05, contrast: .6 }); x.restore(); };
    band(0, .035, PAL.juteDark, 22); band(.07, .23, PAL.indigo, 23); band(.255, .272, PAL.madder, 24);
    const inset = d => rect(d * m, d * m, W - d * m, H - d * m);
    stitch(x, inset(.095), { color: PAL.thread, dash: m * .008, gap: m * .006, width: Math.max(1.6, m * .0024), seed: 31 });
    stitch(x, inset(.205), { color: PAL.thread, dash: m * .008, gap: m * .006, width: Math.max(1.6, m * .0024), seed: 32 });
    for (const [y, s] of [[.15, 1], [H / m - .15, -1]]) stitch(x, wave(.15 * m, W - .15 * m, y * m, m * .018 * s, m * .09, 260), { color: PAL.khadi, dash: m * .007, gap: m * .005, width: Math.max(1.6, m * .0022), seed: 33 + s });
    for (const [xx, s] of [[.15, 1], [W / m - .15, -1]]) { const pts = wave(.15 * m, H - .15 * m, 0, m * .018 * s, m * .09, 200).map(([a, b]) => [xx * m + b, a]); stitch(x, pts, { color: PAL.khadi, dash: m * .007, gap: m * .005, width: Math.max(1.6, m * .0022), seed: 35 + s }); }
    stitch(x, inset(.31), { color: PAL.ochre, dash: m * .007, gap: m * .006, width: Math.max(1.6, m * .002), seed: 37 });
    // field: a quiet lattice of stitched crosses in undyed thread, and the lotus at the centre
    for (let gx = .5; gx < 2.74 - .45; gx += .2) for (let gy = .5; gy < 1.978 - .45; gy += .2) {
      if (Math.hypot(gx - 1.37, (gy - .989) * 1.1) < .52) continue;
      const cx = gx * m, cy = gy * m, s = m * .018; stitch(x, line(cx - s, cy, cx + s, cy), { color: 'rgba(240,229,205,.75)', dash: m * .006, gap: m * .004, width: Math.max(1.4, m * .002), seed: gx * 97 + gy });
      stitch(x, line(cx, cy - s, cx, cy + s), { color: 'rgba(240,229,205,.75)', dash: m * .006, gap: m * .004, width: Math.max(1.4, m * .002), seed: gx * 31 + gy * 7 });
    }
    x.fillStyle = PAL.indigo; x.beginPath(); x.arc(W / 2, H / 2, m * .1, 0, Math.PI * 2); x.fill();
    lotus(x, W / 2, H / 2, m * .42, [PAL.thread, PAL.madder, PAL.indigoDeep], 41, m * .008);
    for (const [cx, cy] of [[.52, .52], [2.74 - .52, .52], [.52, 1.978 - .52], [2.74 - .52, 1.978 - .52]]) buti(x, LEAF, cx * m, cy * m, m * .016, { 1: PAL.indigo, 2: PAL.madder });
    rugTexture = texture(c, { clamp: true });
    rugTexture.repeat.set(1 / 2.74, 1 / 1.978); rugTexture.offset.set(.5, -.011 / 1.978);
  }
  if (want('RC_WARP_WEFT')) {
    // five hangings 0.44 m wide, 6 cm apart, on an oak rail 7 cm off the wall; x 10.98-13.42 between the lounge and the planter
    const g = new THREE.Group(); g.name = 'RC_WARP_WEFT'; group.add(g);
    const lengths = [1.86, 1.66, 1.95, 1.74, 1.58], top = 2.40, z = WALL_S - .075, x0 = 12.2 - 1.22, colW = px(400), A = px(2048), pad = Math.round((A - colW * 5) / 5);
    const c = canvas(A, A), x = c.getContext('2d'), m = A / 1.95;    // pixels per metre down a column
    const col = k => k * (colW + pad) + pad / 2;
    const designs = [
      (X, L) => { cloth(x, X, 0, colW, L, PAL.khadi, { cell: 4, seed: 51, slub: .14 });
        for (let r = 0, y = m * .2; y < L - m * .32; r++, y += m * .17) for (const f of r % 2 ? [.5] : [.27, .73]) buti(x, BUTI, X + colW * f, y, m * .011, { 1: PAL.indigo, 2: PAL.ochre });   // half-drop grid
        cloth(x, X, L - m * .24, colW, m * .17, PAL.indigo, { cell: 4, seed: 52 });
        for (let c2 = 0; c2 < 9; c2++) for (let s = 0; s < 4; s++) { x.fillStyle = c2 % 2 ? PAL.ochre : PAL.khadi; x.fillRect(X + c2 * colW / 9 + s * 4, L - m * .22 + s * m * .03, colW / 9 - s * 8, m * .026); } },
      (X, L) => { cloth(x, X, 0, colW, L, PAL.indigo, { cell: 4, seed: 53, slub: .1 });
        for (let y = m * .1; y < L - m * .1; y += m * .016) stitch(x, wave(X + 10, X + colW - 10, y, m * .003, m * .2, 40), { color: 'rgba(236,228,210,.55)', dash: m * .006, gap: m * .005, width: 1.6, seed: y });
        x.fillStyle = PAL.indigoDeep; x.beginPath(); x.arc(X + colW / 2, L * .42, m * .13, 0, Math.PI * 2); x.fill();
        lotus(x, X + colW / 2, L * .42, m * .17, [PAL.thread, PAL.ochre, PAL.thread], 54, m * .007); },
      (X, L) => { cloth(x, X, 0, colW, L, PAL.jute, { cell: 6, seed: 55, slub: .22, contrast: .9 });
        for (const [y, c2, h] of [[L - m * .34, PAL.indigo, .035], [L - m * .28, PAL.madder, .012], [L - m * .25, PAL.indigo, .012]]) cloth(x, X, y, colW, m * h, c2, { cell: 6, seed: y }); },
      (X, L) => { cloth(x, X, 0, colW, L, PAL.madder, { cell: 4, seed: 57, slub: .1 });
        for (let r = 0, y = m * .22; y < L - m * .36; r++, y += m * .24) buti(x, LEAF, X + colW / 2 + (r % 2 ? -1 : 1) * colW * .16, y, m * .016, { 1: PAL.ochre, 2: PAL.khadi });
        cloth(x, X, L - m * .28, colW, m * .2, PAL.khadi, { cell: 4, seed: 58 });
        stitch(x, line(X + 8, L - m * .18, X + colW - 8, L - m * .18), { color: PAL.madder, dash: m * .007, gap: m * .005, width: 2, seed: 59 }); },
      (X, L) => { cloth(x, X, 0, colW, L, PAL.khadi, { cell: 4, seed: 61, slub: .12 });
        for (let s = 0; s < 7; s++) { const xx = X + colW * (.1 + s * .133); x.fillStyle = s % 3 === 1 ? 'rgba(143,74,58,.7)' : 'rgba(51,72,106,.55)'; x.fillRect(xx, 0, colW * (s % 3 === 1 ? .012 : .02), L - m * .3); }
        cloth(x, X, L - m * .3, colW, m * .22, PAL.indigo, { cell: 4, seed: 62 });
        for (let i = 0; i < 6; i++) buti(x, BUTI, X + colW * (.12 + i * .152), L - m * .19, m * .007, { 1: PAL.khadi, 2: PAL.ochre }); },
    ];
    designs.forEach((draw, k) => {
      const X = col(k), L = lengths[k] * m; draw(X, L);
      x.fillStyle = 'rgba(0,0,0,.18)'; x.fillRect(X, 0, colW, m * .035);            // the sleeve folded over the rail
      fringe(x, X, L - m * .06, colW, m * .06, [PAL.khadiShade, PAL.indigoDeep, PAL.juteDark, PAL.madder, PAL.khadiShade][k], 70 + k);
      lightFalloff(x, X, 0, colW, L - m * .06);
    });
    const atlas = texture(c, { clamp: true }), weft = weaveNormal.clone(); weft.repeat.set(480, 480); weft.needsUpdate = true; textures.push(weft);   // ~4 mm weave across the atlas
    const cloths = std('warp_weft', { map: atlas, normalMap: weft, normalScale: new THREE.Vector2(.55, .55), roughness: .96, side: THREE.DoubleSide, alphaTest: .5, emissive: '#ffffff', emissiveMap: atlas, emissiveIntensity: .14 });
    lengths.forEach((L, k) => {
      const u0 = col(k) / A, u1 = (col(k) + colW) / A;
      const panel = mesh(g, hangingGeometry(.44, L, u0, u1, L / 1.95, 3 + (k % 2), 80 + k), cloths, x0 + .22 + k * .5, top - L / 2, z, 0, Math.PI);
      panel.userData.interiorItem = 'RC_WARP_WEFT';
    });
    const oak = std('rail_oak', { color: PAL.oak, roughness: .55 }), brass = std('rail_brass', { color: PAL.brass, roughness: .32, metalness: .85 });
    mesh(g, new THREE.CylinderGeometry(.017, .017, 2.62, 20), oak, 12.2, top + .012, z, 0, 0, Math.PI / 2);
    for (const s of [-1, 1]) { mesh(g, new THREE.SphereGeometry(.022, 16, 10), brass, 12.2 + s * 1.31, top + .012, z);
      mesh(g, new THREE.CylinderGeometry(.007, .007, .075, 10), brass, 12.2 + s * 1.2, top + .012, WALL_S - .0375, Math.PI / 2); }
    // a slim surface wall-washer above the rail (under the steel beams, bottom y 2.59) and the warm pool it throws on the wall
    const fixture = std('washer_body', { color: '#24282a', roughness: .5, metalness: .4 }), led = std('washer_led', { color: '#000000', emissive: '#ffd9a8', emissiveIntensity: 2.2 });
    mesh(g, new THREE.BoxGeometry(2.5, .035, .06), fixture, 12.2, 2.55, WALL_S - .03);
    mesh(g, new THREE.PlaneGeometry(2.46, .03), led, 12.2, 2.5315, WALL_S - .03, Math.PI / 2);
    mesh(g, new THREE.PlaneGeometry(3.0, 2.3), glowMaterial('wash_south', 3.0, 2.3, 'wash', '#f4b47a', .22), 12.2, 2.53 - 1.15, WALL_S - .006, 0, Math.PI);
    // the bay behind the hangings in natural grasscloth (jute weft on a fine cotton warp), framed by slim oak trims
    const gc = canvas(px(1024), px(1024)), gx = gc.getContext('2d'), G = gc.width, gr = rng(131);
    gx.fillStyle = '#b9a47f'; gx.fillRect(0, 0, G, G);
    for (let y = 0; y < G;) {                                    // jute strands: irregular width and tone, slightly wavy
      const h = 2 + gr() * 5, tone = .8 + gr() * .32, wv = gr() * 1.5;
      gx.fillStyle = `rgb(${Math.round(185 * tone)},${Math.round(164 * tone)},${Math.round(127 * tone)})`;
      gx.beginPath(); gx.moveTo(0, y); for (let s = 0; s <= G; s += 64) gx.lineTo(s, y + Math.sin(s * .013 + y) * wv); gx.lineTo(G, y + h); gx.lineTo(0, y + h); gx.fill();
      if (gr() > .6) { gx.fillStyle = `rgba(60,42,22,${.1 + gr() * .12})`; gx.fillRect(gr() * G, y, 20 + gr() * 160, h * .5); }
      y += h;
    }
    for (let s = 3; s < G; s += 7) { gx.fillStyle = 'rgba(236,226,204,.10)'; gx.fillRect(s, 0, 1, G); }   // fine cotton warp
    gx.fillStyle = 'rgba(70,52,30,.35)'; gx.fillRect(0, 0, 2, G);                                          // panel seam every 0.91 m
    const cover = std('grasscloth', { map: texture(gc, { repeat: [2.84 / .91, 2.59 / .91] }), normalMap: weaveNormal, normalScale: new THREE.Vector2(.25, .25), roughness: .92, emissive: '#ffffff', emissiveIntensity: .18 });
    cover.emissiveMap = cover.map;
    mesh(g, new THREE.PlaneGeometry(2.84, 2.59), cover, 12.2, 2.59 / 2, WALL_S - .003, 0, Math.PI);
    for (const s of [-1, 1]) mesh(g, new THREE.BoxGeometry(.03, 2.59, .018), oak, 12.2 + s * 1.435, 2.59 / 2, WALL_S - .009);
  }
  if (want('RC_PANEL_LIGHT')) {
    // the Jamdani-inspired panel (identity-props): 2.1 x 0.72 m centred at x 9.65, y 1.78, its face at z 6.254
    const g = new THREE.Group(); g.name = 'RC_PANEL_LIGHT'; group.add(g);
    const brass = std('picture_brass', { color: PAL.brass, roughness: .3, metalness: .85 }), led = std('picture_led', { color: '#000000', emissive: '#ffd6a6', emissiveIntensity: 2.4 });
    mesh(g, new THREE.CylinderGeometry(.014, .014, .9, 18), brass, 9.65, 2.215, WALL_S - .13, 0, 0, Math.PI / 2);
    mesh(g, new THREE.PlaneGeometry(.86, .012), led, 9.65, 2.2005, WALL_S - .13, Math.PI / 2);
    for (const s of [-1, 1]) mesh(g, new THREE.CylinderGeometry(.006, .006, .13, 8), brass, 9.65 + s * .3, 2.215, WALL_S - .065, Math.PI / 2);
    mesh(g, new THREE.BoxGeometry(.12, .05, .012), brass, 9.65, 2.215, WALL_S - .006);
    mesh(g, new THREE.PlaneGeometry(2.5, 1.0), glowMaterial('picture_pool', 2.5, 1.0, 'pool', '#f4b47a', .2), 9.65, 1.86, WALL_S - .022, 0, Math.PI);
  }
  if (want('RC_SOFTS')) {
    // cushion faces: 2 x 2 atlas of 512 px squares
    const S = px(512), c = canvas(S * 2, S * 2), x = c.getContext('2d'), m = S / .45;
    const face = (k, draw) => { const X = (k % 2) * S, Y = Math.floor(k / 2) * S; x.save(); x.beginPath(); x.rect(X, Y, S, S); x.clip(); draw(X, Y); x.restore(); };
    face(0, (X, Y) => { cloth(x, X, Y, S, S, PAL.indigo, { cell: 4, seed: 91 }); for (let i = 1; i < 9; i++) stitch(x, rect(X + i * S / 20, Y + i * S / 20, X + S - i * S / 20, Y + S - i * S / 20), { color: 'rgba(238,230,212,.85)', dash: m * .008, gap: m * .006, width: 2, seed: 92 + i }); lotus(x, X + S / 2, Y + S / 2, S * .14, [PAL.thread, PAL.ochre, PAL.thread], 93, m * .007); });
    face(1, (X, Y) => {                                       // khadi with bold kantha waves, three stitched rows per band so it reads at a distance
      cloth(x, X, Y, S, S, PAL.khadi, { cell: 4, seed: 94 });
      for (let i = 0; i < 7; i++) for (let k = 0; k < 3; k++) stitch(x, wave(X + 14, X + S - 14, Y + S * (.1 + i * .133) + k * S * .018, m * .009, m * .07, 60), { color: i % 2 ? PAL.indigo : PAL.madder, dash: m * .009, gap: m * .005, width: 3.4, seed: 95 + i * 3 + k });
    });
    face(2, (X, Y) => { cloth(x, X, Y, S, S, PAL.madder, { cell: 4, seed: 96 }); for (let r = 0; r < 3; r++) for (let k = 0; k < 3; k++) buti(x, LEAF, X + S * (.2 + .3 * k) + (r % 2) * S * .15 - S * .07, Y + S * (.2 + .3 * r), m * .011, { 1: PAL.ochre, 2: PAL.khadi }); });
    face(3, (X, Y) => { cloth(x, X, Y, S, S, PAL.jute, { cell: 5, seed: 97, slub: .2, contrast: .9 }); for (const [f, cc, h] of [[.3, PAL.indigo, .07], [.42, PAL.khadi, .02], [.6, PAL.indigo, .07]]) cloth(x, X, Y + S * f, S, S * h, cc, { cell: 4, seed: f * 100 }); });
    const atlas = texture(c, { clamp: true }), quad = k => { const t = atlas.clone(); t.repeat.set(.5, .5); t.offset.set((k % 2) * .5, .5 - Math.floor(k / 2) * .5); t.needsUpdate = true; textures.push(t); return t; };
    const soft = k => std('cushion_' + k, { map: quad(k), normalMap: weaveNormal, normalScale: new THREE.Vector2(.4, .4), roughness: .95, emissive: '#ffffff', emissiveMap: quad(k), emissiveIntensity: .06 });
    const g = new THREE.Group(); g.name = 'RC_SOFTS'; group.add(g);
    // local +z is the face; yaw turns it to the room, a negative tilt leans the top back against the backrest
    const pillow = (mat, w, h, t, x, y, z, yaw, tilt) => { const p = mesh(g, pillowGeometry(w, h, t), mat); p.position.set(x, y, z); p.rotation.set(tilt, yaw, 0, 'YXZ'); return p; };
    // sofa F009: seat top 0.444, back cushions' face z 5.893, arms x 8.60-8.70 / 10.60-10.72; seated people at x 9.25 and 10.07,
    // so each corner keeps ~0.36 m: one cushion per corner, turned towards the middle of the sofa
    pillow(soft(0), .36, .36, .15, 8.885, .64, 5.775, Math.PI - .38, -.2);
    pillow(soft(1), .36, .36, .15, 10.425, .64, 5.775, Math.PI + .38, -.2);
    // lounge chairs: F011 back face x 8.21 (faces +x), F012 back face x 11.09 (faces -x); seat top 0.483
    pillow(soft(2), .42, .28, .13, 8.295, .63, 4.37, Math.PI / 2, -.22);
    pillow(soft(3), .42, .28, .13, 11.005, .63, 4.37, -Math.PI / 2, -.22);
    // stitched throw over the east sofa arm (top 0.610, x 10.60-10.72): an inverted U, 0.42 m along the arm
    const tc = canvas(px(512), px(512)), tx = tc.getContext('2d'), T = tc.width;
    cloth(tx, 0, 0, T, T, PAL.indigo, { cell: 3, seed: 98 });                // indigo kantha throw: reads against the sand sofa
    for (let i = 0; i < 30; i++) stitch(tx, line(6, T * (i + .5) / 30, T - 6, T * (i + .5) / 30), { color: [PAL.thread, PAL.thread, PAL.madder, PAL.ochre][i % 4], dash: 6, gap: 4, width: 1.8, seed: 99 + i });
    cloth(tx, 0, 0, T, T * .06, PAL.madder, { cell: 3, seed: 130 }); cloth(tx, 0, T * .94, T, T * .06, PAL.madder, { cell: 3, seed: 131 });
    const throwMat = std('throw', { map: texture(tc, { clamp: true }), normalMap: weaveNormal, roughness: .96, side: THREE.DoubleSide });
    const path = [[10.594, .47], [10.597, .585], [10.61, .614], [10.66, .622], [10.71, .614], [10.726, .585], [10.73, .4], [10.728, .3]];
    const pos = [], uv = [], index = [], zs = 12; let total = 0; const acc = [0];
    for (let i = 1; i < path.length; i++) acc.push(total += Math.hypot(path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1]));
    for (let j = 0; j <= zs; j++) path.forEach(([px2, py], i) => { const zz = 5.40 + .40 * j / zs, sag = (i === 0 || i === path.length - 1) ? .006 * Math.sin(j / zs * Math.PI * 3) : 0; pos.push(px2 + sag, py, zz); uv.push(acc[i] / total, j / zs); });
    for (let j = 0; j < zs; j++) for (let i = 0; i < path.length - 1; i++) { const a = j * path.length + i, b = a + 1, c2 = a + path.length, d = c2 + 1; index.push(a, c2, b, b, c2, d); }
    const tg = new THREE.BufferGeometry(); tg.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); tg.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); tg.setIndex(index); tg.computeVertexNormals();
    mesh(g, tg, throwMat);
  }
  if (want('RC_WELCOME_SWATCHES')) {
    // visitor ledge of the reception desk: terrazzo top y 1.067 over x 12.25-12.55, z 2.5-5.2 (badge hand-over at z 3.75)
    const g = new THREE.Group(); g.name = 'RC_WELCOME_SWATCHES'; group.add(g);
    const oak = std('tray_oak', { color: '#a9814f', roughness: .5 }), walnut = std('bowl_walnut', { color: '#5a3d27', roughness: .45, side: THREE.DoubleSide }), shell = std('shell_button', { color: '#4f3422', roughness: .38 });
    const box = (mat, x, y, z, w, h, d) => mesh(g, new THREE.BoxGeometry(w, h, d), mat, x, y + h / 2, z);
    box(oak, 12.40, 1.067, 4.72, .19, .012, .34);
    [PAL.jute, PAL.khadi, PAL.indigo, PAL.madder, '#8b8f8a'].forEach((cc, i) => {   // rolls lie across the ledge (along x)
      const mat = std('roll_' + i, { color: cc, roughness: .95, normalMap: weaveNormal, normalScale: new THREE.Vector2(.35, .35) });
      mesh(g, new THREE.CylinderGeometry(.024, .024, .15, 22), mat, 12.40, 1.079 + .024, 4.585 + i * .062, 0, 0, Math.PI / 2);
    });
    const bowl = mesh(g, new THREE.SphereGeometry(.065, 24, 10, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), walnut, 12.40, 1.067 + .039, 5.03); bowl.scale.y = .6;   // shallow, resting on the ledge
    const r = rng(101);
    for (let i = 0; i < 14; i++) { const a = r() * 6.28, d = r() * .036; mesh(g, new THREE.CylinderGeometry(.009, .009, .004, 14), shell, 12.40 + Math.cos(a) * d, 1.071 + d * .35 + r() * .004, 5.03 + Math.sin(a) * d, (r() - .5) * .5, 0, (r() - .5) * .5); }
  }
  if (want('RC_SCALLOPS')) {
    // track spots LT008-LT011 (x 13.80-13.95, y 2.60-2.81) at z 2.41 / 3.43 / 4.445 / 5.46 light the fluted oak face x 14.27
    const W = 256, H = 512, c = canvas(W, H), x = c.getContext('2d'), img = x.createImageData(W, H);
    for (let j = 0; j < H; j++) for (let i = 0; i < W; i++) {
      const X = i / (W - 1) * 2 - 1, Y = j / (H - 1), top = .03 + .3 * X * X;              // rounded top just under the fitting
      const v = Math.min(1, Math.max(0, (Y - top) / .06)) * Math.exp(-Math.pow((Y - .2) / .42, 2)) * Math.pow(Math.max(0, 1 - X * X), 1.6);
      const k = (j * W + i) * 4; img.data[k] = img.data[k + 1] = img.data[k + 2] = Math.round(255 * v); img.data[k + 3] = 255;   // intensity in RGB
    }
    x.putImageData(img, 0, 0);
    const scallop = std('scallop', { color: '#000000', emissive: '#ffc488', emissiveMap: texture(c, { clamp: true }), transparent: true, opacity: .32, depthWrite: false, blending: THREE.AdditiveBlending, roughness: 1, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 });
    for (const z of [2.41, 3.43, 4.445, 5.46]) mesh(group, new THREE.PlaneGeometry(.85, 1.9), scallop, 14.262, 2.62 - .95, z, 0, -Math.PI / 2);
  }
  if (want('EC_MATERIALS_LIBRARY')) {
    // material table F026: top y 0.863 over x 16.55-20.15, z -8.95..-8.05. Its west end already holds two rows of standing rolls
    // (z -8.67..-8.58 and -8.37..-8.28, x 16.65-17.6), so the library uses the free north strip (z -9.0..-8.70) and south strip
    // (z -8.25..-8.05); both are clear of the
    // existing garment stacks, notebook and tape measure, and of the three people (x 18.5-20.3)
    const g = new THREE.Group(); g.name = 'EC_MATERIALS_LIBRARY'; group.add(g); const TOP = .863;
    const oak = std('lib_oak', { color: '#b28a59', roughness: .5 }), walnut = std('lib_walnut', { color: '#5a3d27', roughness: .42 });
    const box = (mat, x, y, z, w, h, d, ry = 0) => mesh(g, new THREE.BoxGeometry(w, h, d), mat, x, y + h / 2, z, 0, ry);
    // 1. yarn cones on an oak board: cross-wound thread, paper core at the tip
    const yarn = (() => { const c = canvas(64, 64), x = c.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0, 0, 64, 64);
      for (let y = 0; y < 64; y += 3) { x.strokeStyle = 'rgba(0,0,0,.16)'; x.lineWidth = 1.2; x.beginPath(); x.moveTo(0, y); for (let s = 0; s <= 64; s += 8) x.lineTo(s, y + Math.sin(s * .2 + y) * .8); x.stroke(); }
      for (let s = -64; s < 64; s += 9) { x.strokeStyle = 'rgba(0,0,0,.07)'; x.beginPath(); x.moveTo(s, 0); x.lineTo(s + 64, 64); x.stroke(); }
      return texture(c, { repeat: [5, 8] }); })();
    const paper = std('cone_core', { color: '#c9a86e', roughness: .8 });
    box(oak, 16.93, TOP, -8.84, .64, .018, .2);
    [PAL.khadi, '#d6c3a0', PAL.indigo, PAL.madder, PAL.ochre, '#6f7a4c', '#9a9a96', '#3b3d40'].forEach((cc, i) => {
      const cx = 16.69 + (i % 4) * .16, cz = -8.89 + Math.floor(i / 4) * .1, base = TOP + .018;
      mesh(g, new THREE.CylinderGeometry(.011, .033, .16, 28), std('yarn_' + i, { color: cc, map: yarn, roughness: .9 }), cx, base + .08, cz);
      mesh(g, new THREE.CylinderGeometry(.008, .0105, .024, 16), paper, cx, base + .172, cz);
    });
    // 2. knit stitch swatches on an oak tray, each stitch at its true scale
    box(oak, 17.96, TOP, -8.84, .66, .012, .2);
    [['jersey', '#e1d6c2', .026], ['rib', PAL.indigo, .05], ['cable', '#d6c3a0', .09], ['moss', '#6f7a4c', .035], ['waffle', PAL.khadi, .05], ['pointelle', PAL.madder, .026]].forEach(([stitch, cc, scale], i) => {
      const t = texture(knitTile(stitch), { srgb: false, repeat: [.13 / scale, .13 / scale * (stitch === 'cable' ? 128 / 192 : 1)] });
      const sw = mesh(g, new THREE.BoxGeometry(.13, .006, .13), std('swatch_' + stitch, { color: cc, map: t, roughness: .96, emissive: '#ffffff', emissiveMap: t, emissiveIntensity: .05 }), 17.7 + i * .104, TOP + .012 + .003 + (i % 2) * .001, -8.84, 0, (i - 2.5) * .05);
      sw.userData.stitch = stitch;
    });
    // 3. coconut shell to button: raw shell pieces, blanks, finished buttons, buttons sewn on a knit swatch
    box(walnut, 16.93, TOP, -8.15, .44, .014, .13);
    for (const dx of [-.11, 0, .11]) box(walnut, 16.93 + dx, TOP + .014, -8.15, .006, .016, .12);
    const hole = std('lib_hole', { color: '#1d130c', roughness: 1 }), shellOut = std('lib_shell_out', { color: '#4a2f1c', roughness: .55 }), shellIn = std('lib_shell_in', { color: '#a68a63', roughness: .8 }), blankMat = std('lib_blank', { color: '#b8956a', roughness: .6 }), buttonMat = std('lib_button', { color: '#4f3422', roughness: .32 });
    for (let k = 0; k < 3; k++) { const s = mesh(g, new THREE.SphereGeometry(.03, 16, 8, 0, 1.6, 0, 1.1), shellOut, 16.765 + (k - 1) * .022, TOP + .02, -8.15 + (k - 1) * .03, -.4, k * 1.9, .3); s.scale.set(1, .6, 1);
      const s2 = mesh(g, new THREE.SphereGeometry(.0295, 16, 8, 0, 1.6, 0, 1.1), shellIn, s.position.x, s.position.y, s.position.z, -.4, k * 1.9, .3); s2.scale.set(1, .6, 1); s2.material.side = THREE.BackSide; }
    const r = rng(141);
    for (let k = 0; k < 9; k++) mesh(g, new THREE.CylinderGeometry(.011, .011, .003, 18), blankMat, 16.875 + (k % 3) * .027 - .027, TOP + .016 + Math.floor(k / 3) * .0005, -8.18 + Math.floor(k / 3) * .03, (r() - .5) * .2, 0, (r() - .5) * .2);
    for (let k = 0; k < 9; k++) { const bx = 16.985 + (k % 3) * .027 - .027, bz = -8.18 + Math.floor(k / 3) * .03;
      mesh(g, new THREE.CylinderGeometry(.0105, .0105, .0035, 20), buttonMat, bx, TOP + .016, bz);
      for (const [hx, hz] of [[-.0025, -.0025], [.0025, -.0025], [-.0025, .0025], [.0025, .0025]]) mesh(g, new THREE.CircleGeometry(.0011, 8), hole, bx + hx, TOP + .0179, bz + hz, -Math.PI / 2); }
    const knitPatch = texture(knitTile('jersey'), { srgb: false, repeat: [4, 4] });
    box(std('lib_patch', { color: PAL.indigo, map: knitPatch, roughness: .96 }), 17.095, TOP + .014, -8.15, .1, .004, .1);
    for (let k = 0; k < 3; k++) mesh(g, new THREE.CylinderGeometry(.0095, .0095, .003, 20), buttonMat, 17.095, TOP + .0195, -8.18 + k * .03);
    // a small concept card: what each sample will carry once suppliers provide it
    const card = (() => { const c = canvas(512, 300), x = c.getContext('2d'); x.fillStyle = '#f4f0e8'; x.fillRect(0, 0, 512, 300); x.fillStyle = '#26302b';
      x.font = '700 34px Inter, Arial, sans-serif'; x.fillText('Materials library', 28, 58); x.font = '400 22px Inter, Arial, sans-serif'; x.fillStyle = '#4b5a52';
      ['Yarn · stitch · coconut-shell buttons', 'Each sample: fibre, origin, weight,', 'wash and test reports.', 'Concept display: supplier data pending.'].forEach((s, i) => x.fillText(s, 28, 108 + i * 40));
      const t = texture(c, { clamp: true }); return std('lib_card', { map: t, roughness: .88, emissive: '#ffffff', emissiveMap: t, emissiveIntensity: .3 }); })();
    box(oak, 17.36, TOP, -8.84, .03, .018, .17);
    const cm = mesh(g, new THREE.PlaneGeometry(.17, .1), card, 17.36, TOP + .018 + .05 * Math.cos(.15), -8.84); cm.rotation.set(-.15, -Math.PI / 2, 0, 'YXZ');
  }
  // ceiling-hung items join the model's overhead group (the app hides it with the ceiling in the dollhouse views)
  const overhead = new THREE.Group(); overhead.name = 'INTERIOR_DESIGN_OVERHEAD';
  if (want('EC_TEXTILE_BAFFLES')) {
    // deck underside y 2.90; beams with track rails at z -9.05 / -7.31 (spots reach z -9.24 / -7.14): fins span z -8.85..-7.60,
    // hang to y 2.49, skip the AC unit (x 15.05-16.24) and the smoke detector (x 15.59-15.71)
    const W = px(256), H = px(1024), c = canvas(W * 3, H), x = c.getContext('2d'), m = H / 1.25;
    [[PAL.khadi, PAL.indigo, 201], ['#cdbb94', PAL.madder, 202], [PAL.jute, PAL.indigo, 203]].forEach(([base, band, seed], k) => {
      // the cloth hangs with its long side along z: the woven bands sit near the hem (canvas left = fin bottom)
      cloth(x, k * W, 0, W, H, base, { cell: 3, seed, slub: .14 });
      for (const [f, wdt, col] of [[.10, .07, band], [.20, .015, PAL.madder], [.235, .015, band]]) cloth(x, k * W + W * f, 0, W * wdt, H, col, { cell: 3, seed: seed + f * 100 });
    });
    const atlas = texture(c, { clamp: true });
    const fins = std('baffle_cloth', { map: atlas, roughness: .95, side: THREE.DoubleSide, emissive: '#ffffff', emissiveMap: atlas, emissiveIntensity: .12 });
    const oak = std('baffle_oak', { color: PAL.oak, roughness: .55 });
    const xs = [10.1, 10.7, 11.3, 11.9, 12.5, 13.1, 13.7, 14.3, 16.7, 17.3, 17.9, 18.5, 19.1, 19.7, 20.3, 20.9, 21.5];
    xs.forEach((fx, i) => {
      const k = i % 3, geom = new THREE.PlaneGeometry(1.25, .38, 12, 2), uv = geom.attributes.uv, p = geom.attributes.position;
      for (let v = 0; v < uv.count; v++) {         // canvas column k: u across the fin height (hem at canvas left), v along z
        const along = uv.getX(v), up = uv.getY(v); uv.setXY(v, (k + up * .999) / 3, along);
        p.setZ(v, .012 * Math.sin(along * Math.PI * 3 + i) * (1 - up));   // a soft ripple at the hem
      }
      geom.computeVertexNormals();
      const fin = mesh(overhead, geom, fins, fx, 2.87 - .19, -8.225, 0, Math.PI / 2);
      fin.userData.interiorItem = 'EC_TEXTILE_BAFFLES';
      mesh(overhead, new THREE.BoxGeometry(.024, .03, 1.27), oak, fx, 2.885, -8.225);
    });
  }
  if (want('EC_GALLERY_LIGHT')) {
    const pool = (() => { const c = canvas(256, 256), x = c.getContext('2d'); x.fillStyle = '#000'; x.fillRect(0, 0, 256, 256);
      const g = x.createRadialGradient(128, 128, 6, 128, 128, 126); g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(.55, 'rgba(255,255,255,.4)'); g.addColorStop(1, 'rgba(255,255,255,0)'); x.fillStyle = g; x.fillRect(0, 0, 256, 256);
      return texture(c, { clamp: true }); })();
    const warm = (op, name) => std(name, { color: '#000000', emissive: '#ffc488', emissiveMap: pool, transparent: true, opacity: op, depthWrite: false, blending: THREE.AdditiveBlending, roughness: 1, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 });
    const plinthPool = warm(.3, 'pool_plinth'), tablePool = warm(.22, 'pool_table');
    for (const fx of [11.635, 12.345, 13.055, 13.765]) mesh(group, new THREE.PlaneGeometry(.78, .6), plinthPool, fx, .2015, -8.56, -Math.PI / 2);   // plinth top y 0.20
    mesh(group, new THREE.PlaneGeometry(3.3, .86), tablePool, 18.33, .8636, -8.5, -Math.PI / 2);                                               // table top y 0.863
  }
  // the approved rug keeps its baked Cycles light; only the woven design (albedo) changes when the Reception atlas is live
  function prepareRoom(room) {
    if (room.id !== 'Z02' || !rugTexture) return;
    for (const root of room.groups) root.traverse(o => {
      if (!o.isMesh) return;
      for (const material of Array.isArray(o.material) ? o.material : [o.material]) {
        if ((material.userData.sourceMaterial || material.name) !== 'rug_wool' || material.userData.interiorRug) continue;
        material.map = rugTexture; material.color.set('#ffffff'); if ('sheenColor' in material) material.sheenColor?.set('#3a3226');
        material.userData.interiorRug = true; material.needsUpdate = true;
      }
    });
  }
  return {
    group, overhead, items: items.map(i => ({ id: i.id, zone: i.zone, note: i.note })), prepareRoom,
    stats: { items: items.length, meshes: geometries.length, textures: textures.length, detail },
    textures: () => textures,
    dispose() { geometries.forEach(g => g.dispose()); materials.forEach(m => m.dispose()); textures.forEach(t => t.dispose()); },
  };
}
