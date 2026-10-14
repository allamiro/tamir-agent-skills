# `modeling-paper-writing`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> Outline my systems biology paper and write the methods section describing my ODE model of insulin signalling (12 species, 20 parameters, 8 fitted to Western blots, the rest from the literature).

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 6,739 | 6,765 |
| Input tokens read across all turns (including cached context) | 97,506 | 159,463 |
| Extra input tokens when the skill is installed | | +61,956 |
| Cost, US dollars at list price | 0.256 | 0.335 |
| Skills invoked in the sample run | none | `modeling-paper-writing` |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 340 tokens for its name and description, which are in every session where the skill is installed, and about 2,000 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
I've written a paper outline and a draft Methods section in `insulin_model_paper_draft.md`. You didn't give me your equations, species list, cell line, solver or fitting details, so everything model-specific is a `[placeholder]`. Where I had to assume something, it's marked **[CONFIRM]**. I didn't make up any references.

**The outline:**
- **Journal choice comes first.** If your main result is about the biology, aim for a biology journal and put the full model in the supplement. If it's about the modelling method, aim for a computational journal.
- **Claims table:** each claim is linked to its figure, the script that produced it, and how strong the evidence is. The wording matches the strength: "reproduces" for something fitted, "predicted…, which we confirmed" for a prediction you tested, "predicts" for one you haven't tested yet.
- **Results are written as questions:** does the model fit the data, can the fitted parameters be pinned down, does it predict data it wasn't fitted to, which parameters matter most, and do alternative versions of the model fit as well?
- **The introduction ends with your question and hypothesis.** The discussion covers limitations and the next experiment that could prove the model wrong.

**The Methods (2.1–2.8):**
1. The model's structure and its 12 species, plus seven explicit assumptions.
2. A parameter table with 20 rows (12 from the literature, 8 fitted). Each row has a unit, a source, and for literature values the organism or cell type they came from.
3. The Western blot data, and how the model's values are scaled to the blots' arbitrary units.
4. The fitting method: weighted least squares from many random starting points, plus checks on whether each fitted parameter is well determined.
5. Testing the model on held-out data, and comparing alternative models by AIC/BIC.
6. Sensitivity analysis.
7. Solver, tolerances and software versions.
8. Data and code availability: the model as an SBML file in BioModels, with the code archived on Zenodo.

**Three things a reviewer is likely to raise:**
- **Scaling factors are extra fitted parameters.** If you fitted scaling factors to match the model to the blots' arbitrary units, you actually fitted more than 8 parameters. Report them, and count them in AIC/BIC.
- **Fits alone aren't validation.** If the paper only shows the model fitted to the blots it was trained on, it hasn't been validated. You need at least one prediction tested on data held out from fitting, or the claim has to be worded as "the model predicts".
- **Literature values from other systems.** Some of your 12 literature parameters probably come from other cell types or from test-tube measurements. The sensitivity analysis should show whether your conclusions depend on them.

If you send me the equations or model file, the list of species and parameters with their values, and your experimental details, I'll fill in the placeholders, write out Table 1 in full, and draft the Results.
````

## Answer without the skill (excerpt)

````text
I've written the outline and a full draft Methods section to `manuscript_draft.md`. Your working directory was empty, so I didn't have your model files or data. I wrote the draft around the numbers you gave me (12 species, 20 parameters, 8 fitted to Western blots, 12 from the literature) and left placeholders in **[brackets]** for everything else.

**The outline** follows a standard paper structure:
- **Abstract**
- **Introduction:** the biology, why it matters clinically, earlier models (Sedaghat, Brännmark, Nyman, Kubota), the gap your paper fills.
- **Methods:** nine subsections, drafted in full.
- **Results:** calibration, identifiability, validation, sensitivity, predictions.
- **Discussion**
- **Figures and tables:** six suggested figures and two tables.

**The Methods section has nine subsections:**
1. Model structure and assumptions.
2. Equations and how the starting (basal) state is set.
3. How the parameters were split: 12 fixed from the literature, 8 estimated, with the reason for each.
4. The Western blot experiments and how the band intensities were normalised.
5. How the 8 parameters were fitted. Because blot data are relative, each readout gets a scaling factor.
6. Which parameters the data can actually pin down, with confidence intervals.
7. Sensitivity analysis, including a test of how much the results depend on the 12 literature values.
8. Validation against data that wasn't used for fitting.
9. Software and reproducibility (SBML model file, PEtab, BioModels).

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
