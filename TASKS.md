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

### T1.1 Pick the canonical schema format and tool

- **Files:** new `schema/` directory at repo root; new `schema/README.md` design note.
- **Decision (RESOLVED 2026-08):** **YAML files + Pydantic v2 models.**
  - YAML is human‑diff‑friendly, survives without Python installed.
  - Pydantic v2 gives validation + IDE autocomplete + JSON Schema export (which generates the TS types).
  - The cookiecutter generator already imports Python; loading YAML in Pydantic is one import.
  - The `schema/` directory already exists and uses YAML as the working format (per `schema/README.md`); this decision ratifies that choice rather than revisiting it.
- **Sub‑questions (RESOLVED):**
  - **Scope:** move only the *structured subset* into the schema (weeks/gates/mandalas/forge/darbar/agents/math/system-design/engineering/interview/resources). The free-form prose in `CAPSTONE.md` / `MANDALA.md` stays as authored Markdown files that reference the schema by ID.
  - **Images:** live in `public/images/` and are linked from the site via `url()` — no duplication.
- **Acceptance:** `schema/README.md` (already exists) declares the format. Pydantic v2 models land as part of T1.2 / T1.3 when the schema entities are written.

> **Note for the executor:** this decision was pre-authorized because it is the obvious
> default given the existing `schema/*.yaml` files. Do not re-litigate the format
> choice; proceed directly to T1.2.

### T1.2 Define the schema entity set

- **Files:** `schema/*.yaml` + `schema/models.py` (Pydantic).
- **Initial entities (one YAML file per entity type):**
  - `phases.yaml` — 10 phases
  - `weeks.yaml` — 108 weekly entries with `{week, phase, module, focus, mode, deliverable, forge_tier, forge_topic, recovery_after?}`
  - `gates.yaml` — 10 milestone gates
  - `programs.yaml` — 3 stackable programs
  - `mandalas.yaml` — 16 mandalas
  - `math_tracks.yaml` — 10 tracks × 10 modules
  - `forge.yaml` — lanes + bosses + coverage matrix
  - `darbar.yaml` — patterns + catalog summary + categories
  - `engineering.yaml` — 30 tasks + 40 drills
  - `system_design.yaml` — weeks + patterns + families + cases
  - `agents.yaml` — 18 modules + 7.5 + bridge rows + Manus capstone
  - `interview.yaml` — CARL stories + 176‑item roadmap + completion levels
  - `resources.yaml` — videos/books/papers/blogs
  - `prerequisites.yaml` — 9 resources + 36‑week plan
- **Acceptance:** every `src/data/*.ts` file has a corresponding `schema/*.yaml` source. Pydantic models validate the YAML at import time.

### T1.3 Write the generators (schema → site + cookiecutter)

- **Files:** new `tools/generate.py` (or `scripts/build_site.py` + `scripts/build_cookiecutter.py`).
- **Detail:** generators that read `schema/*.yaml` and emit:
  1. `src/data/*.ts` (typed, ready to import) — wire into Astro via a prebuild hook or run on `npm run build`
  2. `cookiecutter/hooks/post_gen_project.py` constants (`PHASE_1..10`, `AGENT_MODULES_CC`, `BRIDGE_SUMMARY_CC`, etc.) — emit as a Python module the hook imports
  3. (optional) Markdown sections that include schema‑derived tables — useful for the `ALGORITHMIC_FORGE.md` lane map and the `README.md` "Full 108‑Week Curriculum" table
- **Acceptance:** running `python tools/generate.py` regenerates all of the above from `schema/*.yaml` byte‑for‑byte equivalent to current `src/data/*.ts` (the drift test in T1.4 enforces this going forward).

### T1.4 Add the test suite

