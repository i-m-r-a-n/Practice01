/** Bengal Earth Lab proposal layer, used only by the /bengal-earth-lab/ route (Claude, 29-30 Oct 2026).
 * "The Living Bengal Factory": a few small trees, bonsai and stones in place of the approved planters, work by rural
 * artists, rural instruments, tea in clay and wood, the Sun wall (a concept demonstration with no data) and the
 * Earth-to-Product gallery. Self-made procedural geometry and canvas artwork only. Makers, artists, growers, stone
 * sources, test records and energy data are still to be identified: nothing here is claimed as made, tested or measured.
 * The route config hides the approved items this layer replaces (hideNodes) and every replacement keeps the same
 * footprint, so the approved walk grid stays valid; new floor items report their footprint through blocksMovement().
 * Usage: buildBengalEarthLab(THREE, { zones, drinkware, anisotropy, detail }) -> { group, items, stats, textures, blocksMovement, dispose }
 * Coordinates: viewer metres, x east, y up, z south (as office_web_metadata.json).
 */
export const BEL_ITEMS = [
  { id: 'BEL_GATE_BONSAI', zone: 'Z01', note: 'A banyan bonsai on a granite plinth beside the glass gate, in place of the approved potted tree and on its footprint. Grower, species and stone source to be confirmed; it takes turns in daylight at the studio windows.' },
  { id: 'BEL_LOBBY_STONES', zone: 'Z01', note: 'Three granite stones in place of the approved small planter, on its footprint. Stone only from a documented legal source, never from illegal river extraction.' },
  { id: 'BEL_EARTH_DESK', zone: 'Z01', note: 'Handmade terracotta tiles on the visitor face of the check-in desk (proposal; potter to be identified).' },
  { id: 'BEL_LOBBY_RELIEF', zone: 'Z01', note: 'Six terracotta plaques by a rural artist on the free west wall: sun, river boat, shapla, fish, rice and a doel bird. Placeholder composition: the artist is to be commissioned, paid and credited by name.' },
  { id: 'BEL_RECEPTION_TREE', zone: 'Z02', note: 'A small fig tree in a handmade terracotta planter, in place of the approved potted tree and on its footprint.' },
  { id: 'BEL_RECEPTION_ALOE', zone: 'Z02', note: 'Ghritokumari (aloe) in a clay pot on a low stone, in place of the approved small planter: a plant traditionally kept in Bengali homes; no medical claim.' },
  { id: 'BEL_INSTRUMENTS', zone: 'Z02', note: 'Rural instruments above the console: ektara, dotara and banshi on an oak rail, a dhol on the console. Makers to be identified and credited; played at events, never used as props.' },
  { id: 'BEL_TEA_CLAY', zone: 'Z02', note: 'Tea in clay cups from a clay pot on a wooden tray, in place of the porcelain props. Glazes to be tested for lead and cadmium release before use.' },
  { id: 'BEL_SUN_WALL', zone: 'Z03', note: 'The Sun wall: sun, solar generation, direct use and storage, operations, with grid and backup shown. Concept demonstration, not live factory data. The message stays "Designed for a Solar-Powered Future" until measured evidence exists.' },
  { id: 'BEL_EARTH_WALL', zone: 'Z03', note: 'Handmade terracotta tiles between the guest WC doors, with a narrow oak ledge of clay bowls holding clay, jute, hogla, cane and rice straw (proposal).' },
  { id: 'BEL_EARTH_TO_PRODUCT', zone: 'Z30', note: 'The Earth-to-Product gallery on the plinth (the four forms are removed): raw material, craft technique, prototype, testing, collection. Illustrative objects; real samples and test records replace them.' },
  { id: 'BEL_MATERIAL_TABLE', zone: 'Z30', note: 'Living materials on the material table: woven jute, hogla, cane, water hyacinth, bamboo and kaisa samples and terracotta tiles, each with its card. Origins to be documented.' },
  { id: 'BEL_COLLECTION_BAYS', zone: 'Z30', note: 'The four display bays (garments removed on this route) show three illustrative collections and the experimental work: Bengal Nordic (handloom textiles), River to Home (hogla, water hyacinth, terracotta), Second Life Bangladesh (garment offcuts, kantha patchwork) and Future of Bengal (bamboo, cane, jute composite). Concept objects, not products on sale.' },
  { id: 'BEL_FUTURE_LAMP', zone: 'Z30', note: 'Future of Bengal: an experimental bamboo and handmade-paper lamp on a granite plinth beside the boardroom door, in place of the approved potted tree and on its footprint.' },
  { id: 'BEL_WATER_KOLSHI', zone: 'Z30', note: 'Drinking water from a clay kolshi with clay cups. The source is client-stated (deep tube well); only dated laboratory reports will ever be shown, and none are available yet.' },
  { id: 'BEL_BOARD_SAMPLES', zone: 'Z08', note: 'Wooden sample trays on the table centre line with woven samples, a terracotta tile and a small basket (illustrative).' },
  { id: 'BEL_BOARD_BONSAI', zone: 'Z08', note: 'A bonsai on a jute-wrapped stand in the corner by the screen, in place of the approved planter; it rotates to the studio windows for light.' },
  { id: 'BEL_STUDIO_SUN_SHELF', zone: 'Z18', note: 'The sunning shelf at the east window W10: three bonsai and a tulsi pot take turns in daylight. Grower and species to be confirmed.' },
  { id: 'BEL_STUDIO_TREE', zone: 'Z18', note: 'A small fig tree in daylight by window W09, in place of the approved potted tree and on its footprint.' },
  { id: 'BEL_COCREATION', zone: 'Z18', note: 'Co-creation set on the presentation table: basket prototypes, woven samples, a colour fan and form sketches (illustrative).' },
  { id: 'BEL_CLAY_DRINKWARE', zone: '*', note: 'Every glass, mug, cup, jug, bottle and tray on the route is clay or wood (glazes to be tested; wood with food-safe finishes).' },
];

