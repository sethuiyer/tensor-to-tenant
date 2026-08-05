# Reviewers

> The honest reviewer policy for a solo-authored open-source curriculum.

## Current state

This project is solo-authored. The default owner for every surface is
`@sethuiyer` (see `.github/CODEOWNERS`). Until a real second reviewer
materializes, all review requests go to the author.

This is acknowledged in the FAQ: *"It's not the same as having a
teacher, and pretending otherwise would be dishonest."*

## What we want (eventually)

The curriculum needs reviewers in three roles:

1. **Curriculum reviewers** — second eyes on math and systems claims.
   Authoritative in their domain. Spot-check that the 108-week spine
   matches current field knowledge. The T1.13 audit's
   `FLAGGED-FOR-HUMAN` items are exactly this work.
2. **Pedagogy reviewers** — second eyes on the *teaching* shape of the
   curriculum: is the math-first approach actually load-bearing? Are
   the seams the right ones? Does the cookiecutter scaffold produce a
   usable learner repo? Harder to formalize; best done by people who
   have actually tried to teach this material.
3. **Process reviewers** — second eyes on the tooling: does the
   schema discipline hold? Are tests catching real bugs? Is the drift
   check doing what it claims? Mostly internal to the project's
   tooling layer.

## How to become a reviewer

If you have expertise in any of the three roles above and want to
review curriculum content:

1. **Open an issue** titled "Reviewer nomination — [your domain]"
   on GitHub. Describe your background in 2–3 sentences and which
   surface (curriculum, pedagogy, tooling) you'd review.
2. The author will respond within a week with either an acceptance
   (you'll be added to `.github/CODEOWNERS` for that surface) or a
   counter-proposal (a different surface that better matches your
   expertise).
3. Once added, you'll receive review requests on PRs that touch
   your surface.

## What review requests look like

When a PR touches a surface you own, GitHub will auto-assign you.
The expected response time is one week for curriculum reviews, three
days for tooling reviews (the latter is faster because the tooling
surface is smaller and more mechanical).

If you can't review within the expected window, comment "I'll get to
this by [date]" and the author will wait. Silence past the expected
window is interpreted as "approve and merge" only after an explicit
comment from the reviewer.

## What reviewing actually involves

For curriculum reviews (the bulk of the work):

- **Math claims**: open the relevant week/gate document, check that
  the formulas match what the code does (or vice versa). The T1.13
  audit's `tools/audit.py` is a starting point; reviewer work goes
  deeper.
- **Systems claims**: cross-reference the systems weeks (W82–W93) and
  capstones against current production knowledge. The schema paper
  list (`schema/resources.yaml`) is the canonical reference; flag
  citations that need human verification.
- **Pedagogy**: read the cookiecutter-generated learner repo. Does
  the 108-week scaffold actually produce a usable apprenticeship?
  Where do learners get stuck?

For tooling reviews:

- Run `pipx run pytest tests/ -v` against the PR.
- Run `python3 tools/audit.py` and confirm zero `FAIL` verdicts.
- Verify the schema discipline in `schema/` files matches the
  contract documented in `TASKS.md`.

## The author's commitment

The author will not merge curriculum PRs (anything that changes
`README.md`, `MANDALA.md`, the `CAPSTONE*.md` files, or `src/data/`)
without:

- A linked issue with the proposed change, OR
- A reviewer (human or LLM-assisted) flagging the change as safe.

This is the `T0.3 CONTRIBUTING.md` policy. It applies to the author
too — the self-discipline is the point.

## What this is NOT

This document is not a community-infrastructure commitment. There is
no Discord, no Matrix, no scheduled office hours. It is a written
record of who reviews what, so that when a second reviewer arrives
they know where to slot in.

The bottleneck is not governance; it is reviewer recruitment. Adding
a second name to `CODEOWNERS` requires that person actually exists
and wants to do the work. Until then, this document is a placeholder
for the policy that will apply.

---

*Last updated: 2026-08 (T1.13 / T3.1)*
