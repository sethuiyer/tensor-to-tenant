# Leetcode Darbar — Parallel High-Achiever Track

The [Leetcode Darbar](https://aninokuma.codeberg.page/leetcode-darbar/) is a
parallel interview-execution track. The catalog target is **548 problems**:
255 Easy, 240 Medium, and 53 Hard. It is deliberately separate from the
Algorithmic Forge: Darbar builds speed and pattern recognition; Forge builds
algorithmic depth; Tensor-to-Tenant shows where the ideas live in production.

```text
Darbar       -> recognize and implement quickly
Algorithmic Forge -> derive, generalize, and survive adversarial workloads
Core course  -> choose the right abstraction for an AI system
```

## Two completion paths

| Path | Darbar expectation | What it proves |
|---|---|---|
| Standard Apprenticeship | One aligned problem or review set most weeks; no 548-problem requirement | Reliable interview rhythm alongside the 108-week core |
| Auror Track | All 548 catalog entries solved, explained, and tracked | High-volume execution, pattern breadth, and timed interview readiness |

The Auror target averages **about five problems per week** across 108 weeks.
That is an optional high-achiever load; it never replaces a core deliverable,
weakens a blocking gate, or turns a recovery week into a punishment week.

## Pacing map

| Weeks | Darbar emphasis | Production connection |
|---:|---|---|
| 1–6 | Arrays, strings, hash tables, stacks, queues, searching/sorting | Python engineering, APIs, diagnostics |
| 7–30 | Math, bit manipulation, divide and conquer, recursion, backtracking | Linear algebra, probability, statistics, optimization |
| 31–45 | Heaps, linked lists, tries, range queries, hashing | Retrieval, Top-K, caching, sketches, routing |
| 46–57 | Graphs, trees, greedy, DSU, range queries | System design, workflows, sharding, scheduling |
| 58–69 | Dynamic programming, greedy, math, probability | Experiment assignment, rollouts, monitoring |
| 70–81 | Strings, tries, graphs, sequence DP | Tokenization, retrieval, agents, guardrails |
| 82–102 | Heaps, priority queues, graphs, trees, range queries | Inference schedulers, quotas, queues, tenant fairness |
| 103–108 | Mixed timed sets and mock interviews | Mo's traces, Euler/DSU boss, portfolio defense |

## Weekly operating rule

The standard lane gets a deliberately small aligned set. The Auror lane uses a
five-slot queue:

```text
Mon–Thu: one catalog problem per day
Fri: one timed problem or contest set
Weekend: review, editorial rewrite, or recovery
```

Every solved entry records the problem identifier, category, difficulty,
attempts, final complexity, one mistake, and the production concept it
reinforces. A green check without an explanation is not completion evidence.

## Category spine

The catalog is organized around array, backtracking, bit manipulation, divide
and conquer, dynamic programming, graphs, greedy, hash table, heap, linked
list, math, queue, range query, recursion, searching and sorting, stack,
string, trees, and trie work. The generated tracker preserves one row per
catalog slot and lets a learner add the source title/URL without changing the
108-week curriculum.

## Concept triangulation

| Concept | Darbar speed set | Forge depth | Tensor-to-Tenant artifact |
|---|---|---|---|
| Heap | Top-K and scheduler problems | Heap invariants and adversarial streams | Streaming Top-K / inference batching |
| Trees | Traversal, LCA, tree DP | Euler Tour, HLD, DSU on Tree | Agent-execution forensics |
| Graphs | BFS/DFS and shortest paths | SCC, flow, matching, min-cost flow | Workflow and routing platform |
| Strings | Prefix matching and tries | KMP, Aho-Corasick, suffix structures | PII detector / retrieval index |
| Hashing | Frequency and lookup patterns | Consistent/rendezvous hashing | Tenant-aware routing and caches |

## Evidence and badges

The generated repository contains `09_interview/leetcode_darbar/TRACKER.csv`,
one row for each of the 548 target slots, plus a `problem_###.md` scaffold
command. `make progress` reports Darbar completion without mixing it into core
completion. `make auror` verifies the optional 548-problem badge.

The point is compounding value: someone can complete Foundations, Engineering +
Systems, or LLM Platform and stop with a credible release; someone who also
finishes Darbar and the Forge bosses has chosen the extended interview route.
