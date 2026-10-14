# `quantitative-research-methods`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Compute Cronbach's alpha for my 4-item quiz on steady-state concepts (items scored 0 or 1): i1,i2,i3,i4 rows 1,1,0,1; 1,0,0,0; 1,1,1,1; 0,0,0,0; 1,1,1,0; 1,0,1,1; 0,1,0,0; 1,1,1,1. Is the quiz measuring understanding of steady state?

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 2,485 | 3,028 |
| Input tokens read across all turns (including cached context) | 30,460 | 36,464 |
| Extra input tokens when the skill is installed | | +6,004 |
| Cost, US dollars at list price | 0.110 | 0.169 |
| Skills invoked in the sample run | none | none |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 340 tokens for its name and description, which are in every session where the skill is installed, and about 3,300 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
# Cronbach's alpha for your 4-item steady-state quiz

**α ≈ 0.71.** Because the items are scored 0/1, this is the same as KR-20.

## Calculation

| | i1 | i2 | i3 | i4 | Total |
|---|---|---|---|---|---|
| Proportion correct (p) | 0.750 | 0.625 | 0.500 | 0.500 | mean 2.375 |
| Variance p(1−p) | 0.1875 | 0.2344 | 0.2500 | 0.2500 | **Σ = 0.9219** |

- The total scores are 3, 1, 4, 0, 3, 3, 1, 4, and their variance is **1.9844**.
- α = k/(k−1) · (1 − Σσ²ᵢ / σ²ₜ) = 4/3 · (1 − 0.9219/1.9844) = 4/3 · 0.5354 = **0.714**

## Item diagnostics

| Item | Corrected item–total r | α if item deleted |
|---|---|---|
| i1 | 0.59 | 0.61 |
| **i2** | **0.27** | **0.78** |
| i3 | 0.59 | 0.59 |
| i4 | 0.59 | 0.59 |

i2 doesn't fit the other items. Respondent 7 got only i2 right, and respondent 6 got everything except i2 right. Dropping i2 would raise α to 0.78. Before you drop it, read its wording. It may be guessable, ambiguous, or testing something other than steady state.

## Is the quiz measuring understanding of steady state?

Alpha alone can't answer that.

1. **Alpha measures consistency, not meaning.** It shows the items rank students in a similar order. It doesn't show what they rank them on. Four items that all reward reading skill or algebra could reach the same α.
2. **Eight students is too few to trust the value.** A rough 95% confidence interval (Feldt) runs from about **0.2 to 0.9**. The true reliability could be poor or good. You'd need roughly 30 or more respondents for a stable estimate.
3. **Alpha assumes one underlying construct** and items that contribute about equally. With 4 items and n = 8, you can't test either assumption, and i2 already suggests they may not hold.

## What would show the quiz measures steady state

- **Content:** Check each item against a short map of steady-state ideas: inflow equals outflow, steady state vs. equilibrium, setting dx/dt = 0, and stability. Make sure each item needs one of those ideas to answer it.
- **Response processes:** Ask 3–5 students to think aloud while answering. Check whether right answers come from right reasoning and wrong answers from known misconceptions, such as confusing steady state with equilibrium.
- **Relations with other measures:** Scores should correlate with other evidence of understanding, such as an exam question or a modelling task. They should correlate less with unrelated skills.
- **Structure:** With a larger sample, fit a Rasch model or a one-factor model to check that the items behave as one scale.

**Bottom line:** α ≈ 0.71 is acceptable for a short classroom quiz. Revise or replace i2. Don't claim the quiz measures understanding of steady state until you have at least the content and think-aloud evidence.
````

## Answer without the skill (excerpt)

````text
# Cronbach's alpha for the 4-item steady-state quiz

**α ≈ 0.71.** Because the items are scored 0/1, this is the same number as KR-20.

## Calculation

| | i1 | i2 | i3 | i4 | Total |
|---|---|---|---|---|---|
| Proportion correct (p) | .750 | .625 | .500 | .500 | mean = 2.375 |
| Item variance (n−1) | .214 | .268 | .286 | .286 | Σ = 1.054 |

- Student totals: 3, 1, 4, 0, 3, 3, 1, 4. Their variance (n−1) is 15.875 / 7 = **2.268**.
- α = (k/(k−1)) · (1 − Σσ²ᵢ / σ²ₜ) = (4/3) · (1 − 1.054/2.268) = (4/3)(0.535) ≈ **0.714**

## Item diagnostics

| Item | Corrected item–total r | α if item deleted |
|---|---|---|
| i1 | .59 | — |
| i2 | **.27** | **.78** |
| i3 | .59 | — |
| i4 | .59 | — |

Item i2 fits the rest of the quiz least well. Removing it raises alpha to about 0.78. Look at its wording: it may be testing something other than steady state, such as reading a graph or a vocabulary term. It's also the only item missed by a student whose total was high (student 6).

## Is the quiz measuring understanding of steady state?

Alpha can't tell you that. Alpha measures **reliability**, meaning how consistently the items rank students the same way. It does not measure **validity**, meaning whether the quiz measures the concept you intend. Four items could hang together well because they all test algebra skill, test-taking skill, or one memorized fact.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
