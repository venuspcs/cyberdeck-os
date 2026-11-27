# Repair and rollback

**Status: written for Alpha 3 (Hatchet).**

At the installed GRUB menu, the advanced or main list includes snapshot entries from grub-btrfs after apt has taken a snapshot. Booting a snapshot returns the Btrfs root to that moment. Data you stored only on `/library` is not inside the root snapshot.

If the 7.3 kernel will not boot or Wi-Fi will not associate, choose the `6.12` kernel line instead of a snapshot. That kernel stays installed next to the backports kernel.

This guide is licensed under [CC BY 4.0](../../LICENSE-docs).
