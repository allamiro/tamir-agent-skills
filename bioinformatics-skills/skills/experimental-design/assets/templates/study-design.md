# Study design: <short title>

Author: <name>   Date: <date>   Status: fixed before data collection

## Question and primary comparison

<The comparison, its direction, and the measurement it is made on.>

## Units

| Item | Value |
|---|---|
| Independent unit (one sample is) | |
| Biological replicates per group | |
| Technical replicates, if any, and what they check | |
| Groups | |

## Effect size and variability

| Item | Value | Source |
|---|---|---|
| Expected difference | | |
| Standard deviation | | |
| Standardized effect d | | |

## Sample size

Alpha: <value>   Number of tests: <n>   Power: <value>   Samples per group: <n>   Margin for dropout: <n>

Calculation: `python3 scripts/design.py n --d <d> --tests <n>`

## Controls

- Positive: <describe>
- Negative: <describe>
- Blank or mock: <describe>
- Reference sample in every batch: <describe>

## Layout

Batches: <number and what defines them>   Seed: <value>   Sheet: <file>

Confounding check: `python3 scripts/design.py confound <sheet> --group <col> --batch <col>`   Result: <Cramer's V>

## Decided in advance

- Exclusion rules: <list>
- Correction for many tests: <method and threshold>
- Stopping rule: <rule>
- Analysis to be run: <short description>

## Pilot

<What the pilot checked and what changed as a result.>
