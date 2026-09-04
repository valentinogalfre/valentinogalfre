#!/usr/bin/env python3
"""
Render data/contributions.json as contrib-heatmap.svg.

Three deliberate departures from the usual profile-README heatmap:

1. Fail-open. The base state of every cell is the finished frame. The reveal
   lives only in an @keyframes rule, which non-animating renderers (librsvg,
   resvg, VS Code's preview, OG-card generators, PDF export) ignore -- so they
   show the full graph instead of a blank panel. Putting opacity:0 on the base
   rule, the common pattern, makes the artwork invisible everywhere animation
   does not run.

2. An opaque painted card. Transparent backgrounds inherit the reader's page,
   so a dark-tuned graph is unreadable in light theme, and prefers-color-scheme
   inside an <img>-embedded SVG does not reach Safari at all. Painting the card
   makes the theme irrelevant.

3. The footer states the private share. The graph is green but most of it
   points at client repos nobody can open; saying so converts an unverifiable
   number into a business fact.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "contributions.json"
OUT = ROOT / "contrib-heatmap.svg"

W, H = 880, 196
PAD_X = 27
DAYCOL = 30           # width of the Mon/Wed/Fri gutter
GRID_X = PAD_X + DAYCOL
GRID_Y = 44
PITCH = 15
CELL = 12
RADIUS = 2.5

BG = "#0d1117"
FRAME = "#30363d"
TEXT = "#7d8590"
TEXT_HI = "#c9d1d9"
SCALE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

FONT = ("ui-monospace, SFMono-Regular, Menlo, Consolas, "
        "'DejaVu Sans Mono', monospace")

DUR = 0.42            # per-cell fade
STEP = 0.0085         # per-column stagger -> ~0.9s total, then still


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def layout(days: list[dict]) -> list[dict]:
    """Assign each day a (col, row). Rows are Sun..Sat, matching GitHub."""
    out, col = [], 0
    for i, d in enumerate(days):
        row = (dt.date.fromisoformat(d["date"]).weekday() + 1) % 7
        if i and row == 0:
            col += 1
        out.append({**d, "col": col, "row": row})
    return out


def month_labels(cells: list[dict]) -> list[tuple[int, str]]:
    """One label per month, at the first column that month occupies."""
    labels, seen, last_col = [], set(), -99
    for c in cells:
        d = dt.date.fromisoformat(c["date"])
        key = (d.year, d.month)
        if key in seen or c["col"] - last_col < 3:
            continue
        seen.add(key)
        last_col = c["col"]
        labels.append((c["col"], d.strftime("%b")))
    return labels


def main() -> None:
    data = json.loads(DATA.read_text())
    cells = layout(data["days"])
    t, streak = data["totals"], data["streak"]

    # Start the stagger where the data starts, so the reveal does not spend its
    # first half second animating an empty stretch of calendar.
    active_cols = [c["col"] for c in cells if c["count"] > 0]
    first_active = min(active_cols) if active_cols else 0

    p: list[str] = []
    p.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" font-family="{FONT}">'
    )
    p.append(
        "<style>"
        f"@keyframes cell{{from{{opacity:0}}to{{opacity:1}}}}"
        f".d{{animation:cell {DUR}s ease-out both}}"
        f"@keyframes line{{from{{opacity:0}}to{{opacity:1}}}}"
        f".t{{animation:line .5s ease-out both}}"
        "@media (prefers-reduced-motion:reduce){"
        ".d,.t{animation:none}}"
        "</style>"
    )

    # card
    p.append(f'<rect width="{W}" height="{H}" rx="12" fill="{BG}"/>')
    p.append(
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="11.5" '
        f'fill="none" stroke="{FRAME}"/>'
    )

    # title
    p.append(
        f'<text class="t" x="{PAD_X}" y="26" fill="{TEXT}" font-size="12">'
        f'valentino@galfredev:~$ <tspan fill="{TEXT_HI}">./contributions</tspan></text>'
    )

    # month labels
    for col, name in month_labels(cells):
        x = GRID_X + col * PITCH
        p.append(
            f'<text class="t" x="{x}" y="{GRID_Y - 6}" fill="{TEXT}" '
            f'font-size="10" style="animation-delay:.15s">{name}</text>'
        )

    # weekday gutter
    for row, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        y = GRID_Y + row * PITCH + CELL - 2.5
        p.append(
            f'<text class="t" x="{PAD_X}" y="{y:.1f}" fill="{TEXT}" '
            f'font-size="10" style="animation-delay:.15s">{name}</text>'
        )

    # cells
    for c in cells:
        x = GRID_X + c["col"] * PITCH
        y = GRID_Y + c["row"] * PITCH
        delay = max(0, c["col"] - first_active) * STEP
        p.append(
            f'<rect class="d" x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
            f'rx="{RADIUS}" fill="{SCALE[c["level"]]}" '
            f'style="animation-delay:{delay:.3f}s"/>'
        )

    # footer
    share = data.get("private_share_pct")
    # No Less/More legend: everyone can read a heatmap, and the space buys a
    # line that says something the native graph 400px below does not.
    bits = [
        f"{t['year']:,} contributions in the last year",
        f"{t['last60']:,} in the last 60 days",
        f"{t['active_days']} active days",
    ]
    if share:
        bits.append(f"~{share}% in private client repos")
    footer = "  ·  ".join(bits)
    fy = GRID_Y + 7 * PITCH + 24
    p.append(
        f'<text class="t" x="{PAD_X}" y="{fy}" fill="{TEXT}" font-size="11" '
        f'style="animation-delay:.55s">{esc(footer)}</text>'
    )

    p.append("</svg>")
    OUT.write_text("".join(p))
    print(f"wrote {OUT.relative_to(ROOT)}  {len(''.join(p)) / 1024:.1f} KB  {W}x{H}")


if __name__ == "__main__":
    main()
