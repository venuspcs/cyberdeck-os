#!/usr/bin/env python3
"""Draw original Cyberdeck OS homestead art. No Debian artwork."""

from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent / "image"


def sky(img, top, bottom):
    w, h = img.size
    px = img.load()
    for y in range(h):
        t = y / (h - 1)
        color = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        for x in range(w):
            px[x, y] = color


def cabin(draw, x, y, scale, night):
    wall = (186, 142, 86) if not night else (92, 68, 42)
    roof = (120, 62, 42) if not night else (58, 32, 24)
    w, h = int(220 * scale), int(130 * scale)
    draw.polygon(
        [(x, y + int(40 * scale)), (x + w // 2, y), (x + w, y + int(40 * scale))],
        fill=roof,
    )
    draw.rectangle([x + int(16 * scale), y + int(40 * scale), x + w - int(16 * scale), y + h], fill=wall)
    win = (255, 214, 120) if night else (196, 224, 232)
    draw.rectangle(
        [x + int(48 * scale), y + int(62 * scale), x + int(92 * scale), y + int(100 * scale)],
        fill=win,
    )
    draw.rectangle(
        [x + int(128 * scale), y + int(62 * scale), x + int(172 * scale), y + int(100 * scale)],
        fill=win,
    )
    draw.rectangle(
        [x + int(96 * scale), y + int(78 * scale), x + int(124 * scale), y + h],
        fill=(90, 58, 36) if not night else (48, 30, 20),
    )


def tree(draw, x, y, night):
    trunk = (110, 74, 42) if not night else (62, 42, 26)
    leaf = (62, 130, 58) if not night else (28, 62, 40)
    draw.rectangle([x + 18, y + 70, x + 34, y + 130], fill=trunk)
    draw.ellipse([x, y, x + 52, y + 80], fill=leaf)


def draw_scene(night, size):
    img = Image.new("RGB", size)
    if night:
        sky(img, (12, 22, 48), (28, 40, 62))
    else:
        sky(img, (142, 196, 232), (214, 228, 196))
    d = ImageDraw.Draw(img)
    w, h = size
    ground_y = int(h * 0.62)
    hill = (74, 140, 72) if not night else (24, 48, 36)
    d.polygon([(0, ground_y + 40), (int(w * 0.35), ground_y - 30), (int(w * 0.7), ground_y + 20), (w, ground_y - 10), (w, h), (0, h)], fill=hill)
    d.rectangle([0, int(h * 0.78), w, h], fill=(86, 120, 52) if not night else (18, 36, 24))
    if night:
        d.ellipse([int(w * 0.78), int(h * 0.08), int(w * 0.78) + 70, int(h * 0.08) + 70], fill=(236, 232, 210))
        for sx, sy in ((120, 80), (260, 140), (400, 60), (900, 100), (1400, 70), (1600, 160)):
            if sx < w and sy < h:
                d.ellipse([sx, sy, sx + 3, sy + 3], fill=(240, 240, 230))
    else:
        d.ellipse([int(w * 0.78), int(h * 0.1), int(w * 0.78) + 90, int(h * 0.1) + 90], fill=(255, 214, 90))
    tree(d, int(w * 0.12), ground_y - 40, night)
    tree(d, int(w * 0.72), ground_y - 20, night)
    cabin(d, int(w * 0.38), ground_y - 20, max(w / 1920, 0.6), night)
    return img


def main():
    OUT.joinpath("wallpapers").mkdir(parents=True, exist_ok=True)
    day = draw_scene(False, (1920, 1080))
    night = draw_scene(True, (1920, 1080))
    day.save(OUT / "wallpapers" / "daybreak.png")
    night.save(OUT / "wallpapers" / "nightwatch.png")
    day.resize((1024, 768), Image.Resampling.LANCZOS).save(OUT / "grub-background.png")
    day.resize((467, 280), Image.Resampling.LANCZOS).save(OUT / "slide.png")
    logo = Image.new("RGB", (256, 256), (28, 58, 74))
    d = ImageDraw.Draw(logo)
    cabin(d, 28, 70, 0.9, False)
    logo.save(OUT / "logo.png")
    print("art written", OUT)


if __name__ == "__main__":
    main()
