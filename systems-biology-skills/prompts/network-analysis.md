# `network-analysis` prompts

Represent interaction data as graphs, measure them, find motifs against a null model, and keep track of
where every edge came from.

- **Give it:** the edge list and its source (database, version, evidence, organism), whether edges are
  directed or signed, and the question
- **Skill file:** [`skills/network-analysis/SKILL.md`](../skills/network-analysis/SKILL.md)
- **Network medicine and provenance:** [`network-medicine.md`](../skills/network-analysis/references/network-medicine.md)

## 1. Feed-forward loops

> Find feed-forward loops in my regulatory network. Edges (directed): X Y, Y Z, X Z, Z W, W X. Build the adjacency matrix too, and tell me whether the motif is enriched.

A good answer: one feed-forward loop, X → Y → Z with X → Z. It gives the 4 × 4 adjacency matrix (rows from,
columns to). It says that one count cannot show enrichment: that needs comparison with degree-preserving
randomised networks and a z-score or empirical p-value, which is meaningless for a five-edge graph.

## 2. Hubs and bottlenecks

> In the undirected network A-B, B-C, C-D, B-E, E-F, which node is the hub and which the bottleneck? Give degree and betweenness.

A good answer: B has the highest degree (3) and the highest betweenness (0.8 normalised), so here the hub and
the bottleneck are the same node. In general they differ: degree counts neighbours, while betweenness counts
the shortest paths passing through a node.

## 3. Reactions as a graph

> How do I represent the reaction A + B -> C + D as a graph without losing information?

A good answer: a simple graph loses the fact that A and B react together. Use a bipartite graph with a node
for the reaction linked to its substrates and products, or a hypergraph whose hyperedge joins {A, B} to
{C, D}. The incidence matrix with −1 and +1 has the same sign convention as a stoichiometric matrix.

## 4. Network medicine

> We found 12 disease genes and want to propose new candidates using the protein interaction network. What is the approach and what biases should we watch for?

A good answer: look for a disease module, meaning genes connected to or near the known disease genes, and rank
candidates by network proximity. Check significance against random gene sets matched for degree. Watch for
study bias (well-studied proteins have more recorded interactions), an incomplete interactome, mixed evidence
types, and edges from other cell types or organisms. Record database versions.

## 5. Provenance

> We are merging interaction data from three databases and patient expression data. How do we record provenance so the network can be rebuilt?

A good answer: record for each entity its source database and release, download date and query; the
processing activity with script version and parameters; the agent responsible; and per-edge evidence and
publication identifiers. It follows the entity, activity and agent model of W3C PROV and stores
checksums.
