#!/usr/bin/env python3
"""Boot the installed erase disk, snapshot before an update, and shoot GRUB."""

import socket
import subprocess
import time
from pathlib import Path

from PIL import Image

OUT = Path("/tmp/m1")
DISK = str(OUT / "erase.qcow2")
VARS = str(OUT / "vars-erase.fd")
OVMF = "/usr/share/OVMF/OVMF_CODE_4M.fd"


def start(extra, port, mon):
    return subprocess.Popen(
        [
            "qemu-system-x86_64",
            "-enable-kvm",
            "-cpu",
            "host",
            "-m",
            "2560",
            "-smp",
            "2",
            "-vga",
            "virtio",
            "-serial",
            f"tcp:127.0.0.1:{port},server=on,wait=off",
            "-monitor",
            f"unix:{mon},server=on,wait=off",
            "-display",
            "none",
            "-nic",
            "user",
            *extra,
        ]
    )


def connect_serial(port):
    for _ in range(40):
        try:
            return socket.create_connection(("127.0.0.1", port), timeout=5)
        except OSError:
            time.sleep(0.4)
    raise SystemExit(f"no serial {port}")


def mon(path, cmd):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(8)
    s.connect(path)
    try:
        s.recv(1024)
    except socket.timeout:
        pass
    s.sendall((cmd + "\n").encode())
    time.sleep(0.15)
    s.close()


def shot(mon_path, png: Path):
    ppm = str(png) + ".ppm"
    mon(mon_path, f"screendump {ppm}")
    time.sleep(0.6)
    Image.open(ppm).save(png)
    print("shot", png.name, flush=True)


def wait_token(sock, token, seconds):
    sock.settimeout(1)
    data = b""
    end = time.time() + seconds
    while time.time() < end:
        try:
            chunk = sock.recv(16384)
        except socket.timeout:
            continue
        if not chunk:
            break
        data += chunk
        if token.encode() in data:
            return data
    return data


def send(sock, line):
    sock.sendall((line + "\n").encode())
    time.sleep(0.3)


def sudo(cmd):
    # Password is the installed user's. The success token must not appear here.
    return f"printf '%s\\n' cyberdeck | sudo -S -p '' {cmd}"


def boot(port, mon_path, shots):
    proc = start(
        [
            "-drive",
            f"if=pflash,format=raw,readonly=on,file={OVMF}",
            "-drive",
            f"if=pflash,format=raw,file={VARS}",
            "-drive",
            f"file={DISK},format=qcow2,if=virtio",
            "-boot",
            "order=c",
        ],
        port,
        mon_path,
    )
    for delay, name in shots:
        time.sleep(delay)
        shot(mon_path, OUT / name)
    return proc


def main():
    mon_path = str(OUT / "grub1.mon")
    proc = boot(
        4501,
        mon_path,
        ((4, "20-grub-install-snapshot-a.png"), (4, "21-grub-install-snapshot-b.png")),
    )
    sock = connect_serial(4501)
    log = wait_token(sock, "login:", 150)
    print("login", b"login:" in log, flush=True)
    if b"login:" not in log:
        proc.kill()
        return 1
    send(sock, "cyberdeck")
    time.sleep(0.8)
    send(sock, "cyberdeck")
    time.sleep(2)
    send(sock, sudo("apt-get update"))
    upd = wait_token(sock, "Reading package lists", 180)
    (OUT / "apt-update.txt").write_bytes(upd)
    print("apt update", b"Reading package lists" in upd, flush=True)
    send(sock, sudo("apt-get install -y --reinstall ncurses-base"))
    inst = wait_token(sock, "Setting up ncurses-base", 240)
    (OUT / "apt-reinstall.txt").write_bytes(inst)
    print("reinstall", b"Setting up ncurses-base" in inst, flush=True)
    send(sock, sudo("snapper --no-dbus list"))
    snaps = wait_token(sock, "before apt", 40)
    (OUT / "snap-after-apt.txt").write_bytes(snaps)
    print(snaps.decode("utf-8", "replace")[-800:], flush=True)
    send(sock, sudo("update-grub"))
    grub = wait_token(sock, "Found snapshot", 90)
    (OUT / "update-grub.txt").write_bytes(grub)
    print("grub snapshot line", b"Found snapshot" in grub, flush=True)
    print(grub.decode("utf-8", "replace")[-600:], flush=True)
    send(sock, sudo("reboot"))
    time.sleep(2)
    sock.close()
    try:
        proc.wait(timeout=40)
    except subprocess.TimeoutExpired:
        proc.terminate()
        proc.wait(timeout=15)

    mon_path = str(OUT / "grub2.mon")
    proc = boot(
        4502,
        mon_path,
        (
            (3, "22-grub-after-apt-a.png"),
            (3, "23-grub-after-apt-b.png"),
            (4, "24-grub-after-apt-c.png"),
        ),
    )
    # Open the snapshots submenu if it is present: down to it, then right/enter.
    time.sleep(1)
    mon(mon_path, "sendkey down")
    time.sleep(0.4)
    mon(mon_path, "sendkey down")
    time.sleep(0.4)
    mon(mon_path, "sendkey ret")
    time.sleep(1)
    shot(mon_path, OUT / "25-grub-submenu.png")
    proc.terminate()
    try:
        proc.wait(timeout=15)
    except subprocess.TimeoutExpired:
        proc.kill()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
