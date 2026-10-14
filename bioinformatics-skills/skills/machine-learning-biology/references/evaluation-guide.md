# Evaluation guide

Standard practice; VERIFY against your field's conventions.

## Confusion matrix and the metrics built on it

|  | Predicted positive | Predicted negative |
|---|---|---|
| Actually positive | TP | FN |
| Actually negative | FP | TN |

| Metric | Formula | Notes |
|---|---|---|
| Accuracy | (TP + TN) / all | Misleading when classes are unbalanced |
| Recall (sensitivity) | TP / (TP + FN) | Share of positives found |
| Specificity | TN / (TN + FP) | Share of negatives correctly rejected |
| Precision | TP / (TP + FP) | Share of calls that are right |
| F1 | 2 P R / (P + R) | Ignores true negatives |
| Balanced accuracy | (recall + specificity) / 2 | 0.5 for a trivial classifier |
| MCC | (TP TN - FP FN) / sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN)) | -1 to 1; 0 if a margin is empty |

Worked: TP 5, FP 1, TN 3, FN 1 gives MCC (15 - 1) / sqrt(6 x 6 x 4 x 4) = 14/24 = 0.583.

## Ranking metrics

| Metric | Meaning | Chance level |
|---|---|---|
| AUROC | Probability that a random positive scores above a random negative (ties count half) | 0.5 |
| Average precision | Area under the precision-recall curve, as recall gained times precision at each threshold | The positive rate |

AUROC can look good while precision is poor when positives are rare, because it counts the many
negatives. Report both when classes are unbalanced. The standard example (labels 0, 0, 1, 1; scores
0.1, 0.4, 0.35, 0.8) gives AUROC 0.75 and average precision 0.8333.

## Splitting

| Data have | Split by |
|---|---|
| Protein or gene families | Family or sequence cluster at a stated identity |
| Several samples per person or animal | Individual |
| Species structure | Species or clade, if the model must work on new species |
| Batches or sites | Batch or site, if it must work on a new one |
| Time order | Time, training on the past and testing on the future |

A random split is correct only when examples are exchangeable, which biological data seldom are.

## Leakage checklist

1. Same example, or a near-copy, on both sides of the split.
2. Features selected, scaled or imputed using all the data.
3. Hyperparameters tuned on the test set.
4. A feature that encodes the label (an identifier, a date, a batch tag, depth).
5. Labels transferred by similarity from a training example to its test relative.
6. Duplicates created by augmentation before splitting.

## Uncertainty and comparison

Resample groups, not examples, to get an interval. Compare models on identical folds and report
the difference with its interval. Report how many models, features or settings were tried.

## Calibration

A score of 0.8 should be right about 80% of the time if it is used as a probability. Check with a
reliability plot or a binned comparison on held-out data.

## Independent validation

Hold out data from a different source, centre, batch or period. A drop in performance on such data is
the honest estimate of performance in use.
