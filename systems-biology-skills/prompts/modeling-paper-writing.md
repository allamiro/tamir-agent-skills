# `modeling-paper-writing` prompts

Write, submit and revise a paper built on a model, from choosing the journal to answering reviewers.

- **Give it:** the question, main result and evidence; the model (equations or file, assumptions, parameters,
  code); the figures; the target journal and its instructions; the authors; and, for revisions, the reviews
- **Skill file:** [`skills/modeling-paper-writing/SKILL.md`](../skills/modeling-paper-writing/SKILL.md)
- **Manuscript craft, from decision to proofs:** [`manuscript-craft.md`](../skills/modeling-paper-writing/references/manuscript-craft.md)
- **Outline and claims ledger:** [`model-paper-outline.md`](../skills/modeling-paper-writing/assets/templates/model-paper-outline.md)
- **Cover letter and response:** [`review-response.md`](../skills/modeling-paper-writing/assets/templates/review-response.md)

## 1. Outline and model description

> Outline my systems biology paper and write the methods section describing my ODE model of insulin signalling (12 species, 20 parameters, 8 fitted to Western blots, the rest from the literature).

A good answer: starts from the journal and audience, then gives the claims ledger and the section jobs. The
model description lets others rebuild the model: diagram, all equations with units, assumption list, a
parameter table with value, unit, source and status (8 fitted, 12 from the literature with references),
initial conditions, solver and tolerances, fitting procedure and identifiability, and the SBML and code
with a permanent identifier, as MIASE asks.

## 2. Which journal first

> I have a model that predicts a new drug combination and one validation experiment. Which journal should I submit to, and how does that change how I write the paper?

A good answer: choose the journal before writing, because the audience decides the emphasis: a
computational journal for the method, a biology or pharmacology journal for the prediction and its test,
or a clinical journal only with careful limits. Read the instructions for authors, aim high but
realistically, and plan the next journal in case of rejection.

## 3. Write the abstract

> Write the abstract for my paper. Here are the results: <paste>.

A good answer: written last, in the journal's format (structured or single paragraph, word limit), after
reading several abstracts from that journal. It states the question, approach, main finding with its
evidence level, and the main limitation, with no claim that is not in the paper.

## 4. Respond to reviewers

> Respond to these reviewer comments. Reviewer 2 says my model was only fitted, never validated, and that one parameter is not identifiable.

A good answer: a point-by-point response. It concedes the validation point and adds a prediction of
held-out or new data, or narrows the claim. It shows a profile likelihood and reports the identifiable
combination or the range for the parameter. Each change is given with its page and line, the reviewer is
thanked where the paper improved, and no new claims are added.

## 5. Rejected

> My modelling paper was rejected. What now?

A good answer: rejection is common and not final. Take the constructive comments, revise, agree the next
journal with the co-authors, and resubmit with a new cover letter. If several journals reject it for the
same reason, reconsider whether the paper is ready, for example by adding a validation experiment.
