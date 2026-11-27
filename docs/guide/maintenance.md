# Maintaining the OS and Nomad

**Status: stub, except the Wi-Fi note.** The rest of this chapter is not written.

## Wi-Fi

Two separate problems showed up on an Asus Vivobook S16 with a MediaTek MT7922 (`mt7921e`).

The connection dropped every few minutes on kernel `7.3.4+deb13`.
The image turns power saving off and disables ASPM for that driver:

`/etc/NetworkManager/conf.d/default-wifi-powersave-off.conf` sets `wifi.powersave = 2`

`/etc/modprobe.d/mt7921e.conf` sets `options mt7921e disable_aspm=1`

A Starlink Mini SSID then failed immediately on 5 GHz.
Ethernet was plugged into that same router.
The log line is `CTRL-EVENT-SSID-TEMP-DISABLED` with `reason=CONN_FAILED` at 802.11 authenticate.
Another router's SSID worked. The same laptop worked on Zorin OS and Linux Mint.
Those systems are Ubuntu-based.
Zorin 17 is 22.04. Mint 22 is 24.04. Both use Ubuntu `linux-firmware`.
This image had been using Linux 7.3.4 and MediaTek firmware `20260916` from Debian backports.
The MT7922 patch file in that package is dated `20260724`.

Debian's NetworkManager also scanned with a random MAC and connected with the permanent MAC.
`mt7921e` is not in the driver list that skips MAC changes.
The image now scans and connects with one stable MAC:

`/etc/NetworkManager/conf.d/wifi-stable-mac.conf`

`wifi.scan-rand-mac-address=no` and `wifi.cloned-mac-address=stable`

MediaTek firmware stays on Debian 13 `firmware-mediatek` (`20250410-2`), not backports.
Wi-Fi still uses `wpa_supplicant`. iwd is not installed. WPA3 is not turned off for every network.

On a WPA2/WPA3 mixed router, such as Starlink, WPA3 (SAE) can still drop after it connects.
Open the connection and set security to WPA2 (`wpa-psk`).
Forget the network once after this image update so the stable MAC is used.

The boot menu lists the Debian 13 stock kernel, `6.12`, next to `7.3.4`.
Choose the `6.12` entry if the backports kernel still cannot join the Starlink SSID.
AMD graphics firmware stays on backports. Only `firmware-mediatek` is held back.

This chapter will cover routine care of Cyberdeck OS and Project Nomad through the Cyberdeck Control Panel: update, repair, backup, drive health, restarting Nomad, and the theme and display-mode controls (Daybreak, Nightwatch, night vision, sunlight mode, low-power/solar). It will also point at the support-the-creator link inside that panel.

Requirements: [the specification](../SPEC.md), sections 7 and 12 through 14.

This guide is licensed under [CC BY 4.0](../../LICENSE-docs).
