"""Download the CC0 assets used by the model (Poly Haven + ambientCG, both CC0 1.0) at 1K resolution.
Run once: python3 scripts/fetch_assets.py   (safe to re-run; existing files are kept)."""
import io, json, os, subprocess, zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
TEX, MOD = os.path.join(ROOT, 'textures'), os.path.join(ROOT, 'models')
PH_TEX = ['white_oak_veneer', 'natural_walnut_veneer', 'herringbone_parquet', 'smooth_concrete_floor', 'leather_white', 'laminate_floor_02']
ACG_TEX = ['Tiles043', 'Terrazzo019M', 'Carpet004', 'Carpet003', 'Fabric030', 'Fabric034', 'Fabric036', 'Tiles040']
PH_MOD = ['modern_arm_chair_01', 'mid_century_lounge_chair', 'coffee_table_round_01', 'side_table_01', 'potted_plant_02',
          'potted_plant_04', 'pachira_aquatica_01', 'calathea_orbifolia_01', 'modern_ceiling_lamp_01',
          'ceramic_vase_01', 'modern_wooden_cabinet', 'wall_clock']
LICENSE_LINES = []


def get(url, dst):
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        return
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    subprocess.run(['curl', '-sS', '--fail', '--retry', '3', '--max-time', '180', '-o', dst, url], check=True)


def ph_json(path):
    out = subprocess.run(['curl', '-sS', '--fail', '--retry', '3', '--max-time', '60', 'https://api.polyhaven.com/' + path],
                         check=True, capture_output=True).stdout
    return json.loads(out)


def poly_texture(name):
    files = ph_json('files/' + name)
    out = os.path.join(TEX, name)
    for key, short in (('Diffuse', 'diff'), ('Rough', 'rough'), ('nor_gl', 'nor_gl')):
        if key in files and '1k' in files[key]:
            info = files[key]['1k'].get('jpg') or files[key]['1k'].get('png')
            get(info['url'], os.path.join(out, f'{name}_{short}_1k.' + info['url'].rsplit('.', 1)[1]))
    LICENSE_LINES.append(f'| texture | {name} | Poly Haven | https://polyhaven.com/a/{name} | CC0 1.0 |')


def acg_texture(name):
    out = os.path.join(TEX, name)
    if os.path.isdir(out) and any(f.endswith('.jpg') for f in os.listdir(out)):
        LICENSE_LINES.append(f'| texture | {name} | ambientCG | https://ambientcg.com/view?id={name} | CC0 1.0 |')
        return
    os.makedirs(out, exist_ok=True)
    data = subprocess.run(['curl', '-sS', '--fail', '-L', '--retry', '3', '--max-time', '180',
                           f'https://ambientcg.com/get?file={name}_1K-JPG.zip'], check=True, capture_output=True).stdout
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for n in z.namelist():
            if n.endswith('.jpg') and any(k in n for k in ('_Color', '_Roughness', '_NormalGL', '_Opacity')):
                with open(os.path.join(out, os.path.basename(n)), 'wb') as f:
                    f.write(z.read(n))
    LICENSE_LINES.append(f'| texture | {name} | ambientCG | https://ambientcg.com/view?id={name} | CC0 1.0 |')


def poly_model(name):
    files = ph_json('files/' + name)
    blend = files['blend']['1k']['blend']
    out = os.path.join(MOD, name)
    get(blend['url'], os.path.join(out, os.path.basename(blend['url'])))
    for rel, inc in blend.get('include', {}).items():
        get(inc['url'], os.path.join(out, rel))
    LICENSE_LINES.append(f'| model | {name} | Poly Haven | https://polyhaven.com/a/{name} | CC0 1.0 |')


def convert_pngs():
    """Size optimisation: model textures without real transparency are stored as JPG; the generator remaps paths."""
    import glob
    from PIL import Image
    import numpy as np
    for p in glob.glob(os.path.join(MOD, '*', 'textures', '*.png')):
        im = Image.open(p)
        if im.mode in ('RGBA', 'LA') and np.asarray(im.getchannel('A')).min() < 250:
            continue
        im.convert('RGB').save(p[:-4] + '.jpg', quality=92 if '_nor' in p else 88, optimize=True)
        os.remove(p)


if __name__ == '__main__':
    for n in PH_TEX:
        poly_texture(n); print('tex', n)
    for n in ACG_TEX:
        acg_texture(n); print('tex', n)
    for n in PH_MOD:
        poly_model(n); print('model', n)
    with open(os.path.join(ROOT, 'LICENSES.md'), 'w') as f:
        f.write('# Third-party assets\n\nAll downloaded assets are CC0 1.0 (public domain dedication): free for commercial use, '
                'no attribution required. Sources are listed for traceability.\n\n'
                '| type | asset | source | url | licence |\n|---|---|---|---|---|\n' + '\n'.join(LICENSE_LINES) + '\n\n'
                'Client branding in assets/brand/ is cropped, unmodified, from the client\'s own business card and company profile '
                '(supplied by the client). Not for reuse outside this project.\n')
    convert_pngs()
    print('done')
