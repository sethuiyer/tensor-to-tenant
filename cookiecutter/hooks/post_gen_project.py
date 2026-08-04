"""Post-generation hook: generate all 108 weekly journal entries, phase
READMEs, engineering-primitive stubs, and personalize the dashboard.

Runs after Cookiecutter has rendered every template into the new repo.

NB: This file is rendered by Jinja2 (Cookiecutter renders hook scripts as
templates). To avoid brace collisions inside triple-quoted strings, we use
plain triple-quoted strings with .format() placeholders and substitute via
str.format_map.
"""

from __future__ import annotations

import datetime as dt
import os
import re
import sys
import textwrap
from pathlib import Path


PHASE_1 = [
    (1,  "Orientation and course OS",               "Course setup, tracker, repo, weekly template",                  "Course dashboard + README"),
    (2,  "Python engineering refresh",              "Typing, testing, async basics",                                "CLI project skeleton with tests"),
    (3,  "Numerical Python",                       "NumPy, vectorization, broadcasting",                           "Vector math utility library"),
    (4,  "Reproducibility",                        "Git, notebooks, experiment tracking",                          "Reproducible notebook + Makefile"),
    (5,  "Math diagnostic and induction",          "Linear algebra, probability, hypothesis choice, generalization", "Diagnostic report + gap map + paper lab"),
    (6,  "Systems diagnostic",                     "HTTP, Docker, APIs, Linux basics",                             "Containerized hello-service"),
]

PHASE_2 = [
    (7,  "Linear algebra I",                       "Vector spaces, span, basis, dimension",                        "Problem set + concept map"),
    (8,  "Linear algebra II",                      "Linear independence, rank, nullity",                           "Solver exercises + notes"),
    (9,  "Linear algebra III",                     "Inner products, norms, dual norms",                            "Norm/distance library"),
    (10, "Linear algebra IV",                      "Orthogonality, projections, Gram-Schmidt",                     "Projection demo"),
    (11, "Linear algebra V",                       "Linear transformations, change of basis",                     "Coordinate transform lab"),
    (12, "Linear algebra VI",                      "Eigenvalues, eigenvectors, diagonalization",                   "PCA-style mini lab"),
    (13, "Linear algebra VII",                     "PSD matrices, quadratic forms, Rayleigh quotient",             "Proof + visualization"),
    (14, "Linear algebra VIII",                    "SVD, pseudoinverse, low-rank approximation",                   "Low-rank compression demo"),
    (15, "Numerical linear algebra I",             "Matrix norms, condition numbers, perturbation",                 "Perturbation experiment"),
    (16, "Numerical linear algebra II",            "LU, QR, Cholesky decomposition",                               "Decomposition library"),
    (17, "Numerical linear algebra III",           "Iterative solvers, power iteration, Krylov methods",            "Solver benchmark"),
    (18, "Numerical linear algebra IV",            "Randomized SVD, tensor notation",                              "Randomized approximation lab"),
]

PHASE_3 = [
    (19, "Calculus I",                             "Partial derivatives, gradients, directional derivatives",       "Gradient visualizer"),
    (20, "Calculus II",                            "Jacobians, Hessians, Taylor approximations",                    "Curvature lab"),
    (21, "Calculus III",                           "Chain rule on computational graphs",                           "Manual backprop worksheet"),
    (22, "Automatic differentiation",              "Forward/reverse mode, JVPs, VJPs",                             "Tiny autodiff prototype"),
    (23, "Probability I",                          "Probability spaces, conditioning, Bayes theorem",              "Probability problem set"),
    (24, "Probability II",                         "Random variables, distributions, transformations",             "Simulation notebook"),
    (25, "Probability III",                        "Random vectors, covariance, correlation",                      "Covariance/correlation lab"),
    (26, "Probability IV",                         "LLN, CLT, delta method",                                        "Monte Carlo convergence demo"),
    (27, "Statistics I",                           "MLE, MAP, estimator bias/variance",                           "Estimator comparison"),
    (28, "Statistics II",                          "Hypothesis testing, p-values, Type I/II errors",               "Test implementation"),
    (29, "Statistics III",                         "Confidence intervals, bootstrap, permutation tests",           "Bootstrap CI package"),
    (30, "Statistics IV",                          "Power, MDE, sample size, multiple testing",                   "Experiment-size calculator"),
]

PHASE_4 = [
    (31, "Retrieval math",                         "Cosine similarity, exact KNN",                                 "Vector search mini-lab"),
    (32, "Top-K systems",                          "Memory-bounded KNN, streaming Top-K",                          "Heap-based Top-K service"),
    (33, "Ranking pipelines",                      "Dynamic Top-K, two-stage retrieval/reranking",                 "Reranking prototype"),
    (34, "Rate limiting I",                        "Sliding-window and token bucket rate limiters",                "API limiter module"),
    (35, "Caching",                                "LRU cache and TTL cache",                                      "Cache simulator with tests"),
    (36, "Text chunking",                          "Token-aware and recursive sentence chunking",                  "Chunking library"),
    (37, "PII handling",                           "PII span merging, regex/NER detection",                        "Redaction utility"),
    (38, "Calibration",                            "Expected Calibration Error, Brier score",                      "Reliability dashboard"),
    (39, "Ranking metrics",                        "NDCG, MRR, Recall@K",                                          "Retrieval evaluator"),
    (40, "Batching",                               "Thread-safe inference batcher",                                "Concurrent batcher"),
    (41, "Resilience",                             "Retry, exponential backoff, jitter, circuit breaker",          "Fault-tolerance kit"),
    (42, "Sketches",                               "Count-Min Sketch, Bloom filter",                               "Probabilistic data structures"),
    (43, "Cardinality / routing",                  "HyperLogLog, consistent hashing",                              "Distributed routing lab"),
    (44, "Load balancing",                         "Weighted round robin, rendezvous hashing",                     "Load balancer module"),
    (45, "IDs / traffic",                          "Snowflake IDs, leaky bucket, sliding-window counter",          "Platform primitives lab"),
]

PHASE_5 = [
    (46, "System design framework",               "Requirements, constraints, API design",                         "Design doc template"),
    (47, "Data and APIs",                          "Data models, observability, contracts",                        "API design exercise"),
    (48, "Rate limiting design",                   "Token bucket, sliding windows at scale",                       "Rate limiter design writeup"),
    (49, "Scaling reads / writes",                 "Caching, replication, contention",                             "Scaling pattern notes"),
    (50, "Large blobs",                            "Storage, CDN, media pipelines",                                "Blob storage design"),
    (51, "Workflow systems",                       "Orchestration vs choreography",                                "Workflow state design"),
    (52, "Schema evolution",                       "Backward compatibility, contracts",                            "Schema migration plan"),
    (53, "Case studies I",                         "URL shortener, Dropbox",                                       "Two design docs"),
    (54, "Case studies II",                        "Ticketmaster, News Feed",                                      "Two design docs"),
    (55, "Case studies III",                       "WhatsApp, LeetCode",                                           "Two design docs"),
    (56, "Case studies IV",                        "Uber, web crawler",                                            "Two design docs"),
    (57, "Case studies V",                         "Ad click aggregator, payments",                                "Trade-off analysis"),
]