- **Files:** new `tests/` at repo root; new `pyproject.toml` at repo root (separate from the cookiecutter's).
- **Sub‑tasks:**
  - **T1.4.b** — (done; see commit `feb7a32`. 49 concept_seed tests live in `tests/test_concept_seed.py`.)
  - **T1.4.c** — (done; see commit `feb7a32`. 30 battle tests live in `tests/test_battle.py`.)
  - **T1.4.d** — (done; see commit `feb7a32`. 13 e2e render tests live in `tests/test_end_to_end_render.py`. The post-gen hook now also seeds `journal/memory.json` with 324 concepts per the T1.13 audit fix.)
  - **T1.4.e** — **drift test**: after `tools/generate.py` runs, hash every emitted `src/data/*.ts` and `cookiecutter/.../PHASES` constant block; compare against committed reference hashes. Mismatch → fail.
  - **T1.4.f** — **site build test**: `npm run build` must succeed. Astro emits to `dist/`; check for any broken `url()` references.
- **Acceptance:** `pytest` exits 0 from the repo root, no skipped tests, ≥ 80% line coverage on the cookiecutter's pure‑Python modules.

### T1.6 Drift check between canonical curriculum and website

- **Files:** `tests/test_drift.py`, possibly a new `tools/drift_report.py`.
- **Detail:** for each curriculum fact that appears on the site AND in the schema, assert equality. The site is the rendered output of the schema, so the check is structural, not visual:
  - Every week in `schema/weeks.yaml` has a row in `src/data/weeks.ts`.
  - Every gate in `schema/gates.yaml` has a row in `src/data/gates.ts`.
  - Every phase ID in `weeks.yaml` exists in `phases.yaml`.
  - Every mandala ID referenced by a phase exists in `mandalas.yaml`.
  - The 108 count, the 10‑phase count, the 10‑gate count, the 3‑program count are all consistent.
- **Acceptance:** a CI job fails when you add a new week without bumping `MODE_COUNTS` in `weeks.ts`, or when you rename a phase ID without updating its dependents.

### T1.7 Eliminate the old hand‑written data sources

- **Files:** `src/data/*.ts` (rewrite), `cookiecutter/hooks/post_gen_project.py` (replace constants with import from generated module).
- **Detail:** once T1.3 + T1.4 land, the hand‑written arrays in `post_gen_project.py` (`PHASE_1..10`, `AGENT_MODULES_CC`, `BRIDGE_SUMMARY_CC`, `MANDALAS_CC`, `PREREQUISITES`, `PREREQ_PLAN`, `FORGE_LANES`, `FORGE_BOSSES`, `RECOVERY_AFTER`, `RELEASES`, `AGENT_PAPERS_CC`, `AGENT_PAPER_WEEKS`) and the hand‑written `src/data/*.ts` content become *generated* files.
- **Acceptance:** no curriculum fact is written by hand in two places; the cookiecutter hook and the site both import from a single generated source.

> **Coordination note for the executor:** the T1.13 audit
> (`tools/audit.py`) verifies *hand-written* `src/data/*.ts` files
> against the canonical markdown and schema. When T1.7 replaces those
> hand-written files with *generated* ones, the generated output may
> differ in wording from the originals (even whitespace) and the
> audit's text-match assertions may start failing. **Re-run
> `tools/audit.py` after T1.7 lands** and expect ~25 findings / 24
> VERIFIED. If the count drops, the generator is producing output the
> audit doesn't recognize — investigate before merging. The fix, if
> needed, is to update the audit's expected text to match the
> generator's output, not to suppress the check.

### T1.12 Parallel track — Tool recommendation systems (SEARCH.md + SNOWFLAKE.md)

> **Dependency:** blocks on **T1.2** (the schema entity-set decision
> defines how SEARCH/SNOWFLAKE get catalogued — specifically
> `schema/deep_dives.yaml` per T1.12.j). T1.1 (format decision)
> does *not* unblock T1.12 on its own; the entity-set decision is what
> tells the executor how to model the track. Don't start T1.12 right
> after T1.1 — wait for T1.2.

> Local artifacts:
> <SEARCH.md> · <SNOWFLAKE.md>. Both live in the repo root as of this
> task and are not yet referenced from any page, schema entry, or
> cookiecutter scaffold.

A polished two-part deep-dive on building a multi-signal recommendation
engine: **SEARCH.md** introduces the math (graph traversal, hop decay,
Adamic–Adar, IDF weighting, type affinity, dynamic thresholds,
multi-signal combination); **SNOWFLAKE.md** implements the same theory
in production Snowflake SQL using `AI_EMBED`, recursive CTEs, IDF
via `LN((N+1)/(df+1))`, weighted Adamic–Adar, dynamic thresholds
via `PERCENTILE_CONT`, and Streams + Tasks for incremental refresh.

The pair is exactly the **seam philosophy in a single domain**:
SEARCH.md is the Level 2 (the math); SNOWFLAKE.md is the Level 3
(the math dies on contact with `AI_EMBED` permissions, recursive-CTE
cycle prevention, Cortex Search latency, and Snowflake credit burn).

#### T1.12.a — Why this earns a parallel track, not spine additions

The 108-week spine is already at capacity:

- 30 engineering tasks + 40 timed practice drills (Phase 4)
- Algorithmic Forge (every Friday, four tiers)
- 200 TensorTonic implementation problems (T1.10)
- 100 math modules across 10 tracks
- Leetcode Darbar (548 slots)
- GenAI Agents track (18 modules + Module 7.5 + Manus)
- Three capstones

Adding another batch of spine items would crowd what is already a
dense schedule. A *parallel track* — self-contained, opt-in, with its
own reading order — is the right shape. Same pattern as the existing
Algorithmic Forge, System Design Track, Leetcode Darbar, and GenAI
Agents track: a learner finishes one of those tracks *alongside* the
spine without the spine needing to acknowledge it.

The recommendation engine content is dense enough (≈57 KB across two
files, 41 numbered sections between them, 17 named mathematical
primitives) to stand alone as a track rather than being folded in.

#### T1.12.b — Mapping to spine weeks (where these become load-bearing)

| SEARCH.md / SNOWFLAKE.md primitive | Spine week(s) | Level | Why it earns the cross-reference |
|---|---|---|---|
| Cosine similarity (with normalization) | W31 (Retrieval math) | 2 | The vector-search primitive the curriculum currently states as `dot(a,b)` and only implies the operational reality behind. |
| Length-weighted pooling | W36 (Text chunking), W77 (Retrieval fusion) | 2 | The chunk-aggregation strategy the curriculum names but never formalizes. |
| Graph traversal + hop decay | W77 (Retrieval patterns), W81 (Agent foundations) | 3 | Agent tool graphs ARE the recommendation graph; hop decay IS the relevance-vs-precision knob. |
| Adamic–Adar + hub defence | W81 (agents sharing tools), W97 (Quotas/priority) | 3 | Rare shared neighbours weigh more than popular ones — same principle as quota-priority for unpopular tenants. |
| IDF weighting | W36 (chunking), W78 (retrieval eval) | 2 | The reason "postgresql" matches harder than "API" — the curriculum's lexical weeks should know this. |
| Intent signals + type affinity | W97 (quotas), W94 (router) | 3 | The router that picks between MQA/GQA/MLA and the quota that picks between tenants are both type-affinity matrices. |
| Dynamic noise-floor filtering | W86 (vLLM metrics), W78 (eval) | 2 | Eval weeks should not use fixed cutoffs; SEARCH.md Section 9 derives the right thresholding policy. |
| Multi-signal combination | Capstone 3 (OpenRouter gateway), W94 | 3 | The gateway capstone *is* a multi-signal router — Capstone 3's failure-injection matrix is the production version of SEARCH.md Section 14. |
| Telemetry-based reranking | W68 (Monitoring), Capstone 3 | 3 | The reward function in SEARCH.md Section 15 is the literal instrumentation surface for an LLM gateway. |
| Evaluation discipline (Recall@K, MRR, NDCG, diversity) | W39 (Ranking metrics), W78 | 2 | The spine already names these metrics but does not derive the operational meaning of each. |

Net: **every SEARCH.md primitive has a spine week where it becomes
load-bearing, and SNOWFLAKE.md's implementation surfaces are exactly
the schema discipline the spine is missing.**

#### T1.12.c — The paired-reading structure

Per T1.11's third-party discipline (and consistent with T1.8.g / T1.8.i's
MOPD-paper-plus-companion-video pattern), the two artifacts ship as a
**paired reading unit** with a fixed order:

