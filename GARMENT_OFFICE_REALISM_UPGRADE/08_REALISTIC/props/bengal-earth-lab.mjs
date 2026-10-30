/** Bengal Earth Lab proposal layer, used only by the /bengal-earth-lab/ route (Claude, 29-30 Oct 2026).
 * "The Living Bengal Factory": a knitwear (RMG) factory whose fabric comes from the earth (cotton, jute) and from what
 * was already made (cutting waste and used garments, spun again), with Bengal craft (kutir shilpo) as the addition that
 * represents Bangladesh: a few small trees, bonsai and stones, work by rural artists, rural instruments, kantha, clay and
 * wood tableware, the Sun wall (a concept demonstration with no data). The approved knitwear dressing stays (garments,
 * forms, sample cards, review sets); this layer adds the fabric story around it. Self-made procedural geometry and canvas
 * artwork only. Makers, artists, growers, suppliers, recycling partners, fibre origins, certificates, test records and
 * energy data are still to be identified: nothing here is claimed as made, recycled, tested or measured.
 * The route config hides the approved items this layer replaces (hideNodes) and every replacement keeps the same
 * footprint, so the approved walk grid stays valid; new floor items report their footprint through blocksMovement().
 * Usage: buildBengalEarthLab(THREE, { zones, drinkware, anisotropy, detail }) -> { group, items, stats, textures, blocksMovement, dispose }
 * Coordinates: viewer metres, x east, y up, z south (as office_web_metadata.json).
 */
import { knitTile } from './knit-tiles.mjs';

export const BEL_ITEMS = [
  // arrival: Bengal craft, a few living trees, rural art and music, the Sun wall
  { id: 'BEL_GATE_BONSAI', zone: 'Z01', note: 'A banyan bonsai on a granite plinth beside the glass gate, in place of the approved potted tree and on its footprint. Grower, species and stone source to be confirmed; it takes turns in daylight at the studio windows.' },
  { id: 'BEL_LOBBY_STONES', zone: 'Z01', note: 'Three granite stones in place of the approved small planter, on its footprint. Stone only from a documented legal source, never from illegal river extraction.' },
  { id: 'BEL_EARTH_DESK', zone: 'Z01', note: 'Handmade terracotta tiles on the visitor face of the check-in desk (proposal; potter to be identified).' },
  { id: 'BEL_LOBBY_RELIEF', zone: 'Z01', note: 'Six terracotta plaques by a rural artist on the free west wall: sun, river boat, shapla, fish, rice and a doel bird. Placeholder composition: the artist is to be commissioned, paid and credited by name.' },
  { id: 'BEL_RECEPTION_TREE', zone: 'Z02', note: 'A small fig tree in a handmade terracotta planter, in place of the approved potted tree and on its footprint.' },
  { id: 'BEL_RECEPTION_ALOE', zone: 'Z02', note: 'Ghritokumari (aloe) in a clay pot on a low stone, in place of the approved small planter: a plant traditionally kept in Bengali homes; no medical claim.' },
  { id: 'BEL_INSTRUMENTS', zone: 'Z02', note: 'Rural instruments above the console: ektara, dotara and banshi on an oak rail, a dhol on the console. Makers to be identified and credited; played at events, never used as props.' },
  { id: 'BEL_TEA_CLAY', zone: 'Z02', note: 'Tea in clay cups from a clay pot on a wooden tray, in place of the porcelain props. Glazes to be tested for lead and cadmium release before use.' },
  { id: 'BEL_SUN_WALL', zone: 'Z03', note: 'The Sun wall: sun, solar generation, direct use and storage, operations, with grid and backup shown. Concept demonstration, not live factory data. The message stays "Designed for a Solar-Powered Future" until measured evidence exists.' },
  { id: 'BEL_EARTH_WALL', zone: 'Z03', note: 'Handmade terracotta tiles between the guest WC doors, with a narrow oak ledge of clay bowls holding the raw side of the fabric story: cotton, jute, fibre recovered from cutting waste and natural indigo, beside clay (proposal).' },
  // the experience centre: the approved knitwear stays; the fabric story is added around it
  { id: 'BEL_FABRIC_STORIES', zone: 'Z30', note: 'The four approved forms keep their knitwear. At the foot of each, a dish of the fibre and a fabric story card: cutting waste sorted by colour and spun again, a jute and cotton blend (research), used garments taken back, cotton. Illustrative stories: fibre origins, recycled shares and tests are still to be documented.' },
  { id: 'BEL_BAY_STORIES', zone: 'Z30', note: 'The four approved garment bays, each with a fabric story at its foot: Earth (cotton), Golden fibre (a jute and cotton blend, research only), Second life from cutting waste (jhut sorted by colour and spun again) and Second life from used garments (take-back, repair in kantha stitch, recycling). Recycling partners, certificates and tests are still to be identified.' },
  { id: 'BEL_EC_TREE', zone: 'Z30', note: 'A small fig tree in a handmade terracotta planter beside the boardroom door, in place of the approved potted tree and on its footprint.' },
  { id: 'BEL_INDIGO_SWAGS', zone: 'Z30', note: 'Natural indigo overhead: three resist-dyed cloths in shallow swags under the deck, in place of the approved cloth fins on this route and clear of the AC unit and the smoke detector. Indigo dyer to be identified; colourfastness to be tested.' },
  { id: 'BEL_JHUT_RIVER', zone: 'Z30', note: 'An installation between the forms and the material table: a sewing machine on a wooden table and a river of patchwork pieced from cutting waste, running off the table and across the floor. Makers to be credited; not a product.' },
  { id: 'BEL_WATER_KOLSHI', zone: 'Z30', note: 'Drinking water from a clay kolshi with clay cups, in place of the approved water point and on its spot. The source is client-stated (deep tube well); only dated laboratory reports will ever be shown, and none are available yet.' },
  { id: 'BEL_BOARD_BONSAI', zone: 'Z08', note: 'A bonsai on a jute-wrapped stand in the corner by the screen, in place of the approved planter; it rotates to the studio windows for light.' },
  { id: 'BEL_STUDIO_SUN_SHELF', zone: 'Z18', note: 'The sunning shelf at the east window W10: three bonsai and a tulsi pot take turns in daylight. Grower and species to be confirmed.' },
  { id: 'BEL_STUDIO_TREE', zone: 'Z18', note: 'A small fig tree in daylight by window W09, in place of the approved potted tree and on its footprint.' },
  { id: 'BEL_CLAY_DRINKWARE', zone: '*', note: 'Every glass, mug, cup, jug, bottle and tray on the route is clay or wood (glazes to be tested; wood with food-safe finishes).' },
  // the design wing in every option: the labs behind the glass of the studio street are the exhibit
  { id: 'BEL_MAKING_LINE', zone: 'Z22', note: 'The making line on the solid wall of the design-wing entrance (the corridor walls are glass): one knit T-shirt in six steps on oak ledges, from fibre (cotton, jute, fibre recovered from cutting waste) to yarn, knit fabric, cut and sew, testing, and wear, repair and return. Illustrative objects; real samples and dated records replace them.' },
  { id: 'BEL_MATERIALS_LIBRARY', zone: 'Z15', note: 'The fibre library on the low shelf: eight labelled boxes (cotton, recycled cotton from cutting waste, recycled fibre from used garments, jute, banana fibre, pineapple leaf fibre, natural indigo, coconut-shell buttons) and Fabric Passport cards on the review table, every field still to be documented. Banana, pineapple and indigo are research only. The D65 colour booth and the approved fabric library stay.' },
  { id: 'BEL_TEST_LAB', zone: 'Z16', note: 'Fabric lab on the post-processing bench: a GSM cutter and a balance, knit swatches marked for wash shrinkage, a grey scale for colourfastness and an empty test log. Methods to be agreed with an accredited laboratory; no results are shown. The 3D printers stay for trims and moulds.' },
  { id: 'BEL_PROTOTYPE_WORKSHOP', zone: 'Z17', note: 'Remake and repair on the pattern table: paper pattern pieces, cutting waste sorted by colour, a panel pieced from offcuts and a T-shirt mended in kantha stitch. The sample machines and forms stay.' },
  // pilot rooms: the small academy, staff and artisan dining, the records room, the buyer project room
  { id: 'BEL_ACADEMY_ANNEX', zone: 'Z21', note: 'The pilot academy in the training room: a class of six at the approved table (knit swatches, yarn cones, a mending kit) and a craft wall of pinned swatches, a kantha mend and sketches. The lounge stays.' },
  { id: 'BEL_TEA_STALL', zone: 'Z20', note: 'The tong, the Bengali tea stall, as the tea point on the free west wall of the dining room: a wall-mounted cart front on two wheels with a painted canopy (rickshaw-art colours), a kettle on a clay stove, clay cups, biscuit jars, an electric lantern in the hurricane form (no kerosene indoors) and three wood-slice stools.' },
  { id: 'BEL_ARTISAN_DINING', zone: 'Z20', note: 'Staff and artisan dining with the same care as the buyer rooms: clay plates, cups and jugs on hogla runners, and water and tea in clay on the pantry counter. Glazes to be tested before use.' },
  { id: 'BEL_RECORDS_ROOM', zone: 'Z09', note: 'The records room: the originals behind every claim on the floor, fibre origins and recycled content first. Labelled evidence files on the table and an Open Record index on the wall; every line still reads "none yet" or "to be collected" until documents arrive.' },
  { id: 'BEL_BUYER_PROJECT', zone: 'Z04', note: 'Buyer project room, which in the pilot is also the export and order desk: knit swatches on a wooden tray, clay water, an order checklist with the fabric passport and a project board whose dates are all "to be agreed".' },
  // option A only (full conversion): shown on this route if the merchandising and accounts teams move; the owner decides
  { id: 'BEL_UTHAN', zone: 'Z07', note: 'Option A only. The Green Uthan: a Bengali courtyard in Merchandising, with a bot-tola seat of handmade terracotta around the steel column, two small fig trees and a banyan bonsai under grow lights (this room has no daylight), split-granite stone seats and an open split-bamboo canopy (fire treatment and smoke-detector coverage to be checked). Natural jute carpet over the whole room.' },
  { id: 'BEL_ARTISAN_CORNER', zone: 'Z07', note: 'Option A only. Artisan corner in the Uthan, by invitation and never as a spectacle: a Chakma back-strap loom (bain) shown only with the consent and participation of Chakma weavers, a Marma weaving and basketry stand (the same consent rule), a nakshi kantha frame, cane basketry and painted terracotta on a sitalpati mat. Quiet, clean crafts only; dusty work stays in the workshop.' },
  { id: 'BEL_UTHAN_CRAFT', zone: 'Z07', note: 'Option A only. The Uthan dressed by hand: kula and dala laid over the bamboo canopy, alpana in rice-paste white around the courtyard (to be painted by rural women artists), four painted bamboo posts with electric lanterns in the hurricane form, natural indigo and undyed yarn and small clay pots hanging from the canopy.' },
  { id: 'BEL_CRAFT_CORNER', zone: 'Z07', note: 'Option A only. A craft corner on the solid south wall: a bamboo trellis with a gamchha, a kantha, a kula and a framed painting by a rural artist (placeholder, to be commissioned), a cane bowl chair on a round sitalpati, a jute pouf and a snake plant in clay.' },
  { id: 'BEL_CRAFT_SHELF', zone: 'Z07', note: 'Option A only. A low bamboo shelf on the solid lower west wall: painted pots in the shokher hari tradition (Rajshahi), tepa putul clay dolls, a dholak and a khol, and a polo (bamboo fish trap) beside it. Makers to be identified, paid and credited.' },
  { id: 'BEL_CIRCLE_WEAR', zone: 'Z07', note: 'Option A only. Circular knitwear studio, 1 · Wear: two bamboo rails of knitwear in earth and recycled fabrics and a low table of folded samples. Illustrative garments, not products on sale.' },
  { id: 'BEL_CIRCLE_REMAKE', zone: 'Z07', note: 'Option A only. Circular knitwear studio, 2 · Remake: cutting waste (jhut) sorted by colour on a sorting table under a basket lamp and in jute sacks, recycled yarn cones and a roll of recycled jersey. Recycling partners to be identified; recycled shares to be certified.' },
  { id: 'BEL_CIRCLE_REPAIR', zone: 'Z07', note: 'Option A only. Circular knitwear studio, 3 · Repair: a live-edge mending table with wood-slice stools under a basket lamp, where knitwear is repaired in kantha running stitch, the Bengal tradition of stitching old cloth into new use. Embroiderers to be invited, paid and credited.' },
  { id: 'BEL_CIRCLE_RETURN', zone: 'Z07', note: 'Option A only. Circular knitwear studio, 4 · Return: take-back bins for worn garments (repair, resale, recycling) beside two bamboo armchairs, a bent-bamboo table and a large nakshi kantha by a rural embroiderer (placeholder; to be commissioned, paid and credited). The take-back pilot is still to be designed.' },
  { id: 'BEL_ACADEMY', zone: 'Z06', note: 'Option A only. The design education academy inside the existing glass accounts suite: 20 seats shown at mango-wood tables, a demonstration bench with a sewing machine and a hands camera, a mobile screen, a pin-up board and a materials shelf; the discussion room becomes the tutor room. Capacity is set by the fire engineer, not by this drawing.' },
];

