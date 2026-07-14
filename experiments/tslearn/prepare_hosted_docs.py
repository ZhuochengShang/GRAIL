#!/usr/bin/env python3
"""Freeze the rendered tslearn Read the Docs single-page archive for A1/A2.

No LLM is involved. The official HTML zip is checksum-verified, then only the
rendered main content is converted to stable Markdown-like text. Navigation,
scripts, styles, and binary assets never enter the audience context.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from bs4 import BeautifulSoup


URL = "https://tslearn.readthedocs.io/_/downloads/en/latest/htmlzip/"
ARCHIVE_SHA256 = "1b9331bd08f9c5c927ac1d6505057bd066324343ef50a3fb879ff0c19a31991a"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rendered_text(html: bytes) -> str:
    soup = BeautifulSoup(html, "html.parser")
    main = soup.select_one("main#main-content")
    if main is None:
        raise ValueError("archive index.html has no main#main-content")

    for node in main.select("script, style, nav, .headerlink, .bd-sidebar"):
        node.decompose()
    for br in main.find_all("br"):
        br.replace_with("\n")
    for pre in main.find_all("pre"):
        code = pre.get_text("", strip=False).strip("\n")
        pre.replace_with(f"\n```python\n{code}\n```\n")
    for level in range(1, 7):
        for heading in main.find_all(f"h{level}"):
            title = heading.get_text(" ", strip=True)
            heading.replace_with(f"\n{'#' * level} {title}\n")
    for row in main.find_all("tr"):
        cells = [c.get_text(" ", strip=True) for c in row.find_all(["th", "td"])]
        if cells:
            row.replace_with("\n| " + " | ".join(cells) + " |\n")
    for item in main.find_all("li"):
        item.insert_before("\n- ")
        item.append("\n")
    for block in main.find_all(["p", "div", "section", "article", "dl", "dt", "dd"]):
        block.insert_before("\n")
        block.append("\n")

    text = main.get_text(" ", strip=False)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    return text


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("archive", type=Path)
    ap.add_argument("--out", type=Path,
                    default=Path("tslearn/.aideal_hosted_docs"))
    args = ap.parse_args()

    payload = args.archive.read_bytes()
    actual = sha256(payload)
    if actual != ARCHIVE_SHA256:
        raise SystemExit(f"archive SHA-256 mismatch: expected {ARCHIVE_SHA256}, got {actual}")
    with zipfile.ZipFile(args.archive) as zf:
        html = zf.read("tslearn-latest/index.html")
    text = rendered_text(html)

    args.out.mkdir(parents=True, exist_ok=True)
    rendered = args.out / "rendered_readthedocs.md"
    rendered.write_text(text, encoding="utf-8")
    metadata = {
        "source_url": URL,
        "archive_sha256": actual,
        "archive_bytes": len(payload),
        "archive_entry": "tslearn-latest/index.html",
        "rendered_sha256": sha256(text.encode("utf-8")),
        "rendered_chars": len(text),
        "extractor": str(Path(__file__).name),
    }
    (args.out / "snapshot.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rendered": str(rendered), **metadata}, indent=2))


if __name__ == "__main__":
    main()
