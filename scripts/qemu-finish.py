#!/usr/bin/env python3
"""Finish the boot test: press Enter through the menu, launch Calamares, install, boot the disk."""

import shutil
import socket
import subprocess
import time
from pathlib import Path

from PIL import Image

ISO = "/workspace/build/amd64/cyberdeck-os-amd64-amd64.hybrid.iso"
OUT = Path("/tmp/cyberdeck-qemu")
OVMF_CODE = "/usr/share/OVMF/OVMF_CODE_4M.fd"
OVMF_VARS_SRC = "/usr/share/OVMF/OVMF_VARS_4M.fd"


def qemu(extra, serial_port, mon):
    return subprocess.Popen(
        [
            "qemu-system-x86_64",
            "-enable-kvm",
            "-cpu",
            "host",
            "-m",
            "3072",
            "-smp",
            "2",
            "-vga",
            "virtio",
            "-serial",
            f"tcp:127.0.0.1:{serial_port},server=on,wait=off",
            "-monitor",
            f"unix:{mon},server=on,wait=off",
            "-display",
            "none",
            "-no-reboot",
            *extra,
        ]
    )


def mon_cmd(mon, cmd):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(10)
    s.connect(mon)
    try:
        s.recv(2048)
    except socket.timeout:
        pass
    s.sendall((cmd + "\n").encode())
    time.sleep(0.3)
    s.close()


def shot(mon, png):
    ppm = png.with_suffix(".ppm")
    mon_cmd(mon, f"screendump {ppm}")
    time.sleep(0.8)
    if ppm.exists():
        Image.open(ppm).save(png)
        print("shot", png, flush=True)


def serial_conn(port):
    for _ in range(30):
        try:
            return socket.create_connection(("127.0.0.1", port), timeout=5)
        except OSError:
            time.sleep(0.5)
    raise SystemExit(f"no serial on {port}")


def read_for(sock, seconds):
    sock.settimeout(1)
    data = b""
    end = time.time() + seconds
    while time.time() < end:
        try:
            chunk = sock.recv(8192)
        except socket.timeout:
            continue
        if not chunk:
            break
        data += chunk
    return data.decode("utf-8", "replace")


def send(sock, line):
    sock.sendall((line + "\n").encode())
    time.sleep(0.5)


