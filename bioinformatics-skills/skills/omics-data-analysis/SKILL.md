---
name: omics-data-analysis
description: Analyses high-throughput biological tables from transcriptomics, proteomics, interactomics and metabolomics, plus the clustering, dimension reduction and network methods used on them, covering design and replication, quality control, normalisation, batch effects, missing values, differential testing with correction, clustering and PCA, enrichment, and networks from interaction data or correlation. Use for "analyse this expression matrix", "cluster these samples", "run a PCA", "is this a batch effect", "build a network from correlations", "read this heatmap", "false positives in two-hybrid data". Use sequence-statistics for the tests and corrections, sequence-formats for reading files, and bioinformatics-review to audit the finished analysis.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Omics data analysis

## Purpose and activation

Take a table of measurements (genes, proteins or metabolites by samples), or a list of
interactions, and reach conclusions that survive the ways such data go wrong. The common failures
are not in the statistics but in the design: batch confounded with condition, no real replicates,
and clusters or networks that are artefacts of a threshold. Activate when the user has such a
table, a heatmap, a cluster, a network, or an interaction list.

## Required inputs

The data matrix and what the rows and columns are; the sample table (condition, batch, date,
replicate type, any pairing); the platform and how values were produced (counts, intensities,
ratios); what was already normalised or filtered; the comparison of interest; and the number of
samples per group.

## Workflow

1. **Read the design before the data.** Count biological replicates per group. Technical
   replicates of one sample are not biological replicates. If batch and condition are perfectly
   aligned, the effect cannot be separated from the batch; say so and stop.
2. **Quality control.** Missing values by sample and feature, distributions per sample, outliers,
   and a first look at sample-to-sample structure (PCA or clustering) coloured by condition and by batch.
3. **Normalise for the data type** (`references/clustering-and-dimension-reduction.md` for the
   scale and distance choices; the platform's documentation for the rest). Record every step.
4. **Test per feature** with a method suited to the data, then correct for the number of features
   with `adjust` from `sequence-statistics`. Report effect sizes, not only adjusted p-values.
5. **Cluster or reduce** only to look at structure or to generate hypotheses. A clustering
   method always returns clusters; check that they are stable and not driven by batch.
6. **Enrichment.** Test a gene or protein set against the features that were measured, not the
   whole genome, using the hypergeometric calculation in `sequence-statistics`.
7. **Networks.** Decide whether the edges are measured interactions or inferred from correlation,
   and read the network accordingly (`references/network-inference.md`).
8. **Report limits:** replicates, batch, missing data, what was filtered, and what the platform cannot see.

## Decision framework

| Data | Main risks | First checks |
|---|---|---|
| Transcriptomics (expression of many genes) | Batch, library or intensity scale, low counts, few replicates | Sample structure by batch; per-sample distributions |
| Proteomics (gel, column or mass-spectrometry based) | Missing values that depend on abundance, identification confidence, dynamic range | Missingness pattern; identification criteria |
| Interactomics (two-hybrid, crosslinking, affinity, correlated expression) | False positives and negatives, indirect links, method-specific bias | Overlap between methods; controls |
| Metabolomics (spectra and metabolite tables) | Identification, scaling, strong correlations between metabolites | Scaling choice; pooled quality-control samples |
| Clustering or PCA of samples | Batch driving structure, scaling choices, over-reading | Colour by batch; stability across settings |
| Network from correlation | Threshold-made structure, indirect effects, hairball | Edge count vs threshold; shuffled-data network |

## Implementation guidance

- Keep an immutable copy of the raw table and do every transformation in a script, never by hand.
- Do multiple-testing correction over all features tested, including those filtered out by a
  rule chosen after seeing the data (or choose the filter before).
- For each plot, note what the axes and colours are; a heatmap's row and column order is a choice.
- Run the whole analysis on a shuffled sample-label version; it should find nothing.

## Failure and edge cases

- **Confounded design:** one batch per condition.
- **Pseudoreplication:** treating repeated measures or technical replicates as independent samples.
- **Normalising away the signal,** for example forcing every sample to the same distribution
  when conditions truly differ globally.
- **Missing values filled with zero** or with the mean without saying so.
- **Cluster number chosen to fit a story,** or clusters read as biology without stability checks.
- **PCA axes interpreted as processes;** components are summaries of variance, not mechanisms.
- **Correlation read as interaction,** and thresholds chosen to give a pleasing network.
- **Enrichment against the wrong background,** giving enrichment for anything expressed in the tissue.
- **Database annotation circularity:** an enrichment term that was itself derived from similar data.

## Validation

- Shuffled-label rerun finds roughly the nominal false-discovery fraction, no more.
- A positive control (a feature known to differ) is recovered.
- Results do not change materially when one sample, one batch, or one parameter is changed.
- Falsifier: the top finding disappears after adjusting for batch.

## Expected output

The design summary (replicates, batches), the quality-control findings, the normalisation and
tests used with their settings, adjusted results with effect sizes, the structure analysis with
its stability checks, and a limits paragraph.

## Sources and confidence

- Ramsden, *Bioinformatics: An Introduction*, 2nd ed.: ch. 14 (transcriptomics, proteomics, protein
  identification, isotope-coded affinity tags, protein microarrays, expression patterns, the kinome),
  ch. 15 (interactomics: inference of regulatory networks, in vivo and in vitro methods, global
  statistics), ch. 16 (metabolomics: data collection, analysis, metabolic regulation and networks),
  ch. 7 (systems and networks) and ch. 8 (clustering, principal component and discriminant analysis,
  wavelets, multidimensional scaling and seriation, visualization): section titles only, from the
  table of contents; the text of these chapters was not supplied
- Ch. 1.2 (supplied): the usual physical-science routine of assigning numbers and then manipulating
  them by public rules is often confounded in biology, so the first question is always how the
  numbers were obtained
- All methods guidance, thresholds and pitfalls: general practice from author knowledge, VERIFY
  against the platform documentation and a statistics text for the specific data type
- Not covered: single-cell data, imaging, spatial data, clinical cohorts, machine-learning
  prediction pipelines
