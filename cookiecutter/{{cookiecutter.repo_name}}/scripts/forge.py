"""Prepare an Algorithmic Forge artifact for a specific week.

Run from the repo root:
    python scripts/forge.py --week 57
"""

from __future__ import annotations

import argparse
from pathlib import Path


LANES = [
    (1, 6, "core", "Complexity, arrays, prefix sums, two pointers, binary search, bitmasks"),
    (7, 14, "core", "Matrix operations, Gaussian elimination, exponentiation, recurrences"),
    (15, 22, "supporting", "Numerical methods, binary search on answer, ternary search, Newton iteration"),
    (23, 30, "core", "Probability simulation, expectation DP, combinatorics, inclusion-exclusion, number theory basics"),
    (31, 37, "core", "Heaps, hashing, tries, linked structures, intervals, basic pattern matching"),
    (38, 45, "core", "Fenwick trees, segment trees, range queries, sketches, DSU, randomized hashing"),
    (46, 52, "core", "Graph representation, BFS/DFS, SCC, topological sort, shortest paths"),
    (53, 57, "core", "MST, Euler paths, max flow, min-cost flow, matching"),
    (58, 69, "core", "Dynamic programming, greedy methods, bitmask DP, probability DP, experiment assignment"),
    (70, 81, "core", "KMP, Aho-Corasick, trie retrieval, sequence DP, suffix-array survey"),
    (82, 93, "supporting", "Priority scheduling, interval allocation, capacity search, randomized load balancing"),
    (94, 102, "supporting", "Euler indexing, subtree aggregation, DSU on Tree, HLD survey"),
    (103, 108, "boss_fights", "Mo's algorithm, capstone integration, and tree forensics"),
]

BOSSES = {
    18: ("Numerical matrix boss", "Gaussian elimination, matrix exponentiation, or randomized SVD with stability notes."),
    30: ("Foundations mini-contest", "Expectation DP, combinatorics, modular arithmetic, and optimization search."),
    45: ("Data-structure mini-contest", "Fenwick/segment tree, DSU, hashing, and a range-query workload."),
    57: ("Graph/flow boss", "Euler indexing plus a flow or matching formulation for resource allocation."),
    69: ("MLOps algorithm boss", "Experiment assignment, greedy rollout, or bandit allocation with trade-offs."),
    81: ("String/agent boss", "Aho-Corasick tool or prompt detector, or a sequence-DP planner."),
    93: ("Inference scheduling boss", "Priority scheduling, interval allocation, and binary search on capacity."),
    102: ("Platform tree boss", "Euler Tour plus DSU on Tree subtree analytics."),
    108: ("Capstone 2 optional boss", "Euler Tour + DSU on Tree over agent execution trees."),
}


def forge_for_week(week: int) -> tuple[str, str, str]:
    if week in BOSSES:
        name, drill = BOSSES[week]
        return "boss_fights", name, drill
    for start, end, tier, topic in LANES:
        if start <= week <= end:
            return tier, topic, "Choose one representative problem and record implementation, complexity, and a failure mode."
    raise ValueError(f"no Forge lane for Week {week}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", type=int, required=True)
    args = parser.parse_args()
    if not 1 <= args.week <= 108:
        parser.error("--week must be between 1 and 108")

    tier, theme, drill = forge_for_week(args.week)
    destination = Path("09_interview/algorithmic_forge") / tier / f"week_{args.week:03d}.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        destination.write_text(
            f"""# Algorithmic Forge — Week {args.week}

**Tier:** {tier.replace('_', ' ').title()}
**Theme:** {theme}
**Drill:** {drill}

## Workload fit

- What is the input/query shape?
- Why does this algorithm fit the workload?

## Implementation

- Code:
- Tests:

## Analysis

- Time complexity:
- Space complexity:
- Failure mode / counterexample:
- Interview explanation:

## Outcome

- Result:
- Retrospective:
""",
            encoding="utf-8",
        )
    print(f"Prepared Algorithmic Forge artifact: {destination}")


if __name__ == "__main__":
    main()
