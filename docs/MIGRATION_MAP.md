# README content migration map

The landing README was shortened by moving structured facts to schema/site
sinks and unique prose/prompts into focused Markdown artifacts. This map records
where each substantial former README section now lives, and flags the few areas
that require reconciliation before legacy fixtures are retired.

## Former README → current home

| Former section | Current home | Ownership |
|---|---|---|
| Course Goal, Target Audience, Why this course, scarcity in the seams, capability ladder, target roles | [`COURSE_PHILOSOPHY.md`](./COURSE_PHILOSOPHY.md) | Narrative rationale |
| Prerequisites and 36-week schedule | [`../schema/prerequisites.yaml`](../schema/prerequisites.yaml) · [site](https://sethuiyer.github.io/tensor-to-tenant/prerequisites/) · generated learner `docs/prerequisites.md` | Structured curriculum data |
| Course structure, 108-week matrix, phase details, weekly modes, gates, release criteria | [`../schema/weeks.yaml`](../schema/weeks.yaml), [`../schema/gates.yaml`](../schema/gates.yaml) · [site](https://sethuiyer.github.io/tensor-to-tenant/curriculum/) · [`PHASE_DETAILS.md`](./PHASE_DETAILS.md) | Structured data + preserved implementation notes |
| Weekly contract, time budget, recovery policy, evidence loop, Sailboat ritual | [`WEEKLY_OPERATING_MODEL.md`](./WEEKLY_OPERATING_MODEL.md) · [`../SAILBOAT_RETRO.md`](../SAILBOAT_RETRO.md) | Operating policy + template |
| Week 5 weakest-hypothesis paper brief | [`WEEK_05_GENERALIZATION_LAB.md`](./WEEK_05_GENERALIZATION_LAB.md) · [resource view](https://sethuiyer.github.io/tensor-to-tenant/resources/) | Teaching brief + structured resource |
| Algorithmic Forge, System Design, Darbar, recommender, Sailboat, Mandala | [`PARALLEL_TRACKS.md`](./PARALLEL_TRACKS.md) and linked root artifacts | Routing index + long-form artifacts |
| Agent-building bootcamp bridge | [`AGENT_BRIDGE.md`](./AGENT_BRIDGE.md) · [`../schema/agents.yaml`](../schema/agents.yaml) · [site](https://sethuiyer.github.io/tensor-to-tenant/agents/) | Conceptual bridge + structured mappings |
| 100 math modules | [`../schema/math.yaml`](../schema/math.yaml) · [site](https://sethuiyer.github.io/tensor-to-tenant/math/) · [`archive/MATH_CATALOG_HEAD.md`](./archive/MATH_CATALOG_HEAD.md) | Schema/site are canonical; conflicting pre-rewrite rows/task verbs are archived for reconciliation, not active scheduling |
| Engineering tasks and practice exercises | [`../ENGINEERING_TASKS.md`](../ENGINEERING_TASKS.md) for the legacy full prompts/drills; [`../schema/engineering.yaml`](../schema/engineering.yaml) · [site](https://sethuiyer.github.io/tensor-to-tenant/engineering/) for the current 30/40 structured index | Legacy prompt bank + structured catalog; schema IDs/titles remain canonical |
| Source-material mapping and reference resources | [`SOURCE_MAP.md`](./SOURCE_MAP.md) for topic→week prose; [`../schema/resources.yaml`](../schema/resources.yaml) · [site](https://sethuiyer.github.io/tensor-to-tenant/resources/) for metadata-backed resources | Map + structured catalog; legacy lists require promotion from `schema/source_data.yaml` |
| Interview integration, CARL stories, 176-item roadmap | [`../schema/interview.yaml`](../schema/interview.yaml) · [site](https://sethuiyer.github.io/tensor-to-tenant/interview/) | Structured catalog |
| Weekly template and generated repository layout | [`../cookiecutter/README.md`](../cookiecutter/README.md) and generated learner `journal/TEMPLATE.md` | Downstream learner bundle |
| Final capstone requirements | [`../CAPSTONE.md`](../CAPSTONE.md), [`../CAPSTONE2_EULER_DSU.md`](../CAPSTONE2_EULER_DSU.md), [`../CAPSTONE3_OPENROUTER.md`](../CAPSTONE3_OPENROUTER.md) | Long-form specifications |
| Additional specialized tracks and inventory | [`OPTIONAL_TRACKS.md`](./OPTIONAL_TRACKS.md) | Optional, non-gating routing inventory |
| Completion records | [`../COMPLETIONS.md`](../COMPLETIONS.md) | Real learner records only |

## What remains in the root README

The root file intentionally keeps only the high-signal launch path:

- what the apprenticeship is and who it is for;
- the Cookiecutter quickstart;
- stackable releases and blocking-gate summary;
- the compact phase arc and seam philosophy;
- capstone choices and image links; and
- links to the canonical site, schema, and long-form Markdown artifacts.

The WebP visuals remain directly embedded in the README: the mandala map and all
three capstone maps. The curriculum map PNG remains embedded near the phase map.

## Editing rule

If a change is a structured fact—week, gate, release, resource, math module,
engineering task, agent mapping, interview item, or capstone card—edit the
corresponding YAML and regenerate. If it is explanatory prose, a specification, a task prompt, a template, or a
deep dive, edit its named Markdown artifact. For legacy resource or math
conflicts, reconcile into the schema before deleting the migration fixture. Do
not create a new hand-maintained catalog in `docs/`.
