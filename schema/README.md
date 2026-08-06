# Tensor-to-Tenant canonical schema

> **Status:** provisional format. Formal decision lands in T1.1.
> Working assumption: **YAML** files + (eventually) Pydantic v2 validation
> + JSON Schema export to TypeScript types. See TASKS.md § T1.1 for the
> design space.

## Why a schema at all

Curriculum content lives in three places that must stay in sync:

1. **Markdown prose** (`CAPSTONE.md`, `MANDALA.md`, etc.) — the canonical
   narrative.
2. **Site data** (`src/data/*.ts`) — what the Astro site renders.
3. **Cookiecutter constants** (`cookiecutter/hooks/post_gen_project.py`) —
   what the learner-repo generator emits.

Today these three are hand-written and drift silently. The schema is the
single source of truth that generators (T1.3) read from to produce (2)
and (3), and that drift checks (T1.6) verify against (1).

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
| `weeks.yaml` | 108-week spine, one entry per week | Coming with T1.2 |
| `gates.yaml` | 10 milestone gates | Coming with T1.2 |
| `programs.yaml` | 3 stackable programs | Coming with T1.2 |
| `mandalas.yaml` | 16 mandalas | Coming with T1.2 |
| `math.yaml` | 100-module math curriculum | Coming with T1.2 |
| `forge.yaml` | Algorithmic Forge lanes/bosses | Coming with T1.2 |
| `darbar.yaml` | Leetcode Darbar catalog summary | Coming with T1.2 |
| `engineering.yaml` | 30 engineering tasks + 40 drills | Coming with T1.2 |
| `system_design.yaml` | Weeks 46–57 design track | Coming with T1.2 |
| `agents.yaml` | 18 agent modules + bridges + Manus | Coming with T1.2 |
| `interview.yaml` | CARL stories + 176-item roadmap | Coming with T1.2 |
| `interview_questions.yaml` | Level 3 question bank (T1.11) | T1.11 (landing Phase 2) |
| `implementation_exercises.yaml` | TensorTonic catalog + Pattern C prerequisites | T1.10 (landing Phase 2) |
| `deep_dives.yaml` | Parallel-track pair registry (T1.12) | T1.12 (theory + production pairs) |
| `prerequisites.yaml` | 9-resource on-ramp | Coming with T1.2 |
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

## Pydantic v2 (when T1.1 lands)

Each entity file will have a sibling `models.py` that defines a
Pydantic v2 model for the entity type, with validators that enforce
the discipline above. Loading any entity file will validate it at
import time. JSON Schema export from Pydantic will generate the
TypeScript types for `src/data/*.ts`.

Until that lands, the schema files are documentation plus a CI
contract enforced by drift-check tests (T1.6).
