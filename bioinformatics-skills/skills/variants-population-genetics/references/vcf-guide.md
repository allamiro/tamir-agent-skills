# VCF guide

Source: VCF specification (hts-specs VCFv4.3), read 2026-10-14, except where marked.

## Columns

| Column | Content |
|---|---|
| CHROM | Chromosome or contig name; must match the reference |
| POS | Reference position, 1-based |
| ID | Identifier such as an rs number, or `.` |
| REF | Reference allele |
| ALT | Alternative allele or alleles, comma separated |
| QUAL | Phred-scaled quality score for the assertion made in ALT |
| FILTER | `PASS` if the site passed all filters, otherwise the names of the filters failed |
| INFO | Site-level key=value annotations |
| FORMAT | Colon-separated list of the per-sample fields |
| samples | One column per sample, with values in the FORMAT order |

## Genotypes (GT)

| GT | Meaning |
|---|---|
| 0/0 | Homozygous reference |
| 0/1 | Heterozygous |
| 1/1 | Homozygous for the first ALT allele |
| 0\|1 | Heterozygous, phased |
| ./. | Missing |
| 1/2 | Het for the first and second ALT alleles (a multi-allelic site) |

Allele indexes: 0 is the REF allele, 1 the first listed ALT, 2 the second, and so on.

## Representation hazards

- Indels are written with a shared leading base, and the same event can be written several ways;
  normalise (left-align and trim) before comparing files.
- A multi-allelic site can be split into biallelic records or kept whole; know which a tool expects.
- A site with REF and ALT swapped or on the other strand relative to another dataset flips the
  frequency; check alleles when merging.

## Quality fields (general practice, VERIFY for your caller)

| Field | Use |
|---|---|
| QUAL | Confidence that a variant exists at the site |
| DP | Read depth; very low or very high depth is suspect |
| GQ | Genotype quality for a sample |
| FILTER | Pipeline's pass or fail labels; keep the labels, do not delete failing sites without recording it |
| Call rate | Fraction of samples with a called genotype at the site |

## Checks worth running

1. Every REF base matches the reference at its position (catches build mismatch).
2. The share of heterozygous calls per sample is similar across samples (outliers suggest
   contamination or failure).
3. Transition to transversion ratio is in a plausible range for the organism (VERIFY expected
   values).
4. Sex chromosome genotypes agree with sample sex.
5. Duplicate or related samples are identified before any frequency is computed.
