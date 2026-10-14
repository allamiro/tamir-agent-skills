# `flux-balance-analysis` prompts

Find the best a metabolic network can do within its bounds, check whether that optimum is unique, and
predict knockouts, with the method's limits stated.

- **Give it:** the network, flux bounds and medium, the objective and why it is plausible, and any measured
  rates for comparison
- **Skill file:** [`skills/flux-balance-analysis/SKILL.md`](../skills/flux-balance-analysis/SKILL.md)
- **Checklist before trusting a result:** [`fba-checklist.md`](../skills/flux-balance-analysis/references/fba-checklist.md)

## 1. Run FBA and knockouts

> Run flux balance analysis on this network to maximise R6, check whether the solution is unique with flux variability analysis, and say which reactions are essential: R1: -> A, R2: A -> B, R3: A -> C, R4: B -> D, R5: C -> 2 D, R6: D ->, with bounds R1 0 to 10 and R4 0 to 3.

A good answer: the optimum is R6 = 20, through R1 = 10, R3 = 10 and R5 = 10, because the C route makes two D
per A. FVA shows every flux fixed at the optimum. Knockouts: R1 and R6 are essential (objective 0), while
knocking out R3 or R5 drops the objective to 3 through the capped B route.

## 2. Growth from nothing

> My FBA model reaches the default bound of 1000 on the objective. What is wrong?

A good answer: a bound is missing. Most likely an uptake reaction is unbounded, or a loop or energy-generating
cycle carries unlimited flux. Fix the medium (bound every uptake), close all uptakes and confirm the
objective drops to zero, and check for loops with FVA.

## 3. Pros and cons

> List the pros and cons of FBA for predicting growth of E. coli on glucose.

A good answer: pros are no kinetic parameters, genome scale, fast convex optimisation and testable knockout
predictions. Cons are an assumed objective, alternative optima, no regulation, no metabolite concentrations
or dynamics, and strong dependence on bounds. It mentions overflow metabolism as a known failure of plain
FBA without enzyme constraints.

## 4. Gene essentiality

> Can I call a gene essential if knocking out its reaction gives zero growth in FBA?

A good answer: not directly. Gene–reaction rules matter: isozymes can carry the reaction, and one gene may
catalyse several reactions. Use gene knockouts through the rules (for example in COBRApy), set a growth
threshold, and compare with experimental essentiality data.

## 5. Genome-scale model

> I downloaded a genome-scale model in SBML. What should I check before running FBA?

A good answer: run MEMOTE, set the medium bounds, confirm there is no growth with all uptakes closed, check
reaction balance and for energy-generating cycles, check the biomass objective is for the organism, and
record the model version and solver.
