# installer/

Calamares configuration and the non-interactive install path used to test the disk layout.

The live desktop icon **Install Cyberdeck OS** is the Debian Calamares launcher with that name. It opens Calamares. Erase disk uses GPT, a 512 MiB EFI system partition on UEFI machines, a 1 MiB BIOS boot partition, and one Btrfs root. Alongside and manual partitioning stay available. Optional encryption is Calamares' own LUKS checkbox. Snapper is configured at the end of the install, and apt takes a snapshot before later package changes.

`cyberdeck-autoinstall` performs the same GPT, ESP, BIOS-boot, and Btrfs layout without the GUI so a virtual machine can install the live squashfs and reboot it. It is the test path. The desktop path is Calamares.

Supported install targets are at least 256 GB. Calamares' hard stop is 8 GiB so a smaller disk can still be used for a test.

Requirements: [docs/SPEC.md](../docs/SPEC.md), sections 6 and 7.
