# `quantities-units-balances` prompts

Catch unit errors before they become results, and write the balances that every dynamic model rests on.

- **Give it:** the equations or model file, every parameter with its value and unit as reported, the units of
  the data, and for a balance the control volume, its flows and its reactions
- **Skill file:** [`skills/quantities-units-balances/SKILL.md`](../skills/quantities-units-balances/SKILL.md)
- **Unit pitfalls:** [`unit-pitfalls.md`](../skills/quantities-units-balances/references/unit-pitfalls.md)

## 1. Check my units

> Are my units consistent? My model has dC/dt = k1*C*E with C and E in mM, k1 = 1e6 per molar per second, and time in seconds. Convert k1 to per micromolar per second and per millimolar per second.

A good answer: k1 has units of 1/(concentration × time), so it is second order. 1e6 1/(M s) equals 1 1/(µM s)
and 1000 1/(mM s). With C and E in mM, the model needs k1 = 1000 1/(mM s). The right side then has units of
mM/s, matching dC/dt.

## 2. Per minute or per hour

> A paper gives a degradation rate of 0.1 per minute but my simulation runs in hours. What value do I use?

A good answer: 6 per hour (0.1 × 60). It converts the parameter rather than the time axis and records the
source value and factor.

## 3. Chemostat steady state

> A chemostat runs at dilution rate 0.2 per hour with Monod growth, mumax 0.5 per hour, Ks 0.1 g/L, feed substrate 10 g/L and yield 0.5 g biomass per g substrate. What are the steady-state substrate and biomass concentrations, and at what dilution rate does washout occur?

A good answer: at steady state the growth rate equals D, so S\* = Ks D/(mumax − D) = 0.0667 g/L and
X\* = Y (S0 − S\*) = 4.97 g/L. Washout happens when D reaches mumax S0/(Ks + S0), about 0.495 per hour.

## 4. Growing volume

> My fed-batch reactor volume grows from 1 to 2 L over the run. I wrote dX/dt = mu*X for the biomass concentration. What is wrong?

A good answer: the balance must be on the amount (X V), so the concentration balance needs a dilution term:
dX/dt = mu X − (F/V) X, with F the feed rate (dV/dt = F). Leaving it out overestimates the concentration.

## 5. Extensive or intensive

> Which of these are extensive and which intensive: mass of biomass, glucose concentration, reactor volume, temperature, amount of ATP, pH? Which ones can I write a balance for directly?

A good answer: extensive are biomass mass, reactor volume and amount of ATP; intensive are glucose
concentration, temperature and pH. Balances are written for extensive quantities (mass, amount, volume,
energy). Intensive ones follow by dividing by volume, or for pH from the amounts of the species involved.
