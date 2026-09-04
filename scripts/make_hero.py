#!/usr/bin/env python3
"""
Build hero.svg: a neofetch-style identity card on one opaque painted panel.

Deliberately no ASCII portrait, which is where this kind of profile README
usually starts. GitHub already renders the account avatar at 260px, in colour,
directly beside the README -- an ASCII transcription of a photograph the reader
is already looking at carries no information. At a size that fits above the
fold it is illegible anyway, and at a size where it reads it costs the vertical
space that the pinned repositories occupy, which are the actual argument the
profile is making.

One file rather than the usual two-column <table> of two images: it stays
inside the ~450px budget above the fold, removes the sideways scroll a
fixed-width table causes on phones, makes a height mismatch between panels
impossible, and costs one request instead of two.

The panel paints its own background. A transparent SVG inherits the reader's
page, so a dark-tuned card is unreadable in light theme, and prefers-color-
scheme inside an <img>-embedded SVG never reaches Safari at all. Painting the
card makes the reader's theme irrelevant.

The animation is one short fade that settles and stops. The base state of the
document is the finished frame, so a renderer with no animation engine (the
VS Code preview, OG-card generators, PDF export, resvg, librsvg) shows the card
rather than an empty panel.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "contributions.json"
OUT = ROOT / "hero.svg"

NAME = "Valentino Galfré"
ROLE = "Backend & automation developer"

W = 880
PAD = 28
HEAD_H = 42
COL_X = 344          # right-hand column
LABEL_W = 76
LINE = 19
GROUP_GAP = 9

BG = "#0d1117"
FRAME = "#30363d"
INK = "#e6edf3"
TEXT = "#c9d1d9"
DIM = "#7d8590"
LABEL = "#58a6ff"
ACCENT = "#3fb950"

FONT = ("ui-monospace, SFMono-Regular, Menlo, Consolas, "
        "'DejaVu Sans Mono', monospace")

STEP = 0.028


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rows() -> list[tuple[str, list[str]]]:
    """Every value line carries a number, a proper noun or a verb.

    A line that survives that rule is evidence; one that does not is filler,
    which is the whole failure mode of profile READMEs. There is no PREV row:
    that format comes from senior profiles where "Prev: Stripe" does work, and
    filling it with coursework spends space lowering the reader's estimate.
    """
    d = json.loads(DATA.read_text())
    t = d["totals"]
    share = d.get("private_share_pct")

    year = [f"{t['year']:,} contributions · {t['last60']:,} in the last 60 days"]
    if share:
        # Stated openly. The graph is green but most of it points at client
        # repos nobody can open, so declaring the split turns a number that
        # would not survive a check into a fact about the work -- and explains
        # the public star count at the same time.
        year.append(f"~{share}% of them in private client repos")

    return [
        ("STACK", ["TypeScript · Node · Python · Next.js",
                   "Postgres · n8n · Flutter · llama.cpp"]),
        ("FOCUS", ["Local-first AI · OCR→LLM pipelines",
                   "WhatsApp, CRM and third-party API glue"]),
        ("SHIPPED", ["cotejo — on-device invoice reconciler",
                     "Vector — WhatsApp sales agent, in production",
                     "Canva pipeline — content automation"]),
        ("YEAR", year),
    ]


def main() -> None:
    data = rows()
    p: list[str] = []
    n = 0

    def line(**kw: str) -> str:
        nonlocal n
        delay = n * STEP
        n += 1
        attrs = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items())
        return f'<text class="l" {attrs} style="animation-delay:{delay:.3f}s">'

    # ── right column height drives the panel ──────────────────────────────
    body_top = HEAD_H + 30
    y = body_top
    right: list[str] = []
    for label, lines in data:
        for i, text in enumerate(lines):
            if i == 0:
                right.append(
                    line(x=str(COL_X), y=f"{y}", fill=LABEL, font_size="11.5",
                         font_weight="600") + esc(label) + "</text>"
                )
                n -= 1  # label and its first value share one delay
            right.append(
                line(x=str(COL_X + LABEL_W), y=f"{y}", fill=TEXT,
                     font_size="12.5") + esc(text) + "</text>"
            )
            y += LINE
        y += GROUP_GAP
    H = round(y - GROUP_GAP + PAD + 6)

    p.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" font-family="{FONT}">'
    )
    p.append(
        "<style>"
        "@keyframes rise{from{opacity:0;transform:translateY(3px)}"
        "to{opacity:1;transform:translateY(0)}}"
        ".l{animation:rise .45s ease-out both}"
        "@media (prefers-reduced-motion:reduce){.l{animation:none}}"
        "</style>"
    )
    p.append(f'<rect width="{W}" height="{H}" rx="12" fill="{BG}"/>')
    p.append(
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="11.5" '
        f'fill="none" stroke="{FRAME}"/>'
    )
    p.append(
        f'<text class="l" x="{PAD}" y="26" fill="{DIM}" font-size="12">'
        f'valentino@galfredev:~$ <tspan fill="{TEXT}">whoami</tspan></text>'
    )
    p.append(f'<line x1="0" y1="{HEAD_H}" x2="{W}" y2="{HEAD_H}" stroke="{FRAME}"/>')
    p.append(f'<line x1="{COL_X - 34}" y1="{HEAD_H + 16}" x2="{COL_X - 34}" '
             f'y2="{H - 20}" stroke="{FRAME}"/>')

    # ── left column: who, where, and how to reach him ─────────────────────
    n = 0
    ly = body_top + 4
    p.append(line(x=str(PAD), y=f"{ly}", fill=INK, font_size="19",
                  font_weight="600") + esc(NAME) + "</text>")
    ly += 24
    p.append(line(x=str(PAD), y=f"{ly}", fill=TEXT, font_size="12.5")
             + esc(ROLE) + "</text>")
    ly += 30
    for text in ("Córdoba, Argentina · UTC−3",
                 "Works in English and Spanish",
                 "Open to remote backend and",
                 "automation work"):
        p.append(line(x=str(PAD), y=f"{ly}", fill=DIM, font_size="12")
                 + esc(text) + "</text>")
        ly += LINE
    ly += 12
    p.append(line(x=str(PAD), y=f"{ly}", fill=DIM, font_size="12.5")
             + '~$ <tspan fill="' + ACCENT + '">galfredev.com</tspan></text>')

    p.extend(right)
    p.append("</svg>")

    svg = "".join(p)
    OUT.write_text(svg)
    print(f"wrote {OUT.relative_to(ROOT)}  {len(svg) / 1024:.1f} KB  {W}x{H}")


if __name__ == "__main__":
    main()
