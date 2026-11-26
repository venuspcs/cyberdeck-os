# Cyberdeck OS specification

**Status: planning / pre-alpha.**

This is the locked product spec for the first images. The repository documents that spec and reserves directories for later work. It does not contain live-build configuration, an installer, package lists, scripts that produce an image, or a GitHub Actions workflow.

Cyberdeck OS is free for anyone building a cyberdeck. Donations are welcome and never required. See the Support the Creator section of the [README](../README.md).

## 1. Purpose

Cyberdeck OS is a lean Debian-based live and installable system. Its job is to run Project Nomad and to avoid being a general-purpose distribution beyond the baseline in this spec.

Project Nomad is an offline knowledge server: a set of Docker applications that includes Kiwix, Jellyfin, Open WebUI with Ollama, Meshtastic Web, and the other apps Nomad ships.

A person using an installed system, or a live session, can still install additional software in three ways:

- the terminal, with Debian packages
- Project Nomad
- Flatpak, with Flathub enabled

## 2. Base system

- Debian 13.
- A newer kernel, backported, in place of the default Debian 13 kernel. One reason is newer accelerators such as the AMD XDNA NPU in the Ryzen AI HX370. The exact package version is chosen when the AMD64 image is built, and then recorded here.
- AMD64 and ARM64 only. Apple Silicon is not a target.

## 3. Architectures and images

| Image | Architecture | Machines | Desktop |
| --- | --- | --- | --- |
| Live and installer ISO | AMD64 | PCs and laptops | KDE Plasma (Wayland) |
| Generic UEFI image | ARM64 | Laptops, desktops, and boards that boot UEFI | KDE Plasma (Wayland) |
| PinePhone Pro | ARM64 | That phone | Plasma Mobile |
| Librem 5 | ARM64 | That phone | Plasma Mobile |
| PineTab2 | ARM64 | That tablet | Plasma Mobile |
| Raspberry Pi 5 | ARM64 | That board | KDE Plasma (Wayland) |

There is one generic ARM64 UEFI image. Phones and tablets get their own images, starting with the PinePhone Pro, the Librem 5, and the PineTab2. Those images lean on postmarketOS device support where it fits. The Raspberry Pi 5 gets its own image as well. It is not the generic UEFI image, and it uses the desktop session, not Plasma Mobile.

Per-device notes and, later, device-specific config belong under [devices/](../devices/README.md).

## 4. Desktop

- KDE Plasma on Wayland for AMD64, for the generic ARM64 UEFI image, and for the Raspberry Pi 5.
- Plasma Mobile for phones and tablets.
- Two built-in themes, Daybreak and Nightwatch, described in section 14.
- A Field Dashboard Plasma widget, described in section 15.

## 5. Live session

The image boots from removable media (USB, SD, or similar) into the full desktop. Project Nomad is usable in that live session.

How the live session carries Nomad (preinstalled data versus the same first-boot path used after install) is decided in the AMD64 milestone. The requirement is the behavior: a live desktop can use Nomad.

## 6. Installer

The installed desktop has an icon named **Install Cyberdeck OS**. It launches Calamares.

Calamares offers:

- erase disk
- install alongside
- manual partitioning

Full-disk encryption is an option in the installer. It is off unless the user turns it on.

The installer is specified for the AMD64 ISO and the generic ARM64 UEFI image. Phone, tablet, and Raspberry Pi 5 images follow the boot process those devices actually support. See the implementer notes at the end of this document.

## 7. Storage

- A supported install target has at least 256 GB of storage.
- Disks are partitioned GPT, including disks larger than 2 TB, so the whole disk is used. An MBR layout is not used for these install targets.
- The root filesystem is one Btrfs partition covering the rest of the disk. The only other partition on that install target is the small EFI System Partition required to boot (see the implementer notes).
- The system takes a snapshot before every update.
- The user can roll back from the boot menu, in the style of Snapper plus grub-btrfs.

## 8. First boot, the Welcome app, and `/library`

The installed system starts a first-boot Welcome app. Welcome is the place that collects the choices below, then installs Project Nomad and its containers.

Welcome asks the user to:

