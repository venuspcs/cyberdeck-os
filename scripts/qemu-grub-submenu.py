#!/usr/bin/env python3
"""Open the Cyberdeck OS snapshots submenu and screenshot it."""

import socket
import subprocess
import time
from pathlib import Path

from PIL import Image

OUT = Path("/tmp/m1")
DISK = str(OUT / "erase.qcow2")
VARS = str(OUT / "vars-erase.fd")
OVMF = "/usr/share/OVMF/OVMF_CODE_4M.fd"
MON = str(OUT / "submenu.mon")


def mon(cmd):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(8)
    s.connect(MON)
    try:
        s.recv(1024)
    except socket.timeout:
        pass
    s.sendall((cmd + "\n").encode())
    time.sleep(0.15)
    s.close()


def shot(name):
    png = OUT / name
    ppm = str(png) + ".ppm"
    mon(f"screendump {ppm}")
    time.sleep(0.5)
    Image.open(ppm).save(png)
    print("shot", name, flush=True)


def main():
    proc = subprocess.Popen(
        [
            "qemu-system-x86_64",
            "-enable-kvm",
            "-cpu",
            "host",
            "-m",
            "2048",
            "-smp",
            "2",
            "-vga",
            "virtio",
            "-monitor",
            f"unix:{MON},server=on,wait=off",
            "-display",
            "none",
            "-nic",
            "none",
            "-drive",
            f"if=pflash,format=raw,readonly=on,file={OVMF}",
            "-drive",
            f"if=pflash,format=raw,file={VARS}",
            "-drive",
            f"file={DISK},format=qcow2,if=virtio",
            "-boot",
            "order=c",
        ]
    )
    time.sleep(6)
    shot("26-menu-before-keys.png")
    # GNU/Linux, Advanced, UEFI Firmware, Cyberdeck OS snapshots.
    for _ in range(3):
        mon("sendkey down")
        time.sleep(0.3)
    shot("27-snapshots-highlighted.png")
    mon("sendkey ret")
    time.sleep(1)
    shot("28-snapshots-submenu.png")
    proc.terminate()
    try:
        proc.wait(timeout=15)
    except subprocess.TimeoutExpired:
        proc.kill()


if __name__ == "__main__":
    main()
