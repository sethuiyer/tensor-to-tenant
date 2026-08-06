"""Focused tests for schema-driven agent bridge generation."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parent.parent
_SPEC = importlib.util.spec_from_file_location("generate", ROOT / "tools" / "generate.py")
assert _SPEC is not None and _SPEC.loader is not None
_GENERATE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_GENERATE)


def _agent_rows() -> list[dict]:
    return _GENERATE._records(_GENERATE._load_yaml(ROOT / "schema" / "agents.yaml"))


def test_new_agent_and_bridge_rows_reach_site_and_cookiecutter() -> None:
    """A schema-only module addition must not depend on snapshot rows."""
    rows = _agent_rows()
    rows.extend(
        [
            {
                "id": "agent-module-99",
                "module_id": "99",
                "title": "Synthetic Agent",
                "topics": ["Build a synthetic agent"],
            },
            {
                "id": "agent-bridge-99",
                "module": "99",
                "title": "Synthetic Agent",
                "gap": "The synthetic bridge explains the implementation gap.",
                "rows": [
                    {"concept": "Concept 1", "weeks": "Week 1", "insight": "Insight 1"},
                    {"concept": "Concept 2", "weeks": "Week 2", "insight": "Insight 2"},
                    {"concept": "Concept 3", "weeks": "Week 3", "insight": "Insight 3"},
                    {"concept": "Concept 4", "weeks": "Week 4", "insight": "Insight 4"},
                ],
            },
        ]
    )

    effective = copy.deepcopy(_GENERATE._source_data())
    _GENERATE._apply_agent_schema_overrides(effective, rows)
    cookie = _GENERATE._load_yaml(ROOT / "schema" / "cookiecutter.yaml")
    hook_values = _GENERATE._hook_values(effective, cookie)

    assert effective["agents"]["AGENT_MODULES"][-1]["id"] == "99"
    bridge = effective["agents"]["AGENT_BRIDGES"][-1]
    assert bridge["module"] == "99"
    assert len(bridge["rows"]) == 4

    site_view = _GENERATE._render_module(ROOT / "src" / "data" / "agents.ts", effective["agents"])
    cookie_view = _GENERATE._render_hook_module(hook_values)
    assert "Synthetic Agent" in site_view
    assert "Concept 4" in site_view
    assert "AGENT_BRIDGE_CC" in cookie_view
    assert "Concept 4" in cookie_view


def test_bridge_summary_and_pitch_are_schema_overrides() -> None:
    rows = _agent_rows()
    for row in rows:
        if row["id"] == "bridge-summary-module-1":
            row["weeks"] = "Week 999 (synthetic test)"
        elif row["id"] == "bridge-pitch":
            row["quote"] = "Synthetic quote"
            row["tag"] = "Synthetic tag"

    effective = copy.deepcopy(_GENERATE._source_data())
    _GENERATE._apply_agent_schema_overrides(effective, rows)

    summary = next(item for item in effective["agents"]["BRIDGE_SUMMARY"] if item["module"] == "Module 1")
    assert summary["weeks"] == "Week 999 (synthetic test)"
    assert effective["agents"]["BRIDGE_PITCH"] == {"quote": "Synthetic quote", "tag": "Synthetic tag"}

    hook_values = _GENERATE._hook_values(
        effective, _GENERATE._load_yaml(ROOT / "schema" / "cookiecutter.yaml")
    )
    assert ("Module 1", "Week 999 (synthetic test)") in hook_values["BRIDGE_SUMMARY_CC"]
    assert hook_values["BRIDGE_PITCH_QUOTE"] == "Synthetic quote"
    assert hook_values["BRIDGE_PITCH_TAG"] == "Synthetic tag"


def test_bridge_reference_must_name_an_agent_module() -> None:
    rows = _agent_rows()
    rows.append(
        {
            "id": "agent-bridge-missing",
            "module": "does-not-exist",
            "title": "Broken bridge",
            "gap": "broken",
            "rows": [{"concept": "c", "weeks": "Week 1", "insight": "i"}],
        }
    )

    with pytest.raises(_GENERATE.GenerationError, match="unknown module"):
        _GENERATE._validate_agents_schema(rows, ROOT / "schema" / "agents.yaml")
