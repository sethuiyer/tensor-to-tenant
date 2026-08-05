"""Build scripts for the remaining schema YAML files.

Reads src/data/*.ts and emits schema/*.yaml with the schema discipline.
T1.3 will replace this with the canonical generator; for now, these
are one-off build scripts that avoid hand-transcription of 100s of
entries.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "src" / "data"
SCHEMA = REPO / "schema"


def parse_ts_array(text: str, var_name: str) -> list[dict]:
    """Parse a top-level TS array of objects: `const NAME: Type[] = [ { ... }, ... ];`

    Uses a state machine rather than regex because the array can contain
    nested braces, strings with braces, etc.
    """
    marker = f"export const {var_name}"
    start = text.find(marker)
    if start < 0:
        return []
    # Skip type annotation if present (e.g. `: Type[] = [`).
    # Find the LAST `=` before the array's `[`, which is the assignment,
    # not the `[]` from the type annotation.
    eq_pos = text.find("=", start)
    if eq_pos > 0:
        # Walk forward from `=` to find the first `[` that is the array opening.
        # (The `[]` from the type annotation comes BEFORE the `=`, not after.)
        bracket_start = text.find("[", eq_pos)
    else:
        bracket_start = text.find("[", start)
    if bracket_start < 0:
        return []

    # Walk through, tracking depth and string state
    items = []
    depth = 0
    in_string = False
    string_char = None
    i = bracket_start + 1  # skip the `[`
    item_start = i
    while i < len(text):
        c = text[i]
        if in_string:
            if c == "\\":
                i += 2
                continue
            if c == string_char:
                in_string = False
        else:
            if c in ("'", '"', "`"):
                in_string = True
                string_char = c
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    # End of object; capture the item text
                    item_text = text[item_start:i + 1]
                    items.append(parse_object_text(item_text))
                    item_start = i + 1
            elif c == "]" and depth == 0:
                break
        i += 1
    return items


def parse_object_text(text: str) -> dict:
    """Parse a single TS object literal `{ key: value, ... }` into a dict.

    Handles string values, array values, and nested objects one level deep.
    Sufficient for the TS files in this repo which don't have deeper nesting
    inside the array entries.
    """
    result = {}
    text = text.strip().rstrip(",").strip("{").strip("}").strip()
    if not text:
        return result
    i = 0
    while i < len(text):
        # Skip whitespace and commas
        while i < len(text) and text[i] in " \t\n,":
            i += 1
        if i >= len(text):
            break
        # Parse key (must be a quoted string or an identifier)
        if text[i] in ("'", '"'):
            key_end = text.index(text[i], i + 1)
            key = text[i + 1:key_end]
            i = key_end + 1
        else:
            m = re.match(r"([A-Za-z_][A-Za-z0-9_]*)", text[i:])
            if not m:
                break
            key = m.group(1)
            i += len(key)
        # Skip whitespace
        while i < len(text) and text[i] in " \t\n":
            i += 1
        if i >= len(text) or text[i] != ":":
            break
        i += 1  # skip the colon
        while i < len(text) and text[i] in " \t\n":
            i += 1
        # Parse value
        if i >= len(text):
            break
        if text[i] in ("'", '"', "`"):
            quote = text[i]
            # Find matching quote (handle escapes)
            j = i + 1
            value_chars = []
            while j < len(text):
                if text[j] == "\\":
                    value_chars.append(text[j + 1])
                    j += 2
                elif text[j] == quote:
                    break
                else:
                    value_chars.append(text[j])
                    j += 1
            value = "".join(value_chars)
            i = j + 1
        elif text[i] == "[":
            # Array value - find matching ]
            depth = 1
            j = i + 1
            while j < len(text) and depth > 0:
                if text[j] in ("'", '"', "`"):
                    quote2 = text[j]
                    j += 1
                    while j < len(text):
                        if text[j] == "\\":
                            j += 2
                            continue
                        if text[j] == quote2:
                            break
                        j += 1
                elif text[j] == "[":
                    depth += 1
                elif text[j] == "]":
                    depth -= 1
                j += 1
            # Parse the array contents as a JSON-ish list
            array_text = text[i + 1:j - 1]
            value = parse_array_value(array_text)
            i = j
        elif text[i] == "{":
            depth = 1
            j = i + 1
            while j < len(text) and depth > 0:
                if text[j] in ("'", '"', "`"):
                    quote2 = text[j]
                    j += 1
                    while j < len(text):
                        if text[j] == "\\":
                            j += 2
                            continue
                        if text[j] == quote2:
                            break
                        j += 1
                elif text[j] == "{":
                    depth += 1
                elif text[j] == "}":
                    depth -= 1
                j += 1
            value = parse_object_text(text[i:j])
            i = j
        else:
            # Bare number, boolean, or identifier
            m = re.match(r"([^,\n}]+)", text[i:])
            value = m.group(1).strip() if m else ""
            i += len(value)
        result[key] = value
    return result


def parse_array_value(text: str) -> list:
    """Parse a flat array of strings or numbers into a list."""
    result = []
    i = 0
    while i < len(text):
        while i < len(text) and text[i] in " \t\n,":
            i += 1
        if i >= len(text):
            break
        if text[i] in ("'", '"', "`"):
            quote = text[i]
            j = i + 1
            value_chars = []
            while j < len(text):
                if text[j] == "\\":
                    value_chars.append(text[j + 1])
                    j += 2
                elif text[j] == quote:
                    break
                else:
                    value_chars.append(text[j])
                    j += 1
            result.append("".join(value_chars))
            i = j + 1
        else:
            m = re.match(r"([^,\n\]]+)", text[i:])
            if m:
                result.append(m.group(1).strip())
                i += len(m.group(0))
            else:
                break
    return result


# Phase → (level, seam)
PHASE_META = {
    1: (1, "orientation"),
    2: (1, "math foundations"),
    3: (1, "math foundations"),
    4: (2, "engineering primitives"),
    5: (2, "system design"),
    6: (2, "MLOps"),
    7: (2, "LLM systems"),
    8: (3, "inference operations"),
    9: (3, "production AI platform"),
    10: (3, "graduation"),
}


def phase_for_week(week: int) -> int:
    """Map a week number to its phase (1-10)."""
    ranges = [(1, 6, 1), (7, 18, 2), (19, 30, 3), (31, 45, 4),
              (46, 57, 5), (58, 69, 6), (70, 81, 7), (82, 93, 8),
              (94, 102, 9), (103, 108, 10)]
    for lo, hi, p in ranges:
        if lo <= week <= hi:
            return p
    return 0


def gate_for_week(week: int) -> int | None:
    """Map week to its gate (if any)."""
    return {6: 1, 18: 2, 30: 3, 45: 4, 57: 5, 69: 6, 81: 7, 93: 8, 102: 9, 108: 10}.get(week)


# ============================================================================
# Build mandalas.yaml
# ============================================================================

def build_mandalas() -> None:
    text = (SRC / "mandalas.ts").read_text()
    raw = parse_ts_array(text, "MANDALAS")
    if not raw:
        print("mandalas.yaml: no MANDALAS parsed, skipping")
        return

    out_lines = [
        "# The 16-mandala identity progression.",
        "# 15 full mandalas (48 days each) + 1 graduation mandala = 16 entries.",
        "# Per T1.2 / T1.6: schema discipline with id / tier / level / seam /",
        "# cross_references. Each mandala is a load-bearing identity shift.",
        "",
    ]
    for m in raw:
        # Parse: id, weeks (string), days (string), title (string), identity,
        # topics (array), evidence (array), transformation (string)
        num = m.get("id") if isinstance(m.get("id"), int) else None
        if num is None:
            # id might be string like "1" or "final"
            id_str = str(m.get("id", ""))
        else:
            id_str = str(num)
        out_lines.append(f"- id: mandala-{id_str}")
        out_lines.append(f"  number: {id_str}")
        out_lines.append(f"  days: \"{m.get('days', '')}\"")
        out_lines.append(f"  weeks: \"{m.get('weeks', '')}\"")
        out_lines.append(f"  title: \"{m.get('title', '')}\"")
        out_lines.append(f"  identity: \"{m.get('identity', '')}\"")
        out_lines.append(f"  transformation: >")
        out_lines.append(f"    {m.get('transformation', '')}")
        out_lines.append(f"  tier: core")
        out_lines.append(f"  level: 2")
        out_lines.append(f"  seam: \"identity progression\"")
        out_lines.append(f"  topics:")
        topics = m.get("topics", [])
        if isinstance(topics, list):
            for t in topics:
                out_lines.append(f"    - \"{t}\"")
        out_lines.append(f"  evidence:")
        evidence = m.get("evidence", [])
        if isinstance(evidence, list):
            for e in evidence:
                out_lines.append(f"    - \"{e}\"")
        out_lines.append(f"  cross_references:")
        out_lines.append(f"    - {{ entity: weeks, role: \"identity shift window\" }}")
        out_lines.append("")

    (SCHEMA / "mandalas.yaml").write_text("\n".join(out_lines), encoding="utf-8")
    print(f"mandalas.yaml: wrote {len(raw)} mandalas")


# ============================================================================
# Build engineering.yaml
# ============================================================================

def build_engineering() -> None:
    text = (SRC / "engineering.ts").read_text()

    engineering_tasks = parse_ts_array(text, "ENGINEERING_TASKS")
    practice_exercises = parse_ts_array(text, "PRACTICE_EXERCISES")

    out_lines = [
        "# Engineering primitives: 30 production-style implementations + 40 timed drills.",
        "# Per T1.2: schema discipline with id / tier / level / seam /",
        "# cross_references. Phase 4 (Engineering Micro-Projects) anchors these.",
        "",
        "# ============================================================================",
        "# Engineering tasks (30)",
        "# ============================================================================",
        "",
    ]
    for t in engineering_tasks:
        n = t.get("n")
        title = t.get("title", "")
        out_lines.append(f"- id: eng-task-{n}")
        out_lines.append(f"  number: {n}")
        out_lines.append(f"  title: \"{title}\"")
        out_lines.append(f"  tier: core")
        out_lines.append(f"  level: 2")
        out_lines.append(f"  seam: \"engineering primitives\"")
        out_lines.append(f"  cross_references:")
        out_lines.append(f"    - {{ entity: phases, phase_id: phase-4, role: \"lives in Phase 4\" }}")
        out_lines.append(f"    - {{ entity: gates, gate_id: gate-4, role: \"verified at gate 4\" }}")
        out_lines.append("")

    out_lines.extend([
        "",
        "# ============================================================================",
        "# Practice exercises (40 timed drills)",
        "# ============================================================================",
        "",
    ])
    for e in practice_exercises:
        n = e.get("n")
        title = e.get("title", "")
        out_lines.append(f"- id: practice-{n}")
        out_lines.append(f"  number: {n}")
        out_lines.append(f"  title: \"{title}\"")
        out_lines.append(f"  tier: core")
        out_lines.append(f"  level: 2")
        out_lines.append(f"  seam: \"engineering primitives\"")
        out_lines.append(f"  cross_references:")
        out_lines.append(f"    - {{ entity: phases, phase_id: phase-4, role: \"lives in Phase 4\" }}")
        out_lines.append("")

    (SCHEMA / "engineering.yaml").write_text("\n".join(out_lines), encoding="utf-8")
    print(f"engineering.yaml: wrote {len(engineering_tasks)} tasks + {len(practice_exercises)} exercises")


# ============================================================================
# Build system_design.yaml
# ============================================================================

def build_system_design() -> None:
    text = (SRC / "systemDesign.ts").read_text()

    arrays = {
        "design_weeks": "DESIGN_WEEKS",
        "design_loop": "DESIGN_LOOP",
        "tech_core": "DESIGN_TECH_CORE",
        "tech_supporting": "DESIGN_TECH_SUPPORTING",
        "tech_question": "DESIGN_TECH_QUESTION",
        "patterns": "DESIGN_PATTERNS",
        "pattern_index_foundations": "DESIGN_PATTERN_INDEX_FOUNDATIONS",
        "pattern_index_distributed": "DESIGN_PATTERN_INDEX_DISTRIBUTED",
        "families": "DESIGN_FAMILIES",
        "cases": "DESIGN_CASES",
        "ood": "DESIGN_OOD",
        "ood_contract": "DESIGN_OOD_CONTRACT",
        "ai_extensions": "DESIGN_AI_EXTENSIONS",
        "capabilities": "DESIGN_CAPABILITIES",
        "gate5": "DESIGN_GATE5",
    }

    parsed = {name: parse_ts_array(text, ts_name) for name, ts_name in arrays.items()}

    out_lines = [
        "# System design track (Weeks 46-57): canonical interview prep.",
        "# Per T1.2: schema discipline with id / tier / level / seam /",
        "# cross_references. Phase 5 anchors the system design weeks.",
        "",
    ]

    # design_weeks (12 entries)
    out_lines.extend([
        "# ============================================================================",
        "# Design weeks (Weeks 46-57)",
        "# ============================================================================",
        "",
    ])
    for w in parsed["design_weeks"]:
        out_lines.append(f"- id: design-week-{w.get('week')}")
        out_lines.append(f"  week: {w.get('week')}")
        out_lines.append(f"  topic: \"{w.get('topic', '')}\"")
        out_lines.append(f"  case_lab: \"{w.get('caseLab', '')}\"")
        out_lines.append(f"  evidence: \"{w.get('evidence', '')}\"")
        out_lines.append(f"  tier: core")
        out_lines.append(f"  level: 2")
        out_lines.append(f"  seam: \"system design\"")
        out_lines.append(f"  cross_references:")
        out_lines.append(f"    - {{ entity: phases, phase_id: phase-5, role: \"lives in Phase 5\" }}")
        out_lines.append(f"    - {{ entity: weeks, week: {w.get('week')}, role: \"spine alignment\" }}")
        out_lines.append("")

    # design_loop (4 steps)
    out_lines.extend([
        "",
        "# ============================================================================",
        "# Four-layer design loop",
        "# ============================================================================",
        "",
    ])
    for step in parsed["design_loop"]:
        out_lines.append(f"- id: design-loop-{step.get('step', '').lower()}")
        out_lines.append(f"  step: \"{step.get('step', '')}\"")
        out_lines.append(f"  detail: \"{step.get('detail', '')}\"")
        out_lines.append(f"  tier: core")
        out_lines.append(f"  level: 2")
        out_lines.append(f"  seam: \"system design methodology\"")
        out_lines.append("")

    # patterns (10 design patterns)
    out_lines.extend([
        "",
        "# ============================================================================",
        "# Design patterns (canonical library)",
        "# ============================================================================",
        "",
    ])
    for p in parsed["patterns"]:
        out_lines.append(f"- id: design-pattern-{p.get('pattern', '').lower().replace(' ', '-').replace('(', '').replace(')', '')}")
        out_lines.append(f"  pattern: \"{p.get('pattern', '')}\"")
        out_lines.append(f"  problem: \"{p.get('problem', '')}\"")
        out_lines.append(f"  solution: \"{p.get('solution', '')}\"")
        out_lines.append(f"  tier: core")
        out_lines.append(f"  level: 2")
        out_lines.append(f"  seam: \"design patterns\"")
        out_lines.append("")

    # cases (10 case studies)
    out_lines.extend([
        "",
        "# ============================================================================",
        "# Case studies (deep-dives)",
        "# ============================================================================",
        "",
    ])
    for c in parsed["cases"]:
        out_lines.append(f"- id: design-case-{c.get('name', '').lower().replace(' ', '-')}")
        out_lines.append(f"  name: \"{c.get('name', '')}\"")
        out_lines.append(f"  focuses: \"{c.get('focuses', '')}\"")
        out_lines.append(f"  tier: core")
        out_lines.append(f"  level: 2")
        out_lines.append(f"  seam: \"case study\"")
        out_lines.append("")

    # families (8 families)
    out_lines.extend([
        "",
        "# ============================================================================",
        "# Case-study families",
        "# ============================================================================",
        "",
    ])
    for f in parsed["families"]:
        out_lines.append(f"- id: design-family-{f.get('family', '').lower().replace(' ', '-').replace(',', '')}")
        out_lines.append(f"  family: \"{f.get('family', '')}\"")
        out_lines.append(f"  cases: \"{f.get('cases', '')}\"")
        out_lines.append(f"  tier: core")
        out_lines.append(f"  level: 2")
        out_lines.append(f"  seam: \"case-study taxonomy\"")
        out_lines.append("")

    # OOD list (scalar list)
    out_lines.extend([
        "",
        "# ============================================================================",
        "# OOD / LLD problems (Thursday implementation variant)",
        "# ============================================================================",
        "",
    ])
    ood_items = parsed["ood"]
    if isinstance(ood_items, list) and ood_items and isinstance(ood_items[0], dict) is False:
        # OOD is a flat string array
        out_lines.append("- id: ood-problems")
        out_lines.append("  problems:")
        for o in ood_items:
            out_lines.append(f"    - \"{o}\"")
        out_lines.append(f"  tier: core")
        out_lines.append(f"  level: 2")
        out_lines.append(f"  seam: \"object-oriented design\"")

    # ai_extensions (scalar list of dicts)
    if parsed["ai_extensions"]:
        out_lines.extend([
            "",
            "# ============================================================================",
            "# AI extensions (one per base design)",
            "# ============================================================================",
            "",
        ])
        for e in parsed["ai_extensions"]:
            out_lines.append(f"- id: ai-extension-{e.get('base', '').lower().replace(' ', '-')}")
            out_lines.append(f"  base: \"{e.get('base', '')}\"")
            out_lines.append(f"  extension: \"{e.get('extension', '')}\"")
            out_lines.append(f"  tier: core")
            out_lines.append(f"  level: 3")
            out_lines.append(f"  seam: \"design + AI\"")
            out_lines.append("")

    # tech_core, tech_supporting (scalar arrays of strings)
    if parsed["tech_core"]:
        out_lines.extend([
            "",
            "# ============================================================================",
            "# Core technologies (substrate for the patterns)",
            "# ============================================================================",
            "",
            "- id: tech-core",
            "  tier: core",
            "  technologies:",
        ])
        for t in parsed["tech_core"]:
            if isinstance(t, str):
                out_lines.append(f"    - \"{t}\"")
        out_lines.append(f"  seam: \"technology substrate\"")
        out_lines.append("")

    if parsed["tech_supporting"]:
        out_lines.append("- id: tech-supporting")
        out_lines.append("  tier: core")
        out_lines.append("  technologies:")
        for t in parsed["tech_supporting"]:
            if isinstance(t, str):
                out_lines.append(f"    - \"{t}\"")
        out_lines.append(f"  seam: \"technology substrate (supporting)\"")

    (SCHEMA / "system_design.yaml").write_text("\n".join(out_lines), encoding="utf-8")
    print(f"system_design.yaml: wrote {sum(len(v) if isinstance(v, list) else 0 for v in parsed.values())} entries")


# ============================================================================
# Build math.yaml
# ============================================================================

def build_math() -> None:
    text = (SRC / "math.ts").read_text()
    tracks = parse_ts_array(text, "MATH_TRACKS")
    if not tracks:
        print("math.yaml: no MATH_TRACKS parsed, skipping")
        return

    out_lines = [
        "# Mastery-level mathematics curriculum: 100 modules across 10 tracks.",
        "# Per T1.2: schema discipline with id / tier / level / seam /",
        "# cross_references. Phase 2-3 anchor the math weeks (W7-30).",
        "",
    ]
    for t in tracks:
        track_id = t.get("id")
        out_lines.append(f"- id: math-track-{track_id}")
        out_lines.append(f"  track_number: {track_id}")
        out_lines.append(f"  name: \"{t.get('name', '')}\"")
        out_lines.append(f"  range: \"{t.get('range', '')}\"")
        out_lines.append(f"  description: \"{t.get('description', '')}\"")
        out_lines.append(f"  tier: core")
        out_lines.append(f"  level: 1")
        out_lines.append(f"  seam: \"math foundations\"")

        # Modules
        modules = t.get("modules", [])
        out_lines.append(f"  modules:")
        if isinstance(modules, list):
            for m in modules:
                if isinstance(m, dict):
                    out_lines.append(f"    - module: {m.get('n')}")
                    out_lines.append(f"      title: \"{m.get('title', '')}\"")
                    out_lines.append(f"      focus: \"{m.get('focus', '')}\"")

        out_lines.append(f"  cross_references:")
        if track_id in (1, 2):
            out_lines.append(f"    - {{ entity: phases, phase_id: phase-2, role: \"Phase 2 weeks 7-18\" }}")
        elif track_id == 3:
            out_lines.append(f"    - {{ entity: phases, phase_id: phase-3, role: \"Phase 3 weeks 19-30\" }}")
        out_lines.append("")

    (SCHEMA / "math.yaml").write_text("\n".join(out_lines), encoding="utf-8")
    print(f"math.yaml: wrote {len(tracks)} tracks")


# ============================================================================
# Build interview.yaml
# ============================================================================

def build_interview() -> None:
    text = (SRC / "interview.ts").read_text()

    carl_stories = parse_ts_array(text, "CARL_STORIES")
    weekly_minimums = parse_ts_array(text, "WEEKLY_MINIMUMS")
    interview_focus = parse_ts_array(text, "INTERVIEW_FOCUS")
    roadmap_tracks = parse_ts_array(text, "ROADMAP_TRACKS")
    capstone_reqs = parse_ts_array(text, "CAPSTONE_REQUIREMENTS")
    completion_levels = parse_ts_array(text, "COMPLETION_LEVELS")

    out_lines = [
        "# Interview preparation: continuous track, CARL stories, 176-item roadmap.",
        "# Per T1.2: schema discipline. Runs parallel to the 108-week spine.",
        "",
    ]

    # CARL stories (10)
    out_lines.extend([
        "# ============================================================================",
        "# CARL behavioral stories (10)",
        "# ============================================================================",
        "",
    ])
    for s in carl_stories:
        out_lines.append(f"- id: carl-{s.get('story', '').lower().replace(' ', '-')}")
        out_lines.append(f"  story: \"{s.get('story', '')}\"")
        out_lines.append(f"  weeks: \"{s.get('weeks', '')}\"")
        out_lines.append(f"  tier: core")
        out_lines.append(f"  level: 2")
        out_lines.append(f"  seam: \"behavioral interview prep\"")
        out_lines.append("")

    # Weekly minimums (scalar list)
    if weekly_minimums:
        out_lines.extend([
            "",
            "# ============================================================================",
            "# Weekly interview prep minimums",
            "# ============================================================================",
            "",
            "- id: interview-weekly-minimums",
            "  tier: core",
            "  level: 1",
            "  seam: \"weekly cadence\"",
            "  rules:",
        ])
        for w in weekly_minimums:
            if isinstance(w, str):
                out_lines.append(f"    - \"{w}\"")
        out_lines.append("")

    # Interview focus (8 phase-ranges)
    out_lines.extend([
        "",
        "# ============================================================================",
        "# Interview focus by phase",
        "# ============================================================================",
        "",
    ])
    for f in interview_focus:
        out_lines.append(f"- id: interview-focus-{f.get('weeks', '').replace(' ', '').replace('-', 'to').lower()}")
        out_lines.append(f"  weeks: \"{f.get('weeks', '')}\"")
        out_lines.append(f"  focus: \"{f.get('focus', '')}\"")
        out_lines.append(f"  tier: core")
        out_lines.append(f"  level: 2")
        out_lines.append(f"  seam: \"phase-aligned interview prep\"")
        out_lines.append("")

    # Roadmap tracks (3)
    out_lines.extend([
        "",
        "# ============================================================================",
        "# 176-item interview roadmap (3 tracks)",
        "# ============================================================================",
        "",
    ])
    for r in roadmap_tracks:
        items = r.get("items", [])
        out_lines.append(f"- id: roadmap-track-{r.get('name', '').lower().replace(' ', '-')}")
        out_lines.append(f"  name: \"{r.get('name', '')}\"")
        out_lines.append(f"  count: {len(items) if isinstance(items, list) else 0}")
        out_lines.append(f"  tier: core")
        out_lines.append(f"  level: 2")
        out_lines.append(f"  seam: \"interview prep roadmap\"")
        if isinstance(items, list):
            out_lines.append(f"  items:")
            for item in items:
                if isinstance(item, dict):
                    out_lines.append(f"    - step: \"{item.get('step', '')}\"")
                    out_lines.append(f"      item: \"{item.get('item', '')}\"")
                    out_lines.append(f"      type: \"{item.get('type', '')}\"")
                    out_lines.append(f"      completion: \"{item.get('completion', '')}\"")
        out_lines.append("")

    # Capstone requirements (7)
    out_lines.extend([
        "",
        "# ============================================================================",
        "# Final capstone requirements (7 dimensions)",
        "# ============================================================================",
        "",
    ])
    for c in capstone_reqs:
        out_lines.append(f"- id: capstone-req-{c.get('area', '').lower().replace(' ', '-')}")
        out_lines.append(f"  area: \"{c.get('area', '')}\"")
        out_lines.append(f"  requirement: \"{c.get('requirement', '')}\"")
        out_lines.append(f"  tier: core")
        out_lines.append(f"  level: 3")
        out_lines.append(f"  seam: \"capstone completion\"")
        out_lines.append("")

    # Completion levels (4)
    out_lines.extend([
        "",
        "# ============================================================================",
        "# Completion levels (4 tiers, including optional Auror)",
        "# ============================================================================",
        "",
    ])
    for c in completion_levels:
        out_lines.append(f"- id: completion-level-{c.get('level', '').lower().replace(' ', '-').replace('(', '').replace(')', '')}")
        out_lines.append(f"  level: \"{c.get('level', '')}\"")
        out_lines.append(f"  requires: \"{c.get('requires', '')}\"")
        out_lines.append(f"  tier: core")
        out_lines.append(f"  level_note: \"3\"")
        out_lines.append(f"  seam: \"graduation\"")
        out_lines.append("")

    (SCHEMA / "interview.yaml").write_text("\n".join(out_lines), encoding="utf-8")
    print(f"interview.yaml: wrote {len(carl_stories)} CARL + {len(weekly_minimums)} minimums + {len(interview_focus)} focus + {len(roadmap_tracks)} tracks + {len(capstone_reqs)} reqs + {len(completion_levels)} levels")


# ============================================================================
# Build prerequisites.yaml
# ============================================================================

def build_prerequisites() -> None:
    text = (SRC / "prerequisites.ts").read_text()
    raw_resources = parse_ts_array(text, "PREREQUISITE_RESOURCES")
    raw_plan = parse_ts_array(text, "PREREQUISITE_36_WEEKS")

    out_lines = [
        "# Prerequisite on-ramp: optional 36-week lane for learners without",
        "# engineering/comfort foundations. Per T1.2: schema discipline.",
        "",
        "# ============================================================================",
        "# Prerequisite resources (9)",
        "# ============================================================================",
        "",
    ]
    for r in raw_resources:
        out_lines.append(f"- id: prereq-{r.get('title', '').lower().replace(' ', '-').replace('(', '').replace(')', '').replace(',', '')[:50]}")
        out_lines.append(f"  title: \"{r.get('title', '')}\"")
        out_lines.append(f"  url: \"{r.get('url', '')}\"")
        out_lines.append(f"  focus: \"{r.get('focus', '')}\"")
        out_lines.append(f"  weeks: \"{r.get('weeks', '')}\"")
        out_lines.append(f"  outcome: \"{r.get('outcome', '')}\"")
        out_lines.append(f"  tier: optional")
        out_lines.append(f"  level: 1")
        out_lines.append(f"  seam: \"on-ramp\"")
        out_lines.append("")

    out_lines.extend([
        "",
        "# ============================================================================",
        "# 36-week budget plan (8 phases)",
        "# ============================================================================",
        "",
    ])
    for p in raw_plan:
        out_lines.append(f"- id: prereq-plan-{p.get('weeks', '').replace(' ', '').replace('-', 'to').lower()}")
        out_lines.append(f"  weeks: \"{p.get('weeks', '')}\"")
        out_lines.append(f"  title: \"{p.get('title', '')}\"")
        out_lines.append(f"  resources: \"{p.get('resources', '')}\"")
        out_lines.append(f"  outcome: \"{p.get('outcome', '')}\"")
        out_lines.append(f"  tier: optional")
        out_lines.append(f"  level: 1")
        out_lines.append(f"  seam: \"on-ramp phase\"")
        out_lines.append("")

    (SCHEMA / "prerequisites.yaml").write_text("\n".join(out_lines), encoding="utf-8")
    print(f"prerequisites.yaml: wrote {len(raw_resources)} resources + {len(raw_plan)} plan phases")


# ============================================================================
# Build agents.yaml
# ============================================================================

def build_agents() -> None:
    """Build agents.yaml from src/data/agents.ts (746 lines).

    The agents file is the largest. We focus on the structured entries:
    AGENT_MODULES, AGENT_BRIDGES, BRIDGE_SUMMARY, MANUS_CAPSTONE.
    Other top-level arrays (theme strings, sections) are skipped.
    """
    text = (SRC / "agents.ts").read_text()

    agent_modules = parse_ts_array(text, "AGENT_MODULES")
    if not agent_modules:
        print("agents.yaml: no AGENT_MODULES parsed, skipping")
        return

    out_lines = [
        "# GenAI Agents curriculum: 18 modules + Module 7.5 (MCP) + Manus capstone.",
        "# Per T1.2: schema discipline. Maps onto Phase 7 (LLM training + RAG + agents).",
        "",
        "# ============================================================================",
        "# Agent modules (18 + 1 MCP)",
        "# ============================================================================",
        "",
    ]
    for m in agent_modules:
        mid = m.get("id", "")
        out_lines.append(f"- id: agent-module-{mid}")
        out_lines.append(f"  module_id: \"{mid}\"")
        out_lines.append(f"  title: \"{m.get('title', '')}\"")
        theme = m.get("theme", "")
        if theme:
            out_lines.append(f"  theme: \"{theme}\"")
        topics = m.get("topics", [])
        out_lines.append(f"  topics:")
        if isinstance(topics, list):
            for t in topics:
                out_lines.append(f"    - \"{t}\"")
        outcomes = m.get("outcomes", [])
        if isinstance(outcomes, list) and outcomes:
            out_lines.append(f"  outcomes:")
            for o in outcomes:
                out_lines.append(f"    - \"{o}\"")
        out_lines.append(f"  tier: core")
        out_lines.append(f"  level: 2")
        out_lines.append(f"  seam: \"GenAI agents\"")
        out_lines.append(f"  cross_references:")
        out_lines.append(f"    - {{ entity: phases, phase_id: phase-7, role: \"LLM training + RAG + agents\" }}")
        if mid == "7":
            out_lines.append(f"    - {{ project: manus, role: \"feeds Project Manus\" }}")
        out_lines.append("")

    # MANUS_CAPSTONE (scalar entry)
    # Find it in the source
    manus_match = re.search(
        r"export const MANUS_CAPSTONE = \{(.*?)\};",
        text,
        re.DOTALL,
    )
    if manus_match:
        # Parse the manus object via parse_object_text (simplified)
        manus_text = manus_match.group(1)
        # Just extract key fields with regex
        def extract_field(pattern):
            m = re.search(pattern, manus_text, re.DOTALL)
            return m.group(1).strip() if m else ""

        out_lines.extend([
            "",
            "# ============================================================================",
            "# Project Manus capstone",
            "# ============================================================================",
            "",
            "- id: project-manus",
            "  title: \"Project Manus - Agentic UI Automation\"",
            "  vision: >",
            f"    {extract_field(r'vision:\\s*\\n\\s*\\\"(.+?)\\\"')}",
            "  architecture:",
        ])
        arch_items = re.findall(r"-\\s*\\\"([^\\\"]+)\\\"", extract_field(r"architecture:\\s*\\[(.*?)\\]"))
        for item in arch_items:
            out_lines.append(f"    - \"{item}\"")
        out_lines.append("  features:")
        feat_items = re.findall(r"-\\s*\\\"([^\\\"]+)\\\"", extract_field(r"features:\\s*\\[(.*?)\\]"))
        for item in feat_items:
            out_lines.append(f"    - \"{item}\"")
        out_lines.append("  challenges:")
        ch_items = re.findall(r"-\\s*\\\"([^\\\"]+)\\\"", extract_field(r"challenges:\\s*\\[(.*?)\\]"))
        for item in ch_items:
            out_lines.append(f"    - \"{item}\"")
        out_lines.append(f"  tier: core")
        out_lines.append(f"  level: 3")
        out_lines.append(f"  seam: \"agent capstone\"")

    (SCHEMA / "agents.yaml").write_text("\n".join(out_lines), encoding="utf-8")
    print(f"agents.yaml: wrote {len(agent_modules)} modules + Project Manus")


# ============================================================================
# Main
# ============================================================================

def main() -> int:
    builders = [
        ("mandalas", build_mandalas),
        ("engineering", build_engineering),
        ("system_design", build_system_design),
        ("math", build_math),
        ("interview", build_interview),
        ("prerequisites", build_prerequisites),
        ("agents", build_agents),
    ]
    for name, fn in builders:
        try:
            fn()
        except Exception as e:
            print(f"  ✗ {name}: {e}")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
