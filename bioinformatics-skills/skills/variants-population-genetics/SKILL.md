---
name: variants-population-genetics
description: Reads and checks genetic variant data and basic population genetics, covering VCF fields and genotypes, allele frequencies, Hardy-Weinberg checks, linkage disequilibrium, quality filters, and the limits of interpreting variants and association results. Use for "what do these VCF columns mean", "is this variant in Hardy-Weinberg equilibrium", "compute allele frequency", "what does r squared between SNPs mean", "filter my variants", "what can I conclude from a GWAS hit", "is this variant disease-causing". Use ngs-pipelines for producing calls from reads, sequence-statistics for tests and multiple testing, and data-governance-ethics for human genomic data.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Variants and population genetics

## Purpose and activation

Read a variant file correctly, check it for errors, and say what a frequency, a deviation from
Hardy-Weinberg or a linkage statistic does and does not show. Activate when the user has a VCF or a
table of genotypes, asks about allele frequencies or linkage, or asks what a variant means for a
trait or disease. Clinical interpretation belongs to a qualified service; this skill stops short of it.

## Required inputs

The variant file and the caller or pipeline that made it; the reference genome build; the samples
(how many, related or not, ancestry, case or control status); the question; and for human data the
consent and access terms.

## Workflow

1. **Fix the build.** Positions mean nothing without the reference they were called on.
2. **Read the file.** `python3 scripts/popgen.py vcf FILE` summarises each biallelic site: genotype
   counts, missing calls, alternative-allele frequency and a Hardy-Weinberg p-value. Multi-allelic
   sites are listed as skipped, not forced into two alleles.
3. **Apply quality filters** from the FILTER column, depth, genotype quality and call rate, and
   record what was removed (`references/vcf-guide.md`).
4. **Check sample quality:** missingness per sample, relatedness, ancestry, sex against metadata.
5. **Compute frequencies** and compare with a reference population only when ancestry matches.
6. **Test Hardy-Weinberg** with `popgen.py hwe AA Aa aa`, in controls or a homogeneous group. A
   strong deviation at one site more often means a genotyping or mapping error than biology.
7. **Measure linkage** with `popgen.py ld AB Ab aB ab`: D, D' and r squared from haplotype counts.
8. **For association results,** state the model, the correction across all variants tested, the
   effect size and the population structure control (`references/population-genetics-notes.md`).
9. **Stop at the limit.** Name what was and was not shown, and refer clinical questions on.

## Decision framework

| Situation | Choice |
|---|---|
| VCF POS | 1-based; the first base of the reference is position 1 |
| Genotype `0/1` or `0\|1` | Het; `/` is unphased and `\|` phased; `.` is missing |
| Site with several ALT alleles | Multi-allelic: split and normalise first, or analyse with a tool that handles it |
| Hardy-Weinberg fails at a site | Check genotyping, mapping and population structure before biology |
| Two variants correlated | Linkage disequilibrium; the associated variant may only tag the causal one |
| Rare variant | Frequency estimates are very uncertain; do not test with the large-sample approximation |
| Association hit | A signal in a region, not a mechanism |
| A medical question about a person | Out of scope; refer to a clinical genetics service |

## Implementation guidance

- The Hardy-Weinberg test here is the large-sample chi-square with one degree of freedom, computed
  with the complementary error function; with small expected counts use an exact test (not
  included).
- D' is Lewontin's normalisation of D by its largest possible value; r squared is the squared
  correlation between the two loci's alleles. They answer different questions.
- Keep alleles and strand consistent when merging files; a flipped strand reverses a frequency.
- Normalise indels (left-align, split multi-allelic) before comparing files.
- This script reads diploid genotypes only.

## Failure and edge cases

- **Strand flips and swapped REF/ALT** between datasets.
- **Genome build mismatch** or a liftover that dropped sites.
- **Multi-allelic and indel representation** differing between callers.
- **Population stratification:** allele frequencies differing between groups create false association.
- **Relatedness:** related samples violate independence in every test here.
- **Hardy-Weinberg tested in cases,** where a true association can cause deviation.
- **Low call rate and depth,** which bias heterozygote calls downward.
- **Winner's curse:** the effect of the top hit is overestimated.
- **Reading association as causation,** or a tag variant as the causal one.
- **Sharing genotypes** without checking consent.

## Validation

- `python3 scripts/popgen.py --selftest` must pass.
- Hand check: genotype counts 36, 48, 16 give allele frequency 0.6 and chi-square 0.
- Hand check: haplotype counts 40, 10, 10, 40 give D = 0.15, D' = 0.6 and r squared = 0.36.
- Hand check: 3.841 on one degree of freedom corresponds to p = 0.05.
- Falsifier: a site called wrong in the same way across many samples shows up as a Hardy-Weinberg
  deviation; one that does not may still be wrong.

## Expected output

The build and filters used with counts removed, per-site or per-variant summaries, quality
findings at sample and site level, the Hardy-Weinberg and linkage results with their assumptions,
and a limits paragraph that separates what is shown from what is inferred.

## Sources and confidence

- VCF specification (hts-specs VCFv4.3), read 2026-10-14: the fixed columns CHROM, POS, ID, REF, ALT,
  QUAL, FILTER, INFO, then FORMAT and samples; POS is 1-based; GT uses 0 for REF and 1 for the first
  ALT, `/` unphased and `|` phased, `.` missing; PASS means the site passed all filters; QUAL is
  Phred-scaled
- Ramsden, *Bioinformatics: An Introduction*, 2nd ed.: ch. 1.2 (supplied text) leaves the design of
  genetic association studies out; ch. 17 (the genetic basis of disease, cancer, automated diagnosis,
  drug discovery, personalized medicine): section titles only
- Hardy-Weinberg, linkage disequilibrium, association pitfalls: standard population genetics,
  checked by hand-computed cases; VERIFY methods against a population genetics text
- Not covered: clinical variant classification, haplotype phasing, imputation, selection scans,
  structural variants, somatic variant calling
