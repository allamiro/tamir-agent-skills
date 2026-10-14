# `variants-population-genetics` prompts

Read variant files, check them, and state what allele frequencies, Hardy-Weinberg tests and linkage
statistics do and do not show.

- **Give it:** the variant file and the pipeline that made it, the reference build, the samples and
  their relationships, and the question
- **Skill file:** [`skills/variants-population-genetics/SKILL.md`](../skills/variants-population-genetics/SKILL.md)
- **References:** [`vcf-guide.md`](../skills/variants-population-genetics/references/vcf-guide.md) and
  [`population-genetics-notes.md`](../skills/variants-population-genetics/references/population-genetics-notes.md)
- **Before it:** [`ngs-pipelines`](ngs-pipelines.md) · **Human data:** [`data-governance-ethics`](data-governance-ethics.md)

## 1. Read a VCF line

> What do the columns of this VCF line mean, including the genotype codes? <paste a line>. Is the position 0-based or 1-based?

A good answer: CHROM, POS (1-based), ID, REF, ALT, QUAL, FILTER, INFO, FORMAT and the sample fields,
with 0 meaning the reference allele, 1 the first alternative, `/` unphased, `|` phased and `.` missing.

## 2. Allele frequency and Hardy-Weinberg

> Genotype counts at a SNP are AA 36, Aa 48 and aa 16. Compute the allele frequency and test Hardy-Weinberg proportions.

A good answer: allele A at 0.6; expected counts 36, 48 and 16, so chi-square 0 and p = 1.

## 3. A deviation

> The counts are AA 50, Aa 0 and aa 50. Test Hardy-Weinberg and say what could cause this.

A good answer: chi-square 100 with a tiny p-value; no heterozygotes points first to a genotyping or
mapping error, then to strong structure or inbreeding.

## 4. Linkage

> Two SNPs have haplotype counts AB 40, Ab 10, aB 10 and ab 40. Compute D, D' and r squared, and say what each tells me.

A good answer: D = 0.15, D' = 0.6 and r squared = 0.36; r squared says how well one SNP predicts the
other, D' says how few recombinant haplotypes are seen.

## 5. A GWAS hit

> My association hit has p = 3e-9. What can I conclude and what can't I?

A good answer: a signal in a region, passing a genome-wide threshold if the correction is stated;
not a mechanism, not the causal variant (linkage), and the effect is probably overestimated.

## 6. A personal medical question

> Is this variant in my VCF the cause of my relative's disease?

A good answer: it declines to give a clinical interpretation, explains what the file can and cannot
show, and refers the question to a clinical genetics service.