```
READING ORDER (Level 2 → Level 3):

1. SEARCH.md   (~30 min skim, ~2 hr full read)
   - Establish the math: graph, embedding, hop decay,
     Adamic-Adar, IDF, type affinity, dynamic threshold,
     multi-signal combination, evaluation discipline.

2. SNOWFLAKE.md   (~45 min skim, ~3 hr full read)
   - Apply the math: AI_EMBED + VECTOR, recursive CTE
     cycle prevention, weighted Adamic-Adar, min-max
     normalization, PERCENTILE_CONT, Streams + Tasks,
     Cortex Search production serving.
```

The pair is **inseparable** in the schema: a learner is allowed to
read SEARCH.md alone (math is general), but reading SNOWFLAKE.md
without SEARCH.md first is incoherent (the SQL implements specific
equations). The pair_id field in `schema/deep_dives.yaml` enforces this.

#### T1.12.d — Schema additions

New schema entity: `schema/deep_dives.yaml`. Tracks are peer to the
existing `tracks` (Phase 4–9 spine tracks) but explicitly *not* part
of the spine — they live alongside, with their own progression.

```yaml
# schema/deep_dives.yaml

- id: tool_recommendation_systems
  title: "Tool Recommendation Systems"
  short_name: "recommender"
  parallel_track: true              # explicit: not part of the spine
  primary_artifacts:
    - { id: search_md,   path: "SEARCH.md",   role: theory    }
    - { id: snowflake_md, path: "SNOWFLAKE.md", role: production }
  pair_enforcement: strict         # cannot reference SNOWFLAKE.md without SEARCH.md
  tier: optional
  level: 2                         # SEARCH.md teaches Level 2; SNOWFLAKE.md teaches Level 3
  seam: "multi-signal recommendation over graph + embedding + metadata"
  selection_rationale: >
    The pair is the seam philosophy applied to recommendation systems.
    SEARCH.md introduces the elegant math (graph traversal, hop decay,
    Adamic-Adar, IDF, type affinity, dynamic thresholds, multi-signal
    combination) — Level 2. SNOWFLAKE.md implements the same theory
    in production Snowflake SQL and exposes where the math dies on
    contact with AI_EMBED permissions, recursive-CTE cycle prevention,
    Cortex Search latency, and Snowflake credit burn — Level 3. The
    spine covers every primitive implicitly (W31, W36, W39, W77, W78,
    W81, W86, W94, W97) but never formalizes the combination. This
    parallel track makes the combination load-bearing.
  load_bearing_for:
    - { week: 31,  primitive: "cosine similarity + length-weighted pooling" }
    - { week: 36,  primitive: "IDF-weighted token scoring" }
    - { week: 39,  primitive: "Recall@K, MRR, NDCG evaluation" }
    - { week: 77,  primitive: "graph traversal + hop decay" }
    - { week: 78,  primitive: "dynamic noise-floor filtering" }
    - { week: 81,  primitive: "Adamic-Adar for tool graph" }
    - { week: 86,  primitive: "operational telemetry into ranking" }
    - { week: 94,  primitive: "multi-signal router" }
    - { week: 97,  primitive: "type affinity for tenant policies" }
    - { capstone: 3, primitive: "OpenRouter gateway as multi-signal recommender" }
  cross_references:
    - { track: "agents",      role: "shares agent-tool graph model" }
    - { track: "darbar",      role: "shares Recall@K / MRR evaluation" }
    - { track: "forge",       role: "shares graph-traversal algorithmic depth" }
    - { capstone: 3,            role: "shares multi-signal routing pattern" }
```

