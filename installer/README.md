# installer/

Reserved for Calamares configuration.

The installed desktop will have an icon named **Install Cyberdeck OS** that launches Calamares. The installer will offer erase disk, install alongside, and manual partitioning, plus optional full-disk encryption. Install targets use GPT, including disks larger than 2 TB, with a Btrfs root after the EFI System Partition required to boot. A supported target is at least 256 GB.

Phone, tablet, and Raspberry Pi 5 images may need a different installer path. That difference is documented with the device, not invented here.

**There is no Calamares config in this directory.** No `settings.conf`, no partition module config, and no branding folder. Those files arrive with the AMD64 milestone.

Requirements: [docs/SPEC.md](../docs/SPEC.md), sections 6 and 7.
