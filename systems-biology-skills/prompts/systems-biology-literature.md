# `systems-biology-literature` prompts

Find papers, models and parameters, read modelling papers critically, and check references so none are invented.

- **Give it:** the topic (pathway, organism, formalism), what the literature is for, the date range, and any
  references already in hand
- **Skill file:** [`skills/systems-biology-literature/SKILL.md`](../skills/systems-biology-literature/SKILL.md)
- **Reading checklist:** [`reading-checklist.md`](../skills/systems-biology-literature/references/reading-checklist.md)
- **Source record template:** [`source-record.md`](../skills/systems-biology-literature/assets/templates/source-record.md)

## 1. Is there a published model

> Find papers on modelling the circadian clock in mammals, and tell me whether there is a published model I can reuse and where to get kinetic parameters.

A good answer: runs the search if it has web access and logs the queries, databases and date; without web
access it says so and gives the queries and databases to run. It points to BioModels and the papers'
supplements and code for models, and to parameter sources (BRENDA and SABIO-RK where enzyme kinetics apply,
otherwise the papers' fitted parameter tables) with organism and conditions recorded. Every reference it
could not open is marked as recalled and unverified rather than presented as a checked citation, and it says
to confirm that a reused model reproduces a figure of its paper before changing it.

## 2. Check my reference list

> Check my reference list for invented citations. One entry is: Nobody N (2019). A new result. J Imaginary Biol 5:1-9. doi:10.1000/imaginary.2019.1

A good answer: runs the reference checker. The DOI is syntactically valid but should be resolved online,
where a DOI that does not exist is the strongest sign of an invented reference. A pass only shows the
record matches the line, not that the paper says what is cited.

## 3. Read a modelling paper

> Read this modelling paper and tell me whether the model is any good: <paste or attach>.

A good answer: goes through the checklist: question, formalism, assumptions, equations with units,
parameter sources, fitting and identifiability, validation on independent data, sensitivity,
alternatives, model availability, and claims within the evidence. It ranks the problems and says what
it could not check.

## 4. Parameters from databases

> I found a Km of 0.2 mM for my enzyme in a database. Can I use it in my model?

A good answer: only after checking the primary source, the organism, pH, temperature, assay and whether the
value was measured in vitro. Record these, and test the model's sensitivity to the value because in vivo
conditions may differ.

## 5. Related work

> Help me write the related work section comparing my model with earlier models of the same pathway.

A good answer: a comparison by question rather than a list of papers: for each earlier model, the
formalism, scope, data, assumptions and validation, where they agree and differ and why. Every reference is
checked and marked read, seen or recalled.