Plus the per-artifact entries (each tracks its own schema discipline):

```yaml
- id: search_md
  title: "SEARCH.md — Multi-signal recommendation math"
  path: "SEARCH.md"                # local path; schema supports local artifacts
  size_kb: 25
  tier: optional
  level: 2
  section_count: 17
  pair_id: tool_recommendation_systems
  pair_role: theory
  selection_rationale: >
    Level 2 treatment of the recommendation math: graph representation,
    cosine + length-weighted pooling, hop decay with multiplicative
    path score, Adamic-Adar with hub defence, IDF weighting with worked
    example, intent boosting with type affinity, dynamic noise-floor
    filtering, multi-signal combination with worked example, priority
    and confidence mapping, 10-step pipeline, pseudocode, five
    production problems (double-counting, popularity bias, graph drift,
    query ambiguity, threshold instability), telemetry-based weight
    learning, evaluation across retrieval/ranking/diversity/operational
    success, and a final "core intuition" paragraph that articulates
    "no single signal wins, the combination wins." The pseudocode is
    implementable, not aspirational. The math is correct (1/log deg(z)
    Adamic-Adar, 1/(h+1) hop decay, IDF smoothing with alpha=1).
  cross_references: [...]         # same week mapping as parent

- id: snowflake_md
  title: "SNOWFLAKE.md — Production Snowflake implementation"
  path: "SNOWFLAKE.md"
  size_kb: 32
  tier: optional
  level: 3
  section_count: 24
  pair_id: tool_recommendation_systems
  pair_role: production
  prerequisite_of: search_md      # SNOWFLAKE.md assumes SEARCH.md read first
  selection_rationale: >
    Level 3 implementation: the math dies on contact with AI_EMBED
    permissions, recursive-CTE cycle prevention, Cortex Search latency,
    and Snowflake credit burn. 24 sections of production SQL — schema
    design (entities, edges, type affinity, tokens, term stats),
    Cortex embedding via AI_EMBED, recursive-CTE graph walk with
    cycle prevention via POSITION, weighted Adamic-Adar, min-max
    normalization across heterogeneous score ranges, dynamic
    threshold via PERCENTILE_CONT, Cortex Search for low-latency
    serving, and Streams + Tasks for incremental refresh. The
    opening line ("this is where the elegant math puts on a hard hat
    and becomes data plumbing") is the seam philosophy stated as a
    meme. The "Snowflake credits will begin performing Adamic-Adar
    directly on your bank account" line is the credit-economics lesson
    the curriculum should teach at W93.
  cross_references: [...]         # same week mapping as parent
```

