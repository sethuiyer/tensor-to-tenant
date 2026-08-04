"""Prepare a focused remediation plan for a blocked milestone gate.

Run from the repo root:
    python scripts/remediate.py --gate 18
"""

from __future__ import annotations

import argparse
from pathlib import Path


GATES = {
    6: "orientation, tooling, and systems diagnostic",
    18: "linear algebra and numerical routines",
    30: "calculus, statistics, and experimentation foundations",
    45: "engineering primitives and their tests",
    57: "system design case studies",
    69: "experimentation, evaluation, and MLOps",
    81: "LLM, RAG, memory, and agent foundations",
    93: "inference benchmarking and operations",
    102: "production AI platform capabilities",
    108: "capstone, portfolio, and interview readiness",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gate", type=int, required=True)
    args = parser.parse_args()

    if args.gate not in GATES:
        parser.error(f"--gate must be one of: {', '.join(map(str, sorted(GATES)))}")

    destination = Path("journal/remediation") / f"gate_{args.gate:03d}.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        destination.write_text(
            f"""# Remediation plan — Gate {args.gate}

**Blocked capability:** {GATES[args.gate]}

This is a targeted repair cycle. Do not begin new gate-dependent content until
the missing evidence is complete and the gate checker passes.

## Diagnosis

- Failed criterion:
- Evidence that is missing or too weak:
- Why the original attempt failed:

## Seven-day repair plan

- [ ] Day 1: identify the smallest missing concept or capability
- [ ] Day 2: review the relevant notes or source material
- [ ] Day 3: implement or rewrite the smallest working version
- [ ] Day 4: test, benchmark, or verify it
- [ ] Day 5: explain the trade-offs in writing or out loud
- [ ] Day 6: package code, result, explanation, and retrospective evidence
- [ ] Day 7: rerun `make gate` and record the outcome

## Exit evidence

- Implementation:
- Benchmark / result:
- Technical explanation:
- Retrospective:
- Gate result:
""",
            encoding="utf-8",
        )

    print(f"Prepared remediation plan: {destination}")


if __name__ == "__main__":
    main()
