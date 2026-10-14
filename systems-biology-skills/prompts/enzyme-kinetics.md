# `enzyme-kinetics` prompts

Choose, derive and fit enzyme rate laws, and read inhibition and cooperativity correctly.

- **Give it:** the reaction and mechanism as far as known, the data (substrate concentrations, initial rates,
  replicates, inhibitor levels) with units, and the conditions
- **Skill file:** [`skills/enzyme-kinetics/SKILL.md`](../skills/enzyme-kinetics/SKILL.md)
- **Rate laws:** [`rate-laws.md`](../skills/enzyme-kinetics/references/rate-laws.md)

## 1. Fit Michaelis-Menten

> Fit Michaelis-Menten to my data (S in mM, v in µM/min): S,v 0.1,0.9; 0.25,1.9; 0.5,3.4; 1,4.9; 2,6.8; 4,8.0; 8,8.9. Is fitting the Lineweaver-Burk plot OK?

A good answer: nonlinear least squares gives Vmax ≈ 10.06 µM/min and Km ≈ 1.01 mM. The substrate range covers
Km, so both are well determined. The Lineweaver–Burk regression happens to give similar values on these
clean data, but it should not be used for estimation: taking reciprocals magnifies the error of the slowest
rates. Use the plot only to show the inhibition pattern.

## 2. Which inhibition type

> With an inhibitor, the apparent Km of my enzyme rises from 1 to 3 mM while Vmax stays at 10. What type of inhibition is this, and what is Ki if the inhibitor is at 1 mM?

A good answer: competitive inhibition, since only the apparent Km changes. Km(1 + I/Ki) = 3 gives Ki = 0.5 mM.
At S = 2 the rate falls from 6.67 to 4.

## 3. Hill coefficient

> My fit gives a Hill coefficient of 2.4. Does that mean the enzyme has 2.4 binding sites?

A good answer: no. The Hill coefficient measures cooperativity and is a lower bound on the number of
interacting sites, not a count. A value of 2.4 means strong positive cooperativity, consistent with at
least three sites. It suggests a mechanistic model (for example MWC) if the mechanism matters.

## 4. Rate falls at high substrate

> My enzyme's rate rises, peaks around 2 mM substrate, and falls at higher concentrations. Which rate law should I use?

A good answer: substrate inhibition, v = Vmax S/(Km + S + S²/Ksi). Compare it with plain Michaelis–Menten
using AICc, check the fall is not caused by a contaminant or an assay artefact, and cover enough points
on both sides of the peak.

## 5. Derive Michaelis-Menten

> Derive the Michaelis-Menten equation from mass action for E + S <-> ES -> E + P and state the assumptions.

A good answer: setting d[ES]/dt = 0 (quasi-steady state) and using enzyme conservation E_total = E + ES gives
v = k2 E_total S/((k−1 + k2)/k1 + S), so Vmax = k2 E_total and Km = (k−1 + k2)/k1. The assumptions are enzyme
much scarcer than substrate, initial rate with no product, and an irreversible catalytic step. Km equals the
dissociation constant only when k2 is much smaller than k−1.
