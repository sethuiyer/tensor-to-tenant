# {{ cookiecutter.repo_name }}

> **{{ cookiecutter.course_name }}**

**Student:** {{ cookiecutter.student_name }}
**GitHub:** [@{{ cookiecutter.github_username }}](https://github.com/{{ cookiecutter.github_username }})
**Start date:** {{ cookiecutter.start_date }} (Monday of Week 1)
**Effort:** {{ cookiecutter.effort_hours_per_week }} hours/week
**Track:** {{ cookiecutter.track }}

This is the learner journal for the **Tensor-to-Tenant** course -- a 108-week journey from linear algebra to multi-tenant production AI platforms.

## Layout

```text
.
├── docs/                              # course map, milestone gates
├── journal/
│   ├── TEMPLATE.md                    # canonical weekly template
│   ├── RETRO_TEMPLATE.md              # canonical retro template
│   └── weeks/                         # week_001.md ... week_108.md
├── 00_orientation/                    # Weeks 1-6
├── 01_math/                           # Weeks 7-30 (math foundations)
├── 02_engineering_primitives/         # Weeks 31-45
├── 03_system_design/                  # Weeks 46-57
├── 04_ml_systems/                     # Weeks 58-69
├── 05_llm/                            # Weeks 70-81
├── 06_inference/                      # Weeks 82-93
├── 07_platform/                       # Weeks 94-102
├── 08_capstone/                       # Weeks 103-108
├── 09_interview/                      # continuous
└── scripts/                           # new_week, milestone_gate, progress
```

## Daily cadence

| Day | Slot | Purpose |
|---|---|---|
| Mon | Theory | Math / paper / concept |
| Tue | Build | Code the deliverable |
| Wed | Systems / Papers | Architecture / paper reading |
| Thu | Eval / Interview | Offline slice or interview drill |
| Fri | Review / Retro | Update journal, retro, plan next week |
| Weekend | Buffer | Catch up or rest |

## Quickstart

```bash
make init          # create venv, install deps
make journal       # open this week's journal entry
make progress      # print weekly completion dashboard
make gate          # run the current milestone gate checker
make test          # pytest across engineering primitives
```

## Capstone

Phase 9 is the **Multi-Tenant LLM Trace Forensics with Mo's Algorithm** drill
(see your course bundle's `CAPSTONE.md` for the full pedagogical walkthrough,
pitfalls index, and worked solution). The scaffolding in `08_capstone/` is wired
to that artifact.

## License

Apache 2.0 -- same as the parent course.