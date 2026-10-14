# Scoring

## The recurrence

For sequences a (length n) and b (length m), H(i, j) is the best score for aligning the first i
letters of a with the first j of b.

| Alignment | H(0, j) and H(i, 0) | H(i, j) |
|---|---|---|
| Global | j times gap, i times gap | max of H(i-1, j-1) + s(a_i, b_j), H(i-1, j) + gap, H(i, j-1) + gap |
| Local | 0 | the same maximum, but never below 0 |

Global: the answer is H(n, m) and the traceback starts there. Local: the answer is the largest H
anywhere and the traceback stops at 0.

## Choosing scores

| Scheme | Typical use | Caution |
|---|---|---|
| Match +1, mismatch -1, gap -1 | Teaching, close DNA, edit-distance-like | Not tuned to any real divergence |
| Match +2, mismatch -1, gap -2 | Local DNA default in this script | Arbitrary; change it and report it |
| Match 0, mismatch -1, gap -1 | Edit distance (the score is minus the distance) | Useful as a test |
| Substitution matrix with affine gaps | Protein alignment | Not implemented here; use a tool and name the matrix (VERIFY) |

Rules of thumb: a match must score more than a mismatch; the gap penalty should reflect how often
insertions and deletions occur compared with substitutions; with a positive expected score per
column, local alignment extends to the full length instead of finding a region, so local scoring
needs a negative expected score for random pairs.

## Linear and affine gaps

Linear: each gap position costs the same, so a gap of length L costs L times gap. Affine: opening
a gap costs more than extending it, which models one insertion event of several bases better.
This script is linear only.

## Significance by shuffling

1. Compute the observed local score.
2. Shuffle the second sequence many times (this keeps its composition), recompute the score each time.
3. p = (1 + number of shuffles scoring at least as high) / (1 + number of shuffles).

The p-value is empirical and cannot fall below 1 / (1 + shuffles). Database search tools instead
report analytical statistics for local alignment scores (VERIFY the model before quoting one).

## Reading an alignment

- Identity is matched columns over alignment length; it depends on where the alignment is cut,
  so state the length.
- Similarity for protein counts conservative substitutions as well, which needs a matrix.
- A long gap near an end can be a missing piece of the sequence, not an event in evolution.
- Equal-scoring alignments are common in repeats. Do not draw biology from which one is printed.
