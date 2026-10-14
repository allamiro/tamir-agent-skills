# Estimation pitfalls and how to defend an interpretation

## Before fitting

- Count independent observations, not data points: ten time points from one culture are not ten replicates.
- Decide which parameters are fixed from the literature, and from which organism, temperature and assay.
- Write the error model down; it decides the objective function.

## While fitting

- Use several starting points spread over plausible ranges (log-uniform for rate constants).
- Bound parameters to physically meaningful ranges, and report when a fit sits on a bound.
- Record every model tried, including those discarded; selection among many models inflates apparent fit.

## After fitting

- Plot residuals against time, against the fitted value and against each input.
- Profile each parameter; report flat or one-sided profiles.
- Test on held-out data before calling the model validated.

## Defending the interpretation (after Hattie's foreword to Teo 2013, paraphrased)

Software makes sophisticated methods easy to run, which makes it easy to be impressed by output that cannot
bear the weight put on it. A defensible interpretation needs four things, each of which can be checked:

1. The method fits the question and the data (not chosen because it is available).
2. The decisions made while using it (starting values, error model, exclusions, number of components) are
   reported and justified.
3. The interpretation goes no further than the evidence, and states its consequences for the decision
   the result will inform.
4. The data are of adequate quality for that use.

The foreword also notes that many methods are special cases of a few general models (the generalised
regression model and the nonlinear factor model), so knowing the general model shows what each special
case assumes. For example, a Rasch model assumes a single dimension with all items related to it equally
strongly (`quantitative-research-methods`).
