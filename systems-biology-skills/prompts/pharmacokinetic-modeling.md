# `pharmacokinetic-modeling` prompts

Model drug concentration and effect over time, from one-compartment basics to links with pathway models.

- **Give it:** dose, route and schedule; concentration–time data with units; known parameters with sources;
  effect data for PD; and the population
- **Skill file:** [`skills/pharmacokinetic-modeling/SKILL.md`](../skills/pharmacokinetic-modeling/SKILL.md)
- **Formulas:** [`pk-formulas.md`](../skills/pharmacokinetic-modeling/references/pk-formulas.md)

## 1. Half-life and exposure

> What is the half-life of a drug given as a 100 mg IV bolus with volume of distribution 20 L and clearance 5 L/h? Give the concentration at 2 h and the AUC.

A good answer: k = CL/V = 0.25 per hour and t½ = ln 2/k ≈ 2.77 h. C0 = 5 mg/L, C(2 h) ≈ 3.03 mg/L, and
AUC to infinity = Dose/CL = 20 mg·h/L, assuming linear one-compartment kinetics.

## 2. Oral dose

> The same drug is given orally at 100 mg with bioavailability 0.8 and absorption rate constant 1.5 per hour. When is the peak and how high is it?

A good answer: tmax = ln(ka/k)/(ka − k) ≈ 1.43 h and Cmax ≈ 2.80 mg/L, from the Bateman function. AUC is
F·Dose/CL = 16 mg·h/L.

## 3. Accumulation

> If I give 100 mg every 8 hours, how much will the drug accumulate and what is the average steady-state concentration?

A good answer: accumulation ratio 1/(1 − e^(−kτ)) ≈ 1.16 and Css,avg = F·Dose/(CL τ) = 2.5 mg/L. About 90
percent of steady state is reached after about 3.3 half-lives, roughly 9.2 h.

## 4. AUC from samples

> Compute the AUC from these samples (t in h, C in mg/L): 0 0; 0.5 2.1; 1 3.0; 2 2.8; 4 1.6; 8 0.5; 12 0.15. Should I use the linear or the log-down trapezoidal method?

A good answer: the linear trapezoidal AUC from 0 to 12 h is 14.6 mg·h/L, and the linear-up, log-down
method gives about 13.9. The log-down method is preferred on the declining part because concentrations
fall exponentially and linear trapezoids overestimate. Report the extrapolated share if AUC to infinity
is given.

## 5. Effect lags concentration

> When I plot effect against plasma concentration, the points form a loop: the effect is higher on the way down than on the way up. What does that mean for my PD model?

A good answer: anticlockwise hysteresis, meaning the effect lags the plasma concentration. Use an effect
compartment (link model) or an indirect-response model rather than a direct Emax model, and check for
active metabolites.
