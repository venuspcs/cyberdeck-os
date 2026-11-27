# Cyberdeck OS How-To guide

**Status: outline only.** The chapters linked below are stubs, except the Wi-Fi drop note in maintenance. They are not a full install or repair guide.

When the guide is written, it will ship offline as a PDF, a Kiwix ZIM, and an ODT file, so it can be read from Project Nomad without the network. Those editions are not built yet. Generated copies belong on a release or under `docs/guide/dist/` (gitignored), not next to the chapter source.

This guide is licensed under [CC BY 4.0](../../LICENSE-docs). Copyright (c) 2026 Richard Colbert. Credit Richard Colbert and Cyberdeck OS if you share or adapt it.

The behavior the guide will describe is specified in [../SPEC.md](../SPEC.md).

## Chapters

### 1. [Installing](install.md)

Creating boot media, booting the live desktop, and running Calamares from the **Install Cyberdeck OS** icon. Erase disk, install alongside, and manual partitioning. Optional full-disk encryption. GPT and a Btrfs root, and the 256 GB minimum for the install target.

### 2. [Live use](live-use.md)

What the live session is for, how the desktop is laid out, and how to use Project Nomad before anything is installed to a disk.

### 3. [Updates](updates.md)

Installing updates, the snapshot taken before each update, and where to look when an update needs a reboot.

### 4. [Repair and rollback](repair-rollback.md)

Choosing a snapshot from the boot menu, returning to the previous root, and what rollback does to Nomad and to `/library`.

### 5. [Maintenance](maintenance.md)

Day-to-day care of the OS and of Project Nomad: the Cyberdeck Control Panel (update, repair, backup, drive health, restart Nomad), disk space, and logs worth keeping. The written note covers Wi-Fi drops on the MediaTek MT7922 and WPA2/WPA3 mixed routers.

### 6. [Adding software](adding-software.md)

### 6b. [Other systems with Distrobox](containers.md)

The three supported ways to add software: the terminal, Project Nomad, and Flatpak with Flathub. The offline package cache on `/library`.

### 7. [Drives](drives.md)

The first-boot choice of where `/library` lives. A folder on the boot drive, or another drive formatted or used as-is, mounted by UUID. Moving `/library` later. Docker starting only after that filesystem is mounted.

### 8. [Meshtastic](meshtastic.md)

`meshtasticd`, the Meshtastic web client, and how that fits next to Meshtastic Web inside Nomad.

### 9. [Ham and SDR tools](ham-tools.md)

GQRX, WSJT-X, Fldigi, and CHIRP: what each program is on the image, and where radio hardware setup will be documented.

## Also covered when the chapters are written

- Ports that stay fixed: Nomad admin on 8080, Open WebUI on 3000, Ollama on localhost port 11434.
- The Welcome app: theme, `/library`, Wi-Fi, ROCm or CUDA, and the account password.
- Daybreak and Nightwatch, automatic sunrise/sunset switching, red night-vision, and high-contrast sunlight mode.
- The Field Dashboard and its tiles, including adding a Bluetooth battery or charge controller.
- Offline OpenStreetMap tiles on `/library/maps`.
- The low-power/solar mode toggle.
- Phone, tablet, and Raspberry Pi 5 differences, once those images exist.
- How to support the creator, with the same links as the project README.
