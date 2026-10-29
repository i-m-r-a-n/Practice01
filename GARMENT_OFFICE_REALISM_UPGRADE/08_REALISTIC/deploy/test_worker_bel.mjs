// Verify the /bengal-earth-lab/ Worker before it touches production:
//   1. every original-tour request answers byte-for-byte as the preserved production Worker
//   2. every /realistic/ request answers exactly as the live /realistic/ Worker (same upstream file, status, headers, body)
//   3. the proposal route maps to its own page, bundle and config at its own commit
// node test_worker_bel.mjs <live realistic worker.js> <bel worker.js>
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const here = new URL('.', import.meta.url);
function sandbox(source) {
  const calls = [];
  const context = { Response, Request, Headers, URL, console, addEventListener() {}, fetch: async (url, options) => {
    calls.push({ url, method: options.method, range: options.headers.get('Range') });
    return new Response(options.method === 'HEAD' ? null : (url.endsWith('index.html') ? '<script src="./app.js"></script>' : 'fixture-body'), { status: options.headers.has('Range') ? 206 : 200, headers: { 'x-origin': 'fixture', 'content-type': 'application/octet-stream' } });
  } };
  vm.createContext(context); vm.runInContext(source, context);
  return { calls, run: req => context.route(req) };
}
const [livePath, belPath] = process.argv.slice(2);
const original = sandbox(fs.readFileSync(new URL('production-worker-before.js', here), 'utf8'));
const live = sandbox(fs.readFileSync(livePath, 'utf8'));
const bel = sandbox(fs.readFileSync(belPath, 'utf8'));
let count = 0;
const same = async (a, b, path, method = 'GET', headers = {}) => {
  const req = () => new Request('https://tour.example' + path, { method, headers }), na = a.calls.length, nb = b.calls.length;
  const [x, y] = await Promise.all([a.run(req()), b.run(req())]);
  assert.equal(y.status, x.status, path); assert.deepEqual([...y.headers], [...x.headers], path); assert.equal(await y.text(), await x.text(), path);
  assert.deepEqual(b.calls.slice(nb), a.calls.slice(na), path + ' upstream');   // the same upstream fetches (none for redirects and refusals)
  count++;
};
const routes = ['/', '/index.html', '/app.js', '/model_web.glb', '/model.glb', '/present', '/presentation', '/pitch.mp4', '/tour.mp4', '/presentation.pdf', '/render-book.pdf', '/renders/CAM_01_Reception_A.jpg', '/health', '/not-found'];
for (const path of routes) for (const method of ['GET', 'HEAD']) await same(original, bel, path, method);
const realistic = ['/realistic', '/realistic/', '/realistic/app.js', '/realistic/release-config.json', '/realistic/health', '/realistic/model_web_baked.glb', '/realistic/lightmaps/Z02.ktx2',
  '/realistic/renders/CAM_01_Reception_A.jpg', '/realistic/renders/CAM_34_Merchandising_Sample_Hub.jpg', '/realistic/viewer/basis_transcoder.wasm', '/realistic/%2e%2e%2fsecret.txt', '/realistic/unknown.xyz'];
for (const path of realistic) await same(live, bel, path);
await same(live, bel, '/realistic/room.glb', 'GET', { Range: 'bytes=0-31' });
await same(live, bel, '/realistic/app.js', 'POST');
// the proposal route
const B = 'GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/';
const commit = fs.readFileSync(belPath, 'utf8').match(/const BEL_COMMIT = '([0-9a-f]{40})'/)[1];
assert.equal((await bel.run(new Request('https://tour.example/bengal-earth-lab?x=1'))).headers.get('location'), 'https://tour.example/bengal-earth-lab/?x=1'); count++;
const health = await (await bel.run(new Request('https://tour.example/bengal-earth-lab/health'))).json(); assert.equal(health.source, commit); assert.equal(health.route, '/bengal-earth-lab'); count++;
for (const [path, type, target] of [['/bengal-earth-lab/', 'text/html', B + 'viewer/dist-bel/index.html'], ['/bengal-earth-lab/app.js', 'text/javascript', B + 'viewer/dist-bel/app.js'],
  ['/bengal-earth-lab/release-config.json', 'application/json', B + 'viewer/dist-bel/release-config.json'], ['/bengal-earth-lab/model_web_baked.glb', 'model/gltf-binary', B + 'revised-model/Optimized_Office_Interior_web_baked.glb'],
  ['/bengal-earth-lab/lighting-v2/manifest-hybrid.json', 'application/json', B + 'lighting-v2/manifest-hybrid.json'], ['/bengal-earth-lab/textures/pbr2k/ktx2/Terrazzo019M/basecolor.ktx2', 'image/ktx2', B + 'textures/pbr2k/ktx2/Terrazzo019M/basecolor.ktx2']]) {
  const res = await bel.run(new Request('https://tour.example' + path)); assert.equal(res.status, 200, path); assert.ok(res.headers.get('content-type').startsWith(type), path);
  assert.equal(res.headers.get('x-bel-source'), commit); assert.equal(bel.calls.at(-1).url, `https://raw.githubusercontent.com/i-m-r-a-n/Practice01/${commit}/${target}`); count++;
}
assert.equal((await bel.run(new Request('https://tour.example/bengal-earth-lab/app.js', { method: 'POST' }))).status, 405); count++;
assert.equal((await bel.run(new Request('https://tour.example/bengal-earth-lab/%2e%2e%2fsecret.txt'))).status, 400); count++;
assert.equal((await bel.run(new Request('https://tour.example/bengal-earth-lab/x.exe'))).status, 404); count++;
const partial = await bel.run(new Request('https://tour.example/bengal-earth-lab/model_web_baked.glb', { headers: { Range: 'bytes=0-31' } })); assert.equal(partial.status, 206); assert.equal(bel.calls.at(-1).range, 'bytes=0-31'); count++;
console.log(JSON.stringify({ checks: count, unchanged_original_requests: routes.length * 2, unchanged_realistic_requests: realistic.length + 2, bel_commit: commit, passed: true }));
