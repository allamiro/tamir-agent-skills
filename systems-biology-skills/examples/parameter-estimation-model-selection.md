# `parameter-estimation-model-selection`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Which model is better? I fitted three candidate models to the same 12 data points: model A (residual sum of squares 2.1, 3 parameters), model B (RSS 1.6, 4 parameters), model C (RSS 1.9, 4 parameters). Compute AICc and Akaike weights and tell me how strong the evidence is.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 2,027 | 2,086 |
| Input tokens read across all turns (including cached context) | 30,422 | 36,427 |
| Extra input tokens when the skill is installed | | +6,005 |
| Cost, US dollars at list price | 0.100 | 0.150 |
| Skills invoked in the sample run | none | none |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 290 tokens for its name and description, which are in every session where the skill is installed, and about 1,900 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
# Model A is best by AICc, but the evidence is moderate at most

## Method

For least-squares fits with independent Gaussian errors:

- AIC = n·ln(RSS/n) + 2K
- AICc = AIC + 2K(K+1)/(n − K − 1)
- Akaike weight wᵢ = exp(−Δᵢ/2) / Σ exp(−Δⱼ/2)

Here n = 12. Following the standard convention (Burnham & Anderson), K also counts the error variance σ², so K = (fitted parameters) + 1.

## Results (K includes σ²)

| Model | RSS | K | n·ln(RSS/n) | AIC | Small-sample correction | **AICc** | **ΔAICc** | **Weight** |
|---|---|---|---|---|---|---|---|---|
| A | 2.1 | 4 | −20.92 | −12.92 | +5.71 | **−7.20** | **0.00** | **0.77** |
| B | 1.6 | 5 | −24.18 | −14.18 | +10.00 | **−4.18** | **3.02** | **0.17** |
| C | 1.9 | 5 | −22.12 | −12.12 | +10.00 | **−2.12** | **5.08** | **0.06** |

- **A is best.** B fits better (lower RSS), but with only 12 points the penalty for its extra parameter (+4.3 in the correction term alone) outweighs that gain.
- **A vs B:** the evidence ratio is 0.77 / 0.17 ≈ **4.5 : 1**, and Δ = 3.0. That counts as "considerably less support" for B, but B isn't ruled out. People often use Δ > 10 as the point where a model is essentially ruled out, and this is nowhere near that.
- **A vs C:** Δ = 5.1, about 13 : 1. C has little support.
- **B vs C:** both have the same K, so the comparison depends only on RSS. B beats C by Δ = 2.1 (about 2.8 : 1) under either convention.

## Check: if you don't count σ² (K = 3, 4, 4)

| Model | AICc | Δ | Weight |
|---|---|---|---|
| A | −11.92 | 0.00 | 0.60 |
| B | −10.46 | 1.45 | 0.29 |
| C | −8.40 | 3.51 | 0.10 |

The ranking stays the same, but the evidence gets weaker: A vs B drops to about **2 : 1**, with Δ < 2, which is essentially a tie. Whichever convention you use, apply it to all three models and report which one it was.

## How strong is the evidence?

**Moderate at best.** A is the most parsimonious choice, but about 20–30% of the weight stays on B. I wouldn't call A "the true model." Points to keep in mind:

1. **With only n = 12, the AICc correction dominates.** It is larger than the RSS differences, so a few new data points could change the ranking.
2. **Check the assumptions.** All three models must be fitted to exactly the same 12 data points, with the same weighting and transformation. The residuals should be roughly independent with constant variance. If you used weighted least squares, use the weighted RSS.
3. **If A is nested in B** (B = A plus one parameter), you can also run an extra-sum-of-squares F-test as a second check: F = [(2.1 − 1.6)/1] / [1.6/(12 − 4)] = 2.5, with df = (1, 8), giving p ≈ 0.15. That also says the extra parameter isn't justified.
4. **If you care about predictions or parameter values more than picking one model,** use model averaging with these weights instead of committing to A.
5. **To separate A from B more clearly,** collect more data where their predictions differ most. Adding more points where they already agree won't help.
````

## Answer without the skill (excerpt)

````text
# AICc comparison: model A is preferred, but the evidence is only moderate

**Model A comes out ahead, with about a 77% Akaike weight.** It is roughly 4.5 times more likely than B to be the best model in this set (in the Kullback–Leibler sense). That's a clear lean towards A, not a decisive result.

## Method
For least-squares fits, assuming independent Gaussian errors:

- AIC = n·ln(RSS/n) + 2K
- AICc = AIC + 2K(K+1)/(n − K − 1)
- n = 12, and K = number of fitted parameters + 1, because the error variance σ² is also estimated.

| Model | RSS | p | K | n·ln(RSS/n) | AIC | Correction | **AICc** | ΔAICc | exp(−Δ/2) | **Weight wᵢ** |
|---|---|---|---|---|---|---|---|---|---|---|
| A | 2.1 | 3 | 4 | −20.916 | −12.916 | 5.714 | **−7.20** | 0.00 | 1.000 | **0.770** |
| B | 1.6 | 4 | 5 | −24.179 | −14.179 | 10.000 | **−4.18** | 3.02 | 0.221 | **0.170** |
| C | 1.9 | 4 | 5 | −22.117 | −12.117 | 10.000 | **−2.12** | 5.08 | 0.079 | **0.061** |

**Evidence ratios:** A vs B = 4.5; A vs C = 12.7; B vs C = 2.8.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
