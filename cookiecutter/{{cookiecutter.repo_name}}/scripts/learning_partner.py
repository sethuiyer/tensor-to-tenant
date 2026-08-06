"""Learning partner CLI -- talk to OpenRouter with course-aware context.

Subcommands:
    ask     -- open-ended question (socratic mode by default)
    quiz    -- recall drill driven by RPG memory DB (FADING/LOST targets)
    review  -- walk the current week's journal entry
    plan    -- propose a 4-week arc from current mandala + next gate
    debug   -- minimal-hint diagnostic helper

The system prompt is the content of AGENTS.md. The CLI assembles user
context from the journal + RPG state + docs and sends it all to OpenRouter.

Default model: deepseek/deepseek-v4-flash-20260731 (configurable).
Default base: https://openrouter.ai/api/v1.

Run from the repo root:
    python scripts/learning_partner.py ask "Why does SVD perturbation need rank?"
    python scripts/learning_partner.py quiz --week 14
    python scripts/learning_partner.py review
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Iterable, Optional


# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------
DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "deepseek/deepseek-v4-flash-20260731"
LOG_DIR = Path("partner_log")
LOG_MAX_BYTES = 8 * 1024  # keep conversation threads bounded

AGENTS_FILE = Path("AGENTS.md")
JOURNAL_DIR = Path("journal/weeks")
CHARACTER_FILE = Path("journal/character.json")
MEMORY_FILE = Path("journal/memory.json")
README = Path("README.md")

WEEK_RE = re.compile(r"week_(\d{1,3})\.md")
START_DATE_RE = re.compile(r"Start date\*\*:\s*(\d{4}-\d{2}-\d{2})")

# AGENTS.md is prose, so references are deliberately limited to unambiguous
# ``Week 14``/``Weeks 70-81`` and ``Gate 7`` forms.  Placeholders such as
# ``week_NNN`` and generic words such as "weekly" are not references.  The
# parser also accepts the canonical schema IDs (``week-014``/``gate-7``).
_WEEK_REFERENCE_RE = re.compile(
    r"(?<![A-Za-z0-9])"
    r"(?P<label>weeks?|w)"
    r"(?:\s*[_-]?\s*)"
    r"(?P<start>\d{1,3})"
    r"(?:\s*(?P<range>to|through|[-–—])\s*(?P<end>\d{1,3}))?"
    r"(?!\d)",
    re.IGNORECASE,
)
_GATE_REFERENCE_RE = re.compile(
    r"(?<![A-Za-z0-9])"
    r"(?P<label>gates?|g)"
    r"(?:\s*[_-]?\s*)"
    r"(?P<start>\d{1,2})"
    r"(?:\s*(?P<range>to|through|[-–—])\s*(?P<end>\d{1,2}))?"
    r"(?!\d)",
    re.IGNORECASE,
)


class PartnerPromptValidationError(ValueError):
    """Raised when AGENTS.md points at a missing schema week or gate."""


# More discoverable aliases for callers that do not know the implementation's
# historical name.  Keep the exception specific so build and cookiecutter
# errors can be caught without swallowing unrelated failures.
PromptReferenceError = PartnerPromptValidationError


def _reference_numbers(
    match: re.Match[str], *, kind: str, text: str
) -> list[int]:
    """Expand one week/gate match into normalized integer IDs.

    A range is expanded rather than checking just its endpoints: a schema
    missing a week in the middle of ``Weeks 10-12`` must fail too.  Reversed
    ranges are malformed prompt references and get a useful source error.
    """
    start = int(match.group("start"))
    end_raw = match.group("end")
    if end_raw is None:
        return [start]
    end = int(end_raw)
    if end < start:
        line = text.count("\n", 0, match.start()) + 1
        raise PartnerPromptValidationError(
            f"AGENTS.md line {line}: invalid {kind} range {match.group(0)!r} "
            f"(range end {end} is before start {start})"
        )
    # The schema is intentionally small (108 weeks, ten gates); refuse an
    # accidental enormous range instead of allocating unboundedly on bad prose.
    if end - start > 1000:
        line = text.count("\n", 0, match.start()) + 1
        raise PartnerPromptValidationError(
            f"AGENTS.md line {line}: {kind} range {match.group(0)!r} is too large"
        )
    return list(range(start, end + 1))


def _collect_prompt_references(
    text: str,
) -> tuple[dict[int, list[int]], dict[str, list[int]]]:
    """Return referenced week numbers and canonical gate IDs with line numbers."""
    weeks: dict[int, list[int]] = {}
    gates: dict[str, list[int]] = {}
    for match in _WEEK_REFERENCE_RE.finditer(text):
        for number in _reference_numbers(match, kind="week", text=text):
            line = text.count("\n", 0, match.start()) + 1
            weeks.setdefault(number, []).append(line)
    for match in _GATE_REFERENCE_RE.finditer(text):
        for number in _reference_numbers(match, kind="gate", text=text):
            line = text.count("\n", 0, match.start()) + 1
            gates.setdefault(f"gate-{number}", []).append(line)
    return weeks, gates


def extract_prompt_references(text: str) -> dict[str, set[Any]]:
    """Extract normalized references from an AGENTS.md prompt.

    The returned mapping has integer week numbers and canonical gate IDs, for
    example ``{"weeks": {14}, "gates": {"gate-7"}}``.  It is intentionally
    independent of the schema so callers can validate source templates and
    generated projects with the same parser.
    """
    weeks, gates = _collect_prompt_references(text)
    return {"weeks": set(weeks), "gates": set(gates)}


# ``extract_agents_references`` is the name used by the build helper and is
# kept as a small public alias for scripts that read naturally.
extract_agents_references = extract_prompt_references


def _normalize_week_id(value: Any) -> int:
    if isinstance(value, bool):
        raise ValueError(f"invalid schema week ID {value!r}")
    if isinstance(value, int):
        return value
    raw = str(value).strip().lower()
    match = re.fullmatch(r"(?:week[-_ ]?)?(\d{1,3})", raw)
    if not match:
        raise ValueError(f"invalid schema week ID {value!r}")
    return int(match.group(1))


def _normalize_gate_id(value: Any) -> str:
    if isinstance(value, bool):
        raise ValueError(f"invalid schema gate ID {value!r}")
    raw = str(value).strip().lower()
    match = re.fullmatch(r"(?:gate[-_ ]?)?(\d{1,2})", raw)
    if not match:
        raise ValueError(f"invalid schema gate ID {value!r}")
    return f"gate-{int(match.group(1))}"


def validate_agents_references(
    text: str,
    week_ids: Iterable[Any],
    gate_ids: Iterable[Any],
    *,
    source: str | Path = "AGENTS.md",
) -> None:
    """Assert all numbered AGENTS.md references exist in schema IDs.

    ``week_ids`` and ``gate_ids`` are explicit inputs so this function remains
    stdlib-only in the learner repo (which does not ship the source YAML).
    Build tooling passes IDs loaded from ``schema/weeks.yaml`` and
    ``schema/gates.yaml``; the post-generation hook passes the generated
    adapter's constants.  Errors include the prompt path, line, missing ID,
    and a compact view of the schema's known IDs.
    """
    if not isinstance(text, str):
        raise TypeError("AGENTS.md prompt must be text")
    try:
        valid_weeks = {_normalize_week_id(value) for value in week_ids}
        valid_gates = {_normalize_gate_id(value) for value in gate_ids}
    except (TypeError, ValueError) as error:
        raise PartnerPromptValidationError(
            f"invalid schema IDs while validating {source}: {error}"
        ) from error

    referenced_weeks, referenced_gates = _collect_prompt_references(text)
    missing_weeks = sorted(set(referenced_weeks) - valid_weeks)
    missing_gates = sorted(set(referenced_gates) - valid_gates)
    if not missing_weeks and not missing_gates:
        return

    source_name = str(source)
    details: list[str] = []
    if missing_weeks:
        week_details = ", ".join(
            f"week-{number:03d} (line {referenced_weeks[number][0]})"
            for number in missing_weeks
        )
        known = _format_known_numbers(valid_weeks, prefix="week")
        details.append(f"unknown week reference(s): {week_details}; known: {known}")
    if missing_gates:
        gate_details = ", ".join(
            f"{gate_id} (line {referenced_gates[gate_id][0]})"
            for gate_id in missing_gates
        )
        known = _format_known_numbers(
            {int(gate.removeprefix("gate-")) for gate in valid_gates},
            prefix="gate",
        )
        details.append(f"unknown gate reference(s): {gate_details}; known: {known}")
    raise PartnerPromptValidationError(f"{source_name}: " + "; ".join(details))


def _format_known_numbers(numbers: set[int], *, prefix: str) -> str:
    """Format known schema IDs compactly while retaining clear diagnostics."""
    if not numbers:
        return "<none>"
    ordered = sorted(numbers)
    if prefix == "week" and ordered == list(range(1, 109)):
        return "week-001..week-108"
    if prefix == "gate" and ordered == list(range(1, 11)):
        return "gate-1..gate-10"
    return ", ".join(
        f"{prefix}-{number:03d}" if prefix == "week" else f"{prefix}-{number}"
        for number in ordered
    )


# Alias used by a few callers/tests; the behavior and error type are identical.
validate_prompt_references = validate_agents_references


def _now() -> dt.date:
    return dt.date.today()


def _read_start_date() -> Optional[dt.date]:
    if not README.exists():
        return None
    m = START_DATE_RE.search(README.read_text(encoding="utf-8"))
    return dt.date.fromisoformat(m.group(1)) if m else None


def _current_week(today: dt.date | None = None) -> int:
    today = today or _now()
    start = _read_start_date()
    if not start:
        return 1
    return max(1, min(108, ((today - start).days // 7) + 1))


# --------------------------------------------------------------------------
# Context assembly
# --------------------------------------------------------------------------
def _load_agents_prompt() -> str:
    if not AGENTS_FILE.exists():
        return "You are a learning partner for Tensor-to-Tenant."
    text = AGENTS_FILE.read_text(encoding="utf-8")
    # Trim the AGENTS.md so it's not absurdly large in the system prompt.
    if len(text) > 12_000:
        text = text[:12_000] + "\n\n... [truncated for brevity] ..."
    return text


def _read_journal(week: int) -> Optional[str]:
    path = JOURNAL_DIR / f"week_{week:03d}.md"
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def _read_rpg_state() -> dict[str, Any]:
    out: dict[str, Any] = {}
    if CHARACTER_FILE.exists():
        try:
            out["character"] = json.loads(
                CHARACTER_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            out["character"] = {"error": "character.json malformed"}
    if MEMORY_FILE.exists():
        try:
            mem = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
            counts: dict[str, int] = {"FRESH": 0, "SETTLING": 0, "WANING": 0,
                                      "FADING": 0, "LOST": 0, "UNSEEN": 0,
                                      "total": 0}
            # Imported lazily to keep partner CLI runnable even without the
            # character module depending on this one.
            from forgetting import retention, tier_for_retention
            today = _now()
            for c in mem.get("concepts", {}).values():
                if c.get("last_seen") is None:
                    counts["UNSEEN"] += 1
                else:
                    days = (today - dt.date.fromisoformat(c["last_seen"])).days
                    r = retention(c["stability"], days)
                    counts[tier_for_retention(r)] += 1
                counts["total"] += 1
            out["concept_tiers"] = counts
            # Pick up the top-3 most-at-risk concepts.
            from battle import eligible_for
            fading = eligible_for(mem, today, tier="WANING")[:3]
            out["fading"] = [
                {"name": c["name"], "week": c.get("week"), "id": c["id"]}
                for c, _ in fading
            ]
        except json.JSONDecodeError:
            out["memory"] = {"error": "memory.json malformed"}
    return out


def _assemble_user_context(args: argparse.Namespace) -> str:
    """Build the user-side context block (everything besides AGENTS.md)."""
    week = getattr(args, "week", None) or _current_week()
    parts: list[str] = []
    parts.append(f"# Current week: {week} of 108")

    journal = _read_journal(week)
    if journal:
        parts.append(f"\n## This week's journal (week_{week:03d}.md)\n")
        parts.append(journal)
    else:
        parts.append(f"\n(week_{week:03d}.md not yet generated)")

    prev = _read_journal(week - 1)
    if prev:
        parts.append(f"\n## Prior week (week_{week-1:03d}.md)\n")
        parts.append(prev)

    if getattr(args, "with_rpg", False):
        rpg = _read_rpg_state()
        if rpg:
            parts.append("\n## RPG character layer\n```json")
            parts.append(json.dumps(rpg, indent=2)[:4_000])
            parts.append("```")

    if getattr(args, "topic", None):
        topic = args.topic.lower()
        hits = []
        for f in sorted(JOURNAL_DIR.glob("week_*.md")):
            text = f.read_text(encoding="utf-8")
            if topic in text.lower():
                wk = int(WEEK_RE.search(f.name).group(1))
                hits.append((wk, f"week_{wk:03d}.md"))
            if len(hits) >= 5:
                break
        if hits:
            parts.append("\n## Related weeks by topic match\n")
            for wk, name in hits:
                parts.append(f"- {name}")

    return "\n".join(parts)


# --------------------------------------------------------------------------
# OpenRouter call -- urllib only, no extra dependencies.
# --------------------------------------------------------------------------
def _redact_secrets(text: str) -> str:
    """Defensive: catch obvious API keys pasted in user prompts."""
    text = re.sub(r"sk-or-[A-Za-z0-9_-]{20,}", "[REDACTED-OPENROUTER-KEY]", text)
    text = re.sub(r"sk-[A-Za-z0-9]{20,}", "[REDACTED-OPENAI-KEY]", text)
    return text


def _call_openrouter(messages: list[dict[str, str]],
                     model: str, base_url: str,
                     temperature: float = 0.4,
                     timeout: float = 60.0) -> str:
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        print(__doc_setup_hint())
        sys.exit(2)

    url = base_url.rstrip("/") + "/chat/completions"
    body = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 1200,
    }).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/tensor-to-tenant",
            "X-Title": "Tensor-to-Tenant learning partner",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")[:400]
        raise SystemExit(
            f"OpenRouter returned {e.code}: {detail}"
        )
    except urllib.error.URLError as e:
        raise SystemExit(f"Network error contacting OpenRouter: {e.reason}")

    try:
        return payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise SystemExit(
            "Unexpected response shape from OpenRouter: "
            + json.dumps(payload)[:400]
        )


def __doc_setup_hint() -> str:
    return (
        "OPENROUTER_API_KEY is not set.\n"
        "  1. Sign up at https://openrouter.ai\n"
        "  2. Create an API key\n"
        "  3. export OPENROUTER_API_KEY=sk-or-v1-...\n"
        "  4. Override OPENROUTER_MODEL to swap the default:\n"
        f"       export OPENROUTER_MODEL=\"{DEFAULT_MODEL}\"\n"
        "     or any other OpenRouter catalog id."
    )


# --------------------------------------------------------------------------
# Mode handlers
# --------------------------------------------------------------------------
def _mode_ask(args: argparse.Namespace) -> int:
    system = _load_agents_prompt()
    context = _assemble_user_context(args)
    user_q = " ".join(args.prompt) if isinstance(args.prompt, list) else args.prompt
    user_q = _redact_secrets(user_q)
    messages = [
        {"role": "system", "content": system},
        {"role": "user",
         "content": f"## Learner question\n\n{user_q}\n\n## Context\n{context}"},
    ]
    answer = _call_openrouter(messages, args.model, args.base_url,
                              temperature=args.temperature)
    print(answer)
    _maybe_append_log(_thread_path(args), "ask", user_q, answer)
    return 0


def _mode_quiz(args: argparse.Namespace) -> int:
    system = _load_agents_prompt()
    context = _assemble_user_context(args)
    rpg = _read_rpg_state()
    rpg_block = json.dumps(rpg, indent=2) if rpg else "(no RPG state)"
    instr = (
        "Generate 3-5 recall questions.\n"
        "- Prefer concepts at FADING or LOST in the RPG memory DB if present.\n"
        "- For each question, cite the course week, the concept ID from the\n"
        "  memory DB, and what evidence file would prove mastery.\n"
        "- DO NOT provide the answers. Reserve them in a fenced block at the\n"
        "  END labeled `[answers hidden -- reveal after attempt]`.\n"
        "- Keep it short -- a partner that returns essays is failing the role.\n"
    )
    user_block = (
        f"## Mode: quiz\n{instr}\n\n"
        f"## Context\n{context}\n\n"
        f"## RPG state\n```json\n{rpg_block[:4000]}\n```"
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_block},
    ]
    answer = _call_openrouter(messages, args.model, args.base_url,
                              temperature=0.6)
    print(answer)
    return 0


def _mode_review(args: argparse.Namespace) -> int:
    system = _load_agents_prompt()
    context = _assemble_user_context(args)
    instr = (
        "Walk this week's journal with the learner.\n"
        "- Identify which checkboxes are still unchecked.\n"
        "- Identify missing evidence (code, benchmark, design doc, retro).\n"
        "- If the Sailboat retro is empty, prompt them to fill it instead of\n"
        "  continuing the review.\n"
        "- End with a single concrete next-step adjustment.\n"
        "- DO NOT rewrite the journal for them. Comment on it.\n"
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"## Mode: review\n{instr}\n\n{context}"},
    ]
    answer = _call_openrouter(messages, args.model, args.base_url,
                              temperature=0.2)
    print(answer)
    return 0


def _mode_plan(args: argparse.Namespace) -> int:
    system = _load_agents_prompt()
    today = _now()
    week = _current_week(today)
    context = _assemble_user_context(args)
    instr = (
        f"Plan the next 4 weeks from week {week}.\n"
        "- Anchor on the next milestone gate (look it up from the README).\n"
        "- Surface the open evidence gaps from the prior 2 weeks.\n"
        "- Each week needs ONE core deliverable and ONE optional depth lane.\n"
        "- Include one Algorithmic Forge drill per week (Core tier).\n"
        "- Recommend one Leetcode Darbar problem per week for vocabulary.\n"
        "- Cap the plan at ~15 hrs/week of work. If the gate is looming, name\n"
        "  the gate explicitly and reduce optional lane.\n"
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"## Mode: plan\n{instr}\n\n{context}"},
    ]
    answer = _call_openrouter(messages, args.model, args.base_url,
                              temperature=0.4)
    print(answer)
    return 0


def _mode_debug(args: argparse.Namespace) -> int:
    system = _load_agents_prompt()
    context = _assemble_user_context(args)
    user_q = " ".join(args.prompt) if isinstance(args.prompt, list) else args.prompt
    instr = (
        "Help debug. Behavior:\n"
        "- Ask, don't tell. One diagnostic question at a time.\n"
        "- Suggest the smallest possible next test the learner can run.\n"
        "- Resist the urge to refactor or rewrite their code.\n"
        "- If the learner asks for 'the answer', redirect to the relevant\n"
        "  course week and ask which step of that week's drill is failing.\n"
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"## Mode: debug\n{instr}\n\n"
                                    f"## Question\n{user_q}\n\n{context}"},
    ]
    answer = _call_openrouter(messages, args.model, args.base_url,
                              temperature=0.3)
    print(answer)
    return 0


# --------------------------------------------------------------------------
# Optional log thread (so `ask` and `debug` can accumulate across calls)
# --------------------------------------------------------------------------
def _thread_path(args: argparse.Namespace) -> Optional[Path]:
    thread = getattr(args, "thread", None)
    if not thread:
        return None
    p = Path(thread)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def _maybe_append_log(path: Optional[Path], mode: str, q: str, a: str) -> None:
    if not path:
        return
    ts = dt.datetime.now().isoformat(timespec="seconds")
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"\n\n## {mode} -- {ts}\n\n")
        handle.write(f"**Q:** {q}\n\n**A:** {a}\n")


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(
        description=("Tensor-to-Tenant learning partner -- OpenRouter-backed "
                     "socratic helper."),
    )
    parser.add_argument("--model", default=os.environ.get(
        "OPENROUTER_MODEL", DEFAULT_MODEL
    ), help=f"OpenRouter model id (default: {DEFAULT_MODEL})")
    parser.add_argument("--base-url", default=os.environ.get(
        "OPENROUTER_BASE_URL", DEFAULT_BASE_URL
    ), help=f"OpenRouter base URL (default: {DEFAULT_BASE_URL})")
    parser.add_argument("--temperature", type=float, default=None,
                        help="Override temperature (mode-specific otherwise)")
    parser.add_argument("--week", type=int, default=None,
                        help="Override the week context (default: current)")
    parser.add_argument("--topic", default=None,
                        help="Grep journals for this topic string")
    parser.add_argument("--with-rpg", action="store_true",
                        help="Include RPG character + memory state in context")
    parser.add_argument("--thread", default=None,
                        help="Append this exchange to a thread file")

    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ask = sub.add_parser("ask", help="Open-ended socratic question")
    p_ask.add_argument("prompt", nargs="+", help="Learner question")
    p_ask.set_defaults(func=_mode_ask, temperature=0.4)

    p_quiz = sub.add_parser("quiz",
                            help="Generate 3-5 recall questions")
    p_quiz.set_defaults(func=_mode_quiz, temperature=0.6)

    p_review = sub.add_parser("review",
                              help="Walk this week's journal")
    p_review.set_defaults(func=_mode_review, temperature=0.2)

    p_plan = sub.add_parser("plan",
                            help="Plan the next 4 weeks")
    p_plan.set_defaults(func=_mode_plan, temperature=0.4)

    p_debug = sub.add_parser("debug", help="Minimal-hint diagnostic mode")
    p_debug.add_argument("prompt", nargs="+", help="What's going wrong")
    p_debug.set_defaults(func=_mode_debug, temperature=0.3)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