#### T1.12.e — Drift enforcement (extends T1.6 / T1.8.f / T1.11.e)

- Every entry in `schema/deep_dives.yaml` with `parallel_track: true`
  must have a `primary_artifacts` list with at least one
  `role: theory` and one `role: production` artifact. A track with
  only theory is a paper, not a parallel track.
- A `production`-role artifact must declare a `prerequisite_of` pointing
  at the `theory`-role artifact in the same pair. Drift fails if a
  production artifact is added without its theory prerequisite.
- A `theory`-role artifact must declare a `pair_id`. Drift fails if an
  entry is added to `deep_dives.yaml` with a `path` but no `pair_id`.
- Local artifact entries (those with `path` instead of `url`) must
  have the file verified to exist at CI time. CI fails if a `path` in
  `schema/deep_dives.yaml` does not resolve in the repo.

#### T1.12.f — Site additions

The Astro site gets a new page at `/recommendation/` (or
`/recommender/`) modeled after `/agents/`:

- `src/pages/recommender.astro` — page header, paired-reading intro,
  per-section card (SEARCH.md → SNOWFLAKE.md), cross-reference table
  to spine weeks, optional-depth callout.
- Update `src/config.ts → SITE.programs` to include "Recommender" as a
  fourth parallel program (alongside Foundations / Engineering + Systems
  / LLM Platform).
