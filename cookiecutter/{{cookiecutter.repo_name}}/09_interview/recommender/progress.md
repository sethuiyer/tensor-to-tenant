# Recommender progress

Complete the paired reading in order. Keep the production notes concrete:
name the signal, the failure mode it can hide, and the metric or alert that
would catch it.

## SEARCH.md — theory (17 sections)

- [ ] Section 1: Representing the Recommendation Space as a Graph
- [ ] Section 2: Semantic Similarity with Cosine Similarity
- [ ] Section 3: Length-Weighted Mean Pooling for Long Descriptions
- [ ] Section 4: Graph Traversal with Hop Decay
- [ ] Section 5: Adamic–Adar for Relationship Strength
- [ ] Section 6: Lexical Matching with IDF Weighting
- [ ] Section 7: Intent Signals and Controlled Boosting
- [ ] Section 8: Type Affinity
- [ ] Section 9: Dynamic Noise-Floor Filtering
- [ ] Section 10: Combining All Signals
- [ ] Section 11: From Ranking Score to Priority and Confidence
- [ ] Section 12: End-to-End Retrieval Pipeline
- [ ] Section 13: Python-Like Pseudocode
- [ ] Section 14: Important Production Problems
- [ ] Section 15: Improving the Model with Telemetry
- [ ] Section 16: Evaluation
- [ ] Section 17: The Core Intuition

## SNOWFLAKE.md — production (24 sections)

- [ ] Section 1: Create the Database Objects
- [ ] Section 2: Store the Entities
- [ ] Section 3: Build a Canonical Search Document
- [ ] Section 4: Generate the Embeddings
- [ ] Section 5: Store the Recommendation Graph
- [ ] Section 6: Add the Type-Affinity Matrix
- [ ] Section 7: Tokenize the Entity Metadata
- [ ] Section 8: Calculate IDF in Snowflake
- [ ] Section 9: Start a Recommendation Query
- [ ] Section 10: Retrieve Semantic Seed Nodes
- [ ] Section 11: Compute the Lexical IDF Score
- [ ] Section 12: Walk the Graph with Decay
- [ ] Section 13: Calculate Node Degrees
- [ ] Section 14: Build the Candidate Universe
- [ ] Section 15: Calculate Adamic–Adar
- [ ] Section 16: Calculate Semantic Scores for Every Candidate
- [ ] Section 17: Normalize the Signals
- [ ] Section 18: Combine the Signals
- [ ] Section 19: Apply a Dynamic Noise Floor
- [ ] Section 20: Return Explainable Recommendations
- [ ] Section 21: Package It Behind a Stored Procedure
- [ ] Section 22: Keep the Index Fresh
- [ ] Section 23: Use Cortex Search for Low-Latency Seed Retrieval
- [ ] Section 24: Final Snowflake Architecture

## Evidence

- Theory notes: `evidence/recommender/search.md`
- Production notes: `evidence/recommender/snowflake.md`
- Failure-mode / metric pair: `evidence/recommender/retrospective.md`
