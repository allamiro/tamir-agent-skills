---
name: quantitative-research-methods
description: Guides measurement and quantitative study design for biological, biomedical and educational research, covering construct maps, item or readout design, outcome spaces and scoring, measurement models (classical test theory, Rasch, IRT) and their assumptions (monotonicity, unidimensionality, local independence), levels of measurement, reflective versus formative indices, reliability and validity evidence, missing responses, effect sizes, and choosing among regression, multilevel, longitudinal, factor, SEM, mediation, moderation, mixture and meta-analytic methods. Use for "is my readout measuring what I think", "design a questionnaire or scoring rubric", "compute Cronbach's alpha", "fit a Rasch model", "which statistical method fits my design", "how big is this effect", "evaluate a teaching intervention". Use parameter-estimation-model-selection for mechanistic model fitting, multivariate-omics for omics tables, and modeling-research-planning for the whole proposal.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# Quantitative research methods and measurement

## Purpose and activation

Every quantitative claim rests on a measurement, and a measurement is only as good as the argument that
it reflects the intended property. This holds for a questionnaire on self-efficacy, a scoring rubric for
student models, a histology score, a composite disease index, or a reporter readout of "pathway activity".
This skill makes that argument explicit, chooses an analysis that fits the design, and keeps the
interpretation within what the evidence and its consequences allow. Activate when a study measures
something not directly observable, combines items or readouts into a score, compares groups, or chooses a
statistical method.

## Required inputs

The construct or property to be measured and why; the population; the instrument or readouts (items,
markers, assays), with how they are scored; the design (groups, repeated measures, nesting, sample size);
the intended use of the scores (describe, compare, decide about individuals, evaluate an intervention);
and the data, if collected.

## Workflow

1. **Define the construct with a construct map:** an ordered description of what low, middle and high levels
   of the property look like, on the respondent (or sample) side and the item (or readout) side. If no
   ordering can be written, the construct is not yet defined well enough to measure.
2. **Design the items or readouts** so that each targets a known region of the construct map, and say what
   observation each produces (`references/construct-modelling.md`).
3. **Define the outcome space:** a finite, exhaustive, ordered and well-defined set of response categories,
   with scoring rules, exemplars and rater training where judgement is involved. Decide how missing responses
   are coded: not administered is missing; a run of omitted hard items at the end may be scored differently;
   either way, investigate why responses are missing.
4. **Listen to respondents:** pilot with think-aloud sessions or exit interviews (for assays, pilot runs with
   known samples), record them, and revise items whose responses do not follow the intended reasoning.
