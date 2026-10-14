---
name: experimental-design
description: Designs the sampling, replication, controls and batch layout of a bioinformatics or omics study before any data are collected, and works out sample size and power for a two-group comparison. Use for "how many replicates do I need", "how many samples", "plan my sequencing experiment", "is my design confounded with batch", "randomise samples across batches", "what controls should I include", "power analysis". Use bioinformatics-workflow for the whole analysis plan, omics-data-analysis once data exist, and sequence-statistics for the tests themselves.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Experimental design

## Purpose and activation

Fix the problems that no analysis can repair afterwards: too few independent samples, a condition
tangled up with a batch, missing controls. Activate before samples are collected or sequenced, or
when someone asks why a result will not hold up and the cause is how the data were gathered.

## Required inputs

The comparison of interest in words; what counts as one independent sample (an animal, a patient,
a culture, a plate); the expected size of the difference and the variability, from a pilot or the
literature; the number of features that will be tested; the practical limits (budget, samples
available, how many can go on one run or batch); and any pairing or time structure.

## Workflow

1. **Name the unit of replication.** The independent unit is the thing that could have turned out
   differently by chance. Repeated measures of one sample are technical replicates and do not count
   as more samples.
2. **Choose the replicates.** Biological replicates carry the between-sample variation the
   conclusion is about. Technical replicates measure the assay's noise. Often more samples beat
   deeper sequencing of fewer (VERIFY for your assay).
3. **Estimate the effect and the spread** and state where each came from. A single small pilot gives
   a poor estimate, and an effect picked because it looked large is usually overestimated.
4. **Calculate the sample size.** `python3 scripts/design.py n --d 0.5 --tests 1` gives samples per
   group for a standardized effect d; `--tests` divides alpha by the number of tests. `power --n N
   --d D` gives the power for a fixed size.
5. **Plan controls:** a positive control, a negative control, blanks or mock samples, and a
   reference sample run in every batch.
6. **Spread conditions over batches.** `python3 scripts/design.py assign SAMPLES.csv --batches 3`
   deals every group out evenly. Then test the layout with `confound`, which reports whether batch
   and condition are tangled up.
7. **Write the plan down before the data come in:** the primary comparison, exclusion rules, the
   correction for many tests and the stopping rule (`assets/templates/study-design.md`).
8. **Run a pilot** to check the assay, the layout and the pipeline on a few samples.

## Decision framework

| Situation | Choice |
|---|---|
| Two groups, a continuous measurement | `design.py n` as a first estimate |
| Counts such as RNA-seq reads | The formula is only a guide; use a count-based power tool (VERIFY) |
| Paired or repeated samples | A paired design needs fewer samples; this script does not model it |
| Thousands of features, a few true effects | Raise n for the corrected alpha (`--tests`), or accept lower power |
| Samples cannot all go in one batch | Spread every group over every batch; never one group per batch |
| One batch is much better or cheaper | Still balance it; do not put all cases there |
| Unknown variability | Run a pilot; do not guess |

## Implementation guidance

- A sample sheet is a CSV with `sample` and `group` columns for `assign`, and any two columns for
  `confound`. Keep the sheet with the data.
- Randomise with a recorded seed, so the layout can be reproduced and audited.
- A design where Cramer's V between condition and batch is 1 has no way to separate them. Values
  near 0 are what a balanced layout gives.
- The sample-size formula is the normal approximation with a small-sample correction, and
  reproduces the usual table values (64, 26 and 17 per group for d = 0.5, 0.8 and 1.0). The power
  function is optimistic at small n.
- `references/design-principles.md` covers replicate types, batches, power and common designs.
- `references/measurement-and-interpretation.md` covers defining what a readout measures, reliability
  against validity, missing values, nested designs and interpreting with consequences in view.

## Failure and edge cases

- **Pseudoreplication:** many cells or reads from one animal counted as many samples.
- **Confounding:** treatment on one day and control on another, or one lane per condition.
- **Unbalanced groups** that make a variance estimate unreliable.
- **Sample size from a significant pilot,** which overestimates the effect.
- **Power for the wrong test:** a calculation for one comparison used for thousands.
- **Dropout:** samples lost to quality failure; plan for a margin.
- **Hidden batch factors:** extraction date, operator, reagent lot, sequencing lane.
- **Changing the plan after looking** at the data.

## Validation

- `python3 scripts/design.py --selftest` must pass.
- Hand check: d = 0.5 needs 64 per group, 128 samples in all.
- Hand check: a 2 by 2 layout of [[3, 2], [2, 3]] has Cramer's V of 0.2; [[5, 0], [0, 5]] has 1.
- Falsifier: shuffle group labels in the final data and rerun the analysis; the design must not
  produce effects that line up with the batches.

## Expected output

The unit of replication, the replicate plan, the assumed effect and variability with their source,
the sample size and power, the controls, the batch layout and its confounding check, the decisions
fixed in advance, and the pilot plan.

## Sources and confidence

- Ramsden, *Bioinformatics: An Introduction*, 2nd ed., ch. 1.2 (supplied text): the design of
  genetic association studies is left out of the book, so this skill is original guidance
- Sample size and power for two groups: standard normal-approximation results with a small-sample
  correction, checked against remembered table values (64, 26 and 17 per group) in the self-test; VERIFY
  the final number with a tool that matches your test
- Replicate types, batch practice, controls, count-data caveats: general practice from author
  knowledge, VERIFY against your field's guidelines
- Measurement and interpretation lessons: Teo (Ed.), *Handbook of Quantitative Methods for Educational
  Research*, Sense 2013, doi:10.1007/978-94-6209-404-8 (foreword and chapter 1 supplied, paraphrased, carried
  over to biology by analogy: VERIFY)
- Not covered: adaptive and sequential designs, mixed models, clinical trial design, time series
