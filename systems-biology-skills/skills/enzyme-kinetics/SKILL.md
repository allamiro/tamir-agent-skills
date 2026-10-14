---
name: enzyme-kinetics
description: Derives, chooses and fits enzyme rate laws, covering the law of mass action, reaction rates, Michaelis-Menten kinetics and its assumptions, reversible Michaelis-Menten, competitive, uncompetitive and mixed inhibition, substrate inhibition, cooperative enzymes and Hill kinetics, the Lineweaver-Burk plot and why not to fit with it, and nonlinear least-squares estimation of Vmax and Km. Use for "fit Michaelis-Menten to my data", "which inhibition type is this", "derive the rate law", "what does a Hill coefficient of 2 mean", "is Lineweaver-Burk fitting OK", "rate law for a reversible reaction", "my enzyme shows inhibition at high substrate". Use ode-dynamics to put the rate law in a model, parameter-estimation-model-selection to compare rate laws, and pharmacokinetic-modeling for drug concentration over time.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# Enzyme kinetics

## Purpose and activation

Rate laws turn a reaction network into a dynamic model. Choosing one is a modelling decision with
assumptions (quasi-steady state of the enzyme–substrate complex, enzyme much scarcer than substrate,
initial rates without product), and estimating its parameters is a statistical problem in which the
classical linearisations perform badly. Activate when the user chooses, derives or fits a rate law, or
interprets inhibition or cooperativity.

## Required inputs

The reaction and mechanism, as far as known; the data (substrate concentrations and initial rates,
replicates, inhibitor concentrations) with units; the enzyme concentration if known; and the conditions
(pH, temperature).

## Workflow

1. **Start from mass action:** an elementary step's rate is a rate constant times the product of reactant
   concentrations raised to their stoichiometric coefficients.
2. **Derive or choose the rate law** (`references/rate-laws.md`). State the assumptions: Michaelis–Menten
   needs the enzyme–substrate complex at quasi-steady state and total enzyme much lower than substrate.
3. **Compute rates** at given conditions with `python3 scripts/kinetics.py rate LAW --S VALUE ...` to see shapes and
   check units.
4. **Fit by nonlinear least squares** with `python3 scripts/kinetics.py fit DATA.csv [--model mm|hill]`, which uses
   Levenberg–Marquardt on the untransformed rates and prints the Lineweaver–Burk estimate beside it for
   comparison only.
5. **Diagnose inhibition** from fits at several inhibitor levels: competitive raises apparent Km only;
   uncompetitive lowers apparent Vmax and Km by the same factor; mixed changes both differently. Use a
   Lineweaver–Burk plot to show the pattern, not to estimate.
6. **Compare rate laws** (Michaelis–Menten against Hill or substrate inhibition) with AICc in
   `parameter-estimation-model-selection`, not by eye.
7. **Report** parameters with units, standard errors or intervals, the substrate range covered (Km should lie
   inside it), and the assumptions.

## Decision framework

| Data pattern | Rate law |
|---|---|
| Hyperbolic saturation | Michaelis–Menten |
| Sigmoidal | Hill (cooperative), or a mechanistic model such as MWC: VERIFY which the data support |
| Rate falls at high substrate | Substrate inhibition |
| Product present, reaction near equilibrium | Reversible Michaelis–Menten (Haldane relation links the constants to Keq) |
| Inhibitor raises apparent Km, Vmax unchanged | Competitive |
| Apparent Km and Vmax fall in proportion | Uncompetitive |
| Both change, not in proportion | Mixed (non-competitive is the special case Ki = Kii) |

## Failure and edge cases

- **Fitting the double reciprocal plot:** 1/v magnifies the noise of the lowest rates, biasing Km and Vmax.
- **Substrate range below Km only:** Vmax is extrapolated and unreliable.
- **A Hill coefficient read as the number of binding sites;** it is a lower bound on cooperativity, not a count.
- **Enzyme not scarce** (total enzyme comparable to Km): use the full quadratic (tight-binding) form.
- **Initial rates measured after product accumulates.**
- **Units of Vmax** (concentration per time) confused with kcat (per time, Vmax divided by enzyme concentration).

## Validation

- `python3 scripts/kinetics.py --selftest` passes.
- Residuals of the fit show no trend with substrate concentration.
- The fitted Km lies within the measured substrate range.
- Parameters agree within their uncertainty across replicate experiments.
- Falsifier: rates at a new substrate concentration outside the fitted curve's prediction interval.

## Expected output

The mechanism and assumptions; the rate law; fitted parameters with units and uncertainty; the comparison
with the Lineweaver–Burk estimate and why the nonlinear fit is preferred; inhibition type with evidence;
and the substrate range.

## Sources and confidence

- Sauter and Albrecht 2023, doi:10.11647/OBP.0291, learning checklist Part 4 (supplied text): law of mass
  action, reaction rate, Michaelis–Menten, Lineweaver–Burk plot, reversible Michaelis–Menten, inhibition,
  substrate inhibition, cooperative enzymes and Hill kinetics are listed topics. Chapter text not seen
- Lineweaver and Burk 1934, doi:10.1021/ja01318a036; Johnson and Goody 2011, doi:10.1021/bi201284u (translation
  of the 1913 Michaelis–Menten paper). Records checked on Crossref 2026-10-15; content from author knowledge, VERIFY
