# Documentation index

The root [`README.md`](../README.md) is the action-first launchpad. This directory
holds the long-form rationale, operating policies, routing indexes, and
maintainer records that would otherwise make the landing page unreadable.

## Read next

| Need | Document |
|---|---|
| Why the apprenticeship is long and seam-oriented | [`COURSE_PHILOSOPHY.md`](./COURSE_PHILOSOPHY.md) |
| How to budget and execute a week | [`WEEKLY_OPERATING_MODEL.md`](./WEEKLY_OPERATING_MODEL.md) |
| Week 5 generalization paper lab | [`WEEK_05_GENERALIZATION_LAB.md`](./WEEK_05_GENERALIZATION_LAB.md) |
| Choose a parallel lane | [`PARALLEL_TRACKS.md`](./PARALLEL_TRACKS.md) |
| Understand the agents-bootcamp bridge | [`AGENT_BRIDGE.md`](./AGENT_BRIDGE.md) |
| Preserve engineering prompts and timed drills | [`../ENGINEERING_TASKS.md`](../ENGINEERING_TASKS.md) |
| Browse the source-to-week map | [`SOURCE_MAP.md`](./SOURCE_MAP.md) |
| Review optional topic inventory | [`OPTIONAL_TRACKS.md`](./OPTIONAL_TRACKS.md) |
| Read phase implementation notes | [`PHASE_DETAILS.md`](./PHASE_DETAILS.md) |
| Audit where former README content moved | [`MIGRATION_MAP.md`](./MIGRATION_MAP.md) |

## Canonical structured curriculum

Structured facts live once in `schema/*.yaml`. They are rendered by the Astro
site and emitted into the generated learner repository; do not create a second
hand-maintained Markdown copy of the tables.

| Surface | Structured source | Reader-facing view |
|---|---|---|
| Weeks, phases, modes, recovery | [`../schema/weeks.yaml`](../schema/weeks.yaml) | [Curriculum](https://sethuiyer.github.io/tensor-to-tenant/curriculum/) |
| Gates and stackable releases | [`../schema/gates.yaml`](../schema/gates.yaml) | [Gates](https://sethuiyer.github.io/tensor-to-tenant/gates/) |
| Prerequisites | [`../schema/prerequisites.yaml`](../schema/prerequisites.yaml) | [Prerequisites](https://sethuiyer.github.io/tensor-to-tenant/prerequisites/) |
| Math modules | [`../schema/math.yaml`](../schema/math.yaml) | [Math](https://sethuiyer.github.io/tensor-to-tenant/math/) |
| Engineering tasks and drills | [`../schema/engineering.yaml`](../schema/engineering.yaml) | [Engineering](https://sethuiyer.github.io/tensor-to-tenant/engineering/) |
| Agents and bridge mappings | [`../schema/agents.yaml`](../schema/agents.yaml) | [Agents](https://sethuiyer.github.io/tensor-to-tenant/agents/) |
| Interview roadmap | [`../schema/interview.yaml`](../schema/interview.yaml) | [Interview](https://sethuiyer.github.io/tensor-to-tenant/interview/) |
| Resources | [`../schema/resources.yaml`](../schema/resources.yaml) | [Resources](https://sethuiyer.github.io/tensor-to-tenant/resources/) |
| Capstone cards | [`../schema/capstones.yaml`](../schema/capstones.yaml) | [Capstones](https://sethuiyer.github.io/tensor-to-tenant/capstones/) |

## Long-form Markdown artifacts

These are narrative/spec/template sources, not competing structured catalogs:

- [`../CAPSTONE.md`](../CAPSTONE.md), [`../CAPSTONE2_EULER_DSU.md`](../CAPSTONE2_EULER_DSU.md), [`../CAPSTONE3_OPENROUTER.md`](../CAPSTONE3_OPENROUTER.md)
- [`../ALGORITHMIC_FORGE.md`](../ALGORITHMIC_FORGE.md), [`../SYSTEM_DESIGN_TRACK.md`](../SYSTEM_DESIGN_TRACK.md), [`../LEETCODE_DARBAR.md`](../LEETCODE_DARBAR.md)
- [`../SEARCH.md`](../SEARCH.md), [`../SNOWFLAKE.md`](../SNOWFLAKE.md), [`../ML_CODING_CHALLENGES.md`](../ML_CODING_CHALLENGES.md), [`../PROGRAMMING_CAMP.md`](../PROGRAMMING_CAMP.md), [`../ENGINEERING_TASKS.md`](../ENGINEERING_TASKS.md)
- [`../MANDALA.md`](../MANDALA.md), [`../SAILBOAT_RETRO.md`](../SAILBOAT_RETRO.md), [`../COMPLETIONS.md`](../COMPLETIONS.md)

## Maintainer surfaces

- [`ARCHITECTURE.md`](./ARCHITECTURE.md) — ownership and architectural decisions
- [`archive/MATH_CATALOG_HEAD.md`](./archive/MATH_CATALOG_HEAD.md) — historical math-table snapshot for reconciliation only
- [`AUDIT.md`](./AUDIT.md) — generated technical-audit findings
- [`DRIFT.md`](./DRIFT.md) — schema/site drift notes
- [`REVIEWERS.md`](./REVIEWERS.md) — review protocol
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — contribution contract

## Archive policy

Files under [`archive/`](./archive/) are provenance snapshots for explicit
reconciliation only. They are not active curriculum inputs, generated sinks, or
permission to create a second catalog.

## Generated learner documentation

The Cookiecutter template emits learner-facing snapshots such as
`docs/course_map.md`, `docs/programs.md`, `docs/milestone_gates.md`,
`docs/prerequisites.md`, `docs/agents_track.md`, and `docs/bridge.md`. Those
files are intentionally generated downstream; edit the schema or the narrative
artifact, not a rendered learner copy.
