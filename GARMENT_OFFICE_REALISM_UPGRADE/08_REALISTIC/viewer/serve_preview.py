"""Local-only routing equivalent for the new Worker subroute; existing tour untouched."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, unquote
import argparse

HERE = Path(__file__).resolve().parent
REALISTIC = HERE.parent
REPO = HERE.parents[2]

class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        name = unquote(urlparse(path).path).removeprefix('/realistic/').lstrip('/')
        if name in ('', 'index.html', 'app.js'):
            return str(HERE / 'dist' / (name or 'index.html'))
        if name in ('model_web.glb', 'model_web_baked.glb'):
            return str(REPO / ('GARMENT_OFFICE_REALISM_UPGRADE/08_REALISTIC/revised-model/Optimized_Office_Interior_web_baked.glb' if name == 'model_web_baked.glb' else 'GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/Final_Office_Interior_web.glb'))
        if name.startswith('renders/') and (REALISTIC / 'revised-model' / name).is_file():
            return str(REALISTIC / 'revised-model' / name)
        if name.startswith('renders/'):
            return str(REPO / 'GARMENT_OFFICE_FINAL_PRESENTATION/02_RENDERED_IMAGES/final' / Path(name).name)
        candidate = (REALISTIC / name).resolve()
        return str(candidate if candidate.is_relative_to(REALISTIC) else HERE / 'missing')

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8783)
    options = parser.parse_args()
    ThreadingHTTPServer(('127.0.0.1', options.port), Handler).serve_forever()
