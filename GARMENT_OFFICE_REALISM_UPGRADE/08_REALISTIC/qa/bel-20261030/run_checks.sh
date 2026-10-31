#!/bin/bash
# Runs the proposal route's browser checks one after another against a local serve_preview.py (port 8790 by default),
# writes each check's evidence to qa/bel-20261030/<prefix>-<check>/ (screenshots as JPEG) and prints one line per check.
# ./run_checks.sh PREFIX [PORT] [CHECK ...]     checks: stills phone-walk arrows gallery landscape tour-play
HERE=$(cd "$(dirname "$0")" && pwd); PREFIX=$1; PORT=${2:-8790}; shift $(( $# < 2 ? $# : 2 ))
CHECKS=${@:-stills phone-walk arrows gallery landscape tour-play}
URL=http://127.0.0.1:$PORT/stage2-concept/
for c in $CHECKS; do
  out=$HERE/$PREFIX-$c; t0=$(date +%s)
  case $c in
    stills)     python3 -I $HERE/bel_stills_check.py --out $out --url "${URL}?welcome=0" ;;
    phone-walk) python3 -I $HERE/bel_phone_walk_check.py --out $out --url "${URL}?welcome=0" ;;
    arrows)     python3 -I $HERE/bel_arrows_check.py --out $out --url "${URL}?welcome=0" ;;
    gallery)    python3 -I $HERE/bel_gallery_check.py --out $out --url "$URL" ;;
    landscape)  python3 -I $HERE/bel_landscape_check.py --out $out --url "$URL" ;;
    tour-play)  python3 -I $HERE/bel_tour_play.py --out $out --url "${URL}?welcome=0" ;;
  esac > /tmp/check_$c.log 2>&1
  rc=$?
  python3 -I -c "
import sys; from pathlib import Path; from PIL import Image
for f in Path(sys.argv[1]).glob('*.png'): Image.open(f).convert('RGB').save(f.with_suffix('.jpg'), quality=82, optimize=True); f.unlink()
" $out 2>/dev/null
  echo "CHECK $c exit=$rc $(( $(date +%s) - t0 ))s $(tail -n 1 /tmp/check_$c.log | cut -c1-300)"
done
