"""One-off build script: generate schema/weeks.yaml from src/data/weeks.ts.

This is exactly what T1.3 (write the generators) will do permanently.
Running it now as a one-off avoids hand-transcribing 108 entries.

Maps week data to schema discipline:
  - level: derived from phase (1 for orientation+math, 2 for engineering+MLOps,
    3 for LLM/inference/platform/capstone)
  - seam: derived from phase theme
  - cross_references: each week references its gate (if a gate week) and
    its phase

Usage: python3 tools/build_weeks_schema.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
WEEKS_TS = REPO_ROOT / "src" / "data" / "weeks.ts"
OUT = REPO_ROOT / "schema" / "weeks.yaml"


# Phase → (level, seam, theme_short)
PHASE_META = {
    1: (1, "orientation", "Orientation, tooling, and diagnostics"),
    2: (1, "math foundations", "Mathematical foundations I: linear algebra & numerical methods"),
    3: (1, "math foundations", "Mathematical foundations II: calculus, autodiff, probability, statistics"),
    4: (2, "engineering primitives", "Engineering micro-projects and applied ML primitives"),
    5: (2, "system design", "System design and distributed systems fundamentals"),
    6: (2, "MLOps", "ML lifecycle, experimentation, and MLOps"),
    7: (2, "LLM systems", "LLM training, RAG, agents, and evaluation"),
    8: (3, "inference operations", "LLM inference and performance engineering"),
    9: (3, "production AI platform", "Production AI platform engineering"),
    10: (3, "graduation", "Capstone, portfolio, and interview readiness"),
}

# Map week → gate (week 6 = gate 1, week 18 = gate 2, etc.)
WEEK_TO_GATE = {
    6: 1, 18: 2, 30: 3, 45: 4, 57: 5, 69: 6, 81: 7, 93: 8, 102: 9, 108: 10,
}

# Recovery weeks scheduled as deliberate buffer windows.
RECOVERY_AFTER = [6, 14, 22, 30, 38, 46, 54, 62, 70, 78, 86, 94, 102]


def parse_weeks(ts_text: str) -> list[dict]:
    """Extract week entries from the WEEKS array in weeks.ts.

    Matches the TS shape literally: each entry is `{ week: N, module: '...',
    focus: '...', mode: '...', deliverable: '...' }`.
    """
    entries = []
    pattern = re.compile(
        r"\{\s*week:\s*(\d+),\s*module:\s*'([^']*)',\s*focus:\s*'([^']*)',\s*"
        r"mode:\s*'([^']*)',\s*deliverable:\s*'([^']*)'\s*\}",
    )
    for m in pattern.finditer(ts_text):
        entries.append({
            "week": int(m.group(1)),
            "module": m.group(2),
            "focus": m.group(3),
            "mode": m.group(4),
            "deliverable": m.group(5),
        })
    return entries


def parse_phases(ts_text: str) -> list[dict]:
    """Extract phase entries from the PHASES array."""
    entries = []
    pattern = re.compile(
        r"\{\s*id:\s*(\d+),\s*weeks:\s*'([^']*)',\s*theme:\s*'([^']*)',"
        r"\s*start:\s*(\d+),\s*end:\s*(\d+)\s*\}",
    )
    for m in pattern.finditer(ts_text):
        entries.append({
            "id": int(m.group(1)),
            "weeks": m.group(2),
            "theme": m.group(3),
            "start": int(m.group(4)),
            "end": int(m.group(5)),
        })
    return entries


def phase_for_week(week: int, phases: list[dict]) -> int:
    for p in phases:
        if p["start"] <= week <= p["end"]:
            return p["id"]
    return 0


def render_yaml(phases: list[dict], weeks: list[dict]) -> str:
    """Render the schema/weeks.yaml content."""
    lines = [
        "# Curriculum spine: 108 weeks across 10 phases.",
        "# Per T1.2 / T1.6: each week has id + phase + module + focus +",
        "# mode + deliverable. Schema discipline applied: level (1/2/3),",
        "# seam (which structural seam it addresses), cross_references (to",
        "# gate and phase).",
        "",
        "# ============================================================================",
        "# Phases",
        "# ============================================================================",
        "",
    ]
    for p in phases:
        level, seam, _ = PHASE_META[p["id"]]
        lines.append(f"- id: phase-{p['id']}")
        lines.append(f"  number: {p['id']}")
        lines.append(f"  weeks: \"{p['weeks']}\"")
        lines.append(f"  theme: \"{p['theme']}\"")
        lines.append(f"  start: {p['start']}")
        lines.append(f"  end: {p['end']}")
        lines.append(f"  tier: core")
        lines.append(f"  level: {level}")
        lines.append(f"  seam: \"{seam}\"")
        lines.append(f"  selection_rationale: >")
        lines.append(
            f"    Phase {p['id']} of the 10-phase spine. "
        )
        if p["id"] == 1:
            lines.append(
                "    Orientation week — every learner enters here. "
                "The seam is 'getting the engineering substrate "
                "working before any math shows up.'"
            )
        elif p["id"] in (2, 3):
            lines.append(
                "    Math foundations. The seam is 'you cannot ship "
                "production ML without calculus, linear algebra, and "
                "statistics in your hands.'"
            )
        elif p["id"] == 4:
            lines.append(
                "    Engineering primitives. The seam is 'the vocabulary "
                "every system-design week assumes you have implemented.'"
            )
        elif p["id"] == 5:
            lines.append(
                "    System design fundamentals. The seam is 'the case "
                "studies that prep you for Staff-level interviews.'"
            )
        elif p["id"] == 6:
            lines.append(
                "    MLOps. The seam is 'trustworthy evidence — "
                "experiments, monitoring, postmortems.'"
            )
        elif p["id"] == 7:
            lines.append(
                "    LLM training + RAG + agents. The seam is 'you can "
                "ship an LLM product, not just call an API.'"
            )
        elif p["id"] == 8:
            lines.append(
                "    LLM inference. The seam is 'you can serve a model "
                "in production — not just prompt one.'"
            )
        elif p["id"] == 9:
            lines.append(
                "    Production AI platform. The seam is 'multi-tenant, "
                "fair, observable, cost-attributed.'"
            )
        else:
            lines.append(
                "    Capstone, portfolio, and interview readiness. The "
                "seam is 'proof of completion — code, design docs, "
                "benchmarks.'"
            )
        lines.append(f"  cross_references:")
        lines.append(f"    - {{ entity: gates, role: \"release gate\", gate_id: gate-{p['id']} }}")
        lines.append(f"    - {{ entity: weeks, role: \"week range\", range: \"{p['start']}-{p['end']}\" }}")
        if p["id"] in (1, 2, 3):
            lines.append(f"    - {{ entity: programs, role: \"in program\", program_id: foundations }}")
        elif p["id"] in (4, 5, 6):
            lines.append(f"    - {{ entity: programs, role: \"in program\", program_id: engineering_systems }}")
        elif p["id"] in (7, 8, 9, 10):
            lines.append(f"    - {{ entity: programs, role: \"in program\", program_id: llm_platform }}")
        lines.append("")

    lines.extend([
        "",
        "# ============================================================================",
        "# Weeks (108 entries)",
        "# ============================================================================",
        "",
    ])
    for w in weeks:
        phase_id = phase_for_week(w["week"], phases)
        level, seam, _ = PHASE_META.get(phase_id, (2, "engineering primitives", ""))
        lines.append(f"- id: week-{w['week']:03d}")
        lines.append(f"  week: {w['week']}")
        lines.append(f"  phase: {phase_id}")
        lines.append(f"  module: \"{w['module']}\"")
        lines.append(f"  focus: \"{w['focus']}\"")
        lines.append(f"  mode: {w['mode']}")
        lines.append(f"  deliverable: \"{w['deliverable']}\"")
        lines.append(f"  tier: core")
        lines.append(f"  level: {level}")
        lines.append(f"  seam: \"{seam}\"")
        # cross_references: gate (if any), phase
        lines.append(f"  cross_references:")
        lines.append(f"    - {{ entity: phases, phase_id: phase-{phase_id} }}")
        if w["week"] in WEEK_TO_GATE:
            gate_num = WEEK_TO_GATE[w["week"]]
            lines.append(f"    - {{ entity: gates, gate_id: gate-{gate_num}, role: \"exit criterion\" }}")
        if w["week"] in RECOVERY_AFTER:
            lines.append(f"    - {{ entity: weeks, role: \"recovery_after\" }}")
        lines.append("")

    lines.extend([
        "",
        "# ============================================================================",
        "# Recovery weeks (deliberate buffer windows)",
        "# ============================================================================",
        "",
    ])
    for w in RECOVERY_AFTER:
        lines.append(f"- id: recovery-after-week-{w}")
        lines.append(f"  after_week: {w}")
        lines.append(f"  phase: {phase_for_week(w, phases)}")
        lines.append(f"  tier: core")
        lines.append(f"  level: 1")
        lines.append(f"  seam: \"recovery\"")
        lines.append(f"  selection_rationale: >")
        lines.append(
            f"    Deliberate buffer after week {w} so the learner can consolidate, "
            "remediate failed gates, or rest. Recovery weeks are generated, "
            "not additional topics."
        )
        lines.append(f"  cross_references:")
        lines.append(f"    - {{ entity: weeks, week: {w}, role: \"recovery after\" }}")
        lines.append("")

    lines.extend([
        "",
        "# ============================================================================",
        "# GPU weeks (the only deploy_benchmark mode entries)",
        "# ============================================================================",
        "",
    ])
    gpu_weeks = [w for w in weeks if w["mode"] == "deploy_benchmark"]
    for w in gpu_weeks:
        lines.append(f"- id: gpu-week-{w['week']}")
        lines.append(f"  week: {w['week']}")
        lines.append(f"  module: \"{w['module']}\"")
        lines.append(f"  cross_references:")
        lines.append(f"    - {{ entity: weeks, week: {w['week']} }}")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    ts_text = WEEKS_TS.read_text(encoding="utf-8")
    phases = parse_phases(ts_text)
    weeks = parse_weeks(ts_text)

    print(f"Parsed {len(phases)} phases and {len(weeks)} weeks from {WEEKS_TS}")

    yaml_content = render_yaml(phases, weeks)
    OUT.write_text(yaml_content, encoding="utf-8")
    print(f"Wrote {OUT} ({len(yaml_content):,} bytes)")

    # Sanity check: 108 weeks, 10 phases, 13 recovery weeks, 4 GPU weeks.
    assert len(phases) == 10, f"expected 10 phases, got {len(phases)}"
    assert len(weeks) == 108, f"expected 108 weeks, got {len(weeks)}"
    gpu_count = sum(1 for w in weeks if w["mode"] == "deploy_benchmark")
    assert gpu_count == 4, f"expected 4 GPU weeks, got {gpu_count}"
    print(f"Sanity checks passed: 10 phases, 108 weeks, {gpu_count} GPU weeks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
