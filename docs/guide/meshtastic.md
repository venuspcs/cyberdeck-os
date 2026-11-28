# Meshtastic

**Status: written for Beta 1 (Plow).**

`meshtasticd` is installed from the Meshtastic repository configured for Debian 13. Its web server listens on port 9443 with a self-signed certificate that is created the first time the service starts. Open https://localhost:9443 and accept that certificate once. The TCP API listens on port 4403. Both ports are reachable from this computer and from the local network, and the firewall drops them from the public internet. The Supply Depot Meshtastic Web container, if you install it, is on port 9445 so it does not take 9443. MeshCore Web is on port 9444 when its image can be pulled. Vaultwarden is not installed.

This guide is licensed under [CC BY 4.0](../../LICENSE-docs).
