"""One bounded sequential bake batch; this does not install a schedule or service."""
import argparse
import hashlib
import shutil
import uuid
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = Path(__file__).with_name('bake_rooms.py')
DEFAULT_OUT = SCRIPT.parent.parent / 'lighting-v2'
WORK = Path('/workspace/office-bake-work')
SOURCE_SHA = 'fa3ed3d58f6d44c3554e3761307841b96115ff7816e4e541c8e6611cb363810d'
SHARED = ['SHELL_WALLS', 'SHELL_STRUCTURE', 'SHELL_FLOOR', 'SHELL_DECK']
KEY_ROOMS = ['Z02', 'Z30', 'Z08', 'Z12', 'Z07', 'Z18']
SPECS = {'SHELL_WALLS': (4096, 1.0), 'Z07': (4096, 1.4),
         'Z30': (2048, 1.3), 'Z18': (2048, 1.5)}


def valid_existing(out, room, size, weight, samples):
    entry = out / (room + '.json')
    if not entry.exists():
        return False
    data = json.loads(entry.read_text())
    bake = data.get('bake', {})
    light = data.get('lightMap', {})
    return (data.get('status') == 'baked-unreviewed'
            and bake.get('source_sha256') == SOURCE_SHA
            and bake.get('target_uv_layer') == 'LightmapUV'
            and not bake.get('smoke_only')
            and light.get('denoiser') == 'OIDN2.3.3 RTLightmap HDR'
            and light.get('size') == size and light.get('samples') == samples
            and bake.get('uv_metrics', {}).get('floor_uv_weight') == weight
            and all((out / (room + suffix)).exists()
                    for suffix in ('.glb', '.exr', '_raw.exr', '.denoise.json')))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rooms', default=','.join(KEY_ROOMS + SHARED))
    parser.add_argument('--samples', type=int, default=None, help='Override samples; otherwise Reception512 and otherrooms256')
    parser.add_argument('--threads', type=int, default=4)
    parser.add_argument('--output-root', type=Path, default=DEFAULT_OUT)
    parser.add_argument('--blend-copy', type=Path, default=WORK / 'approved-copy.blend')
    parser.add_argument('--blender', default='/workspace/tools/blender-5.2.3-linux-x64/blender')
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--export-only', action='store_true')
    parser.add_argument('--stop-file', type=Path, default=WORK / 'STOP_BAKES')
    args = parser.parse_args()
    metadata = json.loads((ROOT / 'GARMENT_OFFICE_WALKTHROUGH_FINAL/07_WEB_TOUR_ASSETS/office_web_metadata.json').read_text())
    all_rooms = [room['zone'] for room in metadata['rooms']]
    rooms = (KEY_ROOMS + SHARED + [room for room in all_rooms if room not in KEY_ROOMS]
             if args.rooms == 'all' else args.rooms.split(','))
    assert len(set(rooms)) == len(rooms), 'Duplicate room in batch'
    assert all(room in all_rooms + SHARED for room in rooms), 'Unknown room'
    args.output_root.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(exist_ok=True)
    for room in rooms:
        size, weight = SPECS.get(room, (2048, 1.0))
        samples = args.samples if args.samples is not None else (512 if room == 'Z02' else 256)
        if args.stop_file.exists():
            print('STOP_FILE_PRESENT', args.stop_file, 'No further room started.', flush=True)
            return
        if args.resume and valid_existing(args.output_root, room, size, weight, samples):
            print('RETAIN_COMPLETED_CANDIDATE', room, flush=True)
            continue
        command = [args.blender, '-b', str(args.blend_copy), '-t', str(args.threads),
                   '--python-exit-code','1','--python', str(SCRIPT), '--', '--room', room, '--size', str(size),
                   '--samples', str(samples), '--shared-shell', '--save-guides', '--floor-uv-weight',
                   str(weight), '--out', str(args.output_root)]
        if args.export_only:
            command.append('--export-only')
        print('PLAN' if args.dry_run else 'START', room, size, samples, weight,
              time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), flush=True)
        if args.dry_run:
            continue
        snapshot = SCRIPT.parent / 'run-snapshots' / (time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()) + '-' + room + '-' + uuid.uuid4().hex[:6])
        snapshot.mkdir(parents=True)
        hashes = {}
        for filename in ('bake_rooms.py', 'denoise_lightmap.py','doorway_repairs.py'):
            target = snapshot / filename
            shutil.copyfile(SCRIPT.with_name(filename), target)
            hashes[filename] = hashlib.sha256(target.read_bytes()).hexdigest()
        command[command.index('--python') + 1] = str(snapshot / 'bake_rooms.py')
        environment = os.environ.copy()
        environment['OFFICE_PROJECT_ROOT'] = str(ROOT)
        run_record = {'capture_method': 'Immutable script copies created before execution',
                      'command': command, 'project_root': str(ROOT), 'script_sha256': hashes,
                      'source_sha256': SOURCE_SHA, 'status': 'running'}
        (snapshot / 'run.json').write_text(json.dumps(run_record, indent=2))
        log = WORK / (room + '-v2.log')
        with log.open('w') as stream:
            result = subprocess.run(command, cwd=ROOT, env=environment, stdout=stream, stderr=subprocess.STDOUT)
        run_record.update(status='completed' if result.returncode == 0 else 'failed', returncode=result.returncode)
        (snapshot / 'run.json').write_text(json.dumps(run_record, indent=2))
        entry = args.output_root / (room + '.json')
        if result.returncode or not entry.exists():
            raise RuntimeError(f'{room} failed with {result.returncode}; see {log}')
        data = json.loads(entry.read_text())
        print('DONE', room, data['status'], data['bake']['total_seconds'], flush=True)
    print('BATCH_COMPLETE', ','.join(rooms), flush=True)


if __name__ == '__main__':
    main()
