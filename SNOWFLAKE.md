Bro, this is where the elegant math puts on a hard hat and becomes **data plumbing** 😭🔥

# Wiring the CTX Recommendation Engine in Snowflake

The recommendation engine can live almost entirely inside Snowflake:

```text
Entity metadata
      ↓
Cortex embeddings
      ↓
Semantic seed retrieval
      ↓
Graph expansion
      ↓
Adamic–Adar + IDF features
      ↓
Score normalization
      ↓
Decay + dynamic threshold
      ↓
Ranked skills, agents, MCPs, and harnesses
```

Snowflake provides the main primitives we need:

* `AI_EMBED` to generate embeddings.
* The `VECTOR` data type to store them.
* `VECTOR_COSINE_SIMILARITY` for semantic retrieval.
* Recursive CTEs for bounded graph walks.
* Standard SQL aggregations for IDF and Adamic–Adar.
* `PERCENTILE_CONT` or `APPROX_PERCENTILE` for dynamic thresholds.
* Streams and Tasks for incremental refreshes.

`AI_EMBED` is Snowflake’s current embedding interface, and the vector functions operate directly on stored `VECTOR` values. In this tutorial, we will use `snowflake-arctic-embed-m-v1.5`, which produces 768-dimensional vectors. ([Snowflake Documentation][1])

---

## 1. Create the Database Objects

We will maintain four main datasets:

1. Entities.
2. Graph edges.
3. Entity tokens.
4. Term statistics.

```sql
CREATE OR REPLACE DATABASE CTX_DB;
CREATE OR REPLACE SCHEMA CTX_DB.RECOMMENDER;

USE DATABASE CTX_DB;
USE SCHEMA RECOMMENDER;
```

The role running the embedding queries needs the appropriate Cortex database role.

```sql
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_EMBED_USER
TO ROLE CTX_APP_ROLE;
```

Snowflake currently allows either `SNOWFLAKE.CORTEX_USER` or the more narrowly scoped `SNOWFLAKE.CORTEX_EMBED_USER` role to call `AI_EMBED`. ([Snowflake Documentation][2])

---

# 2. Store the Entities

Every skill, agent, MCP server, harness, and connector becomes one entity row.

```sql
CREATE OR REPLACE TABLE CTX_ENTITIES (
    entity_id       VARCHAR PRIMARY KEY,
    entity_type     VARCHAR NOT NULL,
    slug            VARCHAR,
    display_name    VARCHAR,
    description     VARCHAR,
    tags            ARRAY,
    status          VARCHAR DEFAULT 'active',
    quality_score   FLOAT DEFAULT 1.0,
    search_text     VARCHAR,
    embedding       VECTOR(FLOAT, 768),
    updated_at      TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
```

Example entities:

```sql
INSERT INTO CTX_ENTITIES (
    entity_id,
    entity_type,
    slug,
    display_name,
    description,
    tags
)
SELECT
    'skill_invoice_extract',
    'skill',
    'invoice-extraction',
    'Invoice Extraction',
    'Extract vendor, date, currency, tax and total fields from invoices.',
    ARRAY_CONSTRUCT(
        'invoice',
        'ocr',
        'document extraction',
        'accounts payable'
    )

UNION ALL

SELECT
    'agent_invoice_processor',
    'agent',
    'invoice-processing-agent',
    'Invoice Processing Agent',
    'Processes incoming invoice files and routes structured results.',
    ARRAY_CONSTRUCT(
        'agent',
        'invoice',
        'classification',
        'workflow'
    )

UNION ALL

SELECT
    'mcp_gmail',
    'mcp-server',
    'gmail-mcp',
    'Gmail MCP Server',
    'Search Gmail and retrieve messages, threads and attachments.',
    ARRAY_CONSTRUCT(
        'gmail',
        'email',
        'attachment',
        'mcp'
    )

UNION ALL

SELECT
    'harness_postgres',
    'harness',
    'postgres-output-harness',
    'PostgreSQL Output Harness',
    'Writes validated structured records into PostgreSQL.',
    ARRAY_CONSTRUCT(
        'postgresql',
        'database',
        'sql',
        'structured output'
    );
```

---

## 3. Build a Canonical Search Document

Rather than embedding only the description, construct a canonical representation containing the most useful metadata.

