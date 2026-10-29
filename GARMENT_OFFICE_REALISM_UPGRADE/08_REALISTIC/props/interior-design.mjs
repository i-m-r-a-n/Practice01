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
  { id: 'MD_RUG_SOFTS', zone: 'Z12', note: 'MD lounge: the approved rug redesigned as an indigo kantha weave (same footprint); stitched cushions on the sofa and armchair.' },
  { id: 'MD_KANTHA_PANEL', zone: 'Z12', note: 'A framed nakshi-kantha-inspired panel on the free east wall behind the desk, under a brass picture light (design reference).' },
  { id: 'BR_KANTHA_PANEL', zone: 'Z08', note: 'A tall kantha-inspired panel on the free wall between the reception glass and the executive-suite door, under a picture light (design reference).' },
  { id: 'BR_DESK_PADS', zone: 'Z08', note: 'Khadi desk pads with a kantha running-stitch edge and a stitched leaf at the eight places with a notebook and a glass, clear of the cable channel.' },
  { id: 'BR_TABLE_LIGHT', zone: 'Z08', note: 'Warm pool of the existing linear pendants along the boardroom table.' },
  { id: 'LB_BRAND_LIGHT', zone: 'Z01', note: 'Warm scallops of the three existing track spots on the oak slats of the brand wall, which falls off softly towards the floor; the white logo panel and the logos keep their look.' },
  { id: 'LB_WOVEN_PIER', zone: 'Z01', note: 'One narrow handloom hanging (khadi with sparse Jamdani-style butis and indigo selvedge stripes) on the blank pier between the two windows, on the way to the Reception door. Design reference; maker to be identified.' },
  { id: 'LB_WOOD_WARMTH', zone: 'Z01', note: 'The walnut of the check-in desk and the oak of the two north doors read warmer (lobby only, same textures).' },
  { id: 'MR_FIT_FORMS', zone: 'Z07', note: 'The two dress forms dressed for fit development: a calico toile with marker-traced style lines and pinned princess seams, and a knitted body sample in indigo jersey with a cable panel (illustrative, not an actual collection).' },
  { id: 'MR_APPROVAL_BOARD', zone: 'Z07', note: 'The approved approval board with the same swatch layout and colours, shown as pinned cloth with garment flats on its sheets.' },
  { id: 'CAD_SCREENS', zone: 'Z14', note: 'The six CAD monitors and the wall screen show one illustrative development exercise for a knit cardigan: technical flats, pattern pieces, a grading nest, a marker and a stitch chart. Self-drawn, generic graphics: no software interface, buyer or measurements.' },
  { id: 'CAD_PINBOARD', zone: 'Z14', note: 'The tech-pack pinboard keeps its sheet positions, ordered left to right from sketch to flats, pattern, marker, fit notes and approval, with knit swatches and a coconut-shell button card.' },
  { id: 'CAD_LAYOUT_TABLE', zone: 'Z14', note: 'A pattern marker on the layout table with an L-square, pattern weights and a pencil, and a small folded knit reference set; the east third of the table stays clear.' },
  { id: 'DS_DAYLIGHT', zone: 'Z18', note: 'Overcast daylight in the three existing east windows and its soft spill on the floor; true north, sun angles and glare are still to be measured on site.' },
  { id: 'DS_FABRIC_BOARD', zone: 'Z18', note: 'The approved mood board with the same swatch layout and colours, shown as pinned cloth (pinked edges, pins, weave and knit, Jamdani-style butis on the whites) and garment flats on its paper sheets, lit by the scallops of its five existing track spots.' },
  { id: 'DS_REVIEW_TABLE', zone: 'Z18', note: 'A sample-review set on the presentation table for teaching and fit reviews: a knit sample laid flat, drafted pattern pieces, swatch header cards, a tape measure, a sketchbook of garment flats and a card of coconut-shell buttons (illustrative, not an actual collection).' },
];

const PAL = { khadi: '#e6dccb', khadiShade: '#cfc1a8', jute: '#b39867', juteDark: '#7e6440', indigo: '#33486a', indigoDeep: '#24344f',
  madder: '#8f4a3a', ochre: '#b98a45', thread: '#efe7d6', oak: '#b88e5f', brass: '#a57c3c' };

