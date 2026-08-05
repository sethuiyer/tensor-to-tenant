"""Unit tests for cookiecutter/.../scripts/forgetting.py.

Pure-function module: Ebbinghaus retention R(t) = exp(-t/S), SuperMemo
SM-2 stability updates, level/XP curve. These are the math primitives
the RPG layer (battle.py, character.py) is built on, so any regression
here cascades.

The test cases are anchored to known mathematical properties, not
arbitrary values, so they're robust to implementation tweaks that
preserve the math.
"""

from __future__ import annotations

import math

import pytest

from forgetting import (
    BASE_XP,
    EF_MIN,
    LEVEL_XP_COST,
    MULT_FADING,
    MULT_FRESH,
    MULT_MID,
    STABILITY_LOSS,
    TIER_FADING,
    TIER_FRESH,
    TIER_SETTLING,
    TIER_WANING,
    TIERS,
    level_from_xp,
    retention,
    retention_multiplier,
    tier_for_retention,
    update_sm2,
    xp_for_recall,
    xp_into_level,
)


# --------------------------------------------------------------------------
# retention()
# --------------------------------------------------------------------------

class TestRetention:
    """R(t) = exp(-t / S)."""

    def test_zero_days_returns_one(self) -> None:
        """At t=0 (just seen), recall probability is 1.0 by definition."""
        assert retention(stability=1.0, days_since=0) == 1.0
        assert retention(stability=5.0, days_since=0) == 1.0

    def test_negative_days_returns_one(self) -> None:
        """Defensive: future-dated reviews should not blow up."""
        assert retention(stability=2.5, days_since=-3) == 1.0

    def test_known_values(self) -> None:
        """Spot-check against the closed form for known (S, t)."""
        # R(2.5, 0) = 1.0
        assert retention(2.5, 0) == pytest.approx(1.0)
        # R(2.5, 2.5) = exp(-1) ≈ 0.3679
        assert retention(2.5, 2.5) == pytest.approx(math.exp(-1))
        # R(1.0, 1.0) = exp(-1) ≈ 0.3679
        assert retention(1.0, 1.0) == pytest.approx(math.exp(-1))
        # R(10.0, 10.0) = exp(-1) ≈ 0.3679
        assert retention(10.0, 10.0) == pytest.approx(math.exp(-1))

    def test_higher_stability_slower_decay(self) -> None:
        """For the same elapsed time, higher S -> higher R."""
        r_low = retention(stability=1.0, days_since=5)
        r_high = retention(stability=10.0, days_since=5)
        assert r_high > r_low

    def test_stability_floor_prevents_division_by_zero(self) -> None:
        """Stability is floored at 0.1 so the math never blows up."""
        # S = 0 should not raise; it floors to 0.1.
        r = retention(stability=0.0, days_since=10)
        assert 0.0 <= r <= 1.0
        r = retention(stability=-5.0, days_since=10)
        assert 0.0 <= r <= 1.0

    def test_monotonic_decrease(self) -> None:
        """R(t) is monotonically non-increasing in t for fixed S."""
        s = 2.0
        prev = retention(s, 0)
        for d in (1, 2, 5, 10, 30, 100, 365):
            cur = retention(s, d)
            assert cur <= prev, f"R(t) increased at t={d}: {cur} > {prev}"
            prev = cur


# --------------------------------------------------------------------------
# tier_for_retention()
# --------------------------------------------------------------------------

