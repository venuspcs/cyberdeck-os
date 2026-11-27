#!/usr/bin/env python3
"""Build a text PDF and an ODT from the guide chapters."""

import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs" / "guide"
OUT = Path(__file__).resolve().parent / "image"
CHAPTERS = [
    "README.md",
    "install.md",
    "live-use.md",
    "updates.md",
    "repair-rollback.md",
    "maintenance.md",
    "adding-software.md",
    "containers.md",
    "drives.md",
    "meshtastic.md",
    "ham-tools.md",
]


def wrap(text, width=90):
    words = text.split()
    if not words:
        return [""]
    rows = []
    cur = words[0]
    for word in words[1:]:
        if len(cur) + 1 + len(word) > width:
            rows.append(cur)
            cur = word
        else:
            cur += " " + word
    rows.append(cur)
    return rows


def lines():
    out = ["Cyberdeck OS Alpha 3 (Hatchet)", "How-To guide", ""]
    for name in CHAPTERS:
        path = GUIDE / name
        if not path.exists():
            continue
        out.append(name)
        out.append("")
        for raw in path.read_text(encoding="utf-8").splitlines():
            text = raw.replace("**", "").replace("`", "")
            if text.startswith("#"):
                text = text.lstrip("#").strip()
            out.extend(wrap(text))
        out.append("")
    return out


def write_pdf(paragraphs, dest: Path):
    # One page per 48 lines. A tiny PDF writer, no extra libraries.
    pages = [paragraphs[i : i + 48] for i in range(0, len(paragraphs), 48)] or [[""]]
    objects = []

    def add(data: str):
        objects.append(data)
        return len(objects)

    add("<< /Type /Catalog /Pages 2 0 R >>")
    page_ids = []
    content_ids = []
    font_id = 3
    # placeholder pages object filled after we know ids
    objects.append("")  # pages
    add("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    for page in pages:
        commands = ["BT", "/F1 11 Tf", "50 780 Td", "14 TL"]
        for line in page:
            safe = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            if len(safe) > 110:
                safe = safe[:110]
            commands.append(f"({safe}) '")
        commands.append("ET")
        stream = "\n".join(commands).encode("latin-1", "replace")
        content_ids.append(
            add(f"<< /Length {len(stream)} >>\nstream\n".encode("ascii") + stream + b"\nendstream")
        )
    for cid in content_ids:
        page_ids.append(
            add(
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                f"/Contents {cid} 0 R /Resources << /Font << /F1 {font_id} 0 R >> >> >>"
            )
        )
    kids = " ".join(f"{pid} 0 R" for pid in page_ids)
    objects[1] = f"<< /Type /Pages /Count {len(page_ids)} /Kids [{kids}] >>"
    out = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        if isinstance(obj, bytes):
            out += f"{i} 0 obj\n".encode() + obj + b"\nendobj\n"
        else:
            out += f"{i} 0 obj\n{obj}\nendobj\n".encode()
    xref = len(out)
    out += f"xref\n0 {len(objects)+1}\n".encode()
    out += b"0000000000 65535 f \n"
    for off in offsets[1:]:
        out += f"{off:010d} 00000 n \n".encode()
    out += f"trailer << /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    dest.write_bytes(out)


def write_odt(paragraphs, dest: Path):
    body = "".join(f"<text:p>{escape(line)}</text:p>" for line in paragraphs)
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body><office:text>{body}</office:text></office:body>
</office:document-content>
"""
    manifest = """<?xml version="1.0" encoding="UTF-8"?>
<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0">
 <manifest:file-entry manifest:full-path="/" manifest:media-type="application/vnd.oasis.opendocument.text"/>
 <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>
</manifest:manifest>
"""
    with zipfile.ZipFile(dest, "w") as zf:
        zf.writestr("mimetype", "application/vnd.oasis.opendocument.text", compress_type=zipfile.ZIP_STORED)
        zf.writestr("content.xml", content)
        zf.writestr("META-INF/manifest.xml", manifest)


def main():
    text = lines()
    write_pdf(text, OUT / "Cyberdeck-OS-Manual.pdf")
    write_odt(text, OUT / "Cyberdeck-OS-Manual.odt")
    print("manual", OUT)


if __name__ == "__main__":
    main()
