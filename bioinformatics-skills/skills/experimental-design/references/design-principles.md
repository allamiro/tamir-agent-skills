# Design principles

All guidance here is general practice; VERIFY it against the guidelines of your field.

## Kinds of replicate

| Kind | What varies | What it tells you | Counts as a sample |
|---|---|---|---|
| Biological replicate | The individual: a different animal, patient, culture grown separately | Variation between individuals, which conclusions about a population need | Yes |
| Technical replicate | The assay: the same material measured again | Noise of the measurement | No |
| Pseudoreplicate | Nothing independent: many cells or reads from one sample | Nothing about the population | No |

Reads, cells, spots and probes from one sample are pseudoreplicates of that sample. Test and
report at the level of the sample.

## Randomisation, blocking, balance

- **Randomise** the allocation of conditions to positions, batches and run order, with a recorded seed.
- **Block** on a known nuisance factor (batch, plate, day) by putting every condition in every block.
- **Balance** the number per condition, so no group carries more weight in the variance estimate.
- Include a **reference sample** in every batch so batches can be compared.

## Batch effects

A batch is anything done together that could shift the measurement: extraction day, reagent lot,
operator, plate, lane, instrument. If condition and batch are perfectly aligned, no method can
separate them. If they are only partly aligned, adjusting is possible but fragile. The only reliable
fix is design: spread every condition over every batch.

## Sample size and power

| Term | Meaning |
|---|---|
| Effect size d | Difference in means divided by the common standard deviation |
| Alpha | Chance of a false positive per test (0.05 is a convention, not a law) |
| Power | Chance of detecting a true effect of size d (0.8 is a convention) |
| Per-group n | Samples in each of two equal groups |

- n grows with 1 / d squared: halving the effect size quadruples the samples.
- Testing thousands of features lowers the usable alpha; with `--tests`, alpha is divided by the
  number of tests (the Bonferroni choice, the most demanding one).
- The effect size comes from a pilot or earlier work; a small pilot gives an unreliable estimate.
- For counts and many correlated features the simple formula is only a guide.
- Power is for the planned analysis. Changing the analysis after seeing data changes the power.

## Controls

| Control | Purpose |
|---|---|
| Positive | A case where the answer is known to be yes: shows the assay can detect an effect |
| Negative | A case where the answer is known to be no: shows what noise looks like |
| Blank or mock | Reagent-only sample: shows contamination |
| Spike-in | Known material added at a known amount: checks quantification |
| Reference sample | Same material in every batch: checks batch drift |

## Pilot

A pilot of a few samples checks the assay, the batch layout, the pipeline and the variance. It is
not a source of the final effect size and not a place to look for results.

## Writing the plan

Fix before the data arrive: the primary comparison and its direction, the number of tests, the
correction, the exclusion criteria, the sample size and the stopping rule. Date it and keep it with
the data.
