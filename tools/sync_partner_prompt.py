"""Validate the cookiecutter learning-partner prompt against schema IDs.

The learner repository intentionally does not carry ``schema/*.yaml``.  This
source-tree check is therefore the build-time side of T2.4: it loads the
schema IDs, imports the stdlib-only validator shipped in the cookiecutter,
and fails before a stale ``AGENTS.md`` can be generated.

Usage::

    python tools/sync_partner_prompt.py
    python tools/sync_partner_prompt.py --agents path/to/AGENTS.md
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_AGENTS = ROOT / "cookiecutter" / "{{cookiecutter.repo_name}}" / "AGENTS.md"
DEFAULT_WEEKS = ROOT / "schema" / "weeks.yaml"
DEFAULT_GATES = ROOT / "schema" / "gates.yaml"
PARTNER_SCRIPT = (
    ROOT / "cookiecutter" / "{{cookiecutter.repo_name}}" / "scripts" / "learning_partner.py"
)


class PartnerPromptBuildError(RuntimeError):
    """Raised for malformed schema inputs or an invalid partner prompt."""


def _load_records(path: Path) -> list[dict[str, Any]]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise PartnerPromptBuildError(f"missing schema/input file: {path}") from error
    except OSError as error:
        raise PartnerPromptBuildError(f"cannot read {path}: {error}") from error
    except yaml.YAMLError as error:
        raise PartnerPromptBuildError(f"invalid YAML in {path}: {error}") from error
    if not isinstance(value, list):
        raise PartnerPromptBuildError(f"{path}: expected a YAML list of records")
    records = [item for item in value if isinstance(item, dict)]
    if len(records) != len(value):
        raise PartnerPromptBuildError(f"{path}: every YAML item must be a mapping")
    return records


def schema_reference_ids(
    weeks_path: Path = DEFAULT_WEEKS,
    gates_path: Path = DEFAULT_GATES,
) -> tuple[tuple[str, ...], tuple[str, ...], dict[str, int]]:
    """Return canonical week IDs, gate IDs, and gate exit weeks from YAML."""
    week_rows = _load_records(weeks_path)
    week_ids = tuple(
        row["id"]
        for row in sorted(
            week_rows,
            key=lambda row: int(row.get("week", 0)) if row.get("week") is not None else -1,
        )
        if isinstance(row.get("id"), str)
        and row["id"].startswith("week-")
        and row.get("week") is not None
    )
    gate_rows = _load_records(gates_path)
    gate_rows = [
        row
        for row in gate_rows
        if isinstance(row.get("id"), str)
        and row["id"].startswith("gate-")
        and row.get("gate") is not None
    ]
    gate_rows.sort(key=lambda row: int(row["gate"]))
    gate_ids = tuple(row["id"] for row in gate_rows)
    gate_weeks = {
        row["id"]: int(row["week"])
        for row in gate_rows
        if row.get("week") is not None
    }
    if not week_ids:
        raise PartnerPromptBuildError(f"{weeks_path}: no week-* records found")
    if not gate_ids:
        raise PartnerPromptBuildError(f"{gates_path}: no gate-* records found")
    return week_ids, gate_ids, gate_weeks


def _load_partner_validator(path: Path = PARTNER_SCRIPT) -> Any:
    spec = importlib.util.spec_from_file_location("cookiecutter_learning_partner", path)
    if spec is None or spec.loader is None:
        raise PartnerPromptBuildError(f"cannot import partner validator: {path}")
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except (OSError, SyntaxError, ImportError) as error:
        raise PartnerPromptBuildError(f"cannot import partner validator {path}: {error}") from error
    return module


def validate_partner_prompt(
    agents_path: Path = DEFAULT_AGENTS,
    weeks_path: Path = DEFAULT_WEEKS,
    gates_path: Path = DEFAULT_GATES,
) -> None:
    """Validate one AGENTS.md against canonical schema IDs."""
    try:
        text = agents_path.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise PartnerPromptBuildError(f"missing AGENTS.md prompt: {agents_path}") from error
    except OSError as error:
        raise PartnerPromptBuildError(f"cannot read AGENTS.md {agents_path}: {error}") from error
    week_ids, gate_ids, _gate_weeks = schema_reference_ids(weeks_path, gates_path)
    validator = _load_partner_validator()
    try:
        validator.validate_agents_references(
            text,
            week_ids,
            gate_ids,
            source=agents_path,
        )
    except Exception as error:
        # Preserve the useful validator wording but make this CLI's failure
        # boundary unambiguous to build systems and users.
        raise PartnerPromptBuildError(str(error)) from error


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate cookiecutter AGENTS.md week/gate references against schema YAML."
    )
    parser.add_argument("--agents", type=Path, default=DEFAULT_AGENTS, help=f"prompt path (default: {DEFAULT_AGENTS})")
    parser.add_argument("--weeks", type=Path, default=DEFAULT_WEEKS, help=f"weeks schema (default: {DEFAULT_WEEKS})")
    parser.add_argument("--gates", type=Path, default=DEFAULT_GATES, help=f"gates schema (default: {DEFAULT_GATES})")
    args = parser.parse_args(argv)
    try:
        validate_partner_prompt(args.agents, args.weeks, args.gates)
    except PartnerPromptBuildError as error:
        print(f"sync_partner_prompt.py: error: {error}", file=sys.stderr)
        return 1
    print(f"sync_partner_prompt.py: {args.agents} references valid schema weeks and gates")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
