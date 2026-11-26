# packages/

Package lists for the image build.

| File | Profile |
| --- | --- |
| [amd64/ci.list.chroot](amd64/ci.list.chroot) | Bootable AMD64 image: Plasma, Calamares, Snapper, Docker, ufw, Firefox ESR |
| [amd64/full.list.chroot](amd64/full.list.chroot) | Spec baseline that exists in Debian 13, added on top of `ci` |

ROCm and CUDA stay off these lists. The Nomad installer offers them after hardware detection.

`meshtasticd` and a Jellyfin desktop client are not published in Debian 13, so they are not in the lists. Flatpak and Flathub are in the `full` profile. The image hook adds the Flathub remote when `flatpak` is installed.

Requirements: [docs/SPEC.md](../docs/SPEC.md), sections 9, 10, 15, and 16.
