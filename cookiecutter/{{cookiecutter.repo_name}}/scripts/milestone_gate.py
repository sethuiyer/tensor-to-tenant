"""Milestone gate checker.

Run from the repo root:
    python scripts/milestone_gate.py
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path


GATES = [
    (6,   ["00_orientation/diagnostic.md", "Dockerfile"]),
    (18,  ["01_math/linear_algebra/notes.md"]),
    (30,  ["01_math/probability/notes.md", "01_math/statistics/notes.md"]),
    (45,  [
        "02_engineering_primitives/retrieval/__init__.py",
        "02_engineering_primitives/rate_limiting/__init__.py",
        "02_engineering_primitives/caching/__init__.py",
        "02_engineering_primitives/sketches/__init__.py",
    ]),
    (57,  ["03_system_design/writeups/"]),
    (69,  ["04_ml_systems/experimentation/"]),
    (81,  ["05_llm/rag/"]),
    (93,  ["06_inference/benchmarks.md"]),
    (102, ["07_platform/router/"]),
    (108, ["08_capstone/reports/final.md"]),
]


def main() -> None:
    today = dt.date.today()
    start = dt.date.fromisoformat("{{ cookiecutter.start_date }}")
    current_week = max(1, min(108, ((today - start).days // 7) + 1))

    print(f"Start date  : {start}")
    print(f"Today       : {today}")
    print(f"Current week: {current_week}\n")

    passed = []
    failed = []
    pending = []

    for gate_week, paths in GATES:
        if current_week < gate_week:
            pending.append(gate_week)
            continue
        if all((Path(p)).exists() for p in paths):
            passed.append(gate_week)
        else:
            failed.append((gate_week, paths))

    em_dash = chr(8212)
    print(f"Passed gates : {passed or em_dash}")
    print(f"Failed gates : {[g for g, _ in failed] or em_dash}")
    print(f"Pending gates: {pending or em_dash}\n")

    for gw, paths in failed:
        print(f"  Gate {gw} missing:")
        for p in paths:
            print(f"    - {p}")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()