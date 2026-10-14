# `machine-learning-biology`: a sample answer

A real answer from a Claude Code session, with the numbers behind it. The prompt is the skill's starter prompt (the first one in its prompts file). The answers are excerpts of single runs picked to be typical in length; the token and cost figures are means over 3 runs with the skill and 3 without.

## Prompt

> My classifier gets 98% accuracy on a dataset where 2% of the examples are positive. Is that good? What should I report instead?

## Tokens

| | Without the skill | With the skill |
|---|---|---|
| Output tokens (what the model wrote, including its reasoning) | 891 | 1,032 |
| Input tokens read across all turns (including cached context) | 30,354 | 35,641 |
| Extra input tokens when the skill is installed | | +5,287 |
| Cost, US dollars at list price | 0.077 | 0.122 |
| Skills invoked in the sample run | none | none |

Size of the skill by Claude Code's own estimate (`claude plugin details`): about 230 tokens for its name and description, which are in every session where the skill is installed, and about 1,900 tokens when the skill is used and its instructions are loaded. The estimate is not a measurement.

## Answer with the skill (excerpt)

````text
**No, 98% accuracy tells you almost nothing here.** A model that always predicts "negative" also gets 98%, because 98% of your examples are negative. Your classifier might be finding no positives at all.

## What to report instead

**1. The confusion matrix.** Give the raw counts of true positives (TP), false positives (FP), false negatives (FN) and true negatives (TN) on the test set. Every other metric comes from these, and readers can check your numbers.

**2. Metrics that focus on the positive class:**

| Metric | Question it answers | Trivial "all negative" model gets |
|---|---|---|
| **Recall** (sensitivity) = TP/(TP+FN) | Of the real positives, how many did we find? | 0 |
| **Precision** (PPV) = TP/(TP+FP) | Of the examples we flagged, how many are really positive? | undefined / 0 |
| **F1** | Combines precision and recall into one number | 0 |
| **MCC** (Matthews correlation coefficient) | Uses all four cells; 0 means chance level | 0 |
| **Balanced accuracy** | The average of recall on each class | 0.5 |

**3. Metrics that don't depend on a threshold:**
- **Average precision (AUPRC)** is the best single number for rare positives. The random baseline equals the prevalence, so **0.02**. Always state that baseline next to your score.
- **AUROC** is fine to report, but it can look good (for example 0.95) while precision is still poor. That happens because even a small false-positive rate on the large negative class produces many false positives. Report it alongside AUPRC, not instead of it.

**4. Baselines.** Include the majority-class predictor and a simple model, such as logistic regression on obvious features. This shows how much your model actually adds.

**5. Uncertainty.** With only 2% positives, a test set of 1,000 has about 20 positives. One extra hit moves recall by 5 percentage points. Report the number of positives in the test set and give confidence intervals, for example by bootstrapping the test set.

**6. How you chose the threshold.** Choose it on validation data, not test data, and base it on the real cost of a missed positive compared with a false alarm. If the prevalence in real use differs from 2%, precision will change too, so say what prevalence you assumed.

## Also check
- **Splits.** If your data has related groups (the same patient, similar sequences, the same batch), split by group. Otherwise the test scores will be too high.
- **Resampling.** If you oversampled or used SMOTE, apply it only to the training folds. Evaluate on data with the true 2% prevalence.

**What to write in the paper:** something like "Recall 0.70 [95% CI …], precision 0.35, AUPRC 0.41 (baseline 0.02), MCC 0.48, with 40 positives in the test set," plus the confusion matrix. Report accuracy only as a side note, if at all.
````

## Answer without the skill (excerpt)

````text
**No, 98% accuracy tells you almost nothing here.** A classifier that predicts "negative" for every example also gets 98% accuracy, and it never finds a single positive. Your model could be doing exactly that, or barely better.

### Report these instead

**1. Confusion matrix (TP, FP, FN, TN).** Always show the raw counts. Every other metric comes from them, and they make "catches 0 of 200 positives" impossible to hide.

**2. Precision and recall for the positive class.**
- **Recall** (sensitivity) = TP / (TP + FN): what fraction of the real positives you catch.
- **Precision** = TP / (TP + FP): when you flag something, how often you're right.

At a 2% base rate, precision is usually the harder one. Even a fairly specific model can produce many false positives for each true positive.

**3. F1 score, or F-beta if errors don't cost the same.** F1 combines precision and recall into one number. Use F2 if missing a positive is worse (fraud, disease), or F0.5 if false alarms cost more.

**4. PR-AUC (average precision).** This measures performance across all thresholds. Prefer it to ROC-AUC on imbalanced data. ROC-AUC can look great (say 0.95) while precision is poor, because the huge number of true negatives hides the false positives. **The baseline PR-AUC for a random classifier equals the positive rate (0.02)**, so report the baseline next to your score.

**5. Baselines.** Show the majority-class result (98% accuracy, 0 recall) and a simple model like logistic regression, so readers can see what your model adds.

[... excerpt ends; the full answer is longer]
````

Agent model claude-opus-5-5, Claude Code 2.1.296. Excerpts are cut at the length shown; the model-judged and regular-expression checks for this skill are in [`evals/results/outcome.md`](../evals/results/outcome.md).
