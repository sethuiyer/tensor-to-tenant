"""Focused T2.1 checks for schema-driven capstone artifacts."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schema" / "capstones.yaml"


def _generator_module():
    spec = importlib.util.spec_from_file_location("generate_capstones", ROOT / "tools/generate_capstones.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_schema_contains_three_structured_capstones() -> None:
    records = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    assert [record["id"] for record in records] == ["capstone-1", "capstone-2", "capstone-3"]
    assert len(records[0]["events"]) == 6
    assert records[0]["queries"] == [[0, 4], [1, 5]]
    assert records[0]["expected"][0] == {
        "top_error_model": 1,
        "count": 2,
        "distinct": 3,
        "wasted": 380,
    }
    assert records[1]["tree"]["root"] == 0
    assert len(records[1]["tree"]["nodes"]) == len(records[1]["tree"]["children"]) == 5
    assert records[1]["queries"] == [0, 2]
    assert records[1]["expected"][1]["wasted_tokens"] == 280
    assert len(records[2]["failure_matrix"]) == 10
    assert len(records[2]["interview_questions"]) == 7
    assert records[2]["rubric"]["points"] == 24


def test_capstone_generator_check_is_clean_and_non_mutating() -> None:
    result = subprocess.run(
        [sys.executable, "tools/generate_capstones.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_generated_page_data_and_prose_matrix_use_schema() -> None:
    generator = _generator_module()
    records = generator.load_capstones()
    output = (ROOT / "src/data/capstones.ts").read_text(encoding="utf-8")
    page = (ROOT / "src/pages/capstones/ai-gateway.astro").read_text(encoding="utf-8")
    index = (ROOT / "src/pages/capstones/index.astro").read_text(encoding="utf-8")

    assert "export const CAPSTONES" in output
    assert '"failureMatrix"' in output
    assert "CAPSTONE_3" in page
    assert "const failureMatrix = [" not in page
    assert "{r.failure}" in page and "{r.expectedBehavior}" in page
    assert "CAPSTONES" in index and "const capstones = [" not in index

    expected_block = generator.render_failure_matrix_markdown(records[2])
    prose = (ROOT / "CAPSTONE3_OPENROUTER.md").read_text(encoding="utf-8")
    assert expected_block in prose
    assert prose.count(generator.MARKER_START) == prose.count(generator.MARKER_END) == 1