export function buildBengalEarthLab(THREE, { zones = null, drinkware = [], anisotropy = 4, detail = 1 } = {}) {
  const group = new THREE.Group(); group.name = 'BENGAL_EARTH_LAB';
  const geometries = [], materials = [], textures = [], footprints = [];
  const items = BEL_ITEMS.filter(i => !zones || i.zone === '*' || zones.includes(i.zone));
  const want = id => items.some(i => i.id === id);
  const px = n => Math.max(32, Math.round(n * detail));
  // ---------------------------------------------------------------- helpers (deterministic, self-made)
  const rng = seed => () => { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  const canvas = (w, h) => { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; };
  function tex(c, { srgb = true, repeat = null, clamp = false } = {}) {
    const t = new THREE.CanvasTexture(c); t.colorSpace = srgb ? THREE.SRGBColorSpace : THREE.NoColorSpace; t.anisotropy = anisotropy;
    t.wrapS = t.wrapT = clamp ? THREE.ClampToEdgeWrapping : THREE.RepeatWrapping; if (repeat) t.repeat.set(...repeat); textures.push(t); return t;
  }
  const cache = new Map();
  function std(key, make) { if (!cache.has(key)) { const m = new THREE.MeshStandardMaterial({ name: 'bel_' + key, ...make() }); materials.push(m); cache.set(key, m); } return cache.get(key); }
  function add(parent, geometry, material, x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0) {
    geometries.push(geometry); const m = new THREE.Mesh(geometry, material); m.position.set(x, y, z); m.rotation.set(rx, ry, rz);
    m.castShadow = false; m.receiveShadow = false; parent.add(m); return m;
  }
  function item(id) { const def = BEL_ITEMS.find(i => i.id === id); const g = new THREE.Group(); g.name = id; g.userData = { conceptItem: id, zone: def.zone }; group.add(g); return g; }
  const box = (parent, mat, x, y, z, w, h, d, ry = 0) => add(parent, new THREE.BoxGeometry(w, h, d), mat, x, y + h / 2, z, 0, ry);
  const V2 = (r, y) => new THREE.Vector2(r, y);
  const lathe = (profile, seg = 40) => new THREE.LatheGeometry(profile.map(([r, y]) => V2(r, y)), seg);
  function noise3(seed) {
    const r = rng(seed), P = new Uint8Array(512), V = new Float32Array(256);
    for (let i = 0; i < 256; i++) { P[i] = i; V[i] = r() * 2 - 1; }
    for (let i = 255; i > 0; i--) { const j = Math.floor(r() * (i + 1)); const t = P[i]; P[i] = P[j]; P[j] = t; }
    for (let i = 0; i < 256; i++) P[i + 256] = P[i];
    const f = t => t * t * (3 - 2 * t), L = (a, b, t) => a + (b - a) * t, h = (x, y, z) => V[P[P[P[x & 255] + (y & 255)] + (z & 255)]];
    return (x, y, z) => { const X = Math.floor(x), Y = Math.floor(y), Z = Math.floor(z), u = f(x - X), v = f(y - Y), w = f(z - Z);
      return L(L(L(h(X, Y, Z), h(X + 1, Y, Z), u), L(h(X, Y + 1, Z), h(X + 1, Y + 1, Z), u), v), L(L(h(X, Y, Z + 1), h(X + 1, Y, Z + 1), u), L(h(X, Y + 1, Z + 1), h(X + 1, Y + 1, Z + 1), u), v), w); };
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
  // tapered branch or trunk along a smooth curve (rings follow the curve's Frenet frames)
  function taperedTube(pts, r0, r1, segs = 20, radial = 8) {
    const curve = new THREE.CatmullRomCurve3(pts.map(p => new THREE.Vector3(...p))), frames = curve.computeFrenetFrames(segs, false);
    const pos = [], nor = [], uv = [], idx = [];
    for (let i = 0; i <= segs; i++) {
      const t = i / segs, P = curve.getPointAt(t), N = frames.normals[i], B = frames.binormals[i], r = r0 + (r1 - r0) * Math.pow(t, .75);
      for (let j = 0; j <= radial; j++) {
        const a = j / radial * Math.PI * 2, c = Math.cos(a), s = Math.sin(a), nx = c * N.x + s * B.x, ny = c * N.y + s * B.y, nz = c * N.z + s * B.z;
        pos.push(P.x + r * nx, P.y + r * ny, P.z + r * nz); nor.push(nx, ny, nz); uv.push(j / radial, t * 3);
      }
    }
    for (let i = 0; i < segs; i++) for (let j = 0; j < radial; j++) { const a = i * (radial + 1) + j, b = a + radial + 1; idx.push(a, b, a + 1, b, b + 1, a + 1); }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('normal', new THREE.Float32BufferAttribute(nor, 3));
    g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); g.setIndex(idx); return g;
  }
  // a stone: a sphere pushed by smooth noise, with a flattened base that rests on the floor (base at y 0)
  function rockGeometry(r, seed, sx = 1, sy = .72, sz = 1) {
    const g = new THREE.SphereGeometry(r, 40, 28), p = g.attributes.position, n = noise3(seed);
    for (let i = 0; i < p.count; i++) {
      const x = p.getX(i) / r, y = p.getY(i) / r, z = p.getZ(i) / r;
      const d = 1 + .2 * n(x * 1.3 + 5, y * 1.3, z * 1.3) + .08 * n(x * 3.1, y * 3.1 + 2, z * 3.1) + .02 * n(x * 9, y * 9, z * 9 + 4);
      let Y = y * sy * d * r; const floor = -r * sy * .55; if (Y < floor) Y = floor + (Y - floor) * .12;
      p.setXYZ(i, x * sx * d * r, Y, z * sz * d * r);
    }
    g.computeVertexNormals(); g.computeBoundingBox(); g.translate(0, -g.boundingBox.min.y, 0); g.computeBoundingBox(); return g;
  }
  function footprint(x0, z0, x1, z1) { footprints.push([Math.min(x0, x1), Math.min(z0, z1), Math.max(x0, x1), Math.max(z0, z1)]); }

  // ---------------------------------------------------------------- shared materials (one texture per kind, reused)
  const M = {};
  M.granite = std('granite', () => {
    const s = px(256), c = canvas(s, s), x = c.getContext('2d'), r = rng(31), hc = canvas(s, s), hx = hc.getContext('2d');
    x.fillStyle = '#8e8680'; x.fillRect(0, 0, s, s); hx.fillStyle = '#808080'; hx.fillRect(0, 0, s, s);
    const inks = ['#2c2927', '#4b4643', '#6d6560', '#b8b0a7', '#d9d0c5', '#8f7064', '#a7887a'];
    for (let i = 0; i < s * s / 7; i++) { const cx = r() * s, cy = r() * s, rr = .5 + r() * 1.7 * s / 256, k = Math.floor(r() * inks.length);
      x.fillStyle = inks[k]; x.beginPath(); x.arc(cx, cy, rr, 0, 7); x.fill(); hx.fillStyle = k < 3 ? '#6a6a6a' : '#9a9a9a'; hx.beginPath(); hx.arc(cx, cy, rr, 0, 7); hx.fill(); }
    return { map: tex(c), normalMap: tex(normalFromHeight(hc, 1.2), { srgb: false }), roughness: .62, color: '#ffffff' };
  });
  M.graniteRough = std('graniteRough', () => ({ map: M.granite.map, normalMap: M.granite.normalMap, roughness: .9, color: '#d8d2cc' }));
  function terracottaCanvas(cols, rows, seed, size = 512, { relief = false } = {}) {
    const c = canvas(size, size), x = c.getContext('2d'), hc = canvas(size, size), hx = hc.getContext('2d'), r = rng(seed), tw = size / cols, th = size / rows, gr = Math.max(2, size / 140);
    const inks = ['#94512f', '#8a4a2c', '#a05a37', '#7e4128', '#99573a', '#874a31', '#a8643f'];   // fired earth, not orange
    x.fillStyle = '#b8a487'; x.fillRect(0, 0, size, size); hx.fillStyle = '#303030'; hx.fillRect(0, 0, size, size);
    for (let j = 0; j < rows; j++) for (let i = -1; i < cols; i++) {
      const off = (j % 2) * tw / 2, X = i * tw + off + gr / 2 + (r() - .5) * gr * .5, Y = j * th + gr / 2, W = tw - gr * (1 + r() * .4), H = th - gr * (1 + r() * .4), base = inks[Math.floor(r() * inks.length)];
      x.fillStyle = base; x.fillRect(X, Y, W, H);
      const g = x.createLinearGradient(X, Y, X + W, Y + H); g.addColorStop(0, 'rgba(255,230,200,.10)'); g.addColorStop(1, 'rgba(60,20,8,.14)'); x.fillStyle = g; x.fillRect(X, Y, W, H);
      for (let k = 0; k < W * H / 60; k++) { x.fillStyle = r() > .5 ? 'rgba(70,25,10,.16)' : 'rgba(255,225,190,.12)'; x.fillRect(X + r() * W, Y + r() * H, 1 + r() * 2, 1 + r() * 2); }
      x.strokeStyle = 'rgba(70,28,12,.28)'; x.lineWidth = 1.5; x.strokeRect(X + .75, Y + .75, W - 1.5, H - 1.5);
      hx.fillStyle = '#d0d0d0'; hx.fillRect(X, Y, W, H);
      for (let k = 0; k < W * H / 220; k++) { hx.fillStyle = '#a8a8a8'; hx.beginPath(); hx.arc(X + r() * W, Y + r() * H, .8 + r() * 1.6, 0, 7); hx.fill(); }
      if (relief) { hx.fillStyle = '#e8e8e8'; hx.fillRect(X + W * .12, Y + H * .12, W * .76, H * .76); }
    }
    return { c, hc };
  }
  M.terracotta = std('terracotta', () => { const { c, hc } = terracottaCanvas(4, 8, 51, px(512)); return { map: tex(c), normalMap: tex(normalFromHeight(hc, 2.4), { srgb: false }), roughness: .86 }; });
  M.oak = std('oak', () => {
    const c = canvas(px(128), px(256)), x = c.getContext('2d'), r = rng(61); x.fillStyle = '#b88c5c'; x.fillRect(0, 0, c.width, c.height);
    for (let i = 0; i < 70; i++) { const X = r() * c.width; x.strokeStyle = `rgba(${r() > .5 ? '90,58,30' : '230,200,160'},${.08 + r() * .12})`; x.lineWidth = .6 + r() * 1.6; x.beginPath(); x.moveTo(X, 0); for (let y = 0; y <= c.height; y += 16) x.lineTo(X + Math.sin(y * .03 + i) * 2.2, y); x.stroke(); }
    return { map: tex(c), roughness: .55 };
  });
  M.wood = std('mango', () => {   // darker wood for trays and turned pieces
    const c = canvas(px(128), px(256)), x = c.getContext('2d'), r = rng(67); x.fillStyle = '#7b5233'; x.fillRect(0, 0, c.width, c.height);
    for (let i = 0; i < 60; i++) { const X = r() * c.width; x.strokeStyle = `rgba(${r() > .5 ? '45,26,12' : '180,130,85'},${.1 + r() * .14})`; x.lineWidth = .6 + r() * 1.4; x.beginPath(); x.moveTo(X, 0); for (let y = 0; y <= c.height; y += 16) x.lineTo(X + Math.sin(y * .04 + i * 1.7) * 3, y); x.stroke(); }
    return { map: tex(c), roughness: .45 };
  });
  M.bark = std('bark', () => {
    const c = canvas(64, 128), x = c.getContext('2d'), r = rng(71); x.fillStyle = '#6e6052'; x.fillRect(0, 0, 64, 128);
    for (let i = 0; i < 90; i++) { const X = r() * 64; x.strokeStyle = r() > .6 ? 'rgba(35,28,22,.45)' : 'rgba(170,155,135,.3)'; x.lineWidth = .7 + r() * 1.5; x.beginPath(); x.moveTo(X, 0); for (let y = 0; y <= 128; y += 8) x.lineTo(X + (r() - .5) * 2.5, y); x.stroke(); }
    return { map: tex(c), roughness: .9 };
  });
  M.bamboo = std('bamboo', () => ({ color: '#c9ab6f', roughness: .55 }));
  M.soil = std('soil', () => {
    const c = canvas(128, 128), x = c.getContext('2d'), r = rng(73); x.fillStyle = '#3d2b1f'; x.fillRect(0, 0, 128, 128);
    for (let i = 0; i < 2600; i++) { x.fillStyle = r() > .7 ? 'rgba(98,120,62,.55)' : r() > .5 ? 'rgba(20,14,10,.5)' : 'rgba(120,96,72,.45)'; x.fillRect(r() * 128, r() * 128, 1 + r() * 2.2, 1 + r() * 2.2); }
    return { map: tex(c), roughness: 1 };
  });
  M.moss = std('moss', () => {
    const c = canvas(128, 128), x = c.getContext('2d'), r = rng(79); x.fillStyle = '#4f6a31'; x.fillRect(0, 0, 128, 128);
    for (let i = 0; i < 2400; i++) { x.fillStyle = r() > .5 ? 'rgba(126,152,72,.55)' : 'rgba(38,54,22,.55)'; x.beginPath(); x.arc(r() * 128, r() * 128, .8 + r() * 1.6, 0, 7); x.fill(); }
    return { map: tex(c), roughness: 1 };
  });
  // pottery: lathe UV runs from the outer foot (v 0) over the rim to the inside (v 1): unglazed outside, glazed rim and inside
  function potteryMaterial(key, body, glaze, glazeFrom = .5) {
    return std('pot_' + key, () => {
      const c = canvas(64, px(256)), x = c.getContext('2d'), rc = canvas(64, px(256)), rx = rc.getContext('2d'), r = rng(key.length * 97), H = c.height;
      x.fillStyle = body; x.fillRect(0, 0, 64, H); rx.fillStyle = '#e6e6e6'; rx.fillRect(0, 0, 64, H);
      for (let i = 0; i < 900; i++) { x.fillStyle = r() > .5 ? 'rgba(60,24,10,.18)' : 'rgba(255,225,190,.14)'; x.fillRect(r() * 64, r() * H, 1 + r(), 1 + r()); }
      for (let y = 0; y < H; y += 3) { x.fillStyle = `rgba(255,255,255,${.03 * Math.sin(y * .35) + .02})`; x.fillRect(0, y, 64, 1); }   // throwing rings
      const g0 = H * (1 - glazeFrom);   // canvas y 0 = top of the texture = v 1 (inside)
      const gg = x.createLinearGradient(0, g0, 0, g0 - H * .06); gg.addColorStop(0, 'rgba(0,0,0,0)'); gg.addColorStop(1, glaze); x.fillStyle = gg; x.fillRect(0, g0 - H * .06, 64, H * .06); x.fillStyle = glaze; x.fillRect(0, 0, 64, g0 - H * .06);
      rx.fillStyle = '#4a4a4a'; rx.fillRect(0, 0, 64, g0 - H * .04);
      return { map: tex(c, { clamp: true }), roughnessMap: tex(rc, { srgb: false, clamp: true }), roughness: 1, side: THREE.DoubleSide };
    });
  }
  M.clay = potteryMaterial('clay', '#9b5534', '#4a2c1c', .55);           // red clay, dark brown glaze inside
  M.clayCream = potteryMaterial('cream', '#a7623d', '#d9cdb4', .55);      // red clay with a cream glaze
  M.clayBlue = potteryMaterial('blue', '#8f5233', '#3c5266', .5);        // bonsai pots: indigo-grey glaze
  M.clayRaw = std('clayRaw', () => ({ map: M.terracotta.map, roughness: .95, color: '#d7a587' }));
  // weave textures (basket and sample surfaces): one canvas per weave, tinted per material
  function weaveCanvas(kind, size = px(256)) {
    const c = canvas(size, size), x = c.getContext('2d'), n = 16, u = size / n, r = rng(kind.length * 31 + 7);
    x.fillStyle = '#5a5a5a'; x.fillRect(0, 0, size, size);
    for (let j = 0; j < n; j++) for (let i = 0; i < n; i++) {
      const over = kind === 'twill' ? ((i + j) % 4) < 2 : (i + j) % 2 === 0, l = 175 + Math.floor(r() * 60);
      const g = over ? x.createLinearGradient(i * u, 0, (i + 1) * u, 0) : x.createLinearGradient(0, j * u, 0, (j + 1) * u);
      g.addColorStop(0, `rgb(${l - 70},${l - 70},${l - 70})`); g.addColorStop(.5, `rgb(${l},${l},${l})`); g.addColorStop(1, `rgb(${l - 70},${l - 70},${l - 70})`);
      x.fillStyle = g;
      if (kind === 'lattice') { if ((i % 2) && (j % 2)) continue; x.fillRect(i * u + u * .08, j * u + u * .08, u * .84, u * .84); }
      else if (over) x.fillRect(i * u, j * u + u * .06, u, u * .88); else x.fillRect(i * u + u * .06, j * u, u * .88, u);
    }
    if (kind === 'coil') {   // coiled basketry: horizontal coils wrapped by short stitches
      x.fillStyle = '#5a5a5a'; x.fillRect(0, 0, size, size);
      for (let y = 0; y < size; y += u) { const g = x.createLinearGradient(0, y, 0, y + u); g.addColorStop(0, '#6e6e6e'); g.addColorStop(.5, '#e6e6e6'); g.addColorStop(1, '#6e6e6e'); x.fillStyle = g; x.fillRect(0, y + 1, size, u - 2);
        for (let s = (y / u % 2) * u * .7; s < size; s += u * 1.4) { x.fillStyle = 'rgba(40,40,40,.35)'; x.fillRect(s, y + 1, u * .18, u - 2); } }
    }
    if (kind === 'plait') {  // water hyacinth: thick braided rope rows
      x.fillStyle = '#4a4a4a'; x.fillRect(0, 0, size, size);
      for (let y = 0; y < size; y += u * 1.5) for (let s = 0; s < size; s += u) {
        for (const side of [-1, 1]) { x.save(); x.translate(s + u / 2, y + u * .75); x.rotate(side * .55); const g = x.createLinearGradient(-u * .5, 0, u * .5, 0); g.addColorStop(0, '#707070'); g.addColorStop(.5, '#e0e0e0'); g.addColorStop(1, '#707070'); x.fillStyle = g; x.fillRect(-u * .55, -u * .22, u * 1.1, u * .44); x.restore(); }
      }
    }
    return c;
  }
  const weave = {};
  for (const kind of ['plain', 'twill', 'coil', 'lattice', 'plait']) { const c = weaveCanvas(kind); weave[kind] = { map: c, normal: normalFromHeight(c, 3) }; }
  function wovenMaterial(key, kind, color, repeat = [3, 3]) {
    return std(`woven_${key}`, () => {
      const map = tex(weave[kind].map, { repeat }), normalMap = tex(weave[kind].normal, { srgb: false, repeat });
      return { color, map, normalMap, roughness: .92, side: THREE.DoubleSide };
    });
  }
  const FIBRE = { jute: '#c9a565', hogla: '#b9ab73', cane: '#d2a25e', hyacinth: '#8a6b47', bamboo: '#cbb27a', kaisa: '#bfa06a', handloom: '#e3d7c1' };
  // leaves: one grey leaf sprite per shape; instance colours give each leaf its own green
  function leafSprite(kind) {
    const s = 128, c = canvas(s, s), x = c.getContext('2d');
    x.clearRect(0, 0, s, s);
    const draw = (cx, cy, len, wid, ang) => {
      x.save(); x.translate(cx, cy); x.rotate(ang);
      const g = x.createLinearGradient(-wid, 0, wid, 0); g.addColorStop(0, '#9c9c9c'); g.addColorStop(.5, '#f2f2f2'); g.addColorStop(1, '#b4b4b4');
      x.fillStyle = g; x.beginPath(); x.moveTo(0, 0); x.bezierCurveTo(wid, -len * .15, wid * .9, -len * .75, 0, -len); x.bezierCurveTo(-wid * .9, -len * .75, -wid, -len * .15, 0, 0); x.fill();
      x.strokeStyle = 'rgba(255,255,255,.55)'; x.lineWidth = Math.max(1, wid * .08); x.beginPath(); x.moveTo(0, -len * .02); x.lineTo(0, -len * .95); x.stroke();
      x.restore();
    };
    if (kind === 'fine') {        // tamarind-like pinnate leaf: rachis with pairs of small leaflets
      x.strokeStyle = '#d8d8d8'; x.lineWidth = 2; x.beginPath(); x.moveTo(s / 2, s - 4); x.lineTo(s / 2, 6); x.stroke();
      for (let k = 0; k < 9; k++) { const y = s - 14 - k * 12.5; draw(s / 2, y, 18, 6, 1.25); draw(s / 2, y, 18, 6, -1.25); }
    } else if (kind === 'tulsi') {
      draw(s / 2, s - 4, s * .9, s * .32, 0);
      x.globalCompositeOperation = 'destination-out'; for (let k = 0; k < 9; k++) { const y = s - 20 - k * 10; x.beginPath(); x.arc(s / 2 + s * .27 * Math.sin((k + 2) / 12 * Math.PI), y, 3.5, 0, 7); x.fill(); x.beginPath(); x.arc(s / 2 - s * .27 * Math.sin((k + 2) / 12 * Math.PI), y, 3.5, 0, 7); x.fill(); }
      x.globalCompositeOperation = 'source-over';
    } else draw(s / 2, s - 4, s * .94, s * .3, 0);   // fig: elliptic leaf with a drip tip
    return c;
  }
  const leafMat = kind => std('leaf_' + kind, () => ({ map: tex(leafSprite(kind), { clamp: true }), alphaTest: .5, side: THREE.DoubleSide, roughness: .5, color: '#ffffff' }));
  const leafGeo = {};
  function leafGeometry(kind) { if (!leafGeo[kind]) { const g = new THREE.PlaneGeometry(1, 1); g.translate(0, .5, 0); geometries.push(g); leafGeo[kind] = g; } return leafGeo[kind]; }
  // leaves scattered over crowns or pads (ellipsoids), pushed towards the outside, facing up and out
  function scatterLeaves(parent, pads, { kind = 'fig', size = .05, hue = .27, sat = .42, light = .3, seed = 1 } = {}) {
    const total = pads.reduce((s, p) => s + p.n, 0), inst = new THREE.InstancedMesh(leafGeometry(kind), leafMat(kind), total);
    const r = rng(seed), m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler(0, 0, 0, 'YXZ'), sc = new THREE.Vector3(), P = new THREE.Vector3(), col = new THREE.Color();
    let k = 0;
    for (const pad of pads) for (let i = 0; i < pad.n; i++) {
      let u, v, w; do { u = r() * 2 - 1; v = r() * 2 - 1; w = r() * 2 - 1; } while (u * u + v * v + w * w > 1 || u * u + v * v + w * w < .01);
      const len = Math.hypot(u, v, w), out = Math.pow(len, .3) / len;
      P.set(pad.c[0] + u * out * pad.r[0], pad.c[1] + v * out * pad.r[1], pad.c[2] + w * out * pad.r[2]);
      e.set(-1.1 + v / len * .5 + (r() - .5) * .8, Math.atan2(u, w) + (r() - .5) * 1.2, (r() - .5) * .9); q.setFromEuler(e);
      const s = size * (.65 + r() * .7); sc.set(s * .55, s, s); m4.compose(P, q, sc); inst.setMatrixAt(k, m4);
      col.setHSL(hue + (r() - .5) * .05, sat * (.8 + r() * .35), light * (.75 + r() * .55)); inst.setColorAt(k, col); k++;
    }
    inst.instanceMatrix.needsUpdate = true; if (inst.instanceColor) inst.instanceColor.needsUpdate = true; inst.frustumCulled = false; parent.add(inst); return inst;
  }
  // text card: a small printed card (canvas) with a thin border
  function card(lines, { w = .16, h = .1, scale = 1, bg = '#f3ece0', ink = '#3c2a1e', accent = '#9c5534' } = {}) {
    const W = px(512 * scale), H = Math.round(W * h / w), c = canvas(W, H), x = c.getContext('2d');
    x.fillStyle = bg; x.fillRect(0, 0, W, H); x.strokeStyle = 'rgba(60,40,25,.25)'; x.lineWidth = W / 160; x.strokeRect(W / 80, W / 80, W - W / 40, H - W / 40);
    let y = H * .2;
    lines.forEach((ln, i) => { const big = i === 0, fs = (big ? W / 11 : W / 17) * (ln.size || 1); x.fillStyle = big ? ink : (ln.color || '#5b4636'); x.font = `${big ? 600 : 400} ${fs}px system-ui, -apple-system, 'Segoe UI', sans-serif`;
      x.textBaseline = 'top'; x.fillText(ln.t ?? ln, W * .07, y); y += fs * 1.35; if (big) { x.fillStyle = accent; x.fillRect(W * .07, y - fs * .1, W * .12, W / 140); y += fs * .25; } });
    return std('card_' + lines.map(l => l.t ?? l).join('|'), () => ({ map: tex(c, { clamp: true }), roughness: .8 }));
  }
  function standingCard(parent, lines, x, y, z, ry, opts = {}) {
    const w = opts.w || .16, h = opts.h || .1, g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = ry; parent.add(g);
    add(g, new THREE.PlaneGeometry(w, h), card(lines, opts), 0, h / 2 + .012, 0, -.18);
    box(g, M.oak, 0, 0, -.012, w * .9, .012, .04);
    return g;
  }

  // ---------------------------------------------------------------- object builders
  function plinth(parent, x, z, w, d, h, y = 0, mat = M.granite) { box(parent, mat, x, y, z, w, h, d); }
  function stoneGroup(parent, x, z, seed, specs) {
    for (const [dx, dz, r, sy, ry] of specs) add(parent, rockGeometry(r, seed + Math.round(r * 1000), 1, sy, .9), M.graniteRough, x + dx, 0, z + dz, 0, ry);
  }
  function bonsai(parent, { x, y, z, ry = 0, scale = 1, seed = 1, style = 'banyan', pot = M.clayBlue, kind = 'fig' }) {
    const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = ry; g.scale.setScalar(scale); parent.add(g);
    const r = rng(seed), J = a => (r() - .5) * a;
    add(g, lathe([[0, .004], [.13, 0], [.15, .012], [.16, .05], [.17, .062], [.158, .064], [.148, .022], [0, .022]], 40), pot);
    add(g, new THREE.CircleGeometry(.15, 32), M.moss, 0, .057, 0, -Math.PI / 2);
    const H = style === 'banyan' ? .46 : .42;
    const trunk = [[0, .05, 0], [.035 + J(.02), .13, J(.03)], [-.03 + J(.02), .22, J(.03)], [.025 + J(.02), .31, J(.03)], [J(.02), H, J(.02)]];
    add(g, taperedTube(trunk, .046, .013, 28, 10), M.bark);
    add(g, new THREE.CylinderGeometry(.045, .075, .035, 12), M.bark, 0, .07, 0);
    const curve = new THREE.CatmullRomCurve3(trunk.map(p => new THREE.Vector3(...p))), pads = [];
    for (let b = 0; b < 5; b++) {
      const t = .38 + b * .12, P = curve.getPointAt(Math.min(1, t)), a = b * 2.39 + J(.5), len = (.2 - b * .02) * (style === 'cascade' && b === 0 ? 1.6 : 1);
      const droop = style === 'cascade' && b === 0 ? -.16 : .02 + r() * .04;
      const tip = [P.x + Math.cos(a) * len, P.y + droop, P.z + Math.sin(a) * len], mid = [P.x + Math.cos(a) * len * .5, P.y + droop * .3 + .03, P.z + Math.sin(a) * len * .5];
      add(g, taperedTube([[P.x, P.y, P.z], mid, tip], .015 - b * .0015, .005, 10, 6), M.bark);
      pads.push({ c: [tip[0], tip[1] + .03, tip[2]], r: [.085 + r() * .035, .032 + r() * .012, .085 + r() * .035], n: kind === 'fine' ? 110 : 150 });
      if (style === 'banyan' && (b === 1 || b === 3)) add(g, taperedTube([[mid[0], mid[1] - .01, mid[2]], [mid[0] + .01, (mid[1] + .06) / 2, mid[2]], [mid[0], .062, mid[2]]], .0045, .003, 8, 5), M.bark);
    }
    const top = curve.getPointAt(1); pads.push({ c: [top.x, top.y + .04, top.z], r: [.1, .05, .1], n: kind === 'fine' ? 140 : 190 });
    scatterLeaves(g, pads, { kind, size: kind === 'fine' ? .05 : .03, hue: kind === 'fine' ? .25 : .29, sat: .48, light: .3, seed });
    return g;
  }
  function smallTree(parent, { x, z, seed = 3, height = 1.75, planter = 'terracotta' }) {
    const g = new THREE.Group(); g.position.set(x, 0, z); parent.add(g); const r = rng(seed), J = a => (r() - .5) * a;
    const pm = planter === 'terracotta' ? M.clayRaw : M.clay;
    add(g, lathe([[0, .01], [.17, 0], [.2, .04], [.215, .4], [.235, .425], [.235, .45], [.212, .45], [.2, .42], [0, .42]], 44), pm);
    add(g, new THREE.CircleGeometry(.2, 32), M.soil, 0, .43, 0, -Math.PI / 2);
    for (let s = 0; s < 3; s++) {
      const a = s * 2.1 + J(.4), b0 = [Math.cos(a) * .03, .43, Math.sin(a) * .03];
      add(g, taperedTube([b0, [Math.cos(a) * .05 + J(.03), .8, Math.sin(a) * .05 + J(.03)], [Math.cos(a) * .09 + J(.05), height * .72, Math.sin(a) * .09 + J(.05)]], .022, .009, 16, 7), M.bark);
    }
    scatterLeaves(g, [
      { c: [J(.08), height * .8, J(.08)], r: [.36, .3, .36], n: 520 },
      { c: [.16 + J(.05), height * .66, .05 + J(.05)], r: [.24, .2, .24], n: 240 },
      { c: [-.14 + J(.05), height * .9, -.07 + J(.05)], r: [.24, .2, .24], n: 240 },
    ], { kind: 'fig', size: .085, hue: .3, sat: .45, light: .27, seed: seed + 9 });
    return g;
  }
  // tableware in clay and wood
  function cup(parent, x, y, z, kind = 'tumbler', mat = M.clay) {
    if (kind === 'tumbler') return add(parent, lathe([[0, 0], [.029, 0], [.033, .005], [.037, .095], [.033, .095], [.03, .008], [0, .008]], 28), mat, x, y, z);
    if (kind === 'teacup') { const g = new THREE.Group(); g.position.set(x, y, z); parent.add(g); add(g, lathe([[0, 0], [.018, 0], [.02, .006], [.036, .03], [.042, .052], [.038, .052], [.032, .03], [.016, .01], [0, .01]], 28), mat); return g; }
    if (kind === 'mug') { const g = new THREE.Group(); g.position.set(x, y, z); parent.add(g); add(g, lathe([[0, 0], [.036, 0], [.039, .006], [.04, .09], [.036, .09], [.035, .008], [0, .008]], 28), mat);
      add(g, new THREE.TorusGeometry(.024, .006, 8, 16, Math.PI), mat, .04, .048, 0, 0, 0, -Math.PI / 2); return g; }
    if (kind === 'bottle') return add(parent, lathe([[0, 0], [.04, 0], [.052, .05], [.048, .1], [.02, .135], [.013, .2], [.017, .21], [.012, .21], [.009, .14], [0, .14]], 28), M.clayCream, x, y, z);   // a small surahi
    return null;
  }
  function jug(parent, x, y, z, ry = 0) {
    const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = ry; parent.add(g);
    add(g, lathe([[0, 0], [.05, 0], [.075, .04], [.08, .09], [.06, .14], [.042, .17], [.05, .2], [.045, .2], [.036, .17], [0, .16]], 36), M.clay);
    add(g, new THREE.TorusGeometry(.045, .008, 8, 18, Math.PI * 1.1), M.clay, .068, .12, 0, 0, 0, -Math.PI / 2 - .25); return g;
  }
  function teapot(parent, x, y, z, ry = 0) {
    const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = ry; parent.add(g);
    add(g, lathe([[0, 0], [.045, 0], [.07, .03], [.072, .06], [.05, .095], [.03, .1], [0, .1]], 36), M.clay);
    add(g, new THREE.SphereGeometry(.012, 12, 8), M.clay, 0, .108, 0);
    add(g, taperedTube([[.06, .04, 0], [.09, .07, 0], [.11, .1, 0]], .012, .006, 10, 8), M.clay);
    add(g, new THREE.TorusGeometry(.035, .007, 8, 18, Math.PI), M.clay, -.065, .055, 0, 0, 0, Math.PI / 2); return g;
  }
  function tray(parent, x, y, z, w, d, ry = 0) {
    const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = ry; parent.add(g);
    box(g, M.wood, 0, 0, 0, w, .012, d); for (const s of [-1, 1]) { box(g, M.wood, 0, .012, s * (d / 2 - .006), w, .022, .012); box(g, M.wood, s * (w / 2 - .006), .012, 0, .012, .022, d - .024); }
    return g;
  }
  function basket(parent, x, y, z, { r = .16, h = .26, kind = 'twill', fibre = 'jute', ry = 0, handles = false, partial = 1 } = {}) {
    const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = ry; parent.add(g);
    const mat = wovenMaterial(fibre + kind, kind, FIBRE[fibre], [Math.round(r * 40), Math.round(h * 30)]), H = h * partial;
    add(g, lathe([[0, .004], [r * .86, 0], [r, H * .12], [r * 1.04, H], [r * 1.0, H], [r * .95, H * .1], [0, .012]], 36), mat);
    add(g, new THREE.TorusGeometry(r * 1.02, .009, 8, 40), std('rim_' + fibre, () => ({ color: FIBRE[fibre], roughness: .8, map: tex(weave.coil.map, { repeat: [24, 1] }) })), 0, H, 0, Math.PI / 2);
    if (handles) for (const s of [-1, 1]) add(g, new THREE.TorusGeometry(.035, .007, 8, 16, Math.PI), M.oak, s * r * 1.02, H - .02, 0, 0, Math.PI / 2, 0);
    return g;
  }
  function swatch(parent, x, y, z, fibre, kind, size = .14, ry = 0) { return add(parent, new THREE.BoxGeometry(size, .008, size), wovenMaterial(`sw_${fibre}${kind}`, kind, FIBRE[fibre], [2, 2]), x, y + .004, z, 0, ry); }
  function tile(parent, x, y, z, size = .12, ry = 0) { return add(parent, new THREE.BoxGeometry(size, .014, size), M.terracotta, x, y + .007, z, 0, ry); }
  function bambooLamp(parent, x, y, z, { r = .13, h = .36, glow = 1 } = {}) {
    const g = new THREE.Group(); g.position.set(x, y, z); parent.add(g);
    const paper = std('paper_glow', () => { const c = canvas(128, 256), xx = c.getContext('2d'), rr = rng(83); xx.fillStyle = '#f2dfba'; xx.fillRect(0, 0, 128, 256);
      for (let i = 0; i < 260; i++) { xx.strokeStyle = `rgba(150,110,60,${.06 + rr() * .1})`; xx.lineWidth = .6; xx.beginPath(); const X = rr() * 128, Y = rr() * 256; xx.moveTo(X, Y); xx.lineTo(X + (rr() - .5) * 14, Y + (rr() - .5) * 14); xx.stroke(); }
      const t = tex(c); return { map: t, emissive: '#ffcf8a', emissiveMap: t, emissiveIntensity: .95, roughness: .9, side: THREE.DoubleSide }; });
    add(g, new THREE.CylinderGeometry(r * .92, r, h * .86, 32, 1, true), paper, 0, h * .5 + .03, 0);
    const slats = 16; for (let i = 0; i < slats; i++) { const a = i / slats * Math.PI * 2; box(g, M.bamboo, Math.cos(a) * (r + .006), .02, Math.sin(a) * (r + .006), .008, h, .006, -a); }
    for (const yy of [.03, h + .015]) add(g, new THREE.TorusGeometry(r + .007, .005, 6, 40), M.bamboo, 0, yy, 0, Math.PI / 2);
    add(g, new THREE.CylinderGeometry(r * .7, r * .8, .03, 24), M.wood, 0, .015, 0);
    if (glow) {
      if (!M.halo) { const c = canvas(128, 128), xx = c.getContext('2d'), gr = xx.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, 'rgba(255,200,130,.5)'); gr.addColorStop(1, 'rgba(255,200,130,0)'); xx.fillStyle = gr; xx.fillRect(0, 0, 128, 128);
        M.halo = new THREE.MeshBasicMaterial({ name: 'bel_halo', map: tex(c, { clamp: true }), transparent: true, depthWrite: false, blending: THREE.AdditiveBlending }); materials.push(M.halo); }
      add(g, new THREE.PlaneGeometry(r * 6, r * 6), M.halo, 0, .004, 0, -Math.PI / 2); }
    return g;
  }
  function pillowGeometry(w, h, t, seg = 16) {
    const pos = [], uv = [], index = [];
    for (const side of [1, -1]) for (let j = 0; j <= seg; j++) for (let i = 0; i <= seg; i++) {
      const u = i / seg, v = j / seg, a = 1 - Math.pow(Math.abs(2 * u - 1), 2.6), b = 1 - Math.pow(Math.abs(2 * v - 1), 2.6), pinch = 1 - .08 * (1 - a) * (1 - b);
      pos.push((u - .5) * w * pinch, (v - .5) * h * pinch, side * t / 2 * Math.pow(a * b, .55)); uv.push(side > 0 ? u : 1 - u, v);
    }
    const n = seg + 1;
    for (let s = 0; s < 2; s++) for (let j = 0; j < seg; j++) for (let i = 0; i < seg; i++) { const a = s * n * n + j * n + i, b = a + 1, c = a + n, d = c + 1; if (s === 0) index.push(a, b, d, a, d, c); else index.push(a, d, b, a, c, d); }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); g.setIndex(index); g.computeVertexNormals(); return g;
  }
  const handloomCushion = std('cushion_handloom', () => {
    const s = px(256), c = canvas(s, s), x = c.getContext('2d'); x.fillStyle = FIBRE.handloom; x.fillRect(0, 0, s, s);
    x.globalCompositeOperation = 'multiply'; x.fillStyle = x.createPattern(weave.plain.map, 'repeat'); x.globalAlpha = .35; x.fillRect(0, 0, s, s); x.globalAlpha = 1; x.globalCompositeOperation = 'source-over';
    for (const [y, col, wdt] of [[.16, '#3d5170', .05], [.24, '#9c5534', .015], [.76, '#9c5534', .015], [.84, '#3d5170', .05]]) { x.fillStyle = col; x.fillRect(0, s * y, s, s * wdt); }
    return { map: tex(c), roughness: .95 };
  });
  // instruments (simplified, self-made forms)
  function ektara(parent, x, y, z, ry = 0) {        // y = top of the instrument (hangs from the peg)
    const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = ry; parent.add(g);
    const gourd = std('gourd', () => ({ color: '#6b4426', roughness: .38 })), skin = std('skin', () => ({ color: '#d8c39a', roughness: .8, side: THREE.DoubleSide }));
    add(g, lathe([[.05, -.84], [.074, -.8], [.082, -.74], [.07, -.68], [.05, -.665]], 28), gourd);
    add(g, new THREE.CircleGeometry(.05, 24), skin, 0, -.84, 0, Math.PI / 2);
    for (const s of [-1, 1]) add(g, new THREE.BoxGeometry(.016, .66, .008), M.bamboo, s * .034, -.36, 0, 0, 0, s * .055);
    add(g, new THREE.CylinderGeometry(.009, .009, .09, 10), M.wood, 0, -.05, 0, 0, 0, Math.PI / 2);
    add(g, new THREE.CylinderGeometry(.0012, .0012, .79, 4), std('string', () => ({ color: '#d9d4c8', metalness: .6, roughness: .3 })), 0, -.445, .004);
    return g;
  }
  function dotara(parent, x, y, z, ry = 0) {
    const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = ry; parent.add(g);
    const wood = std('dotara_wood', () => ({ color: '#4e2f1b', roughness: .35 })), skin = std('skin', () => ({}));
    const bowl = add(g, new THREE.SphereGeometry(.1, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), wood, 0, -.68, 0, -Math.PI / 2); bowl.scale.set(1, .7, 1);
    add(g, new THREE.CircleGeometry(.1, 28), skin, 0, -.68, .002);
    add(g, new THREE.BoxGeometry(.045, .5, .03), wood, 0, -.35, -.01);
    add(g, new THREE.BoxGeometry(.03, .48, .004), std('fret', () => ({ color: '#b9b9b4', metalness: .8, roughness: .3 })), 0, -.34, .006);
    add(g, new THREE.TorusGeometry(.04, .012, 8, 16, Math.PI * 1.3), wood, .01, -.06, -.01, 0, 0, .4);
    for (let k = 0; k < 4; k++) add(g, new THREE.CylinderGeometry(.006, .006, .06, 8), M.wood, (k % 2 ? .03 : -.03), -.1 - Math.floor(k / 2) * .04, -.01, 0, 0, Math.PI / 2);
    for (let k = 0; k < 4; k++) add(g, new THREE.CylinderGeometry(.0009, .0009, .62, 4), std('string', () => ({})), -.009 + k * .006, -.42, .01);
    return g;
  }
  function banshi(parent, x, y, z, ry = 0) {        // horizontal, centred at x
    const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = ry; parent.add(g);
    const bam = std('banshi', () => { const c = canvas(256, 32), xx = c.getContext('2d'), rr = rng(91); xx.fillStyle = '#cdb27a'; xx.fillRect(0, 0, 256, 32); for (let i = 0; i < 30; i++) { xx.fillStyle = 'rgba(120,90,40,.15)'; xx.fillRect(rr() * 256, 0, 1, 32); } xx.fillStyle = '#8f6a35'; for (const s of [40, 190]) xx.fillRect(s, 0, 5, 32); return { map: tex(c, { clamp: true }), roughness: .5 }; });
    add(g, new THREE.CylinderGeometry(.013, .013, .52, 16), bam, 0, 0, 0, 0, 0, Math.PI / 2);
    for (let k = 0; k < 7; k++) add(g, new THREE.CircleGeometry(.0045, 10), std('hole', () => ({ color: '#1a120a', roughness: 1 })), (k === 0 ? -.2 : -.02 + k * .035), 0, .0131);
    return g;
  }
  function dhol(parent, x, y, z, ry = 0) {          // lying on its side, axis along local x, resting at y
    const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = ry; parent.add(g);
    const shell = std('dhol_shell', () => ({ color: '#7a3b22', roughness: .45 })), skin = std('dhol_skin', () => ({ color: '#d7c2a0', roughness: .85, side: THREE.DoubleSide })), rope = std('dhol_rope', () => ({ color: '#d9cdb2', roughness: .9 }));
    const body = add(g, lathe([[.125, -.21], [.15, -.12], [.158, 0], [.15, .12], [.125, .21]], 32), shell, 0, .16, 0, 0, 0, Math.PI / 2);
    for (const s of [-1, 1]) { add(g, new THREE.CircleGeometry(.13, 28), skin, s * .212, .16, 0, 0, s * Math.PI / 2); add(g, new THREE.TorusGeometry(.13, .008, 8, 32), rope, s * .208, .16, 0, 0, Math.PI / 2); }
    for (let k = 0; k < 12; k++) { const a = k / 12 * Math.PI * 2, b = (k + .5) / 12 * Math.PI * 2;
      add(g, taperedTube([[-.205, .16 + Math.sin(a) * .13, Math.cos(a) * .13], [0, .16 + Math.sin((a + b) / 2) * .16, Math.cos((a + b) / 2) * .16], [.205, .16 + Math.sin(b) * .13, Math.cos(b) * .13]], .003, .003, 8, 4), rope); }
    for (const s of [-1, 1]) box(g, M.wood, s * .12, -.0, 0, .04, .03, .2);   // cradle feet
    void body; return g;
  }

  // ---------------------------------------------------------------- Z01 Entrance lobby
  if (want('BEL_GATE_BONSAI')) {
    const g = item('BEL_GATE_BONSAI');   // approved potted tree F003/PL003: x 6.86-7.37, z 4.70-5.21
    plinth(g, 7.115, 4.955, .46, .46, .62);
    bonsai(g, { x: 7.115, y: .62, z: 4.955, ry: 2.4, seed: 7, style: 'banyan', pot: M.clayBlue });
  }
  if (want('BEL_LOBBY_STONES')) {
    const g = item('BEL_LOBBY_STONES');  // approved small planter F004/PL004: x 4.27-4.67, z 4.78-5.18
    box(g, std('slate', () => ({ color: '#3f3a36', roughness: .7 })), 4.47, 0, 4.98, .56, .012, .5);
    stoneGroup(g, 4.47, 4.98, 101, [[-.08, -.06, .17, .95, .3], [.13, .07, .12, .8, 1.4], [-.02, .15, .08, .7, 2.2]]);
  }
  if (want('BEL_EARTH_DESK')) {
    const g = item('BEL_EARTH_DESK');    // security desk F001: x 5.21-6.43, z 2.74-3.35; visitor face at z 3.35
    const front = std('terracotta_desk', () => ({ map: M.terracotta.map.clone(), normalMap: M.terracotta.normalMap.clone(), roughness: .86 }));
    front.map.repeat.set(3, 2.5); front.normalMap.repeat.set(3, 2.5); front.map.needsUpdate = front.normalMap.needsUpdate = true; textures.push(front.map, front.normalMap);
    box(g, front, 5.82, .03, 3.362, 1.16, .71, .016);
  }
  if (want('BEL_LOBBY_RELIEF')) {
    const g = item('BEL_LOBBY_RELIEF');  // free west wall (x 0) between the north wall and the stair foot (z 2.58)
    const W = px(768), H = Math.round(W * 1.05 / 1.62), hc = canvas(W, H), hx = hc.getContext('2d');
    hx.fillStyle = '#5a5a5a'; hx.fillRect(0, 0, W, H);
    const cols = 3, rows = 2, gw = W / cols, gh = H / rows;
    const raise = (fn) => { for (let k = 6; k >= 0; k--) { hx.save(); hx.fillStyle = hx.strokeStyle = `rgb(${130 + (6 - k) * 18},${130 + (6 - k) * 18},${130 + (6 - k) * 18})`; hx.lineWidth = 2 + k * 1.6; hx.lineJoin = hx.lineCap = 'round'; fn(k); hx.restore(); } };
    for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) {
      const X = i * gw + gw * .05, Y = j * gh + gh * .06, w = gw * .9, h = gh * .88; hx.fillStyle = '#909090'; hx.fillRect(X, Y, w, h); hx.fillStyle = '#7a7a7a'; hx.fillRect(X + w * .06, Y + h * .06, w * .88, h * .88);
      const cx = X + w / 2, cy = Y + h / 2, u = Math.min(w, h);
      const k = j * cols + i;
      raise(() => {
        hx.beginPath();
        if (k === 0) { hx.arc(cx, cy, u * .2, 0, 7); hx.stroke(); for (let a = 0; a < 12; a++) { const A = a / 12 * Math.PI * 2; hx.moveTo(cx + Math.cos(A) * u * .28, cy + Math.sin(A) * u * .28); hx.lineTo(cx + Math.cos(A) * u * .38, cy + Math.sin(A) * u * .38); } hx.stroke(); }
        else if (k === 1) { hx.moveTo(cx - u * .36, cy + u * .05); hx.quadraticCurveTo(cx, cy + u * .26, cx + u * .36, cy + u * .05); hx.lineTo(cx - u * .36, cy + u * .05); hx.moveTo(cx, cy + u * .05); hx.lineTo(cx, cy - u * .3); hx.lineTo(cx + u * .22, cy - .02 * u); hx.lineTo(cx, cy - .02 * u); hx.stroke(); for (let w2 = 0; w2 < 2; w2++) { hx.beginPath(); for (let s = -.4; s <= .4; s += .05) hx.lineTo(cx + s * u, cy + u * (.3 + w2 * .08) + Math.sin(s * 18) * u * .02); hx.stroke(); } }
        else if (k === 2) { for (let p = 0; p < 8; p++) { const A = p / 8 * Math.PI * 2; hx.moveTo(cx, cy); hx.quadraticCurveTo(cx + Math.cos(A - .35) * u * .3, cy + Math.sin(A - .35) * u * .3, cx + Math.cos(A) * u * .36, cy + Math.sin(A) * u * .36); hx.quadraticCurveTo(cx + Math.cos(A + .35) * u * .3, cy + Math.sin(A + .35) * u * .3, cx, cy); } hx.stroke(); hx.beginPath(); hx.arc(cx, cy, u * .07, 0, 7); hx.stroke(); }
        else if (k === 3) { for (const s of [-1, 1]) { hx.beginPath(); hx.ellipse(cx, cy + s * u * .14, u * .28, u * .08, 0, 0, 7); hx.moveTo(cx + u * .28, cy + s * u * .14); hx.lineTo(cx + u * .38, cy + s * u * .14 - u * .07); hx.lineTo(cx + u * .38, cy + s * u * .14 + u * .07); hx.closePath(); hx.stroke(); } }
        else if (k === 4) { for (let s = -2; s <= 2; s++) { hx.moveTo(cx + s * u * .05, cy + u * .36); hx.quadraticCurveTo(cx + s * u * .06, cy - u * .05, cx + s * u * .14, cy - u * .32); for (let q = 0; q < 4; q++) { const t = .55 + q * .1; hx.moveTo(cx + s * u * .08 * t * 1.6, cy - u * .1 - q * u * .05); hx.lineTo(cx + s * u * .08 * t * 1.6 + u * .04, cy - u * .15 - q * u * .05); } } hx.stroke(); }
        else { hx.ellipse(cx, cy, u * .18, u * .1, -.2, 0, 7); hx.moveTo(cx + u * .16, cy - u * .06); hx.lineTo(cx + u * .26, cy - u * .1); hx.moveTo(cx - u * .16, cy + u * .02); hx.lineTo(cx - u * .38, cy - u * .12); hx.lineTo(cx - u * .36, cy + u * .02); hx.closePath(); hx.moveTo(cx + u * .02, cy + u * .1); hx.lineTo(cx, cy + u * .26); hx.moveTo(cx - u * .3, cy + u * .26); hx.lineTo(cx + u * .3, cy + u * .26); hx.stroke(); }
      });
    }
    const map = canvas(W, H), mx = map.getContext('2d'), hd = hx.getImageData(0, 0, W, H).data, md = mx.createImageData(W, H), r = rng(5);
    for (let i = 0; i < W * H; i++) { const v = hd[i * 4] / 255, n = (r() - .5) * .05, k = .62 + .5 * v + n; md.data[i * 4] = Math.min(255, 178 * k); md.data[i * 4 + 1] = Math.min(255, 96 * k); md.data[i * 4 + 2] = Math.min(255, 62 * k); md.data[i * 4 + 3] = 255; }
    mx.putImageData(md, 0, 0);
    const mat = std('relief', () => ({ map: tex(map, { clamp: true }), normalMap: tex(normalFromHeight(hc, 4), { srgb: false, clamp: true }), roughness: .9 }));
    add(g, new THREE.PlaneGeometry(1.62, 1.05), mat, .035, 1.6, 1.43, 0, Math.PI / 2);
    box(g, std('relief_back', () => ({ color: '#7d4128', roughness: .9 })), .02, 1.075, 1.43, .028, 1.05, 1.62);
  }

  // ---------------------------------------------------------------- Z02 Reception
  if (want('BEL_RECEPTION_TREE')) { const g = item('BEL_RECEPTION_TREE'); smallTree(g, { x: 8.125, z: 5.845, seed: 13, height: 1.72 }); }   // approved F015/PL015: x 7.87-8.38, z 5.59-6.10
  if (want('BEL_RECEPTION_ALOE')) {
    const g = item('BEL_RECEPTION_ALOE');  // approved F016/PL016: x 13.72-14.12, z 5.69-6.10
    const rock = rockGeometry(.2, 211, 1.1, .55, .95); add(g, rock, M.graniteRough, 13.92, 0, 5.9);
    const pot = new THREE.Group(); pot.position.set(13.92, rock.boundingBox.max.y - .015, 5.9); g.add(pot);
    add(pot, lathe([[0, .005], [.08, 0], [.105, .03], [.115, .17], [.125, .19], [.11, .19], [.1, .17], [0, .17]], 32), M.clayRaw);
    add(pot, new THREE.CircleGeometry(.1, 24), M.soil, 0, .175, 0, -Math.PI / 2);
    const aloe = std('aloe', () => { const c = canvas(32, 128), x = c.getContext('2d'), r = rng(17); const gr = x.createLinearGradient(0, 128, 0, 0); gr.addColorStop(0, '#7f9b5a'); gr.addColorStop(1, '#5e7d48'); x.fillStyle = gr; x.fillRect(0, 0, 32, 128);
      for (let i = 0; i < 40; i++) { x.fillStyle = 'rgba(230,240,215,.55)'; x.beginPath(); x.ellipse(r() * 32, r() * 128, 1.6, .9, 0, 0, 7); x.fill(); } return { map: tex(c, { clamp: true }), roughness: .45, side: THREE.DoubleSide }; });
    for (let k = 0; k < 14; k++) {
      const a = k * 2.399, tilt = .25 + (k % 3) * .22, len = .26 + (k % 4) * .05, geo = new THREE.ConeGeometry(.018, len, 6, 4, true); geo.translate(0, len / 2, 0); geo.scale(1.6, 1, .55);
      const leaf = add(pot, geo, aloe, Math.cos(a) * .02, .175, Math.sin(a) * .02); leaf.rotation.set(0, -a, 0); leaf.rotateZ(tilt);
    }
  }
  if (want('BEL_INSTRUMENTS')) {
    const g = item('BEL_INSTRUMENTS');   // console F014: x 10.69-12.53, z 0.03-0.45, top 0.787; north wall face z 0.0; books x 11.06, frame x 12.10 on the console
    box(g, M.oak, 11.6, 1.97, .03, 1.5, .05, .03);
    for (const pxx of [10.98, 11.6]) add(g, new THREE.CylinderGeometry(.006, .006, .05, 8), std('brass', () => ({ color: '#a57c3c', metalness: .85, roughness: .32 })), pxx, 1.98, .065, Math.PI / 2);
    ektara(g, 10.98, 1.97, .1, 0);
    dotara(g, 11.6, 1.97, .085, 0);
    for (const pxx of [11.95, 12.33]) add(g, new THREE.CylinderGeometry(.005, .005, .05, 8), std('brass', () => ({})), pxx, 1.56, .045, Math.PI / 2);
    banshi(g, 12.14, 1.578, .045, 0);
    dhol(g, 11.55, .787 + .015, .25, 0);
    const lbl = card(['Rural instruments', 'Ektara, dotara, banshi, dhol', 'Makers to be identified and credited'], { w: .22, h: .1 });
    add(g, new THREE.PlaneGeometry(.22, .1), lbl, 12.14, 1.36, .012);
  }
  if (want('BEL_TEA_CLAY')) {
    const g = item('BEL_TEA_CLAY');      // lounge coffee table top 0.406 (teacup prop 9.831, 4.699); reception desk transaction top 1.067 (tray prop 12.446, 3.607)
    tray(g, 9.84, .406, 4.71, .3, .22, .2);
    teapot(g, 9.79, .418, 4.71, .2);
    for (const [dx, dz] of [[.09, -.055], [.1, .05]]) cup(g, 9.84 + dx, .418, 4.71 + dz, 'teacup', M.clayCream);
    tray(g, 12.446, 1.067, 3.607, .22, .16, Math.PI / 2); cup(g, 12.446, 1.079, 3.607, 'teacup', M.clayCream);
  }

  // ---------------------------------------------------------------- Z03 Visitor passage: Sun wall (west, x 9.32) and Earth wall (east, x 10.67)
  if (want('BEL_SUN_WALL')) {
    // solid east wall (face x 10.669) between the guest WC doors D32 (z -4.86..-4.03) and D33 (z -1.56..-0.72);
    // read from reception (south) to the experience centre (north): 1 at z -1.89 ... 4 at z -3.71
    const g = item('BEL_SUN_WALL');
    const panels = [
      { z: -1.885, title: '1 · Sun', lines: ['Where the energy', 'story starts.'] },
      { z: -2.495, title: '2 · Generation', lines: ['Roof panels, if the', 'structure and area', 'allow. Size and', 'output: to be designed.'] },
      { z: -3.105, title: '3 · Use and storage', lines: ['Daytime use first;', 'a battery keeps', 'some for later.', 'Capacity: to be', 'assessed against', 'the real demand.'] },
      { z: -3.715, title: '4 · Operations', lines: ['Grid and backup stay', 'connected and are', 'shown until measured', 'data proves otherwise.'], dash: true },
    ];
    const PW = .55, PH = .95, W = px(440), H = Math.round(W * PH / PW);
    panels.forEach((p, idx) => {
      const c = canvas(W, H), x = c.getContext('2d'), r = rng(300 + idx); x.fillStyle = '#f1e8d8'; x.fillRect(0, 0, W, H);
      for (let i = 0; i < 420; i++) { x.strokeStyle = `rgba(150,115,70,${.04 + r() * .06})`; x.lineWidth = .7; x.beginPath(); const X = r() * W, Y = r() * H; x.moveTo(X, Y); x.lineTo(X + (r() - .5) * 16, Y + (r() - .5) * 16); x.stroke(); }
      x.textBaseline = 'top'; x.fillStyle = '#3c2a1e'; x.font = `600 ${W / 11}px system-ui, 'Segoe UI', sans-serif`; x.fillText(p.title, W * .08, H * .05);
      x.fillStyle = '#9c5534'; x.fillRect(W * .08, H * .05 + W / 8.5, W * .16, W / 90);
      const cx = W / 2, cy = H * .36, u = W * .3; x.lineWidth = W / 80; x.lineCap = 'round';
      if (idx === 0) { for (let k = 0; k < 7; k++) { x.strokeStyle = k % 2 ? '#c8873f' : '#b05a32'; x.beginPath(); x.arc(cx, cy, u * (.16 + k * .1), 0, 7); x.stroke(); } x.setLineDash([W / 50, W / 70]); x.strokeStyle = '#b05a32'; for (let a = 0; a < 16; a++) { const A = a / 16 * Math.PI * 2; x.beginPath(); x.moveTo(cx + Math.cos(A) * u * .9, cy + Math.sin(A) * u * .9); x.lineTo(cx + Math.cos(A) * u * 1.2, cy + Math.sin(A) * u * 1.2); x.stroke(); } x.setLineDash([]); }
      if (idx === 1) { x.strokeStyle = '#3d5170'; x.fillStyle = '#c9d3dc'; for (let k = 0; k < 2; k++) { x.save(); x.translate(cx - u * .55 + k * u * 1.1, cy); x.transform(1, 0, -.35, .8, 0, 0); x.fillRect(-u * .45, -u * .32, u * .9, u * .55); x.strokeRect(-u * .45, -u * .32, u * .9, u * .55); x.beginPath(); for (let q = 1; q < 3; q++) { x.moveTo(-u * .45 + q * u * .3, -u * .32); x.lineTo(-u * .45 + q * u * .3, u * .23); } x.stroke(); x.restore(); } x.strokeStyle = '#6b5340'; x.beginPath(); x.moveTo(cx - u * 1.3, cy + u * .45); x.lineTo(cx + u * 1.3, cy + u * .45); x.stroke(); }
      if (idx === 2) { x.strokeStyle = '#4f6a31'; x.beginPath(); x.moveTo(cx - u, cy - u * .35); x.lineTo(cx + u * .6, cy - u * .35); x.stroke(); x.beginPath(); x.moveTo(cx + u * .4, cy - u * .52); x.lineTo(cx + u * .65, cy - u * .35); x.lineTo(cx + u * .4, cy - u * .18); x.stroke();
        x.strokeStyle = '#3d5170'; x.strokeRect(cx - u * .55, cy, u * 1.1, u * .55); x.fillStyle = '#4f6a31'; x.fillRect(cx - u * .48, cy + u * .07, u * .55, u * .41); x.fillStyle = '#3d5170'; x.fillRect(cx + u * .55, cy + u * .17, u * .09, u * .2); }
      if (idx === 3) { x.strokeStyle = '#3c2a1e'; x.strokeRect(cx - u * 1.05, cy - u * .2, u * 1.0, u * .7); x.beginPath(); x.moveTo(cx - u * 1.05, cy - u * .2); x.lineTo(cx - u * .55, cy - u * .55); x.lineTo(cx - u * .05, cy - u * .2); x.stroke();
        x.setLineDash([W / 40, W / 60]); x.strokeStyle = '#7a7a7a'; x.beginPath(); x.moveTo(cx + u * .05, cy + u * .15); x.lineTo(cx + u * .62, cy + u * .15); x.stroke(); x.setLineDash([]);
        x.strokeStyle = '#7a7a7a'; x.beginPath(); x.moveTo(cx + u * .7, cy + u * .5); x.lineTo(cx + u * .88, cy - u * .5); x.lineTo(cx + u * 1.06, cy + u * .5); x.moveTo(cx + u * .76, cy); x.lineTo(cx + u * 1.0, cy); x.stroke();
        x.fillStyle = '#6a6a6a'; x.font = `400 ${W / 20}px system-ui, sans-serif`; x.fillText('grid', cx + u * .62, cy + u * .58); x.fillText('backup', cx + u * .02, cy + u * .22); }
      x.fillStyle = '#4a3a2c'; x.font = `400 ${W / 15}px system-ui, 'Segoe UI', sans-serif`;
      p.lines.forEach((ln, i) => x.fillText(ln, W * .08, H * .58 + i * W / 12.5));
      if (p.dash) {   // the dashboard frame: no numbers until a verified feed exists
        const X = W * .06, Y = H * .58 + p.lines.length * W / 12.5 + W / 40, w = W * .88, hh = H - Y - H * .035;
        x.fillStyle = '#2b2b2b'; x.fillRect(X, Y, w, hh); x.fillStyle = '#e9e1d2'; x.font = `600 ${W / 22}px system-ui, sans-serif`; x.fillText('ENERGY DATA', X + w * .06, Y + hh * .08); x.fillText('NOT CONNECTED', X + w * .06, Y + hh * .08 + W / 18);
        x.font = `400 ${W / 24}px system-ui, sans-serif`; ['Solar now  — kW', 'Grid today  — kWh'].forEach((t, i) => x.fillText(t, X + w * .06, Y + hh * (.42 + i * .17)));
        x.fillStyle = '#d9a35f'; x.font = `600 ${W / 26}px system-ui, sans-serif`; x.fillText('Concept demonstration —', X + w * .06, Y + hh * .74); x.fillText('not live factory data', X + w * .06, Y + hh * .74 + W / 22);
      }
      const mat = std('sun_' + idx, () => ({ map: tex(c, { clamp: true }), roughness: .85 }));
      add(g, new THREE.PlaneGeometry(PW, PH), mat, 10.652, 1.475, p.z, 0, -Math.PI / 2);
      box(g, M.oak, 10.658, .985, p.z, .02, .018, PW + .03); box(g, M.oak, 10.658, 1.955, p.z, .02, .018, PW + .03);
    });
    const tc = canvas(px(1024), px(80)), tx = tc.getContext('2d'); tx.fillStyle = '#b88c5c'; tx.fillRect(0, 0, tc.width, tc.height);
    tx.fillStyle = '#4a2f1b'; tx.font = `600 ${tc.height * .5}px system-ui, 'Segoe UI', sans-serif`; tx.textBaseline = 'middle'; tx.fillText('Designed for a Solar-Powered Future', tc.width * .04, tc.height * .52);
    add(g, new THREE.PlaneGeometry(2.38, .19), std('sun_title', () => ({ map: tex(tc, { clamp: true }), roughness: .6 })), 10.656, 2.09, -2.8, 0, -Math.PI / 2);
  }
  if (want('BEL_EARTH_WALL')) {
    // the solid 1.22 m base of the glazed west wall (face x 9.323; glass above y 1.22), clear of door D10 (z -1.46..-0.27)
    const g = item('BEL_EARTH_WALL');
    const band = std('terracotta_band', () => ({ map: M.terracotta.map.clone(), normalMap: M.terracotta.normalMap.clone(), roughness: .88 }));
    band.map.repeat.set(7, 2.2); band.normalMap.repeat.set(7, 2.2); band.map.needsUpdate = band.normalMap.needsUpdate = true; textures.push(band.map, band.normalMap);
    box(g, band, 9.334, .04, -3.45, .018, 1.12, 3.8);
    box(g, M.oak, 9.37, 1.16, -3.45, .07, .025, 3.8);
    [['#8f4a2c', 'clay'], [FIBRE.jute, 'jute'], [FIBRE.hogla, 'hogla'], [FIBRE.cane, 'cane'], ['#d9c58e', 'rice straw']].forEach(([col, nm], i) => {
      const z = -4.9 + i * .78; add(g, lathe([[0, 0], [.04, 0], [.06, .035], [.055, .04], [.035, .012], [0, .012]], 24), M.clay, 9.37, 1.185, z);
      add(g, new THREE.CircleGeometry(.05, 20), std('earth_' + i, () => ({ color: col, roughness: 1, map: i ? tex(weave.plain.map) : M.soil.map })), 9.37, 1.215, z, -Math.PI / 2);
      add(g, new THREE.PlaneGeometry(.1, .03), card([nm], { w: .1, h: .03, scale: .4 }), 9.4065, 1.165, z, 0, Math.PI / 2);
    });
  }

  // ---------------------------------------------------------------- Z30 Experience centre
  if (want('BEL_EARTH_TO_PRODUCT')) {
    const g = item('BEL_EARTH_TO_PRODUCT'); const T = .2032, ZC = -8.5, front = -8.02;   // plinth F021: x 11.05-14.35, z -9.07..-7.95, top 0.20
    // 1 raw material: a jute bundle, a hogla bundle, a clay lump on a board, a cane coil
    const jute = std('jute_fibre', () => { const c = canvas(64, 256), x = c.getContext('2d'), r = rng(23); x.fillStyle = FIBRE.jute; x.fillRect(0, 0, 64, 256); for (let i = 0; i < 160; i++) { x.strokeStyle = r() > .5 ? 'rgba(255,235,190,.35)' : 'rgba(110,80,35,.3)'; x.lineWidth = .8; x.beginPath(); const X = r() * 64; x.moveTo(X, 0); x.lineTo(X + (r() - .5) * 4, 256); x.stroke(); } return { map: tex(c), roughness: .95 }; });
    add(g, new THREE.CylinderGeometry(.045, .065, .52, 20, 1), jute, 11.3, T + .26, ZC - .2);
    add(g, new THREE.TorusGeometry(.052, .008, 6, 20), std('band', () => ({ color: '#6b4a2b', roughness: .9 })), 11.3, T + .3, ZC - .2, Math.PI / 2);
    for (let k = 0; k < 7; k++) add(g, new THREE.BoxGeometry(.62, .006, .022), wovenMaterial('hogla_leaf', 'plain', FIBRE.hogla, [6, 1]), 11.42, T + .004 + k * .006, ZC + .14 + (k - 3) * .018, 0, (k - 3) * .03);
    box(g, M.wood, 11.25, T, ZC + .3, .22, .02, .16); add(g, rockGeometry(.07, 401, 1.2, .6, 1), std('wet_clay', () => ({ color: '#8f5134', roughness: .55 })), 11.25, T + .02, ZC + .3);
    const helix = new THREE.CatmullRomCurve3(Array.from({ length: 60 }, (_, i) => { const a = i / 59 * Math.PI * 2 * 3; return new THREE.Vector3(Math.cos(a) * .09, i / 59 * .03, Math.sin(a) * .09); }));
    add(g, new THREE.TubeGeometry(helix, 180, .005, 6, false), std('cane_coil', () => ({ color: FIBRE.cane, roughness: .5 })), 11.5, T + .006, ZC - .3);
    // 2 craft technique: a small frame with warp threads and a half-woven hogla mat; a coiled basket in progress
    const fr = new THREE.Group(); fr.position.set(12.0, T, ZC - .1); fr.rotation.y = .15; g.add(fr);
    for (const s of [-1, 1]) { box(fr, M.oak, s * .22, 0, 0, .025, .5, .025); box(fr, M.oak, s * .22, 0, 0, .025, .015, .16); }
    box(fr, M.oak, 0, .1, 0, .465, .02, .02); box(fr, M.oak, 0, .48, 0, .465, .02, .02);
    for (let k = 0; k < 15; k++) add(fr, new THREE.CylinderGeometry(.0012, .0012, .36, 4), std('warp', () => ({ color: '#e7dcc4', roughness: .8 })), -.196 + k * .028, .3, 0);
    add(fr, new THREE.PlaneGeometry(.4, .16), wovenMaterial('hogla_mat', 'twill', FIBRE.hogla, [3, 1.2]), 0, .19, .002);
    basket(g, 12.08, T, ZC + .22, { r: .13, h: .22, kind: 'coil', fibre: 'jute', partial: .55 });
    // 3 prototype: one basket form with a paper tag
    basket(g, 12.72, T, ZC - .05, { r: .15, h: .25, kind: 'twill', fibre: 'hogla', handles: true });
    add(g, new THREE.PlaneGeometry(.05, .03), card(['prototype'], { w: .05, h: .03, scale: .4 }), 12.86, T + .2, ZC + .11, 0, .4);
    // 4 testing: the same form beside its (empty) test card
    basket(g, 13.36, T, ZC - .05, { r: .15, h: .25, kind: 'twill', fibre: 'hogla', handles: true, ry: .6 });
    standingCard(g, ['Test step', 'Moisture, mould, strength', 'Records to be added'], 13.36, T, ZC + .25, 0, { w: .16, h: .1 });
    // 5 collection: nested baskets, a handloom cushion, a bamboo and paper lamp
    basket(g, 13.9, T, ZC - .18, { r: .17, h: .2, kind: 'plait', fibre: 'hyacinth' });
    basket(g, 13.9, T + .02, ZC - .18, { r: .12, h: .2, kind: 'plait', fibre: 'hyacinth' });
    add(g, pillowGeometry(.4, .4, .12), handloomCushion, 14.08, T + .2, ZC + .12, -.25, -.5, 0);
    bambooLamp(g, 14.2, T, ZC - .22, { r: .09, h: .3 });
    ['1 · Raw material', '2 · Craft technique', '3 · Prototype', '4 · Testing', '5 · Collection'].forEach((t, i) =>
      standingCard(g, [t], 11.38 + i * .665, T, front - .03, 0, { w: .17, h: .055 }));
    standingCard(g, ['From earth to product', 'Illustrative objects', 'Real samples and records to follow'], 11.13, T, -8.06, -.5, { w: .2, h: .11 });
  }
  if (want('BEL_MATERIAL_TABLE')) {
    const g = item('BEL_MATERIAL_TABLE'); const TOP = .863;   // material table top 0.863; free north strip z -9.0..-8.7 east of x 17.7; notebook 19.15 and tape 19.79 at z -8.865
    [['jute', 'twill', 'Jute'], ['hogla', 'plain', 'Hogla'], ['cane', 'lattice', 'Cane'], ['hyacinth', 'plait', 'Water hyacinth'], ['bamboo', 'twill', 'Bamboo'], ['kaisa', 'coil', 'Kaisa grass']].forEach(([fibre, kind, name], i) => {
      const x = 17.78 + i * .19; swatch(g, x, TOP, -8.86, fibre, kind, .15, (i - 2.5) * .04);
      add(g, new THREE.PlaneGeometry(.12, .035), card([name], { w: .12, h: .035, scale: .5 }), x, TOP + .002, -8.74, -Math.PI / 2);
    });
    for (let i = 0; i < 3; i++) tile(g, 16.98 + i * .14, TOP, -8.18, .1, (i - 1) * .1);
    add(g, new THREE.PlaneGeometry(.12, .035), card(['Terracotta'], { w: .12, h: .035, scale: .5 }), 17.12, TOP + .002, -8.105, -Math.PI / 2);
  }
  if (want('BEL_COLLECTION_BAYS')) {
    // bays F017-F020 (measured in the scene): base top 0.1016, top shelf 0.... 1.8592, green back z -10.7251, front edge z -10.1347,
    // brass rail y 1.676 at z -10.44; the garments and hangers are hidden on this route (hideParts)
    const g = item('BEL_COLLECTION_BAYS'); const BASE = .1016, SHELF = 1.8592, BACK = -10.7251, RAIL = 1.676, RZ = -10.44;
    const textile = (key, draw) => std('tx_' + key, () => { const c = canvas(px(256), px(256)), x = c.getContext('2d'); draw(x, c.width, c.height); x.globalCompositeOperation = 'multiply'; x.globalAlpha = .3; x.fillStyle = x.createPattern(weave.plain.map, 'repeat'); x.fillRect(0, 0, c.width, c.height); x.globalAlpha = 1; x.globalCompositeOperation = 'source-over'; return { map: tex(c), roughness: .95, side: THREE.DoubleSide }; });
    const T = {
      khadi: textile('khadi_buti', (x, w, h) => { x.fillStyle = '#e6dccb'; x.fillRect(0, 0, w, h); x.fillStyle = '#7d8a9c'; for (let j = 0; j < 6; j++) for (let i = 0; i < 6; i++) { const cx = (i + .5 + (j % 2) * .5) * w / 6, cy = (j + .5) * h / 6; x.beginPath(); for (let k = 0; k < 4; k++) { const A = k / 4 * Math.PI * 2; x.ellipse(cx + Math.cos(A) * w * .02, cy + Math.sin(A) * w * .02, w * .012, w * .006, A, 0, 7); } x.fill(); } x.fillStyle = '#3d5170'; x.fillRect(0, h * .9, w, h * .03); }),
      indigo: textile('indigo', (x, w, h) => { x.fillStyle = '#2f4363'; x.fillRect(0, 0, w, h); x.fillStyle = '#e8e0cf'; for (const y of [.12, .16, .84, .88]) x.fillRect(0, h * y, w, h * .012); }),
      patch: textile('kantha_patch', (x, w, h) => { const r = rng(77), cols = ['#8f4a3a', '#3d5170', '#c9a565', '#6f7a4c', '#d9cdb4', '#a36b4f', '#4a4a52', '#b88c5c']; for (let j = 0; j < 5; j++) { let X = 0; while (X < w) { const ww = w * (.12 + r() * .2); x.fillStyle = cols[Math.floor(r() * cols.length)]; x.fillRect(X, j * h / 5, ww, h / 5); X += ww; } }
        x.strokeStyle = 'rgba(245,238,225,.85)'; x.lineWidth = w / 220; x.setLineDash([w / 70, w / 110]); for (let y = h / 20; y < h; y += h / 14) { x.beginPath(); x.moveTo(0, y); x.lineTo(w, y + (r() - .5) * 3); x.stroke(); } x.setLineDash([]); }),
      rope: textile('rope_multi', (x, w, h) => { const cols = ['#8f4a3a', '#d9cdb4', '#3d5170', '#c9a565', '#6f7a4c']; for (let j = 0; j < 16; j++) { x.fillStyle = cols[j % cols.length]; x.fillRect(0, j * h / 16, w, h / 16); } }),
    };
    function drape(parent, x, w, h, mat) {   // a throw hung over the rail: soft vertical folds, rolled over the bar
      const geo = new THREE.PlaneGeometry(w, h, 24, 10), pp = geo.attributes.position;
      for (let i = 0; i < pp.count; i++) { const X = pp.getX(i), Y = pp.getY(i), down = .5 - Y / h; pp.setZ(i, (.008 + .02 * down) * Math.sin((X / w + .5) * 5 * Math.PI) + .004); }
      geo.computeVertexNormals(); add(parent, geo, mat, x, RAIL - h / 2 - .01, RZ + .015);
      add(parent, new THREE.CylinderGeometry(.016, .016, w, 16, 1, false, 0, Math.PI), mat, x, RAIL, RZ, 0, 0, Math.PI / 2);
    }
    const folded = (parent, x, y, z, mat, n = 3) => { for (let k = 0; k < n; k++) box(parent, mat, x + (k % 2) * .008, y + k * .045, z, .34, .042, .26, (k - 1) * .03); };
    const vase = (parent, x, y, z, prof, mat = M.clayRaw) => add(parent, lathe(prof, 36), mat, x, y, z);
    const VASE_A = [[0, 0], [.06, 0], [.1, .08], [.105, .16], [.06, .26], [.045, .3], [.055, .32], [.045, .32], [.035, .3], [0, .29]];
    const VASE_B = [[0, 0], [.05, 0], [.075, .05], [.06, .12], [.07, .2], [.06, .2], [.05, .12], [0, .11]];
    const header = (x0, name, sub) => standingCard(g, [name, sub, 'Illustrative collection · concept'], x0 + .2, BASE, -10.22, 0, { w: .2, h: .1 });
    // 1 Bengal Nordic (x 9.79-12.36)
    let x0 = 9.7917; drape(g, x0 + .55, .62, .72, T.khadi); drape(g, x0 + 1.32, .55, .64, T.indigo);
    add(g, pillowGeometry(.42, .42, .12), handloomCushion, x0 + .55, BASE + .2, -10.6, -.25, .12, 0);
    add(g, pillowGeometry(.4, .4, .12), T.indigo, x0 + 1.0, BASE + .19, -10.62, -.25, -.1, 0);
    basket(g, x0 + 1.75, BASE, -10.45, { r: .16, h: .3, kind: 'twill', fibre: 'jute' }); folded(g, x0 + 2.2, BASE, -10.45, T.khadi, 2);
    folded(g, x0 + .55, SHELF, -10.45, T.indigo); vase(g, x0 + 1.35, SHELF, -10.45, VASE_B, M.clayCream); basket(g, x0 + 2.0, SHELF, -10.45, { r: .12, h: .16, kind: 'twill', fibre: 'jute' });
    header(x0, 'Bengal Nordic', 'Handloom textiles, quiet colour');
    // 2 River to Home (x 12.53-15.10)
    x0 = 12.5349; add(g, new THREE.PlaneGeometry(.72, .8, 1, 1), wovenMaterial('hogla_panel', 'twill', FIBRE.hogla, [5, 6]), x0 + .95, RAIL - .42, RZ + .012);
    add(g, new THREE.CylinderGeometry(.016, .016, .72, 12), M.oak, x0 + .95, RAIL, RZ, 0, 0, Math.PI / 2);
    basket(g, x0 + .45, BASE, -10.42, { r: .2, h: .32, kind: 'plait', fibre: 'hyacinth' });
    basket(g, x0 + 1.05, BASE, -10.42, { r: .17, h: .4, kind: 'twill', fibre: 'hogla', handles: true });
    add(g, new THREE.CylinderGeometry(.065, .065, .7, 24), wovenMaterial('hogla_roll', 'plain', FIBRE.hogla, [4, 1]), x0 + 1.75, BASE + .065, -10.45, 0, 0, Math.PI / 2);
    vase(g, x0 + 2.25, BASE, -10.45, VASE_A);
    basket(g, x0 + .6, SHELF, -10.45, { r: .15, h: .14, kind: 'twill', fibre: 'hogla' }); basket(g, x0 + .6, SHELF + .015, -10.45, { r: .11, h: .14, kind: 'twill', fibre: 'hogla' });
    vase(g, x0 + 1.4, SHELF, -10.45, VASE_B); vase(g, x0 + 1.68, SHELF, -10.45, VASE_A.map(([r, y]) => [r * .7, y * .8]));
    basket(g, x0 + 2.2, SHELF, -10.45, { r: .13, h: .12, kind: 'coil', fibre: 'kaisa' });
    header(x0, 'River to Home', 'Hogla, water hyacinth, terracotta');
    // 3 Second Life Bangladesh (x 16.14-18.25)
    x0 = 16.1417; drape(g, x0 + .75, .8, .8, T.patch);
    const ropeBasket = (x, y, z, r, h) => { const gg = new THREE.Group(); gg.position.set(x, y, z); g.add(gg); add(gg, lathe([[0, .004], [r * .86, 0], [r, h * .12], [r * 1.04, h], [r, h], [r * .95, h * .1], [0, .012]], 36), T.rope); add(gg, new THREE.TorusGeometry(r * 1.02, .012, 8, 36), T.rope, 0, h, 0, Math.PI / 2); };
    ropeBasket(x0 + .4, BASE, -10.42, .17, .28); ropeBasket(x0 + .85, BASE, -10.42, .13, .22);
    add(g, pillowGeometry(.4, .4, .12), T.patch, x0 + 1.45, BASE + .19, -10.62, -.25, 0, 0);
    folded(g, x0 + 1.85, BASE, -10.45, T.patch, 3);
    [['#8f4a3a', -.12], ['#3d5170', 0], ['#c9a565', .12]].forEach(([cc, dx]) => add(g, new THREE.CylinderGeometry(.03, .045, .17, 24), std('yarn_rec_' + cc, () => ({ color: cc, roughness: .9, map: tex(weave.coil.map, { repeat: [3, 6] }) })), x0 + .7 + dx, SHELF + .085, -10.45));
    ropeBasket(x0 + 1.55, SHELF, -10.45, .1, .13);
    header(x0, 'Second Life Bangladesh', 'Garment offcuts, kantha patchwork');
    // 4 Future of Bengal (x 18.43-20.54), next to the doors to merchandising and the boardroom
    x0 = 18.4277; const pend = new THREE.Group(); pend.position.set(x0 + 1.0, 1.08, -10.44); g.add(pend);
    add(pend, new THREE.CylinderGeometry(.002, .002, RAIL - 1.08 - .3, 4), std('cord', () => ({ color: '#2a2a2a', roughness: .6 })), 0, .3 + (RAIL - 1.08 - .3) / 2, 0);
    bambooLamp(pend, 0, 0, 0, { r: .12, h: .3, glow: 0 });
    const stool = new THREE.Group(); stool.position.set(x0 + .5, BASE, -10.42); g.add(stool);
    add(stool, new THREE.CylinderGeometry(.17, .17, .04, 28), std('jute_composite', () => { const c = canvas(128, 128), xx = c.getContext('2d'), rr = rng(97); xx.fillStyle = '#a98b58'; xx.fillRect(0, 0, 128, 128); for (let i = 0; i < 700; i++) { xx.strokeStyle = `rgba(${rr() > .5 ? '80,55,25' : '230,205,150'},.35)`; xx.lineWidth = .8; xx.beginPath(); const X = rr() * 128, Y = rr() * 128, A = rr() * 6.3; xx.moveTo(X, Y); xx.lineTo(X + Math.cos(A) * 8, Y + Math.sin(A) * 8); xx.stroke(); } return { map: tex(c), roughness: .7 }; }), 0, .43, 0);
    for (let k = 0; k < 3; k++) { const a = k / 3 * Math.PI * 2; add(stool, new THREE.CylinderGeometry(.014, .016, .43, 10), M.bamboo, Math.cos(a) * .11, .215, Math.sin(a) * .11, Math.sin(a) * .08, 0, -Math.cos(a) * .08); }
    bambooLamp(g, x0 + 1.65, BASE, -10.45, { r: .1, h: .34 });
    for (let k = 0; k < 3; k++) box(g, std('jute_composite', () => ({})), x0 + .45 + k * .14, SHELF, -10.5, .12, .12, .012, 0);
    vase(g, x0 + 1.4, SHELF, -10.45, VASE_A.map(([r, y]) => [r * .8, y * .9]), M.clay);
    header(x0, 'Future of Bengal', 'Experiments in bamboo, cane, jute');
  }
  if (want('BEL_FUTURE_LAMP')) {
    const g = item('BEL_FUTURE_LAMP');   // approved potted tree F029/PL029: x 21.34-21.84, z -7.87..-7.37
    plinth(g, 21.59, -7.62, .46, .46, .86);
    bambooLamp(g, 21.59, .86, -7.62, { r: .15, h: .42 });
    standingCard(g, ['Future of Bengal', 'Experimental lamp: bamboo and handmade paper', 'Prototype, not tested'], 21.41, .86, -7.5, -Math.PI / 2 + .35, { w: .2, h: .09 });
  }
  if (want('BEL_WATER_KOLSHI')) {
    const g = item('BEL_WATER_KOLSHI');  // counter top 0.889, x 10.91-20.07, z -6.08..-5.56 (room side -z); identity water point at x 11.40 is excluded on this route
    const T = .889, X = 13.0; add(g, new THREE.TorusGeometry(.085, .02, 10, 28), M.wood, X, T + .02, -5.84, Math.PI / 2);
    add(g, lathe([[0, 0], [.07, 0], [.12, .05], [.135, .13], [.12, .2], [.07, .245], [.05, .28], [.062, .3], [.055, .305], [.042, .28], [0, .27]], 40), M.clay, X, T + .015, -5.84);
    tray(g, X + .28, T, -5.84, .22, .16, 0); for (const dx of [-.06, 0, .06]) cup(g, X + .28 + dx, T + .012, -5.84, 'tumbler', M.clayCream);
    standingCard(g, ['Drinking water', 'Source stated by the client: deep tube well', 'Laboratory results: none yet', 'Only dated reports will be shown'], X + .52, T, -5.8, Math.PI, { w: .2, h: .12 });
  }

  // ---------------------------------------------------------------- Z08 Boardroom
  if (want('BEL_BOARD_SAMPLES')) {
    const g = item('BEL_BOARD_SAMPLES'); const T = .749;   // table centre line z -2.845 (identity review trays excluded on this route)
    for (const [x, ry] of [[16.3, 0], [18.33, Math.PI]]) {
      const t = tray(g, x, T, -2.845, .38, .24, ry);
      swatch(t, -.12, .012, -.03, 'jute', 'twill', .1, .1); swatch(t, -.01, .012, .03, 'hogla', 'plain', .1, -.1); tile(t, .1, .012, -.04, .09, .2);
      basket(t, .12, .012, .06, { r: .045, h: .06, kind: 'coil', fibre: 'kaisa' });
    }
  }
  if (want('BEL_BOARD_BONSAI')) {
    const g = item('BEL_BOARD_BONSAI');  // approved planter F050/PL050: x 12.50-12.90, z -5.16..-4.75
    const jt = std('jute_rope', () => { const c = canvas(64, 64), x = c.getContext('2d'); x.fillStyle = FIBRE.jute; x.fillRect(0, 0, 64, 64); for (let y = 0; y < 64; y += 4) { x.fillStyle = 'rgba(90,60,25,.35)'; x.fillRect(0, y, 64, 1.2); x.fillStyle = 'rgba(255,240,200,.25)'; x.fillRect(0, y + 2, 64, 1); } return { map: tex(c, { repeat: [3, 14] }), roughness: .95 }; });
    add(g, new THREE.CylinderGeometry(.17, .19, .6, 28), jt, 12.7, .3, -4.955);
    add(g, new THREE.CylinderGeometry(.2, .2, .025, 28), M.wood, 12.7, .612, -4.955);
    bonsai(g, { x: 12.7, y: .625, z: -4.955, ry: .8, seed: 29, style: 'informal', kind: 'fine', pot: M.clay, scale: .9 });
  }

  // ---------------------------------------------------------------- Z18 Global Design Studio
  if (want('BEL_STUDIO_SUN_SHELF')) {
    const g = item('BEL_STUDIO_SUN_SHELF');   // in front of W10 (x 33.8, z -20.40..-17.50); trend table ends at x 32.72; bay F185 starts at z -17.27
    const X0 = 33.25, X1 = 33.57, Z0 = -20.15, Z1 = -17.85, H = .55, xm = (X0 + X1) / 2;
    for (const z of [Z0 + .15, Z1 - .15]) box(g, M.granite, xm, 0, z, X1 - X0, H - .045, .26);
    box(g, M.oak, xm, H - .045, (Z0 + Z1) / 2, X1 - X0, .045, Z1 - Z0);
    footprint(X0 - .02, Z0 - .02, X1 + .02, Z1 + .02);
    bonsai(g, { x: xm, y: H, z: -19.75, ry: .4, seed: 41, style: 'banyan', pot: M.clayBlue, scale: .82 });
    bonsai(g, { x: xm, y: H, z: -19.0, ry: 2.2, seed: 43, style: 'cascade', kind: 'fine', pot: M.clay, scale: .78 });
    bonsai(g, { x: xm, y: H, z: -18.3, ry: 4.1, seed: 47, style: 'informal', pot: M.clayBlue, scale: .76 });
    const tp = new THREE.Group(); tp.position.set(xm, H, -17.98); g.add(tp);
    add(tp, lathe([[0, .005], [.06, 0], [.075, .02], [.08, .13], [.088, .145], [.075, .145], [.07, .13], [0, .13]], 28), M.clayRaw);
    add(tp, new THREE.CircleGeometry(.072, 20), M.soil, 0, .135, 0, -Math.PI / 2);
    for (let s = 0; s < 4; s++) add(tp, taperedTube([[0, .13, 0], [Math.cos(s * 1.6) * .03, .22, Math.sin(s * 1.6) * .03], [Math.cos(s * 1.6) * .05, .3, Math.sin(s * 1.6) * .05]], .004, .002, 8, 5), std('tulsi_stem', () => ({ color: '#5b4a3a', roughness: .8 })));
    scatterLeaves(tp, [{ c: [0, .27, 0], r: [.09, .07, .09], n: 170 }], { kind: 'tulsi', size: .035, hue: .3, sat: .4, light: .28, seed: 53 });
    standingCard(g, ['Sunning shelf', 'The bonsai take turns in daylight', 'Tulsi: traditionally kept in Bengali homes'], X0 + .07, H, -18.65, -Math.PI / 2, { w: .18, h: .09 });
  }
  if (want('BEL_STUDIO_TREE')) { const g = item('BEL_STUDIO_TREE'); smallTree(g, { x: 33.02, z: -22.355, seed: 19, height: 1.7 }); }   // approved F186/PL186: x 32.77-33.27, z -22.61..-22.10
  if (want('BEL_COCREATION')) {
    const g = item('BEL_COCREATION'); const T = .7493;   // presentation table F175: x 30.25-31.47, z -18.29..-15.24; notebooks at x 31.105, mugs at x 30.581 (z -15.911, -17.617)
    basket(g, 30.9, T, -16.75, { r: .11, h: .18, kind: 'coil', fibre: 'jute' });
    basket(g, 30.9, T, -16.35, { r: .09, h: .14, kind: 'twill', fibre: 'hogla', ry: .5 });
    [['cane', 'lattice'], ['hyacinth', 'plait'], ['jute', 'plain'], ['bamboo', 'twill']].forEach(([f, k], i) => swatch(g, 30.52 + (i % 2) * .155, T, -16.95 + Math.floor(i / 2) * .18, f, k, .13, (i - 1.5) * .12));
    const sk = canvas(px(384), px(512)), sx = sk.getContext('2d'); sx.fillStyle = '#f4efe4'; sx.fillRect(0, 0, sk.width, sk.height);
    sx.strokeStyle = '#3c2a1e'; sx.lineWidth = sk.width / 180; const U = sk.width;
    for (let k = 0; k < 3; k++) { const cx = U * (.25 + (k % 2) * .5), cy = U * (.3 + Math.floor(k / 2) * .55), w = U * .17, h = U * (.14 + k * .03);
      sx.beginPath(); sx.ellipse(cx, cy - h / 2, w, w * .25, 0, 0, 7); sx.moveTo(cx - w, cy - h / 2); sx.lineTo(cx - w * .8, cy + h / 2); sx.lineTo(cx + w * .8, cy + h / 2); sx.lineTo(cx + w, cy - h / 2); sx.stroke();
      for (let q = 1; q < 4; q++) { sx.beginPath(); sx.moveTo(cx - w + q * w * .05, cy - h / 2 + q * h / 4); sx.lineTo(cx + w - q * w * .05, cy - h / 2 + q * h / 4); sx.stroke(); } }
    sx.fillStyle = '#3c2a1e'; sx.font = `400 ${U / 22}px system-ui, sans-serif`; sx.fillText('Basket forms · sketch (illustrative)', U * .06, sk.height * .95);
    add(g, new THREE.PlaneGeometry(.21, .28), std('sketch', () => ({ map: tex(sk, { clamp: true }), roughness: .9 })), 30.98, T + .002, -17.25, -Math.PI / 2, 0, .12);
    const fan = new THREE.Group(); fan.position.set(30.62, T + .004, -17.3); g.add(fan);
    ['#b4613c', '#c9a565', '#3d5170', '#4f6a31', '#d9cdb4', '#7a3b22', '#8a6b47'].forEach((col, i) => add(fan, new THREE.BoxGeometry(.03, .002, .17), std('fan_' + i, () => ({ color: col, roughness: .8 })), 0, i * .0021, -.07, 0, (i - 3) * .14));
  }

  // ---------------------------------------------------------------- clay and wood in place of every drinkware prop on the route
  if (want('BEL_CLAY_DRINKWARE') && drinkware.length) {
    const g = item('BEL_CLAY_DRINKWARE');
    for (const d of drinkware) {
      if (zones && !zones.includes(d.zone)) continue;
      const [x, y, z] = d.position;
      if (d.type === 'glass') cup(g, x, y, z, 'tumbler');
      else if (d.type === 'mug') cup(g, x, y, z, 'mug').rotation.y = d.rotationY || 0;
      else if (d.type === 'teacup') cup(g, x, y, z, 'teacup', M.clayCream);
      else if (d.type === 'bottle') cup(g, x, y, z, 'bottle');
      else if (d.type === 'jug') jug(g, x, y, z, d.rotationY || 0);
      else if (d.type === 'tray') tray(g, x, y, z, .22, .16, d.rotationY || 0);
    }
  }

  // ---------------------------------------------------------------- bookkeeping
  group.traverse(o => { if (o.isMesh) { o.castShadow = false; o.receiveShadow = false; o.userData.conceptLayer = true; } });
  const pixels = textures.reduce((s, t) => s + (t.image?.width || 0) * (t.image?.height || 0), 0);
  const stats = { items: items.length, meshes: 0, instancedLeaves: 0, textures: textures.length, textureMB: Math.round(pixels * 4 * 1.33 / 1e5) / 10 };
  group.traverse(o => { if (o.isInstancedMesh) stats.instancedLeaves += o.count; else if (o.isMesh) stats.meshes++; });
  function blocksMovement(x, z, radius = .15) { return footprints.some(([x0, z0, x1, z1]) => x > x0 - radius && x < x1 + radius && z > z0 - radius && z < z1 + radius); }
  return {
    group, stats, items: items.map(i => ({ id: i.id, zone: i.zone, note: i.note })), footprints,
    textures: () => textures, blocksMovement,
    dispose() { geometries.forEach(g => g.dispose()); materials.forEach(m => m.dispose()); textures.forEach(t => t.dispose()); },
  };
}
