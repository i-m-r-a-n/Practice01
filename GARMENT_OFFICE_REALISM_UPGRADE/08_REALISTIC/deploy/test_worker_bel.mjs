// Verify the /stage2-concept/ proposal Worker before it touches production:
//   1. every original-tour request answers byte-for-byte as the preserved production Worker
//   2. every /realistic/ request answers exactly as the live /realistic/ Worker (same upstream file, status, headers, body)
//   3. the proposal route maps to its own page, bundle and config at its own commit, and its earlier address /bengal-earth-lab/ redirects
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
const routes = ['/', '/index.html', '/app.js', '/model_web.glb', '/model.glb', '/present', '/presentation', '/pitch.mp4', '/tour.mp4', '/presentation.pdf', '/render-book.pdf', '/renders/CAM_01_Reception_A.jpg', '/health', '/not-found', '/stage2-concepts', '/bengal-earth-labs'];
for (const path of routes) for (const method of ['GET', 'HEAD']) await same(original, bel, path, method);
const realistic = ['/realistic', '/realistic/', '/realistic/app.js', '/realistic/release-config.json', '/realistic/health', '/realistic/model_web_baked.glb', '/realistic/lightmaps/Z02.ktx2',
  '/realistic/renders/CAM_01_Reception_A.jpg', '/realistic/renders/CAM_34_Merchandising_Sample_Hub.jpg', '/realistic/viewer/basis_transcoder.wasm', '/realistic/%2e%2e%2fsecret.txt', '/realistic/unknown.xyz'];
for (const path of realistic) await same(live, bel, path);
await same(live, bel, '/realistic/room.glb', 'GET', { Range: 'bytes=0-31' });
await same(live, bel, '/realistic/app.js', 'POST');
// the proposal route
const B = 'GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/';
const commit = fs.readFileSync(belPath, 'utf8').match(/const BEL_COMMIT = '([0-9a-f]{40})'/)[1];
const P = '/stage2-concept';
for (const [from, to] of [[P + '?x=1', P + '/?x=1'], ['/bengal-earth-lab?x=1', P + '/?x=1'], ['/bengal-earth-lab/', P + '/'], ['/bengal-earth-lab/app.js', P + '/app.js'], ['/bengal-earth-lab/health', P + '/health']]) {
  const r = await bel.run(new Request('https://tour.example' + from)); assert.equal(r.status, 307, from); assert.equal(r.headers.get('location'), 'https://tour.example' + to, from); count++;
}
const health = await (await bel.run(new Request('https://tour.example' + P + '/health'))).json(); assert.equal(health.source, commit); assert.equal(health.route, P); count++;
for (const [path, type, target] of [[P + '/', 'text/html', B + 'viewer/dist-bel/index.html'], [P + '/app.js', 'text/javascript', B + 'viewer/dist-bel/app.js'],
  [P + '/release-config.json', 'application/json', B + 'viewer/dist-bel/release-config.json'], [P + '/model_web_baked.glb', 'model/gltf-binary', B + 'revised-model/Optimized_Office_Interior_web_baked.glb'],
  [P + '/lighting-v2/manifest-hybrid.json', 'application/json', B + 'lighting-v2/manifest-hybrid.json'], [P + '/textures/pbr2k/ktx2/Terrazzo019M/basecolor.ktx2', 'image/ktx2', B + 'textures/pbr2k/ktx2/Terrazzo019M/basecolor.ktx2'],
  // the tour-stop images: the owner's AI concept images and the Cycles renders, from the same commit
  [P + '/concept-images/CAM_03_Entrance_Lobby.jpg', 'image/jpeg', B + 'concept-images/CAM_03_Entrance_Lobby.jpg'], [P + '/concept-images/render_CAM_ISO_SE.jpg', 'image/jpeg', B + 'concept-images/render_CAM_ISO_SE.jpg'],
  // the light images page and a 3D model view of an AI image
  [P + '/images.html', 'text/html', B + 'images.html'], [P + '/concept-images/model/render_CAM_03_Entrance_Lobby.jpg', 'image/jpeg', B + 'concept-images/model/render_CAM_03_Entrance_Lobby.jpg']]) {
  const res = await bel.run(new Request('https://tour.example' + path)); assert.equal(res.status, 200, path); assert.ok(res.headers.get('content-type').startsWith(type), path);
  assert.equal(res.headers.get('x-bel-source'), commit); assert.equal(bel.calls.at(-1).url, `https://raw.githubusercontent.com/i-m-r-a-n/Practice01/${commit}/${target}`); count++;
}
assert.equal((await bel.run(new Request('https://tour.example' + P + '/app.js', { method: 'POST' }))).status, 405); count++;
assert.equal((await bel.run(new Request('https://tour.example' + P + '/%2e%2e%2fsecret.txt'))).status, 400); count++;
assert.equal((await bel.run(new Request('https://tour.example' + P + '/x.exe'))).status, 404); count++;
const partial = await bel.run(new Request('https://tour.example' + P + '/model_web_baked.glb', { headers: { Range: 'bytes=0-31' } })); assert.equal(partial.status, 206); assert.equal(bel.calls.at(-1).range, 'bytes=0-31'); count++;
console.log(JSON.stringify({ checks: count, unchanged_original_requests: routes.length * 2, unchanged_realistic_requests: realistic.length + 2, bel_commit: commit, passed: true }));
