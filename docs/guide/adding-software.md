# Adding software

**Status: written for Beta 1 (Plow).**

Debian packages install with apt. The host sources are Debian 13 (main, contrib, non-free, non-free-firmware), updates, security, and backports. Do not add Ubuntu, Sid, or Testing.

These are already in the full image: the network tools (nmap, zenmap, Wireshark, tcpdump, and the rest of that set except Kismet), qBittorrent, Tor Browser launcher, KeePassXC, Syncthing, GParted, Okular, BleachBit, Remmina, FileZilla, Ark, 7-Zip, Xarchiver, KCalc, Qalculate!, Galculator, the build tools, Git, Rust from Debian, Node, Go, the radio tools that Debian ships (JS8Call, Pat, Dire Wolf, Xastir, gpsd), WireGuard, ClamAV, Lynis, cool-retro-term, btop, Conky, and Foliate.

GIMP, Krita, Kdenlive, Audacity, OBS Studio, Calibre, KiCad, Arduino, PlatformIO, the KDE games set, RetroArch, PeaZip, GitHub Desktop, Brave, Signal, VS Code, VirtualBox, and Grok Bot install when the machine is online. Open **Install Extras** or wait for its timer. They are not copied into the ISO because of size or license.

Kismet, SpeedCrunch, FoxtrotGPS, Briar, and VeraCrypt are not in Debian 13 and this image does not add an unsigned repository for them.

Chrome and Grok Bot come from their publishers' apt repositories. The packages are not stored in the ISO.

This guide is licensed under [CC BY 4.0](../../LICENSE-docs).
