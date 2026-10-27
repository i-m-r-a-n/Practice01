"""Install the official Khronos KTX CLI into an explicit local tools directory."""
import argparse, hashlib, json, pathlib, tarfile, urllib.request

VERSION = '4.4.2'
ARCHIVE = f'KTX-Software-{VERSION}-Linux-x86_64.tar.bz2'
URL = f'https://github.com/KhronosGroup/KTX-Software/releases/download/v{VERSION}/{ARCHIVE}'
SHA256 = 'a8781bad05f9624edbf910b7f258cd0a4ba7d3e63b49ecc0a0ab440bf6a0a245'

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--directory',type=pathlib.Path,required=True)
    args=parser.parse_args()
    args.directory.mkdir(parents=True,exist_ok=True)
    req=urllib.request.Request(URL,headers={'User-Agent':'OfficeRealism-asset-pipeline'})
    data=urllib.request.urlopen(req).read()
    assert hashlib.sha256(data).hexdigest()==SHA256, 'Official CLI archive hash changed'
    archive=args.directory/ARCHIVE
    archive.write_bytes(data)
    with tarfile.open(archive) as source: source.extractall(args.directory,filter='data')
    print(json.dumps({'version':VERSION,'source':URL,'sha256':SHA256,'ktx':str(args.directory/f'KTX-Software-{VERSION}-Linux-x86_64/bin/ktx')}))

if __name__=='__main__':main()
