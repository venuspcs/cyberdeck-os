# devices/

Per-device ARM images. The generic ARM64 UEFI image for laptops, desktops, and boards is [build/arm64/](../build/arm64/README.md), not a directory here.

| Device | Session | Starting point |
| --- | --- | --- |
| [PinePhone Pro](pinephone-pro/README.md) | Plasma Mobile | postmarketOS device support where it fits |
| [Librem 5](librem-5/README.md) | Plasma Mobile | postmarketOS device support where it fits |
| [PineTab2](pinetab2/README.md) | Plasma Mobile | postmarketOS device support where it fits |
| [Raspberry Pi 5](raspberry-pi-5/README.md) | KDE Plasma (Wayland) | Dedicated board image |

The first handheld image is one of the PinePhone Pro, the Librem 5, or the PineTab2. Which one is first is decided at the start of that milestone. The other two, and the Raspberry Pi 5, follow.

Each subdirectory is a planning stub. None of them contain a kernel, a bootloader config, or an image definition.

Requirements: [docs/SPEC.md](../docs/SPEC.md), sections 3 and 17.
