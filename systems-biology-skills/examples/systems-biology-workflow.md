# `systems-biology-workflow`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> I want to model the glycolysis pathway in yeast. I have the reaction list and measured uptake and secretion rates, but no kinetic parameters. Which kind of model should I build first, and what should my project plan look like?

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 2,192 | 2,134 |
| Input tokens read across all turns (including cached context) | 30,382 | 75,238 |
| Extra input tokens when the skill is installed | | +44,856 |
| Cost, US dollars at list price | 0.103 | 0.177 |
| Skills invoked in the sample run | none | `systems-biology-workflow` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 240 tokens for its name and description, which are in every session where the skill is installed, and about 2,100 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
**Build a stoichiometric model first and run metabolic flux analysis (MFA) on it.** Then add flux balance analysis (FBA) with flux variability analysis (FVA) if the network still has unresolved freedom. Build a kinetic ODE model only if your question is about time courses, stability or regulation, and only once you have a source for its parameters.

## Why stoichiometric first

- **It fits your data.** A reaction list plus uptake and secretion rates is exactly the input MFA needs. At steady state, S·v = 0. Your measured exchange fluxes (glucose in; ethanol, glycerol, CO₂, maybe acetate, pyruvate or succinate out) fix some entries of v, and linear algebra gives the rest. It needs no kinetic parameters.
- **An ODE model would be poorly posed now.** Yeast glycolysis has about 12–15 enzymes with 3–6 parameters each, so 40 to 80 unknowns. Steady-state exchange rates can't identify them: many parameter sets give the same fluxes.
- **It gives you the scaffold for any kinetic model later.** Kinetic models need a balanced network and a consistent steady-state flux distribution. The MFA solution is that reference state.

## Project plan

**0. State the question as something you can measure.** For example: "What is the intracellular flux split between ethanol and glycerol at steady state, and is it consistent with redox balance?" Or: "How does deleting gene X change ethanol yield?" The question decides how far down this list you need to go.

**1. Network and boundary.**
- Write the stoichiometric matrix S, including the cofactors ATP/ADP/AMP, NAD⁺/NADH and Pi.
- Decide the boundary: the cytosol only, or mitochondria too. Decide whether glycerol, trehalose/glycogen, acetate and pyruvate decarboxylase/alcohol dehydrogenase (PDC/ADH) are inside.
- Check element and charge balance for every reaction.
- Convert all rates to one unit, such as mmol gDW⁻¹ h⁻¹.

**2. Structural analysis (no data needed).**
- Rank of S and the degrees of freedom: the number of reactions minus the rank.
- Left null space: these are the conserved moieties, such as the adenylate total and NAD(H) total.
- Elementary flux modes: the possible routes from glucose to ethanol, glycerol and CO₂.
- Check that the redox balance closes. Glycerol production is how yeast reoxidises surplus NADH, so the network should show that.

**3. Metabolic flux analysis.**
- Plug in the measured exchange rates and classify the system as determined, underdetermined or redundant.
- If it is redundant, use the extra measurements to check consistency. A carbon balance of about 100% recovery is the key test that your measurements are sound.
- If it is underdetermined, note which fluxes stay free.

**4. FBA and FVA, if freedom remains.**
- Set bounds from your measurements.
- Use FVA to get the range of every flux, rather than reporting one optimum as if it were unique.
- Optionally simulate gene or reaction knockouts.
- For context, check your results against a genome-scale yeast model such as Yeast8 or yeast-GEM.

[... excerpt ends; the full answer is longer]
````

## Answer without the skill (excerpt)

````text
## Recommendation: start with a constraint-based (stoichiometric) model

With a reaction list and measured exchange fluxes but no kinetic parameters, build a **stoichiometric model** and analyze it with **metabolic flux analysis (MFA)** and **flux balance / flux variability analysis (FBA/FVA)**. Here's why:

- **It only needs what you have.** It uses the stoichiometric matrix S, the steady-state assumption S·v = 0, and bounds on fluxes. Your uptake and secretion rates become those bounds or fixed values.
- **Glycolysis is small and nearly linear.** With glucose uptake plus ethanol, glycerol, CO₂ and maybe acetate/pyruvate secretion measured, the system is often close to **fully determined or overdetermined**. Classical MFA (least squares on measured fluxes) then gives you internal fluxes directly, and you may not need an FBA objective at all.
- **It tests your data.** Redundant measurements let you check carbon, redox (NADH) and ATP balances. A balance that doesn't close points to a missing reaction or a measurement error before you've invested in kinetics.
- **It sets up a kinetic model later.** Kinetic models are much easier to fit when you already have a consistent steady-state flux distribution to anchor them.

A kinetic (ODE) model first would mean guessing dozens of Vmax/Km values from rates that only describe one steady state. Those parameters would be badly underdetermined.

## Project plan

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
