---
name: modeling-research-planning
description: Plans systems biology research and writes proposals, covering the research question and hypothesis, aims that combine modelling and experiments, the iterative model-experiment cycle, experimental design for model discrimination and parameter identifiability, measurement and sample-size reasoning, data management and provenance, risk and alternatives, timelines, ethics and team skills across biology, mathematics and computing. Use for "plan my systems biology project", "write the aims for my modelling grant", "design experiments to test my model", "which data do I need to fit this model", "how many time points should I measure", "data management plan for my modelling project", "risks in my proposal". Use systems-biology-workflow to pick the formalism, quantitative-research-methods for measurement and statistics, and modeling-paper-writing once results exist.
license: Apache-2.0
metadata:
  library: systems-biology-skills
  version: "1.0"
---

# Modelling research planning

## Purpose and activation

Systems biology projects fail most often at the joints: models built without the data to constrain them,
experiments done without asking what the model needs, and teams whose biologists and modellers talk past
each other. A plan that runs the model–experiment cycle on purpose, with measurement and analysis decided
before data collection, avoids that. Activate when the user plans a project, writes a proposal or thesis
plan, or designs experiments to inform a model.

## Required inputs

The question and why it matters; prior models and data; the formalism, if chosen; available methods and
budget; the team's skills; time frame; the funder's or programme's rules; and any ethical or data-sharing
constraints (patients, animals, human data).

## Workflow

1. **State the question and a falsifiable hypothesis,** and what result would change practice or belief.
2. **Write aims** that each pair a modelling task with an experimental one, and say what each aim's result
   feeds into the next (`assets/templates/proposal-plan.md`).
3. **Plan the model–experiment cycle:** build a first model from existing data, use it to choose the most
   informative experiment, measure, refit, and repeat. Budget at least two rounds.
4. **Design experiments for the model's needs:** which states must be observed (observability,
   `control-systems-feedback`), which perturbations separate rival models, which time points capture the fast
   and slow dynamics, and how many replicates give the precision the fit needs.
5. **Plan measurement** with `quantitative-research-methods`: define each construct or readout, its outcome
   space and scoring, its reliability and validity evidence, the missing-data rule, and the analysis method,
   all before collecting data.
6. **Reason about sample size** from the effect size or parameter precision required; for time courses, from
   an identifiability analysis on simulated data with realistic noise.
7. **Plan data and provenance:** formats, metadata, versioning, model files (SBML, SED-ML), repositories, and
   provenance records for integrated data (`references/planning-checklist.md`).
8. **List risks and alternatives** for each aim (the model may be unidentifiable, the experiment may fail, the
   hypothesis may be false), with what you will do in each case.
9. **Make the timeline** with dependencies, and run `python3 scripts/plancheck.py PLAN.md` to check that every aim has
   a hypothesis, a measurement, an analysis, a risk and a deliverable.

## Decision framework

| Situation | Plan |
|---|---|
| Several mechanisms are plausible | Design the experiment that maximises the difference between their predictions |
| Parameters unidentifiable from planned data | Add an observable, a perturbation, or more time points; check on simulated data |
| Expensive measurements | Use the model to choose the few most informative conditions |
| New readout or score | Pilot it and gather validity evidence before the main study |
| Patient or animal data | Ethics approval, data protection and minimisation planned first |
| Team lacks a skill | Collaborator, training plan, or a lighter formalism |

## Failure and edge cases

- **Aims that depend on each other in series,** so one failure stops the project.
- **A model planned for data that cannot constrain it.**
- **Analysis chosen after seeing the data.**
- **No validity evidence for a new readout** that the whole project depends on.
- **Sample size from habit,** not from the precision needed.
- **No plan for a negative result.**
- **Integration of data from many sources without provenance.**

## Validation

- `python3 scripts/plancheck.py --selftest` passes, and the plan passes `plancheck.py` with no missing fields.
- Each aim names its hypothesis, measurement, analysis, risk with alternative, and deliverable.
- A simulated dataset from the planned design, with realistic noise, recovers the key parameters.
- Falsifier: the result, stated in advance, that would refute the main hypothesis.

## Expected output

The question and hypothesis; aims with modelling and experimental parts; the model–experiment cycle; the
experimental and measurement design; sample-size reasoning; data and provenance plan; risks and
alternatives; timeline; and the plancheck report.

## Sources and confidence

- Sauter and Albrecht 2023, doi:10.11647/OBP.0291 (supplied text): the contrasting ways of thinking of
  biologists, engineers, physicists and computer scientists, and that recognising them helps avoid
  misunderstanding in interdisciplinary teams; the systems medicine call for reproducible workflows, data
  provenance and benchmark data (introduction, from Apweiler et al. 2018, doi:10.1038/emm.2017.290)
- Planning measurement and analysis before data collection, and defending interpretation with attention to
  method appropriateness, decisions, data quality and consequences: Teo (Ed.) 2013,
  doi:10.1007/978-94-6209-404-8, foreword and chapter 1 (supplied text, paraphrased)
- Experimental design for model discrimination and identifiability: author knowledge, consistent with Raue
  et al. 2009, doi:10.1093/bioinformatics/btp358 and Kirk, Thorne and Stumpf 2013,
  doi:10.1016/j.copbio.2013.03.012 (records checked 2026-10-15), VERIFY
