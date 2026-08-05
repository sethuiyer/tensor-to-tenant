"""Unit tests for cookiecutter/.../scripts/concept_seed.py.

Pure-function regex extraction + deterministic memory-DB IO.
Anchor tests to known properties, not arbitrary values.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import pytest

from concept_seed import (
    DELIV_RE,
    FOCUS_RE,
    JOURNAL_DIR,
    MEMORY_FILE,
    SEED_VERSION,
    TITLE_RE,
    WEEK_RE,
    _concept_id,
    _defaults,
    _new_concept_row,
    _slugify,
    extract_concepts,
    load_memory,
    save_memory,
    seed_memory,
    stats,
)


# ===========================================================================
# Regex extraction patterns
# ===========================================================================

class TestWeekFilenameRegex:
    """WEEK_RE matches `week_NNN.md` filenames."""

    @pytest.mark.parametrize(
        "filename,expected_week",
        [
            ("week_001.md", 1),
            ("week_108.md", 108),
            ("week_14.md", 14),
        ],
    )
    def test_matches_three_digit_padded(self, filename: str, expected_week: int) -> None:
        m = WEEK_RE.search(filename)
        assert m is not None
        assert int(m.group(1)) == expected_week

    def test_matches_unpadded(self) -> None:
        """The regex accepts both `week_1.md` and `week_001.md`."""
        m = WEEK_RE.search("week_1.md")
        assert m is not None
        assert int(m.group(1)) == 1

    def test_no_match_on_other_files(self) -> None:
        for bad in ("week_001.txt", "week_.md", "monthly_001.md", "week.md"):
            assert WEEK_RE.search(bad) is None, f"unexpected match on {bad!r}"


class TestTitleRegex:
    """TITLE_RE matches the `# Week N: <title>` heading."""

    def test_extracts_title_after_colon(self) -> None:
        text = "# Week 14: SVD, pseudoinverse, low-rank approximation\n"
        m = TITLE_RE.search(text)
        assert m is not None
        assert m.group("title") == "SVD, pseudoinverse, low-rank approximation"

    def test_does_not_match_section_heading(self) -> None:
        """A `## Week 14:` (h2) must not be picked up; only h1 counts."""
        text = "## Week 14: Not a title\n"
        assert TITLE_RE.search(text) is None


class TestFocusRegex:
    """FOCUS_RE matches `**Focus:** <text>` lines."""

    def test_extracts_focus(self) -> None:
        text = "**Focus:** Cosine similarity, exact KNN\n"
        m = FOCUS_RE.search(text)
        assert m is not None
        assert m.group("focus") == "Cosine similarity, exact KNN"

    def test_stops_at_bold_marker(self) -> None:
        """The focus regex stops at the next `**...**` marker."""
        text = "**Focus:** Stuff **bold** more\n"
        m = FOCUS_RE.search(text)
        assert m is not None
        # Stops at the start of the inner `**bold**`.
        assert m.group("focus").strip() == "Stuff"


class TestDeliverableRegex:
    """DELIV_RE matches `**Core deliverable:** <text>` lines."""

    def test_extracts_deliverable(self) -> None:
        text = "**Core deliverable:** Vector search mini-lab\n"
        m = DELIV_RE.search(text)
        assert m is not None
        assert m.group("deliv") == "Vector search mini-lab"


# ===========================================================================
# Slug + ID helpers
# ===========================================================================

class TestSlugify:
    @pytest.mark.parametrize(
        "raw,slugified",
        [
            ("SVD, pseudoinverse, low-rank approximation", "svd-pseudoinverse-low-rank-approximation"),
            ("Multi-Head Attention (MHA)", "multi-head-attention-mha"),
            ("  leading and trailing spaces  ", "leading-and-trailing-spaces"),
            ("café résumé", "caf-r-sum"),  # non-ASCII -> hyphen
        ],
    )
    def test_lowercases_and_replaces_non_alphanumerics(self, raw: str, slugified: str) -> None:
        assert _slugify(raw) == slugified

    def test_truncates_to_48_chars(self) -> None:
        long = "a" * 100
        assert len(_slugify(long)) == 48

    def test_empty_string_returns_concept(self) -> None:
        """Empty input -> 'concept' fallback so the ID is never empty."""
        assert _slugify("") == "concept"
        assert _slugify("---") == "concept"


class TestConceptId:
    def test_format_is_w_zero_padded_week(self) -> None:
        """Week is zero-padded to 3 digits so IDs sort lexically."""
        cid = _concept_id(week=1, kind="title", text="Foo")
        assert cid.startswith("w001-")
        cid = _concept_id(week=108, kind="title", text="Foo")
        assert cid.startswith("w108-")

    def test_format_includes_kind(self) -> None:
        cid = _concept_id(week=14, kind="focus", text="Foo")
        assert "focus" in cid

    def test_format_includes_slugified_text(self) -> None:
        cid = _concept_id(week=14, kind="title", text="Hello, World!")
        assert cid.endswith("-hello-world")

    def test_two_distinct_texts_produce_two_ids(self) -> None:
        a = _concept_id(week=14, kind="title", text="Foo")
        b = _concept_id(week=14, kind="title", text="Bar")
        assert a != b

    def test_dedup_within_one_week_one_kind(self) -> None:
        """Identical text -> identical ID (used by extract_concepts to dedupe)."""
        a = _concept_id(week=14, kind="title", text="Foo")
        b = _concept_id(week=14, kind="title", text="Foo")
        assert a == b


# ===========================================================================
# extract_concepts()
# ===========================================================================

def _sample_journal(week: int = 14) -> str:
    """Minimal but realistic journal block matching the cookiecutter template."""
    return (
        f"# Week {week}: SVD, pseudoinverse, low-rank approximation\n"
        f"\n"
        f"**Phase 2 -- Mathematical Foundations I** (Weeks 7 to 18)\n"
        f"**Dates:** 2026-04-06 to 2026-04-12\n"
        f"**Focus:** Matrix norms and conditioning, perturbation analysis\n"
        f"**Core deliverable:** Low-rank compression demo\n"
        f"\n"
        f"## Core objective\n"
        f"-\n"
    )


class TestExtractConcepts:
    def test_extracts_three_concepts_from_realistic_journal(self) -> None:
        concepts = extract_concepts(14, _sample_journal(14))
        kinds = [c["kind"] for c in concepts]
        assert kinds == ["title", "focus", "deliverable"]

    def test_returns_list_of_dicts_with_required_keys(self) -> None:
        concepts = extract_concepts(14, _sample_journal(14))
        for c in concepts:
            assert {"id", "name", "kind", "week"} <= set(c.keys())

    def test_week_field_is_preserved(self) -> None:
        concepts = extract_concepts(42, _sample_journal(42))
        assert all(c["week"] == 42 for c in concepts)

    def test_missing_fields_yield_fewer_concepts(self) -> None:
        """A journal with only a title extracts one concept, not three."""
        concepts = extract_concepts(14, "# Week 14: Just a title\n")
        assert len(concepts) == 1
        assert concepts[0]["kind"] == "title"

    def test_empty_journal_extracts_nothing(self) -> None:
        assert extract_concepts(14, "") == []

    def test_short_focus_or_deliverable_skipped(self) -> None:
        """Values < 3 chars are dropped — the add() guard."""
        text = (
            "# Week 14: Title\n"
            "**Focus:** x\n"           # 1 char -> skipped
            "**Core deliverable:** Low-rank demo\n"
        )
        concepts = extract_concepts(14, text)
        kinds = [c["kind"] for c in concepts]
        assert "focus" not in kinds
        assert "title" in kinds
        assert "deliverable" in kinds

    def test_whitespace_only_value_skipped(self) -> None:
        text = (
            "# Week 14: Title\n"
            "**Focus:**     \n"        # whitespace -> stripped -> empty -> skipped
        )
        concepts = extract_concepts(14, text)
        assert "focus" not in [c["kind"] for c in concepts]

    def test_duplicate_text_different_kinds_kept_separate(self) -> None:
        """Title and focus are different kinds -> different IDs even with identical text.

        The dedup is keyed by (week, kind, slugified_text); the kind
        distinguishes a title concept from a focus concept even when
        their human-readable text happens to coincide.
        """
        same_text = "SVD everywhere"
        text = (
            f"# Week 14: {same_text}\n"
            f"**Focus:** {same_text}\n"
        )
        concepts = extract_concepts(14, text)
        # Both kept — different kinds, different concept IDs.
        assert len(concepts) == 2
        ids = {c["id"] for c in concepts}
        # The kind is part of the ID, so they don't collide.
        assert any("title" in cid for cid in ids)
        assert any("focus" in cid for cid in ids)


# ===========================================================================
# Memory DB IO
# ===========================================================================

class TestMemoryDefaults:
    def test_defaults_have_required_keys(self) -> None:
        d = _defaults()
        assert d["version"] == SEED_VERSION
        assert d["seeded_from"] == "journal"
        assert d["concepts"] == {}

    def test_defaults_have_no_concepts(self) -> None:
        d = _defaults()
        assert len(d["concepts"]) == 0


class TestNewConceptRow:
    def test_spreads_input_keys(self) -> None:
        c = {"id": "w001-title-foo", "name": "Foo", "kind": "title", "week": 1}
        row = _new_concept_row(c)
        # Original keys are present.
        assert row["id"] == "w001-title-foo"
        assert row["name"] == "Foo"
        assert row["kind"] == "title"
        assert row["week"] == 1

    def test_sm2_defaults_present(self) -> None:
        """The RPG layer depends on these defaults — verify they don't drift."""
        c = {"id": "x", "name": "x", "kind": "x", "week": 1}
        row = _new_concept_row(c)
        assert row["stability"] == 1.0
        assert row["ef"] == 2.5
        assert row["difficulty"] == 3

    def test_battle_history_starts_at_zero(self) -> None:
        c = {"id": "x", "name": "x", "kind": "x", "week": 1}
        row = _new_concept_row(c)
        assert row["last_score"] is None
        assert row["last_seen"] is None
        assert row["times_fought"] == 0
        assert row["times_rescued"] == 0
        assert row["times_lost"] == 0


