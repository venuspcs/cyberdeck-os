# Install Cyberdeck OS

Cyberdeck OS is a Debian 13 live system for 64-bit PCs (AMD64). The image file is one hybrid ISO, `cyberdeck-os-amd64-amd64.hybrid.iso`. It boots on UEFI and on legacy BIOS, and it can install to a disk with Calamares. The desktop icon is **Install Cyberdeck OS**.

Alpha 3 is tag `v0.3.0-alpha3`, titled **Cyberdeck OS Alpha 3 (Hatchet)**. The ISO filename is still `cyberdeck-os-amd64-amd64.hybrid.iso`. GitHub Release files are limited to 2 GB, so the release splits the ISO into parts named `cyberdeck-os-amd64-amd64.hybrid.iso.part-aa`, `part-ab`, and so on. `SHA256SUMS` covers the joined ISO and each part.

This ISO is about 4 GB. Use a USB drive of **8 GB or larger**. Writing the USB erases that drive.

Apple Silicon Macs (M1 and later) cannot boot this image. An ARM64 image is planned and is not this download.

## Contents

1. [Download and check the checksum](#1-download-and-check-the-checksum)
2. [Unzip the download](#2-unzip-the-download)
3. [Make a bootable USB](#3-make-a-bootable-usb)
4. [Boot the computer](#4-boot-the-computer)
5. [Live session and installer](#5-live-session-and-installer)
6. [Troubleshooting](#6-troubleshooting)

## 1. Download and check the checksum

You need the ISO and a file named `SHA256SUMS`. Unzip the download first (section 2). `SHA256SUMS` is inside that zip, next to the ISO. The checksum file is one line: the SHA256 hash, two spaces, then `cyberdeck-os-amd64-amd64.hybrid.iso`.

Check the hash before you write the USB. If it does not match, download again. Do not flash a file that failed the check.

### GitHub Releases

Open [the Releases page](https://github.com/venuspcs/cyberdeck-os/releases).

Alpha 3 is published there as a pre-release, tag `v0.3.0-alpha3`. Download every `part-*` file and `SHA256SUMS`. The build writes `cyberdeck-os-amd64-amd64.hybrid.iso`; the release splits that file because GitHub allows 2 GB per asset.

Join the parts before you check the ISO hash or write the USB.

Linux:

```sh
cat cyberdeck-os-amd64-amd64.hybrid.iso.part-* > cyberdeck-os-amd64-amd64.hybrid.iso
sha256sum -c SHA256SUMS
```

Windows Command Prompt, in the folder that contains the parts:

```bat
copy /b cyberdeck-os-amd64-amd64.hybrid.iso.part-aa+cyberdeck-os-amd64-amd64.hybrid.iso.part-ab cyberdeck-os-amd64-amd64.hybrid.iso
```

Add further `+part-ac` names if the release has more than two parts. Then compare `Get-FileHash` with the ISO line in `SHA256SUMS`. Also check each part's own line in `SHA256SUMS` before joining if a download was interrupted.

### What you can download today

The image is a GitHub Actions artifact. Artifacts are kept for **7 days**, then deleted. If the download is missing, open a newer successful run.

1. Open [Build AMD64 ISO](https://github.com/venuspcs/cyberdeck-os/actions/workflows/build-amd64.yml).
2. Open the newest run that finished successfully.
3. Download the artifact named `cyberdeck-os-amd64-full`.

GitHub saves that download as a zip, `cyberdeck-os-amd64-full.zip`. Inside it are:

- `cyberdeck-os-amd64-amd64.hybrid.iso`
- `SHA256SUMS`

Those two files may sit in a folder (often `build/amd64`) inside the zip. Use the files with those names.

A second artifact, `cyberdeck-os-amd64-ci`, is a smaller test image. Use `cyberdeck-os-amd64-full` unless you were told to use the test image.

The ISO is a single file. The only archive around it is that artifact zip.

### Windows (PowerShell)

Extract the zip first (see below), then open PowerShell in the folder that contains both files. The hash must match the first field in `SHA256SUMS`. Letter case does not matter.

```powershell
Get-FileHash -Algorithm SHA256 .\cyberdeck-os-amd64-amd64.hybrid.iso
Get-Content .\SHA256SUMS
```

Or let PowerShell compare them:

```powershell
$expected = (Get-Content -Raw .\SHA256SUMS).Trim().Split(" ", [System.StringSplitOptions]::RemoveEmptyEntries)[0].ToLower()
$actual = (Get-FileHash -Algorithm SHA256 .\cyberdeck-os-amd64-amd64.hybrid.iso).Hash.ToLower()
if ($actual -eq $expected) { "MATCH" } else { "NOT A MATCH" }
```

`MATCH` means the file is intact.

### macOS

In Terminal, `cd` to the folder that contains both files, then:

```sh
shasum -a 256 -c SHA256SUMS
```

You want a line ending in `OK`. To print the hash yourself:

```sh
shasum -a 256 cyberdeck-os-amd64-amd64.hybrid.iso
```

Compare that hash with the hash in `SHA256SUMS`.

### Linux

In the folder that contains both files:

```sh
sha256sum -c SHA256SUMS
```

A good file prints:

```text
cyberdeck-os-amd64-amd64.hybrid.iso: OK
```

## 2. Unzip the download

The Actions download is a normal zip of one ISO plus `SHA256SUMS`. Unzip it, then check the checksum. Do not point the USB writer at the zip.

### Windows

- File Explorer: right-click `cyberdeck-os-amd64-full.zip`, choose **Extract All**, and pick a folder.
- 7-Zip: right-click the zip, then **7-Zip** → **Extract Here** (or **Extract to `cyberdeck-os-amd64-full\`**).

### macOS

Double-click the zip. Finder unpacks it next to the zip.

### Linux

```sh
unzip cyberdeck-os-amd64-full.zip
```

If `unzip` is not installed, `7z x cyberdeck-os-amd64-full.zip` does the same job.

### Split parts

Current builds ship as one ISO inside the zip. Join files only when the download page lists several parts of that same image.

If a later `` `<version>` `` release is split, that page lists the real part names. Download every part into one folder and join them in the order the page lists. The placeholders below are not real filenames.

Windows Command Prompt, with the parts in one folder:

```bat
copy /b <first-part>+<second-part>+<third-part> cyberdeck-os-amd64-amd64.hybrid.iso
```

7-Zip on Windows, macOS, or Linux: put every part in the same folder, right-click the **first** part, and extract. Or:

```sh
7z x <first-part>
```

Linux and macOS can also concatenate parts that were split as raw pieces:

```sh
cat <first-part> <second-part> <third-part> > cyberdeck-os-amd64-amd64.hybrid.iso
```

Then check `SHA256SUMS` against the joined ISO before you write the USB.

## 3. Make a bootable USB

**This erases the whole USB drive.** Copy off anything you still need. Unplug other USB disks so you do not pick the wrong one. Dragging the ISO onto a normal USB does not make it boot, except on Ventoy after Ventoy itself is installed.

Use the `.hybrid.iso` file, after the checksum matches.

### Rufus (Windows)

1. Download Rufus from [rufus.ie](https://rufus.ie/) and start it.
2. **Device:** your USB drive.
3. **Boot selection:** `cyberdeck-os-amd64-amd64.hybrid.iso`.
4. When Rufus asks how to write the image, choose **DD Image mode**.
5. In DD Image mode, Rufus copies the hybrid image unchanged. The **Partition scheme** box does not change the result. That image already boots UEFI and legacy BIOS.
6. If you stay in **ISO Image mode** instead, the partition scheme does matter: **GPT** for UEFI, **MBR** for legacy BIOS/CSM. Prefer DD Image mode for this ISO.
7. Click **Start** and confirm the erase warning.

### balenaEtcher (Windows, macOS, Linux)

1. Download Etcher from [etcher.balena.io](https://etcher.balena.io/).
2. Click **Flash from file** and choose the `.hybrid.iso` (not the zip).
3. Click **Select target** and choose the USB drive. Check the size.
4. Click **Flash**. Etcher warns you that the drive will be erased.

### Ventoy (more than one ISO on one USB)

1. Download Ventoy from [ventoy.net](https://www.ventoy.net/).
2. Install Ventoy onto the USB. That step erases the drive. Install the UEFI option, the BIOS option, or both, to match the computers you boot.
3. When the install finishes, copy `cyberdeck-os-amd64-amd64.hybrid.iso` onto the large Ventoy data partition, like any other file. You can copy other ISOs beside it.
4. Boot the USB and pick Cyberdeck OS from the Ventoy menu.

### Linux `dd`

1. Plug in the USB and list disks:

   ```sh
   lsblk -o NAME,SIZE,TYPE,MODEL,TRAN,MOUNTPOINT
   ```

2. Find the row whose `TRAN` is `usb` and whose size matches the stick. The name is something like `sdb`. Your internal disk is often `sda` or `nvme0n1`, and it has your system mounted on it. **Do not use that disk.**
3. Unmount any partitions of the USB, not the internal disk. If the stick is `sdb`:

   ```sh
   udisksctl unmount -b /dev/sdb1
   ```

   Repeat for `sdb2` and so on if they are mounted. `umount` is fine if `udisksctl` is missing.
4. Write the whole disk (`sdb`), not a partition (`sdb1`). Replace `sdX` with the name you read from `lsblk`:

   ```sh
   sudo dd if=cyberdeck-os-amd64-amd64.hybrid.iso of=/dev/sdX bs=4M status=progress conv=fsync
   sudo sync
   ```

5. Wait until `dd` and `sync` both return. Then unplug the USB.

### macOS `dd`

1. List disks:

   ```sh
   diskutil list
   ```

2. Find the **external, physical** disk whose size matches the USB stick. It looks like `/dev/disk2`. The internal drive is usually `/dev/disk0`. **Do not use the internal drive.**
3. Unmount the USB (the whole disk, not one slice). Replace `N` with the number from `diskutil list`:

   ```sh
   diskutil unmountDisk /dev/diskN
   ```

4. Write to the raw device `rdiskN` (faster than `diskN`):

   ```sh
   sudo dd if=cyberdeck-os-amd64-amd64.hybrid.iso of=/dev/rdiskN bs=4m
   ```

5. When `dd` finishes:

   ```sh
   diskutil eject /dev/diskN
   ```

## 4. Boot the computer

Plug the USB in, then power on. Open the one-time boot menu and choose the USB. It may show up as the brand of the stick, as `CYBERDECKOS`, or as UEFI: the stick name.

Tap the key as soon as the logo appears. Tap it again if the computer boots the internal disk. Keys differ by model. The table is the one-time **boot menu**. Firmware setup is a different screen, usually Del, F2, or F10 (HP).

| Vendor | Common boot-menu key |
| --- | --- |
| Asus | Esc |
| Acer | F12 (turn on **F12 Boot Menu** in firmware setup first) |
| Dell | F12 |
| HP | Esc, then F9 |
| Lenovo | F12. Some IdeaPads use Fn+F12, or a small Novo button |
| MSI | F11 |
| Gigabyte | F12 |
| ASRock | F11 |
| Toshiba | F12 (some models need the F12 menu enabled in setup) |
| Samsung | F10 or Esc |
| Apple, Intel Mac | Option (Alt). Choose **EFI Boot** |

### UEFI

Prefer UEFI when the menu lists both a UEFI USB entry and a legacy USB entry. The ISO's UEFI bootloader is GRUB.

### Legacy BIOS / CSM

The same ISO also has a legacy BIOS bootloader (syslinux). Use it when the computer has no UEFI, or when the UEFI entry will not start.

If the USB is missing, open firmware setup and enable CSM or Legacy support. Many PCs hide the legacy entry until CSM is on. Some firmware will not enable CSM and Secure Boot at the same time. Use the UEFI entry when Secure Boot is on.

### Secure Boot

Secure Boot can stay on. On the ASUS Vivobook S16 test, firmware reported Secure Boot Active in User mode with the factory keys, and both the live USB and the installed system booted.

Leave Secure Boot enabled and choose the USB from the boot menu. If a machine's firmware refuses the USB, that is a firmware quirk on that machine, not a requirement to turn Secure Boot off for Cyberdeck OS.

### Fast Boot and Windows Fast Startup

These are two different settings.

**Fast Boot** is in firmware. It skips USB startup, so the stick never appears. Set Fast Boot to Disabled, save, and try the boot menu again.

**Windows Fast Startup** is in Windows. It hibernates the Windows disk instead of shutting down. That can hide disks and break a later dual boot. In Windows:

1. Open Control Panel → Power Options → **Choose what the power buttons do**.
2. Click **Change settings that are currently unavailable**.
3. Clear **Turn on fast startup**. Save.
4. Shut down fully. Hold Shift while you click Shut down.

### BitLocker

If Windows uses BitLocker or device encryption, save the recovery key **before** you change Secure Boot, switch RAID to AHCI, or resize the Windows partition. A firmware or partition change can boot Windows into a blue recovery screen that asks for that key.

The key is often in your Microsoft account, or your organization has it. You can suspend protection for the next boot and turn it back on from Windows afterward. In an administrator PowerShell window: `manage-bde -protectors -disable C:`.

### RAID / Intel RST to AHCI

Linux often cannot see a disk that firmware has set to RAID or Intel RST (VMD). The installer needs AHCI.

Look in firmware setup under SATA, VMD, or storage. If the mode is already AHCI, leave it. If it is RAID or Intel RST, and the installer later shows no internal disk, switch it to AHCI.

That switch can stop an existing Windows install from booting. Back up first. If you still need Windows on that disk:

1. In Windows, open an administrator Command Prompt and run `bcdedit /set {current} safeboot minimal`.
2. Reboot into firmware and set the disk mode to AHCI. Save and exit.
3. Let Windows start in Safe Mode.
4. Open an administrator Command Prompt and run `bcdedit /deletevalue {current} safeboot`.
5. Reboot.

If you are erasing the disk and do not need Windows, you still need the disk to show up, so the firmware mode still has to be AHCI. You can skip the `bcdedit` steps.

### Apple Silicon

Not supported. This file is an AMD64 image for Intel and AMD PCs. M1, M2, M3, and later Macs cannot boot it. The planned ARM64 image is a different download, and it is not a Mac image.

Intel Macs can use the Option key, as in the table above.

## 5. Live session and installer

Booting the USB does not install anything. It starts a live desktop. Your internal disk is unchanged until you confirm the install.

**Back up first.** Copy personal files off the computer before you confirm the install. Erase disk deletes every partition on the drive you select. Install alongside keeps the other system and resizes its partition, and that resize can still leave the other system unable to boot. If Windows is encrypted, save the BitLocker recovery key before you start.

1. At the menu titled **Cyberdeck OS Beta 1 (Plow)**, choose a **Live system** line. The current image lists two kernels on that menu: `Live system, kernel 7.3.4+deb13-amd64` and `Live system, kernel 6.12.118+deb13-amd64`. Either line is a valid start. The 6.12 line is the fallback when the newer kernel misbehaves (including some Wi-Fi chips). A later image may print different version numbers. Use the lines that menu shows.
2. Wait for the desktop. The live session logs in by itself as the user `cyberdeck`, password `cyberdeck`, on KDE Plasma (Wayland). That account can use `sudo`. This password is only for the live session.
3. Open **Install Cyberdeck OS** on the desktop or in the application menu. That starts Calamares.
4. Walk through Welcome, location, keyboard, partitions, and the user account for the **installed** system. Read the summary. The disk is written when you confirm.

The installed system has no separate root password. The account you create in Calamares is the administrator (`sudo`).

### Full disk or dual boot

The partition screen offers **Erase disk**, **Install alongside**, and **Manual partitioning**.

**Erase disk** deletes the selected drive and installs Cyberdeck OS. The layout is GPT: a 1 MB BIOS boot partition, a 512 MB EFI system partition, and one Btrfs root. Pick this when this computer will only run Cyberdeck OS, or when you have already copied your files off.

**Install alongside** is the dual-boot choice. It keeps the other operating system and adds Cyberdeck OS on the same disk. A slider shows the two systems side by side. Drag it to choose how much space each one gets, then continue. Leave the other system enough room for its own files. The installer shrinks that system's partition to make the space.

Do this before you choose Install alongside on a Windows PC:

1. Back up anything you still need. The slider changes the size of the Windows partition.
2. Turn off Windows Fast Startup, then shut Windows down fully (hold Shift while you click Shut down). Fast Startup leaves Windows half-hibernated, and the installer cannot safely resize that partition.
3. If Windows uses BitLocker or device encryption, save the recovery key first (often in your Microsoft account). Suspend protection before the install, or Windows can boot to a recovery screen after the partition changes size. In an administrator PowerShell window: `manage-bde -protectors -disable C:`. Turn protection back on from Windows after you have confirmed Windows still boots.

Install alongside needs a GPT disk. A disk that is not GPT is not eligible. Rewriting it as GPT means Erase disk, which removes the other system.

**Manual partitioning** is the advanced choice. Use it when you want to pick the partitions yourself. Leave the other system's partitions in place, and put the Cyberdeck OS Btrfs root in free space on a GPT disk.

A supported install disk is at least **256 GB**. Calamares will still allow a smaller disk, down to about 8 GB, so a test install can finish. A disk under 256 GB is not a supported everyday install.

Encryption is optional. `cryptsetup` is in the image, and it stays off unless you turn it on in the partition step. If you turn it on, store the passphrase somewhere you can read without this disk. There is no recovery if you lose it.

When Calamares finishes, reboot and remove the USB when the computer asks you to. Sign in with the account you created.

The installed system opens **Project Nomad Setup** once, in a terminal, at first login. The live desktop does not open that setup by itself. You can start it later from the menu under the same name. It asks where the `/library` drive lives. You can skip the network parts and come back to them.

## 6. Troubleshooting

### The USB is not in the boot menu

- Reboot and tap the boot-menu key earlier. Use a USB port on the computer itself, not a hub. On a desktop, try a USB 2.0 port on the back.
- Turn firmware **Fast Boot** off, and turn off Windows Fast Startup, then shut Windows down fully (hold Shift).
- Leave Secure Boot on and try the UEFI USB entry. The Vivobook test booted with Secure Boot Active.
- In firmware setup, enable USB boot. On Acer and some Toshiba models, enable the F12 boot menu.
- Rufus must be in **DD Image mode**, or the stick was written with Etcher or `dd`. A file copy of the ISO does not boot. Ventoy is the exception: the ISO is a file, and the Ventoy installer prepared the stick.
- Recreate the stick. Then try the other firmware mode (UEFI if you used legacy, or legacy/CSM if you used UEFI).

### Black screen

UEFI boots with GRUB. Legacy BIOS boots with Syslinux. The edit is the same idea on both, and it lasts for this boot only.

**UEFI (GRUB).** Highlight the Live system line and press `e`. Find the line that starts with `linux`. At the end of that line, add a space and `nomodeset`. Press Ctrl+X or F10 to boot.

**Legacy BIOS (Syslinux).** Highlight the Live line and press Tab. The boot command appears at the bottom of the screen. At the end of that line, add a space and `nomodeset`. Press Enter to boot.

`nomodeset` tells the kernel to skip the graphics driver's modesetting, which gets past a blank screen on some GPUs. The picture may be a plain mode until the system is installed and a driver is set up.

If the menu has a fail-safe Live entry, you can try that too. The build's fail-safe options are `noapic noapm nodma nomce nosplash`. You can still add `nomodeset` on that line the same way: `e` then Ctrl+X or F10 in GRUB, or Tab then Enter in Syslinux.

### The boot hangs

- Wait a few minutes. The first live boot unpacks a large image.
- Reboot and choose the other **Live system** kernel line.
- Add `nomodeset`, or use the fail-safe entry, as above.
- Unplug extra USB devices (printers, external disks, dongles) and try again.
- Write the USB again, after the checksum matches.

### Wi-Fi does not connect

The live desktop uses NetworkManager. Use the network icon in the panel.

- Confirm the radio is on (a hardware switch or a key such as Fn plus a wireless key).
- Forget the network and join it again.
- If the router offers both WPA2 and WPA3, set this connection to WPA2 (`wpa-psk`). Forget the network once after that so the saved address is the stable one. The image turns scan MAC randomization off and uses a stable connection MAC. Mixed WPA2/WPA3 networks have failed after they associate when that is left on automatic.
- Reboot and choose the Live system line for the Debian 13 kernel (`6.12.118+deb13-amd64` on the current image). That kernel is the fallback for Wi-Fi chips that misbehave on the newer one. This was reported on an Asus Vivobook S16 with an MT7922 (`mt7921e`).
- Plug in Ethernet if you can. The installer does not need Wi-Fi.

---

This guide is documentation for Cyberdeck OS and is licensed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
