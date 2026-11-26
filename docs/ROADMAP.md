# Roadmap

Cyberdeck OS is pre-alpha. Milestone 1 has an AMD64 live-build tree, a GitHub Actions workflow, and a built full hybrid ISO. What that image actually did under QEMU is in [build/amd64/README.md](../build/amd64/README.md). Checked items are done in the docs or in that image. Unchecked items are not accepted yet.

The product requirements are in [SPEC.md](SPEC.md).

## Milestone 0 — Planning baseline

- [x] Locked spec in `docs/SPEC.md`
- [x] This checklist
- [x] How-To outline and chapter stubs in `docs/guide/`
- [x] Directory skeleton with a README in each future work area
- [x] Contributing guide, code of conduct, security policy, issue templates, pull request template
- [x] Funding links (Cash App and Venmo only)
- [x] `.gitignore` for live-build and image output
- [x] Homestead themes, Welcome, Field Dashboard, offline maps, and release codenames recorded in the spec
- [ ] Maintainer pass over the spec before any build config is added

## Milestone 1 — AMD64 live and installer ISO

The first image. A `full` hybrid ISO has been built. `build/amd64/README.md` records what QEMU actually showed, including Plasma, Calamares, and Snapper rollback. Acceptance for the milestone is still an ISO that boots to Plasma, runs Nomad, and installs with Calamares.

- [x] live-build configuration under `build/amd64/` (`ci` profile for the boot test and GitHub Actions, `full` profile for the rest of the Debian packages in the spec)
- [ ] Package lists under `packages/` for the baseline in the spec
- [x] Backported kernel selected, pinned, and named in `docs/SPEC.md`
- [ ] KDE Plasma on Wayland
- [ ] Firefox ESR, Chromium as a Flatpak, full media codecs, VLC, Jellyfin client, LibreOffice
- [ ] Flatpak with the Flathub remote
- [ ] `firmware-linux-nonfree` and common Wi-Fi, Bluetooth, and GPU firmware
- [ ] Mesa and Vulkan
- [ ] `meshtasticd` and Meshtastic web
- [ ] GQRX, WSJT-X, Fldigi, and CHIRP
- [x] Host firewall enabled by default, and the chosen implementation recorded in the spec
- [ ] NVIDIA proprietary driver included and enabled when a GPU is detected
- [ ] In-kernel AMD and Intel NPU support via the newer kernel
- [ ] Calamares launched from a desktop icon named Install Cyberdeck OS
- [ ] Erase disk, install alongside, and manual partitioning
- [ ] Optional full-disk encryption
- [ ] GPT on the install target, including disks larger than 2 TB, with one Btrfs root after the EFI System Partition
- [ ] Install target of at least 256 GB enforced or clearly warned
- [ ] Snapshot before every update, and rollback from the boot menu (Snapper and grub-btrfs style)
- [ ] Welcome app: theme, `/library` drive, Wi-Fi (skippable), ROCm or CUDA when hardware is present (skippable), account password, then Project Nomad and its containers
- [ ] `/library` on the boot drive or on another drive, UUID mount, Docker ordered after that mount
- [ ] Nomad admin on port 8080, Open WebUI on port 3000, Ollama bound to localhost port 11434
- [ ] Offline package cache stored on `/library`
- [ ] Low-power/solar mode toggle
- [ ] Daybreak (light) and Nightwatch (dark), each with its own homestead wallpaper, boot splash, and login screen
- [ ] Automatic Daybreak/Nightwatch switching at sunrise and sunset, by location or by set times
- [ ] Red night-vision mode (red-only screen filter)
- [ ] High-contrast sunlight mode
- [ ] Field Dashboard Plasma widget: add, remove, rearrange, and resize tiles, with per-tile settings
- [ ] Dashboard tiles for internal battery, multiple BLE batteries, multiple BLE solar controllers, drive space, Nomad status, Meshtastic node count, and GPS time
- [ ] Driver model so a new BLE battery or charge controller is a new plugin. First controller drivers: Victron SmartSolar BLE, Renogy BT-1, Renogy BT-2, EPEver
- [ ] Offline OpenStreetMap viewer, tiles stored under `/library/maps`
- [ ] GitHub Actions workflow that builds this ISO
- [ ] GitHub Release with the ISO and a SHA256 checksum
- [ ] SourceForge mirror when the file is larger than 2 GB
- [ ] Theme art hooks. Final Daybreak and Nightwatch splash, wallpaper, login art, and the shared logo when the artwork exists

## Milestone 2 — Generic ARM64 UEFI image

One image for ARM64 laptops, desktops, and boards that boot UEFI. Same desktop and installer behavior as milestone 1, adapted to UEFI ARM64. This image is not a phone image and it is not the Raspberry Pi 5 image.

- [ ] live-build (or the equivalent image config) under `build/arm64/`
- [ ] Boot to KDE Plasma on Wayland
- [ ] Calamares install path, GPT, Btrfs root, snapshots, and rollback
- [ ] Welcome, themes, Field Dashboard, and offline maps carried over from milestone 1
- [ ] GitHub Release with SHA256, and a SourceForge mirror when the file is larger than 2 GB

## Milestone 3 — First phone or tablet image

One device from this set: PinePhone Pro, Librem 5, PineTab2. Plasma Mobile. Use postmarketOS device support where it fits.

- [ ] Device chosen and named in `docs/SPEC.md` and in `devices/<device>/`
- [ ] Image boots to Plasma Mobile on that device
- [ ] Nomad and `/library` behavior adapted to that device's storage
- [ ] Boot-menu rollback path documented for that device's bootloader
- [ ] GitHub Release with SHA256, and a SourceForge mirror when the file is larger than 2 GB

## Milestone 4 — Remaining device images

- [ ] The two handhelds not built in milestone 3
- [ ] Raspberry Pi 5 image, KDE Plasma on Wayland, under `devices/raspberry-pi-5/`
- [ ] Each image released with a SHA256 checksum, and a SourceForge mirror when the file is larger than 2 GB

## Spec items that span milestones

These are part of the spec. They land with the earliest milestone that can carry them, and they apply to later images.

- [ ] How-To guide written in `docs/guide/`
- [ ] Guide exported to PDF, Kiwix ZIM, and ODT, and included for offline reading
- [ ] Cyberdeck Control Panel (update, repair, backup, drive health, move `/library`, restart Nomad, theme and display modes, support-the-creator link)
- [ ] Final Daybreak and Nightwatch artwork, plus the shared logo, in `branding/`
- [ ] Release 1.0 named Axe. Later numbered releases take the next homestead-tool codename

## Explicitly later

- [ ] GitHub Sponsors, only after Richard Colbert enrolls. Until then, funding stays on the custom links in `.github/FUNDING.yml`.
