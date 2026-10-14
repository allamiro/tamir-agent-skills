# Model card: <model name>

Author: <name>   Date: <date>   Code version: <commit>

## Task

Predicts: <what>   For: <what a new example is>   Input available at prediction time: <list>

## Data

| Item | Value |
|---|---|
| Source and accession, with version | |
| Examples, positives, negatives | |
| Where labels came from | |
| Known relatives in the data (families, patients, batches) | |

## Split

Method: <how groups were defined and kept together>   Seed: <value>   Near-duplicate check: <method, limit, pairs found and handled>

## Baselines

| Baseline | Score |
|---|---|
| Majority class | |
| Simple model | |
| Trivial feature (length, batch, depth) | |

## Results

| Metric | Value | Interval | Method for the interval |
|---|---|---|---|
| AUROC | | | |
| Average precision (chance = positive rate) | | | |
| MCC | | | |

Models, features and settings tried: <number>   Selected on: <data>

## Independent validation

Data: <source, batch, period>   Result: <metrics>

## Shortcut and biology check

<Which features matter; whether any encode batch, centre, depth or species; what was done about it.>

## Intended use and limits

<Where the model should and should not be used; known failure cases; calibration.>
