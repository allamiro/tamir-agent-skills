# `phylogenetics` prompts

Build trees from aligned sequences, read Newick strings, and say how much of a tree is data and
how much is method.

- **Give it:** an alignment of homologous sequences, the gene or region, an outgroup if you have
  one, and what the tree is for
- **Skill file:** [`skills/phylogenetics/SKILL.md`](../skills/phylogenetics/SKILL.md)
- **Methods:** [`methods.md`](../skills/phylogenetics/references/methods.md)
- **Before it:** [`sequence-alignment`](sequence-alignment.md) · **For support:** [`sequence-statistics`](sequence-statistics.md)

## 1. Two kinds of distance

> Compute the p-distance and the Jukes-Cantor distance between ACGTACGTAC and ACGTACGTAA. Say when the Jukes-Cantor correction stops being usable.

A good answer: p = 0.1 and a Jukes-Cantor distance of about 0.107, which is undefined from
p = 0.75 because of saturation.

## 2. A UPGMA tree

> Build a UPGMA tree from the distances A-B 2, A-C 4, A-D 6, B-C 4, B-D 6, C-D 6 and write it in Newick format. Say what assumption UPGMA makes.

A good answer: (((A:1,B:1):1,C:2):1,D:3); and the assumption of a constant rate, so all tips end
at the same height.

## 3. The same matrix by neighbour-joining

> Build the neighbour-joining tree from the same matrix. Does it agree with the UPGMA tree, and why does the Newick string look different?

A good answer: the same unrooted tree, written as ((A:1,B:1):1,C:2,D:4); the UPGMA tree is rooted,
and merging its two root branches (1 and 3) gives the single branch of length 4 to D.

## 4. Which method

> My sequences evolve at very different speeds in different lineages. Should I use UPGMA? What should I use instead, and what would I want for a published tree?

A good answer: not UPGMA, since it assumes a clock; neighbour-joining for a quick guide tree, and
a likelihood or Bayesian method with support values for publication.

## 5. A distance that does not exist

> Two of my sequences differ at 76% of the compared sites. What does the Jukes-Cantor distance give, and what should I do?

A good answer: it is undefined at 0.75 or above, the pair is saturated, and the fix is a better
model, a slower-evolving region, or leaving the pair out; not capping the number.

## 6. Reading a Newick string

> Explain ((A:1,B:1):1,C:2); in words: which taxa group together, how long is each branch, and what does swapping A and B change?

A good answer: A and B share an ancestor one unit from each, that ancestor is one unit from the
root, and C is two units from the root; swapping A and B changes nothing.
