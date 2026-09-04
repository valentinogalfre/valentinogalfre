#!/usr/bin/env python3
"""
Two assertions over every generated SVG, run in CI before anything is committed.

They cover the two ways this artwork fails silently -- both of which leave the
workflow green and the profile broken:

  1. A stray unescaped "&" makes the file invalid XML. The browser reports
     naturalWidth 0 and logs nothing; the image is simply absent.

  2. The animation hides the artwork in the base state. Renderers with no
     animation engine then show an empty panel. This is the default outcome of
     the usual `opacity: 0` + `animation: ... forwards` pattern, and it is what
     the reference implementation this project started from does: rasterised,
     its portrait is a blank terminal window and its heatmap has zero visible
     cells.

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

    # The reveal must live in @keyframes only. A base rule that hides the
    # element is what makes the artwork disappear outside a browser.
    for rule in re.findall(r"\.[a-z]\s*\{([^}]*)\}", raw):
        if re.search(r"opacity\s*:\s*0(?!\.)", rule):
            errors.append(f"base rule hides content (fails closed): {{{rule.strip()}}}")

    # Same failure in SMIL form: a clip or rect that starts at zero width and is
    # only opened by an <animate>.
    if re.search(r'<rect[^>]*\bwidth="0"[^>]*>\s*<animate', raw):
        errors.append("clip rect starts at width=0 (fails closed)")

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
