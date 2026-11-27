# Maintaining the OS and Nomad

**Status: stub, except the Wi-Fi note.** The rest of this chapter is not written.

## Wi-Fi drops

The image turns Wi-Fi power saving off:

`/etc/NetworkManager/conf.d/default-wifi-powersave-off.conf`

`wifi.powersave = 2`

It also loads the MediaTek driver with ASPM disabled:

`/etc/modprobe.d/mt7921e.conf`

`options mt7921e disable_aspm=1`

That pair is for the MT7922 on an Asus Vivobook S16.
The `mt7921e` driver dropped Wi-Fi every few minutes on kernel `7.3.4+deb13`.

On a WPA2/WPA3 mixed router, such as Starlink, WPA3 (SAE) can still drop.
Open the connection and set security to WPA2 (`wpa-psk`).

This chapter will cover routine care of Cyberdeck OS and Project Nomad through the Cyberdeck Control Panel: update, repair, backup, drive health, restarting Nomad, and the theme and display-mode controls (Daybreak, Nightwatch, night vision, sunlight mode, low-power/solar). It will also point at the support-the-creator link inside that panel.

Requirements: [the specification](../SPEC.md), sections 7 and 12 through 14.

This guide is licensed under [CC BY 4.0](../../LICENSE-docs).
