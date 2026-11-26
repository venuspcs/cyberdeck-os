# firstboot/

The first-boot Project Nomad installer and the stubs around it.

`cyberdeck-nomad-setup` asks whether `/library` is a folder on the boot drive or another disk. Another disk can be formatted as Btrfs or used as-is. The mount is written to `fstab` by UUID, and Docker is ordered with `RequiresMountsFor=/library`. The compose file it writes keeps Nomad admin on port 8080, Open WebUI on port 3000, and Ollama on `127.0.0.1:11434`. If an NVIDIA or AMD display device is present it offers a one-click package install (NVIDIA driver and CUDA toolkit, or Debian's `rocminfo` for AMD). Container images are pulled only when the user says yes and a network is up.

`cyberdeck-welcome` and `cyberdeck-control-panel` are stubs. Welcome prints the TODO for themes, Wi-Fi, and the password screen, then runs the Nomad installer. Calamares collects the account password. NetworkManager is on the image for Wi-Fi.

Nothing here is a finished Welcome app or Control Panel.

Requirements: [docs/SPEC.md](../docs/SPEC.md), sections 5, 8, and 10.