```sql
UPDATE CTX_ENTITIES
SET search_text =
    CONCAT_WS(
        '\n',
        'Type: ' || entity_type,
        'Name: ' || COALESCE(display_name, ''),
        'Slug: ' || COALESCE(slug, ''),
        'Description: ' || COALESCE(description, ''),
        'Tags: ' || COALESCE(ARRAY_TO_STRING(tags, ', '), '')
    );
```

A resulting document might look like:

```text
Type: skill
Name: Invoice Extraction
Slug: invoice-extraction
Description: Extract vendor, date, currency, tax and total fields from invoices.
Tags: invoice, ocr, document extraction, accounts payable
```

This gives the embedding model enough context to distinguish:

* What the entity does.
* What type of entity it is.
* Which exact technologies it supports.
* Which broader use cases it belongs to.

---

# 4. Generate the Embeddings

```sql
UPDATE CTX_ENTITIES
SET embedding = AI_EMBED(
    'snowflake-arctic-embed-m-v1.5',
    search_text
)
WHERE search_text IS NOT NULL;
```

Snowflake stores the returned value directly as a `VECTOR`. The vector dimension must agree with the selected model; `snowflake-arctic-embed-m-v1.5` returns 768 dimensions. ([Snowflake Documentation][1])

For large descriptions, keep chunks in a separate table:

```sql
CREATE OR REPLACE TABLE CTX_ENTITY_CHUNKS (
    entity_id       VARCHAR,
    chunk_id        INTEGER,
    chunk_text      VARCHAR,
    token_count     INTEGER,
    embedding       VECTOR(FLOAT, 768),
    PRIMARY KEY (entity_id, chunk_id)
);
```

Each chunk can be embedded independently:

```sql
UPDATE CTX_ENTITY_CHUNKS
SET embedding = AI_EMBED(
    'snowflake-arctic-embed-m-v1.5',
    chunk_text
);
```

At retrieval time, combine the chunk scores:

$$
S_{\text{entity}}
=
0.7\max_i S_i
+
0.3
\frac{\sum_i w_iS_i}{\sum_iw_i}
$$

The maximum preserves a highly relevant local passage, while the weighted mean captures the entity’s overall relevance.

---

# 5. Store the Recommendation Graph

The graph edges represent structural relationships.

```sql
CREATE OR REPLACE TABLE CTX_EDGES (
    source_id       VARCHAR NOT NULL,
    target_id       VARCHAR NOT NULL,
    edge_type       VARCHAR NOT NULL,
    edge_weight     FLOAT NOT NULL,
    is_bidirectional BOOLEAN DEFAULT TRUE,
    updated_at      TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),

    CHECK (edge_weight BETWEEN 0 AND 1)
);
```

Example edges:

```sql
INSERT INTO CTX_EDGES
    (source_id, target_id, edge_type, edge_weight)
VALUES
    (
        'agent_invoice_processor',
        'skill_invoice_extract',
        'uses_skill',
        0.95
    ),
    (
        'agent_invoice_processor',
        'mcp_gmail',
        'reads_from',
        0.85
    ),
    (
        'agent_invoice_processor',
        'harness_postgres',
        'writes_through',
        0.80
    );
```

---

## 6. Add the Type-Affinity Matrix

Some entity relationships are naturally stronger than others.

```sql
CREATE OR REPLACE TABLE CTX_TYPE_AFFINITY (
    source_type VARCHAR,
    target_type VARCHAR,
    affinity    FLOAT,
    PRIMARY KEY (source_type, target_type)
);
```

```sql
INSERT INTO CTX_TYPE_AFFINITY VALUES
    ('skill',      'agent',      1.00),
    ('agent',      'skill',      1.00),

    ('skill',      'mcp-server', 0.90),
    ('mcp-server', 'skill',      0.90),

    ('skill',      'harness',    0.75),
    ('harness',    'skill',      0.75),

    ('agent',      'mcp-server', 0.65),
    ('mcp-server', 'agent',      0.65),

    ('agent',      'harness',    0.70),
    ('harness',    'agent',      0.70),

    ('mcp-server', 'harness',    0.60),
    ('harness',    'mcp-server', 0.60);
```

Construct a directional adjacency view, including reverse edges where permitted:

```sql
CREATE OR REPLACE VIEW CTX_RAW_ADJACENCY AS

SELECT
    source_id AS node_id,
    target_id AS neighbour_id,
    edge_type,
    edge_weight
FROM CTX_EDGES

UNION ALL

SELECT
    target_id AS node_id,
    source_id AS neighbour_id,
    edge_type,
    edge_weight
FROM CTX_EDGES
WHERE is_bidirectional;
```

