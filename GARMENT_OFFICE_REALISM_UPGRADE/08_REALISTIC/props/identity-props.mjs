/** Client-identity dressing for the six-room /realistic/ release (Claude sprint 2026-10-28).
 * Self-made geometry and canvas artwork only. No source mesh is read or moved and nothing stands on the floor:
 * every item sits on an existing furniture top or hangs on an existing wall, so walking paths are unchanged.
 * Every value the client has not evidenced is drawn as an explicit "pending" placeholder, never invented.
 * Usage: buildIdentityProps(THREE, { zones: ['Z02', ...], anisotropy: 8 }) -> { group, items, stats, textures, dispose }
 * Coordinates: viewer metres, x east, y up, z south (as office-props-manifest.json). In every item group the
 * visitor-facing side is local +z; `yaw` turns it towards the room.
 */
export const IDENTITY_ITEMS = [
  // Experience Centre counter (ec_counter: x 10.91-20.07, z -6.08..-5.56, top y 0.889; the room is on its -z side)
  { id: 'ID_WATER_POINT', zone: 'Z30', kind: 'water', position: [11.40, 0.889, -5.84], yaw: Math.PI,
    note: 'Water & Wellbeing refill point (concept). Reusable glasses. The water record only ever shows dated laboratory results; all results are pending.' },
  { id: 'ID_COCONUT_STORY', zone: 'Z30', kind: 'coconut', position: [15.60, 0.889, -5.84], yaw: Math.PI,
    note: 'Material story (concept): coconut shell, button blanks, finished buttons on a garment panel. Supplier, origin and test data pending.' },
  { id: 'ID_SAMPLE_CARD_1', zone: 'Z30', kind: 'samplecard', position: [13.46, 0.889, -5.72], yaw: Math.PI },
  { id: 'ID_SAMPLE_CARD_2', zone: 'Z30', kind: 'samplecard', position: [19.45, 0.889, -5.72], yaw: Math.PI },
  // Reception: one craft story on the blank front wall behind the sofa (wall face z 6.27; the room is on its -z side)
  { id: 'ID_JAMDANI_PANEL', zone: 'Z02', kind: 'jamdani', position: [9.65, 1.78, 6.255], yaw: Math.PI,
    note: 'Jamdani-inspired textile panel (design reference, concept). The maker is to be identified and credited.' },
  // MD Office credenza (x 24.94-27.38, z 5.76-6.29, top y 0.762): current development pieces between the existing frame and books
  { id: 'ID_MD_DEVELOPMENT', zone: 'Z12', kind: 'devshelf', position: [26.18, 0.762, 6.00], yaw: Math.PI },
  // Boardroom table centre line (top y 0.749), between the jug, conference phone, cable and remote
  { id: 'ID_BOARD_REVIEW_1', zone: 'Z08', kind: 'reviewtray', position: [16.30, 0.749, -2.845], yaw: 0 },
  { id: 'ID_BOARD_REVIEW_2', zone: 'Z08', kind: 'reviewtray', position: [18.33, 0.749, -2.845], yaw: Math.PI },
];

