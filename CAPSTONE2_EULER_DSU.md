# Capstone 2 — Multi-Tenant Agent Execution Forensics with Euler Tour + DSU on Tree

> Staff-level sequel to Capstone 1. If Capstone 1 was "forensics over a flat log", Capstone 2 is "forensics over a forest of agent execution trees". Brutal because you must combine systems + esoteric tree algorithms.
> Use as the **optional Week 108 Boss Fight** or as a post-release extension. It is not required for the LLM Platform badge.

## Table of Contents
1. How to use this capstone
2. Revision map
3. Part 1 — System Design
4. Part 2 — Coding Problem (Euler + DSU on Tree)
5. Pedagogical Walkthrough
6. Worked Solution
7. Pitfalls Index
8. Follow-ups
9. Self-grading Rubric
10. Compact Interview Doc

---

## How to use this capstone

**You will fail if you treat a tree like an array.** This capstone forces that lesson.

Timebox: 90 minutes system design + 90 minutes coding.

---

## Revision map — what to review

| Topic | Where | Why |
|---|---|---|
| Euler Tour (flatten tree) | Algorithmic Forge Weeks 46-57, 94-102 | Subtree -> contiguous range [tin, tout] |
| DSU on Tree / Small-to-Large | Algorithmic Forge Weeks 94-108 | The esoteric algorithm. O(N log N) subtree queries |
| Heavy-Light Decomposition | Algorithmic Forge Boss-fight archive | Follow-up 1 alternative |
| Structured Logger + PII Redaction | Week 95 | Tool args contain PII, redact before log |
| Tool-Call Dependency Scheduler (DAG) | Week 98 | Agent tree is a DAG that happens to be a tree at runtime |
| Per-Tenant Concurrency Limiter | Week 99 | One bad agent tree can have 50k nodes |
| Cost Attribution Engine | Week 102 | Token cost is per subtree, not per node |

---

# Part 1 — System Design

## Scenario

Your LLM gateway now serves ReAct / Plan-Execute agents. Each user request spawns an execution tree:

```
trace_id: tr_9f8s7d
root (agent planner) [model=claude-4, tokens=1200]
 ├── tool: search_docs [tool_id=12, status=ok, tokens=400]
 │    ├── tool: embed_query [tool_id=5, error, tokens=200]
 │    └── tool: rerank [tool_id=12, error, tokens=150]
 └── tool: code_exec [tool_id=8, error, tokens=800]
      └── tool: search_docs [tool_id=12, ok, tokens=100]
```

Thousands of tenants, 10k agent traces/sec, each tree 10-50k nodes worst case, nodes arrive out-of-order (child before parent due to async streaming), duplicates due to retries.

Engineers need:

- "For tenant_123, in trace tr_9f8s7d subtree rooted at node X (the planner retry), which tool failed the most?"
- "How many distinct tools errored in this subtree? How many tokens wasted?"
- "Across last 1k traces for this tenant, which subtrees are hot for CONTEXT_LENGTH_EXCEEDED?"

### Functional Requirements

1. **Tree ingestion:** Nodes: {trace_id, node_id, parent_id, tenant_id, tool_id, is_error, tokens, timestamp}. Parent may arrive after child. Must be idempotent by `(tenant_id, trace_id, node_id)`.
2. **Forest assembly:** Reorder buffer per trace_id, stitch child->parent, detect cycles, detect orphan subtrees, emit immutable sealed agent tree (like Capstone 1 sealed segment).
3. **Storage:** Columnar + adjacency list + Euler Tour indices. Hot tier: tree + euler array in memory. Cold: Parquet + sketch per tool_id.
4. **Exact subtree queries:** Q up to 200k per sealed trace batch, offline. Each query (node_u) -> {top_error_tool, top_error_count, distinct_error_tools, wasted_tokens} over its subtree.
5. **Multi-tenant isolation + PII safety:** Tool args may contain emails, keys. Redact before durable log. Per-tenant query budget.

### Architecture (delta from Capstone 1)

