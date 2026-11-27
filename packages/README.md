# packages/

Package lists for the image build.

| File | Profile |
| --- | --- |
| [amd64/ci.list.chroot](amd64/ci.list.chroot) | Bootable AMD64 image: Plasma, Calamares, Snapper, Docker, ufw, Firefox ESR |
| [amd64/full.list.chroot](amd64/full.list.chroot) | Spec baseline that exists in Debian 13, added on top of `ci` |

ROCm and CUDA stay off these lists. The Nomad installer offers them after hardware detection.

`meshtasticd` is installed on the `full` profile from the Meshtastic Open Build Service repository for Debian 13. The Jellyfin client is the Flathub app `org.jellyfin.JellyfinDesktop`, installed by the image hook when that profile is built. Flatpak and Flathub are in the `full` package list.

Requirements: [docs/SPEC.md](../docs/SPEC.md), sections 9, 10, 15, and 16.