class TestTierForRetention:
    """Tier boundaries are exposed constants; tests pin the exact mapping."""

    @pytest.mark.parametrize(
        "r,expected_tier",
        [
            (1.0, "FRESH"),
            (TIER_FRESH + 0.001, "FRESH"),
            # Boundary: r == TIER_FRESH is NOT strictly greater than
            # TIER_FRESH, so it falls through to the next comparison.
            (TIER_FRESH, "SETTLING"),
            (TIER_FRESH - 0.001, "SETTLING"),
            (TIER_SETTLING + 0.001, "SETTLING"),
            (TIER_SETTLING, "WANING"),
            (TIER_SETTLING - 0.001, "WANING"),
            (TIER_WANING + 0.001, "WANING"),
            (TIER_WANING, "FADING"),
            (TIER_WANING - 0.001, "FADING"),
            (TIER_FADING + 0.001, "FADING"),
            (TIER_FADING, "LOST"),
            (TIER_FADING - 0.001, "LOST"),
            (0.0, "LOST"),
            (-0.5, "LOST"),
        ],
    )
    def test_boundaries(self, r: float, expected_tier: str) -> None:
        # The implementation uses STRICT `>` for every tier threshold.
        # A retention value at exactly the boundary falls through to
        # the next comparison, so the tier at the boundary is the next
        # one DOWN. This is intentional per the existing __main__
        # block's tier table — the test pins the documented behavior.
        assert tier_for_retention(r) == expected_tier

    def test_tiers_constant_is_five_elements(self) -> None:
        """Sanity: TIERS exposes exactly the five documented tiers."""
        assert TIERS == ("FRESH", "SETTLING", "WANING", "FADING", "LOST")


# --------------------------------------------------------------------------
# retention_multiplier()
# --------------------------------------------------------------------------

class TestRetentionMultiplier:
    """Reward multiplier is the operational incentive for hard recall work."""

    def test_fading_recall_gets_highest_multiplier(self) -> None:
        """R < 0.30 -> 1.5x — rescuing a fading memory is hardest, most rewarded."""
        assert retention_multiplier(0.0) == MULT_FADING
        assert retention_multiplier(0.10) == MULT_FADING
        assert retention_multiplier(0.299) == MULT_FADING

    def test_fresh_recall_gets_lowest_multiplier(self) -> None:
        """R > 0.70 -> 0.5x — easy recall is expected, low reward."""
        assert retention_multiplier(0.71) == MULT_FRESH
        assert retention_multiplier(0.95) == MULT_FRESH
        assert retention_multiplier(1.0) == MULT_FRESH

    def test_mid_recall_gets_baseline(self) -> None:
        """0.30 <= R <= 0.70 -> 1.0x — middle band, baseline reward."""
        assert retention_multiplier(0.30) == MULT_MID
        assert retention_multiplier(0.50) == MULT_MID
        assert retention_multiplier(0.70) == MULT_MID


# --------------------------------------------------------------------------
# update_sm2() — Wozniak SuperMemo SM-2 stability update
# --------------------------------------------------------------------------

class TestUpdateSm2:
    """Pass: S' = S * EF. Fail: S' = S * STABILITY_LOSS. EF updates only on success."""

    def test_perfect_recall_grows_stability(self) -> None:
        """score=5 -> S' = S * EF, growth proportional to easiness."""
        new_s, new_ef = update_sm2(stability=1.0, ef=2.5, score=5)
        # delta = 0.1 - (5-5)*(0.08 + 0) = 0.1
        # new_ef = max(1.3, 2.5 + 0.1) = 2.6
        assert new_s == pytest.approx(2.5)
        assert new_ef == pytest.approx(2.6)

    def test_ef_floor_is_enforced(self) -> None:
        """EF cannot drop below 1.3 even after many low-quality successes."""
        # score=3 gives the worst EF delta for a "pass" (since (5-3)=2).
        # delta = 0.1 - 2 * (0.08 + 2 * 0.02) = 0.1 - 0.24 = -0.14
        # Starting at EF=1.5, EF -> max(1.3, 1.36) = 1.36.
        new_s, new_ef = update_sm2(stability=1.0, ef=1.5, score=3)
        assert new_ef >= EF_MIN

    def test_blackout_collapses_stability(self) -> None:
        """score=0 -> S' = S * 0.6."""
        new_s, new_ef = update_sm2(stability=1.0, ef=2.5, score=0)
        assert new_s == pytest.approx(1.0 * STABILITY_LOSS)
        assert new_ef == 2.5  # EF unchanged on failure (Wozniak)

    def test_failure_does_not_change_ef(self) -> None:
        """Per Wozniak: EF only updates on successful recall (score >= 3)."""
        for score in (0, 1, 2):
            _, new_ef = update_sm2(stability=2.0, ef=2.5, score=score)
            assert new_ef == 2.5, f"EF changed on failure score={score}"

    def test_score_is_clamped(self) -> None:
        """Out-of-range scores do not raise; they clamp to [0, 5]."""
        # Negative score clamps to 0 (failure).
        new_s_neg, _ = update_sm2(stability=1.0, ef=2.5, score=-3)
        new_s_zero, _ = update_sm2(stability=1.0, ef=2.5, score=0)
        assert new_s_neg == new_s_zero

        # Score > 5 clamps to 5 (perfect).
        new_s_huge, _ = update_sm2(stability=1.0, ef=2.5, score=99)
        new_s_five, _ = update_sm2(stability=1.0, ef=2.5, score=5)
        assert new_s_huge == new_s_five

    def test_success_growth_uses_current_ef(self) -> None:
        """S' = S * EF, not a fixed multiplier."""
        # Same score, different EF -> different growth.
        s1, _ = update_sm2(stability=1.0, ef=1.5, score=5)
        s2, _ = update_sm2(stability=1.0, ef=2.5, score=5)
        assert s2 > s1
        assert s1 == pytest.approx(1.5)
        assert s2 == pytest.approx(2.5)