Now apply type affinity:

```sql
CREATE OR REPLACE VIEW CTX_ADJACENCY AS
SELECT
    a.node_id,
    a.neighbour_id,
    a.edge_type,
    a.edge_weight,
    COALESCE(ta.affinity, 0.35) AS type_affinity,

    a.edge_weight
        * COALESCE(ta.affinity, 0.35)
        * COALESCE(dst.quality_score, 1.0)
        AS effective_weight

FROM CTX_RAW_ADJACENCY a

JOIN CTX_ENTITIES src
    ON src.entity_id = a.node_id

JOIN CTX_ENTITIES dst
    ON dst.entity_id = a.neighbour_id

LEFT JOIN CTX_TYPE_AFFINITY ta
    ON  ta.source_type = src.entity_type
    AND ta.target_type = dst.entity_type

WHERE src.status = 'active'
  AND dst.status = 'active';
```

The effective traversal weight is therefore:

$$
w_{\text{effective}}(u,v)
=
w_{\text{edge}}(u,v)
\cdot
A(type(u),type(v))
\cdot
q(v)
$$

where $q(v)$ is the candidate’s quality score.

---

# 7. Tokenize the Entity Metadata

Semantic retrieval handles meaning. For exact terms such as `postgresql`, `jira`, `netsuite`, or `gmail`, we also want lexical evidence.

We first produce a field-aware token table.

```sql
CREATE OR REPLACE TABLE CTX_ENTITY_TOKENS AS

WITH fields AS (

    SELECT
        entity_id,
        'slug' AS field_name,
        LOWER(COALESCE(slug, '')) AS field_text
    FROM CTX_ENTITIES

    UNION ALL

    SELECT
        entity_id,
        'name',
        LOWER(COALESCE(display_name, ''))
    FROM CTX_ENTITIES

    UNION ALL

    SELECT
        entity_id,
        'description',
        LOWER(COALESCE(description, ''))
    FROM CTX_ENTITIES

    UNION ALL

    SELECT
        entity_id,
        'tag',
        LOWER(COALESCE(ARRAY_TO_STRING(tags, ' '), ''))
    FROM CTX_ENTITIES
),

cleaned AS (
    SELECT
        entity_id,
        field_name,
        REGEXP_REPLACE(
            field_text,
            '[^a-z0-9_+#.-]+',
            ' '
        ) AS normalized_text
    FROM fields
)

SELECT DISTINCT
    entity_id,
    field_name,
    TRIM(tokens.value::VARCHAR) AS token

FROM cleaned,
LATERAL SPLIT_TO_TABLE(normalized_text, ' ') tokens

WHERE TRIM(tokens.value::VARCHAR) <> '';
```

Keeping `field_name` allows us to score a slug match more strongly than a casual description match.

---

# 8. Calculate IDF in Snowflake

Document frequency is:

$$
df(t)
=
\left|
{e:t\in e}
\right|
$$

```sql
CREATE OR REPLACE TABLE CTX_TERM_STATS AS

WITH entity_count AS (
    SELECT COUNT(*) AS total_entities
    FROM CTX_ENTITIES
    WHERE status = 'active'
),

document_frequency AS (
    SELECT
        token,
        COUNT(DISTINCT entity_id) AS df
    FROM CTX_ENTITY_TOKENS
    GROUP BY token
),

raw_idf AS (
    SELECT
        d.token,
        d.df,
        n.total_entities,

        LN(
            (n.total_entities + 1.0)
            /
            (d.df + 1.0)
        ) AS idf

    FROM document_frequency d
    CROSS JOIN entity_count n
)

SELECT
    token,
    df,
    total_entities,
    idf,

    IFF(
        MAX(idf) OVER () = 0,
        0,
        idf / MAX(idf) OVER ()
    ) AS normalized_idf

FROM raw_idf;
```

Now common terms receive very small weights, while rare product or domain terms receive larger weights.

---

# 9. Start a Recommendation Query

Assume the developer asks:

```text
I need an agent that reads invoice attachments from Gmail
and writes the extracted fields to PostgreSQL.
```

Store the query and its embedding in a temporary table:

```sql
SET query_text =
    'I need an agent that reads invoice attachments from Gmail
     and writes the extracted fields to PostgreSQL.';

CREATE OR REPLACE TEMP TABLE Q_CONTEXT AS
SELECT
    $query_text::VARCHAR AS query_text,

    AI_EMBED(
        'snowflake-arctic-embed-m-v1.5',
        $query_text
    ) AS query_embedding;
```

