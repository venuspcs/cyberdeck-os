# packages/

Reserved for the package lists the image build will install.

The lists, once a milestone adds them, will cover the baseline in the spec:

- Debian 13 with the backported kernel
- KDE Plasma (Wayland), and Plasma Mobile for phone and tablet images
- Firefox ESR, full media codecs, VLC, a Jellyfin client, LibreOffice
- Flatpak, with Chromium delivered as a Flatpak and Flathub enabled
- `firmware-linux-nonfree` and common Wi-Fi, Bluetooth, and GPU firmware
- Mesa and Vulkan
- `meshtasticd` and the Meshtastic web client
- GQRX, WSJT-X, Fldigi, and CHIRP
- the host firewall (package chosen in milestone 1)
- the NVIDIA proprietary driver, enabled when a GPU is detected
- Calamares and the snapshot tools (Snapper and grub-btrfs style)
- the Welcome app, the Cyberdeck Control Panel, and the Field Dashboard Plasma widget
- an OpenStreetMap viewer that reads tiles from `/library/maps`

ROCm and CUDA stay off these lists. Welcome offers them as a later install, and they are not part of the image.

**No package list files are in this directory.** An empty or guessed `.list.chroot` would look like a live-build input. Do not add one until the AMD64 config exists and the list matches the spec.

Requirements: [docs/SPEC.md](../docs/SPEC.md), sections 9, 10, 15, and 16.
