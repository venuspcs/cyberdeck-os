# Changelog

Draft notes for the next image. Nothing here is a published GitHub Release until that image is tagged.

## Beta 1 (Plow)

### Automatic multi-WAN load balancing

When two or more internet connections are up at once, such as wired Ethernet plus Wi-Fi or a USB tether, Cyberdeck OS spreads new outbound connections across the healthy ones. Each link keeps its own gateway. A link that cannot reach the internet is left out of the route, and a link that drops is removed so later connections fail over. One healthy link uses ordinary routing. A VPN that takes the default route is left in charge.

This is per-flow ECMP, not single-stream bonding. The kernel hashes each connection, including its ports, so two downloads can use two links. One download is not split across links.

It is on by default. `cyberdeck-multiwan status` shows the links. Set `ENABLED=no` in `/etc/cyberdeck/multiwan.conf`, or run `sudo cyberdeck-multiwan off`, to turn it off.

### Meshtastic web server

`meshtasticd` listens for Meshtastic Web on https://localhost:9443. Accept the self-signed certificate once. The TCP API on port 4403, and port 9443, are open to localhost and the local network only.
