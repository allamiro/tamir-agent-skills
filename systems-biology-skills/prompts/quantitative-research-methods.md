# `quantitative-research-methods` prompts

Make the argument that a score or readout measures what you intend, choose an analysis that fits the
design, and interpret it with its consequences in view.

- **Give it:** the construct or property, the population, the items or readouts and how they are scored, the
  design, the intended use of the scores, and the data if collected
- **Skill file:** [`skills/quantitative-research-methods/SKILL.md`](../skills/quantitative-research-methods/SKILL.md)
- **Construct modelling:** [`construct-modelling.md`](../skills/quantitative-research-methods/references/construct-modelling.md)
- **Validity evidence:** [`validity-evidence.md`](../skills/quantitative-research-methods/references/validity-evidence.md)
- **Measurement plan template:** [`measurement-plan.md`](../skills/quantitative-research-methods/assets/templates/measurement-plan.md)

## 1. Is my score reliable and valid

> Compute Cronbach's alpha for my 4-item quiz on steady-state concepts (items scored 0 or 1): i1,i2,i3,i4 rows 1,1,0,1; 1,0,0,0; 1,1,1,1; 0,0,0,0; 1,1,1,0; 1,0,1,1; 0,1,0,0; 1,1,1,1. Is the quiz measuring understanding of steady state?

A good answer: alpha ≈ 0.71 on 8 respondents. Item i2 has the weakest item-rest correlation (about 0.27), and
dropping it would raise alpha to about 0.78, so it should be checked. Alpha is not validity evidence, and
with 8 respondents it is very uncertain. A validity argument needs a construct map of levels of
understanding, items mapped to it, think-aloud evidence that students answer for the intended reasons, and
relations to other measures.

## 2. Design a scoring rubric

> Help me design a scoring rubric for students' written explanations of feedback loops, using a construct map.

A good answer: a construct map from misconception to expert, for example 0 confusing feedback with
feed-forward, 1 naming the loop, 2 tracing signs, 3 predicting behaviour, and 4 explaining when the
prediction fails. Items target each level. The outcome space is finite, exhaustive and ordered, with
exemplars and rater training, plus a rule for missing or off-topic answers. Pilot with think-alouds and
check inter-rater agreement.

## 3. Effect size

> Two groups of students scored 5.1, 4.8, 5.6, 5.0, 5.3 (flipped classroom) and 4.2, 4.6, 4.0, 4.4, 4.3 (lecture). How big is the effect?

A good answer: Cohen's d ≈ 3.2 and Hedges' g ≈ 2.9, with a wide approximate interval of about 1.1 to 4.7
because n = 5 per group. The effect is very large but very uncertain. Students nested in one class each
cannot separate the method from the class or teacher, and Cohen's conventional thresholds should not be
applied without context.

## 4. Reflective or formative

> I combine income, education and occupation into a socio-economic index and my alpha is only 0.4. Is my index bad?

A good answer: no. This is a formative index: the indicators define the construct rather than being caused by
it, so they need not correlate and alpha is the wrong statistic. Its validity rests on the theoretical
justification for the indicators and weights and on relations to other variables.

## 5. Which statistical method

> I measured students' modelling skill before and after a course in 12 classes, with 25 students per class. Which analysis should I use, and how do I handle students who missed the post-test?

A good answer: a multilevel longitudinal model, with time nested in students nested in classes. Analysing
students as independent ignores the clustering and overstates precision. Missing post-tests need a
stated mechanism: ask why they are missing, use methods valid under missing at random (multiple
imputation or full-information maximum likelihood), and run a sensitivity analysis if dropout may relate
to skill.
