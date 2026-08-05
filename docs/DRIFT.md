# Drift Dashboard

> Public, machine-readable view of the curriculum's drift status.
>
> **Status:** dashboard scaffold. The drift check itself is T1.6
> (not yet implemented). Until T1.6 lands, this dashboard is a
> placeholder that points at the audit and the manual verification
> commands.

## Current state

- **Audit run:** `python3 tools/audit.py` produces `docs/AUDIT.md`
  with per-claim verdicts. Re-run after any curriculum change.
- **Schema discipline:** `pipx run pytest tests/ -v` enforces the
  schema field requirements (every paper entry has
  `selection_rationale`, every level: 3 question has
  `acceptable_answers_skeleton`, etc.). Re-run after any change to
  `schema/*.yaml`.
- **End-to-end cookiecutter render:** the cookiecutter generator is
  exercised by `tests/test_end_to_end_render.py`. Re-run after any
  change to `cookiecutter/`.

## What this dashboard will become (T1.6)

When the drift check lands:

1. **Per-week consistency**: for each of the 108 weeks, verify that
   the schema entry, the site rendering, and the cookiecutter journal
   entry all agree on module / focus / deliverable.
2. **Per-paper verification**: every paper in `schema/resources.yaml`
   has its title / author / year / venue / URL fields populated AND
   matches the actual paper.
3. **Per-question coverage**: every Level 3 question in
   `schema/interview_questions.yaml` has an
   `acceptable_answers_skeleton` and `cross_references`.
4. **Per-exercise prerequisite map**: every Pattern C entry in
   `schema/implementation_exercises.yaml` has a `load_bearing_for`
   list pointing at weeks that exist in `schema/weeks.yaml`.

## Manual verification (interim)

Until the automated drift check lands, run these after any curriculum
edit:

```bash
# 1. Audit per-claim verdicts.
python3 tools/audit.py

# 2. Schema discipline (every entry has required fields).
pipx run pytest tests/ -v

# 3. Cookiecutter end-to-end render.
pipx run pytest tests/test_end_to_end_render.py -v
```

A red run on any of these three commands means drift has landed and
needs to be reconciled.

## Recent drift events

None yet. This section will record drift events as they are
discovered and fixed.

```
(empty)
```

The format will be:

```markdown
- 2026-XX-XX: drift between `schema/resources.yaml` and the README's
  paper list. Fix: [#N](https://github.com/sethuiyer/tensor-to-tenant/issues/N).
  Resolution: schema entry updated to match the README.
```

## How to file a drift report

Use the `.github/ISSUE_TEMPLATE/drift_report.md` template. The issue
body walks you through identifying the drift, naming the surfaces,
and proposing which one is canonical.

---

*Last updated: 2026-08 (T3.3 dashboard scaffold; T1.6 drift check is
the next milestone).*
