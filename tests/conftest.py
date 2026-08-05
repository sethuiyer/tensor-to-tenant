"""Pytest configuration for the tensor-to-tenant generator test harness.

The cookiecutter scripts live inside a Jinja template path
(`cookiecutter/{{cookiecutter.repo_name}}/scripts/`), so they cannot be
imported via the package name. This conftest adds the cookiecutter
scripts directory to sys.path so tests can `from forgetting import ...`
directly without copying or vendoring the source.

When the schema migration (TASKS.md T1.2 – T1.3) lands, the generator
scripts will move out of the cookiecutter tree into a proper `tools/`
package. This conftest is the bridge until that happens.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Repo root: tests/conftest.py -> tests/ -> repo root.
_REPO_ROOT = Path(__file__).resolve().parent.parent

# The cookiecutter generator's scripts directory, where forgetting.py
# and friends live before the schema migration extracts them.
_COOKIECUTTER_SCRIPTS = (
    _REPO_ROOT / "cookiecutter" / "{{cookiecutter.repo_name}}" / "scripts"
)

if _COOKIECUTTER_SCRIPTS.exists() and str(_COOKIECUTTER_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_COOKIECUTTER_SCRIPTS))
