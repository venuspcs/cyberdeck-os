# Other systems with Distrobox

**Status: short guide.**

Cyberdeck OS keeps one Debian system on the disk. When a program is packaged for Ubuntu, Arch, or another distribution, run it in a container instead of adding that distribution's package repository to the host.

The image includes Distrobox and Podman.

Create an Ubuntu container and open a shell in it:

```sh
distrobox create --name ubuntu --image ubuntu:24.04
distrobox enter ubuntu
```

Arch is the same idea:

```sh
distrobox create --name arch --image archlinux:latest
distrobox enter arch
```

Programs installed inside the container stay there. The host apt sources stay Debian 13, plus the vendor repositories Cyberdeck OS configures (Google Chrome, Docker CE, and Meshtastic). Do not add Ubuntu, Debian Sid, or Debian Testing repositories to the host.

Requirements: [the specification](../SPEC.md), section 9.
