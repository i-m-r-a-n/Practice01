"""Download native 2K maps from the same CC0 providers as the approved model.

Never writes to the approved assets directory. No resizing or upscaling.
ZIP downloads are cached outside the repository; only selected RGB maps persist.
"""
import argparse, hashlib, io, json, pathlib, tempfile, urllib.request, zipfile
from PIL import Image

ROOT=pathlib.Path(__file__).resolve().parent/'pbr2k'
PH_SETS={'white_oak_veneer','natural_walnut_veneer','herringbone_parquet','laminate_floor_02','leather_white','smooth_concrete_floor'}
ACG_SETS={'Terrazzo019M','Fabric030','Fabric034','Tiles040','Tiles043'}
ROLE_SUFFIX={'basecolor':'diff','normal':'nor_gl','roughness':'rough'}

def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Office-realism-source-audit/1.0'}),timeout=60) as response:
        assert response.status==200
        return response.read(),response.url

def store(name,role,filename,data,source,resolved):
    path=ROOT/'source'/name/filename
    with Image.open(io.BytesIO(data)) as image:
        size=list(image.size); mode=image.mode
    assert size==[2048,2048], f'{filename}: source was not native 2048 square: {size}'
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    return {'set':name,'role':role,'file':str(path.relative_to(ROOT)), 'source':source,'resolvedSource':resolved,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'pixels':size,'mode':mode,'upscaled':False,'normalConvention':'OpenGL +Y' if role=='normal' else None}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('sets',nargs='+',choices=sorted(PH_SETS|ACG_SETS));args=parser.parse_args()
    ROOT.mkdir(parents=True,exist_ok=True)
    manifest_path=ROOT/'sources.json'
    records=json.loads(manifest_path.read_text()) if manifest_path.exists() else []
    for name in args.sets:
        records=[r for r in records if r['set']!=name]
        maps=[]
        if name in PH_SETS:
            for role,suffix in ROLE_SUFFIX.items():
                filename=f'{name}_{suffix}_2k.jpg';url=f'https://dl.polyhaven.org/file/ph-assets/Textures/jpg/2k/{name}/{filename}'
                data,resolved=fetch(url);maps.append(store(name,role,filename,data,url,resolved))
            licence='https://polyhaven.com/license';asset='https://polyhaven.com/a/'+name
        else:
            api='https://ambientcg.com/api/v2/full_json?include=downloadData&id='+name
            metadata,_=fetch(api);(ROOT/(name+'-provider.json')).write_bytes(metadata)
            data=json.loads(metadata)['foundAssets'][0]
            downloads=data['downloadFolders']['default']['downloadFiletypeCategories']['zip']['downloads']
            url=next(d['downloadLink'] for d in downloads if d['attribute']=='2K-JPG')
            archive,resolved=fetch(url)
            with zipfile.ZipFile(io.BytesIO(archive)) as z:
                for role,suffix in [('basecolor','Color'),('normal','NormalGL'),('roughness','Roughness')]:
                    filename=f'{name}_2K-JPG_{suffix}.jpg'
                    maps.append(store(name,role,filename,z.read(filename),url,resolved))
            licence='https://docs.ambientcg.com/license/';asset=data['shortLink']
        for record in maps:record.update(licence='CC0-1.0',licenceURL=licence,assetURL=asset)
        records.extend(maps);manifest_path.write_text(json.dumps(records,indent=2)+'\n')
        print(json.dumps({'set':name,'maps':len(maps),'bytes':sum(r['bytes'] for r in maps),'sourcePixels':[2048,2048]}),flush=True)

if __name__=='__main__':main()
