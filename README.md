# Tensor-to-Tenant

> **Build the math, systems, and judgment behind production AI.**
>
> A production-oriented apprenticeship that takes you from vectors and
> numerical methods to RAG, agents, LLM inference, multi-tenant platforms, and
> the interviews that test whether you can defend the trade-offs.

**108 weeks · 10–15 hours/week · 3 stackable releases · 10 gates · GPU only in W75/W84/W87/W89**

[**Start the apprenticeship →**](https://sethuiyer.github.io/tensor-to-tenant/curriculum/) ·
[Browse the interactive site](https://sethuiyer.github.io/tensor-to-tenant/) ·
[See the capstones](https://sethuiyer.github.io/tensor-to-tenant/capstones/) ·
[Generate a learner repo](#start-in-five-minutes)

**Jump to:** [Start](#start-in-five-minutes) · [Choose a path](#choose-your-path) ·
[Releases](#three-stackable-releases) · [Gates](#progress-is-gated-not-assumed) ·
[Capstones](#capstones-choose-the-evidence-you-want-to-defend) · [Contribute](#for-contributors-and-site-developers)

---

## The short version

Most AI tutorials stop at *calling a model*. This one keeps going until you can
**explain, implement, benchmark, operate, and defend** the system around it.

By the end of the core path, you will have practiced:

- **Foundations:** linear algebra, numerical methods, calculus, probability, statistics, and optimization.
- **Engineering:** retrieval, Top-K, rate limiting, caching, chunking, PII redaction, metrics, resilience, sketches, and routing.
- **ML/LLM systems:** experimentation, evaluation, RAG, fine-tuning plans, agents, memory, and guardrails.
- **Inference:** roofline reasoning, FlashAttention, PagedAttention block allocation, vLLM/SGLang, batching, quantization, and disaggregation.
- **Platform judgment:** routing, quotas, tracing, idempotency, work queues, model registries, cost attribution, safety, and tenant isolation.
- **Interview evidence:** coding, system design, behavioral stories, technical explanations, benchmarks, and public portfolio releases.

> **The target identity:** a straight line from `vector.dot()` to a per-tenant
> concurrency limiter with leader election.

---

## Start in five minutes

You do **not** need to read 108 weeks before beginning. Pick a path below, scaffold
your journal, and ship Week 1.

```bash
# Install Cookiecutter once (choose your preferred installer)
pipx install cookiecutter
# If pipx is unavailable: python -m pip install cookiecutter

# Generate a personal learner repository
cookiecutter gh:sethuiyer/tensor-to-tenant

# The default directory is tensor-to-tenant-journal
cd tensor-to-tenant-journal
make init
make week=1
```

Then use the operating loop:

```bash
make progress       # see what is actually complete
make week=14        # prepare any weekly journal + evidence scaffold
make gate           # check the current blocking checkpoint
make release=30     # prepare a publishable release checklist
make badge=30       # verify Foundations evidence + Gate 3
make badge=69       # verify Engineering + Systems evidence + Gate 6
make badge=108      # verify LLM Platform evidence + Gate 10
```

The generated repo includes all 108 journals, evidence folders, phase READMEs,
recovery plans, milestone gates, interview tracks, capstone scaffolds, and
helper commands. See the [cookiecutter guide](./cookiecutter/README.md) for all
options and commands.

### If you only want to browse

- [Full interactive curriculum](https://sethuiyer.github.io/tensor-to-tenant/curriculum/)
- [Milestone gates](https://sethuiyer.github.io/tensor-to-tenant/gates/)
- [FAQ](https://sethuiyer.github.io/tensor-to-tenant/faq/)

---

## Choose your path

| You are here | Do this now | Your first useful link |
|---|---|---|
| Comfortable writing Python and building small services | Start at Week 1 | [Curriculum](https://sethuiyer.github.io/tensor-to-tenant/curriculum/) |
| Rusty on programming, CS, or statistics | Take the optional 36-week on-ramp, then start Week 1 | [Prerequisites](https://sethuiyer.github.io/tensor-to-tenant/prerequisites/) |
| Already building agents and want the systems underneath | Use the 18-module agents track and its bridge into the spine | [Agents](https://sethuiyer.github.io/tensor-to-tenant/agents/) · [Generator guide](./cookiecutter/README.md) |
| Optimizing for interviews | Keep the core path; add Friday Forge and selected Darbar problems | [Interview hub](https://sethuiyer.github.io/tensor-to-tenant/interview/) |
| Want the shortest credible stopping point | Finish Weeks 1–30 and publish the Foundations release | [Programs and gates](https://sethuiyer.github.io/tensor-to-tenant/gates/) |

**Best fit:** a working engineer or data scientist who can protect 10–15 hours
per week and wants production depth rather than another API wrapper tutorial.
The on-ramp is intentionally an on-ramp, not a gate.

During scaffolding, choose one optional weighting: `balanced`,
`production-ai-platform`, `llm-inference`, or `rag-agents`. The track changes
where depth is suggested; every learner shares the same 108-week core.

---

## The arc: tensor → tenant

```text
 tensor → vector → model → serving → platform → tenant
```

| Layer | Focus |
|---|---|
| **Tensor** | Linear algebra, numerical methods, calculus, probability, and statistics |
| **Vector** | Embeddings, retrieval, ranking, and search geometry |
| **Model** | Fine-tuning, alignment, RAG, memory, agents, and evaluation |
| **Serving** | vLLM/SGLang, batching, quantization, scheduling, and inference economics |
| **Platform** | Routing, quotas, tracing, idempotency, queues, safety, and cost |
| **Tenant** | Isolation, fairness, admission control, auditability, and staff judgment |

### At a glance

| 108 weeks | 10 phases | 10 gates | 3 releases | 100 math modules | 30 engineering tasks |
|---:|---:|---:|---:|---:|---:|
| Core spine | Math → platform | Blocking | W30 / W69 / W108 | 10 tracks | Plus 40 practice exercises |

### Ten phases, one deliverable at a time

| Phase | Weeks | What you build or prove |
|---:|---:|---|
| 1 | 1–6 | Your course operating system, diagnostics, tooling, and a containerized service |
| 2 | 7–18 | Linear algebra and numerical routines: projections, decompositions, solvers, low-rank approximation |
| 3 | 19–30 | Calculus, autodiff, probability, statistics, bootstrap, power, and experimentation math |
| 4 | 31–45 | Retrieval and production primitives: Top-K, rate limits, caches, chunkers, redaction, metrics, resilience, routing |
| 5 | 46–57 | System design: APIs, data models, scale, queues, consistency, case studies, and failure modes |
| 6 | 58–69 | ML lifecycle: framing, data quality, leakage, offline/online evaluation, rollouts, monitoring, postmortems |
| 7 | 70–81 | LLM data/training concepts, RAG, retrieval evaluation, prompts, memory, agents, and guardrails |
| 8 | 82–93 | GPU performance, vLLM/SGLang, batching, quantization, speculative decoding, and disaggregated serving |
| 9 | 94–102 | A production AI platform: routing, quotas, tracing, queues, registries, safety, and cost |
| 10 | 103–108 | Capstone, portfolio release, mock interviews, behavioral stories, and a 30-day plan |

[Open the week-by-week curriculum →](https://sethuiyer.github.io/tensor-to-tenant/curriculum/)

<p align="center">
  <img src="./tensor_to_tenant_cutout.png" alt="Tensor-to-Tenant curriculum map" width="800">
</p>

---

## Three stackable releases

You can stop with a public artifact at any checkpoint. Continuing raises the
ceiling; it does not invalidate the work already shipped.

| Release | Weeks | Publish this |
|---|---:|---|
| **Foundations** | 1–30 | Math diagnostic, numerical routines, statistics/experimentation toolkit, and explanation of the work |
| **Engineering + Systems** | 31–69 | Tested production primitives, system-design portfolio, experimentation tools, monitoring plan, and postmortem |
| **LLM Platform** | 70–108 | RAG/agent work, inference benchmark, production platform layer, capstone, and interview-ready portfolio |

Every release is evidence-backed: **implementation · benchmark/result · design
or technical explanation · retrospective**.

---

## How a week works

### Core first. Depth second.

Every week has one **core deliverable** sized for the stated time budget. Optional
depth can add a proof, from-scratch implementation, benchmark, failure analysis,
or production trade-off—but it never blocks the core path.

| Mode | Ship this | Typical week |
|---|---|---|
| `implement` | Working, tested code | W35 cache, W63 A/B calculator, W99 tenant limiter |
| `read_diagram` | Design doc, trade-off note, comparison, or methodology | W74 training map, W93 serving plan |
| `deploy_benchmark` | A live deployment or benchmark | W75 index, W84 vLLM, W87 dashboard, W89 SGLang |

**Scope rule:** if a `read_diagram` week turns into 15+ hours of coding, stop and
write the document. If an `implement` week has no running artifact after 8 hours,
trim scope until it runs.

### The weekly rhythm

```text
Mon  theory / mathematics
Tue  implementation
Wed  systems, papers, architecture
Thu  evaluation + interview practice
Fri  Algorithmic Forge drill + Sailboat retrospective
```

The interview layer is continuous: one coding drill, one design question or
pattern, one behavioral story refinement, and one technical explanation each
week. Planned recovery windows follow Weeks **6, 14, 22, 30, 38, 46, 54, 62,
70, 78, 86, 94, and 102**.

---

## Progress is gated, not assumed

A gate is a **stop/continue checkpoint**, not a decorative badge. If it fails,
pause new gate-dependent material, use the next recovery window, and submit
focused remediation evidence. You do not restart the course.

| Gate | Week | Prove this |
|---:|---:|---|
| 1 | 6 | Repo, tracker, Dockerized service, and diagnostics |
| 2 | 18 | Numerical-algebra fluency: eigenvalues, SVD, norms, conditioning, routines |
| 3 | 30 | Gradients, MLE/MAP, tests, bootstrap CIs, power/MDE; **Foundations release** |
| 4 | 45 | Retrieval, limits, caching, chunking, PII, metrics, resilience, sketches, routing |
| 5 | 57 | Defensible system-design case studies with scale and failure analysis |
| 6 | 69 | Experiment tools, assignment, monitoring, and postmortem; **Engineering + Systems release** |
| 7 | 81 | RAG pipeline, slice evaluation, prompt system, memory, and agent prototype |
| 8 | 93 | vLLM/SGLang benchmark, observability, quantization, speculative decoding, cost model |
| 9 | 102 | Working AI platform: router, quotas, tracing, idempotency, queue, registry, cost, safety |
| 10 | 108 | Capstone, portfolio, mock interviews, behavioral stories, and 30-day plan |

[See gate criteria and remediation details →](https://sethuiyer.github.io/tensor-to-tenant/gates/)

---

## The learning philosophy: make every elegant idea survive contact with reality

The course deliberately moves through three levels:

1. **Level 1 — recognize it.** You have heard of the idea.
2. **Level 2 — implement it.** You can make it work on a bounded problem.
3. **Level 3 — defend it.** You know when it breaks, what the workload exposes,
   and what replaces it.

| Pretty answer | The seam that breaks it | What you learn next |
|---|---|---|
| Cosine similarity | 100M vectors do not fit in RAM | HNSW, IVF-PQ, quantization, sharding, admission |
| Retry with backoff | A payment can be charged twice | Idempotency, outbox, exactly-once boundaries |
| PagedAttention | MoE all-to-all and phase differences dominate | Overlap, scheduling, prefill/decode disaggregation |
| Per-tenant rate limit | Fairness, billing, noisy neighbors, and cost collide | Quotas, tracing, leader election, isolation |

That seam philosophy is why the path is long—and why the portfolio is more than
a list of technologies.

---

## Parallel tracks (use them without derailing the core)

| Track | Role | Where to go |
|---|---|---|
| **Algorithmic Forge** | Friday depth: derive, implement, and stress algorithms; Core / Supporting / Archive / Boss tiers | [Forge](./ALGORITHMIC_FORGE.md) · [site](https://sethuiyer.github.io/tensor-to-tenant/algorithmic-forge/) |
| **System Design** | Canonical architecture/interview track for Weeks 46–57 | [Track](./SYSTEM_DESIGN_TRACK.md) · [site](https://sethuiyer.github.io/tensor-to-tenant/system-design/) |
| **Leetcode Darbar** | Optional timed execution lane: 548 catalog slots; speed, not production evidence | [Guide](./LEETCODE_DARBAR.md) · [catalog](https://aninokuma.codeberg.page/leetcode-darbar/) |
| **Agents** | 18 modules + MCP + Project Manus, bridged back to the math/systems spine | [site](https://sethuiyer.github.io/tensor-to-tenant/agents/) · [cookiecutter guide](./cookiecutter/README.md) |
| **Recommender** | Optional paired deep dive: theory in `SEARCH.md`, production in `SNOWFLAKE.md` | [Theory](./SEARCH.md) · [Production](./SNOWFLAKE.md) |

**Rule:** Darbar never replaces a core deliverable or a blocking gate. The
standard path stays completable; the optional lanes raise the ceiling.

### The 16-mandala identity map

The 108-week arc is also fifteen 48-day capability cycles plus a final graduation
cycle. Each mandala ends with a capability, evidence, and retrospective. Open the
full progression from the visual:

<a href="./MANDALA.md">
  <img src="./mandala.webp" alt="Tensor-to-Tenant 16-mandala capability progression" width="800">
</a>

---

## Capstones: choose the evidence you want to defend

| Path | Status | What you build | Specification |
|---|---|---|---|
| **Multi-Tenant LLM Trace Forensics** | Required canonical path | Immutable trace segments, PII-safe ingestion, exact batch forensics with Mo's algorithm, approximate alternatives, and tenancy | [`CAPSTONE.md`](./CAPSTONE.md) |
| **Agent Execution Forensics** | Optional Week 108 boss fight | Euler Tour + DSU on Tree over large agent-execution forests and subtree queries | [`CAPSTONE2_EULER_DSU.md`](./CAPSTONE2_EULER_DSU.md) |
| **Enterprise Multi-Model AI Gateway** | Alternative final path | Unified API, policy-aware routing, stream-safe failover, admission, accounting, observability, and enterprise controls | [`CAPSTONE3_OPENROUTER.md`](./CAPSTONE3_OPENROUTER.md) |

**Completion rule:** finish Capstone 1, or choose Capstone 3 as the alternative;
Capstone 2 is optional. In every case, publish the design, implementation,
evaluation, observability, cost, safety, and interview evidence.

[Browse the visual capstone hub →](https://sethuiyer.github.io/tensor-to-tenant/capstones/)

### Visual capstone map

Each image links to its complete specification:

<a href="./CAPSTONE.md">
  <img src="./capstone_trace_forensics_infographic.webp" alt="Capstone 1 — Multi-Tenant LLM Trace Forensics with Mo's Algorithm" width="800">
</a>

<a href="./CAPSTONE2_EULER_DSU.md">
  <img src="./capstone_tree_nightmare_forensics.webp" alt="Capstone 2 — Multi-Tenant Agent Execution Forensics with Euler Tour and DSU on Tree" width="800">
</a>

<a href="./CAPSTONE3_OPENROUTER.md">
  <img src="./capstone3_enterprise_ai_gateway.webp" alt="Capstone 3 — OpenRouter-inspired Enterprise Multi-Model AI Gateway" width="800">
</a>

---

## The first four weeks are intentionally concrete

| Week | Ship |
|---:|---|
| 1 | Course dashboard, tracker, repo, and weekly README |
| 2 | Tested Python CLI skeleton with typing, testing, and async basics |
| 3 | Vector-math utility library using NumPy and vectorization |
| 4 | Reproducible notebook plus Makefile and experiment record |

Do not wait until you understand transformers to begin. The early operating
system is what lets the later theory become durable evidence. The Week 5
hypothesis/generalization lab is preserved in [`docs/WEEK_05_GENERALIZATION_LAB.md`](./docs/WEEK_05_GENERALIZATION_LAB.md).

---

## Prerequisites and recovery

- **Already comfortable?** Start at Week 1.
- **Need fundamentals?** Follow the fixed, optional **36-week on-ramp**: search
  and documentation, Git, CS50x, Nand to Tetris, discrete math, programming
  paradigms, statistical learning, software engineering, and a synthesis project.
- **Blocked by hardware?** Only Weeks 75, 84, 87, and 89 require GPU access.
  Use the documented benchmark methodology and recovery plan if you cannot run
  those weeks immediately.
- **Behind schedule?** Protect the core deliverable, use a recovery week, and
  write the retrospective. Do not turn optional depth into a hidden prerequisite.

[Open the on-ramp](https://sethuiyer.github.io/tensor-to-tenant/prerequisites/) ·
[Read the FAQ](https://sethuiyer.github.io/tensor-to-tenant/faq/) ·
[Cookiecutter guide](./cookiecutter/README.md) (the generated repo includes `docs/bottlenecks.md`)

---

## The evidence loop

For each core week, save four links in the generated evidence folder:

```text
1. Code / implementation
2. Benchmark / result
3. Design doc / technical explanation
4. Retrospective / learning note
```

End Friday with a short [Sailboat retrospective](./SAILBOAT_RETRO.md): destination,
wind, anchor, rocks, boat position, and the single next heading. This keeps a
long apprenticeship navigable instead of turning it into a checkbox graveyard.

---

## Find the detail you need

The README is the launchpad. The site is the canonical structured view; the
Markdown docs preserve the rationale, operating policy, and routing context.

| Need | Open |
|---|---|
| Week-by-week deliverables | [Curriculum](https://sethuiyer.github.io/tensor-to-tenant/curriculum/) |
| Why the apprenticeship is long and seam-oriented | [`docs/COURSE_PHILOSOPHY.md`](./docs/COURSE_PHILOSOPHY.md) |
| Weekly budget, modes, gates, and evidence policy | [`docs/WEEKLY_OPERATING_MODEL.md`](./docs/WEEKLY_OPERATING_MODEL.md) |
| Week 5 paper anchor | [`docs/WEEK_05_GENERALIZATION_LAB.md`](./docs/WEEK_05_GENERALIZATION_LAB.md) |
| Parallel-track routing | [`docs/PARALLEL_TRACKS.md`](./docs/PARALLEL_TRACKS.md) |
| Agents bootcamp bridge | [`docs/AGENT_BRIDGE.md`](./docs/AGENT_BRIDGE.md) |
| Math modules | [Math hub](https://sethuiyer.github.io/tensor-to-tenant/math/) |
| Engineering task prompts | [`ENGINEERING_TASKS.md`](./ENGINEERING_TASKS.md) · [hub](https://sethuiyer.github.io/tensor-to-tenant/engineering/) |
| Source-to-week mapping | [`docs/SOURCE_MAP.md`](./docs/SOURCE_MAP.md) |
| Optional topic inventory | [`docs/OPTIONAL_TRACKS.md`](./docs/OPTIONAL_TRACKS.md) |
| Inference, RAG, and agent resources | [Resources](https://sethuiyer.github.io/tensor-to-tenant/resources/) |
| Interview roadmap | [Interview hub](https://sethuiyer.github.io/tensor-to-tenant/interview/) |
| Mandala identity progression | [`MANDALA.md`](./MANDALA.md) · [site](https://sethuiyer.github.io/tensor-to-tenant/mandala/) |
| Weekly retrospective ritual | [`SAILBOAT_RETRO.md`](./SAILBOAT_RETRO.md) · [site](https://sethuiyer.github.io/tensor-to-tenant/sailboat/) |
| Phase implementation notes | [`docs/PHASE_DETAILS.md`](./docs/PHASE_DETAILS.md) |
| Structured curriculum data | [`schema/`](./schema/) · [`docs/README.md`](./docs/README.md) |

---

## For contributors and site developers

This repository also contains the Astro site and the schema-driven generators.

```bash
npm install
npm run dev             # local site
npm run prebuild        # schema, generator, capstone, and drift checks
pytest tests/ -q        # Python test suite
npm run build           # production Astro build + Pagefind index
```

- Edit canonical curriculum entities in [`schema/`](./schema/), then run the
  generator; do not hand-edit generated `src/data/*.ts` files.
- Read [`CONTRIBUTING.md`](./CONTRIBUTING.md) before changing curriculum prose,
  capstones, or the 108-week spine.
- Review the [technical audit](./docs/AUDIT.md) and [architecture decisions](./docs/ARCHITECTURE.md)
  when a change crosses schema or generator boundaries.

---

## License

Apache-2.0. See [`LICENSE`](./LICENSE).

**This is an apprenticeship with valuable stopping points—not a promise that
every learner must finish all 108 weeks. Start with one artifact.**

[Start with Week 1 →](https://sethuiyer.github.io/tensor-to-tenant/curriculum/)