- Update `src/layouts/BaseLayout.astro` nav to add "Recommender" link.
- Add a serving-stack / recommender-pipeline image similar to the
  capstone infographics (T1.11.a.1 introduced the serving stack
  diagram; the recommender pipeline diagram from SNOWFLAKE.md Section
  24 is a natural fit).

#### T1.12.g — Cookiecutter additions

The generated learner repo gains:

```text
09_interview/recommender/          # parallel to 09_interview/agents/
├── README.md                      # paired-reading intro
├── SEARCH.md                      # symlink or copy at scaffold time
├── SNOWFLAKE.md                   # symlink or copy at scaffold time
├── progress.md                    # per-section completion log
└── exercises/                     # optional: implement one SEARCH.md section per week
```

The `make status` command extends to print recommender progress
alongside the existing Darbar, Forge, and Implementation-Exercise
counters.

#### T1.12.h — The pair-enforcement principle (durable)

> Every deep-dive track that earns its way into the curriculum must
> ship as a **paired reading unit**: a `theory` artifact that introduces
> the math, and a `production` artifact that implements it on a
> concrete platform and exposes where the math breaks.

This is the deep-dive equivalent of P-principle 2 (selection filter)
plus P-principle 3 (Level 2 vs Level 3 framing). Future candidates for
the deep-dives track must pass both:

- **Selection filter:** does the theory build a muscle the course uses?
- **Pair enforcement:** does a production artifact exist that exposes
  where the theory dies? If only a theory exists, it's a paper and
  belongs in `resources.yaml`, not in `deep_dives.yaml`.

This prevents the deep-dives track from becoming "another reading list
of papers." Every entry must be a pair.

#### T1.12.i — Acceptance

- `schema/deep_dives.yaml` exists with at least the tool recommendation
  pair (parent + two children), each with full `selection_rationale`,
  `cross_references`, and `pair_id` (or `prerequisite_of`).
- The file `SEARCH.md` and `SNOWFLAKE.md` are referenced from
  `schema/deep_dives.yaml` via `path` entries that resolve in the
  repo at CI time.
- A new site page `/recommender/` (or `/recommendation/`) exists,
  rendered from the same data, with the paired-reading intro, the
  cross-reference table, and a link from the site nav.
- The cookiecutter generates `09_interview/recommender/` with the two
  artifacts copied or symlinked and a `progress.md` scaffold.
- `make status` (in the generated repo) reports recommender completion
  percentage.
- The drift check from T1.12.e fails loudly if a new deep-dive is
  added without a pair, or if a production artifact is added without
  its theory prerequisite.
- The README's existing parallel-track language is updated to include
  the Recommender track alongside Forge, Darbar, and Agents.

#### T1.12.j — Open question (recorded, not blocking)

SNOWFLAKE.md uses the database name `CTX_DB` and schema `RECOMMENDER`,
suggesting the user's own implementation is named "CTX Recommender" or
similar. If the curriculum adopts this pair as canonical, decide
whether:

- (a) The track is named generically ("Tool Recommendation Systems")
  and the user's "CTX" name is treated as one possible instantiation.
- (b) The track adopts the user's "CTX Recommender" name to credit the
  authorship and stay concrete.

Recommendation: **(a)**. Generic naming scales to future
recommendation-system deep-dives (e.g., a "Vector Database Internals"
pair could be a different track). The user's "CTX" naming is a
specific implementation; the track is a pattern.

This decision can be revisited when T2.6's schema-validation work
lands, but for now the schema entry uses the generic name.

### T2.1 Make the capstones also schema‑driven where possible

