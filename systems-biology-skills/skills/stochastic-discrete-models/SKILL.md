---
name: stochastic-discrete-models
description: Builds and analyses stochastic and discrete models of biological systems, covering the Gillespie stochastic simulation algorithm and when copy numbers make noise matter, intrinsic versus extrinsic noise, Boolean and logical network models with synchronous and asynchronous updating and their attractors, systems discrete in state and time, difference equations and the logistic map with fixed points and chaos. Use for "simulate this at low copy number", "how noisy is expression", "build a Boolean model of this regulatory network", "find the attractors", "difference equation for population growth", "is the logistic map chaotic here", "when do I need a stochastic model". Use ode-dynamics for deterministic continuous models, network-analysis for graph structure, and control-systems-feedback for feedback design.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# Stochastic and discrete models

## Purpose and activation

ODE models assume large copy numbers and continuous time and state. When a gene has one or two copies, a
transcription factor a few dozen molecules, or the question is variation between cells, randomness is the
phenomenon, and stochastic simulation is needed. When the network is large and only on and off states are
known, a Boolean model gives its stable states without kinetic parameters. Populations counted per
generation call for difference equations. Activate for low copy numbers, noise, logical models or
discrete-time dynamics.

## Required inputs

For stochastic models: species with initial molecule counts, reactions with stochastic rate constants,
and the cell volume used to convert from concentrations. For Boolean models: nodes and their update rules
from the literature with references. For difference equations: the update rule and its parameters.

## Workflow

1. **Decide whether noise matters:** copy numbers below roughly hundreds, bursts, bimodal distributions in
   single-cell data, or a question about variation all point to a stochastic model.
2. **Convert rate constants** from concentration units to stochastic constants with Avogadro's number and the
   volume (`quantities-units-balances`); second-order constants scale with 1/(N_A V).
3. **Simulate** with `python3 scripts/discrete.py ssa REACTIONS.txt --t T --runs N --seed S` (Gillespie's direct method);
   report the mean and spread across runs and compare the mean with the ODE solution.
4. **Separate noise sources** if data allow: intrinsic (from the reactions themselves) and extrinsic (from
   variation in shared factors between cells), for example with dual reporters.
5. **Boolean models:** write one rule per node and find attractors with `python3 scripts/discrete.py boolean RULES.txt`.
   Fixed points are stable states (often cell types or fates); cycles are oscillations. Check whether
   asynchronous updating changes the attractors before interpreting synchronous ones.
6. **Difference equations:** iterate and find fixed points; the logistic map x' = r x (1 - x) shows how a simple
   rule gives a stable point, oscillations and chaos as r rises (`python3 scripts/discrete.py map --r R`).
   Stability of a fixed point needs |f'(x*)| < 1.
7. **Report** the number of runs, the seeds, the update scheme and the sensitivity of conclusions to them.

## Decision framework

| Situation | Model |
|---|---|
| Large copy numbers, mean behaviour | ODE |
| Low copy numbers, exact trajectories | Gillespie SSA |
| Many molecules but noise still matters, speed needed | Chemical Langevin or tau-leaping: VERIFY accuracy conditions |
| Large regulatory network, qualitative data | Boolean or multivalued logical model |
| Timing unknown in a logical model | Asynchronous update, or analyse both |
| Generations or seasons | Difference equation |

## Failure and edge cases

- **One stochastic run shown** as if it were typical.
- **Rate constants not converted** between deterministic and stochastic forms.
- **Synchronous Boolean updating** producing cycles that vanish under asynchronous updating.
- **Rules taken from different cell types** combined into one Boolean model.
- **Chaos claimed** from a short or noisy time series.
- **Seeds not recorded,** so runs cannot be repeated.

## Validation

- `python3 scripts/discrete.py --selftest` passes, including an SSA mean that matches the ODE solution for a linear birth–death process.
- For linear networks, the SSA mean matches the ODE solution within sampling error.
- Every attractor reported is a fixed point or cycle of the update rule (check by applying it).
- Results are stable when the number of runs is doubled.
- Falsifier: a measured single-cell distribution whose shape (for example bimodality) the model cannot produce.

## Expected output

The justification for a stochastic or discrete model; the model with converted constants; simulation
summaries (mean, variance, distribution, number of runs, seeds); attractors and their interpretation;
fixed points and stability for difference equations; and caveats about update schemes.

## Sources and confidence

- Sauter and Albrecht 2023, doi:10.11647/OBP.0291, learning checklist Parts 3 and 4 (supplied text): systems
  discrete in state and time, difference equations and noise are listed topics. Chapter text not seen
- Gillespie 1977, doi:10.1021/j100540a008; Kauffman 1969, doi:10.1016/0022-5193(69)90015-0 (random Boolean
  networks). Records checked on Crossref 2026-10-15; content from author knowledge, VERIFY
- `references/noise-and-logic.md` summarises the conversions and logic conventions (author knowledge, VERIFY)
