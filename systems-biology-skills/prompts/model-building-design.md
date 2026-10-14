# `model-building-design` prompts

Make a model's purpose, assumptions and structure explicit before solving anything.

- **Give it:** the purpose of the model, the system and boundary, what is known about the mechanism, the data
  and its resolution, and the formalism if chosen
- **Skill file:** [`skills/model-building-design/SKILL.md`](../skills/model-building-design/SKILL.md)
- **The modelling cycle:** [`modelling-cycle.md`](../skills/model-building-design/references/modelling-cycle.md)
- **Assumption register:** [`assumption-register.md`](../skills/model-building-design/assets/templates/assumption-register.md)

## 1. What does my model assume

> Here is my model: dS/dt = -Vmax*S/(Km+S), dP/dt = Vmax*S/(Km+S). What assumptions does it make, and is S a variable or a parameter? Classify every quantity and fill in an assumption register.

A good answer: S and P are state variables; Vmax and Km are parameters; the coefficient 1 in each term is a
stoichiometric coefficient. Assumptions include a well-mixed constant volume, constant temperature and enzyme
level, quasi-steady state of the enzyme–substrate complex with enzyme much scarcer than substrate, an
irreversible reaction with no product inhibition, and no other reactions. Each comes with how it could fail
and how to check, and the answer notes that S + P is conserved.

## 2. Classify the model

> Classify this model along every axis you can: a set of ODEs for 8 proteins with mass-action kinetics, fitted to Western blot time courses from a cell population.

A good answer: dynamic, continuous in time and state, deterministic, lumped (no space), nonlinear (mass action
with bimolecular terms), mechanistic, fitted to population averages. It says what each choice excludes:
cell-to-cell variation, spatial gradients, and low-copy noise.

## 3. Is the problem well posed

> I want to infer the full interaction network of 50 genes from 10 microarray samples. Is this a well-posed problem?

A good answer: no. With far more unknowns (thousands of possible interactions) than observations the
solution is not unique and depends strongly on noise, so the problem fails Hadamard's uniqueness and
stability conditions. Remedies: regularisation or sparsity assumptions, prior knowledge, perturbation data,
or a smaller question, each with its own assumptions stated.

## 4. Quasi-steady state

> Can I replace the enzyme-substrate complex in my model by the Michaelis-Menten expression? The enzyme concentration is 5 µM and the substrate 10 µM, Km is 2 µM.

A good answer: warns that the standard quasi-steady-state assumption needs enzyme much scarcer than substrate
(or than substrate plus Km). Here the enzyme is half the substrate concentration, so the approximation is
doubtful. It suggests keeping the complex explicitly, or the total quasi-steady-state (tight-binding) form,
and checking by simulating both.

## 5. Plan the test

> Before I fit my model of a bacterial stress response, how should I plan to test it so that I am not just checking the fit?

A good answer: hold back data (a different stress level, a mutant, or a time window) not used for fitting.
Write the prediction down before comparing, state what result would show the model wrong, and check
whether the parameters are identifiable from the fitting data.
