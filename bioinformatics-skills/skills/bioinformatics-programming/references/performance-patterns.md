# Performance patterns

General practice; VERIFY the details for your language. Profile before optimising: measure where
the time and memory go, then change that part.

## Estimate first

| Quantity | How |
|---|---|
| Memory for a sequence as text | About one byte per base in many languages, more with object overhead |
| Memory packed in two bits | One quarter of a byte per base |
| Memory for k-mer counts | Distinct k-mers times (key + count); up to 4 to the power k |
| Time for a nested loop | Outer count times inner count; a window of w over n bases is n times w if recounted |

Four to the power k grows quickly: 4^10 is about a million, 4^16 about four billion, so for large
k use hashing or a counting tool and expect memory to dominate.

## Patterns

| Problem | Pattern |
|---|---|
| Large file | Stream one record or one chunk at a time |
| Many small records | Batch them to cut per-record overhead |
| Repeated membership tests | A set or dictionary, not a list |
| Sliding window statistic | Add the incoming element, subtract the outgoing one |
| Strand-symmetric counting | Count the canonical k-mer |
| Product of probabilities | Add logarithms; use log-sum-exp for sums |
| Huge numbers of small integers | Packed arrays, not objects |
| Same lookup many times | Cache the result with a key that includes the input |
| String building in a loop | Collect pieces, join once |
| Independent units of work | Process pool or scheduler job per unit |
| Sorted output needed | Sort once at the end; do not keep re-sorting |

## Two-bit packing

A, C, G and T take values 0 to 3, four per byte. It cuts memory by about four times against text
and speeds comparison, but it cannot represent N or other codes, loses case, and needs unpacking
for most text operations. Keep a mask of non-ACGT positions if they matter.

## Canonical k-mers

A k-mer and its reverse complement describe the same sequence on opposite strands. Counting the
smaller of the two as the key halves the table and removes strand bias from the counts. For odd k no
k-mer equals its own reverse complement; for even k some do (palindromes).

## Log space

The product of 2,000 probabilities near 0.01 is about 10 to the power minus 4000, far below what a
64-bit float holds. Add log probabilities instead. To add probabilities held as logs, use
log-sum-exp: subtract the maximum, exponentiate, sum, take the log, add the maximum back.

## Parallelism

- Split by record, chromosome or sample, never by position inside a dependent calculation.
- Give each worker its own seeded generator, derived from a base seed and the worker number.
- Merge in a fixed order so the output does not depend on which worker finished first.
- Count memory per worker; it multiplies.

## Profiling

Measure with the language's profiler on a representative sample, find the one or two hot spots,
and change those. A complex fix for code that takes two percent of the run time is wasted.
