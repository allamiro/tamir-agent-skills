---
name: model-building-design
description: Designs a mathematical model of a biological system before any equation is solved, covering the modelling cycle from reality to model and back, explicit assumptions, variables versus parameters versus coefficients, model classification, scope and resolution, dimension analysis, poorly posed problems and how a model will be tested. Use for "what assumptions does my model make", "is this a variable or a parameter", "classify my model", "how detailed should my model be", "my model has too many parameters", "write the model description section", "is this problem well posed". Use systems-biology-workflow to choose the formalism, quantities-units-balances for units and balances, and model-review to audit a finished model.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# Model building and design

## Purpose and activation

A model is a deliberate simplification made for a purpose, and its value depends on whether the
simplifications fit that purpose. This skill makes the purpose, assumptions and structure explicit before
the mathematics, so that a reader can tell which conclusions follow from biology and which from the
modeller's choices. Activate when a model is being planned, when its assumptions are being written down,
or when a model has grown faster than the data that could constrain it.

## Required inputs

The purpose of the model (explain, predict, design, integrate data, teach); the system and its boundary;
the known mechanism and how certain it is; the data and its resolution in time, space and number of
molecules; and the formalism, if chosen (`systems-biology-workflow`).

## Workflow

1. **Walk the modelling cycle.** Real situation, simplified situation, mathematical model, mathematical
   result, interpretation in the real situation, and validation against it; then go round again. The
   cycle in `references/modelling-cycle.md` names what can go wrong at each step.
2. **List the assumptions** in `assets/templates/assumption-register.md`: each with why it is acceptable
   for this purpose, how it could fail, and how you would notice. Typical ones: well mixed, constant volume,
   constant temperature, quasi-steady state for fast species, mass action, no spatial structure.
3. **Classify the quantities.** A state variable changes with time as the model runs; a parameter is
   fixed for one run but may be varied between runs; a coefficient is a number in an equation (for example
   a stoichiometric coefficient) that follows from structure. An input is set from outside; an output is
   what you compare with data.
4. **Classify the model** along the axes in the decision table, and say what each choice excludes.
5. **Check dimensions** of every term with `quantities-units-balances`; a sum of terms with different units
   is an error, not a modelling choice.
6. **Ask whether the problem is well posed:** does a solution exist, is it unique, and does it depend
   continuously on the data? Inverse problems (inferring parameters or networks from data) often fail the
   second or third test; say how you will regularise or constrain them.
7. **Count unknowns against information.** If parameters outnumber independent observations, reduce the
   model (lump, fix from literature, use quasi-steady state) or plan the experiment that supplies the data.
8. **Plan the test:** which prediction, on which data not used to build the model, would show it wrong.

## Decision framework

| Axis | Options | Choose by |
|---|---|---|
| Purpose | Explanatory, predictive, design | What the result will be used for |
| Mechanism | Mechanistic, phenomenological, statistical | Whether parameters must mean something physical |
| Time | Static (steady state), dynamic | Whether transients matter |
| Time representation | Continuous, discrete | Measurement interval, generations, events |
| State values | Continuous, discrete (counts, Boolean) | Copy numbers, available data |
| Chance | Deterministic, stochastic | Copy numbers; whether variation is the question |
| Space | Lumped (ODE), distributed (PDE, agent-based) | Gradients, diffusion, tissue structure |
| Linearity | Linear, nonlinear | Saturation, cooperativity, feedback |

| Sign | Response |
|---|---|
| A parameter that never affects any output | Remove it or fix it; say so |
| Two parameters that only appear as a product or ratio | Reparameterise to the identifiable combination |
| Results that change with an arbitrary choice (step size, boundary) | Report the dependence or fix the method |

## Failure and edge cases

- **Assumptions implicit in the equations** but not stated in the text.
- **Quasi-steady state applied where time scales are not separated.**
- **Mass action used for enzyme-catalysed steps** without saying why the enzyme is not saturated.
- **A parameter treated as a constant that the experiment changes** (temperature, cell volume, enzyme level).
- **Too fine a resolution for the data,** giving a model that can fit anything and predict nothing.
- **Validation against the data used to build the model.**
- **Model reduction that removes the mechanism the question is about.**

## Validation

- Every assumption has a stated failure mode and a check.
- Every quantity is classified as variable, parameter, coefficient, input or output, with a unit.
- Every equation is dimensionally consistent.
- A prediction for new data is written down before the comparison.
- Falsifier: an assumption whose failure would reverse the main conclusion, and evidence that it holds.

## Expected output

The purpose; the modelling cycle applied to this system; the assumption register; the classified
quantities with units; the model classification and what it excludes; the well-posedness check; and the
planned test.

## Sources and confidence

- Sauter and Albrecht 2023, doi:10.11647/OBP.0291, learning checklist Part 4 (supplied text): reality and
  model, the modelling cycle of Blum and Leiß, assumptions, model building, distinguishing variable,
  parameter and coefficient, dimension analysis, poorly posed problems, sensitivity analysis and model
  classification are listed topics; the chapter text was not seen, so the treatment here is author
  knowledge: VERIFY against the chapter
- Well-posedness (existence, uniqueness, continuous dependence) is Hadamard's classical definition, from
  author knowledge, VERIFY
- Identifiability as a design concern: Raue et al. 2009, doi:10.1093/bioinformatics/btp358 (record checked
  on Crossref 2026-10-15)
