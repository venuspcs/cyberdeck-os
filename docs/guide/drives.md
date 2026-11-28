# Drives and Project Nomad

**Status: written for Beta 1 (Plow).**

Project Nomad Setup asks where `/library` lives, writes it to fstab by UUID, and orders Docker after that mount. It then starts Nomad admin on port 8080, Open WebUI on `127.0.0.1:3000`, Ollama on `127.0.0.1:11434`, Dozzle logs on `127.0.0.1:9999`, and Qdrant on `127.0.0.1:6333`.

It also starts the Supply Depot apps except Vaultwarden: Kiwix (8090), Kolibri, Flatnotes, CyberChef, Stirling PDF, File Browser, Calibre Web, IT Tools, Excalidraw, Homebox, Jellyfin (8490), LibreTranslate, Meshtastic Web (9443), and MeshCore Web (9444). Each image is pulled on its own, with retries, and a failure is listed at the end instead of cancelling the others. Their data directories are under `/library/nomad/storage`. Qdrant's directory is mode 777 so the container can write it.

The firewall allows those published LAN ports only from `192.168.0.0/16` and `10.0.0.0/8`. Ollama, Open WebUI, Dozzle, and Qdrant stay on localhost.

The default model pull is `llama3.2:3b`. After Qdrant answers `http://127.0.0.1:6333/healthz`, upload a document in the Knowledge Base and ask the 3b model about it.

This guide is licensed under [CC BY 4.0](../../LICENSE-docs).
