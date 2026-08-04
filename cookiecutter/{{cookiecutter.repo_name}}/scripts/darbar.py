"""Prepare evidence for one Leetcode Darbar catalog slot."""

from __future__ import annotations

import argparse
from pathlib import Path


TOTAL = 548


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", type=int, required=True)
    args = parser.parse_args()
    if not 1 <= args.problem <= TOTAL:
        parser.error(f"problem must be between 1 and {TOTAL}")

    destination = Path("09_interview/leetcode_darbar") / f"problem_{args.problem:03d}.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        destination.write_text(
            f"""# Leetcode Darbar — Problem {args.problem}

**Source title / URL:**
**Category:**
**Difficulty:**
**Aligned course week:**

## Attempt log

- Attempt 1:
- Attempt 2:
- Final approach:

## Explanation

- Invariant / key observation:
- Time complexity:
- Space complexity:
- Mistake corrected:

## Production connection

- Which Tensor-to-Tenant primitive, system pattern, or platform component does this reinforce?
- What workload shape or failure mode makes the connection useful?

## Evidence

- Code:
- Tests:
- Retrospective:
""",
            encoding="utf-8",
        )
    print(f"Prepared Leetcode Darbar evidence: {destination}")


if __name__ == "__main__":
    main()
