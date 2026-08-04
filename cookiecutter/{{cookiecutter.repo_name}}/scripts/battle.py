"""Battle engine -- ambushes, drills, mandala barriers.

Builds on forgetting.py for the math and concept_seed.py for the memory DB.
All persistence is in journal/memory.json and journal/character.json; neither
has any other write surface.
"""

from __future__ import annotations

import datetime as dt
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from forgetting import (
    TIER_FADING, TIER_FRESH, TIER_SETTLING, TIER_WANING,
    retention, retention_multiplier, tier_for_retention, update_sm2,
    xp_for_recall,
)
from concept_seed import (
    MEMORY_FILE as CONCEPT_FILE, load_memory, save_memory,
)


# --------------------------------------------------------------------------
# Mandala mapping -- 15 full 48-day mandalas + 1 graduation.
# Source: MANDALA.md and README.md phase structure.
# --------------------------------------------------------------------------
MANDALAS: list[tuple[int, int, str]] = [
    (1,   7,  "Disciplined learner"),
    (7,   14, "Linear-algebra thinker"),
    (14,  21, "Numerical programmer"),
    (21,  28, "Statistical reasoner"),
    (28,  35, "Retrieval + experimentation builder"),
    (35,  42, "Reliability-minded engineer"),
    (42,  48, "Distributed-systems implementer"),
    (49,  55, "System designer"),
    (55,  62, "ML systems practitioner"),
    (62,  69, "Experimentation engineer"),
    (69,  76, "LLM training + retrieval engineer"),
    (76,  83, "RAG + agent engineer"),
    (83,  90, "Inference performance engineer"),
    (90,  96, "Serving + routing engineer"),
    (97,  103, "Multi-tenant AI platform engineer"),
    (103, 108, "Portfolio-backed Staff candidate"),
]


def mandala_for_week(week: int) -> int:
    for i, (lo, hi, _name) in enumerate(MANDALAS, start=1):
        if lo <= week <= hi:
            return i
    if week >= 103:
        return 16
    return 1


def mandala_name(week: int) -> str:
    idx = mandala_for_week(week) - 1
    if 0 <= idx < len(MANDALAS):
        return MANDALAS[idx][2]
    return "Apprentice"


def days_to_mandala_end(week: int, start: dt.date) -> int:
    """Days remaining until the end of the current mandala.

    Assumes 7 days/week and 1 mandala = 7 weeks for the standard 15.
    """
    end_week = next(hi for lo, hi, _ in MANDALAS if lo <= week <= hi)
    return max(0, (end_week - week + 1) * 7)


# --------------------------------------------------------------------------
# Battle result type
# --------------------------------------------------------------------------
@dataclass
class BattleResult:
    concept_id: str
    name: str
    week: int
    tier_before: str
    score: int
    xp_delta: int
    new_stability: float
    new_ef: float
    rescued: bool
    lost: bool

    def summary(self) -> str:
        verdict = "RESCUED" if self.rescued else "LOST" if self.lost else "REVIEW"
        return (f"[{verdict}] {self.name} (W{self.week}) "
                f"score={self.score} xp={self.xp_delta:+d} "
                f"tier_before={self.tier_before}")


# --------------------------------------------------------------------------
# Concept selection
# --------------------------------------------------------------------------
def _concept_retention(c: dict[str, Any], today: dt.date) -> float:
    if c.get("last_seen") is None:
        # Brand new concept: pretend we just saw it today -- FRESH.
        return 1.0
    days = (today - dt.date.fromisoformat(c["last_seen"])).days
    return retention(c["stability"], days)


def eligible_for(memory: dict[str, Any], today: dt.date,
                 tier: str = "WANING") -> list[tuple[dict[str, Any], float]]:
    """Concepts at or below the named retention tier."""
    cutoff = {
        "FRESH": 1.01, "SETTLING": TIER_FRESH, "WANING": TIER_SETTLING,
        "FADING": TIER_WANING, "LOST": TIER_FADING,
    }[tier]
    out = []
    for c in memory["concepts"].values():
        r = _concept_retention(c, today)
        if r <= cutoff:
            out.append((c, r))
    out.sort(key=lambda cr: cr[1])
    return out


