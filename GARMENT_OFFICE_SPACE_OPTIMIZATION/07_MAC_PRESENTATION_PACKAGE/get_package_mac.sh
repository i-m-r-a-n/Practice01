#!/bin/sh
# Downloads the STAGE II presentation package (130 files, 453 MB) into ./STAGE_II_Presentation and checks every SHA-256.
# Mac:  cd ~/Downloads && sh get_package_mac.sh      (fetches manifest.csv from GitHub if it is not next to the script)
cd "$(dirname "$0")" || exit 1
[ -f manifest.csv ] || curl -fsSL -o manifest.csv https://raw.githubusercontent.com/i-m-r-a-n/Practice01/1ba6ff0/GARMENT_OFFICE_SPACE_OPTIMIZATION/07_MAC_PRESENTATION_PACKAGE/manifest.csv || { echo 'Cannot download manifest.csv'; exit 1; }
OUT=STAGE_II_Presentation
tail -n +2 manifest.csv | while IFS=, read -r target size sha url; do
  url=$(printf %s "$url" | tr -d "\r")
  f="$OUT/$target"; mkdir -p "$(dirname "$f")"
  if [ -f "$f" ] && [ "$(shasum -a 256 "$f" | cut -d' ' -f1)" = "$sha" ]; then continue; fi
  curl -fsSL --retry 3 -o "$f" "$url" || echo "FAILED $target"
  [ "$(shasum -a 256 "$f" | cut -d' ' -f1)" = "$sha" ] && echo "ok  $target" || echo "BAD $target"
done
echo "Done. Any BAD or FAILED line above: run the script again."
