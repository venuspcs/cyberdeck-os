#!/bin/sh
# Build the AMD64 hybrid ISO.
# Usage: scripts/build-amd64.sh [ci|full]
set -eu

PROFILE="${1:-${CYBERDECK_PROFILE:-ci}}"
ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
cd "${ROOT}/build/amd64"

export CYBERDECK_PROFILE="${PROFILE}"
chmod +x auto/config auto/build auto/clean config/hooks/normal/*.hook.chroot config/hooks/normal/*.hook.binary

./auto/config
# A chroot left by the other profile does not install this profile's packages.
if [ -f chroot/etc/cyberdeck/profile ] && ! grep -qx "${PROFILE}" chroot/etc/cyberdeck/profile; then
	sudo lb clean noauto
	./auto/config
fi
sudo -E env CYBERDECK_PROFILE="${PROFILE}" lb bootstrap noauto
sudo -E env CYBERDECK_PROFILE="${PROFILE}" lb chroot noauto
# live-build restores sources.list after the chroot hooks. Apply the
# deb822 sources and branding once more so the squashfs keeps them.
if [ -x chroot/usr/sbin/cyberdeck-apply-image ]; then
	sudo chroot chroot /usr/sbin/cyberdeck-apply-image
fi
sudo -E env CYBERDECK_PROFILE="${PROFILE}" lb binary noauto

iso="$(find . -maxdepth 1 -name '*.hybrid.iso' -o -name '*.iso' | head -n 1)"
if [ -z "${iso}" ]; then
	echo "No ISO was produced." >&2
	exit 1
fi
sha256sum "${iso}" | tee SHA256SUMS
ls -lh "${iso}"
