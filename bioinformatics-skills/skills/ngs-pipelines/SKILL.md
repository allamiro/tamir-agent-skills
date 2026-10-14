---
name: ngs-pipelines
description: Plans and checks short-read sequencing pipelines from raw reads to alignments, variant calls or counts, covering read quality control, trimming, reference choice, mapping, duplicate handling, coverage and depth arithmetic, reading SAM flags and CIGAR strings, and the common failure points. Use for "how do I process my sequencing reads", "what does FLAG 99 mean", "how deep do I need to sequence", "decode this CIGAR", "my mapping rate is low", "is my coverage enough", "design an RNA-seq or variant-calling pipeline". Use sequence-formats for FASTQ and coordinates, variants-population-genetics for interpreting calls, omics-data-analysis for expression tables, and reproducible-research-code to build the pipeline.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# NGS pipelines

## Purpose and activation

Take sequencing reads to something analysable, and know at each stage whether the data are good
enough to go on. Pipelines fail quietly: a wrong reference, an adapter left on the reads, mates out
of order. Activate when the user has reads or alignments, asks how to process them, asks what a
flag or CIGAR string means, or asks how much sequencing is enough.

## Required inputs

The assay (whole genome, exome, RNA-seq, targeted, metagenome, other); the platform and read type
(single or paired, length); the organism and the reference genome build and annotation; the number
of samples and their design; and what the output is for (variants, counts, assembly).

## Workflow

1. **Name the assay and the question,** since they set the reference, the aligner type and the
   checks (`references/pipeline-stages.md`).
2. **Plan depth.** `python3 scripts/ngs.py coverage --reads N --length L --genome G` gives the mean
   depth and the best-case fraction covered. `reads-needed --depth 30 ...` goes the other way.
   Real coverage is less even than the model assumes.
3. **Check the raw reads:** base quality along the read, adapter content, GC distribution,
   duplication, contamination, and that paired files have the same number of reads in the same order.
4. **Trim only what the data call for,** and keep a count of what was removed.
5. **Fix the reference** (build, annotation release, decoy or contig sets) and record it.
6. **Map,** with an aligner suited to the assay (spliced for RNA; VERIFY for your data), then
   sort, index and mark duplicates.
7. **Check the alignments:** fraction mapped, properly paired, duplicate rate, insert size and
   depth. Decode flags with `python3 scripts/ngs.py flags N` and CIGAR strings with
   `python3 scripts/ngs.py cigar STRING --pos P`.
8. **Run the downstream step** (variant calling, quantification) and check that it recovers a known
   sample or control.
9. **Record versions and parameters** for every tool (`reproducible-research-code`).

## Decision framework

| Question | Do this |
|---|---|
| Is a read mapped | FLAG bit 0x4 is the only reliable place to tell |
| Is a pair properly aligned | FLAG bit 0x2, set by the aligner; check the insert size too |
| Which strand is the read on | FLAG 0x10 means the read is reverse complemented |
| Where does an alignment end | POS plus reference-consuming CIGAR operations minus 1 |
| How much sequencing | Choose depth for the question, then the reads from `ngs.py reads-needed` |
| Low mapping rate | Wrong reference or species, adapters, contamination, poor quality, too-short reads |
| Duplicates high | Low-input library, over-amplification, or a small target; mark them, do not delete blindly |
| Coverage very uneven | GC bias, repeats, mappability; look at depth against GC |

## Implementation guidance

- Flag bits and CIGAR operations are exactly as in the SAM specification; the script's self-test
  checks all 4096 flag values for round-trip and the CIGAR arithmetic by hand.
- A CIGAR with soft clips (S) keeps those bases in the read but outside the aligned part; hard clips
  (H) remove them from the stored read.
- A spliced RNA-seq read has an N operation that skips the intron on the reference.
- Always sort and index before use, and keep the index with its file.
- Work on a small subsample of reads first to check the whole pipeline, then run in full.
- `references/sam-bam-guide.md` has the flag and CIGAR tables.

## Failure and edge cases

- **Wrong build or species,** giving a plausible but meaningless low mapping rate.
- **Read pairs out of sync** after filtering one file but not the other.
- **Adapter read-through** inflating mismatches at read ends.
- **Quality trimming too aggressive,** shortening reads until they map ambiguously.
- **Strandedness assumed wrongly** in RNA-seq counting.
- **PCR and optical duplicates** treated as independent evidence.
- **Lane or batch effects** treated as biology.
- **Sample swaps and contamination** unnoticed without a fingerprint or sex check.
- **Multi-mapping reads** (low MAPQ) counted as if unique.
- **Mean depth quoted as if uniform;** a mean of 30 does not mean every base has 30.

## Validation

- `python3 scripts/ngs.py --selftest` must pass.
- Hand check: FLAG 99 is paired, properly aligned, mate reverse, first in pair; FLAG 147 is paired,
  proper, reverse, second in pair.
- Hand check: 5S10M3D10M2S at POS 100 spans reference bases 100 to 122.
- Hand check: one-fold coverage leaves about 37% of bases unseen (the exponential of minus one).
- Falsifier: a control sample with a known answer is processed and the answer is not recovered.

## Expected output

The assay and reference, the QC findings at raw and alignment stage with numbers, the depth
arithmetic, the pipeline stages with tools and versions, the checks that were run, and the
limits (unevenness, bias, anything not checked).

## Sources and confidence

- SAM specification (hts-specs), read 2026-10-14: FLAG bits 0x1 to 0x800, the CIGAR operation table
  with query and reference consumption, POS as the 1-based leftmost position of the first operation
  that consumes the reference, and the statement that bit 0x4 is the only reliable test for unmapped
- Coverage model: Lander and Waterman (random, independent placement of reads), general knowledge
  and hand-checked values; VERIFY for real data with bias
- Pipeline stages, tool choices, thresholds: general practice from author knowledge, VERIFY against
  the tools' documentation and your platform's guidance
- Ramsden, *Bioinformatics: An Introduction*, 2nd ed.: ch. 13.1 (DNA sequencing, expressed sequence
  tags, section titles only) and ch. 14.1 (transcriptomics, section title only)
- Not covered: long-read data, single-cell protocols, assembly, metagenomic classification, base calling
