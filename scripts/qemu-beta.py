#!/usr/bin/env python3
"""Boot the Version 1 Alpha ISO: live BIOS, live UEFI, and an installed UEFI system."""

import socket
import subprocess
import time
from pathlib import Path

from PIL import Image

ISO = "/workspace/build/amd64/cyberdeck-os-amd64-amd64.hybrid.iso"
OUT = Path("/tmp/beta")
OVMF = "/usr/share/OVMF/OVMF_CODE_4M.fd"
VARS = "/usr/share/OVMF/OVMF_VARS_4M.fd"


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


def connect(port):
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
    time.sleep(0.12)
    s.close()


def shot(path, png):
    ppm = str(png) + ".ppm"
    mon(path, f"screendump {ppm}")
    time.sleep(0.5)
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


def boot_menu(path):
    time.sleep(8)
    shot(path, OUT / "boot-menu.png")
    for _ in range(4):
        mon(path, "sendkey ret")
        time.sleep(1.5)


def login(sock):
    send(sock, "cyberdeck")
    time.sleep(0.6)
    send(sock, "cyberdeck")
    time.sleep(2)


def stop(proc):
    proc.terminate()
    try:
        proc.wait(timeout=20)
    except subprocess.TimeoutExpired:
        proc.kill()


def live(firmware, port, name):
    mon_path = str(OUT / f"{name}.mon")
    extra = ["-cdrom", ISO, "-boot", "order=d"]
    if firmware == "uefi":
        vars_path = str(OUT / f"vars-{name}.fd")
        subprocess.run(["cp", VARS, vars_path], check=True)
        extra = [
            "-drive",
            f"if=pflash,format=raw,readonly=on,file={OVMF}",
            "-drive",
            f"if=pflash,format=raw,file={vars_path}",
            *extra,
        ]
    proc = start(extra, port, mon_path)
    sock = connect(port)
    boot_menu(mon_path)
    log = wait_token(sock, "login:", 180)
    print(name, "login", b"login:" in log, flush=True)
    if b"login:" not in log:
        stop(proc)
        return 1
    time.sleep(20)
    shot(mon_path, OUT / f"{name}-desktop.png")
    login(sock)
    send(sock, "cat /etc/os-release; echo OS_DONE")
    info = wait_token(sock, "OS_DONE", 20)
    (OUT / f"{name}-os-release.txt").write_bytes(info)
    print(info.decode("utf-8", "replace")[-700:], flush=True)
    send(sock, "cat /etc/issue; ls /etc/skel/Desktop; ls /usr/share/wallpapers/cyberdeck; echo FILES_DONE")
    files = wait_token(sock, "FILES_DONE", 20)
    (OUT / f"{name}-files.txt").write_bytes(files)
    print(files.decode("utf-8", "replace")[-500:], flush=True)
    sock.close()
    stop(proc)
    return 0


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if live("bios", 4601, "bios") != 0:
        return 1
    if live("uefi", 4602, "uefi") != 0:
        return 1
    disk = str(OUT / "disk.qcow2")
    subprocess.run(["qemu-img", "create", "-f", "qcow2", disk, "20G"], check=True)
    vars_path = str(OUT / "vars-inst.fd")
    subprocess.run(["cp", VARS, vars_path], check=True)
    mon_path = str(OUT / "inst.mon")
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
        4603,
        mon_path,
    )
    sock = connect(4603)
    boot_menu(mon_path)
    log = wait_token(sock, "login:", 180)
    print("install login", b"login:" in log, flush=True)
    login(sock)
    send(sock, "sudo -n cyberdeck-autoinstall")
    done = wait_token(sock, "CYBERDECK_INSTALL_EXIT:", 900)
    (OUT / "install.txt").write_bytes(done)
    print(done[-200:].decode("utf-8", "replace"), flush=True)
    sock.close()
    stop(proc)
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
        4604,
        mon_path,
    )
    time.sleep(8)
    shot(mon_path, OUT / "installed-grub.png")
    sock = connect(4604)
    boot = wait_token(sock, "login:", 180)
    print("installed login", b"login:" in boot, flush=True)
    if b"login:" in boot:
        login(sock)
        send(sock, "cat /etc/os-release; echo INST_OS")
        info = wait_token(sock, "INST_OS", 20)
        (OUT / "installed-os-release.txt").write_bytes(info)
        print(info.decode("utf-8", "replace")[-500:], flush=True)
        time.sleep(15)
        shot(mon_path, OUT / "installed-desktop.png")
    sock.close()
    stop(proc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
