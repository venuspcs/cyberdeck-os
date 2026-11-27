#!/usr/bin/env python3
"""Calamares partition pages plus an alongside install that keeps a partition."""

import base64
import socket
import subprocess
import time
from pathlib import Path

from PIL import Image

ISO = "/workspace/build/amd64/cyberdeck-os-amd64-amd64.hybrid.iso"
OUT = Path("/tmp/side")
OVMF = "/usr/share/OVMF/OVMF_CODE_4M.fd"
VARS_SRC = "/usr/share/OVMF/OVMF_VARS_4M.fd"
WRAPPER = Path("/workspace/installer/calamares-install-debian").read_text()
BRANDING = Path("/workspace/installer/calamares/branding.desc").read_text()

NAV = r"""#!/bin/sh
xa=$(sed -n 's/^XAUTHORITY=//p' /tmp/session-env)
export DISPLAY=:0
export XAUTHORITY="$xa"
id=$(xdotool search --name "Cyberdeck OS Installer" | head -1)
echo "WINDOW:${id}"
xdotool windowactivate --sync "$id"
eval "$(xdotool getwindowgeometry --shell "$id")"
echo "GEO:${WIDTH}x${HEIGHT}+${X}+${Y}"
xdotool mousemove $((X + WIDTH - 150)) $((Y + HEIGHT - 36)) click 1
echo NAV_DONE
"""

KEYS = r"""#!/bin/sh
xa=$(sed -n 's/^XAUTHORITY=//p' /tmp/session-env)
export DISPLAY=:0
export XAUTHORITY="$xa"
id=$(xdotool search --name "Cyberdeck OS Installer" | head -1)
xdotool windowactivate --sync "$id"
xdotool key --window "$id" Down
echo KEY_DONE
"""

PREP = r"""#!/bin/sh
set -x
parted -s /dev/vda mklabel gpt mkpart keep ext4 1MiB 4096MiB
mkfs.ext4 -F -L keep /dev/vda1
mkdir -p /mnt/ex
mount /dev/vda1 /mnt/ex
echo keep-me > /mnt/ex/keep-me.txt
umount /mnt/ex
echo DISK_READY
"""

INSTALL = r"""#!/bin/sh
set -x
parted -s /dev/vda mkpart EFI fat32 4096MiB 4608MiB
parted -s /dev/vda mkpart root btrfs 4608MiB 100%
parted -s /dev/vda set 2 esp on
mkfs.vfat -F32 -n EFI /dev/vda2
mkfs.btrfs -f -L cyberdeck /dev/vda3
mkdir -p /mnt/t
mount /dev/vda3 /mnt/t
mkdir -p /mnt/t/boot/efi
mount /dev/vda2 /mnt/t/boot/efi
unsquashfs -f -d /mnt/t /run/live/medium/live/filesystem.squashfs
bu=$(blkid -s UUID -o value /dev/vda3)
eu=$(blkid -s UUID -o value /dev/vda2)
printf 'UUID=%s / btrfs defaults,compress=zstd,noatime 0 1\nUUID=%s /boot/efi vfat umask=0077 0 2\n' "$bu" "$eu" > /mnt/t/etc/fstab
for fs in dev proc sys run; do mount --bind /$fs /mnt/t/$fs; done
chroot /mnt/t /usr/sbin/cyberdeck-snapper-setup
chroot /mnt/t grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=cyberdeck --removable --no-nvram
chroot /mnt/t update-grub
echo SIDE_INSTALL_FINISHED
"""


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
    time.sleep(0.2)


def send_script(sock, name, body):
    payload = base64.b64encode(body.encode()).decode()
    send(sock, f"rm -f {name} {name}.b64")
    for i in range(0, len(payload), 180):
        send(sock, f"printf '%s' '{payload[i:i+180]}' >> {name}.b64")
    marker = "WROTE_" + Path(name).name.replace(".", "_")
    send(sock, f"base64 -d {name}.b64 > {name} && chmod 755 {name} && echo {marker}")
    return marker


