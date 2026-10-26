#!/bin/bash
# Checks the delivered model files and rewrites 05_PROJECT_HANDOFF/verification_results.md.
#   verify_all.sh [PROJECT_ROOT]
# 1. the packed .blend is copied ALONE into an empty temp folder and reopened there (self-containment test)
# 2. the .glb is re-imported into an empty Blender session
# 3. verify_geometry.py measures the .blend against the survey values (04_DOCUMENTATION/geometry_verification.*)
set -e
P=${1:-$(cd "$(dirname "$0")/../.." && pwd)}
S=$P/01_EDITABLE_3D/scripts
R=$P/05_PROJECT_HANDOFF/verification_results.md
T=$(mktemp -d)
cp "$P/01_EDITABLE_3D/Final_Office_Interior.blend" "$T/"
{
  echo "# Verification results"
  echo
  echo "Generated $(TZ=Asia/Dhaka date '+%Y-%m-%d %H:%M') Asia/Dhaka by \`01_EDITABLE_3D/scripts/verify_all.sh\` in fresh $(blender --version | head -1) processes."
  echo
  echo "Self-containment test: the .blend was copied alone into an empty temporary folder and reopened there, so every texture it"
  echo "finds must be packed inside the file."
  echo
} > "$R"
blender -b "$T/Final_Office_Interior.blend" --python "$S/verify_files.py" -- blend "$R" > "$T/blend.log" 2>&1
blender -b --factory-startup --python "$S/verify_files.py" -- glb "$P/01_EDITABLE_3D/Final_Office_Interior.glb" "$R" > "$T/glb.log" 2>&1
blender -b "$P/01_EDITABLE_3D/Final_Office_Interior.blend" --python "$S/verify_geometry.py" -- "$P/04_DOCUMENTATION" > "$T/geo.log" 2>&1
N=$(grep -c ",PASS," "$P/04_DOCUMENTATION/geometry_verification.csv" || true)
A=$(($(wc -l < "$P/04_DOCUMENTATION/geometry_verification.csv") - 1))
{
  echo "## Geometry (checkpoint A)"
  echo "- \`verify_geometry.py\` on the delivered .blend: $N of $A measurements match the survey values (\`04_DOCUMENTATION/geometry_verification.md\`)."
  echo
} >> "$R"
rm -rf "$T"
cat "$R"
