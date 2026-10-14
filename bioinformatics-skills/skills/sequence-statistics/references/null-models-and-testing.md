# Null models and testing

## Choosing a null model

| The data arose by | Null model | How to generate it |
|---|---|---|
| Independent positions with fixed base probabilities | Random sequence, same composition | Draw each base from the probabilities, or use `expect` for counts |
| A fixed set of letters in unknown order | Shuffle | Permute the letters of the observed sequence; composition is exactly preserved |
| Neighbouring-letter structure | Preserve dinucleotide counts | Use a dinucleotide-preserving shuffle (the method is specialised; VERIFY a tool) |
| Items drawn from a finite pool | Hypergeometric | `hypergeom` |
| Labels on samples | Permute the labels | Shuffle label columns, keep the data columns together |
| A network | Degree-preserving rewiring | Swap edge endpoints, keep each node's degree (VERIFY a tool) |

A shuffle null answers "same letters, no meaningful order". If the question is about composition
itself, shuffling hides it and a composition-aware null is needed.

## Empirical p-value

Generate B null values of the statistic. Then p = (1 + number of null values at least as extreme)
/ (1 + B). It cannot be 0, and it cannot be smaller than 1 / (1 + B), so B must be large enough
for the threshold you need: for a threshold of 0.001 use well over 1,000 shuffles. Record the seed.

## Overlapping words

Occurrences of a word that can overlap itself (for example AAAA, or ACAC) are positively
correlated: one occurrence makes a neighbouring one more likely. The expected count from `expect`
stays correct, but the variance is larger than the binomial's, so a binomial tail is too
optimistic. A shuffle null handles this without any formula.

## Many tests

| Procedure | Controls | Use when |
|---|---|---|
| Bonferroni: p times the number of tests, capped at 1 | Probability of any false positive | A single false positive is costly, few tests |
| Benjamini-Hochberg | Expected fraction of false discoveries among those reported | Screening many features, follow-up will sort the leads |

Both need the full list of tests that were run. Dropping the boring ones before adjusting defeats
the correction. Benjamini-Hochberg assumes independent or positively dependent tests (VERIFY
the exact condition for your case).

## Effect size and context

Report the size of the difference with its interval, not only the p-value. State the sample size.
A very small p-value from a very large sample can describe a difference too small to matter.

## Likelihood

For data D and parameters theta, the likelihood L(theta) = P(D | theta) as a function of theta.
For independent positions the log-likelihood is a sum, which the script's `log_likelihood()`
computes. The maximum entropy method, named in the source's contents (ch. 5.5), picks the
distribution of greatest entropy consistent with stated constraints (VERIFY the details in a text).

## Markov chains

A first-order chain has transition probabilities P(next | current). If the chain can reach every
state from every other and is not periodic, it has one stationary distribution, reached from any
start; `stationary` finds it by repeated multiplication. For DNA, a first-order chain captures
dinucleotide bias that independent-position models miss.
