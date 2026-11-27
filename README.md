# Cyberdeck OS

Cyberdeck OS is a lean, open-source Linux distribution for cyberdecks. Richard Colbert, a disabled Navy veteran ([@VeteranPrepper](https://x.com/VeteranPrepper) on X, [@Disabled_Vet_72](https://www.youtube.com/@Disabled_Vet_72) on YouTube), is building it for anyone who wants a deck that can carry an offline library.

The system is a Debian 13 live and installable OS. Its job is to run Project Nomad, an offline knowledge server made of Docker apps (Kiwix, Jellyfin, Open WebUI with Ollama, Meshtastic Web, and the rest of the Nomad set), and nothing extra. Anything beyond the baseline in the spec is installed from the terminal, from Nomad, or from Flatpak. Welcome can also install ROCm or CUDA when that hardware is present. Those two stacks are not part of the image. The OS is free to use. Donations are welcome and never required.

**Status: planning / pre-alpha**

There is no numbered release yet. The AMD64 live and installer image builds from this repository with Debian live-build. See [Build the AMD64 image](#build-the-amd64-image). Other architectures are still reserved directories.

The full locked spec is in [docs/SPEC.md](docs/SPEC.md). The milestone checklist is in [docs/ROADMAP.md](docs/ROADMAP.md).

## Features

- Debian 13 base with a newer backported kernel, so newer hardware (including the AMD XDNA NPU on Ryzen AI HX370) can work.
- AMD64 and ARM64 only. One generic ARM64 UEFI image for laptops, desktops, and boards, plus separate images for phones, tablets, and the Raspberry Pi 5.
- KDE Plasma on Wayland. Plasma Mobile on phones and tablets.
- Live boot from USB, SD, or similar media into the full desktop, with Nomad usable in that session.
- An **Install Cyberdeck OS** desktop icon that launches Calamares, with erase-disk, install-alongside, and manual partitioning. Full-disk encryption is optional.
- Erase-disk installs use GPT, including drives larger than 2 TB, with one Btrfs root after the EFI system partition. Install alongside keeps the other operating system and adds a Btrfs root in the free space. Snapshots run before every update, with rollback from the boot menu (Snapper and grub-btrfs style).
- A first-boot Welcome app: choose Daybreak or Nightwatch, pick the `/library` drive, join Wi-Fi, install ROCm or CUDA when the hardware needs it, set a password, then install Project Nomad and its containers.
- Nomad admin stays on port 8080, Open WebUI on port 3000, and Ollama on localhost port 11434.
- Firefox ESR, Google Chrome (from Google's apt repository, installed when online), full media codecs, VLC, a Jellyfin client, LibreOffice, Flatpak with Flathub, firmware, Mesa/Vulkan, Meshtastic tools, and a ham/SDR set (GQRX, WSJT-X, Fldigi, CHIRP).
- A host firewall enabled by default.
- In-kernel AMD and Intel NPU support. The NVIDIA proprietary driver is included and turned on when a matching GPU is detected. ROCm and CUDA are offered from Welcome when that hardware is present, and they are not part of the image.
- An offline package cache on `/library`, a Cyberdeck Control Panel, and a low-power/solar mode toggle.
- Two themes, with working names Daybreak (light) and Nightwatch (dark). Each has its own rural homestead / off-grid wallpaper. Boot splash and login follow the selected theme. The theme can switch automatically at sunrise and sunset, by location or by set times.
- A red night-vision mode (red-only screen filter) and a high-contrast sunlight mode for outdoor screens.
- A Field Dashboard on the desktop, built as a KDE Plasma widget. Tiles can be added, removed, rearranged, and resized, with settings per tile: internal battery, multiple Bluetooth batteries, multiple Bluetooth solar charge controllers, drive space, Nomad status, Meshtastic node count, and GPS time. New BLE batteries and controllers are added as drivers.
- Offline OpenStreetMap maps, with tiles stored on `/library`.
- Custom boot splash, wallpaper, and logo. Artwork is not in the tree yet.
- Release codenames taken from homestead tools. Version 1.0 is Axe.
- A How-To guide, shipped offline as PDF, Kiwix ZIM, and ODT. The guide is outlined and not written yet.

## Supported hardware

Apple Silicon is outside this project. A supported install needs at least 256 GB of storage.

| Hardware | Architecture | Session | Image | Status |
| --- | --- | --- | --- | --- |
| PCs and laptops | AMD64 | KDE Plasma (Wayland) | Live and installer ISO | In progress, Version 1 (Alpha) |
| Generic UEFI laptops, desktops, and boards | ARM64 | KDE Plasma (Wayland) | One generic UEFI image | On hold |
| PinePhone Pro | ARM64 | Plasma Mobile | Per-device image | On hold |
| Librem 5 | ARM64 | Plasma Mobile | Per-device image | On hold |
| PineTab2 | ARM64 | Plasma Mobile | Per-device image | On hold |
| Raspberry Pi 5 | ARM64 | KDE Plasma (Wayland) | Per-device image | On hold |

Phone and tablet images are on hold. The current work is the AMD64 image. Per-device notes live under [devices/](devices/README.md).

## Tested on (hardware)

Reports use the columns in [docs/HARDWARE.md](docs/HARDWARE.md). Add a row by opening a [Hardware test report](https://github.com/venuspcs/cyberdeck-os/issues/new?template=hardware_test_report.md).

| Device | CPU/GPU | Build/version | Live boot | Install | Wi-Fi | Audio | Notes | Tester |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Asus Vivobook S16 (M5606WA) | AMD Ryzen AI 9 HX370, Radeon 890M | Cyberdeck OS Version 1 (Alpha), pre-fix ISO | Works | Works | Drops | Unknown | MT7922 (`mt7921e`) dropped every few minutes on kernel `7.3.4+deb13`. This image turns Wi-Fi powersave off and sets `mt7921e disable_aspm=1`. On a WPA2/WPA3 mixed router such as Starlink, set the connection to WPA2 if SAE drops. Debian branding, wallpaper, manual, and Nomad autorun issues were also found on that ISO | [@VeteranPrepper](https://x.com/VeteranPrepper) |
| QEMU (BIOS and UEFI) | Virtual machine, no GPU | Local full ISO `4d1a64bf8b7652401d24b3a4f1f87afd1f0fa4c85d10ecd91a86fe54462ecdc4` | Works, BIOS and UEFI, Plasma Wayland | Erase install boots to SDDM under UEFI. Snapper snapshots appear in the GRUB menu after an update | n/a | n/a | Calamares opened after the launcher fix was applied in the live session. Install alongside kept an existing ext4 file, then GRUB stopped at a prompt | Project QEMU test |

## Roadmap

1. AMD64 live and installer ISO.
2. Generic ARM64 UEFI image.
3. The first phone or tablet image (PinePhone Pro, Librem 5, or PineTab2).

Further device images, including the Raspberry Pi 5, follow that first handheld image. Finished images will be published on GitHub Releases with SHA256 checksums. Files larger than 2 GB will also be mirrored on SourceForge. Numbered releases take a homestead-tool codename. Version 1.0 is Axe. GitHub Actions builds the AMD64 ISO. The checklist is in [docs/ROADMAP.md](docs/ROADMAP.md).

## Build the AMD64 image

The first image is an AMD64 hybrid ISO built with Debian live-build.

```sh
sudo scripts/build-amd64.sh ci
```

`full` is the image GitHub Actions builds. A live session of that profile was opened under QEMU and the Calamares partition page was screenshotted after the launcher fix was applied in the session. The ISO artifact from the run before that fix does not include it. `sudo scripts/build-amd64.sh ci` is the smaller profile used while bringing the build up. Details and the limits of that test are in [build/amd64/README.md](build/amd64/README.md).

## Repository layout

| Path | What it will hold |
| --- | --- |
| [build/](build/README.md) | live-build configuration, split by architecture |
| [installer/](installer/README.md) | Calamares configuration |
| [firstboot/](firstboot/README.md) | Welcome app, Nomad install, and `/library` drive setup |
| [dashboard/](dashboard/README.md) | Field Dashboard Plasma widget and device drivers |
| [packages/](packages/README.md) | Package lists for the image |
| [devices/](devices/README.md) | Per-device ARM images |
| [control-panel/](control-panel/README.md) | Cyberdeck Control Panel |
| [branding/](branding/README.md) | Daybreak and Nightwatch art, boot splash, login, and logo (assets later) |
| [scripts/](scripts/README.md) | Maintainer scripts, when there is something to automate |
| [docs/](docs/README.md) | Spec, roadmap, and the How-To guide |

Each of those directories currently contains a README and no build files.

## Contributing

The useful work right now is spec review, hardware reports, and writing the How-To. Build scripts, live-build config, and GitHub Actions workflows belong with the milestone that produces a real image.

Read [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md). Security reports go through [SECURITY.md](SECURITY.md).

Issue templates:

- [Bug report](.github/ISSUE_TEMPLATE/bug_report.md)
- [Hardware report](.github/ISSUE_TEMPLATE/hardware_report.md)
- [Feature request](.github/ISSUE_TEMPLATE/feature_request.md)

## License

- Code, build configuration, and scripts: GNU General Public License v3. See [LICENSE](LICENSE).
- Project documentation, including this README, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, the Markdown under `.github/`, and [docs/](docs/README.md): Creative Commons Attribution 4.0 International. See [LICENSE-docs](LICENSE-docs).

## Support the Creator

Cyberdeck OS is free for anyone building a cyberdeck. If you want to support Richard Colbert:

- Cash App: <https://cash.app/$richardcolbert72>
- Venmo: <https://venmo.com/u/Richard-Colbert-17>
- X Money: visit [@VeteranPrepper](https://x.com/VeteranPrepper) on X and tap the $ icon

GitHub Sponsors is not set up yet. The funding links in this repository are the Cash App and Venmo URLs above.
