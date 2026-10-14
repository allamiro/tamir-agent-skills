# Tree-building methods

Everything below the first table is general knowledge; VERIFY against a phylogenetics text before
relying on a statement.

## Families

| Family | Input | Idea | Strength | Weakness |
|---|---|---|---|---|
| Distance (UPGMA, neighbour-joining) | Pairwise distance matrix | Build a tree whose path lengths fit the distances | Fast, simple, scales to many taxa | Throws away site-level information |
| Parsimony | Aligned characters | Fewest changes | No model needed | Can mislead when rates are very uneven |
| Maximum likelihood | Aligned characters and a model | Tree and parameters that make the data most probable | Uses a substitution model, well studied | Slower; model must fit |
| Bayesian | Aligned characters, model and priors | Distribution over trees | Gives probabilities and handles uncertainty | Priors and convergence need care |

## UPGMA and neighbour-joining

| Property | UPGMA | Neighbour-joining |
|---|---|---|
| Rooted | Yes | No |
| Assumes a clock | Yes, all tips end at the same height | No |
| Output lengths | Height differences | Branch lengths that can be negative |
| Exact for | Ultrametric distances | Additive distances |
| Joining rule | Closest pair | Pair minimising Q, which corrects for each taxon's average distance |

For a pair i, j among m taxa: Q(i, j) = (m - 2) d(i, j) - r(i) - r(j), where r(i) is the sum of
the distances from i to all others. Neighbour-joining joins the pair with the smallest Q.

## Distances from sequences

| Distance | Formula | Valid for |
|---|---|---|
| p-distance | differing sites / compared sites | Very close sequences |
| Jukes-Cantor (JC69) | -3/4 ln(1 - 4p/3) | All substitutions equally likely and equal base frequencies; undefined at p >= 0.75 |

Real substitutions are not equally likely (transitions are commoner than transversions), and base
composition varies, so richer models exist. Use them through an established package.

## Reading a Newick string

`((A:1,B:1):1,C:2);` is a tree where A and B share an ancestor one unit from each, that ancestor
is one unit from the root, and C is two units from the root. In a rooted tree the root is the last
node; in a neighbour-joining tree the outermost parentheses are not a root, just a place to start
writing the unrooted tree.

## Support

Bootstrap: resample alignment columns with replacement, rebuild the tree, count how often each
branch appears. A value of 90% means 90% of resampled data sets gave that branch under the
method; it is not the probability the branch is correct. Bayesian posterior probabilities are a
different quantity with a different meaning.

## Common mistakes

- Using a tree from distances as if it were a likelihood result.
- Interpreting the horizontal order of tips.
- Calling a gene tree the species tree.
- Rooting by the longest branch because it looks right.
- Building from an alignment that includes non-homologous regions.
