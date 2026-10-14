# Trigger results: bioinformatics-skills

Engine direct. Agent model claude-opus-5-5, judge model default (1 vote per verdict), 3 runs per case. Trigger runs stop at the first skill call, so their cost is not tallied.

Each skill has a should-trigger prompt (written without naming the skill) and a near-miss prompt that shares vocabulary but belongs elsewhere; there are also unrelated prompts that should trigger nothing. Every prompt was run several times with the skills installed and the first skill the agent invoked was recorded from its tool calls. A should-trigger run passes when the expected skill was invoked; a near-miss run passes when the named skill was not.

Measured 2026-10-14 with 2.1.296 (Claude Code).

## Overall

| Measure | Value |
|---|---|
| Recall on should-trigger prompts | 80% (69-88) |
| Specificity on near-miss prompts | 100% (95-100) |
| Precision (invoked when it should be) | 100% (93-100) |
| Unrelated prompts that triggered a skill | 0/6 |

Recall 0.80, precision 1.00, specificity 1.00. Wilson 95% intervals; runs of one prompt are not independent.

## By skill

| Skill | Should-trigger runs hit | Near-miss runs that falsely triggered |
|---|---|---|
| `bioinformatics-learning-path` | 3/3 | 0/3 |
| `bioinformatics-programming` | 3/3 | 0/3 |
| `bioinformatics-review` | 0/3 | 0/3 |
| `bioinformatics-workflow` | 2/3 | 0/3 |
| `biological-databases` | 3/3 | 0/3 |
| `data-governance-ethics` | 3/3 | 0/3 |
| `experimental-design` | 3/3 | 0/3 |
| `gene-finding-translation` | 0/3 | 0/3 |
| `information-theory-sequences` | 2/3 | 0/3 |
| `literature-search-appraisal` | 3/3 | 0/3 |
| `machine-learning-biology` | 1/3 | 0/3 |
| `method-benchmarking` | 2/3 | 0/3 |
| `ngs-pipelines` | 3/3 | 0/3 |
| `omics-data-analysis` | 3/3 | 0/3 |
| `phylogenetics` | 3/3 | 0/3 |
| `protein-analysis` | 3/3 | 0/3 |
| `reproducible-research-code` | 3/3 | 0/3 |
| `research-proposal-planning` | 3/3 | 0/3 |
| `research-writing-reporting` | 3/3 | 0/3 |
| `sequence-alignment` | 3/3 | 0/3 |
| `sequence-formats` | 2/3 | 0/3 |
| `sequence-statistics` | 1/3 | 0/3 |
| `variants-population-genetics` | 3/3 | 0/3 |
