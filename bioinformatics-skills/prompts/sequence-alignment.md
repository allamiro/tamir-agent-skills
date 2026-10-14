# `sequence-alignment` prompts

Align two sequences, explain the score, and test whether the similarity is more than chance.

- **Give it:** the two sequences, their type (DNA, RNA or protein), whether the whole length should
  match or only the best region, and the scoring scheme
- **Skill file:** [`skills/sequence-alignment/SKILL.md`](../skills/sequence-alignment/SKILL.md)
- **Scoring and significance:** [`scoring.md`](../skills/sequence-alignment/references/scoring.md)
- **After it:** [`phylogenetics`](phylogenetics.md) for trees, [`sequence-statistics`](sequence-statistics.md) for the null

## 1. A global alignment

> Globally align GCATGCG and GATTACA with match +1, mismatch -1 and gap -1. Show the alignment, the score, and tell me whether the alignment is the only optimal one.

A good answer: a score of 0, one alignment such as GCA-TGCG over G-ATTACA, and the statement
that the score is unique but the alignment is not: three alignments tie for the best score.

## 2. A local match

> Find the best local match of ACGT inside TTACGTT with match +1, mismatch -1 and gap -1. Give the score and the matched spans in both sequences.

A good answer: a score of 4, covering positions 2 to 6 of the first sequence (0-based, end
exclusive) and the whole of the second.

## 3. Is the match more than chance

> Is the best local alignment of <sequence A> and <sequence B> better than chance? Shuffle the second sequence 1,000 times with a fixed seed, report the empirical p-value, and tell me the smallest p-value that this test can give.

A good answer: the observed score, the p-value computed as (1 + count) / (1 + shuffles), the
seed, and the floor of 1/1,001.

## 4. Choosing scores

> What gap penalty and mismatch score should I use to align two closely related DNA sequences, and what changes for proteins? Tell me what goes wrong if a mismatch costs more than two gaps.

A good answer: a simple match, mismatch and gap scheme for close DNA, a substitution matrix and
affine gaps from a tool for proteins, and the point that the aligner then prefers two gaps to a
mismatch.

## 5. Explain a score

> Explain this alignment score by re-scoring it column by column: <paste the two aligned rows and the scoring scheme>. Say how much of the score comes from gaps.

A good answer: a per-column tally that sums to the stated score, and the share contributed by gaps.

## 6. Check my code

> Check my alignment code: <paste>. Suggest a hand-computed case, an exhaustive cross-check on tiny inputs, and a test with match 0 and mismatch and gap -1 that must equal minus the edit distance.

A good answer: the three independent checks named, and a request to run them on small random
pairs before trusting the code on real data.
