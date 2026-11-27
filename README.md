# cyberdeck-os
Cyberdeck OS: a lean Debian-based live/installable Linux for cyberdecks, built around Project Nomad offline tools. AMD64 + ARM64.

## Install

The installable image today is the AMD64 live ISO (Debian 13) with the Calamares installer. The file is `cyberdeck-os-amd64-amd64.hybrid.iso` (about 4 GB). No GitHub Release is published yet. Download the `cyberdeck-os-amd64-full` artifact from a successful [Build AMD64 ISO](https://github.com/venuspcs/cyberdeck-os/actions/workflows/build-amd64.yml) run. GitHub wraps it in a zip with `SHA256SUMS`. Artifacts expire after 7 days. When a release exists, use [GitHub Releases](https://github.com/venuspcs/cyberdeck-os/releases).

1. Unzip the artifact. The ISO is one file, not split parts. `SHA256SUMS` is inside the zip.
2. Check the SHA256 checksum against `SHA256SUMS`.
3. Write it to an 8 GB or larger USB. This erases the USB. Use Rufus in DD Image mode, balenaEtcher, or `dd`. With Ventoy, install Ventoy on the USB first, then copy the ISO onto it.
4. Boot the USB in UEFI, or legacy BIOS. Secure Boot is not supported; turn it off.
5. On the live desktop, open **Install Cyberdeck OS**. Back up your files first.

Checksum commands, firmware notes, and fixes are in [docs/INSTALL.md](docs/INSTALL.md).
