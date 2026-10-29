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
  // the design wing in every option (increment 3): the labs behind the glass of the studio street are the exhibit
  { id: 'BEL_MAKING_LINE', zone: 'Z22', note: 'The making line on the solid wall of the design-wing entrance (the corridor walls are glass): one River to Home basket in six steps on oak ledges, from hogla leaves to the collection. Illustrative objects; real samples and dated records replace them.' },
  { id: 'BEL_MATERIALS_LIBRARY', zone: 'Z15', note: 'The living materials library: eight labelled boxes of natural materials on the low shelf (jute, hogla, cane, bamboo, water hyacinth, kaisa grass, coconut shell, terracotta) and Material Passport cards on the review table, with fields still to be documented. The D65 colour booth and the approved fabric library stay.' },
  { id: 'BEL_TEST_LAB', zone: 'Z16', note: 'Materials lab: a moisture and mould test set-up on the post-processing bench (sealed sample boxes, a scale, a moisture meter) and an empty test log. Methods to be agreed with an accredited laboratory; no results are shown. The 3D printers stay for trims and moulds.' },
  { id: 'BEL_PROTOTYPE_WORKSHOP', zone: 'Z17', note: 'Prototype workshop: cane and bamboo prototyping on the pattern table (a basket on its mould, split bamboo, a steam-bent hoop and hand tools) under a dust-extraction hood marked "to be engineered", and a steam-bending jig. The sample machines and forms stay.' },
  // option A only (full conversion): shown on this route if the merchandising and accounts teams move; the owner decides
  { id: 'BEL_UTHAN', zone: 'Z07', note: 'Option A only. The Green Uthan: a Bengali courtyard in Merchandising, with a bot-tola seat of handmade terracotta around the steel column, two small fig trees and a banyan bonsai under grow lights (this room has no daylight), split-granite stone seats and an open split-bamboo canopy (fire treatment and smoke-detector coverage to be checked). Natural jute carpet over the whole room.' },
  { id: 'BEL_ARTISAN_CORNER', zone: 'Z07', note: 'Option A only. Artisan corner in the Uthan, by invitation and never as a spectacle: a Chakma back-strap loom (bain) shown only with the consent and participation of Chakma weavers, a Marma weaving and basketry stand (the same consent rule), a nakshi kantha frame, cane basketry and painted terracotta on a sitalpati mat. Quiet, clean crafts only; dusty work stays in the prototype workshop.' },
  { id: 'BEL_ROOMSET_LIVING', zone: 'Z07', note: 'Option A only. Bengal Nordic living room-set: a mango-wood sofa in handloom, a cane armchair, a jute rug, a bamboo and paper lamp and a framed kantha. Illustrative concept, not products on sale.' },
  { id: 'BEL_ROOMSET_DINING', zone: 'Z07', note: 'Option A only. River to Home dining room-set: a mango-wood table with cane chairs on a hogla rug, clay tableware on hogla mats, a cane pendant and a sideboard with terracotta. Illustrative concept.' },
  { id: 'BEL_ROOMSET_BEDROOM', zone: 'Z07', note: 'Option A only. Second Life Bangladesh bedroom room-set: a kantha patchwork quilt made from garment offcuts, a cane headboard and a rag rug. Illustrative concept.' },
  { id: 'BEL_ROOMSET_HOSPITALITY', zone: 'Z07', note: 'Option A only. Future of Bengal hospitality corner for hotel buyers: cane lounge chairs, a bamboo and jute table, dried kash flowers in clay and a large nakshi kantha by a rural embroiderer (placeholder; to be commissioned, paid and credited).' },
  { id: 'BEL_ACADEMY', zone: 'Z06', note: 'Option A only. The design education academy inside the existing glass accounts suite: 20 seats shown at mango-wood tables, a demonstration bench with a hands camera, a mobile screen, a pin-up board and a materials shelf; the discussion room becomes the tutor room. Capacity is set by the fire engineer, not by this drawing.' },
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
  M.graniteSplit = std('granite_split', () => ({ map: M.granite.map, normalMap: M.granite.normalMap, roughness: .8, flatShading: true, color: '#b3aba4' }));   // quarried, split faces
  M.clayRaw = std('clayRaw', () => {   // unglazed fired clay: warm, mottled, faint throwing rings
    const c = canvas(64, px(256)), x = c.getContext('2d'), r = rng(57); x.fillStyle = '#a65b38'; x.fillRect(0, 0, 64, c.height);
    for (let i = 0; i < 40; i++) { const g = x.createRadialGradient(0, 0, 0, 0, 0, 1), cx = r() * 64, cy = r() * c.height, rr = 6 + r() * 26; g.addColorStop(0, r() > .5 ? 'rgba(70,28,12,.18)' : 'rgba(230,170,120,.16)'); g.addColorStop(1, 'rgba(0,0,0,0)'); x.setTransform(rr, 0, 0, rr, cx, cy); x.fillStyle = g; x.fillRect(-1, -1, 2, 2); x.setTransform(1, 0, 0, 1, 0, 0); }
    for (let y = 0; y < c.height; y += 3) { x.fillStyle = `rgba(255,235,210,${.025 + .025 * Math.sin(y * .4)})`; x.fillRect(0, y, 64, 1); }
    return { map: tex(c), roughness: .93 }; });
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
  // one GPU texture per weave: clones share its source and differ only in repeat (and the material's tint)
  const clone = t => { const c = t.clone(); c.needsUpdate = true; textures.push(c); return c; };
  const weaveBase = {};
  const weaveMap = (kind, repeat = [1, 1], which = 'map') => { const k = kind + which; if (!weaveBase[k]) weaveBase[k] = tex(weave[kind][which], { srgb: which === 'map' }); const t = clone(weaveBase[k]); t.repeat.set(...repeat); return t; };
  function wovenMaterial(key, kind, color, repeat = [3, 3]) {
    return std(`woven_${key}`, () => {
      const map = weaveMap(kind, repeat), normalMap = weaveMap(kind, repeat, 'normal');
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
    const W = px(320 * scale), H = Math.round(W * h / w), c = canvas(W, H), x = c.getContext('2d');   // ~2,000 px per metre of card: legible up close, light on memory
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
  // quarried granite (split faces, slightly eased edges), never river-rounded stone
  function graniteBlock(r, seed, sy = .8) {
    const g = new THREE.IcosahedronGeometry(r, 1), p = g.attributes.position, n = noise3(seed), seen = new Map();
    for (let i = 0; i < p.count; i++) {
      const key = `${p.getX(i).toFixed(4)},${p.getY(i).toFixed(4)},${p.getZ(i).toFixed(4)}`;
      if (!seen.has(key)) { const x = p.getX(i) / r, y = p.getY(i) / r, z = p.getZ(i) / r, d = 1 + .28 * n(x * 1.7 + 3, y * 1.7, z * 1.7); seen.set(key, [x * d * r, Math.max(y * sy * d * r, -r * sy * .5), z * d * r]); }
      p.setXYZ(i, ...seen.get(key));
    }
    g.computeVertexNormals(); g.computeBoundingBox(); g.translate(0, -g.boundingBox.min.y, 0); g.computeBoundingBox(); return g;
  }
  function stoneGroup(parent, x, z, seed, specs) {
    for (const [dx, dz, r, sy, ry] of specs) add(parent, graniteBlock(r, seed + Math.round(r * 1000), sy), M.graniteSplit, x + dx, 0, z + dz, 0, ry);
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
      pads.push({ c: [tip[0], tip[1] + .03, tip[2]], r: [.085 + r() * .035, .034 + r() * .012, .085 + r() * .035], n: kind === 'fine' ? 190 : 260 });
      if (style === 'banyan' && (b === 1 || b === 3)) add(g, taperedTube([[mid[0], mid[1] - .01, mid[2]], [mid[0] + .01, (mid[1] + .06) / 2, mid[2]], [mid[0], .062, mid[2]]], .0045, .003, 8, 5), M.bark);
    }
    const top = curve.getPointAt(1); pads.push({ c: [top.x, top.y + .04, top.z], r: [.1, .055, .1], n: kind === 'fine' ? 240 : 320 });
    scatterLeaves(g, pads, { kind, size: kind === 'fine' ? .05 : .032, hue: kind === 'fine' ? .26 : .29, sat: .58, light: .18, seed });
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
    ], { kind: 'fig', size: .085, hue: .3, sat: .55, light: .2, seed: seed + 9 });
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
    add(g, new THREE.TorusGeometry(r * 1.02, .009, 8, 40), std('rim_' + fibre, () => ({ color: FIBRE[fibre], roughness: .8, map: weaveMap('coil', [24, 1]) })), 0, H, 0, Math.PI / 2);
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
    bonsai(g, { x: 7.115, y: .62, z: 4.955, ry: 2.4, seed: 7, style: 'banyan', pot: M.clayBlue, scale: 1.25 });
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
    // six plaques on the free west wall (face x 0.0) between the north wall and the stair foot (z 2.58); a placeholder for
    // the work of a rural terracotta artist, to be commissioned, paid and credited (motifs: sun, river boat, shapla, fish, rice, doel)
    const g = item('BEL_LOBBY_RELIEF'), C = px(256), R = Math.round(C * .9), hc = canvas(C * 3, R * 2), hx = hc.getContext('2d');
    hx.fillStyle = '#5c5c5c'; hx.fillRect(0, 0, hc.width, hc.height);
    const soft = on => { if ('filter' in hx) hx.filter = on ? `blur(${Math.max(1, C / 140)}px)` : 'none'; };
    const raised = (shade, draw) => { hx.save(); soft(true); hx.fillStyle = `rgb(${shade},${shade},${shade})`; hx.beginPath(); draw(); hx.fill(); hx.restore(); };
    const carve = (draw, w = C / 90) => { hx.save(); soft(false); hx.strokeStyle = 'rgb(110,110,110)'; hx.lineWidth = w; hx.lineCap = 'round'; hx.beginPath(); draw(); hx.stroke(); hx.restore(); };
    for (let k = 0; k < 6; k++) {
      const X = (k % 3) * C, Y = Math.floor(k / 3) * R, cx = X + C / 2, cy = Y + R / 2, u = C;
      hx.fillStyle = '#9a9a9a'; hx.fillRect(X, Y, C, R); hx.fillStyle = '#7e7e7e'; hx.fillRect(X + C * .07, Y + R * .07, C * .86, R * .86);
      if (k === 0) { raised(200, () => hx.arc(cx, cy, u * .17, 0, 7)); for (let a = 0; a < 12; a++) { const A = a / 12 * Math.PI * 2; raised(185, () => { hx.moveTo(cx + Math.cos(A - .12) * u * .21, cy + Math.sin(A - .12) * u * .21); hx.lineTo(cx + Math.cos(A) * u * .36, cy + Math.sin(A) * u * .36); hx.lineTo(cx + Math.cos(A + .12) * u * .21, cy + Math.sin(A + .12) * u * .21); }); }
        carve(() => { for (let a = 0; a < 8; a++) { const A = a / 8 * Math.PI * 2; hx.moveTo(cx, cy); hx.lineTo(cx + Math.cos(A) * u * .13, cy + Math.sin(A) * u * .13); } }); }
      if (k === 1) { raised(195, () => { hx.moveTo(cx - u * .36, cy + u * .04); hx.quadraticCurveTo(cx, cy + u * .24, cx + u * .36, cy + u * .04); hx.quadraticCurveTo(cx, cy + u * .12, cx - u * .36, cy + u * .04); });
        raised(205, () => { hx.moveTo(cx - u * .02, cy + u * .06); hx.lineTo(cx - u * .02, cy - u * .32); hx.quadraticCurveTo(cx + u * .2, cy - u * .14, cx + u * .22, cy + u * .02); });
        for (let w = 0; w < 2; w++) raised(170, () => { for (let t = -.42; t <= .42; t += .02) hx.lineTo(cx + t * u, cy + u * (.27 + w * .09) + Math.sin(t * 22) * u * .018); for (let t = .42; t >= -.42; t -= .02) hx.lineTo(cx + t * u, cy + u * (.30 + w * .09) + Math.sin(t * 22) * u * .018); });
        carve(() => { for (let q = 1; q < 4; q++) { hx.moveTo(cx - u * .02, cy - u * .32 + q * u * .09); hx.lineTo(cx + u * .05 * q, cy - u * .32 + q * u * .09 + u * .03); } }); }
      if (k === 2) { for (let pt = 0; pt < 8; pt++) { const A = pt / 8 * Math.PI * 2 - Math.PI / 2; raised(190, () => { hx.ellipse(cx + Math.cos(A) * u * .17, cy + Math.sin(A) * u * .17, u * .17, u * .065, A, 0, 7); }); }
        raised(215, () => hx.arc(cx, cy, u * .08, 0, 7)); carve(() => { for (let pt = 0; pt < 8; pt++) { const A = pt / 8 * Math.PI * 2 - Math.PI / 2; hx.moveTo(cx + Math.cos(A) * u * .09, cy + Math.sin(A) * u * .09); hx.lineTo(cx + Math.cos(A) * u * .3, cy + Math.sin(A) * u * .3); } }); }
      if (k === 3) { for (const sgn of [-1, 1]) { const fy = cy + sgn * u * .13; raised(195, () => { hx.ellipse(cx - u * .04, fy, u * .27, u * .085, 0, 0, 7); }); raised(185, () => { hx.moveTo(cx + u * .2, fy); hx.lineTo(cx + u * .38, fy - u * .09); hx.lineTo(cx + u * .38, fy + u * .09); });
        carve(() => { for (let q = 0; q < 5; q++) { hx.moveTo(cx - u * .12 + q * u * .07, fy - u * .06); hx.quadraticCurveTo(cx - u * .09 + q * u * .07, fy, cx - u * .12 + q * u * .07, fy + u * .06); } hx.moveTo(cx - u * .25, fy - u * .02); hx.arc(cx - u * .24, fy - u * .02, u * .012, 0, 7); }); } }
      if (k === 4) { for (let st = -3; st <= 3; st++) { raised(175, () => { hx.moveTo(cx + st * u * .025, cy + u * .36); hx.quadraticCurveTo(cx + st * u * .03, cy, cx + st * u * .1, cy - u * .2); hx.lineTo(cx + st * u * .1 + u * .012, cy - u * .2); hx.quadraticCurveTo(cx + st * u * .03 + u * .012, cy, cx + st * u * .025 + u * .012, cy + u * .36); });
        for (let q = 0; q < 6; q++) raised(210, () => hx.ellipse(cx + st * u * .1 + (q % 2 ? u * .022 : -u * .022) + st * u * .006 * q, cy - u * .2 - q * u * .035, u * .016, u * .028, (q % 2 ? .5 : -.5), 0, 7)); }
        carve(() => { hx.moveTo(cx - u * .1, cy + u * .12); hx.lineTo(cx + u * .1, cy + u * .12); }, C / 60); }
      if (k === 5) { raised(200, () => { hx.ellipse(cx, cy, u * .17, u * .095, -.15, 0, 7); }); raised(205, () => hx.arc(cx + u * .17, cy - u * .07, u * .06, 0, 7)); raised(190, () => { hx.moveTo(cx - u * .14, cy + u * .02); hx.lineTo(cx - u * .36, cy - u * .2); hx.lineTo(cx - u * .3, cy - u * .24); hx.lineTo(cx - u * .1, cy - u * .03); });
        raised(185, () => { hx.moveTo(cx + u * .22, cy - u * .085); hx.lineTo(cx + u * .3, cy - u * .065); hx.lineTo(cx + u * .22, cy - u * .055); }); raised(165, () => hx.rect(cx - u * .34, cy + u * .2, u * .68, u * .035));
        carve(() => { hx.moveTo(cx - u * .08, cy - u * .02); hx.quadraticCurveTo(cx + u * .02, cy + u * .05, cx + u * .12, cy - u * .01); hx.moveTo(cx + u * .02, cy + u * .09); hx.lineTo(cx + u * .02, cy + u * .2); hx.moveTo(cx + u * .07, cy + u * .09); hx.lineTo(cx + u * .07, cy + u * .2); }); }
    }
    const map = canvas(hc.width, hc.height), mx = map.getContext('2d'), hd = hx.getImageData(0, 0, hc.width, hc.height).data, md = mx.createImageData(hc.width, hc.height), r = rng(5), n2 = noise3(13);
    for (let i = 0, N = hc.width * hc.height; i < N; i++) { const h = hd[i * 4] / 255, px2 = i % hc.width, py2 = Math.floor(i / hc.width), m = .1 * n2(px2 / 40, py2 / 40, 1) + (r() - .5) * .05, k = .66 + .48 * h + m;
      md.data[i * 4] = Math.min(255, 176 * k); md.data[i * 4 + 1] = Math.min(255, 94 * k); md.data[i * 4 + 2] = Math.min(255, 56 * k); md.data[i * 4 + 3] = 255; }
    mx.putImageData(md, 0, 0);
    const front = std('relief_front', () => ({ map: tex(map, { clamp: true }), normalMap: tex(normalFromHeight(hc, 5), { srgb: false, clamp: true }), roughness: .9 }));
    const body = std('relief_body', () => ({ color: '#8c4a2c', roughness: .9 }));
    const PW = .5, PH = .45, GAP = .05, r2 = rng(17);
    for (let k = 0; k < 6; k++) {
      const col = k % 3, row = Math.floor(k / 3), z = 1.43 + (1 - col) * (PW + GAP) + (r2() - .5) * .008, y = 1.6 + (row ? -1 : 1) * (PH + GAP) / 2 + (r2() - .5) * .008;
      const plaque = new THREE.Group(); plaque.position.set(.004, y, z); plaque.rotation.set((r2() - .5) * .02, Math.PI / 2, 0); g.add(plaque);
      add(plaque, new THREE.BoxGeometry(PW, PH, .026), body, 0, 0, .013);
      const geo = new THREE.PlaneGeometry(PW, PH), uv = geo.attributes.uv;
      for (let i = 0; i < uv.count; i++) uv.setXY(i, (col + uv.getX(i)) / 3, 1 - (row + 1 - uv.getY(i)) / 2);
      add(plaque, geo, front, 0, 0, .0265);
    }
  }

  // ---------------------------------------------------------------- Z02 Reception
  if (want('BEL_RECEPTION_TREE')) { const g = item('BEL_RECEPTION_TREE'); smallTree(g, { x: 8.125, z: 5.845, seed: 13, height: 1.72 }); }   // approved F015/PL015: x 7.87-8.38, z 5.59-6.10
  if (want('BEL_RECEPTION_ALOE')) {
    const g = item('BEL_RECEPTION_ALOE');  // approved F016/PL016: x 13.72-14.12, z 5.69-6.10
    const rock = graniteBlock(.2, 211, .6); add(g, rock, M.graniteSplit, 13.92, 0, 5.9, 0, .4);
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
      add(g, new THREE.CircleGeometry(.05, 20), std('earth_' + i, () => ({ color: col, roughness: 1, map: i ? weaveMap('plain') : M.soil.map })), 9.37, 1.215, z, -Math.PI / 2);
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
    // bays F017-F020 (measured in the scene): base top 0.1016, top shelf 1.8592, green back z -10.7251, front edge z -10.1347,
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
    add(g, pillowGeometry(.42, .42, .13), handloomCushion, x0 + .55, BASE + .2, -10.6, -.38, .12, 0);
    add(g, pillowGeometry(.4, .4, .13), T.indigo, x0 + 1.0, BASE + .19, -10.62, -.38, -.1, 0);
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
    add(g, pillowGeometry(.4, .4, .13), T.patch, x0 + 1.45, BASE + .19, -10.62, -.38, 0, 0);
    folded(g, x0 + 1.85, BASE, -10.45, T.patch, 3);
    [['#8f4a3a', -.12], ['#3d5170', 0], ['#c9a565', .12]].forEach(([cc, dx]) => add(g, new THREE.CylinderGeometry(.03, .045, .17, 24), std('yarn_rec_' + cc, () => ({ color: cc, roughness: .9, map: weaveMap('coil', [3, 6]) })), x0 + .7 + dx, SHELF + .085, -10.45));
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

  // ---------------------------------------------------------------- option A: Merchandising Z07 and the accounts suite in Z06
  // The full-conversion option only (owner decision). The route config hides every approved item that the relocation
  // ledger (viewer/option-a-ledger.json) moves off this floor and releases the walk-grid cells only that furniture
  // blocked. Walls, glass, doors, columns, fire extinguishers, air conditioning and the kept lights stay as approved.
  const shadows = { Z07: [], Z06: [] };
  const RUG = .016;   // rugs and mats lie on the new floor finish (y 0.0135)
  const shade = (zone, x0, z0, x1, z1, k = .45) => shadows[zone].push([Math.min(x0, x1), Math.min(z0, z1), Math.max(x0, x1), Math.max(z0, z1), k]);
  const B = (w, h, d, x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0) => [new THREE.BoxGeometry(w, h, d), x, y + h / 2, z, rx, ry, rz];   // y = bottom
  function merged(parts) {   // [geometry, x, y, z, rx, ry, rz] parts -> one geometry (for a single mesh or for instancing)
    const pos = [], nor = [], uv = [], m = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler(), one = new THREE.Vector3(1, 1, 1);
    for (const [g0, x = 0, y = 0, z = 0, rx = 0, ry = 0, rz = 0] of parts) {
      const g = g0.index ? g0.toNonIndexed() : g0; g.applyMatrix4(m.compose(new THREE.Vector3(x, y, z), q.setFromEuler(e.set(rx, ry, rz)), one));
      for (const v of g.attributes.position.array) pos.push(v); for (const v of g.attributes.normal.array) nor.push(v); for (const v of g.attributes.uv.array) uv.push(v);
      g0.dispose(); if (g !== g0) g.dispose();
    }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('normal', new THREE.Float32BufferAttribute(nor, 3));
    g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); geometries.push(g); return g;
  }
  function instances(parent, geometry, material, placements) {   // [x, y, z, ry] per copy
    const im = new THREE.InstancedMesh(geometry, material, placements.length), m = new THREE.Matrix4(), q = new THREE.Quaternion(), up = new THREE.Vector3(0, 1, 0), one = new THREE.Vector3(1, 1, 1);
    placements.forEach(([x, y, z, ry = 0], i) => im.setMatrixAt(i, m.compose(new THREE.Vector3(x, y, z), q.setFromAxisAngle(up, ry), one)));
    im.instanceMatrix.needsUpdate = true; im.computeBoundingSphere(); parent.add(im); return im;
  }
  const textileMat = (key, draw, [cw, ch] = [384, 384], extra = {}) => std('tx_' + key, () => { const c = canvas(px(cw), px(ch)), x = c.getContext('2d'); draw(x, c.width, c.height);
    x.globalCompositeOperation = 'multiply'; x.globalAlpha = .25; x.fillStyle = x.createPattern(weave.plain.map, 'repeat'); x.fillRect(0, 0, c.width, c.height); x.globalAlpha = 1; x.globalCompositeOperation = 'source-over';
    return { map: tex(c), roughness: .95, side: THREE.DoubleSide, ...extra }; });
  const stitch = (x, w, col, dash = [w / 90, w / 140]) => { x.strokeStyle = col; x.lineWidth = Math.max(1.5, w / 170); x.setLineDash(dash); x.lineCap = 'round'; };
  // nakshi kantha: running-stitch motifs on a cream ground (a placeholder for the work of a rural embroiderer)
  function drawKantha(x, w, h, seed = 5) {
    const r = rng(seed); x.fillStyle = '#efe5cf'; x.fillRect(0, 0, w, h);
    stitch(x, w, 'rgba(160,140,110,.45)', [w / 160, w / 220]); for (let y = h * .04; y < h; y += h / 70) { x.beginPath(); x.moveTo(0, y); for (let X = 0; X <= w; X += w / 20) x.lineTo(X, y + Math.sin(X / w * 12 + y) * h * .004); x.stroke(); }
    for (const [inset, col] of [[.03, '#9c3b2a'], [.055, '#2f4a6b'], [.075, '#9c3b2a']]) { stitch(x, w, col); x.strokeRect(w * inset, h * inset, w * (1 - 2 * inset), h * (1 - 2 * inset)); }
    const lotus = (cx, cy, R, n, col) => { stitch(x, w, col); for (let k = 0; k < n; k++) { const a = k / n * Math.PI * 2; x.beginPath(); x.ellipse(cx + Math.cos(a) * R * .55, cy + Math.sin(a) * R * .55, R * .45, R * .17, a, 0, 7); x.stroke(); }
      x.beginPath(); x.arc(cx, cy, R * .22, 0, 7); x.stroke(); x.beginPath(); x.arc(cx, cy, R * .12, 0, 7); x.stroke(); };
    const s = Math.min(w, h); lotus(w / 2, h / 2, s * .3, 16, '#9c3b2a'); lotus(w / 2, h / 2, s * .17, 10, '#2f4a6b');
    const fish = (cx, cy, L, a, col) => { x.save(); x.translate(cx, cy); x.rotate(a); stitch(x, w, col); x.beginPath(); x.ellipse(0, 0, L * .5, L * .2, 0, 0, 7); x.moveTo(L * .45, 0); x.lineTo(L * .75, -L * .18); x.lineTo(L * .75, L * .18); x.closePath(); x.stroke(); x.beginPath(); x.arc(-L * .3, -L * .04, L * .03, 0, 7); x.stroke(); x.restore(); };
    const boat = (cx, cy, L, col) => { stitch(x, w, col); x.beginPath(); x.moveTo(cx - L / 2, cy); x.quadraticCurveTo(cx, cy + L * .35, cx + L / 2, cy); x.quadraticCurveTo(cx, cy + L * .15, cx - L / 2, cy); x.moveTo(cx, cy + L * .1); x.lineTo(cx, cy - L * .55); x.lineTo(cx + L * .3, cy - L * .05); x.stroke(); };
    const kalka = (cx, cy, L, a, col) => { x.save(); x.translate(cx, cy); x.rotate(a); stitch(x, w, col); x.beginPath(); x.moveTo(0, -L * .5); x.bezierCurveTo(L * .5, -L * .3, L * .45, L * .45, 0, L * .5); x.bezierCurveTo(-L * .35, L * .4, -L * .3, 0, 0, -L * .5); x.stroke();
      x.beginPath(); x.moveTo(0, -L * .3); x.bezierCurveTo(L * .3, -L * .15, L * .25, L * .3, 0, L * .32); x.stroke(); x.restore(); };
    [[.17, .2, .6], [.83, .2, 2.2], [.17, .8, -.6], [.83, .8, 3.8]].forEach(([u, v, a]) => kalka(w * u, h * v, s * .16, a, '#2f4a6b'));
    fish(w * .3, h * .5, s * .14, 0, '#2f4a6b'); fish(w * .7, h * .5, s * .14, Math.PI, '#2f4a6b');
    boat(w * .5, h * .17, s * .2, '#5a4a2a'); boat(w * .5, h * .86, s * .2, '#5a4a2a');
    x.setLineDash([]); void r;
  }
  function floorOverlay(parent, zone, [x0, z0, x1, z1], { map, repeat, color = '#ffffff', y = .0135, edge = .35 }) {   // the approved carpet top is at y 0.0097
    // a finish laid over an approved floor whose baked light still shows the removed furniture: unlit like the baked shell,
    // with soft wall shadows and contact shadows of the new furniture painted into its occlusion map
    const W = x1 - x0, D = z1 - z0, cw = px(256), ch = Math.max(32, Math.round(cw * D / W)), c = canvas(cw, ch), o = c.getContext('2d'), sx = cw / W, sz = ch / D;
    o.fillStyle = '#ffffff'; o.fillRect(0, 0, cw, ch);
    const ramp = (gx0, gy0, gx1, gy1, rx, ry, rw, rh) => { const g = o.createLinearGradient(gx0, gy0, gx1, gy1); g.addColorStop(0, 'rgba(0,0,0,.42)'); g.addColorStop(1, 'rgba(0,0,0,0)'); o.fillStyle = g; o.fillRect(rx, ry, rw, rh); };
    const ex = edge * sx, ez = edge * sz;
    ramp(0, 0, ex, 0, 0, 0, ex, ch); ramp(cw, 0, cw - ex, 0, cw - ex, 0, ex, ch); ramp(0, 0, 0, ez, 0, 0, cw, ez); ramp(0, ch, 0, ch - ez, 0, ch - ez, cw, ez);
    if ('filter' in o) o.filter = `blur(${Math.max(2, Math.round(.06 * sx))}px)`;
    for (const [a, b, c2, d, k] of shadows[zone]) { if (c2 < x0 || a > x1 || d < z0 || b > z1) continue; o.fillStyle = `rgba(0,0,0,${k})`; o.fillRect((a - x0) * sx, (b - z0) * sz, (c2 - a) * sx, (d - b) * sz); }
    if ('filter' in o) o.filter = 'none';
    const ao = tex(c, { clamp: true, srgb: false }); map.repeat.set(...repeat);
    const mat = new THREE.MeshBasicMaterial({ name: 'bel_floor_' + zone, map, aoMap: ao, aoMapIntensity: 1, color }); materials.push(mat);
    return add(parent, new THREE.PlaneGeometry(W, D), mat, (x0 + x1) / 2, y, (z0 + z1) / 2, -Math.PI / 2);
  }
  const juteFloor = (key, base, seed) => { const s = px(256), c = canvas(s, s), x = c.getContext('2d'), r = rng(seed); x.fillStyle = base; x.fillRect(0, 0, s, s);
    const u = s / 32; for (let j = 0; j < 32; j++) for (let i = 0; i < 32; i++) { const over = (i + j) % 2 === 0, l = r() * .16 - .08; x.fillStyle = l > 0 ? `rgba(255,240,210,${l})` : `rgba(60,40,20,${-l})`; if (over) x.fillRect(i * u, j * u + u * .1, u, u * .8); else x.fillRect(i * u + u * .1, j * u, u * .8, u);
      x.fillStyle = 'rgba(50,35,20,.18)'; x.fillRect(i * u, j * u, over ? u : u * .1, over ? u * .1 : u); }
    void key; return tex(c); };
  function signStand(parent, lines, x, z, ry, opts = {}) {   // a floor-standing oak sign, board at eye height
    const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = ry; parent.add(g);
    box(g, M.oak, 0, 0, 0, .34, .02, .26); box(g, M.oak, 0, .02, 0, .04, 1.02, .04);
    add(g, new THREE.PlaneGeometry(.44, .3), card(lines, { w: .44, h: .3, scale: 1.2, ...opts }), 0, 1.24, .026, -.12);
    box(g, M.oak, 0, 1.06, .012, .47, .33, .02);
    footprint(x - .2, z - .2, x + .2, z + .2); return g;
  }
  // furniture, front towards local +z (shared by the room-sets and the academy)
  const cane = wovenMaterial('cane_seat', 'lattice', FIBRE.cane, [5, 5]);
  const chairWood = merged([B(.035, .45, .035, -.19, 0, .19), B(.035, .45, .035, .19, 0, .19), B(.035, .92, .035, -.19, 0, -.19), B(.035, .92, .035, .19, 0, -.19),
    B(.42, .04, .03, 0, .41, .2), B(.42, .04, .03, 0, .41, -.2), B(.03, .04, .42, -.2, .41, 0), B(.03, .04, .42, .2, .41, 0), B(.42, .05, .03, 0, .84, -.19), B(.38, .02, .02, 0, .12, .19), B(.38, .02, .02, 0, .12, -.19)]);
  const chairCane = merged([B(.39, .015, .39, 0, .44, 0), B(.37, .3, .012, 0, .52, -.19)]);
  const tableWood = (w, d, h) => merged([B(w, .035, d, 0, h - .035, 0), ...[[-1, -1], [1, -1], [-1, 1], [1, 1]].map(([a, b]) => B(.05, h - .035, .05, a * (w / 2 - .06), 0, b * (d / 2 - .06))),
    B(w - .14, .06, .025, 0, h - .095, d / 2 - .06), B(w - .14, .06, .025, 0, h - .095, -d / 2 + .06)]);
  function caneArmchair(parent, x, z, ry, cushion = handloomCushion) {
    const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = ry; parent.add(g);
    add(g, merged([...[[-1, -1], [1, -1], [-1, 1], [1, 1]].map(([a, b]) => B(.045, .38, .045, a * .31, 0, b * .31)), B(.06, .04, .7, -.33, .58, .02), B(.06, .04, .7, .33, .58, .02),
      B(.045, .2, .045, -.33, .38, .31), B(.045, .2, .045, .33, .38, .31), B(.045, .5, .045, -.31, .38, -.31), B(.045, .5, .045, .31, .38, -.31), B(.66, .05, .045, 0, .84, -.32), B(.62, .05, .04, 0, .33, .3)]), M.wood);
    add(g, merged([B(.6, .02, .6, 0, .36, 0), [new THREE.BoxGeometry(.6, .42, .016), 0, .62, -.29, -.16, 0, 0]]), cane);
    add(g, pillowGeometry(.56, .56, .09), cushion, 0, .43, .02, -Math.PI / 2, 0, 0);
    return g;
  }
  function floorLamp(parent, x, z, h = 1.45) {
    const g = new THREE.Group(); g.position.set(x, 0, z); parent.add(g);
    add(g, new THREE.CylinderGeometry(.14, .16, .03, 24), M.wood, 0, .015, 0); add(g, new THREE.CylinderGeometry(.014, .016, h, 10), M.bamboo, 0, h / 2, 0);
    for (const yy of [.35, .75, 1.15]) if (yy < h) add(g, new THREE.TorusGeometry(.017, .004, 6, 12), M.wood, 0, yy, 0, Math.PI / 2);
    bambooLamp(g, 0, h - .05, 0, { r: .17, h: .3, glow: 0 }); return g;
  }
  function clayPlate(parent, x, y, z, r = .12, mat = M.clayCream) { return add(parent, lathe([[0, 0], [r * .55, 0], [r * .6, .006], [r, .028], [r * .96, .03], [r * .55, .012], [0, .012]], 32), mat, x, y, z); }
  function kashVase(parent, x, z, h = .62) {   // dried kash flowers (Saccharum spontaneum) in a tall clay vase: autumn in Bengal, no living plant claimed
    const g = new THREE.Group(); g.position.set(x, 0, z); parent.add(g); const r = rng(Math.round(x * 100 + z * 10));
    add(g, lathe([[0, 0], [.1, 0], [.15, h * .3], [.13, h * .7], [.07, h * .92], [.08, h], [.065, h], [.055, h * .92], [0, h * .9]], 36), M.clayRaw);
    const plume = std('kash_plume', () => { const c = canvas(64, 160), xx = c.getContext('2d'), q = rng(97); xx.clearRect(0, 0, 64, 160);
      for (let i = 0; i < 260; i++) { const t = q(), y = 150 - t * 140, sp = Math.sin(t * Math.PI) * 26; xx.strokeStyle = `rgba(250,246,236,${.35 + q() * .4})`; xx.lineWidth = .8; xx.beginPath(); xx.moveTo(32, y); xx.lineTo(32 + (q() - .5) * sp * 2, y - 6 - q() * 10); xx.stroke(); }
      return { map: tex(c, { clamp: true }), alphaTest: .3, side: THREE.DoubleSide, roughness: 1, color: '#f6f1e6' }; });
    for (let k = 0; k < 11; k++) {
      const a = r() * Math.PI * 2, lean = .05 + r() * .16, L = .55 + r() * .35, tx = Math.cos(a) * lean * L, tz = Math.sin(a) * lean * L;
      add(g, taperedTube([[0, h * .9, 0], [tx * .5, h + L * .5, tz * .5], [tx, h + L, tz]], .003, .002, 6, 4), std('kash_stem', () => ({ color: '#b9a57a', roughness: .9 })));
      for (const s of [0, Math.PI / 2]) add(g, new THREE.PlaneGeometry(.09, .26), plume, tx, h + L + .1, tz, 0, a + s, -Math.cos(a) * lean);
    }
    footprint(x - .17, z - .17, x + .17, z + .17); return g;
  }

  if (want('BEL_UTHAN')) {
    const g = item('BEL_UTHAN'), CX = 15.65, CZ = -16.08;   // steel column COL07 (survey, photo-estimated) at the room centre
    // bot-tola: a seat platform of handmade terracotta around the column, oak top at seat height (free-standing, not fixed to the steel)
    const clad = std('terracotta_seat', () => ({ map: M.terracotta.map.clone(), normalMap: M.terracotta.normalMap.clone(), roughness: .86 }));
    clad.map.repeat.set(2.75, 1.05); clad.normalMap.repeat.set(2.75, 1.05); clad.map.needsUpdate = clad.normalMap.needsUpdate = true; textures.push(clad.map, clad.normalMap);
    box(g, clad, CX, 0, CZ, 2.2, .42, 2.2); box(g, M.oak, CX, .42, CZ, 2.3, .05, 2.3);
    footprint(CX - 1.15, CZ - 1.15, CX + 1.15, CZ + 1.15); shade('Z07', CX - 1.2, CZ - 1.2, CX + 1.2, CZ + 1.2, .5);
    bonsai(g, { x: CX - .78, y: .47, z: CZ - .78, ry: 1.2, seed: 61, style: 'banyan', pot: M.clayBlue, scale: 1.05 });
    // terracotta tiles of the courtyard floor
    const tc = terracottaCanvas(4, 4, 63, px(256)), tileMap = tex(tc.c); tileMap.repeat.set(3.5, 3.5);
    const tiles = new THREE.MeshBasicMaterial({ name: 'bel_uthan_tiles', map: tileMap, color: '#d9d2c8' }); materials.push(tiles);
    add(g, new THREE.PlaneGeometry(4.2, 4.2), tiles, CX, .019, CZ, -Math.PI / 2);
    box(g, M.graniteRough, CX, 0, CZ - 2.13, 4.32, .02, .06); box(g, M.graniteRough, CX, 0, CZ + 2.13, 4.32, .02, .06);
    box(g, M.graniteRough, CX - 2.13, 0, CZ, .06, .02, 4.2); box(g, M.graniteRough, CX + 2.13, 0, CZ, .06, .02, 4.2);
    // two small fig trees and stone seats
    smallTree(g, { x: 13.95, z: -14.45, seed: 67, height: 1.85 }); footprint(13.7, -14.7, 14.2, -14.2); shade('Z07', 13.65, -14.75, 14.25, -14.15, .5);
    smallTree(g, { x: 17.35, z: -17.72, seed: 71, height: 1.9 }); footprint(17.1, -17.97, 17.6, -17.47); shade('Z07', 17.05, -18.02, 17.65, -17.42, .5);
    stoneGroup(g, 14.05, -17.55, 211, [[0, 0, .24, .78, .4], [.42, .22, .14, .7, 1.9]]); footprint(13.8, -17.8, 14.6, -17.2); shade('Z07', 13.8, -17.8, 14.6, -17.2, .35);
    stoneGroup(g, 17.35, -14.5, 223, [[0, 0, .23, .8, 2.6], [-.38, .2, .13, .7, .4]]); footprint(16.85, -14.75, 17.6, -14.25); shade('Z07', 16.85, -14.75, 17.6, -14.25, .35);
    // the Bengal Canopy: an open split-bamboo lattice under the felt baffles, clear of the AC units and smoke detectors
    const Y = 2.34, X0 = 13.65, X1 = 17.65, Z0 = -18.08, Z1 = -14.08, step = .16, hole = .3, strips = [];
    const strip = (len, x, z, along) => strips.push(along === 'x' ? B(len, .006, .028, x, 0, z) : B(.028, .006, len, x, .008, z));
    for (let zz = Z0 + .08; zz < Z1; zz += step) { if (Math.abs(zz - CZ) < hole) { strip(CX - hole - X0, (X0 + CX - hole) / 2, zz, 'x'); strip(X1 - CX - hole, (CX + hole + X1) / 2, zz, 'x'); } else strip(X1 - X0, (X0 + X1) / 2, zz, 'x'); }
    for (let xx = X0 + .08; xx < X1; xx += step) { if (Math.abs(xx - CX) < hole) { strip(CZ - hole - Z0, xx, (Z0 + CZ - hole) / 2, 'z'); strip(Z1 - CZ - hole, xx, (CZ + hole + Z1) / 2, 'z'); } else strip(Z1 - Z0, xx, (Z0 + Z1) / 2, 'z'); }
    add(g, merged(strips), M.bamboo, 0, Y, 0);
    for (const [x, z, w, d] of [[(X0 + X1) / 2, Z0, X1 - X0 + .06, .05], [(X0 + X1) / 2, Z1, X1 - X0 + .06, .05], [X0, (Z0 + Z1) / 2, .05, Z1 - Z0], [X1, (Z0 + Z1) / 2, .05, Z1 - Z0]]) box(g, M.bamboo, x, Y - .02, z, w, .05, d);
    for (const [x, z] of [[X0 + .1, Z0 + .1], [X1 - .1, Z0 + .1], [X0 + .1, Z1 - .1], [X1 - .1, Z1 - .1]]) add(g, new THREE.CylinderGeometry(.003, .003, 2.895 - Y, 4), std('cord', () => ({ color: '#2a2a2a', roughness: .6 })), x, (Y + 2.895) / 2, z);
    const grow = new THREE.MeshBasicMaterial({ name: 'bel_growlight', color: '#fff3dc' }); materials.push(grow);
    for (const [x, z] of [[13.95, -14.45], [17.35, -17.72], [CX - .78, CZ - .78]]) { box(g, std('lamp_body', () => ({ color: '#2b2b2b', roughness: .5 })), x, Y - .05, z, .5, .04, .06); add(g, new THREE.PlaneGeometry(.46, .03), grow, x, Y - .051, z, Math.PI / 2); }
    standingCard(g, ['Green Uthan', 'A Bengali courtyard: a bot-tola seat around the column', 'Trees under grow lights: this room has no daylight', 'Option A only'], CX + .55, .47, CZ + .85, -.3, { w: .22, h: .13 });
  }
  if (want('BEL_ARTISAN_CORNER')) {
    const g = item('BEL_ARTISAN_CORNER');   // west of the Uthan; the fire extinguisher on the west wall (z -15.34..-15.14) stays clear
    const pati = textileMat('sitalpati', (x, w, h) => { x.fillStyle = '#d6c393'; x.fillRect(0, 0, w, h); const u = w / 96;
      for (let j = 0; j < h / u; j++) for (let i = 0; i < w / u; i++) if ((i + j) % 4 < 2) { x.fillStyle = 'rgba(120,90,40,.16)'; x.fillRect(i * u, j * u, u, u); }
      for (const [y0, col] of [[.06, '#6b3a24'], [.9, '#6b3a24']]) { x.fillStyle = col; x.fillRect(0, h * y0, w, h * .04); x.fillStyle = '#2f4a3a'; for (let i = 0; i < w; i += w / 16) { x.beginPath(); x.moveTo(i, h * (y0 + .02)); x.lineTo(i + w / 32, h * (y0 - .005)); x.lineTo(i + w / 16, h * (y0 + .02)); x.lineTo(i + w / 32, h * (y0 + .045)); x.fill(); } } });
    box(g, pati, 11.3, RUG, -16.05, 1.8, .008, 1.2);
    // Chakma back-strap loom (bain): warp from a bar on two posts to the breast bar at the weaver's lap; plain stripes only
    const L0 = [10.4, .86], L1 = [11.55, .32], ZC = -16.15, WW = .34, len = Math.hypot(L1[0] - L0[0], L1[1] - L0[1]), ang = Math.atan2(L1[1] - L0[1], L1[0] - L0[0]);
    const slant = m => { m.rotation.order = 'ZYX'; m.rotation.set(-Math.PI / 2, 0, ang); return m; };   // lay the plane flat, then tilt it down towards the weaver
    for (const dz of [-.3, .3]) { box(g, M.wood, 10.36, 0, ZC + dz, .05, 1.0, .05); }
    add(g, new THREE.CylinderGeometry(.018, .018, .7, 12), M.bamboo, 10.38, L0[1], ZC, Math.PI / 2, 0, 0);
    const warp = std('warp_threads', () => { const c = canvas(128, 256), x = c.getContext('2d'); x.clearRect(0, 0, 128, 256);
      for (let i = 0; i < 40; i++) { x.fillStyle = i % 10 < 2 ? '#8f2f24' : i % 10 === 5 ? '#26313f' : '#efe6d4'; x.fillRect(i * 3.2 + .6, 0, 1.6, 256); } return { map: tex(c, { clamp: true }), alphaTest: .4, side: THREE.DoubleSide, roughness: .85 }; });
    slant(add(g, new THREE.PlaneGeometry(len * .72, WW), warp, L0[0] + (L1[0] - L0[0]) * .36, L0[1] + (L1[1] - L0[1]) * .36, ZC));
    const band = std('woven_band', () => { const c = canvas(128, 64), x = c.getContext('2d'); x.fillStyle = '#efe6d4'; x.fillRect(0, 0, 128, 64);
      for (const [y, h, col] of [[6, 6, '#8f2f24'], [20, 3, '#26313f'], [41, 3, '#26313f'], [52, 6, '#8f2f24']]) { x.fillStyle = col; x.fillRect(0, y, 128, h); }
      x.globalCompositeOperation = 'multiply'; x.fillStyle = x.createPattern(weave.plain.map, 'repeat'); x.globalAlpha = .35; x.fillRect(0, 0, 128, 64); return { map: tex(c), roughness: .9, side: THREE.DoubleSide }; });
    slant(add(g, new THREE.PlaneGeometry(len * .3, WW), band, L0[0] + (L1[0] - L0[0]) * .86, L0[1] + (L1[1] - L0[1]) * .86 + .002, ZC));
    add(g, new THREE.CylinderGeometry(.016, .016, .44, 10), M.wood, L1[0], L1[1], ZC, Math.PI / 2, 0, 0);
    for (const t of [.45, .6]) add(g, new THREE.CylinderGeometry(.008, .008, .42, 8), M.bamboo, L0[0] + (L1[0] - L0[0]) * t, L0[1] + (L1[1] - L0[1]) * t + .012, ZC, Math.PI / 2, 0, 0);
    add(g, new THREE.TorusGeometry(.2, .025, 6, 18, Math.PI), std('strap', () => ({ color: '#6b4a2b', roughness: .9 })), L1[0] + .02, .3, ZC, Math.PI / 2, 0, -Math.PI / 2);
    footprint(10.3, ZC - .36, 11.62, ZC + .36); shade('Z07', 10.3, ZC - .36, 11.62, ZC + .36, .25);
    standingCard(g, ['Chakma back-strap loom (bain)', 'Shown only with the consent and participation', 'of Chakma weavers; their designs stay theirs', 'Makers paid and credited by name'], 11.95, RUG + .008, -15.55, .5, { w: .2, h: .12 });
    // Marma weaving and basketry (thami and angi weaving is common among Marma women: Banglapedia): a low bamboo stand with
    // a folded plain-striped cloth and a basket; no community's designs are copied
    const ms = new THREE.Group(); ms.position.set(10.75, 0, -17.08); g.add(ms);
    add(ms, merged([B(.03, .45, .03, -.38, 0, -.17), B(.03, .45, .03, .38, 0, -.17), B(.03, .45, .03, -.38, 0, .17), B(.03, .45, .03, .38, 0, .17), B(.8, .025, .38, 0, .42, 0), B(.8, .025, .38, 0, .15, 0)]), M.bamboo);
    const cloth = textileMat('marma_plain_stripes', (x, w, h) => { x.fillStyle = '#2b2d3a'; x.fillRect(0, 0, w, h); for (const [y, hh, col] of [[.18, .05, '#b23a2c'], [.3, .02, '#e2c25a'], [.68, .02, '#e2c25a'], [.77, .05, '#b23a2c']]) { x.fillStyle = col; x.fillRect(0, h * y, w, h * hh); } }, [192, 192]);
    for (let k = 0; k < 3; k++) box(ms, cloth, -.12 + k * .006, .445 + k * .035, .0, .38, .033, .27, (k - 1) * .04);
    basket(ms, .22, .445, 0, { r: .1, h: .22, kind: 'twill', fibre: 'bamboo' });
    footprint(10.33, -17.27, 11.17, -16.89); shade('Z07', 10.35, -17.25, 11.15, -16.91, .3);
    standingCard(g, ['Marma weaving and basketry', 'Thami and angi weaving is common among Marma women', 'Shown only with the consent and participation of', 'Marma weavers; their designs stay theirs'], 10.62, .445, -16.92, .15, { w: .2, h: .12 });
    // nakshi kantha on a low frame
    const kf = new THREE.Group(); kf.position.set(12.75, 0, -16.85); kf.rotation.y = .2; g.add(kf);
    for (const [a, b] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) box(kf, M.wood, a * .52, 0, b * .32, .04, .34, .04);
    box(kf, M.wood, 0, .34, -.33, 1.12, .035, .045); box(kf, M.wood, 0, .34, .33, 1.12, .035, .045); box(kf, M.wood, -.54, .34, 0, .045, .035, .7); box(kf, M.wood, .54, .34, 0, .045, .035, .7);
    add(kf, new THREE.PlaneGeometry(1.03, .62), textileMat('kantha_frame', (x, w, h) => drawKantha(x, w, h, 9), [384, 232]), 0, .358, 0, -Math.PI / 2);
    footprint(12.15, -17.3, 13.35, -16.4); shade('Z07', 12.2, -17.25, 13.3, -16.45, .3);
    standingCard(g, ['Nakshi kantha in progress', 'Embroiderer to be invited, paid and credited'], 13.15, 0, -16.25, -.4, { w: .18, h: .07 });
    // cane basketry on a low pira stool, painted terracotta on a low table
    box(g, M.wood, 12.35, 0, -15.0, .34, .12, .26);
    basket(g, 12.75, 0, -15.05, { r: .18, h: .3, kind: 'lattice', fibre: 'cane', partial: .6 });
    const coil = new THREE.CatmullRomCurve3(Array.from({ length: 80 }, (_, i) => { const a = i / 79 * Math.PI * 2 * 4; return new THREE.Vector3(Math.cos(a) * (.1 + i * .0006), i / 79 * .05, Math.sin(a) * (.1 + i * .0006)); }));
    add(g, new THREE.TubeGeometry(coil, 240, .004, 5, false), std('cane_coil', () => ({ color: FIBRE.cane, roughness: .5 })), 12.35, .125, -14.75);
    footprint(12.15, -15.3, 13.0, -14.8); shade('Z07', 12.15, -15.25, 12.95, -14.8, .3);
    const pt = new THREE.Group(); pt.position.set(11.1, 0, -14.98); g.add(pt);
    add(pt, tableWood(.62, .42, .36), M.wood);
    const sora = std('sora_paint', () => { const c = canvas(px(256), px(256)), x = c.getContext('2d'), s = c.width; x.fillStyle = '#b8643c'; x.fillRect(0, 0, s, s);
      x.fillStyle = '#efe0bf'; x.beginPath(); x.arc(s / 2, s / 2, s * .42, 0, 7); x.fill(); x.strokeStyle = '#7a2f1e'; x.lineWidth = s / 60; x.beginPath(); x.arc(s / 2, s / 2, s * .42, 0, 7); x.stroke();
      x.fillStyle = '#2f4a6b'; x.beginPath(); x.ellipse(s / 2, s * .55, s * .2, s * .07, 0, 0, 7); x.fill(); x.fillStyle = '#7a2f1e'; x.beginPath(); x.moveTo(s * .3, s * .55); x.lineTo(s / 2, s * .3); x.lineTo(s * .7, s * .55); x.fill();
      return { map: tex(c, { clamp: true }), roughness: .8 }; });
    for (const [dx, dz] of [[-.17, -.06], [.05, .08], [.2, -.07]]) add(pt, new THREE.CylinderGeometry(.085, .07, .014, 28), sora, dx, .367, dz);
    add(pt, lathe([[0, 0], [.06, 0], [.1, .07], [.09, .13], [.05, .16], [.055, .17], [.045, .17], [0, .15]], 28), M.clayRaw, -.2, .36, .12);
    footprint(10.75, -15.22, 11.45, -14.74); shade('Z07', 10.78, -15.2, 11.42, -14.76, .3);
    standingCard(g, ['Artisan corner', 'Demonstrations by invitation, never as a spectacle', 'Quiet crafts only: dusty work stays in the workshop', 'Option A only'], 11.2, .36, -14.83, .25, { w: .22, h: .13 });
  }
  if (want('BEL_ROOMSET_LIVING')) {
    const g = item('BEL_ROOMSET_LIVING');   // south-west corner; fire extinguisher at x 9.35-9.52, z -12.80..-12.60 stays clear
    box(g, wovenMaterial('rug_jute', 'twill', '#cdb68a', [14, 10]), 11.5, RUG, -12.55, 2.6, .01, 1.9);
    const sofa = new THREE.Group(); sofa.position.set(11.5, 0, -11.42); sofa.rotation.y = Math.PI; g.add(sofa);
    const upholstery = wovenMaterial('upholstery_khadi', 'plain', '#d8ccb4', [10, 10]), W = 2.1, D = .88;
    add(sofa, merged([B(W, .12, D, 0, .1, 0), ...[[-1, -1], [1, -1], [-1, 1], [1, 1]].map(([a, b]) => B(.05, .1, .05, a * (W / 2 - .06), 0, b * (D / 2 - .06)))]), M.wood);
    add(sofa, merged([B(.15, .32, D, -(W / 2 - .075), .22, 0), B(.15, .32, D, W / 2 - .075, .22, 0), B(W, .5, .14, 0, .22, -D / 2 + .07)]), upholstery);
    for (let k = 0; k < 3; k++) { const cx = -W / 2 + .15 + (W - .3) * (k + .5) / 3; add(sofa, pillowGeometry((W - .3) / 3 - .02, D - .2, .16), upholstery, cx, .32, .06, -Math.PI / 2, 0, 0); add(sofa, pillowGeometry((W - .3) / 3 - .03, .44, .16), upholstery, cx, .6, -D / 2 + .2, -.14, 0, 0); }
    add(sofa, pillowGeometry(.42, .42, .13), handloomCushion, -.62, .58, -.14, -.3, .25, 0); add(sofa, pillowGeometry(.4, .4, .13), textileMat('indigo_plain', (x, w, h) => { x.fillStyle = '#2f4363'; x.fillRect(0, 0, w, h); x.fillStyle = '#e8e0cf'; for (const y of [.14, .2, .8, .86]) x.fillRect(0, h * y, w, h * .015); }, [256, 256]), .64, .58, -.14, -.3, -.25, 0);
    footprint(10.43, -11.88, 12.57, -10.95); shade('Z07', 10.4, -11.9, 12.6, -10.95, .5);
    const ct = new THREE.Group(); ct.position.set(11.5, 0, -12.5); g.add(ct); add(ct, tableWood(1.0, .55, .4), M.wood); box(ct, cane, 0, .1, 0, .88, .014, .43);
    basket(ct, -.25, .4, 0, { r: .1, h: .1, kind: 'coil', fibre: 'kaisa' }); add(ct, lathe([[0, 0], [.05, 0], [.08, .06], [.06, .14], [.035, .17], [.04, .18], [.03, .18], [0, .16]], 28), M.clayCream, .22, .4, .05);
    footprint(10.98, -12.8, 12.02, -12.2); shade('Z07', 11.0, -12.78, 12.0, -12.22, .4);
    caneArmchair(g, 13.08, -12.55, -Math.PI / 2 - .25); footprint(12.68, -12.95, 13.48, -12.15); shade('Z07', 12.72, -12.92, 13.45, -12.18, .45);
    floorLamp(g, 12.86, -11.25); footprint(12.7, -11.4, 13.0, -11.1);
    const st = new THREE.Group(); st.position.set(10.1, 0, -11.3); g.add(st); add(st, tableWood(.42, .42, .5), M.wood); bambooLamp(st, 0, .5, 0, { r: .08, h: .22 }); footprint(9.87, -11.53, 10.33, -11.07);
    basket(g, 12.84, 0, -11.75, { r: .17, h: .34, kind: 'twill', fibre: 'jute', handles: true });
    const fr = new THREE.Group(); fr.position.set(11.5, 1.25, -10.885); fr.rotation.y = Math.PI; g.add(fr);   // local z -.015 = the wall face
    box(fr, M.wood, 0, 0, 0, .96, .66, .03); add(fr, new THREE.PlaneGeometry(.86, .56), textileMat('kantha_living', (x, w, h) => drawKantha(x, w, h, 11), [384, 250]), 0, .33, .017);
    signStand(g, ['Bengal Nordic · living', 'Mango wood, cane, jute and handloom', 'Illustrative room-set · option A'], 10.0, -13.85, Math.PI / 2);
  }
  if (want('BEL_ROOMSET_DINING')) {
    const g = item('BEL_ROOMSET_DINING');   // north-west corner
    box(g, wovenMaterial('rug_hogla', 'plain', FIBRE.hogla, [16, 12]), 11.85, RUG, -19.5, 2.8, .01, 2.2);
    const TX = 11.85, TZ = -19.5, TH = .75; const t = new THREE.Group(); t.position.set(TX, 0, TZ); g.add(t); add(t, tableWood(1.8, .9, TH), M.wood);
    footprint(TX - .92, TZ - .47, TX + .92, TZ + .47); shade('Z07', TX - .9, TZ - .45, TX + .9, TZ + .45, .4);
    const seats = [-.6, 0, .6].flatMap(dx => [[TX + dx, 0, TZ - .68, 0], [TX + dx, 0, TZ + .68, Math.PI]]);
    instances(g, chairWood, M.wood, seats); instances(g, chairCane, cane, seats);
    for (const [x, , z] of seats) { footprint(x - .23, z - .23, x + .23, z + .23); shade('Z07', x - .22, z - .22, x + .22, z + .22, .3); }
    for (const [x, , z, ry] of seats) {
      const pz = z + (ry ? -.36 : .36);   // the place setting on the table edge in front of each chair box(t, wovenMaterial('mat_hogla', 'twill', FIBRE.hogla, [3, 2]), x - TX, TH, pz - TZ, .4, .006, .28);
      clayPlate(t, x - TX, TH + .006, pz - TZ, .12); cup(t, x - TX + .17, TH + .006, pz - TZ + (ry ? -.06 : .06), 'tumbler'); }
    jug(t, -.2, TH, 0, .5); add(t, lathe([[0, 0], [.08, 0], [.16, .05], [.17, .09], [.15, .09], [.07, .03], [0, .03]], 36), M.clay, .25, TH, 0);
    const pend = new THREE.Group(); pend.position.set(TX, 1.62, TZ); g.add(pend);
    add(pend, lathe([[.02, .28], [.12, .26], [.24, .14], [.29, 0], [.27, 0], [.22, .12], [.11, .24], [.02, .26]], 40), wovenMaterial('cane_shade', 'lattice', FIBRE.cane, [8, 3]));
    const bulb = new THREE.MeshBasicMaterial({ name: 'bel_bulb', color: '#ffe2b0' }); materials.push(bulb); add(pend, new THREE.SphereGeometry(.05, 16, 10), bulb, 0, .14, 0);
    add(pend, new THREE.CylinderGeometry(.003, .003, 2.895 - 1.9, 4), std('cord', () => ({ color: '#2a2a2a', roughness: .6 })), 0, .28 + (2.895 - 1.9) / 2, 0);
    // sideboard along the west wall (solid to 1.22 m)
    const sb = new THREE.Group(); sb.position.set(9.6, 0, -19.9); sb.rotation.y = Math.PI / 2; g.add(sb);
    add(sb, merged([B(2.0, .66, .44, 0, .12, 0), ...[[-1, -1], [1, -1], [-1, 1], [1, 1]].map(([a, b]) => B(.05, .12, .05, a * .94, 0, b * .18))]), M.wood);
    for (let k = 0; k < 4; k++) add(sb, new THREE.PlaneGeometry(.44, .56), cane, -.72 + k * .48, .45, .221);
    add(sb, lathe([[0, 0], [.07, 0], [.11, .1], [.1, .22], [.05, .32], [.06, .36], [.045, .36], [0, .3]], 32), M.clayRaw, -.6, .78, 0);
    add(sb, lathe([[0, 0], [.05, 0], [.08, .06], [.06, .2], [.07, .26], [.055, .26], [0, .24]], 32), M.clay, -.35, .78, 0);
    basket(sb, .4, .78, 0, { r: .14, h: .14, kind: 'plait', fibre: 'hyacinth' }); bambooLamp(sb, .78, .78, 0, { r: .07, h: .2 });
    footprint(9.36, -20.92, 9.84, -18.88); shade('Z07', 9.36, -20.9, 9.84, -18.9, .45);
    signStand(g, ['River to Home · dining', 'Hogla, water hyacinth and terracotta', 'Illustrative room-set · option A'], 13.45, -18.05, Math.PI * .8);
  }
  if (want('BEL_ROOMSET_BEDROOM')) {
    const g = item('BEL_ROOMSET_BEDROOM');   // headboard on the north wall (solid to 1.22 m, glass above to the hallway)
    const BX = 16.15, BZ = -20.17, linen = std('linen', () => ({ color: '#ece6da', roughness: .9, map: weaveMap('plain', [10, 10]) }));
    const quilt = textileMat('quilt_offcuts', (x, w, h) => { const r = rng(79), cols = ['#8a5a4a', '#4a5a72', '#b8a070', '#6f7558', '#d9cdb4', '#9c7a62', '#5a5a60', '#b89a78', '#7d8a9c', '#cfc2a8', '#e2d8c4'];
      for (let j = 0; j < 14; j++) { let X = 0; while (X < w) { const ww = w * (.04 + r() * .08); x.fillStyle = cols[Math.floor(r() * cols.length)]; x.fillRect(X, j * h / 14, ww, h / 14); X += ww; } }
      stitch(x, w, 'rgba(245,238,225,.85)'); for (let y = h / 40; y < h; y += h / 22) { x.beginPath(); x.moveTo(0, y); x.lineTo(w, y + (r() - .5) * 4); x.stroke(); } x.setLineDash([]); });
    box(g, textileMat('rag_rug', (x, w, h) => { const r = rng(89), cols = ['#8a5a4a', '#4a5a72', '#b8a070', '#6f7558', '#cfc2a8', '#9c7a62', '#5a5a60']; for (let j = 0; j < 48; j++) { x.fillStyle = cols[Math.floor(r() * cols.length)]; x.fillRect(0, j * h / 48, w, h / 48 + 1); }
      x.fillStyle = 'rgba(40,30,20,.25)'; for (let j = 0; j < 48; j++) for (let i = 0; i < w; i += w / 64) x.fillRect(i, j * h / 48, w / 200, h / 48); }, [256, 256]), BX, RUG, -18.95, 2.0, .012, 1.15);
    const bed = new THREE.Group(); bed.position.set(BX, 0, BZ); g.add(bed);
    add(bed, merged([B(1.72, .26, 2.1, 0, .1, 0), ...[[-1, -1], [1, -1], [-1, 1], [1, 1]].map(([a, b]) => B(.06, .1, .06, a * .8, 0, b * .99))]), M.wood);
    box(bed, linen, 0, .36, 0, 1.6, .2, 2.0);
    add(bed, merged([B(1.76, .03, 1.2, 0, .56, .42), B(.02, .26, 1.2, -.87, .33, .42), B(.02, .26, 1.2, .87, .33, .42), B(1.76, .26, .02, 0, .33, 1.02)]), quilt);
    for (const s of [-1, 1]) add(bed, pillowGeometry(.62, .4, .14), linen, s * .38, .64, -.78, -1.2, 0, 0);
    add(bed, pillowGeometry(.42, .42, .13), quilt, -.2, .7, -.55, -1.0, .2, 0);
    const hb = new THREE.Group(); hb.position.set(0, 0, -1.07); bed.add(hb);
    add(hb, merged([B(.06, 1.15, .06, -.9, 0, 0), B(.06, 1.15, .06, .9, 0, 0), B(1.86, .06, .06, 0, 1.12, 0), B(1.86, .05, .05, 0, .42, 0)]), M.wood);
    add(hb, new THREE.PlaneGeometry(1.74, .68), cane, 0, .79, .01);
    footprint(BX - .88, -21.25, BX + .88, -19.1); shade('Z07', BX - .87, -21.25, BX + .87, -19.1, .45);
    for (const s of [-1, 1]) { const nx = BX + s * 1.12, n = new THREE.Group(); n.position.set(nx, 0, -20.98); g.add(n); add(n, merged([B(.44, .5, .38, 0, 0, 0)]), M.wood);
      add(n, new THREE.PlaneGeometry(.38, .14), cane, 0, .36, .191); bambooLamp(n, 0, .5, 0, { r: .075, h: .2 }); footprint(nx - .23, -21.2, nx + .23, -20.77); shade('Z07', nx - .22, -21.2, nx + .22, -20.78, .35); }
    signStand(g, ['Second Life Bangladesh · bedroom', 'Kantha patchwork from garment offcuts', 'Illustrative room-set · option A'], 14.55, -18.75, Math.PI * .25);
  }
  if (want('BEL_ROOMSET_HOSPITALITY')) {
    const g = item('BEL_ROOMSET_HOSPITALITY');   // along the solid south wall (behind it: the experience-centre bays)
    const hang = new THREE.Group(); hang.position.set(16.4, .82, -10.885); hang.rotation.y = Math.PI; g.add(hang);
    add(hang, new THREE.PlaneGeometry(2.4, 1.28), textileMat('kantha_hanging', (x, w, h) => drawKantha(x, w, h, 13), [768, 410]), 0, .66, .004);
    add(hang, new THREE.CylinderGeometry(.018, .018, 2.55, 12), M.bamboo, 0, 1.32, .025, 0, 0, Math.PI / 2);
    standingCard(g, ['Nakshi kantha', 'By a rural embroiderer: placeholder,', 'to be commissioned, paid and credited'], 17.75, 0, -11.12, Math.PI + .3, { w: .18, h: .1 });
    box(g, wovenMaterial('rug_jute_hosp', 'twill', '#bfa577', [12, 7]), 16.4, RUG, -11.95, 2.5, .01, 1.45);
    caneArmchair(g, 15.55, -12.0, Math.PI - .35); caneArmchair(g, 17.25, -12.0, Math.PI + .35);
    for (const x of [15.55, 17.25]) { footprint(x - .4, -12.4, x + .4, -11.6); shade('Z07', x - .38, -12.38, x + .38, -11.62, .45); }
    const rt = new THREE.Group(); rt.position.set(16.4, 0, -11.75); g.add(rt);
    add(rt, new THREE.CylinderGeometry(.32, .32, .035, 40), std('jute_composite_top', () => ({ color: '#b39463', roughness: .7, map: weaveMap('twill', [4, 4]) })), 0, .405, 0);
    for (let k = 0; k < 3; k++) { const a = k / 3 * Math.PI * 2 + .5; add(rt, new THREE.CylinderGeometry(.016, .02, .4, 10), M.bamboo, Math.cos(a) * .2, .2, Math.sin(a) * .2); }
    cup(rt, -.08, .42, .05, 'teacup', M.clayCream); cup(rt, .1, .42, -.04, 'teacup', M.clayCream); teapot(rt, 0, .42, .12, .6);
    footprint(16.06, -12.09, 16.74, -11.41); shade('Z07', 16.08, -12.07, 16.72, -11.43, .35);
    kashVase(g, 14.45, -11.35); kashVase(g, 18.45, -11.3, .5);
    signStand(g, ['Future of Bengal · hospitality', 'Cane, bamboo and jute composite for hotels', 'Illustrative room-set · option A'], 14.05, -12.6, Math.PI * .2);
  }
  if (want('BEL_ACADEMY')) {
    const g = item('BEL_ACADEMY');   // inside the glass accounts suite: every partition and door stays (D50 entrance, D51 to the north corridor)
    const rows = [-15.2, -13.95, -12.7, -11.45, -10.2], cols = [3.98, 6.08], seats = [], desks = [];
    for (const z of rows) for (const x of cols) { desks.push([x, 0, z, 0]); for (const dx of [-.37, .37]) seats.push([x + dx, 0, z + .56, Math.PI]); }
    instances(g, tableWood(1.5, .6, .74), M.wood, desks); instances(g, chairWood, M.wood, seats); instances(g, chairCane, cane, seats);
    for (const [x, , z] of desks) { footprint(x - .77, z - .32, x + .77, z + .32); shade('Z06', x - .75, z - .3, x + .75, z + .3, .4); }
    for (const [x, , z] of seats) { footprint(x - .23, z - .23, x + .23, z + .23); shade('Z06', x - .21, z - .21, x + .21, z + .21, .28); }
    for (const [x, , z] of desks) for (const dx of [-.37, .37]) { const k = Math.round((x + dx) * 10 + z) % 3;
      if (k === 0) swatch(g, x + dx, .74, z - .05, 'jute', 'twill', .13, .2); else if (k === 1) add(g, new THREE.PlaneGeometry(.21, .28), std('notebook', () => ({ color: '#efe8da', roughness: .9 })), x + dx, .742, z - .02, -Math.PI / 2, 0, .15); else swatch(g, x + dx, .74, z - .05, 'hogla', 'plain', .12, -.15); }
    // teaching zone at the north glass: demonstration bench with a hands camera, a mobile screen, a pin-up board
    const db = new THREE.Group(); db.position.set(5.1, 0, -16.6); db.rotation.y = Math.PI; g.add(db);
    add(db, tableWood(2.0, .7, .9), M.oak); box(db, M.wood, 0, .12, 0, 1.86, .02, .56);
    add(db, merged([B(.04, .8, .04, .8, .9, .3), B(.04, .04, .5, .8, 1.68, .08)]), std('steel_dark', () => ({ color: '#2e2e30', metalness: .6, roughness: .45 }))); box(db, std('cam_body', () => ({ color: '#151515', roughness: .4 })), .8, 1.6, -.15, .09, .07, .12);
    const fl = new THREE.Group(); fl.position.set(-.35, .9, 0); db.add(fl);
    for (const s of [-1, 1]) box(fl, M.oak, s * .2, 0, 0, .025, .32, .025); box(fl, M.oak, 0, .3, 0, .43, .02, .02); box(fl, M.oak, 0, .06, 0, .43, .02, .02);
    for (let k = 0; k < 13; k++) add(fl, new THREE.CylinderGeometry(.0012, .0012, .24, 4), std('warp', () => ({ color: '#e7dcc4', roughness: .8 })), -.18 + k * .03, .18, 0);
    add(fl, new THREE.PlaneGeometry(.38, .08), wovenMaterial('jute_band', 'twill', FIBRE.jute, [3, 1]), 0, .11, .003);
    for (const [dx, col] of [[.2, '#8f4a3a'], [.32, '#c9a565'], [.44, '#3d5170']]) add(db, new THREE.CylinderGeometry(.035, .05, .17, 20), std('cone_' + col, () => ({ color: col, roughness: .9, map: weaveMap('coil', [3, 6]) })), dx, .985, .1);
    basket(db, -.75, .9, .05, { r: .13, h: .16, kind: 'coil', fibre: 'jute' });
    footprint(4.07, -16.97, 6.13, -16.23); shade('Z06', 4.1, -16.95, 6.1, -16.25, .45);
    const scr = new THREE.Group(); scr.position.set(3.35, 0, -16.95); g.add(scr);
    add(scr, merged([B(.6, .03, .5, 0, 0, 0), B(.06, 1.75, .06, 0, .03, -.05)]), std('steel_dark', () => ({})));
    box(scr, std('screen_bezel', () => ({ color: '#111', roughness: .35 })), 0, .95, .0, 1.47, .85, .05);
    const slide = std('lesson_slide', () => { const c = canvas(px(640), px(360)), x = c.getContext('2d'), W = c.width, H = c.height; x.fillStyle = '#f3ede2'; x.fillRect(0, 0, W, H);
      x.fillStyle = '#3c2a1e'; x.font = `600 ${H * .085}px system-ui, sans-serif`; x.fillText('Lesson 1 · From fibre to product', W * .06, H * .17);
      x.fillStyle = '#9c5534'; x.fillRect(W * .06, H * .22, W * .1, H * .012);
      [['Fibre', '#c9a565'], ['Technique', '#8f4a3a'], ['Prototype', '#3d5170'], ['Test', '#6f7a4c']].forEach(([t, col], i) => { const X = W * (.06 + i * .23); x.fillStyle = col; x.fillRect(X, H * .36, W * .19, H * .3); x.fillStyle = '#fff'; x.font = `500 ${H * .06}px system-ui, sans-serif`; x.fillText(t, X + W * .02, H * .53);
        if (i < 3) { x.fillStyle = '#3c2a1e'; x.fillText('›', X + W * .2, H * .53); } });
      x.fillStyle = '#5b4636'; x.font = `400 ${H * .05}px system-ui, sans-serif`; x.fillText('Illustrative lesson · Design Education Academy (option A)', W * .06, H * .85);
      const t = tex(c, { clamp: true }); return { map: t, emissive: '#ffffff', emissiveMap: t, emissiveIntensity: .55, roughness: .4 }; });
    add(scr, new THREE.PlaneGeometry(1.4, .79), slide, 0, 1.375, .027);
    footprint(3.03, -17.22, 3.67, -16.68); shade('Z06', 3.05, -17.2, 3.65, -16.7, .4);
    const pin = new THREE.Group(); pin.position.set(6.95, 0, -16.95); g.add(pin);
    add(pin, merged([B(.04, 1.75, .04, -.42, 0, 0), B(.04, 1.75, .04, .42, 0, 0), B(.9, .04, .3, 0, 0, 0)]), M.oak);
    box(pin, std('felt_board', () => ({ color: '#6f6658', roughness: 1, map: weaveMap('plain', [6, 8]) })), 0, .55, 0, .82, 1.15, .03);
    [['jute', 'twill'], ['cane', 'lattice'], ['hyacinth', 'plait'], ['hogla', 'plain'], ['bamboo', 'twill'], ['kaisa', 'coil']].forEach(([f, k], i) => add(pin, new THREE.PlaneGeometry(.17, .17), wovenMaterial(`sw_${f}${k}`, k, FIBRE[f], [2, 2]), -.25 + (i % 3) * .25, 1.42 - Math.floor(i / 3) * .25, .017));
    add(pin, new THREE.PlaneGeometry(.36, .25), std('sketch', () => ({ color: '#f4efe4', roughness: .9 })), -.15, .82, .017); add(pin, new THREE.PlaneGeometry(.25, .3), textileMat('kantha_pin', (x, w, h) => drawKantha(x, w, h, 17), [192, 230]), .22, .8, .017);
    footprint(6.48, -17.12, 7.42, -16.78); shade('Z06', 6.5, -17.1, 7.4, -16.8, .35);
    // materials shelf at the south end, tutor room in the old discussion room
    const sh = new THREE.Group(); sh.position.set(5.35, 0, -6.08); sh.rotation.y = Math.PI; g.add(sh);
    add(sh, merged([B(2.0, .03, .34, 0, 0, 0), B(2.0, .03, .34, 0, .4, 0), B(2.0, .03, .34, 0, .8, 0), B(2.0, .03, .34, 0, 1.17, 0), B(.03, 1.2, .34, -1.0, 0, 0), B(.03, 1.2, .34, 1.0, 0, 0)]), M.wood);
    basket(sh, -.7, .03, 0, { r: .14, h: .2, kind: 'twill', fibre: 'jute' }); basket(sh, -.25, .03, 0, { r: .13, h: .2, kind: 'plait', fibre: 'hyacinth' }); basket(sh, .3, .03, 0, { r: .14, h: .18, kind: 'coil', fibre: 'kaisa' });
    for (let k = 0; k < 8; k++) box(sh, std('book_' + (k % 4), () => ({ color: ['#8f4a3a', '#3d5170', '#c9a565', '#6f7a4c'][k % 4], roughness: .8 })), -.8 + k * .07, .43, 0, .05, .26, .2);
    for (const [dx, col] of [[.25, '#8f4a3a'], [.37, '#c9a565'], [.49, '#3d5170'], [.61, '#6f7a4c']]) add(sh, new THREE.CylinderGeometry(.035, .05, .17, 20), std('cone_' + col, () => ({ color: col, roughness: .9, map: weaveMap('coil', [3, 6]) })), dx, .915, 0);
    tile(sh, -.6, .83, 0, .12); tile(sh, -.42, .83, 0, .12, .3); bambooLamp(sh, .75, .43, 0, { r: .08, h: .24 });
    footprint(4.33, -6.27, 6.37, -5.89); shade('Z06', 4.35, -6.25, 6.35, -5.9, .4);
    const tut = new THREE.Group(); tut.position.set(8.55, 0, -6.75); g.add(tut); add(tut, tableWood(.9, .6, .74), M.wood);
    const tutorSeats = [[8.55, 0, -7.38, 0], [7.75, 0, -6.75, Math.PI / 2]];   // facing the table (south and east)
    instances(g, chairWood, M.wood, tutorSeats); instances(g, chairCane, cane, tutorSeats);
    bambooLamp(tut, .3, .74, -.1, { r: .07, h: .2 }); footprint(8.08, -7.08, 9.02, -6.42); shade('Z06', 8.1, -7.06, 9.0, -6.44, .4); footprint(7.52, -7.6, 8.78, -6.52);
    standingCard(g, ['Tutor room', 'One-to-one sessions and course planning'], 8.85, .74, -6.55, Math.PI + .3, { w: .16, h: .07 });
    signStand(g, ['Design Education Academy', 'Option A only: if the accounts team moves', '20 seats shown; the fire engineer sets', 'the capacity, not this drawing'], 3.3, -8.15, -.25);
  }
  // ---------------------------------------------------------------- the design wing (every option): making line, library, lab, workshop
  if (want('BEL_MAKING_LINE')) {
    // the solid south wall of the corridor's north strip (face z -21.4104; the strip's north side and the corridor are glass)
    const g = item('BEL_MAKING_LINE'), WZ = -21.4104, LY = .98, xs = [22.85, 23.5, 24.15, 24.8, 25.45, 26.1];
    for (const x of xs) box(g, M.oak, x, LY, WZ - .066, .6, .03, .13);
    footprint(22.5, WZ - .14, 26.42, WZ);
    const step = (i, lines) => add(g, new THREE.PlaneGeometry(.5, .26), card(lines, { w: .5, h: .26, scale: 1.1 }), xs[i], 1.47, WZ - .004, 0, Math.PI);
    const Y = LY + .03, Z = WZ - .07;
    for (let k = 0; k < 9; k++) add(g, new THREE.BoxGeometry(.5, .005, .02), wovenMaterial('hogla_leaf', 'plain', FIBRE.hogla, [6, 1]), xs[0], Y + .003 + Math.floor(k / 3) * .006, Z + (k % 3 - 1) * .022, 0, (k - 4) * .02);
    add(g, new THREE.TorusGeometry(.04, .006, 6, 20), std('band', () => ({ color: '#6b4a2b', roughness: .9 })), xs[0] - .12, Y + .012, Z, Math.PI / 2);
    for (let k = 0; k < 3; k++) add(g, new THREE.TorusGeometry(.05 - k * .005, .008, 8, 28), std('hogla_rope', () => ({ color: FIBRE.hogla, roughness: .9, map: weaveMap('coil', [8, 1]) })), xs[1] - .14 + k * .14, Y + .008, Z, Math.PI / 2);
    const fr = new THREE.Group(); fr.position.set(xs[2], Y, Z); fr.rotation.y = Math.PI; g.add(fr); box(fr, M.wood, 0, 0, 0, .3, .02, .1);   // faces the strip box(fr, M.wood, 0, .02, -.03, .28, .2, .02);
    add(fr, new THREE.PlaneGeometry(.24, .16), wovenMaterial('hogla_mat', 'twill', FIBRE.hogla, [3, 1.2]), 0, .12, -.019);
    basket(g, xs[3], Y, Z, { r: .1, h: .14, kind: 'twill', fibre: 'hogla', handles: true });
    add(g, new THREE.PlaneGeometry(.05, .03), card(['prototype'], { w: .05, h: .03, scale: .4 }), xs[3] + .12, Y + .1, Z + .02, 0, Math.PI - .3);
    basket(g, xs[4], Y, Z, { r: .1, h: .14, kind: 'twill', fibre: 'hogla', handles: true, ry: .6 });
    basket(g, xs[5] - .08, Y, Z, { r: .11, h: .13, kind: 'twill', fibre: 'hogla' }); basket(g, xs[5] - .08, Y + .012, Z, { r: .08, h: .13, kind: 'twill', fibre: 'hogla' }); basket(g, xs[5] + .14, Y, Z, { r: .06, h: .09, kind: 'plait', fibre: 'hyacinth' });
    step(0, ['1 · Raw material', 'Hogla leaves, cut and sun-dried']); step(1, ['2 · Preparation', 'Twisted into rope']); step(2, ['3 · Technique', 'Coiling and stitching']);
    step(3, ['4 · Prototype', 'Form, size and handles']); step(4, ['5 · Testing', 'Moisture, mould, strength', 'Records to be added']); step(5, ['6 · Collection', 'River to Home (illustrative)']);
    const tc = canvas(px(1280), px(64)), tx = tc.getContext('2d'); tx.fillStyle = '#b88c5c'; tx.fillRect(0, 0, tc.width, tc.height); tx.fillStyle = '#3c2a1e'; tx.font = `600 ${tc.height * .46}px system-ui, 'Segoe UI', sans-serif`; tx.textBaseline = 'middle';
    tx.fillText('The making line · from rural hands to global homes · one basket in six steps (illustrative)', tc.width * .02, tc.height * .54);
    add(g, new THREE.PlaneGeometry(3.9, .195), std('making_title', () => ({ map: tex(tc, { clamp: true }), roughness: .6 })), (xs[0] + xs[5]) / 2, 1.9, WZ - .004, 0, Math.PI);
  }
  if (want('BEL_MATERIALS_LIBRARY')) {
    const g = item('BEL_MATERIALS_LIBRARY');   // low shelf F132 top 0.7112 (x 22.25-22.61, z -9.41..-6.74); review table F134 top 0.9144, D65 booth at x 23.98-24.79
    const T = .7112, X = 22.43, fibres = [['jute', 'twill', 'Jute'], ['hogla', 'plain', 'Hogla'], ['cane', 'lattice', 'Cane'], ['bamboo', 'twill', 'Bamboo'], ['hyacinth', 'plait', 'Water hyacinth'], ['kaisa', 'coil', 'Kaisa grass'], ['coconut', null, 'Coconut shell'], ['terracotta', null, 'Terracotta']];
    fibres.forEach(([f, k, name], i) => {
      const z = -9.25 + i * .32, b = new THREE.Group(); b.position.set(X, T, z); g.add(b);
      const side = k ? wovenMaterial(`box_${f}`, k, FIBRE[f], [2, 1]) : f === 'coconut' ? std('coconut_shell', () => ({ color: '#5a3b24', roughness: .7, map: M.bark.map })) : M.terracotta;
      add(b, merged([B(.3, .14, .015, 0, 0, -.135), B(.3, .14, .015, 0, 0, .135), B(.015, .14, .27, -.143, 0, 0), B(.015, .14, .27, .143, 0, 0), B(.3, .012, .3, 0, 0, 0)]), M.oak);
      add(b, new THREE.BoxGeometry(.27, .1, .25), side, 0, .07, 0);
      add(b, new THREE.PlaneGeometry(.2, .05), card([name], { w: .2, h: .05, scale: .6 }), .152, .07, 0, 0, Math.PI / 2);
    });
    const RT = .9144; [[24.97, -9.2, .1], [24.97, -8.88, -.05], [23.8, -9.15, .08]].forEach(([x, z, ry], i) =>
      add(g, new THREE.PlaneGeometry(.15, .21), card(['Material Passport', ['Material: hogla', 'Material: jute', 'Material: cane'][i], 'Origin: to be documented', 'Maker: to be identified', 'Tests: none yet'], { w: .15, h: .21, scale: .8 }), x, RT + .002, z, -Math.PI / 2, 0, ry));
    add(g, new THREE.TorusGeometry(.04, .005, 8, 24), std('brass', () => ({ color: '#b08d57', metalness: .8, roughness: .35 })), 23.8, RT + .006, -8.7, Math.PI / 2);
    add(g, new THREE.CylinderGeometry(.008, .008, .09, 8), M.wood, 23.8 + .07, RT + .008, -8.66, Math.PI / 2, .5, 0);
  }
  if (want('BEL_TEST_LAB')) {
    const g = item('BEL_TEST_LAB'); const T = .7874, X = 22.56;   // post-processing bench F143 (terrazzo top 0.7874), x 22.25-22.88, z -14.87..-12.06
    const clear = std('clear_box', () => ({ color: '#e8f0f2', roughness: .1, transparent: true, opacity: .35, depthWrite: false }));
    [['jute', 'twill'], ['hogla', 'plain'], ['cane', 'lattice'], ['hyacinth', 'plait']].forEach(([f, k], i) => {
      const z = -14.55 + i * .3; swatch(g, X, T, z, f, k, .14, i * .2);
      add(g, new THREE.BoxGeometry(.22, .16, .22), clear, X, T + .08, z);
      add(g, new THREE.PlaneGeometry(.1, .03), card([`Sample ${i + 1}`], { w: .1, h: .03, scale: .4 }), X + .111, T + .12, z, 0, Math.PI / 2);
    });
    box(g, std('scale_body', () => ({ color: '#dfe2e4', roughness: .4 })), X, T, -13.2, .24, .05, .26); box(g, std('lcd', () => ({ color: '#1b1f22', roughness: .3 })), X + .121, T + .015, -13.2, .002, .025, .08);
    box(g, std('meter_body', () => ({ color: '#e0b43a', roughness: .5 })), X, T, -12.9, .07, .03, .15); for (const dz of [-.015, .015]) add(g, new THREE.CylinderGeometry(.002, .002, .05, 6), std('steel', () => ({ color: '#c8c8c8', metalness: .8, roughness: .3 })), X, T + .015, -12.9 - .1 + dz, Math.PI / 2, 0, 0);
    add(g, new THREE.PlaneGeometry(.21, .29), card(['Test log', 'Moisture and mould', 'Method: to agree with an accredited lab', 'Records to be added'], { w: .21, h: .29, scale: .9 }), X, T + .004, -12.48, -Math.PI / 2, 0, -.1);
    standingCard(g, ['Materials lab', 'No results shown until tests are done'], X + .2, T, -12.2, Math.PI / 2, { w: .18, h: .07 });
  }
  if (want('BEL_PROTOTYPE_WORKSHOP')) {
    const g = item('BEL_PROTOTYPE_WORKSHOP'); const T = .9145, X = 25.53;   // pattern table F151 top 0.9145, x 24.92-26.14, z -20.52..-18.08; steam station F155 top 0.8636
    add(g, lathe([[0, 0], [.13, 0], [.12, .2], [.1, .22], [0, .22]], 32), M.wood, X, T, -19.85);
    basket(g, X, T + .02, -19.85, { r: .15, h: .22, kind: 'lattice', fibre: 'cane', partial: .55 });
    for (let k = 0; k < 9; k++) box(g, M.bamboo, X - .1 + (k % 3) * .03, T + Math.floor(k / 3) * .012, -19.15, .02, .01, .9, (k - 4) * .01);
    add(g, new THREE.TorusGeometry(.17, .007, 8, 40), std('cane_coil', () => ({ color: FIBRE.cane, roughness: .5 })), X - .05, T + .007, -18.45, Math.PI / 2);
    const mallet = new THREE.Group(); mallet.position.set(X + .35, T, -18.55); mallet.rotation.y = .6; g.add(mallet);
    add(mallet, new THREE.CylinderGeometry(.035, .035, .1, 16), M.wood, 0, .035, 0, 0, 0, Math.PI / 2); add(mallet, new THREE.CylinderGeometry(.01, .01, .25, 8), M.oak, 0, .035, .13, Math.PI / 2, 0, 0);
    standingCard(g, ['Prototype workshop', 'Cane and bamboo', 'Dust extraction: to be engineered'], X - .45, T, -18.35, Math.PI / 2, { w: .18, h: .09 });
    // a dust-extraction hood over the table, marked as not yet designed
    const hood = std('hood_steel', () => ({ color: '#b9bec2', metalness: .55, roughness: .45 }));
    add(g, new THREE.CylinderGeometry(.12, .45, .3, 4, 1, true), std('hood_steel_2s', () => ({ color: '#b9bec2', metalness: .55, roughness: .45, side: THREE.DoubleSide })), X, 2.0, -19.3, 0, Math.PI / 4, 0);   // capture 0.64 m square at 1.85 m
    add(g, new THREE.CylinderGeometry(.09, .09, 2.895 - 2.15, 16), hood, X, (2.15 + 2.895) / 2, -19.3);
    add(g, new THREE.PlaneGeometry(.34, .08), card(['Dust extraction: to be engineered'], { w: .34, h: .08, scale: .8 }), X + .335, 1.95, -19.3, 0, Math.PI / 2);
    // steam bending: a cane strip around a pegged board on the steam station
    const jig = new THREE.Group(); jig.position.set(23.62, .8636, -15.47); g.add(jig); box(jig, M.oak, 0, 0, 0, .5, .025, .3);
    for (let k = 0; k < 6; k++) { const a = Math.PI * (k / 5); add(jig, new THREE.CylinderGeometry(.008, .008, .06, 8), M.wood, Math.cos(a) * .16, .055, -Math.sin(a) * .1 + .05); }
    add(jig, new THREE.TorusGeometry(.15, .006, 6, 24, Math.PI), std('cane_coil', () => ({})), 0, .045, .05, -Math.PI / 2, 0, 0);
  }
  // the floor finishes go in last, so their occlusion maps hold the contact shadows of everything above
  if (want('BEL_UTHAN')) floorOverlay(group.getObjectByName('BEL_UTHAN'), 'Z07', [9.32, -21.29, 22.0, -10.87], { map: juteFloor('z07', '#cdbb94', 81), repeat: [25, 21], color: '#cfc8bd' });
  if (want('BEL_ACADEMY')) {
    const jute = juteFloor('z06', '#a89474', 83), floor = group.getObjectByName('BEL_ACADEMY');
    floorOverlay(floor, 'Z06', [2.74, -17.48, 9.19, -8.55], { map: jute, repeat: [13, 18], color: '#c9c2b6' });
    floorOverlay(floor, 'Z06', [2.74, -8.55, 6.56, -7.4], { map: clone(jute), repeat: [8, 2.3], color: '#c9c2b6' });
    floorOverlay(floor, 'Z06', [4.11, -7.4, 6.56, -5.87], { map: clone(jute), repeat: [5, 3], color: '#c9c2b6' });
    floorOverlay(floor, 'Z06', [6.57, -8.54, 9.19, -5.87], { map: clone(jute), repeat: [5.2, 5.3], color: '#c9c2b6' });
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
  const sources = new Set(), pixels = textures.reduce((s, t) => sources.has(t.source) ? s : (sources.add(t.source), s + (t.image?.width || 0) * (t.image?.height || 0)), 0);   // clones share their source's GPU memory
  const stats = { items: items.length, meshes: 0, instancedLeaves: 0, textures: textures.length, textureMB: Math.round(pixels * 4 * 1.33 / 1e5) / 10 };
  group.traverse(o => { if (o.isInstancedMesh) stats.instancedLeaves += o.count; else if (o.isMesh) stats.meshes++; });
  function blocksMovement(x, z, radius = .15) { return footprints.some(([x0, z0, x1, z1]) => x > x0 - radius && x < x1 + radius && z > z0 - radius && z < z1 + radius); }
  return {
    group, stats, items: items.map(i => ({ id: i.id, zone: i.zone, note: i.note })), footprints,
    textures: () => textures, blocksMovement,
    dispose() { geometries.forEach(g => g.dispose()); materials.forEach(m => m.dispose()); textures.forEach(t => t.dispose()); },
  };
}
