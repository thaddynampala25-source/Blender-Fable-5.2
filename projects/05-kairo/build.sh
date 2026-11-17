#!/usr/bin/env bash
# Rebuild Kairo from nothing in the live Blender, one stage per tool call (each stays under
# the 180 s limit). Intermediate files go to work/ (not committed); the result is kairo.blend.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; root="$(cd "$here/../.." && pwd)"
"$here/install_mpfb.sh"
for stage in base face stylise dress clothes hair accessories; do
  echo "== $stage"
  "$root/scripts/bmcp.py" code "$here/$stage.py" | grep -v '^\[' | tail -2
done
