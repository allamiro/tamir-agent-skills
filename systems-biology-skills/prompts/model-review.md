# `model-review` prompts

Audit a model or modelling paper layer by layer and rank what threatens its conclusions.

- **Give it:** the model (equations, file or paper), its question and claims, the data used to build, fit and
  test it, the code if available, and the purpose of the review
- **Skill file:** [`skills/model-review/SKILL.md`](../skills/model-review/SKILL.md)
- **Review dimensions:** [`review-dimensions.md`](../skills/model-review/references/review-dimensions.md)
- **Review form:** [`review-form.md`](../skills/model-review/assets/templates/review-form.md)

## 1. Referee a modelling paper

> Review this model as a referee: an ODE model of a metabolic pathway, 30 parameters, fitted to one time course, claims to explain why a mutant accumulates an intermediate. Parameters are in a table without units. No model file is provided.

A good answer: ranked major findings. The fit is presented as an explanation without validation on
independent data. Identifiability is doubtful with 30 parameters and one time course. Parameters have
no units, so units and balances cannot be checked. Without a model file the model cannot be rebuilt. For
each it gives what would resolve it, then minor points, a verdict and the reviewer's confidence.

## 2. Ready to publish?

> Is my model ready to publish? Here is the model file and the draft: <attach>.

A good answer: goes through the 12 dimensions, recomputes at least one quantity (units, a balance or a
steady state), attempts a rebuild from the files, and gives a fix list ordered by impact.

## 3. Is the conclusion justified

> The paper concludes that negative feedback causes drug resistance because removing the feedback in the model abolishes resistance. Is that justified?

A good answer: only partly. The model shows the feedback is sufficient within its assumptions. Necessity
needs alternative models without the feedback to fail to fit, sensitivity to the feedback parameters, and
ideally an experimental test of a prediction. The wording should be "the model suggests".

## 4. Measurement problem

> The model is fitted to a reporter that the authors call "pathway activity". What should a reviewer ask?

A good answer: ask for validity evidence for the readout: that it responds to the pathway and not to
confounders, its dynamic range and reliability, and its relation to an independent measure. If the
conclusion rests on the readout, this is a major point.

## 5. Keep the review fair

> I disagree with the authors' choice of a Boolean model; I would have used ODEs. Should I ask them to change it?

A good answer: only if the Boolean model cannot answer their question. Judge the paper they wrote. Ask
whether the conclusions depend on the update scheme, whether attractors were checked under asynchronous
updating, and whether the claims stay qualitative. Suggesting ODEs as an optional extension is fine.