1. Choose a theme: Daybreak or Nightwatch. The same step can turn on automatic day/night switching (section 14).
2. Pick the drive that holds `/library`.
3. Join a Wi-Fi network. This step can be skipped. Downloads wait until a network is available, and the Cyberdeck Control Panel keeps the same offers for later.
4. Install an AI driver when the hardware needs it: a one-click ROCm or CUDA install, then configure Ollama for that driver (section 10). This step can be skipped.
5. Set the account password.

If the user chooses the boot drive for `/library`, Welcome creates a `/library` directory on that drive.

If the user chooses another drive, Welcome offers two choices: format the drive, or use it as-is. Either way it mounts that drive by UUID from `/etc/fstab`, and Docker is configured to start only after `/library` is mounted.

Welcome is the first-boot path on an installed system. The live session requirement stays in section 5.

Service ports:

| Service | Port | Where it listens |
| --- | --- | --- |
| Nomad admin | 8080 | Kept on 8080, as Nomad ships it |
| Open WebUI | 3000 | Kept on 3000, as Nomad ships it |
| Ollama (local AI) | 11434 | Localhost only |

Ollama listens on 127.0.0.1. It is not exposed on the network.

## 9. Software in the image

The baseline image includes:

- Firefox ESR
- Chromium, installed as a Flatpak
- Full media codecs
- VLC
- A Jellyfin client
- LibreOffice
- Flatpak, with the Flathub remote enabled
- `firmware-linux-nonfree`, plus common Wi-Fi, Bluetooth, and GPU firmware
- Mesa and Vulkan
- Meshtastic tools: `meshtasticd` and the Meshtastic web client
- Ham and SDR tools: GQRX, WSJT-X, Fldigi, and CHIRP
- The Field Dashboard (section 15)
- An OpenStreetMap viewer, with map tiles stored under `/library/maps` (section 16)
- A host firewall that is enabled by default

The firewall package (for example nftables directly, firewalld, or ufw) is chosen in the AMD64 milestone and then named in this spec. The requirement for this pass is that a firewall is on in the default system.

Anything outside this list is something the user installs, through the terminal, Nomad, or Flatpak.

## 10. Drivers and compute stacks

- AMD and Intel NPUs use their in-kernel drivers. The backported kernel exists in part so those drivers are present, including AMD XDNA on Ryzen AI HX370.
- The NVIDIA proprietary driver is included in the image and enabled automatically when an NVIDIA GPU is detected.
- ROCm and CUDA are not in the image.
- Welcome offers a one-click ROCm or CUDA install when that hardware is present, then configures Ollama to use it. The same offer stays available from the Cyberdeck Control Panel.

## 11. Offline package cache

An offline package cache and mirror is stored on `/library`, so package installs can be repeated without the network. The tool that fills the mirror is chosen with the AMD64 image and recorded here.

## 12. Cyberdeck Control Panel

A desktop application named Cyberdeck Control Panel provides:

- update
- repair
- backup
- drive health
- move `/library`
- restart Nomad
- theme selection (Daybreak or Nightwatch) and automatic day/night switching
- red night-vision mode and high-contrast sunlight mode
- the ROCm or CUDA install, when Welcome skipped it or the hardware shows up later
- a link to support the creator (the same destinations as the README: Cash App, Venmo, and X Money via @VeteranPrepper)

The panel is the maintenance app. Glanceable field readings live on the Field Dashboard (section 15), not in this panel.

The UI toolkit is chosen when the panel is implemented. This repository does not contain the application yet.

## 13. Power

The system has a low-power/solar mode toggle for battery and solar cyberdecks. The concrete policy (CPU governor, screen power, which services pause) is defined with the control panel work and then added to this spec.

Low-power/solar mode is a power policy. Red night-vision and high-contrast sunlight mode are display modes (section 14). Each one is its own toggle.

## 14. Themes and branding

Cyberdeck OS ships two themes. The names Daybreak and Nightwatch are the working names.

| Theme | Working name | Mode | Wallpaper |
| --- | --- | --- | --- |
| Light | Daybreak | Light colors across the desktop | A rural homestead / off-grid home, unique to this theme |
| Dark | Nightwatch | Dark colors across the desktop | A rural homestead / off-grid home, a different image from Daybreak |

