# Trigger results: bioinformatics-skills

Engine direct. Agent model claude-sonnet-5-5, judge model claude-sonnet-5-5 (3 votes per verdict), 2 runs per case. Trigger runs stop at the first skill call, so their cost is not tallied.

Each skill has a should-trigger prompt (written without naming the skill) and a near-miss prompt that shares vocabulary but belongs elsewhere; there are also unrelated prompts that should trigger nothing. Every prompt was run several times with the skills installed and the first skill the agent invoked was recorded from its tool calls. A should-trigger run passes when the expected skill was invoked; a near-miss run passes when the named skill was not.

Measured 2026-10-14 with 2.1.296 (Claude Code).

## Overall

| Measure | Value |
|---|---|
| Recall on should-trigger prompts | 76% (62-86) |
| Specificity on near-miss prompts | 100% (92-100) |
| Precision (invoked when it should be) | 100% (90-100) |
| Unrelated prompts that triggered a skill | 0/4 |

Recall 0.76, precision 1.00, specificity 1.00. Wilson 95% intervals; runs of one prompt are not independent.

## By skill

| Skill | Should-trigger runs hit | Near-miss runs that falsely triggered |
|---|---|---|
| `bioinformatics-learning-path` | 2/2 | 0/2 |
| `bioinformatics-programming` | 2/2 | 0/2 |
| `bioinformatics-review` | 1/2 | 0/2 |
| `bioinformatics-workflow` | 0/2 | 0/2 |
| `biological-databases` | 1/2 | 0/2 |
| `data-governance-ethics` | 2/2 | 0/2 |
| `experimental-design` | 2/2 | 0/2 |
| `gene-finding-translation` | 2/2 | 0/2 |
| `information-theory-sequences` | 2/2 | 0/2 |
| `literature-search-appraisal` | 1/2 | 0/2 |
| `machine-learning-biology` | 0/2 | 0/2 |
| `method-benchmarking` | 0/2 | 0/2 |
| `ngs-pipelines` | 2/2 | 0/2 |
| `omics-data-analysis` | 2/2 | 0/2 |
| `phylogenetics` | 2/2 | 0/2 |
| `protein-analysis` | 2/2 | 0/2 |
| `reproducible-research-code` | 2/2 | 0/2 |
| `research-proposal-planning` | 2/2 | 0/2 |
| `research-writing-reporting` | 1/2 | 0/2 |
| `sequence-alignment` | 2/2 | 0/2 |
| `sequence-formats` | 2/2 | 0/2 |
| `sequence-statistics` | 1/2 | 0/2 |
| `variants-population-genetics` | 2/2 | 0/2 |

## When the wrong skill fired

| Expected | Fired instead | Runs |
|---|---|---|
| `bioinformatics-workflow` | `omics-data-analysis` | 2 |
| `bioinformatics-review` | `machine-learning-biology` | 1 |
