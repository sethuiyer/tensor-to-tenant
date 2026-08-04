"""Open a GenAI agents track module scaffold.

Run from the repo root:
    python scripts/agents.py --module 7.5
    python scripts/agents.py --module 18

Each module scaffolds into 09_interview/agents/module_<slug>.md. The full
track lives in docs/agents_track.md; the bridge to the main arc lives in
docs/bridge.md.
"""

from __future__ import annotations

import argparse
from pathlib import Path

MODULES = {
    "1": "Exploring the Generative AI Universe",
    "2": "AI Agent Prototyping (No-Code Introduction)",
    "3": "Coding Essentials for AI Programming",
    "4": "Introduction to LangChain",
    "5": "Prompt Engineering Essentials",
    "6": "RAG Systems Essentials",
    "7": "Building AI Agents from Scratch & Graph-RAG",
    "7.5": "Model Context Protocol (MCP)",
    "8": "Implementing ReAct Agents with LangChain",
    "9": "Building Agents with LangGraph",
    "10": "Building Agents with AutoGen",
    "11": "Building Agents with CrewAI",
    "12": "Agentic AI Design Patterns",
    "13": "Advanced LangGraph Agents",
    "14": "Advanced AutoGen Agents",
    "15": "Advanced CrewAI Agents",
    "16": "Agentic RAG using LangGraph",
    "17": "Stanford DSPy",
    "18": "K\u00f9zu Deep Dive",
}


def module_slug(mid: str) -> str:
    """Map a module id to a zero-padded folder slug: '7.5' -> '07_5'."""
    if "." in mid:
        whole, frac = mid.split(".", 1)
        return "{0:02d}_{1}".format(int(whole), frac)
    return "{0:02d}".format(int(mid))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--module", type=str, required=True)
    args = parser.parse_args()

    if args.module not in MODULES:
        parser.error(
            "--module must be one of: {0}".format(
                ", ".join(sorted(MODULES, key=lambda s: (s.count("."), float(s))))
            )
        )

    title = MODULES[args.module]
    slug = module_slug(args.module)
    destination = Path("09_interview/agents") / f"module_{slug}.md"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if not destination.exists():
        destination.write_text(
            f"""# Module {args.module}: {title}

## Topics

- <topic 1>
- <topic 2>
- <topic 3>

## Evidence

- Implementation / lab artifact:
- Written explanation:
- Retrospective:
""",
            encoding="utf-8",
        )
    print(f"Prepared GenAI agents module scaffold: {destination}")


if __name__ == "__main__":
    main()
