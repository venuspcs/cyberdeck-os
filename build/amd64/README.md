# build/amd64/

Debian live-build configuration for the AMD64 hybrid ISO (UEFI and BIOS).

```sh
sudo scripts/build-amd64.sh ci
sudo scripts/build-amd64.sh full
```

`ci` is the profile that fits a boot test and a GitHub-hosted runner: KDE Plasma, Calamares, Snapper, grub-btrfs, Docker, ufw, and Firefox ESR. `full` adds the rest of the Debian packages named in the spec (codecs, VLC, LibreOffice, firmware, Mesa/Vulkan, the NVIDIA driver, Flatpak, and the ham/SDR tools).

The backports kernel pin, Calamares settings, and first-boot scripts are copied into the image tree by `auto/config` from `packages/amd64/`, `installer/`, and `firstboot/`.

GitHub Actions (`.github/workflows/build-amd64.yml`) builds the `full` profile on push. A workflow dispatch can select `ci` or `full`. The job uploads the ISO and a SHA256 file. The checksum step writes `SHA256SUMS` as root, because the ISO build does.

`full` installs `meshtasticd` from the Meshtastic OBS repository for Debian 13 and the Jellyfin Desktop Flatpak from Flathub. Daybreak, Nightwatch, the Welcome app, the Control Panel, and the Field Dashboard are stubs. See the TODO files those directories install into `/usr/share/doc/cyberdeck-os/`.

## What was built and booted

The `full` profile produced `cyberdeck-os-amd64-amd64.hybrid.iso`, 3992977408 bytes.

```
4d1a64bf8b7652401d24b3a4f1f87afd1f0fa4c85d10ecd91a86fe54462ecdc4
```

That image contains the backports kernel `7.3.4+deb13-amd64`, `meshtasticd`, and `org.jellyfin.JellyfinDesktop`. QEMU checks on it:

- The live session is KDE Plasma Wayland and shows an **Install Cyberdeck OS** icon. Calamares opens on Xwayland after the branding file includes a `style` map and the desktop launcher starts Calamares with `QT_QPA_PLATFORM=xcb`. The wizard was walked with Alt+N through Welcome, Location (New York), Keyboard (English US), and Partitions.
- On a 20 GiB GPT disk that already has a 4 GiB ext4 partition, the partition page offers **Erase disk** and **Manual partitioning**, labels the disk GPT, and draws the existing `vda1` ext4 next to free space. It does not offer a separate Install alongside radio for that disk.
- A scripted alongside install on a 40 GiB disk left the existing ext4 partition in place (`keep-me` was read back from GRUB) and created an EFI system partition plus a Btrfs root. Snapper's install snapshot was created. The removable GRUB image dropped to a `grub>` prompt instead of the menu.
- `cyberdeck-autoinstall` (erase) wrote a GPT disk that boots under OVMF to the SDDM greeter, Plasma Wayland. Snapper created the install snapshot. After `apt-get install --reinstall ncurses-base`, GRUB's **Cyberdeck OS snapshots** menu listed the install snapshot and the before-apt snapshot.

The completed GitHub Actions build of this tree before the Calamares launcher fix is run [45839014847](https://github.com/venuspcs/cyberdeck-os/actions/runs/45839014847). Its ISO checksum is `fc84c567536f591e944335156e28c34b7eecc6601164663f4e9f19c43a09d010`. A later commit fixes the Calamares branding and launcher; that run is a separate rebuild.

Requirements: [docs/SPEC.md](../../docs/SPEC.md). Milestone: [docs/ROADMAP.md](../../docs/ROADMAP.md), milestone 1.
