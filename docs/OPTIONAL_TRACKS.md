# Optional-track inventory

> These topics are deliberately **optional and non-gating**. They are inventory
> and direction, not an eleventh phase. Promote one into the core only after it
> receives a week, level, seam, selection rationale, and schema cross-reference.

The core spine, gates, and three releases remain the completion contract. Use the
[parallel-track router](./PARALLEL_TRACKS.md) to find the canonical artifacts.

## LLM inference and serving

PagedAttention, continuous batching, RadixAttention, prefix caching, speculative
decoding, AWQ, GPTQ, GGUF, quantization trade-offs, and benchmarking.

## Vector databases and retrieval

HNSW, IVF/IVF-PQ, product quantization, hybrid search (BM25 + dense), query
rewriting, parent-child chunking, multi-vector retrieval, agentic RAG,
cross-encoder rerankers, and embedding evaluation.

## Alignment and fine-tuning

RLHF, DPO, ORPO, GRPO, and supervised fine-tuning (SFT).

## Distributed training

DDP/FSDP, tensor parallelism, Megatron-LM, pipeline parallelism, DeepSpeed, and
ZeRO optimizer state partitioning.

## Guardrails and safety

Llama Guard, NeMo Guardrails, prompt-injection defense, PII handling, and
hallucination detection.

## Evaluation

LLM-as-a-judge, Ragas, TruLens, MMLU, GSM8K, HumanEval, slice metrics,
calibration, and regression analysis.

## Embeddings

Embedding evaluation and cross-encoder rerankers.

## Classical ML and statistics

Bias–variance, overfitting and underfitting, precision/recall/F1, ROC-AUC and
PR curves, class imbalance (SMOTE and class weights), threshold tuning, XGBoost,
LightGBM, random forests, hypothesis testing, and A/B testing.

## ML system design and production ML

Problem framing, objective/constraint design, data quality and labeling,
leakage/contamination checks, deployment modes, feature and model versioning,
experiment tracking, offline/online evaluation, slice metrics, rollout strategy,
monitoring, drift, and incident response. These topics deepen the core ML
lifecycle without creating another required phase.

## AI engineering

Framework-oriented implementation, API/tool integration, prompt management,
retrieval pipelines, evaluation harnesses, and production reliability patterns.
Choose a workload and failure mode; do not collect framework badges.

## AI agents

ReAct, plan-and-execute, reflection/self-critique loops, planner–executor–reviewer,
function calling, code interpreters and sandboxes, LangGraph workflows, AutoGen,
API/database tools, short-term context memory, and long-term vector/graph memory.

The structured module map and bridge live at the [agents page](https://sethuiyer.github.io/tensor-to-tenant/agents/)
and [`../schema/agents.yaml`](../schema/agents.yaml).

## Multimodal AI

CLIP and image embeddings, diffusion models, vision-language architecture,
text-to-image systems, video generation, cross-modal retrieval, and multimodal
search architecture.

## Architecture and leadership

RFCs and design docs, architectural reviews, technical roadmaps, cross-team
influence, technical debt management, infrastructure cost modeling, and capacity
planning.

## Additional system-design problems

Design ChatGPT, chat/messaging systems, donations websites, notification systems,
payment systems, distributed file systems, rate limiters, ad-click aggregators,
real-time chess, marketplaces, REST aggregation, and rule-based OO design.
The canonical case-study sequence remains [`../SYSTEM_DESIGN_TRACK.md`](../SYSTEM_DESIGN_TRACK.md).

## Snowflake and data engineering

Snowflake projects, DBT + Snowflake + AWS, hotel-booking pipelines, data cleaning
and deduplication, tokenization, A/B testing, and data-science mock interviews.
The paired production deep dive is [`../SNOWFLAKE.md`](../SNOWFLAKE.md).

## AI fundamentals and vocabulary

Short explainers on AI concepts, distilling an LLM into a small model, and
practical A/B-testing stories. These are orientation resources, not core gates.

## Selection rule

A topic becomes core only when it changes how the learner thinks about a system
and exposes a seam the curriculum can test. A fancier model without a workload,
failure mode, evaluation plan, or production boundary remains optional/archive.
