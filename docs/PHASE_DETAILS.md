# Phase detail notes

> Small implementation notes preserved from the former README. Phase themes and
> week-level deliverables remain schema/site-backed; these notes explain the
> learner-repo contracts that are easy to lose in a summary table.

## Phase 1 — orientation, tooling, and diagnostics (Weeks 1–6)

**Objective:** build the operating system for the next 108 weeks.

**Outcomes:** a course repo, weekly tracker, notes system, Python environment
with testing/linting, a Docker starter service, and a math + systems diagnostic
report.

**Habits:** weekly plan, weekly retrospective, one repo, and one Markdown file
per week.

## Phase 4 — engineering primitives (Weeks 31–45)

The reusable library is intentionally separated by production seam. Its
preserved package layout and legacy prompt bank live in
[`../ENGINEERING_TASKS.md`](../ENGINEERING_TASKS.md); use the
[engineering hub](https://sethuiyer.github.io/tensor-to-tenant/engineering/)
for the current structured index.

## Phase 5 — system design and distributed systems (Weeks 46–57)

Every design must include requirements, API, data model, scale plan, failure
modes, trade-offs, and an AI extension. The canonical sequence is
[`../SYSTEM_DESIGN_TRACK.md`](../SYSTEM_DESIGN_TRACK.md).

## Phase 7 — LLM training, RAG, agents, and evaluation (Weeks 70–81)

The phase moves from model/data concepts through retrieval, slice evaluation,
prompt management, memory, tool calling, and agent harnesses. The optional
agent bootcamp bridge is [`AGENT_BRIDGE.md`](./AGENT_BRIDGE.md).

## Phase 8 — inference and performance (Weeks 82–93)

The four `deploy_benchmark` weeks are the hardware-dependent exceptions. The
rest of the phase deliberately uses architecture notes, methodology documents,
comparison tables, and cost models when a live GPU run is not available.

## Phase 9 — production AI platform (Weeks 94–102)

The platform layer's preserved package layout is recorded alongside the
engineering prompt bank in [`../ENGINEERING_TASKS.md`](../ENGINEERING_TASKS.md).

## Phase 10 — capstone and portfolio (Weeks 103–108)

The current canonical choices are:

- [`../CAPSTONE.md`](../CAPSTONE.md) — required trace forensics path;
- [`../CAPSTONE3_OPENROUTER.md`](../CAPSTONE3_OPENROUTER.md) — alternative enterprise gateway;
- [`../CAPSTONE2_EULER_DSU.md`](../CAPSTONE2_EULER_DSU.md) — optional Week 108 boss fight.

Do not treat the historical list of possible project themes as additional
required capstones; the three specifications above define the current contract.