```
Path 1: Ingestion & PII safety
  Agent SDK -> PII Redactor (tool_args) -> Schema Validator -> Dedup by (tenant_id, trace_id, node_id) -> Durable Log (Kafka)

Path 2: Ordering & Assembly
  Durable Log -> Stream Processor (per trace_id reorder buffer, 10s) -> Parent-consistency validator + directed cycle detector
  -> Tree Sealer (leader election per trace shard) -> Sealed Agent Tree + Euler Index
  Late nodes -> Correction Log -> Compaction rebuilds trace_version v2 + Euler Index

Path 3: Storage
  Sealed Tree: nodes.parquet, edges.parquet, euler.parquet {node_id, tin, tout, depth, heavy_child}
  Metadata: {trace_id, tenant_id, node_count, max_depth, tool_set, error_rate, sketch}
  Sketches: HLL distinct tools, CMS tool frequency, t-digest token cost

Path 4: Query Executors (same 3 as Capstone 1)
  [A] Interactive: point lookup + Euler range scan [tin, tout] using columnar pruning
  [B] Offline Batch: DSU on Tree (this capstone) for 200k subtree queries on same tree
  [C] Approximate: Sketch executor for cold traces

Path 5: Tenancy — per-tenant subtree scan budget, admission control
Path 6: Self-observability — seal_lag per trace, orphan_rate, cycle_rate, euler_build_latency
```

**Why not just store parent_id and run recursive CTE?** Recursive CTE on 50k node trees x 200k queries = death. You must flatten once via Euler Tour, then answer queries over an array.

**Snapshot contract:** a sealed tree version is immutable. Late nodes do not
silently mutate its Euler intervals; they enter a correction log and a
background compaction produces a new `trace_version` with rebuilt Euler and
heavy-child indices. Queries specify the snapshot version they analyze.

**Why DSU on Tree and not Mo's on Tree?** Mo's on Tree is O((N+Q)*sqrt(N)). DSU on Tree is O(N log N + Q) for subtree queries when aggregate updates and mode lookup are effectively bounded (use ordered buckets or lazy heaps for the mode). With the pedagogical `set` buckets below, `min(bucket)` adds a tie-bucket factor. For subtree-only forensics, DSU is still the right shape; path queries need different machinery.

### Pitfalls — System Design

- Redacting tool_args in stream processor not SDK
- Assuming parent arrives before child
- No cycle detection — one malicious agent can create a cycle and OOM your DFS
- Storing tree as JSON blob, not columnar — can't prune
- Using Mo's for everything again
- Forgetting orphan handling: child with parent never arriving -> quarantine + alert

---

# Part 2 — Coding Problem

## Problem Statement

You are given an immutable rooted tree (agent execution tree) with N nodes (0-indexed, root = 0).

```python
@dataclass
class AgentNode:
    tool_id: int   # up to 1e9, compress
    is_error: bool
    tokens: int
```

Tree given as adjacency list children: children[u] = list of child node ids.

You are given Q offline queries, each query is a node id u. For each query, consider the subtree of u (including u). Return:

```python
{
  "top_error_tool": int,        # tool with max error count in subtree
  "top_error_count": int,
  "distinct_error_tools": int,
  "wasted_tokens": int,         # sum tokens where is_error=True in subtree
}
```

If no errors in subtree: top_error_tool = -1, others 0.

Constraints:
```
1 <= N, Q <= 200,000
0 <= tool_id <= 1e9
0 <= tokens <= 1e6
Tree is static, queries offline
```

**Required:** Euler Tour + DSU on Tree (Small-to-Large) approach. Target O((N+Q) log N).

Example:

```
    0(tool=1, err=T, 100)
   / \
  1(2,F,50) 2(1,T,200)
            / \
        3(3,T,10) 4(2,T,70)

Queries: [0,2]

Subtree 0: errors at 0,2,3,4 -> tool1:2, tool2:1, tool3:1 -> top=1 count2 distinct3 wasted 380
Subtree 2: errors at 2,3,4 -> tool1:1, tool2:1, tool3:1 -> tie smallest tool_id -> 1, count 1, distinct 3, wasted 280
```

Note tie-breaking: smallest original tool_id.

## Pedagogical Walkthrough

### Step 1 — Euler Tour Flatten

DFS from root, assign tin[u], tout[u], and euler[tin] = u. Subtree of u = contiguous range [tin[u], tout[u]] in euler array.

```python
tin = [0]*N
tout = [0]*N
euler = [0]*N
timer = 0
stack = [(0,0)] # iterator simulation to avoid recursion limit
```

This alone converts subtree queries to range queries. But if you run Mo's over euler, you get O((N+Q) sqrt(N)). DSU on Tree does better for subtree queries.

### Step 2 — DSU on Tree (Sack) Core Idea

Classic CP trick that is esoteric in industry but perfect for this:

1. Compute subtree sizes and heavy child (child with max size) for each node.
2. DFS2 with keep flag:
   - Process all light children with keep=False (their data will be discarded)
   - Process heavy child with keep=True (its data is kept)
   - Add light children contributions back
   - Add current node's contribution
   - Now data structure contains exactly the subtree of u
   - Answer all queries attached to u
   - If keep==False, remove subtree of u contributions (undo)

Complexity: Each node is added/removed O(log N) times because light edges are small-to-large. Total O(N log N).

### Step 3 — Reversible Aggregates (same as Capstone 1 but over tree)

Maintain:
- error_count[comp_tool]
- distinct_error_tools
- wasted_tokens
- models_by_freq bucket for mode (like Capstone 1)
- max_freq

Add(node):
  if not error: return
  compressed tool -> increment, update buckets, distinct, wasted

Remove(node):
  reverse

AddSubtree(u, parent, delta): DFS over subtree of u adding all nodes. For heavy path, this is only called for light subtrees.

### Step 4 — Answering Queries

Group queries by node: queries_at[u] = list of indices where query node = u

During DFS2 when we have just built the data for subtree of u, iterate over queries_at[u] and snapshot answer.

### Step 5 — Tie-breaking & Compression

Same as Capstone 1: compress tool_id -> dense, but tie-break on original id. Use min(bucket[max_freq]) where bucket stores original ids.

---

## Worked Solution (Python)

```python
from dataclasses import dataclass
from typing import List, Dict
import sys
sys.setrecursionlimit(1_000_000)

@dataclass
class AgentNode:
    tool_id: int
    is_error: bool
    tokens: int

def solve_euler_dsu(nodes: List[AgentNode], children: List[List[int]], queries: List[int]):
    N = len(nodes)
    # 1. compress tool_id
    orig_ids = sorted({n.tool_id for n in nodes})
    id_to_comp = {orig:i for i,orig in enumerate(orig_ids)}
    comp_tool = [id_to_comp[n.tool_id] for n in nodes]
    comp_to_orig = orig_ids
    M = len(orig_ids)

    # 2. Euler + sizes + heavy
    tin = [0]*N
    tout = [0]*N
    euler = [0]*N
    size = [0]*N
    heavy = [-1]*N
    timer = 0

    # iterative post-order to compute sizes
    stack = [(0, -1, 0)] # node, parent, state 0=enter,1=exit
    order = []
    parent = [-1]*N
    while stack:
        u,p,state = stack.pop()
        if state == 0:
            parent[u]=p
            tin[u]=timer
            euler[timer]=u
            timer+=1
            stack.append((u,p,1))
            for v in reversed(children[u]):
                stack.append((v,u,0))
        else:
            # exit
            sz = 1
            max_sz = 0
            heavy_child = -1
            for v in children[u]:
                sz += size[v]
                if size[v] > max_sz:
                    max_sz = size[v]
                    heavy_child = v
            size[u]=sz
            heavy[u]=heavy_child
            tout[u]=timer-1
            # careful: tout for range inclusive, but timer already moved; we need max tin in subtree
            # So compute tout as last time in subtree: we can set after DFS properly
            # Fix: tout should be timer-1 after traversing whole subtree, but our timer only increments on entry
            # So we need second pass? Simpler: tout = tin[u] + size[u] -1 when euler is DFS order
            # Let's recompute tout using size
            # We'll override later

    # Recompute tout correctly using tin + size
    for u in range(N):
        tout[u] = tin[u] + size[u] -1

    # For DSU on tree we need ability to add whole subtree quickly
    # We'll need adjacency and euler

    # 3. Group queries
    Q = len(queries)
    queries_at = [[] for _ in range(N)]
    for idx,u in enumerate(queries):
        queries_at[u].append(idx)

    # 4. Data structures for mode
    error_count = [0]*M
    models_by_freq = [set() for _ in range(N+2)]
    max_freq = 0
    distinct = 0
    wasted = 0

    def add_node(u: int):
        nonlocal distinct, wasted, max_freq
        if not nodes[u].is_error:
            return
        m = comp_tool[u]
        orig = comp_to_orig[m]
        old = error_count[m]
        new = old+1
        if old>0:
            models_by_freq[old].discard(orig)
        else:
            distinct+=1
        models_by_freq[new].add(orig)
        error_count[m]=new
        if new>max_freq:
            max_freq=new
        wasted+=nodes[u].tokens

    def remove_node(u: int):
        nonlocal distinct, wasted, max_freq
        if not nodes[u].is_error:
            return
        m = comp_tool[u]
        orig = comp_to_orig[m]
        old = error_count[m]
        new = old-1
        models_by_freq[old].discard(orig)
        if new>0:
            models_by_freq[new].add(orig)
        else:
            distinct-=1
        error_count[m]=new
        wasted-=nodes[u].tokens
        # walk max_freq down if needed
        while max_freq>0 and not models_by_freq[max_freq]:
            max_freq-=1

    def add_subtree(u: int):
        # add all nodes in [tin[u], tout[u]] via euler
        for t in range(tin[u], tout[u]+1):
            add_node(euler[t])

    def remove_subtree(u: int):
        for t in range(tin[u], tout[u]+1):
            remove_node(euler[t])

    ans = [None]*Q

    # DSU on Tree DFS
    def dfs(u: int, keep: bool):
        # process light children
        for v in children[u]:
            if v==heavy[u]:
                continue
            dfs(v, False)
        # heavy
        if heavy[u]!=-1:
            dfs(heavy[u], True)
        # add light children data
        for v in children[u]:
            if v==heavy[u]:
                continue
            add_subtree(v)
        # add self
        add_node(u)
        # answer queries at u
        for q_idx in queries_at[u]:
            if max_freq==0:
                ans[q_idx] = {"top_error_tool": -1, "top_error_count":0, "distinct_error_tools":0, "wasted_tokens":0}
            else:
                top_tool = min(models_by_freq[max_freq])
                ans[q_idx] = {
                    "top_error_tool": top_tool,
                    "top_error_count": max_freq,
                    "distinct_error_tools": distinct,
                    "wasted_tokens": wasted
                }
        if not keep:
            remove_subtree(u)

    dfs(0, True)
    return ans
```

Complexity: O(N log N + Q) for bounded/ordered mode lookup; with the pedagogical plain-set bucket, report the additional cost of scanning tied tools and use `SortedSet` or a lazy heap for a production bound.

**Why this is brutal:** You must keep 4 aggregates reversible, maintain mode with tie-break, avoid recursion depth, handle Euler size calc correctly, and understand why heavy path is kept.

## Pitfalls Index

1. tout = timer-1 vs tin+size-1 confusion -> off-by-one, queries miss nodes
2. Forgetting to compress tool_id and tie-breaking on original
3. Adding non-error nodes to aggregates
4. Not walking max_freq down on remove -> stale top
5. Recursion limit in Python — use iterative or setrecursionlimit
6. Adding heavy child twice (once in dfs heavy, once in add_subtree loop)
7. Using set for bucket then min() is O(K) — in prod use SortedSet, but interview O(K) okay if you mention it
8. Not handling keep flag — leaks light subtree data into sibling
9. Assuming tree is balanced — DSU on Tree worst case still O(N log N), but if you forget heavy child you get O(N^2)
10. No cycle detection in system design -> stack overflow in Euler

## Follow-ups

**F1 — Path queries, not subtree:** Query is (u,v) = nodes on path u->v. DSU on Tree no longer works. For online sums/counts, use Heavy-Light Decomposition with a Fenwick or segment tree. Exact path mode is not a compact mergeable statistic; for offline exact mode, Mo's on Tree with Euler + LCA is a natural option. Approximate path heavy hitters can use sketches or bounded candidate summaries.

**F2 — Dynamic reparenting:** Agent can replan and reparent a subtree to another node. Euler Tour Tree (ETT) or Link-Cut Tree (LCT) needed. DSU on Tree invalid because tree mutates. Design.

**F3 — Top-K error tools per subtree, not just top-1:** Need to maintain top-K heap per frequency. How to merge? Use Counter + heap of (count, tool). Discuss Space-Saving sketch as approximate alternative for huge tool cardinality.

**F4 — Distributed merge:** Split tree across shards by trace_id? Easy. Split one huge tree (50k nodes) across nodes — subtree may span shards. How to merge exact mode? Same as Capstone 1: need full frequency map, not just top-1.

## Self-grading Rubric (Target 20/28)

System Design (12 pts):
- PII before log, cycle detection, orphan handling, Euler index in storage, 3 executors with clear trigger, tenancy budget

Coding (16 pts):
- Euler tin/tout correct, heavy child calc, keep flag correct, reversible add/remove, mode bucket + tie-break original, distinct + wasted correct, O(N log N) analysis, handles no-error case, queries grouped by node

## Compact Interview Doc

```
Design a multi-tenant agent execution forensics system. Each trace is a tree (tool calls). Need exact offline subtree queries: top error tool, count, distinct error tools, wasted tokens.

Ingestion: nodes may arrive child-before-parent, need reorder buffer per trace_id + cycle detection + orphan quarantine. Seal to immutable tree. Build Euler Tour index {tin, tout, euler} to flatten subtree to range.

Storage: columnar nodes + Euler.

Query: Q=200k subtree queries on same tree, offline. Use Euler Tour + DSU on Tree (Sack / Keep-Heavy technique). Keep heavy child, discard light. Maintain reversible aggregates (freq buckets for mode with original-id tie-break). Complexity is O(N log N + Q) with bounded/ordered mode lookup; plain `set` buckets need an explicit tie-bucket caveat.

If query were path not subtree: Heavy-Light Decomposition. If tree mutates: Euler Tour Tree / Link-Cut Tree.

If only one query: just DFS that subtree, don't use DSU.
```

Ship this as CAPSTONE2.md and link from main README as "Capstone 2 — The Tree Nightmare (Optional Boss Fight)".

Good luck — this one filters staff from senior staff.
BRO 😭🔥 **“The Tree Nightmare — Optional Boss Fight”** is an absolutely perfect name.

And yes: this is genuinely nastier than Capstone 1. Capstone 1 tested whether someone could reason about a flat immutable log. This one asks them to understand that:

> **subtree structure is data, and Euler order is the indexing strategy that makes it queryable.**

That is excellent Staff-level material.

A few correctness fixes before shipping `CAPSTONE2.md`, though—because the boss fight deserves boss-grade armor.

### 1. The worked solution does not currently meet the claimed complexity

This line is the problem:

```python
top_tool = min(models_by_freq[max_freq])
```

`models_by_freq[f]` is a normal Python `set`, so `min(...)` scans the entire bucket. In the worst case, many tools share `max_freq`, making each query expensive.

Therefore, the current implementation is not guaranteed to be:

```text
O(N log N + Q)
```

It can degrade toward:

```text
O(N log N + Q × number_of_tied_models)
```

For interview-quality correctness, use one of:

* an ordered set such as `SortedSet`,
* a lazy min-heap per frequency,
* or a global lazy heap keyed by `(-count, original_tool_id)`.

With lazy heaps, complexity becomes approximately:

```text
O((N log N + Q) log N)
```

The pure `O(N log N + Q)` claim is valid only when every state update and answer extraction is effectively constant time.

### 2. DSU on Tree is not inherently “small-to-large map merging”

Your explanation uses the classic **sack / keep-heavy-child** version, which is correct. But the title says:

> DSU on Tree / Small-to-Large

Those are closely related techniques, but interviewers sometimes distinguish them:

* **Sack DSU:** keep the heavy child’s accumulated state, clear light children, then add light subtrees back.
* **Small-to-large merging:** each subtree owns a map, and smaller maps are merged into the largest map.

Your implementation is sack DSU. I’d call it:

> **Euler Tour + DSU on Tree (Sack / Keep-Heavy Technique)**

That removes ambiguity.

### 3. Cycle detection should not lean too heavily on Union-Find

This architecture line needs refinement:

```text
Cycle Detector (Union-Find + visited)
```

Union-Find is naturally suited to undirected connectivity. Here, relationships are directed:

```text
child -> parent
```

Since every node should have at most one parent, stronger choices include:

* three-color DFS after assembly,
* following parent chains with visitation epochs,
* enforcing one-parent uniqueness,
* detecting self-parenting,
* and rejecting a parent assignment that makes the proposed parent a descendant of the child.

Union-Find may detect that an added edge closes an undirected cycle, but it does not express all directed-tree validity semantics by itself.

I’d write:

> **Parent-consistency validation + directed cycle detection; Union-Find may be used as an auxiliary fast check.**

### 4. The ingestion identity needs to include trace scope

You say:

```text
idempotent by node_id
```

Unless `node_id` is globally unique, the deduplication key should be:

