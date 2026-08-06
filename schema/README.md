# Tensor-to-Tenant canonical schema

> **Status:** schema-backed generation is landed; the YAML format remains
> provisional until the deferred Pydantic/JSON-Schema decision is made.
> Structured curriculum facts live here; narrative specifications and teaching
> briefs remain in Markdown; site and cookiecutter views are generated sinks.

## Why a schema at all

Curriculum information has two intentional authoring surfaces:

1. **Structured facts** (`schema/*.yaml`) — weeks, gates, resources, modules,
   mappings, and metadata; this is the source for generated views.
2. **Narrative artifacts** (root Markdown and focused `docs/*.md`) — rationale,
   specifications, teaching briefs, templates, and deep dives that are not
   useful as typed row data.

The generated site data (`src/data/*.ts`) and generated learner-repo docs/constants
are downstream sinks. Do not hand-edit them or create a second Markdown copy of
a structured catalog.

`source_data.yaml` and `cookiecutter.yaml` are generated migration fixtures.
They retain legacy exports that were not represented by the first entity pass;
edit the entity YAML files, then run `python3 tools/generate.py`. The generator
merges modeled entity fields over those fixtures and refuses malformed spine
IDs/ranges before writing any output.

## P-principles applied

Every entry in any entity file must pass:

- **P-principle 2 (selection rule):** add content that changes how the
  learner thinks about a system, not content that demonstrates textbook
  fluency. A bare URL fails this filter.
- **P-principle 3 (Level 2 vs Level 3):** `level: 2` = "I can implement
  this"; `level: 3` = "I know when this breaks and what replaces it."
  Level 3 is the curriculum's target.
- **T1.8.h (metadata-first):** no entry lands without
  `selection_rationale`, `tier`, `week`, `level`, `seam`, and
  `cross_references`. The drift check enforces this; a missing field
  fails CI.

## Entity files

| File | Contents | Status |
|---|---|---|
| `resources.yaml` | Papers, videos, books, blogs, agent papers | T1.8 + T1.8.g + T1.8.h + T1.8.i (landed Phase 2) |
| `weeks.yaml` | 108-week spine, one entry per week | Landed in schema-backed generation |
| `gates.yaml` | 3 stackable programs + 10 milestone gates | Landed in schema-backed generation |
| `mandalas.yaml` | 16 mandalas | Landed in schema-backed generation |
| `math.yaml` | 100-module math curriculum | Landed in schema-backed generation |
| `forge.yaml` | Algorithmic Forge lanes/bosses | Landed in schema-backed generation |
| `darbar.yaml` | Leetcode Darbar catalog summary | Landed in schema-backed generation |
| `engineering.yaml` | 30 engineering tasks + 40 drills | Landed in schema-backed generation |
| `system_design.yaml` | Weeks 46–57 design track | Landed in schema-backed generation |
| `agents.yaml` | 18 agent modules + bridges + Manus | Landed in schema-backed generation |
| `interview.yaml` | CARL stories + 176-item roadmap | Landed in schema-backed generation |
| `interview_questions.yaml` | Level 3 question bank (T1.11) | T1.11 (landing Phase 2) |
| `implementation_exercises.yaml` | TensorTonic catalog + Pattern C prerequisites | T1.10 (landing Phase 2) |
| `deep_dives.yaml` | Parallel-track pair registry (T1.12) | T1.12 (theory + production pairs) |
| `prerequisites.yaml` | 9-resource on-ramp | Landed in schema-backed generation |
| `capstones.yaml` | Three capstone page cards and structured artifacts | T2.1 |

## Schema discipline is enforced in three places

1. **Drift check** (T1.6) — every entry's required fields are present.
2. **Generator** (T1.3) — `src/data/*.ts` and cookiecutter constants are
   emitted from these files, so a missing field here is a missing
   field in the rendered output.
3. **CONTRIBUTING.md** — the human-readable contract says "no entry
   without metadata."

## Format conventions (provisional)

- Indent: 2 spaces.
- Lists use `-` with a single space.
- Strings may be quoted or unquoted; prefer unquoted unless the string
  contains special characters.
- Multi-line strings use `>-` folded scalar style for `selection_rationale`.
- IDs use `snake_case` and must be unique within their entity file.
- Cross-references use the `id` of the target entity, not its path.

## Pydantic v2 (deferred decision)

If adopted, each entity file will have a sibling `models.py` that defines a
Pydantic v2 model for the entity type, with validators that enforce
the discipline above. Loading any entity file will validate it at
import time. JSON Schema export from Pydantic will generate the
TypeScript types for `src/data/*.ts`.

Until that decision lands, the YAML files plus generator/validation tools are
the contract enforced by drift-check tests.
