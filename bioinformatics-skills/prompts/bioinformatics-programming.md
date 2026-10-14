# `bioinformatics-programming` prompts

Write, structure and speed up code for biological data, without running out of memory and without the
bugs that recur in sequence code.

- **Give it:** the task, the size of the inputs, the machine, the language you know, and whether a
  tool already does part of the job
- **Skill file:** [`skills/bioinformatics-programming/SKILL.md`](../skills/bioinformatics-programming/SKILL.md)
- **References:** [`performance-patterns.md`](../skills/bioinformatics-programming/references/performance-patterns.md) and
  [`common-bugs.md`](../skills/bioinformatics-programming/references/common-bugs.md)
- **Related:** [`reproducible-research-code`](reproducible-research-code.md), [`sequence-formats`](sequence-formats.md)

## 1. A file too big for memory

> How do I read a 50 GB compressed FASTA file and compute a statistic for every record without running out of memory?

A good answer: stream the file one record at a time, decompress as a stream, keep only the running
result, and test on a small file and then a larger one to see that memory stays flat.

## 2. Probabilities that become zero

> My likelihood for a 5,000-base sequence comes out as 0 and my log of it fails. Why, and how do I fix it?

A good answer: the product of thousands of small probabilities underflows; add log probabilities and
use log-sum-exp for sums.

## 3. Pack the bases

> Pack ACGTACGTAC at two bits per base. How many bytes does it take, and what do I do about an N in the sequence?

A good answer: 3 bytes (10 bases in 2 bits each is 20 bits), and N cannot be stored in two bits, so
keep a separate mask of the positions of non-ACGT characters.

## 4. A slow window loop

> My loop that computes GC content in windows is too slow on a whole chromosome. Make it linear, and show me how to check that it matches the slow version.

A good answer: add the base entering and remove the base leaving the window, and compare against
the direct calculation on many small random sequences.

## 5. Which language

> Which language should I use to process 200 million short reads, and should I write it myself?

A good answer: use an existing tool for the standard steps; write glue in a language the team can
maintain; use array or compiled code only for a profiled bottleneck.

## 6. Output order changes between runs

> The order of my output changes every time I run the script, though the input is the same. What could cause that?

A good answer: unordered collections whose order depends on hashing, parallel workers finishing in
different orders, and unseeded random numbers; sort at the end, merge in a fixed order, and seed.
