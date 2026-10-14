# Pharmacokinetic formulas (one compartment, linear)

| Quantity | Formula |
|---|---|
| Elimination rate constant | k = CL / V |
| Half-life | t½ = ln 2 / k |
| IV bolus concentration | C(t) = (Dose / V) e^(-k t) |
| Oral (Bateman) | C(t) = F·Dose·ka / (V (ka - k)) · (e^(-k t) - e^(-ka t)), ka ≠ k |
| Time of peak | tmax = ln(ka / k) / (ka - k) |
| AUC to infinity | AUC = F·Dose / CL |
| Accumulation ratio (dosing interval τ) | R = 1 / (1 - e^(-k τ)) |
| Average steady-state concentration | Css,avg = F·Dose / (CL τ) |
| Time to about 90 percent of steady state | about 3.3 half-lives |
| Emax model | E = E0 + Emax C^n / (EC50^n + C^n) |

Standard results (author knowledge, VERIFY); they match the skill's pk script.
