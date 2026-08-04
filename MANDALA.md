A mandala is **48 days**, so the 108-week course lasts:

> **756 days = 15 complete mandalas + one final 36-day graduation mandala**

Each full mandala spans about **6 weeks and 6 days**. That is long enough to produce a real capability—not merely “finish a chapter.”

The course already moves through ten phases, from orientation and mathematics to production AI platforms and capstones.  Here is the journey mandala by mandala.

![Tensor-to-Tenant mandala map](./mandala.webp)

## Mandala 1 — Build the learner’s operating system

**Days 1–48 · Weeks 1–7**

The learner establishes:

* Python engineering, typing, testing and async fundamentals
* NumPy, vectorization and broadcasting
* Git, notebooks, Makefiles and reproducible experiments
* Docker, HTTP, APIs and Linux basics
* personal mathematics and systems diagnostics
* weekly journals, evidence tracking and retrospectives
* vector spaces, span, basis and dimension

**Evidence produced:**

* course dashboard and repository
* tested CLI project
* numerical utility library
* reproducible notebook
* diagnostic gap map
* containerized service
* first mathematics problem set

**Transformation:**
They stop being someone “planning to study AI” and become someone with a functioning learning and engineering system.

---

## Mandala 2 — Learn the geometry beneath intelligence

**Days 49–96 · Weeks 7–14**

The learner develops serious linear-algebra fluency:

* linear independence
* rank and nullity
* inner products and dual norms
* orthogonality and projections
* Gram–Schmidt
* coordinate transformations
* eigenvalues and diagonalization
* PSD matrices and quadratic forms
* Rayleigh quotients
* SVD, pseudoinverse and low-rank approximation

**Evidence produced:**

* projection and coordinate-transformation labs
* PCA-style experiment
* quadratic-form visualization
* low-rank compression demo

**Transformation:**
Embeddings, attention and matrix models stop looking like mystical equations. The learner can reason geometrically.

---

## Mandala 3 — Numerical computation and differentiation

**Days 97–144 · Weeks 14–21**

The learner moves from exact algebra into computation:

* matrix norms and conditioning
* perturbation analysis
* LU, QR and Cholesky
* iterative solvers
* power iteration and Krylov methods
* randomized SVD
* tensor notation
* partial and directional derivatives
* gradients, Jacobians and Hessians
* Taylor approximations
* chain rule on computational graphs

**Evidence produced:**

* numerical decomposition library
* solver benchmarks
* perturbation experiment
* randomized approximation lab
* gradient and curvature visualizers
* manual backpropagation worksheet

**Transformation:**
They begin understanding not only whether an algorithm is mathematically correct, but whether it is numerically sane.

---

## Mandala 4 — Probability, autodiff and statistical inference

**Days 145–192 · Weeks 21–28**

The learner builds the mathematical machinery behind learning:

* computational graphs
* forward- and reverse-mode autodiff
* JVPs and VJPs
* probability spaces
* conditional probability and Bayes
* random variables and distributions
* covariance and correlation
* LLN, CLT and delta method
* MLE and MAP
* estimator bias and variance
* hypothesis testing
* Type I and Type II errors

**Evidence produced:**

* tiny autodiff engine
* probability simulations
* covariance analysis
* Monte Carlo convergence demo
* estimator comparison
* statistical-test implementation

**Transformation:**
They can explain why training and evaluation procedures work—not merely import them.

---

## Mandala 5 — Experimentation meets retrieval

**Days 193–240 · Weeks 28–35**

The learner connects statistics with production coding:

* p-values and test statistics
* confidence intervals
* bootstrap and permutation tests
* power, MDE and sample-size calculations
* multiple-testing correction
* cosine similarity
* exact and memory-bounded KNN
* streaming Top-K
* dynamically changing scores
* two-stage retrieval and reranking
* sliding-window and token-bucket rate limiting
* LRU and TTL caching

**Evidence produced:**

* bootstrap CI package
* experiment-size calculator
* vector-search mini-lab
* Top-K service
* reranking prototype
* rate-limiter module
* cache simulator

**Transformation:**
They can now build the primitives behind search, experimentation and traffic control.

---

## Mandala 6 — Production reliability and measurable AI

**Days 241–288 · Weeks 35–42**

The learner gains production instincts:

* text and sentence-aware chunking
* PII span merging
* regex and NER-based redaction
* Expected Calibration Error
* Brier score and reliability diagrams
* NDCG, MRR and Recall@K
* thread-safe inference batching
* retries, exponential backoff and jitter
* circuit breakers
* Count-Min Sketch and Bloom filters

**Evidence produced:**

* chunking library
* safe redaction utility
* calibration dashboard
* retrieval evaluator
* concurrent batcher
* fault-tolerance toolkit
* probabilistic data structures

The curriculum explicitly treats calibration, ranking metrics, batching, resilience and sketches as reusable engineering primitives.