class TestLoadMemory:
    def test_missing_file_returns_defaults(self, tmp_path: Path) -> None:
        """load_memory of a non-existent path returns _defaults()."""
        path = tmp_path / "no_such_file.json"
        assert load_memory(path) == _defaults()

    def test_round_trips_valid_json(self, tmp_path: Path) -> None:
        path = tmp_path / "memory.json"
        original = _defaults()
        original["concepts"]["w001-title-x"] = _new_concept_row(
            {"id": "w001-title-x", "name": "x", "kind": "title", "week": 1}
        )
        save_memory(original, path)
        loaded = load_memory(path)
        assert loaded == original


class TestSaveMemory:
    def test_creates_parent_directory(self, tmp_path: Path) -> None:
        """save_memory must mkdir -p the parent (called on first seed)."""
        path = tmp_path / "deep" / "nested" / "memory.json"
        save_memory(_defaults(), path)
        assert path.exists()

    def test_writes_valid_json(self, tmp_path: Path) -> None:
        path = tmp_path / "memory.json"
        save_memory(_defaults(), path)
        # Must round-trip through json.loads.
        assert json.loads(path.read_text(encoding="utf-8"))


# ===========================================================================
# seed_memory() — the integration test for the extraction + IO pipeline
# ===========================================================================

class TestSeedMemory:
    def test_no_journal_dir_returns_defaults(self, tmp_path: Path) -> None:
        """If journal/weeks doesn't exist, seed_memory returns defaults."""
        empty = tmp_path / "empty_journal"
        result = seed_memory(
            journal_dir=empty,
            memory_file=tmp_path / "memory.json",
        )
        assert result == _defaults()

    def test_seeds_three_concepts_per_week(self, tmp_path: Path) -> None:
        journal = tmp_path / "weeks"
        journal.mkdir()
        (journal / "week_001.md").write_text(_sample_journal(1), encoding="utf-8")
        (journal / "week_002.md").write_text(_sample_journal(2), encoding="utf-8")
        memory_file = tmp_path / "memory.json"
        result = seed_memory(journal_dir=journal, memory_file=memory_file)
        assert len(result["concepts"]) == 6  # 2 weeks x 3 concepts

    def test_skips_files_not_matching_week_pattern(self, tmp_path: Path) -> None:
        """Non-week_*.md files are ignored (e.g. README.md, journal entries)."""
        journal = tmp_path / "weeks"
        journal.mkdir()
        (journal / "week_001.md").write_text(_sample_journal(1), encoding="utf-8")
        (journal / "README.md").write_text("readme content", encoding="utf-8")
        (journal / "TEMPLATE.md").write_text("template content", encoding="utf-8")
        memory_file = tmp_path / "memory.json"
        result = seed_memory(journal_dir=journal, memory_file=memory_file)
        assert len(result["concepts"]) == 3  # only week_001 contributed

    def test_merge_preserves_existing_state(self, tmp_path: Path) -> None:
        """merge=True keeps battle history when re-seeding."""
        journal = tmp_path / "weeks"
        journal.mkdir()
        (journal / "week_001.md").write_text(_sample_journal(1), encoding="utf-8")
        memory_file = tmp_path / "memory.json"

        # First seed
        seed_memory(journal_dir=journal, memory_file=memory_file)

        # Mutate a concept as if the learner had fought it
        memory = load_memory(memory_file)
        cid = next(iter(memory["concepts"]))
        memory["concepts"][cid]["stability"] = 4.2
        memory["concepts"][cid]["times_fought"] = 5
        memory["concepts"][cid]["last_seen"] = "2026-07-01"
        save_memory(memory, memory_file)

        # Re-seed with merge=True (the default) — state preserved.
        seed_memory(journal_dir=journal, memory_file=memory_file)
        memory = load_memory(memory_file)
        assert memory["concepts"][cid]["stability"] == 4.2
        assert memory["concepts"][cid]["times_fought"] == 5
        assert memory["concepts"][cid]["last_seen"] == "2026-07-01"

    def test_fresh_resets_memory(self, tmp_path: Path) -> None:
        """merge=False wipes battle history."""
        journal = tmp_path / "weeks"
        journal.mkdir()
        (journal / "week_001.md").write_text(_sample_journal(1), encoding="utf-8")
        memory_file = tmp_path / "memory.json"

        seed_memory(journal_dir=journal, memory_file=memory_file)
        memory = load_memory(memory_file)
        cid = next(iter(memory["concepts"]))
        memory["concepts"][cid]["stability"] = 9.9
        save_memory(memory, memory_file)

        seed_memory(
            journal_dir=journal,
            memory_file=memory_file,
            merge=False,
        )
        memory = load_memory(memory_file)
        # Stability reset to SM-2 default.
        assert memory["concepts"][cid]["stability"] == 1.0

    def test_reports_added_count_via_dunder_key(self, tmp_path: Path) -> None:
        """The return value includes `_added_this_run` for the CLI to print."""
        journal = tmp_path / "weeks"
        journal.mkdir()
        (journal / "week_001.md").write_text(_sample_journal(1), encoding="utf-8")
        memory_file = tmp_path / "memory.json"

        result = seed_memory(journal_dir=journal, memory_file=memory_file)
        assert result["_added_this_run"] == 3

    def test_idempotent_on_second_seed(self, tmp_path: Path) -> None:
        """Second seed of the same journals adds 0 concepts."""
        journal = tmp_path / "weeks"
        journal.mkdir()
        (journal / "week_001.md").write_text(_sample_journal(1), encoding="utf-8")
        memory_file = tmp_path / "memory.json"

        seed_memory(journal_dir=journal, memory_file=memory_file)
        result = seed_memory(journal_dir=journal, memory_file=memory_file)
        assert result["_added_this_run"] == 0


