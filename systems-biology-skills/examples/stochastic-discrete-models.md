# `stochastic-discrete-models`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Simulate this at low copy number with the Gillespie algorithm: production of A at 10 molecules per unit time, degradation at 0.5 per molecule per unit time, starting from zero. What are the mean and variance at t = 50, and how do they compare with the ODE?

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 2,856 | 2,714 |
| Input tokens read across all turns (including cached context) | 158,809 | 223,248 |
| Extra input tokens when the skill is installed | | +64,438 |
| Cost, US dollars at list price | 0.165 | 0.238 |
| Skills invoked in the sample run | none | `stochastic-discrete-models` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 290 tokens for its name and description, which are in every session where the skill is installed, and about 1,700 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
I ran the simulation with Gillespie's direct method (reactions ∅ → A at 10 per unit time and A → ∅ at 0.5·A, starting from A = 0). At t = 50 the stochastic mean is the same as the ODE answer of 20. The ODE gives a single number and no spread, but the simulation shows a cell-to-cell standard deviation of about 4.5 molecules.

| Runs (seed) | Mean A(50) | SD | Variance | Fano (var/mean) | Range |
|---|---|---|---|---|---|
| 2000 (seed 1) | 20.05 | 4.43 | 19.6 | 0.98 | 7–34 |
| 4000 (seed 2) | 20.06 | 4.46 | 19.9 | 0.99 | 6–37 |

The simulator's built-in self-test passed (21 checks), and the results barely change when the number of runs is doubled.

**How this compares with the ODE:**
- **ODE:** dA/dt = 10 − 0.5A gives A(t) = 20(1 − e^(−0.5t)). By t = 50 that is 20(1 − e^(−25)), which is 20 to within about 10⁻¹⁰. The system reaches steady state after about 5/0.5 = 10 time units.
- **Exact theory:** for a birth–death process that starts at zero, the number of molecules at time t follows a Poisson distribution with mean = variance = 20(1 − e^(−0.5t)). At t = 50 the mean and the variance should both be 20.
- **Mean:** 20.06 ± 0.07 (standard error from 4000 runs), so it matches the ODE within sampling error. That is expected because the reactions are linear: the equation for the mean is exactly the ODE.
- **Variance:** 19.9 ± about 0.45 (standard error), which agrees with the Poisson value of 20. The Fano factor of about 1 is what this kind of noise, produced only by the reactions themselves, looks like.
- **What the ODE misses:** the noise relative to the mean (coefficient of variation) is 1/√20, about 22%. Single cells ranged from 6 to 37 molecules, even though the ODE says every cell has exactly 20.

The mean agrees here only because both reactions are linear. With nonlinear reactions such as dimerisation or cooperative feedback, the stochastic mean can drift away from the ODE at low copy numbers. A Fano factor well above 1 in real data would point to bursty production or noise from outside the reaction (for example, variation in shared factors between cells), which this model doesn't include.

The reaction file is `scratchpad/bd.txt`, and I used seeds 1 and 2 so the runs can be repeated.
````

## Answer without the skill (excerpt)

````text
At t = 50 the simulated mean is **20.01** and the variance is **20.18**. The ODE gives exactly 20, so the mean matches it. The variance is also about 20, which tells you the copy number is Poisson-distributed.

**Setup:** the reactions are ∅ → A at rate k = 10 and A → ∅ at rate γ·n with γ = 0.5, starting from n = 0. I ran 20,000 independent Gillespie (direct method) trajectories to t = 50 with seed 1. The script is in the scratchpad as `gill.py`.

| | Gillespie (20k runs) | ODE / exact theory |
|---|---|---|
| Mean ⟨n(50)⟩ | **20.01** ± 0.03 (SE) | 20.000 |
| Variance | **20.18** ± ~0.20 | 20.000 |
| Fano factor (variance / mean) | **1.009** | 1 |

**How it compares with the ODE:**
- **Mean:** the ODE dx/dt = k − γx gives x(t) = (k/γ)(1 − e^(−γt)) = 20(1 − e^(−25)) ≈ 20.000. Because both reactions are linear (zeroth- and first-order), the mean of the stochastic process follows the ODE exactly at every time, not just roughly. The simulated 20.01 is within one standard error of 20.
- **Variance:** the ODE gives a single deterministic number, so it has no variance. For this process the exact distribution at any t is Poisson, with variance equal to the mean, (k/γ)(1 − e^(−γt)). By t = 50 (25 relaxation times) the system has reached its steady state, Poisson(20). The simulated variance of 20.18 is within one standard error of 20, and the Fano factor is about 1.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
