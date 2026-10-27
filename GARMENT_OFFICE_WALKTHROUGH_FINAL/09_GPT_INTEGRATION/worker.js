// Stage II interactive tour — audited production Worker release.
// Asset contents remain pinned to Claude's immutable commit.
const CODE = "https://raw.githubusercontent.com/i-m-r-a-n/Practice01/6a65b7d10982563ee7fdb059b791a67126d98ccb/";
const ASSETS = "https://raw.githubusercontent.com/i-m-r-a-n/Practice01/ddf99eee703600ee722f06595708439560373567/";
addEventListener("fetch", (event) => event.respondWith(route(event.request)));
async function route(req) {
  const p = new URL(req.url).pathname;
  let path, type, base = ASSETS;
  if (p === "/" || p === "/index.html") { path = "GARMENT_OFFICE_WALKTHROUGH_FINAL/08_WORKER_READY_TOUR/index.html"; type = "text/html; charset=utf-8"; }
  else if (p === "/app.js") { path = "GARMENT_OFFICE_WALKTHROUGH_FINAL/08_WORKER_READY_TOUR/app.js"; type = "text/javascript; charset=utf-8"; base = CODE; }
  else if (p === "/model_web.glb") { path = "GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/Final_Office_Interior_web_baked.glb"; type = "model/gltf-binary"; }
  else if (p === "/model.glb") { path = "GARMENT_OFFICE_FINAL_PRESENTATION/01_EDITABLE_3D/Final_Office_Interior.glb"; type = "model/gltf-binary"; }
  else if (/^\/renders\/CAM_[A-Za-z0-9_]+\.jpg$/.test(p)) { path = "GARMENT_OFFICE_FINAL_PRESENTATION/02_RENDERED_IMAGES/final/" + p.slice(9); type = "image/jpeg"; }
  else if (p === "/health") { return Response.json({ ok:true, environment:"production", variant:"baked-light", assetCommit:"ddf99eee703600ee722f06595708439560373567", frontendCommit:"6a65b7d10982563ee7fdb059b791a67126d98ccb", expectedModelBytes:19452524 }); }
  else return new Response("Not found", { status:404 });
  const res = await fetch(base+path, { cf:{cacheEverything:true, cacheTtl:1800} });
  if (!res.ok) return new Response("Asset unavailable "+res.status, { status:502 });
  const h = new Headers(res.headers);
  h.set("content-type", type);
  h.set("cache-control", type.startsWith("text/html") ? "no-store" : "public,max-age=900");
  h.set("x-content-type-options","nosniff");
  h.delete("content-security-policy");
  if (type.startsWith("text/html")) {
    h.delete("content-length");
    return new Response((await res.text()).replace('src="./app.js"', 'src="./app.js?v=6a65b7d10982"'),{status:res.status,headers:h});
  }
  return new Response(res.body,{status:res.status,headers:h});
}