---

# 10. Retrieve Semantic Seed Nodes

```sql
CREATE OR REPLACE TEMP TABLE Q_SEMANTIC_SEEDS AS

WITH scored AS (
    SELECT
        e.entity_id,
        e.entity_type,
        e.display_name,

        GREATEST(
            0.0,
            VECTOR_COSINE_SIMILARITY(
                e.embedding,
                q.query_embedding
            )
        ) AS semantic_score

    FROM CTX_ENTITIES e
    CROSS JOIN Q_CONTEXT q

    WHERE e.status = 'active'
      AND e.embedding IS NOT NULL
)

SELECT *
FROM scored
WHERE semantic_score >= 0.20
ORDER BY semantic_score DESC
LIMIT 50;
```

`VECTOR_COSINE_SIMILARITY` returns a value from $-1$ to $1$. Here, negative similarity is clamped to zero because it does not provide useful positive ranking evidence. ([Snowflake Documentation][3])

These are not yet the final recommendations. They are the starting nodes for graph discovery.

---

# 11. Compute the Lexical IDF Score

First tokenize the query:

```sql
CREATE OR REPLACE TEMP TABLE Q_TOKENS AS
SELECT DISTINCT
    TRIM(tokens.value::VARCHAR) AS token

FROM TABLE(
    SPLIT_TO_TABLE(
        REGEXP_REPLACE(
            LOWER($query_text),
            '[^a-z0-9_+#.-]+',
            ' '
        ),
        ' '
    )
) tokens

WHERE TRIM(tokens.value::VARCHAR) <> '';
```

Then match the query tokens against entity fields:

```sql
CREATE OR REPLACE TEMP TABLE Q_LEXICAL AS

SELECT
    et.entity_id,

    SUM(
        CASE et.field_name
            WHEN 'slug'        THEN 50
            WHEN 'name'        THEN 20
            WHEN 'tag'         THEN 10
            WHEN 'description' THEN 4
            ELSE 0
        END
        *
        (1 + COALESCE(ts.normalized_idf, 0))
    ) AS lexical_score

FROM Q_TOKENS qt

JOIN CTX_ENTITY_TOKENS et
    ON et.token = qt.token

LEFT JOIN CTX_TERM_STATS ts
    ON ts.token = qt.token

GROUP BY et.entity_id;
```

This means an exact rare slug match can contribute:

$$
50(1+IDF_{\text{norm}})
$$

while a description match contributes:

$$
4(1+IDF_{\text{norm}})
$$

The same token is therefore weighted according to both rarity and where it occurred.

---

# 12. Walk the Graph with Decay

Snowflake recursive CTEs can repeatedly traverse hierarchical or graph-shaped relationships while carrying state from one level to the next. ([Snowflake Documentation][4])

We begin from the strongest semantic seeds and walk at most three hops.

```sql
CREATE OR REPLACE TEMP TABLE Q_GRAPH AS

WITH RECURSIVE walk (
    seed_id,
    node_id,
    hop,
    path_strength,
    visited_path
) AS (

    -- Anchor: semantic seed nodes
    SELECT
        entity_id AS seed_id,
        entity_id AS node_id,
        0 AS hop,
        semantic_score AS path_strength,
        '|' || entity_id || '|' AS visited_path

    FROM Q_SEMANTIC_SEEDS
    WHERE semantic_score >= 0.35

    UNION ALL

    -- Recursive graph expansion
    SELECT
        w.seed_id,
        a.neighbour_id AS node_id,
        w.hop + 1 AS hop,

        w.path_strength
            * a.effective_weight
            AS path_strength,

        w.visited_path
            || a.neighbour_id
            || '|'
            AS visited_path

    FROM walk w

    JOIN CTX_ADJACENCY a
        ON a.node_id = w.node_id

    WHERE w.hop < 3

      -- Avoid cycles within the same path
      AND POSITION(
          '|' || a.neighbour_id || '|'
          IN w.visited_path
      ) = 0

      -- Stop carrying extremely weak paths
      AND w.path_strength * a.effective_weight >= 0.02
)

SELECT
    node_id AS entity_id,

    LEAST(
        1.0,
        SUM(
            path_strength
            /
            (hop + 1)
        )
    ) AS graph_score,

    COUNT(*) AS supporting_paths,
    MIN(hop) AS nearest_hop

FROM walk

WHERE hop > 0
GROUP BY node_id;
```

