"""Structural drift checks between canonical YAML and generated site data.

Unlike a text grep, this tool parses the generated TypeScript literals and
checks identifiers, ranges, counts, modes, and cross-reference targets.  It
never runs the generator in place: a hand-edited generated file is therefore
visible as drift.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

TOOLS = Path(__file__).resolve().parent
REPO_ROOT = TOOLS.parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import generate  # noqa: E402


def _records(value: Any) -> list[dict[str, Any]]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []


def _yaml(name: str) -> list[dict[str, Any]]:
    with (REPO_ROOT / "schema" / name).open(encoding="utf-8") as handle:
        return _records(yaml.safe_load(handle) or [])


def _num(value: Any) -> int | Any:
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return value


def _same(expected: Any, actual: Any, label: str, errors: list[str]) -> None:
    if expected != actual:
        errors.append(f"{label}: expected {expected!r}, got {actual!r}")


def collect_drift() -> list[str]:
    errors: list[str] = []
    weeks_schema = _yaml("weeks.yaml")
    phases_schema = [row for row in weeks_schema if str(row.get("id", "")).startswith("phase-")]
    week_schema = [row for row in weeks_schema if str(row.get("id", "")).startswith("week-")]
    recovery_schema = [row for row in weeks_schema if str(row.get("id", "")).startswith("recovery-after-week-")]
    gpu_schema = [row for row in weeks_schema if str(row.get("id", "")).startswith("gpu-week-")]

    weeks_ts = generate._literal_values((REPO_ROOT / "src/data/weeks.ts").read_text(encoding="utf-8"))
    phases_ts = weeks_ts.get("PHASES", [])
    weeks_ts_rows = weeks_ts.get("WEEKS", [])
    _same(
        sorted(int(_num(row.get("number"))) for row in phases_schema),
        sorted(int(row.get("id")) for row in phases_ts),
        "phase IDs",
        errors,
    )
    expected_phase_rows = [
        {
            "id": _num(row.get("number")),
            "weeks": row.get("weeks", ""),
            "theme": row.get("theme", ""),
            "start": _num(row.get("start")),
            "end": _num(row.get("end")),
        }
        for row in sorted(phases_schema, key=lambda item: int(_num(item.get("number"))))
    ]
    _same(expected_phase_rows, phases_ts, "PHASES", errors)
    expected_week_rows = [
        {
            "week": _num(row.get("week")),
            "module": row.get("module", ""),
            "focus": row.get("focus", ""),
            "mode": row.get("mode", ""),
            "deliverable": row.get("deliverable", ""),
        }
        for row in sorted(week_schema, key=lambda item: int(_num(item.get("week"))))
    ]
    _same(expected_week_rows, weeks_ts_rows, "WEEKS", errors)
    _same(
        sorted(int(_num(row.get("after_week"))) for row in recovery_schema),
        sorted(weeks_ts.get("RECOVERY_AFTER", [])),
        "RECOVERY_AFTER",
        errors,
    )

    modes = {"implement", "read_diagram", "deploy_benchmark"}
    actual_counts = {mode: sum(row.get("mode") == mode for row in weeks_ts_rows) for mode in modes}
    if set(actual_counts) != modes or sum(actual_counts.values()) != 108:
        errors.append(f"MODE_COUNTS: invalid mode distribution {actual_counts}")
    expected_gpu = [row["week"] for row in expected_week_rows if row["mode"] == "deploy_benchmark"]
    actual_gpu = [row["week"] for row in weeks_ts_rows if row["mode"] == "deploy_benchmark"]
    _same(expected_gpu, actual_gpu, "GPU_WEEKS derived rows", errors)
    _same(
        sorted(int(_num(row.get("week"))) for row in gpu_schema),
        sorted(actual_gpu),
        "gpu-week schema rows",
        errors,
    )

    gates_schema = _yaml("gates.yaml")
    gate_schema = [row for row in gates_schema if row.get("gate") is not None]
    program_schema = [row for row in gates_schema if row.get("release_week") is not None]
    gates_ts = generate._literal_values((REPO_ROOT / "src/data/gates.ts").read_text(encoding="utf-8"))
    expected_gates = [
        {
            "gate": _num(row.get("gate")),
            "week": _num(row.get("week")),
            "criteria": row.get("criteria", ""),
            "remediation": row.get("remediation", ""),
        }
        for row in sorted(gate_schema, key=lambda item: int(_num(item.get("gate"))))
    ]
    expected_programs = [
        {
            "name": row.get("name", ""),
            "weeks": row.get("weeks", ""),
            "releaseWeek": _num(row.get("release_week")),
            "release": row.get("release", ""),
        }
        for row in sorted(program_schema, key=lambda item: int(_num(item.get("release_week"))))
    ]
    _same(expected_gates, gates_ts.get("GATES", []), "GATES", errors)
    _same(expected_programs, gates_ts.get("PROGRAMS", []), "PROGRAMS", errors)

    # Cross-reference checks are conditional: the current phase rows do not
    # declare mandala IDs, so no artificial phase→mandala requirement is made.
    phase_ids = {f"phase-{int(_num(row.get('number')))}" for row in phases_schema}
    gate_ids = {f"gate-{int(_num(row.get('gate')))}" for row in gate_schema}
    week_ids = {f"week-{int(_num(row.get('week'))):03d}" for row in week_schema}
    for filename, rows in (("weeks.yaml", weeks_schema), ("gates.yaml", gates_schema)):
        for index, row in enumerate(rows):
            for ref_index, ref in enumerate(row.get("cross_references", []) or []):
                if not isinstance(ref, dict):
                    errors.append(f"{filename}[{index}].cross_references[{ref_index}] is not a mapping")
                    continue
                entity = ref.get("entity")
                target = ref.get("phase_id") or ref.get("gate_id")
                known = {"phases": phase_ids, "gates": gate_ids, "weeks": week_ids}.get(entity)
                if entity == "gates" and isinstance(target, int):
                    target = f"gate-{target}"
                if target and known is not None and target not in known:
                    errors.append(f"{filename}[{index}].cross_references[{ref_index}] targets unknown {target!r}")

    mandala_schema = _yaml("mandalas.yaml")
    mandala_ids = {row.get("id") for row in mandala_schema if row.get("id")}
    mandalas_ts = generate._literal_values((REPO_ROOT / "src/data/mandalas.ts").read_text(encoding="utf-8"))
    if len(mandalas_ts.get("MANDALAS", [])) != len(mandala_ids):
        errors.append(
            f"mandala count: schema has {len(mandala_ids)}, site has {len(mandalas_ts.get('MANDALAS', []))}"
        )
    for row in phases_schema:
        for ref in row.get("cross_references", []) or []:
            if isinstance(ref, dict) and ref.get("entity") == "mandalas" and ref.get("mandala_id") not in mandala_ids:
                errors.append(f"phase {row.get('id')} references unknown mandala {ref.get('mandala_id')!r}")

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    errors = collect_drift()
    if errors:
        print("drift_report.py: drift detected:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print("drift_report.py: schema and generated site data agree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
