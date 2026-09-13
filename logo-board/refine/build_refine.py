#!/usr/bin/env python3
"""Lock-ready Stickers&Soap Co. YES-logo refine. Path-outlined SVG + PNG sizes."""
from __future__ import annotations

import math
import subprocess
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.misc.transform import Transform
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parent
FONTS = ROOT / "fonts"
OUT = ROOT

# --- fonts ---
def load_font(name: str, **axes) -> TTFont:
    font = TTFont(FONTS / name)
    if "fvar" in font:
        loc = {a.axisTag: a.defaultValue for a in font["fvar"].axes}
        loc.update(axes)
        instantiateVariableFont(font, loc, inplace=True, overlap=True)
    return font


def _cmap(font: TTFont):
    return font.getBestCmap()


def glyph_advance(font: TTFont, ch: str, scale: float) -> float:
    if ch == " ":
        return 0.33 * font["head"].unitsPerEm * scale
    cmap = _cmap(font)
    gname = cmap.get(ord(ch))
    if not gname:
        return 0.0
    return font.getGlyphSet()[gname].width * scale


def measure(font: TTFont, text: str, size: float, tracking: float = 0.0) -> float:
    scale = size / font["head"].unitsPerEm
    w = 0.0
    for ch in text:
        w += glyph_advance(font, ch, scale) + tracking
    return w - (tracking if text else 0.0)


def glyph_d(font: TTFont, ch: str, x: float, y: float, size: float) -> str | None:
    cmap = _cmap(font)
    gname = cmap.get(ord(ch))
    if not gname:
        return None
    gs = font.getGlyphSet()
    scale = size / font["head"].unitsPerEm
    pen = SVGPathPen(gs)
    tp = TransformPen(pen, Transform(scale, 0, 0, -scale, x, y))
    gs[gname].draw(tp)
    d = pen.getCommands()
    return d or None


def text_paths(
    font: TTFont,
    text: str,
    x: float,
    y: float,
    size: float,
    fill: str,
    *,
    anchor: str = "left",
    tracking: float = 0.0,
    extra: str = "",
    stroke: str | None = None,
    sw: float = 0.0,
) -> str:
    total = measure(font, text, size, tracking)
    if anchor == "center":
        x -= total / 2
    elif anchor == "right":
        x -= total
    scale = size / font["head"].unitsPerEm
    parts = []
    cx = x
    for ch in text:
        d = glyph_d(font, ch, cx, y, size)
        if d:
            st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"' if stroke and sw else ""
            parts.append(f'<path d="{d}" fill="{fill}"{st} {extra}/>')
        cx += glyph_advance(font, ch, scale) + tracking
    return "\n".join(parts)


def text_group_transform(
    font: TTFont,
    text: str,
    x: float,
    y: float,
    size: float,
    fill: str,
    transform: str,
    **kw,
) -> str:
    inner = text_paths(font, text, 0, 0, size, fill, **kw)
    return f'<g transform="translate({x:.2f} {y:.2f}) {transform}">{inner}</g>'


def arc_text(
    font: TTFont,
    text: str,
    cx: float,
    cy: float,
    radius: float,
    size: float,
    fill: str,
    *,
    side: str = "top",
    tracking: float = 0.0,
) -> str:
    """Readable badge arc. Top sits on the upper half; bottom stays upright."""
    scale = size / font["head"].unitsPerEm
    advances = [glyph_advance(font, ch, scale) + tracking for ch in text]
    total = sum(advances)
    start = -total / 2
    parts = []
    acc = start
    for ch, adv in zip(text, advances):
        mid = acc + adv / 2
        theta = mid / radius
        d = glyph_d(font, ch, 0, 0, size)
        if d and ch != " ":
            if side == "top":
                px = cx + radius * math.sin(theta)
                py = cy - radius * math.cos(theta)
                rot = math.degrees(theta)
            else:
                px = cx + radius * math.sin(theta)
                py = cy + radius * math.cos(theta)
                rot = -math.degrees(theta)
            parts.append(
                f'<g transform="translate({px:.2f} {py:.2f}) rotate({rot:.3f}) translate({-adv/2:.2f} 0)">'
                f'<path d="{d}" fill="{fill}"/></g>'
            )
        acc += adv
    return "\n".join(parts)


