---
name: machine-learning-biology
description: Frames, trains and evaluates machine-learning models on biological data without fooling yourself, covering problem definition, baselines, splits that respect homology and patients, class imbalance, metrics such as AUROC, average precision and MCC, leakage, calibration, and honest reporting. Use for "evaluate my classifier", "why is my accuracy so high", "split my protein data for cross-validation", "AUROC or precision-recall", "is my model leaking", "small data, many features", "write a model card". Use bioinformatics-review to audit the finished work, sequence-statistics for the underlying tests, and omics-data-analysis for the feature tables.
license: Apache-2.0
metadata:
  library: bioinformatics-skills
  version: "1.0"
---

# Machine learning for biology

## Purpose and activation

Make a model's reported performance mean what it appears to mean. Biological data are full of hidden
relatives: homologous proteins, patients with several samples, sequences copied from a common
source, batches that line up with the label. A model can score well by learning those, and fail
on the first new case. Activate when someone trains, compares or reports a predictive model.

## Required inputs

The task and what one example is (a sequence, a variant, a sample, a patient); the labels and where
they came from; the features; the size and class balance; the relatives that exist in the data
(families, patients, species, batches); the current split; and what the model will be used for.

## Workflow

1. **Define the task and the unit.** What is predicted, for what new case, with what information
   available at prediction time.
2. **Set baselines first:** the majority class, a simple model on obvious features, and a trivial
   feature such as sequence length or batch. A model that cannot beat them has learned nothing.
3. **Split by group.** Put whole groups on one side with `python3 scripts/mlmetrics.py split
   GROUPS --folds 5`, where the groups are families, patients, species or clusters.
4. **Look for near-duplicates across the split** with `mlmetrics.py similar TRAIN.fa TEST.fa`;
   move or drop pairs above your similarity limit.
5. **Fit everything inside the training fold:** feature selection, scaling, hyperparameter tuning.
   Any step that sees the test data makes the score optimistic.
6. **Pick metrics for the question** (`references/evaluation-guide.md`). With rare positives use
   average precision and MCC; accuracy alone misleads. `mlmetrics.py metrics TRUE PRED` and
   `auc TRUE SCORES` compute them.
7. **Quantify uncertainty,** for example by resampling groups, and compare models on the same folds.
8. **Validate on independent data** from another source, batch or time.
9. **Check the biology.** Which features matter; are they shortcuts such as batch markers or sequencing depth?
10. **Report** with a model card (`assets/templates/model-card.md`).

## Decision framework

| Situation | Choice |
|---|---|
| Balanced classes | Accuracy, AUROC |
| Rare positives | Average precision, MCC, recall at fixed precision; not accuracy |
| Related sequences or proteins | Group split by family or sequence cluster |
| Several samples per patient | Group split by patient |
| Batch correlated with label | Split by batch, or re-balance the design; do not trust a random split |
| Few samples, many features | Strong regularisation, simple model, nested validation |
| Many models tried | Count them; report the selection, and confirm on held-out data |
| Probabilities used for decisions | Check calibration, not only ranking |

## Implementation guidance

- AUROC is the chance that a random positive outranks a random negative, with ties counted half. It
  does not change under a monotone transform of the scores and ignores class balance.
- Average precision summarises the precision-recall curve; its chance level is the positive rate.
- MCC uses all four cells of the confusion matrix and is 0 for a classifier that predicts one class.
- The group splitter fills folds largest group first and is seeded; record the seed.
- Near-duplicate detection here uses shared k-mers (Jaccard similarity) and is a quick screen. For
  proteins use alignment-based clustering with an identity limit that matches your use (VERIFY).

## Failure and edge cases

- **Leakage:** features chosen on all the data; duplicates or relatives in both sides; preprocessing
  fitted before splitting; labels derived from features.
- **Optimistic cross-validation** after many rounds of tuning on the same folds.
- **Imbalance** hidden by accuracy: 95% accuracy from always saying no on a 95:5 set.
- **Shortcut learning:** the model reads batch, centre, depth or species instead of biology.
- **Distribution shift:** a new organism, tissue, platform or time period.
- **Label noise** from weak or inferred annotations used as truth.
- **p much larger than n,** where many models fit the training data perfectly.
- **Best-of-many reporting,** without the number of attempts.
- **Uncalibrated scores** read as probabilities.

## Validation

- `python3 scripts/mlmetrics.py --selftest` must pass.
- Hand check: scores 0.1, 0.4, 0.35, 0.8 with labels 0, 0, 1, 1 give AUROC 0.75 and average precision 0.8333.
- Hand check: TP 5, FP 1, TN 3, FN 1 gives MCC 14/24 = 0.583.
- Hand check: always predicting negative on 95 negatives and 5 positives gives accuracy 0.95, MCC 0
  and balanced accuracy 0.5.
- Falsifier: shuffle the labels and rerun the whole pipeline; performance must fall to chance.

## Expected output

The task and unit, baselines and their scores, the split and how groups were defined, the
near-duplicate check, the metrics with uncertainty, the validation on independent data, the
shortcut check, and a model card.

## Sources and confidence

- Ramsden, *Bioinformatics: An Introduction*, 2nd ed.: ch. 8 (pattern recognition, clustering, principal
  component and discriminant analysis, section titles only) and ch. 8.2 (pattern recognition)
- Metrics, group cross-validation, leakage: standard practice, with the metric formulas checked by
  hand-computed cases and a brute-force count of positive-negative pairs in the self-test; VERIFY
  conventions against your field
- Not covered: deep-learning architectures, protein language models, causal inference, fairness analysis
