"""After a deploy of the proposal route, check the live Worker against the release commit:
- /stage2-concept/health names the commit and the route; /realistic/health and the original tour's /, /app.js and /health are unchanged;
- /bengal-earth-lab/ (and below) and /stage2-concept without a slash answer 307 to /stage2-concept/;
- the page, its bundle, its config and every stop image (with its thumbnail and any 3D view) match the commit's files byte for byte,
  with the right content type and the x-bel-source header;
- refusals: an unknown file type is 404 and a POST is 405.
python3 -I verify_bel_live.py SOURCE_COMMIT [--out FILE]   (run from anywhere inside the repository)"""
import argparse, hashlib, json, subprocess, time, urllib.error, urllib.request

SITE = 'https://stage2-office-virtual-tour.imranahmedjh611.workers.dev'
A = 'GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/'
GUARD = {'/': 'ff75beb54b3134b3e1eee7d29d0f6016ed1bf5895777c715f3815ebe3dcd2675',
         '/app.js': 'c6af8144c56302bf92a975179d847b89c6e4eac63068ecc16a96c7c0c02e9bc4',
         '/health': '5118ed4955892545f48d6edf7fee295fdd0e8963fe1c7704041534fc04de378b'}
REALISTIC = 'd5939f9ef3928340908459efc440259df0d34b6d'
p = argparse.ArgumentParser(); p.add_argument('commit'); p.add_argument('--out'); a = p.parse_args()


class Keep(urllib.request.HTTPRedirectHandler):   # report redirects instead of following them
    def redirect_request(self, *args, **kw): return None


plain, keep = urllib.request.build_opener(), urllib.request.build_opener(Keep)


def get(path, method='GET', follow=True):
    req = urllib.request.Request(SITE + path, method=method, headers={'User-Agent': 'Mozilla/5.0', 'Cache-Control': 'no-cache'})
    try:
        r = (plain if follow else keep).open(req, timeout=120); return r.status, {k.lower(): v for k, v in r.headers.items()}, r.read()
    except urllib.error.HTTPError as e:
        return e.code, {k.lower(): v for k, v in e.headers.items()}, e.read()


def blob(path):
    return subprocess.run(['git', 'show', f'{a.commit}:{A}{path}'], capture_output=True, check=True).stdout


sha = lambda b: hashlib.sha256(b).hexdigest()
R = {'site': SITE, 'commit': a.commit, 'time_utc': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()), 'checks': [], 'failed': []}


def check(name, ok, detail=''):
    R['checks'].append({'check': name, 'ok': bool(ok), 'detail': detail})
    if not ok: R['failed'].append(name)


s, h, b = get('/stage2-concept/health')
health = json.loads(b or b'{}') if s == 200 else {}
check('/stage2-concept/health', s == 200 and health.get('source') == a.commit and health.get('route') == '/stage2-concept', f'{s} {health}')
s, h, b = get('/realistic/health')
check('/realistic/health unchanged', s == 200 and json.loads(b).get('source') == REALISTIC, f'{s}')
for path, want in GUARD.items():
    s, h, b = get(path); check(f'{path} unchanged', s == 200 and sha(b) == want, f'{s} {sha(b)[:8]}')
for path, to in (('/bengal-earth-lab/', '/stage2-concept/'), ('/bengal-earth-lab/app.js', '/stage2-concept/app.js'), ('/stage2-concept', '/stage2-concept/')):
    s, h, b = get(path, follow=False); check(f'{path} redirects', s == 307 and h.get('location', '').endswith(to), f"{s} {h.get('location')}")
cfg = json.loads(blob('viewer/dist-bel/release-config.json'))
files = [('', 'viewer/dist-bel/index.html', 'text/html'), ('app.js', 'viewer/dist-bel/app.js', 'text/javascript'), ('release-config.json', 'viewer/dist-bel/release-config.json', 'application/json')]
for v in cfg.get('conceptStills', {}).values():
    for key in ('src', 'thumb', 'model'):
        if isinstance(v, dict) and v.get(key): files.append((v[key], v[key], 'image/jpeg'))
for rel, path, ctype in files:
    s, h, b = get('/stage2-concept/' + rel)
    ok = s == 200 and h.get('content-type', '').startswith(ctype) and h.get('x-bel-source') == a.commit and sha(b) == sha(blob(path))
    check('/stage2-concept/' + rel, ok, f"{s} {h.get('content-type')} {len(b)} bytes")
s, h, b = get('/stage2-concept/x.exe'); check('unknown type is 404', s == 404, str(s))
s, h, b = get('/stage2-concept/app.js', method='POST'); check('POST is 405', s == 405, str(s))
R['files_checked'] = len(files); R['passed'] = not R['failed']
if a.out: open(a.out, 'w').write(json.dumps(R, indent=2) + '\n')
print(json.dumps({'passed': R['passed'], 'checks': len(R['checks']), 'files': len(files), 'failed': R['failed'][:10]}))