# ===========================================================================
# stats()
# ===========================================================================

class TestStats:
    def test_empty_memory_counts(self) -> None:
        memory = _defaults()
        counts = stats(memory)
        # All zero except total = 0.
        assert counts["total"] == 0
        for tier in ("FRESH", "SETTLING", "WANING", "FADING", "LOST", "UNSEEN"):
            assert counts[tier] == 0

    def test_unseen_concepts_count_as_unseen(self) -> None:
        """Concepts never fought (last_seen=None) go in the UNSEEN bucket."""
        memory = _defaults()
        memory["concepts"]["w001-title-foo"] = _new_concept_row(
            {"id": "w001-title-foo", "name": "Foo", "kind": "title", "week": 1}
        )
        counts = stats(memory)
        assert counts["UNSEEN"] == 1
        assert counts["total"] == 1

    def test_seen_concepts_bucket_by_tier(self) -> None:
        """Concepts with last_seen set are bucketed by their current retention tier."""
        memory = _defaults()
        today = dt.date.today()
        memory["concepts"]["w001-title-fresh"] = _new_concept_row(
            {"id": "w001-title-fresh", "name": "Fresh", "kind": "title", "week": 1}
        )
        memory["concepts"]["w001-title-fresh"]["last_seen"] = today.isoformat()
        # All FRESH because just seen today.
        counts = stats(memory)
        assert counts["FRESH"] == 1
        assert counts["UNSEEN"] == 0

    def test_total_equals_sum_of_tiers(self) -> None:
        """Total always equals the sum across all tier buckets."""
        memory = _defaults()
        memory["concepts"]["a"] = _new_concept_row(
            {"id": "a", "name": "a", "kind": "title", "week": 1}
        )
        memory["concepts"]["b"] = _new_concept_row(
            {"id": "b", "name": "b", "kind": "focus", "week": 1}
        )
        memory["concepts"]["b"]["last_seen"] = "2020-01-01"  # long-ago -> likely LOST
        counts = stats(memory)
        assert counts["total"] == sum(
            counts[t] for t in ("FRESH", "SETTLING", "WANING", "FADING", "LOST", "UNSEEN")
        )
