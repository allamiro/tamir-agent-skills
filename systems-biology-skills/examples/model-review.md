# `model-review`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Review this model as a referee: an ODE model of a metabolic pathway, 30 parameters, fitted to one time course, claims to explain why a mutant accumulates an intermediate. Parameters are in a table without units. No model file is provided.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 2,500 | 3,392 |
| Input tokens read across all turns (including cached context) | 30,389 | 74,584 |
| Extra input tokens when the skill is installed | | +44,195 |
| Cost, US dollars at list price | 0.110 | 0.197 |
| Skills invoked in the sample run | none | `model-review` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 290 tokens for its name and description, which are in every session where the skill is installed, and about 1,600 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
# Referee report: ODE model of a metabolic pathway explaining intermediate accumulation in a mutant

**Scope.** I reviewed the paper as you described it: a 30-parameter ODE model, fitted to one time course, a parameter table without units, and no model file. I couldn't recompute anything or rebuild the model, because no equations, values or files were provided. That gap is itself a major finding (M4). The points below are what I'd raise with the authors, and what I'd check once they send the material.

## Summary of the claim

The authors say their pathway model explains why a mutant builds up an intermediate. This only becomes a mechanistic claim if the model (a) predicts the build-up from a stated change, such as lower activity of the downstream enzyme, that was not tuned to the mutant data, and (b) does better than other plausible explanations. As described, the manuscript shows neither.

## Major issues

**M1. 30 parameters from one time course are almost certainly unidentifiable.**
- **Problem:** A single time course, even with several species at 10–20 time points, cannot constrain 30 parameters. Many combinations, such as Vmax/Km ratios and production and consumption rates that trade off against each other, will fit equally well.
- **Why it matters:** If the parameters that control the intermediate are among the unidentifiable ones, the mechanism is not supported. The data would fit equally well with very different values.
- **What would resolve it:**
  - Report the number of data points against the number of parameters, and run a structural identifiability check (e.g. DAISY, StructuralIdentifiability.jl, or a GenSSI-type analysis).
  - Report profile likelihoods for every fitted parameter, or at least for those the claim depends on.
  - Fix parameters that have literature values (BRENDA, SABIO-RK, with sources) and fit only the rest.
  - Report confidence intervals, not point estimates.

**M2. The fit is presented as an explanation, with no independent test.**
- **Problem:** The manuscript doesn't say whether the one time course is wild type, mutant, or both. Each case has a problem:
  - **Mutant only:** a 30-parameter model fitted to the accumulation describes it but doesn't explain it.
  - **Wild type only, then the mutant simulated:** this is the right design, but the authors must state which parameters changed for the mutant, justify the change from the genetics (e.g. the gene encodes enzyme E_k, so set Vmax,k to 0 or to its measured residual activity), and show that nothing else was re-tuned.
  - **Both together:** the authors must show which parameters were shared and which were allowed to differ.
- **What would resolve it:** A prediction of data not used for fitting. Options include a second mutant, a titrated allele or inducible knockdown of the suspected enzyme, a different substrate pulse, or measured fluxes. The model should predict these before the measurement is made.

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
# Referee Report

**Manuscript:** ODE model of a metabolic pathway explaining intermediate accumulation in a mutant
**Recommendation:** Major revision. In its current form the central claim isn't supported.

I've only seen your summary, not the manuscript. I've written the concerns so they apply generally; please match them to the specific sections.

---

## Summary of the submission

The authors build an ODE model of a metabolic pathway with about 30 parameters and fit it to a single time course. They argue that the model explains why a mutant accumulates a pathway intermediate. The parameters are reported in a table with no units, and the model is not provided in any executable form.

The question is reasonable, and a mechanistic account of the mutant's accumulation would be useful. But the evidence doesn't yet separate "the model can reproduce the data" from "the model explains the phenotype."

---

## Major concerns

### 1. The parameters can't be identified from one time course

Thirty parameters fitted to one time course is almost certainly underdetermined. Even when each species is sampled densely, one trajectory usually constrains only a few combinations of parameters, not each parameter on its own.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
