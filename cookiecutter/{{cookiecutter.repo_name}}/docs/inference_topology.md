# Inference Topology — One Pipeline, Many Weeks

> Companion to the inference weeks (W82–W93). Shows every component
> of modern LLM serving as a single coherent pipeline rather than
> eight separate weekly concepts.
>
> A rendered version of this diagram (`public/images/serving-stack.webp`)
> will land in the Astro site via T1.11.a.1. Until then, this
> markdown view is the canonical reference for the cookiecutter repo.

## The pipeline

```text
                           ┌──────────────────────────┐
User Request                │ Load Balancer +          │
  │                         │ Request Batching         │
  │                         └────────────┬─────────────┘
  │                                      │
  │                                      ▼
  │                         ┌──────────────────────────┐
  │                         │ KV Cache Lookup          │
  │                         │ (PagedAttention)         │
  │                         └────────────┬─────────────┘
  │                                      │
  │                                      ▼
  │                         ┌──────────────────────────┐
  │                         │ MoE Expert Routing       │
  │                         │ (if applicable)          │
  │                         └────────────┬─────────────┘
  │                                      │
  │                                      ▼
  │                         ┌──────────────────────────┐
  │                         │ Multi-Head Attention     │
  │                         │ (with FlashAttention)    │
  │                         └────────────┬─────────────┘
  │                                      │
  │                                      ▼
  │                         ┌──────────────────────────┐
  │                         │ Speculative Decoding     │
  │                         │ Verification              │
  │                         └────────────┬─────────────┘
  │                                      │
  │                                      ▼
  │                         ┌──────────────────────────┐
  │                         │ Response Streaming       │
  │                         │ (with Top-p/Top-k        │
  │                         │  sampling)                │
  │                         └────────────┬─────────────┘
  │                                      │
  │                                      ▼
  │                         ┌──────────────────────────┐
  └────────────────────────►│ Metrics Logging          │
                           │ (TTFT, TPOT, P99)        │
                           └──────────────────────────┘
```

## Where each step lives in the curriculum

| Pipeline step | Spine week | Key artifact |
|---|---|---|
| Load Balancer + Request Batching | W90 (continuous batching), W94 (router) | `02_engineering_primitives/rate_limiting/`, `02_engineering_primitives/batching/` |
| KV Cache Lookup (PagedAttention) | W84 (PagedAttention), W85 (vLLM internals) | vLLM deployment |
| MoE Expert Routing | W90 (MoE + Warp Decode + COMET) | MoE overlap design doc |
| Multi-Head Attention (with FlashAttention) | W82 (GPU performance), W83 (Roofline) | FlashAttention knowledge |
| Speculative Decoding Verification | W92 (Medusa, EAGLE, StreamingLLM, KV eviction; linear attention/SSM alternatives) | Latency/memory lab |
| Response Streaming (with sampling) | W73 (alignment/sampling), W81 (agents) | Sampling logic |
| Metrics Logging (TTFT, TPOT, P99) | W86 (vLLM metrics), W87 (Prometheus/Grafana) | Live dashboard |

## The Level 3 question this diagram answers

When asked to design or debug a serving stack, the interviewer wants
to see that you can:

1. **Trace a single request through all eight stages** — what work
   happens at each step, what can fail, what is measured.
2. **Identify which optimization affects which stage** — quantization
   doesn't change the request flow but changes per-token latency;
   PagedAttention changes the KV-cache stage only; continuous batching
   changes the load-balancer stage.
3. **Place a failure in the right stage** — high TTFT points at the
   prefill or routing stage; high per-token jitter points at the
   sampling or scheduling stage; low throughput with normal latency
   points at the batching stage.

The TensorTonic problems (W84, W86, W90, W93 prerequisites) supply the
*implementation primitives* that make this trace concrete. The
schema-disciplined resources (see `schema/resources.yaml`) supply the
*Level 3 questions* that make the trace defensible.

## See also

- `schema/interview_questions.yaml` — the Level 3 question bank
- `schema/resources.yaml` — paper list with selection rationale
- `schema/implementation_exercises.yaml` — TensorTonic integration
- `docs/bottlenecks.md` — three documented bottlenecks + self-recovery
  protocols, including the GPU-budget redirect to Modal