5. **Choose and fit a measurement model** that relates scores back to the construct map: classical test theory
   (observed score = true score + error) for reliability of totals, or a Rasch or IRT model to place items and
   persons on one scale. Check its assumptions: monotonicity, unidimensionality, local independence
   (`python3 scripts/measure.py rasch ITEMS.csv` reports infit, outfit and Yen's Q3; `python3 scripts/measure.py alpha ITEMS.csv`
   reports Cronbach's alpha with item-rest correlations; `python3 scripts/measure.py missing ITEMS.csv` shows the missing pattern).
6. **Establish the level of measurement by testing,** not by assertion: scores are interval-level only if a
   model that implies it fits. Ordinal scores need methods that respect order.
7. **Decide reflective or formative:** if the items are caused by the construct (they should correlate),
   reliability statistics apply; if the items define it (an index such as socio-economic status), they need
   not correlate and alpha is meaningless.
8. **Assemble validity evidence** (`references/validity-evidence.md`): content, response processes, internal
   structure, relations to other variables, and consequences of use.
9. **Choose the analysis** that matches the design (decision table), report effect sizes with intervals
   (`python3 scripts/measure.py effect A.csv B.csv`; `python3 scripts/measure.py sb --r --factor` for test length),
   and interpret within the intended use, stating the consequences of being wrong.

## Decision framework

| Design or question | Method family | Key assumption to check |
|---|---|---|
| One outcome, several predictors | Multiple regression | Linearity, independent errors, collinearity |
| Binary outcome | Logistic regression | Events per predictor, separation |
| Students in classes, cells in patients, repeated measures | Multilevel (hierarchical) models | Correct nesting structure |
| Change over time | Longitudinal models (growth curves, mixed models) | Missing-data mechanism, time coding |
| Several outcomes, group differences | MANOVA | Covariance homogeneity, more cases than outcomes |
| Latent constructs from items | Exploratory then confirmatory factor analysis | Separate samples for exploring and confirming |
| Relations among latent constructs | Structural equation modelling | Measurement model fits first; equivalent models exist |
| Is the instrument the same across groups | Measurement invariance testing | Configural, metric, scalar steps in order |
| Does X act through M | Mediation analysis | Temporal order, no unmeasured confounding of M and Y |
| Does the effect of X depend on W | Moderation (interaction) | Centring, power for interactions |
| Unobserved subgroups | Mixture or latent class models | Number of classes not chosen by fit alone |
| Combine studies | Meta-analysis | Comparable effect sizes, heterogeneity, publication bias |
| Emergent behaviour from individual rules | Agent-based modelling | Calibration and validation against data |

| Use of scores | Interpretation | Needs |
|---|---|---|
| Rank against a group | Norm-referenced | A representative norm group |
| Judge against a standard | Criterion-referenced | A construct map with described levels |
| Look back (grade, certify) | Summative | High reliability for individual decisions |
| Guide next steps | Formative | Diagnostic categories, quick feedback |
| Describe | Descriptive measurement | The measurement model |
| Explain or predict scores from item or person features | Explanatory measurement | Covariates in the model |

## Failure and edge cases

- **A construct named but not defined,** so items drift to whatever is easy to ask or assay.
- **Alpha reported as proof of validity,** or computed for a formative index.
- **High alpha from many items or duplicated wording,** not from a coherent construct.
- **Sum scores of Likert items treated as interval** without a model that supports it.
- **Local dependence:** items sharing a stem, passage or sample inflate reliability (Q3 flags it; judge Q3
  against its baseline of about -1/(L-1) for L items, not against zero).
- **Missing responses coded as wrong** when the item was never administered.
- **Factor analysis explored and confirmed on the same sample.**
- **Effect size without an interval,** or Cohen's thresholds (0.2, 0.5, 0.8) applied without context.
- **Mediation claimed from cross-sectional data** without addressing confounding.
- **Consequences ignored:** a score used for a decision it was never validated for.

## Validation

- `python3 scripts/measure.py --selftest` passes (hand-computed alpha, Spearman–Brown, d and g; Rasch centring,
  ordering, extreme scores and local dependence on simulated data).
- The construct map, items design, outcome space and measurement model are written down and consistent.
- At least two sources of validity evidence beyond internal consistency are reported.
- The analysis matches the design's nesting and the level of measurement.
- Falsifier: respondents' think-aloud reasoning does not follow the intended construct levels, or scores fail
  to relate to an external variable they should predict.

## Expected output

A filled `assets/templates/measurement-plan.md`, containing: the construct map; items or readouts mapped to it; the outcome space and scoring with missing-data rules;
the measurement model with assumption checks; reliability and validity evidence; the analysis plan or
results with effect sizes and intervals; and an interpretation that names the intended use and its
consequences.

## Sources and confidence

- Wilson and Gochyyev, "Psychometrics", in Teo (Ed.), *Handbook of Quantitative Methods for Educational
  Research*, Sense 2013, pp. 3–30, doi:10.1007/978-94-6209-404-8_1 (supplied text, partial; All Rights
  Reserved, so ideas are paraphrased and nothing is quoted): construct modelling with four building blocks
  (construct map, items design, outcome space, measurement model); Stevens' levels established by testing a
  model; fundamental, derived and implicit measurement; norm- versus criterion-referenced, summative versus
  formative, descriptive versus explanatory, reflective versus formative; monotonicity, unidimensionality,
  local independence; think-alouds and exit interviews; missing-response coding; X = T + E; the Rasch model
- Hattie's foreword to the same handbook (supplied text): interpretation needs defence and attention to
  consequences, method appropriateness, decisions made, and data quality
- Method families follow the handbook's table of contents (doi:10.1007/978-94-6209-404-8); their descriptions
  are author knowledge, VERIFY
- Cronbach 1951, doi:10.1007/BF02310555; Yen 1984, doi:10.1177/014662168400800201; Cohen 1992,
  doi:10.1037/0033-2909.112.1.155; Rubin 1976, doi:10.1093/biomet/63.3.581; Messick 1995,
  doi:10.1037/0003-066X.50.9.741; Baron and Kenny 1986, doi:10.1037/0022-3514.51.6.1173. Records checked on
  Crossref 2026-10-15; content from author knowledge, VERIFY
- Sauter and Albrecht 2023, doi:10.11647/OBP.0291: the workbook reports educational effect sizes as Cohen's d
  with the conventional small, medium and large readings (supplied text)
