---
name: information-theory-sequences
description: Measures how much information, variety, complexity or conservation a biological sequence carries, through Shannon entropy of bases or k-mers, diversity numbers, relative entropy, motif information content, mutual information between positions, and compression distance between sequences, with the limits of each estimate. Use for "how random is this sequence", "find low-complexity regions", "how conserved is this motif column", "compute the entropy of this DNA", "measure distance by compression". Use sequence-statistics for p-values and null models, sequence-alignment for position-by-position comparison, and gene-finding-translation for codon and word counts.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Information theory for sequences

## Purpose and activation

Put a number on "how much structure is in this sequence", and say what the number does not mean.
Activate when the user asks about randomness, complexity, conservation, redundancy or distance
between sequences, or says "entropy" or "information content". The source text treats information
as the central idea of biology: a sequence carries information only to the extent that it departs
from randomness, so a measure of departure is the right first tool.

## Required inputs

The sequences or columns (letters, alphabet size, case rules); the question (composition, local
complexity, conservation, dependence between positions, or distance); the sequence length, since
every estimate here depends on it; and, for conservation, the background composition to compare with.

## Workflow

1. **Fix the alphabet.** DNA has 4 letters, so the largest possible entropy is 2 bits per base.
   Protein has 20. State the alphabet before quoting a number.
2. **Pick the measure** from the decision table. Run it with `python3 scripts/seqinfo.py`; the
   subcommands are `bits`, `entropy`, `hill`, `ncd` and `mi`.
3. **Report the units and the estimator.** Bits for log base 2. Say it is a plug-in estimate from
   observed frequencies.
4. **Check the length.** With K-mers of size k there are up to 4^k kinds; if the sequence has
   fewer than a few times that many k-mers, the entropy estimate is biased low. Say so.
5. **Compare with a baseline.** Entropy of 1.9 bits means little until you know what shuffled or
   random sequence of the same composition gives. Hand this to `sequence-statistics`.
6. **Say what it is not.** Entropy measures variety, not meaning, function or biological effect.
7. **Hand off.** A region flagged as low complexity goes to `gene-finding-translation` or
   `sequence-alignment` to be masked or interpreted, not read as functional.

## Decision framework

| Question | Measure | Command |
|---|---|---|
| How many bits to name one of N equally likely kinds | variety, log2 N | `seqinfo.py bits N` |
| How much composition bias in a sequence | Shannon entropy of base frequencies | `seqinfo.py entropy SEQ` |
| How repetitive at word level | entropy of k-mers | `seqinfo.py entropy SEQ --k K` |
| Effective number of kinds, abundant or rare | diversity numbers D0, D1, D2 | `seqinfo.py hill SEQ` |
| How conserved is an alignment column | log2(alphabet) minus column entropy | `motif_column_information()` in the script |
| How far a column differs from the background | relative entropy | `kl_divergence()` in the script |
| Do two positions vary together | mutual information | `seqinfo.py mi COL1 COL2` |
| How different are two sequences, with no alignment | normalized compression distance | `seqinfo.py ncd SEQ1 SEQ2` |

Formulas, units and worked values are in `references/measures.md`.

## Implementation guidance

- The script is standard-library Python and runs on 3.9 or later. Its self-test reproduces numbers
  printed in the source text (1.585, 3.585 and 6.91 bits; 2.79 bits for the weighted case) and
  hand-computed entropies.
- For long inputs, compute windowed entropy by slicing in your own loop and calling `entropy()`.
- Treat compression distance as a quick screen. The result depends on the compressor, and a
  compressor with a limited window cannot see repeats farther apart than that window.
- Keep sequence case and ambiguity codes out of the count unless they are part of the question.

## Failure and edge cases

- **Short sequences.** The plug-in entropy is biased low, so short windows look more repetitive
  than they are.
- **Entropy read as function.** Low entropy flags repeats and composition bias, not genes.
- **High entropy read as meaning.** A random sequence has maximal entropy and carries nothing;
  the source text notes randomness is minimally informative.
- **Mixed alphabets.** Entropy of a table that mixes DNA and protein is meaningless.
- **Independence assumed.** Single-base entropy ignores dependence between neighbours; use k-mers
  or mutual information when order matters.
- **Rounded textbook numbers.** The source prints two decimals and rounds in places; compare with
  a tolerance, not with equality.

## Validation

- `python3 scripts/seqinfo.py --selftest` must pass.
- Sanity: ACGT gives 2 bits, AAAA gives 0, AACC gives 1.
- D0 is at least D1, and D1 at least D2 (the source's inequality, from Jensen).
- Falsifier: shuffle the sequence; entropy of single bases must not change, entropy of k-mers
  should rise toward the maximum if the original had structure.

## Expected output

The measure, the value with units, the alphabet, the sequence length, the estimator and its bias
note, the baseline it was compared with, and one sentence on what the value does not show.

## Sources and confidence

- Ramsden, *Bioinformatics: An Introduction*, 2nd ed., ch. 2 opening (supplied text): variety as
  the logarithm of the number of kinds; Hartley's formula; the Shannon-Wiener index as a weighted
  mean; the worked values above; the diversity numbers D0, D1, D2; Jensen's inequality
- Ch. 1.1 (supplied): randomness is minimally informative, so departure from randomness is the
  core of bioinformatics
- Ch. 3 (channel capacity, coding, compression, noise, error correction), ch. 5.5 (maximum entropy),
  ch. 6.5 (complexity): section titles only, from the table of contents
- Relative entropy, mutual information, motif information content, estimator bias, compression
  distance: from general knowledge, VERIFY against a text on information theory
- Not covered: Kolmogorov complexity beyond its mention, channel coding design, quantum information
