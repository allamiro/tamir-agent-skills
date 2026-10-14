# Pipeline stages

General practice; VERIFY tool choices and thresholds against current documentation. Tool names
are examples.

## The stages

| Stage | Input | Output | Check before moving on |
|---|---|---|---|
| Raw read QC | FASTQ | QC report | Quality along reads, adapters, GC, duplication, read counts of mates equal |
| Trimming and filtering | FASTQ | cleaned FASTQ | Counts of reads and bases removed, reads still paired |
| Reference preparation | genome FASTA, annotation | index | Build and annotation release recorded |
| Mapping | FASTQ, index | SAM or BAM | Fraction mapped, properly paired, MAPQ distribution |
| Sort, index, mark duplicates | BAM | sorted BAM, index | Duplicate rate plausible for the library |
| Alignment QC | BAM | metrics | Depth, evenness, insert size, strand balance, contamination |
| Downstream: variants | BAM | VCF | Known-sample recovery, call rate, depth |
| Downstream: expression | BAM | count matrix | Counts per sample, strandedness, genes detected |

## By assay

| Assay | Reference | Mapper type | Particular checks |
|---|---|---|---|
| Whole-genome resequencing | genome | unspliced short-read | Depth near target, GC bias, contamination, sample identity |
| Exome or panel | genome plus target regions | unspliced | On-target fraction, per-target depth, uniformity |
| RNA-seq | genome plus annotation, or transcriptome | spliced (or pseudo-alignment) | Strandedness, rRNA fraction, genes detected, 3' bias |
| ChIP, ATAC | genome | unspliced | Fragment size, duplicates, peak-calling controls |
| Amplicon, metagenome | marker or reference set | alignment or classifier | Primer removal, chimeras, contamination |

## Depth

| Aim | Typical need | Note |
|---|---|---|
| Common variants in a diploid genome | Tens of fold | Depends on the caller and quality; VERIFY |
| Rare or somatic variants | Much more | Depends on the allele fraction sought |
| Expression with replicates | Millions of reads per sample | More samples usually beats more depth |
| De novo assembly | Depends on genome and read type | Not covered here |

`ngs.py coverage` gives the best-case mean depth and covered fraction; plan for uneven coverage.

## Sample identity and contamination

- Check sex against metadata where applicable.
- Compare genotypes at known sites across samples to catch swaps and relatedness.
- Check the species of the reads against the intended organism.
- Include negative controls to see reagent and cross-sample contamination.

## Records to keep

Tool names and versions, parameters, reference build and annotation release, the number of reads
at every stage, random seeds, and the commands. Put them in the methods record.
