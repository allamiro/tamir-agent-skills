# `systems-biology-workflow` prompts

Start a systems biology project from the question, choose the lightest modelling formalism that can
answer it, and put the steps in order.

- **Give it:** the biological question, what the answer will be used for, the system boundary, the data you
  have (topology, fluxes, time courses, single-cell counts, omics tables) and the time scale
- **Skill file:** [`skills/systems-biology-workflow/SKILL.md`](../skills/systems-biology-workflow/SKILL.md)
- **Choosing a formalism:** [`formalism-choice.md`](../skills/systems-biology-workflow/references/formalism-choice.md)
- **Project log template:** [`project-log.md`](../skills/systems-biology-workflow/assets/templates/project-log.md)

## 1. Which kind of model do I need

> I want to model the glycolysis pathway in yeast. I have the reaction list and measured uptake and secretion rates, but no kinetic parameters. Which kind of model should I build first, and what should my project plan look like?

A good answer: turns "model glycolysis" into a question about an observable (for example which flux
distributions are possible, or the maximum ethanol yield), and recommends a stoichiometric or
constraint-based model first because no kinetic parameters are available, with an ODE model only if
regulation or transients become the question. It orders the steps (network and balances, assumptions,
analysis, comparison with measured rates, review, standard format, write-up) and names the skill for each.

## 2. Too many parameters

> My ODE model of a signalling pathway has 45 parameters and I have three time courses of one phosphorylated protein. My supervisor says the model is too big. Is that right, and what should I do?

A good answer: agrees that the model is very likely unidentifiable, since 45 unknowns cannot be pinned down
by three time courses of one readout. It suggests reducing the model (lumping steps, quasi-steady state,
fixing literature parameters), checking identifiability, asking which question needs this detail, and
planning experiments that measure more states or perturbations.

## 3. Low copy numbers

> The transcription factor I study has about 20 molecules per cell and the cells show two subpopulations. My colleague built an ODE model that gives one steady state. What formalism should I use instead?

A good answer: says that at about 20 molecules noise matters, so a stochastic model (Gillespie simulation) is
needed. Bimodality may come from noise-driven switching between states of a bistable system, which an ODE
model with one steady state cannot show. It suggests first checking for bistability in the deterministic
model (`ode-dynamics`), then simulating stochastically (`stochastic-discrete-models`) and comparing the
distributions with single-cell data.

## 4. Order the steps

> I have a draft metabolic network, flux measurements, and want to publish a model of how a knockout changes lactate secretion. List the steps in order, with what to check at each.

A good answer: an ordered plan: state the observable (lactate secretion with and without the knockout), check
units and element balance, write assumptions, run FBA with the measured uptake bounds and FVA, simulate the
knockout, compare with measured secretion, review the model, encode it in SBML with annotations, and write it
up. It names a falsifier stated in advance.

## 5. Systems medicine question

> We want to use patient data, a pathway model and drug exposure to stratify patients for a targeted therapy. How do these pieces fit together, and what are the main risks?

A good answer: links PK (exposure), a mechanistic pathway model (target response) and statistical models of
patient variation, with each part's scale and interface variables stated. Risks named: data quality and
provenance across sources, unvalidated readouts, parameters from cell lines applied to patients, and
predictions fitted and tested on the same patients. It recommends a focused clinical question and validation
on an independent cohort.
