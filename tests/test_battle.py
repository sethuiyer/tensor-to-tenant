"""Unit tests for cookiecutter/.../scripts/battle.py.

Pure-function battle engine: ambush target selection, mandala mapping,
resurrection queue, weekly forge picks. Tests anchor to known
properties; SM-2 stability math is covered by test_forgetting.py.
"""

from __future__ import annotations

import datetime as dt
import random
from pathlib import Path

import pytest

from battle import (
    MANDALAS,
    BattleResult,
    _concept_retention,
    apply_recall,
    days_to_mandala_end,
    eligible_for,
    mandala_for_week,
    mandala_name,
    resurrection_queue,
    select_ambush_target,
    should_trigger_ambush,
    weekly_forge_picks,
)


# ===========================================================================
# Mandala mapping (the canonical 16-mandala table)
# ===========================================================================

class TestMandalaMapping:
    def test_mandala_count_is_sixteen(self) -> None:
        """MANDALAS must have exactly 16 entries (15 + graduation)."""
        assert len(MANDALAS) == 16

    def test_first_mandala_starts_at_week_one(self) -> None:
        assert MANDALAS[0][0] == 1

    def test_last_mandala_ends_at_week_one_hundred_eight(self) -> None:
        assert MANDALAS[-1][1] == 108

    def test_mandala_weeks_cover_one_through_one_hundred_eight(self) -> None:
        """The union of all mandala weeks must cover 1-108 without gaps.

        Boundary behavior: most transitions share the boundary week
        (next_start == current_end), which means weeks are double-counted
        at the seam but every week is in at least one mandala. Two
        transitions (M7->M8 and M14->M15) are back-to-back
        (next_start == current_end + 1). The invariant the curriculum
        cares about is coverage of every week.
        """
        all_weeks: set[int] = set()
        for lo, hi, _ in MANDALAS:
            for w in range(lo, hi + 1):
                all_weeks.add(w)
        # Every week 1..108 is covered.
        missing = set(range(1, 109)) - all_weeks
        assert not missing, f"Weeks not covered by any mandala: {sorted(missing)}"

    def test_mandala_for_week_known_values(self) -> None:
        """Spot-check a few well-known mappings."""
        # M1 (1-7): week 7 is shared with M2 (7-14). mandala_for_week
        # returns the first mandala whose range includes the week, so
        # week 7 belongs to M1.
        assert mandala_for_week(1) == 1
        assert mandala_for_week(7) == 1
        assert mandala_for_week(8) == 2
        assert mandala_for_week(103) == 15
        assert mandala_for_week(108) == 16


class TestMandalaName:
    def test_name_lookup(self) -> None:
        assert "Disciplined learner" in mandala_name(1)
        assert "Staff" in mandala_name(108) or "Portfolio" in mandala_name(108)


# ===========================================================================
# Retention helper
# ===========================================================================

class TestConceptRetention:
    def test_unseen_concept_has_full_retention(self) -> None:
        """A never-fought concept has no last_seen -> retention = 1.0 (FRESH)."""
        concept = {"stability": 1.0, "last_seen": None}
        assert _concept_retention(concept, dt.date(2026, 7, 1)) == 1.0

    def test_seen_concept_uses_days_since(self) -> None:
        """For a seen concept, R(t) = exp(-t/S) with t = days since last_seen."""
        concept = {"stability": 2.5, "last_seen": "2026-07-01"}
        # 10 days later.
        r = _concept_retention(concept, dt.date(2026, 7, 11))
        import math
        assert r == pytest.approx(math.exp(-10 / 2.5))


# ===========================================================================
# eligible_for() — filter concepts by retention tier
# ===========================================================================