The contribution from one path is:

$$
S(n,p)
=
S_{\text{seed}}
\left(
\prod_{e\in p}w_{\text{effective}}(e)
\right)
\frac{1}{h+1}
$$

Consider a seed score of $0.90$, followed by two edges with effective weights $0.80$ and $0.75$.

At hop two:

$$
S
=
0.90
\times 0.80
\times 0.75
\times \frac13
$$

$$
S=0.18
$$

The candidate remains discoverable, but it cannot inherit the seed’s full score.

---

# 13. Calculate Node Degrees

Adamic–Adar requires the degree of each shared neighbour.

```sql
CREATE OR REPLACE VIEW CTX_NODE_DEGREE AS
SELECT
    node_id AS entity_id,
    COUNT(DISTINCT neighbour_id) AS degree
FROM CTX_ADJACENCY
GROUP BY node_id;
```

---

# 14. Build the Candidate Universe

A candidate can enter through:

* Semantic retrieval.
* Lexical matching.
* Graph traversal.

```sql
CREATE OR REPLACE TEMP TABLE Q_CANDIDATES AS

SELECT entity_id FROM Q_SEMANTIC_SEEDS

UNION

SELECT entity_id FROM Q_LEXICAL

UNION

SELECT entity_id FROM Q_GRAPH;
```

This is important.

A PostgreSQL harness may not be one of the top semantic matches for “invoice attachment,” but it can still enter through:

* The exact token `postgresql`.
* A structural connection to an invoice-processing agent.
* Shared graph neighbours.

---

# 15. Calculate Adamic–Adar

Two entities receive Adamic–Adar evidence when they share neighbours.

```sql
CREATE OR REPLACE TEMP TABLE Q_ADAMIC_ADAR AS

SELECT
    candidate_side.node_id AS entity_id,

    LEAST(
        1.0,

        SUM(
            seeds.semantic_score
            *
            seed_side.effective_weight
            *
            candidate_side.effective_weight
            /
            LN(
                GREATEST(
                    common_degree.degree,
                    2
                )
            )
        )
    ) AS adamic_adar_score

FROM Q_SEMANTIC_SEEDS seeds

-- Neighbours belonging to the semantic seed
JOIN CTX_ADJACENCY seed_side
    ON seed_side.node_id = seeds.entity_id

-- Candidates sharing the same neighbour
JOIN CTX_ADJACENCY candidate_side
    ON candidate_side.neighbour_id =
       seed_side.neighbour_id

JOIN Q_CANDIDATES candidates
    ON candidates.entity_id =
       candidate_side.node_id

JOIN CTX_NODE_DEGREE common_degree
    ON common_degree.entity_id =
       seed_side.neighbour_id

WHERE candidate_side.node_id <> seeds.entity_id

GROUP BY candidate_side.node_id;
```

The weighted form being calculated is:

$$
AA(c,s)
=
\sum_{z\in\Gamma(c)\cap\Gamma(s)}
\frac{
S_{\text{semantic}}(s)
\cdot w(c,z)
\cdot w(s,z)
}{
\log(\max(\deg(z),2))
}
$$

This rewards candidates that share specific, meaningful neighbours with strong semantic seeds.

A generic hub contributes little because its degree appears in the denominator.

---

# 16. Calculate Semantic Scores for Every Candidate

The first semantic query retrieved only the top seeds. We now calculate semantic similarity for every candidate discovered by any channel.

```sql
CREATE OR REPLACE TEMP TABLE Q_FEATURES AS

SELECT
    c.entity_id,
    e.entity_type,
    e.display_name,
    e.slug,

    GREATEST(
        0.0,
        VECTOR_COSINE_SIMILARITY(
            e.embedding,
            q.query_embedding
        )
    ) AS semantic_raw,

    COALESCE(g.graph_score, 0) AS graph_raw,
    COALESCE(aa.adamic_adar_score, 0) AS adamic_adar_raw,
    COALESCE(l.lexical_score, 0) AS lexical_raw,

    LN(
        1 + COALESCE(d.degree, 0)
    ) AS degree_raw,

    COALESCE(g.supporting_paths, 0) AS supporting_paths,
    g.nearest_hop

FROM Q_CANDIDATES c

JOIN CTX_ENTITIES e
    ON e.entity_id = c.entity_id

CROSS JOIN Q_CONTEXT q

LEFT JOIN Q_GRAPH g
    ON g.entity_id = c.entity_id

LEFT JOIN Q_ADAMIC_ADAR aa
    ON aa.entity_id = c.entity_id

LEFT JOIN Q_LEXICAL l
    ON l.entity_id = c.entity_id

LEFT JOIN CTX_NODE_DEGREE d
    ON d.entity_id = c.entity_id

WHERE e.status = 'active';
```

