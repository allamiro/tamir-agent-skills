---
name: network-analysis
description: Represents and analyses biological networks as graphs, covering adjacency and incidence matrices, adjacency lists, directed, signed and hypergraph representations, degree, closeness and betweenness centrality, shortest paths, components, feed-forward and feedback loops, motif enrichment against randomised networks, and network and systems medicine with data provenance. Use for "build the adjacency matrix", "which nodes are hubs", "find feed-forward loops in my regulatory network", "is this motif enriched", "represent reactions as a hypergraph", "network medicine approach to this disease", "track provenance of my network data". Use stoichiometric-networks for mass-balanced reaction networks, linear-algebra-networks for matrix computations, and stochastic-discrete-models for Boolean dynamics on a network.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# Network analysis

## Purpose and activation

A graph view shows which components can influence which, before anything is known about rates.
It answers questions of connectivity, centrality and recurring patterns, and in network medicine it places
disease genes in modules of interacting proteins. It cannot answer questions about quantities or time.
Activate when the user has interaction data (protein interactions, regulation, signalling, metabolic
connectivity) and wants a representation, a measure or a pattern.

## Required inputs

The edge list with its source and evidence (database and version, experimental method, organism);
whether edges are directed and signed; what a node stands for (gene, protein, metabolite, reaction,
patient); and the question.

## Workflow

1. **Choose the representation.** Undirected for physical binding, directed for regulation, signed for
   activation and inhibition, bipartite or hypergraph for reactions (a reaction links several substrates to
   several products at once, which a simple graph cannot show without an extra node per reaction).
2. **Build the matrices** with `python3 scripts/graphs.py matrices EDGES.txt [--directed]`: the adjacency matrix (node by
   node), the incidence matrix (node by edge, -1 where an edge leaves and +1 where it enters, the same sign
   convention as a stoichiometric matrix) and the adjacency list.
3. **Measure** with `python3 scripts/graphs.py measures EDGES.txt`: degree, closeness, betweenness, components. Report
   what each measure means for the question; hubs by degree and bottlenecks by betweenness are different nodes.
4. **Find paths** with `python3 scripts/graphs.py path EDGES.txt --from A --to B`.
5. **Count motifs** with `python3 scripts/graphs.py motifs EDGES.txt`. A count is not an enrichment: compare with randomised
   networks that keep each node's in- and out-degree, and report the z-score or empirical p-value.
6. **Check the data's provenance** before interpreting: interaction databases mix evidence types, and
   well-studied genes have more recorded interactions (study bias). Record sources with the provenance
   fields in `references/network-medicine.md`.
7. **Interpret cautiously:** a central node is a hypothesis for an experiment, not a proven driver.

## Decision framework

| Question | Measure or method | Caveat |
|---|---|---|
| Most connected | Degree | Inflated by study bias |
| Information flow between modules | Betweenness | Depends on all shortest paths, sensitive to missing edges |
| Close to everything | Closeness | Undefined across disconnected components |
| Recurring circuit | Motif count plus degree-preserving randomisation | Many randomisations needed for small p-values |
| Disease module | Neighbourhood of known disease genes in the interactome | Incomplete interactome |
| Robustness | Remove nodes and track the largest component | Random failure and targeted attack differ |

## Failure and edge cases

- **Motif counts reported as significant** without a null model.
- **Mixing directed and undirected edges** in one adjacency matrix.
- **Hairballs:** a whole-interactome figure that shows nothing; filter by evidence or module first.
- **Study bias** read as biology (hubs are often the best-studied proteins).
- **Interactions from another organism or cell type** used without saying so.
- **Reaction networks drawn as simple graphs,** losing which substrates react together.
- **Database version not recorded,** so the network cannot be rebuilt.

## Validation

- `python3 scripts/graphs.py --selftest` passes.
- The sum of a directed adjacency matrix equals the number of edges; each incidence column sums to zero.
- Centrality rankings are stable when a small random share of edges is removed (report the check).
- Every edge source is recorded with database, version and evidence type.
- Falsifier: the result disappears when only high-confidence edges are kept.

## Expected output

The representation chosen and why; the matrices; the measures with their meaning; motifs with enrichment
against a stated null model; provenance records; and a list of hypotheses for experiments.

## Sources and confidence

- Sauter and Albrecht 2023, doi:10.11647/OBP.0291 (supplied text): incidence matrix, adjacency matrix and
  list, graph notation and hypergraphs (checklist Part 1); feed-forward and feedback loops (Part 3); systems
  medicine and network medicine (Part 0); W3C PROV for data provenance and the integration challenges of
  systems medicine (introduction, quoting Apweiler et al. 2018, doi:10.1038/emm.2017.290)
- Barabási, Gulbahce and Loscalzo, network medicine, doi:10.1038/nrg2918 (recommended by the book; Crossref
  dates it 2010 online, 2011 in print); Milo et al. 2002, doi:10.1126/science.298.5594.824, and Alon 2007,
  doi:10.1038/nrg2102, for motifs; Brandes 2001, doi:10.1080/0022250X.2001.9990249, for betweenness (records
  checked on Crossref 2026-10-15; content from author knowledge, VERIFY)
