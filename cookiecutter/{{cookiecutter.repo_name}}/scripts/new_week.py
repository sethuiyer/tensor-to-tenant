"""Generate (or refresh) the journal entry for the current week.

Run from the repo root:
    python scripts/new_week.py            # current week
    python scripts/new_week.py --week 47  # explicit
    python scripts/new_week.py --week 47 --no-open  # prepare only
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import subprocess
import sys
from pathlib import Path


JOURNAL = Path("journal/weeks")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--week", type=int, help="1-108; defaults to the current week vs start_date in README.md")
    p.add_argument("--no-open", action="store_true", help="prepare the evidence scaffold without opening an editor")
    args = p.parse_args()

    if args.week:
        target = args.week
    else:
        today = dt.date.today()
        start = _read_start_date()
        if start is None:
            print("Could not infer start_date from README.md; pass --week N.")
            sys.exit(2)
        target = max(1, min(108, ((today - start).days // 7) + 1))

    if not 1 <= target <= 108:
        p.error("week must be between 1 and 108")

    dest = JOURNAL / f"week_{target:03d}.md"
    if not dest.exists():
        print(f"{dest} does not exist -- cookiecutter should have generated all 108.")
        sys.exit(2)

    evidence = _prepare_evidence(target)
    print(f"Prepared Week {target}: {dest}")
    print(f"Evidence scaffold: {evidence}")
    if not args.no_open:
        subprocess.run([_editor(), str(dest)], check=False)


def _prepare_evidence(week: int) -> Path:
    destination = Path("evidence/weeks") / f"week_{week:03d}" / "README.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        destination.write_text(
            f"""# Evidence — Week {week}

Link the four evidence types required for the core deliverable:

- Code / implementation:
- Benchmark / result:
- Design doc / technical explanation:
- Retrospective / learning note:
""",
            encoding="utf-8",
        )
    return destination


def _read_start_date() -> dt.date | None:
    readme = Path("README.md")
    if not readme.exists():
        return None
    m = re.search(r"\*\*Start date:\*\* (\d{4}-\d{2}-\d{2})", readme.read_text(encoding="utf-8"))
    return dt.date.fromisoformat(m.group(1)) if m else None


def _editor() -> str:
    return os.environ.get("EDITOR", "vi")


if __name__ == "__main__":
    main()
