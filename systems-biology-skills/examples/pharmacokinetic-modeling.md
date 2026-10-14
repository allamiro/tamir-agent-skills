# `pharmacokinetic-modeling`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> What is the half-life of a drug given as a 100 mg IV bolus with volume of distribution 20 L and clearance 5 L/h? Give the concentration at 2 h and the AUC.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 487 | 505 |
| Input tokens read across all turns (including cached context) | 30,377 | 36,385 |
| Extra input tokens when the skill is installed | | +6,008 |
| Cost, US dollars at list price | 0.069 | 0.118 |
| Skills invoked in the sample run | none | none |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 280 tokens for its name and description, which are in every session where the skill is installed, and about 1,600 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
For a one-compartment model with first-order elimination, the drug has a **half-life of about 2.8 h**, a **concentration at 2 h of about 3.0 mg/L**, and an **AUC of 20 mg·h/L**.

**Elimination rate constant**
k = CL / V = 5 L/h ÷ 20 L = **0.25 h⁻¹**

**Half-life**
t½ = ln 2 / k = 0.693 / 0.25 ≈ **2.77 h**

**Concentration at 2 h**
- Initial concentration: C₀ = Dose / V = 100 mg ÷ 20 L = 5 mg/L
- C(2 h) = C₀ · e^(−k·t) = 5 · e^(−0.25 × 2) = 5 · e^(−0.5) = 5 × 0.607 ≈ **3.03 mg/L**

**AUC (from 0 to infinity)**
AUC = Dose / CL = 100 mg ÷ 5 L/h = **20 mg·h/L**

As a check, C₀ / k = 5 ÷ 0.25 also gives 20 mg·h/L.
````

## Answer without the skill (excerpt)

````text
This assumes a one-compartment model with first-order elimination.

**Elimination rate constant**
k = CL / V = 5 L/h ÷ 20 L = **0.25 h⁻¹**

**Half-life: about 2.8 h**
t½ = ln 2 / k = 0.693 / 0.25 = **2.77 h**

**Concentration at 2 h: about 3.0 mg/L**
- Starting concentration: C₀ = Dose / V = 100 mg ÷ 20 L = 5 mg/L
- C(2 h) = C₀ · e^(−k·t) = 5 · e^(−0.25 × 2) = 5 × 0.6065 = **3.03 mg/L**

**AUC (time 0 to infinity): 20 mg·h/L**
AUC = Dose / CL = 100 mg ÷ 5 L/h = **20 mg·h/L**

As a check, C₀ / k = 5 ÷ 0.25 = 20 mg·h/L, which gives the same AUC.
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
