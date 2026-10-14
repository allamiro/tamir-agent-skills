# Population genetics notes

Standard results; VERIFY against a population genetics text before relying on a statement.

## Allele frequency and Hardy-Weinberg

For a biallelic locus with genotype counts AA, Aa, aa out of N individuals, the frequency of A is
p = (2 AA + Aa) / (2 N) and q = 1 - p. Under Hardy-Weinberg proportions the expected genotype
frequencies are p squared, 2 p q and q squared. The chi-square statistic sums (observed - expected)
squared over expected across the three genotypes and has one degree of freedom (three classes, one
estimated parameter).

| Worked example | Result |
|---|---|
| AA = 36, Aa = 48, aa = 16 | p = 0.6; expected 36, 48, 16; chi-square 0 |
| AA = 50, Aa = 0, aa = 50 | p = 0.5; expected 25, 50, 25; chi-square 100 |
| AA = 1, Aa = 1, aa = 1 | chi-square 1/3, p = 0.564 |

Assumptions behind the expectation: random mating, no selection, no migration, no mutation, a large
population. Deviations arise from real biology (inbreeding, structure, selection) and from errors
(genotyping, mapping, merging samples from different groups).

## Linkage disequilibrium

For two biallelic loci with allele frequencies pA, pB and haplotype frequency pAB:

| Quantity | Formula |
|---|---|
| D | pAB - pA pB |
| r squared | D squared / (pA (1 - pA) pB (1 - pB)) |
| D' | D divided by its largest possible value given the allele frequencies |

r squared is the squared correlation and predicts how well one variant tags another; D' is 1 when
no recombinant haplotype is seen, even if r squared is small. LD depends on the population.

## Population structure

Allele frequencies differ between populations. A sample that mixes groups shows an excess of
homozygotes (the Wahlund effect) and false association when group is correlated with the trait.
Account for structure with principal components, mixed models, or matched sampling (VERIFY the
method for your design).

## Association studies

- Millions of variants are tested, so the threshold is very strict; report the correction method.
- A significant variant marks a region; many nearby variants are correlated by LD.
- Effect sizes of top hits are overestimated (winner's curse); replicate in independent data.
- Association is not causation; a mechanism needs functional evidence.
- The source text leaves the design of association studies out, so consult a dedicated reference.

## Medical use

Interpreting a variant for a person's health is a clinical task with its own standards and
oversight. This skill gives no clinical classification. Chapters on medical applications in the
source (genetic basis of disease, cancer, diagnosis, drug discovery, personalized medicine) are
known here by section title only.
