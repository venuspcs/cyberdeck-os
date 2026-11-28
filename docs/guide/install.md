# Installing

**Status: written for Beta 1 (Plow).**

Download the ISO from GitHub Releases. Join the parts if the release split the file, check SHA256, then write the USB. Secure Boot can stay on. The full walk-through is [docs/INSTALL.md](../INSTALL.md).

On the live desktop, open **Install Cyberdeck OS**. Erase disk replaces the disk with GPT, an EFI system partition, and a Btrfs root. Install alongside needs a GPT disk with free space. Manual partitioning is the advanced path. Calamares asks for the account password.

The boot menu title is Cyberdeck OS Beta 1 (Plow). It lists the 7.3 backports kernel and the Debian 13 6.12 kernel.

This guide is licensed under [CC BY 4.0](../../LICENSE-docs).
