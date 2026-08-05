"""Focused contract tests for the T1.12 paired deep-dive track."""

from __future__ import annotations

import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schema" / "deep_dives.yaml"


def _entries() -> list[dict]:
    entries = yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))
    assert isinstance(entries, list)
    return entries


def test_parallel_tracks_are_strict_theory_production_pairs() -> None:
    entries = _entries()
    by_id = {entry["id"]: entry for entry in entries}
    parallel_tracks = [entry for entry in entries if entry.get("parallel_track") is True]
    assert parallel_tracks, "deep_dives.yaml must declare a parallel track"

    for track in parallel_tracks:
        assert track["pair_enforcement"] == "strict"
        artifacts = track["primary_artifacts"]
        roles = {artifact["role"] for artifact in artifacts}
        assert {"theory", "production"} <= roles
        theory_refs = [artifact for artifact in artifacts if artifact["role"] == "theory"]
        production_refs = [artifact for artifact in artifacts if artifact["role"] == "production"]
        assert theory_refs and production_refs
        theory_ids = {artifact["id"] for artifact in theory_refs}
        records = [by_id[artifact["id"]] for artifact in artifacts]
        assert all(record["pair_id"] == track["id"] for record in records)
        assert all(record["selection_rationale"].strip() for record in records)
        assert all(record["cross_references"] for record in records)

        for production_ref in production_refs:
            production = by_id[production_ref["id"]]
            assert production["prerequisite_of"] in theory_ids


def test_local_artifacts_exist_and_match_declared_section_counts() -> None:
    for entry in _entries():
        path = entry.get("path")
        if not path:
            continue
        artifact = ROOT / path
        assert artifact.is_file(), f"missing local deep-dive: {path}"
        assert entry["selection_rationale"].strip()
        assert entry["cross_references"]
        assert entry["pair_id"]
        numbered_sections = re.findall(
            r"^#{1,6}\s+(\d+)\.\s+", artifact.read_text(encoding="utf-8"), re.MULTILINE
        )
        assert len(numbered_sections) == entry["section_count"], (
            f"{path}: schema says {entry['section_count']}, found {len(numbered_sections)}"
        )
        assert numbered_sections == [str(number) for number in range(1, entry["section_count"] + 1)]


def test_recommender_is_wired_to_site_and_learner_scaffold() -> None:
    page = (ROOT / "src/pages/recommender.astro").read_text(encoding="utf-8")
    assert "TOOL_RECOMMENDATION_SYSTEMS" in page
    assert "cross-reference" in page.lower()
    assert "SEARCH.md" in page and "SNOWFLAKE.md" in page
    assert (ROOT / "src/data/deepDives.ts").exists()
    assert "recommender" in (ROOT / "src/layouts/BaseLayout.astro").read_text(encoding="utf-8")
    assert "Recommender" in (ROOT / "src/config.ts").read_text(encoding="utf-8")

    scaffold = ROOT / "cookiecutter/{{cookiecutter.repo_name}}/09_interview/recommender"
    for path in ("README.md", "SEARCH.md", "SNOWFLAKE.md", "progress.md", "exercises/README.md"):
        assert (scaffold / path).is_file(), f"missing scaffold file: {path}"
    progress = (scaffold / "progress.md").read_text(encoding="utf-8")
    assert progress.count("- [ ]") == 41  # 17 theory + 24 production sections
    learner_readme = (ROOT / "cookiecutter/{{cookiecutter.repo_name}}/README.md").read_text(
        encoding="utf-8"
    )
    assert "Tool recommendation systems" in learner_readme


def test_status_reports_recommender_progress() -> None:
    makefile = (ROOT / "cookiecutter/{{cookiecutter.repo_name}}/Makefile").read_text(
        encoding="utf-8"
    )
    progress = (ROOT / "cookiecutter/{{cookiecutter.repo_name}}/scripts/progress.py").read_text(
        encoding="utf-8"
    )
    assert "scripts/progress.py --recommender-only" in makefile
    assert "Recommender:" in progress
