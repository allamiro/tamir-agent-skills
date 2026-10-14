---
name: model-review
description: Audits a systems biology model or modelling paper, as a reviewer, supervisor or before submission, covering whether the question fits the formalism, assumptions, units and balances, conservation, parameter tables, sources and identifiability, numerical correctness, validation on independent data, sensitivity and robustness, alternative models, measurement validity of the data, reproducibility from the model files, and whether claims stay within the evidence. Use for "review this model", "referee this systems biology paper or ODE model", "is my model ready to publish", "what would a reviewer criticise", "check my model for errors", "audit this SBML model", "is this conclusion justified by the model". Use systems-biology-literature to find related models, modeling-paper-writing to fix the write-up, and the formalism skills to redo an analysis.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# Model review

## Purpose and activation

A model can be mathematically correct and still answer the wrong question, rest on unidentifiable
parameters, or be impossible to rebuild. A structured review checks each layer in turn, ranks the
findings by how much they threaten the conclusions, and says what would fix each. Activate when the user
asks for a review of a model, a modelling paper, a thesis chapter, or their own work before submission.

## Required inputs

The model (equations, file, or paper); its question and claims; the data used to build, fit and test it;
the code or model file, if available; and the review's purpose (journal review, supervision, self-check)
and any review form.

## Workflow

1. **Restate the question and the main claim** in your own words; if you cannot, that is the first finding.
2. **Run the checks in order** using `assets/templates/review-form.md` and the details in
   `references/review-dimensions.md`: question and formalism; assumptions; units, balances and conservation;
   parameters; numerics; fitting and identifiability; validation; sensitivity; alternatives; data and
   measurement; reproducibility; claims.
3. **Recompute what you can:** units with `quantities-units-balances`, balances with `systems-biology-programming`,
   a steady state or simulation with `ode-dynamics`, a flux optimum with `flux-balance-analysis`.
4. **Try to rebuild the model** from the paper and files and reproduce one main figure; report what was missing.
5. **Rank findings:** major (threatens the main claim), minor (weakens a secondary point or the clarity),
   and suggestions. For each, give the location, the problem, why it matters and what would resolve it.
6. **Write the verdict** with your confidence and the parts outside your expertise.
7. **Keep it about the work:** judge the paper the authors wrote, not the one you would have written, and keep
   a confidential manuscript out of external tools unless the venue's policy allows it.

## Decision framework

| Finding | Usually | What resolves it |
|---|---|---|
| Fit presented as validation | Major | Prediction of data not used for fitting |
| Key parameter unidentifiable, conclusion depends on it | Major | Profile likelihood, new data, or weakened claim |
| Unbalanced reactions or unit error in the main model | Major | Correction and rerun |
| Model cannot be rebuilt (missing equations or parameters) | Major for publication | Complete description and files |
| Alternative model not considered that fits equally well | Major if it changes the mechanism claimed | Comparison with AICc or a discriminating experiment |
| Readout's validity not shown | Major if the conclusion rests on it | Validity evidence (`quantitative-research-methods`) |
| Solver settings not reported | Minor unless results change with them | Report and test |
| Unclear figure | Minor | Redraw |

## Failure and edge cases

- **Reviewing the biology only** and missing a unit or balance error, or the reverse.
- **Not trying to rebuild the model,** so missing parameters go unnoticed.
- **Demanding a different formalism** when the chosen one answers the question.
- **Vague findings** ("needs more validation") without saying which data would do.
- **Missing the dependence of the main claim on one assumption.**
- **A confidential manuscript pasted into an external tool** against the venue's rules.

## Validation

- Every major finding names its location, why it threatens the claim and what would resolve it.
- At least one quantity (unit, balance, steady state or figure) was recomputed independently.
- The rebuild attempt is reported with what was missing.
- Falsifier: the authors resolve every major finding and the main claim still fails a test you proposed.

## Expected output

A summary of the question and claims; ranked findings with locations and remedies; the rebuild report;
recomputed checks; a verdict with confidence; and, for self-review, a fix list ordered by impact.

## Sources and confidence

- Review dimensions combine the topics of the Sauter and Albrecht checklist (assumptions, units, balances,
  sensitivity, AIC; doi:10.11647/OBP.0291, supplied text) with reproducibility standards (MIASE,
  doi:10.1371/journal.pcbi.1001122; MIRIAM, doi:10.1038/nbt1156) and the measurement-validity and
  interpretation points of Teo (Ed.) 2013, doi:10.1007/978-94-6209-404-8 (supplied foreword and chapter 1,
  paraphrased)
- The review procedure and severity ranking: author knowledge, VERIFY against the venue's reviewer guidance