export function buildIdentityProps(THREE, { zones = null, exclude = [], anisotropy = 4 } = {}) {
  const group = new THREE.Group(); group.name = 'CLIENT_IDENTITY_PROPS';
  const geometries = [], materials = new Map(), textures = [];
  const items = IDENTITY_ITEMS.filter(i => (!zones || zones.includes(i.zone)) && !exclude.includes(i.id));
  const std = (key, props) => { if (!materials.has(key)) materials.set(key, new THREE.MeshStandardMaterial({ name: 'identity_' + key, ...props })); return materials.get(key); };
  const M = {
    oak: std('oak', { color: '#b88e5f', roughness: .62 }), oakDark: std('oakDark', { color: '#7a5a3a', roughness: .6 }),
    chrome: std('chrome', { color: '#c9cdcf', roughness: .18, metalness: .9 }), steel: std('steel', { color: '#9aa0a2', roughness: .35, metalness: .7 }),
    glass: std('glass', { color: '#d6e6e4', roughness: .05, transparent: true, opacity: .35, depthWrite: false, side: THREE.DoubleSide }),
    shell: std('shell', { color: '#4a2f1c', roughness: .55 }), shellIn: std('shellIn', { color: '#a68a63', roughness: .8 }),
    button: std('button', { color: '#5b3b24', roughness: .4 }), linen: std('linen', { color: '#ddd5c4', roughness: .95 }),
    felt: std('felt', { color: '#3f4a44', roughness: .9 }), tray: std('tray', { color: '#a07b52', roughness: .55 }),
  };
  // one self-made woven-thread texture (plain weave, slight slub), tinted per fabric so swatches read as cloth up close
  const weave = (() => {
    const c = document.createElement('canvas'); c.width = c.height = 128; const x = c.getContext('2d');
    x.fillStyle = '#d8d8d8'; x.fillRect(0, 0, 128, 128);
    for (let i = 0; i < 32; i++) for (let j = 0; j < 32; j++) {
      const over = (i + j) % 2 === 0, slub = .9 + .1 * Math.sin(i * 1.7 + j * .9) * Math.cos(j * 2.3);
      const v = Math.round((over ? 236 : 176) * slub); x.fillStyle = `rgb(${v},${v},${v})`;
      if (over) x.fillRect(i * 4, j * 4 + .5, 4, 3); else x.fillRect(i * 4 + .5, j * 4, 3, 4);
    }
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(2, 2); t.anisotropy = anisotropy; textures.push(t); return t;
  })();
  const fabric = ['#7b8a77', '#b9a487', '#56677a', '#a46a4f', '#d9d1c1', '#8e8f6c', '#6a5a72', '#c7b496'].map((c, i) => std('fabric' + i, { color: c, map: weave, roughness: .97 }));
  function canvasMaterial(key, w, h, draw) {
    const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d'), w, h);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = anisotropy; textures.push(t);
    // printed surfaces get a little self-light so they stay legible in the vertex-lit rooms (not a light source)
    return std(key, { map: t, roughness: .88, emissive: '#ffffff', emissiveMap: t, emissiveIntensity: .32 });
  }
  function mesh(parent, geometry, material, x, y, z, rx = 0, ry = 0) {
    geometries.push(geometry); const m = new THREE.Mesh(geometry, material); m.position.set(x, y, z); m.rotation.set(rx, ry, 0);
    m.castShadow = false; m.receiveShadow = false; parent.add(m); return m;
  }
  const box = (p, mat, x, y, z, w, h, d, ry = 0) => mesh(p, new THREE.BoxGeometry(w, h, d), mat, x, y + h / 2, z, 0, ry);   // y = bottom
  const cyl = (p, mat, x, y, z, r, h, seg = 20) => mesh(p, new THREE.CylinderGeometry(r, r, h, seg), mat, x, y + h / 2, z);
  const tumbler = (p, x, z, y = 0) => mesh(p, new THREE.CylinderGeometry(.031, .026, .095, 18, 1, true), M.glass, x, y + .0475, z);
  // a printed card on a small timber foot, leaning back slightly; its face turns `face` radians from local +z towards local +x
  function card(p, mat, x, z, w, h, tilt = .16, face = 0) {
    box(p, M.oakDark, x, 0, z, w + .02, .018, .07, face);
    const nx = Math.sin(face), nz = Math.cos(face), back = .02 + h / 2 * Math.sin(tilt);
    const m = mesh(p, new THREE.PlaneGeometry(w, h), mat, x - nx * back, .018 + h / 2 * Math.cos(tilt), z - nz * back);
    m.rotation.set(-tilt, face, 0, 'YXZ');
    return m;
  }
  const text = (ctx, s, x, y, size, weight = 400, color = '#26302b') => { ctx.fillStyle = color; ctx.font = `${weight} ${size}px Inter, Arial, sans-serif`; ctx.fillText(s, x, y); };
  const paper = (ctx, w, h) => { ctx.fillStyle = '#f4f0e8'; ctx.fillRect(0, 0, w, h); };

  for (const item of items) {
    const g = new THREE.Group(); g.name = item.id; g.position.fromArray(item.position); g.rotation.y = item.yaw || 0;
    g.userData = { identityItem: true, zone: item.zone, note: item.note || '' };
    if (item.kind === 'water') {
      // [clean tumblers]  [refill tap seen in profile: column, spout, nozzle over its drip tray]  [water record sign, used-glass tray]
      box(g, M.tray, -.36, 0, .02, .30, .014, .22);
      for (let i = 0; i < 6; i++) tumbler(g, -.44 + (i % 3) * .08, -.025 + Math.floor(i / 3) * .09, .014);
      box(g, M.steel, -.01, 0, -.02, .17, .012, .13);
      cyl(g, M.steel, .085, 0, -.03, .03, .012);
      cyl(g, M.chrome, .085, .012, -.03, .014, .31);
      box(g, M.chrome, .025, .30, -.03, .135, .02, .022);
      cyl(g, M.chrome, -.035, .262, -.03, .007, .04, 10);
      cyl(g, M.chrome, .085, .25, -.03, .02, .015, 16);
      box(g, M.tray, .30, 0, .11, .18, .014, .13);
      tumbler(g, .28, .11, .014);
      const record = canvasMaterial('watercard', 600, 840, (x, w, h) => {
        paper(x, w, h); x.fillStyle = '#26673d'; x.fillRect(44, 112, 70, 5);
        text(x, 'Our water', 44, 90, 52, 700);
        text(x, 'We know our water source, test it', 44, 160, 23); text(x, 'appropriately and maintain the system.', 44, 192, 23);
        [['Source', 'Deep tube well (client-stated)'], ['Depth', 'Pending: well record'], ['Treatment', 'Pending: set after lab results'],
          ['S1 Well / source', 'Pending: date, lab, standard'], ['S2 After treatment', 'Pending: date, lab, standard'], ['S3 This outlet', 'Pending: date, lab, standard'],
          ['Maintenance log', 'Pending: tank cleaning dates'], ['Groundwater permit', 'Pending (a separate topic)']]
          .forEach(([k, v], i) => { const y = 252 + i * 64; x.fillStyle = '#d5cdbd'; x.fillRect(44, y - 34, w - 88, 2); text(x, k, 44, y, 22, 700); text(x, v, 44, y + 27, 21, 400, '#6b6a60'); });
        x.strokeStyle = '#8a877b'; x.lineWidth = 3; x.strokeRect(w - 164, h - 150, 120, 120);
        ['QR when', 'reports are', 'online'].forEach((s, i) => text(x, s, w - 152, h - 104 + i * 24, 19, 400, '#6b6a60'));
        text(x, 'Concept display: no results yet.', 44, h - 56, 21, 700, '#8a4b2c');
      });
      card(g, record, .33, -.10, .24, .336, .1, .55);
    } else if (item.kind === 'coconut') {
      // shell -> blanks -> finished buttons on a garment panel, on a felt-lined tray, with its story card behind
      box(g, M.tray, 0, 0, .03, .52, .014, .28); box(g, M.felt, 0, .014, .03, .49, .004, .25);
      const top = .018;
      const shellA = mesh(g, new THREE.SphereGeometry(.062, 22, 10, 0, Math.PI * 2, 0, Math.PI / 2), M.shell, -.17, top, .0, Math.PI); shellA.scale.y = .75;
      mesh(g, new THREE.CircleGeometry(.058, 22), M.shellIn, -.17, top + .001, .0, -Math.PI / 2);
      const shellB = mesh(g, new THREE.SphereGeometry(.048, 18, 8, 0, Math.PI * 2, 0, Math.PI / 2), M.shell, -.17, top, .1); shellB.scale.y = .8;
      for (let i = 0; i < 8; i++) cyl(g, M.shellIn, -.04 + (i % 4) * .03, top, -.02 + Math.floor(i / 4) * .045, .011, .005, 16);
      box(g, fabric[4], .15, top, .03, .15, .004, .22);
      for (let i = 0; i < 4; i++) cyl(g, M.button, .15, top + .004, -.045 + i * .05, .009, .004, 16);
      const story = canvasMaterial('coconutcard', 560, 400, (x, w, h) => {
        paper(x, w, h);
        text(x, 'Coconut-shell buttons', 32, 62, 34, 700); text(x, 'Shell → blank → button → garment', 32, 106, 23, 400, '#4b5a52');
        ['Composition, origin, wash and', 'durability tests: pending supplier', 'verification.'].forEach((s, i) => text(x, s, 32, 176 + i * 30, 22));
        ['Natural does not automatically', 'mean lower impact.'].forEach((s, i) => text(x, s, 32, 300 + i * 26, 20, 400, '#6b6a60'));
      });
      card(g, story, 0, -.19, .30, .214, .14, .35);
    } else if (item.kind === 'samplecard') {
      const sample = canvasMaterial('samplecard', 480, 340, (x, w, h) => {
        paper(x, w, h); text(x, 'Sample card', 28, 50, 30, 700);
        [['Composition', 'pending'], ['Construction', 'pending'], ['Weight g/m²', 'pending'], ['Hand feel / use', 'pending'], ['Tests (report no.)', 'pending'], ['Origin', 'awaiting supplier']]
          .forEach(([k, v], i) => { const y = 98 + i * 40; text(x, k, 28, y, 20, 700, '#3c4640'); text(x, v, 250, y, 20, 400, '#8a4b2c'); });
      });
      card(g, sample, 0, 0, .20, .142, .18, .8);
    } else if (item.kind === 'jamdani') {
      // fine muslin ground, sparse woven butis in a half-drop grid, a border band; slim timber frame against the wall (local -z)
      const W = 2.1, H = .72;
      box(g, M.oak, 0, -H / 2 - .03, -.012, W + .06, H + .06, .024);
      const panel = canvasMaterial('jamdani', 2048, 704, (x, w, h) => {
        x.fillStyle = '#f1eadc'; x.fillRect(0, 0, w, h);
        for (let i = 0; i < w; i += 3) { x.fillStyle = i % 6 ? 'rgba(120,110,95,.06)' : 'rgba(255,255,255,.2)'; x.fillRect(i, 0, 1, h); }
        for (let j = 0; j < h; j += 3) { x.fillStyle = j % 6 ? 'rgba(120,110,95,.06)' : 'rgba(255,255,255,.16)'; x.fillRect(0, j, w, 1); }
        // a buti drawn on the weaving grid: each cell is one woven float, as in a hand-loom motif
        const MOTIF = ['....1....', '...111...', '..1.1.1..', '.1112111.', '1.12221.1', '.1112111.', '..1.1.1..', '...111...', '....1....'];
        const ink = { '1': 'rgba(44,68,98,.82)', '2': 'rgba(176,128,58,.9)' };
        const buti = (cx, cy, u) => MOTIF.forEach((row, r) => [...row].forEach((v, c) => { if (ink[v]) { x.fillStyle = ink[v]; x.fillRect(cx + (c - 4.5) * u, cy + (r - 4.5) * u, u - 1, u - 1); } }));
        for (let r = 0; r < 4; r++) for (let c = 0; c < 9; c++) buti(130 + c * 225 + (r % 2) * 112, 92 + r * 128, 7);
        x.fillStyle = 'rgba(44,68,98,.5)'; x.fillRect(0, h - 128, w, 5); x.fillRect(0, h - 34, w, 5);
        for (let c = 0; c < 64; c++) for (let k = 0; k < 5; k++) {           // stepped triangles along the border, alternating thread colours
          x.fillStyle = c % 2 ? 'rgba(176,128,58,.78)' : 'rgba(44,68,98,.72)';
          x.fillRect(8 + c * 32 + k * 3, h - 112 + k * 13, 26 - k * 6, 12);
        }
      });
      mesh(g, new THREE.PlaneGeometry(W, H), panel, 0, 0, .001);
    } else if (item.kind === 'devshelf') {
      // three stacks of folded development samples, and a framed swatch study leaning on the wall (local -z)
      for (let i = 0; i < 3; i++) for (let k = 0; k < 3; k++) box(g, fabric[(i * 3 + k) % 8], -.2 + i * .2, k * .026, .03, .17, .025, .22, (k - 1) * .03);
      box(g, M.oakDark, -.46, 0, -.12, .26, .02, .06);
      const study = canvasMaterial('swatchstudy', 512, 640, (x, w, h) => {
        x.fillStyle = '#efe9dd'; x.fillRect(0, 0, w, h);
        ['#7b8a77', '#b9a487', '#56677a', '#a46a4f', '#8e8f6c', '#6a5a72', '#c7b496', '#d9d1c1', '#5d6b60']
          .forEach((c, i) => { x.fillStyle = c; x.fillRect(48 + (i % 3) * 142, 60 + Math.floor(i / 3) * 150, 118, 118); });
        text(x, 'Development swatch study', 48, 560, 26, 700, '#3c4640'); text(x, 'Concept display', 48, 596, 22, 400, '#6b6a60');
      });
      mesh(g, new THREE.PlaneGeometry(.22, .275), study, -.46, .02 + .1375 * Math.cos(.12), -.13 - .1375 * Math.sin(.12), -.12);
    } else if (item.kind === 'reviewtray') {
      box(g, M.tray, 0, 0, 0, .36, .012, .26); box(g, M.linen, 0, .012, 0, .34, .003, .24);
      for (let i = 0; i < 5; i++) box(g, fabric[(i + (item.yaw ? 3 : 0)) % 8], -.12 + i * .06, .015 + i * .002, 0, .1, .003, .14, (i - 2) * .12);
    }
    group.add(g);
  }
  return {
    group, items: items.map(i => ({ id: i.id, zone: i.zone, kind: i.kind, note: i.note || null })),
    stats: { items: items.length, meshes: geometries.length, textures: textures.length },
    textures: () => textures,
    dispose() { geometries.forEach(g => g.dispose()); materials.forEach(m => m.dispose()); textures.forEach(t => t.dispose()); },
  };
}
