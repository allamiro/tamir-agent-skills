---
name: sequence-alignment
description: Aligns two biological sequences by dynamic programming, global (Needleman-Wunsch) or local (Smith-Waterman), explains the scoring choices, and tests whether a score is more than chance by shuffling. Use for "align these two sequences", "how similar are these", "is this match significant", "what gap penalty should I use", "explain this alignment score", "check my alignment code", "which alignment tool should I use". Use sequence-statistics for the general null-model and multiple-testing rules, phylogenetics when alignments feed a tree, and gene-finding-translation for finding genes rather than comparing sequences.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Sequence alignment

## Purpose and activation

Compare two sequences position by position, score the comparison, and decide whether the
similarity is real. Sequence comparison is where the field began, and the source text frames it as
a study of the non-randomness of sequences: a high score matters only because chance rarely gives
one. Activate when the user has two sequences and asks how alike they are, or asks why an
alignment looks the way it does.

## Required inputs

The two sequences and their type (DNA, RNA or protein); whether the whole length should match
(global) or only the best shared region (local); the scoring scheme (match, mismatch, gap, and a
substitution matrix for protein); the sequence lengths; and what the answer will be used for.

## Workflow

1. **Choose global or local.** Two sequences of similar length that should align end to end:
   global. A domain or motif inside longer sequences: local.
2. **Set the scores.** For DNA a simple scheme such as match +1, mismatch -1, gap -1 is a start;
   see `references/scoring.md`. A mismatch must cost less than a gap pair would, or the aligner
   prefers gaps everywhere.
3. **Align.** `python3 scripts/align.py global SEQ1 SEQ2` or `local`; override scores with
   `--match`, `--mismatch=-1` and `--gap=-2`. It prints one optimal alignment, the score, the
   identity and the matched spans.
4. **Test the score.** `python3 scripts/align.py significance SEQ1 SEQ2 --shuffles 1000` gives an
   empirical p-value against shuffles of the second sequence. Report it with the number of shuffles.
5. **Look at the alignment.** A good score built from one long gap plus a short match is not the
   same as a spread-out match. Check where the matches are.
6. **Scale up carefully.** The script is O(length1 x length2) and is for small inputs and for
   checking other tools. For genomes or databases use an established heuristic tool and
   verify a sample of its output with this script.
7. **Hand off.** A set of aligned sequences goes to `phylogenetics`; a score used as a claim
   goes to `sequence-statistics` and `bioinformatics-review`.

## Decision framework

| Situation | Choice |
|---|---|
| Full-length homologs | Global |
| Motif, domain or gene inside a larger sequence | Local |
| Closely related DNA | Simple scoring, small gap penalty |
| Distant protein relatives | A substitution matrix and affine gaps, from a tool (not in this script) |
| More than two sequences | A multiple-alignment tool; this script is pairwise only |
| Very large input | A heuristic search tool, then verify a sample here |
| Score reported without a null | Add the shuffle test before believing it |

## Implementation guidance

- Ties in the traceback prefer diagonal, then a gap in sequence 2, then a gap in sequence 1. Equal
  scoring alignments can differ; the score is unique, the alignment is not.
- Local alignment returns the first best cell it meets and reports spans as 0-based with an
  exclusive end, matching Python slices.
- The linear gap model charges every gap position equally. Real insertions are often one event
  of several bases, which an affine model (opening plus extension) represents better.
- The self-test compares the dynamic-programming result with an exhaustive search over every
  alignment of small random pairs, re-scores each printed alignment independently, and checks that
  with match 0 and mismatch and gap -1 the score equals minus the edit distance.

## Failure and edge cases

- **Score without a null.** A raw score cannot be compared across different lengths or compositions.
- **Low-complexity sequence.** Repeats align well to unrelated repeats; mask or test against a
  composition-matched shuffle.
- **Wrong alphabet.** DNA scoring on protein, or the reverse.
- **Reverse strand.** A DNA match on the opposite strand needs the reverse complement first
  (`gene-finding-translation`).
- **Over-reading one alignment.** Many optimal or near-optimal alignments may exist.
- **Database reliability.** A match to an annotated entry inherits any error in the annotation; the
  source's contents list database reliability as a topic in its comparison chapter.
- **Shuffle null too weak or too strong** for the question; see `sequence-statistics`.

## Validation

- `python3 scripts/align.py --selftest` must pass.
- Hand check: ACGT against AGT with +1, -1, -1 scores 2, aligned as ACGT over A-GT.
- Hand check: local alignment of ACGT inside TTACGTT with +1, -1, -1 scores 4, spanning 2-6 of the
  first sequence (with the local default of +2, -1, -2 it scores 8).
- Falsifier: the shuffle p-value for two unrelated random sequences is not small.

## Expected output

The alignment (three lines), the score and scoring scheme, the identity and span, the shuffle
p-value with its count, and a sentence on what kind of similarity this does and does not show.

## Sources and confidence

- Ramsden, *Bioinformatics: An Introduction*, 2nd ed., ch. 13.4 (sequence comparison and alignment,
  dynamic programming algorithms, database reliability), ch. 13.5.2 (hidden Markov models) and ch. 1.2
  (supplied text: sequence comparison as the origin of the field, and as a study of non-randomness):
  section titles from the table of contents, plus the chapter 1 statement
- Needleman-Wunsch and Smith-Waterman recurrences: standard algorithms, verified by the exhaustive
  cross-check in the self-test
- Substitution matrices, affine gaps, heuristic search, alignment statistics: general knowledge,
  VERIFY against the tool's documentation
- Not covered: multiple alignment, structural alignment, read mapping, alignment of long reads