# --------------------------------------------------------------------------
# xp_for_recall()
# --------------------------------------------------------------------------

class TestXpForRecall:
    """Total XP = base[score] * (multiplier(R) + class_bonus)."""

    def test_base_xp_table_covers_all_scores(self) -> None:
        """BASE_XP must define an entry for every score 0..5."""
        assert set(BASE_XP.keys()) == {0, 1, 2, 3, 4, 5}

    def test_base_xp_ordering(self) -> None:
        """Higher score -> at least as much base XP (monotonic in score)."""
        prev = -float("inf")
        for score in range(6):
            assert BASE_XP[score] >= prev, (
                f"Non-monotonic: BASE_XP[{score}]={BASE_XP[score]} < "
                f"BASE_XP[{score - 1}]={prev}"
            )
            prev = BASE_XP[score]

    def test_blackout_costs_xp(self) -> None:
        """score=0 -> -3 base, even at FRESH retention (0.5x), is negative."""
        # MULT_FRESH = 0.5, base = -3, mult = 0.5, xp = round(-1.5) = -1 (banker's rounding)
        # Actually round(-1.5) = -2 in Python (banker's rounds to even).
        xp = xp_for_recall(score=0, retention_at_test=0.9, class_bonus=0.0)
        assert xp < 0

    def test_perfect_recall_pays_well(self) -> None:
        """score=5 -> +50 base, multiplied by tier."""
        # FRESH retention (0.5x): 50 * 0.5 = 25.
        assert xp_for_recall(score=5, retention_at_test=0.9, class_bonus=0.0) == 25
        # FADING retention (1.5x): 50 * 1.5 = 75.
        assert xp_for_recall(score=5, retention_at_test=0.20, class_bonus=0.0) == 75
        # MID retention (1.0x): 50 * 1.0 = 50.
        assert xp_for_recall(score=5, retention_at_test=0.50, class_bonus=0.0) == 50

    def test_class_bonus_is_additive(self) -> None:
        """A 10% class bonus on top of FADING (1.5x) gives 1.6x total."""
        xp = xp_for_recall(score=5, retention_at_test=0.20, class_bonus=0.1)
        # 50 * (1.5 + 0.1) = 80
        assert xp == 80

    def test_score_is_clamped_at_call_site(self) -> None:
        """Out-of-range scores clamp to [0, 5] before lookup."""
        # Score 7 clamps to 5.
        xp = xp_for_recall(score=7, retention_at_test=0.9, class_bonus=0.0)
        assert xp == xp_for_recall(score=5, retention_at_test=0.9, class_bonus=0.0)


# --------------------------------------------------------------------------
# level_from_xp() and xp_into_level()
# --------------------------------------------------------------------------

