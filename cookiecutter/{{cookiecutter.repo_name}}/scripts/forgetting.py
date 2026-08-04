"""Forgetting curve math -- Ebbinghaus retention + SuperMemo SM-2 stability.

Pure functions, no I/O. The rest of the RPG layer is built on top of these
primitives so the math is testable in isolation.

References
----------
- Ebbinghaus, H. (1885/1913). Memory: A Contribution to Experimental Psychology.
- Wozniak, P. A. (1990). SuperMemo SM-2 algorithm.
- Ebbinghaus forgetting curve parametrized: R(t) = exp(-t / S), where S is a
  per-concept stability that grows with successful recall.
"""

from __future__ import annotations

import math
from typing import Final


# ---- Retention tier thresholds (visible state names) -----------------------

TIER_FRESH: Final[float] = 0.70     # > 0.70   FRESH
TIER_SETTLING: Final[float] = 0.50  # 0.50..0.70 SETTLING
TIER_WANING: Final[float] = 0.30    # 0.30..0.50 WANING
TIER_FADING: Final[float] = 0.10    # 0.10..0.30 FADING
                                  # < 0.10   LOST

TIERS: Final[tuple[str, ...]] = ("FRESH", "SETTLING", "WANING", "FADING", "LOST")


# ---- XP multipliers by recall context --------------------------------------

# Rescuing a fading memory is the hardest, most rewarding work.
MULT_FADING: Final[float] = 1.5
# Expected recall on a fresh concept is the baseline.
MULT_MID: Final[float] = 1.0
# Easy recall is small XP -- expected behavior.
MULT_FRESH: Final[float] = 0.5


# ---- Base XP by self-rated recall score (SM-2 0..5 scale) ------------------

BASE_XP: Final[dict[int, int]] = {
    0: -3,   # total blackout
    1: 0,    # incorrect, recognized answer
    2: 5,    # incorrect, easy to remember once shown
    3: 15,   # correct with hesitation
    4: 25,   # correct after thought
    5: 50,   # perfect recall
}


# ---- SM-2 algorithm constants ----------------------------------------------

STABILITY_LOSS: Final[float] = 0.6  # failure collapses stability
EF_MIN: Final[float] = 1.3         # Wozniak's floor on easiness factor


# ---- Level curve ------------------------------------------------------------

# Level n -> n+1 costs 100*n XP. Quadratic growth.
LEVEL_XP_COST = lambda level: 100 * level


def retention(stability: float, days_since: float) -> float:
    """Ebbinghaus retention R(t) = exp(-t / S).

    Returns the probability of recall given stability S and days elapsed.
    Floored stability at 0.1 so the math never blows up.
    """
    if days_since <= 0:
        return 1.0
    safe = max(stability, 0.1)
    return math.exp(-days_since / safe)


def tier_for_retention(r: float) -> str:
    """Map a retention probability to its visible tier name."""
    if r > TIER_FRESH:
        return "FRESH"
    if r > TIER_SETTLING:
        return "SETTLING"
    if r > TIER_WANING:
        return "WANING"
    if r > TIER_FADING:
        return "FADING"
    return "LOST"


def tier_emoji(r: float) -> str:
    """Glyph for the retention tier (safe ASCII)."""
    tier = tier_for_retention(r)
    return {
        "FRESH":    " ",
        "SETTLING": ".",
        "WANING":   ":",
        "FADING":   "*",
        "LOST":     "X",
    }.get(tier, " ")


def retention_multiplier(r: float) -> float:
    """Reward multiplier based on how close to forgetting the concept was."""
    if r < 0.30:
        return MULT_FADING
    if r > 0.70:
        return MULT_FRESH
    return MULT_MID


def xp_for_recall(score: int, retention_at_test: float,
                  class_bonus: float = 0.0) -> int:
    """Total XP awarded for a recall attempt.

    score: self-rated 0..5 (SM-2 quality)
    retention_at_test: R(t) the moment the battle started
    class_bonus: additive bonus on top of multiplier (e.g. 0.05 for class)
    """
    score = max(0, min(5, score))
    base = BASE_XP[score]
    mult = retention_multiplier(retention_at_test) + class_bonus
    return round(base * mult)


def update_sm2(stability: float, ef: float, score: int
               ) -> tuple[float, float]:
    """Wozniak SM-2 update -- returns (new_stability, new_ef).

    score >= 3 grows stability by the easiness factor; failures collapse
    stability by STABILITY_LOSS. EF only updates on success (Wozniak).
    """
    score = max(0, min(5, score))
    if score < 3:
        new_stability = stability * STABILITY_LOSS
        new_ef = ef
    else:
        new_stability = stability * ef
        delta = 0.1 - (5 - score) * (0.08 + (5 - score) * 0.02)
        new_ef = max(EF_MIN, ef + delta)
    return new_stability, new_ef


def level_from_xp(total_xp: int) -> int:
    """Inverse: given total XP, what level are you?

    Lvl 1 at 0 XP. Each level n costs 100*n XP beyond the prior.
    Hard caps at L100 to avoid runaway levels.
    """
    level = 1
    cumulative = 0
    while level < 100:
        cost = LEVEL_XP_COST(level)
        if cumulative + cost > total_xp:
            break
        cumulative += cost
        level += 1
    return level


def xp_into_level(total_xp: int) -> tuple[int, int, float]:
    """Return (xp_into_current, xp_required, fraction).

    Fraction is 0.0..1.0 of progress within the current level.
    """
    level = level_from_xp(total_xp)
    cumulative = sum(LEVEL_XP_COST(n) for n in range(1, level))
    cost = LEVEL_XP_COST(level)
    into = max(0, total_xp - cumulative)
    frac = (into / cost) if cost else 0.0
    return into, cost, min(1.0, frac)


def days_since(iso_date: str | None) -> float:
    """Days elapsed since an ISO date string. Returns 0 if None."""
    if not iso_date:
        return 0.0
    import datetime as dt
    return (dt.date.today() - dt.date.fromisoformat(iso_date)).days


if __name__ == "__main__":
    # Sanity: a concept with stability 2.5 fades from 1.0 toward 0.0 over 30 days.
    print("Sanity: stability=2.5 over 30 days")
    for d in (0, 1, 3, 7, 14, 21, 30):
        r = retention(2.5, d)
        print(f"  day {d:>3}  R={r:.3f}  tier={tier_for_retention(r)}")

    print("\nSM-2 update on score=5, starting I=1.0 EF=2.5")
    print(f"  -> {update_sm2(1.0, 2.5, 5)}")

    print("\nSM-2 update on score=0, starting I=1.0 EF=2.5")
    print(f"  -> {update_sm2(1.0, 2.5, 0)}")

    print("\nLevel curve preview (XP -> Level)")
    for xp in (0, 100, 300, 600, 1000, 3000, 6000, 10000, 16000, 21000):
        lvl = level_from_xp(xp)
        into, cost, frac = xp_into_level(xp)
        print(f"  XP {xp:>5} -> L{lvl:>3}  ({into:>4}/{cost:<4} {frac*100:>5.1f}%)")
