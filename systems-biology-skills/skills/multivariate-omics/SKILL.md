---
name: multivariate-omics
description: Analyses many-variable biological data such as transcriptomics, proteomics and metabolomics tables with multivariate methods, covering centring and scaling, principal component analysis (PCA) with explained variance, loadings and scores, partial least squares regression (PLSR) and PLS-DA, variable importance in projection (VIP), validation by cross-validation and permutation, and how PCA relates to factor analysis, clustering, MANOVA and regression. Use for "run a PCA on my omics data", "which variables drive the separation", "compute VIP scores", "PLS regression of phenotype on metabolites", "should I scale my variables", "is my PLS-DA overfitted", "PCA or factor analysis". Use parameter-estimation-model-selection for mechanistic model fitting, quantitative-research-methods for measurement and latent constructs, and network-analysis for interaction networks.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# Multivariate analysis of omics data

## Purpose and activation

Omics tables have more variables than samples, so univariate tests struggle and patterns lie in
combinations of variables. PCA finds the main directions of variation without using group labels; PLS
regression finds directions in the variables that predict a response; VIP scores rank variables by their
part in that prediction. Supervised methods overfit easily when variables outnumber samples. Activate when
the user has a samples-by-variables table and wants structure, separation or prediction.

## Required inputs

The table (samples by variables) with units and preprocessing so far (normalisation, log transform,
missing value handling, batch); sample metadata (groups, batches, response variable); the number of
samples per group; and the question (explore, explain a response, classify).

## Workflow

1. **Preprocess deliberately:** log-transform skewed intensities, handle missing values (and say why they are
   missing: below detection is not missing at random), and record batches.
2. **Centre, and decide on scaling:** `--scale` (unit variance) when variables have different units or ranges;
   without it, high-variance variables dominate.
3. **Explore with PCA** using `python3 scripts/multivar.py pca DATA.csv [--scale] [--components K]`. Read the explained
   variance per component, the scores (samples) and the loadings (variables). Colour scores by batch before
   colouring by biology: a batch effect on PC1 is common.
4. **Predict a response with PLS** using `python3 scripts/multivar.py pls DATA.csv --y COLUMN [--components K]`; it reports
   coefficients, R² and VIP. A VIP above about 1 is a heuristic for an influential variable, not a test.
5. **Validate every supervised model:** choose the number of components by cross-validation (report Q²), and
   run a permutation test (refit with shuffled labels) to show the separation is better than chance.
6. **Choose the right method family** with the decision table; the handbook chapters on cluster analysis,
   MANOVA, factor analysis and regression each answer a different question (`references/method-map.md`).
7. **Report** preprocessing, scaling, components, validation statistics and the variables, with the caveat
   that loadings and VIP show association, not mechanism.

## Decision framework

| Question | Method | Watch for |
|---|---|---|
| Main sources of variation, outliers, batch | PCA | Scaling choice changes the result |
| Which variables predict a continuous response | PLS regression, VIP | Overfitting; validate |
| Separate known groups | PLS-DA or penalised logistic regression | Perfect separation is expected with many variables; permutation test |
| Find groups without labels | Cluster analysis | Clusters appear in any data; check stability |
| Do groups differ on several variables together | MANOVA (needs more samples than variables) or PERMANOVA | Assumptions on covariance |
| Latent constructs behind correlated variables | Factor analysis | PCA is not factor analysis; see `quantitative-research-methods` |
| Thousands of variables, univariate testing | Per-variable tests with false discovery rate control | Not a multivariate method, often the right first step |

## Failure and edge cases

- **Supervised separation shown without validation:** with more variables than samples, PLS-DA separates random labels.
- **Feature selection before cross-validation** (selecting on all samples, then validating) leaks information.
- **Batch confounded with group,** making the biology inseparable from the batch.
- **Unscaled data** where one high-abundance variable dominates.
- **VIP ranks read as significance.**
- **Missing values imputed as zero** when they mean "below detection".
- **PCA loadings interpreted as latent constructs** (that needs factor analysis and a measurement model).

## Validation

- `python3 scripts/multivar.py --selftest` passes; PCA and PLS outputs were checked against scikit-learn.
- Explained variance sums to at most 100 percent; scores times loadings reconstruct the centred data.
- Cross-validated Q² and a permutation test are reported for any supervised model.
- Conclusions hold when the analysis is repeated without the most extreme samples.
- Falsifier: the permutation distribution includes the observed separation.

## Expected output

Preprocessing record; PCA explained variance, score and loading summaries with batch checks; PLS
coefficients, R², Q², VIP and permutation result; the method choice justified against alternatives; and
the variables of interest as hypotheses.

## Sources and confidence

- Sauter and Albrecht 2023, doi:10.11647/OBP.0291, learning checklist Part 1 (supplied text): PCA, PLSR and VIP
  are listed as priority-1 topics. Chapter text not seen
- Wold, Sjöström and Eriksson 2001, doi:10.1016/S0169-7439(01)00155-1 (record checked on Crossref 2026-10-15;
  content from author knowledge, VERIFY)
- The method families (cluster analysis, MANOVA, factor analysis, regression, logistic regression) follow the
  table of contents of Teo (Ed.), *Handbook of Quantitative Methods for Educational Research*, Sense 2013,
  doi:10.1007/978-94-6209-404-8; only the table of contents and chapter 1 were supplied, so the method
  descriptions are author knowledge, VERIFY
