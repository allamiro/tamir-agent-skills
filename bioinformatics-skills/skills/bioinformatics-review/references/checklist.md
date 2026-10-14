# Review checklist

Work down the list for each claim. Mark each item pass, fail, not applicable, or not checked.

## Claim

- [ ] The claim can be false, and the result that would falsify it is stated.
- [ ] The wording matches the evidence: candidate, correlation, similarity and enrichment are not
  upgraded to gene, interaction, homology and function.
- [ ] An effect size and its uncertainty are given, not only a p-value.

## Null model and statistics

- [ ] The null model is stated and was generated or calculated, not assumed.
- [ ] The number of tests is stated, including those not reported.
- [ ] A correction for multiple testing was applied to the whole family of tests.
- [ ] The tail and the test match the question (at least k, not exactly k).
- [ ] Independence is justified for neighbouring positions, overlapping words and related samples.
- [ ] A shuffled-label or shuffled-sequence rerun gives about the nominal rate of positives.

## Data layer

- [ ] Every input has a source, accession, version and date.
- [ ] The genome build and annotation release are stated and the same throughout.
- [ ] The coordinate convention (0-based or 1-based, half-open or closed) is stated and consistent.
- [ ] Identifiers are mapped without losing or duplicating records, and counts match before and after.
- [ ] Units, scales and transformations are stated.
- [ ] File formats are what they claim to be, and nothing was silently dropped.

## Design

- [ ] Biological replicates are counted per group, and technical replicates are not counted as them.
- [ ] Batch, date and operator are balanced across conditions, or adjusted for with justification.
- [ ] No sample, sequence or gene appears in both training and test data, directly or through
  near-duplicates or relatives.
- [ ] Features and settings were chosen without looking at the test data.
- [ ] Controls: a positive control is recovered and a negative control is not.

## Methods and code

- [ ] Each figure and table traces to a script, its inputs and its parameters.
- [ ] Software versions, seeds and settings are recorded.
- [ ] Defaults are justified, or their effect is shown.
- [ ] Results are stable under small changes (one sample removed, another seed, another threshold).
- [ ] The code is available, and a clean-checkout rerun reproduces the numbers.

## Annotation and interpretation

- [ ] Functional labels do not come from the method being evaluated (no circularity).
- [ ] Database entries used as truth are checked for their own provenance.
- [ ] Enrichment uses the measured features as background, not the whole genome.
- [ ] Predicted genes, interactions and structures are called predictions.
- [ ] Species, strain and period of the data match the species the conclusion is about.

## Sensitive data

- [ ] Consent and access terms are met, and identifiers are not in code, logs or file names.

## Close-out

- [ ] The report states counts: claims checked, traced to a source, and findings by severity.
- [ ] The report states what was not checked.