The boot splash and the login screen follow the theme that is in effect. With a theme chosen by hand, they use that theme. With automatic switching on, they use Daybreak or Nightwatch according to the rule below.

The logo is one shared mark. Theme art is the wallpaper, the boot splash, and the login screen. Assets are not in this planning pass. They will land under [branding/](../branding/README.md). Until they exist, the image build uses a documented stand-in only if a file is required for the boot path to succeed, and that stand-in is labeled as temporary.

### Automatic day/night switching

The user can keep one theme, or turn on automatic switching. Automatic mode applies Daybreak at sunrise and Nightwatch at sunset.

The switch time comes from one of two sources, chosen by the user:

- Location. Sunrise and sunset are computed on the machine for a GPS fix, or for coordinates the user enters. The location stays on the machine.
- Set times. The user picks the clock time for the morning switch and the clock time for the evening switch.

Welcome and the Cyberdeck Control Panel both expose this choice.

### Red night-vision mode

A red night-vision mode applies a red-only filter to the screen, for working in the dark without a bright white display. The user turns it on and off. It stays available on top of whichever base theme is active.

### High-contrast sunlight mode

A high-contrast sunlight mode makes the screen readable outdoors. The user turns it on and off. It stays available on top of whichever base theme is active.

## 15. Field Dashboard

The Field Dashboard is a desktop widget built on KDE Plasma widgets. It is a glanceable board for power, storage, and radio status in the field.

The user can add tiles, remove tiles, rearrange them, and resize them. Each tile has its own settings. The layout and those settings are saved for the user and restored at the next login.

On Plasma Mobile, the same widget is included where that shell can place a Plasma widget. A device image records any layout difference in its device directory when that image is built.

### Tiles

| Tile | What it shows | How many |
| --- | --- | --- |
| Internal laptop battery | Charge and state of the machine's own battery | One tile type. It reports that no internal battery is present when the machine has none |
| External battery | Readings from one smart battery over Bluetooth, including a LiFePO4 or other solar battery that exposes a BMS | One tile per battery. Several batteries can be on the dashboard at the same time |
| Solar charge controller | Readings from one controller over Bluetooth | One tile per controller. Several controllers can be on the dashboard at the same time |
| Drive space | Free and used space for the mounts chosen in that tile's settings. The starting set is the root filesystem and `/library` | As many tiles as the user adds |
| Nomad status | Whether Project Nomad is running, and the state of its containers | As many tiles as the user adds |
| Meshtastic node count | How many nodes the local Meshtastic node currently knows | As many tiles as the user adds. Tile settings choose the radio when more than one is present |
| GPS time | The time reported by a GPS receiver | As many tiles as the user adds |

The first external-battery driver covers smart LiFePO4 and solar batteries that expose a BMS over Bluetooth Low Energy. Further brands are additional drivers.

The first solar-controller drivers cover:

- Victron SmartSolar over BLE
- Renogy BT-1
- Renogy BT-2
- EPEver

A battery tile shows state of charge, voltage, current, and connection status when the BMS provides them. A controller tile shows the PV and battery readings that controller provides (such as PV voltage, charge current, battery voltage, and charge state) and a connection status. A device that is out of range shows a disconnected state on its own tile and leaves the other tiles alone.

The dashboard can keep several Bluetooth devices connected at once, so a set of batteries and a set of controllers can appear together.

### Plugin and driver model

Tiles are plugins loaded by the dashboard shell. The shell owns layout: add, remove, rearrange, resize, and per-tile settings. A plugin owns one tile type.

Hardware plugins are drivers. A driver has a stable name, a device class, a way to discover matching devices, and a way to read one selected device. The same driver can be added more than once, once per physical device, which is how the dashboard shows multiple batteries and multiple charge controllers.

A new BLE battery or charge controller is a new driver. Adding one does not require a change to the shell. The driver is the supported way to grow the device list.

The language and the Plasma widget packaging are chosen when the dashboard is implemented and then recorded in this spec. This repository does not contain a widget, a driver, or sample device data. The reserved directory is [dashboard/](../dashboard/README.md).

## 16. Offline maps

