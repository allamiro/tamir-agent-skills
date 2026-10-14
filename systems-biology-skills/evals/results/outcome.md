# Outcome results: systems-biology-skills

Engine direct. Agent model claude-opus-5-5, judge model claude-sonnet-5-5 (3 votes per verdict), 3 runs per case. Cost of this run, agent and judge at list price: 34.42 US dollars.

Each skill's starter prompt was run 3 times with the skills installed and 3 times with none, each in a fresh Claude Code project. Three kinds of check are reported separately: **facts** (regular expressions for the key facts in the answer), **rubric** (a model judges the answer against the prompt's own "a good answer" description) and **limits stated** (a model checks that the answer marks specific items as unverified or assumed and says what it did check). The judge is a model, not a person.

Measured 2026-10-14 with 2.1.296 (Claude Code).

## Overall

| Check | With the skills | No skills | Difference (95% interval) |
|---|---|---|---|
| Every expected fact present | 94% (85-98) | 78% (66-86) | +16 points (+4 to +28) |
| Rubric passed | 90% (81-96) | 60% (48-71) | +30 points (+15 to +44) |
| States its limits | 27% (18-39) | 21% (12-32) | +6 points (-9 to +21) |
| Expected skill invoked | 56% (43-67) | n/a | |
| Its script run (skills that ship one, and not denied) | 31% (19-46) | n/a | |

Cells are the share of runs, with a Wilson 95% interval. Runs: 63 with, 63 without (21 skills). Runs of the same skill are not independent, so the intervals are narrower than the true uncertainty.

Runs in which the permission mode denied at least one tool call: 0 of 63 with the skills, 0 of 63 without. Denied calls do not count as a script run.

Consistency (pass^3: the chance that all 3 runs of a skill pass): facts 0.81 with the skills, 0.71 without; rubric 0.81 with, 0.52 without.

Tokens and cost, mean per run: output tokens 2,765 with and 2,182 without; input tokens processed (including cached) 116,882 with and 54,324 without; cost 0.223 with and 0.119 without US dollars; total spent on these runs 21.50 (agent runs only, judge calls excluded).

## By skill

| Skill | Facts with | Facts without | Rubric with | Rubric without | Limits with | Limits without | Skill invoked | Script run |
|---|---|---|---|---|---|---|---|---|
| `control-systems-feedback` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| `enzyme-kinetics` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 3/3 | 3/3 |
| `flux-balance-analysis` | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 3/3 | 2/3 | 2/3 |
| `linear-algebra-networks` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| `model-building-design` | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 1/3 | 3/3 | n/a |
| `model-review` | 2/3 | 3/3 | 3/3 | 0/3 | 3/3 | 1/3 | 3/3 | n/a |
| `modeling-paper-writing` | 3/3 | 0/3 | 2/3 | 0/3 | 3/3 | 3/3 | 3/3 | n/a |
| `modeling-research-planning` | 2/3 | 0/3 | 2/3 | 0/3 | 2/3 | 0/3 | 3/3 | n/a |
| `multivariate-omics` | 3/3 | 3/3 | 3/3 | 1/3 | 1/3 | 0/3 | 3/3 | 3/3 |
| `network-analysis` | 3/3 | 2/3 | 3/3 | 2/3 | 1/3 | 0/3 | 3/3 | 3/3 |
| `ode-dynamics` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| `parameter-estimation-model-selection` | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 |
| `pharmacokinetic-modeling` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| `quantitative-research-methods` | 2/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| `quantities-units-balances` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| `stochastic-discrete-models` | 3/3 | 3/3 | 3/3 | 2/3 | 0/3 | 0/3 | 3/3 | 2/3 |
| `stoichiometric-networks` | 3/3 | 2/3 | 3/3 | 3/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| `systems-biology-learning-path` | 3/3 | 0/3 | 2/3 | 0/3 | 0/3 | 0/3 | 3/3 | n/a |
| `systems-biology-literature` | 2/3 | 0/3 | 0/3 | 0/3 | 3/3 | 2/3 | 3/3 | n/a |
| `systems-biology-programming` | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 0/3 | 0/3 |
| `systems-biology-workflow` | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 | 0/3 | 3/3 | n/a |

2 run(s) ended with an error such as a turn or time limit; they are graded on what they produced.
