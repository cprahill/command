#!/usr/bin/env python3
"""2026-09-13 recut: revert unrequested marks, recut peel-blob + diecut, keep ticket."""
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FONTS = ROOT / "fonts"
CONCEPTS = ROOT.parent / "concepts"
SRC = ROOT / "_recut-src"
OUT = ROOT
ARCHIVO = FONTS / "ArchivoBlack-Regular.ttf"


def magick(*args: str) -> None:
    subprocess.check_call(["magick", *args])


def square_from_photo(src: Path, dest: Path, size: int, bg: str) -> None:
    magick(
        str(src),
        "-resize",
        f"{size}x{size}",
        "-gravity",
        "center",
        "-background",
        bg,
        "-extent",
        f"{size}x{size}",
        str(dest),
    )


def sizes_from_photo(stem: str, src: Path, bg: str) -> None:
    sticker = OUT / f"{stem}-sticker.png"
    square_from_photo(src, sticker, 1024, bg)
    magick(str(sticker), "-resize", "400x400", str(OUT / f"{stem}-avatar.png"))
    magick(str(sticker), "-resize", "800x800", str(OUT / f"{stem}-avatar@2x.png"))
    magick(str(sticker), "-resize", "2048x2048", str(OUT / f"{stem}-lock.png"))
    magick(str(sticker), str(OUT / f"{stem}-board.svg"))
    magick(str(sticker), str(OUT / f"{stem}.svg"))


def label_from_sticker(stem: str, bg: str, ink: str = "#1A1714") -> None:
    sticker = OUT / f"{stem}-sticker.png"
    dest = OUT / f"{stem}-label.png"
    magick(
        "-size",
        "1800x500",
        f"xc:{bg}",
        "(",
        str(sticker),
        "-resize",
        "440x440",
        ")",
        "-gravity",
        "west",
        "-geometry",
        "+28+0",
        "-composite",
        "-font",
        str(ARCHIVO),
        "-pointsize",
        "72",
        "-fill",
        ink,
        "-gravity",
        "center",
        "-annotate",
        "+210+8",
        "Stickers&Soap Co.",
        str(dest),
    )
    magick(str(dest), str(OUT / f"{stem}-label.svg"))


def revert_from_concept(stem: str, bg: str, ink: str = "#1A1714") -> None:
    src = CONCEPTS / f"{stem}.png"
    sizes_from_photo(stem, src, bg)
    label_from_sticker(stem, bg, ink)


def main() -> None:
    sizes_from_photo("02-peel-blob", SRC / "02-peel-blob-recut.jpg", "#F3EDE3")
    label_from_sticker("02-peel-blob", "#F3EDE3", "#FF3B6B")
    sizes_from_photo("02-peel-blob-b", SRC / "02-peel-blob-b-recut.jpg", "#F3EDE3")
    label_from_sticker("02-peel-blob-b", "#FFF6C8", "#C2185B")
    sizes_from_photo("02-peel-blob-c", SRC / "02-peel-blob-c-recut.jpg", "#F3EDE3")
    label_from_sticker("02-peel-blob-c", "#E8F8F0", "#1B2A4A")

    sizes_from_photo("04-diecut-s", SRC / "04-diecut-s-recut.jpg", "#F3E6D4")
    label_from_sticker("04-diecut-s", "#F3E6D4")

    revert_from_concept("06-factory-stamp", "#F3EBD8")
    revert_from_concept("09-kraft-band", "#F4EFE4")
    revert_from_concept("13-script-shop", "#F6EDE0")
    revert_from_concept("21-box-logo", "#F7F4EE", "#111111")

    print("OK recut — 17-drop-ticket kept")


if __name__ == "__main__":
    main()
