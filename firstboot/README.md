# firstboot/

Reserved for the first-boot Project Nomad installer and the `/library` drive setup.

When it is written, this installer will:

- install Project Nomad and its containers
- if the user picks the boot drive, create a `/library` directory there
- if the user picks another drive, offer to format it or use it as-is, mount it by UUID in `/etc/fstab`, and start Docker only after `/library` is mounted
- leave Nomad admin on port 8080 and Open WebUI on port 3000
- bind Ollama to localhost port 11434
- offer a one-click ROCm or CUDA install when that hardware is detected, then configure Ollama for it

The live session also has to make Nomad usable. How that session shares this installer is an open milestone 1 decision, recorded in the spec.

**There is no installer here.** No shell script, no systemd unit, and no Docker compose file. Adding a script that looks ready to run would pretend this step works.

Requirements: [docs/SPEC.md](../docs/SPEC.md), sections 5, 8, and 10.
