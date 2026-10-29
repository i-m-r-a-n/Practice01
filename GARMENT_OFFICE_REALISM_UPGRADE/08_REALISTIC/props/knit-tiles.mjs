/** Self-made stitch tiles (grey canvases, light = raised yarn) shared by the knitwear shader (viewer/release-finishes.js)
 * and the knit swatches of the interior layer. Plain canvas drawing, no external art.
 * knitTile(name) -> HTMLCanvasElement; names: jersey, rib, moss, waffle, cable, pointelle, weave
 */
function tile(w, h, draw) { const c = document.createElement('canvas'); c.width = w; c.height = h; const x = c.getContext('2d'); draw(x, w, h); return c; }
const V = (x, v) => { const g = Math.round(255 * v); x.strokeStyle = x.fillStyle = `rgb(${g},${g},${g})`; };
function knitV(x, cx, cy, w, h) {              // one stockinette loop: two legs of a V, dark edge then light core
  for (const [lw, v] of [[w * .34, .5], [w * .2, .98]]) { V(x, v); x.lineWidth = lw; x.lineCap = 'round'; x.beginPath(); x.moveTo(cx - w * .32, cy - h * .42); x.lineTo(cx, cy + h * .38); x.lineTo(cx + w * .32, cy - h * .42); x.stroke(); }
}
function purl(x, cx, cy, w, h) {                // a purl bump: a short horizontal bar
  for (const [lh, v] of [[h * .5, .45], [h * .28, .86]]) { V(x, v); x.lineWidth = lh; x.lineCap = 'round'; x.beginPath(); x.moveTo(cx - w * .34, cy); x.lineTo(cx + w * .34, cy); x.stroke(); }
}
const TILES = {
  jersey: () => tile(128, 128, (x, w, h) => { V(x, .55); x.fillRect(0, 0, w, h); for (let i = 0; i < 4; i++) for (let j = -1; j <= 5; j++) knitV(x, 16 + i * 32, 12.8 + j * 25.6, 32, 25.6); }),
  rib: () => tile(128, 128, (x, w, h) => { V(x, .5); x.fillRect(0, 0, w, h); for (let i = 0; i < 8; i++) for (let j = -1; j <= 5; j++) (i % 4 < 2 ? knitV : purl)(x, 8 + i * 16, 12.8 + j * 25.6, 16, 25.6); }),
  moss: () => tile(128, 128, (x, w, h) => { V(x, .52); x.fillRect(0, 0, w, h); for (let i = 0; i < 8; i++) for (let j = -1; j <= 8; j++) ((i + j) % 2 ? knitV : purl)(x, 8 + i * 16, 8 + j * 16, 16, 16); }),
  waffle: () => tile(128, 128, (x, w, h) => {      // raised cells with soft knit ridges between them (not a printed grid)
    V(x, .74); x.fillRect(0, 0, w, h);
    for (let i = 0; i < 4; i++) for (let j = 0; j < 4; j++) { const g = x.createRadialGradient(i * 32 + 16, j * 32 + 14, 2, i * 32 + 16, j * 32 + 16, 16); g.addColorStop(0, 'rgb(255,255,255)'); g.addColorStop(.7, 'rgb(226,226,226)'); g.addColorStop(1, 'rgb(196,196,196)'); x.fillStyle = g; x.fillRect(i * 32 + 3, j * 32 + 3, 26, 26); }
    for (let j = 0; j < 4; j++) for (let i = 0; i < 8; i++) knitV(x, 8 + i * 16, j * 32 + 1, 16, 8);   // knit rows in the ridges
  }),
  pointelle: () => tile(128, 128, (x, w, h) => { V(x, .55); x.fillRect(0, 0, w, h); for (let i = 0; i < 4; i++) for (let j = -1; j <= 5; j++) knitV(x, 16 + i * 32, 12.8 + j * 25.6, 32, 25.6);
    for (const [cx, cy] of [[32, 32], [96, 96]]) { V(x, .18); x.beginPath(); x.arc(cx, cy, 7, 0, Math.PI * 2); x.fill(); } }),
  cable: () => tile(128, 192, (x, w, h) => {
    V(x, .5); x.fillRect(0, 0, w, h);
    for (const cx of [10, 118]) for (let j = -1; j <= 8; j++) purl(x, cx, 12 + j * 24, 20, 24);
    for (const cx of [28, 100]) for (let j = -1; j <= 8; j++) knitV(x, cx, 12 + j * 24, 16, 24);
    for (const [lw, v] of [[30, .42], [20, .97]]) for (const s of [1, -1]) {   // two strands crossing once per tile
      V(x, v); x.lineWidth = lw; x.lineCap = 'round'; x.beginPath();
      for (let t = -.1; t <= 1.1; t += .02) { const y = t * h, cx2 = 64 + s * 17 * Math.cos(t * Math.PI * 2); t <= -.08 ? x.moveTo(cx2, y) : x.lineTo(cx2, y); }
      x.stroke();
    }
  }),
  weave: () => tile(128, 128, (x, w, h) => {      // handloom plain weave with slubs
    V(x, .78); x.fillRect(0, 0, w, h);
    for (let i = 0; i < 32; i++) for (let j = 0; j < 32; j++) { const over = (i + j) % 2 === 0, s = .9 + .1 * Math.sin(i * 1.7 + j * .9) * Math.cos(j * 2.3); V(x, (over ? .98 : .76) * s); if (over) x.fillRect(i * 4, j * 4 + .5, 4, 3); else x.fillRect(i * 4 + .5, j * 4, 3, 4); }
    for (let k = 0; k < 40; k++) { V(x, .66 + (k % 3) * .14); x.fillRect((k * 37) % w, (k * 53) % h, 10 + (k * 7) % 22, 2); }
  }),
};
const cache = new Map();
export function knitTile(name) { if (!TILES[name]) throw new Error('unknown stitch ' + name); if (!cache.has(name)) cache.set(name, TILES[name]()); return cache.get(name); }
