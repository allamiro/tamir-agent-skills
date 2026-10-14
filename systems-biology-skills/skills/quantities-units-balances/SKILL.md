---
name: quantities-units-balances
description: Checks quantities, SI units and dimensions in biological models, and writes mass, amount-of-substance and volume balances, covering quantity calculus, extensive versus intensive quantities, unit conversion (mM, µM, mol/m^3, per hour versus per second), the laws of thermodynamics as constraints, and bioreactor and chemostat balances. Use for "are my units consistent", "convert this rate constant", "write the mass balance for my reactor", "what is the dimension of this parameter", "why does my model give nonsense values", "chemostat steady state", "is this quantity extensive". Use model-building-design for assumptions, ode-dynamics to simulate the balances, and systems-biology-programming for element and charge balance of reactions.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# Quantities, units and balances

## Purpose and activation

A large share of modelling errors are unit errors: a rate constant in per minute used with time in
hours, a concentration in µM added to one in mM, a second-order constant treated as first order. Quantity
calculus (a quantity is a number times a unit, and both are carried through every step) catches them before
they become results. Balances (accumulation equals in minus out plus production minus consumption) are the
skeleton of every dynamic model. Activate whenever a model is written, data from several sources are
combined, or a result looks off by a power of ten.

## Required inputs

The equations or the model file; every parameter with its value and unit as reported by its source; the
units of the data; and, for a balance, the control volume, the flows across its boundary and the reactions
inside it.

## Workflow

1. **Write every quantity as value times unit,** and keep the unit through each calculation.
2. **Check each equation's dimensions** term by term with `python3 scripts/units.py dims "UNIT"` and
   `python3 scripts/units.py same "UNIT1" "UNIT2"`. Arguments of exp, log and powers must be dimensionless.
3. **Convert to one unit system** for the model with `python3 scripts/units.py convert VALUE UNIT --to UNIT`;
   record the conversion factor beside the source value.
4. **Classify quantities** as extensive (scale with system size: mass, amount, volume, energy) or intensive
   (do not: concentration, temperature, pressure, density). Balances are written for extensive quantities;
   intensive ones follow by dividing.
5. **Write the balance** for the control volume: d(amount)/dt = inflow - outflow + production - consumption.
   If the volume changes, the concentration balance gains a dilution term: dc/dt = (rates)/V - c (dV/dt)/V.
6. **Apply thermodynamic constraints:** energy is conserved (first law), and a reaction runs forward only
   if its Gibbs energy change is negative (second law), which fixes reaction directions in flux models.
7. **For a chemostat,** use `python3 scripts/units.py chemostat --D --mumax --Ks --S0 --Y` for the Monod steady state
   and the washout dilution rate; check that D is below the washout value before trusting the result.
8. **Report** the unit table and every conversion (`references/unit-pitfalls.md` lists frequent traps).

## Decision framework

| Situation | Do |
|---|---|
| Rate constant from a paper | Record the unit as printed; derive its order from the unit (1/s first order, 1/(M s) second order) |
| Concentrations from several sources | Convert all to one unit before fitting |
| Molecule counts in a stochastic model | Convert with Avogadro's number and the cell volume; state the volume |
| Changing volume (growth, fed-batch) | Balance amounts, not concentrations, or add the dilution term |
| Temperature in a rate law | Use kelvin; Celsius needs an offset, not a factor |
| A dimensionless group (Km/S, D/mumax) | Use it to reduce the parameter count and to compare regimes |

## Failure and edge cases

- **Per minute versus per hour** mixed between a parameter and the time axis.
- **Molar (mol/L) versus mol/m^3:** a factor of 1000 that is easy to miss.
- **Second-order rate constants** converted as if first order when changing concentration units.
- **Balances on concentration** when volume changes.
- **Celsius in an Arrhenius term.**
- **Specific rates** (per gram of biomass) used as volumetric rates.
- **Log of a dimensional quantity** without a reference value.

## Validation

- `python3 scripts/units.py --selftest` passes.
- Every term of every equation has the same dimension, checked with the script or by hand.
- Each converted value is traceable to the source value and the factor.
- A balance closes on its own data: total in minus total out equals accumulation within measurement error.
- Falsifier: a parameter whose unit, when carried through, does not give the unit of the output.

## Expected output

A unit table (quantity, symbol, value, unit, source, converted value); the dimension check per equation;
the balance equations for each control volume; thermodynamic direction constraints; and the conversions
used.

## Sources and confidence

- Sauter and Albrecht 2023, doi:10.11647/OBP.0291, learning checklist Part 4 (supplied text): the first and
  second laws of thermodynamics, extensive and intensive quantities, reading SI units, quantity calculus,
  balancing, mass, volume and amount-of-substance balances, and the bioreactor are listed topics; chapter
  text not seen, so the treatment is author knowledge: VERIFY
- Monod chemostat equations: standard bioprocess engineering, author knowledge, VERIFY against a bioprocess text
- The script's unit table covers common biochemical units only; it does not know every SI derived unit
