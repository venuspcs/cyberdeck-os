# Drives and `/library`

**Status: stub.** This chapter is not written.

This chapter will cover the first-boot drive choice. On the boot drive, the installer creates a `/library` folder. On another drive, it offers to format the disk or to use it as-is, then mounts it by UUID in `fstab` and starts Docker only after `/library` is mounted. The chapter will also cover moving `/library` later from the Cyberdeck Control Panel.

Requirements: [the specification](../SPEC.md), section 8.

This guide is licensed under [CC BY 4.0](../../LICENSE-docs).