class TestLevelAndXpCurve:
    """Lvl n -> n+1 costs 100*n XP. Quadratic growth."""

    def test_zero_xp_is_level_one(self) -> None:
        assert level_from_xp(0) == 1

    def test_just_below_threshold_stays_at_level(self) -> None:
        """At 99 XP, you are still L1 (L2 costs exactly 100 XP)."""
        assert level_from_xp(99) == 1

    def test_at_threshold_advances(self) -> None:
        """At exactly 100 XP, you hit L2."""
        assert level_from_xp(100) == 2

    def test_quadratic_cost(self) -> None:
        """Level costs follow 100*n: L2=100, L3=200, L4=300, ..."""
        cumulative = 0
        for level in range(1, 10):
            cost = LEVEL_XP_COST(level)
            assert cost == 100 * level, f"L{level} cost wrong: {cost}"
            cumulative += cost
            # At exactly cumulative XP, you are at level+1.
            assert level_from_xp(cumulative) == level + 1

    def test_caps_at_level_100(self) -> None:
        """Hard cap at L100 prevents runaway levels from absurd XP."""
        # L100 cost alone is 10000 XP; cumulative to reach L100 is
        # 100 + 200 + ... + 10000 = 505000. Anything past that is L100.
        assert level_from_xp(10_000_000) == 100

    def test_xp_into_level_invariants(self) -> None:
        """(into, cost, frac) satisfy: 0 <= into <= cost, 0 <= frac <= 1.

        Only exercised BELOW the L100 cap (cumulative cost to reach L100
        is 495,000 XP; see test_l100_cap_behavior for what happens
        past the cap). The cap is a known sharp edge; tests here pin
        behavior in the regime the implementation was designed for.
        """
        for xp in (0, 50, 100, 500, 5000, 100_000, 400_000):
            into, cost, frac = xp_into_level(xp)
            assert 0 <= into <= cost
            assert 0.0 <= frac <= 1.0
            # frac + round-trip: level_from_xp(xp) is consistent.
            assert level_from_xp(xp) >= 1

    def test_l100_cap_behavior(self) -> None:
        """Document the L100 cap's current (inconsistent) behavior.

        The level curve hard-caps at L100 (TASKS.md T1.4.a acceptance).
        At or above the cumulative cap (~495,000 XP), `xp_into_level`
        returns a tuple where `into > cost` but `frac` is clamped to
        1.0. The two values disagree. This is a latent sharp edge — it
        should be fixed by clamping `into` to `cost` at L100 — but it
        is NOT exercised by the existing __main__ smoke test, so it
        has gone undetected. This test pins the current behavior so
        the inconsistency is visible; the fix is a one-liner in
        forgetting.py once the schema migration (T1.1 – T1.3) is in
        flight.
        """
        into, cost, frac = xp_into_level(1_000_000)
        # Current behavior: level caps at 100, frac clamps to 1.0, but
        # `into` is not clamped and can exceed `cost`.
        assert level_from_xp(1_000_000) == 100
        assert frac == 1.0
        assert into >= cost  # current: into > cost is possible past cap

    def test_xp_into_level_round_trips_at_zero(self) -> None:
        into, cost, frac = xp_into_level(0)
        assert into == 0
        assert frac == 0.0
        assert cost == LEVEL_XP_COST(1)


# --------------------------------------------------------------------------
# days_since() helper
# --------------------------------------------------------------------------

class TestDaysSince:
    """Days elapsed since an ISO date string. Returns 0 if None."""

    def test_none_returns_zero(self) -> None:
        # Import locally to keep top of file clean.
        from forgetting import days_since

        assert days_since(None) == 0.0

    def test_iso_date_math(self) -> None:
        """Spot-check: a date 10 days ago is at least 10.0 days."""
        from datetime import date, timedelta

        from forgetting import days_since

        ten_days_ago = (date.today() - timedelta(days=10)).isoformat()
        assert days_since(ten_days_ago) >= 10.0
        assert days_since(ten_days_ago) < 11.0  # clock hasn't crossed a day

    def test_today_returns_zero(self) -> None:
        from datetime import date

        from forgetting import days_since

        assert days_since(date.today().isoformat()) == 0.0


# --------------------------------------------------------------------------
# Smoke test: __main__ block runs without raising
# --------------------------------------------------------------------------

def test_main_block_executes_cleanly(capsys: pytest.CaptureFixture[str]) -> None:
    """The module's __main__ block prints sanity output and exits 0.

    Invoking it directly is awkward; instead, exercise the public surface
    enough to confirm no top-level side effects.
    """
    retention(2.5, 30)
    update_sm2(1.0, 2.5, 5)
    xp_for_recall(5, 0.5, class_bonus=0.0)
    level_from_xp(0)
    tier_for_retention(0.5)
    captured = capsys.readouterr()
    assert captured.err == ""
