---
name: Drift report
about: Report inconsistency between schema, site, and cookiecutter
title: "[drift-report] "
labels: ["drift", "schema"]
assignees: []
---

## Where's the drift?

Which surface drifted from which? Provide both paths:

- **Surface A:** (e.g. `src/data/weeks.ts`)
- **Surface B:** (e.g. `schema/resources.yaml`)

**Expected:** both should agree on `[the specific fact]`.

**Actual:** A says `[X]`; B says `[Y]`.

## How did you find it?

- [ ] Running `pipx run pytest tests/ -v`
- [ ] Running `python3 tools/audit.py`
- [ ] Visual inspection of the deployed site
- [ ] Reading the schema and the site side-by-side
- [ ] Other: (describe)

## Suggested fix

Where should the canonical fact live, and what should the other surface
become?

- [ ] Surface A is canonical; Surface B should match A
- [ ] Surface B is canonical; Surface A should match B
- [ ] Neither is canonical; the fact should move to a new schema entity
- [ ] The drift is intentional (different surfaces show different views of the same fact); no fix needed but document why

## Acceptance

Once fixed:

- `pipx run pytest tests/ -v` passes
- `python3 tools/audit.py` reports zero new `FAIL` verdicts
- A note in the issue (or linked PR) explains which surface was changed and why
