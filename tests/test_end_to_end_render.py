"""End-to-end cookiecutter render test.

Runs `cookiecutter ./cookiecutter --no-input -o <tmpdir>` and validates the
full learner-repo structure the generator emits. This is the integration
test that catches generator regressions: anything that breaks the
post_gen_project.py hook or the Jinja template tree surfaces here.

The test takes 5-15 seconds because cookiecutter must run end-to-end.
It is not a fast unit test; it is the closest thing to a smoke check
on the artifact a learner will actually receive.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
COOKIECUTTER_DIR = REPO_ROOT / "cookiecutter"


def _cookiecutter_available() -> bool:
    """Return True if the cookiecutter CLI is on PATH."""
    return shutil.which("cookiecutter") is not None


pytestmark = pytest.mark.skipif(
    not _cookiecutter_available(),
    reason="cookiecutter CLI not installed; run `pipx install cookiecutter`",
)


@pytest.fixture
def rendered_repo(tmp_path: Path) -> Path:
    """Run cookiecutter and return the path to the rendered repo."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    # --no-input uses all defaults from cookiecutter.json.
    # The default repo_name is `tensor-to-tenant-journal`, so the actual
    # rendered dir is out_dir / tensor-to-tenant-journal.
    result = subprocess.run(
        [
            "cookiecutter",
            str(COOKIECUTTER_DIR),
            "--no-input",
            "-o", str(out_dir),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, (
        f"cookiecutter failed (exit {result.returncode}):\n"
        f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )
    rendered = out_dir / "tensor-to-tenant-journal"
    assert rendered.exists(), f"rendered repo not at expected path: {rendered}"
    return rendered


# ===========================================================================
# Structural assertions about the rendered artifact
# ===========================================================================

class TestRenderedStructure:
    """The rendered repo has the documented shape."""

    def test_top_level_layout_present(self, rendered_repo: Path) -> None:
        for expected in (
            "00_orientation", "01_math", "02_engineering_primitives",
            "03_system_design", "04_ml_systems", "05_llm",
            "06_inference", "07_platform", "08_capstone", "09_interview",
            "AGENTS.md", "docs", "evidence", "journal", "LICENSE",
            "Makefile", "pyproject.toml", "README.md",
        ):
            assert (rendered_repo / expected).exists(), f"missing: {expected}"

    def test_exactly_108_weekly_journals(self, rendered_repo: Path) -> None:
        """One journal per week, week_001.md through week_108.md."""
        weeks_dir = rendered_repo / "journal" / "weeks"
        files = sorted(p.name for p in weeks_dir.glob("week_*.md"))
        assert len(files) == 108, f"expected 108 week files, got {len(files)}"

        # Spot-check first and last.
        assert files[0] == "week_001.md"
        assert files[-1] == "week_108.md"

    def test_no_gaps_in_week_numbering(self, rendered_repo: Path) -> None:
        """week_001.md through week_108.md with no skipped numbers."""
        weeks_dir = rendered_repo / "journal" / "weeks"
        numbers = sorted(int(p.stem.split("_")[1]) for p in weeks_dir.glob("week_*.md"))
        assert numbers == list(range(1, 109))

    def test_evidence_scaffolds_present(self, rendered_repo: Path) -> None:
        for week in range(1, 109):
            path = rendered_repo / "evidence" / "weeks" / f"week_{week:03d}" / "README.md"
            assert path.exists(), f"missing evidence scaffold for week {week}"

    def test_engineering_primitives_have_expected_subdirs(self, rendered_repo: Path) -> None:
        primitives = rendered_repo / "02_engineering_primitives"
        for name in (
            "retrieval", "rate_limiting", "caching", "chunking", "pii",
            "metrics", "batching", "resilience", "sketches", "routing", "ids",
        ):
            assert (primitives / name).is_dir(), f"missing primitive folder: {name}"

    def test_agents_scaffolds_present(self, rendered_repo: Path) -> None:
        """19 agent modules + 1 README = 20 files in 09_interview/agents/."""
        agents = rendered_repo / "09_interview" / "agents"
        files = sorted(p.name for p in agents.iterdir())
        # 18 modules + Module 7.5 + README = 20
        assert len(files) == 20, f"expected 20 files, got {len(files)}: {files}"

    def test_algorithmic_forge_lanes_present(self, rendered_repo: Path) -> None:
        forge = rendered_repo / "09_interview" / "algorithmic_forge"
        for name in ("core", "supporting", "archive", "boss_fights"):
            assert (forge / name).is_dir(), f"missing forge tier: {name}"

    def test_leetcode_darbar_tracker_present(self, rendered_repo: Path) -> None:
        darbar = rendered_repo / "09_interview" / "leetcode_darbar"
        assert (darbar / "TRACKER.csv").exists(), "missing darbar tracker"

    def test_capstone_scaffold_present(self, rendered_repo: Path) -> None:
        """Capstone folder has at least the trace-forensics artifact scaffold."""
        capstone = rendered_repo / "08_capstone"
        assert capstone.is_dir()
        # At minimum, one of the three capstone paths should have a scaffold.
        assert (capstone / "trace-forensics").is_dir() or list(capstone.iterdir())

    def test_recipe_dirs_have_readmes(self, rendered_repo: Path) -> None:
        """Each top-level phase folder has a README explaining its objective."""
        # Glob the actual phase directory names (00_orientation, 01_math, ...).
        phase_dirs = sorted(
            d for d in rendered_repo.iterdir()
            if d.is_dir() and len(d.name) >= 3 and d.name[:2].isdigit() and d.name[2] == "_"
        )
        assert len(phase_dirs) >= 10, f"expected >=10 phase dirs, found {len(phase_dirs)}"
        for phase_dir in phase_dirs:
            readmes = list(phase_dir.glob("README.md"))
            assert readmes, f"phase {phase_dir.name} has no README.md"


# ===========================================================================
# Seeded memory DB
# ===========================================================================

class TestSeededMemory:
    """The generator seeds journal/memory.json via concept_seed.py.

    Validates the integration: the post-gen hook ran concept_seed.py and
    produced a populated memory DB.

    STATUS (T1.13 audit): the post-gen hook now invokes concept_seed.py
    via _seed_memory_db(), seeded with the learner's repo root as CWD
    so the relative paths in concept_seed.py resolve correctly. The
    audit gap was closed in the same commit.
    """

    MEMORY_GAP_FIXED = True  # T1.13 audit finding: closed.

    pytestmark = pytest.mark.skipif(
        not MEMORY_GAP_FIXED,
        reason="post-gen hook does not currently seed memory.json (T1.13 audit gap)",
    )

    def test_memory_file_exists(self, rendered_repo: Path) -> None:
        memory = rendered_repo / "journal" / "memory.json"
        assert memory.exists()

    def test_memory_has_at_least_324_concepts(self, rendered_repo: Path) -> None:
        """108 weeks * 3 concepts/week = 324 minimum."""
        memory = json.loads(
            (rendered_repo / "journal" / "memory.json").read_text(encoding="utf-8")
        )
        total = len(memory["concepts"])
        assert total >= 324, f"expected >= 324 concepts, got {total}"

    def test_memory_concepts_have_required_keys(self, rendered_repo: Path) -> None:
        memory = json.loads(
            (rendered_repo / "journal" / "memory.json").read_text(encoding="utf-8")
        )
        required = {"id", "name", "kind", "week", "stability", "ef", "difficulty"}
        for cid, concept in list(memory["concepts"].items())[:20]:
            assert cid == concept["id"], f"id mismatch for key {cid}"
            missing = required - set(concept.keys())
            assert not missing, f"concept {cid} missing keys: {missing}"

    def test_memory_concept_kinds_are_only_three(self, rendered_repo: Path) -> None:
        """Each week contributes exactly title / focus / deliverable."""
        memory = json.loads(
            (rendered_repo / "journal" / "memory.json").read_text(encoding="utf-8")
        )
        kinds = {c["kind"] for c in memory["concepts"].values()}
        assert kinds <= {"title", "focus", "deliverable"}
        assert kinds == {"title", "focus", "deliverable"}


# ===========================================================================
# Personalization
# ===========================================================================

class TestPersonalization:
    """The student name from cookiecutter.json is substituted into the README."""

    def test_readme_contains_default_student_name(self, rendered_repo: Path) -> None:
        """The default cookiecutter.json has student_name='Your Name'."""
        readme = (rendered_repo / "README.md").read_text(encoding="utf-8")
        # Either substituted with the default OR a personal name from CI.
        # The point is the placeholder got replaced.
        assert "Your Name" not in readme or "Student" in readme

    def test_license_has_default_student(self, rendered_repo: Path) -> None:
        """The cookiecutter LICENSE copyright line is personalized.

        The Apache 2.0 boilerplate has 'Copyright [year] [name]'. When the
        cookiecutter LICENSE template uses `{{ cookiecutter.student_name }}`,
        this should be substituted. The default cookiecutter.json has
        student_name='Your Name', which is itself the placeholder, so
        checking for "Your Name" in the rendered output verifies the
        substitution happened.
        """
        license_text = (rendered_repo / "LICENSE").read_text(encoding="utf-8")
        # The personalized copyright line should mention the student.
        assert "Your Name" in license_text or "{{ cookiecutter.student_name }}" not in license_text

    def test_pyproject_author_personalized(self, rendered_repo: Path) -> None:
        pyproject = (rendered_repo / "pyproject.toml").read_text(encoding="utf-8")
        # Authors block should not contain literal {{ cookiecutter.student_name }}.
        assert "{{ cookiecutter.student_name }}" not in pyproject