# --------------------------------------------------------------------------
# Battle application -- applies SM-2 + persistence + character write.
# --------------------------------------------------------------------------
def apply_recall(concept: dict[str, Any], score: int,
                 today: dt.date,
                 char: dict[str, Any] | None = None,
                 stat: str = "WIS",
                 class_bonus: float = 0.0) -> BattleResult:
    """Run one battle against a concept; update memory DB + character.

    char: the loaded character.json dict. If provided, also writes XP/HP
          changes back to journal/character.json.
    """
    r_before = _concept_retention(concept, today)
    tier_before = tier_for_retention(r_before)

    new_I, new_EF = update_sm2(concept["stability"], concept["ef"], score)
    xp = xp_for_recall(score, r_before, class_bonus=class_bonus)

    rescued = score >= 3
    lost = score <= 1

    # Persist concept update
    memory = load_memory(CONCEPT_FILE)
    cid = concept["id"]
    if cid in memory["concepts"]:
        c = memory["concepts"][cid]
        c["stability"] = round(new_I, 4)
        c["ef"] = round(new_EF, 4)
        c["last_score"] = score
        c["last_seen"] = today.isoformat()
        c["times_fought"] = c.get("times_fought", 0) + 1
        c["times_rescued"] = c.get("times_rescued", 0) + (1 if rescued else 0)
        c["times_lost"] = c.get("times_lost", 0) + (1 if lost else 0)
        save_memory(memory, CONCEPT_FILE)

    # Persist character update
    if char is not None:
        char["total_xp"] = max(0, char.get("total_xp", 0) + xp)
        char["stats"][stat] = char["stats"].get(stat, 0) + max(0, xp)
        # Lost FADING->LOST tick: only if it was a memory-loss event for a concept
        # already in FADING or LOST (we treat this as HP loss signal)
        if tier_before in ("FADING", "LOST") and lost:
            char["hp"] = max(0, char.get("hp", 100) - 5)
        if char.get("last_active") is None:
            char["last_active"] = today.isoformat()

    return BattleResult(
        concept_id=cid,
        name=concept.get("name", "?"),
        week=concept.get("week", 0),
        tier_before=tier_before,
        score=score,
        xp_delta=xp,
        new_stability=new_I,
        new_ef=new_EF,
        rescued=rescued,
        lost=lost,
    )


# --------------------------------------------------------------------------
# Battle type orchestration
# --------------------------------------------------------------------------
def select_ambush_target(memory: dict[str, Any], today: dt.date,
                          seed: int | None = None
                          ) -> Optional[dict[str, Any]]:
    """Pick the most-at-risk concept (lowest retention) eligible for ambush."""
    candidates = eligible_for(memory, today, tier="WANING")
    if not candidates:
        return None
    if seed is not None:
        rng = random.Random(seed)
        # Bias toward lowest-retention but allow a small handful of picks.
        idx = min(len(candidates) - 1, int(rng.random() * min(3, len(candidates))))
        return candidates[idx][0]
    return candidates[0][0]


def should_trigger_ambush(memory: dict[str, Any], today: dt.date,
                          probability: float = 0.25,
                          seed: int | None = None) -> bool:
    """Moderate aggression -- ambush only if a concept is at WANING or below,
    and only with the given probability (default 25% per status)."""
    if not eligible_for(memory, today, tier="WANING"):
        return False
    rng = random.Random(seed) if seed is not None else random
    return rng.random() < probability


def resurrection_queue(memory: dict[str, Any], today: dt.date) -> list[dict[str, Any]]:
    """Concepts that have decayed to LOST (R < 0.10)."""
    return [c for c, _ in eligible_for(memory, today, tier="LOST")]


def mandala_barrier_picks(memory: dict[str, Any], current_mandala: int,
                          today: dt.date) -> list[dict[str, Any]]:
    """One random concept per prior mandala for the Mandala Barrier boss.

    Used when the learner crosses into a new mandala.
    """
    rng = random.Random()
    picks = []
    for idx in range(1, current_mandala):
        lo, hi, _ = MANDALAS[idx - 1] if idx <= len(MANDALAS) else MANDALAS[-1]
        in_range = [
            c for cid, c in memory["concepts"].items()
            if lo <= c.get("week", 0) <= hi
        ]
        if in_range:
            picks.append(rng.choice(in_range))
    return picks


def weekly_forge_picks(memory: dict[str, Any], week: int,
                       today: dt.date) -> list[dict[str, Any]]:
    """Top-3 decaying concepts from current week and prior week for Friday Forge."""
    in_range = [
        c for cid, c in memory["concepts"].items()
        if c.get("week") in (week, week - 1)
    ]
    scored = sorted(
        ((c, _concept_retention(c, today)) for c in in_range),
        key=lambda x: x[1],
    )
    return [c for c, _ in scored[:3]]


# Quick self-test
if __name__ == "__main__":
    import concept_seed  # noqa: F401  -- ensure importable
    print("Battle engine loaded OK.")
    print(f"Mandala 14 = weeks {MANDALAS[13][0]}-{MANDALAS[13][1]} "
          f"'{MANDALAS[13][2]}'")
    print(f"Mandala 16 (graduation) = weeks {MANDALAS[15][0]}-{MANDALAS[15][1]} "
          f"'{MANDALAS[15][2]}'")
