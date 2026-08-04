"""Verify the optional 548-problem Leetcode Darbar track."""

from __future__ import annotations

import csv
from pathlib import Path


TOTAL = 548
SOLVED = {"solved", "complete", "completed", "done"}


def main() -> None:
    tracker = Path("09_interview/leetcode_darbar/TRACKER.csv")
    if not tracker.exists():
        print(f"Missing tracker: {tracker}")
        raise SystemExit(2)

    with tracker.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    solved = sum(row.get("Status", "").strip().lower() in SOLVED for row in rows)
    total = len(rows) or TOTAL
    print(f"Auror Darbar: {solved}/{total} solved ({solved / total * 100:.1f}%)")
    if total != TOTAL:
        print(f"Warning: expected {TOTAL} tracker rows")
    if solved < TOTAL:
        print("Auror badge: NOT EARNED")
        raise SystemExit(1)
    print("Auror badge: EARNED")


if __name__ == "__main__":
    main()