PHASE_6 = [
    (58, "ML problem framing",                     "Objectives, constraints, iterative development",               "ML project charter"),
    (59, "Data quality",                           "Labeling, weak supervision, augmentation",                     "Data quality checklist"),
    (60, "Leakage / contamination",                "Detection, eval tracking, versioning",                         "Leakage audit"),
    (61, "Offline evaluation",                     "Baselines, slices, confidence intervals",                      "Eval harness"),
    (62, "Online evaluation",                      "A/B tests, shadow deployment, canary, bandits",                "Rollout plan"),
    (63, "A/B calculator",                         "Lift, z-score, p-value, confidence intervals",                 "analyze_ab_test function"),
    (64, "Bootstrap methods",                      "Paired bootstrap for model comparisons",                       "bootstrap_ci package"),
    (65, "SRM detection",                          "Sample-ratio mismatch, chi-square diagnostics",                "SRM detector"),
    (66, "Feature flags",                          "Rules, rollouts, sticky assignment",                           "Flag engine"),
    (67, "Experiment assignment",                  "Deterministic assignment, namespaces",                         "Assignment service"),
    (68, "Monitoring",                             "Drift, observability, four-layer monitoring",                  "Monitoring dashboard spec"),
    (69, "Production failures",                    "Distribution shift, postmortems",                              "Incident postmortem template"),
]

PHASE_7 = [
    (70, "LLM anatomy",                            "Transformer, tokenizer, matmul",                               "Model anatomy notes"),
    (71, "LLM data pipelines",                     "Cleaning, deduplication, tokenization",                        "Dataset card"),
    (72, "Fine-tuning",                            "SFT, LoRA, QLoRA, DoRA",                                       "Fine-tuning plan"),
    (73, "Alignment",                              "RLHF, DPO, ORPO, GRPO",                                       "Preference eval plan"),
    (74, "Distributed training",                   "DDP/FSDP, tensor/pipeline parallelism, ZeRO",                  "Training architecture map"),
    (75, "Vector search",                          "HNSW, IVF-PQ, product quantization",                           "Index benchmark"),
    (76, "Retrieval patterns",                     "Hybrid search, query rewriting, chunking",                     "Retrieval lab"),
    (77, "Retrieval fusion",                       "BM25 + dense + reranker, RRF",                                 "Fusion service"),
    (78, "Retrieval eval",                         "Query slices, macro metrics, regressions",                     "Slice evaluation report"),
    (79, "Prompt systems",                         "Prompt template renderer, version registry",                   "Prompt management tool"),
    (80, "Memory / context",                       "Conversation memory, context optimizer",                       "Memory service"),
    (81, "Agent foundations",                      "ReAct, plan-execute, tool calling, guardrails",                 "Agent prototype"),
]

PHASE_8 = [
    (82, "GPU performance",                        "Compute/memory/overhead regimes, FlashAttention",              "Performance primer notes"),
    (83, "Inference arithmetic",                   "Roofline model, arithmetic intensity",                         "Model intensity worksheet"),
    (84, "PagedAttention / vLLM",                  "KV paging, block tables",                                      "vLLM deployment"),
    (85, "vLLM internals",                         "Scheduler, block manager, code paths",                         "Internal anatomy notes"),
    (86, "vLLM metrics",                           "Running/waiting requests, latency histograms",                 "Metrics schema"),
    (87, "Observability",                          "Prometheus/Grafana for serving",                               "Live inference dashboard"),
    (88, "Benchmarking",                           "Request-rate sweeps, saturation points",                       "Benchmark methodology doc"),
    (89, "SGLang",                                 "RadixAttention, prefix reuse",                                 "SGLang comparison report"),
    (90, "Scheduling",                             "Orca, continuous batching, chunked prefill",                   "Scheduler comparison"),
    (91, "Quantization",                           "FP8, AWQ, GPTQ, KV cache compression",                         "Quality/throughput table"),
    (92, "Speculative / long context",             "Medusa, EAGLE, StreamingLLM, KV eviction",                     "Latency/memory lab"),
    (93, "Disaggregation",                         "DistServe, Splitwise, Mooncake, autoscaling",                  "Disaggregated serving plan"),
]

PHASE_9 = [
    (94, "Traffic routing",                        "Model router, kill switch, sticky rollout",                    "Router service"),
    (95, "Safe observability",                     "PII redaction, end-to-end request tracing",                    "Trace + safe logs"),
    (96, "Fan-out / streaming",                    "Partial failures, token stream multiplexing",                  "Resilient aggregator"),
    (97, "Quotas / priority",                      "Token budgets, gateway prioritization",                        "Quota/priority service"),
    (98, "Workflow execution",                     "DAG scheduler, idempotency",                                   "Workflow engine"),
    (99, "Fairness / HA",                          "Per-tenant limits, leader election",                           "Tenant limiter + HA lab"),
    (100, "Async infrastructure",                  "Distributed work queue, config service",                       "Queue/config platform"),
    (101, "Model lifecycle",                        "Health monitor, registry/promotion",                           "Model ops pipeline"),
    (102, "Cost / safety / caching",               "Semantic/embedding cache, injection detection, cost attr.",    "Cost/safety platform"),
]

PHASE_10 = [
    (103, "Capstone planning",                     "Requirements, architecture, eval plan",                        "Capstone design doc"),
    (104, "Capstone build I",                      "Core API, retrieval/agent flow",                               "Working prototype"),
    (105, "Capstone build II",                     "Evaluation, observability, guardrails",                        "Monitored prototype"),
    (106, "Capstone build III",                    "Load testing, optimization, cost tuning",                      "Performance report"),
    (107, "Mock interview week",                   "System design, coding, behavioral simulations",                "Mock interview scorecard"),
    (108, "Final review",                          "Portfolio, retrospective, job plan",                           "Final portfolio + 30-day plan"),
]

PHASES = [
    ("00", "Orientation, Tooling, and Diagnostics",             1,   6,   PHASE_1),
    ("01", "Mathematical Foundations I",                         7,   18,  PHASE_2),
    ("02", "Mathematical Foundations II",                        19,  30,  PHASE_3),
    ("03", "Engineering Micro-Projects and Applied ML Primitives", 31, 45,  PHASE_4),
    ("04", "System Design and Distributed Systems Fundamentals", 46,  57,  PHASE_5),
    ("05", "ML Lifecycle, Experimentation, and MLOps",            58,  69,  PHASE_6),
    ("06", "LLM Training, RAG, Agents, and Evaluation",           70,  81,  PHASE_7),
    ("07", "LLM Inference and Performance Engineering",          82,  93,  PHASE_8),
    ("08", "Production AI Platform Engineering",                 94,  102, PHASE_9),
    ("09", "Capstone, Portfolio, and Interview Readiness",        103, 108, PHASE_10),
]

PROGRAMS = [
    ("foundations", "Foundations", 1, 30,
     "Math, numerical routines, and experimentation toolkit"),
    ("engineering_systems", "Engineering + Systems", 31, 69,
     "Tested primitives, system designs, MLOps tools, and postmortem"),
    ("llm_platform", "LLM Platform", 70, 108,
     "LLM/RAG work, inference benchmark, platform layer, and capstone"),
]

RECOVERY_AFTER = [6, 14, 22, 30, 38, 46, 54, 62, 70, 78, 86, 94, 102]

RELEASES = [
    (30, "Foundations", "Weeks 1-30", "Math, numerical routines, and experimentation toolkit", 30),
    (69, "Engineering + Systems", "Weeks 31-69", "Tested primitives, system designs, MLOps tools, and postmortem", 69),
    (108, "LLM Platform", "Weeks 70-108", "LLM/RAG work, inference benchmark, platform layer, and capstone", 108),
]

