# Implementation Exercises — TensorTonic

> 199 ML coding challenges organized into 6 interview assessments.
> Mapped onto the tensor-to-tenant spine (W70–W93) per
> `schema/implementation_exercises.yaml`. See TASKS.md § T1.10.

The full catalog lives at <https://www.tensortonic.com/problems>; the
six assessment sections are at
<https://www.tensortonic.com/assessments>. This README and the per-
section index files give you the *mapping* — which problems are
load-bearing for which weeks, and which to treat as optional depth.

## Why this exists

The spine covers the inference and LLM training weeks at the
concept level. TensorTonic supplies the *implementation primitives*
that make those concepts legible: the 5-pattern prerequisite problems
(KV cache memory math, FlashAttention online softmax, continuous
batching simulator, throughput+cost under SLO, RoPE) are the
vocabulary the spine assumes you already have.

Without these, "PagedAttention manages the KV cache" and "FlashAttention
is IO-aware" are quotes, not defenses.

## The 6 assessments × spine weeks

| Assessment | Maps to | Level |
|---|---|---|
| 1. Attention Architectures (Scaled Dot-Product, MHA, MQA, GQA, MLA) | W70 + W82–83 | 2 |
| 2. Efficient Transformer Components (RoPE, FlashAttention, Sampling, MoE routing) | W82 + W90 + W73 | 2–3 |
| 3. KV Cache and Decoding (Autoregressive decoding, KV cache memory, PagedAttention, Prefix cache, Speculative decoding) | W84–85 + W89 + W92 | 2–3 |
| 4. Quantization and GPU Performance (INT8, INT4, FP8, Roofline) | W91 + W83 | 2–3 |
| 5. Batching and Serving Metrics (P50/P95/P99, TTFT/TPOT, dynamic/continuous batching, chunked prefill) | W86 + W90 | 2 |
| 6. Parallelism and Disaggregation (Memory/GPU estimation, TP comm, Expert parallel, Disaggregated serving) | W74 + W93 + Capstone 3 | 2–3 |

## Per-section index

- `01_attention_architectures.md` — attention primitives
- `02_efficient_transformer.md` — RoPE, FlashAttention, sampling, MoE
- `03_kv_cache_and_decoding.md` — KV cache, PagedAttention, speculative
- `04_quantization_and_gpu.md` — INT8/INT4/FP8 + roofline
- `05_batching_and_metrics.md` — serving metrics + batching simulations
- `06_parallelism_and_disagg.md` — parallelism + disaggregation

## Progress tracking

Complete one problem per week, in any order. Log completion in
`progress.csv` with the schema:

```csv
problem_id,pattern,week,tier,status,attempts,final_complexity,production_concept_reinforced
ttc_kv_cache_memory,prerequisite,84,core,done,2,O(1) per request,Capstone 3 ledger sizing
ttc_flashattention_online_softmax,prerequisite,82,core,todo,,,
…
```

Run `make progress` to see per-section completion alongside the
existing Darbar and Forge stats.

## The five Pattern C prerequisites

These five are **load-bearing for downstream weeks** and should be
completed before those weeks become legible. They're listed in
`schema/implementation_exercises.yaml` with `pattern: prerequisite`.

| Problem | Week | Why load-bearing |
|---|---|---|
| KV cache memory math (MHA/MQA/GQA/MLA) | W84 | vLLM/SGLang/Capstone 3 all depend on the exact formula |
| FlashAttention with online softmax | W82 | The online softmax trick is the seam itself |
| Continuous batching simulation | W90 | W90's headline topic becomes mechanical after the sim |
| Throughput + cost under latency SLO | W93 | Capstone 3's success criterion, pre-loaded |
| RoPE | W82–92 | Every modern model uses it; W82 inference weeks assume it |
