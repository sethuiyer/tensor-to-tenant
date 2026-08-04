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
    (5,  "Math diagnostic",                        "Linear algebra, calculus, probability baseline",               "Diagnostic report + gap map"),
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

            ## Objective
            -

            ## Monday -- Theory
            -

            ## Tuesday -- Build
            -

            ## Wednesday -- Systems / Papers
            -

            ## Thursday -- Eval / Interview
            -

            ## Friday -- Review / Retro
            -

            ## Deliverable
            - {DELIVERABLE}

            ## Evidence
            - Code:
            - Notes:
            - Results:

            ## Status
            - [ ] Monday
            - [ ] Tuesday
            - [ ] Wednesday
            - [ ] Thursday
            - [ ] Friday
            - [ ] Deliverable shipped
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


def generate_weeks(root: Path, start: dt.date) -> None:
    """Generate all 108 weekly journal entries."""
    weeks_dir = root / "journal" / "weeks"
    weeks_dir.mkdir(parents=True, exist_ok=True)

    for phase_num, phase_name, p_start, p_end, weeks in PHASES:
        for week_no, title, focus, deliverable in weeks:
            monday = monday_of(week_no, start)
            sunday = monday + dt.timedelta(days=6)

            body = (
                "# Week {n}: {title}\n"
                "\n"
                "**Phase {pn} -- {pname}** (Weeks {ps} to {pe})\n"
                "**Dates:** {dates}\n"
                "**Focus:** {focus}\n"
                "**Deliverable:** {deliv}\n"
                "\n"
                "## Objective\n"
                "-\n"
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
                "## Friday -- Review / Retro\n"
                "-\n"
                "\n"
                "## Deliverable\n"
                "- {deliv}\n"
                "\n"
                "## Evidence\n"
                "- Code:\n"
                "- Notes:\n"
                "- Results:\n"
                "\n"
                "## Status\n"
                "- [ ] Monday\n"
                "- [ ] Tuesday\n"
                "- [ ] Wednesday\n"
                "- [ ] Thursday\n"
                "- [ ] Friday\n"
                "- [ ] Deliverable shipped\n"
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
            )
            write(weeks_dir / "week_{0:03d}.md".format(week_no), body)


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
        - 1 system design question or pattern (see `system_design/`)
        - 1 behavioral story refinement (see `behavioral/`)
        - 1 verbal technical explanation (out loud, recorded, or written)

        ## Folder map

        - `system_design/` -- design docs, trade-off writeups, case-study retro notes
        - `coding/` -- LeetCode, Grind75, timed drills, Mo's algorithm practice
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

        ## Folder layout

        - `design/` -- system-design doc, Mermaid/ASCII diagrams, trade-off tables
        - `src/` -- your implementation (start with the worked solution in the
          parent course bundle's `CAPSTONE.md`, then add tenant filtering,
          sketches, etc.)
        - `eval/` -- synthetic workload generator, slice evaluation, regressions
        - `dashboards/` -- Grafana JSON or ASCII dashboards for the forensics
          service itself
        - `reports/` -- final writeup + benchmark + interview summary

        ## Self-grade before mock interview

        Use the 24-point rubric in your course bundle's `CAPSTONE.md`. Schedule
        the Week 107 mock interview only after you score 18+.
        """))


def generate_milestone_gates_doc(root: Path) -> None:
    write(root / "docs" / "milestone_gates.md", textwrap.dedent("""\
        # Milestone Gates

        The 10 pass/fail checkpoints for the course. See `scripts/milestone_gate.py`
        for the automated checker.

        | Gate | Week | Pass criteria |
        |---:|---:|---|
        | 1 | 6  | Course repo + weekly tracker + Dockerized service + diagnostic report |
        | 2 | 18 | Eigenvalues, SVD, norms, condition numbers; basic numerical routines |
        | 3 | 30 | Derive basic gradients; explain MLE/MAP; implement hypothesis tests + bootstrap CIs |
        | 4 | 45 | Completed all engineering primitives |
        | 5 | 57 | Completed system design case studies |
        | 6 | 69 | A/B analysis tool, bootstrap tool, SRM detector, feature flag engine, monitoring plan |
        | 7 | 81 | RAG retrieval pipeline, retrieval evaluation report, prompt system, memory system, agent prototype |
        | 8 | 93 | Deployed vLLM or SGLang, benchmark methodology, observability dashboard, quantization report |
        | 9 | 102 | Working production AI platform |
        | 10 | 108 | Completed capstone, published portfolio, passed mock interviews, behavioral stories, 30-day job-search plan |
        """))


def generate_course_map(root: Path) -> None:
    write(root / "docs" / "course_map.md", textwrap.dedent("""\
        # Course Map

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

        Use `make progress` from the repo root to see live completion by phase.
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

    sys.stdout.write("[t3] writing phase READMEs...\n")
    generate_phase_readmes(root)

    sys.stdout.write("[t3] scaffolding engineering primitives...\n")
    generate_primitive_stubs(root)

    sys.stdout.write("[t3] scaffolding interview folders...\n")
    generate_interview_folders(root)

    sys.stdout.write("[t3] scaffolding capstone...\n")
    generate_capstone_scaffold(root)

    sys.stdout.write("[t3] writing course map and milestone gates doc...\n")
    generate_course_map(root)
    generate_milestone_gates_doc(root)

    sys.stdout.write("[t3] personalizing README...\n")
    personalize_readme(root, start, student, gh, repo)

    sys.stdout.write("[t3] done.\n")


if __name__ == "__main__":
    main()