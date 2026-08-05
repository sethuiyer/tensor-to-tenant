"""T1.4.e: generated output freshness and deterministic hashes."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "tools" / "generated_hashes.json"


def _paths() -> list[Path]:
    return sorted((ROOT / "src/data").glob("*.ts")) + [
        ROOT / "cookiecutter/hooks/curriculum_generated.py",
        ROOT / "cookiecutter/{{cookiecutter.repo_name}}/.curriculum_generated.py",
    ]


def test_generated_hash_manifest_matches_worktree() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expected = manifest["files"]
    actual = {}
    for path in _paths():
        assert path.exists(), f"missing generated output: {path.relative_to(ROOT)}"
        payload = path.read_bytes()
        rel = str(path.relative_to(ROOT))
        actual[rel] = {
            "sha256": hashlib.sha256(payload).hexdigest(),
            "bytes": len(payload),
        }
    assert actual == expected


def test_generator_check_is_non_mutating_and_clean() -> None:
    result = subprocess.run(
        [sys.executable, "tools/generate.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_drift_report_is_clean() -> None:
    result = subprocess.run(
        [sys.executable, "tools/drift_report.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout
