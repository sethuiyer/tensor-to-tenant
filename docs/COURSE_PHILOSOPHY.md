# Course philosophy

> The landing README is optimized for starting. This document preserves the
> deeper argument for why the apprenticeship is shaped this way.

## Course Goal

Train into a production-oriented AI/software engineer who can:

1. Build and evaluate ML/LLM systems.
2. Understand LLM inference, RAG, agents, and serving infrastructure.
3. Implement production-grade backend and distributed-system patterns.
4. Pass system design, coding, ML, and behavioral interviews.
5. Produce a portfolio of reproducible projects, benchmarks, and design docs.

## Target Audience

This is not for the "I want to learn AI in 30 days to get a remote job" crowd. This is for the mid-level Software Engineer or Data Scientist who has 2-3 years of experience, possesses deep intellectual curiosity, and wants to become a Principal/Staff AI Systems Architect.

## Why this course

The market has plenty of specialists. It has far fewer engineers who can move
vertically from numerical reasoning to production AI platform judgment.

This apprenticeship is designed to produce a **production-minded Staff AI
Systems Engineer with algorithmic depth**—someone who can connect the math, the
algorithms, the ML lifecycle, the model stack, and the operational platform.

### The scarcity is in the seams

Many engineers are strong in one lane but have never crossed the boundary into
the next one:

- Can solve Leetcode problems, but would send raw emails into Kafka before durable logging.
- Can build a RAG demo, but treats HNSW as magic and cannot explain Recall@K by query slice.
- Can discuss PagedAttention, but has never built a per-tenant concurrency limiter with leader election.
- Knows transformers, but cannot diagnose why a logistic-regression baseline is miscalibrated.

Tensor-to-Tenant makes those seams the curriculum. The point is not to collect
topic badges; it is to repeatedly carry an idea from first principles into a
system with workload constraints, failure modes, evidence, and trade-offs.

### Why the market doesn't produce this person

Because companies have silos for a reason. At any real company:

- Research team owns Weeks 7 to 30 and 70 to 74
- Retrieval team owns 31 to 39 and 75 to 78
- Inference team owns 82 to 93
- Platform team owns 94 to 102

They literally sit on different floors and use different Slack channels.
Tensor-to-Tenant compresses two job hops, three team transfers, and years of
accidental exposure into one deliberate apprenticeship.

### The vertical capability ladder

| Layer | Graduate capability |
|---|---|
| **Math** | Recognize when an SVD is unstable, inspect the condition number, and choose a numerically defensible approach. |
| **Algorithms** | Move quickly through the 548 Darbar patterns, then go deep on flows, suffix structures, Euler tours, and DSU on Tree when the workload requires it. |
| **ML** | Frame the problem, catch leakage, run bootstrap confidence intervals, and evaluate slices rather than celebrating one aggregate metric. |
| **LLM systems** | Build and critique SFT, LoRA, DPO, GRPO, RAG, agents, memory, evaluation, and guardrails—with an understanding of where each breaks. |
| **Inference** | Read a roofline plot, identify memory-bound behavior, explain PagedAttention, judge when speculative decoding helps, and model serving economics. |
| **Platform** | Ship routing, quotas, tracing, idempotency, work queues, registries, tenant isolation, and cost attribution—the Week 102 platform is working evidence, not slides. |
| **Staff judgment** | Write design docs, challenge assumptions, choose exact versus approximate guarantees from workload shape, and defend trade-offs in review. |

The intended outcome is a straight line from `vector.dot()` to a per-tenant
concurrency limiter with leader election. Mathematics informs the algorithm;
the algorithm informs the primitive; the primitive informs the distributed
design; the design becomes a reliable AI platform.

### What this prepares someone to do

Strong graduates can target roles such as:

- Staff AI Engineer
- Staff ML Systems Engineer
- AI Infrastructure or LLM Platform Engineer
- Retrieval/Search Engineer
- Inference Performance Engineer
- Production ML Platform Engineer

The differentiator is not that the graduate has “seen” all these subjects. It
is that the portfolio shows they can **explain, implement, benchmark, operate,
and defend** the resulting systems.

What this course can provide is Staff-level technical breadth, reasoning, and
portfolio evidence. When the graduate enters that environment, they spend less
time discovering basic production failure modes and more time exercising
judgment, influence, and ownership.

---

## Read the structured outcomes

- [10-phase curriculum](https://sethuiyer.github.io/tensor-to-tenant/curriculum/)
- [Stackable releases and blocking gates](https://sethuiyer.github.io/tensor-to-tenant/gates/)
- [Full resource and interview views](https://sethuiyer.github.io/tensor-to-tenant/resources/)
