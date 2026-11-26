# Security policy

Cyberdeck OS is **planning / pre-alpha**. No image has been released, and the repository has no installer, first-boot program, or image build yet. There are no supported releases.

| Version | Supported |
| --- | --- |
| planning / pre-alpha (no release) | No image to patch |
| Future GitHub Releases | Will be listed here when the first image is published |

## Reporting a vulnerability

Please report a vulnerability in private.

1. Open a draft security advisory on this repository: <https://github.com/venuspcs/cyberdeck-os/security/advisories/new>
2. If private advisories are unavailable, send a direct message to Richard Colbert on X at [@VeteranPrepper](https://x.com/VeteranPrepper).

Include what is affected, what an attacker could do, and how you found it. You do not need to write an exploit.

Please do not open a public GitHub issue for an unfixed vulnerability.

Design notes about the future installer, first-boot path, firewall, or update process can be a public issue when they are not a report of an exploitable flaw. Use a [bug report](.github/ISSUE_TEMPLATE/bug_report.md) or a [feature request](.github/ISSUE_TEMPLATE/feature_request.md) for those.

## What we will do

The maintainer will acknowledge a private report, work on a fix before any public write-up, and credit you if you want to be named. There is no bug-bounty program.

Because the project has not shipped an image, a report during this phase is most useful when it describes a flaw in a committed script or a concrete problem in the published spec (for example a default that would expose Ollama beyond localhost). Ollama is specified to bind to localhost port 11434. Nomad admin stays on port 8080 and Open WebUI on port 3000.
