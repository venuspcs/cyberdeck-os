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
# Package lists, overlays, and hooks changed. Drop those stamps so an
# existing chroot installs them. A fresh tree has no stamps yet.
sudo rm -f .build/chroot_package-lists.live \
	.build/chroot_install-packages.live \
	.build/chroot_includes_after_packages \
	.build/chroot_hooks \
	.build/chroot_hacks
sudo -E env CYBERDECK_PROFILE="${PROFILE}" lb bootstrap noauto
sudo -E env CYBERDECK_PROFILE="${PROFILE}" lb chroot noauto
# live-build restores a classic sources.list at the end of the chroot stage.
# binary_chroot copies this tree before it packs the squashfs, so apply first.
if [ -x chroot/usr/sbin/cyberdeck-apply-image ]; then
	sudo chroot chroot /usr/sbin/cyberdeck-apply-image
fi
for f in \
	chroot/usr/lib/os-release \
	chroot/etc/NetworkManager/conf.d/default-wifi-powersave-off.conf \
	chroot/etc/modprobe.d/mt7921e.conf \
	chroot/etc/apt/sources.list.d/debian.sources \
	chroot/etc/apt/sources.list.d/google-chrome.sources \
	chroot/etc/apt/sources.list.d/docker.sources
do
	if [ ! -f "${f}" ]; then
		echo "Missing ${f} after branding apply." >&2
		exit 1
	fi
done
if ! grep -q 'Cyberdeck OS Beta 1 (Plow)' chroot/usr/lib/os-release; then
	echo "os-release is not Cyberdeck OS Beta 1 (Plow)." >&2
	exit 1
fi
if grep -q '^deb ' chroot/etc/apt/sources.list; then
	echo "sources.list still has deb lines." >&2
	exit 1
fi
sudo lb clean noauto --binary
sudo -E env CYBERDECK_PROFILE="${PROFILE}" lb binary noauto

iso="$(find . -maxdepth 1 -name '*.hybrid.iso' -o -name '*.iso' | head -n 1)"
if [ -z "${iso}" ]; then
	echo "No ISO was produced." >&2
	exit 1
fi
sha256sum "${iso}" | tee SHA256SUMS
ls -lh "${iso}"