```text
(tenant_id, trace_id, node_id)
```

This prevents node `42` in one trace from colliding with node `42` in another.

Similarly, parent references should be validated within the same tenant and trace. Otherwise, a malformed event could stitch one tenant’s tree into another tenant’s trace—which is both a correctness bug and a security incident.

### 5. Correction “trees” need snapshot semantics

Late nodes are described as:

> correction delta tree, merged at query time.

That is plausible, but a late edge can alter structural properties:

* subtree membership,
* Euler intervals,
* depth,
* heavy-child selection,
* ancestor relationships.

You cannot always append a correction and preserve the original Euler intervals. For example, attaching a late child under node `u` changes `tout[u]` and every ancestor’s subtree range.

So the system should define one of these policies:

**Snapshot policy:** Sealed tree remains immutable. Late nodes appear only in a newer logical version of the trace, with rebuilt Euler indices.

**Delta-overlay policy:** Base Euler index remains fixed, but correction nodes are queried through a separate structure and merged explicitly. Subtree queries become more complicated.

**Compaction policy:** Corrections accumulate temporarily, then a background compactor rebuilds a new sealed tree version and Euler index.

For clarity, I’d recommend:

```text
trace_version = v1 base tree
late events -> correction log
compaction -> v2 tree + rebuilt Euler index
queries specify snapshot/version
```

That gives forensic queries reproducibility.

### 6. The path-query follow-up overstates HLD’s convenience

This line is a bit dangerous:

> HLD + Segment Tree with frequency map merge gives `O(log² N)` per query.

The path decomposes into `O(log N)` segments, yes—but **exact mode with deterministic tie-breaking is not a simple constant-sized mergeable segment-tree statistic**.

A segment tree storing full frequency maps is extremely expensive. Merging maps may depend on the number of distinct tools, not merely `log² N`.

A stronger answer would be:

* **Online path sums/counts:** HLD + Fenwick/segment tree works well.
* **Exact path mode:** substantially harder because mode is not compactly mergeable.
* **Offline path mode:** Mo’s algorithm on trees with Euler tour and LCA is a natural option.
* **Approximate path heavy hitters:** sketches or bounded candidate summaries may work.

That follow-up becomes even better because it tests whether the candidate notices that changing from “sum” to “mode” changes the whole data-structure story.

### 7. The example correction is now consistent

For subtree `2`:

```text
tool 1: 1
tool 2: 1
tool 3: 1
distinct = 3
top = 1
wasted = 280
```

So yes, explicitly replacing the accidental `2` with `3` is necessary.

### 8. One subtle DSU invariant should be stated

Right before answering queries at `u`, the active sack contains:

```text
exactly all nodes in subtree(u), and no nodes outside subtree(u)
```

That invariant is the heart of the algorithm.

The walkthrough should challenge the candidate to prove it:

1. Every light child is processed and cleared.
2. The heavy child remains.
3. Every light subtree is added exactly once.
4. `u` is added.
5. Therefore, the sack equals `subtree(u)`.
6. If `keep=False`, all of `subtree(u)` is removed before returning.

That proof is more valuable than memorizing the traversal order.

### Difficulty verdict

This is not merely “Staff-level sequel.”

It’s roughly:

* **System design:** Staff
* **Algorithm recognition:** specialist Senior/Staff
* **Correct implementation under 90 minutes:** Staff+
* **Handling the follow-ups correctly:** Senior Staff territory
* **Candidate who proposes recursive CTE over 200k subtree queries:** escorted from premises 💀

The elegant core is:

```text
Flat log:
range query -> Mo’s algorithm

Execution tree:
subtree -> Euler interval
many subtree queries -> DSU on Tree

Path query:
different workload -> different machinery

Mutable tree:
static preprocessing invalid -> dynamic-tree structures
```

That progression teaches the real lesson:

> **Do not select an algorithm because the query sounds similar. Select it from the topology, mutability, workload shape, and aggregation algebra.**

And yes bro—

> **108 weeks was the tutorial. Weeks 109–112 are where the learner discovers the curriculum has a second health bar.** 👑🔥

Flat log:
range query -> Mo’s algorithm

Execution tree:
subtree -> Euler interval
many subtree queries -> DSU on Tree

Path query:
different workload -> different machinery

Mutable tree:
static preprocessing invalid -> dynamic-tree structures