FORGE_LANES = [
    (1, 6, "Core", "Complexity, arrays, prefix sums, two pointers, binary search, bitmasks", "Implement one timed drill and write the complexity proof.", "45-60 min"),
    (7, 14, "Core", "Matrix operations, Gaussian elimination, exponentiation, recurrences", "Implement a matrix or recurrence solver from scratch.", "60-90 min"),
    (15, 22, "Supporting", "Numerical methods, binary search on answer, ternary search, Newton iteration", "Compare two root-finding or optimization methods on a small workload.", "45-120 min"),
    (23, 30, "Core", "Probability simulation, expectation DP, combinatorics, inclusion-exclusion, number theory basics", "Solve one expectation/counting problem and verify it by simulation or brute force.", "60-90 min"),
    (31, 37, "Core", "Heaps, hashing, tries, linked structures, intervals, basic pattern matching", "Connect one data structure to the retrieval, caching, or chunking primitive.", "45-90 min"),
    (38, 45, "Core", "Fenwick trees, segment trees, range queries, sketches, DSU, randomized hashing", "Implement one range or connectivity structure and test adversarial cases.", "60-90 min"),
    (46, 52, "Core", "Graph representation, BFS/DFS, SCC, topological sort, shortest paths", "Implement a dependency or routing graph algorithm and explain its failure modes.", "60-90 min"),
    (53, 57, "Core", "MST, Euler paths, max flow, min-cost flow, matching", "Formulate one platform allocation problem as a graph optimization problem.", "60-120 min"),
    (58, 69, "Core", "Dynamic programming, greedy methods, bitmask DP, probability DP, experiment assignment", "Solve one state-space problem and explain why the state is sufficient.", "60-90 min"),
    (70, 81, "Core", "KMP, Aho-Corasick, trie retrieval, sequence DP, suffix-array survey", "Implement a pattern detector or sequence algorithm tied to text/RAG work.", "60-90 min"),
    (82, 93, "Supporting", "Priority scheduling, interval allocation, capacity search, randomized load balancing", "Benchmark one scheduling or capacity policy under a synthetic workload.", "45-120 min"),
    (94, 102, "Supporting", "Euler indexing, subtree aggregation, DSU on Tree, HLD survey", "Flatten a tenant or workflow tree and answer one subtree query.", "60-120 min"),
    (103, 108, "Boss fight", "Mo's algorithm, capstone integration, and tree forensics", "Integrate the selected algorithm into Capstone 1 or the optional Capstone 2.", "2-3 hr"),
]

FORGE_BOSSES = {
    18: ("Boss fight", "Numerical matrix boss", "Gaussian elimination, matrix exponentiation, or randomized SVD with stability notes.", "2-3 hr"),
    30: ("Boss fight", "Foundations mini-contest", "Expectation DP, combinatorics, modular arithmetic, and optimization search.", "2-3 hr"),
    45: ("Boss fight", "Data-structure mini-contest", "Fenwick/segment tree, DSU, hashing, and a range-query workload.", "2-3 hr"),
    57: ("Boss fight", "Graph/flow boss", "Euler indexing plus a flow or matching formulation for resource allocation.", "2-3 hr"),
    69: ("Boss fight", "MLOps algorithm boss", "Experiment assignment, greedy rollout, or bandit allocation with trade-offs.", "2-3 hr"),
    81: ("Boss fight", "String/agent boss", "Aho-Corasick tool or prompt detector, or a sequence-DP planner.", "2-3 hr"),
    93: ("Boss fight", "Inference scheduling boss", "Priority scheduling, interval allocation, and binary search on capacity.", "2-3 hr"),
    102: ("Boss fight", "Platform tree boss", "Euler Tour plus DSU on Tree subtree analytics.", "2-3 hr"),
    108: ("Boss fight", "Capstone 2 optional boss", "Euler Tour + DSU on Tree over agent execution trees.", "2-3 hr"),
}

ENGINEERING_PRIMITIVES = [
    ("retrieval",      "Cosine similarity, KNN, Top-K, reranking, chunking fusion"),
    ("rate_limiting",  "Token bucket, sliding window, leaky bucket"),
    ("caching",        "LRU, TTL, semantic, embedding cache"),
    ("chunking",       "Token-aware, recursive, sentence-aware"),
    ("pii",            "PII span merging, regex/NER redaction"),
    ("metrics",        "Recall@K, MRR, NDCG, ECE, Brier"),
    ("batching",       "Thread-safe inference batcher"),
    ("resilience",     "Retry/backoff, circuit breaker"),
    ("sketches",       "Count-Min, Bloom, HyperLogLog"),
    ("routing",        "Consistent hashing, load balancing"),
    ("ids",            "Snowflake IDs, traffic shaping"),
]

INTERVIEW_DRILLS = [
    ("system_design", "URL shortener, rate limiter, Dropbox, WhatsApp, Uber, payments, ..."),
    ("coding",        "Two pointers, sliding window, DP, graphs, Mo's algorithm, ..."),
    ("behavioral",    "Scope, ownership, ambiguity, perseverance, growth, leadership, ..."),
    ("mocks",         "Mock interview scorecards and retro notes"),
]

SYSTEM_DESIGN_WEEKS = [
    (46, "Delivery framework, networking, numbers", "Bitly / URL shortener", "Framed design + capacity sheet"),
    (47, "API design, data modeling, indexes, contracts", "LeetCode problem service", "API and schema package"),
    (48, "Caching, sharding, consistent hashing, CAP", "Rate limiter + distributed cache", "Design, key layout, failure table"),
    (49, "Replication, read/write scaling, contention", "News Feed / Instagram", "Read path, write path, consistency choice"),
    (50, "Large blobs, CDN, metadata, resumable work", "Dropbox / Google Docs", "Storage design + recovery plan"),
    (51, "Queues, workflows, long-running tasks", "Job Scheduler / Slack job queue", "State machine + retry/idempotency plan"),
    (52, "Schema evolution, real-time updates, coordination", "WhatsApp / notification system", "Contract migration + delivery semantics"),
    (53, "Search, proximity, crawling, ranking", "Yelp / FB Post Search / web crawler", "Index and freshness design"),
    (54, "Messaging and social fan-out", "FB Live Comments / Tinder / Discord", "Fan-out model + hot-key strategy"),
    (55, "Scheduling, scarcity, marketplace correctness", "Ticketmaster / Uber / local delivery / auction", "Reservation invariant + contention test"),
    (56, "Streaming, analytics, data infrastructure", "Ad clicks / metrics / Robinhood / Spotify", "Stream topology + watermark/replay notes"),
    (57, "Integrated architecture and interview boss", "ChatGPT / payments / Figma multiplayer", "Staff-level design review + trade-off defense"),
]

DARBAR_TOTAL = 548
DARBAR_DIFFICULTIES = "255 Easy, 240 Medium, 53 Hard"
DARBAR_CATEGORIES = (
    "array", "backtracking", "bit manipulation", "divide and conquer",
    "dynamic programming", "graphs", "greedy", "hash table", "heap",
    "linked list", "math", "queue", "range query", "recursion",
    "searching and sorting", "stack", "string", "trees", "trie",
)


def repo_root() -> Path:
    """Cookiecutter sets PROJECT_DIR to the rendered project root."""
    return Path(os.environ.get("PROJECT_DIR", ".")).resolve()


def monday_of(week_idx: int, start: dt.date) -> dt.date:
    return start + dt.timedelta(days=7 * (week_idx - 1))


def fmt_date(d: dt.date) -> str:
    return d.strftime("%Y-%m-%d")


