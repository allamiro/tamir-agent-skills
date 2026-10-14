# Reporting checklist

General practice; VERIFY against the venue's rules and any guideline for your study type.

## Every computational study

- [ ] The question and the primary comparison, stated before the results.
- [ ] Data: source, accession with version, date retrieved, licence or access terms.
- [ ] Reference genome build and annotation release.
- [ ] Software: name, version and parameters for every tool, including defaults that matter.
- [ ] Statistics: the tests, the null model, the number of tests, the correction, and the software.
- [ ] Sample sizes per group, and what a sample is; exclusions and why.
- [ ] Random seeds and the number of repeated runs where randomness matters.
- [ ] Code and data availability, with a permanent identifier for the code version.
- [ ] Limitations tied to specific findings.

## By type

| Study | Also report |
|---|---|
| Sequencing and alignment | Platform, read length and type, depth, trimming, mapping rate, duplicate handling, QC results |
| Variant calling | Caller and version, filters and thresholds, call rate, sample QC, how sex and ancestry were checked |
| Expression | Normalisation, batch handling, filtering of low counts, replicate structure, the model and correction |
| Proteomics and metabolomics | Instrument, identification criteria, false-discovery control, missing-value handling |
| Phylogenetics | Alignment method and trimming, model, tree method, support method and values, rooting |
| Machine learning | Splits and how groups were kept apart, baselines, metrics with intervals, tuning, independent validation |
| Network analysis | Source of edges, thresholds, how they were chosen, a shuffled comparison |
| Human data | Consent scope, approvals, access route, how identifiers were protected |

## Figures and tables

- [ ] Units and axis labels; n per group; what error bars show.
- [ ] Individual points when n is small.
- [ ] A scale or transformation that does not exaggerate; colour choices readable to colour-blind
  viewers (VERIFY with a checker).
- [ ] Source script named for each figure.

## Before submission

- [ ] Every number in the text regenerates from the stored code and data.
- [ ] Citations for datasets, software and databases include versions.
- [ ] Supplementary material does not contradict the main text.