def star(cx, cy, r_out, r_in, n=8, fill="#111"):
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(-90 + i * 180 / n)
        pts.append(f"{cx + r * math.cos(a):.2f},{cy + r * math.sin(a):.2f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'


def svg_doc(body: str, w=1000, h=1000, bg: str | None = None) -> str:
    bg_el = f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}">\n{bg_el}\n{body}\n</svg>\n'
    )


def write_svg(name: str, body: str, w=1000, h=1000, bg: str | None = None):
    p = OUT / name
    p.write_text(svg_doc(body, w, h, bg), encoding="utf-8")
    return p


def rsvg(src: Path, dest: Path, w: int, h: int):
    subprocess.check_call(
        ["rsvg-convert", "-w", str(w), "-h", str(h), str(src), "-o", str(dest)]
    )


# ---------------------------------------------------------------------------
# 02 peel-blob — RECUT: original blob composition, fun font+color only.
# Peel is a folded corner of the blob (not a leaf). & sits BETWEEN the two S
# letters in the monogram pocket — not stacked on the lower S.
# ---------------------------------------------------------------------------
BLOB = (
    "M 250,195 "
    "C 175,175 118,235 112,330 "
    "C 106,425 128,490 118,580 "
    "C 108,675 155,760 270,820 "
    "C 385,880 500,905 595,860 "
    "C 670,825 725,770 742,690 "
    "C 758,610 742,520 718,425 "
    "C 694,330 640,235 525,195 "
    "C 410,155 325,170 250,195 Z"
)
# Underside of the blob's own BR corner fold (clipped to blob — not a tongue).
PEEL_UNDER = "M 575,775 Q 655,815 705,885 Q 655,860 575,815 Q 560,795 575,775 Z"
PEEL_CREASE = "M 575,775 Q 655,815 705,885"


def blob_mark(font: TTFont, pal: dict, s_size=280, amp_size=152, clip: str = "blobClip") -> str:
    ink, amp, peel, cream, line = pal["ink"], pal["amp"], pal["peel"], pal["cream"], pal["line"]
    # Interlocking stacked S; & nestled in the middle-right pocket.
    s_top = text_paths(font, "S", 405, 425, s_size, ink, anchor="center", stroke=line, sw=10)
    s_bot = text_paths(font, "S", 475, 695, s_size + 8, ink, anchor="center", stroke=line, sw=10)
    ampersand = text_paths(font, "&", 525, 545, amp_size, amp, anchor="center", stroke=line, sw=8)
    bubbles = f"""
    <g fill="{cream}" stroke="{line}" stroke-width="7">
      <circle cx="655" cy="705" r="16"/>
      <circle cx="688" cy="738" r="11"/>
      <circle cx="632" cy="742" r="8"/>
    </g>"""
    inner = (
        f'<g transform="translate(500 500) scale(0.86) translate(-500 -500)">'
        f'<path d="{BLOB}" fill="none" stroke="{line}" stroke-width="10" stroke-linejoin="round"/></g>'
    )
    shadow = f'<path d="{BLOB}" fill="#1a1208" opacity=".16" transform="translate(12 18)"/>'
    sticker = f"""
    {shadow}
    <path d="{BLOB}" fill="{cream}"/>
    <path d="{BLOB}" fill="none" stroke="{line}" stroke-width="20" stroke-linejoin="round"/>
    {inner}
    <clipPath id="{clip}"><path d="{BLOB}"/></clipPath>
    <g clip-path="url(#{clip})">
      <path d="{PEEL_UNDER}" fill="{peel}"/>
    </g>
    <path d="{PEEL_CREASE}" fill="none" stroke="{line}" stroke-width="8" stroke-linecap="round"/>
    {s_top}{s_bot}{ampersand}
    {bubbles}
    """
    return f'<g transform="translate(500 508) rotate(-6) translate(-500 -500)">{sticker}</g>'


