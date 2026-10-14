# `enzyme-kinetics`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Fit Michaelis-Menten to my data (S in mM, v in µM/min): S,v 0.1,0.9; 0.25,1.9; 0.5,3.4; 1,4.9; 2,6.8; 4,8.0; 8,8.9. Is fitting the Lineweaver-Burk plot OK?

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 2,710 | 3,193 |
| Input tokens read across all turns (including cached context) | 115,077 | 249,088 |
| Extra input tokens when the skill is installed | | +134,011 |
| Cost, US dollars at list price | 0.148 | 0.253 |
| Skills invoked in the sample run | none | `enzyme-kinetics` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 280 tokens for its name and description, which are in every session where the skill is installed, and about 1,600 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
## Michaelis–Menten fit to your data

I fitted v = Vmax·S/(Km + S) by nonlinear least squares (Levenberg–Marquardt) on the untransformed rates.

| Parameter | Estimate | SE | 95% CI (t, 5 df) |
|---|---|---|---|
| **Vmax** | **10.06 µM/min** | 0.11 | 9.78 – 10.33 |
| **Km** | **1.01 mM** | 0.034 | 0.93 – 1.10 |

- **Residual sum of squares:** 0.040 (µM/min)². Residual SD is about 0.09 µM/min.
- **Residuals:** −0.003, −0.09, +0.08, −0.10, +0.13, −0.02, −0.03. The signs alternate and don't trend with S, so the hyperbola fits well.
- **Correlation between Vmax and Km:** 0.83. This is normal for this model. The data still pin down both values well because your S range (0.1–8 mM) spans about 0.1×Km to 8×Km.
- **Hill model as a check:** n = 1.03, so there's no sign of cooperativity. Adding n makes the fit worse by AICc (−23.0 vs −29.1 for Michaelis–Menten). Use plain Michaelis–Menten.

## Is fitting the Lineweaver–Burk plot OK?

**You can use it to display the data, but don't use it to estimate Vmax and Km.**

On your data it happens to give nearly the same answer (Vmax = 9.95 µM/min, Km = 1.01 mM). That's only because your data have very little noise. In general it's a poor estimator:

1. **It distorts the errors.** Taking 1/v turns a small error on a slow rate into a large error. Your v = 0.9 point ends up at 1/v ≈ 1.1, far out on the plot, where it pulls on the fitted line much more than the near-saturating points. The fitted slope and intercept, and so Km and Vmax, become biased and imprecise.
2. **It breaks the least-squares assumptions.** Ordinary regression assumes equal variance in the y-values. If the errors in v are roughly constant, the errors in 1/v grow as 1/v², so they are far from equal.
3. **Vmax comes from a reciprocal intercept.** Vmax = 1/intercept, and the intercept is usually small and uncertain, so the uncertainty grows when you invert it.

It's still fine to use a Lineweaver–Burk plot to show inhibition patterns visually: where the lines cross for competitive, uncompetitive or mixed inhibition. Get the numbers themselves from the nonlinear fit.

## What to report

"Vmax = 10.06 ± 0.11 µM/min, Km = 1.01 ± 0.03 mM (nonlinear least squares, n = 7, S = 0.1–8 mM)."

These numbers rely on some assumptions:
- The rates are true initial rates, measured before product builds up.
- The enzyme concentration is much lower than Km (≈1 mM), which is almost certainly true.

If you know the enzyme concentration, kcat = Vmax/[E]ₜ. If you have replicates, fitting them separately or with weights would give more realistic uncertainties than this single series does.
````

## Answer without the skill (excerpt)

````text
## Nonlinear least-squares fit of v = Vmax·S / (Km + S)

| Parameter | Estimate | Std. error |
|---|---|---|
| **Vmax** | **10.06 µM/min** | ± 0.11 |
| **Km** | **1.01 mM** | ± 0.03 |

- Residual SD is 0.09 µM/min and R² = 0.9993.
- The residuals (−0.00, −0.09, +0.08, −0.10, +0.13, −0.02, −0.03) switch sign with no trend, so the Michaelis-Menten model fits these data well.
- Your highest substrate level, 8 mM, is about 8×Km. That reaches about 89% of Vmax, which is enough to pin Vmax down well.

## Is a Lineweaver-Burk fit OK?

Use it to show the data in a figure, but don't use it to estimate Km and Vmax.

On your data, a linear regression of 1/v against 1/S gives Vmax = 9.95 and Km = 1.01. That's close to the nonlinear fit because your data have very little noise. With typical experimental noise it usually goes wrong, for these reasons:

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
