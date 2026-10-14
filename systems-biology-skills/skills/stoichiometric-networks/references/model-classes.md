# Classes of metabolic models

| Class | Ingredients | Steady state assumed | Typical outputs |
|---|---|---|---|
| Topological | Which metabolites connect to which | No | Connectivity, reachability |
| Stoichiometric | N | Yes, N v = 0 | Flux space, elementary modes, conservation relations |
| Constraint-based | N, flux bounds, optionally an objective | Yes | FBA optimum, flux variability, knockout predictions |
| Stationary MFA | N, measured exchange fluxes | Yes | Internal fluxes, if determined |
| 13C (isotope-tracer) MFA | N, atom transitions, labelling patterns | Metabolic and isotopic steady state (or isotopically non-stationary variants) | Internal fluxes including parallel routes and cycles |
| Dynamic MFA | N, time-resolved measurements | Pseudo-steady state in windows | Flux changes over time |
| Kinetic | N, rate laws, parameters | No | Concentrations and fluxes over time |

The workbook's checklist asks to classify MFA by whether it is dynamic and whether it uses isotope tracers;
the rest of the table is author knowledge, VERIFY.
