---
name: pharmacokinetic-modeling
description: Models drug concentration and effect over time, covering one-compartment intravenous and oral (first-order absorption, Bateman) kinetics, clearance, volume of distribution, elimination rate and half-life, bioavailability, AUC by the trapezoidal and log-down methods, repeated dosing and accumulation, Emax and sigmoid Emax pharmacodynamics, and the step to physiologically based (PBPK) and quantitative systems pharmacology models. Use for "what is the half-life", "simulate an oral dose", "compute AUC from these samples", "how much will the drug accumulate", "fit an Emax model", "one or two compartments", "link my network model to drug exposure". Use ode-dynamics for general ODE work, parameter-estimation-model-selection to compare compartment models, and enzyme-kinetics for saturable metabolism rate laws.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# Pharmacokinetic modelling

## Purpose and activation

Pharmacokinetics (PK) describes what the body does to a drug (absorption, distribution, elimination);
pharmacodynamics (PD) describes what the drug does to the body. Linking them to a network model of the
target pathway is the core of quantitative systems pharmacology. Activate when the user works with doses,
plasma concentrations, exposure, half-life or concentration–effect relations, or wants to connect a
mechanistic model to dosing.

## Required inputs

The dose, route and schedule; concentration–time data with units and sampling times; known parameters
(clearance, volume, bioavailability, absorption rate) with sources; the effect measurements for PD; and
the population (healthy volunteers, patients, animals).

## Workflow

1. **Fix the units** (dose in mg, volume in L, clearance in L/h gives concentration in mg/L and k in 1/h) with
   `quantities-units-balances`.
2. **Start with one compartment** (formulas in `references/pk-formulas.md`): k = CL/V and t½ = ln 2 / k. IV bolus with
   `python3 scripts/pk.py iv --dose --V --CL --t`; oral dosing with first-order absorption (Bateman function) with
   `python3 scripts/pk.py oral --dose --F --V --CL --ka --t`, which also gives tmax and Cmax.
3. **Compute exposure from data** with `python3 scripts/pk.py auc DATA.csv [--log-down]`: linear trapezoids while
   concentrations rise, log trapezoids while they fall if `--log-down` is set, plus extrapolation to infinity.
4. **Repeated dosing** with `python3 scripts/pk.py repeat --dose --F --V --CL --tau`: accumulation ratio 1/(1 - e^(-kτ)) and the
   average steady-state concentration F·Dose/(CL·τ).
5. **Check whether one compartment is enough:** a log-concentration plot that bends after IV dosing means
   distribution; compare one- and two-compartment fits with AICc (`parameter-estimation-model-selection`).
6. **Add PD:** `python3 scripts/pk.py emax --C --E0 --Emax --EC50 [--n]`. If effect lags concentration (hysteresis loop in an
   effect–concentration plot), add an effect compartment or an indirect-response model.
7. **Link to mechanism:** use the PK concentration as the input to the network model of the target pathway
   (`ode-dynamics`), and state the tissue concentration assumption.

## Decision framework

| Situation | Model |
|---|---|
| Mono-exponential decline after IV | One compartment |
| Bi-exponential decline | Two compartments |
| Dose-dependent half-life | Saturable (Michaelis–Menten) elimination |
| Predicting across species, organs, or special populations | PBPK |
| Mechanism of action matters for dose selection | QSP: PK linked to a pathway model |
| Variation between patients is the question | Population (nonlinear mixed-effects) PK: VERIFY tools |
| Effect delayed relative to concentration | Effect compartment or indirect response |

## Failure and edge cases

- **Units:** mg/L against ng/mL (a factor of 1000), hours against minutes.
- **Flip-flop kinetics:** when absorption is slower than elimination, the terminal slope reflects ka, not k.
- **AUC extrapolated** from too few terminal points or with a large extrapolated share (report the percentage).
- **Linear kinetics assumed** for a drug with saturable metabolism.
- **Plasma concentration taken as target-site concentration** without justification.
- **PD fitted without checking for hysteresis.**

## Validation

- `python3 scripts/pk.py --selftest` passes.
- Simulated AUC from the model equals F·Dose/CL for linear kinetics.
- The extrapolated share of AUC to infinity is reported and small (a common rule of thumb is below 20 percent: VERIFY your guideline).
- Model-predicted concentrations at observed times fall within the measured variability.
- Falsifier: concentrations after a different dose that do not scale with the dose, contradicting linearity.

## Expected output

The model and its assumptions; parameters with units and sources; concentration–time predictions; AUC,
Cmax, tmax and half-life; accumulation for repeated dosing; PD parameters; and the link to any mechanistic
model.

## Sources and confidence

- Sauter and Albrecht 2023, doi:10.11647/OBP.0291 (supplied text): the systems medicine figure names network
  and PKPD modelling and simulation; one author works in quantitative systems pharmacology. The checklist
  does not list PK topics, so this skill is not book-anchored
- One-compartment, Bateman, AUC and Emax formulas: standard pharmacokinetics, author knowledge, VERIFY against
  a pharmacokinetics text and the relevant regulatory guidance