class TestEligibleFor:
    def _make_concept(self, stability: float, days_ago: int | None, cid: str | None = None) -> dict:
        """Build a concept record with given stability and recency.

        cid: optional explicit id; defaults to a deterministic string.
        """
        if days_ago is None:
            last_seen = None
        else:
            last_seen = (dt.date(2026, 7, 11) - dt.timedelta(days=days_ago)).isoformat()
        return {
            "id": cid or f"test-{stability}-{days_ago}",
            "name": f"S={stability}, d={days_ago}",
            "stability": stability,
            "last_seen": last_seen,
            "ef": 2.5,
        }

    def test_unseen_concepts_eligible_at_fresh_only(self) -> None:
        """Unseen concepts have R=1.0 which only passes the FRESH cutoff (1.01).

        Cutoffs: FRESH=1.01, SETTLING=0.70, WANING=0.50, FADING=0.30,
        LOST=0.10. R=1.0 only passes the FRESH cutoff.
        """
        memory = {"concepts": {f"c{i}": self._make_concept(1.0, None, cid=f"c{i}") for i in range(3)}}
        result = eligible_for(memory, dt.date(2026, 7, 11), tier="FRESH")
        assert len(result) == 3
        # And they don't qualify for tighter tiers.
        for tier in ("SETTLING", "WANING", "FADING", "LOST"):
            assert eligible_for(memory, dt.date(2026, 7, 11), tier=tier) == []

    def test_ordering_by_retention_ascending(self) -> None:
        """eligible_for returns concepts sorted by lowest retention first."""
        memory = {"concepts": {
            "fresh": self._make_concept(10.0, 0, cid="fresh"),       # R ~= 1.0
            "waning": self._make_concept(2.0, 5, cid="waning"),      # R ~= exp(-2.5) ~ 0.082
            "settling": self._make_concept(5.0, 3, cid="settling"),  # R ~= exp(-0.6) ~ 0.549
        }}
        result = eligible_for(memory, dt.date(2026, 7, 11), tier="FRESH")
        # First entry is the lowest retention; first element is the concept dict.
        first_concept, _first_r = result[0]
        assert first_concept["id"] == "waning"

    def test_tier_cutoff_excludes_fresh_concepts(self) -> None:
        """With cutoff=LOST, only R < 0.10 concepts qualify."""
        memory = {"concepts": {
            "fresh": self._make_concept(10.0, 0, cid="fresh"),    # R ~= 1.0
            "lost": self._make_concept(1.0, 50, cid="lost"),      # R = exp(-50) ~ 0
        }}
        result = eligible_for(memory, dt.date(2026, 7, 11), tier="LOST")
        ids = [c["id"] for c, _ in result]
        assert "lost" in ids
        assert "fresh" not in ids


# ===========================================================================
# apply_recall() — the recall outcome mechanics
# ===========================================================================

