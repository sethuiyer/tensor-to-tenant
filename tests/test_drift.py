"""T1.6 structural schema/site drift checks."""
from __future__ import annotations

import importlib.util
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_SPEC = importlib.util.spec_from_file_location("drift_report", _ROOT / "tools/drift_report.py")
_MOD = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(_MOD)


def test_curriculum_schema_and_site_have_no_structural_drift() -> None:
    assert _MOD.collect_drift() == []
