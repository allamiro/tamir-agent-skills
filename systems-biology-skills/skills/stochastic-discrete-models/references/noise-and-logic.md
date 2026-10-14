# Noise and logic: conversions and conventions

## Deterministic to stochastic rate constants (volume V, Avogadro N_A)

| Reaction | Deterministic constant | Stochastic constant c |
|---|---|---|
| ∅ → X | k (M/s) | c = k N_A V (molecules/s) |
| X → … | k (1/s) | c = k |
| X + Y → … | k (1/(M s)) | c = k / (N_A V) |
| X + X → … | k (1/(M s)) | c = 2k / (N_A V), propensity c·x(x-1)/2 (conventions differ by the factor 2: VERIFY your rate law's convention) |

## Noise measures

- Coefficient of variation CV = σ / μ; Fano factor F = σ² / μ (1 for a Poisson birth–death process).
- Bursty expression (several proteins per mRNA) raises the Fano factor above 1.

## Boolean conventions

- A rule gives a node's next value from the current values of its regulators.
- Synchronous: all nodes update together (deterministic, may create artefactual cycles).
- Asynchronous: one node at a time, in random or ordered sequence (closer to unequal time scales).
- An attractor is a set of states the system cannot leave: a fixed point (one state) or a cycle.
