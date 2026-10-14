---
name: systems-biology-workflow
description: Coordinates a systems biology project from question to paper, choosing the modelling formalism (network graph, stoichiometric or constraint-based, ODE, stochastic, Boolean, pharmacokinetic, statistical) and routing each step to the right skill in this collection. Use for "I want to model this pathway", "which kind of model do I need", "plan my systems biology project", "where do I start with this network", "how do these modelling steps fit together", "review my whole modelling plan". Use model-building-design for the assumptions and scope of one model, modeling-research-planning for a proposal, and systems-biology-learning-path to learn the material rather than apply it.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# Systems biology workflow

## Purpose and activation

Systems biology asks how the behaviour of a whole network (steady state, dynamics, control, robustness)
follows from its parts. The commonest mistake is choosing the formalism before stating the question,
which yields an ODE model with forty unidentifiable parameters where a stoichiometric analysis would have
answered the question. This skill states the question first, picks the lightest formalism that can answer
it, and hands each step to the right skill. Activate at the start of a project, when the user is unsure
which model to build, or when several steps need to be put in order.

## Required inputs

The biological question and what decision or claim the answer feeds; the system boundary (which molecules,
cells, compartments or patients); the data available (topology only, fluxes, time courses, concentrations,
single-cell counts, omics tables, clinical measurements) and their units; the time scale of interest; and
the output the user needs (a figure, a prediction, a design, a paper, a lesson).

## Workflow

1. **State the question as an observable.** "Does the knockout lower lactate secretion at steady state?" is
   answerable; "understand glycolysis" is not. Name the quantity, the condition and the comparison.
2. **Draw the system boundary and the network** (species, reactions or interactions, inputs and outputs) and
   check units and balances with `quantities-units-balances`.
3. **Choose the formalism** with the decision table below; prefer the one with the fewest unknown parameters
   that still answers the question.
4. **Write the assumptions and the scope** with `model-building-design` before any equation.
5. **Build and analyse** with the formalism's skill (table below), keeping the model file under version control.
6. **Fit and compare models** to data with `parameter-estimation-model-selection`; ask whether the parameters
   can be identified at all before trusting their values.
7. **Test against data not used for fitting,** then check robustness with sensitivity analysis (`ode-dynamics`).
8. **Review** the whole chain with `model-review`, and encode it in a standard format with `systems-biology-programming`.
9. **Write it up** with `modeling-paper-writing`.

Record each step in `assets/templates/project-log.md`.

## Decision framework

| Question and data | Formalism | Skill |
|---|---|---|
| Who interacts with whom; hubs, modules, disease genes | Graph | `network-analysis` |
| Matrix form, rank, solvability, eigenvalues | Linear algebra | `linear-algebra-networks` |
| Steady-state flux routes, conservation, pathways; topology and stoichiometry only | Stoichiometric | `stoichiometric-networks` |
| Best achievable flux, growth, knockouts; bounds but no kinetics | Constraint-based (FBA) | `flux-balance-analysis` |
| Time courses, steady states and their stability, with rate laws | ODE | `ode-dynamics` |
| Feedback, inputs and outputs, whether a state can be steered or observed | Control theory | `control-systems-feedback` |
| Rate laws of single enzymes, inhibition, cooperativity | Enzyme kinetics | `enzyme-kinetics` |
| Drug concentration and effect over time | PK and PD | `pharmacokinetic-modeling` |
| Low copy numbers, noise, cell-to-cell variation | Stochastic | `stochastic-discrete-models` |
| Only on and off states known; large regulatory networks | Boolean or logical | `stochastic-discrete-models` |
| Many variables, few samples; which variables separate groups | Multivariate statistics | `multivariate-omics` |
| A scored readout, a questionnaire, a composite index, a group comparison | Measurement and statistics | `quantitative-research-methods` |

More detail on choosing, including when to combine formalisms, is in `references/formalism-choice.md`.

## Failure and edge cases

- **The formalism chosen before the question,** usually an ODE model because it looks rigorous.
- **A boundary that moves during the project,** so early and late results describe different systems.
- **Parameters taken from different organisms, temperatures or assays** without saying so.
- **Fitting and testing on the same data,** then calling the fit a validation.
- **A model with more unknown parameters than independent observations,** reported with point estimates.
- **Units mixed between data sources** (mM against µM, minutes against hours).
- **A network drawn from a database without checking its evidence codes** or its organism.

## Validation

- The question names a measurable quantity and a comparison.
- Every species and parameter has a unit, a source and a status (measured, fitted, assumed).
- The formalism's choice is justified against at least one lighter alternative.
- At least one prediction was tested on data not used to build or fit the model.
- Falsifier: an experiment, stated in advance, whose result would show the model is wrong.

## Expected output

The question as an observable; the network and boundary; the formalism with its justification; an ordered
plan naming the skill for each step; the open assumptions; and the project log.

## Sources and confidence

- Sauter and Albrecht, *Introduction to Systems Biology: Workbook for Flipped-Classroom Teaching*, Open Book
  Publishers 2023, doi:10.11647/OBP.0291 (supplied text: introduction and learning checklist): the four parts
  of increasing modelling detail (network matrices and linear algebra; stoichiometric models; dynamics,
  control and systems theory; physical modelling and enzyme kinetics), and the systems medicine framing
  drawn from Apweiler et al. 2018, doi:10.1038/emm.2017.290. Chapter text was not seen
- Formalism choice and failure list: author knowledge, consistent with Kitano 2002, doi:10.1126/science.1069492,
  and Tavassoly, Goldfarb and Iyengar 2018, doi:10.1042/EBC20180003 (records checked on Crossref 2026-10-15;
  content from author knowledge, VERIFY)
- Not covered: spatial models (PDE, agent-based) beyond a pointer, and multiscale coupling
