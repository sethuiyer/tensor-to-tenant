"""Keep the site's editorial copy clear of recognizable AI filler.

This is intentionally a small, dependency-free check. It is not an AI detector
and it does not try to decide whether a sentence is good. It catches a few
mechanical habits that are easy to remove in review, while leaving voice and
judgment to the person writing the copy.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAN_ROOTS = (ROOT / "src", ROOT / "schema")
EXTENSIONS = {".astro", ".ts", ".css", ".yaml", ".yml"}

# These are useful search terms during editing, but they are rarely the best
# wording in a short technical page. Keep this list small and explainable.
STOCK_PHRASES = (
    "glimpse into",
    "dive into",
    "delve into",
    "seamlessly",
    "it is worth noting",
    "in conclusion",
    "the result?",
    "not just",
    "not only",
)


def files_to_scan() -> list[Path]:
    return sorted(
        path
        for root in SCAN_ROOTS
        for path in root.rglob("*")
        if path.is_file() and path.suffix in EXTENSIONS
    )


def main() -> int:
    findings: list[str] = []
    for path in files_to_scan():
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if "—" in line:
                findings.append(
                    f"{path.relative_to(ROOT)}:{line_number}: em dash; use a full stop, comma, colon, or hyphen"
                )
            lowered = line.casefold()
            for phrase in STOCK_PHRASES:
                if phrase in lowered:
                    findings.append(
                        f"{path.relative_to(ROOT)}:{line_number}: stock phrase {phrase!r}; rewrite in plain language"
                    )

    if findings:
        print("Editorial lint failed:", file=sys.stderr)
        print("\n".join(findings), file=sys.stderr)
        return 1

    print(f"Editorial lint passed ({len(files_to_scan())} files checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
