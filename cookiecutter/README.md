# `cookiecutter-tensor-to-tenant`

A [Cookiecutter](https://cookiecutter.readthedocs.io/) template that scaffolds a learner's repo for the **Tensor-to-Tenant** 108-week AI engineering, ML systems & interview mastery course.

## What you get

Running this cookiecutter generates a fresh, opinionated repo with:

- **Top-level config**: `README.md`, `.gitignore`, `Makefile`, `pyproject.toml`, `LICENSE`
- **All 108 weekly journal entries** pre-stamped with your start date and the per-week focus
- **Phase folders** (`00_orientation` to `09_interview`) with READMEs explaining objectives, deliverables, and milestone gates
- **Engineering primitive stubs** (`02_engineering_primitives/`) with `__init__.py`, module README, and `test_*.py` skeletons
- **Capstone scaffolding** (`08_capstone/`) wired to the staff-level **Multi-Tenant LLM Trace Forensics** question
- **Interview folders** (`09_interview/`) for system-design, coding, behavioral, and mock artifacts
- **Helper scripts** (`scripts/`): `new_week.py`, `milestone_gate.py`, `progress.py`

## Usage

```bash
# Install cookiecutter (once)
pipx install cookiecutter
# or: pip install cookiecutter

# Scaffold a new learner repo
cookiecutter gh:sethuiyer/tensor-to-tenant
# or, from a local clone:
cookiecutter /path/to/tensor-to-tenant/cookiecutter
```

You will be prompted for:

| Variable | Default | Description |
|---|---|---|
| `repo_name` | `tensor-to-tenant-journal` | Directory name for the new repo |
| `course_name` | Tensor-to-Tenant full title | Used in README + phase headers |
| `course_short` | `tensor-to-tenant` | Short identifier / badges |
| `student_name` | `Your Name` | Pre-filled in journal entries + LICENSE |
| `github_username` | `yourusername` | Used in `git remote` instructions + README |
| `start_date` | `2026-01-05` | Monday of Week 1. All week ranges derive from this. |
| `effort_hours_per_week` | `10-15` | Printed in the dashboard |
| `python_version` | `3.11` | Used in `pyproject.toml` |
| `use_docker` | `yes` | Adds a `Dockerfile` + `compose.yaml` |
| `track` | `balanced` | Phase weighting: `production-ai-platform`, `llm-inference`, `rag-agents`, `balanced` |

## After scaffolding

```bash
cd tensor-to-tenant-journal
make init          # create venv, install deps, pre-commit
make journal       # open this week's journal entry in $EDITOR
make gate          # check the current milestone gate
make progress      # dashboard of weekly completion
make test          # run pytest on engineering primitives
```

## Repo layout generated

```text
<repo_name>/
├── README.md
├── .gitignore
├── Makefile
├── pyproject.toml
├── LICENSE
├── docs/
│   ├── course_map.md
│   └── milestone_gates.md
├── journal/
│   ├── TEMPLATE.md
│   ├── RETRO_TEMPLATE.md
│   └── weeks/
│       ├── week_001.md
│       ├── week_002.md
│       └── ... (week_108.md)
├── 00_orientation/        # Weeks 1-6
├── 01_math/               # Weeks 7-30 (math foundations)
├── 02_engineering_primitives/   # Weeks 31-45
│   ├── retrieval/
│   ├── rate_limiting/
│   ├── caching/
│   ├── chunking/
│   ├── pii/
│   ├── metrics/
│   ├── batching/
│   ├── resilience/
│   ├── sketches/
│   ├── routing/
│   └── ids/
├── 03_system_design/      # Weeks 46-57
├── 04_ml_systems/         # Weeks 58-69
├── 05_llm/                # Weeks 70-81
├── 06_inference/          # Weeks 82-93
├── 07_platform/           # Weeks 94-102
├── 08_capstone/           # Weeks 103-108 (references CAPSTONE.md)
├── 09_interview/          # continuous interview prep
└── scripts/
    ├── new_week.py
    ├── milestone_gate.py
    └── progress.py
```

## Development

To modify the template itself:

1. Edit files under `cookiecutter/{{cookiecutter.repo_name}}/`.
2. To change the 108-week curriculum, edit the `PHASES` list in `cookiecutter/hooks/post_gen_project.py`.
3. Test locally:

```bash
cookiecutter ./cookiecutter --no-input -o /tmp/t3-test
cd /tmp/t3-test/tensor-to-tenant-journal
make progress
```

## License

Apache 2.0 — same as the parent course.