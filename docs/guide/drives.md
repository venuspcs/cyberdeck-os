# Drives and Project Nomad

**Status: written for Beta 1 (Plow).**

Project Nomad Setup asks where `/library` lives, writes it to fstab by UUID, and orders Docker after that mount. It then starts Nomad admin on port 8080 of this computer, with no password. From another computer on the local network, use https://&lt;this-computer&gt;:8443. Accept the certificate once and sign in with a Cyberdeck administrator account. Open WebUI for people is https://127.0.0.1:3443 here and https://&lt;this-computer&gt;:3443 on the LAN. The desktop icon opens the local address. Port 3000 is only the internal backend. Ollama is on `127.0.0.1:11434`, Dozzle on `127.0.0.1:9999`, and Qdrant on `127.0.0.1:6333`.

It also starts the Supply Depot apps except Vaultwarden: Kiwix (8090), Kolibri, Flatnotes, CyberChef, Stirling PDF, File Browser, Calibre Web, IT Tools, Excalidraw, Homebox, Jellyfin (8490), LibreTranslate, Meshtastic Web container (9445), and MeshCore Web (9444). The meshtasticd web page itself is https://localhost:9443. Accept its certificate once. Each image is pulled on its own, with retries, and a failure is listed at the end instead of cancelling the others. Their data directories are under `/library/nomad/storage`. Qdrant's directory is mode 777 so the container can write it.

The firewall allows those published LAN ports only from `192.168.0.0/16` and `10.0.0.0/8`. Ollama, Open WebUI, Dozzle, and Qdrant stay on localhost.

The default model pull is `llama3.2:3b`. After Qdrant answers `http://127.0.0.1:6333/healthz`, upload a document in the Knowledge Base and ask the 3b model about it.

This guide is licensed under [CC BY 4.0](../../LICENSE-docs).
