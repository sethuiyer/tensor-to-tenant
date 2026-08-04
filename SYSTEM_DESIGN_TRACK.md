# Canonical System Design Track

System design is not an extra phase. It is the canonical interview and
architecture track for **Weeks 46–57**, running beside the mathematical,
engineering, and AI-systems spine. The goal is to move from requirements and
`vector.dot()` to a defensible multi-tenant platform design with APIs, data
models, failure handling, capacity math, and operational evidence.

## The four-layer loop

Every design week uses the same loop:

1. **Frame:** requirements, users, SLOs, scale, privacy, and cost.
2. **Shape:** APIs, data model, partitioning, indexes, caches, and queues.
3. **Stress:** contention, failure modes, consistency, replay, recovery, and
   observability.
4. **Extend:** add the AI concern—embeddings, retrieval, inference routing,
   agent memory, evaluation, safety, or cost attribution.

The artifact is a design document, a small implementation or simulation, and
an interview-ready explanation. A diagram alone does not count.

## Weeks 46–57

| Week | Core system-design theme | Core case/lab | Evidence |
|---:|---|---|---|
| 46 | Delivery framework, requirements, networking, numbers to know | URL shortener / Bitly | Framed design + capacity sheet |
| 47 | API design, data modeling, indexing, contracts | LeetCode problem service | API and schema package |
| 48 | Caching, sharding, consistent hashing, CAP | Rate limiter + distributed cache | Design, key layout, failure table |
| 49 | Replication, read/write scaling, contention | News feed / Instagram | Read path, write path, consistency choice |
| 50 | Large blobs, CDN, metadata, resumable work | Dropbox / Google Docs | Storage design + recovery plan |
| 51 | Queues, workflows, long-running tasks | Job scheduler / Slack job queue | State machine + retry/idempotency plan |
| 52 | Schema evolution, real-time updates, coordination | WhatsApp / notification system | Contract migration + delivery semantics |
| 53 | Search, proximity, crawling, ranking | Yelp / FB post search / web crawler | Index and freshness design |
| 54 | Messaging and social fan-out | FB Live Comments / Tinder / Discord | Fan-out model + hot-key strategy |
| 55 | Scheduling, scarcity, marketplace correctness | Ticketmaster / Uber / local delivery / auction | Reservation invariant + contention test |
| 56 | Streaming, analytics, and data infrastructure | Ad clicks / metrics / Robinhood / Spotify data lake | Stream topology + watermark/replay notes |
| 57 | Integrated architecture and interview boss | ChatGPT / payment system / Figma multiplayer | Staff-level design review + trade-off defense |

The case list is intentionally larger than twelve weeks. Each week has one
core case and a set of adjacent cases for comparison, mock interviews, or
optional depth. The learner is not expected to fully implement every company
analogue.

## Technology labs

Use one technology as a concrete substrate for the design pattern. Core labs
are Redis, PostgreSQL, Kafka, Flink, an API gateway, and a vector database.
Supporting labs are Elasticsearch, Cassandra, DynamoDB, ZooKeeper, time-series
databases, and big-data structures. The question is never “memorize the tool”;
it is “what guarantee does this tool provide, and what does it make harder?”

## Pattern index

### Foundations

Introduction, how to prepare, delivery framework, core concepts, key
technologies, common patterns, networking essentials, API design, data modeling,
and numbers to know.

### Distributed systems

Caching, sharding, consistent hashing, CAP, database indexing, scaling reads,
scaling writes, real-time updates, contention, multi-step processes,
long-running tasks, large blobs, replication, schema evolution, and
observability.

### Case-study families

| Family | Cases |
|---|---|
| Storage and collaboration | Dropbox, Google Docs, Discord message storage, Figma multiplayer |
| Messaging and notifications | WhatsApp, FB Live Comments, notification system, Slack job queue |
| Search and retrieval | Yelp, FB Post Search, proximity search, web crawler, ChatGPT |
| Scheduling and logistics | Job Scheduler, Uber, local delivery, Ticketmaster, online chess |
| Streaming and analytics | Ad Click Aggregator, Metrics Monitoring, Robinhood, Spotify Data Lake |
| Marketplace and money | Online Auction, Payment System, Shopify Inventory Reservations |
| Social products | FB News Feed, Instagram, Tinder, Strava, News Aggregator |
| Platform primitives | Bitly, Distributed Cache, Rate Limiter, YouTube, YouTube Top K, LeetCode, Price Tracking Service |

## OOD / LLD companion lane

Object-oriented design runs as the Thursday implementation/interview variant,
not as another phase. Practice correctness, coordination, scarcity, OOP
concepts, design principles, and patterns through:

Connect Four, Amazon Locker, Elevator, Parking Lot, File System, Movie Ticket
Booking, Logging Service, Rate Limiter, and Inventory Management.

Each LLD artifact must state its invariants, ownership boundaries, concurrency
policy, and extension points. The distributed design then explains how the
single-process model changes when state is replicated or partitioned.

## AI extensions

Every design gets one AI extension so the track connects directly to the rest
of Tensor-to-Tenant:

| Base design | AI extension |
|---|---|
| WhatsApp | Semantic search, agent memory, PII-safe message retrieval |
| Search / Yelp | Hybrid BM25+dense retrieval, reranking, slice evaluation |
| Job scheduler | Tool-call DAGs, retries, cancellation, quota-aware admission |
| ChatGPT | Conversation storage, prompt registry, routing, KV cache, evaluation |
| Streaming metrics | Token/cost attribution, watermarking, late-event correction |
| Payment / reservations | Idempotency, exactly-once effects, auditability, contention |
| Figma multiplayer | Collaborative agent state, conflict resolution, presence |
| Distributed cache | Semantic and embedding cache with tenant isolation |

## Gate 5 contract

By Week 57, the learner must be able to choose a case from any family and
produce, under interview time pressure:

- requirements and SLOs;
- API and data model;
- partition, index, cache, queue, and replication choices;
- capacity estimates and a bottleneck plan;
- consistency, contention, idempotency, and failure semantics;
- observability, privacy, tenant isolation, and cost controls;
- one AI extension and a clear trade-off defense.

Use `make design=54` in a generated learner repo to scaffold a design artifact
for a specific week.
