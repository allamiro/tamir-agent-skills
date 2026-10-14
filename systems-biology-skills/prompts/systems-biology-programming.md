# `systems-biology-programming` prompts

Write, test and share models in standard formats with code others can rerun.

- **Give it:** the model and its formalism, your language and tools, what will be shared and with whom, and any
  journal or repository requirements
- **Skill file:** [`skills/systems-biology-programming/SKILL.md`](../skills/systems-biology-programming/SKILL.md)
- **Code practices:** [`code-practices.md`](../skills/systems-biology-programming/references/code-practices.md)
- **Model repository README template:** [`model-repo-readme.md`](../skills/systems-biology-programming/assets/templates/model-repo-readme.md)

## 1. Check my reactions are balanced

> Check my reactions are balanced. Reactions: R1: glc + 6 o2 -> 6 co2 + 6 h2o; R2: pyr + nadh -> lac + nad; EX_glc: glc ->. Formulas and charges: glc C6H12O6 0, o2 O2 0, co2 CO2 0, h2o H2O 0, pyr C3H3O3 -1, lac C3H5O3 -1, nadh C21H27N7O14P2 -2, nad C21H26N7O14P2 -1.

A good answer: R1 is balanced. R2 is unbalanced by H +1 and charge +1 (products minus substrates), because a
proton is missing on the substrate side: pyr + nadh + h → lac + nad balances. EX_glc is an exchange reaction,
unbalanced by design, and should be named so it is excluded from the check.

## 2. Simulate in Python

> Write Python code to simulate my SBML model of a signalling pathway for 100 minutes and plot two species. Which library should I use?

A good answer: libRoadRunner or Tellurium to load the SBML directly (or SciPy solve_ivp with a stiff method if
the equations are hand-coded), with the solver and tolerances stated, fixed time points, versions pinned and
the model file as the source of truth. The code reads the file rather than re-typing the equations.

## 3. Annotate and deposit

> How do I annotate my model and deposit it in BioModels?

A good answer: annotate species and reactions with identifiers.org URIs to ChEBI, UniProt, Rhea, GO and SBO,
following MIRIAM, with creator, dates and reference publication. Validate the SBML with units, describe the
simulations in SED-ML, check the model reproduces the paper's figures, and submit to BioModels with the
files and a COMBINE archive if possible.

## 4. Test a metabolic model

> What tests should I write for my genome-scale metabolic model before publishing?

A good answer: run MEMOTE. Test that there is no growth with all uptakes closed, that there are no
energy-generating cycles, and that reactions are element- and charge-balanced except exchange, demand and
biomass. Check known essential genes and growth rates on several media, with fixed solver settings
recorded.

## 5. Make it reproducible

> My simulation results changed after I updated my Python environment. How do I make my modelling reproducible?

A good answer: pin exact versions or use a container, record the solver and tolerances, and fix seeds. Keep
the model in SBML with SED-ML for simulations, make figures from one command, and test known behaviour so
a library change that alters results is caught.
