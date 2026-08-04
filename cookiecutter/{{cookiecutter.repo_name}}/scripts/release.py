"""Prepare one of the three portfolio release checklists.

Run from the repo root:
    python scripts/release.py --week 30
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


RELEASES = {
    30: ("Foundations", "Weeks 1-30", "math, numerical routines, and experimentation", 30),
    69: ("Engineering + Systems", "Weeks 31-69", "tested primitives, system designs, and MLOps", 69),
    108: ("LLM Platform", "Weeks 70-108", "LLM/RAG work, inference, platform, and capstone", 108),
}

EVIDENCE_FIELDS = (
    "Code / implementation",
    "Benchmark / result",
    "Design doc / technical explanation",
    "Retrospective / learning note",
)


def _core_complete(text: str) -> bool:
    section = re.search(r"## Core status\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if not section:
        return False
    marks = re.findall(r"- \[([ xX])\]", section.group(1))
    return bool(marks) and all(mark.lower() == "x" for mark in marks)


def _evidence_complete(text: str) -> bool:
    for field in EVIDENCE_FIELDS:
        match = re.search(rf"^- {re.escape(field)}:[ \t]*([^\n]+)$", text, re.MULTILINE)
        if not match or not match.group(1).strip():
            return False
    return True


def _forge_required_and_complete(text: str) -> tuple[bool, bool]:
    tier_match = re.search(r"\*\*Tier:\*\* (?P<tier>[^\n]+)", text)
    if not tier_match:
        return False, True
    required = tier_match.group("tier").strip() in ("Core", "Boss fight")
    if not required:
        return False, True
    section = re.search(r"## Algorithmic Forge status\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if not section:
        return True, False
    marks = re.findall(r"- \[([ xX])\]", section.group(1))
    return True, bool(marks) and all(mark.lower() == "x" for mark in marks)


def _all_gates_pass_through(gate_number: int) -> bool:
    try:
        from milestone_gate import GATES
    except ImportError:
        return False
    for gate, paths in GATES:
        if gate <= gate_number and not all(Path(path).exists() for path in paths):
            return False
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", type=int, required=True)
    parser.add_argument("--check", action="store_true", help="verify evidence and award the badge when eligible")
    args = parser.parse_args()

    if args.week not in RELEASES:
        parser.error("--week must be one of: 30, 69, 108")

    name, weeks, focus, gate_number = RELEASES[args.week]
    slug = name.lower().replace(" + ", "_").replace(" ", "_")
    destination = Path("portfolio/releases") / f"{slug}_week_{args.week:03d}.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        destination.write_text(
            f"""# {name} release — Week {args.week}

**Coverage:** {weeks}
**Release focus:** {focus}

This release is a public checkpoint. It should stand on its own even if the
learner pauses before the next program.

## Program badge

**Badge:** Tensor-to-Tenant {name}
**Status:** NOT EARNED — run `make badge={args.week}` to verify the evidence.
**Eligibility:** core evidence for this program plus Gate {gate_number} passing.

## Release checklist

- [ ] Select the strongest core artifacts from this program
- [ ] Link implementation/code
- [ ] Link benchmark or measurable result
- [ ] Link design document or technical explanation
- [ ] Link retrospective and lessons learned
- [ ] Add a short README explaining what works, what does not, and what comes next
- [ ] Run Gate {gate_number} and record the result
- [ ] Publish or share the release

## Evidence links

- Code:
- Benchmark / result:
- Design / explanation:
- Retrospective:
- Gate result:

## Release summary

- What I can build now:
- The most important trade-off I learned:
- The next capability I want to develop:
""",
            encoding="utf-8",
        )

    if not args.check:
        print(f"Prepared portfolio release: {destination}")
        return

    start_week = 1 if args.week == 30 else (31 if args.week == 69 else 70)
    core_weeks = range(start_week, args.week + 1)
    core_complete = all(
        _core_complete((Path("journal/weeks") / f"week_{week:03d}.md").read_text(encoding="utf-8"))
        for week in core_weeks
    )
    evidence_complete = all(
        _evidence_complete((Path("journal/weeks") / f"week_{week:03d}.md").read_text(encoding="utf-8"))
        for week in core_weeks
    )
    forge_checks = [
        _forge_required_and_complete((Path("journal/weeks") / f"week_{week:03d}.md").read_text(encoding="utf-8"))
        for week in core_weeks
    ]
    forge_complete = all(complete for required, complete in forge_checks if required)
    gates_complete = _all_gates_pass_through(gate_number)
    eligible = core_complete and evidence_complete and forge_complete and gates_complete
    status = "EARNED" if eligible else "NOT EARNED"
    release_text = destination.read_text(encoding="utf-8")
    release_text = re.sub(r"\*\*Status:\*\* .*", f"**Status:** {status}", release_text, count=1)
    destination.write_text(release_text, encoding="utf-8")

    print(f"Badge: {name}")
    print(f"Core weeks complete    : {'yes' if core_complete else 'no'}")
    print(f"Evidence complete      : {'yes' if evidence_complete else 'no'}")
    print(f"Forge Core/Boss complete: {'yes' if forge_complete else 'no'}")
    print(f"Gates through release  : {'yes' if gates_complete else 'no'}")
    print(f"Badge status           : {status}")
    if not eligible:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
