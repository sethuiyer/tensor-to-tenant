/**
 * Algorithmic Forge — the parallel Friday algorithmic spine.
 * Transcribed from ALGORITHMIC_FORGE.md.
 */

export interface ForgeTier {
  level: string;
  treatment: string;
  timebox: string;
  rule: string;
}

export const FORGE_TIERS: ForgeTier[] = [
  { level: 'Core', treatment: 'Recurring Friday skill that directly supports the current phase', timebox: '45–90 min', rule: 'Implement, test, explain complexity and trade-offs' },
  { level: 'Supporting', treatment: 'Guided lab or one representative problem', timebox: '45–120 min', rule: 'Attempt when relevant; record the result and what remains unclear' },
  { level: 'Archive', treatment: 'Reference material for future use or unusual interview prompts', timebox: '0 min scheduled', rule: 'No weekly obligation; promote it only when a project needs it' },
  { level: 'Boss fight', treatment: 'A selected advanced problem integrated with a gate or capstone', timebox: '2–3 hr', rule: 'Complete the artifact, write the reasoning, and include a retrospective' },
];

export interface ForgeLane {
  weeks: string;
  theme: string;
  tier: string;
  artifact: string;
}

export const FORGE_LANES: ForgeLane[] = [
  { weeks: '1–6', theme: 'Complexity, arrays, prefix sums, two pointers, binary search, bitmasks', tier: 'Core', artifact: 'Timed implementation drill with complexity note' },
  { weeks: '7–14', theme: 'Matrix multiplication, Gaussian elimination, matrix exponentiation, recurrences', tier: 'Core', artifact: 'From-scratch matrix or recurrence solver' },
  { weeks: '15–22', theme: 'Numerical methods, binary search on answer, ternary search, Newton iteration', tier: 'Supporting', artifact: 'Root-finding or optimization comparison' },
  { weeks: '23–30', theme: 'Probability simulation, expectation DP, combinatorics, inclusion-exclusion, number theory basics', tier: 'Core', artifact: 'Expectation/counting lab; Week 30 mini-contest' },
  { weeks: '31–37', theme: 'Heaps, hashing, tries, linked structures, intervals, basic pattern matching', tier: 'Core', artifact: 'Retrieval/cache primitive plus timed data-structure drill' },
  { weeks: '38–45', theme: 'Fenwick, segment trees, range queries, sketches, DSU, randomized hashing', tier: 'Core', artifact: 'Range-query or routing primitive; Week 45 mini-contest' },
  { weeks: '46–52', theme: 'Graph representation, BFS/DFS, SCC, topological sort, shortest paths', tier: 'Core', artifact: 'Dependency graph or routing implementation' },
  { weeks: '53–57', theme: 'MST, Euler paths, max flow, min-cost flow, matching', tier: 'Core / Supporting', artifact: 'Resource-allocation design; Week 57 graph boss fight' },
  { weeks: '58–69', theme: 'DP, greedy, bitmask DP, probability DP, experiment assignment', tier: 'Core', artifact: 'Evaluation or assignment tool with algorithmic analysis' },
  { weeks: '70–81', theme: 'KMP, Aho–Corasick, trie retrieval, sequence DP, suffix-array survey', tier: 'Core / Supporting', artifact: 'Pattern detector or retrieval index; Week 81 string boss' },
  { weeks: '82–93', theme: 'Priority scheduling, interval allocation, capacity search, randomized load balancing', tier: 'Core / Supporting', artifact: 'Scheduler benchmark; Week 93 inference boss' },
  { weeks: '94–102', theme: 'Euler indexing, subtree aggregation, DSU on Tree, HLD survey', tier: 'Supporting / Boss', artifact: 'Tenant-tree query lab; Week 102 platform boss' },
  { weeks: '103–108', theme: 'Mo’s algorithm, capstone integration, tree forensics', tier: 'Boss fights', artifact: 'Capstone 1 required; Capstone 2 optional at Week 108' },
];

export interface ForgeBoss {
  name: string;
  description: string;
}

export const FORGE_BOSSES: ForgeBoss[] = [
  { name: 'Week 18 — Numerical matrix boss', description: 'Gaussian elimination, matrix exponentiation, or randomized SVD with numerical-stability notes.' },
  { name: 'Week 30 — Foundations mini-contest', description: 'Expectation DP, combinatorics, modular arithmetic, and one optimization search problem.' },
  { name: 'Week 45 — Data-structure mini-contest', description: 'Fenwick/segment tree, DSU, hashing, and a range-query workload.' },
  { name: 'Week 57 — Graph/flow boss', description: 'Euler indexing plus a flow or matching formulation for scheduling/resource allocation.' },
  { name: 'Week 69 — MLOps algorithm boss', description: 'Experiment assignment, greedy rollout, or bandit allocation with a correctness and trade-off report.' },
  { name: 'Week 81 — String/agent boss', description: 'Aho–Corasick tool/prompt detector or sequence-DP planner.' },
  { name: 'Week 93 — Inference boss', description: 'Priority scheduling, interval allocation, and binary search on capacity backed by a benchmark.' },
  { name: 'Week 102 — Platform tree boss', description: 'Euler Tour plus DSU-on-Tree subtree analytics, used as preparation for Capstone 2.' },
  { name: 'Weeks 103–108 — Capstone 1', description: 'Mo’s algorithm over immutable LLM traces — the required algorithmic capstone.' },
  { name: 'Week 108 optional — Capstone 2', description: 'Euler Tour + DSU on Tree over agent execution trees. Extra depth credit, not required for the LLM Platform badge.' },
];

export const FORGE_COVERAGE: { area: string; treatment: string; lands: string }[] = [
  { area: 'Complexity, arrays, prefix sums, binary search, greedy', treatment: 'Core', lands: 'Weeks 1–6 and recurring' },
  { area: 'Matrix operations, Gaussian elimination, exponentiation, recurrences', treatment: 'Core', lands: 'Weeks 7–18' },
  { area: 'Probability, expectation DP, combinatorics, modular arithmetic, gcd/sieve', treatment: 'Core', lands: 'Weeks 23–30 and Weeks 58–69' },
  { area: 'Heaps, hashing, tries, Fenwick trees, segment trees, DSU', treatment: 'Core', lands: 'Weeks 31–45' },
  { area: 'BFS/DFS, SCCs, topological sort, shortest paths', treatment: 'Core', lands: 'Weeks 46–52' },
  { area: 'MST, Euler paths, flows, matching', treatment: 'Core concepts; selected Boss fights', lands: 'Weeks 53–57' },
  { area: 'Dynamic programming and state-space reduction', treatment: 'Core', lands: 'Weeks 58–69' },
  { area: 'KMP, Aho–Corasick, retrieval-oriented string matching', treatment: 'Core', lands: 'Weeks 70–81' },
  { area: 'Suffix arrays, suffix trees, suffix automata', treatment: 'Supporting / Archive', lands: 'Weeks 70–81; project-driven promotion' },
  { area: 'Scheduling, interval structures, randomized algorithms, capacity search', treatment: 'Core / Supporting', lands: 'Weeks 82–102' },
  { area: 'Euler Tour, DSU on Tree, Mo’s algorithm', treatment: 'Boss fights', lands: 'Weeks 103–108' },
  { area: 'Computational geometry', treatment: 'Supporting basics; Archive advanced', lands: 'Weeks 1–30 and project-driven' },
  { area: 'HLD, dynamic trees, Link-Cut Trees, exotic contest structures', treatment: 'Archive / Boss fight', lands: 'Capstone extensions only' },
];
