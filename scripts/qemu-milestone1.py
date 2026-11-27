#!/usr/bin/env python3
"""Boot-test the full ISO: Plasma, Calamares pages, alongside layout, Snapper in GRUB."""

import base64
import socket
import subprocess
import time
from pathlib import Path

from PIL import Image

ISO = "/workspace/build/amd64/cyberdeck-os-amd64-amd64.hybrid.iso"
OUT = Path("/tmp/m1")
OVMF = "/usr/share/OVMF/OVMF_CODE_4M.fd"
VARS = "/usr/share/OVMF/OVMF_VARS_4M.fd"


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
            "-nic",
            "user",
            *extra,
        ]
    )
    return proc


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
    time.sleep(0.25)
    s.close()


def shot(mon_path, png: Path):
    ppm = str(png) + ".ppm"
    mon(mon_path, f"screendump {ppm}")
    time.sleep(0.7)
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


def send_script(sock, name, body):
    payload = base64.b64encode(body.encode()).decode()
    send(sock, f"echo {payload} | base64 -d > {name}")
    time.sleep(0.5)


def boot_menu(mon_path):
    time.sleep(8)
    for _ in range(5):
        mon(mon_path, "sendkey ret")
        time.sleep(2)


def login(sock):
    send(sock, "cyberdeck")
    time.sleep(1)
    send(sock, "cyberdeck")
    time.sleep(3)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # --- Live desktop and Calamares ---
    mon_path = str(OUT / "live.mon")
    proc = start(["-cdrom", ISO, "-boot", "order=d"], 4480, mon_path)
    sock = connect_serial(4480)
    boot_menu(mon_path)
    log = wait_token(sock, "login:", 180)
    (OUT / "live-serial.txt").write_bytes(log)
    print("live login", b"login:" in log, flush=True)
    time.sleep(25)
    shot(mon_path, OUT / "01-live-desktop.png")
    login(sock)
    # Dismiss the welcome center, then start Calamares through its desktop launcher.
    mon(mon_path, "sendkey alt-f4")
    time.sleep(1)
    send(
        sock,
        "sudo -u cyberdeck bash -lc 'export XDG_RUNTIME_DIR=/run/user/1000; "
        "export WAYLAND_DISPLAY=wayland-0; "
        "export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus; "
        "/usr/bin/calamares-install-debian' >/tmp/cal-launch.txt 2>&1 &",
    )
    time.sleep(18)
    shot(mon_path, OUT / "02-calamares-open.png")
    send(sock, "ps -C calamares -o pid,cmd; echo CAL_PS")
    ps = wait_token(sock, "CAL_PS", 15)
    (OUT / "calamares-ps.txt").write_bytes(ps)
    # Walk the wizard with the keyboard. Next, Next, Next lands on partitioning
    # after welcome, locale, and keyboard when those pages accept Enter.
    for name in ("03-after-next-1.png", "04-after-next-2.png", "05-partition.png"):
        mon(mon_path, "sendkey alt-n")
        time.sleep(0.4)
        mon(mon_path, "sendkey ret")
        time.sleep(2)
        shot(mon_path, OUT / name)
    # Arrow through the partition choices and shoot each one.
    for name in ("06-part-choice-a.png", "07-part-choice-b.png", "08-part-choice-c.png"):
        mon(mon_path, "sendkey down")
        time.sleep(1)
        shot(mon_path, OUT / name)
    sock.close()
    proc.terminate()
    proc.wait(timeout=20)

    # --- Alongside: keep an existing ext4 partition, install into the free space ---
    disk = str(OUT / "alongside.qcow2")
    subprocess.run(["qemu-img", "create", "-f", "qcow2", disk, "20G"], check=True)
    mon_path = str(OUT / "side.mon")
    proc = start(
        ["-cdrom", ISO, "-drive", f"file={disk},format=qcow2,if=virtio", "-boot", "order=d"],
        4481,
        mon_path,
    )
    sock = connect_serial(4481)
    boot_menu(mon_path)
    log = wait_token(sock, "login:", 180)
    print("alongside login", b"login:" in log, flush=True)
    login(sock)
    send(
        sock,
        "sudo -n sh -c 'parted -s /dev/vda mklabel gpt; "
        "parted -s /dev/vda mkpart existing ext4 1MiB 8GiB; "
        "mkfs.ext4 -F -L EXISTING /dev/vda1; "
        "mkdir -p /mnt/ex; mount /dev/vda1 /mnt/ex; "
        "echo keep-me >/mnt/ex/keep-me.txt; umount /mnt/ex; "
        "parted -s /dev/vda mkpart biosboot 8GiB 8193MiB; "
        "parted -s /dev/vda set 2 bios_grub on; "
        "parted -s /dev/vda mkpart ESP fat32 8193MiB 8705MiB; "
        "parted -s /dev/vda set 3 esp on; "
        "parted -s /dev/vda mkpart root btrfs 8705MiB 100%; "
        "echo LAY_OK'",
    )
    lay = wait_token(sock, "Writing superblocks", 40)
    (OUT / "alongside-layout-cmd.txt").write_bytes(lay)
    # Open Calamares so the alongside choice is visible against this disk.
    send(
        sock,
        "sudo -u cyberdeck bash -lc 'export XDG_RUNTIME_DIR=/run/user/1000; "
        "export WAYLAND_DISPLAY=wayland-0; "
        "export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus; "
        "/usr/bin/calamares-install-debian' >/tmp/cal-side.txt 2>&1 &",
    )
    time.sleep(20)
    shot(mon_path, OUT / "09-alongside-calamares.png")
    # Finish the alongside install with the same tools Calamares would use
    # for the new Btrfs root, leaving the existing ext4 partition mounted later.
    send_script(
        sock,
        "/tmp/side.sh",
        """#!/bin/sh
set -x
mkfs.vfat -F32 -n EFI /dev/vda3
mkfs.btrfs -f -L cyberdeck /dev/vda4
mkdir -p /mnt/t/boot/efi
mount /dev/vda4 /mnt/t
mount /dev/vda3 /mnt/t/boot/efi
unsquashfs -f -d /mnt/t /run/live/medium/live/filesystem.squashfs
bu=$(blkid -s UUID -o value /dev/vda4)
eu=$(blkid -s UUID -o value /dev/vda3)
printf 'UUID=%s / btrfs defaults,compress=zstd,noatime 0 1\\nUUID=%s /boot/efi vfat umask=0077 0 2\\n' "$bu" "$eu" > /mnt/t/etc/fstab
for fs in dev proc sys run; do mount --bind /$fs /mnt/t/$fs; done
chroot /mnt/t /usr/sbin/cyberdeck-snapper-setup
chroot /mnt/t grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=cyberdeck --removable --no-nvram
chroot /mnt/t update-grub
echo SIDE_INSTALL_FINISHED
""",
    )
    send(sock, "sudo -n bash /tmp/side.sh")
    side = wait_token(sock, "SIDE_INSTALL_FINISHED", 900)
    (OUT / "alongside-install.txt").write_bytes(side)
    print("alongside done", b"Parallel unsquashfs" in side, flush=True)
    sock.close()
    proc.terminate()
    try:
        proc.wait(timeout=30)
    except subprocess.TimeoutExpired:
        proc.kill()

    # Boot the alongside disk and prove the old partition survived.
    vars_path = str(OUT / "vars-side.fd")
    subprocess.run(["cp", VARS, vars_path], check=True)
    mon_path = str(OUT / "sideboot.mon")
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
        4482,
        mon_path,
    )
    sock = connect_serial(4482)
    boot = wait_token(sock, "login:", 180)
    (OUT / "alongside-boot.txt").write_bytes(boot)
    time.sleep(8)
    shot(mon_path, OUT / "10-alongside-boot.png")
    if b"login:" in boot:
        login(sock)
        send(
            sock,
            "sudo -n sh -c 'mkdir -p /mnt/ex; mount /dev/vda1 /mnt/ex; echo KEEP; cat /mnt/ex/keep-me.txt; "
            "echo SNAPLIST; snapper --no-dbus list; echo LAYOUT_OK'",
        )
        lay = wait_token(sock, "LAYOUT_OK", 30)
        (OUT / "alongside-proof.txt").write_bytes(lay)
        print(lay.decode("utf-8", "replace")[-800:], flush=True)
    sock.close()
    proc.terminate()
    proc.wait(timeout=20)

    # --- Erase-style install, then an apt update that must show a GRUB snapshot ---
    disk = str(OUT / "erase.qcow2")
    subprocess.run(["qemu-img", "create", "-f", "qcow2", disk, "20G"], check=True)
    vars_path = str(OUT / "vars-erase.fd")
    subprocess.run(["cp", VARS, vars_path], check=True)
    mon_path = str(OUT / "erase.mon")
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
        4483,
        mon_path,
    )
    sock = connect_serial(4483)
    boot_menu(mon_path)
    log = wait_token(sock, "login:", 180)
    print("erase login", b"login:" in log, flush=True)
    login(sock)
    send(sock, "sudo -n cyberdeck-autoinstall")
    done = wait_token(sock, "CYBERDECK_INSTALL_EXIT:", 900)
    (OUT / "erase-install.txt").write_bytes(done)
    print(done[-300:].decode("utf-8", "replace"), flush=True)
    sock.close()
    try:
        proc.wait(timeout=40)
    except subprocess.TimeoutExpired:
        proc.terminate()
        proc.wait(timeout=20)

    mon_path = str(OUT / "grub.mon")
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
        4484,
        mon_path,
    )
    sock = connect_serial(4484)
    boot = wait_token(sock, "login:", 180)
    (OUT / "erase-boot.txt").write_bytes(boot)
    if b"login:" not in boot:
        print("installed erase disk did not reach login", flush=True)
        proc.kill()
        return 1
    login(sock)
    send(sock, "sudo -n apt-get update")
    wait_token(sock, "cyberdeck@", 120)
    send(sock, "sudo -n apt-get install -y --reinstall ncurses-base")
    apt = wait_token(sock, "cyberdeck@", 180)
    (OUT / "apt.txt").write_bytes(apt)
    send(sock, "sudo -n snapper --no-dbus list")
    snaps = wait_token(sock, "single", 20)
    (OUT / "snap-list.txt").write_bytes(snaps)
    print(snaps.decode("utf-8", "replace")[-600:], flush=True)
    send(sock, "sudo -n update-grub; echo GRUB_UPDATED")
    wait_token(sock, "GRUB_UPDATED", 60)
    send(sock, "sudo -n reboot")
    time.sleep(8)
    shot(mon_path, OUT / "11-grub-after-update.png")
    time.sleep(8)
    shot(mon_path, OUT / "12-grub-later.png")
    sock.close()
    proc.terminate()
    proc.wait(timeout=20)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
