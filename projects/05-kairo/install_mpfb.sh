#!/usr/bin/env bash
# Download MPFB 2 (checksum-verified, from extensions.blender.org) and install it in the live Blender.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; root="$(cd "$here/../.." && pwd)"
zip="$root/assets/cache/mpfb-2.0.18.zip"
sha=c075b3e9b94b8e5556a5f03f4653602d02ea306de08126e8f55ed6dee28a2dad
mkdir -p "$(dirname "$zip")"
if [ ! -f "$zip" ] || ! echo "$sha  $zip" | sha256sum -c --quiet -; then
  curl -sSL "https://extensions.blender.org/download/sha256:$sha/add-on-mpfb-v2.0.18.zip" -o "$zip"
  echo "$sha  $zip" | sha256sum -c --quiet -
fi
"$root/scripts/bmcp.py" code "$here/install_mpfb.py"
