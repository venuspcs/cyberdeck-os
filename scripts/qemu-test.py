#!/usr/bin/env python3
"""Boot-test a Cyberdeck OS ISO in QEMU (UEFI and BIOS) and install to a virtual disk.

Writes PNGs and logs under the directory given as the second argument.
"""

import os
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None

OVMF_CODE = "/usr/share/OVMF/OVMF_CODE_4M.fd"
OVMF_VARS_SRC = "/usr/share/OVMF/OVMF_VARS_4M.fd"


def run(cmd, **kwargs):
    print("+", " ".join(cmd), flush=True)
    return subprocess.run(cmd, check=False, **kwargs)


def qemu_base(extra, serial_port, mon_path, vnc_display):
    del vnc_display
    return [
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
        f"unix:{mon_path},server=on,wait=off",
        "-display",
        "none",
        "-no-reboot",
        *extra,
    ]


def screendump(mon_path, ppm_path, png_path):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(20)
    sock.connect(mon_path)
    sock.recv(4096)
    sock.sendall(f"screendump {ppm_path}\n".encode())
    time.sleep(1)
    sock.close()
    if Image is not None and Path(ppm_path).exists():
        Image.open(ppm_path).save(png_path)
        print(f"wrote {png_path}", flush=True)
    else:
        print(f"ppm at {ppm_path}", flush=True)


def read_until(sock, token, timeout):
    sock.settimeout(1)
    data = b""
    end = time.time() + timeout
    while time.time() < end:
        try:
            chunk = sock.recv(4096)
        except socket.timeout:
            continue
        if not chunk:
            break
        data += chunk
        text = data.decode("utf-8", "replace")
        if token in text:
            return text
    return data.decode("utf-8", "replace")


def send_line(sock, line):
    sock.sendall((line + "\n").encode())
    time.sleep(0.4)


def boot_live(iso, outdir, mode):
    serial_port = 4444 if mode == "uefi" else 4445
    mon = str(outdir / f"{mode}.mon")
    vnc = 1 if mode == "uefi" else 2
    extra = ["-cdrom", iso, "-boot", "order=d"]
    if mode == "uefi":
        vars_path = str(outdir / "OVMF_VARS.fd")
        shutil.copy(OVMF_VARS_SRC, vars_path)
        extra = [
            "-drive",
            f"if=pflash,format=raw,readonly=on,file={OVMF_CODE}",
            "-drive",
            f"if=pflash,format=raw,file={vars_path}",
            *extra,
        ]
    proc = subprocess.Popen(qemu_base(extra, serial_port, mon, vnc))
    time.sleep(2)
    sock = socket.create_connection(("127.0.0.1", serial_port), timeout=10)
    log = read_until(sock, "login:", 240)
    (outdir / f"{mode}-serial-boot.txt").write_text(log)
    time.sleep(50)
    screendump(mon, str(outdir / f"{mode}-desktop.ppm"), str(outdir / f"{mode}-desktop.png"))
    if "login:" in log:
        send_line(sock, "cyberdeck")
        time.sleep(1)
        send_line(sock, "cyberdeck")
        time.sleep(2)
        send_line(sock, "sudo -n xhost +si:localuser:root || true")
        send_line(sock, "sudo -n bash -lc 'DISPLAY=:0 QT_QPA_PLATFORM=xcb calamares >/tmp/calamares.log 2>&1 &' || true")
        time.sleep(25)
        screendump(mon, str(outdir / f"{mode}-calamares.ppm"), str(outdir / f"{mode}-calamares.png"))
        send_line(sock, "sudo -n sh -c 'ps -C calamares -o pid,cmd; echo CALAMARES_PS_DONE'")
        extra_log = read_until(sock, "CALAMARES_PS_DONE", 20)
        (outdir / f"{mode}-calamares.txt").write_text(extra_log)
    sock.close()
    proc.terminate()
    try:
        proc.wait(timeout=20)
    except subprocess.TimeoutExpired:
        proc.kill()
    return "login:" in log


