# Outcome results: bioinformatics-skills

Engine direct. Agent model claude-opus-5-5, judge model claude-sonnet-5-5 (3 votes per verdict), 3 runs per case. Cost of this run, agent and judge at list price: 29.02 US dollars.

Each skill's starter prompt was run 3 times with the skills installed and 3 times with none, each in a fresh Claude Code project. Three kinds of check are reported separately: **facts** (regular expressions for the key facts in the answer), **rubric** (a model judges the answer against the prompt's own "a good answer" description) and **limits stated** (a model checks that the answer marks specific items as unverified or assumed and says what it did check). The judge is a model, not a person.

Measured 2026-10-14 with 2.1.296 (Claude Code).

## Overall

| Check | With the skills | No skills | Difference (95% interval) |
|---|---|---|---|
| Every expected fact present | 97% (90-99) | 90% (81-95) | +7 points (-1 to +17) |
| Rubric passed | 97% (90-99) | 86% (75-92) | +12 points (+2 to +22) |
| States its limits | 28% (18-39) | 22% (14-33) | +6 points (-9 to +20) |
| **Only prompts that do not presuppose the skill (22 skills)** | | | |
| Every expected fact present | 97% (90-99) | 92% (83-97) | +5 points (-4 to +14) |
| Rubric passed | 97% (90-99) | 89% (80-95) | +8 points (-2 to +18) |
| States its limits | 24% (16-36) | 18% (11-29) | +6 points (-8 to +20) |
| Expected skill invoked | 57% (45-68) | n/a | |
| Its script run (skills that ship one, and not denied) | 31% (20-46) | n/a | |

Some starter prompts ask for the skill's own table, checker or template (`literature-search-appraisal`). A run without the skill cannot supply those, so the difference on those prompts overstates what the skill adds; the second block leaves them out.

Cells are the share of runs, with a Wilson 95% interval. Runs: 69 with, 69 without (23 skills). Runs of the same skill are not independent, so the intervals are narrower than the true uncertainty.

Runs in which the permission mode denied at least one tool call: 0 of 69 with the skills, 0 of 69 without. Denied calls do not count as a script run.

Consistency (pass^3: the chance that all 3 runs of a skill pass): facts 0.96 with the skills, 0.83 without; rubric 0.91 with, 0.83 without.

Tokens and cost, mean per run: output tokens 2,458 with and 2,086 without; input tokens processed (including cached) 101,518 with and 54,658 without; cost 0.185 with and 0.113 without US dollars; total spent on these runs 20.58 (agent runs only, judge calls excluded).

## By skill

| Skill | Facts with | Facts without | Rubric with | Rubric without | Limits with | Limits without | Skill invoked | Script run |
|---|---|---|---|---|---|---|---|---|
| `bioinformatics-learning-path` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 3/3 | n/a |
| `bioinformatics-programming` | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 0/3 | 3/3 | 0/3 |
| `bioinformatics-review` | 3/3 | 3/3 | 2/3 | 2/3 | 3/3 | 3/3 | 3/3 | n/a |
| `bioinformatics-workflow` | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 0/3 | 3/3 | n/a |
| `biological-databases` | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 0/3 | 3/3 | 3/3 |
| `data-governance-ethics` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 3/3 | n/a |
| `experimental-design` | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 3/3 |
| `gene-finding-translation` | 3/3 | 1/3 | 3/3 | 3/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| `information-theory-sequences` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 2/3 | 2/3 |
| `literature-search-appraisal` | 3/3 | 1/3 | 3/3 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| `machine-learning-biology` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| `method-benchmarking` | 3/3 | 2/3 | 3/3 | 3/3 | 0/3 | 0/3 | 2/3 | 2/3 |
| `ngs-pipelines` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| `omics-data-analysis` | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | n/a |
| `phylogenetics` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| `protein-analysis` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| `reproducible-research-code` | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | n/a |
| `research-proposal-planning` | 1/3 | 1/3 | 3/3 | 3/3 | 1/3 | 0/3 | 0/3 | n/a |
| `research-writing-reporting` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 1/3 | 3/3 | n/a |
| `sequence-alignment` | 3/3 | 3/3 | 2/3 | 3/3 | 0/3 | 0/3 | 1/3 | 1/3 |
| `sequence-formats` | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 1/3 | 0/3 | 0/3 |
| `sequence-statistics` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| `variants-population-genetics` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 1/3 | 0/3 |