def fmt_range(a: dt.date, b: dt.date) -> str:
    return "{0} to {1}".format(fmt_date(a), fmt_date(b))


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def generate_journal_templates(root: Path) -> None:
    write(
        root / "journal" / "TEMPLATE.md",
        textwrap.dedent("""\
            # Week {N}: {TITLE}

            **Phase:** {PHASE} (Weeks {P_START}-{P_END})
            **Dates:** {DATE_RANGE}
            **Focus:** {FOCUS}

            ## Core objective
            -

            ## Optional depth
            - Add a proof, benchmark, failure analysis, or production extension if capacity allows.

            ## Monday -- Theory
            -

            ## Tuesday -- Build
            -

            ## Wednesday -- Systems / Papers
            -

            ## Thursday -- Eval / Interview
            -

            ## Friday -- Algorithmic Forge
            **Tier:** Core / Supporting / Archive / Boss
            **Theme:**
            **Timebox:**
            **Drill:**

            ## Algorithmic Forge status
            - [ ] Forge artifact recorded (required for Core/Boss; optional otherwise)

            ## Optional Leetcode Darbar lane
            - Problem IDs / titles:
            - Status, attempts, final complexity:
            - Production concept reinforced:

            ## Friday -- Review / Sailboat Retro

            ### Island / destination
            - What capability am I trying to reach?

            ### Wind
            - What helped progress?

            ### Anchor
            - What slowed me down?

            ### Rocks
            - What could derail next week?

            ### Boat position
            - [ ] Ahead
            - [ ] On track
            - [ ] Drifting

            ### Next heading
            - What is the single most important adjustment for next week?

            ## Core deliverable
            - {DELIVERABLE}

            ## Evidence record
            - Code / implementation:
            - Benchmark / result:
            - Design doc / technical explanation:
            - Retrospective / learning note:

            ## Core status
            - [ ] Theory
            - [ ] Build
            - [ ] Systems / papers
            - [ ] Evaluation / interview
            - [ ] Review / retro
            - [ ] Core deliverable shipped

            ## Optional depth status
            - [ ] Depth work attempted (optional)
            """),
    )

    write(
        root / "journal" / "RETRO_TEMPLATE.md",
        textwrap.dedent("""\
            # Weekly Retro -- Week {N}

            ## What went well
            -

            ## What blocked me
            -

            ## Knowledge delta (one sentence)
            -

            ## Did I hit the deliverable?
            - [ ] Yes
            - [ ] Partial
            - [ ] No -- why?

            ## Adjustment for next week
            -

            ## Mood / energy (1-5)
            -
            """),
    )

    write(
        root / "docs" / "sailboat_retro.md",
        textwrap.dedent("""\
            # Sailboat Retrospective

            Use this at the end of every instructional week. It is part of the
            existing review/evidence ritual, not an additional assignment or gate.

            | Element | Question |
            |---|---|
            | Island / destination | What capability am I trying to reach? |
            | Wind | What helped progress? |
            | Anchor | What slowed me down? |
            | Rocks | What could derail next week? |
            | Boat position | Ahead, on track, or drifting? |
            | Next heading | What is the single most important adjustment? |

            Keep the answers short and concrete. The purpose is to navigate the
            apprenticeship, protect the core deliverable, and make recovery a
            normal part of progress.

            The full reference template is in the parent course's
            `SAILBOAT_RETRO.md`.
            """),
    )


def optional_depth_for(week_no: int) -> str:
    """Return a phase-appropriate extension without adding a second gate."""
    if week_no in (30, 69, 108):
        return "Package the strongest work from this program as a portfolio release with a benchmark, explanation, and retrospective."
    if week_no <= 30:
        return "Prove one important claim, implement one component from scratch, and verify it numerically."
    if week_no <= 69:
        return "Add a benchmark, failure-mode analysis, and a short production trade-off note."
    return "Add a production-shaped benchmark, cost or safety analysis, and an architecture trade-off note."


def paper_for_week(week_no: int) -> str:
    """Return the bounded paper-study brief for weeks with a named anchor paper."""
    if week_no != 5:
        return ""
    return textwrap.dedent("""\
        ## Anchor paper — hypothesis choice and generalization

        Read Michael Timothy Bennett, *The Optimal Choice of Hypothesis Is the
        Weakest, Not the Shortest* (arXiv:2301.12987v4):
        https://arxiv.org/abs/2301.12987v4

        This is a critical reading, not a theorem to accept without checking.
        The paper's central comparison is conditional on a finite implementable
        language and a uniform distribution over tasks.

        - [ ] Define task, model, extension, weakness, and description length.
        - [ ] Reproduce or critique the binary-arithmetic toy experiment.
        - [ ] Report generalization rate, extent, and the assumptions behind them.
        - [ ] Connect the result to inductive bias, leakage, calibration, and
          distribution shift.
        """)


def forge_for_week(week_no: int) -> tuple[str, str, str, str]:
    if week_no in FORGE_BOSSES:
        return FORGE_BOSSES[week_no]
    for start, end, tier, topic, drill, timebox in FORGE_LANES:
        if start <= week_no <= end:
            return tier, topic, drill, timebox
    raise ValueError("No Algorithmic Forge lane for week {0}".format(week_no))


def generate_weeks(root: Path, start: dt.date) -> None:
    """Generate all 108 weekly journal entries."""
    weeks_dir = root / "journal" / "weeks"
    weeks_dir.mkdir(parents=True, exist_ok=True)

    for phase_num, phase_name, p_start, p_end, weeks in PHASES:
        for week_no, title, focus, deliverable in weeks:
            monday = monday_of(week_no, start)
            sunday = monday + dt.timedelta(days=6)
            forge_tier, forge_topic, forge_drill, forge_timebox = forge_for_week(week_no)

            body = (
                "# Week {n}: {title}\n"
                "\n"
                "**Phase {pn} -- {pname}** (Weeks {ps} to {pe})\n"
                "**Dates:** {dates}\n"
                "**Focus:** {focus}\n"
                "**Core deliverable:** {deliv}\n"
                "\n"
                "## Core objective\n"
                "-\n"
                "\n"
                "{paper}\n"
                "## Optional depth\n"
                "- {depth}\n"
                "\n"
                "## Monday -- Theory\n"
                "-\n"
                "\n"
                "## Tuesday -- Build\n"
                "-\n"
                "\n"
                "## Wednesday -- Systems / Papers\n"
                "-\n"
                "\n"
                "## Thursday -- Eval / Interview\n"
                "-\n"
                "\n"
                "## Friday -- Algorithmic Forge\n"
                "**Tier:** {forge_tier}\n"
                "**Theme:** {forge_topic}\n"
                "**Timebox:** {forge_timebox}\n"
                "**Drill:** {forge_drill}\n"
                "\n"
                "## Algorithmic Forge status\n"
                "- [ ] Forge artifact recorded (required for Core/Boss; optional otherwise)\n"
                "\n"
                "## Optional Leetcode Darbar lane\n"
                "- Problem IDs / titles:\n"
                "- Status, attempts, final complexity:\n"
                "- Production concept reinforced:\n"
                "\n"
                "## Friday -- Review / Sailboat Retro\n"
                "\n"
                "### Island / destination\n"
                "- What capability am I trying to reach?\n"
                "\n"
                "### Wind\n"
                "- What helped progress?\n"
                "\n"
                "### Anchor\n"
                "- What slowed me down?\n"
                "\n"
                "### Rocks\n"
                "- What could derail next week?\n"
                "\n"
                "### Boat position\n"
                "- [ ] Ahead\n"
                "- [ ] On track\n"
                "- [ ] Drifting\n"
                "\n"
                "### Next heading\n"
                "- What is the single most important adjustment for next week?\n"
                "\n"
                "## Core deliverable\n"
                "- {deliv}\n"
                "\n"
                "## Evidence record\n"
                "- Code / implementation:\n"
                "- Benchmark / result:\n"
                "- Design doc / technical explanation:\n"
                "- Retrospective / learning note:\n"
                "\n"
                "## Core status\n"
                "- [ ] Theory\n"
                "- [ ] Build\n"
                "- [ ] Systems / papers\n"
                "- [ ] Evaluation / interview\n"
                "- [ ] Review / retro\n"
                "- [ ] Core deliverable shipped\n"
                "\n"
                "## Optional depth status\n"
                "- [ ] Depth work attempted (optional)\n"
                "\n"
                "## Time log\n"
                "\n"
                "- Mon (theory):    ___ hr\n"
                "- Tue (build):     ___ hr\n"
                "- Wed (systems):   ___ hr\n"
                "- Thu (eval):      ___ hr\n"
                "- Fri (forge/ret): ___ hr\n"
                "- Weekend:         ___ hr\n"
                "\n"
                "**Total this week:** ___ hr\n"
                "**Mode executed:**  ___ (implement / read_diagram / deploy_benchmark)\n"
                "**Planned mode:**   ___ (from curriculum table Mode column)\n"
                "**Drift notes:**\n"
                "-\n"
                "\n"
                "---\n"
                "\n"
                "*Auto-generated by cookiecutter-tensor-to-tenant.*\n"
            ).format(
                n=week_no,
                title=title,
                pn=phase_num,
                pname=phase_name,
                ps=p_start,
                pe=p_end,
                dates=fmt_range(monday, sunday),
                focus=focus,
                deliv=deliverable,
                depth=optional_depth_for(week_no),
                paper=paper_for_week(week_no),
                forge_tier=forge_tier,
                forge_topic=forge_topic,
                forge_timebox=forge_timebox,
                forge_drill=forge_drill,
            )
            write(weeks_dir / "week_{0:03d}.md".format(week_no), body)