def install_and_boot(iso, outdir):
    disk = str(outdir / "install.qcow2")
    run(["qemu-img", "create", "-f", "qcow2", disk, "20G"])
    serial_port = 4446
    mon = str(outdir / "install.mon")
    vars_path = str(outdir / "OVMF_VARS_install.fd")
    shutil.copy(OVMF_VARS_SRC, vars_path)
    extra = [
        "-drive",
        f"if=pflash,format=raw,readonly=on,file={OVMF_CODE}",
        "-drive",
        f"if=pflash,format=raw,file={vars_path}",
        "-cdrom",
        iso,
        "-drive",
        f"file={disk},format=qcow2,if=virtio",
        "-boot",
        "order=d",
    ]
    proc = subprocess.Popen(qemu_base(extra, serial_port, mon, 3))
    time.sleep(2)
    sock = socket.create_connection(("127.0.0.1", serial_port), timeout=10)
    log = read_until(sock, "login:", 300)
    (outdir / "install-live-serial.txt").write_text(log)
    if "login:" not in log:
        proc.kill()
        return False
    send_line(sock, "cyberdeck")
    time.sleep(1)
    send_line(sock, "cyberdeck")
    time.sleep(2)
    send_line(sock, "sudo -n cyberdeck-autoinstall >/tmp/autoinstall-console.txt 2>&1; echo AUTOINSTALL_DONE:$?")
    done = read_until(sock, "AUTOINSTALL_DONE:", 900)
    (outdir / "install-run.txt").write_text(done)
    sock.close()
    proc.wait(timeout=120)
    if "AUTOINSTALL_DONE:0" not in done:
        return False

    # Boot the installed disk, UEFI, no CD.
    serial_port = 4447
    mon = str(outdir / "installed.mon")
    extra = [
        "-drive",
        f"if=pflash,format=raw,readonly=on,file={OVMF_CODE}",
        "-drive",
        f"if=pflash,format=raw,file={vars_path}",
        "-drive",
        f"file={disk},format=qcow2,if=virtio",
        "-boot",
        "order=c",
    ]
    proc = subprocess.Popen(qemu_base(extra, serial_port, mon, 4))
    time.sleep(2)
    sock = socket.create_connection(("127.0.0.1", serial_port), timeout=10)
    log = read_until(sock, "login:", 240)
    (outdir / "installed-serial.txt").write_text(log)
    time.sleep(20)
    screendump(mon, str(outdir / "installed-boot.ppm"), str(outdir / "installed-boot.png"))
    ok = False
    if "login:" in log:
        send_line(sock, "cyberdeck")
        time.sleep(1)
        send_line(sock, "cyberdeck")
        time.sleep(1)
        send_line(sock, "findmnt -no FSTYPE,SOURCE /; findmnt -no FSTYPE,SOURCE /boot/efi; lsblk -o NAME,FSTYPE,PARTTYPE,SIZE; echo LAYOUT_DONE")
        layout = read_until(sock, "LAYOUT_DONE", 30)
        (outdir / "installed-layout.txt").write_text(layout)
        ok = "btrfs" in layout and "vfat" in layout
    sock.close()
    proc.terminate()
    try:
        proc.wait(timeout=20)
    except subprocess.TimeoutExpired:
        proc.kill()
    return ok


def main():
    iso = sys.argv[1]
    outdir = Path(sys.argv[2])
    outdir.mkdir(parents=True, exist_ok=True)
    uefi = boot_live(iso, outdir, "uefi")
    bios = boot_live(iso, outdir, "bios")
    installed = install_and_boot(iso, outdir)
    summary = f"uefi_live_login={uefi}\nbios_live_login={bios}\ninstalled_btrfs={installed}\n"
    (outdir / "summary.txt").write_text(summary)
    print(summary)
    return 0 if uefi and bios and installed else 1


if __name__ == "__main__":
    sys.exit(main())
