---
name: stoichiometric-networks
description: Builds and analyses the stoichiometric matrix of a metabolic or reaction network, covering classification of metabolic models, steady state, the Rouche-Capelli theorem for flux solutions, right and left null spaces, conservation relations (conserved moieties), elementary flux modes, and metabolic flux analysis (MFA) with determined, underdetermined and redundant measurements, including dynamic and isotope-tracer MFA. Use for "build the stoichiometric matrix", "what fluxes are possible at steady state", "find the conservation relations", "enumerate elementary flux modes", "which fluxes can I calculate from these measurements", "is my MFA system determined". Use flux-balance-analysis for optimisation with bounds, linear-algebra-networks for general matrix work, and systems-biology-programming for element balance and SBML.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# Stoichiometric networks

## Purpose and activation

The stoichiometric matrix N (metabolites by reactions) encodes everything a reaction network's
structure says, without kinetics. At steady state N v = 0, so the possible flux distributions are its null
space; the left null space gives quantities the network conserves; elementary flux modes are the minimal
pathways. Metabolic flux analysis asks which fluxes a set of measurements pins down. Activate when the user
has reaction equations and asks about feasible fluxes, pathways, conservation or flux calculation.

## Required inputs

The reactions with stoichiometric coefficients and reversibility; which metabolites are internal (balanced)
and which external (boundary); measured fluxes with their uncertainty, for MFA; and the organism and
compartment, if the network comes from a reconstruction.

## Workflow

1. **Write the reactions** in the script format and build N with `python3 scripts/stoich.py matrix NETWORK.txt`. Mark
   boundary metabolites with `_ext` so they are not balanced.
2. **Check the balances** first: element and charge balance of each reaction with `systems-biology-programming`.
3. **Classify the model** (`references/model-classes.md`): stoichiometric, constraint-based, kinetic; and for
   MFA, stationary or dynamic, with or without isotope tracers.
4. **Find the steady-state flux space** with `python3 scripts/stoich.py null NETWORK.txt`: its dimension is reactions minus rank(N).
5. **Find conservation relations** with `python3 scripts/stoich.py conserved NETWORK.txt`: each vector g with g N = 0 is a weighted sum of
   metabolites that never changes (for example ATP + ADP + AMP). A kinetic model must respect them, and they
   reduce the number of independent ODEs.
6. **Enumerate elementary flux modes** for small networks with `python3 scripts/stoich.py efm NETWORK.txt`; each is a minimal set of
   reactions that can operate at steady state with irreversible reactions running forward.
7. **For MFA,** run `python3 scripts/stoich.py mfa NETWORK.txt --measured R1=10,R4=3`. The system is determined if the measured fluxes fix
   every free direction, underdetermined if some fluxes stay free (measure more, or use isotope tracers),
   and redundant if there are more measurements than needed, which allows a consistency (gross error) check.
8. **Interpret** fluxes in their units (for example mmol per gram dry weight per hour), and state what the
   structure alone cannot say (which mode the cell actually uses).

## Decision framework

| Question | Method |
|---|---|
| Is a steady state possible at all with these exchanges | Null space, with signs for irreversible reactions |
| Minimal pathways, pathway yields | Elementary flux modes |
| Pools that must stay constant | Left null space (conservation relations) |
| Fluxes from a few measured exchanges | Stationary MFA by the null space and measured fluxes |
| Internal fluxes through parallel routes or cycles | Isotope-tracer (13C) MFA |
| Fluxes changing over time | Dynamic MFA |
| Best achievable yield or growth | `flux-balance-analysis` |

| MFA status | Meaning | Next step |
|---|---|---|
| Determined | Every flux follows from the measurements | Report with propagated uncertainty |
| Underdetermined | Free directions remain | Add measurements, tracers, or constraints |
| Redundant | More measurements than needed | Test consistency, then fit by weighted least squares |

## Failure and edge cases

- **External metabolites balanced** as if internal, which forces their exchange to zero.
- **Reversibility wrong,** so modes appear that run reactions backwards.
- **Elementary mode explosion:** the count grows combinatorially; the script stops at 16 irreversible directions.
- **Unbalanced reactions** that create mass and give impossible flux solutions.
- **Measured fluxes inconsistent** in a redundant system, averaged instead of checked.
- **Cycles (futile or exchange) that the null space allows** but no measurement constrains.

## Validation

- `python3 scripts/stoich.py --selftest` passes.
- N times each null-space vector is zero; each conservation vector times N is zero.
- rank(N) + dimension of the null space = number of reactions.
- Every elementary mode respects irreversibility and is support-minimal.
- Falsifier: a measured set of fluxes that violates N v = 0 beyond its uncertainty, showing a missing reaction.

## Expected output

The labelled stoichiometric matrix; its rank; the steady-state flux basis; conservation relations with
their meaning; elementary modes (small networks); for MFA, the status, the determined and free fluxes, and
the redundancy; and the limits of a structural analysis.

## Sources and confidence

- Sauter and Albrecht 2023, doi:10.11647/OBP.0291, learning checklist Part 2 (supplied text): classifying
  metabolic models, stoichiometric matrix, steady state, Rouché–Capelli, elementary flux modes, conservation
  relations, left and right null space, classifying MFA as dynamic or isotope-tracer, and MFA are listed
  topics. Chapter text not seen
- Schuster, Fell and Dandekar 2000, doi:10.1038/73786, for elementary modes (record checked on Crossref
  2026-10-15; content from author knowledge, VERIFY); 13C-MFA practice is author knowledge, VERIFY