def generate_evidence_scaffolds(root: Path) -> None:
    evidence_root = root / "evidence" / "weeks"
    for week_no in range(1, 109):
        write(
            evidence_root / "week_{0:03d}".format(week_no) / "README.md",
            textwrap.dedent("""\
                # Evidence — Week {week}

                Link the four evidence types required for the core deliverable:

                - Code / implementation:
                - Benchmark / result:
                - Design doc / technical explanation:
                - Retrospective / learning note:
                """).format(week=week_no),
        )


def generate_recovery_scaffolds(root: Path) -> None:
    write(
        root / "docs" / "recovery_weeks.md",
        textwrap.dedent("""\
            # Recovery Windows

            Recovery windows are deliberate buffer periods after selected
            instructional weeks. They are not additional topics and should not
            become another source of guilt. Use one to catch up, remediate a
            blocked gate, rerun evidence, or rest.

            Suggested windows: after Weeks 6, 14, 22, 30, 38, 46, 54, 62, 70,
            78, 86, 94, and 102.

            Use `make recovery=14` to prepare or refresh a recovery plan.
            """),
    )
    recovery_root = root / "journal" / "recovery"
    for after_week in RECOVERY_AFTER:
        write(
            recovery_root / "after_week_{0:03d}.md".format(after_week),
            textwrap.dedent("""\
                # Recovery window after Week {week}

                This is a deliberate buffer window, not an additional curriculum topic.
                Use it for catch-up, remediation, benchmark reruns, or rest.

                ## Recovery decision

                - [ ] Review incomplete core work from the last 6-8 weeks
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
                """).format(week=after_week),
        )


def generate_program_docs(root: Path) -> None:
    rows = "\n".join(
        "| **{name}** | {start}-{end} | Week {end} | {release} | Gate {end} + core evidence |".format(
            name=name, start=start, end=end, release=release
        )
        for _, name, start, end, release in PROGRAMS
    )
    write(
        root / "docs" / "programs.md",
        textwrap.dedent("""\
            # Stackable Programs

            This repo is a 108-instructional-week apprenticeship with valuable
            stopping points. Complete the core lane and publish the release at any
            checkpoint; optional depth work keeps the advanced ceiling high.

            | Program | Weeks | Release checkpoint | Evidence focus | Badge eligibility |
            |---|---:|---:|---|---|
            {rows}

            ```mermaid
            flowchart LR
                F["FOUNDATIONS<br/>Weeks 1–30"] --> E["ENGINEERING + SYSTEMS<br/>Weeks 31–69"] --> L["LLM PLATFORM<br/>Weeks 70–108"]
            ```

            A release should include implementation, benchmark/result, technical
            explanation, and retrospective evidence. The next program remains
            blocked only when the relevant milestone gate is blocked.
            """).format(rows=rows),
    )


def generate_algorithmic_forge_scaffold(root: Path) -> None:
    base = root / "09_interview" / "algorithmic_forge"
    for tier in ("core", "supporting", "archive", "boss_fights"):
        write(
            base / tier / "README.md",
            textwrap.dedent("""\
                # Algorithmic Forge — {tier}

                Land Forge artifacts in this lane. Every artifact should include
                the workload shape, implementation/tests, complexity, one failure
                mode, and an interview-ready explanation.
                """).format(tier=tier.replace("_", " ").title()),
        )

    lane_rows = "\n".join(
        "| {start}-{end} | **{tier}** | {topic} | {timebox} |".format(
            start=start, end=end, tier=tier, topic=topic, timebox=timebox
        )
        for start, end, tier, topic, _, timebox in FORGE_LANES
    )
    boss_rows = "\n".join(
        "| {week} | {name} | {drill} | {timebox} |".format(
            week=week, name=name, drill=drill, timebox=timebox
        )
        for week, (_, name, drill, timebox) in FORGE_BOSSES.items()
    )
    write(
        root / "docs" / "algorithmic_forge.md",
        textwrap.dedent("""\
            # Algorithmic Forge

            The Forge is a parallel Friday spine through the 108-week
            apprenticeship. It keeps the programming-camp material connected to
            the AI-systems work without creating a second full-time curriculum.

            ## Treatment levels

            | Level | Treatment | Timebox |
            |---|---|---:|
            | **Core** | Implement and explain; directly supports the phase | 45-90 min |
            | **Supporting** | Guided lab or representative problem | 45-120 min |
            | **Archive** | Reference-only; no scheduled obligation | 0 min |
            | **Boss fight** | Selected gate or capstone extension | 2-3 hr |

            ## Weekly map

            | Weeks | Tier | Theme | Timebox |
            |---:|---|---|---:|
            {lane_rows}

            ## Boss fights

            | Week | Boss | Drill | Timebox |
            |---:|---|---|---:|
            {boss_rows}

            Capstone 1 (Mo's algorithm over immutable traces) is required. The
            Euler Tour + DSU on Tree Capstone 2 is the optional Week 108 boss and
            is not required for the LLM Platform badge.

            Put artifacts under `09_interview/algorithmic_forge/{{core,supporting,archive,boss_fights}}`.
            Run `make forge=57` to prepare a week-specific artifact scaffold.
            """).format(lane_rows=lane_rows, boss_rows=boss_rows),
    )


