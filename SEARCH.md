# Building a Smart Tool Recommendation Engine with Semantic Similarity, Graph Traversal, Adamic–Adar, IDF Weighting, Decay, and Thresholds

Suppose a developer types:

> “I need to extract invoices from Gmail, classify them with an LLM, and save the results to PostgreSQL.”

A recommendation engine should ideally return:

1. Gmail connector
2. PDF or invoice extraction skill
3. Document-classification agent
4. PostgreSQL connector
5. A workflow or harness connecting everything together

The tricky part is that no single ranking technique can reliably produce this list.

Semantic similarity understands meaning, but may ignore structural relationships. Keyword matching is precise, but brittle. Graph traversal discovers connected tools, but can drift into irrelevant regions. Popularity signals help break ties, but can overpower genuinely relevant niche tools.

A robust recommendation engine therefore combines several imperfect signals into one ranking score.

---

## 1. Representing the Recommendation Space as a Graph

We begin by modelling the ecosystem as a graph:

$$
G=(V,E)
$$

Each node represents an entity such as:

* Skill
* Agent
* MCP server
* Connector
* Harness
* Workflow template
* Data source
* API operation

An edge represents a relationship between two entities.

Examples:

$$
\text{Gmail Skill} \rightarrow \text{Gmail MCP Server}
$$

$$
\text{Invoice Agent} \rightarrow \text{PDF Extraction Skill}
$$

$$
\text{PostgreSQL Harness} \rightarrow \text{Database Agent}
$$

Edges may also carry weights:

$$
w(u,v)\in[0,1]
$$

A weight near $1$ means the relationship is strong. A lower weight means the connection is weaker or more speculative.

The graph gives us structure. Embeddings and lexical matching give us relevance.

---

# 2. Semantic Similarity with Cosine Similarity

Semantic similarity answers:

> “Does this candidate mean something similar to the user’s request?”

Let the query embedding be $q$, and the candidate embedding be $v$.

Cosine similarity is:

$$
\operatorname{cos}(q,v)
=
\frac{q\cdot v}
{\|q\|_2\|v\|_2}
$$

When vectors are L2-normalized:

$$
\hat q=\frac{q}{\|q\|_2},
\qquad
\hat v=\frac{v}{\|v\|_2}
$$

the cosine similarity simplifies to:

$$
\operatorname{cos}(q,v)=\hat q\cdot\hat v
$$

For normalized vectors, the score usually lies between $-1$ and $1$, though modern text embeddings often cluster mostly in the positive range.

A simple conversion to a ranking score is:

$$
S_{\text{semantic}}(v)
=
100\cdot \max(0,\operatorname{cos}(q,v))
$$

### Example

User query:

> “Extract invoice fields from email attachments.”

Candidate A:

> “Parse invoices and extract vendor, total, date, and tax.”

Candidate B:

> “Generate social-media captions from product descriptions.”

Possible cosine similarities:

$$
\operatorname{cos}(q,A)=0.89
$$

$$
\operatorname{cos}(q,B)=0.21
$$

So:

$$
S_{\text{semantic}}(A)=89
$$

$$
S_{\text{semantic}}(B)=21
$$

Candidate A is clearly more relevant.

---

## 3. Length-Weighted Mean Pooling for Long Descriptions

Embedding models normally have context limits. Even when a model supports long inputs, directly embedding a huge document may dilute important information.

A better approach is to divide the text into chunks.

Suppose a tool description produces chunk embeddings:

$$
v_1,v_2,\ldots,v_n
$$

Let $w_i$ be the number of tokens in chunk $i$. The final embedding is:

$$
v_{\text{final}}
=
\frac{
\sum_{i=1}^{n}w_i v_i
}{
\sum_{i=1}^{n}w_i
}
$$

The result should then be normalized:

$$
\hat v_{\text{final}}
=
\frac{v_{\text{final}}}
{\|v_{\text{final}}\|_2}
$$

Why use length weighting?

Imagine one chunk contains 500 tokens and another contains only 40. Treating both equally would allow the short chunk to influence the representation as much as the long chunk. Length weighting prevents that distortion.

However, raw length weighting is not always ideal. Boilerplate or repetitive chunks can dominate. In production, you may combine length with a quality weight:

$$
w_i
=
\text{tokenCount}_i
\times
\text{informationQuality}_i
$$

---

# 4. Graph Traversal with Hop Decay

Semantic search normally gives us a set of seed nodes. Graph traversal expands those seeds into structurally related candidates.

