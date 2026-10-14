# `network-analysis`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Find feed-forward loops in my regulatory network. Edges (directed): X Y, Y Z, X Z, Z W, W X. Build the adjacency matrix too, and tell me whether the motif is enriched.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 2,280 | 2,890 |
| Input tokens read across all turns (including cached context) | 83,703 | 235,037 |
| Extra input tokens when the skill is installed | | +151,333 |
| Cost, US dollars at list price | 0.128 | 0.243 |
| Skills invoked in the sample run | none | `network-analysis` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 280 tokens for its name and description, which are in every session where the skill is installed, and about 1,800 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
Your network has **one feed-forward loop** (X → Y → Z with the shortcut X → Z). With only 4 nodes and 5 edges, it is **not enriched** (p ≈ 0.29).

## Representation
I treated the edges as directed and unsigned, since you gave no activation or inhibition signs.

**Adjacency matrix** (rows = from, columns = to):

|   | X | Y | Z | W |
|---|---|---|---|---|
| **X** | 0 | 1 | 1 | 0 |
| **Y** | 0 | 0 | 1 | 0 |
| **Z** | 0 | 0 | 0 | 1 |
| **W** | 1 | 0 | 0 | 0 |

The matrix sums to 5, which matches the 5 edges.

**Incidence matrix** (−1 where an edge leaves a node, +1 where it enters):

|   | X→Y | Y→Z | X→Z | Z→W | W→X |
|---|---|---|---|---|---|
| X | −1 | 0 | −1 | 0 | +1 |
| Y | +1 | −1 | 0 | 0 | 0 |
| Z | 0 | +1 | +1 | −1 | 0 |
| W | 0 | 0 | 0 | +1 | −1 |

Each column sums to zero, as it should.

## Feed-forward loops
- **X → Y → Z, plus X → Z.** X is the master regulator, Y the intermediate and Z the target. This is the only one.
- The loop also sits inside **feedback cycles**: X→Y→Z→W→X and X→Z→W→X. So Z feeds back to X through W. Biologically this behaves differently from a stand-alone FFL. Whether it acts as a delay or pulse generator, or as an oscillator or switch, depends on the edge signs.

## Enrichment
A raw count isn't enough, so I compared it with randomised networks that keep each node's in- and out-degree. The network is small enough to list every possibility exactly: only **7 distinct networks** have this degree sequence (no self-loops).

- FFL counts across those 7 networks: 0, 1, 0, 0, 1, 0, 0
- Expected count: 2/7 ≈ 0.29. Observed: 1.
- **Exact p = P(count ≥ 1) = 2/7 ≈ 0.29**

The FFL is not enriched. More importantly, a network this size **can't show enrichment at all**: the smallest p-value possible here is 1/7. Motif enrichment only means something in networks with tens to thousands of edges, as in the E. coli and yeast studies (Milo et al. 2002; Alon 2007).

## Next steps
- **Edge signs:** with signs I can classify the FFL as coherent or incoherent, and the feedback loop as positive or negative. That classification says more about function here than enrichment does.
- **Source of the edges:** tell me the database and version, organism and evidence type so the network can be rebuilt. If this sub-network comes from a larger one, test enrichment on the full network. I can run that with many degree-preserving randomisations and report a z-score.
````

## Answer without the skill (excerpt)

````text
## Feed-forward loops

There is **one** feed-forward loop: **X → Y → Z, with a direct shortcut X → Z**.

- X is the top regulator, Y is the intermediate regulator and Z is the target.
- I checked every other set of three nodes and none forms an FFL. For example, X→Z→W does not count because the edge between W and X runs W → X, not X → W.

Your network also contains feedback cycles, which are a different kind of motif:
- a 3-node cycle X → Z → W → X
- a 4-node cycle X → Y → Z → W → X

## Adjacency matrix (rows = source, columns = target)

|       | X | Y | Z | W |
|-------|---|---|---|---|
| **X** | 0 | 1 | 1 | 0 |
| **Y** | 0 | 0 | 1 | 0 |
| **Z** | 0 | 0 | 0 | 1 |
| **W** | 1 | 0 | 0 | 0 |

## Is the motif enriched? No.

I compared your network against every possible random network of the same size:

| Null model | Random networks | Mean number of FFLs | P(≥1 FFL) |
|---|---|---|---|
| Same number of incoming and outgoing edges per node | 7 | 0.29 | **0.29** |
| Any network with 4 nodes and 5 edges | 792 | 1.09 | **0.71** |

- **Same-connections test:** this is the standard test, used by Milo et al. 2002. Two of the seven possible networks contain an FFL. Your network has more FFLs than the average random one, but a p-value of 0.29 is nowhere near significant.
- **Any-network test:** most random networks of this size contain at least one FFL. Here your network actually has slightly fewer FFLs than average.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