**Transformation:**
They stop thinking only about model output and start thinking about trust, failure, observability and operational behavior.

---

## Mandala 7 — Distributed primitives and design reasoning

**Days 289–336 · Weeks 42–48**

The learner studies:

* HyperLogLog
* consistent hashing
* rendezvous hashing
* weighted load balancing
* distributed unique IDs
* leaky-bucket and sliding-window counters
* requirements and constraint gathering
* APIs and data modelling
* observability
* rate limiting at distributed scale

**Evidence produced:**

* cardinality estimator
* routing lab
* load-balancer module
* platform-primitives library
* system-design document template
* first complete design exercises

**Transformation:**
They can move from implementing one process to reasoning about many machines.

---

## Mandala 8 — Classic distributed systems

**Days 337–384 · Weeks 49–55**

The learner handles:

* scaling reads and writes
* caching and replication
* contention
* large blob storage and CDNs
* orchestration versus choreography
* workflow-state ownership
* backward-compatible schema evolution
* URL shorteners
* Dropbox
* Ticketmaster
* News Feed
* WhatsApp
* LeetCode-style judge systems

**Evidence produced:**

* scaling-pattern notes
* blob-storage design
* workflow-state architecture
* schema-migration plan
* multiple end-to-end design documents

**Transformation:**
They stop naming technologies and start defending architecture.

---

## Mandala 9 — From system design to ML product science

**Days 385–432 · Weeks 55–62**

The learner finishes major system case studies and enters ML systems:

* Uber and web crawlers
* ad-click aggregation
* payments
* business-objective formulation
* model-versus-non-model decisions
* labeling and weak supervision
* data augmentation
* leakage and contamination
* experiment tracking and versioning
* baselines
* slice-based offline evaluation
* confidence intervals
* shadow and canary deployment
* bandits

**Evidence produced:**

* ML project charter
* data-quality checklist
* leakage audit
* evaluation harness
* rollout plan

**Transformation:**
They learn that a production ML system begins with a decision and a dataset—not with model training.

---

## Mandala 10 — Build a mature experimentation platform

**Days 433–480 · Weeks 62–69**

The learner implements:

* A/B-test significance calculation
* absolute and relative lift
* pooled standard errors
* confidence intervals
* paired bootstrap model comparison
* Sample-Ratio Mismatch detection
* chi-square diagnostics
* feature-flag engines
* deterministic sticky assignment
* monitoring and drift detection
* production incident analysis

**Evidence produced:**

* `analyze_ab_test`
* bootstrap comparison package
* SRM detector
* feature-flag service
* experiment-assignment service
* monitoring specification
* incident postmortem

**Transformation:**
They can distinguish “the metric increased” from “we have trustworthy evidence that the product improved.”

---

## Mandala 11 — Train, align and retrieve with LLMs

**Days 481–528 · Weeks 69–76**

The learner enters modern LLM engineering:

* transformer and tokenizer anatomy
* training-data cleaning and deduplication
* SFT
* LoRA, QLoRA and DoRA
* RLHF
* DPO, ORPO and GRPO
* DDP and FSDP
* tensor and pipeline parallelism
* ZeRO
* HNSW
* IVF-PQ and product quantization
* hybrid retrieval
* query rewriting
* parent–child and multi-vector retrieval

**Evidence produced:**

* model-anatomy notes
* dataset card
* fine-tuning plan
* preference-evaluation plan
* distributed-training architecture
* vector-index benchmark
* retrieval lab

**Transformation:**
They understand the whole upstream and retrieval lifecycle rather than treating the LLM as a remote magic endpoint.

---

## Mandala 12 — RAG, agents and inference foundations

**Days 529–576 · Weeks 76–83**

The learner develops:

* BM25 + dense + reranker fusion
* Reciprocal Rank Fusion
* evaluation by query slice
* prompt templates and version registries
* conversation and long-term memory
* context-window optimization
* ReAct
* plan-and-execute
* tool calling
* agent guardrails
* GPU compute-, memory- and overhead-bound regimes
* FlashAttention
* roofline models
* arithmetic intensity

**Evidence produced:**

* retrieval-fusion service
* regression report
* prompt-management tool
* memory service
* agent prototype
* GPU performance primer
* arithmetic-intensity worksheet

**Transformation:**
They can build an agent and explain where its latency, errors, context and cost come from.

---

## Mandala 13 — Become an inference systems engineer

**Days 577–624 · Weeks 83–90**

The learner goes inside serving engines:

* PagedAttention
* KV-cache block tables
* vLLM deployment
* scheduler and block-manager internals
* running and waiting request metrics
* latency histograms
* Prometheus and Grafana
* request-rate sweeps
* saturation analysis
* SGLang
* RadixAttention and prefix reuse
* Orca-style continuous batching
* chunked prefill

**Evidence produced:**

