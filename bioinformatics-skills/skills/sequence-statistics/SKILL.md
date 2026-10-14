---
name: sequence-statistics
description: Counts, probabilities and significance for sequence questions, covering the four ways to sample, binomial and hypergeometric tails, expected counts of a word in random sequence, likelihood, Markov chains, null models by shuffling, and p-value adjustment for many tests (Bonferroni, Benjamini-Hochberg). Use for "is this motif enriched", "how often would this k-mer appear by chance", "what is the p-value", "correct for multiple testing", "how many sequences of length n are possible", "what is the stationary distribution of this chain". Use information-theory-sequences for entropy and conservation, sequence-alignment for alignment scores, and omics-data-analysis for expression tables.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Sequence statistics

## Purpose and activation

Answer "how surprising is this?" with a number whose assumptions are written down. A count, a
score or an enrichment means nothing until it is set against what chance would give. Activate
whenever a result is described as significant, enriched, over-represented, rare or unlikely, or
when someone has run many tests and wants to report the best ones.

## Required inputs

The observation (a count, a score, a list of p-values); the population it came from (sequence
length, number of positions, number of items drawn); the null model in words (what "just chance"
means here); the number of comparisons made, including the ones that were not reported; and the
base composition if it is not uniform.

## Workflow

1. **State the null model.** Independent positions with fixed base probabilities? Draws without
   replacement from a finite set? A Markov chain? Pick the one that matches how the data arose.
2. **Count the possibilities** if the question is combinatorial. `python3 scripts/seqstats.py
   sampling N K` gives all four cases: ordered or unordered, with or without replacement.
3. **Choose the distribution.** Fixed number of independent yes/no trials: binomial. Drawing
   without replacement from a finite pool with marked items: hypergeometric. Expected count of a
   word: `expect`. Long-run composition of a chain: `stationary`.
4. **Compute the tail, not the point.** For "at least this many", use the upper tail, `P(X >= k)`.
5. **Count the tests.** Every comparison made counts, including ones that looked dull. Apply
   `adjust` (Benjamini-Hochberg for a false-discovery rate, Bonferroni for family-wise error).
6. **Check the assumption that matters most.** For words that can overlap themselves, occurrences
   are not independent, and a binomial tail is only a guide. Shuffle to get an empirical null.
7. **Report** the null model, the number of tests, the raw and adjusted values, and an effect
   size. A tiny p-value on a trivial effect is not a finding.

## Decision framework

| Situation | Use |
|---|---|
| Number of possible sequences, codons, samples | `sampling`: n^k, n!/(n-k)!, C(n,k), C(n+k-1,k) |
| k successes in n independent trials | `binom N K P` |
| k marked items in a draw without replacement | `hypergeom` (for example genes in a set among all genes) |
| Expected occurrences of a word | `expect LENGTH WORD --gc G` |
| Many tests, want few false leads | `adjust ... --method bh` |
| Many tests, want no false positive at all | `adjust ... --method bonferroni` |
| Long-run frequencies of states | `stationary "row;row"` |
| Overlapping words, odd composition, dependent data | empirical null by shuffling; see `references/null-models-and-testing.md` |

## Implementation guidance

- All functions are exact and in the standard library. Large factorials are handled by Python
  integers, so there is no overflow, but very large tails can be slow.
- Seed every random shuffle and record the seed.
- Likelihood is a function of the parameters for fixed data; probability is a function of the data
  for fixed parameters. Do not read a likelihood as a probability of the hypothesis.
- Compare models by log-likelihood ratio only when one is a special case of the other (VERIFY the
  reference distribution to use).
- `references/null-models-and-testing.md` has the shuffling recipes and the testing guidance.

## Failure and edge cases

- **Wrong tail.** Reporting the probability of exactly k instead of at least k.
- **Hidden tests.** Reporting the best of many windows or parameters as if it were one test.
- **Independence assumed.** Neighbouring positions, overlapping words and related sequences are
  not independent.
- **Composition ignored.** A GC-rich genome makes GC-rich words common; use the right base
  probabilities.
- **p-value as effect.** Large samples make trivial differences significant.
- **Stationary distribution of a periodic or reducible chain.** A periodic chain can fail to
  converge (the script then raises an error), and a reducible chain has several stationary
  distributions, of which the script returns the one reached from a uniform start. Check that
  every state can reach every other first.
- **Multiple testing adjusted twice,** or the wrong family of tests chosen.

## Validation

- `python3 scripts/seqstats.py --selftest` must pass: binomial and hypergeometric masses sum to 1,
  the four sampling counts for n = 4, k = 2 are 16, 12, 6 and 10, and Benjamini-Hochberg is never
  below the raw p-value and never above Bonferroni.
- Sanity: with a 40% GC genome, A and T are each 0.3 and C and G each 0.2.
- Falsifier: run the same test on shuffled data; it should find about the nominal fraction of
  "significant" results, no more.

## Expected output

The null model, the statistic, the tail, the raw value, the number of tests, the adjusted value,
the effect size, and the assumption most likely to be wrong.

## Sources and confidence

- Ramsden, *Bioinformatics: An Introduction*, 2nd ed., chs. 4 to 6: section titles only (the four
  sampling cases, the binomial theorem, probability, Bernoulli trials, the hypergeometric
  distribution, likelihood, the maximum entropy method, Markov chains, random walks), from the
  table of contents. The text of these chapters was not supplied
- Formulas for the distributions, the Benjamini-Hochberg procedure and Bonferroni correction:
  standard results, checked by hand-computed cases in the self-test; VERIFY choice of procedure
  against the user's field
- Not covered: Bayesian inference, permutation tests beyond shuffling, survival analysis,
  Karlin-Altschul alignment statistics (see `sequence-alignment`)
