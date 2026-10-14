# Networks

The source's interactomics chapter lists inference of regulatory networks, the physical chemistry
of interactions, in vivo and in vitro methods, interactions from sequence, and global statistics
of interactions; its systems chapter covers networks (graphs), trees, complexity parameters and
dynamical properties; its metabolomics chapter covers metabolic control analysis and metabolic
networks (section titles from the table of contents). The guidance below is general practice;
VERIFY it against the literature for your organism and method.

## What an edge means

| Source of the edge | It claims | It does not show |
|---|---|---|
| A measured physical interaction (two-hybrid, crosslinking, affinity capture, protein chip) | Two molecules were found together in that assay | That they interact in the cell, at that time, directly |
| Correlated expression | Two features rise and fall together | Any physical contact, regulation, or direction |
| Interaction predicted from sequence | A pattern like known interacting pairs | Anything about whether it occurs |
| Curated database entry | Someone reported it | That the report was right; entries carry their sources' errors |

## Error rates

Interaction assays have false positives and false negatives that differ by method. Overlap between
independent methods raises confidence. The usual practice is to keep a confidence score on every
edge and to compare against a reference set of known interactions and known non-interactions
(VERIFY the error rates for the assay in use).

## Networks from correlation

1. Compute a similarity (correlation) between every pair of features.
2. Choose a threshold or a statistical cut; each choice changes the network shape.
3. Report how the number of edges, the number of connected components and the largest hub change
   with the threshold. A result that exists at only one threshold is fragile.
4. Build the same network from shuffled data. If it looks similar, it is noise.
5. Remember indirect links: if A drives B and B drives C, A and C correlate without touching.

## Reading a graph

| Quantity | Meaning | Caution |
|---|---|---|
| Degree | Edges at a node | Study bias: well-studied molecules have more recorded edges |
| Hub | A node with unusually high degree | Hubs in assay data may be sticky molecules |
| Path length | Steps between nodes | Depends on missing edges |
| Connected component | A set of mutually reachable nodes | A threshold can split or merge them |
| Tree | A connected graph with no cycles | Most biological networks are not trees |

## Directed and dynamic networks

Regulatory networks have direction (who controls whom) that a correlation cannot supply. Time
series and perturbation experiments carry direction information; inference from them is hard and
needs validation against known regulation (VERIFY the method before use). Interactions are not
fixed constants: rates and occupancy change with concentration and time, and binding can be
specific, nonspecific or cooperative, the distinctions the source's contents list.

## Metabolic networks

Reactions link metabolites through enzymes; measuring metabolite levels does not give fluxes.
Metabolic control analysis asks how much each step controls the flux through a pathway (the
source lists it by name in its metabolomics chapter). Stoichiometry constrains what is possible but
not what happens; do not infer regulation from a reaction list alone.
