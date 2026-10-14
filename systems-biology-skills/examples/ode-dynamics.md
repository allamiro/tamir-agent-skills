# `ode-dynamics`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Find the steady state of dS/dt = v0 - Vmax*S/(Km+S) with v0 = 1, Vmax = 2, Km = 0.5, classify its stability, and say which parameters the steady state is most sensitive to.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 1,163 | 1,252 |
| Input tokens read across all turns (including cached context) | 30,388 | 36,398 |
| Extra input tokens when the skill is installed | | +6,010 |
| Cost, US dollars at list price | 0.083 | 0.133 |
| Skills invoked in the sample run | none | none |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 320 tokens for its name and description, which are in every session where the skill is installed, and about 1,800 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
# Steady state, stability and sensitivity of dS/dt = v0 − Vmax·S/(Km + S)

**Steady state: S\* = 0.5.** It is stable, with eigenvalue −1. S\* is most sensitive to v0 and Vmax: a 1% change in either moves S\* by about 2%, against 1% for Km.

## 1. Steady state

At steady state, supply equals consumption:

v0 = Vmax·S/(Km + S) ⇒ **S\* = Km·v0 / (Vmax − v0)**

S\* = 0.5 · 1 / (2 − 1) = **0.5**

A positive steady state exists only if v0 < Vmax. If supply is at or above the enzyme's maximum rate, S grows without bound.

## 2. Stability

Linearise the right-hand side f(S) around S\*:

f′(S) = −Vmax·Km / (Km + S)²

f′(0.5) = −2·0.5 / (1.0)² = **−1**

- The single eigenvalue is λ = −1, which is negative and real. That makes S\* a **stable node**: after a small disturbance, S returns to 0.5 without oscillating.
- The relaxation time is τ = 1/|λ| = 1 time unit.
- The steady state is also globally stable for S ≥ 0. Consumption increases monotonically with S, so f > 0 below S\* and f < 0 above it, and every trajectory moves toward 0.5.

## 3. Sensitivity (normalised local coefficients, ∂ln S\*/∂ln p)

| Parameter | General formula | Value |
|---|---|---|
| v0 | Vmax / (Vmax − v0) | **+2** |
| Vmax | −Vmax / (Vmax − v0) | **−2** |
| Km | 1 | **+1** |

**Interpretation:**
- **v0 and Vmax matter most, and equally.** A 1% increase in supply raises S\* by about 2%. A 1% increase in Vmax lowers it by about 2%.
- **Km has unit sensitivity.** S\* is directly proportional to Km.
- **The v0 and Vmax effects cancel when both change together.** S\* depends only on the ratio v0/Vmax, so scaling both by the same factor leaves it unchanged.
- **The sensitivities grow as the enzyme saturates.** Here v0/Vmax = 0.5, so the factor is 2. As v0 approaches Vmax, the factor Vmax/(Vmax − v0) diverges. A pathway running close to its enzyme's capacity therefore has a fragile substrate level, and recovery also slows because |λ| shrinks.
````

## Answer without the skill (excerpt)

````text
## Steady state

Set dS/dt = 0:

v0 = Vmax·S/(Km + S)  →  **S\* = Km·v0 / (Vmax − v0) = 0.5·1 / (2 − 1) = 0.5**

A positive steady state exists only when v0 < Vmax. If v0 ≥ Vmax, S grows without bound.

## Stability

Linearize f(S) = v0 − Vmax·S/(Km + S):

f′(S) = −Vmax·Km / (Km + S)²

At S\* = 0.5: f′ = −2·0.5 / (1.0)² = **−1**

The eigenvalue is λ = −1 < 0, so the steady state is **stable**: a perturbation decays as e^(−t), with a relaxation time of 1 time unit. Since f′ < 0 for every S ≥ 0, f is strictly decreasing. That makes S\* the unique steady state and **globally stable** for S ≥ 0.

## Sensitivity

To compare the parameters fairly, use normalized sensitivities, which give the percent change in S\* per percent change in a parameter: ∂ln S\*/∂ln p. Here ln S\* = ln Km + ln v0 − ln(Vmax − v0).

| Parameter | Normalized sensitivity | Value at this point |
|---|---|---|
| v0 | 1 + v0/(Vmax − v0) = Vmax/(Vmax − v0) | **+2** |
| Vmax | −Vmax/(Vmax − v0) | **−2** |
| Km | 1 | **+1** |

**S\* is most sensitive to v0 and Vmax**, with sensitivities of equal size and opposite sign. A 1% increase in v0 raises S\* by about 2%, and a 1% increase in Vmax lowers it by about 2%. Km has a 1:1 effect.

The v0 and Vmax sensitivities sum to zero. This means scaling v0 and Vmax by the same factor leaves S\* unchanged, so what controls S\* is the ratio v0/Vmax. Both sensitivities go to infinity as v0 approaches Vmax, when the enzyme nears saturation. At the current ratio v0/Vmax = 0.5, the system is moderately close to that sensitive region.
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
