---
name: bioinformatics-programming
description: Writes, structures and speeds up code for biological data, covering the choice of language and libraries, compact sequence representations, streaming large files, working in log space, avoiding quadratic loops, parallelism and memory limits, and the bugs that recur in sequence code. Use for "how do I process a 50 GB FASTA", "my script is too slow", "which language should I use", "my probabilities underflow to zero", "write a k-mer counter", "debug my sequence code", "run this in parallel". Use reproducible-research-code for environments, tests and records, sequence-formats for file formats and coordinates, and gene-finding-translation for sequence operations.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Bioinformatics programming

## Purpose and activation

Write code for sequence and omics data that is correct first, then fast enough, and that does not
run out of memory on real inputs. Bioinformatics code fails in a few repeated ways: reading a whole
file into memory, multiplying small probabilities until they become zero, nested loops over long
sequences, and coordinates off by one. Activate when the user is writing, debugging or speeding up
such code.

## Required inputs

The task; the size of the inputs (records, bases, file size, compressed or not); the machine
(memory, cores) and whether a cluster is available; the language the user knows; whether an
existing tool already does the job; and how the result will be checked.

## Workflow

1. **Size the problem.** Multiply it out: records times length, bytes of memory, expected run time.
   Most design choices follow from this one number.
2. **Look for an existing tool first.** A well-tested tool beats new code; write code for the glue,
   the analysis that is yours, and the checks.
3. **Pick the language for the job:** a scripting language for glue and analysis, array or
   compiled code for heavy numeric loops (VERIFY options for your platform). Use the one your team can
   maintain.
4. **Choose a representation.** Plain strings are fine at small scale. For large sets, pack bases in
   two bits (`python3 scripts/bioprog.py pack SEQ`), use integers for k-mers, and store the
   canonical form of a k-mer (`bioprog.py canonical KMER`) so both strands count together.
5. **Stream the input.** Read one record at a time (`bioprog.py fasta FILE`), compressed or not,
   and keep only what you need.
6. **Keep probabilities in log space** and add them with `bioprog.py logsumexp`, so that a long
   product does not underflow to zero.
7. **Make loops linear.** A window statistic updates by adding the base that enters and removing the
   one that leaves (`bioprog.py gcwin SEQ --size W`) instead of recounting each window.
8. **Parallelise by independent unit** (record, chromosome, sample), seed each worker's random
   generator separately, and merge results in a fixed order.
9. **Test small, then scale:** check against a hand answer and against an independent
   implementation, then profile before optimising (`reproducible-research-code`).

## Decision framework

| Situation | Choice |
|---|---|
| File larger than memory | Stream it; never read it whole |
| Billions of bases of k-mers | Packed integers and canonical k-mers; a counting tool if one exists |
| Product of many probabilities | Log space and `logsumexp` |
| Same calculation on every window | Incremental update, O(n), not O(n x window) |
| Many independent samples | One job per sample, on a scheduler or process pool |
| Result differs between runs | Unordered collections, thread order, or unseeded randomness |
| Need speed in a scripting language | Vectorised array code or a compiled extension, after profiling |
| Coordinates | One internal convention, converted at the file boundary (`sequence-formats`) |

## Implementation guidance

- The helpers in `scripts/bioprog.py` are the tested cores of these patterns and can be copied into
  a project: 2-bit packing with an exact round trip, integer k-mers, canonical k-mers, log-sum-exp,
  incremental windows, and a streaming FASTA reader that yields a record as soon as the next header
  is seen.
- Ambiguity codes such as N cannot be stored in two bits; keep a separate mask of their positions.
- Compressed input needs a streaming decompressor; do not decompress to disk without need.
- Strings of text are immutable in many languages; repeated concatenation in a loop is quadratic,
  so collect pieces and join once.
- `references/performance-patterns.md` and `references/common-bugs.md` hold the patterns and the
  bug list.

## Failure and edge cases

- **Whole file in memory,** then the machine swaps or the job is killed.
- **Underflow:** a product of thousands of probabilities becomes 0 and a logarithm of it fails.
- **Quadratic loops** over long sequences, fine on the test file and hopeless on the genome.
- **Off-by-one coordinates** between 0-based slices and 1-based files.
- **Case destroyed** by upper-casing, losing soft-masking information.
- **Non-reproducible order** from unordered sets or dictionaries and from unseeded random numbers.
- **Integer overflow** in languages with fixed-size integers when counting bases or packing k-mers.
- **Silent type changes,** such as identifiers read as numbers.
- **Premature optimisation** of code that is not the bottleneck.
- **Sequences that contain N** passed to code that assumes only A, C, G and T.

## Validation

- `python3 scripts/bioprog.py --selftest` must pass.
- Hand check: ACGT packs to the single byte 0x1B; GTT and AAC have the same canonical form.
- Hand check: log-sum-exp of two values of -1000 is -1000 plus the natural log of 2.
- Hand check: incremental GC windows equal the directly counted windows.
- Falsifier: run on a file ten times larger; memory use should stay roughly flat for streaming code.

## Expected output

The size estimate, the tools or libraries chosen and why, the data representation, the streaming
and numeric design, the parallel plan, the tests, and the profile that justifies any optimisation.

## Sources and confidence

- Ramsden, *Bioinformatics: An Introduction*, 2nd ed., ch. 1.2 (supplied text): practical programming
  is left out of the book because other books cover it. Nothing here comes from it
- Patterns and bug list: general programming practice from author knowledge, VERIFY against the
  documentation of your language and libraries; the helper functions are checked by the self-test
  with hand-computed values and equivalence with a direct implementation
- Not covered: GPU programming, database engines, web services, any one language's idioms in depth
