---
name: phylogenetics
description: Builds and reads evolutionary trees from aligned sequences using pairwise distances (p-distance, Jukes-Cantor), UPGMA and neighbour-joining trees in Newick format, rooting, and the limits of distance methods compared with parsimony, maximum likelihood and Bayesian inference. Use for "build a tree from these sequences", "what is the distance between these", "UPGMA or neighbour-joining", "read this Newick string", "is this tree reliable", "how do I root a tree". Use sequence-alignment to align sequences first, sequence-formats to read the alignment file, and sequence-statistics for support and significance questions.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Phylogenetics

## Purpose and activation

Turn aligned sequences into a tree and say how much of the tree is data and how much is method.
A tree is a hypothesis about common ancestry, not an observation. Activate when the user wants
relationships among sequences or species, a distance matrix, or help interpreting a tree.

## Required inputs

An alignment of homologous sequences (not a pile of similar ones); the sequence type and gene or
region; whether an outgroup is known; the question (relationships, divergence times, or just a
guide tree); and the number of taxa, since some methods do not scale.

## Workflow

1. **Check the alignment first.** A tree is only as good as the alignment. Columns with many gaps
   or doubtful homology should be inspected or removed (`sequence-alignment`).
2. **Compute distances.** `python3 scripts/tree.py distances ALIGNED.fasta --model jc` writes a CSV
   matrix. p-distance is the fraction of differing sites; Jukes-Cantor corrects for multiple
   changes at one site and is undefined from p = 0.75.
3. **Choose the method.** Neighbour-joining for an unrooted tree from distances, without assuming a
   constant rate. UPGMA only when a molecular clock is plausible, since it forces all tips to the
   same height.
4. **Build.** `tree.py nj MATRIX.csv` or `tree.py upgma MATRIX.csv`; both print Newick with branch lengths.
5. **Root with evidence.** Neighbour-joining output is unrooted. Root with an outgroup or a
   stated assumption such as a clock, and say which.
6. **Test support.** Distance trees from one run carry no confidence. Resample columns
   (bootstrap) and report the fraction of trees containing each branch (VERIFY a tool).
7. **Cross-check** with a second method (parsimony, maximum likelihood or Bayesian) from an
   established package when the tree will be reported (`references/methods.md`).
8. **Report** the alignment, the model, the method, the root, and the support.

## Decision framework

| Situation | Choice |
|---|---|
| Quick guide tree, many sequences | Neighbour-joining |
| Closely related sequences with a plausible clock | UPGMA is acceptable |
| Rates differ among lineages | Neighbour-joining or a likelihood method, not UPGMA |
| Distances above about 0.5 substitutions per site | Expect saturation; use a model-based method |
| Few informative sites | Low resolution; report it |
| A tree for publication | Likelihood or Bayesian method with support values |
| Gene sequences from different species | A gene tree; it may differ from the species tree |

## Implementation guidance

- The distance script reads an aligned FASTA file, ignores sites where either sequence has a gap
  or an ambiguity code, and refuses unequal lengths.
- Newick format: parentheses group descendants, `name:length` gives branch length, `;` ends the
  tree. UPGMA output is rooted. Neighbour-joining output is a trifurcation at the last node and is
  unrooted; do not read it as a rooted tree.
- Sibling order in the output is by alphabetical first leaf, so output is repeatable. Order of
  siblings carries no meaning.
- Neighbour-joining can return negative branch lengths when distances are not additive. The
  script reports them as computed; they are a sign the data do not fit a tree.
- The self-test builds known trees (a hand-made one and 25 random ones), derives the distance
  matrix from them, and checks that neighbour-joining returns the same topology and the same
  distances. It also checks UPGMA on hand-worked examples.

## Failure and edge cases

- **Wrong alignment** producing a confident, wrong tree.
- **Paralogs mixed with orthologs,** making the tree describe gene duplication instead of species.
- **Long-branch attraction:** fast-evolving lineages grouped together by chance (VERIFY).
- **Saturation:** at large distances the corrected distances become noisy or undefined.
- **Rooting by midpoint** or by convenience presented as fact.
- **Bootstrap values read as probabilities that the branch is true.**
- **Recombination or horizontal transfer,** which a single tree cannot represent.
- **Tip labels** containing parentheses, commas, colons or semicolons, which break Newick.
- **Reading branch order as ancestry.** Swapping sibling order changes nothing.

## Validation

- `python3 scripts/tree.py --selftest` must pass.
- Hand check: distances A-B 2, A-C 4, B-C 4 give UPGMA `((A:1,B:1):1,C:2);`.
- Hand check: p = 0.3 gives a Jukes-Cantor distance of 0.3831 (minus three quarters of ln 0.6).
- Hand check: for an additive matrix, tree path lengths reproduce the matrix exactly.
- Falsifier: relabel taxa and rebuild; the topology must not change.

## Expected output

The alignment used, the distance model, the method, the Newick string, the rooting and how it was
chosen, support values with their method, and the warnings that apply (saturation, clock
assumption, gene tree versus species tree).

## Sources and confidence

- Ramsden, *Bioinformatics: An Introduction*, 2nd ed.: ch. 10.8 (phylogeny and evolution, models
  of evolution, sources of genome variation, geological eras and taxonomy) and ch. 13.8
  (phylogenies): section titles only, from the table of contents; the text was not supplied
- Jukes-Cantor formula, UPGMA, neighbour-joining: standard methods, verified by hand-worked
  cases and by the recovery test in the self-test
- Model choice, bootstrap interpretation, long-branch attraction, rooting practice, Newick
  details: general knowledge, VERIFY against a phylogenetics text or the package documentation
- Not covered: likelihood or Bayesian inference, divergence-time dating, networks, supertrees
