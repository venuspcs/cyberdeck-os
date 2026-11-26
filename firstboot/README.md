# firstboot/

Reserved for the first-boot Welcome app.

When it is written, Welcome will ask the user to:

1. Choose Daybreak or Nightwatch, and optionally turn on automatic sunrise/sunset switching.
2. Pick the drive that holds `/library`. The boot drive gets a `/library` directory. Another drive can be formatted or used as-is, then mounted by UUID in `/etc/fstab`, with Docker starting only after `/library` is mounted.
3. Join Wi-Fi. This step can be skipped.
4. Install ROCm or CUDA when that hardware is present, then configure Ollama. This step can be skipped. Ollama stays on localhost port 11434.
5. Set the account password.

Welcome then installs Project Nomad and its containers. Nomad admin stays on port 8080. Open WebUI stays on port 3000.

The live desktop also has to make Nomad usable. That session requirement is in the spec. This directory is the installed system's first-boot path.

**There is no Welcome app here.** No shell script, no systemd unit, and no Docker compose file. Adding a script that looks ready to run would pretend this step works.

Requirements: [docs/SPEC.md](../docs/SPEC.md), sections 5, 8, and 10.
