# `systems-biology-programming`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Check my reactions are balanced. Reactions: R1: glc + 6 o2 -> 6 co2 + 6 h2o; R2: pyr + nadh -> lac + nad; EX_glc: glc ->. Formulas and charges: glc C6H12O6 0, o2 O2 0, co2 CO2 0, h2o H2O 0, pyr C3H3O3 -1, lac C3H5O3 -1, nadh C21H27N7O14P2 -2, nad C21H26N7O14P2 -1.

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 811 | 1,010 |
| Input tokens read across all turns (including cached context) | 30,492 | 36,499 |
| Extra input tokens when the skill is installed | | +6,007 |
| Cost, US dollars at list price | 0.077 | 0.129 |
| Skills invoked in the sample run | none | none |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 290 tokens for its name and description, which are in every session where the skill is installed, and about 1,700 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
**Two of the three reactions need nothing; R2 is missing one proton.**

| Reaction | C | H | N | O | P | Charge | Verdict |
|---|---|---|---|---|---|---|---|
| R1 | 6 → 6 | 12 → 12 | – | 18 → 18 | – | 0 → 0 | Balanced |
| R2 | 24 → 24 | **30 → 31** | 7 → 7 | 17 → 17 | 2 → 2 | **−3 → −2** | **Unbalanced** |
| EX_glc | – | – | – | – | – | – | Boundary reaction, not checked |

**R2 (lactate dehydrogenase):**
- Left side: pyr (C3H3O3, −1) + nadh (C21H27N7O14P2, −2) = C24H30N7O17P2, charge −3
- Right side: lac (C3H5O3, −1) + nad (C21H26N7O14P2, −1) = C24H31N7O17P2, charge −2

The right side has one extra H and one extra positive charge. That is exactly one H⁺, so the fix is:

```
R2: pyr + nadh + h -> lac + nad      (h: formula H, charge +1)
```

This is the standard form, `pyr + nadh + h ⇌ lac + nad`. You'll need to add an `h` metabolite to the model. If the model has compartments, use the proton from the same compartment, e.g. `h_c`.

**EX_glc** is an exchange (boundary) reaction. It is supposed to be unbalanced, because it moves glucose across the system boundary. Leave it out of mass-balance checks; COBRApy's `model.boundary` and MEMOTE skip these too. As written (`glc ->`), a positive flux means glucose leaving the system. For uptake, give it a negative lower bound, e.g. `lower_bound = -10`.

If you're using COBRApy, `reaction.check_mass_balance()` returns `{}` for a balanced reaction. For the current R2 it returns `{'H': 1.0, 'charge': 1.0}`.
````

## Answer without the skill (excerpt)

````text
**R1 and EX_glc are fine. R2 is missing a proton.**

| Reaction | Elements (left → right) | Charge | Status |
|---|---|---|---|
| **R1** glc + 6 o2 → 6 co2 + 6 h2o | C6 H12 O18 → C6 H12 O18 | 0 → 0 | ✅ Balanced |
| **R2** pyr + nadh → lac + nad | C24 H30 N7 O17 P2 → C24 **H31** N7 O17 P2 | **−3 → −2** | ❌ Off by 1 H and +1 charge |
| **EX_glc** glc → | — | — | ⚪ Exchange reaction, unbalanced on purpose |

**R2 calculation:**
- Left side: C3H3O3 (−1) + C21H27N7O14P2 (−2) = C24H30N7O17P2, charge −3
- Right side: C3H5O3 (−1) + C21H26N7O14P2 (−1) = C24H31N7O17P2, charge −2
- The products have one more H and one more positive charge than the substrates. That is exactly one proton.

**Fix:** add H⁺ to the substrate side:

```
R2: pyr + nadh + h -> lac + nad
```

with `h` defined as `H`, charge `+1`. This is the standard stoichiometry for lactate dehydrogenase (pyruvate + NADH + H⁺ → lactate + NAD⁺).

EX_glc is a boundary (exchange) reaction. Imbalance is expected there, so leave it out of any mass-balance checks. For example, COBRApy's `check_mass_balance()` returns imbalances for exchange reactions, so filter them out using `model.boundary`.
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
