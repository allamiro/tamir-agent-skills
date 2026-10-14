# Outcome results: egyptology-skills

Engine direct. Agent model claude-sonnet-5-5, judge model claude-sonnet-5-5 (3 votes per verdict), 2 runs per case. Cost of this run, agent and judge at list price: 4.04 US dollars.

Each skill's starter prompt was run 2 times with the skills installed and 2 times with none, each in a fresh Claude Code project. Three kinds of check are reported separately: **facts** (regular expressions for the key facts in the answer), **rubric** (a model judges the answer against the prompt's own "a good answer" description) and **limits stated** (a model checks that the answer marks specific items as unverified or assumed and says what it did check). The judge is a model, not a person.

Measured 2026-10-14 with 2.1.296 (Claude Code).

## Overall

| Check | With the skills | No skills | Difference (95% interval) |
|---|---|---|---|
| Every expected fact present | 94% (72-99) | 75% (51-90) | +19 points (-8 to +44) |
| Rubric passed | 88% (64-97) | 31% (14-56) | +56 points (+22 to +76) |
| States its limits | 100% (81-100) | 81% (57-93) | +19 points (-4 to +43) |
| **Only prompts that do not presuppose the skill (6 skills)** | | | |
| Every expected fact present | 92% (65-99) | 75% (47-91) | +17 points (-15 to +46) |
| Rubric passed | 92% (65-99) | 42% (19-68) | +50 points (+12 to +73) |
| States its limits | 100% (76-100) | 75% (47-91) | +25 points (-4 to +53) |
| Expected skill invoked | 100% (81-100) | n/a | |
| Its script run (skills that ship one, and not denied) | 88% (53-98) | n/a | |

Some starter prompts ask for the skill's own table, checker or template (`gardiner-sign-lookup`, `provenance-research-ethics`). A run without the skill cannot supply those, so the difference on those prompts overstates what the skill adds; the second block leaves them out.

Cells are the share of runs, with a Wilson 95% interval. Runs: 16 with, 16 without (8 skills). Runs of the same skill are not independent, so the intervals are narrower than the true uncertainty.

Runs in which the permission mode denied at least one tool call: 0 of 16 with the skills, 0 of 16 without. Denied calls do not count as a script run.

Consistency (pass^2: the chance that all 2 runs of a skill pass): facts 0.88 with the skills, 0.62 without; rubric 0.75 with, 0.25 without.

Tokens and cost, mean per run: output tokens 2,200 with and 1,740 without; input tokens processed (including cached) 136,528 with and 56,860 without; cost 0.086 with and 0.052 without US dollars; total spent on these runs 2.21 (agent runs only, judge calls excluded).

## By skill

| Skill | Facts with | Facts without | Rubric with | Rubric without | Limits with | Limits without | Skill invoked | Script run |
|---|---|---|---|---|---|---|---|---|
| `accuracy-review` | 2/2 | 1/2 | 2/2 | 0/2 | 2/2 | 2/2 | 2/2 | n/a |
| `edition-conventions` | 2/2 | 0/2 | 2/2 | 0/2 | 2/2 | 1/2 | 2/2 | 1/2 |
| `egyptology-literature` | 2/2 | 2/2 | 2/2 | 0/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| `gardiner-sign-lookup` | 2/2 | 2/2 | 2/2 | 0/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| `hieroglyph-app-builder` | 2/2 | 2/2 | 2/2 | 1/2 | 2/2 | 2/2 | 2/2 | n/a |
| `provenance-research-ethics` | 2/2 | 1/2 | 1/2 | 0/2 | 2/2 | 2/2 | 2/2 | 2/2 |
| `text-annotation` | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | n/a |
| `transliteration` | 1/2 | 2/2 | 1/2 | 2/2 | 2/2 | 0/2 | 2/2 | n/a |
