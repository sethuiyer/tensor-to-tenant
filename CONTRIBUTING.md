# Contributing to `tensor-to-tenant`

> A solo-authored open-source curriculum. Contribution is welcome; the
> rules below protect the course's coherence from casual edits.

This document is a **living policy**, not a wishlist. If your change
violates one of these rules and you cannot defend the violation, the
PR will be closed with a reference back to this file.

---

## What belongs in a PR

The repo has five distinct surfaces, each with its own contribution
contract:

| Surface | What lives there | PR contract |
|---|---|---|
| `README.md` and root `.md` files (`CAPSTONE*.md`, `MANDALA.md`, `ALGORITHMIC_FORGE.md`, `SYSTEM_DESIGN_TRACK.md`, `LEETCODE_DARBAR.md`, `PROGRAMMING_CAMP.md`, `SAILBOAT_RETRO.md`) | Curriculum prose | See "Curriculum prose" below. |
| `src/data/*.ts` and `src/pages/*.astro` | Site code | See "Site code" below. |
| `cookiecutter/` and its subdirectories | Learner-repo generator | See "Generator code" below. |
| `TASKS.md`, `CONTRIBUTING.md`, `CODEOWNERS`, `.github/` | Project meta | Should match the schema discipline in TASKS.md. |
| `SEARCH.md`, `SNOWFLAKE.md`, `ML_CODING_CHALLENGES.md`, future `*.md` deep-dives | Parallel-track content | See "Deep-dives" below. |

---

## Curriculum prose (root `.md` files)

**Source-of-truth rule:** every curriculum fact must live in the
canonical schema before appearing on the site or in the cookiecutter.
See TASKS.md § T1.1 – T1.3 for the planned schema migration. Until that
lands, hand-edited Markdown and hand-edited TypeScript data files may
disagree silently — open an issue if you spot drift, do not patch one
side without the other.

**No drive-by edits to capstones.** `CAPSTONE.md`, `CAPSTONE2_EULER_DSU.md`,
and `CAPSTONE3_OPENROUTER.md` are coordinated wholes (the Mo's coding
walkthrough, the DSU-on-Tree sack invariant proof, the AI gateway
failure-injection matrix). Each section ends with a "Pitfalls" callout
that the rest of the document assumes. **Open an issue first**; a
drive-by typo fix that misses a cross-reference is worse than no edit.

**The seam philosophy is load-bearing.** Every elegant algorithm in the
curriculum is introduced together with the operational detail that
tries to kill it (TASKS.md § P-principle 1). When adding or revising
content, ask: *"what is the production reality that breaks this?"* If
the answer is missing, the section is incomplete.

---

## Site code (`src/`)

**Type-checked end-to-end.** `tsconfig.json` extends `astro/tsconfigs/strict`.
All `src/data/*.ts` exports must be typed; `any` requires an inline
comment explaining why. New pages must declare `Props` interfaces.

**No inline styles for layout primitives.** Reuse the `.card`,
`.chip`, `.kicker`, `.callout`, `.grid-{2,3,4,6}`, `.table-wrap`
vocabulary from `src/styles/global.css`. New design tokens belong in
`:root` (dark) and `:root[data-theme="light"]`, not in page-scoped
inline styles.

**Theme variables, not literals.** Hex colors and font sizes go
through `var(--token)`. The site must remain readable in both dark and
light modes without per-page overrides.

---

## Generator code (`cookiecutter/`)

**Tests required.** Any change to `cookiecutter/.../scripts/*.py`
must include or update tests. Pure-function modules (`forgetting.py`,
`battle.py`, `concept_seed.py`) are the easiest targets; write the
test first, watch it fail, then make it pass.

