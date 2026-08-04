"""Prepare a recovery window after an instructional week.

Run from the repo root:
    python scripts/recovery.py --after-week 14
"""

from __future__ import annotations

import argparse
from pathlib import Path


RECOVERY_AFTER = {6, 14, 22, 30, 38, 46, 54, 62, 70, 78, 86, 94, 102}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--after-week", type=int, required=True, dest="after_week")
    args = parser.parse_args()

    if not 1 <= args.after_week <= 107:
        parser.error("--after-week must be between 1 and 107")

    destination = Path("journal/recovery") / f"after_week_{args.after_week:03d}.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        destination.write_text(
            f"""# Recovery window after Week {args.after_week}

This is a deliberate buffer window, not an additional curriculum topic.
Use it for catch-up, remediation, benchmark reruns, or rest.

## Recovery decision

- [ ] Review incomplete core work from Weeks {max(1, args.after_week - 7)}-{args.after_week}
- [ ] Close one evidence gap (implementation, result, explanation, or retro)
- [ ] Rerun the relevant tests or benchmark
- [ ] Update the affected journal entry and evidence record
- [ ] Check the next blocking gate
- [ ] Continue to the next week
- [ ] Start a targeted remediation plan instead

## Notes

- What needs recovery:
- What I will deliberately defer:
- What will make the next instructional week sustainable:
""",
            encoding="utf-8",
        )

    suggested = "suggested checkpoint" if args.after_week in RECOVERY_AFTER else "custom recovery window"
    print(f"Prepared {suggested}: {destination}")


if __name__ == "__main__":
    main()
