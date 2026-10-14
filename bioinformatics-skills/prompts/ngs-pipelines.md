# `ngs-pipelines` prompts

Plan and check pipelines from reads to alignments, variants or counts, and decode SAM flags and
CIGAR strings.

- **Give it:** the assay, the platform and read type, the organism and reference build, the number
  of samples, and what the output is for
- **Skill file:** [`skills/ngs-pipelines/SKILL.md`](../skills/ngs-pipelines/SKILL.md)
- **References:** [`sam-bam-guide.md`](../skills/ngs-pipelines/references/sam-bam-guide.md) and
  [`pipeline-stages.md`](../skills/ngs-pipelines/references/pipeline-stages.md)
- **Before it:** [`experimental-design`](experimental-design.md) · **After it:** [`variants-population-genetics`](variants-population-genetics.md), [`omics-data-analysis`](omics-data-analysis.md)

## 1. Decode a FLAG

> What does SAM FLAG 99 mean, bit by bit, and what flag would its mate normally have?

A good answer: 1 + 2 + 32 + 64, meaning paired, properly aligned, mate reverse-complemented and first
in the pair; the mate is normally 147.

## 2. Where does an alignment end

> A read maps at POS 100 with CIGAR 5S10M3D10M2S. Where does the alignment end on the reference, and how many read bases does the alignment account for?

A good answer: it spans 23 reference bases and ends at 122, and accounts for 27 read bases including
the soft-clipped ones.

## 3. Depth

> I have 1,000,000 reads of 150 bases for a 5-megabase bacterial genome. What mean depth is that, and what fraction is covered at least once in the best case?

A good answer: 30-fold, and about all of the genome in the best case, with a warning that real
coverage is uneven, so a mean of 30 does not mean 30 everywhere.

## 4. How many reads

> How many reads of 150 bases do I need for 30-fold coverage of a 5-megabase genome?

A good answer: 1,000,000 reads.

## 5. A low mapping rate

> My mapping rate is 35%. List the possible causes in the order I should check them.

A good answer: wrong reference or species, contamination, adapters left on, poor read quality,
reads too short after trimming, then reference build or index problems.

## 6. A pipeline design

> Design an RNA-seq pipeline from FASTQ to a count matrix. For each stage give the input, the output and a check I must pass before moving on.

A good answer: stages from raw QC through mapping to counting, each with a numeric check such as mapped
fraction, strandedness and genes detected, plus a record of versions and parameters.
