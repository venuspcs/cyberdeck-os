#!/usr/bin/env python3
"""Clock and version checks for Alpha 3. No ISO required."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "firstboot"))
import importlib.machinery
import importlib.util

theme_path = Path(__file__).resolve().parents[1] / "firstboot" / "cyberdeck-theme"
loader = importlib.machinery.SourceFileLoader("cyberdeck_theme", str(theme_path))
spec = importlib.util.spec_from_loader("cyberdeck_theme", loader)
theme = importlib.util.module_from_spec(spec)
loader.exec_module(theme)


def expect(cond, message):
    if not cond:
        raise SystemExit(message)


def main():
    # 9:00 AM and 9:00 PM are the times Richard checked, in 24-hour form.
    expect(theme.slot(9, 0) == "day", "09:00 must be Daybreak")
    expect(theme.slot(9, 24) == "day", "09:24 must be Daybreak")
    expect(theme.slot(21, 0) == "night", "21:00 must be Nightwatch")
    expect(theme.slot(21, 28) == "night", "21:28 must be Nightwatch")
    expect(theme.slot(6, 30) == "day", "06:30 is the start of Daybreak")
    expect(theme.slot(18, 29) == "day", "18:29 is still Daybreak")
    expect(theme.slot(18, 30) == "night", "18:30 is the start of Nightwatch")
    expect(theme.slot(3, 0) == "night", "03:00 is Nightwatch")

    os.environ["CYBERDECK_THEME_DRY"] = "1"
    os.environ["CYBERDECK_THEME_HOUR"] = "9"
    os.environ["CYBERDECK_THEME_MINUTE"] = "0"
    os.environ["CYBERDECK_THEME_ZONE"] = "America/Chicago"
    expect(theme.once() == "day", "dry run at 09:00 America/Chicago must be day")
    os.environ["CYBERDECK_THEME_HOUR"] = "21"
    os.environ["CYBERDECK_THEME_MINUTE"] = "28"
    expect(theme.once() == "night", "dry run at 21:28 America/Chicago must be night")

    root = Path(__file__).resolve().parents[1]
    version = (root / "version" / "cyberdeck-os.version").read_text(encoding="utf-8")
    expect("CYBERDECK_VERSION_ID=beta1" in version, "version id")
    expect('CYBERDECK_VERSION="Beta 1 (Plow)"' in version, "version name")
    expect("CYBERDECK_BUILD=4" in version, "build number")
    os_release = (root / "branding" / "image" / "os-release").read_text(encoding="utf-8")
    expect("VERSION_ID=beta1" in os_release, "os-release id")
    expect("Beta 1 (Plow)" in os_release, "os-release pretty")
    expect("SUPPORT_URL=" in os_release, "support url")
    expect("Version 1 (Alpha)" not in os_release, "old version string in os-release")
    identity = [
        root / "branding/image/os-release",
        root / "branding/image/issue",
        root / "branding/image/plymouth/cyberdeck.script",
        root / "installer/calamares/branding.desc",
        root / "branding/image/show.qml",
    ]
    blob = "\n".join(path.read_text(encoding="utf-8") for path in identity)
    expect("Version 1 (Alpha)" not in blob, "identity files still say Version 1 (Alpha)")
    expect("Beta 1 (Plow)" in blob, "identity files missing Alpha 3")
    print("beta1 checks passed")


if __name__ == "__main__":
    main()
