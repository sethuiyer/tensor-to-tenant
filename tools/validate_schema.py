"""Validate canonical YAML entities without mutating generated outputs."""
from __future__ import annotations

import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import generate  # noqa: E402


def main() -> int:
    try:
        generate._validate_curriculum_schema()
        # Loading every registered YAML file catches malformed syntax even for
        # entities whose renderer is intentionally compatibility-backed.
        for path in sorted(generate.SCHEMA_DIR.glob("*.yaml")):
            generate._load_yaml(path)
    except Exception as error:  # CLI boundary: turn validation into a clear red build.
        print(f"validate_schema.py: error: {error}", file=sys.stderr)
        return 1
    print("validate_schema.py: schema is valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
