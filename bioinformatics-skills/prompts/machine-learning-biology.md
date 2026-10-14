# `machine-learning-biology` prompts

Frame, train and evaluate predictive models on biological data without leakage, with metrics that
fit the question.

- **Give it:** the task and what one example is, the labels and their source, the features, the
  class balance, the relatives in the data (families, patients, batches), and the current split
- **Skill file:** [`skills/machine-learning-biology/SKILL.md`](../skills/machine-learning-biology/SKILL.md)
- **Reference and template:** [`evaluation-guide.md`](../skills/machine-learning-biology/references/evaluation-guide.md) and
  [`model-card.md`](../skills/machine-learning-biology/assets/templates/model-card.md)
- **After it:** [`bioinformatics-review`](bioinformatics-review.md)

## 1. Is high accuracy good

> My classifier gets 98% accuracy on a dataset where 2% of the examples are positive. Is that good? What should I report instead?

A good answer: not by itself, since always predicting the negative class also scores 98%; report
average precision, MCC and recall against the baseline, and the positive rate as the chance level.

## 2. Two ranking metrics

> Compute the AUROC and the average precision for the labels 0, 0, 1, 1 and the scores 0.1, 0.4, 0.35, 0.8, and explain why they differ.

A good answer: AUROC 0.75 and average precision 0.8333; AUROC counts all positive-negative pairs,
average precision weights the top of the ranking and depends on the positive rate.

## 3. Splitting related examples

> I have protein sequences from 300 families and want 5-fold cross-validation. How should I split them, and how do I check for leakage?

A good answer: split by family so no family appears on both sides, seed the split, and check for
near-duplicate sequences across the train and test files by shared k-mers or alignment identity.

## 4. A confusion matrix

> A classifier gives TP 5, FP 1, TN 3 and FN 1. Compute precision, recall, specificity and the Matthews correlation coefficient.

A good answer: precision 5/6, recall 5/6, specificity 3/4 and MCC 14/24 = 0.583.

## 5. Near-duplicates

> Check these two FASTA files, my training set and my test set, for near-duplicate sequences, and say what to do with the pairs you find: <give the paths>.

A good answer: pairs above a stated k-mer similarity listed with their indices, and a decision to
drop them or move them to the same side of the split.

## 6. A model card

> Write a model card for <describe the model, data and results>. Mark every field I have not given you as unknown.

A good answer: a filled card with the task, data, split, baselines, metrics with intervals,
independent validation, shortcut check and limits, and unknown fields marked as such.
