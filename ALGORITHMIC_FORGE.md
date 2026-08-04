# Algorithmic Forge

The Algorithmic Forge is a parallel spine through the 108-week apprenticeship.
It runs on Friday alongside the AI-systems track; it does not create a second
108-week course.

```text
Monday     theory and mathematics
Tuesday    production implementation
Wednesday  systems, papers, and architecture
Thursday   evaluation and interview design
Friday     Algorithmic Forge drill + review / retro
Weekend    recovery, revision, or contest
```

The Forge shares the interview surface with the canonical
[`SYSTEM_DESIGN_TRACK.md`](./SYSTEM_DESIGN_TRACK.md) and the optional
[`LEETCODE_DARBAR.md`](./LEETCODE_DARBAR.md) lane:

```text
Darbar  = speed and pattern recognition
Forge   = depth and adversarial reasoning
Design  = workload-shaped architecture and trade-off defense
```

System Design supplies the Week 46-57 workload context for graph, flow,
hashing, scheduling, and queue drills. Darbar supplies a separate high-volume
execution target; it is never silently counted as Forge evidence.

The Forge is where the programming-camp material belongs. The AI-systems
curriculum supplies the context; the algorithmic drill supplies implementation
combat. A learner should be able to explain why an algorithm fits the workload,
not merely recite its name.

## Four treatment levels

| Level | Treatment | Timebox | Completion rule |
|---|---|---:|---|
| **Core** | Recurring Friday skill that directly supports the current phase | 45–90 min | Implement, test, explain complexity and trade-offs |
| **Supporting** | Guided lab or one representative problem | 45–120 min | Attempt when relevant; record the result and what remains unclear |
| **Archive** | Reference material for future use or unusual interview prompts | 0 min scheduled | No weekly obligation; promote it only when a project needs it |
| **Boss fight** | A selected advanced problem integrated with a gate or capstone | 2–3 hr | Complete the artifact, write the reasoning, and include a retrospective |

Supporting and Archive are not hidden prerequisites. A Boss fight is a bounded
depth extension unless the learner explicitly chooses it as the release artifact.
The Week 30, 69, and 108 program releases require the Core Forge evidence for
their range; they do not require every Archive topic.

## Coverage audit

| Programming-camp area | Forge treatment | Where it lands |
|---|---|---|
| Complexity, arrays, prefix sums, binary search, greedy | Core | Weeks 1–6 and recurring |
| Matrix operations, Gaussian elimination, exponentiation, recurrences | Core | Weeks 7–18 |
| Probability, expectation DP, combinatorics, modular arithmetic, gcd/sieve | Core | Weeks 23–30 and Weeks 58–69 |
| Heaps, hashing, tries, Fenwick trees, segment trees, DSU | Core | Weeks 31–45 |
| BFS/DFS, SCCs, topological sort, shortest paths | Core | Weeks 46–52 |
| MST, Euler paths, flows, matching | Core concepts; selected Boss fights | Weeks 53–57 |
| Dynamic programming and state-space reduction | Core | Weeks 58–69 |
| KMP, Aho–Corasick, retrieval-oriented string matching | Core | Weeks 70–81 |
| Suffix arrays, suffix trees, suffix automata | Supporting / Archive | Weeks 70–81; project-driven promotion |
| Scheduling, interval structures, randomized algorithms, capacity search | Core / Supporting | Weeks 82–102 |
| Euler Tour, DSU on Tree, Mo’s algorithm | Boss fights | Weeks 103–108 |
| Computational geometry | Supporting basics; Archive advanced geometry | Weeks 1–30 and project-driven |
| HLD, dynamic trees, Link-Cut Trees, exotic contest structures | Archive / Boss fight | Capstone extensions only |

## 108-week Forge map

