# Agent-building bootcamp bridge

> **Not a merge — a bridge.** This is the conceptual explanation preserved from
> the former README. The module-by-module mapping is structured in
> [`../schema/agents.yaml`](../schema/agents.yaml), rendered at the
> [agents page](https://sethuiyer.github.io/tensor-to-tenant/agents/), and
> emitted into generated learner-repo `docs/bridge.md`.

The agent-building bootcamp teaches builders to ship. Tensor-to-Tenant explains
why those builders hit production ceilings: throughput, deadlocks, degenerate
optimization, retrieval quality, inference economics, and tenancy. The two
surfaces are one ladder, not one merged course.

> Do Modules 1–18 plus the Manus capstone as a focused agent-building sprint.
> When a RAG pipeline breaks at scale, an AutoGen crew deadlocks, or a DSPy
> optimizer converges to garbage, return to the corresponding Tensor-to-Tenant
> week and build the primitive, evaluation harness, or platform control that
> explains the failure.

## How to use the bridge

1. Start with the agent module you need to ship.
2. Follow its mapped Tensor-to-Tenant weeks for the underlying math, primitive,
   system-design seam, and production failure mode.
3. Keep the agent artifact, the supporting evidence, and the failure analysis
   together in the learner repo.
4. Return to the core week and gate; the bridge is depth, not a second spine.

## Canonical mapping surfaces

- [Agents module browser](https://sethuiyer.github.io/tensor-to-tenant/agents/)
- [`schema/agents.yaml`](../schema/agents.yaml)
- [`cookiecutter/README.md`](../cookiecutter/README.md)
- Generated learner bridge: `docs/bridge.md` in the repository emitted by [`../cookiecutter/README.md`](../cookiecutter/README.md)
