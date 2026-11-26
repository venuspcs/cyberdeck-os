# build/amd64/

Debian live-build configuration for the AMD64 hybrid ISO (UEFI and BIOS).

```sh
sudo scripts/build-amd64.sh ci
sudo scripts/build-amd64.sh full
```

`ci` is the profile that fits a boot test and a GitHub-hosted runner: KDE Plasma, Calamares, Snapper, grub-btrfs, Docker, ufw, and Firefox ESR. `full` adds the rest of the Debian packages named in the spec (codecs, VLC, LibreOffice, firmware, Mesa/Vulkan, the NVIDIA driver, Flatpak, and the ham/SDR tools).

The backports kernel pin, Calamares settings, and first-boot scripts are copied into the image tree by `auto/config` from `packages/amd64/`, `installer/`, and `firstboot/`.

GitHub Actions (`.github/workflows/build-amd64.yml`) builds the `ci` profile on push and can build `full` from the workflow dispatch input. The job uploads the ISO and a SHA256 file.

`meshtasticd` and a Jellyfin client are not in Debian 13. Chromium's Flatpak remote is added when Flatpak is installed (`full`). Daybreak, Nightwatch, the Welcome app, the Control Panel, and the Field Dashboard are stubs. See the TODO files those directories install into `/usr/share/doc/cyberdeck-os/`.

## What was built and booted

The `ci` profile produced `cyberdeck-os-amd64-amd64.hybrid.iso` (1.9 GiB).

```
a7043cc5dc1df991b9bf7c0829a7d15eaafadc4d2828ced79dfb23da7e9feced
```

QEMU checks on that ISO:

- UEFI and BIOS both reach a KDE Plasma Wayland live desktop. `loginctl` reported `SESSION=wayland` and the session command was `startplasma-wayland`. The kernel was `7.3.4+deb13-amd64` from trixie-backports.
- The live desktop shows an **Install Cyberdeck OS** icon. A headless start of the Calamares process on that Wayland session did not open a window, so the installer pages were not screenshotted.
- `cyberdeck-autoinstall` wrote a GPT disk: 1 MiB BIOS boot, 512 MiB EFI (vfat), and the rest one Btrfs volume, with `/etc/fstab` mounting those UUIDs. Snapper's `create-config` failed in that run and was logged; GRUB still installed. The disk then booted under OVMF to the SDDM login screen.

The `full` package list is in the repo and was not the image that was booted. `meshtasticd` and a Jellyfin client are not in Debian 13. Daybreak, Nightwatch, Welcome, the Control Panel, and the Field Dashboard are stubs.

Requirements: [docs/SPEC.md](../../docs/SPEC.md). Milestone: [docs/ROADMAP.md](../../docs/ROADMAP.md), milestone 1.