* live vLLM deployment
* internal architecture notes
* metrics schema
* serving dashboard
* benchmark methodology
* vLLM/SGLang comparison
* scheduling report

**Transformation:**
They can diagnose inference rather than simply complain that it is slow.

---

## Mandala 14 — Advanced serving and reliable routing

**Days 625–672 · Weeks 90–96**

The learner tackles:

* continuous batching trade-offs
* FP8, AWQ and GPTQ
* KV-cache compression
* speculative decoding
* Medusa and EAGLE
* StreamingLLM and KV eviction
* DistServe, Splitwise and Mooncake
* prefill/decode disaggregation
* model routing
* canary assignment and kill switches
* PII-safe traces and logs
* async fan-out
* partial failures
* token-stream multiplexing

**Evidence produced:**

* quality-versus-throughput benchmark
* latency and memory lab
* disaggregated serving architecture
* model-router service
* safe tracing layer
* resilient aggregator

**Transformation:**
They can optimize not just a model, but a multi-provider inference service.

---

## Mandala 15 — Build the enterprise AI platform

**Days 673–720 · Weeks 97–103**

The learner integrates the entire stack:

* distributed token budgets
* request prioritization
* DAG workflow execution
* idempotency
* per-tenant concurrency limits
* leader election
* distributed work queues
* dynamic configuration
* model health monitoring
* model registries and promotion
* semantic and embedding caches
* prompt-injection detection
* exact cost attribution
* capstone architecture planning

**Evidence produced:**

* quota and priority service
* workflow engine
* tenant limiter
* HA lab
* queue/configuration platform
* model-operations pipeline
* cost/safety platform
* complete capstone design document

The Phase 9 gate expects a working production platform with routing, quotas, tracing, idempotency, queues, registry, cost accounting and safety.

**Transformation:**
This is where “tensor” finally becomes “tenant.”

---

## Final 36-day graduation mandala

**Days 721–756 · Weeks 103–108**

This final cycle is shorter, but nastier.

The learner:

* completes the capstone core API
* builds the retrieval or agent flow
* installs evaluation, tracing and guardrails
* runs load and failure tests
* tunes latency and cost
* produces architecture and benchmark reports
* completes coding, system-design and behavioral mocks
* publishes the portfolio
* performs a full retrospective
* creates a 30-day career plan

Possible final paths:

1. Multi-Tenant Trace Forensics with Mo’s Algorithm
2. Agent Execution Forensics with Euler Tour + DSU on Tree
3. OpenRouter-inspired Enterprise AI Gateway

**Transformation:**
They no longer need to tell someone they “know AI systems.” They can provide the repository, traces, benchmarks, design documents and failure tests.

---

# What runs in parallel during every mandala

Every 48-day period also includes four continuous streams.

### Auror / Leetcode Darbar

At the high-achiever pace of approximately five problems per week:

> **About 34–35 problems per full mandala**

Across the full course, that reaches all 548 problems:

* 255 Easy
* 240 Medium
* 53 Hard

### Algorithmic Forge

Roughly **6–7 deeper algorithm labs per mandala**, covering:

* graphs
* DP
* strings
* flows
* number theory
* advanced data structures
* Euler tours, Mo’s and DSU on Tree
* selected boss fights

### Interview and Staff communication

Each mandala advances:

* coding fluency
* system-design delivery
* one or more CARL stories
* technical explanations aloud
* architectural writing
* trade-off judgment

The course requires weekly coding, design, behavioral refinement and spoken explanation rather than postponing interviews to the end.

### Personal operating discipline

Each cycle closes with:

* Sailboat retrospective
* Hansei: what went wrong?
* Kaizen: what small change should be made?
* PDCA: what gets tested next?
* milestone evidence
* recovery planning where necessary

---

## The mandala-level progression

| Mandala | Identity gained                             |
| ------: | ------------------------------------------- |
|       1 | Disciplined learner                         |
|       2 | Linear-algebra thinker                      |
|       3 | Numerical programmer                        |
|       4 | Statistical reasoner                        |
|       5 | Retrieval and experimentation builder       |
|       6 | Reliability-minded engineer                 |
|       7 | Distributed-systems implementer             |
|       8 | System designer                             |
|       9 | ML systems practitioner                     |
|      10 | Experimentation engineer                    |
|      11 | LLM training and retrieval engineer         |
|      12 | RAG and agent engineer                      |
|      13 | Inference performance engineer              |
|      14 | Serving and routing engineer                |
|      15 | Multi-tenant AI platform engineer           |
|   Final | Portfolio-backed Staff AI Systems candidate |

So every 48 days, the learner does not merely “cover seven more topics.”

They gain a **new professional identity**, generate evidence for it, reflect on what held them back, and then enter the next mandala with a stronger system.

By the last mandala, Kandaswamy looks at Week 1 and thinks:

> **“That person was learning Python. I now know why exact distributed mode is not mergeable.”** 💀🔥
