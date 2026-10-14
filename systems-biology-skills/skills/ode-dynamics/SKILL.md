---
name: ode-dynamics
description: Builds, simulates and analyses ordinary differential equation models of biological dynamics, covering turning one ODE into a system, ODE versus PDE, analytical solution by separation of variables and integrating factors, numerical integration (Euler, Runge-Kutta, stiff solvers), steady states, linearisation and the Jacobian, eigenvalue-based stability classification, phase portraits, trajectories, slope fields and nullclines, nonlinear behaviour such as bistability and hysteresis, and local sensitivity analysis. Use for "simulate my ODE model", "find the steady states", "is this steady state stable", "draw the phase portrait", "which parameters matter most", "why does my simulation blow up", "solve this differential equation by hand", "is my system bistable". Use control-systems-feedback for transfer functions and controllability, enzyme-kinetics for rate laws, and parameter-estimation-model-selection to fit the model to data.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# ODE dynamics

## Purpose and activation

ODE models describe how concentrations change over time when the system is well mixed and copy numbers
are large. The analysis has two halves: simulation (what happens from these initial values) and
qualitative analysis (where are the steady states, are they stable, what happens near them, which
parameters matter). Activate when a dynamic model is written, simulated, analysed or debugged, or when an
ODE has to be solved by hand.

## Required inputs

The state variables with units and initial values; the rate laws and parameters with units and sources;
the time span; the question (time course, steady state, stability, sensitivity, bifurcation); and any data
for comparison.

## Workflow

1. **Write the model** in the script format (`var`, `par`, `d`), one balance per state, with units checked by
   `quantities-units-balances`. A higher-order ODE becomes a system by introducing derivatives as new states.
2. **Solve by hand when possible:** separable equations by separation of variables; linear first-order
   equations by an integrating factor. Use the result to check the simulation.
3. **Simulate** with `python3 scripts/ode.py simulate MODEL.txt --t T [--dt] [--method rk4|euler]`. Halve the step and
   confirm the result does not change; if it does, or the stiffness ratio is large, use a stiff solver.
4. **Find steady states** with `python3 scripts/ode.py steady MODEL.txt` from several starting points; a nonlinear model may have
   more than one.
5. **Classify stability** with `python3 scripts/ode.py stability MODEL.txt`: the Jacobian at the steady state and its eigenvalues
   (`references/stability-classes.md`). All real parts negative means locally stable.
6. **Draw the phase portrait** for two-state models: nullclines (where one derivative is zero) cross at steady
   states; the slope field shows the flow; trajectories follow it.
7. **Check for bistability and hysteresis:** sweep a parameter up and down; if the steady state reached
   depends on the direction of the sweep, the system has memory.
8. **Rank parameters** with `python3 scripts/ode.py sens MODEL.txt --t T`: normalised local sensitivities (percent change in output per
   percent change in parameter). Local sensitivity holds only near the nominal values; use global methods
   when parameters are uncertain over orders of magnitude.

## Decision framework

| Situation | Choose |
|---|---|
| Smooth, non-stiff, teaching model | Fixed-step RK4 (the script) |
| Fast and slow processes together (stiff) | Adaptive implicit solver (BDF, LSODA) or COPASI |
| Spatial gradients matter | PDE (reaction–diffusion) rather than ODE |
| Low copy numbers | Stochastic simulation (`stochastic-discrete-models`) |
| Uncertain parameters over wide ranges | Global sensitivity (for example Sobol or Morris): VERIFY method choice |
| Steady state only | Solve f(x) = 0 directly; no need to simulate |

## Failure and edge cases

- **Euler with too large a step** gives oscillations or blow-up that are numerical, not biological.
- **Negative concentrations** from a step too large or a missing positivity constraint.
- **A steady state found from one starting point** reported as the only one.
- **Stability of a nonlinear system judged from simulation alone;** use eigenvalues at the steady state.
- **Zero real part eigenvalues:** linearisation cannot decide; a bifurcation may be near.
- **Sensitivities computed at an unrealistic nominal point.**
- **Conservation relations ignored,** giving a singular Jacobian (use `stoichiometric-networks` to find them).

## Validation

- `python3 scripts/ode.py --selftest` passes, including an analytic exponential decay and a logistic solution.
- Halving the step changes the reported values by less than the stated tolerance.
- f(x*) is zero at each reported steady state, within tolerance.
- Conserved totals stay constant in the simulation.
- Falsifier: a predicted steady state or time course that a new experiment contradicts beyond measurement error.

## Expected output

The model with units; analytical solutions where they exist; simulated time courses with the method and
step; steady states with stability classes; phase portrait notes; sensitivity ranking; and any numerical
caveats.

## Sources and confidence

- Sauter and Albrecht 2023, doi:10.11647/OBP.0291, learning checklist Part 3 (supplied text): ODE, ODE versus
  PDE, systems of ODEs, nonlinear dynamics, hysteresis, steady state, stability, damping, characteristic
  polynomial, eigenvalue-based stability classification, phase portrait, trajectory, slope field, isoclines,
  differentiation rules, separation of variables, integration factor and linearisation; sensitivity analysis
  in Part 4. Chapter text not seen
- Numerical and stability theory: standard, author knowledge, VERIFY; parameter sensitivity spread in systems
  biology models: Gutenkunst et al. 2007, doi:10.1371/journal.pcbi.0030189 (record checked 2026-10-15)