The logarithm prevents raw node degree from dominating:

$$
S_{\text{degree}}
=
\log(1+\deg(n))
$$

---

# 17. Normalize the Signals

The semantic score may already be between zero and one, while lexical scores may reach several hundred. They cannot be added directly.

```sql
CREATE OR REPLACE TEMP TABLE Q_NORMALIZED AS

WITH bounds AS (
    SELECT
        MIN(semantic_raw)     AS semantic_min,
        MAX(semantic_raw)     AS semantic_max,

        MIN(graph_raw)        AS graph_min,
        MAX(graph_raw)        AS graph_max,

        MIN(adamic_adar_raw)  AS aa_min,
        MAX(adamic_adar_raw)  AS aa_max,

        MIN(lexical_raw)      AS lexical_min,
        MAX(lexical_raw)      AS lexical_max,

        MIN(degree_raw)       AS degree_min,
        MAX(degree_raw)       AS degree_max

    FROM Q_FEATURES
)

SELECT
    f.*,

    IFF(
        b.semantic_max = b.semantic_min,
        IFF(f.semantic_raw > 0, 1, 0),
        (f.semantic_raw - b.semantic_min)
        /
        NULLIF(b.semantic_max - b.semantic_min, 0)
    ) AS semantic_score,

    IFF(
        b.graph_max = b.graph_min,
        IFF(f.graph_raw > 0, 1, 0),
        (f.graph_raw - b.graph_min)
        /
        NULLIF(b.graph_max - b.graph_min, 0)
    ) AS graph_score,

    IFF(
        b.aa_max = b.aa_min,
        IFF(f.adamic_adar_raw > 0, 1, 0),
        (f.adamic_adar_raw - b.aa_min)
        /
        NULLIF(b.aa_max - b.aa_min, 0)
    ) AS adamic_adar_score,

    IFF(
        b.lexical_max = b.lexical_min,
        IFF(f.lexical_raw > 0, 1, 0),
        (f.lexical_raw - b.lexical_min)
        /
        NULLIF(b.lexical_max - b.lexical_min, 0)
    ) AS lexical_score,

    IFF(
        b.degree_max = b.degree_min,
        IFF(f.degree_raw > 0, 1, 0),
        (f.degree_raw - b.degree_min)
        /
        NULLIF(b.degree_max - b.degree_min, 0)
    ) AS degree_score

FROM Q_FEATURES f
CROSS JOIN bounds b;
```

This converts every feature to approximately:

$$
[0,1]
$$

---

# 18. Combine the Signals

```sql
CREATE OR REPLACE TEMP TABLE Q_SCORED AS

SELECT
    *,

    0.40 * semantic_score
    +
    0.20 * graph_score
    +
    0.15 * adamic_adar_score
    +
    0.20 * lexical_score
    +
    0.05 * degree_score
    AS final_score

FROM Q_NORMALIZED;
```

The initial weighting is:

| Signal              | Weight |
| ------------------- | -----: |
| Semantic similarity |   0.40 |
| Graph walk          |   0.20 |
| Adamic–Adar         |   0.15 |
| IDF lexical match   |   0.20 |
| Graph degree        |   0.05 |

The weights add to one:

$$
0.40+0.20+0.15+0.20+0.05=1
$$

These should eventually be learned from telemetry, but they are a reasonable starting configuration.

---

# 19. Apply a Dynamic Noise Floor

A fixed cutoff is too brittle. Instead, combine:

* An absolute floor.
* A fraction of the highest score.
* The 30th percentile of the candidate distribution.

Snowflake’s `PERCENTILE_CONT` returns the selected percentile, interpolating when the percentile lies between observed values. ([Snowflake Documentation][5])

