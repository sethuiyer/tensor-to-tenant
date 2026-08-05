# Architecture Decision Records

> Decisions about the repo's shape that go deeper than a one-line
> answer. Recorded so future contributors (and future me) don't
> re-litigate the same questions.

---

## ADR-001: Schema format (working assumption: YAML)

**Status:** provisional, pending T1.1 formal decision.

**Decision:** YAML files in `schema/` at repo root, one per entity
type (`resources.yaml`, `weeks.yaml`, `gates.yaml`, etc.).

**Alternatives considered:**
- YAML + Pydantic v2 (recommended)
- Python dataclasses only
- JSON Schema + codegen

**Why YAML:** human-diff-friendly, survives without Python installed,
makes the schema a shared curriculum artifact rather than just a
build input. The Pydantic v2 layer (when it lands) gives validation
+ JSON Schema export for TS types.

**Why not the alternatives:** JSON Schema is friendlier for codegen
but harder to read; Python dataclasses lock the schema behind a
Python interpreter. Both alternatives can be expressed as
constraints on top of YAML.

---

## ADR-002: Source-of-truth architecture (single schema, multiple sinks)

**Status:** T1.2 / T1.3 / T1.7 in flight.

**Decision:** `schema/*.yaml` is canonical. `src/data/*.ts` and
`cookiecutter/hooks/post_gen_project.py` constants are *generated*
sinks. The site renders from the generated TS; the cookiecutter
generator imports from the generated Python.

**Alternatives considered:**
- Hand-edit both surfaces in sync (current state; drift-prone)
- Make the markdown prose canonical and derive everything from it
  (fragile; markdown isn't structured enough for typed data)
- Make the TS file canonical and emit YAML (reverses the design —
  the schema is the curriculum artifact, the site is a render)

**Why this decision:** the curriculum content is the project's
load-bearing artifact. The site and the cookiecutter are
*renderings* of that artifact. If a content change has to land in
two places to take effect, the second place WILL drift.

---

## ADR-003: Cookiecutter extraction (deferred)

**Status:** T3.5 decision recorded. Action deferred.

**Decision (in principle):** extract `cookiecutter/` into its own
repo `sethuiyer/tensor-to-tenant-cookiecutter`. The main repo
becomes curriculum + schema + site only.

**Why deferred:** the schema migration (T1.1 – T1.7) is the work
that benefits most from extraction. Until the schema is real and the
generator emits schema-derived content, extracting the cookiecutter
adds friction (two repos to keep in sync during the schema design
phase) without proportional benefit.

**Trigger for extraction:** T1.3 (generators) lands and the
cookiecutter constants become generated, *not* hand-written. At that
point the cookiecutter is genuinely a downstream consumer of the
schema and can live independently.

**If extraction is done:**
- The new repo's README points at `sethuiyer/tensor-to-tenant` as the
  source of truth.
- The cookiecutter installs via `pipx install
  sethuiyer/tensor-to-tenant-cookiecutter` (or
  `cookiecutter gh:...`).
- `cookiecutter/` is removed from this repo.

**If extraction is NOT done:** the cookiecutter stays here as part
of the curriculum distribution; learners who `cookiecutter
gh:sethuiyer/tensor-to-tenant` get both the curriculum and the
generator in one shot. This is the simpler UX; the trade-off is a
larger repo with mixed concerns.

The author leans toward *not* extracting (simpler UX wins), but the
decision is genuinely open. Revisit after T1.3.

---

## ADR-004: Drift-check authority (the test suite is the contract)

**Status:** T1.6 in flight.

**Decision:** the test suite (`tests/`) is the executable
specification of what the curriculum and generator must do. The
docs (`README.md`, `CAPSTONE.md`, etc.) describe intent; the tests
describe what is actually true. When the two disagree, the tests
win — the docs are updated to match.

**Why:** the cost of a stale doc is paid by future contributors who
act on it. The cost of a stale test is a red CI build. The second
cost is recoverable; the first is not.

**Implementation:** `tests/test_forgetting.py` covers pure-function
math. `tests/test_concept_seed.py` and `tests/test_battle.py` cover
the RPG layer. `tests/test_end_to_end_render.py` covers the
cookiecutter generator. `tools/audit.py` covers curriculum claims
that aren't easily expressed as unit tests.

---

## ADR-005: The L100 cap is a known sharp edge

**Status:** documented bug, deliberately deferred.

**Decision:** do not fix the L100 cap inconsistency in
`forgetting.py:xp_into_level` (where `into` exceeds `cost` past
L100 while `frac` clamps to 1.0). Pin the inconsistency with a test
(`test_l100_cap_behavior`) so it's visible.

**Why deferred:** the fix is one line (`into = min(into, cost)`),
but the only consumer is the character sheet display in
`scripts/character.py`. The display already handles the cap
visually. Fixing without updating the display is a half-fix; fixing
both is a chain of small changes that don't compound value.

**Trigger to fix:** the character sheet is rewritten for any other
reason, OR a learner reports confusion at the cap boundary.

---

## ADR-006: The serving-stack image is decorative, not load-bearing

**Status:** T1.11 / T1.13 reviewed.

**Decision:** the `public/images/serving-stack.webp` infographic is
a decorative asset. The ASCII pipeline in
`cookiecutter/.../docs/inference_topology.md` is the canonical
artifact. Both render the same information; the ASCII is accessible
and searchable, the WebP is first-impression polish.

**Why:** content is frozen. The image does not protect any
correctness claim — the cookiecutter doc and the curriculum prose
do. Adding visual polish to a frozen-content project is a
maintenance liability without proportional value.

---

## Open decisions

These are queued for future ADR entries:

- **Schema field validation strictness** (T1.6 territory) — should
  the drift check accept "warning" alongside "fail", or is it
  binary?
- **Cookiecutter Jinja syntax** — currently uses `{{ var }}`. Is this
  the right shape for the generator when it's emitted from a Python
  script?
- **README length** — currently 1,865 lines. Some content is
  duplicated between README and TASKS.md (the "what's the arc"
  section appears in both). Worth deduplicating, or worth preserving
  the README's standalone-readable property?

---

*Last updated: 2026-08 (T3.5 / ADR initial population).*
