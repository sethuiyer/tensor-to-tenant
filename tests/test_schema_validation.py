"""T2.2 schema validation/build integration checks."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_schema_validator_cli_passes() -> None:
    result = subprocess.run(
        [sys.executable, "tools/validate_schema.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_prebuild_runs_schema_and_drift_validation() -> None:
    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    command = package["scripts"]["prebuild"]
    assert "validate_schema.py" in command
    assert "generate.py --check" in command
    assert "drift_report.py" in command
