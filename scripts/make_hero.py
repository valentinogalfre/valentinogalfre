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

There is no animation, and that is a measured decision rather than a stylistic
one. Tested on the live profile in Chrome: an SVG loaded through <img> is
rendered at t=0 and its timeline never advances. Neither mechanism survives it.

  - CSS @keyframes with `animation-fill-mode: both` pins every element at the
    0% frame. With a fade-in that is opacity 0, so the card renders completely
    blank -- background and divider only. This was published and confirmed
    broken before being removed.
  - SMIL is no better: a `<set>` with begin="0s" applies its hiding value and
    the `<animate>` that should restore it never runs.

So a reveal effect here is not merely ineffective, it is destructive: both
mechanisms apply their initial hidden state and never recover from it. The
widely repeated claim that CSS animation works inside an <img>-embedded SVG on
GitHub does not hold, and the profile READMEs built on it are showing empty
panels to everyone.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "contributions.json"
OUT = ROOT / "hero.svg"

NAME = "Valentino Galfré"
ROLE = "Full-stack developer · freelance"

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
        ("BUILDS", ["Web apps, automations and WhatsApp",
                    "bots for real, paying clients"]),
        ("STACK", ["TypeScript · Node · Python · Next.js",
                   "Postgres · n8n · Flutter · llama.cpp"]),
        ("FOCUS", ["Local-first AI · OCR→LLM pipelines",
                   "CRM and third-party API integration"]),
        ("SHIPPED", ["cotejo — on-device invoice reconciler",
                     "Vector — WhatsApp sales agent, in production",
                     "Canva pipeline — content automation"]),
        ("YEAR", year),
    ]


def main() -> None:
    data = rows()
    p: list[str] = []

    def line(**kw: str) -> str:
        attrs = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items())
        return f"<text {attrs}>"

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
    p.append(f'<rect width="{W}" height="{H}" rx="12" fill="{BG}"/>')
    p.append(
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="11.5" '
        f'fill="none" stroke="{FRAME}"/>'
    )
    p.append(
        f'<text x="{PAD}" y="26" fill="{DIM}" font-size="12">'
        f'valentino@galfredev:~$ <tspan fill="{TEXT}">whoami</tspan></text>'
    )
    p.append(f'<line x1="0" y1="{HEAD_H}" x2="{W}" y2="{HEAD_H}" stroke="{FRAME}"/>')
    p.append(f'<line x1="{COL_X - 34}" y1="{HEAD_H + 16}" x2="{COL_X - 34}" '
             f'y2="{H - 20}" stroke="{FRAME}"/>')

    # ── left column: who, where, and how to reach him ─────────────────────
    ly = body_top + 4
    p.append(line(x=str(PAD), y=f"{ly}", fill=INK, font_size="19",
                  font_weight="600") + esc(NAME) + "</text>")
    ly += 24
    p.append(line(x=str(PAD), y=f"{ly}", fill=TEXT, font_size="12.5")
             + esc(ROLE) + "</text>")
    ly += 30
    for text in ("Córdoba, Argentina · UTC−3",
                 "Works in English and Spanish",
                 "Open to freelance and remote work"):
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