The image includes an OpenStreetMap viewer. Map tiles are stored on `/library`, under `/library/maps`, and the viewer reads those local tiles. Once the tiles for an area are stored, that area can be browsed with no network.

Saving a region onto `/library` can use a network once. The viewer program and the download tool are chosen in the AMD64 milestone and then named in this spec.

## 17. Documentation

A How-To guide covers:

- install
- live use
- updates
- repair and rollback
- maintenance of the OS and of Nomad
- adding software
- drives
- Meshtastic
- ham tools
- themes, including Daybreak, Nightwatch, automatic day/night switching, red night-vision, and sunlight mode
- the Welcome app
- the Field Dashboard
- offline maps

The guide ships offline in three forms: PDF, a Kiwix ZIM, and ODT.

The guide, and the rest of `docs/`, is licensed CC BY 4.0. See [LICENSE-docs](../LICENSE-docs). Code is licensed GPLv3. See [LICENSE](../LICENSE).

The guide is an outline plus chapter stubs in [docs/guide/](guide/README.md). It is not written yet, and the PDF, ZIM, and ODT files are not in the tree.

## 18. Releases and continuous integration

- Images are published on GitHub Releases.
- Each release includes SHA256 checksums.
- A file larger than 2 GB is also mirrored on SourceForge.
- GitHub Actions builds the images.
- A numbered release carries a codename taken from homestead tools. Version 1.0 is **Axe**. The version and the codename are part of the release title and of the OS identity the user can read on the system. Pre-1.0 images use a version number only. Later codenames are chosen when that release is cut and written into the release notes.

No workflow file is committed in the planning pass. A workflow that cannot produce an image would look like a build system that does not exist.

## 19. Build order

1. AMD64 live and installer ISO.
2. Generic ARM64 UEFI image.
3. The first phone or tablet image, chosen from the PinePhone Pro, the Librem 5, and the PineTab2.

The other phone and tablet images, and the Raspberry Pi 5 image, come after that first handheld image. The checklist is [docs/ROADMAP.md](ROADMAP.md).

## 20. Licensing

| Material | License |
| --- | --- |
| Program code, build configuration, installer config, scripts | GNU GPLv3 ([LICENSE](../LICENSE)) |
| `docs/`, including this spec, the roadmap, and the How-To guide in every shipped format | CC BY 4.0 ([LICENSE-docs](../LICENSE-docs)) |

Copyright (c) 2026 Richard Colbert.

## 21. Implementer notes

These notes record boot constraints, and the choices a milestone still has to write back into this spec.

### EFI System Partition

UEFI boot needs a small EFI System Partition. On the AMD64 ISO and the generic ARM64 UEFI image, GPT still covers the whole disk. After that ESP, the rest of the disk is one Btrfs root, including on disks larger than 2 TB. The installer does not divide the root into a set of small fixed partitions.

### Devices that do not boot like a PC

PinePhone Pro, Librem 5, and PineTab2 images follow the partition and boot layout those devices need, leaning on postmarketOS device support where it fits. The Raspberry Pi 5 image uses the boot method chosen for that board when the image is built.

Where GRUB is the bootloader, snapshot rollback is a boot menu entry (Snapper and grub-btrfs style). Where GRUB is not the bootloader, rollback still has to be reachable from the boot menu. The device directory documents that path when the image is built.

### Choices this spec leaves to a milestone

Record the choice in this file when it is made:

- exact backported kernel package and Debian suite pin
- host firewall implementation
- Cyberdeck Control Panel language and toolkit
- which of the three handhelds is the first device image
- Snapper retention
- which program maintains the offline package mirror on `/library`
- NVIDIA packaging details beyond "included, and enabled when the GPU is detected"
- live-session Nomad delivery, as described in section 5
- whether Calamares also asks for a password, or Welcome is the only password step, so the user is asked once
- low-power/solar mode policy, as described in section 13
- display-manager and boot-splash packages that apply Daybreak and Nightwatch
- how a GPS fix is read for the GPS-time tile and for sunrise/sunset location
- Field Dashboard language and how a driver is packaged
- OpenStreetMap viewer and the tool that fills `/library/maps`