**No new hand-written duplicates of schema data.** The hand-written
`PHASE_1..10`, `AGENT_MODULES_CC`, `BRIDGE_SUMMARY_CC`, `MANDALAS_CC`,
`PREREQUISITES`, `PREREQ_PLAN`, `FORGE_LANES`, `FORGE_BOSSES`,
`RECOVERY_AFTER`, `RELEASES`, `AGENT_PAPERS_CC`, `AGENT_PAPER_WEEKS`
arrays in `cookiecutter/hooks/post_gen_project.py` are slated for
generator-driven replacement (TASKS.md § T1.3, T1.7). New
hand-edited copies of the same data elsewhere will be rejected.

**The 108-week spine is not extensible by PR.** If you want to add a
week, change a phase boundary, or alter the gate structure, that is a
**major curriculum decision** and requires an issue with a written
proposal, not a PR. The spine is the load-bearing scaffold; small
additions break load-bearing assumptions downstream.

---

## Deep-dives (`SEARCH.md`, `SNOWFLAKE.md`, future `*.md`)

**Pair-enforcement.** Every deep-dive that earns its way into the
curriculum must ship as a paired reading unit: a `theory` artifact
introducing the math, and a `production` artifact implementing it on
a concrete platform (TASKS.md § T1.12.h). A track without a production
pairing is a paper and belongs in the resource list, not the deep-dives
folder.

**Selection rule.** Deep-dives are accepted if and only if they build
a muscle the course uses later AND expose a seam the seam philosophy
recognizes. A pure math walkthrough without an implementation is
archive material.

---

## Resource additions (papers, videos, books, blogs)

**No URL enters `schema/resources.yaml` without metadata.** Per TASKS.md
§ T1.8.h, every entry must carry: `title`, `tier`, `week`, `level`,
`seam`, and a non-empty `selection_rationale`. Bare URLs fail the
drift check by design.

**Default answer is no.** Add a resource only if it changes how the
learner thinks about a system. A paper that introduces a fancier model
is archive material; a paper that exposes a hidden correctness or
evaluation problem in a system the course builds is core material.

**T1.8.h pending queue is mandatory for bare URLs.** Land the URL in
`schema/resources_pending.yaml` with `status: pending_metadata` first,
then fill in metadata in a follow-up commit. The CI drift check will
fail loudly on stub-only entries.

---

## Third-party content

Pastes, blog posts, conference talk outlines, and job-description
clusters flow through TASKS.md § T1.11's split template: useful
(integrate) / fluff (exclude with reasoning) / useful-but-not-yet
(track in P2). The exclusions are as important as the inclusions.

**Salary claims, career trajectory tables, and "this skillset pays
$X" framing are not curriculum content.** They are sales copy.
Excluding them is the rule, not the exception.

---

## Process

1. **Open an issue first** for any non-trivial change. Drive-by PRs
   for substantive work get closed.
2. **Defend the `selection_rationale`.** If you cannot explain why the
   change earns its slot under P-principle 2 (the selection rule), it
   doesn't.
3. **Run the drift check locally** before pushing:
   ```bash
   pytest tests/ -v
   python tools/generate.py     # when the generator lands
   ```
4. **Reference TASKS.md.** Every PR should link to the task ID it
   addresses (`T0.x`, `T1.x`, `T2.x`, `T3.x`). Orphan PRs are rejected.
5. **One logical change per PR.** Multiple unrelated edits in a single
   PR are split or closed.

---

## What we explicitly do not accept

- **Drive-by typos in capstones.** Use an issue, not a PR.
- **Salary tables or career-trajectory hype.** Sales copy, not
  curriculum.
- **Hand-written copies of schema data in new places.** Wait for T1.3.
- **New weeks in the 108-week spine.** Major curriculum decision;
  requires a proposal.
- **URL-only resource entries.** Drift check will block them.

---

## License

By contributing, you agree that your contributions are licensed under
the project's Apache-2.0 license.

---

*This file is governed by TASKS.md. If the two disagree, TASKS.md wins
because it has the schema-discipline machinery to enforce its rules.
CONTRIBUTING.md is the human-readable summary.*