| Weeks | Forge theme | Default tier | Example artifact |
|---:|---|---|---|
| 1–6 | Complexity, arrays, prefix sums, two pointers, binary search, bitmasks | Core | Timed implementation drill with complexity note |
| 7–14 | Matrix multiplication, Gaussian elimination, matrix exponentiation, recurrences | Core | From-scratch matrix or recurrence solver |
| 15–22 | Numerical methods, binary search on answer, ternary search, Newton iteration | Supporting | Root-finding or optimization comparison |
| 23–30 | Probability simulation, expectation DP, combinatorics, inclusion-exclusion, number theory basics | Core | Expectation/counting lab; Week 30 mini-contest |
| 31–37 | Heaps, hashing, tries, linked structures, intervals, basic pattern matching | Core | Retrieval/cache primitive plus timed data-structure drill |
| 38–45 | Fenwick, segment trees, range queries, sketches, DSU, randomized hashing | Core | Range-query or routing primitive; Week 45 mini-contest |
| 46–52 | Graph representation, BFS/DFS, SCC, topological sort, shortest paths | Core | Dependency graph or routing implementation |
| 53–57 | MST, Euler paths, max flow, min-cost flow, matching | Core / Supporting | Resource-allocation design; Week 57 graph boss fight |
| 58–69 | DP, greedy, bitmask DP, probability DP, experiment assignment | Core | Evaluation or assignment tool with algorithmic analysis |
| 70–81 | KMP, Aho–Corasick, trie retrieval, sequence DP, suffix-array survey | Core / Supporting | Pattern detector or retrieval index; Week 81 string boss |
| 82–93 | Priority scheduling, interval allocation, capacity search, randomized load balancing | Core / Supporting | Scheduler benchmark; Week 93 inference boss |
| 94–102 | Euler indexing, subtree aggregation, DSU on Tree, HLD survey | Supporting / Boss | Tenant-tree query lab; Week 102 platform boss |
| 103–108 | Mo’s algorithm, capstone integration, tree forensics | Boss fights | Capstone 1 required; Capstone 2 optional at Week 108 |

## Boss-fight catalog

These are deliberately selected extensions, not another mandatory syllabus:

1. **Week 18 — Numerical matrix boss:** Gaussian elimination, matrix
   exponentiation, or randomized SVD with numerical-stability notes.
2. **Week 30 — Foundations mini-contest:** expectation DP, combinatorics,
   modular arithmetic, and one optimization search problem.
3. **Week 45 — Data-structure mini-contest:** Fenwick/segment tree, DSU,
   hashing, and a range-query workload.
4. **Week 57 — Graph/flow boss:** Euler indexing plus a flow or matching
   formulation for scheduling/resource allocation.
5. **Week 69 — MLOps algorithm boss:** experiment assignment, greedy rollout,
   or bandit allocation with a correctness and trade-off report.
6. **Week 81 — String/agent boss:** Aho–Corasick tool/prompt detector or
   sequence-DP planner.
7. **Week 93 — Inference boss:** priority scheduling, interval allocation, and
   binary search on capacity backed by a benchmark.
8. **Week 102 — Platform tree boss:** Euler Tour plus DSU-on-Tree subtree
   analytics, used as preparation for Capstone 2.
9. **Weeks 103–108 — Capstone 1:** Mo’s algorithm over immutable LLM traces is
   the required algorithmic capstone.
10. **Week 108 optional boss — Capstone 2:** Euler Tour + DSU on Tree over
    agent execution trees. It earns extra depth credit but is not required for
    the LLM Platform badge.

Optional nightmare extensions—HLD path queries, min-cost-flow schedulers,
Aho–Corasick PII detectors, suffix-automaton log analyzers, and computational
geometry for GPU placement—belong in `boss_fights/`, not in the core calendar.

## Folder contract in a generated learner repo

```text
09_interview/algorithmic_forge/
  README.md
  core/          # required recurring drills
  supporting/    # guided labs and project-driven topics
  archive/       # indexed references; no scheduled work
  boss_fights/   # selected gate/capstone extensions
```

Every Forge artifact records:

- the workload shape and why the algorithm fits it;
- implementation and tests;
- time and space complexity;
- one failure mode or counterexample;
- a short explanation suitable for an interview.

## Selection rule

When a week is busy, do the Core AI-systems deliverable and the Core Forge
drill. When capacity is available, select one Supporting lab. Promote an
Archive topic only when a capstone, project, or interview requires it. Never
turn the existence of a harder topic into a reason to block the main program.

The source inventory is preserved in `PROGRAMMING_CAMP.md`. The tree-forensics
boss is specified in `CAPSTONE2_EULER_DSU.md`; its corrected complexity and
snapshot caveats should be treated as part of the Boss-fight review.