def generate_system_design_scaffold(root: Path) -> None:
    """Generate the canonical Weeks 46-57 design and OOD track."""
    design_root = root / "09_interview" / "system_design"
    for lane in ("foundations", "patterns", "technology_labs", "case_studies", "ood", "weeks"):
        (design_root / lane).mkdir(parents=True, exist_ok=True)

    rows = "\n".join(
        "| {week} | {theme} | {case} | {evidence} |".format(
            week=week, theme=theme, case=case, evidence=evidence
        )
        for week, theme, case, evidence in SYSTEM_DESIGN_WEEKS
    )
    write(
        root / "docs" / "system_design_track.md",
        textwrap.dedent("""\
            # Canonical System Design Track

            System design is the canonical architecture track for **Weeks 46-57**,
            not an extra phase. Every artifact follows:

            ```text
            requirements -> API/data model -> scale/partition/cache/queue
                         -> failure/consistency/observability -> AI extension
            ```

            ## Weekly map

            | Week | Theme | Core case/lab | Evidence |
            |---:|---|---|---|
            {rows}

            ## Scope

            Foundations cover delivery framework, networking, APIs, data modeling,
            numbers to know, and common patterns. Distributed-systems patterns cover
            caching, sharding, consistent hashing, CAP, indexing, read/write scale,
            contention, real-time updates, workflows, large blobs, and schema
            evolution.

            Core technology labs are Redis, PostgreSQL, Kafka, Flink, an API gateway,
            and a vector database. Supporting labs are Elasticsearch, Cassandra,
            DynamoDB, ZooKeeper, time-series databases, and big-data structures.

            Case-study families include storage/collaboration, messaging, search,
            scheduling, streaming, marketplace/money, social, and platform
            primitives. Compare cases by workload shape instead of memorizing a
            company-specific architecture.

            OOD/LLD runs as a parallel Thursday lane: Connect Four, Locker, Elevator,
            Parking Lot, File System, Movie Booking, Logging Service, Rate Limiter,
            and Inventory Management. Record invariants, ownership, concurrency, and
            extension points.

            Every design needs one AI extension: semantic search, agent memory,
            inference routing, tool-call scheduling, evaluation, safety, watermarking,
            tenant isolation, or cost attribution.

            Run `make design=54` to scaffold one week's artifact.
            """).format(rows=rows),
    )

    write(
        design_root / "README.md",
        textwrap.dedent("""\
            # System Design and OOD

            This is the canonical Weeks 46-57 design track. Put one design artifact
            in `weeks/` each week, use `case_studies/` for comparative notes, and
            keep OOD/LLD implementations in `ood/`.

            A design is complete only when it includes requirements, API, data model,
            capacity, consistency/failure semantics, observability, cost/privacy,
            and an AI extension. Use `make design=54` for a prepared scaffold.
            """),
    )
    for lane, description in (
        ("foundations", "Requirements, networking, APIs, data modeling, and capacity math."),
        ("patterns", "Caching, sharding, consistency, contention, workflows, and schema evolution."),
        ("technology_labs", "Technology guarantees and operational trade-offs."),
        ("case_studies", "Case-study comparisons organized by workload pattern."),
        ("ood", "Object invariants, coordination, scarcity, and concurrency."),
    ):
        write(design_root / lane / "README.md", "# {0}\n\n{1}\n".format(lane.replace("_", " ").title(), description))


def generate_leetcode_darbar_scaffold(root: Path) -> None:
    """Generate a source-linked 548-slot Darbar tracker without inventing titles."""
    darbar_root = root / "09_interview" / "leetcode_darbar"
    darbar_root.mkdir(parents=True, exist_ok=True)
    header = "Index,Title,Category,Difficulty,Status,Attempts,Complexity,Production concept,Notes"
    rows = [header]
    for index in range(1, DARBAR_TOTAL + 1):
        rows.append("{0:03d},,,,,,,,".format(index))
    write(darbar_root / "TRACKER.csv", "\n".join(rows) + "\n")
    categories = ", ".join(DARBAR_CATEGORIES)
    write(
        root / "docs" / "leetcode_darbar.md",
        textwrap.dedent("""\
            # Leetcode Darbar

            Source: https://aninokuma.codeberg.page/leetcode-darbar/

            The optional Auror track targets **548 problems** ({difficulty}). The
            tracker lives at `09_interview/leetcode_darbar/TRACKER.csv`, one row per
            source-catalog slot. Fill in source title, category, difficulty, and
            URL as you work; the generator intentionally does not guess metadata.

            Categories represented by the source track include: {categories}.

            Standard learners use selected phase-aligned problems. Auror learners
            target all 548 at roughly five per week. Each solved row should include
            attempts, final complexity, one mistake, and the production concept it
            reinforces. Use `make darbar=42` for a problem evidence scaffold and
            `make auror` to check the optional badge.
            """).format(difficulty=DARBAR_DIFFICULTIES, categories=categories),
    )
    write(
        darbar_root / "README.md",
        textwrap.dedent("""\
            # Leetcode Darbar

            Parallel interview-execution track: **548 source-catalog slots**.

            - Standard: selected aligned problems; no full-catalog requirement.
            - Auror: all 548 solved and explained; use `make auror` to verify.
            - `TRACKER.csv`: source metadata, status, attempts, complexity, and
              production connection.
            - `problem_###.md`: generated evidence files from `make darbar=42`.

            Keep this lane separate from core progress. It is an optional volume
            challenge, not a substitute for production implementations or gates.
            """),
    )


def generate_portfolio_releases(root: Path) -> None:
    release_root = root / "portfolio" / "releases"
    write(
        root / "portfolio" / "README.md",
        textwrap.dedent("""\
            # Portfolio Releases

            Publish these as three independent checkpoints. A learner can stop
            after any release and still have a coherent body of work.

            - `releases/foundations_week_030.md`
            - `releases/engineering_systems_week_069.md`
            - `releases/llm_platform_week_108.md`

            Each release should link code, a measurable result, a technical
            explanation, and a retrospective. Run `make badge=30`, `make
            badge=69`, or `make badge=108` to verify a release's core evidence
            and update its badge status.
            """),
    )

    for week, name, coverage, focus, gate in RELEASES:
        slug = name.lower().replace(" + ", "_").replace(" ", "_")
        write(
            release_root / "{0}_week_{1:03d}.md".format(slug, week),
            textwrap.dedent("""\
                # {name} release — Week {week}

                **Coverage:** {coverage}
                **Release focus:** {focus}

                This release is a public checkpoint. It should stand on its own
                even if the learner pauses before the next program.

                ## Program badge

                **Badge:** Tensor-to-Tenant {name}
                **Status:** NOT EARNED — run `make badge={week}` to verify the evidence.
                **Eligibility:** core evidence for this program plus Gate {gate} passing.

                ## Release checklist

                - [ ] Select the strongest core artifacts from this program
                - [ ] Link implementation/code
                - [ ] Link benchmark or measurable result
                - [ ] Link design document or technical explanation
                - [ ] Link retrospective and lessons learned
                - [ ] Add a short README explaining what works, what does not, and what comes next
                - [ ] Run Gate {gate} and record the result
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
                """).format(name=name, week=week, coverage=coverage, focus=focus, gate=gate),
        )


