"""Focused T2.4 tests for the schema-aware learning partner prompt."""
from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parent.parent
PARTNER = ROOT / "cookiecutter/{{cookiecutter.repo_name}}/scripts/learning_partner.py"
AGENTS = ROOT / "cookiecutter/{{cookiecutter.repo_name}}/AGENTS.md"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def partner():
    return _load(PARTNER, "learning_partner_t24_test")


@pytest.fixture(scope="module")
def sync_tool():
    return _load(ROOT / "tools/sync_partner_prompt.py", "sync_partner_prompt_t24_test")


def test_extract_prompt_references_expands_ranges_and_ignores_placeholders(partner) -> None:
    refs = partner.extract_prompt_references(
        "See Weeks 7-10 and week_014.md; Gate 2 and gate-3 are next. "
        "The prior week_NNN-1 file is a placeholder."
    )
    assert refs["weeks"] == {7, 8, 9, 10, 14}
    assert refs["gates"] == {"gate-2", "gate-3"}


def test_validate_prompt_references_reports_missing_ids_with_lines(partner) -> None:
    with pytest.raises(partner.PartnerPromptValidationError) as error:
        partner.validate_agents_references(
            "Week 109 is not in the spine.\nGate 11 is not in the gates.",
            [f"week-{number:03d}" for number in range(1, 109)],
            [f"gate-{number}" for number in range(1, 11)],
            source="tmp/AGENTS.md",
        )
    message = str(error.value)
    assert "tmp/AGENTS.md" in message
    assert "week-109" in message and "line 1" in message
    assert "gate-11" in message and "line 2" in message
    assert "known" in message


def test_source_sync_validates_checked_in_prompt(sync_tool) -> None:
    # This is the build-time assertion used by npm prebuild and can run
    # without invoking the network-backed learning partner CLI.
    sync_tool.validate_partner_prompt()


def test_source_sync_cli_fails_clearly_for_invalid_prompt(tmp_path: Path) -> None:
    bad_agents = tmp_path / "AGENTS.md"
    bad_agents.write_text("Use Week 109 and Gate 11.", encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            "tools/sync_partner_prompt.py",
            "--agents",
            str(bad_agents),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "unknown week reference" in result.stderr
    assert "week-109" in result.stderr
    assert "unknown gate reference" in result.stderr
    assert "gate-11" in result.stderr


def test_cookiecutter_hook_revalidates_rendered_prompt(tmp_path: Path) -> None:
    """The post-gen hook validates the actual AGENTS.md artifact too."""
    hook = _load(ROOT / "cookiecutter/hooks/post_gen_project.py", "post_gen_t24_test")
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    shutil.copy2(PARTNER, scripts / "learning_partner.py")
    (tmp_path / "AGENTS.md").write_text(AGENTS.read_text(encoding="utf-8"), encoding="utf-8")

    # Valid template survives the same function the hook calls in main().
    hook.validate_learning_partner_prompt(tmp_path)

    (tmp_path / "AGENTS.md").write_text("Week 109 and Gate 11.", encoding="utf-8")
    with pytest.raises(RuntimeError, match=r"week-109.*gate-11"):
        hook.validate_learning_partner_prompt(tmp_path)