```sql
WITH score_distribution AS (
    SELECT
        MAX(final_score) AS max_score,

        PERCENTILE_CONT(0.30)
            WITHIN GROUP (
                ORDER BY final_score
            ) AS percentile_30

    FROM Q_SCORED
),

threshold AS (
    SELECT
        GREATEST(
            0.20,
            0.30 * max_score,
            percentile_30
        ) AS noise_floor

    FROM score_distribution
)

SELECT
    s.entity_id,
    s.entity_type,
    s.display_name,
    s.slug,

    ROUND(s.final_score, 4) AS normalized_score,

    3 + LEAST(
        FLOOR(s.final_score * 12),
        12
    ) AS priority,

    ROUND(
        0.60 + s.final_score * 0.35,
        3
    ) AS confidence,

    s.semantic_score,
    s.graph_score,
    s.adamic_adar_score,
    s.lexical_score,
    s.degree_score,

    s.supporting_paths,
    s.nearest_hop,

    t.noise_floor

FROM Q_SCORED s
CROSS JOIN threshold t

WHERE s.final_score >= t.noise_floor

ORDER BY
    s.final_score DESC,
    s.supporting_paths DESC,
    s.display_name

LIMIT 20;
```

The threshold is:

$$
\tau
=
\max
\left(
0.20,
0.30S_{\max},
P_{30}(S)
\right)
$$

Candidates below $\tau$ disappear entirely.

That is much better than returning:

> “Here are 50 recommendations. The final 38 are spiritually related to your query.”

---

# 20. Return Explainable Recommendations

A recommendation system should show why each candidate was selected.

```sql
SELECT
    entity_id,
    display_name,
    entity_type,
    final_score,

    OBJECT_CONSTRUCT(
        'semantic_similarity', semantic_score,
        'graph_relevance', graph_score,
        'shared_neighbours', adamic_adar_score,
        'exact_term_match', lexical_score,
        'popularity_prior', degree_score,
        'supporting_paths', supporting_paths,
        'nearest_hop', nearest_hop
    ) AS score_explanation

FROM Q_SCORED
ORDER BY final_score DESC;
```

An application can turn this into explanations such as:

```text
Gmail MCP Server

Recommended because:
• Exact match for “Gmail”
• Semantically relevant to email attachments
• Directly connected to the Invoice Processing Agent
• Supported by three independent graph paths
```

This is far more useful than showing a mysterious score of `0.8732`.

---

# 21. Package It Behind a Stored Procedure

The individual temporary tables are excellent for debugging. For application use, wrap the pipeline in a Snowpark Python stored procedure:

```text
recommend_tools(
    query_text,
    requested_types,
    max_results,
    max_hops
)
```

Conceptually:

```python
def recommend_tools(
    session,
    query_text: str,
    requested_types: list[str] | None = None,
    max_results: int = 20,
    max_hops: int = 3,
):
    # 1. Generate query embedding.
    # 2. Retrieve semantic seeds.
    # 3. Extract lexical tokens.
    # 4. Run bounded recursive graph expansion.
    # 5. Calculate Adamic–Adar.
    # 6. Join and normalize features.
    # 7. Apply dynamic threshold.
    # 8. Return ranked recommendations.
    ...
```

Snowpark DataFrames are lazily evaluated relational datasets, making them useful when the orchestration becomes too cumbersome for one large SQL statement. ([Snowflake Documentation][6])

The application call can then be as simple as:

```sql
CALL RECOMMEND_TOOLS(
    'Read Gmail invoice attachments and write the fields to PostgreSQL',
    ARRAY_CONSTRUCT(
        'skill',
        'agent',
        'mcp-server',
        'harness'
    ),
    20,
    3
);
```

---

# 22. Keep the Index Fresh

The recommendation index changes whenever:

* A skill is added.
* A description is edited.
* Tags change.
* An integration is deprecated.
* A graph edge is created or removed.
* Telemetry changes a quality score.

A production pipeline can use:

```text
Source tables
    ↓
Streams detect changes
    ↓
Tasks process changed rows
    ↓
Embeddings and tokens refresh
    ↓
Graph statistics refresh
```

Snowflake streams record table-level DML changes, while tasks can continuously process newly inserted or changed rows. ([Snowflake Documentation][7])

A simplified setup looks like:

```sql
CREATE OR REPLACE STREAM CTX_ENTITY_STREAM
ON TABLE CTX_ENTITY_SOURCE;
```

```sql
CREATE OR REPLACE TASK CTX_REFRESH_ENTITY_INDEX
    WAREHOUSE = CTX_COMPUTE
    SCHEDULE = '5 MINUTE'
    WHEN SYSTEM$STREAM_HAS_DATA('CTX_ENTITY_STREAM')
AS
    CALL REFRESH_CTX_ENTITY_INDEX();
```

The refresh procedure should:

