"""Install the official full OIDN build with its RTLightmap weights locally."""
import argparse,hashlib,json,pathlib,tarfile,urllib.request
URL='https://github.com/RenderKit/oidn/releases/download/v2.3.3/oidn-2.3.3.x86_64.linux.tar.gz'
SHA='3c385230d9e6f63527ba72f2229594dbac5051674219d72e0044b5d0b841796f'
def main():
    p=argparse.ArgumentParser();p.add_argument('--directory',type=pathlib.Path,required=True);a=p.parse_args();a.directory.mkdir(parents=True,exist_ok=True)
    data=urllib.request.urlopen(URL).read();assert hashlib.sha256(data).hexdigest()==SHA
    archive=a.directory/URL.rsplit('/',1)[-1];archive.write_bytes(data)
    with tarfile.open(archive) as f:f.extractall(a.directory,filter='data')
    print(json.dumps({'source':URL,'sha256':SHA,'bytes':len(data),'library':str(a.directory/'oidn-2.3.3.x86_64.linux/lib/libOpenImageDenoise.so')}))
if __name__=='__main__':main()
