# `tensor-to-tenant`

![tensor-to-tenant banner](./tensor_to_tenant_cutout.png)

> *A 108-week journey from linear algebra to multi-tenant production AI platforms.*

A consolidated, production-oriented learning path that turns you into an AI / software engineer who can build, evaluate, deploy, and operate ML and LLM systems — and pass the interviews that get you hired to do it.

![108 weeks](https://img.shields.io/badge/duration-108_weeks-blueviolet)
![Phases](https://img.shields.io/badge/phases-10-blue)
![Effort](https://img.shields.io/badge/effort-10%E2%80%9315_hrs%2Fwk-orange)
![Stack](https://img.shields.io/badge/stack-ML_%2F_LLM_%2F_Platform-success)

> **Duration:** 108 weeks · **Effort:** 10–15 hours/week · **Rhythm:** Mon = theory, Tue = build, Wed = systems/papers, Thu = eval/interview, Fri = review/retro, Weekend = buffer.

### What's inside

| File | Purpose |
|---|---|
| `README.md` | The 108-week curriculum, all phases, all reference resources |
| `CAPSTONE.md` | **Final capstone interview artifact** — staff-level Multi-Tenant LLM Trace Forensics with Mo's algorithm (system design + coding + worked solution + self-grading rubric) |
| `cookiecutter/` | **[`cookiecutter-tensor-to-tenant`](#the-cookiecutter--portfolio-piece--social-proof)** — one-command scaffolder that turns this course into a personalized 108-week learner repo with progress dashboard, milestone gates, and primitive stubs. The cookiecutter itself is the **portfolio piece** and the **social proof** of the course. |
| `chat-108 Week Course Design.txt` *(optional, local-only)* | Original course design source. Not required to use the repo. |
| `COTNEXT.md` *(optional, local-only)* | Source knowledge base (books, papers, blogs, YouTube, math curriculum). Not required to use the repo. |

### The cookiecutter — portfolio piece & social proof

The `cookiecutter/` directory is a runnable [Cookiecutter](https://cookiecutter.readthedocs.io/) template. One command scaffolds a fresh, personalized learner repo with all 108 weekly journal entries pre-stamped with your start date, engineering-primitive stubs, an interview-drill folder tree, the capstone scaffold, and three helper scripts (`make progress`, `make gate`, `make journal`).

```bash
pip install cookiecutter
cookiecutter gh:sethuiyer/tensor-to-tenant
# answer the prompts — repo is ready in 30 seconds.
```

**Why this is the portfolio piece:**

The cookiecutter *is* the artifact. A learner who runs it and ships through Week 108 ends up with:

1. A **public git history** of 108 weeks of focused work — the most credible resume an AI engineer can produce.
2. **A working capstone** (Phase 9) — the same Multi-Tenant LLM Trace Forensics problem this README documents.
3. **A reusable engineering primitive library** in `02_engineering_primitives/` — retrieval, rate limiting, caching, sketches, routing, every primitive with tests.
4. **The cookiecutter itself**, forkable. The cleanest signal of "I understand AI systems end-to-end" is shipping a parameterized, opinionated course that someone else can run.

**Why this is the social proof:**

Every public learner repo generated from this template is a public commit that says *“I did the work.”* The cookiecutter is the course’s compounding loop:

- More learners → more public repos → more visible proof the course works → more learners.
- Every cohort member gets the same folder structure, so peer review and group retros just work.
- When someone forks the cookiecutter to ship their own variant (e.g. *tensor-to-tenant for healthcare*), the original repo gains a citation.

If you’re a hiring manager, an engineer evaluating the course, or a future self wondering whether 108 weeks was worth it: **look at the forks and the public learner repos.** The cookiecutter makes them cheap to start and impossible to fake.

### The arc: tensor → tenant

```text
tensor     — vector spaces, SVD, kernels, attention (Weeks 7–30)
    ↓
model      — transformers, RAG, agents, fine-tuning (Weeks 70–81)
    ↓
inference  — vLLM, SGLang, FlashAttention, quantization (Weeks 82–93)
    ↓
platform   — router, quotas, tracing, model registry, cost (Weeks 94–102)
    ↓
tenant     — multi-tenant isolation, admission, fairness (CAPSTONE)
```

---

## Table of Contents

1. [Course Goal](#course-goal)
2. [Course Structure (10 Phases)](#course-structure-10-phases)
3. [Full 108-Week Curriculum](#full-108-week-curriculum)
4. [Phase Details](#phase-details)
   - [Phase 1 — Orientation, Tooling, Diagnostics (Weeks 1–6)](#phase-1--orientation-tooling-and-diagnostics--weeks-16)
   - [Phase 2 — Mathematical Foundations I (Weeks 7–18)](#phase-2--mathematical-foundations-i--weeks-718)
   - [Phase 3 — Mathematical Foundations II (Weeks 19–30)](#phase-3--mathematical-foundations-ii--weeks-1930)
   - [Phase 4 — Engineering Micro-Projects (Weeks 31–45)](#phase-4--engineering-micro-projects-and-applied-ml-primitives--weeks-3145)
   - [Phase 5 — System Design & Distributed Systems (Weeks 46–57)](#phase-5--system-design-and-distributed-systems-fundamentals--weeks-4657)
   - [Phase 6 — ML Lifecycle, Experimentation & MLOps (Weeks 58–69)](#phase-6--ml-lifecycle-experimentation-and-mlops--weeks-5869)
   - [Phase 7 — LLM Training, RAG, Agents, Evaluation (Weeks 70–81)](#phase-7--llm-training-rag-agents-and-evaluation--weeks-7081)
   - [Phase 8 — LLM Inference & Performance Engineering (Weeks 82–93)](#phase-8--llm-inference-and-performance-engineering--weeks-8293)
   - [Phase 9 — Production AI Platform Engineering (Weeks 94–102)](#phase-9--production-ai-platform-engineering--weeks-94102)
   - [Phase 10 — Capstone, Portfolio & Interview Readiness (Weeks 103–108)](#phase-10--capstone-portfolio-and-interview-readiness--weeks-103108)
5. [Milestone Gates](#milestone-gates)
6. [Source Material Mapping](#source-material-mapping)
   - [Math Curriculum Path](#math-curriculum-path)
   - [Engineering Implementation Tasks](#engineering-implementation-tasks)
   - [Engineering Practice Exercises](#engineering-practice-exercises)
   - [System Design Roadmap](#system-design-roadmap)
   - [ML Systems & MLOps Reading](#ml-systems--mlops-reading)
   - [LLM Inference Papers & Systems](#llm-inference-papers--systems)
   - [LLM Training, RAG, Agents & Evaluation](#llm-training-rag-agents--evaluation)
7. [Weekly Template & Repo Structure](#weekly-template--repo-structure)
8. [Interview Preparation Integration](#interview-preparation-integration)
9. [Behavioral Interview Track (CARL Stories)](#behavioral-interview-track-carl-stories)
10. [Final Capstone Requirements](#final-capstone-requirements)
11. [Completion Criteria](#completion-criteria)
12. [Final Capstone Artifact](#final-capstone-artifact)
13. [Reference Resources](#reference-resources)
    - [YouTube Playlists](#youtube-playlists)
    - [Books & Reading List](#books--reading-list)
    - [Research Papers](#research-papers)
    - [Blog & Article URLs](#blog--article-urls)
    - [Interview Preparation Roadmap](#interview-preparation-roadmap)
14. [Repository Layout](#repository-layout)

---

## Course Goal

Train into a production-oriented AI/software engineer who can:

1. Build and evaluate ML/LLM systems.
2. Understand LLM inference, RAG, agents, and serving infrastructure.
3. Implement production-grade backend and distributed-system patterns.
4. Pass system design, coding, ML, and behavioral interviews.
5. Produce a portfolio of reproducible projects, benchmarks, and design docs.

---

## Course Structure (10 Phases)

| Phase | Weeks | Theme |
|---:|---:|---|
| 1 | 1–6 | Orientation, tooling, and diagnostics |
| 2 | 7–18 | Mathematical foundations I: linear algebra & numerical methods |
| 3 | 19–30 | Mathematical foundations II: calculus, autodiff, probability, statistics |
| 4 | 31–45 | Engineering micro-projects and applied ML primitives |
| 5 | 46–57 | System design and distributed systems fundamentals |
| 6 | 58–69 | ML lifecycle, experimentation, and MLOps |
| 7 | 70–81 | LLM training, RAG, agents, and evaluation |
| 8 | 82–93 | LLM inference and performance engineering |
| 9 | 94–102 | Production AI platform engineering |
| 10 | 103–108 | Capstone, portfolio, and interview readiness |

---

## Full 108-Week Curriculum

| Week | Module | Focus | Deliverable |
|---:|---|---|---|
| 1 | Orientation and course OS | Course setup, tracker, repo, weekly template | Course dashboard + README |
| 2 | Python engineering refresh | Typing, testing, async basics | CLI project skeleton with tests |
| 3 | Numerical Python | NumPy, vectorization, broadcasting | Vector math utility library |
| 4 | Reproducibility | Git, notebooks, experiment tracking | Reproducible notebook + Makefile |
| 5 | Math diagnostic | Linear algebra, calculus, probability baseline | Diagnostic report + gap map |
| 6 | Systems diagnostic | HTTP, Docker, APIs, Linux basics | Containerized hello-service |
| 7 | Linear algebra I | Vector spaces, span, basis, dimension | Problem set + concept map |
| 8 | Linear algebra II | Linear independence, rank, nullity | Solver exercises + notes |
| 9 | Linear algebra III | Inner products, norms, dual norms | Norm/distance library |
| 10 | Linear algebra IV | Orthogonality, projections, Gram-Schmidt | Projection demo |
| 11 | Linear algebra V | Linear transformations, change of basis | Coordinate transform lab |
| 12 | Linear algebra VI | Eigenvalues, eigenvectors, diagonalization | PCA-style mini lab |
| 13 | Linear algebra VII | PSD matrices, quadratic forms, Rayleigh quotient | Proof + visualization |
| 14 | Linear algebra VIII | SVD, pseudoinverse, low-rank approximation | Low-rank compression demo |
| 15 | Numerical linear algebra I | Matrix norms, condition numbers, perturbation | Perturbation experiment |
| 16 | Numerical linear algebra II | LU, QR, Cholesky decomposition | Decomposition library |
| 17 | Numerical linear algebra III | Iterative solvers, power iteration, Krylov methods | Solver benchmark |
| 18 | Numerical linear algebra IV | Randomized SVD, tensor notation | Randomized approximation lab |
| 19 | Calculus I | Partial derivatives, gradients, directional derivatives | Gradient visualizer |
| 20 | Calculus II | Jacobians, Hessians, Taylor approximations | Curvature lab |
| 21 | Calculus III | Chain rule on computational graphs | Manual backprop worksheet |
| 22 | Automatic differentiation | Forward/reverse mode, JVPs, VJPs | Tiny autodiff prototype |
| 23 | Probability I | Probability spaces, conditioning, Bayes theorem | Probability problem set |
| 24 | Probability II | Random variables, distributions, transformations | Simulation notebook |
| 25 | Probability III | Random vectors, covariance, correlation | Covariance/correlation lab |
| 26 | Probability IV | LLN, CLT, delta method | Monte Carlo convergence demo |
| 27 | Statistics I | MLE, MAP, estimator bias/variance | Estimator comparison |
| 28 | Statistics II | Hypothesis testing, p-values, Type I/II errors | Test implementation |
| 29 | Statistics III | Confidence intervals, bootstrap, permutation tests | Bootstrap CI package |
| 30 | Statistics IV | Power, MDE, sample size, multiple testing | Experiment-size calculator |
| 31 | Retrieval math | Cosine similarity, exact KNN | Vector search mini-lab |
| 32 | Top-K systems | Memory-bounded KNN, streaming Top-K | Heap-based Top-K service |
| 33 | Ranking pipelines | Dynamic Top-K, two-stage retrieval/reranking | Reranking prototype |
| 34 | Rate limiting I | Sliding-window and token bucket rate limiters | API limiter module |
| 35 | Caching | LRU cache and TTL cache | Cache simulator with tests |
| 36 | Text chunking | Token-aware and recursive sentence chunking | Chunking library |
| 37 | PII handling | PII span merging, regex/NER detection | Redaction utility |
| 38 | Calibration | Expected Calibration Error, Brier score | Reliability dashboard |
| 39 | Ranking metrics | NDCG, MRR, Recall@K | Retrieval evaluator |
| 40 | Batching | Thread-safe inference batcher | Concurrent batcher |
| 41 | Resilience | Retry, exponential backoff, jitter, circuit breaker | Fault-tolerance kit |
| 42 | Sketches | Count-Min Sketch, Bloom filter | Probabilistic data structures |
| 43 | Cardinality/routing | HyperLogLog, consistent hashing | Distributed routing lab |
| 44 | Load balancing | Weighted round robin, rendezvous hashing | Load balancer module |
| 45 | IDs/traffic | Snowflake IDs, leaky bucket, sliding-window counter | Platform primitives lab |
| 46 | System design framework | Requirements, constraints, API design | Design doc template |
| 47 | Data and APIs | Data models, observability, contracts | API design exercise |
| 48 | Rate limiting design | Token bucket, sliding windows at scale | Rate limiter design writeup |
| 49 | Scaling reads/writes | Caching, replication, contention | Scaling pattern notes |
| 50 | Large blobs | Storage, CDN, media pipelines | Blob storage design |
| 51 | Workflow systems | Orchestration vs choreography | Workflow state design |
| 52 | Schema evolution | Backward compatibility, contracts | Schema migration plan |
| 53 | Case studies I | URL shortener, Dropbox | Two design docs |
| 54 | Case studies II | Ticketmaster, News Feed | Two design docs |
| 55 | Case studies III | WhatsApp, LeetCode | Two design docs |
| 56 | Case studies IV | Uber, web crawler | Two design docs |
| 57 | Case studies V | Ad click aggregator, payments | Trade-off analysis |
| 58 | ML problem framing | Objectives, constraints, iterative development | ML project charter |
| 59 | Data quality | Labeling, weak supervision, augmentation | Data quality checklist |
| 60 | Leakage/contamination | Detection, eval tracking, versioning | Leakage audit |
| 61 | Offline evaluation | Baselines, slices, confidence intervals | Eval harness |
| 62 | Online evaluation | A/B tests, shadow deployment, canary, bandits | Rollout plan |
| 63 | A/B calculator | Lift, z-score, p-value, confidence intervals | `analyze_ab_test` function |
| 64 | Bootstrap methods | Paired bootstrap for model comparisons | `bootstrap_ci` package |
| 65 | SRM detection | Sample-ratio mismatch, chi-square diagnostics | SRM detector |
| 66 | Feature flags | Rules, rollouts, sticky assignment | Flag engine |
| 67 | Experiment assignment | Deterministic assignment, namespaces | Assignment service |
| 68 | Monitoring | Drift, observability, four-layer monitoring | Monitoring dashboard spec |
| 69 | Production failures | Distribution shift, postmortems | Incident postmortem template |
| 70 | LLM anatomy | Transformer, tokenizer, matmul | Model anatomy notes |
| 71 | LLM data pipelines | Cleaning, deduplication, tokenization | Dataset card |
| 72 | Fine-tuning | SFT, LoRA, QLoRA, DoRA | Fine-tuning plan |
| 73 | Alignment | RLHF, DPO, ORPO, GRPO | Preference eval plan |
| 74 | Distributed training | DDP/FSDP, tensor/pipeline parallelism, ZeRO | Training architecture map |
| 75 | Vector search | HNSW, IVF-PQ, product quantization | Index benchmark |
| 76 | Retrieval patterns | Hybrid search, query rewriting, chunking | Retrieval lab |
| 77 | Retrieval fusion | BM25 + dense + reranker, RRF | Fusion service |
| 78 | Retrieval eval | Query slices, macro metrics, regressions | Slice evaluation report |
| 79 | Prompt systems | Prompt template renderer, version registry | Prompt management tool |
| 80 | Memory/context | Conversation memory, context optimizer | Memory service |
| 81 | Agent foundations | ReAct, plan-execute, tool calling, guardrails | Agent prototype |
| 82 | GPU performance | Compute/memory/overhead regimes, FlashAttention | Performance primer notes |
| 83 | Inference arithmetic | Roofline model, arithmetic intensity | Model intensity worksheet |
| 84 | PagedAttention/vLLM | KV paging, block tables | vLLM deployment |
| 85 | vLLM internals | Scheduler, block manager, code paths | Internal anatomy notes |
| 86 | vLLM metrics | Running/waiting requests, latency histograms | Metrics schema |
| 87 | Observability | Prometheus/Grafana for serving | Live inference dashboard |
| 88 | Benchmarking | Request-rate sweeps, saturation points | Benchmark methodology doc |
| 89 | SGLang | RadixAttention, prefix reuse | SGLang comparison report |
| 90 | Scheduling | Orca, continuous batching, chunked prefill | Scheduler comparison |
| 91 | Quantization | FP8, AWQ, GPTQ, KV cache compression | Quality/throughput table |
| 92 | Speculative/long context | Medusa, EAGLE, StreamingLLM, KV eviction | Latency/memory lab |
| 93 | Disaggregation | DistServe, Splitwise, Mooncake, autoscaling | Disaggregated serving plan |
| 94 | Traffic routing | Model router, kill switch, sticky rollout | Router service |
| 95 | Safe observability | PII redaction, end-to-end request tracing | Trace + safe logs |
| 96 | Fan-out/streaming | Partial failures, token stream multiplexing | Resilient aggregator |
| 97 | Quotas/priority | Token budgets, gateway prioritization | Quota/priority service |
| 98 | Workflow execution | DAG scheduler, idempotency | Workflow engine |
| 99 | Fairness/HA | Per-tenant limits, leader election | Tenant limiter + HA lab |
| 100 | Async infrastructure | Distributed work queue, config service | Queue/config platform |
| 101 | Model lifecycle | Health monitor, registry/promotion | Model ops pipeline |
| 102 | Cost/safety/caching | Semantic/embedding cache, injection detection, cost attribution | Cost/safety platform |
| 103 | Capstone planning | Requirements, architecture, eval plan | Capstone design doc |
| 104 | Capstone build I | Core API, retrieval/agent flow | Working prototype |
| 105 | Capstone build II | Evaluation, observability, guardrails | Monitored prototype |
| 106 | Capstone build III | Load testing, optimization, cost tuning | Performance report |
| 107 | Mock interview week | System design, coding, behavioral simulations | Mock interview scorecard |
| 108 | Final review | Portfolio, retrospective, job plan | Final portfolio + 30-day plan |

---

## Phase Details

### Phase 1 — Orientation, Tooling, and Diagnostics (Weeks 1–6)

**Objective:** Build the operating system for the next 108 weeks.

**Outcomes:** course repo, weekly tracker, notes system, Python env with testing/linting, Docker starter service, math + systems diagnostic report.

**Habits:** weekly plan, weekly retro, single repo, one markdown file per week.

### Phase 2 — Mathematical Foundations I (Weeks 7–18)

Vector spaces, span, basis, dimension, linear independence, rank, nullity, inner products, norms, orthogonality, projections, Gram-Schmidt, eigenvalues/eigenvectors, PSD matrices, SVD, matrix norms, condition numbers, LU/QR/Cholesky, iterative solvers, randomized SVD, tensor notation.

### Phase 3 — Mathematical Foundations II (Weeks 19–30)

Partial derivatives, gradients, Jacobians, Hessians, Taylor expansions, computational graphs, forward/reverse autodiff, probability spaces, Bayes, random variables, covariance, LLN/CLT, MLE/MAP, hypothesis testing, bootstrap, power analysis, multiple testing.

### Phase 4 — Engineering Micro-Projects and Applied ML Primitives (Weeks 31–45)

Cosine similarity, KNN, Top-K retrieval, streaming Top-K, reranking, rate limiting, LRU/TTL caches, chunking, PII redaction, calibration metrics, ranking metrics, inference batching, retry/backoff, circuit breakers, Bloom filters, Count-Min Sketch, HyperLogLog, consistent hashing, load balancing, Snowflake IDs.

Reusable library layout:

```text
engineering_primitives/
  retrieval/
  rate_limiting/
  caching/
  chunking/
  pii/
  metrics/
  batching/
  resilience/
  sketches/
  routing/
  ids/
```

### Phase 5 — System Design and Distributed Systems Fundamentals (Weeks 46–57)

Requirements, trade-offs, API design, data modeling, observability, rate limiting, caching, replication, scaling reads/writes, blob storage, workflow orchestration, schema evolution, and **10 classic case studies**: URL shortener, Dropbox, Ticketmaster, News Feed, WhatsApp, LeetCode, Uber, web crawler, ad click aggregator, payments.

For each case study, deliver: requirements, high-level architecture, data model, API design, scaling plan, failure modes, trade-offs, bottom-line recommendation.

### Phase 6 — ML Lifecycle, Experimentation, and MLOps (Weeks 58–69)

Business objectives, constraints, labeling, weak supervision, augmentation, leakage/contamination, experiment tracking, baselines, offline evaluation, slicing, CIs, A/B testing, shadow, canary, bandits, SRM detection, feature flags, monitoring, drift, incident postmortems.

### Phase 7 — LLM Training, RAG, Agents, and Evaluation (Weeks 70–81)

Transformer architecture, tokenization, data pipelines, dedup, SFT/LoRA/QLoRA/DoRA, RLHF/DPO/ORPO/GRPO, distributed training (DDP/FSDP/tensor/pipeline/ZeRO), vector DBs (HNSW, IVF-PQ), hybrid search, query rewriting, chunking, retrieval fusion, retrieval evaluation, prompt management, memory, agent architectures (ReAct, plan-execute).

### Phase 8 — LLM Inference and Performance Engineering (Weeks 82–93)

GPU performance regimes, arithmetic intensity, roofline, FlashAttention, PagedAttention, vLLM, SGLang, RadixAttention, continuous batching, Orca, Sarathi-Serve, chunked prefill, FP8/AWQ/GPTQ, KV-cache compression (KIVI, H2O, SnapKV, MInference), speculative decoding (Medusa, EAGLE), StreamingLLM, DistServe, Splitwise, Mooncake, disaggregated prefill/decode, autoscaling, inference economics.

### Phase 9 — Production AI Platform Engineering (Weeks 94–102)

Model-version traffic routing, canary, kill switches, structured logging, PII redaction, distributed tracing, async fan-out, partial failures, streaming multiplexing, token budgeting, API prioritization, tool-call scheduling, idempotency, per-tenant concurrency limiting, leader election, distributed work queues, config services, model health monitoring, model registry, promotion pipelines, semantic/embedding caching, prompt injection detection, cost attribution.

```text
ai_platform/
  router/  experiments/  logging/  tracing/  fanout/
  quotas/  scheduler/  idempotency/  tenant_limiter/
  leader_election/  work_queue/  config_service/
  model_registry/  health_monitor/  semantic_cache/
  embedding_cache/  injection_detector/  cost_attribution/
```

### Phase 10 — Capstone, Portfolio, and Interview Readiness (Weeks 103–108)

Pick **one** capstone: Enterprise RAG assistant · LLM gateway/platform · Agent workflow platform · Experimentation platform · Multimodal search system.

---

## Milestone Gates

| Gate | Week | Pass criteria |
|---:|---:|---|
| 1 | 6 | Course repo · weekly tracker · Dockerized service · diagnostic report |
| 2 | 18 | Explain eigenvalues, SVD, norms, condition numbers; implement basic numerical routines |
| 3 | 30 | Derive basic gradients; explain MLE/MAP; implement hypothesis tests + bootstrap CIs; explain power/MDE |
| 4 | 45 | Completed all engineering primitives (retrieval, rate limiting, caching, chunking, PII, metrics, resilience, sketches, routing) |
| 5 | 57 | Completed system design case studies with requirements, API, data model, scaling, trade-offs, failure modes |
| 6 | 69 | A/B analysis tool, bootstrap tool, SRM detector, feature flag engine, experiment assignment, monitoring plan |
| 7 | 81 | RAG retrieval pipeline, retrieval evaluation report, prompt system, memory system, agent prototype |
| 8 | 93 | Deployed vLLM or SGLang, benchmark methodology, observability dashboard, quantization report, speculative decoding report, inference cost model |
| 9 | 102 | Working production AI platform: router, quotas, tracing, logging, idempotency, work queue, model registry, cost attribution, safety filters |
| 10 | 108 | Completed capstone, published portfolio, passed mock interviews, behavioral stories, 30-day job-search plan |

---

## Source Material Mapping

### Math Curriculum Path

| Source topic | Course weeks |
|---|---:|
| Linear algebra | 7–14 |
| Numerical linear algebra | 15–18 |
| Calculus | 19–21 |
| Automatic differentiation | 22 |
| Probability | 23–26 |
| Statistics | 27–30 |
| Optimization | Integrated in 28, 61, 72, 88 |
| Information theory | Integrated in 30, 73, 91 |
| Stochastic processes | Integrated in 26, 41, 100 |
| Queueing theory | Integrated in 48, 88, 93, 97 |
| High-dimensional geometry | Integrated in 15, 31, 75 |
| Randomized algorithms | Integrated in 18, 42, 43 |
| Streaming mathematics | Integrated in 32, 42, 43 |
| Graph theory | Integrated in 51, 76, 77, 81 |
| Statistical learning theory | Integrated in 38, 61, 72, 78 |
| Bayesian methods | Integrated in 23, 27, 29, 73 |
| Monte Carlo | Integrated in 26, 29 |
| Distributed systems mathematics | Integrated in 43–45, 94–102 |

The full 100-module mathematics curriculum path (tracks + topics) lives in [§ Mathematics Curriculum Path](#mathematics-curriculum-path) below.

### Engineering Implementation Tasks

| Task | Week |
|---|---:|
| A/B Test Significance Calculator | 63 |
| Bootstrap Confidence Interval | 64 |
| Sample-Ratio Mismatch Detector | 65 |
| Feature Flag Evaluation Engine | 66 |
| Experiment Assignment Service | 67, 94 |
| Retrieval Evaluation by Query Slice | 78 |
| Retrieval Fusion Engine | 77 |
| Prompt Template Renderer | 79 |
| Prompt Version Registry | 79 |
| Conversation Memory Store | 80 |
| Context Window Optimizer | 80 |
| Prompt Injection Detector | 102 |
| Tool-Call Dependency Scheduler | 98 |
| Idempotent Request Deduplicator | 98 |
| Per-Tenant Concurrency Limiter | 99 |
| Model-Version Traffic Router | 94 |
| Structured Logger With PII Redaction | 95 |
| Async Fan-Out With Partial Failures | 96 |
| Streaming Response Multiplexer | 96 |
| Distributed Token Budget Manager | 97 |
| API Gateway Request Prioritizer | 97 |
| Distributed Work Queue | 100 |
| Distributed Configuration Service | 100 |
| Distributed Leader Election | 99 |
| Model Health Monitor | 101 |
| Model Registry & Promotion Pipeline | 101 |
| Semantic Cache | 102 |
| Embedding Cache | 102 |
| Cost Attribution Engine | 102 |
| End-to-End AI Request Trace | 95 |

The full task specs (problem / description / what to do) live in [§ Engineering Implementation Tasks](#engineering-implementation-tasks) below.

### Engineering Practice Exercises

Use the 30 timed drills as **Friday drills** or interview warm-ups.

| Weeks | Category |
|---:|---|
| 31–33 | Retrieval and Top-K |
| 34–35 | Rate limiting and caching |
| 36–37 | Chunking and PII |
| 38–39 | Calibration and ranking metrics |
| 40–41 | Batching and resilience |
| 42–43 | Sketches and probabilistic structures |
| 44–45 | Routing, load balancing, IDs |
| 46–57 | System design drills |
| 58–69 | Experimentation and MLOps drills |
| 70–81 | RAG/agent drills |
| 82–93 | Inference benchmarking drills |
| 94–102 | Production platform drills |

The full list of 30 exercises lives in [§ Engineering Practice Exercises](#engineering-practice-exercises) below.

### System Design Roadmap

| Source topic | Course weeks |
|---|---:|
| System design orientation | 46 |
| Delivery framework | 46 |
| Core concepts | 46–47 |
| Key technologies | 47–48 |
| URL shortener | 53 |
| Dropbox | 53 |
| Ticketmaster | 54 |
| Facebook News Feed | 54 |
| WhatsApp | 55 |
| LeetCode | 55 |
| Uber | 56 |
| Web crawler | 56 |
| Ad click aggregator | 57 |
| Payments | 57 |
| Rate limiter | 48 |
| Scaling reads | 49 |
| Scaling writes | 49 |
| Large blobs | 50 |
| Long-running tasks | 50–51 |
| Orchestration vs choreography | 51 |
| Contracts/schema evolution | 52 |
| Trade-off analysis | 57, 103 |

### ML Systems & MLOps Reading

| Source reading | Course weeks |
|---|---:|
| Business objectives and constraints | 58 |
| Labeling, weak supervision | 59 |
| Data augmentation | 59 |
| Deployment, batch vs online, compression | 60 |
| Production failures, distribution shift | 69 |
| Logging, observability, monitoring, drift | 68 |
| Data leakage, contamination detection | 60 |
| Evaluation, experiment tracking | 60 |
| Baselines, offline evaluation, slices | 61 |
| A/B testing, shadow, canary, bandits | 62 |
| Metrics trade-offs | 39, 61, 78 |
| Search architecture | 76–77 |
| Recommender systems refresher | Optional capstone |
| Requirements, trade-offs, API, data model | 46–47 |
| Scalability, latency, privacy, tenant isolation | 94–102 |
| Orchestration vs choreography | 51 |
| Contracts/schema evolution | 52 |
| Trade-off analysis method | 57 |
| Rollout strategy | 62, 94 |
| Four-layer monitoring framework | 68 |
| Live coding execution | Ongoing from 31 |
| Monitoring/MLOps interview questions | 68–69, 107 |

### LLM Inference Papers & Systems

| Source item | Course week |
|---|---:|
| Making Deep Learning Go Brrrr From First Principles | 82 |
| Transformer Inference Arithmetic | 83 |
| FlashAttention | 82 |
| FlashAttention-2/3 | 82, 92 |
| PagedAttention / vLLM | 84 |
| Inside vLLM | 85 |
| vLLM metrics | 86 |
| Prometheus/Grafana | 87 |
| Benchmarking LLM engines | 88 |
| SGLang | 89 |
| RadixAttention | 89 |
| Orca | 90 |
| Continuous batching | 90 |
| Sarathi-Serve | 90 |
| Chunked prefill | 90 |
| Quantization methods | 91 |
| KIVI / H2O / SnapKV / MInference | 91–92 |
| Speculative decoding | 92 |
| Medusa | 92 |
| EAGLE | 92 |
| StreamingLLM | 92 |
| DistServe | 93 |
| Splitwise | 93 |
| Mooncake | 93 |
| Disaggregated prefill | 93 |
| Inference economics | 93 |

The full papers table with venues and topics lives in [§ Research Papers](#research-papers).

### LLM Training, RAG, Agents & Evaluation

| Source topic | Course weeks |
|---|---:|
| Transformer/tokenizer/matmul | 70 |
| Data cleaning and deduplication | 71 |
| Tokenization pipelines | 71 |
| SFT | 72 |
| LoRA | 72 |
| QLoRA | 72 |
| DoRA | 72 |
| RLHF | 73 |
| DPO | 73 |
| ORPO | 73 |
| GRPO | 73 |
| Data parallelism | 74 |
| Tensor parallelism | 74 |
| Pipeline parallelism | 74 |
| ZeRO | 74 |
| HNSW | 75 |
| IVF & IVF-PQ | 75 |
| Product quantization | 75 |
| Hybrid search | 76 |
| Query rewriting | 76 |
| Parent-child chunking | 76 |
| Multi-vector retrieval | 76 |
| Agentic RAG | 81 |
| Embedding evaluation | 75, 78 |
| Cross-encoder rerankers | 77 |
| MMLU/GSM8K/HumanEval | 78, 105 |
| LLM-as-a-judge | 78, 105 |
| Ragas/TruLens | 78, 105 |
| Guardrails | 81, 102 |
| Prompt injection defense | 102 |
| Hallucination detection | 78, 102 |

---

## Weekly Template

```text
Week [number]: [title]

Objective:
- 

Monday:
- Math/theory:

Tuesday:
- Build:

Wednesday:
- Systems/papers/architecture:

Thursday:
- Evaluation/interview:

Friday:
- Review/docs/retrospective:

Deliverable:
- 

Evidence:
- Link to code:
- Link to notes:
- Link to results:
```

---

## Repository Layout

```text
108-week-ai-engineering-course/
  00_orientation/
  01_math/
    linear_algebra/
    numerical_linear_algebra/
    calculus/
    autodiff/
    probability/
    statistics/
  02_engineering_primitives/
    retrieval/ rate_limiting/ caching/ chunking/ pii/ metrics/
    batching/ resilience/ sketches/ routing/ ids/
  03_system_design/
    case_studies/ patterns/ writeups/
  04_ml_systems/
    experimentation/ evaluation/ monitoring/
  05_llm/
    training/ rag/ agents/ evaluation/
  06_inference/
    vllm/ sglang/ benchmarking/ quantization/
    speculative_decoding/ disaggregation/
  07_platform/
    router/ quotas/ tracing/ logging/ scheduler/ idempotency/
    work_queue/ registry/ cost/
  08_capstone/
    design/ src/ eval/ dashboards/ reports/
  09_interview/
    system_design/ coding/ behavioral/ mocks/
  journal/
    week_001.md
    week_002.md
    ...
```

---

## Interview Preparation Integration

Interview prep is **continuous**, not just at the end.

**Weekly minimums (every week):**
- 1 coding drill
- 1 system design question or pattern
- 1 behavioral story refinement
- 1 technical explanation out loud

| Weeks | Interview focus |
|---:|---|
| 1–30 | Technical communication and basic problem solving |
| 31–45 | Coding patterns and implementation drills |
| 46–57 | System design case studies |
| 58–69 | ML/MLOps/experimentation interview questions |
| 70–81 | LLM/RAG/agent system design |
| 82–93 | LLM inference and performance questions |
| 94–102 | Production AI platform design |
| 103–108 | Full mock interviews |

---

## Behavioral Interview Track (CARL Stories)

| Story type | Suggested weeks |
|---|---:|
| Scope | 1–10 |
| Ownership | 11–20 |
| Ambiguity | 21–30 |
| Perseverance | 31–40 |
| Conflict resolution | 41–50 |
| Growth | 51–60 |
| Communication | 61–70 |
| Leadership | 71–80 |
| Technical trade-offs | 81–90 |
| Production incident | 91–108 |

Use the **CARL** format — **C**ontext, **A**ction, **R**esult, **L**earning.

---

## Final Capstone Requirements

**Product** · clear user problem, defined scope, working end-to-end flow.

**Architecture** · API design, data model, retrieval/model flow, failure handling, tenant isolation.

**Evaluation** · offline metrics, online or simulated metrics, slice-based evaluation, error analysis.

**Observability** · logs, metrics, traces, dashboards, alert thresholds.

**Cost** · token usage, latency, cache hit rate, cost per request or per million tokens.

**Safety** · prompt injection defenses, PII redaction, guardrails, abuse prevention.

**Portfolio** · public repo, architecture diagram, benchmark report, demo video, design doc, interview summary.

The canonical artifact for Phase 10 lives in [`CAPSTONE.md`](./CAPSTONE.md) — a staff-level **Multi-Tenant LLM Trace Forensics with Mo's Algorithm** question that synthesizes Phases 6–9 (ingestion, immutable segments, exact slice forensics, approximation, multi-tenancy) into a single interview drill. It includes a system-design diagram, pitfalls index, pedagogical walkthrough, worked solution, and a 24-point self-grading rubric.

---

## Completion Criteria

1. Completed ≥ 90% of weekly deliverables
2. Built all major engineering primitives
3. Written ≥ 10 system design documents
4. Built an experimentation/evaluation toolkit
5. Built a RAG/agent prototype
6. Completed an LLM inference benchmark report
7. Built a production AI platform layer
8. Completed a capstone
9. Passed ≥ 3 full mock interviews
10. Published a portfolio

---

## Reference Resources

### YouTube Playlists

| Title | URL |
|---|---|
| 20 AI Concepts Explained in 40 Minutes | https://www.youtube.com/watch?v=7QisFjITGlI |
| Distilling an LLM into a 150M-parameter model \| AGI Tamer | https://www.youtube.com/watch?v=3SZSDKEZqoA |
| Learn Snowflake with ONE Project | https://www.youtube.com/watch?v=cSOTxxvqwyE |
| Airbnb End-To-End Data Engineering Project (For Beginners) \| DBT + Snowflake + AWS | https://www.youtube.com/watch?v=MdkLh1UC3IQ |
| End-to-End Hotel Booking Data Engineering Project in Snowflake | https://www.youtube.com/watch?v=DUNk4GPZ9bw |
| Statistics for Data Science (A/B Testing Interview Questions in Tech Companies) | https://www.youtube.com/watch?v=jrvY43-c_UM |
| A/B Testing in Data Science Interviews by a Google Data Scientist \| DataInterview | https://www.youtube.com/watch?v=qjKAqMSD4Vw |
| Increasing Sales through A/B Testing (with Tinder Sr. Data Science Mgr) | https://www.youtube.com/watch?v=cggcQbNC4-k |
| AI Engineer Interview Guide (2026): Questions, System Design, Coding, RAG, Portfolio | https://www.youtube.com/watch?v=2t-ls6ekA8E |
| ML System Design & MLOps For Beginners | https://www.youtube.com/watch?v=OYvlznJ4IZQ |
| Agent AI System Design Explained in 27 Minutes | https://www.youtube.com/watch?v=XVlt94Lemus |
| AI Agents Explained in 14 Minutes (The Complete Guide) | https://www.youtube.com/watch?v=ruA_EYARCNg |
| Multi-Agent AI Systems Explained: The Complete Guide | https://www.youtube.com/watch?v=mwN75EiGfCE |
| FULL Data Science Mock Interview \| SQL, Statistics, Business | https://www.youtube.com/watch?v=TZMdEg1ZoIo |
| Learn Snowflake – Full 1-Hour Crash Course for Complete Beginners | https://www.youtube.com/watch?v=-zBbij9rrEI |

### Books & Reading List

| Book | Pages | Topic |
|---|---:|---|
| Designing ML Systems | 118–132 | Labeling, natural labels, weak supervision |
| Designing ML Systems | 149–156 | Data augmentation, synthetic-to-real gaps |
| Designing ML Systems | 224–247 | Deployment, batch vs online, compression |
| Designing ML Systems | 267–290 | Production failures, distribution shift, monitoring |
| Practical MLOps | 181–204 | Logging, observability, model monitoring, drift |
| Acing System Design | 203–226 | Rate limiting, token bucket, sliding windows |
| ML Interviews | 176–189 | Live coding, thinking aloud, edge cases |
| Designing ML Systems | 174–180 | Data leakage, contamination detection |
| Designing ML Systems | 182–195 | Evaluation, experiment tracking, versioning |
| Designing ML Systems | 203–217 | Baselines, offline evaluation, slices, CIs |
| Designing ML Systems | 316–325 | A/B testing, shadow deployment, canary, bandits |
| ML Interviews | 163–170 | Metrics — Recall@K, MRR, NDCG trade-offs |
| Acing System Design | 277–296 | Search architecture, candidate generation, freshness |
| ML Interviews | 117–122 | Recommender systems refresher |
| Acing System Design | 56–79 | Requirements, trade-offs, API, data model, observability |
| Acing System Design | 86–107 | Scalability, latency, privacy, tenant isolation |
| Designing ML Systems | 52–76 | Business objectives, constraints, iterative development |
| Software Architecture | 317–339 | Orchestration vs choreography, workflow state ownership |
| Software Architecture | 383–397 | Contracts, schema evolution, backward compatibility |
| Software Architecture | 417–433 | Trade-off analysis, MECE reasoning, bottom line over evidence |
| Designing ML Systems | 316–325 | Rollout strategy, canary, interleaving experiments |
| System Design | 191–195 | Interview method checklist — read night before |
| Designing ML Systems | 52–76 | Objectives and constraints |
| Designing ML Systems | 203–217 | Baselines and offline evaluation |
| Designing ML Systems | 267–290 | Production monitoring |
| Designing ML Systems | 316–325 | A/B testing and rollout |
| Acing System Design | 56–79 | Design interview flow |
| Acing System Design | 203–226 | Rate limiting system design |
| Software Architecture | 317–339 | Orchestration vs choreography |
| Software Architecture | 417–433 | Trade-off analysis method |
| Practical MLOps | 181–204 | Four-layer monitoring framework |
| ML Interviews | 176–189 | Live coding execution |
| ML Interviews | 222–239 | Monitoring, MLOps, system design questions |

### Research Papers

| Paper | Venue | Topic | URL |
|---|---|---|---|
| PagedAttention / vLLM | SOSP 2023 | KV cache paging | https://arxiv.org/abs/2309.06180 |
| Orca | OSDI 2022 | Continuous batching | https://www.usenix.org/conference/osdi22/presentation/yu |
| SGLang | NeurIPS 2024 | RadixAttention, prefix reuse | https://arxiv.org/abs/2312.07104 |
| SARATHI / Sarathi-Serve | OSDI 2024 | Chunked prefill | https://arxiv.org/abs/2308.16369 |
| DistServe | OSDI 2024 | Prefill/decode disaggregation | https://arxiv.org/abs/2403.02310 |
| Splitwise | ISCA 2024 | Phase splitting across GPU types | https://www.usenix.org/conference/osdi24/presentation/zhong-yinmin |
| Mooncake | FAST 2025 | KV-cache-centric serving | https://arxiv.org/abs/2311.18677 |
| StreamingLLM | ICLR 2024 | Attention sinks, long context | https://arxiv.org/abs/2407.00079 |
| EAGLE | arXiv | Speculative sampling | https://arxiv.org/abs/2309.17453 |
| FlashAttention | NeurIPS 2022 | IO-aware attention | https://arxiv.org/abs/2401.15077 |
| FlashAttention-2 | ICLR 2024 | Faster attention kernels | — |
| FlashAttention-3 | — | Hopper-optimized attention | — |
| Ring Attention | ICLR 2024 | Long-context distributed attention | — |
| Infini-attention | NeurIPS 2024 | Infinite context | — |
| KIVI | ICML 2024 | KV cache quantization | — |
| H2O | NeurIPS 2023 | Heavy hitter KV eviction | — |
| SnapKV | NeurIPS 2024 | KV cache compression | — |
| MInference | NeurIPS 2024 | Dynamic sparse attention | — |
| Medusa | ICML 2024 | Multi-head speculative decoding | — |
| SpecInfer | SIGMOD 2024 | Speculative inference | — |
| Lookahead Decoding | ACL 2024 | Faster decoding | — |
| TensorRT-LLM | NVIDIA | Production inference optimization | — |
| DeepSpeed-Inference | Microsoft | High-performance inference | — |
| FasterTransformer | NVIDIA | Transformer inference | — |
| Megatron-LM | SC 2019 | Large-scale transformer training | — |
| DeepSpeed | KDD 2020 | ZeRO optimizer | — |
| ZeRO | SC 2020 | Optimizer state partitioning | — |
| ZeRO-Infinity | SC 2021 | Extreme-scale training | — |
| FSDP | PyTorch | Fully Sharded Data Parallel | — |
| Switch Transformer | JMLR | Mixture of Experts | — |
| GShard | ICLR 2021 | Sparse expert scaling | — |
| DeepSeekMoE | arXiv | Modern MoE architecture | — |
| LoRA | ICLR 2022 | Parameter-efficient fine-tuning | — |
| QLoRA | NeurIPS 2023 | 4-bit fine-tuning | — |
| DoRA | ICML 2024 | Weight decomposition tuning | — |
| RLHF | NeurIPS 2022 | Human feedback alignment | — |
| Direct Preference Optimization (DPO) | NeurIPS 2023 | Preference optimization | — |
| ORPO | ICLR 2024 | Odds-ratio preference optimization | — |
| ColBERT | SIGIR 2020 | Late interaction retrieval | — |
| ColBERTv2 | NAACL 2022 | Efficient retrieval | — |
| HyDE | ACL 2023 | Hypothetical document retrieval | — |
| RAPTOR | arXiv 2024 | Hierarchical RAG | — |
| GraphRAG | Microsoft | Graph retrieval | — |
| Self-RAG | ICLR 2024 | Self-reflective retrieval | — |
| CRAG | NeurIPS 2024 | Corrective retrieval augmentation | — |

### Blog & Article URLs

The following blogs/articles are referenced in the course (especially in the inference performance weeks):

- The shift to distributed LLM inference — https://www.bentoml.com/blog/the-shift-to-distributed-llm-inference
- Collective operations — http://www.aleksagordic.com/blog/collective-operations
- ELI5 FlashAttention — https://gordicaleksa.medium.com/eli5-flash-attention-5c44017022ad
- vLLM (Aleksa Gordić) — https://www.aleksagordic.com/blog/vllm
- Matmul — https://www.aleksagordic.com/blog/matmul
- Transformer — https://www.aleksagordic.com/blog/transformer
- Making Deep Learning Go Brrrr From First Principles (Horace He) — https://horace.io/brrr_intro.html
- Stanford CS336 Spring 2025 lectures — https://github.com/stanford-cs336/spring2025-lectures
- GPU MODE Lecture 22 (Hacker's Guide to Speculative Decoding) — https://www.youtube.com/watch?v=6OBtO9niT00
- Transformer Inference Arithmetic (kipply) — https://kipp.ly/transformer-inference-arithmetic/
- CS336 Lecture 5 (Percy Liang, Tatsunori Hashimoto) — https://www.youtube.com/watch?v=fcgPYo3OtV0
- Databricks — LLM Inference Performance Engineering — https://www.databricks.com/blog/llm-inference-performance-engineering-best-practices
- PagedAttention announcement — https://blog.vllm.ai/2023/06/20/vllm.html
- PagedAttention paper (arXiv) — https://arxiv.org/abs/2309.06180
- vLLM on Modal — https://modal.com/docs/examples/vllm_inference
- vLLM Office Hours 22: Intro to vLLM V1 — https://www.youtube.com/watch?v=jmzIvQZCLZM
- vLLM V1 architecture — https://blog.vllm.ai/2025/01/27/v1-alpha-release.html
- Anatomy of a High-Throughput Inference System — https://blog.vllm.ai/2025/09/05/anatomy-of-vllm.html
- vLLM repo — https://github.com/vllm-project/vllm
- vLLM V1 metrics design doc — https://docs.vllm.ai/en/latest/design/v1/metrics/
- Prometheus/Grafana example — https://docs.vllm.ai/en/latest/examples/online_serving/prometheus_grafana/
- NVIDIA benchmarking fundamentals — https://developer.nvidia.com/blog/llm-inference-benchmarking-fundamental-concepts/
- How to Benchmark LLM Engines (Modal) — https://modal.com/llm-almanac/how-to-benchmark
- GuideLLM intro talk — https://www.youtube.com/watch?v=0ZVu0A4wWQg
- GuideLLM repo — https://github.com/vllm-project/guidellm
- vLLM bench serve CLI — https://docs.vllm.ai/en/latest/benchmarking/cli/
- Triton perf_analyzer — https://github.com/triton-inference-server/perf_analyzer
- Practical strategies for vLLM performance tuning — https://developers.redhat.com/articles/2026/03/03/practical-strategies-vllm-performance-tuning
- Lilian Weng — Inference Optimization survey — https://lilianweng.github.io/posts/2023-01-10-inference-optimization/
- vLLM quantization docs — https://docs.vllm.ai/en/latest/features/quantization/
- QLoRA talk (Tim Dettmers) — https://www.youtube.com/watch?v=9wNAgpX6z_4
- vLLM production stack — https://github.com/vllm-project/production-stack
- How to set up KServe autoscaling for vLLM with KEDA — https://developers.redhat.com/articles/2025/09/23/how-set-kserve-autoscaling-vllm-keda
- LLM Inference Economics from First Principles — https://www.tensoreconomics.com/p/llm-inference-economics-from-first
- DigitalOcean — LLM Inference Cost — https://www.digitalocean.com/community/tutorials/llm-inference-cost
- Character.AI — Optimizing AI Inference — https://blog.character.ai/optimizing-ai-inference-at-character-ai-2/
- NVIDIA — Mastering LLM Techniques: Inference Optimization — https://developer.nvidia.com/blog/mastering-llm-techniques-inference-optimization/
- SGLang intro (Lianmin Zheng) — https://www.youtube.com/watch?v=Ny4xxErgFgQ
- SGLang NeurIPS 2024 paper — https://arxiv.org/abs/2312.07104
- SGLang v0.4 zero-overhead scheduler — https://lmsys.org/blog/2024-12-04-sglang-v0-4/
- RadixAttention / SGLang blog — https://lmsys.org/blog/2024-01-17-sglang/
- SGLang docs — https://docs.sglang.io

### Mathematics Curriculum Path

100 learning modules across 28 areas. **Category = Learning Module** for nearly all entries unless otherwise noted.

| # | Step | Order / Topic | Category | Item |
|---:|---|---|---|---|
| 1 | Linear Algebra | Vector Spaces, Subspaces, Span, Basis & Dimension | Learning Module | Derive + Solve Problems |
| 2 | Linear Algebra | Linear Independence, Rank & Nullity | Learning Module | Prove + Solve Problems |
| 3 | Linear Algebra | Inner Products, Norms & Dual Norms | Learning Module | Derive + Implement |
| 4 | Linear Algebra | Orthogonality, Projections & Gram-Schmidt | Learning Module | Derive + Implement |
| 5 | Linear Algebra | Linear Transformations, Change of Basis & Coordinate Systems | Learning Module | Derive + Solve Problems |
| 6 | Linear Algebra | Eigenvalues, Eigenvectors & Diagonalization | Learning Module | Derive + Implement |
| 7 | Linear Algebra | Positive Semidefinite Matrices, Quadratic Forms & Rayleigh Quotients | Learning Module | Prove + Implement |
| 8 | Linear Algebra | Singular Value Decomposition, Pseudoinverse & Low-Rank Approximation | Learning Module | Derive + Implement |
| 9 | Numerical Linear Algebra | Matrix Norms, Operator Norms & Spectral Radius | Learning Module | Derive + Compute |
| 10 | Numerical Linear Algebra | Condition Numbers & Perturbation Analysis | Learning Module | Derive + Experiment |
| 11 | Numerical Linear Algebra | LU, QR & Cholesky Decomposition | Learning Module | Implement from Scratch |
| 12 | Numerical Linear Algebra | Iterative Linear Solvers: Jacobi, Gauss-Seidel, Conjugate Gradient & GMRES | Learning Module | Implement + Benchmark |
| 13 | Numerical Linear Algebra | Power Iteration, Lanczos Method & Krylov Subspaces | Learning Module | Derive + Implement |
| 14 | Numerical Linear Algebra | Randomized SVD & Randomized Matrix Approximation | Learning Module | Derive + Implement |
| 15 | Numerical Linear Algebra | Tensor Products, Tensor Contractions & Einstein Notation | Learning Module | Derive + Implement |
| 16 | Calculus | Partial Derivatives, Gradients & Directional Derivatives | Learning Module | Derive + Solve Problems |
| 17 | Calculus | Jacobian Matrices & Vector-Valued Differentiation | Learning Module | Derive + Implement |
| 18 | Calculus | Hessian Matrices, Curvature & Second-Order Approximations | Learning Module | Derive + Visualize |
| 19 | Calculus | Multivariable Taylor Series & Local Error Analysis | Learning Module | Derive + Apply |
| 20 | Calculus | Chain Rule on Computational Graphs | Learning Module | Derive Backpropagation |
| 21 | Automatic Differentiation | Forward Mode, Reverse Mode, JVPs & VJPs | Learning Module | Implement from Scratch |
| 22 | Automatic Differentiation | Differentiating Softmax, Normalization, Attention & Cross-Entropy | Learning Module | Derive + Verify Numerically |
| 23 | Optimization | Convex Sets, Convex Functions & Epigraphs | Learning Module | Prove + Solve Problems |
| 24 | Optimization | Smoothness, Lipschitz Continuity & Strong Convexity | Learning Module | Derive Convergence Bounds |
| 25 | Optimization | Gradient Descent & Convergence Rates | Learning Module | Derive + Implement |
| 26 | Optimization | Stochastic Gradient Descent, Gradient Noise & Learning-Rate Schedules | Learning Module | Derive + Experiment |
| 27 | Optimization | Momentum, Nesterov Acceleration, AdaGrad, RMSProp & Adam | Learning Module | Derive + Implement |
| 28 | Optimization | Proximal Methods, Mirror Descent & Natural Gradient | Learning Module | Derive + Implement |
| 29 | Optimization | Newton's Method, Quasi-Newton (BFGS) & Trust Regions | Learning Module | Derive + Implement |
| 30 | Optimization | Constrained Optimization & KKT Conditions | Learning Module | Prove + Solve Problems |
| 31 | Probability | Probability Spaces, σ-Algebras & Measure-Theoretic Foundations | Learning Module | Prove + Compute |
| 32 | Probability | Conditional Probability, Independence & Bayes Theorem | Learning Module | Solve Problems |
| 33 | Probability | Discrete & Continuous Random Variables, PMFs, PDFs, CDFs | Learning Module | Implement + Sample |
| 34 | Probability | Common Distributions (Bernoulli, Binomial, Poisson, Gaussian, Exponential, Beta, Dirichlet) | Learning Module | Derive + Sample |
| 35 | Probability | Joint, Marginal & Conditional Distributions; Law of Total Probability | Learning Module | Solve Problems |
| 36 | Probability | Expectation, Variance, Covariance & Correlation | Learning Module | Derive + Compute |
| 37 | Probability | Transformations of Random Variables & Jacobian Method | Learning Module | Derive + Implement |
| 38 | Probability | Convergence Theorems: LLN, CLT & Delta Method | Learning Module | Simulate + Verify |
| 39 | Statistics | MLE, MAP, Method of Moments & Estimator Properties | Learning Module | Derive + Compare |
| 40 | Statistics | Bias–Variance Tradeoff & Mean Squared Error Decomposition | Learning Module | Derive + Experiment |
| 41 | Statistics | Hypothesis Testing, p-Values, Type I/II Errors & Power | Learning Module | Implement Tests |
| 42 | Statistics | Confidence Intervals & Bootstrap Resampling | Learning Module | Implement Bootstrap CI |
| 43 | Statistics | Permutation Tests, Jackknife & Cross-Validation | Learning Module | Implement + Compare |
| 44 | Statistics | Sample-Size Calculation, MDE & Power Analysis | Learning Module | Build Calculator |
| 45 | Statistics | Bayesian Inference: Priors, Posteriors, Conjugacy & Credible Intervals | Learning Module | Derive + Sample |
| 46 | Statistics | Multiple Testing, FDR & Bonferroni/BH Correction | Learning Module | Implement + Analyze |
| 47 | Statistics | Causal Inference Basics: Confounding, Treatment Effects, ATE | Learning Module | Apply to Examples |
| 48 | Statistics | Nonparametric Methods: KDE, Rank Tests, Spearman | Learning Module | Implement + Apply |
| 49 | Experimentation | Experimental Design Principles & A/B Test Pitfalls | Learning Module | Design + Audit |
| 50 | Information Theory | Entropy, Conditional Entropy, Joint Entropy & Chain Rule | Learning Module | Derive + Compute |
| 51 | Information Theory | Mutual Information, KL Divergence & Jensen–Shannon Divergence | Learning Module | Derive + Compute |
| 52 | Information Theory | Cross-Entropy Loss & Maximum Likelihood Equivalence | Learning Module | Derive + Implement |
| 53 | Information Theory | Differential Entropy & KL for Continuous Distributions | Learning Module | Derive + Compute |
| 54 | Information Theory | Source Coding Theorem, Huffman Coding & Compression | Learning Module | Implement + Analyze |
| 55 | Information Theory | Channel Capacity, Noisy-Channel Coding Theorem | Learning Module | Derive + Explain |
| 56 | Information Geometry | Fisher Information Metric & Natural Gradients | Learning Module | Derive + Apply |
| 57 | Stochastic Processes | Markov Chains: Transition Matrices, Stationary Distributions | Learning Module | Simulate + Analyze |
| 58 | Stochastic Processes | Poisson Processes & Birth–Death Processes | Learning Module | Simulate + Derive |
| 59 | Stochastic Processes | Brownian Motion, Martingales & Optional Stopping | Learning Module | Derive + Simulate |
| 60 | Queueing Theory | M/M/1, M/M/c, M/G/1 Queues & Little's Law | Learning Module | Derive + Simulate |
| 61 | Queueing Theory | Network of Queues, Jackson Networks & Product Form | Learning Module | Simulate + Analyze |
| 62 | Queueing Theory | Tail Probabilities, Heavy-Tailed Service Times & Hurst Exponent | Learning Module | Simulate + Analyze |
| 63 | Queueing Theory | Tail-at-Scale, Hedged Requests & Tied Requests | Learning Module | Simulate + Analyze |
| 64 | Queueing Theory | G/G/1 Approximations & Operational Laws | Learning Module | Derive + Apply |
| 65 | High-Dimensional Geometry | Curse of Dimensionality & Concentration of Measure | Learning Module | Derive + Visualize |
| 66 | High-Dimensional Geometry | Johnson–Lindenstrauss Lemma & Random Projections | Learning Module | Prove + Implement |
| 67 | Randomized Algorithms | Reservoir Sampling, MinHash & SimHash | Learning Module | Implement + Analyze |
| 68 | Randomized Algorithms | Locality-Sensitive Hashing (LSH) Families | Learning Module | Derive + Implement |
| 69 | Streaming Mathematics | Count-Min Sketch & Bloom Filter Variants | Learning Module | Implement + Analyze |
| 70 | Streaming Mathematics | HyperLogLog & Cardinality Estimation | Learning Module | Implement + Analyze |
| 71 | Streaming Mathematics | Approximate Quantiles (GK, t-digest) & Sliding-Window Aggregates | Learning Module | Implement + Compare |
| 72 | Graph Theory | Graph Representations, BFS/DFS, Topological Sort | Learning Module | Implement + Apply |
| 73 | Graph Theory | Shortest Paths: Dijkstra, Bellman–Ford, Floyd–Warshall | Learning Module | Implement + Compare |
| 74 | Graph Theory | Minimum Spanning Tree, Cuts & Flows | Learning Module | Implement + Apply |
| 75 | Spectral Graph Theory | Laplacian Eigenmaps, Spectral Clustering & Graph Cuts | Learning Module | Derive + Implement |
| 76 | Spectral Graph Theory | Random Walks, PageRank & Personalized PageRank | Learning Module | Derive + Implement |
| 77 | Combinatorial Optimization | Matching, Covering, Set Packing & Knapsack Variants | Learning Module | Solve + Analyze |
| 78 | Discrete Optimization | Integer Programming, Branch & Bound, Cutting Planes | Learning Module | Solve + Analyze |
| 79 | Statistical Learning Theory | PAC Learning, VC Dimension & Sample Complexity Bounds | Learning Module | Prove + Analyze |
| 80 | Statistical Learning Theory | Bias–Variance, Double Descent & Overparameterization | Learning Module | Derive + Experiment |
| 81 | Statistical Learning Theory | Rademacher Complexity & Uniform Convergence | Learning Module | Derive + Analyze |
| 82 | Statistical Learning Theory | Generalization Bounds for Neural Networks | Learning Module | Derive + Analyze |
| 83 | Statistical Learning Theory | Implicit Regularization, Flat Minima & Generalization | Learning Module | Derive + Analyze |
| 84 | Statistical Learning Theory | Information-Theoretic Generalization Bounds | Learning Module | Derive + Analyze |
| 85 | Learning to Rank | Pairwise, Listwise & LambdaMART | Learning Module | Derive + Implement |
| 86 | Online Learning | Multi-Armed Bandits: UCB, Thompson Sampling | Learning Module | Derive + Implement |
| 87 | Bayesian Methods | Bayesian Linear/Logistic Regression & Gaussian Processes | Learning Module | Derive + Implement |
| 88 | Bayesian Methods | Variational Inference & Mean-Field Approximations | Learning Module | Derive + Implement |
| 89 | Latent Variable Models | EM Algorithm & Mixture Models | Learning Module | Derive + Implement |
| 90 | Monte Carlo | Importance Sampling, Rejection Sampling & MCMC Basics | Learning Module | Derive + Implement |
| 91 | Monte Carlo | Metropolis–Hastings & Gibbs Sampling | Learning Module | Derive + Implement |
| 92 | Monte Carlo | Hamiltonian Monte Carlo & NUTS | Learning Module | Derive + Implement |
| 93 | Variational Inference | ELBO, Reparameterization Trick & VAEs | Learning Module | Derive + Implement |
| 94 | Bayesian Optimization | Gaussian Processes for Hyperparameter Tuning | Learning Module | Derive + Implement |
| 95 | Distributed Systems Mathematics | Vector Clocks, Lamport Timestamps & Causal Ordering | Learning Module | Implement + Analyze |
| 96 | Distributed Systems Mathematics | Quorum Systems, Majority Agreement & Paxos Intuition | Learning Module | Implement + Analyze |
| 97 | Distributed Systems Mathematics | Consistent Hashing, Rendezvous Hashing & Virtual Nodes | Learning Module | Implement + Analyze |
| 98 | Distributed Systems Mathematics | Gossip Protocols, Epidemic Spreading & Membership | Learning Module | Implement + Analyze |
| 99 | Distributed Systems Mathematics | Semilattices, Monotonicity & CRDT Convergence | Learning Module | Prove + Implement |
| 100 | Distributed Systems Mathematics | Consensus Safety, Liveness, Failure Models & Byzantine Thresholds | Learning Module | Study Proofs + Explain |

### Engineering Implementation Tasks

30 production-style implementation tasks, each with a problem statement, full description, and detailed "what to do" prompt.

| # | Problem | What to Do (Summary) |
|---:|---|---|
| 1 | A/B Test Significance Calculator | Implement `analyze_ab_test(control_success, control_total, treatment_success, treatment_total)`. Compute rates, absolute/relative lift, pooled SE, z-score, p-value, 95% CI. Discuss MDE, power, guardrail metrics (latency, error rate). |
| 2 | Bootstrap Confidence Interval | Implement `bootstrap_ci(values, metric_fn, n_bootstrap, confidence, seed)`. Sample with replacement, compute metric, return percentile bounds. Extend to **paired bootstrap** for model A vs B on the same queries. Discuss query-level vs document-level resampling. |
| 3 | Sample-Ratio Mismatch Detector | Implement `detect_srm(observed_counts, expected_proportions)`. Validate proportions sum to 1; compute expected counts and chi-square statistic + p-value. Discuss slicing by tenant/platform/geography to locate the routing defect. |
| 4 | Tool-Call Dependency Scheduler | Model workflow as a DAG. Use adjacency lists + indegrees (Course Schedule/topological sort). Zero-indegree tasks → ready queue, execute each layer concurrently. Detect cycles. Add timeouts, retries, failure propagation, cancellation, deterministic output ordering. Explain orchestration vs choreography. |
| 5 | Idempotent Request Deduplicator | Implement `execute_once(idempotency_key, operation)` with IN_PROGRESS / SUCCEEDED / FAILED states + cached results + expiry. Concurrency via lock or atomic CAS. Discuss TTL, payload hashing, crash recovery, Redis SET NX, DB uniqueness constraints. |
| 6 | Per-Tenant Concurrency Limiter | Async limiter using one `asyncio.Semaphore` per tenant. Provide `async with limiter.acquire(tenant_id)`. Validate limits, release in finally, remove idle state. Add a global limit. Discuss fairness, backpressure, cancellation, noisy-neighbor protection, distributed coordination via Redis/gateway. |
| 7 | Model-Version Traffic Router | Implement `route(request, tenant_id, experiment_config)` using stable hash of tenant/user ID. Support percentage rollouts, allowlists, tenant overrides, shadow execution, kill switch. Record chosen version + experiment assignment. Discuss guardrails (p95 latency, errors, cost, quality) and rollback thresholds. Never use Python's process-randomized `hash()`. |
| 8 | Structured Logger With PII Redaction | Implement `safe_log(event_name, payload, redaction_rules)`. Recursive traversal of dicts/lists. Redact sensitive keys + pattern-based masking on strings. Preserve useful metadata (length, type, hash, trace ID). Handle cycles/excessive nesting. Don't mutate input. Discuss allowlist vs denylist logging, secret rotation, Unicode, structured JSON logs, why raw prompts shouldn't be logged by default. |
| 9 | Retrieval Evaluation by Query Slice | Input: query_id, slice fields, ranked doc IDs, relevant IDs. Implement Recall@K, MRR, NDCG@K per query, macro-average globally + per slice. Return sample counts (avoid over-interpreting tiny slices). Handle queries with no labeled relevant docs. Add paired bootstrap CIs for A vs B; identify slices with statistically meaningful regressions. |
| 10 | Async Fan-Out With Partial Failures | Implement `async fan_out(calls, timeout, max_concurrency)` using `asyncio.gather(..., return_exceptions=True)` or TaskGroup + semaphore + per-call timeout. Preserve mapping from task name → result. Classify failures as retryable vs permanent. Cancel unnecessary tasks when satisfactory result is reached. Discuss retries with jitter, circuit breakers, deadlines, tracing, aggregation when sources disagree. |
| 11 | Feature Flag Evaluation Engine | Implement `evaluate_flag(user, tenant, rules)`. Support percentage rollout, allowlists, prerequisites, rule precedence, sticky assignment, defaults. Discuss evaluation order, caching, consistency, auditability. |
| 12 | Distributed Token Budget Manager | Implement `reserve_tokens(tenant, estimated_tokens)`. Support reservation, refund unused tokens, per-minute/day quotas, burst limits, concurrency safety, distributed coordination. |
| 13 | Prompt Template Renderer | Build a template engine supporting variables, conditionals, loops, escaping, validation of missing placeholders. Prevent prompt injection via variable escaping. |
| 14 | Context Window Optimizer | Given conversation history + token budget, choose messages to keep using recency, importance, summarization. Handle hard token limits + pinned messages. |
| 15 | Embedding Cache | LRU + TTL cache keyed by normalized text + model version. Handle cache invalidation, model upgrades, concurrent requests. |
| 16 | Prompt Injection Detector | Build a detector using regex + heuristics + scoring. Detect "ignore previous instructions", data exfiltration, jailbreaks, suspicious URLs. Return risk score + reasons. |
| 17 | Conversation Memory Store | Implement memory CRUD with semantic retrieval, recency weighting, expiration, tenant isolation. Discuss summarization and forgetting policies. |
| 18 | Retrieval Fusion Engine | Merge BM25, dense retrieval, metadata filters, reranker outputs using Reciprocal Rank Fusion. Handle duplicates + score normalization. |
| 19 | Streaming Response Multiplexer | Merge multiple async token streams preserving ordering, cancellation, heartbeats, client disconnect handling. |
| 20 | Prompt Version Registry | Store prompt versions with metadata, rollback support, A/B variants, approvals, model-version compatibility. |
| 21 | Distributed Work Queue | Implement enqueue/dequeue with leases, retries, dead-letter queues, visibility timeout, idempotency. |
| 22 | Model Health Monitor | Continuously aggregate latency, errors, token usage, hallucination rate, quality metrics. Trigger alerts using rolling windows. |
| 23 | Semantic Cache | Cache responses by embedding similarity. Configurable threshold, eviction, freshness, model-version awareness. |
| 24 | Experiment Assignment Service | Assign users deterministically to experiments with mutually exclusive experiments, namespaces, overrides, audit logging. |
| 25 | Distributed Leader Election | Simulate lease-based leader election with heartbeat renewal, failover, split-brain prevention, fencing tokens. |
| 26 | API Gateway Request Prioritizer | Prioritize premium tenants, interactive traffic, retries using weighted queues + admission control. |
| 27 | Cost Attribution Engine | Aggregate token usage, embeddings, tool calls, GPU time into per-tenant cost reports. Handle retries and shared requests correctly. |
| 28 | Model Registry & Promotion Pipeline | Implement model registration, stage transitions (Dev → Staging → Production), approval workflow, rollback, lineage tracking. |
| 29 | Distributed Configuration Service | Strongly-versioned config retrieval with watches, caching, rollback, consistency guarantees. |
| 30 | End-to-End AI Request Trace | Correlate inference, retrieval, tool calls, prompts, downstream services via trace IDs. Generate execution timeline + latency breakdown. |

### Engineering Practice Exercises

30 timed drills (10–30 min each) covering retrieval, rate limiting, caching, chunking, PII, calibration, ranking metrics, batching, resilience, sketches, routing, retrieval primitives, and more.

| # | Problem | Core Pattern | Target |
|---:|---|---|---|
| 1 | Cosine similarity from scratch | NumPy / vector math | 10 min |
| 2 | Exact KNN from scratch | Top-K + vectorization | 15 min |
| 3 | Memory-bounded KNN | Chunking + heap | 20 min |
| 4 | Streaming Top-K | Min-heap | 10 min |
| 5 | Top-K with dynamic score updates | Heap + lazy deletion | 20 min |
| 6 | Two-stage retrieval and reranking | Heap / partial sorting | 20 min |
| 7 | Per-tenant sliding-window rate limiter | Hash map + deque | 15 min |
| 8 | Token bucket rate limiter | Time arithmetic + state | 15 min |
| 9 | LRU cache | Hash map + doubly linked list | 20 min |
| 10 | LRU cache with TTL | LRU + expiration | 25 min |
| 11 | Token-aware text chunking | Sliding window | 15 min |
| 12 | Sentence-aware recursive chunking | Greedy splitting | 25 min |
| 13 | Merge overlapping PII spans | Interval merging | 15 min |
| 14 | Regex + NER PII detector | Span resolution + scoring | 25 min |
| 15 | Expected Calibration Error | Binning + NumPy | 15 min |
| 16 | Brier score and reliability data | Statistics + aggregation | 15 min |
| 17 | NDCG, MRR and Recall@K | Ranking metrics | 20 min |
| 18 | Thread-safe inference batcher | Queue + condition variable | 30 min |
| 19 | Retry with exponential backoff and jitter | State + timing | 15 min |
| 20 | Circuit breaker | State machine | 20 min |
| 21 | Count-Min Sketch | Streaming data structures | 20 min |
| 22 | Bloom Filter | Probabilistic data structures | 15 min |
| 23 | HyperLogLog | Cardinality estimation | 25 min |
| 24 | Consistent Hash Ring | Distributed systems | 20 min |
| 25 | Weighted Round Robin Load Balancer | Scheduling | 20 min |
| 26 | Rendezvous (Highest Random Weight) Hashing | Distributed routing | 25 min |
| 27 | Distributed Unique ID Generator (Snowflake) | ID generation | 20 min |
| 28 | Leaky Bucket Rate Limiter | Traffic shaping | 15 min |
| 29 | Sliding Window Counter Rate Limiter | Time-series aggregation | 20 min |
| 30 | Weighted Fair Queue Scheduler | Scheduling algorithms | 30 min |
| 31 | Prefix Trie with Autocomplete | Trie + ranking | 20 min |
| 32 | Inverted Index Builder | Information retrieval | 25 min |
| 33 | BM25 Scoring from Scratch | Search ranking | 30 min |
| 34 | SimHash Near-Duplicate Detection | Hashing | 25 min |
| 35 | MinHash & Jaccard Estimation | Locality-sensitive hashing | 30 min |
| 36 | Approximate Quantile Estimator (GK / t-digest concept) | Streaming statistics | 30 min |
| 37 | Reservoir Sampling | Streaming algorithms | 20 min |
| 38 | Producer–Consumer Queue | Concurrency | 20 min |
| 39 | Thread Pool Executor | Concurrency primitives | 30 min |
| 40 | Async Task Scheduler with Priority Queue | Scheduling + heap | 30 min |

### Interview Preparation Roadmap

176 items across 6 main tracks (System Design, Coding, Behavioral) and many sub-tracks (LLM Serving, AI Agents, Multimodal AI, ML System Design, AI Engineering, MLOps, etc.). Each item includes a Step, an Item title, a Type (Article / Lesson / Reading / Practice / Topic / etc.), and a Completion Rule.

#### System Design (28 items)

| Step | Item | Type | Completion |
|---|---|---|---|
| Reading | What is the system design interview? | Article | Read |
| Reading | How to prepare for system design interviews | Article | Read |
| Learning | Learn the delivery framework | Lesson | Complete |
| Concepts | Study core system design concepts | Lesson | Complete |
| Technologies | Learn key technologies | Lesson | Complete |
| Problems | Top 10 Common Problems | Reading | Read |
| Case Study | Design a URL Shortener | Design Exercise | Complete |
| Case Study | Design Dropbox | Design Exercise | Complete |
| Case Study | Design Ticketmaster | Design Exercise | Complete |
| Case Study | Design FB News Feed | Design Exercise | Complete |
| Case Study | Design WhatsApp | Design Exercise | Complete |
| Case Study | Design LeetCode | Design Exercise | Complete |
| Case Study | Design Uber | Design Exercise | Complete |
| Case Study | Design a Web Crawler | Design Exercise | Complete |
| Case Study | Design an Ad Click Aggregator | Design Exercise | Complete |
| Case Study | Design Facebook's Post Search | Design Exercise | Complete |
| Pattern | Real-time Updates | Pattern | Complete |
| Pattern | Dealing with Contention | Pattern | Complete |
| Pattern | Multi-step Processes | Pattern | Complete |
| Pattern | Scaling Reads | Pattern | Complete |
| Pattern | Scaling Writes | Pattern | Complete |
| Pattern | Handling Large Blobs | Pattern | Complete |
| Pattern | Managing Long Running Tasks | Pattern | Complete |
| Practice | Complete 3 easy guided practices | Milestone | 3 Completed |
| Practice | Complete 3 medium guided practices | Milestone | 3 Completed |
| Practice | Complete 2 hard guided practices | Milestone | 2 Completed |
| Practice | Complete 3 easy guided practices | Milestone | 3 Completed |

#### Coding (20 items)

| Step | Item | Type | Completion |
|---|---|---|---|
| Algorithm | Two Pointers | Topic | Complete |
| Algorithm | Sliding Window | Topic | Complete |
| Algorithm | Intervals | Topic | Complete |
| Algorithm | Stack | Topic | Complete |
| Algorithm | Linked List | Topic | Complete |
| Algorithm | Binary Search | Topic | Complete |
| Algorithm | Heap | Topic | Complete |
| Algorithm | Depth-First Search | Topic | Complete |
| Algorithm | Breadth-First Search | Topic | Complete |
| Algorithm | Backtracking | Topic | Complete |
| Algorithm | Graphs | Topic | Complete |
| Algorithm | Dynamic Programming | Topic | Complete |
| Algorithm | Greedy Algorithms | Topic | Complete |
| Algorithm | Trie | Topic | Complete |
| Algorithm | Prefix Sum | Topic | Complete |
| Algorithm | Matrices | Topic | Complete |
| Practice | Grind75 | Question Set | Complete |
| Practice | 50+ Company Tagged Questions | Question Set | 50 Completed |
| Mock | Blank Editor + Think Aloud | Practice | 5–7 Sessions |

#### Behavioral (15 items)

| Step | Item | Type | Completion |
|---|---|---|---|
| Reading | Why the behavioral interview matters | Article | Read |
| Reading | Decode what questions are really asking | Article | Read |
| Story | Scope | Story | Prepared |
| Story | Ownership | Story | Prepared |
| Story | Ambiguity | Story | Prepared |
| Story | Perseverance | Story | Prepared |
| Story | Conflict resolution | Story | Prepared |
| Story | Growth | Story | Prepared |
| Story | Communication | Story | Prepared |
| Story | Leadership | Story | Prepared |
| Story | Technical trade-offs | Story | Prepared |
| Story | Production incident | Story | Prepared |
| Mock | Mock interview #1 | Mock Interview | 1 Completed |
| Mock | Mock interview #2 | Mock Interview | 1 Completed |
| Mock | Mock interview #3 | Mock Interview | 1 Completed |

#### Additional Specialized Tracks

The roadmap also contains curated tracks for **ML System Design**, **AI Engineering**, **LLM Inference / Serving**, **AI Agents**, **Multimodal AI**, **Classical ML**, **Production ML**, and **Snowflake / Data Engineering**. Sample highlights:

**LLM Inference & Serving:**
- PagedAttention, Continuous Batching, RadixAttention, Prefix Caching, Speculative Decoding, AWQ, GPTQ, GGUF, Quantization Trade-offs & Benchmarking — each as a Learning Module marked "Complete".

**Vector Databases & Retrieval:**
- HNSW, IVF & IVF-PQ, Product Quantization, Hybrid Search (BM25 + Dense), Query Rewriting, Parent-Child Chunking, Multi-Vector Retrieval, Agentic RAG, Cross-Encoder Rerankers, Embedding Evaluation.

**Alignment & Fine-Tuning:**
- Reinforcement Learning from Human Feedback (RLHF), Direct Preference Optimization (DPO), ORPO & GRPO, Supervised Fine-Tuning (SFT).

**Distributed Training:**
- Data Parallelism (DDP/FSDP), Tensor Parallelism (Megatron-LM), Pipeline Parallelism (DeepSpeed), ZeRO Optimizer.

**Guardrails & Safety:**
- Llama Guard, NeMo Guardrails, Prompt Injection Defense, Hallucination Detection.

**Evaluation:**
- LLM-as-a-Judge, Ragas Evaluation, TruLens Evaluation, MMLU, GSM8K, HumanEval.

**Embeddings:**
- Embedding Evaluation, Cross-Encoder Rerankers.

**Classical ML / Stats:**
- Bias-Variance Tradeoff, Overfitting & Underfitting, Precision/Recall/F1, ROC-AUC & PR Curves, Class Imbalance (SMOTE & Class Weights), Threshold Tuning, XGBoost, LightGBM, Random Forest, Hypothesis Testing (A/B Testing video).

**AI Agents:**
- ReAct (Reasoning + Acting), Plan-and-Execute, Reflection & Self-Critique Loops, Planner–Executor–Reviewer Pattern, Function Calling, Code Interpreter & Sandbox Execution, LangGraph Workflows, AutoGen Fundamentals, API & Database Tool Integration, Short-Term Context Memory, Long-Term Memory (Vector DB / Knowledge Graph).

**Multimodal AI:**
- CLIP & Image Embeddings, Diffusion Models, Vision-Language Model Architecture, Text-to-Image Systems, Video Generation (Sora-like Systems), Cross-Modal Retrieval, Multimodal Search Architecture.

**Architecture & Leadership:**
- Writing RFCs & Design Docs, Architectural Reviews, Technical Roadmaps, Cross-Team Influence, Technical Debt Management, Infrastructure Cost Modeling, Capacity Planning.

**System Design Practice Problems:**
- Design ChatGPT, Design a Chat/Messaging System, Design a Donations Website, Design a Notification System, Design a Payment System, Design a Distributed File System, Design a Rate Limiter, Design an Ad Click Aggregator, Real-time Systems (Design Online Chess), Marketplace (Design a Book Seller Platform), API Aggregation (REST endpoint aggregating internal services), OO Design (Filter Invalid Expenses Based on Rules).

**Snowflake / Data Engineering:**
- Learn Snowflake with ONE Project, Native Snowflake (Hotel Booking Data Engineering Project), Airbnb Data Engineering Project (DBT + Snowflake + AWS), Data Cleaning & Deduplication, Tokenization Pipelines, Statistics for Data Science (A/B Testing video), Full Data Science Mock Interview.

**AI Fundamentals / Vocabulary:**
- 20 AI Concepts Explained in 40 Minutes.
- Distilling an LLM into a 150M-parameter model (AGI Tamer).
- Increasing Sales through A/B Testing (with Tinder Sr. Data Science Mgr).

---

## Final Notes

- Treat the **weekly template** as non-negotiable: plan Mon, build Tue, systems/papers Wed, eval/interview Thu, retro Fri.
- Use the **milestone gates** as your stop / continue checkpoints — if a gate fails, repeat the previous phase before progressing.
- The interview roadmap runs **continuously**, not just at Week 107 — every week should produce at least one interview artifact (coding drill, design doc, behavioral story, or technical explanation).
- The repository layout is a **template**, not a constraint — collapse folders, add your own, but keep `journal/` religiously.

**You can consider the course complete when you have completed the [Completion Criteria](#completion-criteria) above.** Good luck.