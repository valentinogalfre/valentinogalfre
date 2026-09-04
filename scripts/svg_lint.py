#!/usr/bin/env python3
"""
Two assertions over every generated SVG, run in CI before anything is committed.

They cover the two ways this artwork fails silently -- both of which leave the
workflow green and the profile broken:

  1. A stray unescaped "&" makes the file invalid XML. The browser reports
     naturalWidth 0 and logs nothing; the image is simply absent.

  2. The file contains any declarative animation at all. Verified against the
     live profile in Chrome: an SVG loaded through <img> is painted at t=0 and
     its timeline never advances, so a CSS @keyframes fade with fill-mode
     `both`, or a SMIL `<set begin="0s">`, applies its hidden 0% state and stays
     there. The artwork renders as an empty panel -- which is exactly what the
     reference implementation this project started from does today, in a
     browser and in every static rasteriser.

     So this is not a style rule. Animation here has no upside (it never plays)
     and one large downside (it can silently blank the page), which makes any
     of it a defect.

defusedxml rather than the standard library: stdlib XML parsers accept external
entities and nested-entity expansion by default.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from defusedxml.minidom import parse

MIN_BYTES = 1500


def check(path: Path) -> list[str]:
    errors: list[str] = []
    raw = path.read_text()

    if len(raw) < MIN_BYTES:
        errors.append(f"only {len(raw)} bytes -- looks truncated")

    try:
        parse(str(path))
    except Exception as exc:  # noqa: BLE001 - any parse failure is the failure
        errors.append(f"not well-formed XML: {exc}")

    if "@keyframes" in raw or "animation:" in raw or "animation-delay" in raw:
        errors.append("CSS animation present -- never plays inside <img>, "
                      "and pins elements at the 0% frame")

    for tag in ("<animate", "<animateTransform", "<animateMotion", "<set "):
        if tag in raw:
            errors.append(f"SMIL {tag.strip('< ')} present -- the timeline "
                          "never advances inside <img>")
            break

    # The specific shape that makes the artwork vanish, kept as its own message
    # because it is the one people reach for first.
    for rule in re.findall(r"\.[a-z]\s*\{([^}]*)\}", raw):
        if re.search(r"opacity\s*:\s*0(?!\.)", rule):
            errors.append(f"base rule hides content: {{{rule.strip()}}}")

    if re.search(r'<rect[^>]*\bwidth="0"[^>]*>\s*<animate', raw):
        errors.append("clip rect starts at width=0 and is only opened by animation")

    return errors


def main() -> None:
    targets = [Path(a) for a in sys.argv[1:]]
    if not targets:
        sys.exit("usage: svg_lint.py <file.svg> [...]")

    failed = False
    for path in targets:
        if not path.exists():
            print(f"FAIL {path}: missing")
            failed = True
            continue
        errors = check(path)
        if errors:
            failed = True
            for e in errors:
                print(f"FAIL {path}: {e}")
        else:
            print(f"ok   {path}  {path.stat().st_size / 1024:.1f} KB")

    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