def peel_label(font: TTFont, pal: dict, word_font: TTFont) -> str:
    mark = f'<g transform="translate(-220 0) scale(0.62)">{blob_mark(font, pal)}</g>'
    name = text_paths(word_font, "Stickers&Soap Co.", 980, 292, 92, pal["ink"], anchor="center")
    return f'<g transform="translate(0 -80)">{mark}</g>{name}'


# ---------------------------------------------------------------------------
# 04 die-cut S
# ---------------------------------------------------------------------------
def diecut_mark(font: TTFont, amp_font: TTFont | None = None) -> str:
    """Original rounded vinyl S; & lives on the peeled flap only."""
    cream, ink, coral, halo_c = "#F6EDE3", "#16120F", "#F06A5A", "#FFFaf4"
    amp_font = amp_font or font
    s = text_paths(font, "S", 500, 670, 560, cream, anchor="center", stroke=ink, sw=18)
    halo = text_paths(font, "S", 500, 670, 560, cream, anchor="center", stroke=halo_c, sw=64)
    # Peel is the S lower-right terminal curling up (not a separate leaf).
    peel_d = "M 575,620 C 640,648 690,700 702,768 C 648,784 585,752 542,705 C 552,668 560,640 575,620 Z"
    peel = f"""
    <path d="{peel_d}" fill="none" stroke="{halo_c}" stroke-width="48" stroke-linejoin="round"/>
    <path d="{peel_d}" fill="{coral}" stroke="{ink}" stroke-width="8" stroke-linejoin="round"/>
    <path d="M 575,620 C 552,668 542,705 542,705" fill="none" stroke="{ink}" stroke-width="8" stroke-linecap="round"/>
    <g stroke="{ink}" stroke-width="1.5" opacity=".28">
      <path d="M 568,650 L 668,708"/>
      <path d="M 560,670 L 658,726"/>
      <path d="M 554,690 L 646,744"/>
    </g>
    """
    amp = text_group_transform(
        amp_font, "&", 638, 710, 78, cream, "rotate(32)",
        anchor="center", stroke=ink, sw=5,
    )
    bubbles = f"""
    <g fill="{coral}" stroke="{ink}" stroke-width="7">
      <circle cx="338" cy="268" r="28"/>
      <circle cx="294" cy="230" r="15"/>
      <circle cx="368" cy="222" r="10"/>
    </g>
    <g fill="{halo_c}" opacity=".55">
      <ellipse cx="330" cy="258" rx="8" ry="5" transform="rotate(-30 330 258)"/>
    </g>
    """
    shadow = text_paths(font, "S", 514, 686, 560, "#1a1208", anchor="center")
    return f'<g opacity=".16">{shadow}</g>{halo}{s}{peel}{amp}{bubbles}'


# ---------------------------------------------------------------------------
# 06 factory stamp
# ---------------------------------------------------------------------------
def stamp_mark(ring_font: TTFont, core_font: TTFont) -> str:
    ink, cream = "#1A1714", "#F3EBD8"
    top = arc_text(ring_font, "STICKERS AND SOAP CO.", 500, 500, 338, 48, ink, side="top", tracking=2.4)
    bot = arc_text(ring_font, "STICKERS AND SOAP CO.", 500, 500, 338, 48, ink, side="bottom", tracking=2.4)
    ss = text_paths(core_font, "S&S", 500, 568, 210, ink, anchor="center", tracking=-4)
    return f"""
    <circle cx="506" cy="508" r="430" fill="#1a1208" opacity=".12"/>
    <circle cx="500" cy="500" r="430" fill="{cream}"/>
    <circle cx="500" cy="500" r="418" fill="none" stroke="{ink}" stroke-width="14"/>
    <circle cx="500" cy="500" r="392" fill="none" stroke="{ink}" stroke-width="6"/>
    <circle cx="500" cy="500" r="286" fill="none" stroke="{ink}" stroke-width="8"/>
    {top}{bot}
    {ss}
    """


