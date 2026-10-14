---
name: flux-balance-analysis
description: Sets up, solves and interprets flux balance analysis (FBA) on metabolic networks, covering the constrained optimisation cone, objective functions such as biomass or ATP yield, flux bounds and exchange constraints, alternative optima and flux variability analysis (FVA), gene and reaction knockouts, the pros and cons of FBA, and scaling to genome-scale models with COBRApy. Use for "run FBA on this network", "what is the maximum growth rate", "which reactions are essential", "is my FBA solution unique", "flux variability analysis", "why does my model grow without a carbon source", "pros and cons of FBA". Use stoichiometric-networks for the null space and elementary modes, systems-biology-programming for SBML, COBRApy and MEMOTE, and ode-dynamics when kinetics matter.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# Flux balance analysis

## Purpose and activation

FBA finds a steady-state flux distribution that optimises an objective (often biomass production) within
bounds on each flux. It needs no kinetic parameters, which is why it scales to genome-scale models, but it
assumes the cell optimises something and it returns one of usually many optimal solutions. Activate when the
user wants the best achievable flux, growth or yield, essential reactions, or knockout effects.

## Required inputs

The network (reactions, reversibility); flux bounds, especially uptake limits on the medium; the objective
and why it is plausible for the organism and condition; for genome-scale work, the model file (SBML) and
its version; and any measured fluxes for comparison.

## Workflow

1. **Write the problem:** maximise c·v subject to N v = 0 and lower ≤ v ≤ upper. The feasible set is a convex
   polyhedral cone cut by the bounds; the optimum lies on its boundary.
2. **Set the medium** with bound lines (`bounds R1 0 10`). An uptake left at the default 1000 means
   "unbounded", and an objective that reaches 1000 means a bound is missing.
3. **Solve** with `python3 scripts/fba.py fba NETWORK.txt --objective R` (exact simplex for teaching-size networks).
4. **Check uniqueness** with `python3 scripts/fba.py fva NETWORK.txt --objective R [--fraction 0.9]`: each flux's range at (a fraction of) the
   optimum. A wide range means the optimum does not determine that flux.
5. **Knock out** reactions one at a time with `python3 scripts/fba.py ko NETWORK.txt --objective R`; a reaction is essential if the
   objective drops to zero (or below a stated threshold) without it.
6. **Scale up** with COBRApy for genome-scale models, and test the model with MEMOTE first
   (`systems-biology-programming`).
7. **Compare with data:** measured growth rates, uptake and secretion; disagreement points to wrong bounds,
   a wrong objective, or missing regulation.
8. **Report** the objective, every bound, the optimum, the variability ranges and the solver, after going
   through `references/fba-checklist.md`.

## Decision framework

| Situation | Choose |
|---|---|
| One optimal flux distribution needed for a figure | FBA, then FVA to show which fluxes are fixed |
| Many optima, want a representative one | Parsimonious FBA (minimise total flux at the optimum): VERIFY the variant |
| Essential genes | Knockouts through gene-protein-reaction rules (COBRApy), not reaction knockouts alone |
| Overflow metabolism, enzyme limits | Add enzyme or proteome constraints; plain FBA misses them |
| Dynamics of batch culture | Dynamic FBA (FBA in time steps with changing medium) |
| Regulation matters | Regulatory FBA or a kinetic model |

| FBA strength | FBA weakness |
|---|---|
| No kinetic parameters | Needs an assumed objective |
| Genome scale | Alternative optima: a single solution is not "the" fluxes |
| Fast, convex | No metabolite concentrations, no regulation, no time |
| Knockout predictions testable | Results depend strongly on bounds and medium |

## Failure and edge cases

- **Growth without a carbon source:** an open exchange or an energy-generating cycle; run FVA with uptakes closed.
- **One optimal solution reported as the flux distribution** without FVA.
- **Thermodynamically infeasible loops** carrying flux at the optimum.
- **Biomass objective from another organism** or condition.
- **Units mixed:** uptake in mmol/(gDW h) against growth in 1/h is correct only if biomass is defined per gram.
- **Reaction knockouts called gene essentiality** when isozymes exist.

## Validation

- `python3 scripts/fba.py --selftest` passes; the solver was cross-checked against SciPy's HiGHS on 250 random
  problems with no mismatch in the optimum.
- The solution satisfies N v = 0 and every bound.
- With all uptakes closed, the objective is zero.
- FVA minimum ≤ FBA value ≤ FVA maximum for every flux.
- Falsifier: a measured growth rate above the FBA maximum for the same medium.

## Expected output

The problem statement (objective, bounds, medium); the optimal value and one optimal flux distribution;
FVA ranges; knockout results; the comparison with data; and the stated limits.

## Sources and confidence

- Sauter and Albrecht 2023, doi:10.11647/OBP.0291, learning checklist Part 2 (supplied text): pros and cons of
  FBA, flux balance analysis and the constrained optimisation cone are listed topics. Chapter text not seen
- Orth, Thiele and Palsson 2010, doi:10.1038/nbt.1614; Mahadevan and Schilling 2003,
  doi:10.1016/j.ymben.2003.09.002 (alternative optima, FVA); Ebrahim et al. 2013, doi:10.1186/1752-0509-7-74
  (COBRApy). Records checked on Crossref 2026-10-15; content from author knowledge, VERIFY
- The pros and cons table and the variants (pFBA, dFBA, enzyme-constrained) are author knowledge, VERIFY