1. Rebuild `search_text` only for changed entities.
2. Generate embeddings only when relevant text changed.
3. Refresh tokens for changed entities.
4. Recalculate document frequencies for affected terms.
5. Recalculate degrees for affected graph nodes.

Do not regenerate every embedding whenever one tag changes somewhere. Snowflake credits will begin performing Adamic–Adar directly on your bank account.

---

# 23. Use Cortex Search for Low-Latency Seed Retrieval

The pure SQL vector query is ideal for:

* Building the first version.
* Offline evaluation.
* Weight tuning.
* Inspecting every intermediate signal.

For a serving path with higher request volume, Cortex Search can become the first-stage semantic retriever. Cortex Search provisions a query endpoint and can be called through Python, REST, or SQL’s `SEARCH_PREVIEW`; it also supports multiple indexed fields and custom embeddings. ([Snowflake Documentation][8])

The architecture becomes:

```text
User query
    ↓
Cortex Search returns top 50 semantic seeds
    ↓
Snowflake SQL expands the graph
    ↓
IDF + Adamic–Adar reranking
    ↓
Dynamic noise-floor filtering
    ↓
Top 10 recommendations
```

Cortex Search handles candidate retrieval.

The custom Snowflake ranking pipeline handles:

* Graph structure.
* Type affinity.
* Shared-neighbour scoring.
* Business rules.
* Telemetry.
* Thresholding.
* Explainability.

---

# 24. Final Snowflake Architecture

```text
┌─────────────────────────────────────┐
│ CTX_ENTITIES                        │
│ Metadata, tags, text and embeddings │
└──────────────────┬──────────────────┘
                   │
                   ├──── Cosine similarity
                   │
                   ▼
          Semantic seed candidates
                   │
                   ▼
┌─────────────────────────────────────┐
│ CTX_EDGES + CTX_TYPE_AFFINITY       │
│ Weighted recommendation graph       │
└──────────────────┬──────────────────┘
                   │
                   ├──── Recursive CTE
                   ├──── Hop decay
                   └──── Path aggregation
                   │
                   ▼
          Graph-derived candidates
                   │
                   ▼
┌─────────────────────────────────────┐
│ CTX_ENTITY_TOKENS + TERM_STATS      │
│ Exact matching and normalized IDF   │
└──────────────────┬──────────────────┘
                   │
                   ▼
     Semantic + lexical + graph joins
                   │
                   ├──── Adamic–Adar
                   ├──── Degree prior
                   ├──── Min-max normalization
                   ├──── Weighted final score
                   └──── Dynamic threshold
                   │
                   ▼
┌─────────────────────────────────────┐
│ Ranked recommendations              │
│ Skills, agents, MCPs and harnesses  │
└─────────────────────────────────────┘
```

The key design decision is that Snowflake is not merely storing the recommendation data.

It is executing the recommendation mathematics:

$$
\boxed{
S(n)
=
0.40S_{\text{semantic}}
+
0.20S_{\text{walk}}
+
0.15S_{\text{AA}}
+
0.20S_{\text{IDF}}
+
0.05S_{\text{degree}}
}
$$

followed by:

$$
\boxed{
S(n)\geq
\max
\left(
\tau_{\min},
\alpha S_{\max},
P_{30}(S)
\right)
}
$$

Vector search finds what sounds relevant.

The graph finds what belongs together.

IDF protects exact technical intent.

Adamic–Adar detects structurally meaningful relationships.

Decay stops the graph from wandering into the wilderness.

The noise floor makes sure the wilderness never reaches the user. 🔥

[1]: https://docs.snowflake.com/en/user-guide/snowflake-cortex/vector-embeddings "Vector Embeddings | Snowflake Documentation"
[2]: https://docs.snowflake.com/en/sql-reference/functions/ai_embed "AI_EMBED | Snowflake Documentation"
[3]: https://docs.snowflake.com/en/sql-reference/functions/vector_cosine_similarity "VECTOR_COSINE_SIMILARITY"
[4]: https://docs.snowflake.com/en/user-guide/queries-hierarchical "Querying Hierarchical Data"
[5]: https://docs.snowflake.com/en/sql-reference/functions/percentile_cont "PERCENTILE_CONT"
[6]: https://docs.snowflake.com/en/developer-guide/snowpark/python/working-with-dataframes "Working with DataFrames in Snowpark Python"
[7]: https://docs.snowflake.com/en/user-guide/data-pipelines-intro "Introduction to streams and tasks"
[8]: https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search/cortex-search-overview "Cortex Search"