def boot_menu(mon, seconds=20):
    end = time.time() + seconds
    while time.time() < end:
        mon_cmd(mon, "sendkey ret")
        time.sleep(3)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # 1. BIOS live: menu, plasma, calamares
    mon = str(OUT / "cal.mon")
    proc = qemu(["-cdrom", ISO, "-boot", "order=d"], 4450, mon)
    sock = serial_conn(4450)
    time.sleep(8)
    boot_menu(mon, 12)
    shot(mon, OUT / "bios-menu.png")
    log = read_for(sock, 150)
    (OUT / "cal-serial.txt").write_text(log)
    time.sleep(40)
    shot(mon, OUT / "bios-plasma.png")
    # serial login may already be up
    send(sock, "")
    time.sleep(1)
    chunk = read_for(sock, 3)
    if "login:" in chunk or "login:" in log:
        send(sock, "cyberdeck")
        time.sleep(1)
        send(sock, "cyberdeck")
        time.sleep(2)
    else:
        # try anyway
        send(sock, "cyberdeck")
        time.sleep(1)
        send(sock, "cyberdeck")
        time.sleep(2)
    send(sock, "echo SESSION=$(loginctl show-session $(loginctl | awk '/cyberdeck/{print $1; exit}') -p Type --value 2>/dev/null); echo WAY=$(ps -eo args | grep -m1 startplasma || true); echo MARK_SESSION")
    sess = ""
    end = time.time() + 20
    buf = b""
    sock.settimeout(1)
    while time.time() < end:
        try:
            buf += sock.recv(4096)
        except socket.timeout:
            pass
        if b"MARK_SESSION" in buf:
            break
    (OUT / "session.txt").write_text(buf.decode("utf-8", "replace"))
    send(sock, "sudo -n xhost +si:localuser:root >/tmp/xhost.txt 2>&1 || true")
    send(sock, "sudo -n bash -lc 'DISPLAY=:0 QT_QPA_PLATFORM=xcb calamares >/tmp/calamares.log 2>&1 &'")
    time.sleep(20)
    shot(mon, OUT / "bios-calamares.png")
    send(sock, "ps -C calamares -o pid,cmd; echo CAL_DONE")
    end = time.time() + 15
    buf = b""
    while time.time() < end:
        try:
            buf += sock.recv(4096)
        except socket.timeout:
            pass
        if b"CAL_DONE" in buf:
            break
    (OUT / "calamares-ps.txt").write_text(buf.decode("utf-8", "replace"))
    sock.close()
    proc.terminate()
    proc.wait(timeout=20)

    # 2. Install
    disk = str(OUT / "install.qcow2")
    subprocess.run(["qemu-img", "create", "-f", "qcow2", disk, "20G"], check=True)
    vars_path = str(OUT / "OVMF_VARS_install2.fd")
    shutil.copy(OVMF_VARS_SRC, vars_path)
    mon = str(OUT / "inst.mon")
    proc = qemu(
        [
            "-drive",
            f"if=pflash,format=raw,readonly=on,file={OVMF_CODE}",
            "-drive",
            f"if=pflash,format=raw,file={vars_path}",
            "-cdrom",
            ISO,
            "-drive",
            f"file={disk},format=qcow2,if=virtio",
            "-boot",
            "order=d",
        ],
        4451,
        mon,
    )
    sock = serial_conn(4451)
    time.sleep(12)
    boot_menu(mon, 15)
    log = read_for(sock, 180)
    (OUT / "inst-serial.txt").write_text(log)
    send(sock, "cyberdeck")
    time.sleep(1)
    send(sock, "cyberdeck")
    time.sleep(2)
    send(sock, "sudo -n cyberdeck-autoinstall; echo AUTOINSTALL_DONE:$?")
    end = time.time() + 800
    buf = b""
    sock.settimeout(2)
    while time.time() < end:
        try:
            buf += sock.recv(8192)
        except socket.timeout:
            pass
        if b"AUTOINSTALL_DONE:" in buf:
            break
    (OUT / "autoinstall.txt").write_text(buf.decode("utf-8", "replace"))
    sock.close()
    try:
        proc.wait(timeout=60)
    except subprocess.TimeoutExpired:
        proc.kill()

    if b"AUTOINSTALL_DONE:0" not in buf:
        print("autoinstall failed")
        return 1

    mon = str(OUT / "disk.mon")
    proc = qemu(
        [
            "-drive",
            f"if=pflash,format=raw,readonly=on,file={OVMF_CODE}",
            "-drive",
            f"if=pflash,format=raw,file={vars_path}",
            "-drive",
            f"file={disk},format=qcow2,if=virtio",
            "-boot",
            "order=c",
        ],
        4452,
        mon,
    )
    sock = serial_conn(4452)
    log = read_for(sock, 180)
    (OUT / "disk-serial.txt").write_text(log)
    time.sleep(15)
    shot(mon, OUT / "installed-boot.png")
    send(sock, "cyberdeck")
    time.sleep(1)
    send(sock, "cyberdeck")
    time.sleep(2)
    send(sock, "findmnt -no FSTYPE,SOURCE /; findmnt -no FSTYPE,SOURCE /boot/efi; lsblk -o NAME,FSTYPE,SIZE,PARTTYPENAME; echo LAYOUT_DONE")
    end = time.time() + 30
    buf = b""
    sock.settimeout(1)
    while time.time() < end:
        try:
            buf += sock.recv(4096)
        except socket.timeout:
            pass
        if b"LAYOUT_DONE" in buf:
            break
    (OUT / "layout.txt").write_text(buf.decode("utf-8", "replace"))
    print(buf.decode("utf-8", "replace"))
    sock.close()
    proc.terminate()
    proc.wait(timeout=20)
    return 0 if b"btrfs" in buf and b"vfat" in buf else 1


if __name__ == "__main__":
    raise SystemExit(main())
