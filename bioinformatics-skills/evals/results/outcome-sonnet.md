# Outcome results: bioinformatics-skills

Engine direct. Agent model claude-sonnet-5-5, judge model claude-sonnet-5-5 (3 votes per verdict), 2 runs per case. Cost of this run, agent and judge at list price: 11.10 US dollars.

Each skill's starter prompt was run 2 times with the skills installed and 2 times with none, each in a fresh Claude Code project. Three kinds of check are reported separately: **facts** (regular expressions for the key facts in the answer), **rubric** (a model judges the answer against the prompt's own "a good answer" description) and **limits stated** (a model checks that the answer marks specific items as unverified or assumed and says what it did check). The judge is a model, not a person.

Measured 2026-10-14 with 2.1.296 (Claude Code).

## Overall

| Check | With the skills | No skills | Difference (95% interval) |
|---|---|---|---|
| Every expected fact present | 91% (80-97) | 89% (77-95) | +2 points (-11 to +15) |
| Rubric passed | 93% (82-98) | 83% (69-91) | +11 points (-3 to +25) |
| States its limits | 26% (16-40) | 28% (17-43) | -2 points (-20 to +16) |
| **Only prompts that do not presuppose the skill (22 skills)** | | | |
| Every expected fact present | 91% (79-96) | 91% (79-96) | +0 points (-13 to +13) |
| Rubric passed | 93% (82-98) | 86% (73-94) | +7 points (-7 to +21) |
| States its limits | 23% (13-37) | 25% (15-39) | -2 points (-20 to +15) |
| Expected skill invoked | 57% (42-70) | n/a | |
| Its script run (skills that ship one, and not denied) | 17% (7-34) | n/a | |

Some starter prompts ask for the skill's own table, checker or template (`literature-search-appraisal`). A run without the skill cannot supply those, so the difference on those prompts overstates what the skill adds; the second block leaves them out.

Cells are the share of runs, with a Wilson 95% interval. Runs: 46 with, 46 without (23 skills). Runs of the same skill are not independent, so the intervals are narrower than the true uncertainty.

Runs in which the permission mode denied at least one tool call: 0 of 46 with the skills, 0 of 46 without. Denied calls do not count as a script run.

Consistency (pass^2: the chance that all 2 runs of a skill pass): facts 0.87 with the skills, 0.87 without; rubric 0.91 with, 0.83 without.

Tokens and cost, mean per run: output tokens 1,710 with and 1,890 without; input tokens processed (including cached) 82,198 with and 52,232 without; cost 0.081 with and 0.055 without US dollars; total spent on these runs 6.27 (agent runs only, judge calls excluded).

## By skill

| Skill | Facts with | Facts without | Rubric with | Rubric without | Limits with | Limits without | Skill invoked | Script run |
|---|---|---|---|---|---|---|---|---|
| `bioinformatics-learning-path` | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 0/2 | 2/2 | n/a |
| `bioinformatics-programming` | 2/2 | 2/2 | 2/2 | 0/2 | 0/2 | 0/2 | 2/2 | 0/2 |
| `bioinformatics-review` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | n/a |
| `bioinformatics-workflow` | 2/2 | 2/2 | 2/2 | 0/2 | 0/2 | 0/2 | 2/2 | n/a |
| `biological-databases` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 2/2 | 1/2 |
| `data-governance-ethics` | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 0/2 | 2/2 | n/a |
| `experimental-design` | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 2/2 | 2/2 | 2/2 |
| `gene-finding-translation` | 1/2 | 0/2 | 2/2 | 2/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| `information-theory-sequences` | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| `literature-search-appraisal` | 2/2 | 1/2 | 2/2 | 0/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| `machine-learning-biology` | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 0/2 | 1/2 | 0/2 |
| `method-benchmarking` | 0/2 | 0/2 | 1/2 | 0/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| `ngs-pipelines` | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 0/2 | 1/2 | 0/2 |
| `omics-data-analysis` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 1/2 | 2/2 | n/a |
| `phylogenetics` | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| `protein-analysis` | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| `reproducible-research-code` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | n/a |
| `research-proposal-planning` | 1/2 | 2/2 | 2/2 | 2/2 | 0/2 | 1/2 | 0/2 | n/a |
| `research-writing-reporting` | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 1/2 | 2/2 | n/a |
| `sequence-alignment` | 2/2 | 2/2 | 0/2 | 2/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| `sequence-formats` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 0/2 |
| `sequence-statistics` | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 0/2 | 0/2 | 0/2 |
| `variants-population-genetics` | 2/2 | 2/2 | 2/2 | 2/2 | 0/2 | 0/2 | 2/2 | 0/2 |
