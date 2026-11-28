# Maintaining the OS and Nomad

**Status: written for Beta 1 (Plow).**

## Wi-Fi

The image turns Wi-Fi power saving off (`wifi.powersave = 2`) and sets `options mt7921e disable_aspm=1` for the MediaTek MT7922. Scans and connections use one stable MAC (`wifi.scan-rand-mac-address=no` and `wifi.cloned-mac-address=stable`). MediaTek firmware stays on Debian 13, not backports.

On a WPA2/WPA3 mixed router such as Starlink, if the link drops after it associates, edit the connection and set security to WPA2 (`wpa-psk`). Forget the network once after upgrading so the stable MAC is saved.

If the backports kernel still cannot join, boot the menu line that contains `6.12`.

## Clock and wallpaper

Daybreak (light) runs from 06:30 until 18:30 in the timezone the desktop is using. Nightwatch is every other time. The switch runs at login, again within 15 seconds of a clock or timezone change, and after the machine resumes. The choice is logged in `~/.local/share/cyberdeck-theme.log`.

9:00 America/Chicago is Daybreak. 21:00 America/Chicago is Nightwatch.

## Time sync

`systemd-timesyncd` is installed and enabled. System Settings can turn NTP on. If it still says it cannot change NTP, run `timedatectl set-ntp true`.

## Manual

The desktop icon **Cyberdeck OS Manual** opens the PDF in Okular. Okular is the default PDF application.

## Snapshots

Snapper keeps the 4 newest numbered snapshots (`NUMBER_LIMIT=4`), which is two pre/post pairs from apt. Apt takes a snapshot before it changes packages.

## Support

**Support Cyberdeck OS** in the menu opens X Money, Cash App, and Venmo. Nothing is charged from that window.

This guide is licensed under [CC BY 4.0](../../LICENSE-docs).