For example, semantic retrieval may find:

$$
\text{Invoice Extraction Skill}
$$

The graph can then discover:

* OCR MCP server
* Gmail attachment reader
* Document classifier
* PostgreSQL writer
* Invoice-processing harness

A breadth-first search can explore the graph up to a maximum number of hops.

Let the hop-decay function be:

$$
d(h)=\frac{1}{h+1}
$$

Therefore:

$$
d(0)=1
$$

$$
d(1)=\frac12
$$

$$
d(2)=\frac13
$$

$$
d(3)=\frac14
$$

A node reached through path $p$ receives:

$$
S_{\text{path}}(n,p)
=
\left(
\prod_{e\in p}w(e)
\right)
d(|p|)
$$

Alternatively, an additive edge formulation may be used:

$$
S_{\text{path}}(n,p)
=
\sum_{e\in p} w(e)\cdot d(|p|)
$$

The multiplicative version penalizes paths containing even one weak edge. The additive version is more forgiving. For recommendation graphs, the multiplicative formulation is often safer because it suppresses weak chains.

If multiple paths reach the same node, their contributions may be combined:

$$
S_{\text{walk}}(n)
=
\sum_{p\in P(n)}
S_{\text{path}}(n,p)
$$

To prevent highly connected nodes from collecting unlimited score, use a cap:

$$
S_{\text{walk}}(n)
=
\min
\left(
S_{\text{walk}}(n),
S_{\max}
\right)
$$

---

## Worked Graph Example

Assume the seed node is `Invoice Agent`.

The graph contains:

$$
\text{Invoice Agent}
\xrightarrow{0.9}
\text{PDF Extractor}
$$

$$
\text{PDF Extractor}
\xrightarrow{0.8}
\text{OCR MCP}
$$

$$
\text{OCR MCP}
\xrightarrow{0.6}
\text{Generic Vision Tool}
$$

The scores are:

### PDF Extractor

One hop away:

$$
S = 0.9 \times \frac{1}{2} = 0.45
$$

### OCR MCP

Two hops away:

$$
S = 0.9 \times 0.8 \times \frac{1}{3} = 0.24
$$

### Generic Vision Tool

Three hops away:

$$
S = 0.9 \times 0.8 \times 0.6 \times \frac{1}{4} = 0.108
$$

The further the candidate is from the seed, the more evidence it needs to remain competitive.

---

# 5. Adamic–Adar for Relationship Strength

Graph traversal asks:

> “Can we reach this node?”

Adamic–Adar asks:

> “How meaningful is the relationship between these two nodes?”

For nodes $x$ and $y$, let:

$$
\Gamma(x)
$$

represent the neighbours of $x$.

The Adamic–Adar score is:

$$
AA(x,y)
=
\sum_{z\in\Gamma(x)\cap\Gamma(y)}
\frac{1}{\log |\Gamma(z)|}
$$

Each common neighbour contributes evidence that $x$ and $y$ are related.

However, rare common neighbours contribute more than popular ones.

Consider two tools sharing the neighbour:

> “HTTP”

That is weak evidence because thousands of tools may use HTTP.

Now consider two tools sharing:

> “SAP invoice reconciliation adapter”

That is much stronger evidence because the shared neighbour is highly specific.

### Example

Suppose Tool A and Tool B have three common neighbours:

| Common neighbour   | Degree |
| ------------------ | -----: |
| HTTP               |  5,000 |
| OCR                |    200 |
| GST invoice schema |      8 |

Then:

$$
AA(A,B)
=
\frac{1}{\log 5000}
+
\frac{1}{\log 200}
+
\frac{1}{\log 8}
$$

Approximately:

$$
AA(A,B)
\approx
0.117+0.189+0.481
=
0.787
$$

The rare GST schema contributes most of the relationship score.

This is exactly the behaviour we want.

---

## Avoiding Hub Domination

Extremely connected nodes can still create graph noise. A simple defence is to bound the degree:

$$
\deg'(z)
=
\min(\max(\deg(z),d_{\min}),d_{\max})
$$

Then:

