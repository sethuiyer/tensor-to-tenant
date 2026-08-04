"""Weekly progress dashboard.

Run from the repo root:
    python scripts/progress.py
"""

from __future__ import annotations

import datetime as dt
import csv
import re
from pathlib import Path


JOURNAL = Path("journal/weeks")
STATUS_RE = re.compile(r"- \[(?P<mark>[ xX])\]")
CORE_SECTION_RE = re.compile(r"## Core status\n(?P<body>.*?)(?=\n## |\Z)", re.DOTALL)
DEPTH_SECTION_RE = re.compile(r"## Optional depth status\n(?P<body>.*?)(?=\n## |\Z)", re.DOTALL)
FORGE_SECTION_RE = re.compile(r"## Algorithmic Forge status\n(?P<body>.*?)(?=\n## |\Z)", re.DOTALL)
EVIDENCE_FIELDS = (
    "Code / implementation",
    "Benchmark / result",
    "Design doc / technical explanation",
    "Retrospective / learning note",
)
DARBAR_TRACKER = Path("09_interview/leetcode_darbar/TRACKER.csv")


def _counts(section: str) -> tuple[int, int]:
    marks = STATUS_RE.findall(section)
    return sum(1 for mark in marks if mark.lower() == "x"), len(marks)


def _evidence_complete(text: str) -> bool:
    for field in EVIDENCE_FIELDS:
        match = re.search(rf"^- {re.escape(field)}:[ \t]*([^\n]+)$", text, re.MULTILINE)
        if not match or not match.group(1).strip():
            return False
    return True


def _program(week: int) -> str:
    if week <= 30:
        return "Foundations"
    if week <= 69:
        return "Engineering + Systems"
    return "LLM Platform"


def _darbar_counts() -> tuple[int, int]:
    if not DARBAR_TRACKER.exists():
        return 0, 0
    with DARBAR_TRACKER.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    solved = {"solved", "complete", "completed", "done"}
    return sum(row.get("Status", "").strip().lower() in solved for row in rows), len(rows)


def main() -> None:
    if not JOURNAL.exists():
        print(f"No journal directory at {JOURNAL} -- run from the repo root.")
        raise SystemExit(1)

    total_core = 0
    done_core = 0
    total_depth = 0
    done_depth = 0
    evidence_weeks = 0
    forge_required_total = 0
    forge_required_done = 0
    forge_optional_total = 0
    forge_optional_done = 0
    week_summaries = []
    program_totals: dict[str, list[int]] = {}

    for week_file in sorted(JOURNAL.glob("week_*.md")):
        text = week_file.read_text(encoding="utf-8")
        core_match = CORE_SECTION_RE.search(text)
        depth_match = DEPTH_SECTION_RE.search(text)
        core_done, core_total = _counts(core_match.group("body") if core_match else text)
        depth_done, depth_total = _counts(depth_match.group("body") if depth_match else "")
        total_core += core_total
        done_core += core_done
        total_depth += depth_total
        done_depth += depth_done
        if _evidence_complete(text):
            evidence_weeks += 1

        tier_match = re.search(r"\*\*Tier:\*\* (?P<tier>[^\n]+)", text)
        forge_tier = tier_match.group("tier").strip() if tier_match else "Archive"
        forge_match = FORGE_SECTION_RE.search(text)
        forge_done, forge_total = _counts(forge_match.group("body") if forge_match else "")
        if forge_tier in ("Core", "Boss fight"):
            forge_required_total += forge_total
            forge_required_done += forge_done
            forge_state = "done" if forge_done else "todo"
        else:
            forge_optional_total += forge_total
            forge_optional_done += forge_done
            forge_state = "optional" if forge_tier == "Supporting" else "archive"

        week_match = re.search(r"week_(\d+)", week_file.name)
        week_number = int(week_match.group(1)) if week_match else 0
        program = _program(week_number)
        program_totals.setdefault(program, [0, 0])
        program_totals[program][0] += core_done
        program_totals[program][1] += core_total
        pct = (core_done / core_total * 100.0) if core_total else 0.0
        week_summaries.append((week_file.name, core_done, core_total, pct, depth_done, forge_state))

    print(f"{'Week':<14} {'Core':>9} {'Pct':>7} {'Depth':>7} {'Forge':>9}")
    print("-" * 52)
    for name, done, total, pct, depth_done, forge_state in week_summaries:
        bar = chr(9608) * int(pct / 10) + chr(183) * (10 - int(pct / 10))
        depth_mark = "yes" if depth_done else "optional"
        print(f"{name:<14} {done:>2}/{total:<2} {pct:>6.1f}%  {depth_mark:>8} {forge_state:>9} {bar}")

    overall = (done_core / total_core * 100.0) if total_core else 0.0
    depth_overall = (done_depth / total_depth * 100.0) if total_depth else 0.0
    print("-" * 52)
    print(f"Core: {done_core}/{total_core} checkboxes -- {overall:.1f}%")
    print(f"Optional depth: {done_depth}/{total_depth} -- {depth_overall:.1f}%")
    print(f"Evidence-complete weeks: {evidence_weeks}/{len(week_summaries)}")
    forge_required_pct = (forge_required_done / forge_required_total * 100.0) if forge_required_total else 0.0
    forge_optional_pct = (forge_optional_done / forge_optional_total * 100.0) if forge_optional_total else 0.0
    print(f"Forge required: {forge_required_done}/{forge_required_total} -- {forge_required_pct:.1f}%")
    print(f"Forge supporting/archive: {forge_optional_done}/{forge_optional_total} -- {forge_optional_pct:.1f}%")
    darbar_done, darbar_total = _darbar_counts()
    darbar_pct = (darbar_done / darbar_total * 100.0) if darbar_total else 0.0
    print(f"Leetcode Darbar: {darbar_done}/{darbar_total} -- {darbar_pct:.1f}% (optional Auror lane)")
    print("\nPrograms:")
    for program in ("Foundations", "Engineering + Systems", "LLM Platform"):
        done, total = program_totals.get(program, [0, 0])
        pct = (done / total * 100.0) if total else 0.0
        print(f"  {program:<24} {done}/{total} core checkboxes -- {pct:.1f}%")


if __name__ == "__main__":
    main()
