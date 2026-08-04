"""Concept memory bootstrap.

Walks the generated `journal/weeks/week_*.md` files and extracts three
concepts per week (title / focus / deliverable). The first call creates
`journal/memory.json`; subsequent calls merge in any new weeks.

Run from the repo root:
    python scripts/concept_seed.py            # seed / update memory DB
    python scripts/concept_seed.py --stats    # print concept counts
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


JOURNAL_DIR = Path("journal/weeks")
MEMORY_FILE = Path("journal/memory.json")
SEED_VERSION = 2


# --------------------------------------------------------------------------
# Extraction patterns -- match the cookiecutter-rendered weekly journal.
# --------------------------------------------------------------------------
WEEK_RE = re.compile(r"week_(\d{1,3})\.md")
TITLE_RE = re.compile(r"^# Week \d+:\s*(?P<title>[^\n]+)", re.MULTILINE)
FOCUS_RE = re.compile(r"^\*\*Focus:\*\*\s*(?P<focus>[^*\n]+)", re.MULTILINE)
DELIV_RE = re.compile(r"^\*\*Core deliverable:\*\*\s*(?P<deliv>[^*\n]+)", re.MULTILINE)


def _slugify(text: str) -> str:
    raw = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return raw[:48] or "concept"


def _concept_id(week: int, kind: str, text: str) -> str:
    return f"w{week:03d}-{kind}-{_slugify(text)}"


def extract_concepts(week: int, text: str) -> list[dict[str, Any]]:
    """Pull the three baseline concepts from a generated weekly journal."""
    out: list[dict[str, Any]] = []
    seen = set()

    def add(kind: str, value: str) -> None:
        value = value.strip()
        if not value or len(value) < 3:
            return
        cid = _concept_id(week, kind, value)
        if cid in seen:
            return
        seen.add(cid)
        out.append({
            "id": cid,
            "name": value,
            "kind": kind,
            "week": week,
        })

    m = TITLE_RE.search(text)
    if m:
        add("title", m.group("title"))
    m = FOCUS_RE.search(text)
    if m:
        add("focus", m.group("focus"))
    m = DELIV_RE.search(text)
    if m:
        add("deliverable", m.group("deliv"))

    return out


# --------------------------------------------------------------------------
# Memory DB IO
# --------------------------------------------------------------------------
def _defaults() -> dict[str, Any]:
    return {
        "version": SEED_VERSION,
        "seeded_from": "journal",
        "concepts": {},
    }


def _new_concept_row(c: dict[str, Any]) -> dict[str, Any]:
    """Build the full concept record with SM-2 defaults."""
    return {
        **c,
        "stability": 1.0,
        "ef": 2.5,
        "difficulty": 3,
        "last_score": None,
        "last_seen": None,
        "times_fought": 0,
        "times_rescued": 0,
        "times_lost": 0,
    }


def load_memory(path: Path = MEMORY_FILE) -> dict[str, Any]:
    if not path.exists():
        return _defaults()
    return json.loads(path.read_text(encoding="utf-8"))


def save_memory(memory: dict[str, Any], path: Path = MEMORY_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(memory, indent=2, sort_keys=True), encoding="utf-8")


def seed_memory(journal_dir: Path = JOURNAL_DIR,
                memory_file: Path = MEMORY_FILE,
                merge: bool = True) -> dict[str, Any]:
    """Walk journal/weeks, extract concepts, write journal/memory.json.

    merge=True keeps existing concept state (last_score, stability, etc.)
    and adds new weeks without resetting battle history.
    """
    if not journal_dir.exists():
        return _defaults()

    if merge:
        memory = load_memory(memory_file)
    else:
        memory = _defaults()

    added = 0
    for week_file in sorted(journal_dir.glob("week_*.md")):
        m = WEEK_RE.search(week_file.name)
        if not m:
            continue
        week = int(m.group(1))
        text = week_file.read_text(encoding="utf-8")
        for concept in extract_concepts(week, text):
            cid = concept["id"]
            if cid in memory["concepts"]:
                continue
            memory["concepts"][cid] = _new_concept_row(concept)
            added += 1

    memory["version"] = SEED_VERSION
    save_memory(memory, memory_file)
    memory["_added_this_run"] = added
    return memory


def stats(memory: dict[str, Any]) -> dict[str, int]:
    """Bucket concept counts by tier name -- useful for dashboard output."""
    import datetime as dt
    from forgetting import retention, tier_for_retention

    today = dt.date.today()
    counts = {t: 0 for t in ("FRESH", "SETTLING", "WANING", "FADING", "LOST", "UNSEEN")}
    for c in memory["concepts"].values():
        if c.get("last_seen") is None:
            counts["UNSEEN"] += 1
            continue
        days = (today - dt.date.fromisoformat(c["last_seen"])).days
        r = retention(c["stability"], days)
        counts[tier_for_retention(r)] += 1
    counts["total"] = sum(counts.values())
    return counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stats", action="store_true",
                        help="print concept tier counts and exit")
    parser.add_argument("--fresh", action="store_true",
                        help="regenerate memory from scratch (loses battle history)")
    args = parser.parse_args()

    if args.stats:
        memory = load_memory()
        counts = stats(memory)
        print(f"Total concepts: {counts.pop('total')}")
        for tier, count in counts.items():
            print(f"  {tier:<10} {count}")
        return

    memory = seed_memory(merge=not args.fresh)
    added = memory.pop("_added_this_run", 0)
    total = len(memory["concepts"])
    print(f"Concept memory: {MEMORY_FILE}")
    print(f"  Total concepts: {total}")
    print(f"  Added this run: {added}")


if __name__ == "__main__":
    main()
