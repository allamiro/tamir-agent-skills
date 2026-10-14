# `modeling-research-planning` prompts

Plan research that runs the model–experiment cycle on purpose, with measurement and analysis decided before data collection.

- **Give it:** the question, prior models and data, methods and budget, the team's skills, time frame,
  funder rules, and ethical or data constraints
- **Skill file:** [`skills/modeling-research-planning/SKILL.md`](../skills/modeling-research-planning/SKILL.md)
- **Planning checklist:** [`planning-checklist.md`](../skills/modeling-research-planning/references/planning-checklist.md)
- **Proposal plan template:** [`proposal-plan.md`](../skills/modeling-research-planning/assets/templates/proposal-plan.md)

## 1. Aims for a modelling grant

> Write the aims for my modelling grant on how feedback in the MAPK pathway shapes drug resistance, with experiments to test the model.

A good answer: a falsifiable hypothesis and aims that each pair a modelling task with an experiment.
Each aim names its measurement, analysis, risk with alternative, and deliverable, and the aims are not
chained so that one failure stops all. It plans at least two rounds of the model–experiment cycle and
says what result would refute the hypothesis.

## 2. Which data do I need

> Which data do I need to fit my model of a three-step signalling cascade with 9 parameters, and how many time points should I measure?

A good answer: check structural identifiability first. Choose observables so that the needed states are
observable, perturbations that separate rival models, and time points that cover fast and slow dynamics.
Decide replicates by simulating the planned design with realistic noise and checking whether the
parameters are recovered.

## 3. Check my plan

> Check my proposal plan for missing pieces: <paste plan in the template format>.

A good answer: runs the plan checker and lists every missing or empty field per aim (hypothesis, modelling
task, experiment, measurement, analysis, risk, alternative, deliverable, dependencies). It also warns if
every aim depends on the previous one.

## 4. New readout

> Our whole project depends on a new reporter as a readout of pathway activity. What should we plan before the main experiments?

A good answer: a pilot that gathers validity evidence: that the reporter responds to the pathway and not
to cell size or stress, its dynamic range and reliability, and how it relates to an independent
functional readout. Decide scoring and missing-data rules before the main study, following the
measurement planning in `quantitative-research-methods`.

## 5. Interdisciplinary team

> My team has two biologists and one mathematician and we keep misunderstanding each other. How do I plan around that?

A good answer: name the different habits of thought (biologists often work on inverse problems from
observations, engineers build forward from parts, computer scientists automate). Agree a shared glossary
and model diagram, hold joint sessions where each explains their part, and plan training. Pair each aim's
modelling and experimental tasks so the two people work together.
