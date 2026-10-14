---
name: modeling-paper-writing
description: Plans, drafts and revises papers, theses and reports that present mathematical or computational models of biological systems, covering choosing the journal and audience, authorship, the title, introduction with an explicit question and hypothesis, a model description others can reproduce (equations, assumptions, parameters with sources, units, code and SBML availability), results figures for simulations and fits, discussion and limitations, the abstract, the cover letter, responding to reviewers, rejection and resubmission, and proofs. Use for "write the methods section for my model", "outline my systems biology paper", "how do I describe my ODE model", "write the abstract", "respond to these reviewer comments", "my paper was rejected, what now", "which journal should I submit my model to", "write a cover letter". Use model-review to audit the model first, systems-biology-literature for related work and reference checks, and systems-biology-programming for model files.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# Modelling paper writing

## Purpose and activation

A modelling paper must let a reader judge three things: whether the question matters, whether the
model's assumptions fit it, and whether someone else could rebuild the model and get the same results.
It also has to get through submission and review. This skill covers both the content (claims, model
description, evidence) and the craft (journal choice, authorship, section jobs, cover letter, responses).
Activate when the user is writing, revising, submitting or defending a paper, thesis chapter or report
built on a model.

## Required inputs

The question, the main result and the evidence for it; the model (equations or file, assumptions,
parameters with sources and units, code); the figures; the target journal or venue and its instructions;
the authors and their contributions; and, for revisions, the reviews and the editor's letter.

## Workflow

1. **Decide the journal and audience** before drafting, then read its instructions (`references/manuscript-craft.md`).
2. **Agree authorship** and record contributions (CRediT roles), and the plan for every author to approve the final text.
3. **Build the claims ledger** (`assets/templates/model-paper-outline.md`): each claim, the figure or table, the
   simulation or fit that produced it, and its evidence level (fitted, predicted and tested, predicted only).
4. **Write the model description so it can be rebuilt:** the network or diagram; every equation; every
   assumption (from `model-building-design`); a parameter table with value, unit, source and status (measured,
   fitted, assumed); initial conditions; solver and tolerances; and the SBML or CellML file and code with a
   permanent identifier (`systems-biology-programming`). MIASE lists what a simulation description needs.
5. **Write the results as questions answered:** fit to training data, prediction of held-out or new data,
   sensitivity, and alternative models compared (`parameter-estimation-model-selection`). Show each result once.
6. **Write the introduction** to end in the explicit question and hypothesis, and the **discussion** to say
   whether they were answered, how the result compares with earlier models and data, what the assumptions
   limit, and what experiment would test the model next.
7. **Check the references** with `systems-biology-literature`, then write the **abstract** last, and the **title**
   to state the main finding.
8. **Submit** with a cover letter and, after review, answer point by point (`assets/templates/review-response.md`).
9. **After rejection,** revise on the constructive points, choose the next journal with the co-authors, and resubmit.

## Decision framework

| Evidence for a claim | Wording |
|---|---|
| Model fitted to data | "The model is consistent with" or "reproduces" |
| Prediction tested on new data | "The model predicted ..., which we confirmed" |
| Prediction not yet tested | "The model predicts ...; this remains to be tested" |
| Parameter not identifiable | Do not report a single value; report the identifiable combination or the range |
| Mechanism inferred from fit | "Suggests", with the alternative models that fit equally well |
| Sensitivity shows a conclusion depends on an uncertain parameter | State the dependence in the abstract or discussion |

| Venue type | Emphasis |
|---|---|
| Methods or computational journal | Novelty and generality of the modelling approach, benchmarks |
| Biology journal | The biological insight and its experimental test; model in supplement with full detail |
| Clinical or translational journal | Implications for patients, with careful limits |
| Thesis | Full derivations, failed approaches and what they taught |

## Failure and edge cases

- **A model that cannot be rebuilt:** missing equations, parameters without units or sources, no model file.
- **Fit to training data presented as validation.**
- **Every result shown in text, table and figure.**
- **An introduction that never states the question.**
- **Discussion that ignores models or data that disagree.**
- **Authorship decided at submission,** causing disputes; or an author who never saw the final version.
- **A reviewer's point answered with rhetoric** rather than a change or evidence.
- **Unchecked references,** including invented ones.
- **Abstract claims stronger than the results.**

## Validation

- A colleague rebuilds the model from the methods and files alone and reproduces one main figure.
- Every claim maps to a ledger row with its evidence level, and the wording matches the level.
- Every parameter has a unit and a source or a fitting note; every reference passes the checker or is marked.
- The response letter addresses every reviewer point with a change or a reason.
- Falsifier: a number in the abstract that differs from the figure regenerated from the code.

## Expected output

The journal choice and outline; the claims ledger; drafted sections (model description, results,
introduction, discussion, abstract, title) with placeholders for missing numbers; the parameter table; the
data and code statement; a cover letter; and for revisions a point-by-point response.

## Sources and confidence

- Baker, "How to write your first paper", *Obstetrics, Gynaecology and Reproductive Medicine* 22(3):81–82,
  2012, doi:10.1016/j.ogrm.2011.12.003 (supplied text; record checked on Crossref 2026-10-15; © Elsevier, so
  paraphrased only): journal choice first, authorship early, section jobs, abstract last, cover letter,
  responses, rejection, proofs
- Waltemath et al. 2011, doi:10.1371/journal.pcbi.1001122 (MIASE); CRediT and ICMJE: author knowledge, VERIFY
  the venue's policy
- Wording ladder and model-description requirements: author knowledge, VERIFY against the target journal
