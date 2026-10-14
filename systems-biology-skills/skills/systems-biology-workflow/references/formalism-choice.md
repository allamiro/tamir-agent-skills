# Choosing a formalism

The lightest formalism that answers the question is usually the right first model. Each step up adds
parameters that must be measured or fitted.

| Formalism | Needs | Gives | Cannot give |
|---|---|---|---|
| Graph | Nodes and edges, perhaps signs | Connectivity, centrality, modules, motifs, paths | Fluxes, time courses, quantities |
| Stoichiometric | Reaction equations | Steady-state flux space, conservation relations, elementary modes | Which flux distribution the cell uses |
| Constraint-based | Stoichiometry, bounds, an objective | An optimal flux distribution and its ranges, knockout effects | Dynamics, regulation, metabolite levels |
| ODE (mass action or rate laws) | Rate laws, parameters, initial values | Time courses, steady states, stability, sensitivity | Noise at low copy numbers; space |
| Stochastic (SSA) | Same as ODE, in molecule counts | Distributions, extinction, noise-driven switching | Fast answers for large systems |
| Boolean or logical | Activation and inhibition rules | Attractors (stable states and cycles), perturbation effects | Timing and graded responses |
| PK and PD | Dose, sampling times, concentrations | Exposure (AUC, Cmax), half-life, dose to effect | Mechanism inside the tissue, unless built in |
| Multivariate statistics | A samples-by-variables table | Main sources of variation, predictive variables | Mechanism |

## When to step up

- From graph to stoichiometric: the question involves mass flow or steady-state feasibility.
- From stoichiometric to constraint-based: the question is "what is the best the network can do".
- From constraint-based to ODE: regulation, timing, metabolite concentrations or transient behaviour matter.
- From ODE to stochastic: copy numbers are below roughly hundreds, or variation between cells is the point.
- From ODE to Boolean: the network is too large to parameterise and only qualitative states are known.

## Combining formalisms

- Use a stoichiometric analysis to check an ODE model's mass balances and conservation relations before simulating.
- Use FBA fluxes as a consistency check on the steady state of a kinetic model of the same network.
- Use a graph analysis to choose a module to model kinetically, and say why the rest was left out.
- In systems medicine, link a mechanistic module to PK for exposure and to statistics for patient variation;
  state the scale each part covers (seconds to years) and the interface variables.

Source: author knowledge, organised around the four parts of the Sauter and Albrecht workbook; VERIFY
specific claims against the methods literature cited in each skill.
