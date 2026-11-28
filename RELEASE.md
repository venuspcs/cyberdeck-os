Cyberdeck OS Alpha 3 (Hatchet) is an AMD64 pre-release. Build id 3. Secure Boot can stay on.

## Join the ISO

GitHub stores each file under 2 GB. The ISO is split into `cyberdeck-os-amd64-amd64.hybrid.iso.part-aa`, `part-ab`, and `part-ac`. Download every part and `SHA256SUMS`.

Linux, in the folder that contains the parts:

```sh
cat cyberdeck-os-amd64-amd64.hybrid.iso.part-* > cyberdeck-os-amd64-amd64.hybrid.iso
sha256sum -c SHA256SUMS
```

Windows Command Prompt, in that same folder:

```bat
copy /b cyberdeck-os-amd64-amd64.hybrid.iso.part-aa+cyberdeck-os-amd64-amd64.hybrid.iso.part-ab+cyberdeck-os-amd64-amd64.hybrid.iso.part-ac cyberdeck-os-amd64-amd64.hybrid.iso
```

`SHA256SUMS` lists the joined ISO and each part. Check the parts before you join them if a download stopped halfway. Check the joined ISO before you write the USB. `sha256sum -c SHA256SUMS` prints `OK` for each line it can see. A missing ISO file makes the ISO line fail until you join the parts.

Write the joined ISO to an 8 GB or larger USB. This erases the USB. Rufus in DD Image mode, balenaEtcher, or `dd` all work. The longer install notes are in `docs/INSTALL.md`.

## What this image is

The system identifies itself as Cyberdeck OS Alpha 3 (Hatchet). The live account is `cyberdeck` on the host `cyberdeck`. Daybreak runs from 06:30 to 18:30 local time. Nightwatch is the other hours. `systemd-timesyncd` is enabled. The manual opens in Okular. Project Nomad setup starts Dozzle on 127.0.0.1:9999, Qdrant on 127.0.0.1:6333, and the Supply Depot apps except Vaultwarden. The model it pulls is `llama3.2:3b`. Tags that contain `-text-` are refused. The firewall drops incoming traffic, allows outgoing traffic, and opens Nomad 8080, Jellyfin 8490, Kiwix 8090, and Meshtastic Web 9443 only to 192.168.0.0/16 and 10.0.0.0/8. Ollama and Open WebUI stay on localhost. Snapper keeps four numbered snapshots.

GIMP, Krita, Kdenlive, Audacity, OBS, Calibre, KiCad, Arduino, PlatformIO, the KDE games, RetroArch, PeaZip, GitHub Desktop, Brave, Signal, VS Code, VirtualBox, and Grok Bot download on first boot when the network is up. They are not inside the ISO.

## Known issues

- Kismet, SpeedCrunch, FoxtrotGPS, Briar, and VeraCrypt are not in Debian 13. This image does not add an unsigned repository for them.
- A WPA2/WPA3 mixed router, including some Starlink setups, can still drop after it associates. Set that connection to WPA2 (wpa-psk).
- The Knowledge Base upload and a full `llama3.2:3b` chat were not run on hardware in this build. QEMU has no GPU.
- VirtualBox, if you install the extras, expects Secure Boot to stay off.

## Testers wanted

Please try this ISO and send a hardware test report if you have:

- an NVIDIA GPU
- an Intel CPU or Intel graphics
- an older PC or laptop than a 2024 Ryzen

Richard's Asus Vivobook S16 (Ryzen AI 9 HX 370, Radeon 890M, MT7922) installed and ran build 2. Wi-Fi and Ethernet stayed up on that machine. Audio on that laptop was not in the report.
