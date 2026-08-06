# Weekly operating model

> A practical operating contract for the 108-week apprenticeship. Exact week
> titles, modes, gates, and recovery windows live in the schema and interactive
> curriculum; this document explains how to work them without burning out or
> turning optional depth into a hidden prerequisite.

## Core first, depth second

Every week has two lanes:

- **Core deliverable:** the one artifact that keeps the learner moving. It is
  sized for the stated weekly effort and is the requirement for progress.
- **Optional depth work:** a proof, from-scratch implementation, benchmark,
  failure analysis, or production trade-off note. It raises the ceiling but does
  not decide whether the learner may continue.

Every core artifact records four kinds of evidence:

1. Code or implementation (or the equivalent design artifact for a writing week)
2. Benchmark or result
3. Design document or technical explanation
4. Short retrospective / learning note

The curriculum tracks evidence shipped, not attendance.

## Modes: match the work to the deliverable

| Mode | What you ship | Example |
|---|---|---|
| `implement` | Working code with tests and a runnable entry point | Cache, evaluator, limiter, or router |
| `read_diagram` | A design doc, trade-off note, comparison, or methodology document | Training map or disaggregated-serving plan |
| `deploy_benchmark` | A live deployment or benchmark run | Index, vLLM, dashboard, or SGLang comparison |

The mode is a scope guard. If a `read_diagram` week turns into 15+ hours of
coding, stop and write the document. If an `implement` week has no running
artifact after roughly 8 hours, trim scope until it runs.

Across the 108-week spine there are **69 `implement`**, **35 `read_diagram`**,
and **4 `deploy_benchmark`** weeks. The four GPU-dependent weeks are **75, 84,
87, and 89**; they are declared in
[`../schema/weeks.yaml`](../schema/weeks.yaml) and summarized on the
[interactive curriculum](https://sethuiyer.github.io/tensor-to-tenant/curriculum/).

## Time budget

The course is sized at **10–15 hours per week**. A 15-hour week is two buckets:

```text
15 hr/week total
├── 6–8.5 hr   fixed weekly overhead
│              ├── coding drill
│              ├── system-design question or pattern
│              ├── behavioral story refinement
│              ├── technical explanation out loud
│              ├── Algorithmic Forge drill
│              └── evidence record + Sailboat retrospective
└── 7–9 hr     this week's core deliverable
```

Do not spend the entire budget on optional depth. If a week slips, protect the
core artifact, record the constraint, and use a recovery window rather than
silently expanding the next week.

## Monday–Friday rhythm

```text
Monday     theory / mathematics
Tuesday    implementation
Wednesday  systems, papers, architecture
Thursday   evaluation + interview practice
Friday     Algorithmic Forge drill + Sailboat retrospective
Weekend    recovery, revision, or deliberate depth
```

Interview preparation is continuous. The weekly minimum is:

- one coding drill;
- one system-design question or pattern;
- one behavioral story refinement; and
- one technical explanation out loud.

## Gates, remediation, and recovery

Milestone gates are real dependencies. A failed gate pauses new gate-dependent
content until a focused remediation cycle supplies the missing evidence. It does
not erase prior work and does not require restarting the phase.

Recovery windows are deliberate buffer windows for catching up, rerunning a
benchmark, closing an evidence gap, or taking a planned rest. The exact windows
are maintained in [`../schema/weeks.yaml`](../schema/weeks.yaml); the current
criteria are rendered at the [gates page](https://sethuiyer.github.io/tensor-to-tenant/gates/).

Generated learner-repo commands:

```bash
make week=14        # prepare one journal and its evidence scaffold
make recovery=14   # prepare a recovery plan after a week
make remediate=18  # prepare targeted remediation for a gate
make gate           # check the current blocking checkpoint
make progress       # inspect evidence/progress status
```

## The evidence review ritual

End each week by asking:

- What capability was the destination?
- What helped progress (wind)?
- What slowed progress (anchor)?
- What could derail next week (rocks)?
- Am I ahead, on track, or drifting?
- What is the single next heading?

Use the [Sailboat template](../SAILBOAT_RETRO.md) and keep the answer short.
The goal is navigation, not a performance review.

## Related surfaces

- [Full curriculum and modes](https://sethuiyer.github.io/tensor-to-tenant/curriculum/)
- [Milestone gates](https://sethuiyer.github.io/tensor-to-tenant/gates/)
- [`schema/weeks.yaml`](../schema/weeks.yaml) — structured week source
- [`cookiecutter/README.md`](../cookiecutter/README.md) — generated learner-repo commands
