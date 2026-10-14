# Measures

All logarithms are base 2 unless stated, so the unit is the bit. Use the natural logarithm for D1.

## Variety and entropy

| Quantity | Formula | Example |
|---|---|---|
| Variety of N equally likely kinds | log2 N | 4 bases: 2 bits; 3 kinds: 1.585 bits |
| Shannon entropy of probabilities p_i | H = -sum p_i log2 p_i | (0.5, 0.25, 0.25): 1.5 bits |
| Largest entropy for N kinds | log2 N, when all p_i = 1/N | DNA: 2 bits per base |
| Entropy of k-mers | H over the frequencies of overlapping k-mers | up to 2k bits for DNA |
| Entropy rate estimate | H of k-mers divided by k | biased for large k |

Entropy of unequal probabilities is never larger than the equal case. The source text proves this
with Jensen's inequality applied to x log x.

## Diversity numbers (source equations 2.1 to 2.3)

| Number | Formula | Meaning |
|---|---|---|
| D0 | N, the count of kinds present | richness, ignores abundance |
| D1 | exp(H in nats) | effective number of kinds, weights by abundance |
| D2 | 1 / sum p_i squared | effective number dominated by the common kinds |

For any distribution D0 >= D1 >= D2, with equality when all kinds are equally likely.

## Worked values from the source (ch. 2)

| Case | Bits |
|---|---|
| Three equally likely directions | log2 3 = 1.585 (printed 1.59 and 1.58) |
| Length to the nearest inch, 12 equally likely values | log2 12 = 3.585 (printed 3.59) |
| Same, with prior weight 1/4 on each of 8, 9, 10 inches and 1/4 spread over the other nine | 3/4 log2 4 + 1/4 log2 36 = 2.79 |
| Length to a tenth of an inch, 120 equally likely values | log2 120 = 6.91 |

The printed values are rounded to two places and are not always rounded the same way, so tests
compare within 0.006.

## Measures between two things

| Measure | Formula | Notes |
|---|---|---|
| Relative entropy of p from q | sum p_i log2(p_i / q_i) | not symmetric; q must be non-zero where p is |
| Information content of a motif column | log2(alphabet size) - H(column) | 2 bits for a fully conserved DNA column; small-sample correction is needed for few sequences (VERIFY) |
| Mutual information of X and Y | sum p(x,y) log2( p(x,y) / (p(x) p(y)) ) | 0 for independent columns, H(X) when Y copies X |
| Normalized compression distance | (C(xy) - min(C(x), C(y))) / max(C(x), C(y)) | C is compressed length; depends on the compressor |

## Estimator cautions

- Plug-in estimates (from observed frequencies) are biased low when the number of observations is
  not much larger than the number of kinds. Correction methods exist (VERIFY which suits your case).
- Mutual information from few sequences is biased high: random columns show positive values.
- Compression distance on short sequences is dominated by the compressor's fixed overhead.
- Entropy treats symbols as unordered unless k-mers or conditional measures are used.
