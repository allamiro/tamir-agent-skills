# `experimental-design` prompts

Plan samples, replicates, controls and batches before any data exist, and work out how many samples
a comparison needs.

- **Give it:** the comparison, what counts as one independent sample, the expected effect and
  variability, the number of features to be tested, and the practical limits
- **Skill file:** [`skills/experimental-design/SKILL.md`](../skills/experimental-design/SKILL.md)
- **Reference and template:** [`design-principles.md`](../skills/experimental-design/references/design-principles.md) and
  [`study-design.md`](../skills/experimental-design/assets/templates/study-design.md)
- **Then:** [`omics-data-analysis`](omics-data-analysis.md) for the analysis, [`sequence-statistics`](sequence-statistics.md) for the tests

## 1. How many samples

> I want to compare treated and untreated cells and expect a difference of half a standard deviation. How many samples per group do I need at 80% power, and what changes if I will test 20,000 genes?

A good answer: about 64 per group for a single test, and about 250 per group when alpha is divided
by 20,000 tests, with a note that the formula is a guide and counts need a count-based calculation.

## 2. What counts as a replicate

> I have 3 mice per condition, 4 tubes of cells grown from each mouse, and I sequence every tube twice. How many independent samples do I have, and what are the others?

A good answer: three per condition, because the mouse is the independent unit; the tubes and the
repeat sequencing runs are technical or pseudoreplicates and should not be counted as more samples.

## 3. A batch layout

> I have 12 samples, 6 treated and 6 control, and room for 3 sequencing batches. Spread them across the batches, record the seed, and check the layout for confounding.

A good answer: each batch has 2 treated and 2 control, the seed is recorded, and the confounding
check reports Cramer's V of 0.

## 4. A design that cannot be rescued

> All my control samples were extracted on Monday and all my treated samples on Tuesday. What can I conclude from the comparison, and what should I do?

A good answer: nothing can separate treatment from extraction day (Cramer's V is 1); redo some
extractions with both conditions on each day, or report the comparison as confounded.

## 5. Using a pilot

> A pilot with 3 samples per group showed a large effect. Can I use its effect size to plan the main study?

A good answer: not directly, since a small pilot estimates the effect poorly and a large-looking
effect is usually overestimated; plan for the smallest effect worth detecting, and use the pilot to
check the assay and the layout.

## 6. Controls

> What controls should an RNA-seq experiment include, and what does each one tell me?

A good answer: a positive and a negative control, a blank or mock sample for contamination, a
spike-in for quantification, and a reference sample in every batch, each with its purpose.
