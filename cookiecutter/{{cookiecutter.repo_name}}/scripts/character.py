"""Character sheet + main RPG CLI.

Subcommands:
    status       -- render full character sheet (default if no subcommand)
    init         -- bootstrap character.json + memory.json from journals
    log          -- log this week's XP manually (interview / behavioral bonus)
    boss N       -- record a boss-fight (gate or capstone) reward
    restore      -- spend a recovery week (+HP, gate buffer)
    achievements -- list unlocked achievements

The character save lives at journal/character.json and is git-tracked.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Optional


from battle import (
    MANDALAS, apply_recall, days_to_mandala_end, eligible_for, mandala_for_week,
    mandala_name, resurrection_queue, select_ambush_target,
    should_trigger_ambush,
)
from concept_seed import (
    JOURNAL_DIR, MEMORY_FILE, load_memory, save_memory, seed_memory, stats,
)
from forgetting import (
    retention, retention_multiplier, tier_for_retention, update_sm2,
    xp_for_recall, level_from_xp, xp_into_level,
)


CHARACTER_FILE = Path("journal/character.json")
CHARACTER_VERSION = 1


# --------------------------------------------------------------------------
# Class system -- tied to cookiecutter `track` variable.
# --------------------------------------------------------------------------
CLASSES: dict[str, tuple[str, dict[str, float]]] = {
    "balanced": (
        "Engineering Druid",
        {"WIS": 0.0, "ALGO": 0.0, "ENG": 0.0,
         "INFER": 0.0, "PLAT": 0.0, "JUDG": 0.0},
    ),
    "production-ai-platform": (
        "Platform Paladin",
        {"PLAT": 0.10, "JUDG": 0.05},
    ),
    "llm-inference": (
        "Inference Wizard",
        {"INFER": 0.10, "ALGO": 0.05},
    ),
    "rag-agents": (
        "Retrieval Ranger",
        {"ENG": 0.10, "WIS": 0.05},
    ),
}


STATS: tuple[str, ...] = ("WIS", "ALGO", "ENG", "INFER", "PLAT", "JUDG")


def primary_stat_for_week(week: int) -> str:
    """Map week -> primary stat to grow this week."""
    if week <= 6:
        return "JUDG"
    if week <= 18:
        return "WIS"
    if week <= 30:
        return "WIS"
    if week <= 45:
        return "ENG"
    if week <= 57:
        return "JUDG"
    if week <= 69:
        return "JUDG"
    if week <= 81:
        return "ENG"
    if week <= 93:
        return "INFER"
    if week <= 102:
        return "PLAT"
    return "JUDG"


def class_for_track(track: str) -> tuple[str, dict[str, float]]:
    return CLASSES.get(track, CLASSES["balanced"])


# --------------------------------------------------------------------------
# Save IO
# --------------------------------------------------------------------------
def _now() -> dt.date:
    return dt.date.today()


def _read_start_date(readme: Path = Path("README.md")) -> Optional[dt.date]:
    if not readme.exists():
        return None
    m = re.search(r"Start date\*\*:\s*([0-9-]{10})", readme.read_text(encoding="utf-8"))
    return dt.date.fromisoformat(m.group(1)) if m else None


def new_character(name: str, track: str) -> dict[str, Any]:
    title, bonus = class_for_track(track)
    return {
        "version": CHARACTER_VERSION,
        "created": _now().isoformat(),
        "last_active": None,
        "name": name,
        "track": track,
        "class_title": title,
        "class_bonuses": bonus,
        "level": 1,
        "total_xp": 0,
        "hp": 100,
        "hp_max": 100,
        "streak_current": 0,
        "streak_longest": 0,
        "stats": {s: 0 for s in STATS},
        "achievements": [],
        "bosses_defeated": [],
        "recovery_used": 0,
        "weeks_completed": [],
    }


def load_character() -> dict[str, Any]:
    if not CHARACTER_FILE.exists():
        return {}
    return json.loads(CHARACTER_FILE.read_text(encoding="utf-8"))


def save_character(char: dict[str, Any]) -> None:
    CHARACTER_FILE.parent.mkdir(parents=True, exist_ok=True)
    CHARACTER_FILE.write_text(
        json.dumps(char, indent=2, sort_keys=True), encoding="utf-8"
    )


def ensure_character(track: str | None = None,
                     name: str | None = None) -> dict[str, Any]:
    char = load_character()
    if char:
        # Upgrade missing fields when the version moves forward.
        if not char.get("class_bonuses"):
            _, bonus = class_for_track(char.get("track", "balanced"))
            char["class_bonuses"] = bonus
        if not char.get("stats"):
            char["stats"] = {s: 0 for s in STATS}
        return char
    env_track = os.environ.get("T3_TRACK", "balanced")
    env_name = os.environ.get("T3_STUDENT", "Apprentice")
    title, bonus = class_for_track(track or env_track)
    char = new_character(name=name or env_name, track=track or env_track)
    char["class_bonuses"] = bonus
    return char


# --------------------------------------------------------------------------
# Auto-derive weekly XP from journal mtimes + checked boxes.
# --------------------------------------------------------------------------
CORE_CHECKBOX_RE = re.compile(r"- \[(?P<mark>[ xX])\]")
WEEK_FILE_RE = re.compile(r"week_(\d{1,3})\.md")
EVIDENCE_FIELDS = (
    "Code / implementation",
    "Benchmark / result",
    "Design doc / technical explanation",
    "Retrospective / learning note",
)


def _evidence_complete(text: str) -> bool:
    for field in EVIDENCE_FIELDS:
        m = re.search(
            rf"^- {re.escape(field)}:[ \t]*([^\n]+)$",
            text,
            re.MULTILINE,
        )
        if not m or not m.group(1).strip():
            return False
    return True


def auto_award(char: dict[str, Any],
               journal_dir: Path = JOURNAL_DIR,
               today: dt.date | None = None) -> dict[str, Any]:
    """Award XP retroactively from completed weeks since last status.

    Stamps weeks_completed once per week to avoid double-counting.
    Awards:
        - core deliverable shipped (+50)
        - forge Core/Boss done (+25)
        - retro filled (>=3 sections) (+15)
        - depth lane done (+30)
    """
    today = today or _now()
    if not journal_dir.exists():
        return char
    completed = set(char.get("weeks_completed", []))

    primary_xp_table = {
        "core": 50, "forge": 25, "retro": 15, "depth": 30,
    }

    for week_file in sorted(journal_dir.glob("week_*.md")):
        m = WEEK_FILE_RE.search(week_file.name)
        if not m:
            continue
        week = int(m.group(1))
        if week in completed:
            continue
        text = week_file.read_text(encoding="utf-8")

        # Core deliverable
        core_section = re.search(
            r"## Core status\n(?P<body>.*?)(?=\n## |\Z)", text, re.DOTALL
        )
        core_done = bool(core_section) and any(
            mark.lower() == "x"
            for mark in CORE_CHECKBOX_RE.findall(core_section.group("body"))
        )
        # Forge
        forge_done = bool(
            re.search(
                r"## Algorithmic Forge status\n- \[[xX]\]",
                text,
            )
        )
        # Retro filled -- boat position AND next heading present
        text_lower = text.lower()
        retro_filled = (
            "- [x] ahead" in text_lower
            or "- [x] on track" in text_lower
            or "- [x] drifting" in text_lower
        ) and ("next heading" in text_lower)
        # Depth
        depth_done = bool(
            re.search(
                r"## Optional depth status\n- \[[xX]\]",
                text,
            )
        )

        if not core_done:
            continue

        award = 0
        award += primary_xp_table["core"]
        if forge_done:
            award += primary_xp_table["forge"]
        if retro_filled:
            award += primary_xp_table["retro"]
        if depth_done:
            award += primary_xp_table["depth"]

        stat = primary_stat_for_week(week)
        char["total_xp"] = char.get("total_xp", 0) + award
        char["stats"][stat] = char["stats"].get(stat, 0) + award
        completed.add(week)
        # Streak: increment if this is the latest week completed
        char["streak_current"] = char.get("streak_current", 0) + 1
        char["streak_longest"] = max(
            char.get("streak_longest", 0),
            char["streak_current"],
        )

    # Boss-defeat achievements (gate weeks)
    gates_passed = []
    for week in (6, 18, 30, 45, 57, 69, 81, 93, 102, 108):
        if week in completed:
            gates_passed.append(week)
    char["bosses_defeated"] = gates_passed

    char["weeks_completed"] = sorted(completed)
    char["level"] = level_from_xp(char["total_xp"])
    char["last_active"] = today.isoformat()
    return char


# --------------------------------------------------------------------------
# Achievement rolls
# --------------------------------------------------------------------------
def _maybe_award_achievements(char: dict[str, Any]) -> list[str]:
    added = []
    have = set(char.get("achievements", []))
    completed = char.get("weeks_completed", [])

    candidates = [
        ("Foundations Graduate", 30 in completed, 30),
        ("Engineering + Systems Graduate", 69 in completed, 69),
        ("LLM Platform Graduate", 108 in completed, 108),
        ("Disciple Learner", 48 in completed, 48),  # 1 mandala done = ~7 weeks
        ("Iron Streak", char.get("streak_current", 0) >= 12, 12),
        ("Philosopher", char.get("streak_longest", 0) >= 10, 10),
    ]
    for name, cond, _ in candidates:
        if cond and name not in have:
            char.setdefault("achievements", []).append(name)
            added.append(name)
    return added


# --------------------------------------------------------------------------
# Display -- the character sheet.
# --------------------------------------------------------------------------
BAR_WIDTH = 12
EM_DASH = chr(8212)


def _bar(value: int, width: int = BAR_WIDTH) -> str:
    """Render a stat bar with a soft cap of 1000 XP per stat."""
    full = int(width * min(value, 1000) / 1000)
    return chr(9608) * full + " " * (width - full)


def _class_bonus(char: dict[str, Any], stat: str) -> float:
    bonuses = char.get("class_bonuses", {})
    return bonuses.get(stat, 0.0)


def _current_week(start: dt.date, today: dt.date) -> int:
    if not start:
        return 1
    return max(1, min(108, ((today - start).days // 7) + 1))


def render_character_sheet(char: dict[str, Any],
                          memory: dict[str, Any],
                          start: dt.date,
                          today: dt.date) -> str:
    week = _current_week(start, today)
    mandala_idx = mandala_for_week(week) - 1
    m_lo, m_hi, m_name = MANDALAS[mandala_idx]
    pct_through = min(1.0, (week - m_lo) / max(1, m_hi - m_lo + 1))
    days_in = (today - start).days if start else 0
    days_total = 108 * 7
    grad_days_left = max(0, days_total - days_in)
    level = char.get("level", 1)
    total_xp = char.get("total_xp", 0)
    into, cost, frac = xp_into_level(total_xp)
    hp = char.get("hp", 100)
    hp_max = char.get("hp_max", 100)

    # Concept memory tiers
    concept_counts = stats(memory)

    # Fading concepts (top 3)
    fading = eligible_for(memory, today, tier="WANING")[:3]

    # Class + stat readouts
    cls_title = char.get("class_title", "Apprentice")
    track = char.get("track", "balanced")
    streak = char.get("streak_current", 0)
    longest = char.get("streak_longest", 0)
    achievements = char.get("achievements", [])

    # Recent bosses
    bosses = char.get("bosses_defeated", [])

    lines: list[str] = []
    bar = "=" * 64

    lines.append(bar)
    title_line = f"  {cls_title.upper()}  --  L{level}  --  {char.get('name', 'Apprentice')}"
    lines.append(title_line)
    lines.append(bar)

    hp_bar = _bar(hp * 10, 20)  # HP * 10 = full bar
    streak_glyph = "*" if streak >= 3 else " "
    lines.append(
        f"  HP [{hp_bar}] {hp}/{hp_max}"
    )
    lines.append(
        f"  Streak {streak_glyph} {streak} weeks (longest {longest})     "
        f"Achievements: {len(achievements)}"
    )
    lines.append("")

    lines.append(
        f"  MANDALA {m_name.upper()}  (Weeks {m_lo}-{m_hi}, "
        f"{pct_through*100:>4.1f}% through)"
    )
    lines.append(
        f"  Day {days_in}/{days_total}    "
        f"Graduation in {grad_days_left} days    "
        f"Current week: {week}"
    )
    lines.append("")

    xp_bar = _bar(into * BAR_WIDTH // max(1, cost))
    lines.append(
        f"  XP  L{level:<2} {into:>5}/{cost:<5}  [{xp_bar}]  "
        f"  total: {total_xp:>6}"
    )
    lines.append("")

    lines.append("  STATS")
    for s in STATS:
        v = char["stats"].get(s, 0)
        bonus = _class_bonus(char, s)
        bonus_glyph = "+" if bonus > 0 else " "
        lines.append(
            f"   {s:<5} {_bar(v):<{BAR_WIDTH}}  {v:>5} {bonus_glyph}{int(bonus*100):>2}%"
        )

    lines.append("")
    lines.append(f"  CONCEPT MEMORY  ({concept_counts['total']} tracked)")
    for tier_name in ("FRESH", "SETTLING", "WANING", "FADING", "LOST", "UNSEEN"):
        c = concept_counts.get(tier_name, 0)
        lines.append(f"    {tier_name:<10} {c:>5}")

    if fading:
        lines.append("")
        lines.append("  FORGOTTEN ECHOES (top-3 most-at-risk):")
        for c, r in fading:
            name = c.get("name", "?")[:50]
            tier = tier_for_retention(r)
            lines.append(f"    [{tier:<8} R={r:.2f}]  W{c.get('week', 0):>3}  {name}")

    lines.append("")
    if achievements:
        lines.append("  ACHIEVEMENTS")
        for a in achievements[-6:]:
            lines.append(f"    * {a}")

    if bosses:
        lines.append("")
        lines.append(f"  BOSSES DEFEATED: {', '.join(f'W{b}' for b in bosses)}")

    lines.append(bar)
    lines.append(
        f"  Run \033[1mmake log\033[0m for interview-style XP,  "
        f"\033[1mmake ambush=1\033[0m to force a recall battle."
        if False else  # avoid ANSI in pure text mode
        "  Run `make log` for bonus XP, `make ambush=1` to force a recall battle."
    )
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Subcommand handlers
# --------------------------------------------------------------------------
def cmd_init(args: argparse.Namespace) -> int:
    track = args.track or os.environ.get("T3_TRACK", "balanced")
    name = args.name or os.environ.get("T3_STUDENT", "Apprentice")

    # Seed memory
    mem = seed_memory(merge=True)
    print(f"  Memory DB: {len(mem['concepts'])} concepts")

    # Bootstrap character
    char = ensure_character(track=track, name=name)
    char = auto_award(char)
    added = _maybe_award_achievements(char)
    save_character(char)
    print(f"  Character initialized: {char.get('class_title', '?')}")
    if added:
        print(f"  New achievements: {', '.join(added)}")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    # Lazy bootstrap on first status
    if not CHARACTER_FILE.exists() or not MEMORY_FILE.exists():
        os.environ["T3_TRACK"] = args.track or "balanced"
        cmd_init(args)

    char = load_character()
    memory = load_memory()
    char = auto_award(char)
    save_character(char)
    print(render_character_sheet(char, memory,
                                _read_start_date() or dt.date(2026, 1, 5),
                                _now()))
    return 0


def cmd_log(args: argparse.Namespace) -> int:
    char = load_character()
    if not char:
        cmd_init(args)
        char = load_character()

    today = _now()
    print("Log weekly XP. Pick what shipped this week:")
    print("  c  Core deliverable        (+50 XP)")
    print("  f  Forge Core/Boss done    (+25 XP)")
    print("  r  Retro filled            (+15 XP)")
    print("  d  Optional depth done     (+30 XP)")
    print("  i  Interview artifact      (+20 XP)")
    print("  b  Behavioral story banked (+20 XP)")
    print("  Enter blank to cancel.")

    picks = []
    while True:
        try:
            line = input("  add [c/f/r/d/i/b] : ").strip().lower()
        except EOFError:
            break
        if not line:
            break
        if line in {"c", "f", "r", "d", "i", "b"}:
            picks.append(line)
            print(f"    queued: {line}")
        else:
            print(f"    unknown: {line!r} (use c/f/r/d/i/b)")

    award_map = {"c": 50, "f": 25, "r": 15, "d": 30, "i": 20, "b": 20}
    week = _current_week(_read_start_date() or dt.date.today(), today)
    stat = primary_stat_for_week(week)
    total = 0
    for p in picks:
        total += award_map[p]
    char["total_xp"] = char.get("total_xp", 0) + total
    char["stats"][stat] = char["stats"].get(stat, 0) + total
    char["level"] = level_from_xp(char["total_xp"])
    char["last_active"] = today.isoformat()
    char["streak_current"] = char.get("streak_current", 0) + (1 if picks else 0)
    added = _maybe_award_achievements(char)
    save_character(char)
    print(f"\n  Awarded: +{total} XP to {stat}")
    print(f"  New level: L{char['level']} ({char['total_xp']} total XP)")
    if added:
        print(f"  Achievements: {', '.join(added)}")
    return 0


def cmd_boss(args: argparse.Namespace) -> int:
    char = load_character()
    if not char:
        cmd_init(args)
        char = load_character()
    week = args.week
    if not (1 <= week <= 108):
        print("  --week must be 1..108")
        return 2

    completed = set(char.get("weeks_completed", []))
    if week in completed:
        print(f"  Boss W{week} already recorded.")
    else:
        completed.add(week)
        char.setdefault("weeks_completed", []).extend([])  # ensure key
        char["weeks_completed"] = sorted(completed)
        award = 200 if week in (108,) else 100
        char["total_xp"] = char.get("total_xp", 0) + award
        stat = primary_stat_for_week(week)
        char["stats"][stat] = char["stats"].get(stat, 0) + award
        char["streak_current"] = char.get("streak_current", 0) + 1
        char["level"] = level_from_xp(char["total_xp"])
        save_character(char)
        print(f"  Boss W{week} recorded. +{award} XP to {stat}.")
    added = _maybe_award_achievements(char)
    save_character(char)
    if added:
        print(f"  Achievements: {', '.join(added)}")
    return 0


def cmd_restore(args: argparse.Namespace) -> int:
    char = load_character()
    if not char:
        cmd_init(args)
        char = load_character()
    char["hp"] = min(char.get("hp_max", 100), char.get("hp", 0) + 30)
    char["recovery_used"] = char.get("recovery_used", 0) + 1
    # Reset streak so it isn't a punishment
    char["streak_current"] = max(1, char.get("streak_current", 0))
    save_character(char)
    print(f"  Recovery used. HP restored to {char['hp']}/{char['hp_max']}.")
    print("  Streak preserved.")
    return 0


def cmd_recall(args: argparse.Namespace) -> int:
    """Print concepts ordered by current retention, most at risk first."""
    memory = load_memory()
    today = _now()
    ordered = eligible_for(memory, today, tier="FRESH")
    # Eligible_for with FRESH gives everything at or below FRESH -- invert.
    all_concepts = sorted(
        memory["concepts"].values(),
        key=lambda c: retention(c["stability"],
                                (today - dt.date.fromisoformat(c["last_seen"])
                                 ).days if c.get("last_seen") else 0),
    )
    print(f"  {'Tier':<10} {'R':>5}  {'W':>4}  Concept")
    for c in all_concepts:
        if c.get("last_seen") is None:
            r = 1.0
            tier = "UNSEEN"
        else:
            days = (today - dt.date.fromisoformat(c["last_seen"])).days
            r = retention(c["stability"], days)
            tier = tier_for_retention(r)
        print(f"  {tier:<10} {r:>5.2f}  W{c.get('week', 0):>3}  "
              f"{c['name'][:60]}")
    return 0


def cmd_ambush(args: argparse.Namespace) -> int:
    """Trigger a hallway ambush against the most-at-risk concept."""
    memory = load_memory()
    char = load_character()
    if not char:
        cmd_init(args)
        char = load_character()
    today = _now()
    target = select_ambush_target(memory, today)
    if not target is None:
        # Inline prompt: simulated interview of the named concept
        cls_title = char.get("class_title", "?")
        print()
        print("=" * 64)
        print(f"  HALLWAY AMBUSH")
        print(f"  Target: W{target.get('week', 0)} -- {target['name']}")
        last = target.get("last_seen")
        if last:
            days = (today - dt.date.fromisoformat(last)).days
            r = retention(target["stability"], days)
            print(f"  Last seen: {days} days ago, R(t)={r:.2f}, "
                  f"tier={tier_for_retention(r)}")
        print(f"  Class: {cls_title}")
        print("=" * 64)
        print("  Recall the concept out loud or in writing.")
        print("  Then self-rate: 0 (blackout) .. 5 (perfect)")
        try:
            score_str = input("  Score [0-5, or blank to retreat]: ").strip()
        except EOFError:
            score_str = ""
        if not score_str:
            print("  Retreated. No penalty. Concept rescheduled.")
            return 0
        try:
            score = int(score_str)
        except ValueError:
            print("  Invalid score -- treating as retreat.")
            return 0
        stat = primary_stat_for_week(target.get("week", 1))
        class_bonus = char.get("class_bonuses", {}).get(stat, 0.0)
        result = apply_recall(target, score, today, char=char,
                              stat=stat, class_bonus=class_bonus)
        save_character(char)
        print()
        print("=" * 64)
        print(f"  Result: {result.summary()}")
        print(f"  Stability: {target['stability']:.2f} -> {result.new_stability:.2f}")
        print(f"  Easiness: {target['ef']:.2f} -> {result.new_ef:.2f}")
        print("=" * 64)
    else:
        print("  No ambush candidates. Memory is sharp.")
    return 0


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    p_status = sub.add_parser("status", help="render character sheet")
    p_status.set_defaults(func=cmd_status)

    p_init = sub.add_parser("init", help="bootstrap character + memory")
    p_init.add_argument("--track", default=None)
    p_init.add_argument("--name", default=None)
    p_init.set_defaults(func=cmd_init)

    p_log = sub.add_parser("log", help="log this week's XP manually")
    p_log.set_defaults(func=cmd_log)

    p_boss = sub.add_parser("boss", help="record a boss-fight")
    p_boss.add_argument("--week", type=int, required=True)
    p_boss.set_defaults(func=cmd_boss)

    p_restore = sub.add_parser("restore", help="use a recovery week")
    p_restore.set_defaults(func=cmd_restore)

    p_recall = sub.add_parser("recall", help="list concepts by retention")
    p_recall.set_defaults(func=cmd_recall)

    p_ambush = sub.add_parser("ambush", help="trigger hallway ambush")
    p_ambush.set_defaults(func=cmd_ambush)

    parser.add_argument("--track", default=None)
    parser.add_argument("--name", default=None)

    args = parser.parse_args()
    if args.cmd is None:
        # Default to status for ergonomic `python scripts/character.py`
        args.cmd = "status"
        args.func = cmd_status
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
