# `parameter-estimation-model-selection` prompts

Fit parameters to data, check that they can be identified, and choose between models without overfitting.

- **Give it:** the model or models, the data with replicates and measurement error, which parameters are fitted
  and which fixed, the error model, and the question
- **Skill file:** [`skills/parameter-estimation-model-selection/SKILL.md`](../skills/parameter-estimation-model-selection/SKILL.md)
- **Pitfalls and defending an interpretation:** [`estimation-pitfalls.md`](../skills/parameter-estimation-model-selection/references/estimation-pitfalls.md)

## 1. Which model is better

> Which model is better? I fitted three candidate models to the same 12 data points: model A (residual sum of squares 2.1, 3 parameters), model B (RSS 1.6, 4 parameters), model C (RSS 1.9, 4 parameters). Compute AICc and Akaike weights and tell me how strong the evidence is.

A good answer: AICc ranks model A first. Counting the parameters as given, the weights are about 0.60, 0.29 and
0.10 and B is at ΔAICc ≈ 1.45, so the data give little reason to prefer A strongly. Counting the error variance
as one more parameter (also standard), the weights are about 0.77, 0.17 and 0.06 and B is at Δ ≈ 3.0, which is
somewhat more support for A. Either convention is fine if it is stated and applied to all three models, and
the answer says how strong the evidence is under the one it uses.

## 2. Nested models

> A 2-parameter model gives RSS 4.0 and a nested 3-parameter model RSS 2.5 on 20 points. Is the extra parameter justified?

A good answer: F = ((4.0 − 2.5)/1)/(2.5/17) = 10.2 on (1, 17) degrees of freedom, p ≈ 0.005, so the extra
parameter is supported. AICc can be computed as a check, and held-out prediction is the stronger test.

## 3. Identifiability

> My fit is good but two parameters, k1 and k2, came out at 1e5 and 2e-4, and changing them together does not change the fit. What is going on?

A good answer: they are probably not separately identifiable, because only their product or ratio affects the
output. Check with a profile likelihood, and reparameterise to the identifiable combination. Then fix
one from the literature or design an experiment that separates them, and do not report the individual
point estimates.

## 4. AIC for one fit

> Compute AIC, AICc and BIC for a fit with residual sum of squares 1.2, 20 data points and 3 parameters, and explain when to use each.

A good answer: AIC ≈ −50.27, AICc ≈ −48.77 and BIC ≈ −47.28, from n ln(RSS/n) + 2k with the small-sample
correction and the ln n penalty. Use AICc when n/k is small (below about 40), and BIC when the aim is to
find the true model among candidates with large n. Only differences between models fitted to the same
data matter.

## 5. Defend the interpretation

> My fitted model says drug X works mainly through pathway A. A reviewer says my conclusion is not defensible. How do I check?

A good answer: check that the method fits the question and data, and that every analysis decision (error
model, starting points, exclusions, fixed parameters) is reported and justified. Test whether alternative
models with other mechanisms fit equally well, whether the key parameters are identifiable, and whether
held-out data support the prediction. Then state the consequences of being wrong for whatever decision
the result informs.
