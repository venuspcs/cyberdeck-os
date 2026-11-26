#!/usr/bin/env python3
"""Install the live ISO onto a virtual disk and boot that disk."""

import socket
import subprocess
import time
from pathlib import Path

from PIL import Image

ISO = "/workspace/build/amd64/cyberdeck-os-amd64-amd64.hybrid.iso"
OUT = Path("/tmp/cyberdeck-install")
OVMF_CODE = "/usr/share/OVMF/OVMF_CODE_4M.fd"
OVMF_VARS_SRC = "/usr/share/OVMF/OVMF_VARS_4M.fd"


def start(extra, port, mon):
    proc = subprocess.Popen(
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
            f"tcp:127.0.0.1:{port},server=on,wait=off",
            "-monitor",
            f"unix:{mon},server=on,wait=off",
            "-display",
            "none",
            "-no-reboot",
            *extra,
        ]
    )
    return proc


def mon(mon_path, cmd):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(8)
    s.connect(mon_path)
    try:
        s.recv(1024)
    except socket.timeout:
        pass
    s.sendall((cmd + "\n").encode())
    time.sleep(0.2)
    s.close()


def shot(mon_path, png):
    ppm = str(png) + ".ppm"
    mon(mon_path, f"screendump {ppm}")
    time.sleep(0.6)
    Image.open(ppm).save(png)
    print("shot", png, flush=True)


def connect(port):
    for _ in range(40):
        try:
            return socket.create_connection(("127.0.0.1", port), timeout=5)
        except OSError:
            time.sleep(0.4)
    raise SystemExit("serial down")


def pump(sock, seconds):
    sock.settimeout(1)
    data = b""
    end = time.time() + seconds
    while time.time() < end:
        try:
            data += sock.recv(16384)
        except socket.timeout:
            continue
        if not data.endswith(b"") and False:
            break
    return data


def wait_for(sock, token, seconds):
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
    time.sleep(0.4)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    disk = str(OUT / "disk.qcow2")
    subprocess.run(["qemu-img", "create", "-f", "qcow2", disk, "20G"], check=True)
    vars_path = str(OUT / "vars.fd")
    subprocess.run(["cp", OVMF_VARS_SRC, vars_path], check=True)
    mon_path = str(OUT / "mon.sock")
    proc = start(
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
        4460,
        mon_path,
    )
    sock = connect(4460)
    time.sleep(15)
    for _ in range(6):
        mon(mon_path, "sendkey ret")
        time.sleep(2)
    bootlog = wait_for(sock, "cyberdeck login", 180)
    if b"cyberdeck login" not in bootlog and b"login:" not in bootlog:
        bootlog += pump(sock, 60)
    (OUT / "boot.txt").write_bytes(bootlog)
    shot(mon_path, OUT / "live-desktop.png")
    send(sock, "cyberdeck")
    time.sleep(1)
    send(sock, "cyberdeck")
    time.sleep(2)
    # Launch Calamares on the Wayland session as root.
    send(
        sock,
        "sudo -n env XDG_RUNTIME_DIR=/run/user/1000 WAYLAND_DISPLAY=wayland-0 "
        "QT_QPA_PLATFORM=wayland calamares >/tmp/calamares.log 2>&1 &",
    )
    time.sleep(18)
    shot(mon_path, OUT / "calamares.png")
    send(sock, "ps -C calamares -o pid,cmd > /tmp/cal-ps.txt; echo LAUNCHED")
    launch = wait_for(sock, "LAUNCHED", 15)
    (OUT / "launch.txt").write_bytes(launch)
    send(sock, "sudo -n cyberdeck-autoinstall")
    done = wait_for(sock, "cyberdeck@debian", 900)
    (OUT / "done.txt").write_bytes(done)
    print(done[-400:].decode("utf-8", "replace"), flush=True)
    sock.close()
    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        proc.terminate()
        proc.wait(timeout=20)
    if b"cyberdeck@debian" not in done:
        print("install command did not return")
        return 1
    send(sock, "echo $?")
    code = wait_for(sock, "\n0", 20)
    (OUT / "exitcode.txt").write_bytes(code)
    if b"\n0" not in code and b"\r0" not in code:
        print(code.decode("utf-8", "replace"))
        print("install command failed")
        return 1

    mon_path = str(OUT / "diskmon.sock")
    proc = start(
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
        4461,
        mon_path,
    )
    sock = connect(4461)
    boot = wait_for(sock, "login:", 200)
    (OUT / "installed-boot.txt").write_bytes(boot)
    time.sleep(10)
    shot(mon_path, OUT / "installed.png")
    if b"login:" not in boot:
        print("installed system did not reach a login prompt")
        proc.kill()
        return 1
    send(sock, "cyberdeck")
    time.sleep(1)
    send(sock, "cyberdeck")
    time.sleep(2)
    send(sock, "findmnt -no FSTYPE /; findmnt -no FSTYPE /boot/efi; lsblk -o NAME,FSTYPE,SIZE,PARTTYPENAME; echo LAYOUT_MARKER")
    layout = wait_for(sock, "LAYOUT_MARKER", 30)
    (OUT / "layout.txt").write_bytes(layout)
    print(layout.decode("utf-8", "replace"), flush=True)
    sock.close()
    proc.terminate()
    proc.wait(timeout=20)
    text = layout.decode("utf-8", "replace")
    return 0 if "btrfs" in text and "vfat" in text else 1


if __name__ == "__main__":
    raise SystemExit(main())
