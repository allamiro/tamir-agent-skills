# Trigger results: systems-biology-skills

Engine direct. Agent model claude-opus-5-5, judge model default (1 vote per verdict), 3 runs per case. Trigger runs stop at the first skill call, so their cost is not tallied.

Each skill has a should-trigger prompt (written without naming the skill) and a near-miss prompt that shares vocabulary but belongs elsewhere; there are also unrelated prompts that should trigger nothing. Every prompt was run several times with the skills installed and the first skill the agent invoked was recorded from its tool calls. A should-trigger run passes when the expected skill was invoked; a near-miss run passes when the named skill was not.

Measured 2026-10-14 with 2.1.296 (Claude Code).

## Overall

| Measure | Value |
|---|---|
| Recall on should-trigger prompts | 73% (61-82) |
| Specificity on near-miss prompts | 100% (94-100) |
| Precision (invoked when it should be) | 100% (92-100) |
| Unrelated prompts that triggered a skill | 0/6 |

Recall 0.73, precision 1.00, specificity 1.00. Wilson 95% intervals; runs of one prompt are not independent.

## By skill

| Skill | Should-trigger runs hit | Near-miss runs that falsely triggered |
|---|---|---|
| `control-systems-feedback` | 1/3 | 0/3 |
| `enzyme-kinetics` | 3/3 | 0/3 |
| `flux-balance-analysis` | 3/3 | 0/3 |
| `linear-algebra-networks` | 0/3 | 0/3 |
| `model-building-design` | 3/3 | 0/3 |
| `model-review` | 3/3 | 0/3 |
| `modeling-paper-writing` | 3/3 | 0/3 |
| `modeling-research-planning` | 3/3 | 0/3 |
| `multivariate-omics` | 3/3 | 0/3 |
| `network-analysis` | 3/3 | 0/3 |
| `ode-dynamics` | 0/3 | 0/3 |
| `parameter-estimation-model-selection` | 3/3 | 0/3 |
| `pharmacokinetic-modeling` | 1/3 | 0/3 |
| `quantitative-research-methods` | 3/3 | 0/3 |
| `quantities-units-balances` | 0/3 | 0/3 |
| `stochastic-discrete-models` | 3/3 | 0/3 |
| `stoichiometric-networks` | 0/3 | 0/3 |
| `systems-biology-learning-path` | 3/3 | 0/3 |
| `systems-biology-literature` | 3/3 | 0/3 |
| `systems-biology-programming` | 2/3 | 0/3 |
| `systems-biology-workflow` | 3/3 | 0/3 |
