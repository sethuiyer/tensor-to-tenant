# Source-to-week map

> A reader-facing map of how source areas feed the Tensor-to-Tenant spine. The
> tables below preserve the map that was removed from the landing README. They
> are navigation aids, not a second structured catalog: update IDs and facts in
> `schema/*.yaml`, then regenerate site/cookiecutter views.

## Math → spine

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

The structured 100-module registry lives in [`../schema/math.yaml`](../schema/math.yaml) and the [math hub](https://sethuiyer.github.io/tensor-to-tenant/math/).


## Engineering tasks → weeks

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
| MoE All-to-All Schedule Precomputer (optional depth) | 90 |

The detailed prompt bank lives in [`../ENGINEERING_TASKS.md`](../ENGINEERING_TASKS.md).


## Engineering practice → weeks

Use the 40 timed drills as **Friday drills** or interview warm-ups.

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

The full 40-drill table is preserved in [`../ENGINEERING_TASKS.md`](../ENGINEERING_TASKS.md).


## System design

| Source topic | Course weeks |
|---|---:|
| Canonical track and delivery framework | [`../SYSTEM_DESIGN_TRACK.md`](../SYSTEM_DESIGN_TRACK.md), 46–57 |
| Networking, API, data modeling, numbers | 46–47 |
| Caching, sharding, consistent hashing, CAP | 48–49 |
| Blob storage, workflows, schema evolution | 50–52 |
| Search, messaging, social, scheduling | 53–55 |
| Streaming, analytics, payments, ChatGPT | 56–57 |
| OOD / LLD | Parallel Thursday lane, 46–57 |


## ML / MLOps

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


## Inference papers and systems

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
| MoE all-to-all dispatch/combine patterns | 90 |
| Warp Decode (Cursor blog) | 90 |
| COMET (fine-grained comp-comm overlap for MoE) | 90 |
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

The structured paper/resource view is the [resources hub](https://sethuiyer.github.io/tensor-to-tenant/resources/).


## LLM training, RAG, agents, and evaluation

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

## Ownership and caveats

- Structured week, phase, gate, math, engineering, interview, agent, and
  resource entities belong in [`../schema/`](../schema/).
- The legacy detailed engineering prompts and timed-drill targets live in
  [`../ENGINEERING_TASKS.md`](../ENGINEERING_TASKS.md); the schema retains the
  current title/metadata index, so the two prompt names/orderings are not a
  second task-ID authority.
- Legacy video/book/blog lists are currently carried through the generated
  resource view's migration fixture ([`../schema/source_data.yaml`](../schema/source_data.yaml)). Promote them
  into metadata-first `schema/resources.yaml` entries before removing that
  fixture.
- The former 100-row math table and the current schema taxonomy are not
  identical. The old table is preserved as an
  [`archive/MATH_CATALOG_HEAD.md`](./archive/MATH_CATALOG_HEAD.md) snapshot for
  reconciliation; treat [`../schema/math.yaml`](../schema/math.yaml) and the
  [math hub](https://sethuiyer.github.io/tensor-to-tenant/math/) as active and
  do not schedule from the archive.

## Live views

- [Curriculum](https://sethuiyer.github.io/tensor-to-tenant/curriculum/)
- [Math](https://sethuiyer.github.io/tensor-to-tenant/math/)
- [Engineering](https://sethuiyer.github.io/tensor-to-tenant/engineering/)
- [Resources](https://sethuiyer.github.io/tensor-to-tenant/resources/)
- [Interview](https://sethuiyer.github.io/tensor-to-tenant/interview/)