# ---------------------------------------------------------------------------
# 09 kraft band
# ---------------------------------------------------------------------------
def kraft_mark(font: TTFont, co_font: TTFont) -> str:
    kraft, ink = "#C4A06A", "#1A1714"
    ss = text_paths(font, "S&S", 500, 560, 268, ink, anchor="center", tracking=-6)
    co = text_paths(co_font, "CO.", 500, 668, 72, ink, anchor="center", tracking=6)
    return f"""
    <rect x="168" y="228" width="680" height="560" rx="48" fill="#1a1208" opacity=".14"/>
    <rect x="160" y="218" width="680" height="560" rx="48" fill="{kraft}"/>
    <rect x="196" y="254" width="608" height="488" rx="28" fill="none" stroke="{ink}" stroke-width="10"/>
    {ss}{co}
    """


# ---------------------------------------------------------------------------
# 13 script shop
# ---------------------------------------------------------------------------
def script_mark(script: TTFont, and_font: TTFont, co_font: TTFont) -> str:
    ink, coral = "#1A1714", "#E07A6A"
    stickers = text_paths(script, "Stickers", 500, 430, 168, ink, anchor="center")
    and_w = text_paths(script, "and", 318, 568, 78, ink, anchor="center")
    soap = text_paths(script, "Soap", 620, 620, 176, ink, anchor="center")
    co = text_paths(script, "Co.", 792, 722, 52, ink, anchor="center")
    flick = '<path d="M 250,590 C 300,606 360,602 410,586" fill="none" stroke="#1A1714" stroke-width="8" stroke-linecap="round"/>'
    bubbles = f"""
    <g fill="none" stroke="{coral}" stroke-width="6">
      <circle cx="318" cy="318" r="22"/>
      <circle cx="292" cy="292" r="10"/>
      <circle cx="348" cy="286" r="7"/>
      <circle cx="792" cy="338" r="28"/>
      <circle cx="830" cy="312" r="10"/>
      <circle cx="764" cy="308" r="8"/>
    </g>
    """
    return f"{bubbles}{stickers}{and_w}{flick}{soap}{co}"


