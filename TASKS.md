# TASKS.md — `tensor-to-tenant` hardening backlog

> Living document. Re‑prioritize as work lands.
> Everything below was identified during the 2026‑01 deep‑research pass.
> Sprint for tomorrow = **T1.4.b/c/d + T1.13** (see Suggested execution order).

---

## How to read this

- **P0** — do these next. They're cheap, low‑risk, and unblock everything else.
- **P1** — should land this month. Larger moves but the design space is already clear.
- **P2** — design work + larger refactors. Worth a design doc before coding.
- **P3** — organizational / community. No code yet, but the seeds matter.

Each task lists **files touched**, **verification**, and **acceptance** so it's
executable without re‑asking the same questions.

---

## Guiding principles (durable — survive any task list)

These are the design north stars. Every PR, every paper decision, every schema
edit should be checkable against them. They outlive the schema work, the
refactors, and the tooling churn.

### P‑principle 1 — The seam philosophy

Every elegant algorithm is introduced together with the operational detail
that tries to kill it.

The course does not teach "cosine similarity = `dot(a, b)`." It teaches that
`dot(a, b)` is the *interview* answer; the *production* answer starts when
100M vectors do not fit in RAM and you need HNSW, IVF‑PQ, quantization,
sharding, and admission control. The eight canonical seams:

| Algorithm / idea | Interview answer | Operational reality that breaks it | What the course teaches instead |
|---|---|---|---|
| Cosine similarity | `dot(a, b) / (‖a‖ · ‖b‖)` | 100M vectors don't fit in RAM | HNSW, IVF‑PQ, quantization, sharding — it's a systems problem |
| Calibration | Brier / ECE | Global 0.92 hides slice‑level 0.6 on long‑tail queries | Slice evals, not a single aggregate metric |
| Retries | Exponential backoff | Retrying a payment double‑charges the customer | Idempotency keys, exactly‑once, outbox pattern |
| Streaming | SSE / WebSockets | Client disconnects mid‑token, upstream fails after 800 tokens | Partial failure handling, resume tokens, append‑only ledger |
| Mo's algorithm | Sort queries by block | Add/remove must be reversible & O(1); tie‑break on original ID, not compressed index; mode isn't mergeable across shards | State management, not an algorithm |
| DSU‑on‑Tree | Small‑to‑large | Tree becomes mutable (reparenting); query becomes path (u→v); subtree is split across shards | Euler Tour Tree / Link‑Cut for mutation; HLD for paths; full frequency map for sharded mode |
| PagedAttention | KV cache paging | All‑to‑all in MoE dominates; prefill and decode have different SLOs | Warp Decode, COMET overlap, prefill/decode disaggregation (Week 90 exists because of this seam) |
| Multi‑tenancy | Per‑tenant rate limit | Fairness vs billing vs noisy neighbor vs cost attribution all collide | Quotas, PII‑safe tracing, cost model, tenant isolation, leader election |

**The Level framing** (use this when triaging what to teach deeply):

- **Level 1** — "I have heard of X."
- **Level 2** — "I can implement X." (Mo's, DSU on Tree, PagedAttention, CRAG.)
- **Level 3** — "I know when X breaks and what replaces it." (Elegance dies on contact with product requirements. You don't get Level 3 from a lecture — you get it from being forced to ship the thing that kills your pretty algorithm.)

The seam philosophy is the reason Week 90 exists. The seam philosophy is the
reason the three capstones exist. The seam philosophy is the reason the course
is 108 weeks instead of 12.

### P‑principle 2 — The paper selection rule

> **Add papers that change how the learner thinks about a system, not papers
> that merely introduce another model.**

Every paper added to the canonical list (see T1.8) must pass this filter. The
default answer to "should we add this paper?" is **no**, unless the paper
exposes a *structural mistake* in the naive version of an idea the course
already teaches. A paper that introduces a fancier model is archive material.
A paper that exposes a hidden correctness or evaluation problem in a system
the course builds is core material.

### P‑principle 3 — Local relevance ≠ global correctness

The most important claim in the curriculum:

> Independently relevant chunks may not form sufficient evidence.
> Independently useful tools may not form a useful toolset.
> Independently retrieved memories may not preserve temporal truth.

This is the single sentence behind the three absolute must‑add papers in T1.8
and behind the RAG, agents, and memory weeks in Phase 7. It is the
operational form of P‑principle 1.

### Where these principles live

- This section is canonical. Do not move or rewrite it without the author.
- **P‑principle 1** is also reflected in the Week‑level `Mode` column
  (`implement` / `read_diagram` / `deploy_benchmark`) and in every Capstone
  pitfalls index.
- **P‑principle 2** is operationalised in T1.8 (paper curation) and T1.6
  (drift check, which should be able to flag a paper that violates the rule
  if the schema records the `selection_rationale` field).
- **P‑principle 3** is the headline of the three must‑add papers and the
  thesis statement of Capstones 1 and 2.

---

## P1 — schema + tests + drift (this month)


---

---

## Status

**All tracked tasks done as of 2026-08-06.** Schema spine + depth layer
complete. Test suite: 167 passing. Site builds clean. Drift check
passes. The 108-week curriculum is fully schema-driven end-to-end.

Phase log:

- **Phase 1** (infrastructure): `b5e23f4` — P0 cleanup + forgetting.py tests + CI
- **Phase 2** (curriculum enrichment): `8b32a05`, `9831bb1` — paper curation, TensorTonic integration, Level 3 questions, serving-stack infographic
- **Phase 3** (cookiecutter + institution): `feb7a32`, `97cde2e`, `83c7c5e` — test coverage, T1.13 audit, institution layer
- **Phase 4** (schema migration + depth layer):
  - `b9f1bd2` T1.2 schema entities
  - `002df84` T2.5 site search
  - `75f11f2` T1.3 generators + T1.4.e/f + T1.6 + T1.7 + T1.12
  - `3eed1cc` T2.1-T2.4 + T2.6

**Remaining work** (none tracked in this doc): see `docs/AUDIT.md` for the
1 FLAGGED-FOR-HUMAN item (paper citation accuracy), and
`docs/ARCHITECTURE.md` ADRs for deferred decisions (L100 cap fix,
cookiecutter extraction, schema formalization with Pydantic v2).


## Out of scope (for now)

- **Replacing the OpenRouter default model.** It's a `OPENROUTER_MODEL` env var, swap‑per‑learner. No code change needed.
- **Replacing the Astro site with Next/Remix/etc.** No functional reason to.
- **Hosting the live Darbar catalog here.** It's hosted at `aninokuma.codeberg.page/leetcode-darbar/` by design (split repo).
- **Translating the README.** Nice‑to‑have, separate effort.
- **Adding Discord/Matrix.** Organizational, not technical, and explicitly out of scope per the FAQ.

---

*Last updated: 2026‑08 (execution order reprioritized — content frozen).*
*Owner: @sethuiyer.*
*Status: ready for sprint planning.*