export function buildInteriorDesign(THREE, { zones = null, exclude = [], anisotropy = 4, detail = 1 } = {}) {
  const group = new THREE.Group(); group.name = 'INTERIOR_DESIGN';
  const geometries = [], materials = [], textures = [];
  const items = INTERIOR_ITEMS.filter(i => (!zones || zones.includes(i.zone)) && !exclude.includes(i.id));
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
  // linear base colours of the model's swatch materials (and the board's linen), as canvas sRGB
  const LIN = { o: [.109, .127, .063], g: [.028, .147, .06], s: [.27, .376, .275], a: [.578, .462, .301], h: [.323, .323, .314], k: [.012, .012, .013],
    p: [.913, .896, .855], b: [.694, .456, .381], w: [.839, .823, .776], d: [.047, .091, .171], n: [.019, .032, .068], r: [.323, .082, .037], linen: [.768, .73, .651] };
  const srgb = l => '#' + l.map(v => Math.round(255 * (v <= .0031308 ? v * 12.92 : 1.055 * Math.pow(v, 1 / 2.4) - .055)).toString(16).padStart(2, '0')).join('');
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
  // a kantha-stitched handloom rug drawn at true size (Wm x Hm metres): binding, a dyed border band with running-stitch rows
  // and waves, a thin accent line, a field of stitched crosses, a lotus at the centre and leaf butis in the corners
  function kanthaRug(Wm, Hm, P, seed = 21) {
    const W = px(2048), H = Math.round(W * Hm / Wm), c = canvas(W, H), x = c.getContext('2d'), m = W / Wm;   // pixels per metre
    const fine = Math.max(1.6, m * .0024), thin = Math.max(1.4, m * .002);
    cloth(x, 0, 0, W, H, P.ground, { cell: Math.max(3, Math.round(m * .006)), seed, slub: .16, mottle: .07, contrast: .8 });
    const band = (d0, d1, color, sd) => { const a = d0 * m, b = d1 * m; x.save(); x.beginPath(); x.rect(a, a, W - 2 * a, H - 2 * a); x.rect(b, H - b, W - 2 * b, -(H - 2 * b)); x.clip('evenodd'); cloth(x, 0, 0, W, H, color, { cell: Math.max(3, Math.round(m * .005)), seed: sd, slub: .08, mottle: .05, contrast: .6 }); x.restore(); };
    band(0, .035, P.binding, seed + 1); band(.07, .23, P.band, seed + 2); band(.255, .272, P.line, seed + 3);
    const inset = d => rect(d * m, d * m, W - d * m, H - d * m);
    stitch(x, inset(.095), { color: P.thread, dash: m * .008, gap: m * .006, width: fine, seed: seed + 10 });
    stitch(x, inset(.205), { color: P.thread, dash: m * .008, gap: m * .006, width: fine, seed: seed + 11 });
    for (const [y, sg] of [[.15, 1], [Hm - .15, -1]]) stitch(x, wave(.15 * m, W - .15 * m, y * m, m * .018 * sg, m * .09, 260), { color: P.wave, dash: m * .007, gap: m * .005, width: fine, seed: seed + 12 + sg });
    for (const [xx, sg] of [[.15, 1], [Wm - .15, -1]]) { const pts = wave(.15 * m, H - .15 * m, 0, m * .018 * sg, m * .09, 200).map(([a, b]) => [xx * m + b, a]); stitch(x, pts, { color: P.wave, dash: m * .007, gap: m * .005, width: fine, seed: seed + 15 + sg }); }
    stitch(x, inset(.31), { color: P.accent, dash: m * .007, gap: m * .006, width: thin, seed: seed + 17 });
    for (let gx = .5; gx < Wm - .45; gx += .2) for (let gy = .5; gy < Hm - .45; gy += .2) {
      if (Math.hypot(gx - Wm / 2, (gy - Hm / 2) * 1.1) < .52) continue;
      const cx = gx * m, cy = gy * m, d = m * .018;
      stitch(x, line(cx - d, cy, cx + d, cy), { color: P.cross, dash: m * .006, gap: m * .004, width: thin, seed: gx * 97 + gy });
      stitch(x, line(cx, cy - d, cx, cy + d), { color: P.cross, dash: m * .006, gap: m * .004, width: thin, seed: gx * 31 + gy * 7 });
    }
    x.fillStyle = P.disc; x.beginPath(); x.arc(W / 2, H / 2, m * .1, 0, Math.PI * 2); x.fill();
    lotus(x, W / 2, H / 2, m * .42, P.lotus, seed + 20, m * .008);
    for (const [cx, cy] of [[.52, .52], [Wm - .52, .52], [.52, Hm - .52], [Wm - .52, Hm - .52]]) buti(x, LEAF, cx * m, cy * m, m * .016, P.leaf);
    return c;
  }
  const RECEPTION_RUG = { ground: PAL.jute, binding: PAL.juteDark, band: PAL.indigo, line: PAL.madder, thread: PAL.thread, wave: PAL.khadi, accent: PAL.ochre,
    cross: 'rgba(240,229,205,.75)', disc: PAL.indigo, lotus: [PAL.thread, PAL.madder, PAL.indigoDeep], leaf: { 1: PAL.indigo, 2: PAL.madder } };
  let rugCanvas = null;
  if (want('RC_RUG_KANTHA')) {
    // rug F013: 2.74 x 1.98 m (x 8.28-11.02, z 3.96-5.94); its UV0 is metric (u -1.37..1.37, v 0.011..1.989) -> normalised below
    rugCanvas = kanthaRug(2.74, 1.978, RECEPTION_RUG, 21);
    rugTexture = texture(rugCanvas, { clamp: true });
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
  // the visible light of a track spot on the wall below it (a scallop): rounded top under the fitting, soft long fall-off.
  // Intensity in the RGB of an opaque canvas; one texture shared by every scallop material.
  let scallopTex = null;
  function scallopMaterial(name, opacity) {
    if (!scallopTex) {
      const W = 256, H = 512, c = canvas(W, H), x = c.getContext('2d'), img = x.createImageData(W, H);
      for (let j = 0; j < H; j++) for (let i = 0; i < W; i++) {
        const X = i / (W - 1) * 2 - 1, Y = j / (H - 1), top = .03 + .3 * X * X;
        const v = Math.min(1, Math.max(0, (Y - top) / .06)) * Math.exp(-Math.pow((Y - .2) / .42, 2)) * Math.pow(Math.max(0, 1 - X * X), 1.6);
        const k = (j * W + i) * 4; img.data[k] = img.data[k + 1] = img.data[k + 2] = Math.round(255 * v); img.data[k + 3] = 255;
      }
      x.putImageData(img, 0, 0); scallopTex = texture(c, { clamp: true });
    }
    return std(name, { color: '#000000', emissive: '#ffc488', emissiveMap: scallopTex, transparent: true, opacity, depthWrite: false, blending: THREE.AdditiveBlending, roughness: 1, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 });
  }
  if (want('RC_SCALLOPS')) {
    // track spots LT008-LT011 (x 13.80-13.95, y 2.60-2.81) at z 2.41 / 3.43 / 4.445 / 5.46 light the fluted oak face x 14.27
    const scallop = scallopMaterial('scallop', .32);
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
  // a framed textile panel on a wall: canvas art, slim frame, brass picture light and the warm pool it throws.
  // (cx, cy, cz): centre of the cloth face; yaw turns the face (local +z) towards the room
  function wallPanel(id, zone, W, H, cx, cy, cz, yaw, draw, frameColor) {
    const g = new THREE.Group(); g.name = id; g.position.set(cx, cy, cz); g.rotation.y = yaw; group.add(g);
    const c = canvas(px(Math.round(1400 * W / Math.max(W, H))), px(Math.round(1400 * H / Math.max(W, H)))), x = c.getContext('2d'); draw(x, c.width, c.height);
    const t = texture(c, { clamp: true });
    mesh(g, new THREE.BoxGeometry(W + .06, H + .06, .024), std(id + '_frame', { color: frameColor, roughness: .5 }), 0, 0, -.013);
    mesh(g, new THREE.PlaneGeometry(W, H), std(id + '_cloth', { map: t, normalMap: weaveNormal, normalScale: new THREE.Vector2(.3, .3), roughness: .95, emissive: '#ffffff', emissiveMap: t, emissiveIntensity: .12 }), 0, 0, .001);
    const brass = std(id + '_brass', { color: PAL.brass, roughness: .3, metalness: .85 }), led = std(id + '_led', { color: '#000000', emissive: '#ffd6a6', emissiveIntensity: 2.4 });
    mesh(g, new THREE.CylinderGeometry(.013, .013, Math.min(.9, W * .6), 18), brass, 0, H / 2 + .1, .13, 0, 0, Math.PI / 2);
    mesh(g, new THREE.PlaneGeometry(Math.min(.86, W * .58), .012), led, 0, H / 2 + .0865, .13, Math.PI / 2);
    for (const s of [-1, 1]) mesh(g, new THREE.CylinderGeometry(.006, .006, .13, 8), brass, s * Math.min(.3, W * .2), H / 2 + .1, .065, Math.PI / 2);
    mesh(g, new THREE.PlaneGeometry(W + .5, H * .9 + .3), glowMaterial(id + '_pool', W + .5, H, 'pool', '#f4b47a', .2), 0, H * .1, .004);
    g.userData = { interiorItem: id, zone };
    return g;
  }
  // nakshi-kantha-inspired composition: dense running-stitch ripples, a lotus medallion, kalka (leaf) corners, a wave border
  function kanthaArt(x, w, h, P, seed) {
    cloth(x, 0, 0, w, h, P.ground, { cell: 3, seed, slub: .12 });
    const m = Math.min(w, h);
    for (let y = m * .06; y < h - m * .06; y += m * .022) stitch(x, wave(m * .06, w - m * .06, y, m * .004, m * .3, 80), { color: P.ripple, dash: m * .012, gap: m * .008, width: Math.max(1.6, m * .003), seed: seed + y });
    stitch(x, rect(m * .035, m * .035, w - m * .035, h - m * .035), { color: P.border, dash: m * .012, gap: m * .007, width: Math.max(2, m * .005), seed: seed + 1 });
    for (const yy of [m * .055, h - m * .055]) stitch(x, wave(m * .06, w - m * .06, yy, m * .01, m * .06, 160), { color: P.border, dash: m * .01, gap: m * .006, width: Math.max(2, m * .004), seed: seed + yy });
    x.fillStyle = P.disc; x.beginPath(); x.arc(w / 2, h / 2, m * .12, 0, Math.PI * 2); x.fill();
    lotus(x, w / 2, h / 2, m * .3, P.lotus, seed + 3, m * .014);
    for (const [cx, cy] of [[.16, .18], [.84, .18], [.16, .82], [.84, .82]]) buti(x, LEAF, w * cx, h * cy, m * .02, P.leaf);
  }
  if (want('MD_KANTHA_PANEL')) {
    // MD east wall (room face x 27.64) is free between the planter (z < 2.29) and the credenza (z > 5.74); the desk ends at x 27.23
    wallPanel('MD_KANTHA_PANEL', 'Z12', 1.6, .9, 27.64 - .014, 1.62, 3.85, -Math.PI / 2, (x, w, h) => kanthaArt(x, w, h,
      { ground: PAL.khadi, ripple: 'rgba(51,72,106,.55)', border: PAL.madder, disc: PAL.indigo, lotus: [PAL.thread, PAL.ochre, PAL.madder], leaf: { 1: PAL.indigo, 2: PAL.madder } }, 301), '#5a3d27');
  }
  if (want('BR_KANTHA_PANEL')) {
    // boardroom south wall (room face z -0.25): free between the reception glass (x < 14.35) and the walnut door D20 (x > 15.71)
    wallPanel('BR_KANTHA_PANEL', 'Z08', 1.0, 1.25, 15.03, 1.58, -.25 - .014, Math.PI, (x, w, h) => kanthaArt(x, w, h,
      { ground: PAL.indigo, ripple: 'rgba(236,228,210,.45)', border: PAL.ochre, disc: PAL.indigoDeep, lotus: [PAL.thread, PAL.ochre, PAL.thread], leaf: { 1: PAL.ochre, 2: PAL.khadi } }, 311), PAL.oak);
  }
  if (want('BR_DESK_PADS')) {
    // walnut table F031 (top y 0.749, z -3.442..-2.248, round ends from x 14.69 / 19.60): the eight places with a notebook and a
    // glass (notebooks x 15.01 / 16.23 / 17.86 / 19.08 + 0.2, z -2.56..-2.32 and -3.37..-3.13). Each gets a khadi desk pad with a
    // kantha running-stitch edge, clear of the cable channel (z -2.908..-2.781) and 2 cm inside the table edge
    const W = px(512), H = Math.round(W * .3 / .5), c = canvas(W, H), x = c.getContext('2d'), m = W / .5;
    cloth(x, 0, 0, W, H, PAL.khadi, { cell: 2.5, seed: 321, slub: .12 });
    x.strokeStyle = 'rgba(80,60,35,.35)'; x.lineWidth = 2; x.strokeRect(1, 1, W - 2, H - 2);
    for (const [d, col] of [[.018, PAL.indigo], [.03, PAL.indigo], [.042, PAL.madder]]) stitch(x, rect(d * m, d * m, W - d * m, H - d * m), { color: col, dash: m * .008, gap: m * .005, width: Math.max(1.6, m * .0035), seed: 322 + d * 1000 });
    buti(x, LEAF, W - .075 * m, H - .075 * m, m * .006, { 1: PAL.indigo, 2: PAL.madder });
    const pad = std('board_pad', { map: texture(c, { clamp: true }), normalMap: weaveNormal, normalScale: new THREE.Vector2(.25, .25), roughness: .95, polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -1 });
    for (const px0 of [15.245, 16.465, 18.09, 19.31]) for (const [pz, yaw] of [[-2.42, 0], [-3.27, Math.PI]]) {   // the stitched leaf sits at each sitter's right hand
      mesh(group, new THREE.PlaneGeometry(.5, .3), pad, px0, .7505, pz, -Math.PI / 2, 0, yaw).userData.interiorItem = 'BR_DESK_PADS';
    }
  }
  if (want('BR_TABLE_LIGHT')) {
    // walnut table F031: x 14.10-20.19, z -3.44..-2.25, top y 0.75; its centre line carries the trays, jug and phone (they occlude the pool)
    const c = canvas(512, 128), x = c.getContext('2d'); x.fillStyle = '#000'; x.fillRect(0, 0, 512, 128);
    const g2 = x.createRadialGradient(256, 64, 4, 256, 64, 250); g2.addColorStop(0, '#fff'); g2.addColorStop(.6, 'rgba(255,255,255,.5)'); g2.addColorStop(1, 'rgba(255,255,255,0)');
    x.setTransform(1, 0, 0, .3, 0, 44.8); x.fillStyle = g2; x.fillRect(0, 0, 512, 427); x.setTransform(1, 0, 0, 1, 0, 0);
    const pool = std('board_pool', { color: '#000000', emissive: '#ffc488', emissiveMap: texture(c, { clamp: true }), transparent: true, opacity: .34, depthWrite: false, blending: THREE.AdditiveBlending, roughness: 1, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 });
    mesh(group, new THREE.PlaneGeometry(5.9, 1.1), pool, 17.145, .7515, -2.845, -Math.PI / 2);
  }
  if (want('MD_RUG_SOFTS')) {
    // sofa F068 faces east: back cushions' face x ~22.25, seat top 0.444 over z 3.35-4.75; armchair F070 faces west: back face x ~24.42
    const S = px(512), c = canvas(S * 2, S), x = c.getContext('2d'), m = S / .45;
    x.save(); x.beginPath(); x.rect(0, 0, S, S); x.clip(); cloth(x, 0, 0, S, S, PAL.ochre, { cell: 4, seed: 401 });
    for (let i = 0; i < 7; i++) for (let k = 0; k < 2; k++) stitch(x, wave(14, S - 14, S * (.1 + i * .133) + k * S * .02, m * .008, m * .07, 60), { color: i % 2 ? PAL.indigo : PAL.thread, dash: m * .009, gap: m * .005, width: 3.2, seed: 402 + i * 2 + k }); x.restore();
    x.save(); x.beginPath(); x.rect(S, 0, S, S); x.clip(); cloth(x, S, 0, S, S, PAL.indigo, { cell: 4, seed: 403 });
    lotus(x, S * 1.5, S / 2, S * .3, [PAL.thread, PAL.ochre, PAL.thread], 404, m * .008); x.restore();
    const atlas = texture(c, { clamp: true }), half = k => { const t = atlas.clone(); t.repeat.set(.5, 1); t.offset.set(k * .5, 0); t.needsUpdate = true; textures.push(t); return t; };
    const soft = k => std('md_cushion_' + k, { map: half(k), normalMap: weaveNormal, normalScale: new THREE.Vector2(.4, .4), roughness: .95, emissive: '#ffffff', emissiveMap: half(k), emissiveIntensity: .06 });
    const g = new THREE.Group(); g.name = 'MD_SOFTS'; group.add(g);
    const pillow = (mat, w, h, t, px2, py, pz, yaw, tilt) => { const p = mesh(g, pillowGeometry(w, h, t), mat); p.position.set(px2, py, pz); p.rotation.set(tilt, yaw, 0, 'YXZ'); return p; };
    pillow(soft(0), .42, .42, .15, 22.345, .65, 3.6, Math.PI / 2 + .25, -.2);
    pillow(soft(1), .42, .42, .15, 22.345, .65, 4.5, Math.PI / 2 - .25, -.2);
    pillow(soft(1), .42, .28, .13, 24.335, .63, 4.06, -Math.PI / 2, -.22);
  }
  // world-projected rug designs for approved rugs drawn by the shared base material (MD rug; Reception rug before its atlas)
  const rugBoxes = [];
  if (want('MD_RUG_SOFTS')) rugBoxes.push({ box: [22.10, 3.15, 24.54, 4.98], canvas: kanthaRug(2.44, 1.83, { ground: PAL.indigo, binding: PAL.indigoDeep, band: PAL.khadi, line: PAL.madder,
    thread: PAL.indigo, wave: PAL.madder, accent: PAL.ochre, cross: 'rgba(236,228,210,.5)', disc: PAL.khadi, lotus: [PAL.indigo, PAL.madder, PAL.thread], leaf: { 1: PAL.khadi, 2: PAL.ochre } }, 501) });
  if (rugCanvas) rugBoxes.push({ box: [8.28, 3.96, 11.02, 5.94], canvas: rugCanvas });
  const rugMaps = rugBoxes.map(r => texture(r.canvas, { clamp: true }));
  // Entrance lobby (Z01): light and wood of the arrival view, applied by position to shared model materials, so the same
  // materials elsewhere keep their look. Each patch: material name pattern, world box [x0, y0, z0, x1, y1, z1], GLSL using p.
  const placePatches = [];
  if (want('LB_BRAND_LIGHT')) placePatches.push({ id: 'LB_BRAND_LIGHT', names: /^oak_slat(_baked)?$/, box: [4.25, -.01, -.03, 7.55, 2.76, .09],
    // track spots LT003-LT005 (x 4.83 / 5.89 / 6.96, y 2.63-2.81, z 0.86-1.03) light the slat faces (z 0.07) in soft scallops;
    // the gaps (plinth) stay dark, so the relief reads; the wall falls off a little towards the floor
    glsl: `float lobbyLight = 0.0;
      for (int i = 0; i < 3; i++) { float sx = i == 0 ? 4.83 : (i == 1 ? 5.89 : 6.96);
        float X = (p.x - sx) / .62, Y = (2.66 - p.y) / 2.3, top = .03 + .28 * X * X;
        float d = (Y - .24) / .44;   // squared by hand: pow() of a negative base is undefined in GLSL
        lobbyLight += clamp((Y - top) / .07, 0.0, 1.0) * exp(-d * d) * pow(max(0.0, 1.0 - X * X), 1.6); }
      diffuseColor.rgb *= (1.0 + vec3(.78, .58, .36) * min(lobbyLight, 1.2)) * mix(.84, 1.0, smoothstep(.15, 1.5, p.y));` });
  if (want('LB_WOOD_WARMTH')) for (const [names, box, tint] of [[/^walnut(_baked)?$/, [5.15, .55, 2.68, 6.5, .82, 3.42], '1.22, 1.06, .86'], [/^oak(_baked)?$/, [1.5, -.01, -.32, 4.05, 2.2, .06], '1.12, 1.03, .9']])
    placePatches.push({ id: 'LB_WOOD_WARMTH', names, box, glsl: `diffuseColor.rgb *= vec3(${tint});` });   // check-in desk top; north doors D02 / D17
  function patchPlaces(root) {
    const touched = [];
    root.traverse(o => {
      if (!o.isMesh) return;
      for (const material of [o.material].flat()) {
        const mine = placePatches.filter(q => q.names.test(material.userData.sourceMaterial || material.name));
        if (!mine.length || material.userData.interiorPlaces || material.userData.cyclesLightmap) continue;
        material.userData.interiorPlaces = true; touched.push(material.name);
        const previous = material.onBeforeCompile, previousKey = material.customProgramCacheKey?.bind(material);
        material.onBeforeCompile = (shader, r) => {
          previous?.call(material, shader, r);
          shader.vertexShader = 'varying vec3 vPlaceWorld;\n' + shader.vertexShader.replace('#include <project_vertex>', '#include <project_vertex>\nvPlaceWorld = (modelMatrix * vec4(transformed, 1.0)).xyz;');
          shader.fragmentShader = 'varying vec3 vPlaceWorld;\n' + shader.fragmentShader.replace('#include <color_fragment>', '#include <color_fragment>\n{ vec3 p = vPlaceWorld;\n' +
            mine.map(q => `if (all(greaterThan(p, vec3(${q.box.slice(0, 3).map(v => v.toFixed(3)).join(', ')}))) && all(lessThan(p, vec3(${q.box.slice(3).map(v => v.toFixed(3)).join(', ')})))) { ${q.glsl} }`).join('\n') + '\n}');
        };
        const key = '|places-v2-' + mine.map(q => q.id + ':' + q.box.join(',')).join('+');   // the boxes live in the closure, so they must be in the key
        material.customProgramCacheKey = () => (previousKey ? previousKey() : '') + key;
        material.needsUpdate = true;
      }
    });
    return touched;
  }
  function prepareBase(root) {
    const places = placePatches.length ? patchPlaces(root) : [];
    if (!rugBoxes.length) return places;
    const touched = [...places];
    root.traverse(o => {
      if (!o.isMesh) return;
      for (const material of [o.material].flat()) {
        if (material.name !== 'rug_wool' || material.userData.cyclesLightmap || material.userData.interiorRugs) continue;
        material.userData.interiorRugs = true; touched.push(material.name);
        const previous = material.onBeforeCompile;
        material.onBeforeCompile = (shader, r) => {
          previous?.call(material, shader, r);
          rugMaps.forEach((t, i) => { shader.uniforms['interiorRug' + i] = { value: t }; shader.uniforms['interiorRugBox' + i] = { value: new THREE.Vector4(...rugBoxes[i].box) }; });
          shader.vertexShader = 'varying vec3 vInteriorWorld;\n' + shader.vertexShader.replace('#include <project_vertex>', '#include <project_vertex>\nvInteriorWorld = (modelMatrix * vec4(transformed, 1.0)).xyz;');
          shader.fragmentShader = 'varying vec3 vInteriorWorld;\n' + rugMaps.map((_, i) => `uniform sampler2D interiorRug${i}; uniform vec4 interiorRugBox${i};\n`).join('') +
            shader.fragmentShader.replace('#include <map_fragment>', '#include <map_fragment>\n' + rugMaps.map((_, i) =>
              `if (vInteriorWorld.x > interiorRugBox${i}.x && vInteriorWorld.x < interiorRugBox${i}.z && vInteriorWorld.z > interiorRugBox${i}.y && vInteriorWorld.z < interiorRugBox${i}.w)
                 diffuseColor.rgb = texture2D(interiorRug${i}, vec2((vInteriorWorld.x - interiorRugBox${i}.x) / (interiorRugBox${i}.z - interiorRugBox${i}.x), 1.0 - (vInteriorWorld.z - interiorRugBox${i}.y) / (interiorRugBox${i}.w - interiorRugBox${i}.y))).rgb;`).join('\n'));
        };
        material.customProgramCacheKey = () => 'interior-rugs-v1-' + rugMaps.length;
        material.needsUpdate = true;
      }
    });
    return touched;
  }
  if (want('DS_DAYLIGHT')) {
    // east windows W08 / W09 / W10 (glass x 33.81, sill y 0.76, head 2.13; roller blinds cover y 1.57-2.18 inside): an overcast
    // sky just outside each, and a soft spill on the floor fading 2 m into the room. No sun patches: orientation is not measured.
    const sky = (() => { const c = canvas(64, 256), x = c.getContext('2d'), g = x.createLinearGradient(0, 0, 0, 256);
      g.addColorStop(0, '#f4f7fa'); g.addColorStop(.6, '#e4ebf0'); g.addColorStop(1, '#d6dcd8'); x.fillStyle = g; x.fillRect(0, 0, 64, 256); return texture(c, { clamp: true }); })();
    const skyMat = new THREE.MeshBasicMaterial({ name: 'interior_daylight_sky', map: sky, color: new THREE.Color(1.5, 1.52, 1.56) }); materials.push(skyMat);   // reads as bright overcast after tone mapping
    const spill = (() => { const c = canvas(256, 64), x = c.getContext('2d'); x.fillStyle = '#000'; x.fillRect(0, 0, 256, 64);
      const g = x.createLinearGradient(256, 0, 0, 0); g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(.4, 'rgba(255,255,255,.45)'); g.addColorStop(1, 'rgba(255,255,255,0)'); x.fillStyle = g; x.fillRect(0, 0, 256, 64);   // brightest at the wall
      const e = x.createLinearGradient(0, 0, 0, 64); e.addColorStop(0, 'rgba(0,0,0,1)'); e.addColorStop(.2, 'rgba(0,0,0,0)'); e.addColorStop(.8, 'rgba(0,0,0,0)'); e.addColorStop(1, 'rgba(0,0,0,1)'); x.fillStyle = e; x.fillRect(0, 0, 256, 64);
      return texture(c, { clamp: true }); })();
    const spillMat = std('daylight_spill', { color: '#000000', emissive: '#e9eff5', emissiveMap: spill, transparent: true, opacity: .2, depthWrite: false, blending: THREE.AdditiveBlending, roughness: 1, polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -2 });
    for (const [z0, z1] of [[-29.87, -26.97], [-24.79, -21.89], [-20.40, -17.50]]) {
      const zc = (z0 + z1) / 2, w = z1 - z0;
      mesh(group, new THREE.PlaneGeometry(w + .2, 1.6), skyMat, 34.06, 1.445, zc, 0, -Math.PI / 2);
      mesh(group, new THREE.PlaneGeometry(2.2, w + .8), spillMat, 33.68 - 1.1, .013, zc, -Math.PI / 2);
    }
  }
  // ---------------------------------------------------------------- Entrance lobby (Z01): one woven detail on the route
  if (want('LB_WOVEN_PIER')) {
    // the blank pier of the east wall (face x 7.62, lobby on its -x side) between the interior windows W11 (z 1.52-2.84) and
    // W12 (z 3.45-4.78), on the way to the Reception door D04 (z 0.39-1.56). Top on the window-head line (2.13), hem near the
    // sill line (0.61), 0.15 m / 0.10 m clear of the window frames; an oak rod on two brackets holds it 5 cm off the wall
    // 2.5 cm south of the pier's centre: it hangs 5 cm proud of the wall, so seen from the arrival side it otherwise crowds W11
    const Wd = .36, L = 1.42, top = 2.06, zc = (2.84 + 3.45) / 2 + .025, face = 7.62;
    const W = px(256), H = Math.round(W * L / Wd), c = canvas(W, H), x = c.getContext('2d'), m = W / Wd;
    cloth(x, 0, 0, W, H, PAL.khadi, { cell: 2.5, seed: 901, slub: .14 });
    for (const [u, w] of [[.05, .03], [.1, .012], [.888, .012], [.92, .03]]) cloth(x, W * u, 0, W * w, H * .965, PAL.indigo, { cell: 2.5, seed: 902 + u * 100 });   // selvedge stripes
    for (const [v, col] of [[.86, PAL.madder], [.875, PAL.indigo], [.89, PAL.madder]]) cloth(x, W * .15, H * v, W * .7, H * .006, col, { cell: 2, seed: 905 + v * 100 });
    for (let j = 0; j < 9; j++) for (let i = 0; i < 2; i++) buti(x, BUTI, W * (.35 + i * .3 + (j % 2 ? .15 : 0) - .075), H * (.07 + j * .085), m * .0045, { 1: 'rgba(250,246,236,.95)', 2: PAL.indigo });   // sparse Jamdani-style butis
    fringe(x, 0, H * .965, W, H * .035, PAL.khadiShade, 903);
    const t = texture(c, { clamp: true });
    const cloth3d = std('lobby_hanging', { map: t, normalMap: weaveNormal, normalScale: new THREE.Vector2(.35, .35), roughness: .95, side: THREE.DoubleSide, alphaTest: .4, emissive: '#ffffff', emissiveMap: t, emissiveIntensity: .2 });
    const g = new THREE.Group(); g.name = 'LB_WOVEN_PIER'; group.add(g); g.userData = { interiorItem: 'LB_WOVEN_PIER', zone: 'Z01' };
    const hang = mesh(g, hangingGeometry(Wd, L, 0, 1, 1, 2.5, 904), cloth3d, face - .05, top - L / 2, zc, 0, -Math.PI / 2);
    hang.userData.interiorItem = 'LB_WOVEN_PIER';
    const oak = std('lobby_rod', { color: PAL.oak, roughness: .5 }), brass = std('lobby_brass', { color: PAL.brass, roughness: .3, metalness: .85 });
    mesh(g, new THREE.CylinderGeometry(.011, .011, Wd + .07, 18), oak, face - .05, top + .012, zc, Math.PI / 2);
    for (const s of [-1, 1]) { mesh(g, new THREE.SphereGeometry(.014, 14, 10), brass, face - .05, top + .012, zc + s * (Wd / 2 + .035));
      mesh(g, new THREE.BoxGeometry(.05, .012, .012), brass, face - .025, top + .012, zc + s * (Wd / 2 + .012)); }
  }
  // ---------------------------------------------------------------- CAD / technical design (Z14): one development exercise
  // An illustrative knit cardigan runs through the room: technical flats and pattern work on the screens, a pattern sheet on
  // the layout table, and the pinboard ordered from sketch to approval. Generic, self-drawn graphics: no software interface,
  // buyer, brand or measurement is shown.
  const INK = '#2f3134', LINE = '#3c3d40';
  function devDrawing(x, kind, X, Y, w, h, lw) {          // the drawings shared by screens, pinboard sheets and the table sheet
    const P = (u, v) => [X + u * w, Y + v * h];
    const poly = (pts, close = true, stroke = LINE, width = lw, dash = null, fill = null) => { x.setLineDash(dash || []); x.beginPath(); pts.forEach(([u, v], i) => { const [px0, py0] = P(u, v); i ? x.lineTo(px0, py0) : x.moveTo(px0, py0); }); if (close) x.closePath(); if (fill) { x.fillStyle = fill; x.fill(); } x.strokeStyle = stroke; x.lineWidth = width; x.stroke(); x.setLineDash([]); };
    const front = [[.30, .08], [.14, .14], [.02, .44], [.10, .48], [.20, .30], [.20, .95], [.80, .95], [.80, .30], [.90, .48], [.98, .44], [.86, .14], [.70, .08], [.5, .40]];
    const bodice = [[.06, .06], [.06, .94], [.50, .94], [.52, .40], [.44, .30], [.42, .12], [.40, .04], [.22, .07]];
    const sleeve = Array.from({ length: 13 }, (_, i) => { const t = i / 12; return [.06 + .88 * t, .22 - .2 * Math.sin(t * Math.PI)]; }).concat([[.82, .96], [.18, .96]]);
    const callout = (u, v, r, bu, bv) => { const [cx, cy] = P(u, v); x.strokeStyle = '#b03030'; x.lineWidth = lw; x.beginPath(); x.arc(cx, cy, r * w, 0, Math.PI * 2); x.stroke(); const [bx, by] = P(bu, bv); x.beginPath(); x.moveTo(cx + r * w * Math.sign(bx - cx), cy); x.lineTo(bx, by); x.stroke(); x.strokeStyle = '#8a8d90'; x.lineWidth = Math.max(1, lw * .7); for (let i = 0; i < 2; i++) { x.beginPath(); x.moveTo(bx + (bx > cx ? 4 : -4 - w * .14), by + i * lw * 4); x.lineTo(bx + (bx > cx ? 4 + w * .14 : -4), by + i * lw * 4); x.stroke(); } };
    if (kind === 'flatF' || kind === 'flatB') {
      const box = [.18, .06, .64, .88], q = ([u, v]) => [box[0] + u * box[2], box[1] + v * box[3]];
      poly(front.slice(0, kind === 'flatF' ? 13 : 12).map(q), true, LINE, lw, null, '#fbfbf9');
      if (kind === 'flatB') poly([[.30, .08], [.5, .12], [.70, .08]].map(q), false);
      poly([[.20, .88], [.80, .88]].map(q), false); for (let u = .23; u < .79; u += .025) poly([[u, .88], [u, .95]].map(q), false, LINE, lw * .6);
      if (kind === 'flatF') { poly([[.5, .40], [.5, .95]].map(q), false); for (let i = 0; i < 5; i++) { const [bx, by] = P(...q([.535, .47 + i * .085])); x.beginPath(); x.arc(bx, by, lw * 1.8, 0, Math.PI * 2); x.stroke(); }
        callout(...q([.5, .2]), .05, .9, .14); callout(...q([.535, .55]), .04, .9, .5); callout(...q([.3, .91]), .05, .06, .82); }
      else { poly([[.5, .12], [.5, .95]].map(q), false, LINE, lw * .7, [lw * 3, lw * 2]); callout(...q([.5, .1]), .05, .9, .14); callout(...q([.9, .46]), .04, .92, .62); }
    } else if (kind === 'pattern') {
      x.strokeStyle = 'rgba(70,90,110,.18)'; x.lineWidth = 1; for (let g = 0; g <= 24; g++) { x.beginPath(); x.moveTo(X + g * w / 24, Y); x.lineTo(X + g * w / 24, Y + h); x.stroke(); } for (let g = 0; g <= 14; g++) { x.beginPath(); x.moveTo(X, Y + g * h / 14); x.lineTo(X + w, Y + g * h / 14); x.stroke(); }
      const sub = (pts, bx, by, bw, bh) => pts.map(([u, v]) => [bx + u * bw, by + v * bh]);
      poly(sub(bodice, .04, .08, .30, .84), true, '#2c6fb3', lw * 1.3, null, 'rgba(44,111,179,.06)'); poly(sub(bodice, .36, .08, .30, .84), true);
      poly(sub(sleeve, .68, .10, .28, .80), true);
      for (const [u, v] of sub(bodice, .04, .08, .30, .84)) { const [hx, hy] = P(u, v); x.fillStyle = '#2c6fb3'; x.fillRect(hx - lw * 1.5, hy - lw * 1.5, lw * 3, lw * 3); }
      for (const bx of [.17, .49, .82]) { poly([[bx, .3], [bx, .75]], false, LINE, lw * .8); poly([[bx - .012, .33], [bx, .3], [bx + .012, .33]], false, LINE, lw * .8); poly([[bx - .012, .72], [bx, .75], [bx + .012, .72]], false, LINE, lw * .8); }
    } else if (kind === 'grading') {
      ['#9db7d6', '#7aa0cc', '#4f82bf', '#2c6fb3', '#1f4f86'].forEach((c, i) => { const s = .72 + i * .07; poly(bodice.map(([u, v]) => [.12 + u * s * .9, .9 - (1 - v) * s * .9]), true, c, lw * 1.1); });
      x.fillStyle = '#b03030'; const [ox, oy] = P(.12 + .06 * .65, .9); x.beginPath(); x.arc(ox, oy, lw * 2.4, 0, Math.PI * 2); x.fill();
    } else if (kind === 'marker') {
      x.fillStyle = 'rgba(255,255,255,.35)'; x.fillRect(X + w * .03, Y + h * .12, w * .94, h * .76); x.strokeStyle = LINE; x.lineWidth = lw; x.strokeRect(X + w * .03, Y + h * .12, w * .94, h * .76);
      const fills = ['#c3d3e6', '#e3cfa8', '#cddcc2', '#e6c6bb'];
      const place = (pts, bx, by, bw, bh, k) => poly(pts.map(([u, v]) => [bx + u * bw, by + v * bh]), true, LINE, lw * .9, null, fills[k % 4]);
      place(bodice, .05, .14, .17, .72, 0); place(bodice.map(([u, v]) => [1 - u, v]), .21, .14, .17, .72, 1); place(bodice, .38, .14, .17, .72, 0);
      place(sleeve, .56, .14, .2, .36, 2); place(sleeve.map(([u, v]) => [u, 1 - v]), .56, .5, .2, .36, 2); place([[0, 0], [1, 0], [1, 1], [0, 1]], .78, .16, .17, .12, 3); place([[0, 0], [1, 0], [1, 1], [0, 1]], .78, .32, .17, .12, 3);
      x.strokeStyle = '#b03030'; x.lineWidth = lw * .8; x.setLineDash([lw * 3, lw * 2]); x.beginPath(); x.moveTo(X + w * .03, Y + h * .5); x.lineTo(X + w * .97, Y + h * .5); x.stroke(); x.setLineDash([]);
    } else if (kind === 'chart') {
      const cols = 24, rows = 16, cw = w * .9 / cols, ch = h * .86 / rows, ox = X + w * .05, oy = Y + h * .07;
      for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
        const gx = ox + c * cw, gy = oy + r * ch, purl = c % 12 === 0 || c % 12 === 1 || c % 12 === 10 || c % 12 === 11, cable = c % 12 >= 4 && c % 12 <= 7;
        x.fillStyle = cable ? '#e6edf5' : '#ffffff'; x.fillRect(gx, gy, cw, ch); x.strokeStyle = '#c9ccd0'; x.lineWidth = 1; x.strokeRect(gx, gy, cw, ch);
        if (purl) { x.fillStyle = INK; x.beginPath(); x.arc(gx + cw / 2, gy + ch / 2, Math.min(cw, ch) * .13, 0, Math.PI * 2); x.fill(); }
      }
      x.strokeStyle = INK; x.lineWidth = lw * 1.1;
      for (let r = 2; r < rows; r += 6) for (const c0 of [4, 16]) { const gx = ox + c0 * cw, gy = oy + r * ch; x.beginPath(); x.moveTo(gx, gy + ch); x.lineTo(gx + 4 * cw, gy); x.moveTo(gx, gy); x.lineTo(gx + 1.6 * cw, gy + ch * .4); x.moveTo(gx + 2.4 * cw, gy + ch * .6); x.lineTo(gx + 4 * cw, gy + ch); x.stroke(); }
    } else if (kind === 'sketch') {
      x.strokeStyle = 'rgba(60,60,66,.75)'; x.lineCap = 'round';
      for (let k = 0; k < 3; k++) { x.lineWidth = lw * (1.1 - k * .3); poly(front.map(([u, v]) => [.18 + u * .64 + (k - 1) * .006, .08 + v * .84 + (k - 1) * .004]), true, 'rgba(60,60,66,.55)', lw * (1.1 - k * .3)); }
      for (let i = 0; i < 9; i++) poly([[.25 + i * .05, .62], [.21 + i * .05, .9]], false, 'rgba(60,60,66,.25)', lw * .6);
    } else if (kind === 'notes') {
      x.strokeStyle = 'rgba(60,60,66,.55)'; x.lineWidth = Math.max(1, lw * .7);
      for (let i = 0; i < 7; i++) { x.beginPath(); for (let s = 0; s <= 24; s++) { const px0 = X + w * (.1 + s / 24 * (.55 + (i % 3) * .1)), py0 = Y + h * (.12 + i * .11) + Math.sin(s * 1.7 + i) * lw * .6; s ? x.lineTo(px0, py0) : x.moveTo(px0, py0); } x.stroke(); }
      for (const v of [.12, .45, .78]) { x.strokeStyle = '#b03030'; x.strokeRect(X + w * .82, Y + h * (v - .04), w * .06, w * .06); }
    } else if (kind === 'approval') {
      for (let i = 0; i < 5; i++) { const v = .14 + i * .16; x.strokeStyle = LINE; x.lineWidth = lw; x.strokeRect(X + w * .1, Y + h * v, w * .08, w * .08); if (i < 3) { x.strokeStyle = '#2e7d4f'; x.lineWidth = lw * 1.4; x.beginPath(); x.moveTo(X + w * .115, Y + h * v + w * .04); x.lineTo(X + w * .135, Y + h * v + w * .065); x.lineTo(X + w * .17, Y + h * v + w * .012); x.stroke(); }
        x.strokeStyle = 'rgba(60,60,66,.5)'; x.lineWidth = Math.max(1, lw * .7); x.beginPath(); x.moveTo(X + w * .25, Y + h * v + w * .04); x.lineTo(X + w * (.62 + (i % 2) * .2), Y + h * v + w * .04); x.stroke(); }
    }
  }
  function uiScreen(x, kind, X, Y, w, h) {                 // a neutral drawing application frame: bars and icons, no product UI
    x.fillStyle = '#e9ece9'; x.fillRect(X, Y, w, h); x.fillStyle = '#2f3a36'; x.fillRect(X, Y, w, h * .075);
    for (let i = 0; i < 3; i++) { x.fillStyle = ['#d9dedb', '#aeb6b2', '#7f8a85'][i]; x.beginPath(); x.arc(X + w * (.025 + i * .025), Y + h * .0375, h * .013, 0, Math.PI * 2); x.fill(); }
    x.fillStyle = '#dde1de'; x.fillRect(X, Y + h * .075, w * .055, h * .925);
    for (let i = 0; i < 7; i++) { x.fillStyle = i === 2 ? '#2c6fb3' : '#9aa39f'; x.fillRect(X + w * .015, Y + h * (.11 + i * .085), w * .025, w * .025); }
    x.fillStyle = '#ffffff'; x.fillRect(X + w * .075, Y + h * .11, w * .9, h * .85);
    devDrawing(x, kind, X + w * .085, Y + h * .125, w * .88, h * .82, Math.max(1.2, w / 260));
  }
  if (want('CAD_SCREENS')) {
    // CAD desks F120 / F122 / F124 (west wall): two monitors each, faces x 22.463 facing +x, 0.534 x 0.311 m (y 0.884-1.195);
    // wall screen F129 on the north wall: face z -6.471 facing +z, x 24.432-25.86, y 1.077-1.869. One atlas for all seven.
    const mW = px(512), mH = Math.round(mW * .311 / .534), wW = px(1024), wH = Math.round(wW * .792 / 1.428), AW = mW * 3, AH = mH * 2 + wH;
    const c = canvas(AW, AH), x = c.getContext('2d');
    const kinds = ['flatF', 'flatB', 'pattern', 'grading', 'marker', 'chart'];
    kinds.forEach((k, i) => uiScreen(x, k, (i % 3) * mW, Math.floor(i / 3) * mH, mW, mH));
    { const X = 0, Y = mH * 2, w = wW, h = wH, m2 = w / 1.428;                         // the wall screen: the whole exercise in four steps
      x.fillStyle = '#f4f3ef'; x.fillRect(X, Y, w, h); x.fillStyle = '#20302a'; x.fillRect(X, Y, w, h * .14);
      x.fillStyle = '#f1eadc'; x.font = `600 ${Math.round(h * .062)}px Inter, Arial, sans-serif`; x.fillText('Development exercise: knit cardigan (illustrative)', X + w * .03, Y + h * .095);
      ['Sketch', 'Technical flat', 'Pattern', 'Knit swatch'].forEach((t, i) => {
        const bx = X + w * (.03 + i * .245), by = Y + h * .2, bw = w * .22, bh = h * .7;
        x.fillStyle = '#ffffff'; x.fillRect(bx, by, bw, bh); x.strokeStyle = '#d4d6d2'; x.lineWidth = 2; x.strokeRect(bx, by, bw, bh);
        x.fillStyle = '#3b4742'; x.font = `600 ${Math.round(h * .045)}px Inter, Arial, sans-serif`; x.fillText(t, bx + bw * .06, by + bh * .1);
        if (i < 3) devDrawing(x, ['sketch', 'flatF', 'pattern'][i], bx + bw * .05, by + bh * .14, bw * .9, bh * .82, Math.max(1.5, m2 / 260));
        else { x.save(); x.beginPath(); x.rect(bx + bw * .08, by + bh * .16, bw * .84, bh * .76); x.clip(); x.fillStyle = PAL.indigo; x.fillRect(bx, by, bw, bh); x.globalCompositeOperation = 'multiply'; x.globalAlpha = .6; x.fillStyle = stitchPattern(x, 'cable', bw * .5); x.fillRect(bx, by, bw, bh); x.restore(); }
        if (i < 3) { x.fillStyle = '#9aa39f'; x.beginPath(); const ax = bx + bw + w * .006, ay = by + bh / 2; x.moveTo(ax, ay - h * .025); x.lineTo(ax + w * .013, ay); x.lineTo(ax, ay + h * .025); x.fill(); }
      }); }
    const atlas = texture(c, { clamp: true });
    const screenMat = std('cad_screens', { map: atlas, emissive: '#ffffff', emissiveMap: atlas, emissiveIntensity: .3, roughness: .3 });
    const region = (geo, u0, v0, u1, v1) => { const uv = geo.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setXY(i, u0 + uv.getX(i) * (u1 - u0), 1 - (v1 - uv.getY(i) * (v1 - v0))); return geo; };
    const g = new THREE.Group(); g.name = 'CAD_SCREENS'; group.add(g); g.userData = { interiorItem: 'CAD_SCREENS', zone: 'Z14' };
    [-6.007, -5.423, -4.229, -3.645, -2.451, -1.867].forEach((zc, i) => {
      const k = [0, 1, 2, 3, 4, 5][i], cx0 = (k % 3) * mW / AW, cy0 = Math.floor(k / 3) * mH / AH;
      mesh(g, region(new THREE.PlaneGeometry(.534, .311), cx0, cy0, cx0 + mW / AW, cy0 + mH / AH), screenMat, 22.466, 1.0395, zc, 0, Math.PI / 2);
    });
    mesh(g, region(new THREE.PlaneGeometry(1.428, .792), 0, mH * 2 / AH, wW / AW, 1), screenMat, 25.146, 1.473, -6.468);
  }
  if (want('CAD_PINBOARD')) {
    // felt pinboard F130 on the south wall: face z -0.292 (room on its -z side), x 23.242-26.288, y 1.018-2.335; its 18 sheets
    // (z -0.297) keep their places and are ordered by column from sketch to approval
    const X0 = 23.242, X1 = 26.288, Y0 = 1.018, Y1 = 2.335, Wm = X1 - X0, Hm = Y1 - Y0;
    // seen from the room the east end is on the left, so the exercise reads left to right from the east column
    const SHEETS = [[25.9, 26.213, [[1.892, 2.134, 'sketch'], [1.575, 1.785, 'sketch'], [1.137, 1.39, 'swatch:k']]],
      [25.417, 25.72, [[1.891, 2.098, 'flatF'], [1.51, 1.73, 'flatB'], [1.188, 1.395, 'chart']]],
      [24.881, 25.166, [[2.04, 2.257, 'pattern'], [1.608, 1.855, 'grading'], [1.227, 1.452, 'swatch:b']]],
      [24.441, 24.731, [[2.012, 2.251, 'marker'], [1.577, 1.832, 'swatch:n'], [1.208, 1.454, 'buttons']]],
      [23.985, 24.283, [[1.998, 2.248, 'notes'], [1.581, 1.851, 'flatF'], [1.217, 1.426, 'notes']]],
      [23.449, 23.805, [[1.946, 2.216, 'approval'], [1.577, 1.786, 'swatch:w'], [1.137, 1.377, 'swatch:a']]]];
    const W = px(1280), H = Math.round(W * Hm / Wm), c = canvas(W, H), x = c.getContext('2d'), mx = W / Wm, my = H / Hm, k = mx / 417;
    x.fillStyle = '#2f5d48'; x.fillRect(0, 0, W, H);                                             // brand-green felt
    const r = rng(611); for (let i = 0; i < W * H / 18; i++) { x.fillStyle = r() > .5 ? 'rgba(255,255,255,.05)' : 'rgba(0,0,0,.07)'; x.fillRect(r() * W, r() * H, 1 + r() * 1.5, 1 + r() * 1.5); }
    let n = 0;
    for (const [x0, x1, rows] of SHEETS) for (const [y0, y1, kind] of rows) {
      const PX0 = (X1 - x1) * mx, PX1 = (X1 - x0) * mx, PY0 = (Y1 - y1) * my, PY1 = (Y1 - y0) * my;   // seen from the room, east is on the left
      if (kind.startsWith('swatch')) boardSwatch(x, kind.slice(7), PX0, PY0, PX1, PY1, 300 + n, k);
      else {
        const w = PX1 - PX0, h = PY1 - PY0;
        x.save(); x.shadowColor = 'rgba(20,20,15,.5)'; x.shadowBlur = 6 * k; x.shadowOffsetX = 1.5 * k; x.shadowOffsetY = 3 * k; x.fillStyle = '#f6f4ee'; x.fillRect(PX0, PY0, w, h); x.restore();
        if (kind === 'buttons') { for (let i = 0; i < 6; i++) { const bx = PX0 + w * (.25 + (i % 3) * .25), by = PY0 + h * (.35 + Math.floor(i / 3) * .35); x.fillStyle = '#5a3b26'; x.beginPath(); x.arc(bx, by, w * .07, 0, Math.PI * 2); x.fill(); x.fillStyle = '#1d130c'; for (const [dx, dy] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) { x.beginPath(); x.arc(bx + dx * w * .018, by + dy * w * .018, w * .008, 0, Math.PI * 2); x.fill(); } } }
        else devDrawing(x, kind, PX0 + w * .06, PY0 + h * .08, w * .88, h * .84, Math.max(1, 1.1 * k));
        for (const u of [.12, .88]) pinHead(x, PX0 + w * u, PY0 + 5 * k, 2.6 * k, '#efe9dc', '#8f887a');
      }
      n++;
    }
    mesh(group, new THREE.PlaneGeometry(Wm, Hm), std('cad_pinboard', { map: texture(c, { clamp: true }), roughness: .93 }), (X0 + X1) / 2, (Y0 + Y1) / 2, -.3, 0, Math.PI);   // 3 mm in front of the sheets
  }
  if (want('CAD_LAYOUT_TABLE')) {
    // layout / digitiser table F127: top y 0.9145 (ray-cast in the viewer; the GLB query rounds it to 0.91) over x 24.49-26.31,
    // z -4.16..-2.95. A pattern sheet in the middle, tools at its edges and a small fabric reference set at the west end; the
    // east third stays clear for work
    const g = new THREE.Group(); g.name = 'CAD_LAYOUT_TABLE'; group.add(g); g.userData = { interiorItem: 'CAD_LAYOUT_TABLE', zone: 'Z14' }; const TOP = .9145;
    const lay = (c, w, d, cx, cz, yaw, lift, name, props = {}) => mesh(g, new THREE.PlaneGeometry(w, d), std(name, { map: texture(c, { clamp: true }), roughness: .9, polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -1, ...props }), cx, TOP + lift, cz, -Math.PI / 2, 0, yaw);
    const sheet = (() => { const W = px(1024), H = Math.round(W * .75 / 1.2), c = canvas(W, H), x = c.getContext('2d');   // kraft marker paper
      cloth(x, 0, 0, W, H, '#cdb58d', { cell: 1.5, seed: 651, slub: .02, mottle: .05, contrast: .15 });
      x.fillStyle = 'rgba(70,55,35,.35)'; const inch = W / 1.2 * .0254; for (let i = 0; i * inch < W; i++) for (let j = 0; j * inch < H; j++) x.fillRect(i * inch + inch / 2 - 1, j * inch + inch / 2 - 1, 2, 2);
      devDrawing(x, 'marker', W * .02, H * .02, W * .96, H * .96, 3); return c; })();
    lay(sheet, 1.2, .75, 25.2, -3.555, .02, .0012, 'cad_sheet');
    const alu = std('cad_alu', { color: '#c9ccce', roughness: .35, metalness: .7 }), weight = std('cad_weight', { color: '#2b2d2f', roughness: .5, metalness: .4 });
    mesh(g, new THREE.BoxGeometry(.6, .003, .04), alu, 25.3, TOP + .0027, -3.3);                                    // L-square on the sheet
    mesh(g, new THREE.BoxGeometry(.04, .003, .36), alu, 25.62, TOP + .0027, -3.48);
    for (const [wx, wz] of [[24.78, -3.8], [25.6, -3.86], [24.86, -3.28]]) { const m0 = mesh(g, new THREE.BoxGeometry(.07, .022, .045), weight, wx, TOP + .0012 + .011, wz); m0.rotation.y = wx * 3; }   // pattern weights
    mesh(g, new THREE.CylinderGeometry(.0035, .0035, .17, 8), std('cad_pencil', { color: '#2f5d50', roughness: .5 }), 25.05, TOP + .0047, -3.31, 0, .4, Math.PI / 2);
    // fabric reference set at the west end: three folded knit samples with a header card
    [[PAL.indigo, 'jersey'], [PAL.khadi, 'cable'], ['#6f7a4c', 'rib']].forEach(([col, stitchName], i) => {
      const t = texture(knitTile(stitchName), { srgb: false, repeat: [3, 3] });
      mesh(g, new THREE.BoxGeometry(.2, .018, .16), std('cad_fold_' + i, { color: col, map: t, roughness: .95 }), 24.62, TOP + .009 + i * .018, -3.13, 0, (i - 1) * .05);
    });
    const card = (() => { const c = canvas(256, 160), x = c.getContext('2d'); x.fillStyle = '#f2ede2'; x.fillRect(0, 0, 256, 160); x.fillStyle = '#9a8f7a'; x.beginPath(); x.arc(128, 18, 7, 0, Math.PI * 2); x.fill();
      x.fillStyle = 'rgba(60,60,66,.55)'; for (let i = 0; i < 3; i++) x.fillRect(24, 50 + i * 30, 150 + (i % 2) * 50, 4); return c; })();
    lay(card, .12, .075, 24.62, -3.28, .1, .0015, 'cad_card');
  }
  // ---------------------------------------------------------------- Global Design Studio (Z18): mood board and review table
  // a stitch tile resized so one tile spans `size` pixels, as a repeating pattern of context x
  function stitchPattern(x, name, size) {
    const t = knitTile(name), s = canvas(Math.max(4, Math.round(size)), Math.max(4, Math.round(size * t.height / t.width)));
    s.getContext('2d').drawImage(t, 0, 0, s.width, s.height); return x.createPattern(s, 'repeat');
  }
  // technical flat of a garment in graphite, inside the box (bx, by, bw, bh): tee, cardigan or trouser
  function garmentFlat(x, kind, bx, by, bw, bh, lw) {
    const L = (pts, close = true, dash = null) => { x.setLineDash(dash || []); x.beginPath(); pts.forEach(([u, v], i) => i ? x.lineTo(bx + u * bw, by + v * bh) : x.moveTo(bx + u * bw, by + v * bh)); if (close) x.closePath(); x.stroke(); x.setLineDash([]); };
    x.strokeStyle = '#3c3d40'; x.lineWidth = lw; x.lineJoin = 'round'; x.lineCap = 'round';
    if (kind === 'trouser') {
      L([[.22, .04], [.78, .04], [.78, .12], [.22, .12]]);
      L([[.22, .12], [.17, .96], [.44, .96], [.5, .36], [.56, .96], [.83, .96], [.78, .12]], false);
      L([[.5, .12], [.5, .3]], false); L([[.3, .12], [.36, .22]], false); L([[.7, .12], [.64, .22]], false);
      L([[.18, .91], [.43, .91]], false, [lw * 2.5, lw * 2]); L([[.57, .91], [.82, .91]], false, [lw * 2.5, lw * 2]);
      return;
    }
    const body = [[.38, .05], [.2, .11], [.03, .34], [.12, .42], [.24, .3], [.24, .95], [.76, .95], [.76, .3], [.88, .42], [.97, .34], [.8, .11], [.62, .05]];
    L(kind === 'cardigan' ? [...body, [.5, .46]] : [...body, [.56, .12], [.5, .13], [.44, .12]]);
    L([[.25, .88], [.75, .88]], false, kind === 'cardigan' ? null : [lw * 2.5, lw * 2]);
    if (kind === 'cardigan') {
      L([[.5, .46], [.5, .95]], false);
      for (let i = 0; i < 5; i++) { x.beginPath(); x.arc(bx + .53 * bw, by + (.52 + i * .085) * bh, lw * 1.6, 0, Math.PI * 2); x.stroke(); }
      for (let u = .27; u < .74; u += .03) L([[u, .88], [u, .95]], false);
    } else { L([[.07, .38], [.15, .3]], false, [lw * 2.5, lw * 2]); L([[.93, .38], [.85, .3]], false, [lw * 2.5, lw * 2]); }
  }
  // pinking-shear outline: zigzag teeth pointing into the cloth along all four edges
  function pinkedPath(x, X0, Y0, X1, Y1, tooth) {
    x.beginPath(); let first = true;
    const edge = (ax, ay, bx, by, nx, ny) => { const steps = Math.max(2, Math.round(Math.hypot(bx - ax, by - ay) / (tooth * 2))) * 2;
      for (let i = 0; i <= steps; i++) { const f = i / steps, d = i % 2 ? tooth : 0, X = ax + (bx - ax) * f + nx * d, Y = ay + (by - ay) * f + ny * d; if (first) { x.moveTo(X, Y); first = false; } else x.lineTo(X, Y); } };
    edge(X0, Y0, X1, Y0, 0, 1); edge(X1, Y0, X1, Y1, -1, 0); edge(X1, Y1, X0, Y1, 0, -1); edge(X0, Y1, X0, Y0, 1, 0); x.closePath();
  }
  function pinHead(x, cx, cy, r, light, dark) {
    x.fillStyle = 'rgba(30,20,10,.32)'; x.beginPath(); x.ellipse(cx + r * .5, cy + r * .8, r * 1.05, r * .8, 0, 0, Math.PI * 2); x.fill();
    const g = x.createRadialGradient(cx - r * .35, cy - r * .35, r * .1, cx, cy, r); g.addColorStop(0, '#ffffff'); g.addColorStop(.3, light); g.addColorStop(1, dark);
    x.fillStyle = g; x.beginPath(); x.arc(cx, cy, r, 0, Math.PI * 2); x.fill();
  }
  // one piece of cloth on the board: shadow, pinked edge, the weave or knit of its kind, a slight drape, a pin
  function boardSwatch(x, code, X0, Y0, X1, Y1, n, k) {
    const base = srgb(LIN[code]), w = X1 - X0, h = Y1 - Y0, r = rng(700 + n), tooth = 2.2 * k;
    x.save(); x.shadowColor = 'rgba(35,25,15,.5)'; x.shadowBlur = 7 * k; x.shadowOffsetX = 1.5 * k; x.shadowOffsetY = 3.5 * k;
    x.fillStyle = base; pinkedPath(x, X0, Y0, X1, Y1, tooth); x.fill(); x.restore();
    x.save(); pinkedPath(x, X0, Y0, X1, Y1, tooth); x.clip();
    const lines = (step, alpha, vertical, diag = false) => { x.strokeStyle = `rgba(255,255,255,${alpha})`; x.lineWidth = Math.max(1, .9 * k); x.beginPath();
      for (let s = -h; s < w + h; s += step) { if (diag) { x.moveTo(X0 + s, Y1); x.lineTo(X0 + s + h, Y0); } else if (vertical) { x.moveTo(X0 + s, Y0); x.lineTo(X0 + s, Y1); } else { x.moveTo(X0, Y0 + s); x.lineTo(X1, Y0 + s); } } x.stroke(); };
    const knit = (name, size, alpha) => { x.globalCompositeOperation = 'multiply'; x.globalAlpha = alpha; x.fillStyle = stitchPattern(x, name, size); x.fillRect(X0, Y0, w, h); x.globalAlpha = 1; x.globalCompositeOperation = 'source-over'; };
    if ('agw'.includes(code)) cloth(x, X0, Y0, w, h, base, { cell: Math.max(1.5, 2 * k), seed: 710 + n, slub: .16, mottle: .05, contrast: .5 });
    if (code === 'w') { const u = 1.3 * k, s = 22 * k;                     // Jamdani-style butis woven white on white
      for (let j = 0, yy = Y0 + s * .6; yy < Y1; yy += s * .9, j++) for (let xx = X0 + s * .5 + (j % 2) * s * .5; xx < X1; xx += s) buti(x, BUTI, xx, yy, u, { 1: 'rgba(255,255,255,.95)', 2: '#cbc3b1' }); }
    if (code === 'd') { lines(3 * k, .12, false, true); const g = x.createRadialGradient(X0 + w * .5, Y0 + h * .45, 1, X0 + w * .5, Y0 + h * .45, Math.max(w, h) * .7); g.addColorStop(0, 'rgba(160,185,215,.16)'); g.addColorStop(1, 'rgba(160,185,215,0)'); x.fillStyle = g; x.fillRect(X0, Y0, w, h); }
    if (code === 'n' || code === 'k') { knit('rib', 22 * k, .5); lines(2.75 * k, code === 'k' ? .07 : .05, true); }
    if (code === 'h') for (let i = 0; i < w * h / 10; i++) { const v = r() > .5; x.fillStyle = v ? 'rgba(235,235,228,.35)' : 'rgba(20,20,22,.35)'; x.fillRect(X0 + r() * w, Y0 + r() * h, k * (1 + r()), k * (.6 + r() * .6)); }
    if (code === 'b') knit('jersey', 16 * k, .45);
    if (code === 's') knit('moss', 16 * k, .45);
    if (code === 'r') knit('waffle', 20 * k, .5);
    if (code === 'o') for (let s = 0; s < w; s += 4 * k) { const g = x.createLinearGradient(X0 + s, 0, X0 + s + 4 * k, 0); g.addColorStop(0, 'rgba(0,0,0,.22)'); g.addColorStop(.5, 'rgba(255,255,240,.12)'); g.addColorStop(1, 'rgba(0,0,0,.22)'); x.fillStyle = g; x.fillRect(X0 + s, Y0, 4 * k, h); }   // corduroy wales
    const d = x.createLinearGradient(0, Y0, 0, Y1); d.addColorStop(0, 'rgba(255,255,255,.08)'); d.addColorStop(.45, 'rgba(255,255,255,0)'); d.addColorStop(1, 'rgba(0,0,0,.12)');
    x.fillStyle = d; x.fillRect(X0, Y0, w, h);                                                       // hangs from its pin: lighter top, heavier foot
    const curl = x.createRadialGradient(r() > .5 ? X1 : X0, Y1, 1, r() > .5 ? X1 : X0, Y1, w * .6); curl.addColorStop(0, 'rgba(0,0,0,.1)'); curl.addColorStop(1, 'rgba(0,0,0,0)');
    x.fillStyle = curl; x.fillRect(X0, Y0, w, h);
    x.restore();
    const brass = n % 3 === 0; pinHead(x, X0 + w * (.42 + r() * .16), Y0 + 7 * k, 3.2 * k, brass ? '#d9b46a' : '#efe9dc', brass ? '#6e5124' : '#8f887a');
  }
  function boardSheet(x, X0, Y0, X1, Y1, n, k) {                         // a paper sheet with a garment flat, pinned at both top corners
    const w = X1 - X0, h = Y1 - Y0;
    x.save(); x.shadowColor = 'rgba(35,25,15,.45)'; x.shadowBlur = 6 * k; x.shadowOffsetX = 1.5 * k; x.shadowOffsetY = 3 * k; x.fillStyle = srgb(LIN.p); x.fillRect(X0, Y0, w, h); x.restore();
    garmentFlat(x, ['tee', 'cardigan', 'trouser'][n % 3], X0 + w * .14, Y0 + h * .1, w * .72, h * .66, Math.max(1, 1.1 * k));
    x.strokeStyle = 'rgba(70,70,75,.45)'; x.lineWidth = Math.max(1, .8 * k);
    for (let i = 0; i < 3; i++) { x.beginPath(); for (let s = 0; s <= 24; s++) { const X = X0 + w * (.14 + s / 24 * (.5 + (i % 2) * .2)), Y = Y0 + h * (.83 + i * .05) + Math.sin(s * 1.9 + i) * k; s ? x.lineTo(X, Y) : x.moveTo(X, Y); } x.stroke(); }   // pencil notes (no text)
    for (const u of [.1, .9]) pinHead(x, X0 + w * u, Y0 + 6 * k, 3 * k, '#efe9dc', '#8f887a');
  }
  // a linen pinboard redrawn as pinned cloth. pieces: [code, X0, Y0, X1, Y1] in canvas pixels; pxPerM sets the detail scale
  // (k = 1 at 417 px/m); `first` offsets the per-piece randomness so two boards differ
  function pinnedBoard(W, H, pxPerM, pieces, first) {
    const c = canvas(W, H), x = c.getContext('2d'), k = pxPerM / 417;
    cloth(x, 0, 0, W, H, srgb(LIN.linen), { cell: Math.max(1.5, 2 * k), seed: 601 + first, slub: .05, mottle: .03, contrast: .35 });
    pieces.forEach(([code, X0, Y0, X1, Y1], i) => code === 'p' ? boardSheet(x, X0, Y0, X1, Y1, first + i, k) : boardSwatch(x, code, X0, Y0, X1, Y1, first + i, k));
    return c;
  }
  if (want('DS_FABRIC_BOARD')) {
    // mood board F167 on the studio's west wall: linen face x 29.427, swatches and sheets at x 29.431 over y 0.459-2.284,
    // z -30.479..-23.115. Columns from north to south: [z0, z1, 'code y0-y1 ...'], y in mm, codes as LIN (from the model)
    const BOARD = [[-30.228, -29.978, 'o583-784 g846-1112 s1163-1354 a1420-1696 g1735-1925 h1975-2221'],
      [-29.897, -29.692, 'k652-887 a923-1170 p1240-1505 h1538-1721 g1786-2064'],
      [-29.643, -29.407, 'b572-762 w821-975 b1001-1279 g1342-1565 d1610-1785 a1832-2069'],
      [-29.344, -29.068, 'd609-762 d811-1018 g1058-1309 n1346-1541 o1606-1761 n1826-2075'],
      [-28.979, -28.717, 'd568-744 h771-1037 d1073-1244 w1270-1538 h1568-1749 p1778-1944 r1984-2233'],
      [-28.639, -28.377, 'b685-939 s1013-1255 b1296-1475 b1522-1761 k1796-2037'],
      [-28.28, -28.075, 'a678-910 n938-1134 o1163-1436 a1471-1633 s1708-1938 p1973-2155'],
      [-28.032, -27.743, 'k564-742 d806-1079 b1121-1290 r1338-1598 p1667-1857 n1895-2155'],
      [-27.678, -27.495, 'g610-804 o853-1016 r1046-1321 s1368-1533 b1607-1787 k1846-2120'],
      [-27.441, -27.197, 'b675-846 p878-1100 k1131-1409 o1440-1610 g1670-1881 o1917-2128'],
      [-27.137, -26.889, 's649-824 h872-1093 b1128-1361 n1417-1679 k1711-1969'],
      [-26.798, -26.541, 'k645-909 n937-1159 p1203-1408 k1468-1636 g1709-1871 w1933-2136'],
      [-26.46, -26.238, 'k635-887 n918-1194 n1254-1479 a1548-1774 b1802-2033'],
      [-26.193, -26.015, 'w663-903 s943-1112 b1164-1378 b1433-1657 k1729-1914 r1983-2227'],
      [-25.938, -25.744, 'b626-875 a908-1183 k1223-1502 h1539-1780 s1813-2065'],
      [-25.672, -25.414, 'a625-793 a855-1118 o1147-1350 b1417-1575 a1649-1904 o1963-2222'],
      [-25.346, -25.165, 'r561-837 h899-1116 k1172-1326 g1370-1525 w1552-1824 o1854-2098'],
      [-25.067, -24.832, 'a674-827 r853-1014 g1044-1308 r1345-1583 d1647-1809 w1844-2025'],
      [-24.765, -24.554, 'w645-844 h911-1068 d1138-1297 r1359-1597 r1642-1809 h1844-2079'],
      [-24.472, -24.263, 'n559-715 r770-1046 o1111-1316 r1364-1528 a1575-1847 o1876-2119'],
      [-24.216, -23.975, 'r625-819 o870-1143 g1200-1419 d1457-1658 g1720-1897 r1929-2168'],
      [-23.905, -23.723, 'w596-785 a823-1026 b1073-1234 h1260-1435 n1496-1660 g1692-1878 o1918-2120'],
      [-23.68, -23.476, 'g569-737 n768-941 g988-1257 a1301-1474 g1536-1751 d1818-2064'],
      [-23.378, -23.19, 'o586-777 w828-1071 n1113-1308 b1359-1632 h1676-1828 o1881-2095']];
    const Z0 = -30.479, Z1 = -23.115, Y0 = .459, Y1 = 2.284, Wm = Z1 - Z0, Hm = Y1 - Y0;
    const W = px(3072), H = px(768), mx = W / Wm, my = H / Hm, pieces = [];
    for (const [z0, z1, list] of BOARD) for (const item of list.split(' ')) {
      const [y0, y1] = item.slice(1).split('-').map(v => v / 1000);
      pieces.push([item[0], (Z1 - z1) * mx, (Y1 - y1) * my, (Z1 - z0) * mx, (Y1 - y0) * my]);   // seen from the room, south is on the left
    }
    const face = std('ds_board', { map: texture(pinnedBoard(W, H, mx, pieces, 0), { clamp: true }), roughness: .92 });
    mesh(group, new THREE.PlaneGeometry(Wm, Hm), face, 29.434, (Y0 + Y1) / 2, (Z0 + Z1) / 2, 0, Math.PI / 2);   // 3 mm in front of the swatches
    // its five track spots LT082-LT086 (x 29.73-29.86, y 2.40-2.60) are 0.3-0.45 m off the board, as at the Reception oak wall
    const scallop = scallopMaterial('ds_scallop', .26);
    for (const z of [-29.97, -28.45, -26.92, -25.40, -23.88]) mesh(group, new THREE.PlaneGeometry(.85, 1.9), scallop, 29.437, 2.62 - .95, z, 0, Math.PI / 2);
  }
  if (want('DS_REVIEW_TABLE')) {
    // presentation table F175: walnut top y 0.75 over x 30.25-31.47, z -18.29..-15.24, eight visitor chairs on its long sides.
    // Notebooks and mugs sit at both ends (z -16.02..-15.80 and -17.73..-17.51), so the set uses the free middle
    // (x 30.32-31.39, z -17.44..-16.26). Flat items: canvas top towards north at yaw 0.
    const g = new THREE.Group(); g.name = 'DS_REVIEW_TABLE'; group.add(g); const TOP = .75;
    const lay = (c, w, d, cx, cz, yaw, lift, name, props = {}) => mesh(g, new THREE.PlaneGeometry(w, d),
      std(name, { map: texture(c, { clamp: true }), roughness: .9, alphaTest: .5, polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -1, ...props }), cx, TOP + lift, cz, -Math.PI / 2, 0, yaw);
    const contact = (w, d, cx, cz, yaw, shape) => {                       // soft contact shadow under a flat item
      const c = canvas(128, Math.round(128 * d / w)), x = c.getContext('2d'); x.fillStyle = '#000'; x.fillRect(0, 0, c.width, c.height);
      x.shadowColor = '#fff'; x.shadowBlur = 10; x.fillStyle = '#fff'; x.beginPath(); shape(x, c.width, c.height); x.fill();
      const t = texture(c, { srgb: false, clamp: true });   // unlit black: a lit one would pick up a pale specular haze on the dark walnut
      const m = new THREE.MeshBasicMaterial({ name: 'interior_review_contact_' + cx.toFixed(2), color: 0x000000, alphaMap: t, transparent: true, opacity: .32, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -1, polygonOffsetUnits: -1 });
      materials.push(m); return mesh(g, new THREE.PlaneGeometry(w, d), m, cx, TOP + .0012, cz, -Math.PI / 2, 0, yaw);
    };
    // 1. a knit sample laid flat for a fit review: jersey body, a cable panel down the front, rib at the hem and neck
    const outline = [[.36, .03], [.22, .07], [.05, .30], [0, .52], [.1, .55], [.19, .36], [.21, .97], [.79, .97], [.81, .36], [.9, .55], [1, .52], [.95, .3], [.78, .07], [.64, .03], [.5, .09]];
    const knitSample = (() => {
      const W = px(640), H = Math.round(W * .56 / .48), c = canvas(W, H), x = c.getContext('2d'), m = W / .48;
      const P = () => { x.beginPath(); outline.forEach(([u, v], i) => i ? x.lineTo(u * W, v * H) : x.moveTo(u * W, v * H)); x.closePath(); };
      P(); x.fillStyle = '#d6c6a6'; x.fill(); x.save(); P(); x.clip();
      const knit = (name, size, alpha, X, Y, w, h) => { x.globalCompositeOperation = 'multiply'; x.globalAlpha = alpha; x.fillStyle = stitchPattern(x, name, size); x.fillRect(X, Y, w, h); x.globalAlpha = 1; x.globalCompositeOperation = 'source-over'; };
      knit('jersey', .018 * m, .5, 0, 0, W, H);
      x.fillStyle = '#d6c6a6'; x.fillRect(W * .42, H * .14, W * .16, H * .74); knit('cable', .07 * m, .6, W * .42, H * .14, W * .16, H * .74);
      x.fillStyle = '#d6c6a6'; x.fillRect(0, H * .9, W, H * .1); knit('rib', .04 * m, .6, 0, H * .9, W, H * .1);
      for (const [cx, cy, s] of [[.22, .42, -1], [.78, .42, 1]]) { const f = x.createRadialGradient(cx * W, cy * H, 2, cx * W, cy * H, W * .16); f.addColorStop(0, 'rgba(60,40,20,.16)'); f.addColorStop(1, 'rgba(60,40,20,0)'); x.fillStyle = f; x.fillRect(0, 0, W, H); }
      const hl = x.createLinearGradient(0, H * .1, 0, H * .6); hl.addColorStop(0, 'rgba(255,250,240,.12)'); hl.addColorStop(1, 'rgba(255,250,240,0)'); x.fillStyle = hl; x.fillRect(0, 0, W, H);
      x.restore();
      x.strokeStyle = stitchPattern(x, 'rib', .04 * m); x.lineWidth = .022 * m; x.beginPath(); x.moveTo(.36 * W, .035 * H); x.quadraticCurveTo(.5 * W, .15 * H, .64 * W, .035 * H); x.stroke();
      x.strokeStyle = 'rgba(70,52,30,.5)'; x.lineWidth = 2; P(); x.stroke();
      return c; })();
    contact(.52, .6, 30.56, -16.8, .04, (x, w, h) => { x.beginPath(); outline.forEach(([u, v], i) => { const X = (.04 + u * .92) * w, Y = (.035 + v * .93) * h; i ? x.lineTo(X, Y) : x.moveTo(X, Y); }); x.closePath(); });
    lay(knitSample, .48, .56, 30.56, -16.8, .04, .004, 'review_knit');
    // 2. drafted pattern pieces on dot-and-cross pattern paper, a clear ruler and a pencil
    const paperSheet = (() => {
      const W = px(560), H = Math.round(W * .66 / .46), c = canvas(W, H), x = c.getContext('2d'), m = W / .46, inch = .0254 * m;
      x.fillStyle = '#f4f0e6'; x.fillRect(0, 0, W, H); x.fillStyle = 'rgba(80,80,100,.55)';
      for (let i = 0; i * inch < W; i++) for (let j = 0; j * inch < H; j++) { const X = i * inch + inch / 2, Y = j * inch + inch / 2;
        if (i % 5 === 2 && j % 5 === 2) { x.fillRect(X - 3, Y - .5, 6, 1); x.fillRect(X - .5, Y - 3, 1, 6); } else x.fillRect(X - .8, Y - .8, 1.6, 1.6); }
      const L = (pts, close = true, dash = null, lw = 2.2) => { x.lineWidth = lw; x.setLineDash(dash || []); x.beginPath(); pts.forEach(([u, v], i) => i ? x.lineTo(u * W, v * H) : x.moveTo(u * W, v * H)); if (close) x.closePath(); x.stroke(); x.setLineDash([]); };
      x.strokeStyle = '#34363b';
      const arm = Array.from({ length: 9 }, (_, i) => { const t = i / 8; return [.47 - .09 * Math.sin(t * Math.PI / 2), .30 - .17 * t]; });
      L([[.07, .1], [.07, .62], [.47, .62], ...arm, [.36, .1], [.27, .08], [.2, .15], [.07, .16]]);                         // front bodice, centre front on the fold
      L([[.1, .13], [.1, .59], [.44, .59]], false, [6, 5], 1.4);                                                                // stitching line
      L([[.07, .1], [.07, .62]], false, [14, 6], 4);                                                                           // fold line
      L([[.25, .25], [.25, .5]], false, null, 1.6); L([[.235, .27], [.25, .25], [.265, .27]], false, null, 1.6); L([[.235, .48], [.25, .5], [.265, .48]], false, null, 1.6);   // grainline
      for (const [u, v] of [[.47, .45], [.46, .27], [.3, .62]]) L([[u - .012, v], [u + .012, v]], false, null, 1.6);             // notches
      const cap = Array.from({ length: 13 }, (_, i) => { const t = i / 12; return [.55 + .38 * t, .74 - .08 * Math.sin(t * Math.PI)]; });
      L([...cap, [.88, .97], [.6, .97]]);                                                                                       // sleeve, crown up
      L([[.74, .72], [.74, .93]], false, null, 1.6); L([[.725, .74], [.74, .72], [.755, .74]], false, null, 1.6);
      L([[.55, .1], [.93, .1], [.93, .17], [.55, .17]]); for (let u = .58; u < .92; u += .03) L([[u, .1], [u, .17]], false, null, 1);   // neck rib
      L([[.58, .3], [.86, .3], [.86, .52], [.58, .52]]); L([[.6, .33], [.84, .33]], false, [6, 5], 1.4);                       // pocket
      return c; })();
    lay(paperSheet, .46, .66, 31.13, -16.84, -.05, .0018, 'review_paper');
    const rulerC = (() => { const c = canvas(48, 480), x = c.getContext('2d'); x.fillStyle = 'rgba(225,235,240,1)'; x.fillRect(0, 0, 48, 480);
      x.fillStyle = '#4c5a62'; for (let i = 0; i < 46; i++) x.fillRect(0, 8 + i * 10, i % 5 ? 10 : 18, 1.5); return c; })();
    lay(rulerC, .045, .45, 31.08, -16.86, .55, .0045, 'review_ruler', { transparent: true, opacity: .55, alphaTest: 0, roughness: .25 });
    mesh(g, new THREE.CylinderGeometry(.0035, .0035, .17, 8), std('review_pencil', { color: '#2f5d50', roughness: .5 }), 31.27, TOP + .0055, -16.62, 0, .9, Math.PI / 2);
    // 3. an open sketchbook: two flats of a cardigan on the left page; a pinked swatch, colour chips and notes on the right
    const book = (() => {
      const W = px(640), H = Math.round(W * .27 / .42), c = canvas(W, H), x = c.getContext('2d');
      x.fillStyle = '#efe8d8'; x.fillRect(0, 0, W, H);
      const gut = x.createLinearGradient(W * .44, 0, W * .56, 0); gut.addColorStop(0, 'rgba(0,0,0,0)'); gut.addColorStop(.5, 'rgba(60,45,25,.28)'); gut.addColorStop(1, 'rgba(0,0,0,0)'); x.fillStyle = gut; x.fillRect(0, 0, W, H);
      garmentFlat(x, 'cardigan', W * .04, H * .12, W * .2, H * .76, 1.6); garmentFlat(x, 'tee', W * .25, H * .12, W * .2, H * .76, 1.6);
      x.save(); pinkedPath(x, W * .58, H * .12, W * .74, H * .5, 2.5); x.clip(); cloth(x, W * .58, H * .12, W * .16, H * .38, PAL.indigo, { cell: 2, seed: 731 }); x.restore();
      [PAL.indigo, PAL.madder, PAL.ochre, PAL.khadi, '#6f7a4c'].forEach((cc, i) => { x.fillStyle = cc; x.beginPath(); x.arc(W * (.8 + (i % 3) * .06), H * (.2 + Math.floor(i / 3) * .16), H * .05, 0, Math.PI * 2); x.fill(); });
      x.strokeStyle = 'rgba(60,60,66,.6)'; x.lineWidth = 1.3;
      for (let i = 0; i < 5; i++) { x.beginPath(); for (let s = 0; s <= 30; s++) { const X = W * (.58 + s / 30 * .34), Y = H * (.6 + i * .07) + Math.sin(s * 2.1 + i * 3) * 1.5; s ? x.lineTo(X, Y) : x.moveTo(X, Y); } x.stroke(); }
      return c; })();
    contact(.45, .3, 30.62, -17.3, -.06, (x, w, h) => x.rect(w * .05, h * .06, w * .9, h * .88));
    mesh(g, new THREE.BoxGeometry(.42, .012, .27), std('review_book_edge', { color: '#e6dfcd', roughness: .9 }), 30.62, TOP + .006, -17.3, 0, -.06);
    lay(book, .42, .27, 30.62, -17.3, -.06, .0125, 'review_book');
    // 4. a tailor's tape measure: the coil and a length of tape (marks only)
    const coilTop = (() => { const c = canvas(128, 128), x = c.getContext('2d'); x.fillStyle = '#eccf5a'; x.fillRect(0, 0, 128, 128); x.strokeStyle = 'rgba(90,70,20,.45)'; x.lineWidth = 1;
      for (let rr = 8; rr < 64; rr += 4) { x.beginPath(); x.arc(64, 64, rr, 0, Math.PI * 2); x.stroke(); } return c; })();
    const tapeY = std('review_tape_edge', { color: '#e3c24d', roughness: .6 });
    mesh(g, new THREE.CylinderGeometry(.032, .032, .013, 28), [tapeY, std('review_tape_top', { map: texture(coilTop, { clamp: true }), roughness: .6 }), tapeY], 31.05, TOP + .0065, -17.33);
    const tapeC = (() => { const c = canvas(24, 600), x = c.getContext('2d'); x.fillStyle = '#efd36a'; x.fillRect(0, 0, 24, 600); x.fillStyle = '#2a2a2a'; for (let i = 0; i < 60; i++) x.fillRect(0, i * 10, i % 5 ? 6 : 12, 1.4); return c; })();
    lay(tapeC, .016, .3, 31.235, -17.345, Math.PI / 2 + .08, .0014, 'review_tape', { alphaTest: 0 });
    // 5. swatch header cards: a card top with a punched hole, the cloth below with a pinked foot
    [[PAL.indigo, 'kantha'], [PAL.madder, 'weave'], [PAL.jute, 'weave'], [PAL.ochre, 'jersey']].forEach(([cc, kind], i) => {
      const W = px(200), H = Math.round(W * 1.45), c = canvas(W, H), x = c.getContext('2d');
      x.fillStyle = '#f2ede2'; x.fillRect(0, 0, W, H * .26); x.fillStyle = '#9a8f7a'; x.beginPath(); x.arc(W / 2, H * .08, W * .04, 0, Math.PI * 2); x.fill();
      x.fillStyle = 'rgba(60,60,66,.55)'; x.fillRect(W * .14, H * .15, W * .6, 2); x.fillRect(W * .14, H * .2, W * .4, 2);
      x.save(); pinkedPath(x, 0, H * .26, W, H, 3); x.clip(); cloth(x, 0, H * .26, W, H * .74, cc, { cell: 2.5, seed: 741 + i });
      if (kind === 'kantha') for (let r2 = 0; r2 < 6; r2++) stitch(x, wave(8, W - 8, H * (.34 + r2 * .1), 3, W * .3, 40), { color: PAL.thread, dash: 6, gap: 4, width: 2, seed: 750 + r2 });
      if (kind === 'jersey') { x.globalCompositeOperation = 'multiply'; x.globalAlpha = .5; x.fillStyle = stitchPattern(x, 'jersey', 26); x.fillRect(0, H * .26, W, H * .74); }
      x.restore();
      lay(c, .1, .145, 30.40 + i * .13, -16.33, [-.12, .05, -.03, .1][i], .0012 + i * .0004, 'review_card_' + i);
    });
    // 6. coconut-shell buttons sewn on a trim card
    const trim = (() => { const c = canvas(240, 160), x = c.getContext('2d'); x.fillStyle = '#efe9dc'; x.fillRect(0, 0, 240, 160); x.strokeStyle = '#b9ad95'; x.lineWidth = 3; x.strokeRect(6, 6, 228, 148); return c; })();
    lay(trim, .12, .08, 31.2, -16.33, .03, .0012, 'review_trim');
    const buttonMat = std('review_button', { color: '#4f3422', roughness: .32 });
    for (let i = 0; i < 6; i++) mesh(g, new THREE.CylinderGeometry(.0085, .0085, .003, 18), buttonMat, 31.165 + (i % 3) * .035, TOP + .0027, -16.348 + Math.floor(i / 3) * .032);
  }
  // ---------------------------------------------------------------- Merchandising (Z07): fit forms and the approval board
  if (want('MR_FIT_FORMS')) {
    // dress forms F265 / F266 (centres x 17.323 / 18.237, z -18.923): elliptical rings of the form, read from the model,
    // [y, half-width x, half-depth z]. The garment shell sits 6 mm outside them from the hip line to the base of the neck;
    // u runs round the body with the front centre (+z, towards the room) at u 0.5, v from the hem (0) to the neck (1)
    const RINGS = [[.93, .1613, .1105], [.96, .176, .1205], [1.02, .184, .126], [1.12, .1655, .1135], [1.22, .1385, .095], [1.30, .1495, .1025],
      [1.38, .176, .1205], [1.44, .1815, .1245], [1.50, .160, .1095], [1.53, .1041, .0713], [1.545, .0761, .0521]];
    const yLo = RINGS[0][0], yHi = RINGS[RINGS.length - 1][0], off = .006, seg = 48;
    function shell(cx, cz) {
      const pos = [], uv = [], index = [];
      RINGS.forEach(([y, rx, rz]) => { for (let i = 0; i <= seg; i++) { const u = i / seg, t = Math.PI * 2 * (u - .5); pos.push(cx + (rx + off) * Math.sin(t), y, cz + (rz + off) * Math.cos(t)); uv.push(u, (y - yLo) / (yHi - yLo)); } });
      for (let j = 0; j < RINGS.length - 1; j++) for (let i = 0; i < seg; i++) { const a = j * (seg + 1) + i, b = a + 1, c = a + seg + 1, d = c + 1; index.push(a, b, d, a, d, c); }
      const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); geo.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2));
      geo.setIndex(index); geo.computeVertexNormals(); return geo;
    }
    const W = px(1024), H = px(640), yOf = y => (1 - (y - yLo) / (yHi - yLo)) * H;   // canvas row of a height
    // 1. calico fit toile: style lines traced in marker (centre front, bust, waist, hip, princess seams, side seams), pinned
    const toile = (() => {
      const c = canvas(W, H), x = c.getContext('2d'), k = W / 1024;
      cloth(x, 0, 0, W, H, '#e6dcc4', { cell: Math.max(1.5, 2 * k), seed: 801, slub: .07, mottle: .04, contrast: .4 });
      const curve = (pts, color, width, dash) => { x.strokeStyle = color; x.lineWidth = width * k; x.setLineDash(dash ? dash.map(d => d * k) : []); x.beginPath(); pts.forEach(([u, y], i) => i ? x.lineTo(u * W, yOf(y)) : x.moveTo(u * W, yOf(y))); x.stroke(); x.setLineDash([]); };
      for (const y of [1.44, 1.22, 1.02]) curve([[0, y], [1, y]], '#2f4f86', 5);                               // style tape: bust, waist, hip
      curve([[.5, yHi], [.5, yLo]], '#b03030', 6);                                                              // centre front
      for (const u of [.25, .75]) curve([[u, 1.52], [u, yLo]], '#3b3b3b', 4, [12, 7]);                         // side seams
      for (const s of [-1, 1]) {                                                                               // princess seams
        const pts = [[1.53, .09], [1.47, .085], [1.44, .078], [1.33, .066], [1.22, .058], [1.12, .066], [1.02, .074], [yLo, .078]].map(([y, d]) => [.5 + s * d, y]);
        curve(pts, '#b03030', 4.5, [14, 8]);
        pts.forEach(([u, y], i) => { if (i % 2) return; const X = u * W, Y = yOf(y); x.strokeStyle = '#9aa0a6'; x.lineWidth = 1.4 * k; x.beginPath(); x.moveTo(X - 9 * k, Y + 4 * k); x.lineTo(X + 9 * k, Y - 4 * k); x.stroke(); pinHead(x, X - 9 * k, Y + 4 * k, 3 * k, '#e7e2d8', '#7d776c'); });
      }
      curve([[0, yLo + .012], [1, yLo + .012]], '#6b6355', 1.4, [7, 5]);                                         // turned hem, tacked
      return c; })();
    // 2. knitted body sample: indigo jersey, a cable panel down the centre front between purl columns, rib at the hem and neck
    const knitBody = (() => {
      const c = canvas(W, H), x = c.getContext('2d'), pxm = W / 1.03;                                         // about 1.03 m round the bust
      const knit = (name, size, alpha, X, Y, w, h) => { x.globalCompositeOperation = 'multiply'; x.globalAlpha = alpha; x.fillStyle = stitchPattern(x, name, size); x.fillRect(X, Y, w, h); x.globalAlpha = 1; x.globalCompositeOperation = 'source-over'; };
      x.fillStyle = PAL.indigo; x.fillRect(0, 0, W, H); knit('jersey', .018 * pxm, .55, 0, 0, W, H);
      x.fillStyle = PAL.indigo; x.fillRect(W * .455, 0, W * .09, H); knit('cable', .09 * pxm, .65, W * .455, 0, W * .09, H);
      for (const u of [.445, .545]) { x.fillStyle = PAL.indigo; x.fillRect(W * u, 0, W * .01, H); knit('moss', .016 * pxm, .6, W * u, 0, W * .01, H); }
      for (const [Y, h] of [[H * .93, H * .07], [0, H * .035]]) { x.fillStyle = PAL.indigo; x.fillRect(0, Y, W, h); knit('rib', .04 * pxm, .65, 0, Y, W, h); }
      return c; })();
    const g = new THREE.Group(); g.name = 'MR_FIT_FORMS'; group.add(g);
    [[toile, 17.323, 'mr_toile'], [knitBody, 18.237, 'mr_knit_body']].forEach(([c, cx, name]) => {
      const t = texture(c, { clamp: true }); t.wrapS = THREE.RepeatWrapping;
      const m = mesh(g, shell(cx, -18.923), std(name, { map: t, roughness: .93, side: THREE.DoubleSide, emissive: '#ffffff', emissiveMap: t, emissiveIntensity: .04 }));
      m.userData.interiorItem = 'MR_FIT_FORMS';
    });
  }
  if (want('MR_APPROVAL_BOARD')) {
    // approval board F258 on the south wall: linen face z -10.910 (room on its -z side), pieces 4 mm proud at z -10.914,
    // board x 9.653-11.479, y 1.170-2.183. [code, x0, x1, y0, y1] from the model; seen from the room, east is on the left
    const X0 = 9.653, X1 = 11.479, Y0 = 1.17, Y1 = 2.183, Wm = X1 - X0, Hm = Y1 - Y0;
    const P = [['g', 9.876, 10.095, 1.315, 1.551], ['p', 10.844, 11.104, 1.348, 1.565], ['a', 11.154, 11.405, 1.35, 1.606], ['a', 10.477, 10.749, 1.379, 1.618],
      ['w', 10.165, 10.384, 1.383, 1.662], ['w', 9.876, 10.095, 1.596, 1.772], ['p', 10.844, 11.104, 1.617, 1.826], ['g', 11.154, 11.405, 1.656, 1.92],
      ['p', 10.477, 10.749, 1.69, 1.913], ['r', 10.165, 10.384, 1.725, 1.893], ['p', 9.876, 10.095, 1.842, 2.041], ['a', 10.844, 11.104, 1.884, 2.074]];
    const W = px(1024), H = Math.round(W * Hm / Wm), mx = W / Wm, my = H / Hm;
    const pieces = P.map(([code, x0, x1, y0, y1]) => [code, (X1 - x1) * mx, (Y1 - y1) * my, (X1 - x0) * mx, (Y1 - y0) * my]);
    const face = std('mr_board', { map: texture(pinnedBoard(W, H, mx, pieces, 200), { clamp: true }), roughness: .92 });
    mesh(group, new THREE.PlaneGeometry(Wm, Hm), face, (X0 + X1) / 2, (Y0 + Y1) / 2, -10.917, 0, Math.PI);   // 3 mm in front of the pieces
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
    group, overhead, items: items.map(i => ({ id: i.id, zone: i.zone, note: i.note })), prepareRoom, prepareBase,
    stats: { items: items.length, meshes: geometries.length, textures: textures.length, detail },
    textures: () => textures,
    dispose() { geometries.forEach(g => g.dispose()); materials.forEach(m => m.dispose()); textures.forEach(t => t.dispose()); },
  };
}