# ---------------------------------------------------------------------------
# 17 drop ticket
# ---------------------------------------------------------------------------
def ticket_mark(ss_font: TTFont, meta: TTFont) -> str:
    cream, ink = "#F4EBD8", "#14110F"
    # body + stub with perforation notches
    body = """
    <path d="
      M 86,300
      Q 86,268 118,268
      H 682
      C 682,292 706,316 730,316
      C 754,316 778,292 778,268
      H 914
      Q 946,268 946,300
      V 700
      Q 946,732 914,732
      H 778
      C 778,708 754,684 730,684
      C 706,684 682,708 682,732
      H 118
      Q 86,732 86,700
      Z" fill="#F4EBD8"/>
    <path d="
      M 118,300
      H 650
      V 700
      H 118
      Q 118,700 118,668
      V 332
      Q 118,300 150,300
      Z" fill="none" stroke="#14110F" stroke-width="10" stroke-linejoin="round"/>
    """
    # actually draw a cleaner ticket
    ticket = f"""
    <g transform="translate(8 10)" opacity=".16">
      <rect x="80" y="300" width="840" height="400" rx="28" fill="#000"/>
    </g>
    <rect x="72" y="290" width="840" height="400" rx="28" fill="{cream}"/>
    <rect x="96" y="314" width="580" height="352" rx="16" fill="none" stroke="{ink}" stroke-width="8"/>
    <rect x="724" y="314" width="164" height="352" rx="16" fill="none" stroke="{ink}" stroke-width="8"/>
    <line x1="700" y1="330" x2="700" y2="650" stroke="{ink}" stroke-width="6" stroke-dasharray="0 18" stroke-linecap="round"/>
    <circle cx="700" cy="314" r="18" fill="#0b0b0b"/>
    <circle cx="700" cy="666" r="18" fill="#0b0b0b"/>
    """
    ss = text_group_transform(
        ss_font, "S&S", 386, 500, 168, ink, "skewX(-12)", anchor="center", tracking=-4
    )
    # outline twin for ticket sports feel
    ss_outline = text_group_transform(
        ss_font, "S&S", 386, 500, 168, "none", "skewX(-12)",
        anchor="center", tracking=-4, stroke=cream, sw=0,
    )
    drop = text_paths(meta, "LIMITED DROP", 386, 600, 36, ink, anchor="center", tracking=6)
    rules = f'<line x1="170" y1="572" x2="250" y2="572" stroke="{ink}" stroke-width="3"/>' \
            f'<line x1="522" y1="572" x2="602" y2="572" stroke="{ink}" stroke-width="3"/>'
    stub_star = star(806, 430, 28, 12, 8, ink)
    stub_line = f'<line x1="748" y1="478" x2="864" y2="478" stroke="{ink}" stroke-width="6"/>'
    stub = text_group_transform(
        meta, "STUB", 806, 600, 40, ink, "rotate(-90)", anchor="center", tracking=8
    )
    return f"{ticket}{ss}{drop}{rules}{stub_star}{stub_line}{stub}"


# ---------------------------------------------------------------------------
# 21 box logo
# ---------------------------------------------------------------------------
def box_mark(ss_font: TTFont, co_font: TTFont) -> str:
    ss = text_paths(ss_font, "S&S", 500, 545, 268, "#F7F4EE", anchor="center", tracking=-8)
    co = text_paths(co_font, "CO.", 500, 648, 64, "#F7F4EE", anchor="center", tracking=8)
    return f"""
    <rect x="150" y="250" width="700" height="500" rx="48" fill="#111111"/>
    {ss}{co}
    """


def wordmark_label(mark: str, font: TTFont, fill: str, scale=0.52) -> str:
    name = text_paths(font, "Stickers&Soap Co.", 1080, 278, 86, fill, anchor="center")
    return f'<g transform="translate(80 -20) scale({scale})">{mark}</g>{name}'


def export_square(stem: str, mark: str, bg: str):
    # transparent lock
    write_svg(f"{stem}.svg", f'<g>{mark}</g>', 1000, 1000, bg=None)
    # presentation
    pres = write_svg(f"{stem}-board.svg", f'<g>{mark}</g>', 1000, 1000, bg=bg)
    rsvg(pres, OUT / f"{stem}-sticker.png", 1024, 1024)
    rsvg(pres, OUT / f"{stem}-avatar.png", 400, 400)
    rsvg(pres, OUT / f"{stem}-avatar@2x.png", 800, 800)
    # transparent png master
    lock = OUT / f"{stem}.svg"
    rsvg(lock, OUT / f"{stem}-lock.png", 2048, 2048)


def export_label(stem: str, body: str, bg: str):
    p = write_svg(f"{stem}-label.svg", body, 1800, 500, bg=bg)
    rsvg(p, OUT / f"{stem}-label.png", 1800, 500)


def main():
    # Recut 2026-09-13: raster board assets come from build_recut.py
    # (original-composition peel-blob + diecut; reverted stamp/kraft/script/box;
    # kept drop-ticket). Do not clobber those PNGs from this vector pass.
    print("SKIP raster — run build_recut.py for the recut board")


if __name__ == "__main__":
    main()