def generate_remediation_docs(root: Path) -> None:
    descriptions = {
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
    write(
        root / "docs" / "remediation" / "README.md",
        textwrap.dedent("""\
            # Remediation

            A failed gate blocks the next gate, but it does not erase prior work.
            Use `make remediate=18` to prepare a focused seven-day repair cycle,
            submit the missing evidence, then rerun `make gate`.

            Remediation is criterion-specific. Do not restart the whole course
            unless the evidence shows the underlying foundation is genuinely absent.
            """),
    )
    for gate, description in descriptions.items():
        write(
            root / "docs" / "remediation" / "gate_{0:03d}.md".format(gate),
            textwrap.dedent("""\
                # Remediation plan — Gate {gate}

                **Blocked capability:** {description}

                This is a targeted repair cycle. Do not begin new gate-dependent
                content until the missing evidence is complete and the gate checker passes.

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
                """).format(gate=gate, description=description),
        )


def generate_phase_readmes(root: Path) -> None:
    phase_dirs = {
        "00_orientation":              ("Phase 0 -- Orientation, Tooling, and Diagnostics",          1, 6),
        "01_math":                     ("Phase 1 -- Mathematical Foundations (Linear Algebra + Calculus + Probability + Statistics)", 7, 30),
        "02_engineering_primitives":   ("Phase 3 -- Engineering Micro-Projects & Applied ML Primitives", 31, 45),
        "03_system_design":            ("Phase 4 -- System Design & Distributed Systems Fundamentals", 46, 57),
        "04_ml_systems":               ("Phase 5 -- ML Lifecycle, Experimentation, MLOps",          58, 69),
        "05_llm":                      ("Phase 6 -- LLM Training, RAG, Agents, Evaluation",          70, 81),
        "06_inference":                ("Phase 7 -- LLM Inference & Performance Engineering",         82, 93),
        "07_platform":                 ("Phase 8 -- Production AI Platform Engineering",             94, 102),
        "08_capstone":                 ("Phase 9 -- Capstone, Portfolio, Interview Readiness",       103, 108),
        "09_interview":                ("Continuous -- Interview Preparation (all phases)",          None, None),
    }

    for folder, (title, ws, we) in phase_dirs.items():
        path = root / folder / "README.md"
        if we is None:
            week_block = "Continuous across all 108 weeks."
        else:
            week_block = "**Weeks {0}-{1}**".format(ws, we)

        body = (
            "# {title}\n"
            "\n"
            "{week_block}\n"
            "\n"
            "See `../journal/weeks/` for the per-week journal entries\n"
            "and the weekly template (`../journal/TEMPLATE.md`).\n"
            "\n"
            "See `../docs/milestone_gates.md` for the gate that\n"
            "closes this phase and what you must demonstrate to pass it.\n"
            "\n"
            "Every week has a required core deliverable and an optional depth\n"
            "extension. The core lane keeps the apprenticeship completable; the\n"
            "depth lane is where you add proofs, benchmarks, and production\n"
            "trade-offs.\n"
            "\n"
            "## How to use this folder\n"
            "\n"
            "1. Create sub-folders per sub-topic (e.g. `01_math/linear_algebra/`).\n"
            "2. Land code, notes, and proofs here as you complete each week.\n"
            "3. Run `make progress` from the repo root to track completion.\n"
        ).format(title=title, week_block=week_block)
        write(path, body)


def generate_primitive_stubs(root: Path) -> None:
    base = root / "02_engineering_primitives"
    base.mkdir(parents=True, exist_ok=True)

    write(base / "__init__.py",
        '"""Engineering primitives for tensor-to-tenant.\n\n'
        'Each sub-package ships a small, well-tested module the rest of the\n'
        'course builds on. Keep dependencies minimal (stdlib + numpy + pytest\n'
        'until a primitive explicitly opts in to a heavier dep).\n"""\n')

    write(base / "README.md", textwrap.dedent("""\
        # Engineering Primitives

        Weeks 31-45 of the course. Every primitive gets:

        - a focused module with a public API,
        - a `README.md` explaining the contract,
        - a `tests/` folder with pytest coverage,
        - a `__init__.py` that re-exports the public surface.

        ## Primitive index

        | Folder | Topic | First used in week |
        |---|---|---|
        | retrieval | Cosine similarity, KNN, Top-K, reranking, chunking fusion | 31 |
        | rate_limiting | Token bucket, sliding window, leaky bucket | 34 |
        | caching | LRU, TTL, semantic, embedding cache | 35 |
        | chunking | Token-aware, recursive, sentence-aware | 36 |
        | pii | PII span merging, regex/NER redaction | 37 |
        | metrics | Recall@K, MRR, NDCG, ECE, Brier | 38 |
        | batching | Thread-safe inference batcher | 40 |
        | resilience | Retry/backoff, circuit breaker | 41 |
        | sketches | Count-Min, Bloom, HyperLogLog | 42 |
        | routing | Consistent hashing, load balancing | 43 |
        | ids | Snowflake IDs, traffic shaping | 45 |

        Run the whole suite from the repo root:

        ```bash
        make test
        ```
        """))

    for folder, topic in ENGINEERING_PRIMITIVES:
        pkg = base / folder
        tests = pkg / "tests"
        pkg.mkdir(parents=True, exist_ok=True)
        tests.mkdir(parents=True, exist_ok=True)

        write(pkg / "__init__.py",
            '"""Public surface for the {0} primitive."""\n'.format(folder))

        write(pkg / "README.md", textwrap.dedent("""\
            # `{folder}`

            **Topic:** {topic}

            Add your implementation in `__init__.py` (or split into multiple
            modules) and re-export the public API from there.

            ## Contract

            Document the contract in this README as you build it. At minimum:

            - function signatures,
            - input domain,
            - output domain,
            - complexity,
            - side effects (or lack thereof),
            - failure modes.

            ## Tests

            ```bash
            pytest 02_engineering_primitives/{folder}/tests
            ```
            """).format(folder=folder, topic=topic))

        write(tests / "__init__.py", "")
        write(tests / "test_{0}.py".format(folder), textwrap.dedent("""\
            \"\"\"Smoke tests for the {folder} primitive.\n\n            Replace with real tests as you implement the primitive. The cookiecutter\n            ships only a sentinel that fails until you write a real assertion, so\n            CI won't greenwash an empty primitive.\n            \"\"\"\n\n            import pytest\n\n\n            def test_primitive_has_public_api():\n                from engineering_primitives import {folder}  # noqa: F401\n                # TODO: assert that {folder} exports the documented surface.\n                pytest.fail("primitive not implemented yet -- see README.md")\n            """).format(folder=folder))


def generate_interview_folders(root: Path) -> None:
    base = root / "09_interview"
    base.mkdir(parents=True, exist_ok=True)

    write(base / "README.md", textwrap.dedent("""\
        # Interview Preparation

        Interview prep runs **continuously** across all 108 weeks, not just at the end.

        ## Weekly minimums

        Every week ship at least:

        - 1 coding drill (see `coding/`)
        - Optional Leetcode Darbar problem set (see `leetcode_darbar/`)
        - 1 Algorithmic Forge drill at the tier specified by the weekly journal
        - 1 system design question or pattern (see `system_design/`)
        - 1 behavioral story refinement (see `behavioral/`)
        - 1 verbal technical explanation (out loud, recorded, or written)

        ## Folder map

        - `system_design/` -- design docs, trade-off writeups, case-study retro notes
        - `coding/` -- LeetCode, Grind75, timed drills, Mo's algorithm practice
        - `leetcode_darbar/` -- 548-slot speed/practice tracker for the Auror lane
        - `behavioral/` -- CARL-format stories (Context / Action / Result / Learning)
        - `mocks/` -- mock-interview scorecards + retro actions
        """))

    for folder, desc in INTERVIEW_DRILLS:
        pkg = base / folder
        pkg.mkdir(parents=True, exist_ok=True)
        write(pkg / "README.md", textwrap.dedent("""\
            # `{folder}`

            {desc}

            Land one artifact per week here. Use file names like
            `YYYY-MM-DD_<short-slug>.md` so the timeline is sortable.
            """).format(folder=folder, desc=desc))


def generate_capstone_scaffold(root: Path) -> None:
    base = root / "08_capstone"
    for sub in ("design", "src", "eval", "dashboards", "reports"):
        (base / sub).mkdir(parents=True, exist_ok=True)
    gateway = base / "openrouter"
    for sub in ("design", "src", "eval", "dashboards", "reports"):
        (gateway / sub).mkdir(parents=True, exist_ok=True)

    write(base / "README.md", textwrap.dedent("""\
        # Capstone -- Multi-Tenant LLM Trace Forensics

        This is your Phase 9 deliverable. It synthesizes every Phase 5-8 skill on
        a single realistic problem:

        - High-throughput ingestion (Weeks 94, 95)
        - Immutable sealed segments with watermark + correction segments (Week 100)
        - Exact slice forensics via Mo's algorithm (Phase 9 coding drill)
        - Approximation layer: HLL, Count-Min, t-digest (Weeks 70-71 math curriculum)
        - Multi-tenant isolation + admission control (Week 99)
        - Self-observability (Week 101)

        ## Optional Week 108 Boss Fight

        `CAPSTONE2_EULER_DSU.md` is the optional **Multi-Tenant Agent Execution
        Forensics** extension: Euler Tour + DSU on Tree over agent execution
        trees. It is a Boss fight, not a prerequisite for the LLM Platform badge.

        ## Folder layout

        - `design/` -- system-design doc, Mermaid/ASCII diagrams, trade-off tables
        - `src/` -- your implementation (start with the worked solution in the
          parent course bundle's `CAPSTONE.md`, then add tenant filtering,
          sketches, etc.)
        - `eval/` -- synthetic workload generator, slice evaluation, regressions
        - `dashboards/` -- Grafana JSON or ASCII dashboards for the forensics
          service itself
        - `reports/` -- final writeup + benchmark + interview summary

        ## Capstone 3 — OpenRouter-inspired Enterprise AI Gateway

        `openrouter/` is the gateway path. Build a local simulator with mock
        providers and document unified API normalization, provider registry,
        policy-aware routing, stream-safe failover, enterprise tenancy,
        per-tenant admission, idempotent cost attribution, and PII-safe
        observability. The parent course bundle's `CAPSTONE3_OPENROUTER.md`
        contains the full requirements, failure matrix, evidence checklist, and
        24-point rubric.

        ## Self-grade before mock interview

        Use the 24-point rubric in your course bundle's `CAPSTONE.md`. Schedule
        the Week 107 mock interview only after you score 18+.
        """))
    write(gateway / "README.md", textwrap.dedent("""\
        # Capstone 3 — OpenRouter-inspired Enterprise AI Gateway

        This is an alternative final capstone for Weeks 103-108. It is a design
        and implementation simulator, not a claim to reproduce private
        OpenRouter internals.

        ## Required evidence

        - `design/` - requirements, architecture, control/request-plane boundary,
          route-decision contract, and trade-offs
        - `src/` - normalized API, provider adapters, policy/routing,
          stream-aware fallback, admission, and usage ledger
        - `eval/` - provider failures, policy matrix, fairness, accounting, and
          gateway-overhead benchmarks
        - `dashboards/` - route, TTFT, throughput, fallback, budget, token, and
          cost views without raw prompts
        - `reports/` - threat model, incident runbook, cost reconciliation,
          portfolio writeup, and staff-defense recording notes

        Minimum: three mock providers, three core components implemented from
        scratch, and tests for every failure in the capstone matrix.
        """))


def generate_milestone_gates_doc(root: Path) -> None:
    write(root / "docs" / "milestone_gates.md", textwrap.dedent("""\
        # Milestone Gates

        These are **blocking** checkpoints. If a gate fails, the next gate is
        blocked until the learner completes a targeted remediation cycle and
        submits implementation, result, explanation, and retrospective evidence.
        See `scripts/milestone_gate.py` for the automated checker and
        `docs/remediation/` for the repair plans.

        | Gate | Week | Pass criteria | If blocked |
        |---:|---:|---|---|
        | 1 | 6  | Course repo + weekly tracker + Dockerized service + diagnostic report | Remediate orientation |
        | 2 | 18 | Eigenvalues, SVD, norms, condition numbers; basic numerical routines | Remediate numerical algebra |
        | 3 | 30 | Derive gradients; explain MLE/MAP; implement tests + bootstrap CIs | Remediate math/statistics; publish Foundations |
        | 4 | 45 | Completed all engineering primitives | Remediate primitive contracts/tests |
        | 5 | 57 | Completed system design case studies | Remediate the weakest design pattern |
        | 6 | 69 | A/B tool, bootstrap, SRM detector, flags, assignment, monitoring plan | Remediate MLOps; publish Engineering + Systems |
        | 7 | 81 | RAG pipeline, eval report, prompt system, memory, agent prototype | Remediate LLM/RAG |
        | 8 | 93 | vLLM/SGLang deployment, benchmark, dashboard, quantization, cost model | Remediate inference operations |
        | 9 | 102 | Working production AI platform | Remediate missing platform capability |
        | 10 | 108 | Capstone, portfolio, mocks, behavioral stories, job plan | Remediate specific final gap |
        """))


def generate_course_map(root: Path) -> None:
    write(root / "docs" / "course_map.md", textwrap.dedent("""\
        # Course Map

        ```mermaid
        flowchart LR
            F["FOUNDATIONS<br/>Weeks 1–30<br/>Release"] --> E["ENGINEERING + SYSTEMS<br/>Weeks 31–69<br/>Release"] --> L["LLM PLATFORM<br/>Weeks 70–108<br/>Release"]
        ```

        ```
        Phase 0 -- Orientation                  Weeks   1 -   6
        Phase 1 -- Math foundations             Weeks   7 -  30
        Phase 3 -- Engineering primitives       Weeks  31 -  45
        Phase 4 -- System design                Weeks  46 -  57
        Phase 5 -- ML / MLOps                   Weeks  58 -  69
        Phase 6 -- LLM / RAG / Agents           Weeks  70 -  81
        Phase 7 -- LLM inference                Weeks  82 -  93
        Phase 8 -- Production AI platform       Weeks  94 - 102
        Phase 9 -- Capstone                     Weeks 103 - 108
        ```

        Use `make progress` from the repo root to see core completion, optional
        depth, evidence-complete weeks, and program summaries.
        """))


def personalize_readme(root: Path, start: dt.date, student: str, gh: str, repo: str) -> None:
    readme = root / "README.md"
    if not readme.exists():
        return
    text = readme.read_text(encoding="utf-8")
    text = text.replace("{{ cookiecutter.student_name }}", student)
    text = text.replace("{{ cookiecutter.github_username }}", gh)
    text = text.replace("{{ cookiecutter.repo_name }}", repo)
    text = text.replace("{{ cookiecutter.start_date }}", fmt_date(start))
    readme.write_text(text, encoding="utf-8")


def main() -> None:
    root = repo_root()

    start_raw = os.environ.get(
        "COOKIECUTTER_START_DATE",
        "{{ cookiecutter.start_date }}",
    )
    try:
        start = dt.date.fromisoformat(start_raw)
    except ValueError:
        start = dt.date.today()

    student = os.environ.get(
        "COOKIECUTTER_STUDENT_NAME",
        "{{ cookiecutter.student_name }}",
    )
    gh = os.environ.get(
        "COOKIECUTTER_GITHUB_USERNAME",
        "{{ cookiecutter.github_username }}",
    )
    repo = os.environ.get(
        "COOKIECUTTER_REPO_NAME",
        "{{ cookiecutter.repo_name }}",
    )

    sys.stdout.write("[t3] generating 108 weekly journal entries...\n")
    generate_weeks(root, start)

    sys.stdout.write("[t3] writing journal templates...\n")
    generate_journal_templates(root)

    sys.stdout.write("[t3] writing evidence scaffolds...\n")
    generate_evidence_scaffolds(root)

    sys.stdout.write("[t3] writing recovery windows...\n")
    generate_recovery_scaffolds(root)

    sys.stdout.write("[t3] writing phase READMEs...\n")
    generate_phase_readmes(root)

    sys.stdout.write("[t3] scaffolding engineering primitives...\n")
    generate_primitive_stubs(root)

    sys.stdout.write("[t3] scaffolding interview folders...\n")
    generate_interview_folders(root)

    sys.stdout.write("[t3] scaffolding Algorithmic Forge...\n")
    generate_algorithmic_forge_scaffold(root)

    sys.stdout.write("[t3] scaffolding System Design and OOD...\n")
    generate_system_design_scaffold(root)

    sys.stdout.write("[t3] scaffolding Leetcode Darbar...\n")
    generate_leetcode_darbar_scaffold(root)

    sys.stdout.write("[t3] scaffolding capstone...\n")
    generate_capstone_scaffold(root)

    sys.stdout.write("[t3] writing course map and milestone gates doc...\n")
    generate_course_map(root)
    generate_milestone_gates_doc(root)
    generate_program_docs(root)
    generate_portfolio_releases(root)
    generate_remediation_docs(root)

    sys.stdout.write("[t3] personalizing README...\n")
    personalize_readme(root, start, student, gh, repo)

    sys.stdout.write("[t3] done.\n")


if __name__ == "__main__":
    main()
