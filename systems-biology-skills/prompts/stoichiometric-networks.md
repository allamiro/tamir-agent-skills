# `stoichiometric-networks` prompts

Build the stoichiometric matrix and read off steady-state fluxes, conservation relations, elementary modes
and what flux measurements determine.

- **Give it:** the reactions with coefficients and reversibility, which metabolites are external, and for MFA
  the measured fluxes with their uncertainty
- **Skill file:** [`skills/stoichiometric-networks/SKILL.md`](../skills/stoichiometric-networks/SKILL.md)
- **Classes of metabolic models:** [`model-classes.md`](../skills/stoichiometric-networks/references/model-classes.md)

## 1. Matrix, null space and modes

> Build the stoichiometric matrix for R1: -> A, R2: A -> B, R3: A -> C, R4: B -> D, R5: C -> D, R6: D ->, give its rank and the steady-state flux space, and enumerate the elementary flux modes.

A good answer: a 4 × 6 matrix (A, B, C, D by R1–R6) of rank 4, so the steady-state flux space has
dimension 2. There are 2 elementary flux modes: R1, R2, R4, R6 and R1, R3, R5, R6, each with unit flux.
If it gives a null-space basis, it checks the basis against irreversibility rather than assuming the basis
vectors are the pathways.

## 2. Which fluxes can I calculate

> In the same network, I measured R1 = 10 and R2 = 4. Which fluxes are determined, and is the system determined, underdetermined or redundant? What if I had measured only R1?

A good answer: with R1 = 10 and R2 = 4 the system is determined: R3 = 6, R4 = 4, R5 = 6 and R6 = 10, with no
redundancy. With R1 alone it is underdetermined: R6 = 10 follows, but R2–R5 are not fixed, because the split
between the two branches is free.

## 3. Conservation relations

> Find the conservation relations of R1: S_ext + E <-> ES, R2: ES -> E + P_ext. Why do they matter for an ODE model?

A good answer: one conservation relation, E + ES = constant (total enzyme). An ODE model must keep this total
fixed, so one of the two equations can be replaced by the algebraic relation. Otherwise the Jacobian is
singular and the steady state is not isolated.

## 4. Cofactor pools

> In a closed glycolysis fragment R1: atp + glc -> adp + g6p, R2: g6p <-> f6p, R3: f6p + atp -> fbp + adp, which totals are conserved?

A good answer: atp + adp is conserved (the adenine nucleotide pool), along with combinations involving the
sugar phosphates. It notes that a basis of the left null space is not unique and should be read for
meaningful pools.

## 5. Isotope tracers

> My stationary MFA cannot separate flux through two parallel routes from glucose to pyruvate. What should I do?

A good answer: parallel routes and cycles are not determined by exchange measurements alone, because they lie
in the free directions of the null space. Use 13C tracer experiments, whose labelling patterns distinguish
the routes, or add measurements or constraints. State the metabolic and isotopic steady-state assumptions.
