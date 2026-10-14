---
name: parameter-estimation-model-selection
description: Fits model parameters to data and chooses between competing models, covering least squares and likelihood, error models, identifiability (structural and practical, profile likelihood), sloppy parameters, poorly posed inverse problems, the Akaike information criterion, AICc, BIC and Akaike weights, nested F-tests, cross-validation, overfitting, noise, and reporting uncertainty. Use for "fit my model to the data", "are my parameters identifiable", "which model is better", "compute AIC for these fits", "my fit is good but the parameters are huge", "how many parameters can my data support", "confidence intervals for fitted parameters". Use enzyme-kinetics for rate-law fitting, ode-dynamics for the model itself, quantitative-research-methods for measurement and study design, and model-review to audit a fitted model.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# Parameter estimation and model selection

## Purpose and activation

Fitting a model to data is an inverse problem: many parameter sets may fit equally well, and a good fit
says little about whether the parameters mean anything. Model selection asks which of several structures
the data support, balancing fit against complexity. Activate when parameters are estimated from data,
when models are compared, or when a fit's parameters look implausible.

## Required inputs

The model or models; the data with units, replicates and measurement error; which parameters are fitted
and which fixed (with sources); the error model (additive, proportional, log-normal); and the question
(values, prediction, mechanism discrimination).

## Workflow

1. **State the error model** and the objective: least squares is maximum likelihood only for independent,
   normal, constant-variance errors. Weight by the measurement variance otherwise, or fit on the log scale.
2. **Check structural identifiability** before fitting: could perfect, noise-free data determine each
   parameter? Parameters that only enter as a product or ratio cannot be separated.
3. **Fit from many starting points;** nonlinear fits have local minima. Keep every solution with a similar objective.
4. **Check practical identifiability** with a profile likelihood: fix one parameter at a grid of values, refit
   the rest, and see whether the objective rises enough on both sides. A flat profile means the data do not
   determine that parameter.
5. **Compare models** fitted to the same data with `python3 scripts/fitstats.py compare MODELS.csv` (AICc ranks and
   Akaike weights) or, for nested models, `python3 scripts/fitstats.py ftest --rss1 --k1 --rss2 --k2 --n`. Use
   `python3 scripts/fitstats.py ic --rss --n --k` for one fit.
6. **Test prediction** on data not used for fitting (hold-out or cross-validation); in-sample fit always
   improves with more parameters.
7. **Report uncertainty:** intervals from the profile likelihood or bootstrap, correlations between parameters,
   and which conclusions depend on poorly determined parameters.
8. **Interpret with the consequences in mind** (`references/estimation-pitfalls.md`): a choice of method is
   defensible only if its assumptions match the data and the use the result will be put to.

## Decision framework

| Situation | Choose |
|---|---|
| Few models, same data, n/k below about 40 | AICc and Akaike weights |
| Nested models | F-test or likelihood-ratio test, and AICc as a check |
| Large n, aim is finding the true model among candidates | BIC (penalises parameters more) |
| Aim is prediction | Cross-validation error |
| Flat profile likelihood | Fix the parameter from literature, reparameterise, or design a new experiment |
| Several models nearly tied | Report all, or average predictions with Akaike weights |
| Errors grow with the signal | Fit log-transformed data or use proportional weights |

## Failure and edge cases

- **Comparing AIC across different datasets** or different transformations of the data.
- **k miscounted:** forgetting the error variance in one model but not another.
- **A single local optimum reported** as the answer.
- **Point estimates for non-identifiable parameters,** quoted to four digits.
- **Overfitting:** a model that fits noise, shown by poor prediction on held-out data.
- **Treating ΔAIC of 1 as decisive.** Differences below about 2 give little reason to prefer one model.
- **Selecting a model, then reporting its p-values** as if no selection had happened.

## Validation

- `python3 scripts/fitstats.py --selftest` passes; its F-distribution tail was checked against SciPy.
- Residuals look like the assumed error model (no trend, constant spread on the chosen scale).
- Each reported parameter has an interval, and non-identifiable ones are flagged.
- The chosen model predicts held-out data at least as well as the alternatives.
- Falsifier: a held-out prediction outside the interval the fitted model gives.

## Expected output

The error model and objective; identifiability results; fitted values with intervals and correlations; a
model comparison table (RSS, n, k, AICc, Δ, weight); held-out prediction error; and the conclusions that
depend on uncertain parameters.

## Sources and confidence

- Sauter and Albrecht 2023, doi:10.11647/OBP.0291, learning checklist Part 4 (supplied text): Akaike
  information criterion, poorly posed problems, sensitivity analysis and noise are listed topics. Chapter
  text not seen
- Akaike 1974, doi:10.1109/TAC.1974.1100705; Burnham and Anderson, *Model Selection and Multimodel
  Inference*, 2nd ed., Springer, doi:10.1007/b97636 (Crossref dates the record 2004); Raue et al. 2009,
  doi:10.1093/bioinformatics/btp358; Gutenkunst et al. 2007, doi:10.1371/journal.pcbi.0030189; Kirk, Thorne and
  Stumpf 2013, doi:10.1016/j.copbio.2013.03.012. Records checked 2026-10-15; content from author knowledge, VERIFY
- The point that a method's value depends on its appropriateness, the decisions made while using it, a
  defensible interpretation and data quality: Hattie's foreword to Teo (Ed.), *Handbook of Quantitative
  Methods for Educational Research*, Sense 2013, doi:10.1007/978-94-6209-404-8 (supplied text, paraphrased)