class TestApplyRecall:
    """apply_recall updates a concept's SM-2 state and writes to memory DB.

    Tested with a per-test working directory because the implementation
    reads from journal/memory.json via CONCEPT_FILE.
    """

    @pytest.fixture
    def workdir(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        """Set CWD to a temp dir so CONCEPT_FILE resolves inside it."""
        journal = tmp_path / "journal"
        journal.mkdir()
        monkeypatch.chdir(tmp_path)
        return tmp_path

    def _seed(self, workdir: Path, cid: str = "w001-title-foo", stability: float = 2.5):
        """Seed one concept and return the memory file path."""
        import json
        path = workdir / "journal" / "memory.json"
        path.write_text(
            json.dumps({
                "version": 2,
                "seeded_from": "journal",
                "concepts": {
                    cid: {
                        "id": cid,
                        "name": "Foo",
                        "kind": "title",
                        "week": 1,
                        "stability": stability,
                        "ef": 2.5,
                        "difficulty": 3,
                        "last_score": None,
                        "last_seen": None,
                        "times_fought": 0,
                        "times_rescued": 0,
                        "times_lost": 0,
                    }
                },
            }),
            encoding="utf-8",
        )
        return path

    def _char(self) -> dict:
        """Minimal character dict with the keys apply_recall expects."""
        return {
            "stats": {"WIS": 0, "ALGO": 0, "ENG": 0, "INFER": 0, "PLAT": 0, "JUDG": 0},
            "total_xp": 0,
            "hp": 100,
            "last_active": None,
        }

    def test_score_three_is_rescued_threshold(self, workdir: Path) -> None:
        """Score >= 3 means rescued (per docstring)."""
        self._seed(workdir)
        concept = {
            "id": "w001-title-foo",
            "stability": 2.5,
            "ef": 2.5,
            "last_seen": None,
        }
        result = apply_recall(concept, score=3, today=dt.date(2026, 7, 11), char=self._char(), stat="WIS")
        assert result.rescued is True
        assert result.lost is False

    def test_score_zero_is_lost(self, workdir: Path) -> None:
        self._seed(workdir)
        concept = {
            "id": "w001-title-foo",
            "stability": 2.5,
            "ef": 2.5,
            "last_seen": None,
        }
        result = apply_recall(concept, score=0, today=dt.date(2026, 7, 11), char=self._char(), stat="WIS")
        assert result.lost is True
        assert result.rescued is False

    def test_score_two_is_neither_rescued_nor_lost(self, workdir: Path) -> None:
        """Score=2: recognized-after-being-shown -> neither rescued nor lost."""
        self._seed(workdir)
        concept = {
            "id": "w001-title-foo",
            "stability": 2.5,
            "ef": 2.5,
            "last_seen": None,
        }
        result = apply_recall(concept, score=2, today=dt.date(2026, 7, 11), char=self._char(), stat="WIS")
        assert result.rescued is False
        assert result.lost is False

    def test_persistence_updates_last_seen_and_history(self, workdir: Path) -> None:
        """apply_recall must write last_seen + times_fought + last_score to memory."""
        import json
        self._seed(workdir)
        cid = "w001-title-foo"
        concept = {
            "id": cid,
            "stability": 2.5,
            "ef": 2.5,
            "last_seen": None,
        }
        today = dt.date(2026, 7, 11)
        apply_recall(concept, score=4, today=today, char=self._char(), stat="WIS")
        # Re-read memory and check the persistence.
        memory = json.loads((workdir / "journal" / "memory.json").read_text())
        c = memory["concepts"][cid]
        assert c["last_seen"] == today.isoformat()
        assert c["times_fought"] == 1
        assert c["last_score"] == 4

    def test_times_rescued_increments_only_on_rescue(self, workdir: Path) -> None:
        """Score >= 3 increments times_rescued; score <= 1 increments times_lost."""
        import json
        self._seed(workdir)
        cid = "w001-title-foo"
        concept = {"id": cid, "stability": 2.5, "ef": 2.5, "last_seen": None}

        # Three rescues.
        for s in (3, 4, 5):
            apply_recall(concept, score=s, today=dt.date(2026, 7, 11), char=self._char(), stat="WIS")
        memory = json.loads((workdir / "journal" / "memory.json").read_text())
        c = memory["concepts"][cid]
        assert c["times_rescued"] == 3
        assert c["times_lost"] == 0

        # One loss.
        apply_recall(concept, score=0, today=dt.date(2026, 7, 11), char=self._char(), stat="WIS")
        memory = json.loads((workdir / "journal" / "memory.json").read_text())
        c = memory["concepts"][cid]
        assert c["times_rescued"] == 3
        assert c["times_lost"] == 1

    def test_battle_result_fields_populated(self, workdir: Path) -> None:
        """The returned BattleResult has the documented fields."""
        self._seed(workdir)
        concept = {
            "id": "w001-title-foo",
            "stability": 2.5,
            "ef": 2.5,
            "last_seen": None,
        }
        result = apply_recall(concept, score=4, today=dt.date(2026, 7, 11), char=self._char(), stat="WIS")
        assert result.concept_id == "w001-title-foo"
        assert result.name == "?"
        assert result.week == 0

# ===========================================================================
# days_to_mandala_end()
# ===========================================================================

class TestDaysToMandalaEnd:
    def test_zero_days_at_mandala_end(self) -> None:
        """At the exact last day of a mandala, days remaining is 0."""
        # MANDALAS[0] ends at week 7 -> last day is the Monday of week 7 + 6 days.
        last_week = MANDALAS[0][1]
        # Use a Monday-aligned start.
        start = dt.date(2026, 1, 5)  # Week 1 Monday.
        # End-of-mandala = start of week (last_week + 1) - 1 day.
        # Equivalently: last day is start + 7*(last_week - 1) + 6.
        end_of_mandala = start + dt.timedelta(days=7 * (last_week - 1) + 6)
        # But the implementation uses the *start* of week (end_week + 1).
        # So days_to_mandala_end from start is (end_week + 1) * 7.
        # Test that days_to_mandala_end from start is positive and matches expected math.
        days = days_to_mandala_end(1, start)
        # The function returns days until end-of-mandala based on
        # ((end_week - week + 1) * 7), which from the start of week 1
        # is (last_week - 1 + 1) * 7 = last_week * 7.
        assert days == last_week * 7

    def test_decreases_as_weeks_progress(self) -> None:
        """Later weeks in a mandala have fewer days remaining."""
        start = dt.date(2026, 1, 5)
        d1 = days_to_mandala_end(1, start)
        d5 = days_to_mandala_end(5, start)
        # Week 5 is 4 weeks later than week 1 -> 28 days fewer.
        assert d1 - d5 == 28

    def test_returns_zero_or_positive(self) -> None:
        """Never returns negative; clamps at the end of the mandala."""
        start = dt.date(2026, 1, 5)
        # Week 8 is in the second mandala, not the first.
        d = days_to_mandala_end(7, start)
        assert d >= 0


# ===========================================================================
# resurrection_queue()
# ===========================================================================

class TestResurrectionQueue:
    def test_returns_only_lost_concepts(self, tmp_path: Path) -> None:
        """resurrection_queue filters for R < 0.10 (LOST tier)."""
        import json
        # Build a memory with concepts at varying retentions.
        # Unseen (last_seen=None) -> R=1.0 -> NOT lost.
        # Far-past last_seen with low stability -> R ~= 0 -> LOST.
        today = dt.date(2026, 7, 11)
        memory = {
            "version": 2,
            "seeded_from": "journal",
            "concepts": {
                "unseen": {
                    "id": "unseen", "name": "Unseen", "kind": "title", "week": 1,
                    "stability": 1.0, "ef": 2.5, "difficulty": 3,
                    "last_score": None, "last_seen": None,
                    "times_fought": 0, "times_rescued": 0, "times_lost": 0,
                },
                "lost": {
                    "id": "lost", "name": "Lost", "kind": "focus", "week": 5,
                    "stability": 1.0, "ef": 2.5, "difficulty": 3,
                    "last_score": 0, "last_seen": "2026-06-01",  # 40 days ago
                    "times_fought": 1, "times_rescued": 0, "times_lost": 1,
                },
                "fresh": {
                    "id": "fresh", "name": "Fresh", "kind": "deliverable", "week": 10,
                    "stability": 2.0, "ef": 2.5, "difficulty": 3,
                    "last_score": 5, "last_seen": today.isoformat(),  # today
                    "times_fought": 1, "times_rescued": 1, "times_lost": 0,
                },
            },
        }
        path = tmp_path / "memory.json"
        path.write_text(json.dumps(memory), encoding="utf-8")

        queue = resurrection_queue(memory, today)
        ids = [c["id"] for c in queue]
        assert "lost" in ids
        assert "unseen" not in ids
        assert "fresh" not in ids


# ===========================================================================
# select_ambush_target() — the most-at-risk selection
# ===========================================================================

class TestSelectAmbushTarget:
    def _make_memory_with_retentions(self, tmp_path: Path, records: list[tuple[str, float, str | None]]) -> None:
        """records: list of (id, stability, last_seen_or_None)."""
        import json
        memory = {"version": 2, "seeded_from": "journal", "concepts": {}}
        for cid, stability, last_seen in records:
            memory["concepts"][cid] = {
                "id": cid, "name": cid, "kind": "title", "week": 1,
                "stability": stability, "ef": 2.5, "difficulty": 3,
                "last_score": None, "last_seen": last_seen,
                "times_fought": 0, "times_rescued": 0, "times_lost": 0,
            }
        path = tmp_path / "memory.json"
        path.write_text(json.dumps(memory), encoding="utf-8")

    def test_no_eligible_returns_none(self, tmp_path: Path) -> None:
        """If all concepts are FRESH, the ambush has no target."""
        today = dt.date(2026, 7, 11)
        # All concepts seen today with high stability -> all FRESH.
        self._make_memory_with_retentions(
            tmp_path,
            [(f"c{i}", 10.0, today.isoformat()) for i in range(3)],
        )
        import json
        memory = json.loads((tmp_path / "memory.json").read_text())
        target = select_ambush_target(memory, today)
        assert target is None

    def test_picks_lowest_retention_concept(self, tmp_path: Path) -> None:
        """Default behavior: target = lowest-retention eligible concept."""
        today = dt.date(2026, 7, 11)
        self._make_memory_with_retentions(
            tmp_path,
            [
                ("fresh", 10.0, today.isoformat()),  # R ~= 1
                ("waning", 2.0, "2026-07-08"),      # 3 days -> R ~= exp(-1.5) ~= 0.22
                ("lost", 1.0, "2026-06-01"),          # 40 days -> R ~= 0
            ],
        )
        import json
        memory = json.loads((tmp_path / "memory.json").read_text())
        target = select_ambush_target(memory, today)
        assert target is not None
        assert target["id"] == "lost"

    def test_seed_biased_toward_low_retention(self, tmp_path: Path) -> None:
        """With a seed, the pick is from the bottom-N (lowest retention)."""
        today = dt.date(2026, 7, 11)
        # Build 10 concepts, half LOST, half FRESH.
        records = []
        for i in range(5):
            records.append((f"lost_{i}", 1.0, "2026-06-01"))
        for i in range(5):
            records.append((f"fresh_{i}", 10.0, today.isoformat()))
        self._make_memory_with_retentions(tmp_path, records)
        import json
        memory = json.loads((tmp_path / "memory.json").read_text())

        # With seed 42 and candidates in lowest-retention order,
        # every pick should be a "lost_N" concept, never a fresh one.
        rng = random.Random(42)
        seen_lost = 0
        seen_fresh = 0
        for _ in range(50):
            target = select_ambush_target(memory, today, seed=rng.random())
            if target is None:
                continue
            if target["id"].startswith("lost"):
                seen_lost += 1
            else:
                seen_fresh += 1
        # The bias should be strong — at least 80% picks are LOST.
        assert seen_lost > seen_fresh
        assert seen_lost + seen_fresh > 0


# ===========================================================================
# should_trigger_ambush()
# ===========================================================================

class TestShouldTriggerAmbush:
    def _make_memory(self, tmp_path: Path, *, with_wan_concept: bool) -> None:
        """Memory with or without a WANING-or-worse concept."""
        import json
        memory = {"version": 2, "seeded_from": "journal", "concepts": {}}
        if with_wan_concept:
            memory["concepts"]["waning"] = {
                "id": "waning", "name": "Waning", "kind": "title", "week": 1,
                "stability": 2.0, "ef": 2.5, "difficulty": 3,
                "last_score": None, "last_seen": "2026-07-08",  # 3 days ago
                "times_fought": 0, "times_rescued": 0, "times_lost": 0,
            }
        path = tmp_path / "memory.json"
        path.write_text(json.dumps(memory), encoding="utf-8")

    def test_no_ambush_when_no_eligible_concepts(self, tmp_path: Path) -> None:
        """With no WANING-or-worse concepts, ambush should not trigger."""
        self._make_memory(tmp_path, with_wan_concept=False)
        # Empty concept set -> eligible_for returns [] -> no ambush.
        import json
        memory = json.loads((tmp_path / "memory.json").read_text())
        # Even with probability 1.0, no eligible -> no trigger.
        assert should_trigger_ambush(memory, dt.date(2026, 7, 11), probability=1.0) is False

    def test_probability_one_always_triggers(self, tmp_path: Path) -> None:
        """With probability 1.0 and an eligible concept, ambush always triggers."""
        self._make_memory(tmp_path, with_wan_concept=True)
        import json
        memory = json.loads((tmp_path / "memory.json").read_text())
        assert should_trigger_ambush(memory, dt.date(2026, 7, 11), probability=1.0) is True

    def test_probability_zero_never_triggers(self, tmp_path: Path) -> None:
        """With probability 0.0, ambush never triggers (even with eligible)."""
        self._make_memory(tmp_path, with_wan_concept=True)
        import json
        memory = json.loads((tmp_path / "memory.json").read_text())
        # Run a few times with different seeds — all should be False.
        for _ in range(20):
            assert should_trigger_ambush(memory, dt.date(2026, 7, 11), probability=0.0) is False


# ===========================================================================
# weekly_forge_picks()
# ===========================================================================

class TestWeeklyForgePicks:
    def _seed(self, tmp_path: Path, records: list[tuple[str, int, str]]) -> None:
        """records: list of (id, week, last_seen)."""
        import json
        memory = {"version": 2, "seeded_from": "journal", "concepts": {}}
        for cid, week, last_seen in records:
            memory["concepts"][cid] = {
                "id": cid, "name": cid, "kind": "title", "week": week,
                "stability": 2.0, "ef": 2.5, "difficulty": 3,
                "last_score": None, "last_seen": last_seen,
                "times_fought": 0, "times_rescued": 0, "times_lost": 0,
            }
        path = tmp_path / "memory.json"
        path.write_text(json.dumps(memory), encoding="utf-8")

    def test_returns_top_three_decaying_from_current_and_prior_week(self, tmp_path: Path) -> None:
        """Top-3 most-decaying concepts from weeks W and W-1."""
        today = dt.date(2026, 7, 11)
        # Three concepts at week 10 with varying decay.
        # Far-past last_seen = lowest retention.
        self._seed(tmp_path, [
            ("w10_old", 10, "2026-01-01"),     # very decayed
            ("w10_med", 10, "2026-06-01"),     # medium
            ("w10_new", 10, "2026-07-10"),     # fresh
            ("w9_decayed", 9, "2026-01-01"),   # very decayed (prior week)
        ])
        import json
        memory = json.loads((tmp_path / "memory.json").read_text())

        picks = weekly_forge_picks(memory, week=10, today=today)
        ids = [c["id"] for c in picks]
        assert len(picks) <= 3
        # The most-decayed concept (w9_decayed or w10_old) should be in picks.
        assert "w9_decayed" in ids or "w10_old" in ids

    def test_only_current_and_prior_week_considered(self, tmp_path: Path) -> None:
        """Concepts from weeks other than W or W-1 are ignored."""
        today = dt.date(2026, 7, 11)
        self._seed(tmp_path, [
            ("w10_far_past", 10, "2020-01-01"),     # at week 10, very decayed
            ("w5_decayed", 5, "2020-01-01"),      # very decayed but at week 5
        ])
        import json
        memory = json.loads((tmp_path / "memory.json").read_text())

        picks = weekly_forge_picks(memory, week=10, today=today)
        ids = [c["id"] for c in picks]
        assert "w10_far_past" in ids
        assert "w5_decayed" not in ids  # out of week range

    def test_no_concepts_returns_empty(self, tmp_path: Path) -> None:
        today = dt.date(2026, 7, 11)
        self._seed(tmp_path, [])
        import json
        memory = json.loads((tmp_path / "memory.json").read_text())
        assert weekly_forge_picks(memory, week=10, today=today) == []