- **Files:** new `schema/capstones/*.yaml`, possibly generated into `src/pages/capstones/*.astro` frontmatter.
- **Detail:** the three capstones have structured artifacts (the Mo's coding problem has `events`, `queries`, `expected`; the DSU problem has `tree`, `queries`, `expected`; the AI gateway has `failure_matrix`, `interview_questions`, `rubric`). These could be schema entries that drive both the prose‑heavy `CAPSTONE*.md` files (cross‑referenced) and the page‑level tables.
- **Acceptance:** the failure‑injection matrix in Capstone 3 is generated from a YAML list, not hand‑written twice in `CAPSTONE3_OPENROUTER.md` and `src/pages/capstones/ai-gateway.astro`.

### T2.2 Schema‑validate the site content at build time

- **Files:** add a prebuild step to `package.json`.
- **Detail:** run `tools/generate.py` as a prebuild step in `npm run build`. Fail the build if the schema doesn't round‑trip through the generators cleanly. This means a stale `src/data/*.ts` is *impossible* — Astro always builds from freshly generated files.
- **Acceptance:** `npm run build` runs the generators first, fails loudly if the schema is invalid, and emits a `dist/` derived from the validated schema.

### T2.3 Schema‑driven bridge generation

- **Files:** `schema/agents.yaml` extends with bridge rows.
- **Detail:** the `AGENT_BRIDGE_CC` table in `post_gen_project.py` and the `AGENT_BRIDGES` array in `src/data/agents.ts` are 1:1 duplicates of each other and of the rendering on `/agents/`. Pull all of them into the schema.
- **Acceptance:** adding a new agent module + 4 bridge rows in `schema/agents.yaml` regenerates the cookiecutter, the site data, and the rendered `/agents/` page from one edit.

### T2.4 A schema‑aware `learning_partner.py`

- **Files:** the cookiecutter's `learning_partner.py` (already shipped), plus optional new `tools/sync_partner_prompt.py`.
- **Detail:** the partner's system prompt is the `AGENTS.md` content. If `AGENTS.md` references week IDs or gate IDs, they should be validated against the schema at cookiecutter generation time — currently the prompt references weeks like "Week 14" without any check that "Week 14" is a valid week in the schema.
- **Acceptance:** a build‑time assertion confirms every referenced week/gate ID in `AGENTS.md` exists in the schema.

### T2.5 Add a minimal site search

- **Files:** new `src/pages/search.astro` or new `src/scripts/search-index.ts`.
- **Detail:** **independent of the schema spine** — does not block on T1.1–T1.7.
  Two viable approaches:
  - **Approach A (recommended, ~1 hr):** read directly from the existing
    `src/data/*.ts` files at build time, build a JSON index, ship as
    a tiny client-side filter. No external dependency.
  - **Approach B (~30 min, lower polish):** skip the filter UI; ship a
    `/search/` page that renders the index as a flat list with browser
    `Ctrl+F` as the search mechanism.
- **Acceptance:** `/search/` renders, returns results for "Euler", "SVD",
  "PagedAttention", "MCP" within ~50 ms.

> **Note for the executor:** this task was previously misclassified as
> deferred. It is independent of the schema work and can run right now
> in parallel with T1.1–T1.7. If a second executor is available, this
> is the natural parallel work.

### T2.6 Build verification: schema → site → cookiecutter in one CI job

- **Files:** extend `test.yml`.
- **Detail:** the pipeline becomes `validate schema → generate site data → build site → generate cookiecutter data → render cookiecutter in /tmp → pytest → diff against snapshots`. If any step fails, the PR is red.
- **Acceptance:** a single green check confirms the whole pipeline is healthy.

---

---

## Suggested execution order

> **Reprioritized 2026-08 — curriculum content is declared fixed.** Drift
> prevention no longer drives the order. The critical path is now: (1) prove
> the artifact learners actually receive is correct (cookiecutter tests),
> (2) verify the frozen content is technically sound (independent audit,
> T1.13), (3) build the institution layer (T3.x). The schema migration
> (T1.1/T1.2/T1.3/T1.6/T1.7) and the depth layer (T2.1–T2.6) are optional
> hardening — do them only when the above is green or if curriculum edits
> resume.

**Phase 1 (done, commit `b5e23f4`):**
- T0.1 — `__pycache__` cleanup
- T0.2 — `dist/` decision (no-op; already gitignored)
- T0.3 — `CONTRIBUTING.md`
- T0.4 — `CODEOWNERS`
- T1.4.a — `forgetting.py` unit tests (49 passing, latent L100 cap bug pinned)
- T1.5 — wire CI to run the tests

**Phase 2 (done, commits `8b32a05` + `9831bb1`):**
- T1.8 — paper curation (schema/resources.yaml, 14 papers + 1 video companion)
- T1.9 — curriculum coverage implementation (4 surgical edits to weeks.ts)
- T1.10 — TensorTonic integration (schema/implementation_exercises.yaml + cookiecutter scaffold)
- T1.11 — third-party assessment implementation (schema/interview_questions.yaml + serving-stack.webp + curriculum.astro reveal)
- Serving-stack infographic (Phase 8 spotlight, no tracked task — user-designed)

**Phase 3 (done, commits `feb7a32` + `97cde2e` + `83c7c5e`):**
- T1.4.b — `concept_seed.py` tests (49 passing in `tests/test_concept_seed.py`)
- T1.4.c — `battle.py` tests (30 passing in `tests/test_battle.py`)
- T1.4.d — end-to-end cookiecutter render test (13 passing in
  `tests/test_end_to_end_render.py`; also fixed the post-gen hook to
  seed `journal/memory.json` with 324 concepts per the T1.13 audit)
- T1.13 — independent technical audit (`tools/audit.py` + `docs/AUDIT.md`;
  24 VERIFIED + 1 FLAGGED-FOR-HUMAN + 0 FAIL)
- T3.1 — reviewer policy (`docs/REVIEWERS.md`)
- T3.2 — issue templates (`.github/ISSUE_TEMPLATE/curriculum_review.md`
  and `drift_report.md`)
- T3.3 — drift dashboard scaffold (`docs/DRIFT.md`; the full drift
  check is T1.6, not yet implemented)
- T3.4 — completion story file (`COMPLETIONS.md` placeholder)
- T3.5 — cookiecutter extraction decision (ADR in `docs/ARCHITECTURE.md`;
  deferred until T1.3 makes the cookiecutter a true downstream consumer)

**Phase 4 (optional hardening — only when Phase 3 is green or if edits resume):**

Total: 14 execution items across 13 task headers (T1.4's two remaining sub-tasks e and f are listed separately; all other parent tasks are single-item).

**Active schema spine (7 items; T1.1 is pre-authorized so the executor does not stall):**

- **T1.1** — schema format decision note (RESOLVED 2026-08: YAML + Pydantic v2; see task body)
- **T1.2** — define schema entities (one YAML per surface)
- **T1.3** — write the generators
- **T1.4.e** — drift test
- **T1.4.f** — site build test
- **T1.6** — drift check between schema and site
- **T1.7** — eliminate hand-written sources (re-run audit after this lands)

**Independent of schema (2 items; run in parallel with anything):**

- **T1.12** — tool recommendation systems parallel track (blocks on T1.2's entity-set decision, not T1.1)
- **T2.5** — minimal site search (no schema dependency; ~1 hr)

**Depth layer (5 items; all depend on T1.2 + T1.3):**

- **T2.1** — capstones schema-driven
- **T2.2** — schema-validate site content at build time
- **T2.3** — schema-driven bridge generation
- **T2.4** — schema-aware `learning_partner.py`
- **T2.6** — one CI job (depends on T2.2)

> **Order matters:** T1.4.b/c/d are independent of each other and fast — the
> only remaining "P0-ish" correctness work, and they protect the artifact a
> learner receives. T1.13 (audit) is the highest-leverage correctness check
> left: content is frozen, so there is no future edit to rescue a wrong claim.
> T3.1–T3.5 are the institution layer and are deliberately pulled ahead of the
> schema spine — with content fixed, drift prevention no longer pays for
> itself, but reviewer policy, issue templates, a drift report, and a
> completion story compound. The schema spine (T1.1/T1.2/T1.3/T1.6/T1.7) and
> the depth layer (T2.1–T2.6) are optional hardening; run them only when the
> artifact is proven correct and the institution layer is in place, or if
> curriculum edits resume.

---

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
