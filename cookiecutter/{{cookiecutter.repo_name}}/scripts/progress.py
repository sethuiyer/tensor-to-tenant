"""Weekly progress dashboard.

Run from the repo root:
    python scripts/progress.py
"""

from __future__ import annotations

import datetime as dt
import re
from pathlib import Path


JOURNAL = Path("journal/weeks")
STATUS_RE = re.compile(r"- \[(?P<mark>[ xX])\]")


def main() -> None:
    if not JOURNAL.exists():
        print(f"No journal directory at {JOURNAL} -- run from the repo root.")
        raise SystemExit(1)

    total_checkboxes = 0
    done_checkboxes = 0
    week_summaries = []

    for week_file in sorted(JOURNAL.glob("week_*.md")):
        text = week_file.read_text(encoding="utf-8")
        checks = STATUS_RE.findall(text)
        total = len(checks)
        done = sum(1 for c in checks if c.lower() == "x")
        total_checkboxes += total
        done_checkboxes += done
        pct = (done / total * 100.0) if total else 0.0
        week_summaries.append((week_file.name, done, total, pct))

    print(f"{'Week':<14} {'Done':>5} {'Total':>6} {'Pct':>7}")
    print("-" * 36)
    for name, done, total, pct in week_summaries:
        bar = chr(9608) * int(pct / 10) + chr(183) * (10 - int(pct / 10))
        print(f"{name:<14} {done:>5} {total:>6} {pct:>6.1f}%  {bar}")

    overall = (done_checkboxes / total_checkboxes * 100.0) if total_checkboxes else 0.0
    print("-" * 36)
    print(f"Overall: {done_checkboxes}/{total_checkboxes} checkboxes -- {overall:.1f}%")


if __name__ == "__main__":
    main()