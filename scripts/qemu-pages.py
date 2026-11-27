#!/usr/bin/env python3
"""Open Calamares on a disk and screenshot the partition choices."""

import base64
import socket
import subprocess
import time
from pathlib import Path

from PIL import Image

ISO = "/workspace/build/amd64/cyberdeck-os-amd64-amd64.hybrid.iso"
OUT = Path("/tmp/pages")
OVMF = "/usr/share/OVMF/OVMF_CODE_4M.fd"
VARS = "/usr/share/OVMF/OVMF_VARS_4M.fd"
WRAPPER = Path("/workspace/installer/calamares-install-debian").read_text()
BRANDING = Path("/workspace/installer/calamares/branding.desc").read_text()
MON = str(OUT / "live.mon")


def start():
    disk = str(OUT / "disk.qcow2")
    if not Path(disk).exists():
        subprocess.run(["qemu-img", "create", "-f", "qcow2", disk, "20G"], check=True)
    vars_path = str(OUT / "vars.fd")
    subprocess.run(["cp", VARS, vars_path], check=True)
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
            "-device",
            "virtio-tablet-pci",
            "-serial",
            "tcp:127.0.0.1:4522,server=on,wait=off",
            "-monitor",
            f"unix:{MON},server=on,wait=off",
            "-display",
            "none",
            "-nic",
            "user",
            "-drive",
            f"if=pflash,format=raw,readonly=on,file={OVMF}",
            "-drive",
            f"if=pflash,format=raw,file={vars_path}",
            "-cdrom",
            ISO,
            "-drive",
            f"file={disk},format=qcow2,if=virtio",
            "-boot",
            "order=d",
        ]
    )


def connect():
    for _ in range(40):
        try:
            return socket.create_connection(("127.0.0.1", 4522), timeout=5)
        except OSError:
            time.sleep(0.4)
    raise SystemExit("no serial")


def mon(cmd):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(8)
    s.connect(MON)
    try:
        s.recv(1024)
    except socket.timeout:
        pass
    s.sendall((cmd + "\n").encode())
    time.sleep(0.1)
    s.close()


def shot(name):
    png = OUT / name
    ppm = str(png) + ".ppm"
    mon(f"screendump {ppm}")
    time.sleep(0.45)
    Image.open(ppm).save(png)
    print("shot", name, flush=True)


def click(x, y):
    mon(f"mouse_move {x} {y}")
    time.sleep(0.12)
    mon("mouse_button 1")
    time.sleep(0.05)
    mon("mouse_button 0")
    time.sleep(1.5)


def wait_token(sock, token, seconds):
    sock.settimeout(1)
    data = b""
    end = time.time() + seconds
    while time.time() < end:
        try:
            chunk = sock.recv(65536)
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
    time.sleep(0.15)


def send_script(sock, name, body):
    payload = base64.b64encode(body.encode()).decode()
    send(sock, f"rm -f {name} {name}.b64")
    for i in range(0, len(payload), 180):
        send(sock, f"printf '%s' '{payload[i:i+180]}' >> {name}.b64")
    marker = "WROTE_" + Path(name).name.replace(".", "_")
    send(sock, f"base64 -d {name}.b64 > {name} && chmod 755 {name} && echo {marker}")
    got = wait_token(sock, marker, 30)
    print(marker, marker.encode() in got, flush=True)
    return marker.encode() in got


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    proc = start()
    sock = connect()
    time.sleep(8)
    for _ in range(4):
        mon("sendkey ret")
        time.sleep(1.5)
    log = wait_token(sock, "login:", 180)
    print("login", b"login:" in log, flush=True)
    if b"login:" not in log:
        proc.kill()
        return 1
    time.sleep(18)
    send(sock, "cyberdeck")
    time.sleep(0.7)
    send(sock, "cyberdeck")
    time.sleep(2)
    prep = """#!/bin/sh
parted -s /dev/vda mklabel gpt mkpart keep ext4 1MiB 4096MiB
mkfs.ext4 -F -L keep /dev/vda1
echo DISK_READY
"""
    if not send_script(sock, "/tmp/prep.sh", prep):
        return 1
    send(sock, "sudo -n sh /tmp/prep.sh")
    ready = wait_token(sock, "DISK_READY", 40)
    print("disk", b"DISK_READY" in ready, flush=True)
    send(
        sock,
        "pid=$(pgrep -u cyberdeck -n plasmashell); "
        "tr '\\0' '\\n' < /proc/$pid/environ | "
        "grep -E '^(DISPLAY|XAUTHORITY|WAYLAND_DISPLAY|XDG_RUNTIME_DIR)=' | tee /tmp/session-env",
    )
    env = wait_token(sock, "XDG_RUNTIME_DIR=", 20)
    print(env.decode("utf-8", "replace")[-300:], flush=True)
    if not send_script(sock, "/tmp/calamares-install-debian", WRAPPER):
        return 1
    if not send_script(sock, "/tmp/branding.desc", BRANDING):
        return 1
    send(sock, "sudo -n cp /tmp/calamares-install-debian /usr/bin/calamares-install-debian")
    send(sock, "sudo -n cp /tmp/branding.desc /etc/calamares/branding/cyberdeck/branding.desc")
    time.sleep(0.5)
    mon("sendkey alt-f4")
    time.sleep(0.8)
    send(
        sock,
        "sudo -u cyberdeck bash -lc 'set -a; . /tmp/session-env; set +a; "
        "nohup /usr/bin/calamares-install-debian > /tmp/cal-launch.txt 2>&1 & echo STARTED'",
    )
    wait_token(sock, "STARTED", 15)
    time.sleep(12)
    shot("01-welcome.png")
    send(sock, "echo LAUNCHLOG; cat /tmp/cal-launch.txt; echo LOGEND; ps -C calamares -o pid,cmd; echo PSEND")
    info = wait_token(sock, "PSEND", 15)
    (OUT / "launch.txt").write_bytes(info)
    print(info.decode("utf-8", "replace")[-800:], flush=True)
    # Next button measured on a 1280x800 frame: window 1024x580+129+116.
    for name in ("02-location.png", "03-keyboard.png", "04-partitions.png"):
        click(1008, 678)
        shot(name)
    print("PAGES_READY", flush=True)
    time.sleep(180)
    proc.terminate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
