#!/usr/bin/env python3
"""Open Calamares on the live desktop and screenshot the partition choices.

The desktop launcher is replaced in the running live session with the
Xwayland wrapper, then started as the live user on that display.
"""

import base64
import socket
import subprocess
import time
from pathlib import Path

from PIL import Image

ISO = "/workspace/build/amd64/cyberdeck-os-amd64-amd64.hybrid.iso"
OUT = Path("/tmp/cal")
OVMF = "/usr/share/OVMF/OVMF_CODE_4M.fd"
VARS = "/usr/share/OVMF/OVMF_VARS_4M.fd"
WRAPPER = Path("/workspace/installer/calamares-install-debian").read_text()
BRANDING = Path("/workspace/installer/calamares/branding.desc").read_text()


def start(extra, port, mon):
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
    time.sleep(0.2)
    s.close()


def shot(mon_path, png: Path):
    ppm = str(png) + ".ppm"
    mon(mon_path, f"screendump {ppm}")
    time.sleep(0.8)
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
    time.sleep(0.25)


def send_script(sock, name, body):
    payload = base64.b64encode(body.encode()).decode()
    # Keep each write short so the serial line does not drop characters.
    send(sock, f"rm -f {name}")
    for i in range(0, len(payload), 200):
        send(sock, f"printf '%s' '{payload[i:i+200]}' >> {name}.b64")
    send(sock, f"base64 -d {name}.b64 > {name} && chmod 755 {name} && echo WROTE_{Path(name).name}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    mon_path = str(OUT / "cal.mon")
    proc = start(["-cdrom", ISO, "-boot", "order=d"], 4490, mon_path)
    sock = connect_serial(4490)
    time.sleep(8)
    for _ in range(5):
        mon(mon_path, "sendkey ret")
        time.sleep(2)
    log = wait_token(sock, "login:", 180)
    print("login", b"login:" in log, flush=True)
    if b"login:" not in log:
        proc.kill()
        return 1
    time.sleep(20)
    shot(mon_path, OUT / "00-desktop.png")
    send(sock, "cyberdeck")
    time.sleep(1)
    send(sock, "cyberdeck")
    time.sleep(3)
    send(
        sock,
        "pid=$(pgrep -u cyberdeck -n plasmashell); "
        "tr '\\0' '\\n' < /proc/$pid/environ | grep -E '^(DISPLAY|XAUTHORITY|WAYLAND_DISPLAY|XDG_RUNTIME_DIR)=' "
        "| tee /tmp/session-env; echo ENV_DONE",
    )
    env = wait_token(sock, "ENV_DONE", 20)
    (OUT / "session-env.txt").write_bytes(env)
    print(env.decode("utf-8", "replace")[-500:], flush=True)
    send_script(sock, "/tmp/calamares-install-debian", WRAPPER)
    wrote = wait_token(sock, "WROTE_calamares-install-debian", 30)
    print("wrapper", b"WROTE_calamares-install-debian" in wrote, flush=True)
    send_script(sock, "/tmp/branding.desc", BRANDING)
    branded = wait_token(sock, "WROTE_branding.desc", 30)
    print("branding", b"WROTE_branding.desc" in branded, flush=True)
    send(sock, "sudo -n cp /tmp/calamares-install-debian /usr/bin/calamares-install-debian")
    send(sock, "sudo -n cp /tmp/branding.desc /etc/calamares/branding/cyberdeck/branding.desc")
    time.sleep(1)
    # Close Welcome Center so it does not cover the installer.
    mon(mon_path, "sendkey alt-f4")
    time.sleep(1)
    send(
        sock,
        "sudo -u cyberdeck bash -lc 'set -a; . /tmp/session-env; set +a; "
        "nohup /usr/bin/calamares-install-debian > /tmp/cal-launch.txt 2>&1 & echo STARTED'",
    )
    started = wait_token(sock, "STARTED", 20)
    print("started", b"STARTED" in started, flush=True)
    time.sleep(12)
    shot(mon_path, OUT / "01-launched.png")
    send(sock, "echo LAUNCHLOG; cat /tmp/cal-launch.txt; echo LOGEND; ps -C calamares -o pid,cmd; echo PSEND")
    info = wait_token(sock, "PSEND", 20)
    (OUT / "launch.txt").write_bytes(info)
    print(info.decode("utf-8", "replace")[-1500:], flush=True)
    # Walk forward. Enter activates the focused Next button.
    for name in (
        "02-next-1.png",
        "03-next-2.png",
        "04-next-3.png",
        "05-next-4.png",
        "06-partition.png",
    ):
        mon(mon_path, "sendkey ret")
        time.sleep(2)
        shot(mon_path, OUT / name)
    # Partition choices are a radio list. Down selects the next one.
    for name in ("07-choice-down-1.png", "08-choice-down-2.png", "09-choice-down-3.png"):
        mon(mon_path, "sendkey down")
        time.sleep(1.2)
        shot(mon_path, OUT / name)
    sock.close()
    proc.terminate()
    try:
        proc.wait(timeout=20)
    except subprocess.TimeoutExpired:
        proc.kill()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
