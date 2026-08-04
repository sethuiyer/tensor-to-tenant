"""Pre-generation hook: validate inputs and fail fast with a clear message.

Cookiecutter calls this before rendering any templates. If we exit non-zero,
the whole generation aborts.
"""

from __future__ import annotations

import datetime as dt
import re
import sys


def fail(msg: str) -> None:
    sys.stderr.write(f"\n[cookiecutter-tensor-to-tenant] {msg}\n\n")
    sys.exit(1)


def main() -> None:
    # ---- student_name ------------------------------------------------------
    student_name = "{{ cookiecutter.student_name }}"
    if not student_name or not student_name.strip():
        fail("`student_name` cannot be empty.")
    if len(student_name) > 80:
        fail("`student_name` is unreasonably long (max 80 chars).")

    # ---- github_username ---------------------------------------------------
    gh = "{{ cookiecutter.github_username }}"
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38}[A-Za-z0-9])?", gh or ""):
        fail(
            "`github_username` must be a valid GitHub handle "
            "(alphanumeric and hyphens, 1-40 chars, no leading/trailing hyphen)."
        )

    # ---- start_date --------------------------------------------------------
    raw = "{{ cookiecutter.start_date }}"
    try:
        start = dt.date.fromisoformat(raw)
    except ValueError:
        fail(
            f"`start_date` must be ISO format YYYY-MM-DD (got {raw!r}). "
            "Pick the Monday of Week 1."
        )

    # Course expects Mon-Sun weeks. Pin to a Monday.
    if start.weekday() != 0:
        shifted = start + dt.timedelta(days=(7 - start.weekday()) % 7)
        sys.stderr.write(
            f"\n[cookiecutter-tensor-to-tenant] Note: start_date {start} is a "
            f"{start.strftime('%A')}; shifting to the next Monday ({shifted}). "
            "Re-run with --no-input or pass an explicit Monday if you prefer.\n"
        )

    # ---- python_version ----------------------------------------------------
    py = "{{ cookiecutter.python_version }}"
    if not re.fullmatch(r"3\.(?:1[0-9]|9|[8-9])", py or ""):
        fail(f"`python_version` must be 3.8-3.19 (got {py!r}).")

    # ---- repo_name ---------------------------------------------------------
    repo = "{{ cookiecutter.repo_name }}"
    if not re.fullmatch(r"[A-Za-z0-9._-]+", repo or ""):
        fail("`repo_name` may only contain letters, digits, `.`, `_`, `-`.")

    # All good -- fall through, Cookiecutter will render templates.
    sys.stdout.write("[cookiecutter-tensor-to-tenant] inputs valid.\n")


if __name__ == "__main__":
    main()