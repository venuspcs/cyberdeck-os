# Contributing to Cyberdeck OS

Thank you for helping. Cyberdeck OS is free for anyone building a cyberdeck. Richard Colbert ([@VeteranPrepper](https://x.com/VeteranPrepper) on X) maintains the project.

**Status: planning / pre-alpha.** The repository holds the spec and empty directories. It does not build an image.

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).

## What helps right now

- Read [docs/SPEC.md](docs/SPEC.md) and send corrections, missing hardware constraints, or clearer wording as a pull request.
- File a [hardware report](.github/ISSUE_TEMPLATE/hardware_report.md) for a machine you want the OS to boot, especially cyberdeck boards, handhelds, radios, and GPUs or NPUs.
- Draft a How-To chapter from the outline in [docs/guide/README.md](docs/guide/README.md). Keep it accurate to the spec, and leave it marked as unfinished if the image does not exist yet to verify the steps.
- File a [feature request](.github/ISSUE_TEMPLATE/feature_request.md) when a change belongs in the spec.

## What to hold until a milestone starts

Do not add files that look like a working build:

- live-build `config/` trees, package lists, or hooks that `lb build` would consume
- Calamares configuration
- first-boot shell scripts, systemd units, or compose files
- GitHub Actions workflows that claim to produce an ISO
- branding images standing in for artwork that does not exist yet
- binary disk images, ISOs, or kernel trees

Those belong in the milestone that produces a real image. The checklist is [docs/ROADMAP.md](docs/ROADMAP.md). A pull request that adds them early should explain why the spec says the work can start.

## Licenses

- Code, build configuration, and scripts are GNU GPLv3. See [LICENSE](LICENSE). New code files should carry a short GPLv3 notice and a copyright line.
- Documentation under `docs/`, including the How-To, is CC BY 4.0. See [LICENSE-docs](LICENSE-docs). If you contribute to `docs/`, you license that contribution under CC BY 4.0.

There is no separate contributor license agreement.

## Spec changes

Behavior lives in `docs/SPEC.md`. If a pull request changes what the OS does, update the spec in the same pull request and say why in the description. The roadmap checklist should match.

## Pull requests

- Use a focused branch and a description that says which spec section or roadmap item you touched.
- Keep planning-only changes free of executable build code.
- The pull request template lists the checks.

## Issues

- A bug in the spec, the docs, or (later) an image: [bug report](.github/ISSUE_TEMPLATE/bug_report.md).
- A machine, radio, or cyberdeck: [hardware report](.github/ISSUE_TEMPLATE/hardware_report.md).
- A new capability: [feature request](.github/ISSUE_TEMPLATE/feature_request.md).

## Security

Report vulnerabilities through [SECURITY.md](SECURITY.md). Please do not file an unfixed vulnerability as a public issue.

## Conduct reports

Report conduct issues to Richard Colbert by direct message on X at [@VeteranPrepper](https://x.com/VeteranPrepper), as the [Code of Conduct](CODE_OF_CONDUCT.md) describes. A public issue is the wrong place for that report.
