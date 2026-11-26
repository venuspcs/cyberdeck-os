# build/

Future home of the live-build configuration, split by architecture.

| Directory | Image |
| --- | --- |
| [amd64/](amd64/README.md) | AMD64 live and installer ISO (first image) |
| [arm64/](arm64/README.md) | Generic ARM64 UEFI image for laptops, desktops, and boards |

Phone, tablet, and Raspberry Pi 5 images are device builds. They live under [devices/](../devices/README.md), not here.

**Nothing in this tree builds an image.** There is no `config/`, no `auto/config`, no hooks, and no GitHub Actions workflow. Those arrive with [milestone 1](../docs/ROADMAP.md), when there is a real config to run. Do not add a script that calls `lb build` until that config exists.

Requirements: [docs/SPEC.md](../docs/SPEC.md).
