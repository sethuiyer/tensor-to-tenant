# `cookiecutter-tensor-to-tenant`

A [Cookiecutter](https://cookiecutter.readthedocs.io/) template that scaffolds a learner's repo for the **Tensor-to-Tenant** 108-week AI engineering, ML systems & interview mastery course.

## What you get

Running this cookiecutter generates a fresh, opinionated repo with:

- **Top-level config**: `README.md`, `.gitignore`, `Makefile`, `pyproject.toml`, `LICENSE`
- **All 108 weekly journal entries** pre-stamped with your start date and the per-week focus
- **Three stackable program checkpoints**: Foundations (W1-30), Engineering + Systems (W31-69), and LLM Platform (W70-108)
- **Algorithmic Forge spine** with Core, Supporting, Archive, and Boss-fight tiers mapped across all 108 weeks
- **Canonical System Design track** for Weeks 46-57: foundations, distributed patterns, technology labs, case studies, and OOD/LLD
- **Parallel Leetcode Darbar track** with a 548-slot tracker and optional Standard/Auror completion paths
- **GenAI agents track** (`docs/agents_track.md` + `09_interview/agents/`): all 18 modules plus Module 7.5 (Model Context Protocol) and the Project Manus agentic UI-automation capstone under `08_capstone/manus/`
- **The bridge** (`docs/bridge.md`): every agents-bootcamp module mapped to the tensor-to-tenant weeks that explain why it works under the hood
- **Agent papers mapped into the journals**: ReAct, Toolformer, DSPy, LangGraph, CRAG, MCP, Generative Agents, Reflexion, AutoGen, and Kuzzu assigned to the Weeks 73-81 papers slots
- **Prerequisites on-ramp** (`docs/prerequisites.md`): the optional 36-week lane (CS50x, Nand to Tetris, MIT 6.042J, Statistical Learning, and more) for learners who need fundamentals before Week 1
- **Mandala identity ladder** (`docs/mandala.md`): the 16-mandala / 756-day identity arc
- **Core + optional depth lanes** in every weekly journal, so advanced work remains available without blocking the core path
- **Evidence tracking** for implementation, benchmarks/results, technical explanations, and retrospectives
- **Sailboat retrospective ritual** in every weekly journal: destination, wind, anchor, rocks, boat position, and next heading
- **Recovery and remediation scaffolds** with blocking milestone gates
- **Portfolio release checklists** for Weeks 30, 69, and 108
- **Evidence-based badge verifier** for the three release checkpoints
- **Phase folders** (`00_orientation` to `09_interview`) with READMEs explaining objectives, deliverables, and milestone gates
- **Engineering primitive stubs** (`02_engineering_primitives/`) with `__init__.py`, module README, and `test_*.py` skeletons
- **Capstone scaffolding** (`08_capstone/`) with the required trace-forensics artifact, optional Euler/DSU boss, and OpenRouter-inspired enterprise gateway option
- **Interview folders** (`09_interview/`) for system-design, coding, behavioral, and mock artifacts
- **Helper scripts** (`scripts/`): `new_week.py`, `milestone_gate.py`, `progress.py`
- **Workflow commands**: `make design=54`, `make darbar=42`, and `make auror`

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
make week=14       # prepare and open a specific week's journal + evidence scaffold
make recovery=14   # prepare a recovery plan after Week 14
make remediate=18  # prepare a targeted remediation plan for Gate 18
make release=30    # prepare the Foundations portfolio release checklist
make badge=30      # verify evidence and award the Foundations badge when eligible
make forge=57      # prepare the Week 57 Algorithmic Forge artifact
make design=54     # prepare a Week 54 System Design artifact
make darbar=42     # prepare Darbar problem 42 evidence
make agent=7.5     # open the Module 7.5 (MCP) agents scaffold
make auror         # verify the optional 548-problem Auror track
make gate          # check the current milestone gate
make progress      # dashboard of weekly completion
make test          # run pytest on engineering primitives
```

## The apprenticeship model

This template is designed for a 108-instructional-week apprenticeship, not an
all-or-nothing attendance challenge. It has three stackable stopping points:

| Program | Weeks | Release |
|---|---:|---|
| Foundations | 1-30 | Math, numerical routines, and experimentation toolkit |
| Engineering + Systems | 31-69 | Tested primitives, system designs, MLOps tools, and postmortem |
| LLM Platform | 70-108 | LLM/RAG work, inference benchmark, platform layer, and capstone |

The core lane is the minimum viable weekly artifact. The optional depth lane is
where you add proofs, from-scratch implementations, benchmarks, failure
analysis, and production trade-offs. Depth work raises the ceiling; it does not
decide whether the learner is allowed to continue.

Milestone gates are blocking. A failed gate pauses new content until the
learner completes its targeted remediation plan and submits the missing
evidence. Recovery windows after Weeks 6, 14, 22, 30, 38, 46, 54, 62, 70, 78,
86, 94, and 102 are generated as deliberate catch-up or rest windows; they are
not additional course topics.

Completion is evidence-based rather than attendance-based. At minimum, every
core week records implementation, benchmark/result, technical explanation,
and retrospective evidence. The generated `portfolio/` folder turns Weeks 30,
69, and 108 into independently publishable releases.

System Design is the canonical Weeks 46-57 architecture lane; it is not an
extra phase. The optional [Leetcode Darbar](https://aninokuma.codeberg.page/leetcode-darbar/)
lane is tracked separately so standard learners can keep the 108-week path
viable while Auror learners can solve and explain all 548 catalog slots.

The **Algorithmic Forge** runs in parallel every Friday. Core drills are
required and phase-aligned; Supporting labs are guided depth; Archive topics
are reference-only; Boss fights are selected gate or capstone extensions. See
the generated `docs/algorithmic_forge.md` and use `make forge=57` to scaffold a
drill in the correct tier.

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
│   ├── programs.md
│   ├── algorithmic_forge.md
│   ├── system_design_track.md
│   ├── leetcode_darbar.md
│   ├── prerequisites.md
│   ├── agents_track.md
│   ├── bridge.md
│   ├── mandala.md
│   ├── sailboat_retro.md
│   ├── milestone_gates.md
│   ├── recovery_weeks.md
│   └── remediation/
├── evidence/
│   └── weeks/                 # one evidence scaffold per instructional week
├── journal/
│   ├── TEMPLATE.md
│   ├── RETRO_TEMPLATE.md
│   ├── weeks/
│   │   ├── week_001.md
│   │   ├── week_002.md
│   │   └── ... (week_108.md)
│   └── recovery/              # recovery windows after selected weeks
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
├── 08_capstone/           # Weeks 103-108 (three capstone paths + manus)
│   ├── manus/              # Project Manus agentic UI automation
│   └── openrouter/         # Capstone 3 enterprise AI gateway
├── 09_interview/          # continuous interview prep
│   ├── algorithmic_forge/ # core, supporting, archive, boss_fights
│   └── agents/             # one scaffold per agents module (Modules 1-18 + MCP)
├── portfolio/              # release checklists for Weeks 30, 69, and 108
└── scripts/
    ├── new_week.py         # also powers `make week=14`
    ├── recovery.py
    ├── remediate.py
    ├── release.py
    ├── agents.py           # also powers `make agent=7.5`
    ├── milestone_gate.py
    └── progress.py
```

## Development

To modify the template itself:

1. Edit files under `cookiecutter/{{cookiecutter.repo_name}}/`.
2. To change the 108-week curriculum, edit the `PHASES` list in `cookiecutter/hooks/post_gen_project.py`. Update `PROGRAMS`, `RECOVERY_AFTER`, `FORGE_LANES`, or `FORGE_BOSSES` when changing checkpoints, recovery windows, or algorithmic treatment.
3. The prerequisites, agents track, bridge, agent papers, and mandala content live in the `PREREQUISITES`, `PREREQ_PLAN`, `AGENT_MODULES_CC`, `AGENT_BRIDGE_CC`, `BRIDGE_SUMMARY_CC`, `AGENT_PAPERS_CC`, `AGENT_PAPER_WEEKS`, and `MANDALAS_CC` constants in the same hook file. Their generators are `generate_prerequisites_scaffold`, `generate_agents_scaffold`, `generate_bridge_scaffold`, and `generate_mandala_scaffold`.
4. Test locally:

```bash
cookiecutter ./cookiecutter --no-input -o /tmp/t3-test
cd /tmp/t3-test/tensor-to-tenant-journal
make progress
```

## License

Apache 2.0 — same as the parent course.
