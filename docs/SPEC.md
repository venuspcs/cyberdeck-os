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

## 8. First boot, Project Nomad, and `/library`

The installed system runs a first-boot Nomad installer. It installs Project Nomad and its containers, then asks which drive holds `/library`.

If the user chooses the boot drive, the installer creates a `/library` directory on that drive.

If the user chooses another drive, the installer offers two choices: format the drive, or use it as-is. Either way it mounts that drive by UUID from `/etc/fstab`, and Docker is configured to start only after `/library` is mounted.

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
- A host firewall that is enabled by default

The firewall package (for example nftables directly, firewalld, or ufw) is chosen in the AMD64 milestone and then named in this spec. The requirement for this pass is that a firewall is on in the default system.

Anything outside this list is something the user installs, through the terminal, Nomad, or Flatpak.

## 10. Drivers and compute stacks

- AMD and Intel NPUs use their in-kernel drivers. The backported kernel exists in part so those drivers are present, including AMD XDNA on Ryzen AI HX370.
- The NVIDIA proprietary driver is included in the image and enabled automatically when an NVIDIA GPU is detected.
- ROCm and CUDA are not in the image.
- On first boot, if the hardware needs ROCm or CUDA, the system offers a one-click install and then configures Ollama to use it.

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
- a link to support the creator (the same destinations as the README: Cash App, Venmo, and X Money via @VeteranPrepper)

The UI toolkit is chosen when the panel is implemented. This repository does not contain the application yet.

## 13. Power

The system has a low-power/solar mode toggle for battery and solar cyberdecks. The concrete policy (CPU governor, screen power, which services pause) is defined with the control panel work and then added to this spec.

## 14. Branding

Cyberdeck OS has its own boot splash, wallpaper, and logo. Those assets are not part of this planning pass. They will land under [branding/](../branding/README.md). Until they exist, the image build uses a documented stand-in only if a file is required for the boot path to succeed, and that stand-in is labeled as temporary.

## 15. Documentation

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

The guide ships offline in three forms: PDF, a Kiwix ZIM, and ODT.

The guide, and the rest of `docs/`, is licensed CC BY 4.0. See [LICENSE-docs](../LICENSE-docs). Code is licensed GPLv3. See [LICENSE](../LICENSE).

The guide is an outline plus chapter stubs in [docs/guide/](guide/README.md). It is not written yet, and the PDF, ZIM, and ODT files are not in the tree.

## 16. Releases and continuous integration

- Images are published on GitHub Releases.
- Each release includes SHA256 checksums.
- A file larger than 2 GB is also mirrored on SourceForge.
- GitHub Actions builds the images.

No workflow file is committed in the planning pass. A workflow that cannot produce an image would look like a build system that does not exist.

## 17. Build order

1. AMD64 live and installer ISO.
2. Generic ARM64 UEFI image.
3. The first phone or tablet image, chosen from the PinePhone Pro, the Librem 5, and the PineTab2.

The other phone and tablet images, and the Raspberry Pi 5 image, come after that first handheld image. The checklist is [docs/ROADMAP.md](ROADMAP.md).

## 18. Licensing

| Material | License |
| --- | --- |
| Program code, build configuration, installer config, scripts | GNU GPLv3 ([LICENSE](../LICENSE)) |
| `docs/`, including this spec, the roadmap, and the How-To guide in every shipped format | CC BY 4.0 ([LICENSE-docs](../LICENSE-docs)) |

Copyright (c) 2026 Richard Colbert.

## 19. Implementer notes

These notes record boot constraints so the storage rules can be implemented. They do not add features.

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
- low-power/solar mode policy, as described in section 13