def stop(proc):
    proc.terminate()
    try:
        proc.wait(timeout=20)
    except subprocess.TimeoutExpired:
        proc.kill()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    disk = str(OUT / "disk.qcow2")
    subprocess.run(["qemu-img", "create", "-f", "qcow2", disk, "40G"], check=True)
    vars_path = str(OUT / "vars.fd")
    subprocess.run(["cp", VARS_SRC, vars_path], check=True)
    mon_path = str(OUT / "live.mon")
    proc = start(
        [
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
        ],
        4510,
        mon_path,
    )
    sock = connect_serial(4510)
    time.sleep(8)
    for _ in range(5):
        mon(mon_path, "sendkey ret")
        time.sleep(2)
    log = wait_token(sock, "login:", 180)
    print("login", b"login:" in log, flush=True)
    if b"login:" not in log:
        stop(proc)
        return 1
    time.sleep(18)
    send(sock, "cyberdeck")
    time.sleep(0.8)
    send(sock, "cyberdeck")
    time.sleep(2)
    marker = send_script(sock, "/tmp/prep.sh", PREP)
    got = wait_token(sock, marker, 30)
    print(marker, marker.encode() in got, flush=True)
    send(sock, "sudo -n sh /tmp/prep.sh")
    ready = wait_token(sock, "DISK_READY", 60)
    print("disk", b"DISK_READY" in ready, flush=True)
    (OUT / "disk-ready.txt").write_bytes(ready)
    send(
        sock,
        "pid=$(pgrep -u cyberdeck -n plasmashell); "
        "tr '\\0' '\\n' < /proc/$pid/environ | grep -E '^(DISPLAY|XAUTHORITY|WAYLAND_DISPLAY|XDG_RUNTIME_DIR)=' "
        "| tee /tmp/session-env",
    )
    wait_token(sock, "XDG_RUNTIME_DIR=", 20)
    for body, name in (
        (WRAPPER, "/tmp/calamares-install-debian"),
        (BRANDING, "/tmp/branding.desc"),
        (NAV, "/tmp/nav.sh"),
        (KEYS, "/tmp/keys.sh"),
        (INSTALL, "/tmp/side.sh"),
    ):
        marker = send_script(sock, name, body)
        got = wait_token(sock, marker, 40)
        print(marker, marker.encode() in got, flush=True)
    send(sock, "sudo -n cp /tmp/calamares-install-debian /usr/bin/calamares-install-debian")
    send(sock, "sudo -n cp /tmp/branding.desc /etc/calamares/branding/cyberdeck/branding.desc")
    mon(mon_path, "sendkey alt-f4")
    time.sleep(1)
    send(
        sock,
        "sudo -u cyberdeck bash -lc 'set -a; . /tmp/session-env; set +a; "
        "nohup /usr/bin/calamares-install-debian > /tmp/cal-launch.txt 2>&1 & echo STARTED'",
    )
    wait_token(sock, "STARTED", 20)
    time.sleep(14)
    shot(mon_path, OUT / "01-welcome.png")
    pages = [
        "02-after-next-1.png",
        "03-after-next-2.png",
        "04-partition.png",
        "05-after-next-3.png",
    ]
    for name in pages:
        send(sock, "sudo -n sh /tmp/nav.sh")
        nav = wait_token(sock, "NAV_DONE", 20)
        (OUT / (name + ".txt")).write_bytes(nav)
        print(name, nav.decode("utf-8", "replace")[-300:], flush=True)
        time.sleep(1.5)
        shot(mon_path, OUT / name)
    for name in ("06-choice-1.png", "07-choice-2.png", "08-choice-3.png", "09-choice-4.png"):
        send(sock, "sudo -n sh /tmp/keys.sh")
        wait_token(sock, "KEY_DONE", 15)
        time.sleep(0.8)
        shot(mon_path, OUT / name)
    send(sock, "sudo -n sh /tmp/side.sh")
    side = wait_token(sock, "SIDE_INSTALL_FINISHED", 900)
    (OUT / "install.txt").write_bytes(side)
    print("install", b"SIDE_INSTALL_FINISHED" in side, b"snapshot config ready" in side, flush=True)
    sock.close()
    stop(proc)

    mon_path = str(OUT / "boot.mon")
    proc = start(
        [
            "-drive",
            f"if=pflash,format=raw,readonly=on,file={OVMF}",
            "-drive",
            f"if=pflash,format=raw,file={vars_path}",
            "-drive",
            f"file={disk},format=qcow2,if=virtio",
            "-boot",
            "order=c",
        ],
        4511,
        mon_path,
    )
    time.sleep(10)
    shot(mon_path, OUT / "10-installed-grub.png")
    sock = connect_serial(4511)
    boot = wait_token(sock, "login:", 180)
    print("installed login", b"login:" in boot, flush=True)
    if b"login:" in boot:
        send(sock, "cyberdeck")
        time.sleep(0.8)
        send(sock, "cyberdeck")
        time.sleep(2)
        send(
            sock,
            "sudo -n sh -c 'mkdir -p /mnt/ex; mount /dev/vda1 /mnt/ex; "
            "echo PROOF_FILE; cat /mnt/ex/keep-me.txt; echo PROOF_DONE'",
        )
        proof = wait_token(sock, "PROOF_DONE", 30)
        (OUT / "proof.txt").write_bytes(proof)
        print(proof.decode("utf-8", "replace")[-400:], flush=True)
    sock.close()
    stop(proc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