$$
AA(x,y)
=
\sum_z
\frac{1}{\log \deg'(z)}
$$

You may also cap the final Adamic–Adar score:

$$
S_{\text{AA}}(x,y)
=
\min(AA(x,y),1)
$$

---

# 6. Lexical Matching with IDF Weighting

Semantic similarity is flexible, but exact terminology still matters.

For example, a query containing:

> `postgresql`

should strongly favour a PostgreSQL-specific tool over a generic database tool.

A lexical scorer can use:

* Exact slug match
* Exact token match
* Tag overlap
* Substring match
* Alias match
* Acronym expansion

But not all words should contribute equally.

Words such as `tool`, `agent`, `data`, and `API` appear everywhere. Rare terms such as `snowflake`, `netsuite`, or `adamic-adar` carry more information.

Inverse document frequency measures this rarity.

$$
IDF(t)
=
\log
\left(
\frac{N+\alpha}
{df(t)+\alpha}
\right)
$$

where:

* $N$ is the total number of entities
* $df(t)$ is the number of entities containing term $t$
* $\alpha$ is a smoothing constant, commonly $1$

A normalized version is:

$$
IDF_{\text{norm}}(t)
=
\frac{IDF(t)}
{\max_j IDF(j)}
$$

A token-match score could be:

$$
S_{\text{exact}}(t)
=
50\left(1+IDF_{\text{norm}}(t)\right)
$$

A tag overlap score could be:

$$
S_{\text{tag}}
=
\sum_{t\in Q\cap T}
10\left(1+IDF_{\text{norm}}(t)\right)
$$

where $Q$ is the set of query tokens and $T$ is the candidate’s tag set.

---

## IDF Example

Assume there are:

$$
N=10{,}000
$$

tools.

The term `API` appears in:

$$
df(\text{API})=7{,}000
$$

The term `NetSuite` appears in:

$$
df(\text{NetSuite})=40
$$

Using smoothed IDF:

$$
IDF(\text{API})
=
\log\left(\frac{10001}{7001}\right)
\approx 0.357
$$

$$
IDF(\text{NetSuite})
=
\log\left(\frac{10001}{41}\right)
\approx 5.497
$$

Therefore, matching `NetSuite` should provide much more ranking evidence than matching `API`.

---

# 7. Intent Signals and Controlled Boosting

Queries often reveal multiple intent signals.

Consider:

> “Create a Python agent that reads Gmail attachments and inserts invoice data into PostgreSQL.”

The intent detector may extract:

* Language: Python
* Source: Gmail
* Input type: attachment
* Domain: invoice processing
* Destination: PostgreSQL
* Architecture: agent
* Operation: extract and insert

A candidate matching several independent signals deserves a boost.

One simple function is:

$$
S_{\text{intent}}
=
5\cdot \min(k,3)
$$

where $k$ is the number of matched intent signals.

Thus:

$$
k=1 \Rightarrow 5
$$

$$
k=2 \Rightarrow 10
$$

$$
k\geq3 \Rightarrow 15
$$

The cap is essential. Without it, metadata-rich candidates could dominate the ranking purely because they have many tags.

A more refined version weights different intent classes:

$$
S_{\text{intent}}
=
\min
\left(
\sum_j \lambda_j I_j,
S_{\text{intent,max}}
\right)
$$

For example:

* Exact platform match: (8)
* Programming-language match: (3)
* Operation match: (5)
* File-type match: (4)
* Deployment-environment match: (3)

---

# 8. Type Affinity

Not every entity type should connect equally strongly to every other type.

For example:

* Skill to agent: strong
* Skill to MCP server: strong
* Agent to harness: strong
* Unrelated skill to skill: weaker
* Generic connector to arbitrary agent: medium

We can define a type-affinity matrix:

$$
A(t_i,t_j)\in[0,1]
$$

Example:

| Entity pair          | Affinity |
| -------------------- | -------: |
| Skill ↔ Agent        |     1.00 |
| Skill ↔ MCP server   |     0.90 |
| Skill ↔ Harness      |     0.75 |
| Agent ↔ MCP server   |     0.65 |
| Agent ↔ Harness      |     0.70 |
| MCP server ↔ Harness |     0.60 |
| Same type            |     0.35 |

When constructing or traversing an edge:

$$
w'(u,v)
=
w(u,v)\cdot A(type(u),type(v))
$$

This encodes useful architectural priors into the graph.

It prevents the system from treating every relationship as equally meaningful.

---

# 9. Dynamic Noise-Floor Filtering

Even a good ranking model produces low-quality tail results. Returning all of them reduces trust.

A fixed threshold such as:

$$
S(n)>0.4
$$

is easy to implement, but query score distributions vary.

For one query, the top score may be (0.92). For another, the highest score may only be (0.51).

A dynamic threshold adapts to the result set.

One approach is percentile-based filtering:

$$
\tau
=
P_p(S)
$$

where $P_p$ is the $p$-th percentile of candidate scores.

Then keep:

$$
R
=
\{ n : S(n) \geq \tau \}
$$

A safer hybrid threshold combines a fixed floor and a relative floor:

$$
\tau
=
\max
\left(
\tau_{\min},
\alpha S_{\max},
P_p(S)
\right)
$$

For example:

$$
\tau_{\min}=0.20
$$

$$
\alpha=0.30
$$

$$
p=30
$$

This prevents the engine from returning weak candidates just because every candidate scored poorly.

Different entity classes can have different thresholds:

$$
\tau_{\text{skill}}=0.30
$$

$$
\tau_{\text{tooling}}=0.20
$$

That makes sense when tool or harness relationships are naturally weaker or sparser than skill matches.

---

# 10. Combining All Signals

Each candidate receives several scores:

$$
S_{\text{semantic}}
$$

$$
S_{\text{walk}}
$$

$$
S_{\text{AA}}
$$

$$
S_{\text{lexical}}
$$

$$
S_{\text{degree}}
$$

$$
S_{\text{intent}}
$$

The final score can be a weighted sum:

$$
S_{\text{final}}(n)
=
\lambda_s S_{\text{semantic}}(n)
+
\lambda_g S_{\text{walk}}(n)
+
\lambda_a S_{\text{AA}}(n)
+
\lambda_l S_{\text{lexical}}(n)
+
\lambda_d S_{\text{degree}}(n)
+
S_{\text{intent}}(n)
$$

The weights should satisfy:

$$
\lambda_s+\lambda_g+\lambda_a+\lambda_l+\lambda_d=1
$$

Example configuration:

$$
\lambda_s=0.40
$$

$$
\lambda_g=0.20
$$

$$
\lambda_a=0.15
$$

$$
\lambda_l=0.20
$$

$$
\lambda_d=0.05
$$

Semantic relevance is the strongest signal, but structure and lexical evidence still have substantial influence.

Before combining signals, normalize them to comparable ranges.

Min-max normalization is:

$$
\hat S_i(n)
=
\frac{
S_i(n)-\min S_i
}{
\max S_i-\min S_i+\epsilon
}
$$

A rank-based or percentile normalization is often more robust when score distributions are highly skewed.

---

## Worked Final-Score Example

Assume a PostgreSQL invoice harness receives:

| Signal              | Normalized score |
| ------------------- | ---------------: |
| Semantic similarity |             0.82 |
| Graph walk          |             0.70 |
| Adamic–Adar         |             0.64 |
| Lexical match       |             0.91 |
| Degree score        |             0.40 |
| Intent boost        |             0.10 |

Using:

$$
S_{\text{final}}
=
0.40S_s
+
0.20S_g
+
0.15S_a
+
0.20S_l
+
0.05S_d
+
S_{\text{intent}}
$$

we obtain:

$$
S_{\text{final}}
=
0.40(0.82)
+
0.20(0.70)
+
0.15(0.64)
+
0.20(0.91)
+
0.05(0.40)
+
0.10
$$

$$
S_{\text{final}} = 0.328 + 0.14 + 0.096 + 0.182 + 0.02 + 0.10 = 0.866
$$

This is a strong candidate.

---

# 11. From Ranking Score to Priority and Confidence

The internal ranking score may also be converted into user-facing metadata.

Let the normalized score be:

$$
z\in[0,1]
$$

Priority can be mapped to an integer range:

$$
priority
=
3+\min(\lfloor 12z\rfloor,12)
$$

Therefore:

$$
priority\in[3,15]
$$

Confidence can be calculated as:

$$
confidence
=
0.6+0.35z
$$

Thus:

$$
confidence\in[0.6,0.95]
$$

For:

$$
z=0.8
$$

we get:

$$
priority
=
3+\lfloor9.6\rfloor
12
$$

and:

$$
confidence
=
0.6+0.35(0.8)
0.88
$$

These values should not be interpreted as calibrated probabilities unless the system has actually undergone probability calibration.

A score of (0.88) does not automatically mean there is an 88% chance that the recommendation is correct. It is merely a confidence-like presentation value unless validated against labelled data.

---

# 12. End-to-End Retrieval Pipeline

A practical recommendation pipeline can be organised as follows.

### Step 1: Parse the query

Extract:

* Important entities
* Exact product names
* Technologies
* Operations
* Programming languages
* Input and output formats
* User intent

### Step 2: Embed the query

Generate a normalized query vector:

$$
\hat q
$$

### Step 3: Retrieve semantic seeds

Perform approximate nearest-neighbour search and select the top $k$ candidates.

For example:

$$
k=50
$$

### Step 4: Calculate lexical matches

Score exact tokens, tags, slugs, aliases, and substrings using IDF weighting.

### Step 5: Traverse the graph

Run a bounded graph walk from high-quality seed nodes.

Typical settings:

$$
max_hops=2 \text{ or } 3
$$

### Step 6: Calculate graph features

For every candidate, calculate:

* Decayed graph-walk score
* Adamic–Adar score
* Type affinity
* Degree or popularity feature
* Number of independent paths

### Step 7: Normalize and combine

Normalize the features and calculate the final weighted score.

### Step 8: Apply boosts and penalties

Possible boosts:

* Exact technology match
* Multiple intent-signal match
* Verified integration
* Recently successful usage

Possible penalties:

* Deprecated tool
* High failure rate
* Missing permissions
* Incompatible runtime
* Excessive latency
* Weak path evidence

### Step 9: Apply noise-floor filtering

Discard candidates below the dynamic threshold.

### Step 10: Diversify the output

Avoid returning ten nearly identical tools.

The result should cover useful roles such as:

* Source connector
* Transformation skill
* Agent
* Destination connector
* Harness or workflow

---

# 13. Python-Like Pseudocode

```python
from collections import defaultdict, deque
from dataclasses import dataclass
from math import log
from typing import Iterable


@dataclass
class CandidateFeatures:
    semantic: float = 0.0
    graph_walk: float = 0.0
    adamic_adar: float = 0.0
    lexical: float = 0.0
    degree: float = 0.0
    intent_boost: float = 0.0


def cosine_similarity(
    query_vector: list[float],
    candidate_vector: list[float],
) -> float:
    if len(query_vector) != len(candidate_vector):
        raise ValueError("Embedding dimensions must match.")

    return sum(
        q * c for q, c in zip(query_vector, candidate_vector)
    )


def inverse_document_frequency(
    total_documents: int,
    document_frequency: int,
    smoothing: float = 1.0,
) -> float:
    if total_documents < 1:
        raise ValueError("total_documents must be positive.")

    return log(
        (total_documents + smoothing)
        / (document_frequency + smoothing)
    )


def hop_decay(hop: int) -> float:
    if hop < 0:
        raise ValueError("hop cannot be negative.")

    return 1.0 / (hop + 1)


def graph_walk(
    graph: dict[str, list[tuple[str, float]]],
    seed_scores: dict[str, float],
    max_hops: int = 3,
) -> dict[str, float]:
    scores: dict[str, float] = defaultdict(float)
    queue = deque()

    for seed, seed_score in seed_scores.items():
        scores[seed] += seed_score
        queue.append((seed, 0, seed_score))

    while queue:
        node, hop, path_score = queue.popleft()

        if hop >= max_hops:
            continue

        for neighbour, edge_weight in graph.get(node, []):
            next_hop = hop + 1

            contribution = (
                path_score
                * edge_weight
                * hop_decay(next_hop)
            )

            scores[neighbour] += contribution

            queue.append(
                (neighbour, next_hop, path_score * edge_weight)
            )

    return dict(scores)


def adamic_adar(
    node_a: str,
    node_b: str,
    neighbours: dict[str, set[str]],
    degree_cap: int = 2000,
) -> float:
    common = neighbours.get(node_a, set()) & neighbours.get(
        node_b, set()
    )

    score = 0.0

    for common_node in common:
        degree = len(neighbours.get(common_node, set()))
        bounded_degree = min(max(degree, 2), degree_cap)
        score += 1.0 / log(bounded_degree)

    return score


def final_score(features: CandidateFeatures) -> float:
    return (
        0.40 * features.semantic
        + 0.20 * features.graph_walk
        + 0.15 * features.adamic_adar
        + 0.20 * features.lexical
        + 0.05 * features.degree
        + features.intent_boost
    )


def dynamic_threshold(
    scores: Iterable[float],
    fixed_floor: float = 0.20,
    relative_floor: float = 0.30,
) -> float:
    score_list = sorted(scores)

    if not score_list:
        return fixed_floor

    max_score = score_list[-1]
    percentile_index = int(0.30 * (len(score_list) - 1))
    percentile_floor = score_list[percentile_index]

    return max(
        fixed_floor,
        relative_floor * max_score,
        percentile_floor,
    )
```

---

# 14. Important Production Problems

## Double-counting evidence

Semantic similarity, tag overlap, and graph edges may all originate from the same description.

For example, a tag may have been generated directly from the text used to create the embedding. Treating the semantic score and tag score as fully independent exaggerates the evidence.

Possible defences include:

* Reducing correlated feature weights
* Learning weights from labelled data
* Grouping correlated features
* Using a learning-to-rank model

---

## Popularity bias

Graph degree is useful as a weak prior, but it can bury specialised tools.

Use:

$$
S_{\text{degree}}=\log(1+\deg(n))
$$

rather than raw degree.

Then cap or normalize it.

Popularity should break ties—not decide the entire ranking.

---

## Graph drift

Long graph walks eventually enter generic, popular regions.

To control drift:

* Limit traversal to two or three hops
* Apply hop decay
* Multiply by edge confidence
* Enforce type affinity
* Require minimum semantic relevance
* Penalize generic hubs
* Limit paths per candidate

---

## Query ambiguity

A query such as:

> “I need a Slack tool”

does not reveal whether the user wants to:

* Read messages
* Send messages
* Search history
* Summarize channels
* Manage users
* Trigger workflows

The system should either return a diversified set or ask a clarifying question.

A confident but wrong recommendation is worse than a brief clarification.

---

## Threshold instability

Percentile thresholds behave strangely with very small candidate sets.

When only three candidates exist, the 30th percentile is not very meaningful.

Use a hybrid policy:

$$
\tau =
\begin{cases}
\tau_{\min}, & |C|<k_{\min}\\
\max(\tau_{\min},\alpha S_{\max},P_p(S)),
& \text{otherwise}
\end{cases}
$$

---

# 15. Improving the Model with Telemetry

Hand-tuned weights are a good starting point, but user behaviour should eventually influence ranking.

Useful signals include:

* Recommendation clicked
* Tool installed
* Workflow created
* Workflow successfully executed
* Tool removed shortly after installation
* User returned to search
* Execution failed
* Recommendation manually dismissed

A training label should favour meaningful downstream success, not merely clicks.

For example:

$$
reward
=
0.1(\text{click})
+
0.3(\text{install})
+
1.0(\text{successful execution})
-
0.8(\text{immediate uninstall})
$$

The ranking model can then learn:

$$
f(q,n)
\rightarrow
P(\text{successful use}\mid q,n)
$$

Suitable models include:

* Logistic regression
* Gradient-boosted trees
* LambdaMART
* Pairwise ranking models
* Neural rerankers

The handcrafted semantic and graph scores remain useful as model features.

---

# 16. Evaluation

A recommendation engine should be evaluated at several levels.

### Retrieval quality

Did the system find the right candidate at all?

Useful metrics:

$$
Recall@K
$$

$$
HitRate@K
$$

### Ranking quality

Did the best candidate appear near the top?

Useful metrics:

$$
MRR
$$

$$
NDCG@K
$$

### Diversity

Did the results cover different useful roles rather than returning duplicates?

Possible metrics:

* Type coverage
* Intra-list similarity
* Duplicate rate

### Operational success

Did users successfully build or execute something?

Useful metrics:

* Installation rate
* Successful-run rate
* Time to first successful workflow
* Recommendation abandonment rate

Offline ranking metrics alone are not enough. A recommendation can look mathematically relevant while being operationally useless.

---

# 17. The Core Intuition

Each ranking signal answers a different question.

**Semantic similarity**

> Does this candidate mean roughly what the user asked for?

**IDF-weighted lexical matching**

> Does it contain the exact rare terminology the user used?

**Graph traversal**

> Is it structurally connected to something we already know is relevant?

**Hop decay**

> Is that connection still trustworthy after several graph steps?

**Adamic–Adar**

> Do the two entities share rare, informative neighbours?

**Type affinity**

> Does this relationship make architectural sense?

**Intent boosting**

> Does the candidate satisfy several independent parts of the request?

**Noise-floor filtering**

> Is the evidence strong enough for the candidate to be shown at all?

The final recommender is not based on one magical formula. It works because these signals compensate for one another’s weaknesses.

Semantic similarity gives recall. Lexical matching gives precision. Graph traversal gives compositional discovery. Adamic–Adar measures structural specificity. Decay prevents graph drift. Thresholds protect the user from low-confidence clutter.

That combination turns a plain vector search into an actual recommendation system. 🔥
