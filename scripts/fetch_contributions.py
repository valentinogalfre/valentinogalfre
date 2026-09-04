#!/usr/bin/env python3
"""
Fetch the last year of contribution data for the profile owner.

Primary source is the GraphQL API (typed contract, explicitly outside GitHub's
anti-scraping policy, no 429s from shared runner IPs). If it is unavailable the
script falls back to the public unauthenticated HTML calendar, which serves the
same numbers -- verified: both return 2237 for this account.

Everything is written to data/contributions.json, which is committed. The file
carries no wall clock, only the calendar range, so an unchanged day produces an
unchanged file and the daily workflow makes no empty commit.

Fails loudly. A silent zero here would render an empty heatmap that the workflow
would happily commit with every step green.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import requests

USER = os.environ.get("GH_PROFILE_USER", "valentinogalfre")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "contributions.json"

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount contributionLevel } }
      }
    }
  }
}
"""

LEVELS = {
    "NONE": 0,
    "FIRST_QUARTILE": 1,
    "SECOND_QUARTILE": 2,
    "THIRD_QUARTILE": 3,
    "FOURTH_QUARTILE": 4,
}


def _token() -> str | None:
    """CI supplies GH_TOKEN; locally fall back to the gh CLI's own token."""
    tok = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if tok:
        return tok
    try:
        out = subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True, timeout=10
        )
        return out.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def from_graphql() -> list[dict] | None:
    tok = _token()
    if not tok:
        print("no token available, skipping GraphQL", file=sys.stderr)
        return None
    resp = requests.post(
        "https://api.github.com/graphql",
        json={"query": QUERY, "variables": {"login": USER}},
        headers={"Authorization": f"bearer {tok}", "User-Agent": "profile-art/1.0"},
        timeout=30,
    )
    if resp.status_code != 200:
        print(f"GraphQL HTTP {resp.status_code}", file=sys.stderr)
        return None
    body = resp.json()
    if "errors" in body:
        print(f"GraphQL errors: {body['errors']}", file=sys.stderr)
        return None
    cal = body["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [
        {
            "date": d["date"],
            "count": d["contributionCount"],
            "level": LEVELS.get(d["contributionLevel"], 0),
        }
        for w in cal["weeks"]
        for d in w["contributionDays"]
    ]
    print(f"GraphQL: {len(days)} days, {cal['totalContributions']} contributions")
    return days


def from_html() -> list[dict] | None:
    """Fallback. data-level is an attribute, so the colour never depends on
    parsing localised tooltip prose -- only the exact count does."""
    from bs4 import BeautifulSoup

    resp = requests.get(
        f"https://github.com/users/{USER}/contributions",
        headers={"User-Agent": "profile-art/1.0"},
        timeout=30,
    )
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    cells = soup.select("td.ContributionCalendar-day")
    if not cells:
        print("no calendar cells in HTML", file=sys.stderr)
        return None
    tips = {t.get("for"): t.get_text(strip=True) for t in soup.find_all("tool-tip")}
    days = []
    for td in cells:
        date = td.get("data-date")
        if not date:
            continue
        text = tips.get(td.get("id"), "")
        m = re.match(r"(\d+)", text)
        days.append(
            {
                "date": date,
                "count": int(m.group(1)) if m else 0,
                "level": int(td.get("data-level") or 0),
            }
        )
    print(f"HTML fallback: {len(days)} days")
    return days


PRIVATE_QUERY = """
query {
  viewer {
    contributionsCollection {
      commitContributionsByRepository(maxRepositories: 100) {
        contributions { totalCount }
        repository { isPrivate }
      }
    }
  }
}
"""


def private_share() -> int | None:
    """Share of this year's commit contributions that live in private repos.

    Stated openly in the footer: the heatmap is green but most of it points at
    client work nobody can click into, and saying so turns an unverifiable
    number into a business fact. Needs a token that can see those repos, so it
    carries the previous value forward when CI's token cannot.
    """
    tok = _token()
    if not tok:
        return None
    try:
        resp = requests.post(
            "https://api.github.com/graphql",
            json={"query": PRIVATE_QUERY},
            headers={"Authorization": f"bearer {tok}", "User-Agent": "profile-art/1.0"},
            timeout=30,
        )
        body = resp.json()
        repos = body["data"]["viewer"]["contributionsCollection"][
            "commitContributionsByRepository"
        ]
    except (requests.RequestException, KeyError, TypeError, ValueError):
        return None
    priv = sum(r["contributions"]["totalCount"] for r in repos if r["repository"]["isPrivate"])
    total = sum(r["contributions"]["totalCount"] for r in repos)
    if total < 50:  # too few to state a share honestly
        return None
    return round(priv * 100 / total)


def streaks(days: list[dict]) -> tuple[int, int]:
    counts = [d["count"] for d in days]
    current, i = 0, len(counts) - 1
    if counts and counts[i] == 0:
        i -= 1  # today is not over yet; do not break the streak on it
    while i >= 0 and counts[i] > 0:
        current += 1
        i -= 1
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    return current, longest


def validate(days: list[dict]) -> None:
    """Gate. Anything that trips here means the source changed shape; better to
    fail the workflow than to commit a plausible-looking empty graph."""
    if not 360 <= len(days) <= 380:
        sys.exit(f"expected 360-380 days, got {len(days)}")
    total = sum(d["count"] for d in days)
    if total <= 0:
        sys.exit("total contributions is zero")
    active = sum(1 for d in days if d["count"] > 0)
    if active < 5:
        sys.exit(f"only {active} active days -- looks like a parse failure")
    if OUT.exists():
        try:
            prev = json.loads(OUT.read_text())["totals"]["year"]
            if total < prev * 0.80:
                sys.exit(f"total dropped {prev} -> {total} (>20%); refusing to write")
        except (KeyError, ValueError):
            pass


def main() -> None:
    days = from_graphql() or from_html()
    if not days:
        sys.exit("both GraphQL and HTML fallback failed")
    days.sort(key=lambda d: d["date"])
    validate(days)

    current, longest = streaks(days)
    last60 = days[-60:]

    share = private_share()
    if share is None and OUT.exists():  # carry the last known good value forward
        try:
            share = json.loads(OUT.read_text()).get("private_share_pct")
        except ValueError:
            share = None

    data = {
        "username": USER,
        "private_share_pct": share,
        "range": {"start": days[0]["date"], "end": days[-1]["date"]},
        "totals": {
            "year": sum(d["count"] for d in days),
            "last60": sum(d["count"] for d in last60),
            "active_days": sum(1 for d in days if d["count"] > 0),
            "active_days_last60": sum(1 for d in last60 if d["count"] > 0),
            "best_day": max(d["count"] for d in days),
        },
        "streak": {"current": current, "longest": longest},
        "days": days,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    t = data["totals"]
    print(
        f"wrote {OUT.relative_to(ROOT)}: {t['year']} in the year, "
        f"{t['last60']} in 60 days, {t['active_days']} active days"
    )


if __name__ == "__main__":
    main()
