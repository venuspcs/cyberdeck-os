# Tested on (hardware)

AMD64 is the image under test. ARM64 and phone images are on hold.

Add a result by opening a [Hardware test report](https://github.com/venuspcs/cyberdeck-os/issues/new?template=hardware_test_report.md). Wi-Fi and audio stay "unknown" until someone on that machine has checked them.

| Device | CPU/GPU | Build/version | Live boot | Install | Wi-Fi | Audio | Notes | Tester |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Asus Vivobook S16 (M5606WA) | AMD Ryzen AI 9 HX370, Radeon 890M | Cyberdeck OS Version 1 (Alpha), pre-fix ISO | Works | Works | Drops | Unknown | MT7922 (`mt7921e`) dropped every few minutes on kernel `7.3.4+deb13`. The image after this report ships `/etc/NetworkManager/conf.d/default-wifi-powersave-off.conf` (`wifi.powersave = 2`) and `/etc/modprobe.d/mt7921e.conf` (`disable_aspm=1`). On a WPA2/WPA3 mixed router such as Starlink, set the connection to WPA2 (`wpa-psk`) if SAE drops. Debian branding, wallpaper, the manual icon, and Nomad autorun also failed on this boot. The firewall was on and looked right | [@VeteranPrepper](https://x.com/VeteranPrepper) |
| QEMU (BIOS and UEFI) | Virtual CPU, no GPU | Local full ISO `4d1a64bf8b7652401d24b3a4f1f87afd1f0fa4c85d10ecd91a86fe54462ecdc4` | Works on BIOS and UEFI. The session is KDE Plasma on Wayland | Erase install reaches the SDDM greeter under UEFI. A snapshot taken before an apt reinstall shows in the GRUB snapshot menu | n/a | n/a | Calamares welcome, location, keyboard, and partition pages were screenshotted after the launcher fix was copied into that live session. A scripted alongside install left an existing ext4 file readable. That disk's GRUB stopped at a prompt instead of the menu | Project QEMU test |

The pre-fix ISO is the build Richard installed. It still showed Debian artwork and "Cyberdeck OS 13" because `VERSION_ID` was `13`. Wi-Fi on the MT7922 dropped every few minutes. The Version 1 (Alpha) identifier, homestead wallpapers, manual icon, Nomad autostart, Wi-Fi powersave setting, and `mt7921e` ASPM option are in the image built after that report.
