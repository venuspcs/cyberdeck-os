#!/bin/sh
# Build the AMD64 hybrid ISO.
# Usage: scripts/build-amd64.sh [ci|full]
set -eu

PROFILE="${1:-${CYBERDECK_PROFILE:-ci}}"
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
cd "${ROOT}/build/amd64"

export CYBERDECK_PROFILE="${PROFILE}"
chmod +x auto/config auto/build auto/clean config/hooks/normal/*.hook.chroot

./auto/config
sudo -E env CYBERDECK_PROFILE="${PROFILE}" ./auto/build

iso="$(find . -maxdepth 1 -name '*.hybrid.iso' -o -name '*.iso' | head -n 1)"
if [ -z "${iso}" ]; then
	echo "No ISO was produced." >&2
	exit 1
fi
sha256sum "${iso}" | tee SHA256SUMS
ls -lh "${iso}"
