# `method-benchmarking` prompts

Design a comparison of computational methods that can fail, or audit one. The skill covers methods,
datasets and truth, fair tuning, metrics, leakage, failures, and uncertainty across datasets, and it
computes the sizes and tests that decide whether a gain is real.

- **Give it:** the decision, the methods and versions, the datasets and how truth is known, the metric
  candidates, and who is running the comparison
- **Skill file:** [`skills/method-benchmarking/SKILL.md`](../skills/method-benchmarking/SKILL.md)
- **Checklist it follows:** [`checklist.md`](../skills/method-benchmarking/references/checklist.md)
- **Template it fills:** [`benchmark-plan.md`](../skills/method-benchmarking/assets/templates/benchmark-plan.md)
- **Find existing benchmarks with:** [`literature-search-appraisal`](literature-search-appraisal.md) · **Model-level splits:** [`machine-learning-biology`](machine-learning-biology.md)

## 1. Is a gain real

> A new variant caller scores 0.83 accuracy against 0.81 for the established one on my 200-item test set. Is that a real improvement? Tell me what the test could detect at all and what I would need.

A good answer: the smallest difference detectable with 200 items, about 11 points at 80% accuracy and
80% power for separate test sets, so 2 points is within noise; the effect of pairing the same items; and a
McNemar test on the discordant items.

## 2. The winner's curse

> I compared ten tools on one 200-item test set and the best scored 0.83 while the rest were near 0.80. How much of that lead could be luck if all ten were equally good?

A good answer: a simulation or calculation showing that the best of ten equal methods on 200 items looks
about 4 points above the truth on average, so a lead of 3 points over the rest is expected by chance.

## 3. Design a benchmark

> Design a benchmark of five read aligners for our bacterial isolates. Give me methods, datasets and how truth is known, tuning rules, the primary metric, how failures count, and the controls that show the harness works.

A good answer: inclusion rules and versions, a mix of simulated data and data with trusted truth, equal
tuning on separate data, a primary metric fixed in advance, failures counted, and a degraded copy that
must rank last with a duplicate that must tie.

## 4. Audit a comparison

> Review the comparison in this paper: <paste methods and results>. Who tuned what, could the simulator favour the new method, and are failed runs counted? Give me findings ranked critical, major or minor.

A good answer: ranked findings tied to the checklist, the self-assessment trap named, questions on
datasets chosen and parameters tuned, and what evidence would settle each.

## 5. Across datasets

> Method A beats method B on 7 of 9 datasets. Here is the table: <paste dataset, method, score>. Is A better, and how sure can I be?

A good answer: paired differences, an interval over datasets, an exact sign test near 0.18 (7 wins out of 9
is not enough for 0.05), a note that nine datasets give a limited test, and no claim of "best" where the
interval includes zero.

## 6. Which metric

> My positives are 1 in 500. Which metrics should the benchmark use, and which would mislead?

A good answer: precision-recall based measures as primary for rare positives, the reason ROC curves can
look good when the positives are rare, the count of failures reported, and the metric and threshold fixed
before the run.