export function buildBengalEarthLab(THREE, { zones = null, drinkware = [], anisotropy = 4, detail = 1 } = {}) {
  const group = new THREE.Group(); group.name = 'BENGAL_EARTH_LAB';
  const overhead = new THREE.Group(); overhead.name = 'BENGAL_EARTH_LAB_OVERHEAD';   // ceiling-hung items: the app hides them with the ceiling in the dollhouse views
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
  // knitwear and fibre (self-made): the RMG core of the fabric story. Knit fabric uses the approved stitch tiles
  // (props/knit-tiles.mjs), one GPU texture per stitch tinted per colour; fabric UVs are in metres so every piece knits at one scale
  const scaleUV = (g, su, sv) => { const uv = g.attributes.uv; for (let i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) * su, uv.getY(i) * sv); return g; };
  const knitBase = {};
  function knitMap(stitch = 'jersey', repeat = [36, 36]) { if (!knitBase[stitch]) knitBase[stitch] = tex(knitTile(stitch), { srgb: false }); const t = clone(knitBase[stitch]); t.repeat.set(...repeat); return t; }
  const knit = (color, stitch = 'jersey') => std(`knit_${stitch}_${color}`, () => ({ color, map: knitMap(stitch, stitch === 'rib' ? [30, 30] : [36, 36]), roughness: .96, side: THREE.DoubleSide }));
  function melange(key, base, flecks) {   // recycled fabric: a melange of the colours it was spun from, flecks baked into one small canvas
    return std('melange_' + key, () => { const s = px(128), c = canvas(s, s), x = c.getContext('2d'), r = rng(key.length * 53 + 11); x.fillStyle = base; x.fillRect(0, 0, s, s);
      for (let i = 0; i < s * s / 8; i++) { x.fillStyle = flecks[Math.floor(r() * flecks.length)]; x.fillRect(r() * s, r() * s, 1 + r() * 2.4, .7 + r() * .8); }
      x.globalCompositeOperation = 'multiply'; x.scale(1 / 3, 1 / 3); x.fillStyle = x.createPattern(knitTile('jersey'), 'repeat'); x.fillRect(0, 0, s * 3, s * 3); x.setTransform(1, 0, 0, 1, 0, 0); x.globalCompositeOperation = 'source-over';
      return { map: tex(c, { repeat: [12, 12] }), roughness: .96, side: THREE.DoubleSide }; });
  }
  const KN = {   // the fabric palette: earth fibres in natural and dyed colours, recycled melanges
    ecru: knit('#e9e1d0'), oat: knit('#d6c7a8'), indigo: knit('#3a4d6e'), madder: knit('#8f4a3a'), moss: knit('#6f7a4c'), charcoal: knit('#45474a'),
    juteBlend: knit('#c7ae7c', 'rib'), ecruRib: knit('#e9e1d0', 'rib'),
    recNavy: melange('navy', '#3f4c66', ['#55688a', '#2a3448', '#8a97ad', '#e6dccb']), recGrey: melange('grey', '#8e8b86', ['#5f5d5a', '#b9b5ad', '#3d5170', '#8f4a3a']),
    recRed: melange('red', '#8a4a3e', ['#a8604f', '#5e2f27', '#d9cdb4']), recOlive: melange('olive', '#6d744f', ['#8a9166', '#4b5136', '#c9a565']),
  };
  function fibreMat(key, base, flecks = []) {   // loose fibre: short curled strokes over a base colour
    return std('fibre_' + key, () => { const s = 128, c = canvas(s, s), x = c.getContext('2d'), r = rng(key.length * 41 + 3); x.fillStyle = base; x.fillRect(0, 0, s, s);
      for (let i = 0; i < 900; i++) { const fl = flecks.length && r() < .45; x.strokeStyle = fl ? flecks[Math.floor(r() * flecks.length)] : (r() > .5 ? 'rgba(255,255,255,.45)' : 'rgba(60,45,30,.18)'); x.lineWidth = .7 + r() * .6;
        const X = r() * s, Y = r() * s, A = r() * Math.PI * 2, L = 4 + r() * 9; x.beginPath(); x.moveTo(X, Y); x.quadraticCurveTo(X + Math.cos(A + .6) * L * .5, Y + Math.sin(A + .6) * L * .5, X + Math.cos(A) * L, Y + Math.sin(A) * L); x.stroke(); }
      return { map: tex(c, { repeat: [2, 2] }), roughness: 1 }; });
  }
  const FB = {
    cotton: fibreMat('cotton', '#f2eee6'), jute: fibreMat('jute', '#c9a565'), banana: fibreMat('banana', '#d8c7a1'), pineapple: fibreMat('pineapple', '#e6e0d0'),
    jhutNavy: fibreMat('jhut_navy', '#4a5875', ['#6b7c9c', '#2a3448', '#8a97ad']), usedMix: fibreMat('used_mix', '#9a948b', ['#8f4a3a', '#3d5170', '#c9a565', '#6f7a4c', '#e6dccb', '#3b3d40']),
    indigo: std('indigo_cake', () => ({ color: '#24345a', roughness: .9, map: M.soil.map })),
    juteHank: std('jute_fibre', () => { const c = canvas(64, 256), x = c.getContext('2d'), r = rng(23); x.fillStyle = FIBRE.jute; x.fillRect(0, 0, 64, 256); for (let i = 0; i < 160; i++) { x.strokeStyle = r() > .5 ? 'rgba(255,235,190,.35)' : 'rgba(110,80,35,.3)'; x.lineWidth = .8; x.beginPath(); const X = r() * 64; x.moveTo(X, 0); x.lineTo(X + (r() - .5) * 4, 256); x.stroke(); } return { map: tex(c), roughness: .95 }; }),
  };
  const fibreHeap = (parent, x, y, z, r, mat, seed = 1) => add(parent, rockGeometry(r, seed, 1.25, .55, 1.25), mat, x, y, z);
  function cottonStems(parent, x, y, z, { n = 5, h = .55, seed = 1 } = {}) {   // dried cotton stems with open bolls, merged per material
    const r = rng(seed), J = a => (r() - .5) * a, stems = [], fluff = [], bracts = [];
    for (let s = 0; s < n; s++) {
      const a0 = s / n * Math.PI * 2 + J(.4), lean = .03 + r() * .05, H = h * (.8 + r() * .3), top = [Math.cos(a0) * lean * 3, H, Math.sin(a0) * lean * 3];
      stems.push([taperedTube([[0, 0, 0], [top[0] * .4 + J(.02), H * .5, top[2] * .4 + J(.02)], top], .004, .0025, 10, 5)]);
      for (let k = 0; k < 3; k++) {
        const t = .55 + k * .2, a = a0 + k * 2.1 + J(.6), L = .035 + r() * .03, by = H * t, cx = top[0] * t, cz = top[2] * t, bx = cx + Math.cos(a) * L, bz = cz + Math.sin(a) * L;
        stems.push([taperedTube([[cx, by - .04, cz], [cx + Math.cos(a) * L * .5, by - .01, cz + Math.sin(a) * L * .5], [bx, by + .01, bz]], .0025, .0018, 6, 4)]);
        for (let q = 0; q < 4; q++) { const qa = q / 4 * Math.PI * 2 + a; fluff.push([new THREE.SphereGeometry(.016, 10, 7), bx + Math.cos(qa) * .011, by + .03, bz + Math.sin(qa) * .011]);
          bracts.push([new THREE.ConeGeometry(.011, .028, 4), bx + Math.cos(qa + .4) * .015, by + .018, bz + Math.sin(qa + .4) * .015, Math.sin(qa + .4) * 2.3, 0, -Math.cos(qa + .4) * 2.3]); }
      }
    }
    const g = new THREE.Group(); g.position.set(x, y, z); parent.add(g);
    add(g, merged(stems), std('cotton_stem', () => ({ color: '#5b4330', roughness: .85 }))); add(g, merged(fluff), FB.cotton); add(g, merged(bracts), std('cotton_bract', () => ({ color: '#4a3524', roughness: .8 })));
    return g;
  }
  const coneMat = col => std('cone_' + col, () => ({ color: col, roughness: .9, map: weaveMap('coil', [3, 6]) }));
  function yarnCone(parent, x, y, z, mat) { add(parent, new THREE.CylinderGeometry(.03, .05, .17, 24), mat, x, y + .085, z); add(parent, new THREE.CylinderGeometry(.011, .015, .02, 12), std('cone_core', () => ({ color: '#c9a86e', roughness: .8 })), x, y + .18, z); }
  function fabricRoll(parent, x, y, z, mat, { len = .6, r = .06, ry = 0 } = {}) {   // a roll lying along local x, resting on y
    const g = new THREE.Group(); g.position.set(x, y + r, z); g.rotation.y = ry; parent.add(g);
    add(g, scaleUV(new THREE.CylinderGeometry(r, r, len, 32), 2 * Math.PI * r, len), mat, 0, 0, 0, 0, 0, Math.PI / 2);
    add(g, new THREE.CylinderGeometry(.02, .02, len + .03, 12), std('cone_core', () => ({})), 0, 0, 0, 0, 0, Math.PI / 2); return g;
  }
  const foldGeo = scaleUV(pillowGeometry(.3, .24, .045, 10), .3, .24); geometries.push(foldGeo);
  function foldedStack(parent, x, y, z, mats, ry = 0) {   // folded knitwear, one piece per material, bottom at y
    mats.forEach((m, k) => { const p = new THREE.Mesh(foldGeo, m); p.position.set(x + (k % 2 ? .006 : -.004), y + .0225 + k * .04, z); p.rotation.set(-Math.PI / 2, 0, ry + (k - (mats.length - 1) / 2) * .03); parent.add(p); });
  }
  function garmentOutline(kind) {   // front silhouette, shoulder seam at y 0, x across; tee or long-sleeved sweat
    const R = kind === 'sweat' ? [[.2, -.035], [.29, -.15], [.37, -.58], [.31, -.61], [.245, -.25], [.235, -.66], [.225, -.69]] : [[.2, -.035], [.33, -.17], [.275, -.245], [.235, -.2], [.24, -.7]];
    const s = new THREE.Shape(); s.moveTo(-.085, 0); s.quadraticCurveTo(0, -.075, .085, 0);
    for (const [x, y] of R) s.lineTo(x, y); for (const [x, y] of R.slice().reverse()) s.lineTo(-x, y); s.closePath(); return s;
  }
  const garmentGeos = {};
  function garmentGeometry(kind) {
    if (!garmentGeos[kind]) { const g = new THREE.ExtrudeGeometry(garmentOutline(kind), { depth: .02, bevelEnabled: true, bevelThickness: .014, bevelSize: .012, bevelSegments: 2, curveSegments: 8 }); g.translate(0, 0, -.01); geometries.push(g); garmentGeos[kind] = g; }
    return garmentGeos[kind];
  }
  function hangingGarment(parent, x, y, z, ry, mat, kind = 'tee') {   // y = rail centre; the garment faces local +z, the rail runs along local z
    const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = ry; parent.add(g);
    const wire = std('hook_steel', () => ({ color: '#c9cdcf', metalness: .85, roughness: .25 }));
    add(g, new THREE.TorusGeometry(.016, .0022, 6, 14, Math.PI * 1.5), wire, 0, 0, 0, 0, 0, -Math.PI / 2);
    add(g, new THREE.CylinderGeometry(.0022, .0022, .04, 6), wire, 0, -.036, 0);
    for (const s of [-1, 1]) box(g, M.oak, s * .1, -.082, 0, .21, .012, .014, 0).rotation.z = s * -.2;
    const m = new THREE.Mesh(garmentGeometry(kind), mat); m.position.set(0, -.07, 0); g.add(m); return g;
  }
  function sewingMachine(parent, x, y, z, ry = 0) {   // a simple lockstitch machine (bed, pillar, arm, head, handwheel); front is local +z
    const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = ry; parent.add(g);
    const body = std('machine_body', () => ({ color: '#e8e4da', roughness: .35 })), dark = std('machine_dark', () => ({ color: '#2e2e30', roughness: .4 }));
    box(g, body, 0, 0, 0, .42, .05, .18); box(g, body, .15, .05, -.03, .08, .22, .1); box(g, body, .01, .25, -.03, .36, .075, .09); box(g, body, -.17, .13, -.03, .08, .195, .09);
    add(g, new THREE.CylinderGeometry(.0025, .0025, .06, 6), std('hook_steel', () => ({})), -.17, .105, -.01);
    add(g, new THREE.CylinderGeometry(.055, .055, .025, 24), dark, .205, .2, -.03, 0, 0, Math.PI / 2);
    add(g, new THREE.CylinderGeometry(.013, .013, .03, 12), std('thread_madder', () => ({ color: '#8f4a3a', roughness: .8 })), .03, .34, -.03);
    return g;
  }
  let offcutGeo = null;
  function offcutHeap(parent, x, y, z, { r = .16, h = .1, n = 110, colors = ['#3d5170'], seed = 1 } = {}) {   // a dome of knit offcuts (jhut) in one colour family
    if (!offcutGeo) { offcutGeo = new THREE.PlaneGeometry(1, 1); geometries.push(offcutGeo); }
    const mat = std('offcut', () => ({ color: '#ffffff', roughness: .96, side: THREE.DoubleSide, map: knitMap('jersey', [2, 2]) }));
    const inst = new THREE.InstancedMesh(offcutGeo, mat, n), m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), e = new THREE.Euler(), P = new THREE.Vector3(), S = new THREE.Vector3(), col = new THREE.Color(), rr = rng(seed);
    for (let i = 0; i < n; i++) {
      const a = rr() * Math.PI * 2, d = Math.sqrt(rr()) * r, top = h * (1 - (d / r) ** 2);
      P.set(x + Math.cos(a) * d, y + top * (.75 + rr() * .3), z + Math.sin(a) * d); e.set(-Math.PI / 2 + (rr() - .5) * 1.1, rr() * 6.3, (rr() - .5) * 1.1); q.setFromEuler(e);
      S.set(.035 + rr() * .08, .018 + rr() * .045, 1); inst.setMatrixAt(i, m4.compose(P, q, S)); col.set(colors[Math.floor(rr() * colors.length)]).offsetHSL(0, 0, (rr() - .5) * .1); inst.setColorAt(i, col);
    }
    inst.instanceMatrix.needsUpdate = true; inst.instanceColor.needsUpdate = true; inst.computeBoundingSphere(); parent.add(inst);
    add(parent, rockGeometry(r * .92, seed + 7, 1, Math.min(.9, h / r * 1.1), 1), knit(colors[0]), x, y, z);   // the body under the loose pieces
    return inst;
  }
  function juteSack(parent, x, z, { r = .19, h = .4, y = 0 } = {}) {   // an open jute sack with a rolled rim
    const g = new THREE.Group(); g.position.set(x, y, z); parent.add(g);
    add(g, lathe([[0, .004], [r * .9, 0], [r, .04], [r * 1.03, h * .6], [r * .98, h], [r * 1.06, h + .02], [r * 1.09, h - .035], [r * .96, h - .05], [0, h - .06]], 28), wovenMaterial('sack_jute', 'plain', FIBRE.jute, [8, 6]));
    return g;
  }
  function mendMat(key, base, patch, seed = 3) {   // a knit with a patch darned in kantha running stitch (for folded pieces: the canvas spans one fold top)
    return std('mend_' + key, () => { const s = px(256), c = canvas(s, Math.round(s * .8)), x = c.getContext('2d'), H = c.height, r = rng(seed); x.fillStyle = base; x.fillRect(0, 0, s, H);
      x.save(); x.translate(s * .56, H * .5); x.rotate(-.12); x.fillStyle = patch; x.fillRect(-s * .16, -H * .15, s * .32, H * .3);
      x.strokeStyle = '#f2ead8'; x.lineWidth = Math.max(1.5, s / 150); x.setLineDash([s / 55, s / 85]); x.lineCap = 'round';
      for (let k = -2; k <= 2; k++) { x.beginPath(); x.moveTo(-s * .2, k * H * .065); x.lineTo(s * .2, k * H * .065 + (r() - .5) * 2); x.stroke(); }
      x.strokeRect(-s * .18, -H * .17, s * .36, H * .34); x.setLineDash([]);
      x.strokeStyle = '#c9a565'; x.setLineDash([s / 70, s / 100]); for (let p = 0; p < 6; p++) { const a = p / 6 * Math.PI * 2; x.beginPath(); x.ellipse(Math.cos(a) * s * .045, Math.sin(a) * s * .045, s * .04, s * .015, a, 0, 7); x.stroke(); } x.restore(); x.setLineDash([]);
      x.globalCompositeOperation = 'multiply'; x.scale(.25, .25); x.fillStyle = x.createPattern(knitTile('jersey'), 'repeat'); x.fillRect(0, 0, s * 4, H * 4); x.setTransform(1, 0, 0, 1, 0, 0); x.globalCompositeOperation = 'source-over';
      return { map: tex(c, { repeat: [1 / .3, 1 / .24] }), roughness: .95, side: THREE.DoubleSide }; });
  }
  const kraft = std('kraft', () => ({ color: '#c9a878', roughness: .85, side: THREE.DoubleSide }));
  function patternPieces(parent, x, y, z, ry = 0, scale = 1) {   // kraft-paper pattern of a tee: front, back and a sleeve, flat on a table at y
    const g = new THREE.Group(); g.position.set(x, y + .001, z); g.rotation.y = ry; g.scale.setScalar(scale); parent.add(g);
    for (const [dx, dz, a] of [[-.27, .02, .05], [.27, -.02, -.04]]) add(g, new THREE.ShapeGeometry(garmentOutline('tee'), 6), kraft, dx, 0, dz - .35, -Math.PI / 2, 0, a);
    const sl = new THREE.Shape(); sl.moveTo(-.16, 0); sl.quadraticCurveTo(0, .1, .16, 0); sl.lineTo(.12, -.2); sl.lineTo(-.12, -.2); sl.closePath();
    add(g, new THREE.ShapeGeometry(sl, 6), kraft, 0, .0005, .2, -Math.PI / 2, 0, .3);
    return g;
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
    [['#8f4a2c', 'clay'], ['#efe9dc', 'cotton'], [FIBRE.jute, 'jute'], ['#8e8b86', 'recycled fibre'], ['#2f4363', 'indigo']].forEach(([col, nm], i) => {
      const z = -4.9 + i * .78; add(g, lathe([[0, 0], [.04, 0], [.06, .035], [.055, .04], [.035, .012], [0, .012]], 24), M.clay, 9.37, 1.185, z);
      add(g, new THREE.CircleGeometry(.05, 20), [std('earth_0', () => ({ color: col, roughness: 1, map: M.soil.map })), FB.cotton, FB.jute, FB.usedMix, FB.indigo][i], 9.37, 1.215, z, -Math.PI / 2);
      add(g, new THREE.PlaneGeometry(.1, .03), card([nm], { w: .1, h: .03, scale: .4 }), 9.4065, 1.165, z, 0, Math.PI / 2);
    });
  }

  // ---------------------------------------------------------------- Z30 Experience centre: the approved knitwear stays, the fabric story is added around it
  if (want('BEL_FABRIC_STORIES')) {
    // plinth F021: top 0.2032, x 11.05-14.35, z -9.07..-7.95. The approved forms F022-F025 stand at x 11.63 / 12.34 / 13.06 / 13.77 on
    // bases of radius 0.19 at z -8.56 (measured in the scene), so the front strip z -8.33..-7.97 takes a fibre dish and a card per form
    const g = item('BEL_FABRIC_STORIES'), T = .2032;
    [[11.633, FB.jhutNavy, ['Second life · cutting waste', 'Jhut sorted by colour, spun again', 'Recycled share: to be certified']],
     [12.344, FB.jute, ['Golden fibre · research', 'A jute and cotton blend', 'Trials only, not in production']],
     [13.056, FB.usedMix, ['Second life · used garments', 'Taken back, sorted, recycled', 'Partners: to be identified']],
     [13.767, FB.cotton, ['Earth · cotton', 'Fibre origin: to be documented', 'Organic only with a certificate']]].forEach(([x, mat, lines], i) => {
      add(g, lathe([[0, 0], [.05, 0], [.075, .03], [.07, .036], [.045, .012], [0, .012]], 28), M.clay, x - .1, T, -8.2);
      fibreHeap(g, x - .1, T + .012, -8.2, .05, mat, 431 + i);
      standingCard(g, lines, x + .09, T, -8.06, -.12, { w: .17, h: .09 });
    });
    standingCard(g, ['Ecodesign, fibre to fibre', 'Earth fibres and recycled fabric', 'Made to last, repair and recycle', 'Illustrative · records to follow'], 11.22, T, -8.12, -.45, { w: .19, h: .12 });
  }
  if (want('BEL_BAY_STORIES')) {
    // bays F017-F020 (measured): base top 0.1016, green back z -10.7251, front edge z -10.1347. The approved garments hang from
    // y 0.90 up and folded stacks fill the top shelves, so the story stays low on the base below the garments (under 0.8 m)
    const g = item('BEL_BAY_STORIES'), BASE = .1016, Z = -10.45;
    const header = (x, lines) => standingCard(g, [...lines, 'Illustrative · records to follow'], x, BASE, -10.21, 0, { w: .22, h: .14 });
    // 1 Earth (F017, x 9.79-12.36): dried cotton stems in a clay vase, raw cotton and cones on a tray, a hogla gift box by rural weavers
    let x0 = 9.7917;
    add(g, lathe([[0, 0], [.07, 0], [.1, .08], [.09, .2], [.05, .27], [.055, .3], [.045, .3], [0, .28]], 32), M.clayRaw, x0 + .45, BASE, Z);
    cottonStems(g, x0 + .45, BASE + .27, Z, { n: 5, h: .38, seed: 3 });
    tray(g, x0 + 1.05, BASE, Z, .42, .26, 0); fibreHeap(g, x0 + .96, BASE + .012, Z, .07, FB.cotton, 501);
    yarnCone(g, x0 + 1.14, BASE + .012, Z - .05, coneMat('#efe8da')); yarnCone(g, x0 + 1.2, BASE + .012, Z + .06, coneMat('#d6c7a8'));
    box(g, wovenMaterial('hogla_box', 'twill', FIBRE.hogla, [3, 2]), x0 + 1.68, BASE, Z, .34, .12, .26); box(g, wovenMaterial('hogla_lid', 'twill', '#a99a63', [3, 2]), x0 + 1.68, BASE + .12, Z, .36, .03, .28);
    add(g, new THREE.PlaneGeometry(.1, .06), card(['Hogla box', 'rural weavers, to credit'], { w: .1, h: .06, scale: .5 }), x0 + 1.68, BASE + .08, Z + .131);
    header(x0 + 2.25, ['Earth', 'Cotton knitwear', 'Fibre origin: to be documented']);
    // 2 Golden fibre (F018, x 12.53-15.10): a jute hank, jute and cotton cones, a rib swatch of the blend
    x0 = 12.5349;
    add(g, new THREE.CylinderGeometry(.045, .065, .5, 20, 1), FB.juteHank, x0 + .45, BASE + .25, Z); add(g, new THREE.TorusGeometry(.052, .008, 6, 20), std('band', () => ({ color: '#6b4a2b', roughness: .9 })), x0 + .45, BASE + .32, Z, Math.PI / 2);
    for (const [dx, dz, col] of [[0, -.06, '#c7ae7c'], [.13, .05, '#e6dccb'], [.26, -.04, '#b39867']]) yarnCone(g, x0 + .95 + dx, BASE, Z + dz, coneMat(col));
    box(g, M.oak, x0 + 1.62, BASE, Z, .28, .02, .22); add(g, scaleUV(new THREE.BoxGeometry(.24, .006, .18), .24, .18), KN.juteBlend, x0 + 1.62, BASE + .023, Z, 0, .08);
    header(x0 + 2.25, ['Golden fibre · research', 'A jute and cotton blend knit', 'Trials only, not in production']);
    // 3 Second life from cutting waste (F019, x 16.14-18.25): jute sacks of offcuts sorted by colour, cones spun from them
    x0 = 16.1417;
    [['#3d5170', '#4a5f80', '#33445f'], ['#8f4a3a', '#a35a48', '#7a3d30'], ['#8e8b86', '#a9a59e', '#6f6c68']].forEach((cols, i) => {
      const x = x0 + .3 + i * .42; juteSack(g, x, Z, { r: .16, h: .34, y: BASE }); offcutHeap(g, x, BASE + .28, Z, { r: .15, h: .08, n: 90, colors: cols, seed: 600 + i });
    });
    yarnCone(g, x0 + 1.55, BASE, Z - .06, KN.recNavy); yarnCone(g, x0 + 1.66, BASE, Z + .07, KN.recRed);
    header(x0 + 1.95, ['Second life · cutting waste', 'Jhut sorted by colour, spun again', 'Recycled share: to be certified']);
    // 4 Second life from used garments (F020, x 18.43-20.54): a take-back crate, a garment mended in kantha stitch, recycled fibre
    x0 = 18.4277;
    box(g, wovenMaterial('crate_jute', 'plain', FIBRE.jute, [4, 3]), x0 + .4, BASE, Z, .5, .3, .34);
    foldedStack(g, x0 + .4, BASE + .3, Z, [KN.charcoal, KN.madder, KN.indigo], .1);
    add(g, new THREE.PlaneGeometry(.2, .08), card(['Take-back', 'worn knitwear comes home'], { w: .2, h: .08, scale: .6 }), x0 + .4, BASE + .16, Z + .171);
    foldedStack(g, x0 + 1.05, BASE, Z, [KN.oat, mendMat('indigo', '#3a4d6e', '#8a97ad')], -.08);
    add(g, lathe([[0, 0], [.06, 0], [.09, .035], [.085, .042], [.055, .014], [0, .014]], 28), M.clay, x0 + 1.55, BASE, Z); fibreHeap(g, x0 + 1.55, BASE + .014, Z, .062, FB.usedMix, 611);
    header(x0 + 1.95, ['Second life · used garments', 'Take back, mend in kantha stitch,', 'resell or recycle']);
  }
  if (want('BEL_EC_TREE')) { const g = item('BEL_EC_TREE'); smallTree(g, { x: 21.59, z: -7.62, seed: 23, height: 1.7 }); }   // approved F029/PL029: x 21.34-21.84, z -7.87..-7.37
  if (want('BEL_WATER_KOLSHI')) {
    const g = item('BEL_WATER_KOLSHI');  // counter top 0.889, x 10.91-20.07, z -6.08..-5.56 (room side -z): on the spot of the approved water point (x 11.40), not shown on this route
    const T = .889, X = 11.2; add(g, new THREE.TorusGeometry(.085, .02, 10, 28), M.wood, X, T + .02, -5.84, Math.PI / 2);
    add(g, lathe([[0, 0], [.07, 0], [.12, .05], [.135, .13], [.12, .2], [.07, .245], [.05, .28], [.062, .3], [.055, .305], [.042, .28], [0, .27]], 40), M.clay, X, T + .015, -5.84);
    tray(g, X + .28, T, -5.84, .22, .16, 0); for (const dx of [-.06, 0, .06]) cup(g, X + .28 + dx, T + .012, -5.84, 'tumbler', M.clayCream);
    standingCard(g, ['Drinking water', 'Source stated by the client: deep tube well', 'Laboratory results: none yet', 'Only dated reports will be shown'], X + .52, T, -5.8, Math.PI, { w: .2, h: .12 });
  }

  // ---------------------------------------------------------------- Z08 Boardroom
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

  // Bengal craft helpers from the owner's references (30 Oct 2026), shared by the option A rooms and the craft items further down
  const hexRGB = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
  function shiboriMat(key, seed, ombre = false) {   // natural indigo, resist-dyed: rings and blots on a deep blue ground (or dip-dyed, pale to deep)
    return std('indigo_' + key, () => { const W = px(512), H = px(256), c = canvas(W, H), x = c.getContext('2d'), r = rng(seed);
      const gr = x.createLinearGradient(0, 0, W, 0); if (ombre) { gr.addColorStop(0, '#e6ebef'); gr.addColorStop(.4, '#7d97b8'); gr.addColorStop(1, '#1d3254'); } else { gr.addColorStop(0, '#22385b'); gr.addColorStop(1, '#1b2f4f'); }
      x.fillStyle = gr; x.fillRect(0, 0, W, H);
      for (let k = 0; k < (ombre ? 3 : 7); k++) { const cx = (ombre ? .55 + r() * .4 : r()) * W, cy = r() * H, R = H * (.12 + r() * .18);
        for (let q = 0; q < 5; q++) { x.strokeStyle = `rgba(233,238,242,${.6 - q * .09})`; x.lineWidth = H * .014; x.beginPath(); x.arc(cx, cy, R * (1 - q * .18), 0, 7); x.stroke(); }
        x.fillStyle = 'rgba(233,238,242,.65)'; x.beginPath(); x.arc(cx, cy, R * .12, 0, 7); x.fill(); }
      for (let k = 0; k < 50; k++) { x.fillStyle = `rgba(233,238,242,${.12 + r() * .25})`; x.beginPath(); x.ellipse(r() * W, r() * H, 2 + r() * 12, 1 + r() * 4, r() * 3, 0, 7); x.fill(); }
      x.globalCompositeOperation = 'multiply'; x.globalAlpha = .25; x.fillStyle = x.createPattern(weave.plain.map, 'repeat'); x.fillRect(0, 0, W, H); x.globalAlpha = 1; x.globalCompositeOperation = 'source-over';
      const t = tex(c); return { map: t, roughness: .95, side: THREE.DoubleSide, emissive: '#ffffff', emissiveMap: t, emissiveIntensity: .14 }; });
  }
  function trayWeave(key, base, paint = null) {   // the face of a round woven bamboo tray (kula, dala): spokes and weavers in over-under, optionally painted
    return std('tray_' + key, () => { const s = px(256), c = canvas(s, s), x = c.getContext('2d'), img = x.createImageData(s, s), [br, bg, bb] = hexRGB(base), h = s / 2;
      for (let j = 0; j < s; j++) for (let i = 0; i < s; i++) {
        const dx = i - h + .5, dy = j - h + .5, rho = Math.hypot(dx, dy) / h, th = Math.atan2(dy, dx), ring = rho * 30, spoke = (th / (Math.PI * 2) + .5) * 64;
        const f = (Math.floor(ring) + Math.floor(spoke)) % 2 ? .82 + .18 * Math.sin((ring % 1) * Math.PI) : .6 + .2 * Math.sin((spoke % 1) * Math.PI), k = (j * s + i) * 4;
        img.data[k] = br * f; img.data[k + 1] = bg * f; img.data[k + 2] = bb * f; img.data[k + 3] = 255;
      }
      x.putImageData(img, 0, 0);
      if (paint) { x.globalCompositeOperation = 'multiply'; paint(x, s); x.globalCompositeOperation = 'source-over'; }
      return { map: tex(c, { clamp: true }), roughness: .85, side: THREE.DoubleSide }; });
  }
  const TRAY = [trayWeave('natural', '#d9b779'), trayWeave('honey', '#c69a5a'),
    trayWeave('red', '#d9b779', (x, s) => { x.strokeStyle = '#b8352a'; x.lineWidth = s / 40; for (let k = -6; k <= 6; k++) { x.beginPath(); x.moveTo(s / 2 + k * s / 8 - s, 0); x.lineTo(s / 2 + k * s / 8 + s, s * 2); x.stroke(); x.beginPath(); x.moveTo(s / 2 + k * s / 8 + s, 0); x.lineTo(s / 2 + k * s / 8 - s, s * 2); x.stroke(); } }),
    trayWeave('green', '#d9b779', (x, s) => { for (const [r0, col] of [[.42, '#2f7a5a'], [.3, '#b8352a'], [.18, '#2f7a5a']]) { x.strokeStyle = col; x.lineWidth = s / 22; x.beginPath(); x.arc(s / 2, s / 2, s * r0, 0, 7); x.stroke(); } })];
  function trayCloud(parent, list) {   // [x, y, z, r, k, rx, ry] per tray: one merged mesh per face material and one for all rims
    const faces = TRAY.map(() => []), rims = [];
    for (const [x, y, z, r, k, rx = 0, ry = 0] of list) { faces[k].push([new THREE.CircleGeometry(r, 36), x, y, z, rx, ry, 0]); rims.push([new THREE.TorusGeometry(r, .009, 6, 36), x, y, z, rx, ry, 0]); }
    faces.forEach((f, k) => { if (f.length) add(parent, merged(f), TRAY[k]); });
    add(parent, merged(rims), std('tray_rim', () => ({ color: '#b48a52', roughness: .7 })));
  }
  const glow = std('lantern_glow', () => ({ color: '#fff4dc', emissive: '#ffc47a', emissiveIntensity: 1.3, roughness: .2, transparent: true, opacity: .92 }));
  function hurricaneLantern(parent, x, y, z, enamel = '#25332b') {   // an electric lamp in the form of the hurricane lantern; y = top of the handle
    const g = new THREE.Group(); g.position.set(x, y, z); parent.add(g); const m = std('lantern_' + enamel, () => ({ color: enamel, metalness: .45, roughness: .45 }));
    add(g, new THREE.TorusGeometry(.055, .004, 6, 18, Math.PI), m, 0, -.055, 0);
    add(g, new THREE.ConeGeometry(.065, .05, 20), m, 0, -.085, 0); add(g, new THREE.CylinderGeometry(.03, .03, .03, 16), m, 0, -.06, 0);
    add(g, lathe([[.032, 0], [.05, .03], [.058, .07], [.05, .11], [.034, .14]], 24), glow, 0, -.25, 0);
    for (let k = 0; k < 4; k++) { const a = k / 4 * Math.PI * 2 + .4; add(g, new THREE.CylinderGeometry(.0025, .0025, .15, 4), m, Math.cos(a) * .062, -.18, Math.sin(a) * .062); }
    add(g, new THREE.CylinderGeometry(.068, .07, .055, 24), m, 0, -.285, 0); return g;
  }
  const bambooPainted = std('bamboo_painted', () => { const c = canvas(32, 256), x = c.getContext('2d'); x.fillStyle = '#c9a868'; x.fillRect(0, 0, 32, 256);
    for (let y = 0; y < 256; y += 64) { x.fillStyle = '#2b2420'; x.fillRect(0, y + 8, 32, 14); x.fillRect(0, y + 40, 32, 5); x.fillStyle = '#8f2f24'; x.fillRect(0, y + 26, 32, 4); x.fillStyle = 'rgba(80,55,25,.5)'; x.fillRect(0, y, 32, 2); }
    return { map: tex(c, { repeat: [1, 3] }), roughness: .55 }; });
  const bambooNatural = std('bamboo_natural', () => { const c = canvas(32, 256), x = c.getContext('2d'); x.fillStyle = '#cfae6b'; x.fillRect(0, 0, 32, 256);   // culm with nodes
    for (let y = 0; y < 256; y += 64) { x.fillStyle = 'rgba(110,80,35,.55)'; x.fillRect(0, y, 32, 3); x.fillStyle = 'rgba(255,240,200,.35)'; x.fillRect(0, y + 3, 32, 2); } for (let i = 0; i < 40; i++) { x.fillStyle = 'rgba(120,90,40,.12)'; x.fillRect((i * 7) % 32, 0, 1, 256); }
    return { map: tex(c, { repeat: [1, 3] }), roughness: .45 }; });
  function lanternPost(parent, x, z, ry, h = 2.15) {   // a painted bamboo post with an arm; the lantern hangs over local +z
    const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = ry; parent.add(g);
    add(g, new THREE.CylinderGeometry(.13, .15, .05, 20), M.graniteRough, 0, .025, 0);
    add(g, new THREE.CylinderGeometry(.035, .04, h, 12), bambooPainted, 0, h / 2, 0);
    add(g, new THREE.CylinderGeometry(.025, .025, .5, 10), bambooPainted, 0, h - .1, .22, Math.PI / 2 - .25, 0, 0);
    add(g, new THREE.CylinderGeometry(.015, .015, .3, 8), bambooPainted, 0, h - .3, .1, .75, 0, 0);
    hurricaneLantern(g, 0, h - .02, .42); footprint(x - .15, z - .15, x + .15, z + .15); return g;
  }
  function basketLamp(parent, x, y, z, { r = .26, h = .24, top = 2.895 } = {}) {   // an upturned woven basket as a lamp shade; y = the open rim
    const g = new THREE.Group(); g.position.set(x, y, z); parent.add(g); const wv = weaveMap('coil', [9, 3]);
    add(g, lathe([[r, 0], [r * 1.03, .015], [r * .97, h * .5], [r * .72, h * .88], [.035, h], [0, h]], 40), std('basket_lamp', () => ({ color: '#c9975a', map: wv, emissive: '#ffb766', emissiveMap: wv, emissiveIntensity: .35, roughness: .85, side: THREE.DoubleSide })));
    add(g, new THREE.SphereGeometry(.035, 16, 10), std('bulb_warm', () => ({ color: '#fff3d6', emissive: '#ffc070', emissiveIntensity: 1.6 })), 0, h * .35, 0);
    add(g, new THREE.CylinderGeometry(.003, .003, top - y - h, 4), std('cord', () => ({ color: '#2a2a2a', roughness: .6 })), 0, h + (top - y - h) / 2, 0); return g;
  }
  function bambooArmchair(parent, x, z, ry) {   // round bamboo frame, a fan back of split bamboo, a thick dark cushion; front is local +z
    const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = ry; parent.add(g);
    const rod = (a, b, r) => { const A = new THREE.Vector3(...a), Bv = new THREE.Vector3(...b), d = Bv.clone().sub(A), geo = new THREE.CylinderGeometry(r, r, d.length(), 10);
      geo.applyQuaternion(new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize())); geo.translate((A.x + Bv.x) / 2, (A.y + Bv.y) / 2, (A.z + Bv.z) / 2); return [geo]; };
    const P = [];
    for (const s of [-1, 1]) { P.push(rod([s * .31, 0, .27], [s * .31, .66, .27], .028), rod([s * .31, 0, -.27], [s * .31, .7, -.27], .028), rod([s * .34, .64, .32], [s * .34, .64, -.3], .026), rod([s * .31, .4, .27], [s * .31, .4, -.27], .02)); }
    P.push(rod([-.31, .4, .27], [.31, .4, .27], .022), rod([-.31, .4, -.27], [.31, .4, -.27], .022), rod([-.31, .12, .27], [.31, .12, .27], .016));
    P.push([new THREE.TorusGeometry(.31, .024, 8, 28, Math.PI), 0, .7, -.27]);
    for (let k = 1; k < 8; k++) { const a = k / 8 * Math.PI; P.push(rod([0, .43, -.27], [Math.cos(a) * .3, .7 + Math.sin(a) * .3, -.27], .011)); }
    add(g, merged(P), bambooNatural);
    add(g, pillowGeometry(.58, .52, .1), std('cushion_dark', () => ({ color: '#2b2c30', roughness: .95, map: weaveMap('plain', [6, 6]) })), 0, .47, .01, -Math.PI / 2, 0, 0);
    add(g, pillowGeometry(.42, .36, .12), handloomCushion, 0, .66, -.2, -.25, 0, 0); return g;
  }
  function hourglassTable(parent, x, z, { r = .42, h = .5, n = 28, twist = 2.2 } = {}) {   // bent bamboo slats between two rings: a waisted base, a round top
    const g = new THREE.Group(); g.position.set(x, 0, z); parent.add(g); const P = [], R = .28;
    for (let k = 0; k < n; k++) { const a = k / n * Math.PI * 2, A = new THREE.Vector3(Math.cos(a) * R, 0, Math.sin(a) * R), Bv = new THREE.Vector3(Math.cos(a + twist) * R, h - .04, Math.sin(a + twist) * R), d = Bv.clone().sub(A);
      const geo = new THREE.CylinderGeometry(.009, .009, d.length(), 6); geo.applyQuaternion(new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize())); geo.translate((A.x + Bv.x) / 2, (A.y + Bv.y) / 2, (A.z + Bv.z) / 2); P.push([geo]); }
    P.push([new THREE.TorusGeometry(R, .014, 6, 36), 0, .012, 0, Math.PI / 2], [new THREE.TorusGeometry(R, .014, 6, 36), 0, h - .045, 0, Math.PI / 2]);
    add(g, merged(P), bambooNatural);
    const top = std('bamboo_laminate', () => { const c = canvas(256, 256), xx = c.getContext('2d'); for (let i = 0; i < 16; i++) { xx.fillStyle = i % 2 ? '#d3b06e' : '#c8a35f'; xx.fillRect(i * 16, 0, 16, 256); xx.fillStyle = 'rgba(90,60,25,.25)'; for (let y = 20 + i * 7 % 40; y < 256; y += 64) xx.fillRect(i * 16, y, 16, 2); } return { map: tex(c), roughness: .4 }; });
    add(g, new THREE.CylinderGeometry(r, r, .03, 40), top, 0, h - .015, 0); return g;
  }
  const sliceTop = std('wood_slice', () => { const s = px(256), c = canvas(s, s), x = c.getContext('2d'), r = rng(311); x.fillStyle = '#a8653a'; x.fillRect(0, 0, s, s);
    for (let k = 0; k < 34; k++) { x.strokeStyle = `rgba(${k % 3 ? '120,60,30' : '210,150,100'},${.25 + r() * .2})`; x.lineWidth = 1 + r() * 2; x.beginPath(); x.ellipse(s / 2 + (r() - .5) * 4, s / 2 + (r() - .5) * 4, k * s / 72, k * s / 76, r(), 0, 7); x.stroke(); }
    x.strokeStyle = '#4a2a18'; x.lineWidth = s / 30; x.beginPath(); x.arc(s / 2, s / 2, s * .48, 0, 7); x.stroke(); return { map: tex(c, { clamp: true }), roughness: .35 }; });
  const hairpin = std('hairpin_black', () => ({ color: '#1c1c1e', metalness: .6, roughness: .45 }));
  function woodSliceStool(parent, x, z, { r = .17, h = .45 } = {}) {   // a cross-cut wood slice on three hairpin legs
    const g = new THREE.Group(); g.position.set(x, 0, z); parent.add(g);
    add(g, new THREE.CylinderGeometry(r, r * 1.02, .05, 28), [std('bark', () => ({})), sliceTop, sliceTop], 0, h - .025, 0);
    for (let k = 0; k < 3; k++) { const a = k / 3 * Math.PI * 2; add(g, new THREE.CylinderGeometry(.006, .006, h - .05, 6), hairpin, Math.cos(a) * r * .55, (h - .05) / 2, Math.sin(a) * r * .55, Math.sin(a) * .12, 0, -Math.cos(a) * .12); }
    footprint(x - r, z - r, x + r, z + r); return g;
  }
  function liveEdgeTable(parent, x, z, { len = 1.8, w = .62, h = .74, ry = 0, seed = 5 } = {}) {   // a live-edge slab on hairpin legs, its outline following the tree
    const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = ry; parent.add(g); const n = noise3(seed), s = new THREE.Shape(), N = 48;
    for (let i = 0; i <= N; i++) { const t = i / N, X = -len / 2 + t * len, Wd = w / 2 * (.82 + .25 * n(t * 3, .5, 1) + .1 * Math.sin(t * Math.PI)); i ? s.lineTo(X, Wd) : s.moveTo(X, Wd); }
    for (let i = N; i >= 0; i--) { const t = i / N, X = -len / 2 + t * len, Wd = w / 2 * (.8 + .25 * n(t * 3, 2.5, 4) + .1 * Math.sin(t * Math.PI)); s.lineTo(X, -Wd); }
    const geo = new THREE.ExtrudeGeometry(s, { depth: .05, bevelEnabled: true, bevelThickness: .006, bevelSize: .006, bevelSegments: 1 }); geo.rotateX(-Math.PI / 2); geo.translate(0, h - .056, 0);
    const slab = std('live_edge', () => { const c = canvas(px(512), px(128)), xx = c.getContext('2d'), r = rng(seed * 7); xx.fillStyle = '#8f4f2c'; xx.fillRect(0, 0, c.width, c.height);
      for (let i = 0; i < 70; i++) { const Y = r() * c.height; xx.strokeStyle = `rgba(${r() > .5 ? '70,32,15' : '200,130,80'},${.12 + r() * .15})`; xx.lineWidth = .8 + r() * 1.8; xx.beginPath(); xx.moveTo(0, Y); for (let X = 0; X <= c.width; X += 24) xx.lineTo(X, Y + Math.sin(X * .02 + i) * 4); xx.stroke(); }
      return { map: tex(c, { repeat: [1 / len, 1 / w] }), roughness: .35 }; });
    add(g, geo, slab);
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) add(g, new THREE.CylinderGeometry(.007, .007, h - .06, 6), hairpin, sx * (len / 2 - .2), (h - .06) / 2, sz * w * .25, sz * .14, 0, 0);
    return g;
  }
  function caneMoonChair(parent, x, z, ry) {   // a round cane bowl chair on a wooden ring stand, a handloom cushion; it faces local +z
    const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = ry; parent.add(g);
    const bowl = new THREE.Group(); bowl.position.set(0, .4, 0); bowl.rotation.x = -.32; g.add(bowl);
    add(bowl, lathe(Array.from({ length: 10 }, (_, i) => { const a = i / 9 * Math.PI * .5; return [Math.max(.01, Math.sin(a) * .5), (1 - Math.cos(a)) * .3]; }), 36), wovenMaterial('cane_bowl', 'lattice', FIBRE.cane, [10, 4]), 0, -.02, 0);
    add(bowl, new THREE.TorusGeometry(.5, .02, 8, 40), M.bamboo, 0, .28, 0, Math.PI / 2);
    add(bowl, new THREE.CylinderGeometry(.42, .42, .1, 32), std('cushion_cream', () => ({ color: '#e8dfcf', roughness: .95, map: weaveMap('plain', [8, 8]) })), 0, .09, 0);
    for (const [dx, m] of [[-.16, handloomCushion], [.16, textileMat('kantha_cushion', (xx, w, hh) => drawKantha(xx, w, hh, 27), [192, 192])]]) add(bowl, pillowGeometry(.34, .34, .12), m, dx, .3, -.28, .5, 0, 0);
    add(g, new THREE.TorusGeometry(.28, .015, 6, 28), M.wood, 0, .02, 0, Math.PI / 2);
    for (let k = 0; k < 4; k++) { const a = k / 4 * Math.PI * 2 + .78; add(g, new THREE.CylinderGeometry(.015, .018, .4, 8), M.wood, Math.cos(a) * .22, .2, Math.sin(a) * .22, Math.sin(a) * .25, 0, -Math.cos(a) * .25); }
    footprint(x - .52, z - .52, x + .52, z + .52); return g;
  }
  function shokherHari(parent, x, y, z, { h = .34, seed = 1 } = {}) {   // a painted pot in the shokher hari tradition: fish, lotus, rice stalks on an ochre ground
    const mat = std('hari_' + seed, () => { const W = px(512), H = px(256), c = canvas(W, H), xx = c.getContext('2d'), r = rng(seed * 13); xx.fillStyle = seed % 2 ? '#d9832f' : '#e0a33a'; xx.fillRect(0, 0, W, H);
      xx.fillStyle = '#b3261e'; xx.fillRect(0, 0, W, H * .14); xx.fillStyle = '#1d1a18'; for (const yy of [.14, .38, .7]) xx.fillRect(0, H * yy, W, H * .012);
      for (let k = 0; k < 5; k++) { const cx = (k + .5) * W / 5, cy = H * .26; xx.fillStyle = '#f2e8d6'; xx.beginPath(); xx.ellipse(cx, cy, W * .045, H * .06, 0, 0, 7); xx.fill(); xx.strokeStyle = '#1d1a18'; xx.lineWidth = 2; xx.stroke();
        xx.beginPath(); xx.moveTo(cx + W * .04, cy); xx.lineTo(cx + W * .07, cy - H * .05); xx.lineTo(cx + W * .07, cy + H * .05); xx.closePath(); xx.fillStyle = '#b3261e'; xx.fill(); xx.stroke(); xx.fillStyle = '#1d1a18'; xx.beginPath(); xx.arc(cx - W * .025, cy - H * .01, 2.5, 0, 7); xx.fill(); }
      for (let k = 0; k < 4; k++) { const cx = (k + .5) * W / 4, cy = H * .55; for (let p = 0; p < 7; p++) { const a = -Math.PI / 2 + (p - 3) * .32; xx.fillStyle = p % 2 ? '#b3261e' : '#f2e8d6'; xx.beginPath(); xx.ellipse(cx + Math.cos(a) * W * .03, cy + Math.sin(a) * H * .08, W * .012, H * .07, a + Math.PI / 2, 0, 7); xx.fill(); xx.strokeStyle = '#1d1a18'; xx.lineWidth = 1.5; xx.stroke(); }
        xx.strokeStyle = '#2f6b3a'; xx.lineWidth = 3; xx.beginPath(); xx.moveTo(cx, cy + H * .02); xx.lineTo(cx, cy + H * .13); xx.stroke(); }
      for (let i = 0; i < W; i += W / 40) { xx.strokeStyle = '#2f6b3a'; xx.lineWidth = 2; xx.beginPath(); xx.moveTo(i, H * .95); xx.quadraticCurveTo(i + W / 80, H * .8, i + W / 50 + r() * 3, H * .74); xx.stroke(); }
      return { map: tex(c, { clamp: true }), roughness: .5 }; });
    const s = h / .34; return add(parent, lathe([[0, 0], [.08, 0], [.13, .05], [.15, .14], [.13, .24], [.08, .29], [.065, .31], [.075, .335], [.08, .345], [.07, .345], [.058, .32], [0, .31]].map(([a, b]) => [a * s, b * s]), 40), mat, x, y, z);
  }
  function tepaPutul(parent, x, y, z, seed = 1) {   // a pinched clay doll painted in red earth with white dots
    const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = seed * 1.3; parent.add(g); const r = rng(seed * 31), h = .14 + r() * .08;
    const body = std('tepa_' + (seed % 3), () => { const c = canvas(64, 128), xx = c.getContext('2d'); xx.fillStyle = ['#a8452a', '#b8642f', '#8f3a22'][seed % 3]; xx.fillRect(0, 0, 64, 128); xx.fillStyle = '#f2e8d6'; for (let k = 0; k < 40; k++) { xx.beginPath(); xx.arc((k * 13) % 64, 20 + Math.floor(k / 5) * 12, 2, 0, 7); xx.fill(); } xx.fillStyle = '#1d1a18'; xx.fillRect(0, 10, 64, 4); return { map: tex(c), roughness: .8 }; });
    add(g, lathe([[0, 0], [.04, 0], [.045, .02], [.03, h * .6], [.018, h * .8], [0, h * .82]], 20), body);
    add(g, new THREE.SphereGeometry(.024, 16, 10), body, 0, h * .9, 0);
    for (const s of [-1, 1]) add(g, new THREE.CylinderGeometry(.007, .009, .06, 8), body, s * .03, h * .62, .01, .3, 0, s * .7); return g;
  }
  function drum(parent, kind, x, y, z, ry = 0) {   // dholak (painted barrel, rope lacing) or khol (Bengal's clay drum, one end narrow); lying on its side
    const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = ry; parent.add(g);
    const L = kind === 'khol' ? .56 : .42, R0 = kind === 'khol' ? .1 : .12, R1 = kind === 'khol' ? .065 : .12, Rm = kind === 'khol' ? .15 : .145;
    const shell = kind === 'khol' ? M.clayRaw : std('dholak_paint', () => { const c = canvas(128, 64), xx = c.getContext('2d'); ['#b3261e', '#e0a33a', '#2f6b3a', '#1d3a6b', '#e0a33a', '#b3261e'].forEach((col, i) => { xx.fillStyle = col; xx.fillRect(i * 128 / 6, 0, 128 / 6, 64); }); return { map: tex(c), roughness: .4 }; });
    add(g, lathe([[R0, -L / 2], [Rm * .95, -L / 4], [Rm, 0], [Rm * .95, L / 4], [R1, L / 2]], 28), shell, 0, Rm, 0, 0, 0, Math.PI / 2);
    const skin = std('dhol_skin', () => ({ color: '#d7c2a0', roughness: .85, side: THREE.DoubleSide }));
    add(g, new THREE.CircleGeometry(R0, 24), skin, -L / 2, Rm, 0, 0, -Math.PI / 2); add(g, new THREE.CircleGeometry(R1, 24), skin, L / 2, Rm, 0, 0, Math.PI / 2);
    for (let k = 0; k < 10; k++) { const a = k / 10 * Math.PI * 2; add(g, taperedTube([[-L / 2 + .01, Rm + Math.sin(a) * R0, Math.cos(a) * R0], [0, Rm + Math.sin(a + .3) * Rm * 1.01, Math.cos(a + .3) * Rm * 1.01], [L / 2 - .01, Rm + Math.sin(a + .6) * R1, Math.cos(a + .6) * R1]], .0025, .0025, 8, 4), std('dhol_rope', () => ({ color: '#d9cdb2', roughness: .9 }))); }
    return g;
  }
  const juteBraid = std('jute_braid', () => { const c = canvas(64, 64), x = c.getContext('2d'); x.fillStyle = FIBRE.jute; x.fillRect(0, 0, 64, 64); for (let y = 0; y < 64; y += 8) for (let i = 0; i < 64; i += 8) { x.fillStyle = 'rgba(90,60,25,.35)'; x.beginPath(); x.ellipse(i + 4, y + 4, 3.5, 2, ((y / 8) % 2 ? .6 : -.6), 0, 7); x.fill(); } return { map: tex(c, { repeat: [6, 3] }), roughness: .95 }; });

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
  // the circular knitwear studio around the Uthan: wear, remake, repair, return (option A only)
  if (want('BEL_CIRCLE_WEAR')) {
    const g = item('BEL_CIRCLE_WEAR');   // south-west corner; the fire extinguisher on the west wall (x 9.35-9.52, z -12.80..-12.60) stays clear
    const bamboo = (x0, z0, x1, z1, y = 1.5) => {   // a free-standing bamboo rail on oak feet, from (x0, z0) to (x1, z1)
      const len = Math.hypot(x1 - x0, z1 - z0), a = Math.atan2(z1 - z0, x1 - x0);
      for (const [x, z] of [[x0, z0], [x1, z1]]) { add(g, new THREE.CylinderGeometry(.018, .02, y + .03, 10), M.bamboo, x, (y + .03) / 2, z); box(g, M.oak, x, 0, z, .07, .03, .42, -a); }
      add(g, new THREE.CylinderGeometry(.014, .014, len + .06, 10), M.bamboo, (x0 + x1) / 2, y, (z0 + z1) / 2, 0, -a, Math.PI / 2);
    };
    const wear = [[KN.ecru, 'tee'], [KN.recNavy, 'sweat'], [KN.oat, 'tee'], [KN.recGrey, 'sweat'], [KN.indigo, 'tee'], [KN.moss, 'sweat'], [KN.ecruRib, 'tee'], [KN.recRed, 'tee'], [KN.charcoal, 'sweat'], [KN.juteBlend, 'tee'], [KN.recOlive, 'sweat'], [KN.madder, 'tee']];
    bamboo(9.95, -11.38, 12.05, -11.38);   // along the solid south wall (face z -10.87): garments hang side-on, sleeves clear of the wall
    wear.forEach(([m, k], i) => hangingGarment(g, 10.08 + i * .165, 1.5, -11.38, Math.PI / 2, m, k));
    footprint(9.9, -11.78, 12.1, -10.98); shade('Z07', 9.9, -11.75, 12.1, -11.0, .45);
    bamboo(12.86, -11.4, 12.86, -12.95);   // a second rail at right angles, garments facing the room
    for (let i = 0; i < 9; i++) hangingGarment(g, 12.86, 1.5, -11.55 - i * .165, 0, wear[(i + 5) % wear.length][0], wear[(i + 3) % wear.length][1]);
    footprint(12.45, -13.15, 13.27, -11.2); shade('Z07', 12.47, -13.1, 13.25, -11.25, .45);
    const lt = new THREE.Group(); lt.position.set(11.0, 0, -12.55); g.add(lt); add(lt, tableWood(1.2, .6, .45), M.wood);
    foldedStack(lt, -.38, .45, 0, [KN.ecru, KN.oat, KN.juteBlend], .05); foldedStack(lt, 0, .45, .02, [KN.recNavy, KN.recGrey, KN.indigo], -.06); foldedStack(lt, .38, .45, 0, [KN.recRed, KN.madder], .1);
    footprint(10.38, -12.87, 11.62, -12.23); shade('Z07', 10.4, -12.85, 11.6, -12.25, .4);
    signStand(g, ['1 · Wear', 'Knitwear in earth and recycled fabrics', 'Made to last: durability tests to come', 'Illustrative garments · option A'], 10.0, -13.85, Math.PI / 2);
  }
  if (want('BEL_CIRCLE_REMAKE')) {
    const g = item('BEL_CIRCLE_REMAKE');   // north-west corner: a sorting table, sacks of offcuts along the west wall, recycled yarn on a low shelf
    const TX = 11.85, TZ = -19.5, TH = .86; const t = new THREE.Group(); t.position.set(TX, 0, TZ); g.add(t); add(t, tableWood(1.8, .9, TH), M.wood);
    basketLamp(g, TX, 1.66, TZ, { r: .32, h: .28, top: 2.59 });   // hung from the steel above the table (underside y 2.59, probed)
    footprint(TX - .92, TZ - .47, TX + .92, TZ + .47); shade('Z07', TX - .9, TZ - .45, TX + .9, TZ + .45, .4);
    const sorted = [['#3d5170', '#4a5f80', '#33445f'], ['#8f4a3a', '#a35a48', '#7a3d30'], ['#8e8b86', '#a9a59e', '#6f6c68'], ['#6f7a4c', '#86905f', '#5a6340']];
    sorted.forEach((cols, i) => { const x = -.6 + i * .4; basket(t, x, TH, -.2, { r: .14, h: .12, kind: 'twill', fibre: 'hogla' }); offcutHeap(t, x, TH + .07, -.2, { r: .13, h: .07, n: 70, colors: cols, seed: 640 + i }); });
    offcutHeap(t, .1, TH, .18, { r: .3, h: .06, n: 160, colors: ['#3d5170', '#8f4a3a', '#8e8b86', '#6f7a4c', '#e6dccb', '#c9a565'], seed: 650 });   // the mixed pile still to sort
    [[9.78, -20.55, 0], [9.78, -20.0, 1], [9.78, -19.45, 2]].forEach(([x, z, i]) => { juteSack(g, x, z, { r: .19, h: .46 }); offcutHeap(g, x, .4, z, { r: .18, h: .1, n: 100, colors: sorted[i], seed: 660 + i }); footprint(x - .21, z - .21, x + .21, z + .21); shade('Z07', x - .2, z - .2, x + .2, z + .2, .35); });
    const sh = new THREE.Group(); sh.position.set(11.7, 0, -21.07); g.add(sh);   // low shelf on the solid lower part of the north wall (glass above 1.22 m)
    add(sh, merged([B(1.9, .03, .38, 0, 0, 0), B(1.9, .03, .38, 0, .42, 0), B(1.9, .03, .38, 0, .84, 0), B(.03, .87, .38, -.95, 0, 0), B(.03, .87, .38, .95, 0, 0)]), M.wood);
    [KN.recNavy, KN.recRed, KN.recGrey, KN.recOlive, KN.recNavy, KN.recGrey].forEach((m, i) => yarnCone(sh, -.75 + i * .2, .87, 0, m));
    fabricRoll(sh, -.45, .45, 0, KN.recGrey, { len: .8, r: .07 }); fabricRoll(sh, .45, .45, 0, KN.recNavy, { len: .8, r: .065 });
    for (let k = 0; k < 3; k++) box(sh, wovenMaterial('bale_jute', 'plain', FIBRE.jute, [3, 2]), -.6 + k * .6, .03, 0, .5, .3, .32);
    footprint(10.73, -21.27, 12.67, -20.86); shade('Z07', 10.75, -21.27, 12.65, -20.88, .4);
    signStand(g, ['2 · Remake', 'Cutting waste (jhut) sorted by colour', 'and spun into new yarn', 'Partners to be identified · option A'], 13.45, -18.05, Math.PI * .8);
  }
  if (want('BEL_CIRCLE_REPAIR')) {
    const g = item('BEL_CIRCLE_REPAIR');   // a mending table by the north wall (solid to 1.22 m, glass above to the hallway)
    const TX = 16.15, TZ = -20.25, TH = .74; const t = liveEdgeTable(g, TX, TZ, { len: 1.7, w: .7, h: TH, seed: 7 });   // a live-edge slab on hairpin legs
    footprint(TX - .87, TZ - .4, TX + .87, TZ + .4); shade('Z07', TX - .85, TZ - .36, TX + .85, TZ + .36, .4);
    for (const dx of [-.55, 0, .55]) { woodSliceStool(g, TX + dx, TZ + .6, { r: .17, h: .46 }); shade('Z07', TX + dx - .17, TZ + .43, TX + dx + .17, TZ + .77, .3); }
    basketLamp(g, TX, 1.62, TZ, { r: .3, h: .26 });
    foldedStack(t, -.5, TH, .05, [KN.charcoal, mendMat('charcoal', '#45474a', '#8e8b86', 5)], .1);
    foldedStack(t, .55, TH, .02, [mendMat('madder', '#8f4a3a', '#d6c7a8', 7)], -.15);
    const hoop = new THREE.Group(); hoop.position.set(.05, TH + .012, .02); t.add(hoop);
    add(hoop, new THREE.CircleGeometry(.14, 32), textileMat('kantha_hoop', (x, w, h) => drawKantha(x, w, h, 21), [256, 256]), 0, .002, 0, -Math.PI / 2);
    add(hoop, new THREE.TorusGeometry(.145, .008, 8, 36), M.oak, 0, .006, 0, Math.PI / 2);
    [['#8f4a3a', -.25], ['#2f4a6b', -.18], ['#c9a565', -.11], ['#efe5cf', -.04]].forEach(([col, dz]) => add(t, new THREE.CylinderGeometry(.014, .014, .035, 12), std('thread_' + col, () => ({ color: col, roughness: .8 })), .3, TH + .0175, dz - .1));
    const kp = new THREE.Group(); kp.position.set(14.75, .58, -21.265); g.add(kp);   // a kantha panel on the solid lower wall
    box(kp, M.wood, 0, -.3, .01, .86, .6, .02); add(kp, new THREE.PlaneGeometry(.78, .52), textileMat('kantha_repair', (x, w, h) => drawKantha(x, w, h, 23), [384, 256]), 0, 0, .021);
    signStand(g, ['3 · Repair', 'Kantha: the Bengal tradition of', 'stitching old cloth into new use', 'Embroiderers paid and credited · option A'], 14.55, -18.75, Math.PI * .25);
  }
  if (want('BEL_CIRCLE_RETURN')) {
    const g = item('BEL_CIRCLE_RETURN');   // along the solid south wall (behind it: the experience-centre bays); the east strip to door D49 stays clear
    const hang = new THREE.Group(); hang.position.set(16.4, .82, -10.885); hang.rotation.y = Math.PI; g.add(hang);
    add(hang, new THREE.PlaneGeometry(2.4, 1.28), textileMat('kantha_hanging', (x, w, h) => drawKantha(x, w, h, 13), [768, 410]), 0, .66, .004);
    add(hang, new THREE.CylinderGeometry(.018, .018, 2.55, 12), M.bamboo, 0, 1.32, .025, 0, 0, Math.PI / 2);
    standingCard(g, ['Nakshi kantha', 'By a rural embroiderer: placeholder,', 'to be commissioned, paid and credited'], 17.75, 0, -11.12, Math.PI + .3, { w: .18, h: .1 });
    box(g, wovenMaterial('rug_jute_hosp', 'twill', '#bfa577', [12, 7]), 16.4, RUG, -11.95, 2.5, .01, 1.45);
    bambooArmchair(g, 15.55, -12.0, Math.PI - .35); bambooArmchair(g, 17.25, -12.0, Math.PI + .35);
    for (const x of [15.55, 17.25]) { footprint(x - .4, -12.4, x + .4, -11.6); shade('Z07', x - .38, -12.38, x + .38, -11.62, .45); }
    const rt = hourglassTable(g, 16.4, -11.75, { r: .34, h: .48 });   // bent bamboo slats, after the owner's reference
    cup(rt, -.08, .48, .05, 'teacup', M.clayCream); cup(rt, .1, .48, -.04, 'teacup', M.clayCream); teapot(rt, 0, .48, .12, .6);
    footprint(16.06, -12.09, 16.74, -11.41); shade('Z07', 16.08, -12.07, 16.72, -11.43, .35);
    kashVase(g, 18.45, -11.3, .5);
    [['Repair', [KN.charcoal, KN.indigo]], ['Resell', [KN.oat, KN.moss]], ['Recycle', [KN.recGrey, KN.madder]]].forEach(([label, mats], i) => {   // take-back sacks, labels facing the room
      const x = 18.98 + i * .48, z = -11.17; juteSack(g, x, z, { r: .19, h: .5 }); foldedStack(g, x, .44, z, mats, i * .4);
      add(g, new THREE.PlaneGeometry(.15, .07), card([label], { w: .15, h: .07, scale: .6 }), x, .36, z - .2, 0, Math.PI);
      footprint(x - .21, z - .21, x + .21, z + .21); shade('Z07', x - .2, z - .2, x + .2, z + .2, .35);
    });
    signStand(g, ['4 · Return', 'Worn knitwear comes back:', 'repair, resell or recycle', 'Take-back pilot to be designed · option A'], 20.2, -11.5, Math.PI * 1.2);   // beside door D49, clear of its swing
    signStand(g, ['Circular knitwear studio', '1 Wear · 2 Remake · 3 Repair · 4 Return', 'Around the Green Uthan', 'Option A only'], 21.75, -14.5, -Math.PI / 2);   // by the east wall, facing the room; the walking strip x 19.85-21.55 stays clear
  }
  if (want('BEL_ACADEMY')) {
    const g = item('BEL_ACADEMY');   // inside the glass accounts suite: every partition and door stays (D50 entrance, D51 to the north corridor)
    const rows = [-15.2, -13.95, -12.7, -11.45, -10.2], cols = [3.98, 6.08], seats = [], desks = [];
    for (const z of rows) for (const x of cols) { desks.push([x, 0, z, 0]); for (const dx of [-.37, .37]) seats.push([x + dx, 0, z + .56, Math.PI]); }
    instances(g, tableWood(1.5, .6, .74), M.wood, desks); instances(g, chairWood, M.wood, seats); instances(g, chairCane, cane, seats);
    for (const [x, , z] of desks) { footprint(x - .77, z - .32, x + .77, z + .32); shade('Z06', x - .75, z - .3, x + .75, z + .3, .4); }
    for (const [x, , z] of seats) { footprint(x - .23, z - .23, x + .23, z + .23); shade('Z06', x - .21, z - .21, x + .21, z + .21, .28); }
    for (const [x, , z] of desks) for (const dx of [-.37, .37]) { const k = Math.round((x + dx) * 10 + z) % 3;
      if (k === 1) add(g, new THREE.PlaneGeometry(.21, .28), std('notebook', () => ({ color: '#efe8da', roughness: .9 })), x + dx, .742, z - .02, -Math.PI / 2, 0, .15);
      else add(g, scaleUV(new THREE.BoxGeometry(.13, .005, .13), .13, .13), k ? KN.recNavy : KN.ecru, x + dx, .7425, z - .05, 0, k ? -.15 : .2); }
    // teaching zone at the north glass: demonstration bench with a hands camera, a mobile screen, a pin-up board
    const db = new THREE.Group(); db.position.set(5.1, 0, -16.6); db.rotation.y = Math.PI; g.add(db);
    add(db, tableWood(2.0, .7, .9), M.oak); box(db, M.wood, 0, .12, 0, 1.86, .02, .56);
    add(db, merged([B(.04, .8, .04, .8, .9, .3), B(.04, .04, .5, .8, 1.68, .08)]), std('steel_dark', () => ({ color: '#2e2e30', metalness: .6, roughness: .45 }))); box(db, std('cam_body', () => ({ color: '#151515', roughness: .4 })), .8, 1.6, -.15, .09, .07, .12);
    sewingMachine(db, -.3, .9, .02, 0); foldedStack(db, -.3, .95, .14, [KN.recNavy], 0);   // a knit piece under the presser foot
    for (const [dx, col] of [[.2, '#8f4a3a'], [.32, '#c9a565'], [.44, '#3d5170']]) add(db, new THREE.CylinderGeometry(.035, .05, .17, 20), std('cone_' + col, () => ({ color: col, roughness: .9, map: weaveMap('coil', [3, 6]) })), dx, .985, .1);
    basket(db, -.78, .9, .05, { r: .13, h: .14, kind: 'twill', fibre: 'hogla' }); offcutHeap(db, -.78, .99, .05, { r: .12, h: .05, n: 60, colors: ['#3d5170', '#8f4a3a', '#8e8b86'], seed: 680 });
    footprint(4.07, -16.97, 6.13, -16.23); shade('Z06', 4.1, -16.95, 6.1, -16.25, .45);
    const scr = new THREE.Group(); scr.position.set(3.35, 0, -16.95); g.add(scr);
    add(scr, merged([B(.6, .03, .5, 0, 0, 0), B(.06, 1.75, .06, 0, .03, -.05)]), std('steel_dark', () => ({})));
    box(scr, std('screen_bezel', () => ({ color: '#111', roughness: .35 })), 0, .95, .0, 1.47, .85, .05);
    const slide = std('lesson_slide', () => { const c = canvas(px(640), px(360)), x = c.getContext('2d'), W = c.width, H = c.height; x.fillStyle = '#f3ede2'; x.fillRect(0, 0, W, H);
      x.fillStyle = '#3c2a1e'; x.font = `600 ${H * .085}px system-ui, sans-serif`; x.font = `600 ${H * .075}px system-ui, sans-serif`; x.fillText('Lesson 1 · Fibre to garment, and back', W * .06, H * .17);
      x.fillStyle = '#9c5534'; x.fillRect(W * .06, H * .22, W * .1, H * .012);
      [['Fibre', '#c9a565'], ['Yarn', '#8f4a3a'], ['Knit', '#3d5170'], ['Reuse', '#6f7a4c']].forEach(([t, col], i) => { const X = W * (.06 + i * .23); x.fillStyle = col; x.fillRect(X, H * .36, W * .19, H * .3); x.fillStyle = '#fff'; x.font = `500 ${H * .06}px system-ui, sans-serif`; x.fillText(t, X + W * .02, H * .53);
        if (i < 3) { x.fillStyle = '#3c2a1e'; x.fillText('›', X + W * .2, H * .53); } });
      x.fillStyle = '#5b4636'; x.font = `400 ${H * .05}px system-ui, sans-serif`; x.fillText('Illustrative lesson · Design Education Academy (option A)', W * .06, H * .85);
      const t = tex(c, { clamp: true }); return { map: t, emissive: '#ffffff', emissiveMap: t, emissiveIntensity: .55, roughness: .4 }; });
    add(scr, new THREE.PlaneGeometry(1.4, .79), slide, 0, 1.375, .027);
    footprint(3.03, -17.22, 3.67, -16.68); shade('Z06', 3.05, -17.2, 3.65, -16.7, .4);
    const pin = new THREE.Group(); pin.position.set(6.95, 0, -16.95); g.add(pin);
    add(pin, merged([B(.04, 1.75, .04, -.42, 0, 0), B(.04, 1.75, .04, .42, 0, 0), B(.9, .04, .3, 0, 0, 0)]), M.oak);
    box(pin, std('felt_board', () => ({ color: '#6f6658', roughness: 1, map: weaveMap('plain', [6, 8]) })), 0, .55, 0, .82, 1.15, .03);
    [KN.ecru, KN.recNavy, KN.juteBlend, KN.recGrey, KN.indigo, KN.recRed].forEach((m, i) => add(pin, scaleUV(new THREE.PlaneGeometry(.17, .17), .17, .17), m, -.25 + (i % 3) * .25, 1.42 - Math.floor(i / 3) * .25, .017));
    add(pin, new THREE.PlaneGeometry(.36, .25), std('sketch', () => ({ color: '#f4efe4', roughness: .9 })), -.15, .82, .017); add(pin, new THREE.PlaneGeometry(.25, .3), textileMat('kantha_pin', (x, w, h) => drawKantha(x, w, h, 17), [192, 230]), .22, .8, .017);
    footprint(6.48, -17.12, 7.42, -16.78); shade('Z06', 6.5, -17.1, 7.4, -16.8, .35);
    // materials shelf at the south end, tutor room in the old discussion room
    const sh = new THREE.Group(); sh.position.set(5.35, 0, -6.08); sh.rotation.y = Math.PI; g.add(sh);
    add(sh, merged([B(2.0, .03, .34, 0, 0, 0), B(2.0, .03, .34, 0, .4, 0), B(2.0, .03, .34, 0, .8, 0), B(2.0, .03, .34, 0, 1.17, 0), B(.03, 1.2, .34, -1.0, 0, 0), B(.03, 1.2, .34, 1.0, 0, 0)]), M.wood);
    foldedStack(sh, -.7, .03, 0, [KN.ecru, KN.oat, KN.juteBlend]); foldedStack(sh, -.25, .03, 0, [KN.recNavy, KN.recGrey]);
    basket(sh, .3, .03, 0, { r: .14, h: .18, kind: 'twill', fibre: 'hogla' }); offcutHeap(sh, .3, .16, 0, { r: .13, h: .05, n: 60, colors: ['#6f7a4c', '#8f4a3a', '#8e8b86'], seed: 690 });
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
  // ---------------------------------------------------------------- the design wing (every option): making line, fibre library, fabric lab, remake and repair
  if (want('BEL_MAKING_LINE')) {
    // the solid south wall of the corridor's north strip (face z -21.4104; the strip's north side and the corridor are glass)
    const g = item('BEL_MAKING_LINE'), WZ = -21.4104, LY = .98, xs = [22.85, 23.5, 24.15, 24.8, 25.45, 26.1];
    for (const x of xs) box(g, M.oak, x, LY, WZ - .066, .6, .03, .13);
    footprint(22.5, WZ - .14, 26.42, WZ);
    const step = (i, lines) => add(g, new THREE.PlaneGeometry(.5, .26), card(lines, { w: .5, h: .26, scale: 1.1 }), xs[i], 1.47, WZ - .004, 0, Math.PI);
    const Y = LY + .03, Z = WZ - .07, small = (x, mats) => { const f = new THREE.Group(); f.position.set(x, Y, Z); f.scale.setScalar(.5); g.add(f); foldedStack(f, 0, 0, 0, mats, .1); };
    // 1 fibre: cotton bolls, a jute hank, a tuft recovered from cutting waste
    cottonStems(g, xs[0] - .17, Y, Z, { n: 2, h: .26, seed: 9 });
    add(g, new THREE.CylinderGeometry(.03, .04, .22, 16, 1), FB.juteHank, xs[0] + .02, Y + .11, Z);
    fibreHeap(g, xs[0] + .18, Y, Z, .045, FB.jhutNavy, 701);
    // 2 yarn: cotton, a jute and cotton blend, a recycled melange
    yarnCone(g, xs[1] - .16, Y, Z, coneMat('#efe8da')); yarnCone(g, xs[1], Y, Z, coneMat('#c7ae7c')); yarnCone(g, xs[1] + .16, Y, Z, KN.recNavy);
    // 3 knit fabric: a roll of recycled jersey and a rib swatch
    fabricRoll(g, xs[2] - .08, Y, Z, KN.recNavy, { len: .3, r: .045 }); add(g, scaleUV(new THREE.BoxGeometry(.16, .005, .1), .16, .1), KN.ecruRib, xs[2] + .17, Y + .0025, Z, 0, .1);
    // 4 cut and sew: a cut front panel pinned to the wall, its offcuts kept and sorted
    add(g, new THREE.ShapeGeometry(garmentOutline('tee'), 6), KN.recNavy, xs[3] - .06, 1.315, WZ - .006, 0, Math.PI).scale.setScalar(.4);
    offcutHeap(g, xs[3] + .16, Y, Z, { r: .05, h: .03, n: 30, colors: ['#3f4c66', '#55688a', '#33445f'], seed: 702 });
    // 5 test: the knitted tee beside its (empty) test card
    small(xs[4] - .14, [KN.recNavy]); standingCard(g, ['Test', 'Durability: to be measured', 'Records to be added'], xs[4] + .14, Y, Z + .01, Math.PI, { w: .16, h: .09 });
    // 6 wear and return: the tee mended in kantha stitch, with its take-back tag
    small(xs[5] - .12, [mendMat('navy', '#3f4c66', '#8a97ad', 9)]); standingCard(g, ['Take-back'], xs[5] + .13, Y, Z + .01, Math.PI, { w: .09, h: .045 });
    step(0, ['1 · Fibre', 'Cotton, jute, and fibre', 'recovered from cutting waste']); step(1, ['2 · Yarn', 'Spun from one fibre or a blend', 'Spinner to be identified']); step(2, ['3 · Knit fabric', 'Single jersey and rib']);
    step(3, ['4 · Cut and sew', 'Offcuts kept, sorted by colour']); step(4, ['5 · Test', 'Durability: GSM, shrinkage,', 'colourfastness: to add']); step(5, ['6 · Wear and return', 'Mended in kantha stitch;', 'at the end, back to fibre']);
    const tc = canvas(px(1280), px(64)), tx = tc.getContext('2d'); tx.fillStyle = '#b88c5c'; tx.fillRect(0, 0, tc.width, tc.height); tx.fillStyle = '#3c2a1e'; tx.font = `600 ${tc.height * .46}px system-ui, 'Segoe UI', sans-serif`; tx.textBaseline = 'middle';
    tx.fillText('The making line · ecodesign from fibre to garment and back · one T-shirt in six steps (illustrative)', tc.width * .02, tc.height * .54);
    add(g, new THREE.PlaneGeometry(3.9, .195), std('making_title', () => ({ map: tex(tc, { clamp: true }), roughness: .6 })), (xs[0] + xs[5]) / 2, 1.9, WZ - .004, 0, Math.PI);
  }
  if (want('BEL_MATERIALS_LIBRARY')) {
    const g = item('BEL_MATERIALS_LIBRARY');   // low shelf F132 top 0.7112 (x 22.25-22.61, z -9.41..-6.74); review table F134 top 0.9144, D65 booth at x 23.98-24.79
    const T = .7112, X = 22.43;
    [[FB.cotton, 'Cotton'], [FB.jhutNavy, 'Jhut (recycled)'], [FB.usedMix, 'Used garments'], [FB.jute, 'Jute'], [FB.banana, 'Banana · R&D'], [FB.pineapple, 'Pineapple · R&D'], [FB.indigo, 'Indigo · R&D'], [null, 'Coconut buttons']].forEach(([mat, name], i) => {
      const z = -9.25 + i * .32, b = new THREE.Group(); b.position.set(X, T, z); g.add(b);
      add(b, merged([B(.3, .14, .015, 0, 0, -.135), B(.3, .14, .015, 0, 0, .135), B(.015, .14, .27, -.143, 0, 0), B(.015, .14, .27, .143, 0, 0), B(.3, .012, .3, 0, 0, 0)]), M.oak);
      if (mat) fibreHeap(b, 0, .012, 0, .1, mat, 720 + i);
      else for (let k = 0; k < 14; k++) add(b, new THREE.CylinderGeometry(.012, .012, .004, 18), std('coconut_button', () => ({ color: '#4f3422', roughness: .35 })), -.09 + (k % 5) * .045, .016 + Math.floor(k / 5) * .002, -.06 + Math.floor(k / 5) * .06, (k % 3 - 1) * .2, 0, (k % 2 - .5) * .3);
      add(b, new THREE.PlaneGeometry(.2, .05), card([name], { w: .2, h: .05, scale: .6 }), .152, .07, 0, 0, Math.PI / 2);
    });
    const RT = .9144; [[24.97, -9.2, .1, 'Fibre: recycled cotton (jhut)'], [24.97, -8.88, -.05, 'Fibre: cotton'], [23.8, -9.15, .08, 'Fibre: jute and cotton, R&D']].forEach(([x, z, ry, fibre]) =>
      add(g, new THREE.PlaneGeometry(.15, .21), card(['Product passport', fibre, 'Origin: to be documented', 'Recycled share: to certify', 'Durability tests: none yet', 'Repair and care: to write', 'Recyclability: to assess'], { w: .15, h: .21, scale: .8 }), x, RT + .002, z, -Math.PI / 2, 0, ry));
    standingCard(g, ['Product passport · concept', 'Ready for the EU ecodesign rules', 'for apparel, still being drafted'], 23.85, RT, -8.72, Math.PI / 2, { w: .19, h: .09 });
  }
  if (want('BEL_TEST_LAB')) {
    const g = item('BEL_TEST_LAB'); const T = .7874, X = 22.56;   // post-processing bench F143 (terrazzo top 0.7874), x 22.25-22.88, z -14.87..-12.06
    const marked = (key, base) => std('shrink_' + key, () => { const s = px(128), c = canvas(s, s), x = c.getContext('2d'); x.fillStyle = base; x.fillRect(0, 0, s, s);   // a knit swatch marked for wash shrinkage
      x.globalCompositeOperation = 'multiply'; x.scale(1 / 3, 1 / 3); x.fillStyle = x.createPattern(knitTile('jersey'), 'repeat'); x.fillRect(0, 0, s * 3, s * 3); x.setTransform(1, 0, 0, 1, 0, 0); x.globalCompositeOperation = 'source-over';
      x.strokeStyle = '#f4efe4'; x.lineWidth = s / 90; x.strokeRect(s * .15, s * .15, s * .7, s * .7); for (const [a, b] of [[.15, .15], [.85, .15], [.15, .85], [.85, .85]]) { x.beginPath(); x.arc(s * a, s * b, s / 40, 0, 7); x.stroke(); }
      return { map: tex(c, { clamp: true }), roughness: .95 }; });
    [['ecru', '#e9e1d0'], ['navy', '#3f4c66'], ['jute', '#c7ae7c'], ['grey', '#8e8b86']].forEach(([k, col], i) => {
      const z = -14.62 + i * .27; add(g, new THREE.BoxGeometry(.18, .005, .18), marked(k, col), X - .02, T + .0025, z, 0, (i - 1.5) * .06);
      add(g, new THREE.PlaneGeometry(.08, .025), card([`Sample ${i + 1}`], { w: .08, h: .025, scale: .35 }), X + .22, T + .002, z, -Math.PI / 2, 0, Math.PI / 2);
    });
    const cutter = new THREE.Group(); cutter.position.set(X, T, -13.55); g.add(cutter);   // a round GSM cutter
    add(cutter, new THREE.CylinderGeometry(.08, .08, .02, 32), std('cutter_pad', () => ({ color: '#3a3d40', roughness: .6 })), 0, .01, 0);
    add(cutter, new THREE.CylinderGeometry(.052, .052, .05, 32), std('steel', () => ({ color: '#c8c8c8', metalness: .8, roughness: .3 })), 0, .045, 0);
    add(cutter, new THREE.CylinderGeometry(.01, .01, .12, 10), std('machine_dark', () => ({ color: '#2e2e30', roughness: .4 })), 0, .1, 0, 0, 0, Math.PI / 2);
    box(g, std('scale_body', () => ({ color: '#dfe2e4', roughness: .4 })), X, T, -13.2, .24, .05, .26); box(g, std('lcd', () => ({ color: '#1b1f22', roughness: .3 })), X + .121, T + .015, -13.2, .002, .025, .08);
    const gs = canvas(px(256), px(96)), gx = gs.getContext('2d'); gx.fillStyle = '#f4efe4'; gx.fillRect(0, 0, gs.width, gs.height);   // grey scale for colourfastness
    for (let k = 0; k < 9; k++) { const v = Math.round(70 + k * 20); gx.fillStyle = `rgb(${v},${v},${v})`; gx.fillRect(gs.width * (.05 + k * .1), gs.height * .2, gs.width * .09, gs.height * .45); }
    gx.fillStyle = '#3c2a1e'; gx.font = `500 ${gs.height * .16}px system-ui, sans-serif`; gx.fillText('Grey scale · colourfastness', gs.width * .05, gs.height * .88);
    add(g, new THREE.PlaneGeometry(.2, .075), std('grey_scale', () => ({ map: tex(gs, { clamp: true }), roughness: .7 })), X, T + .002, -12.88, -Math.PI / 2, 0, Math.PI / 2);
    add(g, new THREE.PlaneGeometry(.21, .29), card(['Durability test log', 'GSM · shrinkage · spirality', 'Colourfastness · pilling', 'Method: to agree with an accredited lab', 'Records to be added'], { w: .21, h: .29, scale: .9 }), X, T + .004, -12.48, -Math.PI / 2, 0, -.1);
    standingCard(g, ['Fabric lab', 'No results shown until tests are done'], X + .2, T, -12.2, Math.PI / 2, { w: .18, h: .07 });
  }
  if (want('BEL_PROTOTYPE_WORKSHOP')) {
    const g = item('BEL_PROTOTYPE_WORKSHOP'); const T = .9145, X = 25.53;   // pattern table F151 top 0.9145, x 24.92-26.14, z -20.52..-18.08; steam station F155 top 0.8636
    patternPieces(g, X - .05, T, -19.75, Math.PI / 2, .85);   // a tee pattern in kraft paper
    [['#3d5170', '#4a5f80'], ['#8f4a3a', '#a35a48'], ['#8e8b86', '#a9a59e']].forEach((cols, i) => offcutHeap(g, X - .32 + i * .3, T, -18.95, { r: .11, h: .05, n: 50, colors: cols, seed: 730 + i }));
    const pieced = textileMat('pieced_offcuts', (x, w, h) => { const r = rng(83), cols = ['#3f4c66', '#55688a', '#8f4a3a', '#a35a48', '#8e8b86', '#6f7a4c', '#d6c7a8', '#45474a'];
      for (let j = 0; j < 6; j++) { let X0 = 0; while (X0 < w) { const ww = w * (.1 + r() * .18); x.fillStyle = cols[Math.floor(r() * cols.length)]; x.fillRect(X0, j * h / 6, ww, h / 6); X0 += ww; } }
      x.strokeStyle = 'rgba(245,238,225,.9)'; x.lineWidth = Math.max(1.5, w / 170); x.setLineDash([w / 70, w / 110]); for (let y = h / 12; y < h; y += h / 6) { x.beginPath(); x.moveTo(0, y); x.lineTo(w, y + (r() - .5) * 3); x.stroke(); } x.setLineDash([]); }, [256, 200]);
    add(g, new THREE.PlaneGeometry(.5, .4), pieced, X - .12, T + .002, -18.42, -Math.PI / 2, 0, .05);
    foldedStack(g, X + .32, T, -18.4, [mendMat('charcoal', '#45474a', '#8e8b86', 5)], .2);
    standingCard(g, ['Remake and repair', 'Offcuts pieced into panels', 'Repairs in kantha stitch'], X - .45, T, -18.3, Math.PI / 2, { w: .18, h: .09 });
    foldedStack(g, 23.62, .8636, -15.47, [KN.ecru, KN.recNavy], .1);   // pressed on the steam station, ready for the fit review
  }
  // ---------------------------------------------------------------- pilot rooms: academy annex, staff and artisan dining, records room
  if (want('BEL_ACADEMY_ANNEX')) {
    const g = item('BEL_ACADEMY_ANNEX'); const T = .7493;   // training table F219 (top 0.7493): x 23.55-25.98, z -34.24..-33.32; six chairs on its long sides
    [23.99, 24.77, 25.53].forEach((x, i) => { for (const [z, s] of [[-34.0, 1], [-33.56, -1]]) {
      add(g, scaleUV(new THREE.BoxGeometry(.12, .005, .12), .12, .12), [KN.ecru, KN.recNavy, KN.juteBlend][i], x, T + .0025, z, 0, s * .1);
      add(g, new THREE.PlaneGeometry(.15, .21), std('notebook', () => ({ color: '#efe8da', roughness: .9 })), x + .16, T + .002, z, -Math.PI / 2, 0, s * .12); } });
    foldedStack(g, 24.72, T, -33.78, [KN.oat, mendMat('madder', '#8f4a3a', '#d6c7a8', 7)], .15);   // the mending kit: a tee mended in kantha stitch and thread
    [['#8f4a3a', -.06], ['#2f4a6b', 0], ['#c9a565', .06]].forEach(([col, dz]) => add(g, new THREE.CylinderGeometry(.014, .014, .035, 12), std('thread_' + col, () => ({ color: col, roughness: .8 })), 24.98, T + .0175, -33.78 + dz));
    [['#8f4a3a', -.06], ['#c9a565', .06]].forEach(([col, dz]) => add(g, new THREE.CylinderGeometry(.035, .05, .17, 20), std('cone_' + col, () => ({ color: col, roughness: .9, map: weaveMap('coil', [3, 6]) })), 23.72, T + .085, -33.78 + dz));
    standingCard(g, ['Academy annex · pilot', 'A class of six at this table', 'Fibre, knit and repair'], 25.85, T, -33.78, Math.PI / 2, { w: .18, h: .09 });
    // craft wall on the solid west wall (face x 22.2513), clear of the screen (z -36.40..-34.72)
    const cw = new THREE.Group(); cw.position.set(22.262, 1.0, -33.25); cw.rotation.y = Math.PI / 2; g.add(cw);
    box(cw, std('felt_board', () => ({ color: '#6f6658', roughness: 1, map: weaveMap('plain', [6, 8]) })), 0, 0, .012, 1.5, .95, .024);
    [KN.ecru, KN.recNavy, KN.juteBlend, KN.recGrey, KN.ecruRib, KN.recRed].forEach((m, i) =>
      add(cw, scaleUV(new THREE.PlaneGeometry(.17, .17), .17, .17), m, -.55 + (i % 3) * .22, .7 - Math.floor(i / 3) * .24, .026));
    add(cw, new THREE.PlaneGeometry(.36, .25), std('sketch', () => ({ color: '#f4efe4', roughness: .9 })), .35, .66, .026);
    add(cw, new THREE.PlaneGeometry(.3, .36), textileMat('kantha_pin', (x, w, h) => drawKantha(x, w, h, 17), [192, 230]), .4, .26, .026);
    add(cw, new THREE.PlaneGeometry(.44, .12), card(['Craft wall · student work (illustrative)'], { w: .44, h: .12, scale: 1 }), -.33, .14, .026);
  }
  if (want('BEL_ARTISAN_DINING')) {
    const g = item('BEL_ARTISAN_DINING'); const T = .7493;   // dining tables F194 (z -30.18..-29.26) and F203 (z -26.37..-25.45), x 23.93-26.37; four chairs a side
    for (const zc of [-29.72, -25.91]) {
      box(g, wovenMaterial('runner_hogla', 'twill', FIBRE.hogla, [10, 1]), 25.15, T, zc, 2.2, .004, .3);
      for (const x of [24.235, 24.84, 25.45, 26.06]) for (const s of [-1, 1]) {
        const z = zc + s * .3; clayPlate(g, x, T, z, .1, M.clayCream); cup(g, x + .14, T, z - s * .02, 'tumbler');
      }
      jug(g, 24.7, T + .004, zc, .4); add(g, lathe([[0, 0], [.07, 0], [.14, .045], [.15, .08], [.13, .08], [.06, .028], [0, .028]], 36), M.clay, 25.6, T + .004, zc);
    }
    // water and tea in clay on the pantry counter (top 0.9018 at x 22.25-22.91)
    const P = .9018; add(g, new THREE.TorusGeometry(.085, .02, 10, 28), M.wood, 22.58, P + .02, -28.2, Math.PI / 2);
    add(g, lathe([[0, 0], [.07, 0], [.12, .05], [.135, .13], [.12, .2], [.07, .245], [.05, .28], [.062, .3], [.055, .305], [.042, .28], [0, .27]], 40), M.clay, 22.58, P + .015, -28.2);
    tray(g, 22.58, P, -28.7, .22, .3, Math.PI / 2); for (const dz of [-.08, 0, .08]) cup(g, 22.58, P + .012, -28.7 + dz, 'tumbler', M.clayCream);
    teapot(g, 22.58, P, -29.3, Math.PI / 2); cup(g, 22.5, P, -29.6, 'teacup', M.clayCream); cup(g, 22.66, P, -29.62, 'teacup', M.clayCream);
    standingCard(g, ['Staff and artisan dining', 'The same clay and wood as the buyer rooms', 'Glazes to be tested before use'], 22.75, P, -29.95, Math.PI / 2, { w: .2, h: .1 });
  }
  if (want('BEL_RECORDS_ROOM')) {
    const g = item('BEL_RECORDS_ROOM'); const T = .7493;   // audit table F073 (top 0.7493): x 3.68-5.21, z -21.16..-20.24; north wall solid (face z -22.6323)
    ['01 Fibre', '02 Recycled', '03 Tests', '04 Water', '05 Energy', '06 Makers'].forEach((t, i) => {
      const x = 3.9 + i * .22, b = new THREE.Group(); b.position.set(x, T, -20.98); g.add(b);
      box(b, std('box_file', () => ({ color: '#3d4a42', roughness: .7 })), 0, 0, 0, .08, .32, .28);
      add(b, new THREE.PlaneGeometry(.06, .2), card([t], { w: .06, h: .2, scale: .5 }), 0, .17, .141);
    });
    add(g, new THREE.PlaneGeometry(.3, .21), card(['Evidence register', 'Each claim, its document and date', 'Entries to be added'], { w: .3, h: .21, scale: 1 }), 4.45, T + .002, -20.5, -Math.PI / 2);
    const ic = canvas(px(600), px(840)), ix = ic.getContext('2d'), W = ic.width, H = ic.height; ix.fillStyle = '#f4efe4'; ix.fillRect(0, 0, W, H);
    ix.fillStyle = '#3c2a1e'; ix.font = `600 ${W * .07}px system-ui, sans-serif`; ix.fillText('The Open Record', W * .07, H * .1);
    ix.font = `400 ${W * .036}px system-ui, sans-serif`; ix.fillStyle = '#5b4636'; ix.fillText('Every claim on this floor, its evidence and its status', W * .07, H * .15);
    [['Claim', 'Evidence', 'Status'], ['Fibre origins', 'Supplier papers', 'To be collected'], ['Recycled content', 'Certificates', 'None yet'], ['Durability tests', 'Accredited lab', 'None yet'],
     ['Product passport', 'Passport data set', 'To prepare'], ['Drinking water', 'Dated lab reports', 'None yet'], ['Solar generation', 'Metered data', 'Not connected'],
     ['Makers paid, credited', 'Agreements, receipts', 'To be collected'], ['Glaze safety', 'Lead, cadmium tests', 'None yet']].forEach((row, r) => {
      const y = H * (.25 + r * .075); ix.font = `${r ? 400 : 600} ${W * .03}px system-ui, sans-serif`;
      row.forEach((c, k) => { ix.fillStyle = k === 2 && r ? '#9c3b2a' : '#3c2a1e'; ix.fillText(c, W * [.05, .4, .72][k], y); });
      ix.fillStyle = 'rgba(60,40,25,.2)'; ix.fillRect(W * .07, y + W * .02, W * .86, 2);
    });
    ix.fillStyle = '#5b4636'; ix.font = `400 ${W * .028}px system-ui, sans-serif`; ix.fillText('Passport fields follow the EU apparel rules once adopted.', W * .05, H * .91); ix.fillText('Originals are kept in this room and shown on request.', W * .05, H * .95);
    const fr = new THREE.Group(); fr.position.set(4.3, 1.5, -22.62); g.add(fr);
    box(fr, M.oak, 0, -.45, .01, .66, .9, .02); add(fr, new THREE.PlaneGeometry(.6, .84), std('open_record', () => ({ map: tex(ic, { clamp: true }), roughness: .8 })), 0, 0, .021);
    standingCard(g, ['Records room', 'The originals behind every claim', 'Open to auditors and buyers on request'], 5.05, T, -20.35, 0, { w: .2, h: .1 });
  }
  // ---------------------------------------------------------------- pilot rooms: buyer project room (the approved CAD dressing stays in Z14)
  const screenMat = (key, draw) => std('screen_' + key, () => { const c = canvas(px(640), px(360)), x = c.getContext('2d'); draw(x, c.width, c.height);
    const t = tex(c, { clamp: true }); return { map: t, emissive: '#ffffff', emissiveMap: t, emissiveIntensity: .6, roughness: .35 }; });
  if (want('BEL_BUYER_PROJECT')) {
    const g = item('BEL_BUYER_PROJECT'); const T = .7494;   // guest table F091: x -0.81-1.32, z -2.74..-1.73; screen F098 face z -3.8036 (x -0.25-0.97, y 0.97-1.65)
    add(g, new THREE.PlaneGeometry(1.18, .64), screenMat('project_board', (x, w, h) => {
      x.fillStyle = '#f3ede2'; x.fillRect(0, 0, w, h); x.fillStyle = '#3c2a1e'; x.font = `600 ${h * .085}px system-ui, sans-serif`; x.fillText('Buyer project board', w * .05, h * .16);
      ['Brief', 'Fabric', 'Lab dip', 'Fit', 'Tests', 'Order'].forEach((t, i) => { const X = w * (.05 + i * .153); x.fillStyle = ['#c9a565', '#8f4a3a', '#3d5170', '#6f7a4c', '#b88c5c', '#45474a'][i]; x.fillRect(X, h * .32, w * .14, h * .2);
        x.fillStyle = '#fff'; x.font = `500 ${h * .055}px system-ui, sans-serif`; x.fillText(t, X + w * .01, h * .45); x.fillStyle = '#5b4636'; x.font = `400 ${h * .042}px system-ui, sans-serif`; x.fillText('date to agree', X + w * .005, h * .62); });
      x.fillStyle = '#5b4636'; x.font = `400 ${h * .05}px system-ui, sans-serif`; x.fillText('Export and order desk (pilot) · illustrative', w * .05, h * .88); }), .36, 1.31, -3.795);
    tray(g, .1, T, -2.2, .4, .26, 0); [KN.ecru, KN.recNavy, KN.juteBlend].forEach((m, i) => add(g, scaleUV(new THREE.BoxGeometry(.1, .005, .1), .1, .1), m, -.03 + i * .13, T + .0145, -2.2, 0, (i - 1) * .1));
    jug(g, .85, T, -2.05, -.5); cup(g, .7, T, -2.35, 'tumbler'); cup(g, .98, T, -2.38, 'tumbler');
    add(g, new THREE.PlaneGeometry(.21, .29), card(['Order checklist', 'Tech pack · product passport', 'Lab dip · fit sample · tests', 'Artisan packaging (to agree)', 'All to be agreed with the buyer'], { w: .21, h: .29, scale: .9 }), -.5, T + .002, -2.25, -Math.PI / 2, 0, .1);
    standingCard(g, ['Buyer project room', 'Private desks for visiting buyer teams', 'Export and order desk in the pilot'], .45, T, -1.85, 0, { w: .2, h: .1 });
  }
  // ---------------------------------------------------------------- Bengal craft from the owner's references (30 Oct 2026): natural indigo, jhut patchwork,
  // the tea stall, hurricane lanterns (electric), alpana, kula and dala, cane and bamboo, painted clay, jute. Self-made forms; makers to be identified.
  if (want('BEL_INDIGO_SWAGS')) {
    // the experience-centre deck (underside y 2.90) between the track rails (spots reach z -9.24 / -7.14): three cloths of natural indigo in
    // shallow swags, in place of the approved cloth fins on this route, clear of the AC unit (x 15.05-16.24) and its smoke detector
    const g = item('BEL_INDIGO_SWAGS'); overhead.add(g); const span = 1.2;
    for (const [x0, x1] of [[9.85, 14.85], [16.45, 21.75]]) [[-8.6, 0, 'a', false], [-8.22, .6, 'b', true], [-7.84, .3, 'c', false]].forEach(([zc, ph, key, ombre]) => {
      const len = x1 - x0, geo = new THREE.PlaneGeometry(len, .34, Math.round(len * 24), 3), p = geo.attributes.position, uv = geo.attributes.uv;
      for (let i = 0; i < p.count; i++) { const X = p.getX(i) + len / 2, Zs = p.getY(i), t = (((x0 + X + ph) % span) + span) % span / span, sag = Math.pow(Math.sin(Math.PI * t), .85);
        p.setXYZ(i, X - len / 2, -(.035 + .32 * sag) + Zs * .1 * Math.sin((x0 + X) * 1.7 + ph), Zs); }
      for (let i = 0; i < uv.count; i++) uv.setX(i, uv.getX(i) * len / 1.8);
      geo.computeVertexNormals(); add(g, geo, shiboriMat(key, 300 + key.charCodeAt(0), ombre), (x0 + x1) / 2, 2.895, zc);
      for (let k = Math.ceil((x0 + ph) / span); k * span - ph <= x1; k++) add(g, new THREE.CylinderGeometry(.006, .006, .04, 6), std('brass', () => ({ color: '#a57c3c', metalness: .85, roughness: .32 })), k * span - ph, 2.875, zc);
    });
  }
  if (want('BEL_JHUT_RIVER')) {
    // the free floor between the forms' plinth (x 14.35) and the material table (x 16.51), z -9.0..-8.0 (probed: open terrazzo): a sewing table
    // and a river of patchwork pieced from cutting waste, running off the table and across the floor. An installation, not a product
    const g = item('BEL_JHUT_RIVER'), ZC = -8.58;
    const st = new THREE.Group(); st.position.set(14.9, 0, -8.5); g.add(st); add(st, tableWood(.9, .5, .76), M.wood); sewingMachine(st, -.1, .76, -.03, 0);
    const pieced = textileMat('jhut_river', (x, w, h) => { const r = rng(91), cols = ['#3f4c66', '#55688a', '#8f4a3a', '#a35a48', '#8e8b86', '#6f7a4c', '#d6c7a8', '#45474a', '#c9a565', '#2f6b5a', '#b8352a', '#e6dccb'];
      for (let j = 0; j < 8; j++) { let X0 = 0; while (X0 < w) { const ww = w * (.05 + r() * .09); x.fillStyle = cols[Math.floor(r() * cols.length)]; x.fillRect(X0, j * h / 8, ww, h / 8); X0 += ww; } }
      x.strokeStyle = 'rgba(245,238,225,.8)'; x.lineWidth = Math.max(1.5, w / 260); x.setLineDash([w / 120, w / 180]); for (let y = h / 16; y < h; y += h / 8) { x.beginPath(); x.moveTo(0, y); x.lineTo(w, y + (r() - .5) * 3); x.stroke(); } x.setLineDash([]); }, [768, 256]);
    const path = new THREE.CatmullRomCurve3([[14.66, .772, ZC], [15.05, .776, ZC], [15.36, .77, ZC], [15.47, .6, ZC], [15.52, .3, ZC + .02], [15.6, .06, ZC + .03], [15.85, .018, ZC], [16.1, .018, ZC - .05], [16.33, .018, ZC + .02]].map(v => new THREE.Vector3(...v)), false, 'centripetal');
    const N = 90, pts = path.getSpacedPoints(N), pos = [], uv = [], idx = [], L = path.getLength();
    pts.forEach((P, i) => { const t = i / N, w = .5 + .42 * Math.max(0, (t - .45) / .55), wob = P.y < .05 ? .004 + .004 * Math.sin(i * 1.3) : 0;
      for (const s of [-1, 1]) { pos.push(P.x, P.y + wob + (P.y < .05 ? .004 * (1 + s) : 0), P.z + s * w / 2); uv.push(t * L / .9, s > 0 ? 1 : 0); } });
    for (let i = 0; i < N; i++) idx.push(i * 2, i * 2 + 1, i * 2 + 2, i * 2 + 1, i * 2 + 3, i * 2 + 2);
    const rg = new THREE.BufferGeometry(); rg.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); rg.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); rg.setIndex(idx); rg.computeVertexNormals();
    add(g, rg, pieced);
    standingCard(g, ['Jhut patchwork', 'Cutting waste pieced back into cloth', 'An installation · makers to be credited'], 15.22, .76, -8.31, 0, { w: .19, h: .1 });
    footprint(14.43, -9.0, 16.4, -8.0);
  }
  if (want('BEL_TEA_STALL')) {
    // the free solid west wall of the dining room (face x 22.2513, z -23.3..-25.4, probed clear from the floor to the ceiling): a wall-mounted
    // tong, the Bengali tea stall, as the tea point: a cart front on two wheels, a painted canopy, an electric hurricane lantern, kettle and clay cups
    const g = item('BEL_TEA_STALL'), f = new THREE.Group(); f.position.set(22.2513, 0, -24.35); f.rotation.y = Math.PI / 2; g.add(f);   // local +z: into the room
    const blue = std('stall_blue', () => ({ color: '#2b5f9e', roughness: .5 })), red = std('stall_red', () => ({ color: '#b3261e', roughness: .5 }));
    box(f, M.wood, 0, .82, .23, 1.5, .06, .44); box(f, M.wood, 0, .5, .05, 1.46, .32, .06);
    const skirt = std('stall_skirt', () => { const W = px(512), H = px(96), c = canvas(W, H), x = c.getContext('2d'); x.fillStyle = '#c2185b'; x.fillRect(0, 0, W, H);
      for (let k = 0; k < 10; k++) { const cx = (k + .5) * W / 10, cy = H / 2; for (let p = 0; p < 8; p++) { const a = p / 8 * Math.PI * 2; x.fillStyle = p % 2 ? '#ffd23f' : '#ff7a1a'; x.beginPath(); x.ellipse(cx + Math.cos(a) * H * .16, cy + Math.sin(a) * H * .16, H * .14, H * .06, a, 0, 7); x.fill(); } x.fillStyle = '#1e8a4c'; x.beginPath(); x.arc(cx, cy, H * .08, 0, 7); x.fill(); }
      x.fillStyle = '#ffd23f'; x.fillRect(0, 0, W, H * .08); x.fillRect(0, H * .92, W, H * .08); return { map: tex(c, { clamp: true }), roughness: .55 }; });
    add(f, new THREE.PlaneGeometry(1.5, .26), skirt, 0, .7, .452);
    for (const sx of [-.72, .72]) for (const sz of [.05, .42]) add(f, new THREE.CylinderGeometry(.018, .02, 1.25, 10), blue, sx, .82 + .625, sz);
    const sign = std('stall_sign', () => { const W = px(640), H = px(200), c = canvas(W, H), x = c.getContext('2d'); x.fillStyle = '#c62828'; x.fillRect(0, 0, W, H);
      x.fillStyle = '#ffd23f'; x.fillRect(0, H * .86, W, H * .14); for (let k = 0; k < 16; k++) { x.fillStyle = k % 2 ? '#1e8a4c' : '#ffd23f'; x.beginPath(); x.arc((k + .5) * W / 16, H * .93, H * .045, 0, 7); x.fill(); }
      for (const cx of [W * .09, W * .92]) for (let p = 0; p < 10; p++) { const a = p / 10 * Math.PI * 2; x.fillStyle = p % 2 ? '#ffd23f' : '#ff9ec7'; x.beginPath(); x.ellipse(cx + Math.cos(a) * H * .14, H * .42 + Math.sin(a) * H * .14, H * .12, H * .05, a, 0, 7); x.fill(); }
      x.fillStyle = '#fff6e0'; x.textAlign = 'center'; x.textBaseline = 'middle'; x.font = `700 ${H * .5}px 'Noto Sans Bengali', 'Lohit Bengali', 'Kohinoor Bangla', 'Bangla Sangam MN', 'Nirmala UI', 'Vrinda', sans-serif`; x.fillText('চা', W * .33, H * .43);
      x.font = `700 ${H * .22}px system-ui, sans-serif`; x.fillText('CHA · TEA', W * .6, H * .43); x.font = `500 ${H * .1}px system-ui, sans-serif`; x.fillText('the tong, the Bengali tea stall', W * .5, H * .74);
      const t = tex(c, { clamp: true }); return { map: t, emissive: '#ffffff', emissiveMap: t, emissiveIntensity: .25, roughness: .5 }; });
    box(f, red, 0, 2.06, .2, 1.62, .04, .5); add(f, new THREE.PlaneGeometry(1.6, .5), sign, 0, 2.36, .46); box(f, red, 0, 2.1, .44, 1.62, .52, .02);
    for (let k = 0; k < 13; k++) add(f, new THREE.ConeGeometry(.02, .07, 8), std(k % 2 ? 'tassel_y' : 'tassel_g', () => ({ color: k % 2 ? '#ffd23f' : '#1e8a4c', roughness: .7 })), -.72 + k * .12, 2.03, .455, Math.PI, 0, 0);
    for (const sx of [-.42, .42]) {   // the cart wheels: rim, spokes, hub, in rickshaw-art colours
      add(f, new THREE.TorusGeometry(.3, .02, 8, 40), std('wheel_rim', () => ({ color: '#1c1c1e', roughness: .5 })), sx, .31, .5);
      for (let k = 0; k < 12; k++) add(f, new THREE.CylinderGeometry(.006, .006, .58, 6), std('wheel_spoke', () => ({ color: '#1e8a4c', roughness: .5 })), sx, .31, .5, 0, 0, k / 12 * Math.PI);
      add(f, new THREE.CylinderGeometry(.05, .05, .05, 16), red, sx, .31, .5, Math.PI / 2, 0, 0);
    }
    const T = .88;   // on the counter: a kettle on a clay stove, clay cups (bhar), biscuit jars, the lantern on its hook
    add(f, lathe([[0, 0], [.12, 0], [.13, .1], [.1, .14], [0, .14]], 28), M.clayRaw, -.45, T, .24);
    const kt = new THREE.Group(); kt.position.set(-.45, T + .14, .24); f.add(kt); const alu = std('alu_kettle', () => ({ color: '#c9ccce', metalness: .85, roughness: .3 }));
    add(kt, lathe([[0, 0], [.09, 0], [.1, .05], [.085, .12], [.04, .15], [0, .155]], 28), alu); add(kt, taperedTube([[.08, .05, 0], [.13, .1, 0], [.16, .14, 0]], .014, .007, 8, 6), alu); add(kt, new THREE.TorusGeometry(.07, .006, 6, 18, Math.PI), std('kettle_handle', () => ({ color: '#1c1c1e', roughness: .5 })), 0, .15, 0);
    for (let k = 0; k < 4; k++) for (let q = 0; q < 3 - Math.floor(k / 2); q++) cup(f, -.05 + k * .08, T + q * .02, .3 - (k % 2) * .08, 'tumbler', M.clayRaw);
    const glassJar = std('jar_glass', () => ({ color: '#dfeae6', roughness: .08, transparent: true, opacity: .4, depthWrite: false }));
    [['#d9a35f', .32], ['#f2e8d6', .45], ['#b8642f', .58]].forEach(([col, dx]) => { add(f, new THREE.CylinderGeometry(.055, .055, .1, 20), std('jar_fill_' + col, () => ({ color: col, roughness: .8 })), dx, T + .05, .2); add(f, new THREE.CylinderGeometry(.06, .06, .16, 20), glassJar, dx, T + .08, .2); add(f, new THREE.CylinderGeometry(.064, .064, .02, 20), red, dx, T + .17, .2); });
    hurricaneLantern(f, .55, 1.98, .38, '#2b5f9e');
    standingCard(f, ['The tong: tea in clay cups', 'For staff, artisans and visiting buyers', 'Electric lantern: no kerosene indoors'], .05, T, .4, 0, { w: .2, h: .1 });
    footprint(22.25, -25.15, 22.85, -23.55);
    for (const [x, z] of [[23.25, -23.75], [23.35, -24.5], [23.2, -25.2]]) woodSliceStool(g, x, z, { r: .16, h: .45 });
  }
  if (want('BEL_UTHAN_CRAFT')) {
    // the Uthan dressed by hand: kula and dala laid over the bamboo canopy (seen from below through the lattice), alpana in rice-paste white
    // around the courtyard, four painted bamboo posts with hurricane-form lanterns (electric), indigo and undyed yarn and small pots hanging
    const g = item('BEL_UTHAN_CRAFT'), CX = 15.65, CZ = -16.08, r = rng(808), list = [];
    for (let i = 0; i < 8; i++) for (let j = 0; j < 8; j++) {
      const x = 13.85 + i * .53 + (r() - .5) * .18, z = -17.9 + j * .53 + (r() - .5) * .18, rad = .26 + r() * .1;
      if (Math.hypot(x - CX, z - CZ) < .45 + rad * .5) continue;
      list.push([x, 2.362 + r() * .045, z, rad, Math.floor(r() * 10) % 4 === 3 ? 2 + Math.floor(r() * 2) : Math.floor(r() * 2), Math.PI / 2 + (r() - .5) * .14, r() * 6.3]);
    }
    trayCloud(g, list);
    const al = canvas(px(640), px(640)), ax = al.getContext('2d'), S = al.width, m = S / 4.2, C = S / 2;   // alpana on the courtyard tiles (4.2 m square), ~7 mm a pixel
    ax.clearRect(0, 0, S, S); ax.strokeStyle = ax.fillStyle = 'rgba(247,242,232,.9)'; ax.lineCap = 'round'; ax.lineWidth = S / 260;
    const petalChain = (half, n, size) => { for (let s = 0; s < 4; s++) for (let k = 0; k <= n; k++) { const t = -half + k * (2 * half / n), [px2, py2] = [[t, -half], [half, t], [-t, half], [-half, -t]][s]; ax.beginPath(); ax.ellipse(C + px2 * m, C + py2 * m, size * m, size * m * .45, s % 2 ? 0 : Math.PI / 2, 0, 7); ax.stroke(); } };
    petalChain(1.98, 40, .045); petalChain(1.24, 26, .035);
    for (let k = 0; k < 4 * 60; k++) { const s = Math.floor(k / 60), t = -1.3 + (k % 60) / 59 * 2.6, [px2, py2] = [[t, -1.32], [1.32, t], [-t, 1.32], [-1.32, -t]][s]; ax.beginPath(); ax.arc(C + px2 * m, C + py2 * m, S / 500, 0, 7); ax.fill(); }
    const lotus = (cx, cy, R) => { for (let k = 0; k < 8; k++) { const a = k / 8 * Math.PI * 2; ax.beginPath(); ax.ellipse(cx + Math.cos(a) * R * .55, cy + Math.sin(a) * R * .55, R * .45, R * .18, a, 0, 7); ax.stroke(); }
      for (let k = 0; k < 8; k++) { const a = (k + .5) / 8 * Math.PI * 2; ax.beginPath(); ax.ellipse(cx + Math.cos(a) * R * .3, cy + Math.sin(a) * R * .3, R * .25, R * .1, a, 0, 7); ax.stroke(); } ax.beginPath(); ax.arc(cx, cy, R * .12, 0, 7); ax.fill(); };
    for (const [sx, sy] of [[-1, -1], [1, -1], [1, 1], [-1, 1]]) lotus(C + sx * 1.62 * m, C + sy * 1.62 * m, .3 * m);
    const paddy = (cx, cy, ang) => { ax.save(); ax.translate(cx, cy); ax.rotate(ang); for (let k = -2; k <= 2; k++) { ax.beginPath(); ax.moveTo(k * .05 * m, .25 * m); ax.quadraticCurveTo(k * .09 * m, 0, k * .16 * m, -.25 * m); ax.stroke();
      for (let q = 0; q < 5; q++) { ax.beginPath(); ax.ellipse(k * (.1 + q * .012) * m + k * .02 * m, (-.05 - q * .045) * m, .012 * m, .022 * m, k * .3, 0, 7); ax.fill(); } } ax.restore(); };
    for (const [px2, py2, a] of [[0, -1.62, 0], [1.62, 0, Math.PI / 2], [0, 1.62, Math.PI], [-1.62, 0, -Math.PI / 2]]) paddy(C + px2 * m, C + py2 * m, a);
    const fishPair = (cx, cy, ang) => { ax.save(); ax.translate(cx, cy); ax.rotate(ang); for (const s of [-1, 1]) { ax.save(); ax.scale(s, 1); ax.beginPath(); ax.ellipse(.17 * m, 0, .12 * m, .045 * m, 0, 0, 7); ax.moveTo(.29 * m, 0); ax.lineTo(.36 * m, -.04 * m); ax.lineTo(.36 * m, .04 * m); ax.closePath(); ax.stroke(); ax.restore(); } ax.restore(); };
    for (const [px2, py2, a] of [[-.8, -1.62, 0], [.8, -1.62, 0], [1.62, -.8, Math.PI / 2], [1.62, .8, Math.PI / 2], [.8, 1.62, 0], [-.8, 1.62, 0], [-1.62, .8, Math.PI / 2], [-1.62, -.8, Math.PI / 2]]) fishPair(C + px2 * m, C + py2 * m, a);
    const alp = new THREE.MeshBasicMaterial({ name: 'bel_alpana', map: tex(al, { clamp: true }), transparent: true, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -2 }); materials.push(alp);
    add(g, new THREE.PlaneGeometry(4.2, 4.2), alp, CX, .0205, CZ, -Math.PI / 2);
    lanternPost(g, CX, -18.32, 0); lanternPost(g, CX, -13.84, Math.PI); lanternPost(g, 13.42, CZ, Math.PI / 2); lanternPost(g, 17.88, CZ, -Math.PI / 2);
    const hank = (x, z, col, k) => { const hg = new THREE.Group(); hg.position.set(x, 2.3, z); hg.rotation.y = k * .7; g.add(hg);
      const m2 = std('hank_' + col, () => { const c = canvas(32, 128), xx = c.getContext('2d'); xx.fillStyle = col; xx.fillRect(0, 0, 32, 128); for (let i = 0; i < 32; i += 2) { xx.fillStyle = `rgba(${i % 4 ? '255,255,255' : '0,0,0'},.12)`; xx.fillRect(i, 0, 1, 128); } return { map: tex(c), roughness: .95 }; });
      const t = add(hg, new THREE.TorusGeometry(.045, .02, 8, 20), m2, 0, -.22, 0); t.scale.set(1, 3.4, .7);
      add(hg, new THREE.CylinderGeometry(.002, .002, .04, 4), std('cord', () => ({ color: '#2a2a2a', roughness: .6 })), 0, .0, 0); };
    ['#1d3254', '#2c4a7a', '#5a7aa8', '#93abc9', '#efe6d2', '#1d3254', '#2c4a7a', '#efe6d2'].forEach((col, k) => hank(13.98, -15.15 - k * .3, col, k));
    ['#2c4a7a', '#efe6d2', '#5a7aa8', '#1d3254', '#93abc9', '#efe6d2'].forEach((col, k) => hank(14.35 + k * .4, -17.82, col, k + 3));
    add(g, new THREE.CylinderGeometry(.016, .016, 2.6, 10), M.bamboo, 13.98, 2.31, -16.2, Math.PI / 2, 0, 0); add(g, new THREE.CylinderGeometry(.016, .016, 2.3, 10), M.bamboo, 15.35, 2.31, -17.82, 0, 0, Math.PI / 2);
    for (const [x, z, y, s] of [[16.95, -14.35, 1.98, 1], [17.2, -14.62, 2.12, .8], [17.42, -14.3, 1.92, .9], [16.85, -14.8, 2.08, .7], [17.35, -14.95, 1.97, .85]]) {   // small pots on cords
      add(g, lathe([[0, 0], [.05, 0], [.08, .05], [.075, .1], [.045, .14], [.05, .16], [.04, .16], [0, .15]].map(([a, b]) => [a * s, b * s]), 24), M.clayRaw, x, y, z);
      add(g, new THREE.CylinderGeometry(.0015, .0015, 2.34 - y - .16 * s, 4), std('cord', () => ({})), x, (2.34 + y + .16 * s) / 2, z); }
    standingCard(g, ['Alpana, kula and dala, natural indigo', 'Rice-paste white, painted by rural women artists', 'Lanterns: electric, no kerosene indoors', 'Option A only'], CX - .55, .47, CZ + .85, .3, { w: .22, h: .13 });
  }
  if (want('BEL_CRAFT_CORNER')) {
    // the solid south wall between the wear rail (x 13.27) and the kantha hanging (x 15.2): a bamboo trellis with gamchha, kantha, a kula and framed
    // work by a rural artist (placeholder), a cane bowl chair on a round sitalpati, a jute pouf and a snake plant in clay
    const g = item('BEL_CRAFT_CORNER'), WZ = -10.8725, tr = new THREE.Group(); tr.position.set(14.22, 0, WZ - .03); tr.rotation.y = Math.PI; g.add(tr);   // local +z faces the room
    const P = [], X0 = -.85, X1 = .85, Y0 = .55, Y1 = 2.35;
    for (const x of [X0, X1]) P.push([new THREE.CylinderGeometry(.02, .02, Y1 - Y0 + .1, 10), x, (Y0 + Y1) / 2, 0]); for (const y of [Y0, Y1]) P.push([new THREE.CylinderGeometry(.02, .02, X1 - X0 + .1, 10), 0, y, 0, 0, 0, Math.PI / 2]);
    for (let k = -6; k <= 6; k++) for (const s of [-1, 1]) {   // diagonal split bamboo, clipped to the frame
      const c0 = k * .3, pts = []; for (let t = -2; t <= 2; t += .01) { const x = c0 + t, y = (Y0 + Y1) / 2 + s * t; if (x > X0 && x < X1 && y > Y0 && y < Y1) pts.push([x, y]); }
      if (pts.length > 2) { const [a, b] = [pts[0], pts[pts.length - 1]], L = Math.hypot(b[0] - a[0], b[1] - a[1]); P.push([new THREE.BoxGeometry(L, .022, .006), (a[0] + b[0]) / 2, (a[1] + b[1]) / 2, s * .004 - .006, 0, 0, Math.atan2(b[1] - a[1], b[0] - a[0])]); } }
    add(tr, merged(P), M.bamboo);
    const gamchha = textileMat('gamchha', (x, w, h) => { x.fillStyle = '#b8352a'; x.fillRect(0, 0, w, h); for (let i = 0; i < 12; i++) { x.fillStyle = i % 3 ? '#1e7a4c' : '#f2ead8'; x.fillRect(i * w / 12, 0, w / 36, h); x.fillRect(0, i * h / 12, w, h / 36); } }, [192, 256]);
    add(tr, new THREE.PlaneGeometry(.36, .78), gamchha, -.52, 1.75, .03); add(tr, new THREE.CylinderGeometry(.012, .012, .44, 8), M.bamboo, -.52, 2.15, .035, 0, 0, Math.PI / 2);
    add(tr, new THREE.PlaneGeometry(.48, .48), textileMat('kantha_corner', (x, w, h) => drawKantha(x, w, h, 31), [256, 256]), .4, 1.85, .03);
    const art = canvas(px(256), px(320)), ar = art.getContext('2d'), AW = art.width, AH = art.height; ar.fillStyle = '#f1e6cf'; ar.fillRect(0, 0, AW, AH);   // placeholder: a commissioned painting goes here
    ar.fillStyle = '#c0392b'; ar.beginPath(); ar.ellipse(AW * .5, AH * .5, AW * .3, AH * .14, 0, 0, 7); ar.fill(); ar.fillStyle = '#1e7a4c'; for (let k = 0; k < 7; k++) { ar.beginPath(); ar.ellipse(AW * (.2 + k * .1), AH * .28, AW * .03, AH * .08, (k - 3) * .2, 0, 7); ar.fill(); }
    ar.fillStyle = '#1d1a18'; ar.font = `500 ${AW * .06}px system-ui, sans-serif`; ar.fillText('Placeholder · rural artist', AW * .1, AH * .88); ar.fillText('to be commissioned', AW * .1, AH * .95);
    box(tr, M.oak, .35, 1.0, .01, .4, .48, .03); add(tr, new THREE.PlaneGeometry(.34, .42), std('corner_art', () => ({ map: tex(art, { clamp: true }), roughness: .8 })), .35, 1.24, .042);
    add(tr, new THREE.CircleGeometry(.24, 36), TRAY[3], -.42, .95, .03); add(tr, new THREE.TorusGeometry(.24, .01, 6, 36), std('tray_rim', () => ({})), -.42, .95, .03);
    const rug = textileMat('pati_round', (x, w, h) => { x.fillStyle = '#d6c393'; x.fillRect(0, 0, w, h); for (const [r0, col] of [[.47, '#8f2f24'], [.42, '#1e5a4c'], [.3, '#8f2f24'], [.12, '#1e5a4c']]) { x.strokeStyle = col; x.lineWidth = w / 40; x.beginPath(); x.arc(w / 2, h / 2, w * r0, 0, 7); x.stroke(); } }, [256, 256]);
    add(g, new THREE.CircleGeometry(.78, 48), rug, 14.25, RUG + .001, -11.85, -Math.PI / 2);
    caneMoonChair(g, 14.55, -11.62, Math.PI + .35); shade('Z07', 14.05, -12.1, 15.05, -11.15, .45);
    const pf = add(g, new THREE.CylinderGeometry(.22, .22, .38, 28), juteBraid, 13.72, .19, -12.12); void pf; footprint(13.5, -12.34, 13.94, -11.9); shade('Z07', 13.5, -12.34, 13.94, -11.9, .35);
    const sp = new THREE.Group(); sp.position.set(13.55, 0, -11.12); g.add(sp); add(sp, lathe([[0, .005], [.1, 0], [.13, .2], [.14, .24], [.12, .24], [0, .22]], 28), M.clayRaw);
    for (let k = 0; k < 11; k++) { const a = k * 2.4, l = .45 + (k % 4) * .1, geo = new THREE.ConeGeometry(.03, l, 4, 1); geo.translate(0, l / 2, 0); geo.scale(1, 1, .25);
      const leaf = add(sp, geo, std('snake_plant', () => ({ color: '#3f6b3a', roughness: .5 })), Math.cos(a) * .04, .22, Math.sin(a) * .04); leaf.rotation.set(Math.sin(a) * .15, -a, Math.cos(a) * .15); }
    footprint(13.4, -11.27, 13.7, -10.97);
    standingCard(g, ['Craft corner', 'Gamchha, kantha, kula and a rural painting', 'Cane, sitalpati and jute by named makers', 'Option A only'], 13.95, 0, -12.55, Math.PI + .5, { w: .2, h: .12 });
  }
  if (want('BEL_CRAFT_SHELF')) {
    // a low bamboo shelf on the solid lower part of the west wall (glass above 1.22 m), between the Marma stand and the remake sacks: painted pots in
    // the shokher hari tradition of Rajshahi, tepa putul clay dolls, a dholak and a khol; a polo (bamboo fish trap) beside it. Makers to be identified
    const g = item('BEL_CRAFT_SHELF'), sh = new THREE.Group(); sh.position.set(9.56, 0, -18.32); sh.rotation.y = Math.PI / 2; g.add(sh);   // local +z: into the room
    const P = []; for (const x of [-.73, .73]) for (const z of [-.16, .16]) P.push([new THREE.CylinderGeometry(.02, .02, 1.08, 10), x, .54, z]);
    for (const y of [.06, .5, .94]) for (let k = 0; k < 6; k++) P.push([new THREE.BoxGeometry(1.5, .016, .05), 0, y, -.15 + k * .06]);
    add(sh, merged(P), M.bamboo);
    shokherHari(sh, -.5, .952, 0, { h: .34, seed: 1 }); shokherHari(sh, .02, .952, .02, { h: .28, seed: 2 }); shokherHari(sh, .45, .952, -.01, { h: .31, seed: 3 });
    for (let k = 0; k < 5; k++) tepaPutul(sh, -.62 + k * .13, .508, (k % 2) * .05, k + 1);
    shokherHari(sh, .4, .508, 0, { h: .2, seed: 4 });
    drum(sh, 'dholak', -.35, .068, 0, 0); drum(sh, 'khol', .35, .068, 0, 0);
    standingCard(sh, ['Painted clay and drums', 'Shokher hari (Rajshahi), tepa putul,', 'a dholak and a khol', 'Makers to be identified and credited'], .62, .508, .12, 0, { w: .19, h: .11 });
    footprint(9.35, -19.1, 9.77, -17.54); shade('Z07', 9.35, -19.1, 9.77, -17.54, .4);
    const PP = []; for (let k = 0; k < 18; k++) { const a = k / 18 * Math.PI * 2, A = new THREE.Vector3(Math.cos(a) * .3, 0, Math.sin(a) * .3), Bv = new THREE.Vector3(Math.cos(a) * .1, .5, Math.sin(a) * .1), d = Bv.clone().sub(A);
      const geo = new THREE.CylinderGeometry(.006, .006, d.length(), 5); geo.applyQuaternion(new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize())); geo.translate((A.x + Bv.x) / 2, (A.y + Bv.y) / 2, (A.z + Bv.z) / 2); PP.push([geo]); }
    for (const [y, rr] of [[.02, .3], [.25, .2], [.48, .105]]) PP.push([new THREE.TorusGeometry(rr, .008, 6, 28), 0, y, 0, Math.PI / 2]);
    const polo = new THREE.Group(); polo.position.set(10.1, 0, -18.95); g.add(polo); add(polo, merged(PP), M.bamboo); footprint(9.78, -19.27, 10.42, -18.63);
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
  for (const root of [group, overhead]) root.traverse(o => { if (o.isMesh) { o.castShadow = false; o.receiveShadow = false; o.userData.conceptLayer = true; } });
  const sources = new Set(), pixels = textures.reduce((s, t) => sources.has(t.source) ? s : (sources.add(t.source), s + (t.image?.width || 0) * (t.image?.height || 0)), 0);   // clones share their source's GPU memory
  const stats = { items: items.length, meshes: 0, instancedLeaves: 0, textures: textures.length, textureMB: Math.round(pixels * 4 * 1.33 / 1e5) / 10 };
  for (const root of [group, overhead]) root.traverse(o => { if (o.isInstancedMesh) stats.instancedLeaves += o.count; else if (o.isMesh) stats.meshes++; });
  function blocksMovement(x, z, radius = .15) { return footprints.some(([x0, z0, x1, z1]) => x > x0 - radius && x < x1 + radius && z > z0 - radius && z < z1 + radius); }
  return {
    group, overhead, stats, items: items.map(i => ({ id: i.id, zone: i.zone, note: i.note })), footprints,
    textures: () => textures, blocksMovement,
    dispose() { geometries.forEach(g => g.dispose()); materials.forEach(m => m.dispose()); textures.forEach(t => t.dispose()); },
  };
}
