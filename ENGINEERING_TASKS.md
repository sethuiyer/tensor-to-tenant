# Engineering tasks and timed drills

> A detailed prompt bank preserved from the former README. The schema-backed
> registry in [`schema/engineering.yaml`](./schema/engineering.yaml) remains
> the source for the current 30 Phase 4 core-primitive titles and 40 drill
> titles. The legacy prompts below preserve interfaces, edge cases, and target
> timeboxes that the site cards intentionally keep short; their names/order do
> not replace the current schema IDs.
>
> **Classification rule:** prompts 1–30 below are the legacy detailed production bank.
> The former README's #31 MoE prompt is retained as a Week 90 optional depth
> extension, not counted as a 31st core Phase 4 task.

## Legacy 30-prompt production bank

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

## Phase 8 extension — MoE all-to-all schedule precomputer

The following prompt was formerly listed as task 31. It belongs with Week 90's
MoE scheduling and overlap work, not with the Phase 4 core primitive registry.

> Given $T$ tokens, $E$ experts, and $G$ GPUs, write a CPU-side scheduler that
generates the dispatch/combine offset table ($\Phi$). Simulate a timeline where
compute blocks (FFN) and communication blocks (NVLink All-to-All) are interleaved.
Output a Gantt chart showing the percentage of time the GPU spends idle versus
overlapping. State and test the assumption that precomputing the schedule takes
less than 3% of total step time.

## 40 timed practice drills

These drills are the short Friday/implementation exercises: retrieval, rate
limiting, caching, chunking, PII, calibration, ranking metrics, batching,
resilience, sketches, routing, information retrieval, and scheduling.

| # | Problem | Core Pattern | Mode | Target |
|---:|---|---|---|---|
| 1 | Cosine similarity from scratch | NumPy / vector math | implement | 10 min |
| 2 | Exact KNN from scratch | Top-K + vectorization | implement | 15 min |
| 3 | Memory-bounded KNN | Chunking + heap | implement | 20 min |
| 4 | Streaming Top-K | Min-heap | implement | 10 min |
| 5 | Top-K with dynamic score updates | Heap + lazy deletion | implement | 20 min |
| 6 | Two-stage retrieval and reranking | Heap / partial sorting | implement | 20 min |
| 7 | Per-tenant sliding-window rate limiter | Hash map + deque | implement | 15 min |
| 8 | Token bucket rate limiter | Time arithmetic + state | implement | 15 min |
| 9 | LRU cache | Hash map + doubly linked list | implement | 20 min |
| 10 | LRU cache with TTL | LRU + expiration | implement | 25 min |
| 11 | Token-aware text chunking | Sliding window | implement | 15 min |
| 12 | Sentence-aware recursive chunking | Greedy splitting | implement | 25 min |
| 13 | Merge overlapping PII spans | Interval merging | implement | 15 min |
| 14 | Regex + NER PII detector | Span resolution + scoring | implement | 25 min |
| 15 | Expected Calibration Error | Binning + NumPy | implement | 15 min |
| 16 | Brier score and reliability data | Statistics + aggregation | implement | 15 min |
| 17 | NDCG, MRR and Recall@K | Ranking metrics | implement | 20 min |
| 18 | Thread-safe inference batcher | Queue + condition variable | implement | 30 min |
| 19 | Retry with exponential backoff and jitter | State + timing | implement | 15 min |
| 20 | Circuit breaker | State machine | implement | 20 min |
| 21 | Count-Min Sketch | Streaming data structures | implement | 20 min |
| 22 | Bloom Filter | Probabilistic data structures | implement | 15 min |
| 23 | HyperLogLog | Cardinality estimation | implement | 25 min |
| 24 | Consistent Hash Ring | Distributed systems | implement | 20 min |
| 25 | Weighted Round Robin Load Balancer | Scheduling | implement | 20 min |
| 26 | Rendezvous (Highest Random Weight) Hashing | Distributed routing | implement | 25 min |
| 27 | Distributed Unique ID Generator (Snowflake) | ID generation | implement | 20 min |
| 28 | Leaky Bucket Rate Limiter | Traffic shaping | implement | 15 min |
| 29 | Sliding Window Counter Rate Limiter | Time-series aggregation | implement | 20 min |
| 30 | Weighted Fair Queue Scheduler | Scheduling algorithms | implement | 30 min |
| 31 | Prefix Trie with Autocomplete | Trie + ranking | implement | 20 min |
| 32 | Inverted Index Builder | Information retrieval | implement | 25 min |
| 33 | BM25 Scoring from Scratch | Search ranking | implement | 30 min |
| 34 | SimHash Near-Duplicate Detection | Hashing | implement | 25 min |
| 35 | MinHash & Jaccard Estimation | Locality-sensitive hashing | implement | 30 min |
| 36 | Approximate Quantile Estimator (GK / t-digest concept) | Streaming statistics | implement | 30 min |
| 37 | Reservoir Sampling | Streaming algorithms | implement | 20 min |
| 38 | Producer–Consumer Queue | Concurrency | implement | 20 min |
| 39 | Thread Pool Executor | Concurrency primitives | implement | 30 min |
| 40 | Async Task Scheduler with Priority Queue | Scheduling + heap | implement | 30 min |


## Suggested learner-repo layouts

Phase 4's reusable primitive library:

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

Phase 9's platform layer:

```text
ai_platform/
  router/  experiments/  logging/  tracing/  fanout/
  quotas/  scheduler/  idempotency/  tenant_limiter/
  leader_election/  work_queue/  config_service/
  model_registry/  health_monitor/  semantic_cache/
  embedding_cache/  injection_detector/  cost_attribution/
```

## Gate-4 evidence contract

Gate 4 is passed by shipping the primitive contracts and tests for retrieval,
rate limiting, caching, chunking, PII handling, metrics, resilience, sketches,
and routing. Use the [engineering hub](https://sethuiyer.github.io/tensor-to-tenant/engineering/)
and [Gate 4 criteria](https://sethuiyer.github.io/tensor-to-tenant/gates/) for the
current structured checklist.

## Related surfaces

- [`schema/engineering.yaml`](./schema/engineering.yaml) — structured titles, tiers, levels, and seams
- [Engineering hub](https://sethuiyer.github.io/tensor-to-tenant/engineering/) — browsable catalog
- [`ML_CODING_CHALLENGES.md`](./ML_CODING_CHALLENGES.md) — separate ML/inference interview catalog
- [`ALGORITHMIC_FORGE.md`](./ALGORITHMIC_FORGE.md) — algorithmic depth lane
- [`docs/WEEKLY_OPERATING_MODEL.md`](./docs/WEEKLY_OPERATING_MODEL.md) — scope and evidence rules
